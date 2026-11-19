"""Optional, agent-owned methodological experience lifecycle over reviewed knowledge.

No semantic method selector, automatic lesson extractor, policy promotion, or
second persistent store. The caller authors a procedure only after real work;
this module makes its provenance and later source-checked reconsideration usable.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable, Mapping

from .semantic_architecture.knowledge import read_authored_claim, read_authored_relation
from .semantic_architecture.knowledge_retrieval import (
    _FUNCTION_WORDS, _QUESTION_WORD, _lexical_hit, _query_tokens, _stem,
)
from .semantic_architecture.worktree_context import guarded_git_text

_EPISODE_SLUG = re.compile(r"[a-z0-9][a-z0-9-]{2,70}\Z")
_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_DISPOSITIONS = frozenset({"develop", "adapt", "apply", "reject", "no_change"})
_METHOD_CHANGES = frozenset({"develop", "adapt"})
_METHOD_CLAIM_LIMIT = 250


def method_context(
    question: str, initial: Mapping[str, Any],
    explain: Callable[[str], Mapping[str, Any]], *, limit: int = 8,
    path_contexts: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compose existing reviewed lesson search + explicit later evidence.

    The question is used for literal lexical relevance only. Procedure
    applicability, lessons learned, causation and authority stay agent-owned.
    """
    if not isinstance(question, str) or len(question) > 300 or any(ord(c) < 32 for c in question):
        raise ValueError("question must be one line of at most 300 characters")
    tokens = _query_tokens(question)
    if not 1 <= len(tokens) <= 24:
        raise ValueError("question must have 1..24 distinct words of length 2+")
    if not 1 <= limit <= 25:
        raise ValueError("method context limit must be 1..25")
    content_words = tuple(w for w in tokens if w not in _FUNCTION_WORDS)
    if not content_words:
        raise ValueError("question must contain a decision-relevant content word")

    # Context-for carries explicit source/ownership routes. Evidence references
    # are provenance, not file ownership or proof that a method applies.
    path_contexts = path_contexts or {}
    context_history: dict[str, set[str]] = {}
    path_disclosures: list[dict[str, Any]] = []
    for path, envelope in path_contexts.items():
        ctx = envelope.get("context", {})
        for item in ctx.get("history", []):
            if item.get("kind") == "lesson":
                context_history.setdefault(item["claim_id"], set()).add(path)
        path_disclosures.append({
            "path": path,
            "coverage_status": ctx.get("ownership", {}).get("coverage_status", "NOT_ASSESSED"),
            "context_truncated": bool(ctx.get("truncated", False) or envelope.get("truncated", False)),
            "knowledge_gaps": ctx.get("knowledge_gaps", []),
            "source_ref": envelope.get("target_ref"),
        })

    ranked: list[tuple[int, int, int, str, dict, tuple[str, ...], list[dict]]] = []
    for claim in initial.get("claims", []):
        if claim.get("kind") != "lesson":
            continue
        attributes = claim.get("attributes") or {}
        procedure = attributes.get("method")
        if not isinstance(procedure, str) or not procedure.strip():
            continue
        name = claim["id"].casefold().partition(":")[2]
        text = " ".join(str(part) for part in (
            claim.get("statement", ""), procedure, attributes.get("scope", ""),
            attributes.get("conditions", ""), attributes.get("revisit_when", ""),
        )).casefold()
        stems = {_stem(word) for word in _QUESTION_WORD.findall(name + " " + text)}
        matched = tuple(word for word in content_words if _lexical_hit(word, name, text, stems))
        authored_sources = {ref[5:] for ref in claim.get("evidence_refs", [])
                           if isinstance(ref, str) and ref.startswith("file:")}
        routes: list[dict] = []
        for path in path_contexts:
            reasons = []
            if path in authored_sources or path == claim.get("authority_ref"):
                reasons.append("AUTHORED_SOURCE_REF")
            if path in context_history.get(claim["id"], set()):
                reasons.append("REVIEWED_CONTEXT_HISTORY")
            if reasons:
                routes.append({"path": path, "routes": reasons})
        if matched or routes:
            ranked.append((
                -len(routes), -len(matched), -sum(map(len, matched)),
                claim["id"], claim, matched, routes,
            ))
    ranked.sort(key=lambda item: (item[0], item[1], item[2], item[3]))

    candidates = []
    for _, _, _, identifier, claim, matched, routes in ranked[:limit]:
        linked = claim.get("citing_records") or []
        neighbors = explain(identifier) if linked else {}
        indexed = {record.get("id"): record for record in neighbors.get("claims", [])}
        history = []
        for item in linked:
            source = indexed.get(item.get("id"))
            history.append({
                **item,
                "record": {
                    "statement": source.get("statement"),
                    "epistemic_status": source.get("epistemic_status"),
                    "authority_ref": source.get("authority_ref"),
                    "evidence_refs": source.get("evidence_refs", []),
                    "attributes": source.get("attributes", {}),
                } if source else None,
                "source_read_status": "INDEXED_RECORD" if source else "NOT_ASSESSED",
            })
        candidates.append({
            "id": identifier,
            "statement": claim.get("statement"),
            "procedure": claim["attributes"]["method"],
            "matched_tokens": list(matched),
            "matched_paths": routes,
            "epistemic_status": claim.get("epistemic_status"),
            "authority_ref": claim.get("authority_ref"),
            "evidence_refs": claim.get("evidence_refs", []),
            "recall_conditions": claim.get("recall_conditions", {}),
            "later_related_records": history,
            "related_records_complete": (
                not neighbors.get("truncated", False)
                and all(item["source_read_status"] == "INDEXED_RECORD" for item in history)
                if linked else True
            ),
            "applicability_to_present_task": "NOT_ESTABLISHED",
            "present_method_decision": "AGENT_OWNED",
        })

    return {
        "code": "SEMANTIC_METHOD_CONTEXT",
        "question": question,
        "repository": initial.get("repository"),
        "target_ref": initial.get("target_ref"),
        "workspace_context": initial.get("workspace_context", {}),
        "workspace_index": initial.get("workspace_index", {}),
        "method_candidates": candidates,
        "path_context": path_disclosures,
        "method_candidate_matches": len(ranked),
        "method_candidate_matches_omitted": max(0, len(ranked) - limit),
        "lesson_corpus_returned": len(initial.get("claims", [])),
        "lesson_corpus_total": initial.get("search_hit_total"),
        "lesson_corpus_truncated": bool(initial.get("truncated", False)),
        "source_scope": initial.get("source_scope", []),
        "semantic_truth_established": False,
        "action_authorized": False,
        "explicit_limits": [
            "Methods are explicit authored lesson.attributes.method strings, not inferred from technical lessons.",
            "Candidate discovery uses literal question words or explicit authored evidence/context-for path routes; neither establishes method applicability.",
            "The reviewed lesson corpus is bounded at 250 records. A miss or truncated source is NOT_ASSESSED, not absence.",
            "Related records and their statements are indexed evidence, not verified support/refutation or Git chronology.",
            "Inspect original sources, changed conditions, current authority and counterevidence before selecting a method.",
            "This tool does not choose, adapt, learn, validate or authorize an intellectual procedure.",
        ],
    }


def _relative(root: Path, raw: str, *, existing: bool) -> tuple[Path, str]:
    if (not isinstance(raw, str) or not raw or "\\" in raw or
            raw.startswith(("/", "-")) or ":" in raw or
            any(part in ("", ".", "..") for part in raw.split("/"))):
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


def _string(data: Mapping[str, Any], key: str, *, required: bool = True, maximum: int = 2400) -> str:
    value = data.get(key, "")
    if not isinstance(value, str) or len(value) > maximum or (required and not value.strip()):
        raise ValueError(f"episode.{key} must be a string of at most {maximum} characters"
                         + (" and nonempty" if required else ""))
    return value.strip()


def _git(root: Path, *args: str) -> str:
    try:
        return guarded_git_text(root, *args).strip()
    except (ValueError, OSError) as exc:
        raise ValueError(f"safe Git source check failed: {exc}") from exc


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


def _reviewed_lesson_ids(root: Path, source_revision: str) -> set[str]:
    """A prior method must exist at the episode's cited revision, not only HEAD."""
    names = _git(root, "ls-tree", "-r", "-z", "--name-only", source_revision, "--",
                 ".sensemaking/knowledge").split(chr(0))
    lesson_ids: set[str] = set()
    for name in filter(None, names):
        if not name.endswith(".json"):
            continue
        data = json.loads(_git(root, "show", source_revision + ":" + name))
        for record in data.get("claims", []):
            if record.get("kind") == "lesson":
                lesson_ids.add(record["id"])
    return lesson_ids


def record_method_episode(repo: Path, episode_path: str, output_path: str) -> dict[str, Any]:
    """Create a new uncommitted Git-reviewable pack, never mutate reviewed policy.

    Every semantic assertion comes from the agent-authored, source-attributed
    episode. This is a materialization aid, not verification of that assertion.
    """
    repo = Path(repo).expanduser().resolve()
    root = Path(_git(repo, "rev-parse", "--show-toplevel")).resolve()
    episode_file, episode_relative = _relative(root, episode_path, existing=True)
    output_file, output_relative = _relative(root, output_path, existing=False)
    if (output_file.parent != root / ".sensemaking" / "knowledge"
            or not output_relative.endswith(".json")):
        raise ValueError("output must be a new .sensemaking/knowledge/*.json file")
    if output_file.exists():
        raise ValueError("output already exists; refusing to overwrite a proposal or reviewed record")

    if episode_file.stat().st_size > 131072:
        raise ValueError("episode source exceeds the 128 KiB bounded input limit")
    data = json.loads(episode_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("episode input must be a JSON object")
    accepted = {
        "episode_id", "actor", "source_revision", "decision", "disposition",
        "procedure_before", "procedure_after", "observed_result", "scope",
        "conditions", "counterevidence", "revisit_when", "claim_ceiling",
        "evidence_refs", "prior_lesson_id",
    }
    unknown = set(data) - accepted
    if unknown:
        raise ValueError(f"unknown episode fields: {sorted(unknown)}")
    episode_id = _string(data, "episode_id", maximum=72)
    if not _EPISODE_SLUG.fullmatch(episode_id):
        raise ValueError("episode_id must be a unique lowercase slug (3..71 characters)")
    disposition = _string(data, "disposition", maximum=16)
    if disposition not in _DISPOSITIONS:
        raise ValueError("disposition must be develop, adapt, apply, reject or no_change")
    if disposition == "no_change":
        return {
            "code": "SEMANTIC_METHOD_NO_MODEL_CHANGE",
            "created": False,
            "action_authorized": False,
            "note": "A method change is not warranted; no knowledge artifact was generated.",
        }

    actor = _string(data, "actor", maximum=160)
    source_revision = _string(data, "source_revision", maximum=40)
    if not _COMMIT.fullmatch(source_revision):
        raise ValueError("source_revision must be the exact 40-character source commit SHA")
    if _git(root, "rev-parse", "--verify", "--quiet", f"{source_revision}^{{commit}}") != source_revision:
        raise ValueError("the source_revision is not available as an exact local Git commit")

    decision = _string(data, "decision", maximum=1600)
    procedure_before = _string(data, "procedure_before", required=False)
    procedure_after = _string(data, "procedure_after", required=disposition in _METHOD_CHANGES)
    observed_result = _string(data, "observed_result")
    scope = _string(data, "scope")
    conditions = _string(data, "conditions", required=disposition in _METHOD_CHANGES)
    counterevidence = _string(data, "counterevidence", required=disposition in _METHOD_CHANGES)
    revisit_when = _string(data, "revisit_when", required=disposition in _METHOD_CHANGES)
    ceiling = _string(data, "claim_ceiling")
    previous = _string(data, "prior_lesson_id", required=False, maximum=160)

    if disposition in {"adapt", "apply", "reject"} and not previous:
        raise ValueError("adapt/apply/reject requires prior_lesson_id")
    if previous and not previous.startswith("lesson:"):
        raise ValueError("prior_lesson_id must name a reviewed lesson claim")
    if disposition in _METHOD_CHANGES:
        if not procedure_before:
            raise ValueError("method development needs an explicit earlier procedure for comparison")
        if procedure_after == procedure_before:
            raise ValueError("no changed procedure was supplied; do not claim adaptation")

    tracked = set(filter(None, _git(root, "ls-files", "-z").split("\0")))
    if episode_relative not in tracked:
        raise ValueError("stage or commit the originating episode file before preparing a reviewed proposal")
    if previous and previous not in _reviewed_lesson_ids(root, source_revision):
        raise ValueError("prior_lesson_id is absent from reviewed knowledge at source_revision")
    raw_evidence = data.get("evidence_refs")
    if (not isinstance(raw_evidence, list) or not 1 <= len(raw_evidence) <= 20
            or any(not isinstance(ref, str) or not ref.startswith("file:") for ref in raw_evidence)):
        raise ValueError("evidence_refs must be a nonempty list of tracked file: paths")
    for reference in raw_evidence:
        _, path = _relative(root, reference[5:], existing=True)
        if path not in tracked:
            raise ValueError(f"evidence file is not staged or committed: {path}")
    references = list(dict.fromkeys(["file:" + episode_relative, *raw_evidence]))
    # The source revision may legitimately precede a task's observed result.
    # Disclose that provenance distinction, without claiming chronology or
    # treating a post-decision outcome source as invalid.
    source_paths = set(filter(None, _git(
        root, "ls-tree", "-r", "-z", "--name-only", source_revision, "--",
    ).split(chr(0))))
    missing_at_source = sorted({ref[5:] for ref in references
                                if ref[5:] not in source_paths})

    observation_id = "observation:method-episode-" + episode_id
    lesson_id = "lesson:conditional-method-" + episode_id
    known_ids = _known_claim_ids(root, tracked)
    if observation_id in known_ids or lesson_id in known_ids:
        raise ValueError("method episode identifiers already exist in reviewed knowledge")

    observation = {
        "id": observation_id,
        "kind": "observation",
        "statement": ("Agent-authored method episode: " + observed_result),
        "authority_kind": "document",
        "authority_ref": episode_relative,
        "evidence_refs": references,
        "epistemic_status": "declared",
        "attributes": {
            "actor": actor,
            "source_revision": source_revision,
            "evidence_paths_not_in_source_revision": missing_at_source,
            "decision": decision,
            "method_disposition": disposition,
            "procedure_before": procedure_before or "NOT_RECORDED",
            "procedure_after": procedure_after or "NO_CHANGE_RECORDED",
            "scope": scope,
            "counterevidence": counterevidence or "NOT_ASSESSED",
            "claim_ceiling": ceiling,
            "prior_lesson_id": previous or "NONE",
        },
    }
    claims = [observation]
    relations = []
    if previous:
        relations.append({
            "id": "rel:method-episode-" + episode_id + "-references-prior",
            "subject": observation_id,
            "predicate": "references",
            "object": previous,
            "evidence_refs": references,
            "epistemic_status": "declared",
        })

    if disposition in _METHOD_CHANGES:
        claims.append({
            "id": lesson_id,
            "kind": "lesson",
            "statement": ("Conditional method candidate from episode " + episode_id +
                          ": " + procedure_after),
            "authority_kind": "document",
            "authority_ref": episode_relative,
            "evidence_refs": references,
            "epistemic_status": "declared",
            "attributes": {
                "method": procedure_after,
                "method_before": procedure_before,
                "actor": actor,
                "source_revision": source_revision,
                "scope": scope,
                "conditions": conditions,
                "counterevidence": counterevidence,
                "revisit_when": revisit_when,
                "original_outcome": observed_result,
                "claim_ceiling": ceiling,
                "method_disposition": disposition,
                "prior_lesson_id": previous or "NONE",
            },
        })
        relations.append({
            "id": "rel:method-episode-" + episode_id + "-learned-from",
            "subject": lesson_id,
            "predicate": "learned_from",
            "object": observation_id,
            "evidence_refs": references,
            "epistemic_status": "declared",
        })
        if previous:
            relations.append({
                "id": "rel:method-episode-" + episode_id + "-revises-candidate",
                "subject": lesson_id,
                "predicate": "references",
                "object": previous,
                "evidence_refs": references,
                "epistemic_status": "declared",
            })

    for item in claims:
        read_authored_claim(item, source_ref="file:" + output_relative, schema_version=2)
    for item in relations:
        read_authored_relation(item, source_ref="file:" + output_relative, schema_version=2)

    proposal = {"schema_version": 2, "claims": claims, "relations": relations}
    output_file.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation preserves any existing proposal and other agent's work.
    with output_file.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(proposal, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    return {
        "code": "SEMANTIC_METHOD_PROPOSAL_CREATED",
        "created": True,
        "path": output_relative,
        "episode_id": episode_id,
        "disposition": disposition,
        "proposed_claim_ids": [item["id"] for item in claims],
        "proposed_relation_ids": [item["id"] for item in relations],
        "source_revision": source_revision,
        "evidence_paths_not_in_source_revision": missing_at_source,
        "review_state": "UNREVIEWED_DRAFT",
        "semantic_truth_established": False,
        "method_learning_demonstrated": False,
        "action_authorized": False,
        "next": "Run knowledge-proposal-check, review episode sources and conditions, then use normal Git review; no automatic policy promotion.",
    }
