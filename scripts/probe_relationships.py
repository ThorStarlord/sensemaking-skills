"""Cross-artifact relationship probes (version drift + ADR integrity).

Deterministic evidence acquisition for repo-sensemaker's Probe Engine.

Establishes mechanically knowable facts about cross-artifact relationships
and emits evidence CANDIDATES with provenance -- never diagnoses. The
model (repo-sensemaker) interprets meaning: which source has authority,
whether a disagreement matters, whether a status claim is stale.

Pure functions: filesystem reads only. No network, no writes. Plain dicts
safe for YAML serialization.

Conceptual lineage: distilled from the discovery spike branch
`feat/spike-semantic-drift` (scripts/probe_doc_code_drift.py), which is
evidence, not code transplanted literally. Three capabilities survived:
(1) automatic live-document surface discovery, (2) version relationship
detection, (3) ADR integrity detection. The network-capability detector
did NOT survive (NOT READY). No graph/node/edge abstraction is used.

Live-document discovery is path-signal-driven, plus an explicit opt-in
`<!-- doc-status: historical -->` marker a document can carry near its top
to declare itself a point-in-time record (see _declared_doc_status).

Output shape (one top-level report key, always present):

    relationships:
      doc_surface: {total, live, by_class}
      version:     {declarations, claims, distinct_values, findings[]}
      adr:         {files, catalog[], references, findings[]}

A finding is:

    {concept, finding_type,
     observations: [{source, location, value, evidence, source_kind,
                     claim_class, source_class?}],
     confidence, requires_semantic_review, notes}

A repository with no relationship findings still produces a valid section
with empty findings lists (a correct negative is a valid result).
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# 1. Live-document surface discovery
# ---------------------------------------------------------------------------

SKIP_DIRS = {"node_modules", "__pycache__", "dist", "build"}

# Only clearly point-in-time markers: records of a past state.
HISTORICAL_PATH_RE = re.compile(
    r"(?:^|/)(archived?|historical|old|legacy|backup|bak|releases|handoffs?|"
    r"session_handoffs|reviews?|research|plans|proposals?|changelog|"
    r"experiments?|audits?)(?:/|$)", re.IGNORECASE)
VENDOR_PATH_RE = re.compile(r"(?:^|/)(vendor|third_party|site-packages)(?:/|$)", re.IGNORECASE)
FIXTURE_PATH_RE = re.compile(r"(?:^|/)(fixtures?|test-results|golden|corpus)(?:/|$)", re.IGNORECASE)
EXAMPLE_PATH_RE = re.compile(r"(?:^|/)(examples?|demos?|samples?)(?:/|$)", re.IGNORECASE)
GENERATED_PATH_RE = re.compile(
    r"(?:^|/)(generated|gen|out|dist|build|coverage|site|_build|artifacts|"
    r"outbox|staging|runs|logs|tmp|temp|scratch|transport|evidence)(?:/|$)", re.IGNORECASE)
CANDIDATE_PATH_RE = re.compile(r"(?:^|/)(candidates?|drafts?)(?:/|$)", re.IGNORECASE)
HISTORICAL_NAME_RE = re.compile(r"^(changelog|handoff)", re.IGNORECASE)
HISTORICAL_PREFIX_RE = re.compile(
    r"^(\d{4}-\d{2}(-\d{2})?|v\d+\.\d+|phase-?\d|week\d|stage-?\d)", re.IGNORECASE)

# Explicit in-file lifecycle marker. A document that has become a
# point-in-time record while keeping its original path (a root-level
# `roadmap.md` that predates a pivot, say) cannot be caught by the path
# heuristics above. It can instead declare itself with an HTML comment near
# the top:  <!-- doc-status: historical -->
# Accepted values all mean "not a live current-state surface". Only the
# document head is scanned (DOC_STATUS_HEAD_BYTES) so a mention deeper in the
# body -- documentation of this convention, a quoted example -- does not
# reclassify a live document.
DOC_STATUS_MARKER_RE = re.compile(
    r"<!--\s*doc-status:\s*(?:historical|superseded|archived)\s*-->", re.IGNORECASE)
DOC_STATUS_HEAD_BYTES = 4096


def _declared_doc_status(path: Path) -> Optional[str]:
    """Explicit in-file lifecycle marker read from the document head only.

    Returns "historical" when a `doc-status` marker (see DOC_STATUS_MARKER_RE)
    is present in the first DOC_STATUS_HEAD_BYTES bytes, else None.
    """
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            head = handle.read(DOC_STATUS_HEAD_BYTES)
    except OSError:
        return None
    return "historical" if DOC_STATUS_MARKER_RE.search(head) else None


def _classify_doc_file(rel: str, declared_status: Optional[str] = None) -> str:
    """Classify a discovered .md path: live | historical | generated |
    fixture | vendor | example | candidate.

    Deterministic path signals, plus an optional explicit in-file `doc-status`
    marker (see _declared_doc_status). An explicit marker wins over every path
    heuristic -- the author has stated the document's lifecycle directly.
    Otherwise: point-in-time path/name records win over generic defaults.
    """
    if declared_status:
        return declared_status
    low = rel.lower()
    name = rel.split("/")[-1]
    if (HISTORICAL_PATH_RE.search(low) or HISTORICAL_NAME_RE.match(name)
            or HISTORICAL_PREFIX_RE.match(name)):
        return "historical"
    if VENDOR_PATH_RE.search(low):
        return "vendor"
    if FIXTURE_PATH_RE.search(low):
        return "fixture"
    if EXAMPLE_PATH_RE.search(low):
        return "example"
    if GENERATED_PATH_RE.search(low):
        return "generated"
    if CANDIDATE_PATH_RE.search(low):
        return "candidate"
    return "live"


def _discover_docs(repo_root: Path) -> List[Dict[str, str]]:
    """Bounded *.md walk (hidden/generic dirs pruned in place), classified."""
    docs: List[Dict[str, str]] = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in SKIP_DIRS and not d.startswith("."))
        rel_dir = os.path.relpath(dirpath, repo_root)
        for fname in sorted(filenames):
            if not fname.endswith(".md"):
                continue
            rel = fname if rel_dir == "." else f"{rel_dir}/{fname}"
            rel = rel.replace("\\", "/")
            declared = _declared_doc_status(Path(dirpath) / fname)
            docs.append({"source": rel,
                         "source_class": _classify_doc_file(rel, declared)})
    return docs


def _live_sources(docs: List[Dict[str, str]]) -> List[str]:
    return [d["source"] for d in docs if d["source_class"] == "live"]


def doc_surface(repo_root: Path, docs: Optional[List[Dict[str, str]]] = None) -> Dict[str, object]:
    """Discovered *.md surface: total, live count, and class counts."""
    if docs is None:
        docs = _discover_docs(repo_root)
    by_class: Dict[str, int] = {}
    for d in docs:
        by_class[d["source_class"]] = by_class.get(d["source_class"], 0) + 1
    return {
        "total": len(docs),
        "live": sum(1 for d in docs if d["source_class"] == "live"),
        "by_class": dict(sorted(by_class.items())),
    }


# ---------------------------------------------------------------------------
# 2. Version relationship detection
# ---------------------------------------------------------------------------

VERSION_TOKEN_RE = re.compile(r"\bv?\d+\.\d+\.\d+\b")
CURRENT_KEYWORDS = ("current", "version", "release", "expected", "install", "pip")
HISTORICAL_KEYWORDS = (
    "new in", "since", "changed in", "added in", "introduced in",
    "removed in", "deprecated", "history", "changelog", "release notes",
)
HISTORICAL_MARKER_RE = re.compile(
    r"\b(old|previous|prior|earlier|was|formerly|bumped|fixed)\b", re.IGNORECASE)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _posix(path: Path) -> str:
    return path.as_posix()


def _obs(source: str, line: int, value: str, evidence: str,
         source_kind: str, claim_class: str,
         source_class: Optional[str] = None) -> Dict[str, str]:
    obs = {
        "source": source,
        "location": f"{source}:{line}",
        "value": value,
        "evidence": evidence[:200],
        "source_kind": source_kind,
        "claim_class": claim_class,
    }
    if source_class is not None:
        obs["source_class"] = source_class
    return obs


def _project_name(repo_root: Path) -> Optional[str]:
    """Declared project/package name (dashes normalized to underscores)."""
    pyproject = repo_root / "pyproject.toml"
    if pyproject.is_file():
        match = re.search(r'^name\s*=\s*["\']([^"\']+)["\']',
                          _read_text(pyproject), re.MULTILINE)
        if match:
            return match.group(1).replace("-", "_")
    pkg_json = repo_root / "package.json"
    if pkg_json.is_file():
        match = re.search(r'"name"\s*:\s*"([^"]+)"', _read_text(pkg_json))
        if match:
            return match.group(1).replace("-", "_")
    return None


def _declared_versions(repo_root: Path) -> List[Dict[str, str]]:
    """Version declarations from packaging metadata + top-level __init__.

    Only the top-level package's __version__ (src/<project-name>/
    __init__.py) is a product declaration. Sub-package __version__ values
    are recorded as claim_class 'subpackage' and cannot anchor the product
    family (same string != same concept).
    """
    observations: List[Dict[str, str]] = []

    pyproject = repo_root / "pyproject.toml"
    if pyproject.is_file():
        text = _read_text(pyproject)
        for match in re.finditer(r'^version\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE):
            value = match.group(1).strip()
            if re.match(r"^\d+\.\d+\.\d+", value):
                line = text.count("\n", 0, match.start()) + 1
                observations.append(_obs("pyproject.toml", line, value,
                                         match.group(0).strip(), "declaration", "declared"))

    setup = repo_root / "setup.py"
    if setup.is_file():
        text = _read_text(setup)
        for match in re.finditer(r'version\s*=\s*["\']([^"\']+)["\']', text):
            value = match.group(1).strip()
            if re.match(r"^\d+\.\d+\.\d+", value):
                line = text.count("\n", 0, match.start()) + 1
                observations.append(_obs("setup.py", line, value,
                                         match.group(0).strip(), "declaration", "declared"))

    pkg_json = repo_root / "package.json"
    if pkg_json.is_file():
        text = _read_text(pkg_json)
        for match in re.finditer(r'"version"\s*:\s*"([^"]+)"', text):
            value = match.group(1).strip()
            if re.match(r"^\d+\.\d+\.\d+", value):
                line = text.count("\n", 0, match.start()) + 1
                observations.append(_obs("package.json", line, value,
                                         match.group(0).strip(), "declaration", "declared"))

    name = _project_name(repo_root)
    top_level = [p for p in sorted((repo_root / "src").rglob("__init__.py"))
                 if p.is_file() and _posix(p.relative_to(repo_root)).count("/") == 2] \
        if (repo_root / "src").is_dir() else []
    ambiguous = name is None and len(top_level) > 1
    for init in sorted((repo_root / "src").rglob("__init__.py")) \
            if (repo_root / "src").is_dir() else []:
        rel = _posix(init.relative_to(repo_root))
        is_top_level = rel.count("/") == 2
        is_product = is_top_level and not ambiguous and (
            name is None or rel == f"src/{name}/__init__.py")
        text = _read_text(init)
        for match in re.finditer(r'__version__\s*=\s*["\']([^"\']+)["\']', text):
            value = match.group(1).strip()
            if re.match(r"^\d+\.\d+\.\d+", value):
                line = text.count("\n", 0, match.start()) + 1
                observations.append(_obs(
                    rel, line, value, match.group(0).strip(), "declaration",
                    "declared" if is_product else "subpackage"))
    return sorted(observations, key=lambda o: (o["source_kind"], o["source"], o["location"]))


def _classify_claim(line: str, is_test_file: bool) -> str:
    low = line.lower()
    if any(k in low for k in HISTORICAL_KEYWORDS) or HISTORICAL_MARKER_RE.search(low):
        return "historical"
    if any(k in low for k in CURRENT_KEYWORDS):
        return "current"
    if is_test_file and ("assert" in low or "==" in low):
        return "current"
    return "unknown"


def _doc_version_claims(repo_root: Path, live_sources: List[str]) -> List[Dict[str, str]]:
    """Version tokens on claim-like lines of live docs and test files."""
    observations: List[Dict[str, str]] = []
    for path in sorted((repo_root / "tests").rglob("*.py")) if (repo_root / "tests").is_dir() else []:
        rel = _posix(path.relative_to(repo_root))
        if rel == "tests/test_probe_relationships.py" or rel == "tests/test_probe_doc_code_drift.py":
            continue  # probe test files contain fixture version literals
        text = _read_text(path)
        for lineno, raw in enumerate(text.splitlines(), start=1):
            for match in VERSION_TOKEN_RE.finditer(raw):
                observations.append(_obs(rel, lineno, match.group(0).lstrip("v"),
                                         raw.strip(), "verification",
                                         _classify_claim(raw, True), "verification"))
    for src in live_sources:
        text = _read_text(repo_root / src)
        for lineno, raw in enumerate(text.splitlines(), start=1):
            for match in VERSION_TOKEN_RE.finditer(raw):
                observations.append(_obs(src, lineno, match.group(0).lstrip("v"),
                                         raw.strip(), "documentation",
                                         _classify_claim(raw, False), "live"))
    return sorted(observations, key=lambda o: (o["source_kind"], o["source"], o["location"]))


def _version_family(value: str) -> Optional[tuple]:
    parts = value.split(".")
    try:
        return (int(parts[0]), int(parts[1]))
    except (IndexError, ValueError):
        return None


def _version_decision(declared: List[Dict[str, str]],
                      claims: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Observations that count as claims about the declared version concept.

    Same string != same concept: only values in the declared version family
    (major.minor) join the decision set; the family anchor comes from
    product-declared observations only.
    """
    families = {_version_family(o["value"]) for o in declared
                if o["claim_class"] == "declared"}
    families.discard(None)
    decision: List[Dict[str, str]] = []
    for o in declared + claims:
        if o["claim_class"] not in ("declared", "current"):
            continue
        if families and o["source_kind"] != "declaration":
            if _version_family(o["value"]) not in families:
                continue
        decision.append(o)
    return sorted(decision, key=lambda o: (o["source_kind"], o["source"], o["location"]))


def _version_findings(declared: List[Dict[str, str]],
                      claims: List[Dict[str, str]]) -> List[Dict[str, object]]:
    decision = _version_decision(declared, claims)
    distinct = sorted({o["value"] for o in decision})
    if len(distinct) <= 1:
        return []
    return [{
        "concept": "product_version",
        "finding_type": "conflicting_values",
        "observations": decision,
        "confidence": "high",
        "requires_semantic_review": True,
        "notes": (
            "Values disagree mechanically across sources. Which source has "
            "authority, which is historical, and whether it matters is for "
            "the model to interpret. Claims of other version families are "
            "excluded from this decision set."
        ),
    }]


def version_drift(repo_root: Path, docs: Optional[List[Dict[str, str]]] = None) -> Dict[str, object]:
    """Version relationship evidence: declarations + live claims + findings."""
    if docs is None:
        docs = _discover_docs(repo_root)
    declared = _declared_versions(repo_root)
    claims = _doc_version_claims(repo_root, _live_sources(docs))
    return {
        "declarations": sum(1 for o in declared if o["claim_class"] == "declared"),
        "subpackage_declarations": sum(
            1 for o in declared if o["claim_class"] == "subpackage"),
        "claims": len(claims),
        "distinct_values": sorted(
            {o["value"] for o in _version_decision(declared, claims)}),
        "findings": _version_findings(declared, claims),
    }


# ---------------------------------------------------------------------------
# 3. ADR integrity detection
# ---------------------------------------------------------------------------

STATUS_LINE_RE = re.compile(r"^\*\*Status:?\*\*:?\s*(.+)$", re.IGNORECASE | re.MULTILINE)
STATUS_H2_RE = re.compile(r"^##\s*Status\s*$", re.IGNORECASE | re.MULTILINE)
ADR_REF_RE = re.compile(r"\bADR[- ]?(\d{2,4})\b")
ADR_PATH_REF_RE = re.compile(r"docs/adr/(\d{2,4})-[a-z0-9-]+\.md", re.IGNORECASE)
STATUS_WORD_RE = re.compile(
    r"\b(accepted|ratified|approved|proposed|provisional|superseded|rejected)\b",
    re.IGNORECASE)
NOT_ACCEPTED_RE = re.compile(r"\bnot\s+(yet\s+)?(accepted|ratified|approved)\b", re.IGNORECASE)
VALID_STATUSES = {"accepted", "proposed", "provisional", "superseded", "rejected"}

# Advisory (non-blocking) stale-Accepted-ADR detection.
# Semantic-control-map persistence trial (docs/semantic-control-map-trial.md):
# surface -- never adjudicate -- the case where a newer ADR that is itself
# Accepted refers to an older ADR whose own **Status** is still Accepted using
# supersession language. Deciding whether the older ADR is *truly* superseded
# needs semantic judgment, so the finding is requires_semantic_review=True and
# is NOT in gate_relationship_findings.py's BLOCKING_FINDING_TYPES set.
# Note the deliberate "superced" spelling: docs/adr/0013 line ~258 says
# "now superceded by skill-led model" about ADR 0012.
SUPERSESSION_CUE_RE = re.compile(
    r"\b(supersed|superced|deprecat|replaced\s+by|no\s+longer|"
    r"historical(?:\s*[,)—-]|\s+only|\s+proposal)|"
    r"opposite\s+mechanism|de-?authoriz)", re.IGNORECASE)
_ADR_SOURCE_RE = re.compile(r"^docs/adr/(\d{2,4})-")


def _raw_status_text(text: str) -> Optional[str]:
    """Status value from **Status**: / **Status:** / ## Status block forms."""
    inline = STATUS_LINE_RE.search(text)
    if inline:
        return inline.group(1).strip()
    h2 = STATUS_H2_RE.search(text)
    if h2:
        for line in text[h2.end():].splitlines():
            stripped = line.strip()
            if stripped:
                return stripped
    return None


def adr_catalog(repo_root: Path) -> List[Dict[str, object]]:
    """Catalog of docs/adr/NNNN-*.md: id, file, title, status (normalized)."""
    catalog: List[Dict[str, object]] = []
    for path in sorted((repo_root / "docs" / "adr").glob("*.md")) \
            if (repo_root / "docs" / "adr").is_dir() else []:
        if path.name == "README.md" or not re.match(r"^\d{2,4}-", path.name):
            continue
        text = _read_text(path)
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        raw_status = _raw_status_text(text)
        normalized = None
        if raw_status:
            first = raw_status.lower().split()[0].rstrip(".")
            normalized = first if first in VALID_STATUSES else None
        catalog.append({
            "id": path.name[:re.match(r"^\d{2,4}", path.name).end()],
            "file": _posix(path.relative_to(repo_root)),
            "title": title_match.group(1).strip() if title_match else None,
            "status": normalized,
            "raw_status": raw_status,
        })
    return catalog


def _claimed_status(window: str) -> Optional[str]:
    """Status claimed about an ADR, read from the clipped text window."""
    if NOT_ACCEPTED_RE.search(window):
        return "not_accepted"
    match = STATUS_WORD_RE.search(window)
    if not match:
        return None
    word = match.group(1).lower()
    if word in ("accepted", "ratified", "approved"):
        return "accepted"
    return word


def _adr_references(repo_root: Path, docs: List[Dict[str, str]]) -> List[Dict[str, object]]:
    """References to ADRs across live docs, skills, workflows, and ADRs."""
    refs: List[Dict[str, object]] = []
    scan_globs = [
        (repo_root / "skills").rglob("*.md"),
        (repo_root / "docs" / "adr").glob("*.md"),
        (repo_root / "workflows").rglob("*.yaml"),
    ]
    scan_paths: List[Path] = [repo_root / src for src in _live_sources(docs)]
    for generator in scan_globs:
        scan_paths.extend(p for p in generator if p.is_file())
    config = repo_root / "sensemaking-config.yaml"
    if config.is_file():
        scan_paths.append(config)
    for path in sorted(set(scan_paths)):
        rel = _posix(path.relative_to(repo_root))
        own_match = re.match(r"docs/adr/(\d{2,4})-", rel)
        own_id = own_match.group(1) if own_match else None
        text = _read_text(path)
        seen: set = set()
        for lineno, raw_line in enumerate(text.splitlines(), start=1):
            spans: List[tuple] = []
            for pattern in (ADR_REF_RE, ADR_PATH_REF_RE):
                spans.extend((m.group(1), m.span()) for m in pattern.finditer(raw_line))
            spans.sort(key=lambda s: s[1][0])
            for idx, (adr_id, (start, end)) in enumerate(spans):
                if own_id and adr_id == own_id:
                    continue
                key = (adr_id, lineno)
                if key in seen:
                    continue
                seen.add(key)
                prev_end = spans[idx - 1][1][1] if idx > 0 else None
                next_start = spans[idx + 1][1][0] if idx + 1 < len(spans) else None
                window = raw_line[max(0, start - 80, prev_end or 0)
                                  : min(len(raw_line), end + 80, next_start or len(raw_line))]
                refs.append({
                    "id": adr_id,
                    "source": rel,
                    "location": f"{rel}:{lineno}",
                    "claimed_status": _claimed_status(window),
                    "evidence": raw_line.strip()[:200],
                })
    return sorted(refs, key=lambda r: (r["source"], r["location"]))


def _stale_accepted_adr_findings(
        refs: List[Dict[str, object]],
        catalog: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Advisory: a newer Accepted ADR uses supersession language about an older
    ADR whose own **Status** is still Accepted.

    Mechanical trigger only. Whether the older ADR is genuinely superseded (its
    status line should change) or the newer ADR overstates the case is left to
    the model: requires_semantic_review=True, never blocking (see
    scripts/gate_relationship_findings.py). Introduced for the
    semantic-control-map persistence trial.
    """
    status_by_id: Dict[str, Optional[str]] = {}
    for entry in catalog:
        # if an id is duplicated, treat it as accepted only if every entry is
        status_by_id.setdefault(str(entry["id"]), entry["status"])
        if entry["status"] != "accepted":
            status_by_id[str(entry["id"])] = entry["status"]

    findings: List[Dict[str, object]] = []
    seen: set = set()
    for ref in refs:
        src_match = _ADR_SOURCE_RE.match(str(ref["source"]))
        if not src_match:
            continue
        referencing_id = src_match.group(1)
        referenced_id = str(ref["id"])
        if referenced_id == referencing_id:
            continue
        # referencing ADR must itself be Accepted, and newer (higher id)
        if status_by_id.get(referencing_id) != "accepted":
            continue
        if referenced_id.isdigit() and referencing_id.isdigit() \
                and int(referencing_id) <= int(referenced_id):
            continue
        # referenced ADR's own status must still be Accepted
        if status_by_id.get(referenced_id) != "accepted":
            continue
        evidence_line = str(ref["evidence"])
        if not SUPERSESSION_CUE_RE.search(evidence_line):
            continue
        key = (referencing_id, referenced_id, ref["location"])
        if key in seen:
            continue
        seen.add(key)
        findings.append({
            "concept": "adr_status",
            "finding_type": "stale_accepted_adr_candidate",
            "observations": [{
                "source": ref["source"],
                "location": ref["location"],
                "value": referenced_id,
                "evidence": evidence_line[:200],
                "source_kind": "contract",
                "claim_class": "status_claim",
            }],
            "confidence": "medium",
            "requires_semantic_review": True,
            "notes": (
                f"ADR {referencing_id} (itself Accepted) uses supersession "
                f"language about ADR {referenced_id}, whose own **Status** is "
                f"still Accepted. Candidate inconsistency only: the model must "
                f"decide whether ADR {referenced_id}'s status line is stale or "
                f"ADR {referencing_id} overstates the supersession. Advisory / "
                f"non-blocking."
            ),
        })
    return findings


def _adr_findings(refs: List[Dict[str, object]],
                  catalog: List[Dict[str, object]]) -> List[Dict[str, object]]:
    by_id: Dict[str, List[Dict[str, object]]] = {}
    for entry in catalog:
        by_id.setdefault(str(entry["id"]), []).append(entry)
    findings: List[Dict[str, object]] = []

    # Duplicate identifiers: multiple files declaring the same ADR id is a
    # mechanical defect of the id namespace itself. This makes the duplicate
    # a top-level finding instead of a catalog-only condition the model must
    # notice by reading raw data (evidence-rules Rule 11). The renumber
    # DIRECTION is left to the model (evidence-rules Rule 7), so the finding
    # is mechanical (requires_semantic_review=False) but never blocking.
    for adr_id, entries in sorted(by_id.items()):
        if len(entries) > 1:
            findings.append({
                "concept": "adr_identifier",
                "finding_type": "duplicate_id",
                "observations": [{
                    "source": entry["file"],
                    "location": entry["file"],
                    "value": adr_id,
                    "evidence": f"ADR id {adr_id} declared by {len(entries)} files",
                    "source_kind": "contract",
                    "claim_class": "id_declaration",
                } for entry in entries],
                "confidence": "high",
                "requires_semantic_review": False,
                "notes": (
                    f"Multiple files declare ADR id {adr_id}; the id namespace "
                    "is ambiguous. Before renumbering, count external references "
                    "per candidate and grep all files including handoffs "
                    "(evidence-rules Rule 7); which side is load-bearing is "
                    "for the model to interpret."
                ),
            })

    for ref in refs:
        entries = by_id.get(ref["id"])
        if entries is None:
            findings.append({
                "concept": "adr_reference",
                "finding_type": "missing_reference",
                "observations": [{
                    "source": ref["source"],
                    "location": ref["location"],
                    "value": ref["id"],
                    "evidence": ref["evidence"],
                    "source_kind": "documentation",
                    "claim_class": "reference",
                }],
                "confidence": "high",
                "requires_semantic_review": False,
                "notes": "Referenced ADR id does not exist under docs/adr/.",
            })
            continue
        claimed = ref["claimed_status"]
        for entry in entries:
            actual = entry["status"]
            mismatch = None
            if claimed == "accepted" and actual != "accepted":
                mismatch = f"claimed accepted; actual ADR status is {actual or 'unknown'}"
            elif claimed == "not_accepted" and actual == "accepted":
                mismatch = "claimed not accepted; actual ADR status is accepted"
            if mismatch:
                findings.append({
                    "concept": "adr_status",
                    "finding_type": "status_claim_mismatch",
                    "observations": [{
                        "source": ref["source"],
                        "location": ref["location"],
                        "value": actual,
                        "evidence": ref["evidence"],
                        "source_kind": "documentation",
                        "claim_class": "status_claim",
                    }],
                    "confidence": "high",
                    "requires_semantic_review": True,
                    "notes": mismatch + f" (ADR {entry['id']}: {entry['file']}). "
                            "Which side is stale is for the model to interpret.",
                })

    for entry in catalog:
        if entry["status"] is None:
            if entry["raw_status"]:
                findings.append({
                    "concept": "adr_status",
                    "finding_type": "unrecognized_status",
                    "observations": [{
                        "source": entry["file"],
                        "location": entry["file"],
                        "value": entry["raw_status"],
                        "evidence": f"**Status** line present but first word not in "
                                   f"{sorted(VALID_STATUSES)}",
                        "source_kind": "contract",
                        "claim_class": "status_declaration",
                    }],
                    "confidence": "high",
                    "requires_semantic_review": True,
                    "notes": "Unrecognized status vocabulary; the model must decide "
                            "whether it is a valid new status or a typo.",
                })
            else:
                findings.append({
                    "concept": "adr_status",
                    "finding_type": "missing_status_line",
                    "observations": [{
                        "source": entry["file"],
                        "location": entry["file"],
                        "value": None,
                        "evidence": "No **Status** line found",
                        "source_kind": "contract",
                        "claim_class": "status_declaration",
                    }],
                    "confidence": "high",
                    "requires_semantic_review": False,
                    "notes": "docs/adr/README.md defines the **Status** convention; "
                            "no script validates it today.",
                })

    findings.extend(_stale_accepted_adr_findings(refs, catalog))
    return findings


def adr_integrity(repo_root: Path, docs: Optional[List[Dict[str, str]]] = None) -> Dict[str, object]:
    """ADR relationship evidence: catalog, references, findings."""
    if docs is None:
        docs = _discover_docs(repo_root)
    catalog = adr_catalog(repo_root)
    refs = _adr_references(repo_root, docs)
    return {
        "files": len(catalog),
        "catalog": catalog,
        "references": len(refs),
        "findings": _adr_findings(refs, catalog),
    }


# ---------------------------------------------------------------------------
# Assembler
# ---------------------------------------------------------------------------

def relationships(repo_root: Path) -> Dict[str, object]:
    """Run the cross-artifact relationship probes; assemble the section."""
    docs = _discover_docs(repo_root)
    return {
        "doc_surface": doc_surface(repo_root, docs),
        "version": version_drift(repo_root, docs),
        "adr": adr_integrity(repo_root, docs),
    }
