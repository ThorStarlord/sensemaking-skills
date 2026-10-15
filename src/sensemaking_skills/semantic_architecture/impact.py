"""Read-only, source-bound impact preview over a target repository's Grounding Pack.

This is lexical evidence retrieval, NOT a semantic dependency inference engine.
Claims stay distinct from code observations and never authorize a change.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .models import ObservationKind
from .probes import probe_exact_search

_TAG = re.compile(r"\[(policy|code|test|owner|delegated|hypothesis):\s*([^\]]+)\]\s*$")
_PACK_FILES = (".sensemaking/intent.md", ".sensemaking/context.md", ".sensemaking/invariants.md")
_SHA = re.compile(r"[0-9a-f]{40}\Z")


@dataclass(frozen=True)
class GroundingClaim:
    statement: str
    evidence_ref: str
    provenance_kind: str
    provenance_target: str
    cited_path: str | None
    cited_path_exists: bool | None
    matched_terms: tuple[str, ...]


@dataclass(frozen=True)
class CandidateSurface:
    path: str
    category: str
    evidence_refs: tuple[str, ...]
    matched_terms: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceLink:
    subject: str
    predicate: str
    object: str
    evidence_refs: tuple[str, ...]
    derivation: str


@dataclass(frozen=True)
class ImpactPreview:
    target_ref: str
    subject: str
    searched_terms: tuple[str, ...]
    searched_globs: tuple[str, ...]
    grounding_claims: tuple[GroundingClaim, ...]
    candidate_surfaces: tuple[CandidateSurface, ...]
    evidence_links: tuple[EvidenceLink, ...]
    missing_citations: tuple[str, ...]
    match_count: int
    truncated: bool
    explicit_limits: tuple[str, ...]
    semantic_truth_established: bool = False
    change_authorized: bool = False
    material_impact_established: bool = False


def _git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, capture_output=True, text=True,
            check=False, timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"cannot verify Git snapshot: {exc}") from exc
    if result.returncode:
        raise ValueError(f"cannot verify Git snapshot: {result.stderr.strip()}")
    return result.stdout.strip()


def _verified_tracked_paths(root: Path, target_ref: str) -> set[str]:
    if not _SHA.fullmatch(target_ref):
        raise ValueError("target_ref must be a full 40-character Git commit SHA")
    top = Path(_git(root, "rev-parse", "--show-toplevel")).resolve()
    if top != root:
        raise ValueError("repo_root must be the exact Git worktree root")
    if _git(root, "rev-parse", "HEAD") != target_ref:
        raise ValueError("target_ref does not match checked-out Git HEAD")
    if _git(root, "status", "--porcelain"):
        raise ValueError("working tree is not clean; cannot bind observed bytes to target_ref")
    # Grounding and search hits must be tracked. Ignored generated files may
    # exist in an otherwise clean worktree, but are not part of target_ref.
    return set(_git(root, "ls-files").splitlines())


def _cited_file(root: Path, tracked: set[str], kind: str, target: str) -> tuple[str | None, bool | None]:
    if kind not in {"policy", "test", "code"}:
        return None, None
    value = target.strip()
    if not value or value.startswith(("http://", "https://")):
        return None, False
    candidate = (root / value).resolve()
    try:
        rel = candidate.relative_to(root).as_posix()
    except ValueError:
        return None, False
    return rel, rel in tracked and candidate.is_file() and not (root / value).is_symlink()


def _category(path: str) -> str:
    name = Path(path).name
    if name.endswith((".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx", "_test.py", "test.py")) or path.startswith("tests/"):
        return "test_candidate"
    if path.startswith(("specification/", "docs/")) or path.endswith(".md"):
        return "contract_or_document_candidate"
    if path.startswith("src/") or Path(path).suffix in {".py", ".ts", ".tsx", ".js", ".jsx"}:
        return "implementation_candidate"
    return "other_literal_mention"


def build_impact_preview(
    repo_root: str | Path,
    *,
    target_ref: str,
    subject: str,
    related_terms: Iterable[str] = (),
    include_globs: Iterable[str] = ("*",),
    max_matches: int = 100,
) -> ImpactPreview:
    """Retrieve bounded *candidate* impacts; never infer a dependency from a match.

    All observed bytes are verified against a clean, full-SHA Git checkout.
    Related terms are caller-provided, not invented by the projection.
    """
    root = Path(repo_root).resolve()
    if not subject.strip():
        raise ValueError("subject must be non-empty")
    if not 1 <= max_matches <= 2000:
        raise ValueError("max_matches must be between 1 and 2000")
    terms = tuple(dict.fromkeys(t.strip() for t in (subject, *related_terms) if t.strip()))
    globs = tuple(dict.fromkeys(g.strip() for g in include_globs if g.strip()))
    if not globs:
        raise ValueError("at least one include glob is required")
    tracked = _verified_tracked_paths(root, target_ref)
    claim_list: list[GroundingClaim] = []
    links: list[EvidenceLink] = []
    missing: set[str] = set()
    pack_files = (*_PACK_FILES, *(p for p in sorted(tracked) if p.startswith(".sensemaking/decisions/") and p.endswith(".md")))
    for pack_path in pack_files:
        if pack_path not in tracked:
            continue
        path = root / pack_path
        if path.is_symlink():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            tag = _TAG.search(line)
            if tag is None:
                continue
            matched = tuple(term for term in terms if term.casefold() in line[:tag.start()].casefold())
            if not matched:
                continue
            kind, target = tag.group(1), tag.group(2).strip()
            source_path, exists = _cited_file(root, tracked, kind, target)
            ref = f"file:{pack_path}:line:{line_number}"
            if exists is False:
                missing.add(f"{ref} -> {target}")
            for term in matched:
                links.append(EvidenceLink(ref, "contains_literal_term", term, (ref,), "LEXICAL"))
            if source_path is not None and exists is True:
                links.append(EvidenceLink(ref, f"declares_{kind}_reference", source_path, (ref,), "DECLARED_NOT_VERIFIED"))
            claim_list.append(
                GroundingClaim(
                    statement=line[:tag.start()].strip(),
                    evidence_ref=ref,
                    provenance_kind=kind,
                    provenance_target=target,
                    cited_path=source_path,
                    cited_path_exists=exists,
                    matched_terms=matched,
                )
            )

    grouped: dict[str, dict[str, set[str]]] = {}
    for term in terms:
        for glob in globs:
            result = probe_exact_search(root, target_ref=target_ref, pattern=term, include_glob=glob)
            for observation in result.observations:
                if observation.kind is not ObservationKind.EXACT_SEARCH_MATCH:
                    continue
                path = observation.subject
                if path.startswith(".sensemaking/") or path not in tracked:
                    continue
                entry = grouped.setdefault(path, {"refs": set(), "terms": set()})
                entry["refs"].update(observation.evidence_refs)
                entry["terms"].add(term)

    all_surfaces = [
        CandidateSurface(
            path=path,
            category=_category(path),
            evidence_refs=tuple(sorted(values["refs"])),
            matched_terms=tuple(t for t in terms if t in values["terms"]),
        )
        for path, values in sorted(grouped.items())
    ]
    for surface in all_surfaces[:max_matches]:
        for term in surface.matched_terms:
            links.append(EvidenceLink(surface.path, "contains_literal_term", term, surface.evidence_refs, "LEXICAL"))
    limits = [
        "Literal source mentions are search candidates, NOT established implementation, impact, or dependency relationships.",
        "Cited path existence does not prove that a claimed policy, owner decision, or test assertion is true or still authoritative.",
        "No observation outside the supplied terms, globs, tracked files, and Grounding Pack is represented; absence is NOT ASSESSED.",
        "Search is case-sensitive for repository mentions and case-insensitive for Grounding Pack claims; non-UTF-8 and excluded roots are not covered.",
        "A clean exact Git revision establishes byte identity only, not semantic truth or execution authority.",
    ]
    if len(all_surfaces) > max_matches:
        limits.append("Candidate surfaces are truncated; omitted results must not be treated as absent.")
    if missing:
        limits.append("Some Grounding Pack citations are missing or outside tracked repository sources.")
    return ImpactPreview(
        target_ref=target_ref,
        subject=subject.strip(),
        searched_terms=terms,
        searched_globs=globs,
        grounding_claims=tuple(claim_list),
        candidate_surfaces=tuple(all_surfaces[:max_matches]),
        evidence_links=tuple(sorted(links, key=lambda x: (x.subject, x.predicate, x.object))),
        missing_citations=tuple(sorted(missing)),
        match_count=len(all_surfaces),
        truncated=len(all_surfaces) > max_matches,
        explicit_limits=tuple(limits),
    )
