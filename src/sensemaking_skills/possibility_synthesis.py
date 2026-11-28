"""Optional agent-authored synthesis of a new product possibility.

The active agent owns the synthesis: it names a new candidate, states what it
combines, identifies the goals and existing possibilities it derives from, and
records its dimensions, assumptions, contradictions, evidence and claim
ceiling. This module only validates source/revision provenance and materializes
an unreviewed knowledge proposal. It does not generate candidates, rank them,
select a direction, claim realization or authorize work.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Mapping

from .semantic_architecture.knowledge import read_authored_claim, read_authored_relation
from .semantic_architecture.worktree_context import guarded_git_text

_SLUG = re.compile(r"[a-z0-9][a-z0-9-]{2,70}\Z")
_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z")
_DIMENSIONS = ("alignment", "ambition", "horizon", "realization")
_ASSUMPTION_KINDS = frozenset(
    {"constraint", "hypothesis", "observation", "decision", "invariant"}
)
_CONTRADICTION_KINDS = frozenset(
    {"opportunity", "hypothesis", "decision", "alternative", "constraint"}
)
_MAX_TEXT = 2400
_MAX_REFS = 8
_VALUE_PREDICTION_FIELDS = (
    "beneficiary", "criterion", "comparison_baseline", "expected_observation",
    "would_change_decision_if", "cost_and_downside",
)


def _string(
    data: Mapping[str, Any], key: str, *, required: bool = True, maximum: int = _MAX_TEXT
) -> str:
    value = data.get(key, "")
    if (
        not isinstance(value, str)
        or len(value) > maximum
        or (required and not value.strip())
    ):
        raise ValueError(
            f"episode.{key} must be a string of at most {maximum} characters"
            + (" and nonempty" if required else "")
        )
    return value.strip()


def _relative(root: Path, raw: str, *, existing: bool) -> tuple[Path, str]:
    if (
        not isinstance(raw, str)
        or not raw
        or "\\" in raw
        or raw.startswith(("/", "-"))
        or ":" in raw
        or any(part in ("", ".", "..") for part in raw.split("/"))
    ):
        raise ValueError("paths must be safe repository-relative paths without traversal")
    target = root.joinpath(*raw.split("/"))
    current = root
    for part in raw.split("/"):
        current = current / part
        if current.is_symlink():
            raise ValueError("symlink paths are not permitted")
    if not target.resolve().is_relative_to(root):
        raise ValueError("path escapes repository checkout")
    if existing and not target.is_file():
        raise ValueError(f"source file not found: {raw}")
    return target, raw


def _git(root: Path, *args: str) -> str:
    try:
        return guarded_git_text(root, *args).strip()
    except (ValueError, OSError) as exc:
        raise ValueError(f"safe Git source check failed: {exc}") from exc


def _claims_at_revision(root: Path, revision: str) -> dict[str, dict]:
    names = _git(
        root, "ls-tree", "-r", "-z", "--name-only", revision, "--", ".sensemaking/knowledge"
    ).split(chr(0))
    claims: dict[str, dict] = {}
    for name in filter(None, names):
        if not name.endswith(".json"):
            continue
        data = json.loads(_git(root, "show", revision + ":" + name))
        for record in data.get("claims", []):
            identifier = record.get("id")
            if not isinstance(identifier, str) or not identifier:
                raise ValueError("authored knowledge has an invalid claim id")
            if identifier in claims:
                raise ValueError(f"duplicate authored claim id: {identifier}")
            claims[identifier] = record
    return claims


def _tracked_paths(root: Path) -> set[str]:
    return set(filter(None, _git(root, "ls-files", "-z").split(chr(0))))


def _known_claim_ids(root: Path, tracked: set[str]) -> set[str]:
    ids: set[str] = set()
    for name in sorted(tracked):
        if not name.startswith(".sensemaking/knowledge/") or not name.endswith(".json"):
            continue
        path, _ = _relative(root, name, existing=True)
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data.get("claims", []):
            identifier = record.get("id")
            if not isinstance(identifier, str) or identifier in ids:
                raise ValueError("existing knowledge has an invalid or duplicate claim id")
            ids.add(identifier)
    return ids


def _refs(
    data: Mapping[str, Any],
    key: str,
    *,
    minimum: int,
    maximum: int,
    prefix: str | None = None,
) -> list[str]:
    raw = data.get(key, [])
    if not isinstance(raw, list) or not minimum <= len(raw) <= maximum:
        raise ValueError(f"episode.{key} must be a list of {minimum}..{maximum} ids")
    if any(not isinstance(item, str) or not item for item in raw):
        raise ValueError(f"episode.{key} ids must be nonempty strings")
    if prefix and any(not item.startswith(prefix) for item in raw):
        raise ValueError(f"episode.{key} ids must start with {prefix}")
    return list(dict.fromkeys(raw))


def _dimensions(data: Mapping[str, Any]) -> dict[str, dict]:
    raw = data.get("dimensions")
    if not isinstance(raw, dict):
        raise ValueError("episode.dimensions must be an object")
    unexpected = set(raw) - set(_DIMENSIONS)
    missing = set(_DIMENSIONS) - set(raw)
    if unexpected or missing:
        raise ValueError(
            "episode.dimensions must contain exactly alignment, ambition, horizon and realization"
        )
    result: dict[str, dict] = {}
    for name in _DIMENSIONS:
        item = raw.get(name)
        if not isinstance(item, dict):
            raise ValueError(f"episode.dimensions.{name} must be an object")
        if set(item) - {"value", "basis", "establishment"}:
            raise ValueError(
                f"episode.dimensions.{name} may contain only value, basis and establishment"
            )
        value = _string(item, "value", maximum=80)
        basis = _string(item, "basis")
        cleaned = {"value": value, "basis": basis}
        if "establishment" in item:
            cleaned["establishment"] = _string(item, "establishment", maximum=40)
        result[name] = cleaned
    if result["realization"]["value"] not in {"HYPOTHETICAL", "NOT_ASSESSED"}:
        raise ValueError(
            "a new synthesis must be HYPOTHETICAL or NOT_ASSESSED; use ordinary "
            "reconciliation to claim implementation"
        )
    return result


def record_possibility_synthesis(
    repo: Path, episode_path: str, output_path: str, *, draft_only: bool = False,
) -> dict[str, Any]:
    """Create a new unreviewed possibility proposal; never mutate existing records."""
    repo = Path(repo).expanduser().resolve()
    root = Path(_git(repo, "rev-parse", "--show-toplevel")).resolve()
    episode_file, episode_relative = _relative(root, episode_path, existing=True)
    output_file, output_relative = _relative(root, output_path, existing=False)
    allowed_parents = (
        (root / ".sensemaking" / "proposals", root / "artifacts" / "history")
        if draft_only else (root / ".sensemaking" / "knowledge",)
    )
    if output_file.parent not in allowed_parents or not output_relative.endswith(".json"):
        if draft_only:
            raise ValueError("draft-only output must be a new .sensemaking/proposals/*.json or artifacts/history/*.json file")
        raise ValueError("output must be a new .sensemaking/knowledge/*.json file")
    if output_file.exists():
        raise ValueError(
            "output already exists; refusing to overwrite a proposal or reviewed record"
        )
    if episode_file.stat().st_size > 131072:
        raise ValueError("episode source exceeds the 128 KiB bounded input limit")

    data = json.loads(episode_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("episode input must be a JSON object")
    accepted = {
        "possibility_id",
        "actor",
        "source_revision",
        "origin_date",
        "title",
        "statement",
        "goal_refs",
        "source_candidate_refs",
        "capability_refs",
        "assumption_refs",
        "contradicts_refs",
        "dimensions",
        "synthesis_basis",
        "value_hypothesis",
        "value_prediction",
        "revisit_when",
        "counterevidence",
        "claim_ceiling",
        "evidence_refs",
    }
    unknown = set(data) - accepted
    if unknown:
        raise ValueError(f"unknown episode fields: {sorted(unknown)}")

    slug = _string(data, "possibility_id", maximum=72)
    if not _SLUG.fullmatch(slug):
        raise ValueError("possibility_id must be a lowercase slug (3..71 characters)")
    actor = _string(data, "actor", maximum=160)
    source_revision = _string(data, "source_revision", maximum=40)
    if not _COMMIT.fullmatch(source_revision):
        raise ValueError("source_revision must be the exact 40-character source commit SHA")
    if (
        _git(root, "rev-parse", "--verify", "--quiet", f"{source_revision}^{{commit}}")
        != source_revision
    ):
        raise ValueError("the source_revision is not available as an exact local Git commit")
    origin_date = _string(data, "origin_date", maximum=10)
    if not _DATE.fullmatch(origin_date):
        raise ValueError("origin_date must be YYYY-MM-DD")
    try:
        if date.fromisoformat(origin_date).isoformat() != origin_date:
            raise ValueError
    except ValueError as exc:
        raise ValueError("origin_date must be a valid calendar date") from exc
    title = _string(data, "title", maximum=200)
    statement = _string(data, "statement")
    synthesis_basis = _string(data, "synthesis_basis")
    value_hypothesis = _string(data, "value_hypothesis")
    value_frame: dict[str, str] | None = None
    if "value_prediction" in data:
        prediction = data["value_prediction"]
        if not isinstance(prediction, dict) or set(prediction) != set(_VALUE_PREDICTION_FIELDS):
            raise ValueError(
                "episode.value_prediction must contain exactly "
                + ", ".join(_VALUE_PREDICTION_FIELDS)
            )
        value_frame = {key: _string(prediction, key) for key in _VALUE_PREDICTION_FIELDS}
    revisit_when = _string(data, "revisit_when")
    counterevidence = _string(data, "counterevidence")
    ceiling = _string(data, "claim_ceiling")
    dimensions = _dimensions(data)

    tracked = _tracked_paths(root)
    if episode_relative not in tracked:
        raise ValueError(
            "stage or commit the synthesis episode file before preparing a proposal"
        )
    raw_evidence = data.get("evidence_refs")
    if (
        not isinstance(raw_evidence, list)
        or not 1 <= len(raw_evidence) <= 20
        or any(
            not isinstance(ref, str) or not ref.startswith("file:")
            for ref in raw_evidence
        )
    ):
        raise ValueError("evidence_refs must be a nonempty list of tracked file: paths")
    for reference in raw_evidence:
        _, path = _relative(root, reference[5:], existing=True)
        if path not in tracked:
            raise ValueError(f"evidence file is not staged or committed: {path}")
    references = list(dict.fromkeys(["file:" + episode_relative, *raw_evidence]))

    claims = _claims_at_revision(root, source_revision)
    goal_refs = _refs(data, "goal_refs", minimum=1, maximum=_MAX_REFS, prefix="goal:")
    source_refs = _refs(
        data, "source_candidate_refs", minimum=1, maximum=_MAX_REFS, prefix="poss:"
    )
    capability_refs = _refs(
        data, "capability_refs", minimum=0, maximum=_MAX_REFS, prefix="cap:"
    )
    assumption_refs = _refs(
        data, "assumption_refs", minimum=0, maximum=_MAX_REFS
    )
    contradiction_refs = _refs(
        data, "contradicts_refs", minimum=0, maximum=_MAX_REFS
    )

    for goal_id in goal_refs:
        record = claims.get(goal_id)
        if not record or record.get("kind") != "goal":
            raise ValueError(f"goal_ref is not an authored goal at source_revision: {goal_id}")
    for candidate_id in source_refs:
        record = claims.get(candidate_id)
        if not record or record.get("kind") != "opportunity":
            raise ValueError(
                f"source_candidate_ref is not an authored opportunity at source_revision: {candidate_id}"
            )
    for capability_id in capability_refs:
        record = claims.get(capability_id)
        if not record or record.get("kind") != "capability":
            raise ValueError(
                f"capability_ref is not an authored capability at source_revision: {capability_id}"
            )
    for assumption_id in assumption_refs:
        record = claims.get(assumption_id)
        if not record or record.get("kind") not in _ASSUMPTION_KINDS:
            raise ValueError(
                f"assumption_ref is not an authored assumption-like claim at source_revision: {assumption_id}"
            )
    for contradiction_id in contradiction_refs:
        record = claims.get(contradiction_id)
        if not record or record.get("kind") not in _CONTRADICTION_KINDS:
            raise ValueError(
                f"contradicts_ref is not an authored claim of an expected kind at source_revision: {contradiction_id}"
            )

    possibility_id = "poss:" + slug
    known_ids = _known_claim_ids(root, tracked)
    if possibility_id in claims or possibility_id in known_ids:
        raise ValueError("possibility identifier already exists in reviewed knowledge")
    prediction_id = "conseq:" + slug + "-value"
    if value_frame is not None and (prediction_id in claims or prediction_id in known_ids):
        raise ValueError("value prediction identifier already exists in reviewed knowledge")

    source_paths = set(
        filter(
            None,
            _git(
                root,
                "ls-tree",
                "-r",
                "-z",
                "--name-only",
                source_revision,
                "--",
            ).split(chr(0)),
        )
    )
    missing_at_source = sorted(
        {ref[5:] for ref in references if ref[5:] not in source_paths}
    )

    claim = {
        "id": possibility_id,
        "kind": "opportunity",
        "statement": statement,
        "authority_kind": "hypothesis",
        "authority_ref": episode_relative,
        "evidence_refs": references,
        "epistemic_status": "hypothetical",
        "attributes": {
            "concept": "ProductPossibility",
            "title": title,
            "origin": {
                "ref": episode_relative,
                "date": origin_date,
                "author": actor,
            },
            "dimensions": dimensions,
            "disposition_history": [
                {
                    "value": "EXPLORATORY",
                    "date": origin_date,
                    "authority": "agent-authored synthesis under current delegated mission",
                    "source": episode_relative,
                    "rationale": synthesis_basis,
                }
            ],
            "assessed_ref": source_revision,
            "synthesis_basis": synthesis_basis,
            "value_hypothesis": value_hypothesis,
            "revisit_when": revisit_when,
            "counterevidence": counterevidence,
            "claim_ceiling": ceiling,
            "agent_owned": True,
        },
    }
    relations: list[dict] = []
    for index, goal_id in enumerate(goal_refs, start=1):
        relations.append(
            {
                "id": f"rel:possibility-{slug}-candidate-for-{index}",
                "subject": possibility_id,
                "predicate": "candidate_opportunity_for",
                "object": goal_id,
                "evidence_refs": references,
                "epistemic_status": "hypothetical",
            }
        )
    for index, candidate_id in enumerate(source_refs, start=1):
        relations.append(
            {
                "id": f"rel:possibility-{slug}-derived-from-{index}",
                "subject": possibility_id,
                "predicate": "derived_from",
                "object": candidate_id,
                "evidence_refs": references,
                "epistemic_status": "hypothetical",
                "attributes": {
                    "conceptual_relation": "combines",
                    "establishment": "authored",
                },
            }
        )
    for index, capability_id in enumerate(capability_refs, start=1):
        relations.append(
            {
                "id": f"rel:possibility-{slug}-requires-{index}",
                "subject": possibility_id,
                "predicate": "requires_capability",
                "object": capability_id,
                "evidence_refs": references,
                "epistemic_status": "hypothetical",
            }
        )
    for index, assumption_id in enumerate(assumption_refs, start=1):
        relations.append(
            {
                "id": f"rel:possibility-{slug}-assumes-{index}",
                "subject": possibility_id,
                "predicate": "references",
                "object": assumption_id,
                "evidence_refs": references,
                "epistemic_status": "hypothetical",
                "attributes": {
                    "conceptual_relation": "assumes",
                    "establishment": "authored",
                },
            }
        )
    for index, contradiction_id in enumerate(contradiction_refs, start=1):
        relations.append(
            {
                "id": f"rel:possibility-{slug}-contradicts-{index}",
                "subject": possibility_id,
                "predicate": "contradicts",
                "object": contradiction_id,
                "evidence_refs": references,
                "epistemic_status": "hypothetical",
                "attributes": {
                    "conceptual_relation": "conflicts_with",
                    "establishment": "authored",
                },
            }
        )

    proposed_claims = [claim]
    if value_frame is not None:
        # Preserve the agent's actual hypothesis and criterion; never generate an
        # assessment or infer that the episode was written before an outcome.
        proposed_claims.append({
            "id": prediction_id,
            "kind": "hypothesis",
            "statement": value_hypothesis,
            "authority_kind": "hypothesis",
            "authority_ref": episode_relative,
            "evidence_refs": references,
            "epistemic_status": "hypothetical",
            "attributes": {
                "concept": "ConsequenceHypothesis",
                "source_possibility": possibility_id,
                "category": "benefit",
                "analysis_ref": episode_relative,
                "source_revision": source_revision,
                "origin": {"ref": episode_relative, "date": origin_date, "author": actor},
                "value_frame": value_frame,
                "assumptions": assumption_refs,
                "mechanism": synthesis_basis,
                "counterevidence": counterevidence,
                "would_change_decision_if": value_frame["would_change_decision_if"],
                "claim_ceiling": ceiling,
            },
        })
        relations.append({
            "id": f"rel:possibility-{slug}-value-prediction",
            "subject": prediction_id,
            "predicate": "references",
            "object": possibility_id,
            "evidence_refs": references,
            "epistemic_status": "hypothetical",
        })
    for proposed in proposed_claims:
        read_authored_claim(
            proposed, source_ref="file:" + output_relative, schema_version=2
        )
    for relation in relations:
        read_authored_relation(
            relation, source_ref="file:" + output_relative, schema_version=2
        )

    proposal = {"schema_version": 2, "claims": proposed_claims, "relations": relations}
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(proposal, stream, indent=2, ensure_ascii=False)
        stream.write("\n")

    return {
        "code": "SEMANTIC_POSSIBILITY_SYNTHESIS_CREATED",
        "created": True,
        "path": output_relative,
        "possibility_id": possibility_id,
        "source_revision": source_revision,
        "goal_refs": goal_refs,
        "source_candidate_refs": source_refs,
        "capability_refs": capability_refs,
        "assumption_refs": assumption_refs,
        "contradicts_refs": contradiction_refs,
        "proposed_claim_ids": [item["id"] for item in proposed_claims],
        **({"value_prediction_id": prediction_id} if value_frame is not None else {}),
        "proposed_relation_ids": [item["id"] for item in relations],
        "evidence_paths_not_in_source_revision": missing_at_source,
        "review_state": "UNREVIEWED_DRAFT",
        **({"detached_draft": True, "inside_active_knowledge": False} if draft_only else {}),
        "semantic_truth_established": False,
        "action_authorized": False,
        "next": (
            ("Run knowledge-proposal-check with an explicit new --destination, then "
             "review and copy the checked bytes to the destination and preflight again; "
             if draft_only else "Run knowledge-proposal-check, ")
            + "inspect the cited goals/candidates/capabilities/assumptions and evidence, "
            "then use normal Git review; the new possibility remains hypothetical "
            "and does not select or authorize construction."
        ),
    }
