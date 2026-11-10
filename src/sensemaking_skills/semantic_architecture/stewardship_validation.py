"""Read-only draft verification for Git-authored semantic records.

Proposals are often untracked or edited in a dirty engineering workspace.
This checks schema, references, identity and linkage without indexing those
working bytes as committed architectural truth. Full source-pinned indexing
continues to require a separate CLEAN exact Git checkout.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from .knowledge import (
    AUTHORED_SCHEMA_VERSIONS, KnowledgeClaim, KnowledgeSnapshot, read_authored_claim,
    read_authored_relation, stable_id, validate_snapshot,
)
from .knowledge_sources import _local_evidence_path, _source, _validate_authored_contract_flows

_ADR_PATH = re.compile(r"docs/adr/(\d{3,4})-[^/]+\.md\Z")
_MAX_PROPOSAL_BYTES = 524288


def _git(repo_root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=repo_root, capture_output=True, text=True,
        check=False, timeout=30,
    )
    if result.returncode:
        raise ValueError(f"Git source inspection failed: {result.stderr.strip()}")
    return result.stdout.strip()


def _head_pack(root: Path, relative: str) -> dict:
    """Read a reviewed pack at HEAD, never its possibly dirty worktree bytes."""
    result = subprocess.run(
        ["git", "show", f"HEAD:{relative}"], cwd=root,
        capture_output=True, check=False, timeout=30,
    )
    if result.returncode:
        raise ValueError(f"cannot read committed knowledge pack at HEAD: {relative}")
    data = json.loads(result.stdout.decode("utf-8"))
    if (
        not isinstance(data, dict)
        or data.get("schema_version") not in AUTHORED_SCHEMA_VERSIONS
        or not isinstance(data.get("claims"), list)
        or not isinstance(data.get("relations"), list)
    ):
        raise ValueError(f"invalid committed authored knowledge: {relative}")
    return data


def _safe_proposal(root: Path, proposal: Path) -> tuple[Path, str]:
    candidate = proposal if proposal.is_absolute() else root / proposal
    relative = candidate.absolute().relative_to(root)
    if (
        not relative.parts or ".." in relative.parts
        or len(relative.parts) != 3
        or relative.parts[:2] != (".sensemaking", "knowledge")
        or relative.suffix != ".json"
    ):
        raise ValueError("proposal must be a JSON file under .sensemaking/knowledge/")
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"symlink proposal refused: {relative}")
    if not candidate.is_file() or candidate.stat().st_size > _MAX_PROPOSAL_BYTES:
        raise ValueError("proposal missing or exceeds 512 KiB")
    if not candidate.resolve().is_relative_to(root):
        raise ValueError("proposal escapes repository")
    return candidate, relative.as_posix()


def inspect_knowledge_proposal(repo_root: Path, proposal: Path) -> dict:
    """Inspect proposed authored knowledge without clean-worktree requirements.

    The result is a mechanical preflight, NEVER semantic review/acceptance.
    All referenced local evidence must be Git tracked even for dirty proposals.
    """
    root = repo_root.resolve()
    if not (root / ".git").exists():
        raise ValueError("target must be a Git checkout")
    path, relative = _safe_proposal(root, proposal)
    target_ref = _git(root, "rev-parse", "HEAD")
    committed = set(filter(None, _git(root, "ls-tree", "-r", "-z", "--name-only", "HEAD").split(chr(0))))
    tracked = set(filter(None, _git(root, "ls-files", "-z").split("\0")))
    worktree_clean = not bool(_git(root, "--no-optional-locks", "status", "--porcelain", "--untracked-files=all"))
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"schema_version", "claims", "relations"}:
        raise ValueError("proposal must contain exactly schema_version, claims and relations")
    if data["schema_version"] not in AUTHORED_SCHEMA_VERSIONS or not isinstance(data["claims"], list) or not isinstance(data["relations"], list):
        raise ValueError("proposal must use an authored semantic schema_version (1 or 2) with array records")
    if len(data["claims"]) > 500 or len(data["relations"]) > 1000:
        raise ValueError("proposal exceeds authored record limits")
    version = data["schema_version"]
    claims = [read_authored_claim(item, source_ref=f"file:{relative}", schema_version=version) for item in data["claims"]]
    relations = [read_authored_relation(item, source_ref=f"file:{relative}", schema_version=version) for item in data["relations"]]
    evidence: set[str] = set()
    for item in [*claims, *relations]:
        for ref in item.evidence_refs:
            local = _local_evidence_path(ref)
            if local is not None:
                _source(root, tracked, local)
                evidence.add(local)
        if isinstance(item, KnowledgeClaim):
            for owned_path in item.attributes.get("owned_paths", []):
                _source(root, tracked, owned_path)
                evidence.add(owned_path)
        if isinstance(item, KnowledgeClaim) and item.authority_kind in {"policy", "code", "test"}:
            _source(root, tracked, item.authority_ref)
            evidence.add(item.authority_ref)

    # This is a SINGLE-PACK draft preflight, not a prospective commit.
    # The selected file and referenced, index-tracked evidence use WORKTREE bytes;
    # other authored packs use committed HEAD bytes (not their dirty overlays).
    candidate_ids = {item.id for item in claims}
    if len(candidate_ids) != len(claims):
        raise ValueError("duplicate authored claim ids")
    candidate_relation_ids = {item.id for item in relations}
    if len(candidate_relation_ids) != len(relations):
        raise ValueError("duplicate authored relation ids")

    known_ids = set(candidate_ids)
    path_only_ids: set[str] = set()
    external_kinds: dict[str, str] = {}
    external_attributes: dict[str, dict] = {}
    external_claim_origins: dict[str, str] = {}
    external_relation_origins: dict[str, str] = {}
    external_relations: list[tuple[str, int, dict]] = []
    external_rule_refs: list[tuple[str, str, str]] = []
    previous_ids: set[str] = set()

    for name in sorted(tracked):
        match = _ADR_PATH.fullmatch(name)
        if match:
            known_ids.add(f"adr:{match.group(1)}")
        file_id = stable_id("file", name)
        known_ids.add(file_id)
        path_only_ids.add(file_id)
        parts = Path(name).parts
        for depth in range(1, len(parts)):
            directory_id = stable_id("directory", Path(*parts[:depth]).as_posix())
            known_ids.add(directory_id)
            path_only_ids.add(directory_id)

    for name in sorted(committed):
        if not name.startswith(".sensemaking/knowledge/") or not name.endswith(".json"):
            continue
        other = _head_pack(root, name)
        if name == relative:
            previous_ids = {
                record["id"] for record in other["claims"]
                if isinstance(record, dict) and isinstance(record.get("id"), str)
            }
            continue
        for record in other["claims"]:
            if not isinstance(record, dict) or not isinstance(record.get("id"), str):
                continue
            identifier = record["id"]
            known_ids.add(identifier)
            external_claim_origins.setdefault(identifier, name)
            if isinstance(record.get("kind"), str):
                external_kinds[identifier] = record["kind"]
            if isinstance(record.get("attributes"), dict):
                external_attributes[identifier] = record["attributes"]
                if record.get("kind") == "architecture_rule":
                    for key in ("allowed_targets", "forbidden_targets", "applies_to"):
                        values = record["attributes"].get(key, [])
                        if isinstance(values, list):
                            external_rule_refs.extend(
                                (name, identifier, value) for value in values
                                if isinstance(value, str)
                            )
        for record in other["relations"]:
            if not isinstance(record, dict):
                continue
            if isinstance(record.get("id"), str):
                external_relation_origins.setdefault(record["id"], name)
            external_relations.append((name, other["schema_version"], record))

    for item in claims:
        if item.id in external_claim_origins:
            raise ValueError(
                f"duplicate claim id across packs: {item.id} in {relative} "
                f"conflicts with committed {external_claim_origins[item.id]}"
            )
    for item in relations:
        if item.id in external_relation_origins:
            raise ValueError(
                f"duplicate relation id across packs: {item.id} in {relative} "
                f"conflicts with committed {external_relation_origins[item.id]}"
            )

    # Check incoming relationships whose meaning changes when this pack changes.
    # Do not validate unrelated HEAD packs wholesale: that is knowledge-build's job.
    affected_ids = previous_ids | candidate_ids
    incoming_relations = []
    for name, version, raw in external_relations:
        attrs = raw.get("attributes", {})
        carries = attrs.get("carries") if isinstance(attrs, dict) else None
        if any(value in affected_ids for value in (raw.get("subject"), raw.get("object"), carries)):
            incoming_relations.append(read_authored_relation(
                raw, source_ref=f"file:{name}", schema_version=version,
            ))

    checked_relations = [*relations, *incoming_relations]
    needed = {identifier for rel in checked_relations
              for identifier in (rel.subject, rel.object)}
    needed.update(
        rel.attributes["carries"] for rel in checked_relations
        if rel.predicate == "flows_to" and isinstance(rel.attributes.get("carries"), str)
    )
    for claim in claims:
        if claim.kind == "architecture_rule":
            needed.update(claim.attributes.get("allowed_targets", []) or [])
            needed.update(claim.attributes.get("forbidden_targets", []) or [])

    removed = previous_ids - candidate_ids
    broken_rule_refs = [
        f"{identifier} in {name} references {ref}"
        for name, identifier, ref in external_rule_refs if ref in removed
    ]
    if broken_rule_refs:
        raise ValueError("proposal removes claim referenced by a committed rule: "
                         + "; ".join(broken_rule_refs[:10]))
    missing = needed - known_ids
    if missing:
        raise ValueError(f"unresolved relationship endpoint(s): {', '.join(sorted(missing)[:15])}")

    # Placeholder endpoints are restricted to in-memory validation. They are
    # NEVER indexed, persisted, displayed as factual claims or marked verified.
    # Their identity and kind are checked; their own attributes and rule scope
    # are not, because the owning file is validated where it is read.
    external_ids = frozenset(needed - candidate_ids)
    placeholders = [
        KnowledgeClaim(
            id=identifier, kind=external_kinds.get(identifier, "hypothesis"),
            statement="External endpoint, source not semantically reviewed",
            epistemic_status="hypothetical", authority_kind="hypothesis",
            authority_ref="proposal-validation-only", source_ref="proposal-validation-only",
            evidence_refs=("proposal-validation-only",),
        )
        for identifier in sorted(external_ids)
    ]
    validate_snapshot(KnowledgeSnapshot(
        repository="proposal-validation-only", target_ref=target_ref,
        claims=tuple([*claims, *placeholders]), relations=tuple(checked_relations),
        source_scope=("proposed non-authoritative working records",),
        limits=("Uncommitted proposals and dirty source bytes are not authoritative.",),
    ), existence_only_ids=external_ids)
    # Reuse the exact build-side artifact-contract flow adapter for any flows
    # directly changed by this pack. Unrelated flows remain out of scope.
    flow_claims = [
        KnowledgeClaim(**{**item.__dict__, "attributes": external_attributes.get(item.id, {})})
        for item in placeholders
    ]
    _validate_authored_contract_flows(root, tracked, [*claims, *flow_claims], checked_relations)

    dirty_packs = set(filter(None, _git(
        root, "diff", "--name-only", "-z", "HEAD", "--", ".sensemaking/knowledge",
    ).split(chr(0))))
    dirty_packs.update(filter(None, _git(
        root, "ls-files", "--others", "--exclude-standard", "-z", "--", ".sensemaking/knowledge",
    ).split(chr(0))))
    staged_packs = set(filter(None, _git(
        root, "diff", "--cached", "--name-only", "-z", "--", ".sensemaking/knowledge",
    ).split(chr(0))))
    return {
        "code": "SEMANTIC_KNOWLEDGE_PROPOSAL_VALID",
        "valid": True,
        "proposal": relative,
        "head_sha": target_ref,
        "worktree_clean": worktree_clean,
        "validation_scope": "single_proposed_pack_against_HEAD_packs_and_worktree_evidence",
        "proposal_bytes_source": "working_file_not_staged_blob",
        "other_packs_source": "committed_HEAD_only",
        "staged_other_packs_ignored": sorted(staged_packs - {relative}),
        "dirty_other_packs_ignored": sorted(dirty_packs - {relative}),
        "affected_incoming_relations_checked": len(incoming_relations),
        "structural_path_endpoints_only": sorted(
            (needed - candidate_ids) & (path_only_ids - set(external_kinds))
        ),
        "build_equivalence_established": False,
        "build_modes_checked": [],
        "claims_checked": len(claims),
        "relations_checked": len(relations),
        "existing_endpoints_checked": len(needed - candidate_ids),
        "local_evidence_paths_checked": sorted(evidence),
        "semantic_truth_established": False,
        "authority_verified": False,
        "action_authorized": False,
        "limits": [
            "Selected proposal and index-tracked cited evidence use CURRENT WORKTREE bytes, not staged content.",
            "Other authored knowledge packs use committed HEAD bytes; dirty, deleted or untracked other packs are ignored.",
            "Only relationships referencing this pack are checked across pack boundaries; unrelated pack defects are not assessed.",
            "File/directory endpoint existence does not show that a chosen structural build indexes those records.",
            "No prospective commit, default/structural/import build configuration or SQLite persistence was validated.",
            "Schema/path checks are not semantic truth, owner intent or behavioral verification.",
            "Full semantic knowledge indexing requires an exact clean committed Git HEAD.",
        ],
    }
