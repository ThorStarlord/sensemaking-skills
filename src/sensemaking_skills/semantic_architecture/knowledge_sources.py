"""Build a deterministic, reviewable semantic snapshot from an exact Git revision.

Scope: explicitly tracked Grounding Pack lines, ADR identity/status, optional
Python import *syntax*, and authored .sensemaking/knowledge/*.json records.
We never synthesize owner intent, semantic dependencies or test guarantees.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

from .knowledge import (
    AUTHORED_SCHEMA_VERSIONS, KnowledgeClaim, KnowledgeRelation, KnowledgeSnapshot, read_authored_claim,
    read_authored_relation, stable_id, validate_snapshot,
)
from .models import ObservationKind
from .probes import probe_python_imports

_TAG = re.compile(r"(?:\[(policy|code|test|owner|delegated):\s*([^\]]+)\]|\[(hypothesis)\])\s*$")
_STATUS = re.compile(r"^\*\*Status:?\*\*:?\s*(.+)$", re.IGNORECASE)
_GROUNDING = (".sensemaking/intent.md", ".sensemaking/context.md", ".sensemaking/invariants.md")
_LIMITS = (
    "This is a bounded projection of tracked sources; missing claims/edges mean NOT ASSESSED, not absent.",
    "Declared authorities, authored edges and cited tests are source claims, not automatically verified truth.",
    "Observed code imports are syntax only; neither runtime dependency nor architectural significance is inferred.",
    "No query or graph relationship authorizes a product decision, merge, deployment or release.",
)


def _git(root: Path, *args: str, timeout: int = 30) -> str:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=root, text=True, capture_output=True,
            timeout=timeout, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"Git snapshot inspection unavailable: {exc}") from exc
    if proc.returncode:
        raise ValueError(f"Git snapshot inspection failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def verified_tracked_sources(repo_root: str | Path, target_ref: str) -> tuple[Path, set[str]]:
    """Fail closed unless target is exactly clean committed Git source bytes."""
    root = Path(repo_root).resolve()
    if not re.fullmatch(r"[0-9a-f]{40}", target_ref):
        raise ValueError("target_ref must be a full 40-character Git SHA")
    if Path(_git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise ValueError("repo_root must be the exact Git checkout root")
    if _git(root, "rev-parse", "HEAD") != target_ref:
        raise ValueError("target_ref does not equal the checked-out Git HEAD")
    if _git(root, "status", "--porcelain", "--untracked-files=all"):
        raise ValueError("dirty or untracked worktree: source bytes cannot be pinned")
    tracked = set(_git(root, "ls-files", "-z").split("\0"))
    tracked.discard("")
    return root, tracked


def _source(root: Path, tracked: set[str], relative: str) -> Path:
    if relative not in tracked:
        raise ValueError(f"source not tracked at target Git revision: {relative}")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"source escaped repository root: {relative}") from exc
    if not candidate.is_file():
        raise ValueError(f"source missing: {relative}")
    part = root
    for name in Path(relative).parts:
        part = part / name
        if part.is_symlink():
            raise ValueError(f"symlink source refused: {relative}")
    return candidate


def _local_evidence_path(reference: str) -> str | None:
    if not reference.startswith("file:"):
        return None
    path = reference[5:].split("#", 1)[0]
    return re.sub(r":line:\d+$", "", path)


def _check_authored_evidence(root: Path, tracked: set[str], refs: tuple[str, ...]) -> None:
    for ref in refs:
        path = _local_evidence_path(ref)
        if path is not None:
            _source(root, tracked, path)


def _source_hashes(root: Path, tracked: set[str], refs: tuple[str, ...]) -> dict[str, str]:
    """Hash supported, tracked evidence so a changed cited file is visible in a later snapshot."""
    hashes: dict[str, str] = {}
    for ref in refs:
        local = _local_evidence_path(ref)
        if local is not None:
            data = _source(root, tracked, local).read_bytes()
            hashes[local] = hashlib.sha256(data).hexdigest()
    return dict(sorted(hashes.items()))


def _grounding_claims(root: Path, tracked: set[str]) -> list[KnowledgeClaim]:
    paths = [* _GROUNDING, *(p for p in sorted(tracked) if p.startswith(".sensemaking/decisions/") and p.endswith(".md"))]
    found: list[KnowledgeClaim] = []
    for path in paths:
        if path not in tracked:
            continue
        lines = _source(root, tracked, path).read_text(encoding="utf-8").splitlines()
        kind = "goal" if path.endswith("intent.md") else "invariant" if path.endswith("invariants.md") else "decision" if "/decisions/" in path else "domain_concept"
        for line_num, line in enumerate(lines, 1):
            m = _TAG.search(line)
            if not m:
                continue
            authority = m.group(1) or "hypothesis"
            authority_ref = (m.group(2) or "hypothesis").strip()
            statement = line[:m.start()].strip()
            if not statement or statement.startswith("#"):
                continue
            source_ref = f"file:{path}:line:{line_num}"
            referenced = authority_ref if authority in {"policy", "code", "test"} else None
            present = None
            if referenced:
                try:
                    _source(root, tracked, referenced)
                    present = True
                except ValueError:
                    present = False
            hashes = _source_hashes(root, tracked, (source_ref,))
            if present is True and referenced:
                hashes.update(_source_hashes(root, tracked, (f"file:{referenced}",)))
            found.append(KnowledgeClaim(
                id=stable_id("pack", path, str(line_num), statement, authority),
                kind=kind, statement=statement,
                epistemic_status="hypothetical" if authority == "hypothesis" else "declared",
                authority_kind=authority, authority_ref=authority_ref,
                source_ref=source_ref, evidence_refs=(source_ref,),
                attributes={"cited_source_present": present, "authority_verified": False,
                            "scope": "tagged Grounding Pack statement",
                            "source_sha256": hashes},
            ))
    return found


def _adr_excerpts(lines: list[str], max_chars: int = 1600) -> dict[str, str]:
    """Bounded verbatim ADR context/decision/consequence excerpts, NOT a summary."""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        if line.startswith("## "):
            name = line[3:].strip().lower()
            current = name if name in {"context", "decision", "consequences", "rationale", "alternatives"} else None
            if current is not None:
                sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
    result: dict[str, str] = {}
    for name, body in sections.items():
        full_text = "\n".join(body).strip()
        if full_text:
            result[name] = full_text[:max_chars]
            if len(full_text) > max_chars:
                result[name + "_excerpt_truncated"] = "true"
    return result


def _adr_claims(root: Path, tracked: set[str]) -> list[KnowledgeClaim]:
    result = []
    for p in sorted(tracked):
        if not re.fullmatch(r"docs/adr/\d{3,4}-[^/]+\.md", p):
            continue
        lines = _source(root, tracked, p).read_text(encoding="utf-8").splitlines()
        title = lines[0].lstrip("# ").strip() if lines else ""
        if not title:
            continue
        state = "unclassified"
        for line in lines[:18]:
            m = _STATUS.match(line.strip())
            if m:
                state = m.group(1).strip()
                break
        source_ref = f"file:{p}:line:1"
        result.append(KnowledgeClaim(
            id="adr:" + Path(p).name.split("-", 1)[0],
            kind="decision",
            statement=title, epistemic_status="observed",
            authority_kind="document", authority_ref=p,
            source_ref=source_ref, evidence_refs=(source_ref,),
            attributes={"declared_adr_status": state, "authority_verified": False,
                        "source_sha256": _source_hashes(root, tracked, (source_ref,)),
                        "verbatim_sections": _adr_excerpts(lines),
                        "scope": "ADR title/status + bounded literal excerpts; source remains authoritative"},
        ))
    return result


def _authored_records(root: Path, tracked: set[str]) -> tuple[list[KnowledgeClaim], list[KnowledgeRelation]]:
    claims: list[KnowledgeClaim] = []
    edges: list[KnowledgeRelation] = []
    for p in sorted(tracked):
        if not p.startswith(".sensemaking/knowledge/") or not p.endswith(".json"):
            continue
        data = json.loads(_source(root, tracked, p).read_text(encoding="utf-8"))
        if not isinstance(data, dict) or set(data) != {"schema_version", "claims", "relations"} or data["schema_version"] not in AUTHORED_SCHEMA_VERSIONS:
            raise ValueError(f"invalid authored knowledge document: {p}")
        if not isinstance(data["claims"], list) or not isinstance(data["relations"], list):
            raise ValueError(f"authored claim/relation sets must be arrays: {p}")
        if len(data["claims"]) > 500 or len(data["relations"]) > 1000:
            raise ValueError(f"authored record oversized: {p}")
        for record in data["claims"]:
            claim = read_authored_claim(record, source_ref=f"file:{p}", schema_version=data["schema_version"])
            _check_authored_evidence(root, tracked, claim.evidence_refs)
            references = (*claim.evidence_refs, f"file:{p}")
            if claim.authority_kind in {"policy", "code", "test"}:
                _source(root, tracked, claim.authority_ref)
                references = (*references, f"file:{claim.authority_ref}")
            claims.append(KnowledgeClaim(
                **{**claim.__dict__, "attributes": {
                    **claim.attributes, "source_sha256": _source_hashes(root, tracked, references),
                }}
            ))
        for record in data["relations"]:
            relation = read_authored_relation(record, source_ref=f"file:{p}", schema_version=data["schema_version"])
            _check_authored_evidence(root, tracked, relation.evidence_refs)
            edges.append(KnowledgeRelation(
                **{**relation.__dict__, "attributes": {
                    **relation.attributes,
                    "source_sha256": _source_hashes(root, tracked, (*relation.evidence_refs, f"file:{p}")),
                }}
            ))
    return claims, edges


def _import_syntax(root: Path, tracked: set[str], target_ref: str, limit: int) -> tuple[list[KnowledgeClaim], list[KnowledgeRelation], bool]:
    result = probe_python_imports(root, target_ref=target_ref)
    items = [o for o in result.observations if o.kind is ObservationKind.PYTHON_IMPORT and o.subject in tracked]
    truncated = len(items) > limit or result.completeness.value != "complete"
    claims: dict[str, KnowledgeClaim] = {}
    edges: list[KnowledgeRelation] = []
    for item in sorted(items, key=lambda x: x.id)[:limit]:
        source_id = stable_id("file", item.subject)
        module_id = stable_id("module", item.object)
        for key, kind, statement in ((source_id, "source", item.subject), (module_id, "domain_concept", "Imported module syntax: " + item.object)):
            if key not in claims:
                claims[key] = KnowledgeClaim(
                    id=key, kind=kind, statement=statement, epistemic_status="observed",
                    authority_kind="mechanical", authority_ref="probe:python-imports-v1",
                    source_ref=f"file:{item.subject}", evidence_refs=item.evidence_refs,
                    attributes={"scope": "Python AST import syntax only", "authority_verified": False},
                )
        edges.append(KnowledgeRelation(
            id=stable_id("import", item.id), subject=source_id, predicate="references",
            object=module_id, epistemic_status="observed", derivation="mechanical",
            source_ref=f"file:{item.subject}", evidence_refs=item.evidence_refs,
            attributes={"scope": "import syntax, not runtime or architecture"},
        ))
    return list(claims.values()), edges, truncated


def build_knowledge_snapshot(
    repo_root: str | Path, *,
    repository: str, target_ref: str,
    include_python_imports: bool = False,
    max_imports: int = 1000,
    include_repository_structure: bool = False,
    max_structural_files: int = 600,
) -> KnowledgeSnapshot:
    if not repository.strip() or len(repository) > 255:
        raise ValueError("explicit repository identity is required")
    if not 0 <= max_imports <= 10000:
        raise ValueError("max_imports must be between 0 and 10000")
    if not 1 <= max_structural_files <= 2000:
        raise ValueError("max_structural_files must be between 1 and 2000")
    root, tracked = verified_tracked_sources(repo_root, target_ref)
    claims = [*_grounding_claims(root, tracked), *_adr_claims(root, tracked)]
    authored_claims, authored_edges = _authored_records(root, tracked)
    claims.extend(authored_claims)
    edges = [*authored_edges]
    limits = list(_LIMITS)
    scope = ["tracked Grounding Pack lines", "tracked ADR title/status", "tracked authored knowledge JSON"]
    if include_repository_structure:
        from .repository_bootstrap import structural_records
        structural_claims, structural_edges, partial = structural_records(
            root, tracked, max_structural_files=max_structural_files,
        )
        claims.extend(structural_claims)
        edges.extend(structural_edges)
        scope.append("opt-in Git-tracked file/directory containment skeleton")
        if partial:
            limits.append("Structural file selection truncated; unselected paths are NOT ASSESSED.")
    if include_python_imports:
        extra_claims, extra_edges, partial = _import_syntax(root, tracked, target_ref, max_imports)
        existing = {claim.id: claim for claim in claims}
        for claim in extra_claims:
            previous = existing.get(claim.id)
            if previous is None:
                claims.append(claim)
                existing[claim.id] = claim
            elif not (previous.kind == claim.kind and previous.statement == claim.statement):
                raise ValueError(f"conflicting knowledge claim identity: {claim.id}")
        edges.extend(extra_edges)
        scope.append("opt-in Python AST import syntax")
        if partial:
            limits.append("Python import observations truncated or partially parsed; absence is NOT ASSESSED.")
    snapshot = KnowledgeSnapshot(
        repository=repository.strip(), target_ref=target_ref,
        claims=tuple(sorted(claims, key=lambda x: x.id)),
        relations=tuple(sorted(edges, key=lambda x: x.id)),
        source_scope=tuple(scope), limits=tuple(limits),
    )
    validate_snapshot(snapshot)
    return snapshot
