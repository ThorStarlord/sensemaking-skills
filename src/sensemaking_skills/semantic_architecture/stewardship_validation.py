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
from .knowledge_sources import _local_evidence_path, _source

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
        if isinstance(item, KnowledgeClaim) and item.authority_kind in {"policy", "code", "test"}:
            _source(root, tracked, item.authority_ref)
            evidence.add(item.authority_ref)

    # Cross-pack and observed-file/ADR endpoints are legitimate. Load only
    # currently Git-tracked authored claim identities; do not fabricate claims.
    known_ids = {c.id for c in claims}
    for name in sorted(tracked):
        match = _ADR_PATH.fullmatch(name)
        if match:
            known_ids.add(f"adr:{match.group(1)}")
        known_ids.add(stable_id("file", name))
        parts = Path(name).parts
        for depth in range(1, len(parts)):
            known_ids.add(stable_id("directory", Path(*parts[:depth]).as_posix()))
        if name == relative or not name.startswith(".sensemaking/knowledge/") or not name.endswith(".json"):
            continue
        other = json.loads(_source(root, tracked, name).read_text(encoding="utf-8"))
        if not isinstance(other, dict) or not isinstance(other.get("claims"), list):
            raise ValueError(f"invalid pre-existing authored knowledge: {name}")
        for record in other["claims"]:
            if isinstance(record, dict) and isinstance(record.get("id"), str):
                known_ids.add(record["id"])

    candidate_ids = {item.id for item in claims}
    if len(candidate_ids) != len(claims):
        raise ValueError("duplicate authored claim ids")
    needed = {id for rel in relations for id in (rel.subject, rel.object)}
    missing = needed - known_ids
    if missing:
        raise ValueError(f"unresolved relationship endpoint(s): {', '.join(sorted(missing)[:15])}")

    # Placeholder endpoints are restricted to in-memory validation. They are
    # NEVER indexed, persisted, displayed as factual claims or marked verified.
    placeholders = [
        KnowledgeClaim(
            id=identifier, kind="hypothesis", statement="External endpoint, source not semantically reviewed",
            epistemic_status="hypothetical", authority_kind="hypothesis",
            authority_ref="proposal-validation-only", source_ref="proposal-validation-only",
            evidence_refs=("proposal-validation-only",),
        )
        for identifier in sorted(needed - candidate_ids)
    ]
    validate_snapshot(KnowledgeSnapshot(
        repository="proposal-validation-only", target_ref=target_ref,
        claims=tuple([*claims, *placeholders]), relations=tuple(relations),
        source_scope=("proposed non-authoritative working records",),
        limits=("Uncommitted proposals and dirty source bytes are not authoritative.",),
    ))
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
        "semantic_truth_established": False,
        "authority_verified": False,
        "action_authorized": False,
        "limits": [
            "The source and referenced paths were inspected in the CURRENT WORKTREE, possibly dirty.",
            "Schema/path checks are not semantic truth, owner intent or behavioral verification.",
            "Full semantic knowledge indexing requires an exact clean committed Git HEAD.",
        ],
    }
