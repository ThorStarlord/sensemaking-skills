"""Optional consequence-informed decision review over architecture options or product possibilities.

A review is a later `decision` claim that references the option, the predictions
and assessments it reconsidered, and optionally the method precedent that guided
the review. It never rewrites the source option or possibility, its preference or disposition, never changes
standing automatically, and never promotes the option. The active agent authors
the judgment; this module only validates and materializes its source-attributed
record as a Git-reviewable proposal.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

from .semantic_architecture.consequence_standing import assessment_supersession
from .semantic_architecture.knowledge import read_authored_claim, read_authored_relation
from .semantic_architecture.worktree_context import guarded_git_text

_REVIEW_SLUG = re.compile(r"[a-z0-9][a-z0-9-]{2,70}\Z")
_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_DISPOSITIONS = frozenset({
    "reaffirm", "revise", "reopen", "investigate",
    "retain_with_limitation", "reject", "no_change",
})
_MAX_TEXT = 2400
_MAX_REFS = 20


def _string(data: Mapping[str, Any], key: str, *, required: bool = True,
            maximum: int = _MAX_TEXT) -> str:
    value = data.get(key, "")
    if not isinstance(value, str) or len(value) > maximum or (required and not value.strip()):
        raise ValueError(
            f"episode.{key} must be a string of at most {maximum} characters"
            + (" and nonempty" if required else "")
        )
    return value.strip()


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


def _git(root: Path, *args: str) -> str:
    try:
        return guarded_git_text(root, *args).strip()
    except (ValueError, OSError) as exc:
        raise ValueError(f"safe Git source check failed: {exc}") from exc


def _knowledge_at_revision(
    root: Path, revision: str,
) -> tuple[dict[str, dict], list[dict]]:
    """Read authored claims and relations as reviewed at the exact source revision."""
    names = _git(root, "ls-tree", "-r", "-z", "--name-only", revision,
                 "--", ".sensemaking/knowledge").split(chr(0))
    claims: dict[str, dict] = {}
    relations: list[dict] = []
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
        for record in data.get("relations", []):
            if not isinstance(record, dict):
                raise ValueError("authored knowledge has an invalid relation")
            relations.append(record)
    return claims, relations


def _tracked_paths(root: Path) -> set[str]:
    return set(filter(None, _git(root, "ls-files", "-z").split(chr(0))))


def record_decision_review(
    repo: Path, episode_path: str, output_path: str, *, draft_only: bool = False,
) -> dict[str, Any]:
    """Create a new uncommitted review proposal; never mutate the reviewed option."""
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
        raise ValueError("output already exists; refusing to overwrite a proposal or reviewed record")
    if episode_file.stat().st_size > 131072:
        raise ValueError("episode source exceeds the 128 KiB bounded input limit")

    data = json.loads(episode_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("episode input must be a JSON object")
    accepted = {
        "review_id", "actor", "source_revision", "source_option", "source_possibility", "disposition",
        "basis", "conditions", "counterevidence", "claim_ceiling",
        "evidence_refs", "consequence_refs", "assessment_refs", "method_ref",
    }
    unknown = set(data) - accepted
    if unknown:
        raise ValueError(f"unknown episode fields: {sorted(unknown)}")

    review_id = _string(data, "review_id", maximum=72)
    if not _REVIEW_SLUG.fullmatch(review_id):
        raise ValueError("review_id must be a lowercase slug (3..71 characters)")
    actor = _string(data, "actor", maximum=160)
    source_revision = _string(data, "source_revision", maximum=40)
    if not _COMMIT.fullmatch(source_revision):
        raise ValueError("source_revision must be the exact 40-character source commit SHA")
    if _git(root, "rev-parse", "--verify", "--quiet", f"{source_revision}^{{commit}}") != source_revision:
        raise ValueError("the source_revision is not available as an exact local Git commit")

    if ("source_option" in data) == ("source_possibility" in data):
        raise ValueError("provide exactly one source_option or source_possibility")
    possibility_review = "source_possibility" in data
    source_key = "source_possibility" if possibility_review else "source_option"
    source_option = _string(data, source_key, maximum=160)
    if possibility_review:
        if not source_option.startswith("poss:"):
            raise ValueError("source_possibility must name an authored poss: opportunity")
    elif not source_option.startswith("arch:"):
        raise ValueError("source_option must name an authored arch: architecture option")
    disposition = _string(data, "disposition", maximum=32)
    if disposition not in _DISPOSITIONS:
        raise ValueError(f"disposition must be one of {sorted(_DISPOSITIONS)}")
    basis = _string(data, "basis")
    conditions = _string(data, "conditions")
    counterevidence = _string(data, "counterevidence")
    ceiling = _string(data, "claim_ceiling")
    method_ref = _string(data, "method_ref", required=False, maximum=160)
    if method_ref and not method_ref.startswith("lesson:"):
        raise ValueError("method_ref must name an authored lesson claim")

    tracked = _tracked_paths(root)
    if episode_relative not in tracked:
        raise ValueError("stage or commit the review episode file before preparing a proposal")

    consequence_refs = data.get("consequence_refs")
    if (not isinstance(consequence_refs, list) or not 1 <= len(consequence_refs) <= _MAX_REFS
            or any(not isinstance(item, str) or not item.startswith("conseq:")
                   for item in consequence_refs)):
        raise ValueError("consequence_refs must be 1..20 authored conseq: ids")
    consequence_refs = list(dict.fromkeys(consequence_refs))

    assessment_refs = data.get("assessment_refs", [])
    if (not isinstance(assessment_refs, list) or len(assessment_refs) > _MAX_REFS
            or any(not isinstance(item, str) for item in assessment_refs)):
        raise ValueError("assessment_refs must be at most 20 authored observation ids")
    assessment_refs = list(dict.fromkeys(assessment_refs))

    raw_evidence = data.get("evidence_refs")
    if (not isinstance(raw_evidence, list) or not 1 <= len(raw_evidence) <= _MAX_REFS
            or any(not isinstance(ref, str) or not ref.startswith("file:") for ref in raw_evidence)):
        raise ValueError("evidence_refs must be a nonempty list of tracked file: paths")
    for reference in raw_evidence:
        _, path = _relative(root, reference[5:], existing=True)
        if path not in tracked:
            raise ValueError(f"evidence file is not staged or committed: {path}")
    references = list(dict.fromkeys(["file:" + episode_relative, *raw_evidence]))

    claims, relations = _knowledge_at_revision(root, source_revision)
    option = claims.get(source_option)
    if possibility_review:
        if not option or option.get("kind") != "opportunity":
            raise ValueError("source_possibility must be an authored opportunity at source_revision")
    else:
        if not option or option.get("kind") != "alternative":
            raise ValueError("source_option must be an authored alternative at source_revision")
        preference = (option.get("attributes") or {}).get("preference")
        if not isinstance(preference, Mapping) or not isinstance(preference.get("status"), str):
            raise ValueError("source_option needs an authored preference status")

    for consequence in consequence_refs:
        record = claims.get(consequence)
        if not record or record.get("kind") != "hypothesis":
            raise ValueError(f"consequence_ref is not an authored hypothesis: {consequence}")
        attributes = record.get("attributes") or {}
        if attributes.get(source_key) != source_option:
            raise ValueError(f"consequence does not belong to {source_option}: {consequence}")
        if possibility_review and (
            "source_option" in attributes or not any(
                edge.get("subject") == consequence and edge.get("predicate") == "references"
                and edge.get("object") == source_option for edge in relations
            )
        ):
            raise ValueError(f"consequence lacks an unambiguous authored possibility link: {consequence}")

    superseded_by, cyclic = assessment_supersession(claims, relations)
    for assessment in assessment_refs:
        record = claims.get(assessment)
        if not record or record.get("kind") != "observation":
            raise ValueError(f"assessment_ref is not an authored observation: {assessment}")
        attributes = record.get("attributes") or {}
        if attributes.get("consequence_ref") not in consequence_refs:
            raise ValueError(f"assessment does not resolve a cited consequence: {assessment}")
        # Match consequence-standing semantics: an authored SUPERSEDED status is
        # historical evidence, and a same-prediction supersedes edge makes the
        # target inactive unless it participates in an invalid cycle. A cycle
        # keeps its members active instead of erasing standing.
        relation_superseded = assessment in superseded_by and assessment not in cyclic
        if attributes.get("assessment_status") == "SUPERSEDED" or relation_superseded:
            replacements = sorted(superseded_by.get(assessment, ()))
            reason = (
                "same-prediction supersession by " + ", ".join(replacements)
                if replacements else "an authored SUPERSEDED status"
            )
            raise ValueError(
                f"assessment_ref is not active at source_revision ({reason}): {assessment}"
            )

    if method_ref:
        lesson = claims.get(method_ref)
        if not lesson or lesson.get("kind") != "lesson":
            raise ValueError("method_ref is not an authored lesson at source_revision")
        if not isinstance((lesson.get("attributes") or {}).get("method"), str):
            raise ValueError("method_ref lesson has no authored method")

    decision_id = "decision:review-" + review_id
    if decision_id in claims:
        raise ValueError("decision review identifier already exists in reviewed knowledge")

    source_paths = set(filter(None, _git(
        root, "ls-tree", "-r", "-z", "--name-only", source_revision, "--",
    ).split(chr(0))))
    missing_at_source = sorted({ref[5:] for ref in references if ref[5:] not in source_paths})

    statement = (
        "Consequence-informed decision review at " + source_revision[:10] + ": " +
        disposition + " for " + source_option + ". " + basis
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
            "concept": "DecisionReview",
            "review_of": source_option,
            "disposition": disposition,
            "basis": basis,
            "conditions": conditions,
            "counterevidence": counterevidence,
            "claim_ceiling": ceiling,
            "source_revision": source_revision,
            "actor": actor,
            "consequence_refs": consequence_refs,
            "assessment_refs": assessment_refs,
            "method_ref": method_ref or "NONE",
            "agent_owned": True,
        },
    }
    relations = [{
        "id": ("rel:decision-review-" + review_id
               + ("-references-possibility" if possibility_review else "-references-option")),
        "subject": decision_id,
        "predicate": "references",
        "object": source_option,
        "evidence_refs": references,
        "epistemic_status": "declared",
    }]
    for index, consequence in enumerate(consequence_refs, start=1):
        relations.append({
            "id": "rel:decision-review-" + review_id + "-references-consequence-" + str(index),
            "subject": decision_id,
            "predicate": "references",
            "object": consequence,
            "evidence_refs": references,
            "epistemic_status": "declared",
        })
    for index, assessment in enumerate(assessment_refs, start=1):
        relations.append({
            "id": "rel:decision-review-" + review_id + "-references-assessment-" + str(index),
            "subject": decision_id,
            "predicate": "references",
            "object": assessment,
            "evidence_refs": references,
            "epistemic_status": "declared",
        })
    if method_ref:
        relations.append({
            "id": "rel:decision-review-" + review_id + "-learned-from-method",
            "subject": decision_id,
            "predicate": "learned_from",
            "object": method_ref,
            "evidence_refs": references,
            "epistemic_status": "declared",
        })

    read_authored_claim(decision, source_ref="file:" + output_relative, schema_version=2)
    for relation in relations:
        read_authored_relation(relation, source_ref="file:" + output_relative, schema_version=2)

    proposal = {"schema_version": 2, "claims": [decision], "relations": relations}
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(proposal, stream, indent=2, ensure_ascii=False)
        stream.write("\n")

    return {
        "code": "SEMANTIC_DECISION_REVIEW_CREATED",
        "created": True,
        "path": output_relative,
        "review_id": review_id,
        source_key: source_option,
        "disposition": disposition,
        "proposed_claim_ids": [decision_id],
        "proposed_relation_ids": [item["id"] for item in relations],
        "source_revision": source_revision,
        "evidence_paths_not_in_source_revision": missing_at_source,
        "review_state": "UNREVIEWED_DRAFT",
        **({"detached_draft": True, "inside_active_knowledge": False} if draft_only else {}),
        "semantic_truth_established": False,
        "decision_influence_established": False,
        "action_authorized": False,
        "next": (
            ("Run knowledge-proposal-check with an explicit new --destination, "
             "review the cited sources and copy the checked bytes to the authorized destination "
             "and preflight again; " if draft_only else "Run knowledge-proposal-check, ")
            + ("review the original possibility and cited evidence, "
               "then use normal Git review; the review does not change realization or disposition."
               if possibility_review else
               "review the original option and cited evidence, "
               "then use normal Git review; the review does not change the option or its preference.")
        ),
    }
