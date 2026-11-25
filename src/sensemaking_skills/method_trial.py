"""Optional predecision method trials over reviewed knowledge.

A trial is a `decision` claim opened before work, naming the method and the
observable result the agent expects. Closing it adds a later `observation`
claim linked to that decision. The pair preserves what was committed before
the outcome and what was observed after it; it does not prove that the method
caused the result or that either record is correct.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Mapping

from .method_adaptation import (
    _git,
    _known_claim_ids,
    _relative,
    _string,
)
from .semantic_architecture.knowledge import read_authored_claim, read_authored_relation

_TRIAL_SLUG = re.compile(r"[a-z0-9][a-z0-9-]{2,70}\Z")
_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z")
_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_DISPOSITIONS = frozenset({
    "CONFIRMED", "ADAPTED", "REJECTED", "NO_CHANGE", "INCONCLUSIVE",
})
_MAX_TEXT = 2400
_MAX_REFS = 20


def _tracked_paths(root: Path) -> set[str]:
    return set(filter(None, _git(root, "ls-files", "-z").split(chr(0))))


def _date(value: str, field: str) -> str:
    if not _DATE.fullmatch(value):
        raise ValueError(f"{field} must be YYYY-MM-DD")
    try:
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError
    except ValueError as exc:
        raise ValueError(f"{field} must be a valid calendar date") from exc
    return value


def _reviewed_claims(root: Path, source_revision: str) -> dict[str, dict[str, Any]]:
    names = _git(
        root, "ls-tree", "-r", "-z", "--name-only", source_revision,
        "--", ".sensemaking/knowledge",
    ).split(chr(0))
    claims: dict[str, dict[str, Any]] = {}
    for name in filter(None, names):
        if not name.endswith(".json"):
            continue
        data = json.loads(_git(root, "show", f"{source_revision}:{name}"))
        for record in data.get("claims", []):
            identifier = record.get("id")
            if not isinstance(identifier, str) or not identifier:
                raise ValueError("reviewed knowledge has an invalid claim id")
            if identifier in claims:
                raise ValueError(f"duplicate reviewed claim id: {identifier}")
            claims[identifier] = record
    return claims


def _refs(value: Any, *, field: str) -> list[str]:
    if not isinstance(value, list) or not 1 <= len(value) <= _MAX_REFS:
        raise ValueError(f"episode.{field} must contain 1..{_MAX_REFS} file refs")
    refs: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.startswith("file:"):
            raise ValueError(f"episode.{field} entries must be file: paths")
        if item not in refs:
            refs.append(item)
    return refs


def _source_revision(root: Path, data: Mapping[str, Any]) -> str:
    revision = _string(data, "source_revision", maximum=40)
    if not _COMMIT.fullmatch(revision):
        raise ValueError("source_revision must be the exact 40-character commit SHA")
    if _git(root, "rev-parse", "--verify", "--quiet", f"{revision}^{{commit}}") != revision:
        raise ValueError("source_revision is not an available exact local commit")
    return revision


def _lesson_at(
    claims: Mapping[str, Mapping[str, Any]], lesson_id: str
) -> Mapping[str, Any]:
    lesson = claims.get(lesson_id)
    if not lesson or lesson.get("kind") != "lesson":
        raise ValueError("prior_lesson_id must name a reviewed lesson at source_revision")
    method = (lesson.get("attributes") or {}).get("method")
    if not isinstance(method, str) or not method.strip():
        raise ValueError("prior_lesson_id lesson has no authored method")
    return lesson


def open_method_trial(
    repo: Path, episode_path: str, output_path: str
) -> dict[str, Any]:
    """Create an unreviewed trial-decision proposal; do not select a method."""

    repo = Path(repo).expanduser().resolve()
    root = Path(_git(repo, "rev-parse", "--show-toplevel")).resolve()
    episode_file, episode_relative = _relative(root, episode_path, existing=True)
    output_file, output_relative = _relative(root, output_path, existing=False)
    if (output_file.parent != root / ".sensemaking" / "knowledge"
            or not output_relative.endswith(".json")):
        raise ValueError("output must be a new .sensemaking/knowledge/*.json file")
    if output_file.exists():
        raise ValueError("output already exists; refusing to overwrite")
    if episode_file.stat().st_size > 131072:
        raise ValueError("episode source exceeds the 128 KiB bounded input limit")

    data = json.loads(episode_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("episode input must be a JSON object")
    accepted = {
        "trial_id", "actor", "source_revision", "origin_date", "question",
        "method", "assumptions", "expected_observation", "prior_lesson_id",
        "evidence_refs", "claim_ceiling",
    }
    unknown = set(data) - accepted
    if unknown:
        raise ValueError(f"unknown episode fields: {sorted(unknown)}")
    trial_id = _string(data, "trial_id", maximum=72)
    if not _TRIAL_SLUG.fullmatch(trial_id):
        raise ValueError("trial_id must be a lowercase slug (3..71 characters)")
    actor = _string(data, "actor", maximum=160)
    source_revision = _source_revision(root, data)
    origin_date = _date(_string(data, "origin_date", maximum=10), "origin_date")
    question = _string(data, "question")
    method = _string(data, "method")
    assumptions = _string(data, "assumptions")
    expected = _string(data, "expected_observation")
    ceiling = _string(data, "claim_ceiling")
    prior = _string(data, "prior_lesson_id", required=False, maximum=160)

    tracked = _tracked_paths(root)
    if episode_relative not in tracked:
        raise ValueError("stage or commit the trial episode file before preparing a proposal")
    reviewed = _reviewed_claims(root, source_revision)
    if prior:
        _lesson_at(reviewed, prior)
    refs = [episode_relative, *[r[5:] for r in _refs(
        data.get("evidence_refs"), field="evidence_refs"
    )]]
    for path in refs[1:]:
        if path not in tracked:
            raise ValueError(f"evidence file is not staged or committed: {path}")

    decision_id = "decision:method-trial-" + trial_id
    known = _known_claim_ids(root, tracked)
    if decision_id in known or decision_id in reviewed:
        raise ValueError("trial decision identifier already exists")
    references = list(dict.fromkeys(["file:" + path for path in refs]))
    statement = (
        "Method trial " + trial_id + ": " + question +
        " Selected method: " + method +
        " Expected observation: " + expected
    )

    decision = {
        "id": decision_id,
        "kind": "decision",
        "statement": statement,
        "authority_kind": "delegated",
        "authority_ref": episode_relative,
        "evidence_refs": references,
        "epistemic_status": "declared",
        "attributes": {
            "trial_id": trial_id,
            "trial_status": "OPEN",
            "question": question,
            "method": method,
            "assumptions": assumptions,
            "expected_observation": expected,
            "prior_lesson_id": prior or "NONE",
            "actor": actor,
            "source_revision": source_revision,
            "opened_date": origin_date,
            "claim_ceiling": ceiling,
        },
    }
    relations = []
    if prior:
        relations.append({
            "id": f"rel:method-trial-{trial_id}-applies-precedent",
            "subject": decision_id,
            "predicate": "references",
            "object": prior,
            "evidence_refs": references,
            "epistemic_status": "declared",
            "attributes": {
                "conceptual_relation": "applies_precedent",
                "establishment": "authored",
            },
        })
    read_authored_claim(decision, source_ref="file:" + output_relative, schema_version=2)
    for relation in relations:
        read_authored_relation(
            relation, source_ref="file:" + output_relative, schema_version=2
        )
    proposal = {"schema_version": 2, "claims": [decision], "relations": relations}
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(proposal, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    return {
        "code": "SEMANTIC_METHOD_TRIAL_OPENED",
        "trial_id": trial_id,
        "decision_id": decision_id,
        "path": output_relative,
        "review_state": "UNREVIEWED_DRAFT",
        "prior_lesson_id": prior or "NONE",
        "source_revision": source_revision,
        "method_effect_established": False,
        "semantic_truth_established": False,
        "action_authorized": False,
        "next": "Review and commit the trial decision before the work; close it only with observed evidence.",
    }


def close_method_trial(
    repo: Path, episode_path: str, output_path: str
) -> dict[str, Any]:
    """Append an observed result to a committed, open trial decision."""

    repo = Path(repo).expanduser().resolve()
    root = Path(_git(repo, "rev-parse", "--show-toplevel")).resolve()
    episode_file, episode_relative = _relative(root, episode_path, existing=True)
    output_file, output_relative = _relative(root, output_path, existing=False)
    if (output_file.parent != root / ".sensemaking" / "knowledge"
            or not output_relative.endswith(".json")):
        raise ValueError("output must be a new .sensemaking/knowledge/*.json file")
    if output_file.exists():
        raise ValueError("output already exists; refusing to overwrite")
    if episode_file.stat().st_size > 131072:
        raise ValueError("episode source exceeds the 128 KiB bounded input limit")

    data = json.loads(episode_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("episode input must be a JSON object")
    accepted = {
        "trial_id", "actor", "source_revision", "observed_outcome",
        "disposition", "evidence_refs", "claim_ceiling",
    }
    unknown = set(data) - accepted
    if unknown:
        raise ValueError(f"unknown episode fields: {sorted(unknown)}")
    trial_id = _string(data, "trial_id", maximum=72)
    if not _TRIAL_SLUG.fullmatch(trial_id):
        raise ValueError("trial_id must be a lowercase slug (3..71 characters)")
    actor = _string(data, "actor", maximum=160)
    source_revision = _source_revision(root, data)
    observed = _string(data, "observed_outcome")
    disposition = _string(data, "disposition", maximum=24)
    if disposition not in _DISPOSITIONS:
        raise ValueError(f"disposition must be one of {sorted(_DISPOSITIONS)}")
    ceiling = _string(data, "claim_ceiling")
    tracked = _tracked_paths(root)
    if episode_relative not in tracked:
        raise ValueError("stage or commit the result episode file before preparing a proposal")
    refs = [episode_relative, *[r[5:] for r in _refs(
        data.get("evidence_refs"), field="evidence_refs"
    )]]
    for path in refs[1:]:
        if path not in tracked:
            raise ValueError(f"evidence file is not staged or committed: {path}")

    reviewed = _reviewed_claims(root, source_revision)
    decision_id = "decision:method-trial-" + trial_id
    trial = reviewed.get(decision_id)
    if not trial or trial.get("kind") != "decision":
        raise ValueError("the trial decision is not reviewed at source_revision")
    attributes = trial.get("attributes") or {}
    if attributes.get("trial_status") != "OPEN" or attributes.get("trial_id") != trial_id:
        raise ValueError("the reviewed trial is not an open method trial")
    result_id = "observation:method-trial-" + trial_id + "-result"
    known = _known_claim_ids(root, tracked)
    if result_id in known or result_id in reviewed:
        raise ValueError("trial result identifier already exists; refuse duplicate closure")
    references = list(dict.fromkeys(["file:" + path for path in refs]))
    statement = (
        "Method trial result " + trial_id + ": " + observed +
        " Disposition: " + disposition + "."
    )
    observation = {
        "id": result_id,
        "kind": "observation",
        "statement": statement,
        "authority_kind": "delegated",
        "authority_ref": episode_relative,
        "evidence_refs": references,
        "epistemic_status": "declared",
        "attributes": {
            "trial_id": trial_id,
            "trial_decision_ref": decision_id,
            "trial_status": "CLOSED",
            "observed_outcome": observed,
            "disposition": disposition,
            "actor": actor,
            "source_revision": source_revision,
            "claim_ceiling": ceiling,
        },
    }
    relation = {
        "id": f"rel:method-trial-{trial_id}-closed-by",
        "subject": result_id,
        "predicate": "references",
        "object": decision_id,
        "evidence_refs": references,
        "epistemic_status": "declared",
        "attributes": {
            "conceptual_relation": "closes_trial",
            "establishment": "authored",
        },
    }
    read_authored_claim(observation, source_ref="file:" + output_relative, schema_version=2)
    read_authored_relation(relation, source_ref="file:" + output_relative, schema_version=2)
    proposal = {
        "schema_version": 2,
        "claims": [observation],
        "relations": [relation],
    }
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(proposal, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    return {
        "code": "SEMANTIC_METHOD_TRIAL_CLOSED",
        "trial_id": trial_id,
        "decision_id": decision_id,
        "result_id": result_id,
        "path": output_relative,
        "disposition": disposition,
        "review_state": "UNREVIEWED_DRAFT",
        "method_effect_established": False,
        "semantic_truth_established": False,
        "action_authorized": False,
        "next": "Review and commit the result; the trial decision remains the predecision record.",
    }

def build_method_trial_view(
    trial_id: str, claims: list[Mapping[str, Any]], relations: list[Mapping[str, Any]]
) -> dict[str, Any]:
    """Project a trial decision and its optional closing observation."""

    trial = next(
        (item for item in claims if item.get("id") == trial_id), None
    )
    if not trial or trial.get("kind") != "decision":
        raise ValueError("trial_id is not a reviewed decision claim")
    attributes = trial.get("attributes") or {}
    if attributes.get("trial_status") not in {"OPEN", "CLOSED"}:
        raise ValueError("trial_id is not a method trial decision")
    closing = None
    for relation in relations:
        if relation.get("predicate") != "references":
            continue
        if relation.get("object") != trial_id:
            continue
        if (relation.get("attributes") or {}).get("conceptual_relation") != "closes_trial":
            continue
        closing = next(
            (item for item in claims if item.get("id") == relation.get("subject")),
            None,
        )
        if closing is not None:
            break
    result = None
    if closing is not None:
        result_attributes = closing.get("attributes") or {}
        result = {
            "id": closing.get("id"),
            "statement": closing.get("statement"),
            "observed_outcome": result_attributes.get("observed_outcome"),
            "disposition": result_attributes.get("disposition"),
            "actor": result_attributes.get("actor"),
            "source_revision": result_attributes.get("source_revision"),
            "claim_ceiling": result_attributes.get("claim_ceiling"),
            "evidence_refs": list(closing.get("evidence_refs") or []),
        }
    return {
        "code": "SEMANTIC_METHOD_TRIAL",
        "trial_id": attributes.get("trial_id"),
        "trial_decision": {
            "id": trial.get("id"),
            "statement": trial.get("statement"),
            "question": attributes.get("question"),
            "method": attributes.get("method"),
            "assumptions": attributes.get("assumptions"),
            "expected_observation": attributes.get("expected_observation"),
            "prior_lesson_id": attributes.get("prior_lesson_id"),
            "actor": attributes.get("actor"),
            "source_revision": attributes.get("source_revision"),
            "opened_date": attributes.get("opened_date"),
            "claim_ceiling": attributes.get("claim_ceiling"),
            "evidence_refs": list(trial.get("evidence_refs") or []),
        },
        "closed": result is not None,
        "result": result,
        "predecision_commitment_preserved": True,
        "method_effect_established": False,
        "semantic_truth_established": False,
        "action_authorized": False,
        "explicit_limits": [
            "The trial decision is the predecision record; the result is a later authored observation.",
            "The disposition is agent-authored and does not prove that the method caused the outcome.",
            "No ranking, method selection or action authorization is performed.",
        ],
    }
