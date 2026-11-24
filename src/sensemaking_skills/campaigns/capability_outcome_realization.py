"""Append-only, evidence-linked realization assessment for a bound outcome.

The original ``capability_outcome`` binding remains the authority for the
selected commitment and its original conditions. Assessments are agent-authored
per-condition evidence states appended with a lifecycle transition. They do
not compute an overall completion score, readiness verdict or next action.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from sensemaking_skills.campaign_semantics import canonicalize
from sensemaking_skills.semantic_architecture.worktree_context import guarded_git_text

from .capability_outcome import CAPABILITY_OUTCOME_EXTENSION
from .errors import CampaignTransactionError

CAPABILITY_OUTCOME_REALIZATION_EXTENSION = "capability_outcome_realization"
CAPABILITY_OUTCOME_REALIZATION_SCHEMA_VERSION = "1"

STATUS_EVIDENCE_PRESENT = "EVIDENCE_PRESENT"
STATUS_PARTIAL_EVIDENCE = "PARTIAL_EVIDENCE"
STATUS_NO_EVIDENCE = "NO_EVIDENCE"
STATUS_CONTRADICTING_EVIDENCE = "CONTRADICTING_EVIDENCE"
STATUS_NOT_ASSESSED = "NOT_ASSESSED"
CONDITION_STATUSES = frozenset({
    STATUS_EVIDENCE_PRESENT,
    STATUS_PARTIAL_EVIDENCE,
    STATUS_NO_EVIDENCE,
    STATUS_CONTRADICTING_EVIDENCE,
    STATUS_NOT_ASSESSED,
})
_EVIDENCE_REQUIRED = frozenset({
    STATUS_EVIDENCE_PRESENT,
    STATUS_PARTIAL_EVIDENCE,
    STATUS_CONTRADICTING_EVIDENCE,
})

_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_MAX_BASIS = 2400
_MAX_REFS = 20
_EXPLICIT_LIMIT = (
    "Agent-authored per-condition evidence states. Evidence references are "
    "pointers, not implementation verification; the assessment is not a "
    "completion score, readiness verdict, semantic truth or action authority."
)
_PROJECTION_LIMIT = (
    "Projects the latest agent-authored condition assessment alongside the "
    "immutable binding. It does not decide completion, rank remaining work or "
    "authorize action."
)


def _text(value: Any, *, field: str, maximum: int = _MAX_BASIS) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise CampaignTransactionError(
            f"{field} must be a non-empty string of at most {maximum} characters"
        )
    return value.strip()


def _safe_path(raw: str) -> str:
    if (
        not isinstance(raw, str)
        or not raw
        or "\\" in raw
        or raw.startswith("/")
        or ":" in raw
        or any(part in ("", ".", "..") for part in raw.split("/"))
    ):
        raise CampaignTransactionError(
            "file evidence must be a safe repository-relative path"
        )
    return raw


def _git(root: Path, *args: str) -> str:
    try:
        return guarded_git_text(root, *args).strip()
    except (ValueError, OSError) as exc:
        raise CampaignTransactionError(f"safe Git source check failed: {exc}") from exc


def _repository_root(repo: str | Path) -> Path:
    try:
        root = Path(repo).expanduser().resolve(strict=True)
    except OSError as exc:
        raise CampaignTransactionError(f"repository checkout is unavailable: {exc}") from exc
    if not root.is_dir():
        raise CampaignTransactionError("repository checkout must be a directory")
    top = Path(_git(root, "rev-parse", "--show-toplevel")).resolve()
    return top


def _require_commit(root: Path, value: str, *, field: str) -> str:
    if not isinstance(value, str) or not _COMMIT.fullmatch(value):
        raise CampaignTransactionError(f"{field} must be an exact 40-character Git commit")
    resolved = _git(root, "rev-parse", "--verify", "--quiet", f"{value}^{{commit}}")
    if resolved != value:
        raise CampaignTransactionError(f"{field} is not an exact local Git commit: {value}")
    return value


def _clean_refs(raw: Any, *, root: Path, source_revision: str) -> list[str]:
    if raw is None:
        values: list[str] = []
    elif isinstance(raw, list):
        values = raw
    else:
        raise CampaignTransactionError("evidence_refs must be a list")
    if len(values) > _MAX_REFS:
        raise CampaignTransactionError(f"evidence_refs accepts at most {_MAX_REFS} entries")
    cleaned: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value:
            raise CampaignTransactionError("evidence_refs must contain non-empty strings")
        if value.startswith("file:"):
            path = _safe_path(value[5:])
            listing = _git(
                root, "ls-tree", "-r", "-z", "--name-only", source_revision, "--", path
            ).split(chr(0))
            if path not in listing:
                raise CampaignTransactionError(
                    f"file evidence is not tracked at the source revision: {path}"
                )
        elif value.startswith("commit:"):
            _require_commit(root, value[7:], field="commit evidence")
        else:
            raise CampaignTransactionError(
                "evidence_refs entries must start with file: or commit:"
            )
        if value not in cleaned:
            cleaned.append(value)
    return cleaned


def build_realization_assessment(
    *,
    assessment_id: str,
    transition_id: str,
    binding: Mapping[str, Any],
    prior_assessments: Sequence[Mapping[str, Any]],
    authored: Mapping[str, Any],
    repo: str | Path,
    target_repository_id: str | None = None,
) -> dict[str, Any]:
    """Validate one agent-authored assessment and return its durable record."""

    if not isinstance(authored, Mapping):
        raise CampaignTransactionError("assessment must be a JSON object")
    unknown = set(authored) - {"possibility_id", "source_revision", "conditions"}
    if unknown:
        raise CampaignTransactionError(f"unknown assessment fields: {sorted(unknown)}")

    possibility_id = _text(
        binding.get("possibility_id"), field="binding.possibility_id", maximum=160
    )
    if _text(authored.get("possibility_id"), field="assessment.possibility_id", maximum=160) != possibility_id:
        raise CampaignTransactionError(
            "assessment.possibility_id must match the bound capability outcome"
        )
    root = _repository_root(repo)
    source_revision = _require_commit(
        root,
        _text(authored.get("source_revision"), field="assessment.source_revision", maximum=40),
        field="assessment.source_revision",
    )
    if target_repository_id is not None:
        from .target_snapshot import repository_identity

        try:
            _, repository_id = repository_identity(root)
        except (OSError, UnicodeError) as exc:
            raise CampaignTransactionError(f"repository identity check failed: {exc}") from exc
        if repository_id != target_repository_id:
            raise CampaignTransactionError(
                "the assessment repository is not the Campaign's bound target"
            )

    original_conditions = binding.get("remaining_conditions")
    if not isinstance(original_conditions, list) or not all(
        isinstance(item, str) and item.strip() for item in original_conditions
    ):
        raise CampaignTransactionError(
            "bound capability outcome has no valid remaining_conditions"
        )
    condition_count = len(original_conditions)
    raw_conditions = authored.get("conditions")
    if not isinstance(raw_conditions, list):
        raise CampaignTransactionError("assessment.conditions must be a list")
    by_index: dict[int, Mapping[str, Any]] = {}
    for item in raw_conditions:
        if not isinstance(item, Mapping):
            raise CampaignTransactionError("each condition assessment must be an object")
        unknown = set(item) - {"condition_index", "status", "evidence_refs", "basis"}
        if unknown:
            raise CampaignTransactionError(
                f"unknown condition assessment fields: {sorted(unknown)}"
            )
        index = item.get("condition_index")
        if isinstance(index, bool) or not isinstance(index, int) or not 1 <= index <= condition_count:
            raise CampaignTransactionError(
                f"condition_index must be an integer from 1 to {condition_count}"
            )
        if index in by_index:
            raise CampaignTransactionError(f"duplicate condition_index: {index}")
        status = item.get("status")
        if status not in CONDITION_STATUSES:
            raise CampaignTransactionError(
                f"condition {index} status must be one of {sorted(CONDITION_STATUSES)}"
            )
        basis = _text(item.get("basis"), field=f"condition {index} basis")
        evidence = _clean_refs(
            item.get("evidence_refs", []), root=root, source_revision=source_revision
        )
        if status in _EVIDENCE_REQUIRED and not evidence:
            raise CampaignTransactionError(
                f"condition {index} with {status} requires at least one evidence ref"
            )
        by_index[index] = {
            "condition_index": index,
            "condition": original_conditions[index - 1],
            "status": status,
            "evidence_refs": evidence,
            "basis": basis,
        }
    missing = sorted(set(range(1, condition_count + 1)) - set(by_index))
    if missing:
        raise CampaignTransactionError(
            "assessment must cover every original condition exactly once; missing "
            + ", ".join(str(item) for item in missing)
        )

    prior_id: str | None = None
    for item in prior_assessments:
        if isinstance(item, Mapping) and isinstance(item.get("assessment_id"), str):
            prior_id = item["assessment_id"]
    record = {
        "schema_version": CAPABILITY_OUTCOME_REALIZATION_SCHEMA_VERSION,
        "assessment_id": _text(assessment_id, field="assessment_id", maximum=80),
        "transition_id": _text(transition_id, field="transition_id", maximum=80),
        "possibility_id": possibility_id,
        "source_revision": source_revision,
        "supersedes": prior_id,
        "conditions": [by_index[index] for index in range(1, condition_count + 1)],
        "explicit_limit": _EXPLICIT_LIMIT,
        "semantic_truth_established": False,
        "action_authorized": False,
    }
    return record


def _container(state: Any) -> Mapping[str, Any] | None:
    extensions = getattr(state, "extensions", None)
    if not isinstance(extensions, Mapping):
        return None
    value = extensions.get(CAPABILITY_OUTCOME_REALIZATION_EXTENSION)
    return value if isinstance(value, Mapping) else None


def _assessments(state: Any) -> list[Mapping[str, Any]]:
    container = _container(state)
    if container is None:
        return []
    values = container.get("assessments")
    if not isinstance(values, list):
        return []
    return [item for item in values if isinstance(item, Mapping)]


def latest_realization_assessment(state: Any) -> dict[str, Any] | None:
    values = _assessments(state)
    if not values:
        return None
    return canonicalize(dict(values[-1]))


def realization_assessment_history(state: Any) -> list[dict[str, Any]]:
    return [canonicalize(dict(item)) for item in _assessments(state)]


def realization_assessment_projection(state: Any) -> dict[str, Any] | None:
    latest = latest_realization_assessment(state)
    if latest is None:
        return None
    container = _container(state) or {}
    binding = getattr(state, "extensions", {}).get(CAPABILITY_OUTCOME_EXTENSION, {})
    binding = binding if isinstance(binding, Mapping) else {}
    conditions = [
        item for item in latest.get("conditions", []) if isinstance(item, Mapping)
    ]
    statuses = Counter(item.get("status") for item in conditions)
    return {
        "schema_version": CAPABILITY_OUTCOME_REALIZATION_SCHEMA_VERSION,
        "assessment_count": len(_assessments(state)),
        "latest": latest,
        "condition_status_counts": dict(sorted(statuses.items())),
        "binding_realization": binding.get("realization"),
        "staleness": "NOT_COMPARED",
        "semantic_selection_performed": False,
        "explicit_limit": _PROJECTION_LIMIT,
        "container_possibility_id": container.get("possibility_id"),
    }


def realization_assessment_summary(state: Any) -> dict[str, Any] | None:
    latest = latest_realization_assessment(state)
    if latest is None:
        return None
    projection = realization_assessment_projection(state) or {}
    return {
        "assessment_id": latest.get("assessment_id"),
        "source_revision": latest.get("source_revision"),
        "supersedes": latest.get("supersedes"),
        "assessment_count": projection.get("assessment_count", 0),
        "condition_status_counts": projection.get("condition_status_counts", {}),
        "binding_realization": projection.get("binding_realization"),
        "staleness": "NOT_COMPARED",
        "semantic_selection_performed": False,
    }
