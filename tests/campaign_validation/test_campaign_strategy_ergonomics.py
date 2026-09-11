"""Repository/hermetic qualification for explicit Level-3 strategy ergonomics."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.campaigns import CampaignService
from sensemaking_skills.cli import cli


def _status(frontier: str, *, uncertainty: str = "Which boundary matters?", responsibility: str = "No responsibility selected.") -> str:
    return f"""# Status

## Strategic Repository Evolution state — Level 3

### Current product strategy
- **Level-4 authority:** `docs/product-strategy.md`.
- **Control model:** `docs/strategic-outer-loop.md`.
- **Level-3 contract:** `docs/strategic-state-contract.md`.
- **Level-4 revision contract:** `docs/product-thesis-revision.md`.

### Current capability state
Capabilities are declared.

### Material limitations and evidence ceilings
Repository qualification does not prove product value.

### Strategic Frontier
1. **{frontier} — AUTHORIZED BY OWNER DIRECTION.** Explicit candidate for this fixture.

### Current highest-leverage boundary
{frontier}

### Current decision-changing uncertainty
{uncertainty}

### Current warranted repository-level responsibility
{responsibility}

### Authority / owner direction
Owner may explicitly authorize bounded work.

### Thesis review state
`THESIS_REVIEW_REQUIRED`: **NO**.
"""


def test_strategy_inspect_projects_without_ranking(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "STATUS.md").write_text(_status("Campaign ergonomics"), encoding="utf-8")
    result = CliRunner().invoke(cli, ["campaign", "strategy", "inspect", "--repo-root", str(repo), "--json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["required_sections_present"] is True
    assert payload["strategic_frontier"][0]["name"] == "Campaign ergonomics"
    assert payload["semantic_ranking_performed"] is False
    assert payload["semantic_recommendation_included"] is False


def test_strategy_diff_reports_representation_change_without_preference(tmp_path: Path) -> None:
    before = tmp_path / "before.md"
    after = tmp_path / "after.md"
    before.write_text(_status("A", uncertainty="U1"), encoding="utf-8")
    after.write_text(_status("B", uncertainty="U2", responsibility="Build B."), encoding="utf-8")
    result = CliRunner().invoke(cli, ["campaign", "strategy", "diff", "--from-status", str(before), "--to-status", str(after), "--json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert "Strategic Frontier" in payload["changed_sections"]
    assert "Current decision-changing uncertainty" in payload["changed_sections"]
    assert payload["better_state_selected"] is False
    assert payload["semantic_ranking_performed"] is False


def test_strategy_handoff_requires_explicit_frontier_identity_and_creates_campaign(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "STATUS.md").write_text(_status("Campaign ergonomics"), encoding="utf-8")
    workspace = tmp_path / "campaign"
    runner = CliRunner()
    rejected = runner.invoke(
        cli,
        [
            "campaign", "strategy", "handoff",
            "--repo-root", str(repo),
            "--workspace", str(workspace),
            "--campaign-id", "CMP-STRATEGY",
            "--mission", "execute explicit Level-3 responsibility",
            "--frontier-item", "Not in frontier",
            "--responsibility-id", "R-STRAT",
            "--responsibility-type", "repository_diagnosis",
            "--responsibility-statement", "diagnose the explicit boundary",
            "--decision-blocked", "which repair to perform",
            "--scope", "repository",
            "--authority", "authorized_autonomously",
            "--success-condition", "diagnosis produced",
        ],
    )
    assert rejected.exit_code != 0
    assert "must exactly match" in rejected.output
    assert not workspace.exists()

    accepted = runner.invoke(
        cli,
        [
            "campaign", "strategy", "handoff",
            "--repo-root", str(repo),
            "--workspace", str(workspace),
            "--campaign-id", "CMP-STRATEGY",
            "--mission", "execute explicit Level-3 responsibility",
            "--frontier-item", "Campaign ergonomics",
            "--responsibility-id", "R-STRAT",
            "--responsibility-type", "repository_diagnosis",
            "--responsibility-statement", "diagnose the explicit boundary",
            "--decision-blocked", "which repair to perform",
            "--scope", "repository",
            "--authority", "authorized_autonomously",
            "--success-condition", "diagnosis produced",
            "--json",
        ],
    )
    assert accepted.exit_code == 0, accepted.output
    payload = json.loads(accepted.output)
    assert payload["selection_performed_by_tool"] is False
    snapshot = CampaignService(workspace).resume()
    assert snapshot.state.active_responsibility.id == "R-STRAT"
    assert snapshot.state.extensions["strategy_handoff"]["frontier_item"] == "Campaign ergonomics"
    handoff = json.loads((workspace / "strategy-handoff.json").read_text(encoding="utf-8"))
    assert handoff["selection_performed_by_tool"] is False
    assert handoff["frontier_item"] == "Campaign ergonomics"
