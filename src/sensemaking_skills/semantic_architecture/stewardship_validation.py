"""Read-only draft verification for Git-authored semantic records.

Proposals are often untracked or edited in a dirty engineering workspace.
This checks a proposal as the commit that would add it sees it: the committed
HEAD tree and the other committed reviewed packs, plus the proposal's working
bytes in place of its committed version. It runs the same snapshot assembly and
validation as ``knowledge-build``, so a valid result means that build accepts
the commit, while nothing is indexed, written or treated as semantic truth.
Full source-pinned indexing continues to require a separate CLEAN exact Git checkout.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from .knowledge import (
    AUTHORED_SCHEMA_VERSIONS, KnowledgeClaim, read_authored_claim,
    read_authored_relation, stable_id,
)
from .knowledge_sources import _local_evidence_path, _source, assemble_knowledge_snapshot

_ADR_PATH = re.compile(r"docs/adr/(\d{3,4})-[^/]+\.md\Z")
_MAX_PROPOSAL_BYTES = 524288
_PROPOSAL_REPOSITORY = "proposal-validation-only"


def _git(repo_root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=repo_root, capture_output=True, text=True,
        check=False, timeout=30,
    )
    if result.returncode:
        raise ValueError(f"Git source inspection failed: {result.stderr.strip()}")
    return result.stdout.strip()


def _committed_blob(repo_root: Path, name: str) -> str:
    result = subprocess.run(
        ["git", "cat-file", "blob", f"HEAD:{name}"], cwd=repo_root,
        capture_output=True, check=False, timeout=30,
    )
    if result.returncode:
        raise ValueError(f"committed pack unreadable at HEAD: {name}")
    return result.stdout.decode("utf-8")


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


def _committed_documents(root: Path, committed: set[str], relative: str, proposal_text: str) -> dict[str, str]:
    """Committed reviewed packs, with the proposal's working text standing in for its own path."""
    documents: dict[str, str] = {}
    for name in sorted(committed):
        if name == relative or not name.startswith(".sensemaking/knowledge/") or not name.endswith(".json"):
            continue
        documents[name] = _committed_blob(root, name)
    documents[relative] = proposal_text
    return documents


def _build_refusal(default_error: ValueError | None, structure_error: ValueError | None) -> ValueError | None:
    if default_error is not None:
        note = (" The opt-in --include-repository-structure build accepts it; the default build does not."
                if structure_error is None else "")
        return ValueError(f"knowledge-build would reject this proposal after commit (default options): {default_error}{note}")
    if structure_error is not None:
        return ValueError(f"knowledge-build would reject this proposal after commit with --include-repository-structure: {structure_error}")
    return None


def inspect_knowledge_proposal(repo_root: Path, proposal: Path) -> dict:
    """Preflight a proposed authored pack as the commit that adds it.

    The result is a mechanical preflight, NEVER semantic review/acceptance.
    All referenced local evidence must be committed (tracked at HEAD).
    """
    root = repo_root.resolve()
    if not (root / ".git").exists():
        raise ValueError("target must be a Git checkout")
    path, relative = _safe_proposal(root, proposal)
    target_ref = _git(root, "rev-parse", "HEAD")
    committed = set(filter(None, _git(root, "ls-tree", "-r", "-z", "--name-only", "HEAD").split("\0")))
    # --no-optional-locks: a status read must not refresh and rewrite .git/index.
    worktree_clean = not bool(_git(root, "--no-optional-locks", "status", "--porcelain", "--untracked-files=all"))
    proposal_text = path.read_text(encoding="utf-8")
    data = json.loads(proposal_text)
    if not isinstance(data, dict) or set(data) != {"schema_version", "claims", "relations"}:
        raise ValueError("proposal must contain exactly schema_version, claims and relations")
    if data["schema_version"] not in AUTHORED_SCHEMA_VERSIONS or not isinstance(data["claims"], list) or not isinstance(data["relations"], list):
        raise ValueError("proposal must use an authored semantic schema_version (1 or 2) with array records")
    if len(data["claims"]) > 500 or len(data["relations"]) > 1000:
        raise ValueError("proposal exceeds authored record limits")
    version = data["schema_version"]
    tracked = committed | {relative}
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

    documents = _committed_documents(root, committed, relative, proposal_text)
    known_ids: set[str] = set()
    for name in sorted(committed):
        match = _ADR_PATH.fullmatch(name)
        if match:
            known_ids.add(f"adr:{match.group(1)}")
        known_ids.add(stable_id("file", name))
        parts = Path(name).parts
        for depth in range(1, len(parts)):
            known_ids.add(stable_id("directory", Path(*parts[:depth]).as_posix()))
    for name, text in documents.items():
        if name == relative:
            continue
        other = json.loads(text)
        if not isinstance(other, dict) or not isinstance(other.get("claims"), list):
            raise ValueError(f"invalid pre-existing authored knowledge: {name}")
        known_ids.update(record["id"] for record in other["claims"]
                         if isinstance(record, dict) and isinstance(record.get("id"), str))
    known_ids.update(c.id for c in claims)

    candidate_ids = {item.id for item in claims}
    if len(candidate_ids) != len(claims):
        raise ValueError("duplicate authored claim ids")
    needed = {id for rel in relations for id in (rel.subject, rel.object)}
    needed.update(rel.attributes["carries"] for rel in relations
                  if rel.predicate == "flows_to" and isinstance(rel.attributes.get("carries"), str))
    for claim in claims:
        if claim.kind == "architecture_rule":
            needed.update(claim.attributes.get("allowed_targets", []) or [])
            needed.update(claim.attributes.get("forbidden_targets", []) or [])
    missing = needed - known_ids
    if missing:
        raise ValueError(f"unresolved relationship endpoint(s): {', '.join(sorted(missing)[:15])}")

    # The same assembly and validate_snapshot as knowledge-build, over the
    # committed packs plus this proposal. The default build is the primary
    # contract; the opt-in structure build is checked too, so both agree.
    def assemble(include_structure: bool):
        return assemble_knowledge_snapshot(
            root, tracked, repository=_PROPOSAL_REPOSITORY, target_ref=target_ref,
            include_repository_structure=include_structure, pack_documents=documents,
        )

    default_error: ValueError | None = None
    structure_error: ValueError | None = None
    try:
        assemble(False)
    except ValueError as exc:
        default_error = exc
    try:
        assemble(True)
    except ValueError as exc:
        structure_error = exc
    refusal = _build_refusal(default_error, structure_error)
    if refusal is not None:
        raise refusal from (default_error or structure_error)
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
        "knowledge_build_checked": ["default", "--include-repository-structure"],
        "semantic_truth_established": False,
        "authority_verified": False,
        "action_authorized": False,
        "limits": [
            "Committed packs were read from HEAD; the proposal was read from its working bytes, as the commit that adds only it would contain.",
            "Evidence and source paths were required to be committed; a committed file missing from the working tree is refused.",
            "Opt-in Python import syntax (knowledge-build --include-python-imports) is not simulated.",
            "Schema/path checks are not semantic truth, owner intent or behavioral verification.",
            "Full semantic knowledge indexing requires an exact clean committed Git HEAD.",
        ],
    }
