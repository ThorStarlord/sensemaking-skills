"""Tests for the advisory stale-Accepted-ADR probe finding.

Added for the semantic-control-map persistence trial
(docs/semantic-control-map-trial.md). The finding is
`stale_accepted_adr_candidate`: a newer Accepted ADR uses supersession
language about an older ADR whose own **Status** is still Accepted.

Contract:
  - requires_semantic_review is True (the model adjudicates);
  - the finding_type is NOT in gate_relationship_findings.BLOCKING_FINDING_TYPES
    (advisory / non-blocking);
  - a correct-negative repo produces no such finding.
"""

from pathlib import Path

from scripts.probe_relationships import adr_integrity
from scripts.gate_relationship_findings import BLOCKING_FINDING_TYPES, evaluate


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    _write(repo, "pyproject.toml", '[project]\nname = "x"\nversion = "0.1.0"\n')
    return repo


def _sac(repo: Path):
    return [f for f in adr_integrity(repo)["findings"]
            if f["finding_type"] == "stale_accepted_adr_candidate"]


def test_fires_when_newer_accepted_adr_supersedes_older_still_accepted(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _write(repo, "docs/adr/0005-auto-invoke.md",
           "# ADR 0005: Auto invoke\n\n**Status**: Accepted\n\nSkills chain automatically.\n")
    _write(repo, "docs/adr/0013-agent-native.md",
           "# ADR 0013: Agent native\n\n**Status**: Accepted\n\n"
           "- **ADR 0005**: auto-invocation (now superseded by the skill-led model)\n")
    findings = _sac(repo)
    assert len(findings) == 1
    f = findings[0]
    assert f["observations"][0]["value"] == "0005"
    assert f["observations"][0]["source"] == "docs/adr/0013-agent-native.md"
    assert f["requires_semantic_review"] is True
    assert f["confidence"] == "medium"


def test_matches_the_superced_misspelling(tmp_path: Path) -> None:
    """docs/adr/0013 in the real repo says 'now superceded by skill-led model'."""
    repo = _repo(tmp_path)
    _write(repo, "docs/adr/0012-paths.md",
           "# ADR 0012\n\n**Status**: Accepted\n\nManual and automation paths.\n")
    _write(repo, "docs/adr/0013-agent-native.md",
           "# ADR 0013\n\n**Status**: Accepted\n\n"
           "- **ADR 0012**: invocation paths (now superceded by skill-led model)\n")
    assert len(_sac(repo)) == 1


def test_no_finding_when_older_adr_status_already_superseded(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _write(repo, "docs/adr/0005-auto-invoke.md",
           "# ADR 0005\n\n**Status**: Superseded\n\nSkills chain automatically.\n")
    _write(repo, "docs/adr/0013-agent-native.md",
           "# ADR 0013\n\n**Status**: Accepted\n\n- ADR 0005 is superseded by the skill-led model\n")
    assert _sac(repo) == []


def test_no_finding_when_referencing_adr_not_accepted(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _write(repo, "docs/adr/0005-auto-invoke.md",
           "# ADR 0005\n\n**Status**: Accepted\n\nSkills chain automatically.\n")
    _write(repo, "docs/adr/0018-routing.md",
           "# ADR 0018\n\n**Status**: SUPERSEDED - never Accepted\n\n"
           "table-driven routing (ADR 0005) is no longer the policy\n")
    assert _sac(repo) == []


def test_no_finding_without_supersession_cue(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _write(repo, "docs/adr/0005-auto-invoke.md",
           "# ADR 0005\n\n**Status**: Accepted\n\nSkills chain automatically.\n")
    _write(repo, "docs/adr/0013-agent-native.md",
           "# ADR 0013\n\n**Status**: Accepted\n\n- See **ADR 0005** for auto-invocation mechanics\n")
    assert _sac(repo) == []


def test_no_finding_when_reference_points_forward(tmp_path: Path) -> None:
    """A lower-id ADR referencing a higher-id one with a cue must not fire."""
    repo = _repo(tmp_path)
    _write(repo, "docs/adr/0005-auto-invoke.md",
           "# ADR 0005\n\n**Status**: Accepted\n\n"
           "superseded discussion of **ADR 0013** appears here\n")
    _write(repo, "docs/adr/0013-agent-native.md",
           "# ADR 0013\n\n**Status**: Accepted\n\nAgent owns the loop.\n")
    assert _sac(repo) == []


def test_finding_is_never_blocking(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _write(repo, "docs/adr/0005-auto-invoke.md",
           "# ADR 0005\n\n**Status**: Accepted\n\nSkills chain automatically.\n")
    _write(repo, "docs/adr/0013-agent-native.md",
           "# ADR 0013\n\n**Status**: Accepted\n\n- **ADR 0005**: now superseded by the skill-led model\n")
    assert "stale_accepted_adr_candidate" not in BLOCKING_FINDING_TYPES
    report = {"relationships": {"adr": adr_integrity(repo)}}
    blocking, evidence = evaluate(report)
    assert all(e["finding_type"] != "stale_accepted_adr_candidate" for e in blocking)
    assert any(e["finding_type"] == "stale_accepted_adr_candidate" for e in evidence)


def test_correct_negative_repo_has_no_finding(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _write(repo, "docs/adr/0001-a.md", "# ADR 0001\n\n**Status**: Accepted\n\nFirst.\n")
    _write(repo, "docs/adr/0002-b.md",
           "# ADR 0002\n\n**Status**: Accepted\n\nBuilds on **ADR 0001**, no conflict.\n")
    assert _sac(repo) == []
