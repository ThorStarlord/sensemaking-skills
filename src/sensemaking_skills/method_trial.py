"""Optional predecision method trials over reviewed knowledge.

A trial is a `decision` claim opened before work, naming the method and the
observable result the agent expects. Closing it adds a later `observation`
claim linked to that decision. The pair preserves what was committed before
the outcome and what was observed after it; it does not prove that the method
caused the result or that either record is correct.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Callable, Mapping

from .method_adaptation import (
    _git,
    _known_claim_ids,
    _relative,
    _string,
)
from .semantic_architecture.knowledge import read_authored_claim, read_authored_relation
from .semantic_architecture.knowledge_retrieval import (
    _FUNCTION_WORDS, _QUESTION_WORD, _lexical_hit, _query_tokens, _stem,
)

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


def _trial_digest(attributes: Mapping[str, Any]) -> str:
    payload = {
        key: attributes.get(key)
        for key in (
            "trial_id", "question", "method", "assumptions",
            "expected_observation", "prior_lesson_id", "source_revision",
        )
    }
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


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


def _is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    try:
        _git(root, "merge-base", "--is-ancestor", ancestor, descendant)
        return True
    except ValueError:
        return False


def _ancestry_status(root: Path, ancestor: str, descendant: str) -> str:
    """Return ANCESTOR, NOT_ANCESTOR or UNAVAILABLE for two commits."""

    for revision in (ancestor, descendant):
        try:
            _git(root, "cat-file", "-e", f"{revision}^{{commit}}")
        except ValueError:
            return "UNAVAILABLE"
    return "ANCESTOR" if _is_ancestor(root, ancestor, descendant) else "NOT_ANCESTOR"


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

    data = json.loads(episode_file.read_text(encoding="utf-8-sig"))
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

    source_paths = set(_git(
        root, "ls-tree", "-r", "-z", "--name-only", source_revision, "--"
    ).split(chr(0)))
    missing_at_source = sorted(path for path in refs if path not in source_paths)

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

    trial_attributes = {
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
        "evidence_paths_not_in_source_revision": missing_at_source,
    }
    trial_attributes["trial_digest"] = _trial_digest(trial_attributes)

    decision = {
        "id": decision_id,
        "kind": "decision",
        "statement": statement,
        "authority_kind": "delegated",
        "authority_ref": episode_relative,
        "evidence_refs": references,
        "epistemic_status": "declared",
        "attributes": trial_attributes,
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
        "trial_digest": trial_attributes["trial_digest"],
        "evidence_paths_not_in_source_revision": missing_at_source,
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

    data = json.loads(episode_file.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("episode input must be a JSON object")
    accepted = {
        "trial_id", "actor", "source_revision", "decision_commit",
        "observed_outcome", "disposition", "method_after",
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
    observed = _string(data, "observed_outcome")
    disposition = _string(data, "disposition", maximum=24)
    if disposition not in _DISPOSITIONS:
        raise ValueError(f"disposition must be one of {sorted(_DISPOSITIONS)}")
    ceiling = _string(data, "claim_ceiling")
    decision_commit = _string(data, "decision_commit", maximum=40)
    if not _COMMIT.fullmatch(decision_commit):
        raise ValueError("decision_commit must be the exact 40-character commit SHA")
    if _git(root, "rev-parse", "--verify", "--quiet", f"{decision_commit}^{{commit}}") != decision_commit:
        raise ValueError("decision_commit is not an available exact local commit")
    if decision_commit == source_revision:
        raise ValueError("source_revision must be later than decision_commit")
    if not _is_ancestor(root, decision_commit, source_revision):
        raise ValueError("source_revision must descend from decision_commit")
    method_after = _string(data, "method_after", required=False)
    if disposition == "ADAPTED" and not method_after:
        raise ValueError("ADAPTED requires an explicit method_after")
    tracked = _tracked_paths(root)
    if episode_relative not in tracked:
        raise ValueError("stage or commit the result episode file before preparing a proposal")
    refs = [episode_relative, *[r[5:] for r in _refs(
        data.get("evidence_refs"), field="evidence_refs"
    )]]
    for path in refs[1:]:
        if path not in tracked:
            raise ValueError(f"evidence file is not staged or committed: {path}")
    source_paths = set(_git(
        root, "ls-tree", "-r", "-z", "--name-only", source_revision, "--"
    ).split(chr(0)))
    missing_at_source = sorted(path for path in refs if path not in source_paths)

    reviewed = _reviewed_claims(root, source_revision)
    decision_id = "decision:method-trial-" + trial_id
    trial = reviewed.get(decision_id)
    if not trial or trial.get("kind") != "decision":
        raise ValueError("the trial decision is not reviewed at source_revision")
    attributes = trial.get("attributes") or {}
    if attributes.get("trial_status") != "OPEN" or attributes.get("trial_id") != trial_id:
        raise ValueError("the reviewed trial is not an open method trial")
    stored_digest = attributes.get("trial_digest")
    if not isinstance(stored_digest, str) or stored_digest != _trial_digest(attributes):
        raise ValueError("trial decision content is not anchored by a matching trial_digest")
    at_decision_commit = _reviewed_claims(root, decision_commit).get(decision_id)
    if not at_decision_commit:
        raise ValueError("decision_commit does not contain the trial decision")
    if _trial_digest(at_decision_commit.get("attributes") or {}) != stored_digest:
        raise ValueError("the trial decision changed after decision_commit")
    prior = attributes.get("prior_lesson_id")
    prior = prior if isinstance(prior, str) and prior not in ("", "NONE") else None
    if prior:
        _lesson_at(reviewed, prior)
    for claim in reviewed.values():
        audit = claim.get("attributes") or {}
        if (claim.get("kind") == "observation"
                and (audit.get("trial_id") == trial_id
                     or audit.get("trial_decision_ref") == decision_id)):
            raise ValueError("trial already has a closing observation; refuse duplicate closure")
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
            "decision_commit": decision_commit,
            "trial_digest": attributes["trial_digest"],
            "observed_outcome": observed,
            "disposition": disposition,
            "method_after": method_after or "NOT_RECORDED",
            "actor": actor,
            "source_revision": source_revision,
            "claim_ceiling": ceiling,
            "evidence_paths_not_in_source_revision": missing_at_source,
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
    relations = [relation]
    if prior:
        relations.append({
            "id": f"rel:method-trial-{trial_id}-result-for-lesson",
            "subject": result_id,
            "predicate": "references",
            "object": prior,
            "evidence_refs": references,
            "epistemic_status": "declared",
            "attributes": {
                "conceptual_relation": "trial_result_for",
                "establishment": "authored",
            },
        })
    read_authored_claim(observation, source_ref="file:" + output_relative, schema_version=2)
    for relation_item in relations:
        read_authored_relation(
            relation_item, source_ref="file:" + output_relative, schema_version=2
        )
    proposal = {
        "schema_version": 2,
        "claims": [observation],
        "relations": relations,
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
        "decision_commit": decision_commit,
        "disposition": disposition,
        "method_after": method_after or "NOT_RECORDED",
        "evidence_paths_not_in_source_revision": missing_at_source,
        "review_state": "UNREVIEWED_DRAFT",
        "method_effect_established": False,
        "semantic_truth_established": False,
        "action_authorized": False,
        "next": "Review and commit the result; the trial decision remains the predecision record.",
    }

def trial_ancestry(repo: Path) -> Callable[[str, str], str]:
    """Return a local Git ancestry status function for one repository."""

    root = Path(_git(repo, "rev-parse", "--show-toplevel")).resolve()
    return lambda ancestor, descendant: _ancestry_status(root, ancestor, descendant)


def method_trial_context(
    question: str, initial: Mapping[str, Any],
    explain: Callable[[str], Mapping[str, Any]], *, limit: int = 8,
    ancestry: Callable[[str, str], str] | None = None,
) -> dict[str, Any]:
    """Find authored method-trial precedents by question, then inspect each pair.

    Trials are not lessons. Discovery is lexical, even when a trial cites no
    prior lesson; the existing trial-view contract controls chronology and
    closure. A failed projection is visible, never mistaken for an open trial.
    """
    if (not isinstance(question, str) or len(question) > 300
            or any(ord(c) < 32 for c in question)):
        raise ValueError("question must be one line of at most 300 characters")
    tokens = _query_tokens(question)
    if not 1 <= len(tokens) <= 24 or not 1 <= limit <= 25:
        raise ValueError("method trial context requires 1..24 words and limit 1..25")
    words = tuple(word for word in tokens if word not in _FUNCTION_WORDS)
    if not words:
        raise ValueError("question must contain a decision-relevant content word")
    ranked: list[tuple[int, int, str, tuple[str, ...]]] = []
    for claim in initial.get("claims", []):
        identifier = claim.get("id")
        attributes = claim.get("attributes") or {}
        if (claim.get("kind") != "decision" or not isinstance(identifier, str)
                or not identifier.startswith("decision:method-trial-")
                or attributes.get("trial_status") not in {"OPEN", "CLOSED"}):
            continue
        name = identifier.casefold().partition(":")[2]
        text = " ".join(str(attributes.get(key) or "") for key in (
            "question", "method", "assumptions", "expected_observation",
        )).casefold()
        stems = {_stem(word) for word in _QUESTION_WORD.findall(name + " " + text)}
        matched = tuple(word for word in words if _lexical_hit(word, name, text, stems))
        if matched:
            ranked.append((-len(matched), -sum(map(len, matched)), identifier, matched))
    ranked.sort()
    candidates = []
    for _, _, identifier, matched in ranked[:limit]:
        envelope = explain(identifier)
        item: dict[str, Any] = {
            "id": identifier,
            "matched_tokens": list(matched),
            "applicability_to_present_task": "NOT_ESTABLISHED",
            "projection_status": "NOT_ASSESSED",
            "trial": None,
        }
        if envelope.get("target_ref") != initial.get("target_ref"):
            raise ValueError("method trial context source revision mismatch")
        if envelope.get("truncated"):
            item["projection_reason"] = "EXPLAIN_TRUNCATED"
        else:
            try:
                item["trial"] = build_method_trial_view(
                    identifier, envelope.get("claims", []),
                    envelope.get("relations", []), ancestry=ancestry,
                )
            except ValueError as exc:
                item["projection_reason"] = str(exc)
            else:
                item["projection_status"] = "PROJECTED"
        candidates.append(item)
    return {
        "target_ref": initial.get("target_ref"),
        "trial_candidates": candidates,
        "trial_candidate_matches": len(ranked),
        "trial_candidate_matches_omitted": max(0, len(ranked) - limit),
        "trial_corpus_returned": len(initial.get("claims", [])),
        "trial_corpus_total": initial.get("search_hit_total"),
        "trial_corpus_truncated": bool(initial.get("truncated", False)),
        "method_effect_established": False,
        "semantic_truth_established": False,
        "action_authorized": False,
        "explicit_limits": [
            "Matches use authored trial questions, methods, assumptions, expectations and IDs; lexical overlap is not applicability.",
            "The search corpus is bounded at 250 records; a miss or truncation does not establish absence.",
            "A projected trial preserves the existing chronology, digest and closure limits. An unassessed projection is not an open trial.",
            "Trial precedents are historical evidence, not promoted lessons or method recommendations.",
        ],
    }


def build_method_trial_view(
    trial_id: str,
    claims: list[Mapping[str, Any]],
    relations: list[Mapping[str, Any]],
    *,
    ancestry: Callable[[str, str], str] | None = None,
) -> dict[str, Any]:
    """Project a trial decision and its optional closing observation.

    Ambiguity fails closed: more than one closing relation, a missing closing
    observation, or a closing record whose trial identity does not match raises
    instead of selecting a first match. Preservation is computed from the
    recorded digest and, when available, verified Git ancestry.
    """

    trial = next((item for item in claims if item.get("id") == trial_id), None)
    if not trial or trial.get("kind") != "decision":
        raise ValueError("trial_id is not a reviewed decision claim")
    attributes = trial.get("attributes") or {}
    if attributes.get("trial_status") not in {"OPEN", "CLOSED"}:
        raise ValueError("trial_id is not a method trial decision")

    stored_digest = attributes.get("trial_digest")
    if not isinstance(stored_digest, str):
        decision_digest_match = "NOT_ASSESSED"
    elif stored_digest == _trial_digest(attributes):
        decision_digest_match = "MATCH"
    else:
        decision_digest_match = "MISMATCH"

    closing_relations = [
        relation for relation in relations
        if relation.get("predicate") == "references"
        and relation.get("object") == trial_id
        and (relation.get("attributes") or {}).get("conceptual_relation")
        == "closes_trial"
    ]
    if len(closing_relations) > 1:
        raise ValueError(
            "multiple closing relations for the trial; refuse ambiguous closure"
        )

    result = None
    result_digest_match = "NOT_ASSESSED"
    chronology = "NOT_ASSESSED"
    if closing_relations:
        relation = closing_relations[0]
        closing_id = relation.get("subject")
        matches = [item for item in claims if item.get("id") == closing_id]
        if len(matches) != 1:
            raise ValueError(
                "closing observation is not uniquely present in the explain envelope"
            )
        closing = matches[0]
        if closing.get("kind") != "observation":
            raise ValueError("the closing record is not an observation")
        result_attributes = closing.get("attributes") or {}
        if result_attributes.get("trial_id") != attributes.get("trial_id"):
            raise ValueError("closing observation trial_id does not match the trial")
        if result_attributes.get("trial_decision_ref") != trial_id:
            raise ValueError("closing observation decision ref does not match the trial")
        result_digest = result_attributes.get("trial_digest")
        if isinstance(stored_digest, str) and isinstance(result_digest, str):
            result_digest_match = (
                "MATCH" if result_digest == stored_digest else "MISMATCH"
            )
        decision_commit = result_attributes.get("decision_commit")
        result_revision = result_attributes.get("source_revision")
        if (_COMMIT.fullmatch(str(decision_commit or ""))
                and _COMMIT.fullmatch(str(result_revision or ""))):
            if decision_commit == result_revision:
                chronology = "FAILED"
            elif ancestry is not None:
                status = ancestry(decision_commit, result_revision)
                if status == "ANCESTOR":
                    chronology = "VERIFIED"
                elif status == "NOT_ANCESTOR":
                    chronology = "FAILED"
                else:
                    chronology = "NOT_ASSESSED"
            else:
                chronology = "NOT_ASSESSED"
        if chronology == "FAILED":
            raise ValueError("closing result is not at a later descendant revision")
        result = {
            "id": closing.get("id"),
            "statement": closing.get("statement"),
            "observed_outcome": result_attributes.get("observed_outcome"),
            "disposition": result_attributes.get("disposition"),
            "method_after": result_attributes.get("method_after"),
            "actor": result_attributes.get("actor"),
            "source_revision": result_attributes.get("source_revision"),
            "decision_commit": decision_commit,
            "claim_ceiling": result_attributes.get("claim_ceiling"),
            "evidence_refs": list(closing.get("evidence_refs") or []),
            "evidence_paths_not_in_source_revision": list(
                result_attributes.get("evidence_paths_not_in_source_revision") or []
            ),
        }

    preservation_reasons: list[str] = []
    if result is None:
        preservation_reasons.append("TRIAL_OPEN")
    else:
        if decision_digest_match != "MATCH":
            preservation_reasons.append(
                "DECISION_DIGEST_" + decision_digest_match
            )
        if result_digest_match != "MATCH":
            preservation_reasons.append("RESULT_DIGEST_" + result_digest_match)
        if chronology != "VERIFIED":
            preservation_reasons.append("CHRONOLOGY_" + chronology)

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
            "trial_digest": stored_digest,
            "evidence_refs": list(trial.get("evidence_refs") or []),
            "evidence_paths_not_in_source_revision": list(
                attributes.get("evidence_paths_not_in_source_revision") or []
            ),
        },
        "closed": result is not None,
        "result": result,
        "trial_digest_match": decision_digest_match,
        "result_digest_match": result_digest_match,
        "trial_chronology": chronology,
        "predecision_commitment_preserved": not preservation_reasons,
        "preservation_reasons": preservation_reasons,
        "method_effect_established": False,
        "semantic_truth_established": False,
        "action_authorized": False,
        "explicit_limits": [
            "The trial decision is the predecision record; the result is a later authored observation.",
            "Preservation requires matching digests and verified later Git ancestry, not just a closing relation.",
            "The disposition is agent-authored and does not prove that the method caused the outcome.",
            "No ranking, method selection or action authorization is performed.",
        ],
    }
