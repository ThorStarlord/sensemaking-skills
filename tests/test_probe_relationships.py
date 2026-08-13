"""Tests for scripts/probe_relationships.py (Probe Engine integration).

Covers mechanically decidable behavior: doc-surface discovery and
classification, version relationship detection, ADR integrity detection,
and the assembled `relationships` section (empty findings = valid
correct-negative).
"""

import subprocess
import sys
from pathlib import Path

from scripts.probe_relationships import (
    adr_catalog,
    adr_integrity,
    _classify_doc_file,
    doc_surface,
    relationships,
    version_drift,
)


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _mini_repo(tmp_path: Path, version: str = "0.2.2") -> Path:
    repo = tmp_path / "repo"
    _write(repo, "pyproject.toml", f'[project]\nname = "x"\nversion = "{version}"\n')
    return repo


# ---------------------------------------------------------------------------
# Doc-surface discovery
# ---------------------------------------------------------------------------

def test_classify_doc_file() -> None:
    cases = {
        "README.md": "live",
        "CONTEXT.md": "live",
        "docs/installation.md": "live",
        "docs/guides/install.md": "live",
        "docs/adr/0001-x.md": "live",
        "docs/archive/old-plan.md": "historical",
        "docs/archived/x.md": "historical",
        "docs/releases/v0.37.0.md": "historical",
        "docs/acceptance/v0.5.0-report.md": "historical",
        "docs/2026-07-11-notes.md": "historical",
        "CHANGELOG.md": "historical",
        "docs/experiments/e1.md": "historical",
        "fixtures/example-output.md": "fixture",
        "examples/demo.md": "example",
        "vendor/lib.md": "vendor",
        "docs/generated/out.md": "generated",
        "docs/transport/messages.md": "generated",
        "docs/candidate/proposal.md": "candidate",
        "docs/drafts/idea.md": "candidate",
        "docs/acceptance/criteria.md": "live",
    }
    for rel, expected in cases.items():
        assert _classify_doc_file(rel) == expected, f"{rel} -> {expected}"


def test_doc_surface_skips_hidden_dirs_and_counts_classes(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path)
    _write(repo, "README.md", "# x\n")
    _write(repo, "docs/guide.md", "guide\n")
    _write(repo, "docs/archive/old.md", "old\n")
    _write(repo, ".private/docs/hidden.md", "hidden\n")
    _write(repo, ".venv/docs/x.md", "hidden\n")
    surface = doc_surface(repo)
    assert surface["total"] == 3
    assert surface["live"] == 2
    assert surface["by_class"]["historical"] == 1


# ---------------------------------------------------------------------------
# Version relationships
# ---------------------------------------------------------------------------

def test_version_finding_on_doc_drift(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path, version="0.2.2")
    _write(repo, "README.md", "Current release: 0.2.1\n")
    section = version_drift(repo)
    assert section["declarations"] == 1
    assert section["distinct_values"] == ["0.2.1", "0.2.2"]
    assert len(section["findings"]) == 1
    f = section["findings"][0]
    assert f["finding_type"] == "conflicting_values"
    assert {o["value"] for o in f["observations"]} == {"0.2.1", "0.2.2"}
    assert f["requires_semantic_review"] is False


def test_version_consistent_is_correct_negative(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path, version="0.2.2")
    _write(repo, "README.md", "Current release: 0.2.2\n")
    section = version_drift(repo)
    assert section["findings"] == []


def test_version_family_filter_excludes_other_concepts(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path, version="0.2.2")
    _write(repo, "README.md",
           "Current release: 0.2.1\n"
           "JSON export planned for 0.3.0\n")
    section = version_drift(repo)
    values = {o["value"] for o in section["findings"][0]["observations"]}
    assert "0.2.1" in values and "0.3.0" not in values


def test_subpackage_version_is_not_product_declaration(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path, version="0.37.1")
    _write(repo, "pyproject.toml", '[project]\nname = "auteur"\nversion = "0.37.1"\n')
    _write(repo, "src/auteur/__init__.py", '__version__ = "0.37.1"\n')
    _write(repo, "src/auteur/netorare/__init__.py", '__version__ = "0.1.0"\n')
    section = version_drift(repo)
    assert section["declarations"] == 2  # pyproject + top-level package only
    assert section["subpackage_declarations"] == 1
    assert section["findings"] == []


def test_version_claim_from_test_layer(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path, version="0.2.2")
    _write(repo, "tests/test_cli.py", 'assert "0.2.1" in result.output\n')
    section = version_drift(repo)
    assert len(section["findings"]) == 1
    obs = [o for o in section["findings"][0]["observations"]
           if o["source"] == "tests/test_cli.py"]
    assert len(obs) == 1
    assert obs[0]["source_kind"] == "verification"


# ---------------------------------------------------------------------------
# ADR integrity
# ---------------------------------------------------------------------------

def test_adr_catalog_supports_id_widths_and_status_forms(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path)
    _write(repo, "docs/adr/0001-inline.md",
           "# ADR 0001: Inline\n\n**Status**: Accepted\n")
    _write(repo, "docs/adr/001-h2.md",
           "# ADR 001: H2\n\n## Status\n\nProposed\n")
    _write(repo, "docs/adr/002-coloninside.md",
           "# ADR 002: Colon\n\n**Status:** Accepted.\n")
    catalog = adr_catalog(repo)
    by_id = {e["id"]: e for e in catalog}
    assert by_id["0001"]["status"] == "accepted"
    assert by_id["001"]["status"] == "proposed"
    assert by_id["002"]["status"] == "accepted"  # trailing period tolerated


def test_adr_status_mismatch_and_missing_reference(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path)
    _write(repo, "docs/adr/0006-routing.md",
           "# ADR 0006: Routing\n\n**Status**: Proposed\n")
    _write(repo, "CONTEXT.md",
           "ADR 0006 is accepted and governs routing. ADR 0099 is future.\n")
    section = adr_integrity(repo)
    types = {f["finding_type"] for f in section["findings"]}
    assert "status_claim_mismatch" in types
    assert "missing_reference" in types
    mismatch = [f for f in section["findings"]
                if f["finding_type"] == "status_claim_mismatch"][0]
    assert mismatch["requires_semantic_review"] is True
    assert mismatch["observations"][0]["value"] == "proposed"


def test_adr_duplicate_ids_kept_and_reported_per_entry(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path)
    _write(repo, "docs/adr/013-graph.md",
           "# ADR 013: Graph\n\n## Status\n\nProposed\n")
    _write(repo, "docs/adr/013-propagation.md",
           "# ADR 013: Propagation\n\n## Status\n\nProposed\n")
    _write(repo, "CONTEXT.md", "ADR 013 is accepted.\n")
    section = adr_integrity(repo)
    assert section["files"] == 2
    mismatches = [f for f in section["findings"]
                  if f["finding_type"] == "status_claim_mismatch"]
    assert len(mismatches) == 2  # one per catalog entry
    # Issue #172: the duplicate id is a top-level finding, not a catalog-only
    # condition the model must notice by reading raw data.
    dupes = [f for f in section["findings"]
             if f["finding_type"] == "duplicate_id"]
    assert len(dupes) == 1
    d = dupes[0]
    assert d["concept"] == "adr_identifier"
    assert d["requires_semantic_review"] is False
    assert {o["value"] for o in d["observations"]} == {"013"}
    assert len(d["observations"]) == 2  # one observation per declaring file


def test_adr_missing_status_line_is_detected(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path)
    _write(repo, "docs/adr/0001-x.md", "# ADR 0001: X\n")
    section = adr_integrity(repo)
    assert any(f["finding_type"] == "missing_status_line" for f in section["findings"])


# ---------------------------------------------------------------------------
# Assembled section
# ---------------------------------------------------------------------------

def test_relationships_section_shape_and_correct_negative(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path, version="0.2.2")
    _write(repo, "README.md", "Current release: 0.2.2\n")
    rel = relationships(repo)
    assert set(rel) == {"doc_surface", "version", "adr"}
    assert isinstance(rel["doc_surface"], dict)
    assert "by_class" in rel["doc_surface"]
    assert rel["version"]["findings"] == []
    assert rel["adr"]["findings"] == []
    # Every finding carries the provenance contract.
    _write(repo, "README.md", "Current release: 0.2.1\n")
    rel = relationships(repo)
    f = rel["version"]["findings"][0]
    assert f["concept"] and f["finding_type"] and f["observations"]
    assert all("source" in o and "location" in o and "evidence" in o
               for o in f["observations"])


def test_relationships_detects_real_drift(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path, version="0.2.2")
    _write(repo, "docs/guides/install.md", "Current version: 0.2.1\n")
    rel = relationships(repo)
    sources = {o["source"] for o in rel["version"]["findings"][0]["observations"]}
    assert "docs/guides/install.md" in sources  # discovered live doc, not curated


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------

PROBE_SCRIPT = str(Path(__file__).resolve().parents[1] / "scripts" / "probe-repo.py")


def test_cli_includes_relationships_section(tmp_path: Path) -> None:
    repo = _mini_repo(tmp_path, version="0.2.2")
    _write(repo, "README.md", "Current release: 0.2.1\n")
    out = tmp_path / "probe-report.yaml"
    proc = subprocess.run(
        [sys.executable, PROBE_SCRIPT, "--repo-root", str(repo), "--output", str(out)],
        capture_output=True, text=True, cwd=repo,
    )
    assert proc.returncode == 0, proc.stderr
    import yaml
    data = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert data["relationships"]["version"]["findings"]
    assert "relationships" in proc.stdout
    assert "(evidence candidates, not diagnoses)" in proc.stdout
