"""Read-only continuity inputs for the existing handoff.

Only explicitly selected receipts are opened. Inventories describe working-tree
paths, not a committed snapshot, relevance, authority or semantic adequacy.
Detached proposals and historical JSON records are path hints only: neither
review nor pending work is inferred. The canonical validator owns receipt
validity. No implicit history-wide content scan.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

_MAX_PATHS = 40
_MAX_SELECTED = 5
_MAX_BYTES = 256 * 1024
_MAX_ITEMS = 12
_RECEIPT_NAME = re.compile(r"\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]{0,63}\.session\.yaml")
_RECEIPT_DIR = ".sensemaking/receipts"
_GOVERNING = (
    ".sensemaking/intent.md", ".sensemaking/invariants.md",
    "artifacts/strategic_repository_analysis.md",
    "artifacts/strategic_reconciliation.md",
    "artifacts/sensemaking_decision.md",
    "artifacts/owner_decision_capsule.md",
    "docs/product-strategy.md", "STATUS.md",
)


def _contained(target: Path, path: Path) -> bool:
    """Exclude symlink aliases and external resolution, including parent paths."""
    try:
        return path.resolve() == path and path.is_relative_to(target) and not path.is_symlink()
    except (OSError, RuntimeError):
        return False


def _paths(
    target: Path, directory: str, suffixes: tuple[str, ...], *,
    include_tail: bool = False,
) -> dict[str, Any]:
    folder = target / directory
    if not _contained(target, folder) or not folder.is_dir():
        return {"paths": [], "total": 0, "truncated": False,
                "directory_status": "ABSENT_OR_NOT_INSPECTABLE"}
    try:
        paths = sorted(
            p.relative_to(target).as_posix()
            for p in folder.iterdir()
            if p.name.endswith(suffixes) and _contained(target, p) and p.is_file()
        )
    except OSError:
        return {"paths": [], "total": 0, "truncated": False,
                "directory_status": "NOT_INSPECTABLE"}
    truncated = len(paths) > _MAX_PATHS
    visible = paths[:_MAX_PATHS]
    if include_tail and truncated:
        # Date-prefixed receipt names otherwise hide later-named records once
        # the prefix fills. Keep both ends within the original path budget.
        # Filename order is neither update chronology nor semantic relevance.
        prefix_count = _MAX_PATHS // 2
        suffix_count = _MAX_PATHS - prefix_count
        visible = paths[:prefix_count] + paths[-suffix_count:]
    return {
        "paths": visible, "total": len(paths),
        "truncated": truncated, "directory_status": "OBSERVED",
        **({
            "path_selection": "LEXICOGRAPHIC_ENDS" if truncated else "ALL",
            "omitted_count": len(paths) - len(visible),
        } if include_tail else {}),
    }


def continuity_inventory(target: Path) -> dict[str, Any]:
    return {
        "basis": "WORKING_TREE_PATHS_ONLY",
        "knowledge_files": _paths(target, ".sensemaking/knowledge", (".json",)),
        "detached_proposal_files": _paths(target, ".sensemaking/proposals", (".json",)),
        "historical_json_records": _paths(target, "artifacts/history", (".json",)),
        "speculative_record_review_state": "NOT_ASSESSED",
        "receipt_files": _paths(
            target, _RECEIPT_DIR, (".session.yaml", ".query.yaml"), include_tail=True,
        ),
        "strategic_history": _paths(target, "artifacts/history", (".md",)),
        "governing_paths": [
            name for name in _GOVERNING
            if _contained(target, target / name) and (target / name).is_file()
        ],
        "semantic_adequacy_established": False,
        "relevance_established": False,
    }


def _canonical_validation(target: Path, path: Path) -> tuple[str, dict[str, Any]]:
    # Same trusted runtime resolution and canonical router as CLI validate.
    from .campaigns import ArtifactAdmissionService, ArtifactValidatorError

    try:
        root, validator = ArtifactAdmissionService._require_framework_root(None)
        completed = subprocess.run(
            [sys.executable, str(validator), str(path), "--repo-root", str(root),
             "--target-repo", str(target)],
            cwd=root, capture_output=True, text=True, timeout=120, check=False,
        )
        result = json.loads(completed.stdout)
        if not isinstance(result, dict) or not isinstance(result.get("valid"), bool):
            return "VALIDATOR_UNAVAILABLE", {}
        errors = result.get("errors")
        if not isinstance(errors, list):
            return "VALIDATOR_UNAVAILABLE", {}
        if any(isinstance(e, dict) and str(e.get("error_id", "")).endswith(
                ".validator.execution_error") for e in errors):
            return "VALIDATOR_UNAVAILABLE", {}
        if result["valid"]:
            if completed.returncode != 0:
                return "VALIDATOR_UNAVAILABLE", {}
            if result.get("artifact_id") != "sensemaking_session_receipt":
                return "NOT_SESSION_RECEIPT", result
            return "VALID", result
        return "INVALID", result
    except (ArtifactValidatorError, OSError, ValueError, subprocess.SubprocessError):
        return "VALIDATOR_UNAVAILABLE", {}


def _scalar(value: Any) -> Any:
    return value if value is None or isinstance(value, (str, bool, int)) else None


def _project(data: dict[str, Any]) -> dict[str, Any]:
    """Explicit bounded historical fields; omit unknown data and authority."""
    projection = {key: _scalar(data.get(key)) for key in (
        "session_ref", "state", "target_repository", "claim_ceiling",
    )}
    for key, fields in (
        ("source_identity", ("start_ref", "end_ref")),
        ("skill_identity", ("load_mode", "sensemaking_source_ref")),
        ("goal", ("statement", "source", "source_ref")),
        ("stop", ("disposition", "reason")),
        ("next", ("warranted_responsibility",)),
        ("continuity", ("resumes", "campaign_ref")),
    ):
        item = data.get(key) or {}
        projection[key] = {field: _scalar(item.get(field)) for field in fields}
    blocked = (data.get("next") or {}).get("blocked_on") or []
    projection["next"]["blocked_on"] = [_scalar(item) for item in blocked[:_MAX_ITEMS]]
    projection["next"]["blocked_on_omitted"] = max(0, len(blocked) - _MAX_ITEMS)
    for key, fields in (
        ("responsibilities", ("id", "responsibility", "capability", "status", "reason")),
        ("findings", ("id", "statement", "epistemic_status", "disposition")),
        ("open_questions", ("id", "question", "source", "blocking", "durable_ref")),
    ):
        items = data.get(key) or []
        projection[key] = [
            {field: _scalar(item.get(field)) for field in fields}
            for item in items[:_MAX_ITEMS]
        ]
        projection[key + "_omitted"] = max(0, len(items) - _MAX_ITEMS)
    for index, responsibility in enumerate((data.get("responsibilities") or [])[:_MAX_ITEMS]):
        refs = responsibility.get("artifact_refs") or []
        projection["responsibilities"][index]["artifact_refs"] = [
            _scalar(ref) for ref in refs[:_MAX_ITEMS]
        ]
        projection["responsibilities"][index]["artifact_refs_omitted"] = max(0, len(refs) - _MAX_ITEMS)
        # These are authored historical results, not checks performed by handoff.
        validation = responsibility.get("validation") or []
        projection["responsibilities"][index]["validation"] = [
            {field: _scalar(entry.get(field)) for field in ("command", "result")}
            for entry in validation[:_MAX_ITEMS]
        ]
        projection["responsibilities"][index]["validation_omitted"] = max(
            0, len(validation) - _MAX_ITEMS,
        )
    for index, finding in enumerate((data.get("findings") or [])[:_MAX_ITEMS]):
        refs = finding.get("evidence_refs") or []
        projection["findings"][index]["evidence_refs"] = [_scalar(ref) for ref in refs[:_MAX_ITEMS]]
        projection["findings"][index]["evidence_refs_omitted"] = max(0, len(refs) - _MAX_ITEMS)
    return projection


def selected_receipts(target: Path, names: tuple[str, ...]) -> list[dict[str, Any]]:
    if len(names) > _MAX_SELECTED or len(set(names)) != len(names):
        raise ValueError("select at most five distinct session receipts")
    records = []
    for name in names:
        filename = name.removeprefix(_RECEIPT_DIR + "/")
        if name == filename or not _RECEIPT_NAME.fullmatch(filename):
            raise ValueError("resume-from must name .sensemaking/receipts/<session>.session.yaml")
        path = target / _RECEIPT_DIR / filename
        if not _contained(target, path) or not path.is_file():
            raise ValueError(f"selected receipt is not a regular contained file: {name}")
        if path.stat().st_size > _MAX_BYTES:
            raise ValueError(f"selected receipt exceeds bounded handoff size: {name}")
        raw = path.read_bytes()
        if len(raw) > _MAX_BYTES:
            raise ValueError(f"selected receipt exceeds bounded handoff size: {name}")
        digest = hashlib.sha256(raw).hexdigest()
        status, result = _canonical_validation(target, path)
        # Refuse a projection if before/after bytes differ. Not a snapshot guarantee.
        if (not _contained(target, path) or not path.is_file()
                or path.stat().st_size > _MAX_BYTES
                or hashlib.sha256(path.read_bytes()).hexdigest() != digest):
            status, result = "CHANGED_DURING_READ", {}
        errors = result.get("errors", [])
        record: dict[str, Any] = {
            "path": name, "sha256": digest, "validation": status,
            "validation_basis": "CURRENT_TARGET_WORKING_TREE",
            "validator": result.get("validator"),
            "errors": [
                {"error_id": e.get("error_id"), "field": e.get("field")}
                for e in errors[:_MAX_ITEMS] if isinstance(e, dict)
            ],
            "errors_omitted": max(0, len(errors) - _MAX_ITEMS),
            "historical_projection": None,
            "projection_status": "NOT_PROJECTED",
            "relevance_established": False,
            "action_authorized": False,
        }
        if status == "VALID":
            try:
                data = yaml.safe_load(raw.decode("utf-8"))
                if isinstance(data, dict) and data.get("artifact_id") == "sensemaking_session_receipt":
                    record["historical_projection"] = _project(data)
                    record["projection_status"] = "AVAILABLE"
            except (UnicodeError, yaml.YAMLError, TypeError, ValueError, AttributeError):
                pass  # Original remains readable; no projection is claimed.
        records.append(record)
    return records
