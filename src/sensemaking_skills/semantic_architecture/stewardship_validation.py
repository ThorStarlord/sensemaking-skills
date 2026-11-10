"""Read-only draft verification for Git-authored semantic records.

Proposals are often untracked or edited in a dirty engineering workspace.
The check validates, in memory and without writing, the record set that
knowledge-build would index if the working files were committed, using the
build's own readers and validator. Working bytes are never indexed as committed
architectural truth. Full source-pinned indexing continues to require a
separate CLEAN exact Git checkout.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .knowledge import (
    AUTHORED_SCHEMA_VERSIONS, KnowledgeClaim, KnowledgeRelation, KnowledgeSnapshot, fingerprint,
    read_authored_claim, read_authored_relation, record_dict,
)
from .knowledge_sources import (
    _adr_claims, _authored_records, _grounding_claims, _local_evidence_path, _source,
)
from .repository_bootstrap import structural_records

_MAX_PROPOSAL_BYTES = 524288


def _git(repo_root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=repo_root, capture_output=True, text=True,
        check=False, timeout=30,
    )
    if result.returncode:
        raise ValueError(f"Git source inspection failed: {result.stderr.strip()}")
    return result.stdout.strip()


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


def _build_refusal(
    target_ref: str,
    claims: list[KnowledgeClaim],
    relations: list[KnowledgeRelation],
    structural_only: dict[str, str],
) -> str | None:
    """Return the reason knowledge-build would refuse these records, or None.

    Runs the build's validator and snapshot serialization (fingerprint); the
    earlier checks only add the record id and file to the common refusals.
    """
    first_claim: dict[str, KnowledgeClaim] = {}
    for claim in claims:
        previous = first_claim.get(claim.id)
        if previous is not None:
            return f"duplicate claim id {claim.id}: defined in {previous.source_ref} and {claim.source_ref}"
        first_claim[claim.id] = claim
    first_relation: dict[str, KnowledgeRelation] = {}
    for relation in relations:
        previous = first_relation.get(relation.id)
        if previous is not None:
            return f"duplicate relation id {relation.id}: defined in {previous.source_ref} and {relation.source_ref}"
        first_relation[relation.id] = relation
    for relation in relations:
        for endpoint in (relation.subject, relation.object):
            if endpoint not in first_claim:
                hint = (
                    f" (structural id of {structural_only[endpoint]}, indexed only with --include-repository-structure)"
                    if endpoint in structural_only else ""
                )
                return f"unresolved relationship endpoint {endpoint}{hint}: relation {relation.id} in {relation.source_ref}"
    for record in [*claims, *relations]:
        try:
            json.dumps(record_dict(record), ensure_ascii=False, allow_nan=False).encode("utf-8")
        except ValueError:
            return f"record cannot be serialized as UTF-8 JSON: {record.id} in {record.source_ref}"
    try:
        fingerprint(KnowledgeSnapshot(
            repository="proposal-validation-only", target_ref=target_ref,
            claims=tuple(claims), relations=tuple(relations),
            source_scope=("proposed non-authoritative working records",),
            limits=("Uncommitted proposals and dirty source bytes are not authoritative.",),
        ))
    except ValueError as exc:
        return str(exc)
    return None


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
    tracked = set(filter(None, _git(root, "ls-files", "-z").split("\0")))
    worktree_clean = not bool(_git(root, "status", "--porcelain", "--untracked-files=all"))
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

    id_list = [item.id for item in claims]
    duplicated = sorted({identifier for identifier in id_list if id_list.count(identifier) > 1})
    if duplicated:
        raise ValueError(f"duplicate authored claim ids: {', '.join(duplicated)}")
    candidate_ids = set(id_list)
    needed = {id for rel in relations for id in (rel.subject, rel.object)}
    needed.update(rel.attributes["carries"] for rel in relations
                  if rel.predicate == "flows_to" and isinstance(rel.attributes.get("carries"), str))
    for claim in claims:
        if claim.kind == "architecture_rule":
            needed.update(claim.attributes.get("allowed_targets", []) or [])
            needed.update(claim.attributes.get("forbidden_targets", []) or [])

    # The tracked set a commit of the current working files would have: paths
    # deleted in the worktree are gone, the proposal is present. The build's own
    # readers run over it in memory; nothing is written to disk.
    deleted = set(filter(None, _git(root, "ls-files", "--deleted", "-z").split("\0")))
    committed = (tracked - deleted) | {relative}
    try:
        base =[*_grounding_claims(root, committed), *_adr_claims(root, committed)]
        authored_claims, authored_relations = _authored_records(root, committed)
    except ValueError as exc:
        raise ValueError(f"knowledge-build would refuse a commit of these working files: {exc}") from exc
    try:
        structural_claims, structural_relations, _ = structural_records(root, committed)
    except ValueError as exc:
        raise ValueError(
            f"knowledge-build --include-repository-structure would refuse a commit of these working files: {exc}"
        ) from exc
    structural_only = {claim.id: claim.statement for claim in structural_claims}
    default_reason = _build_refusal(
        target_ref, [*base, *authored_claims], list(authored_relations), structural_only,
    )
    extended_reason = _build_refusal(
        target_ref, [*base, *authored_claims, *structural_claims],
        [*authored_relations, *structural_relations], structural_only,
    )
    if default_reason is not None or extended_reason is not None:
        if default_reason == extended_reason:
            raise ValueError(
                "knowledge-build would refuse a commit of these working files "
                f"(default and --include-repository-structure builds): {default_reason}"
            )
        default_text = f"refuses: {default_reason}" if default_reason is not None else "accepts"
        extended_text = f"refuses: {extended_reason}" if extended_reason is not None else "accepts"
        raise ValueError(
            "knowledge-build would refuse a commit of these working files; "
            f"default build: {default_text}; "
            f"--include-repository-structure build: {extended_text}"
        )

    other_packs = [
        line.strip() for line in _git(root, "diff", "--name-only", "HEAD", "--", ".sensemaking/knowledge").splitlines()
        if line.strip() and line.strip().endswith(".json")
    ]
    return {
        "code": "SEMANTIC_KNOWLEDGE_PROPOSAL_VALID",
        "valid": True,
        "proposal": relative,
        "head_sha": target_ref,
        "worktree_clean": worktree_clean,
        "claims_checked": len(claims),
        "relations_checked": len(relations),
        "existing_endpoints_checked": len(needed - candidate_ids),
        "local_evidence_paths_checked": sorted(evidence),
        "knowledge_build_configurations_checked": ["default", "--include-repository-structure"],
        "other_modified_knowledge_packs": sorted(p for p in other_packs if p != relative),
        "semantic_truth_established": False,
        "authority_verified": False,
        "action_authorized": False,
        "limits": [
            "The source and referenced paths were inspected in the CURRENT WORKTREE, possibly dirty.",
            "Schema/path checks are not semantic truth, owner intent or behavioral verification.",
            "Full semantic knowledge indexing requires an exact clean committed Git HEAD.",
            "valid predicts that the default knowledge-build and the --include-repository-structure build accept a commit of the current working files: this proposal, the tracked knowledge packs (including other_modified_knowledge_packs) and the cited sources as checked. --include-python-imports and other untracked knowledge files are not simulated.",
        ],
    }
