"""Qualification for Strategic Continuity v1 and root strategy projections."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.cli import cli


def _analysis(
    *,
    source_identity: str = "sha:abc1234",
    disposition: str = "BUILD",
    selected_path: str | None = "PATH-1",
    capability_state: str = "PARTIAL",
    continuity: bool = True,
) -> str:
    continuity_block = """
analysis_ref: SRA-2
continuity:
  prior_analysis_ref: SRA-1
  disposition: CONTINUE
  prior_selected_path_id: PATH-1
  reason: "The prior path remains material."
decision_assumptions:
  - assumption_id: ASSUMPTION-1
    statement: "The repository boundary remains stable."
    evidence_refs:
      - docs/product-strategy.md
    reassessment_triggers:
      - "The product boundary changes."
""" if continuity else ""
    selected = "null" if selected_path is None else selected_path
    return f"""# Strategic Repository Analysis

## Machine-Readable Summary

```yaml
artifact_id: strategic_repository_analysis
target_repository: owner/repo
target_source_identity: "{source_identity}"
governing_intent: "Improve repository decisions."
capability_states:
  - capability_id: core
    state: {capability_state}
    evidence_refs:
      - docs/product-strategy.md
strategic_frontier:
  - frontier_id: FRONTIER-1
    statement: "A material boundary exists."
construction_paths:
  - path_id: PATH-1
    name: "Continue core"
    future_state: "A stronger core."
    builds_on: ["core"]
    required_capabilities: ["continuity"]
    construction_sequence: ["record", "reassess"]
    dependencies: ["evidence"]
    unlocks: ["continuation"]
    risks: ["stale assumptions"]
    reversibility: "High"
    evidence_gaps: ["consumer pressure"]
    assumptions: ["The current boundary remains stable."]
    reassessment_triggers: ["The product boundary changes."]
path_comparison:
  - path_id: PATH-1
    lenses:
      mission_relevance: "Direct"
      decision_value: "Material"
      blocking_power: "Relevant"
      evidence_sufficiency: "Bounded"
      consequence_of_error: "Reversible"
      deferral_cost: "Moderate"
      reversibility: "High"
      authority_availability: "Available"
      dependency: "Known"
      smallest_warranted_intervention: "Continue the bounded path."
decision_changing_uncertainty:
  statement: "Whether the boundary remains stable."
  could_change: "The selected path."
  inquiry_warranted: false
  evidence_needed: "None now."
  source: repository_evidence
strategic_disposition: {disposition}
selected_path_id: {selected}
candidate_repository_responsibility: "Continue the bounded path."
smallest_warranted_intervention: "Record continuity."
implementation_authority_established_by_artifact: false
semantic_truth_established: false
{continuity_block}created_at: "2026-09-20T04:40:00Z"
immutable: true
```
"""


def test_root_strategy_inspect_paths_uncertainty_and_assumptions(tmp_path: Path) -> None:
    artifact = tmp_path / "analysis.md"
    artifact.write_text(_analysis(), encoding="utf-8")
    runner = CliRunner()

    inspected = runner.invoke(cli, ["strategy", "inspect", "--artifact", str(artifact), "--json"])
    assert inspected.exit_code == 0, inspected.output
    payload = json.loads(inspected.output)
    assert payload["path_count"] == 1
    assert payload["assumption_count"] == 1
    assert payload["strategy_selected_by_command"] is False

    paths = runner.invoke(cli, ["strategy", "paths", "--artifact", str(artifact), "--json"])
    assert paths.exit_code == 0, paths.output
    assert json.loads(paths.output)["ranked"] is False

    uncertainty = runner.invoke(cli, ["strategy", "uncertainty", "--artifact", str(artifact), "--json"])
    assert uncertainty.exit_code == 0, uncertainty.output
    assert json.loads(uncertainty.output)["inquiry_selected_by_command"] is False

    assumptions = runner.invoke(cli, ["strategy", "assumptions", "--artifact", str(artifact), "--json"])
    assert assumptions.exit_code == 0, assumptions.output
    assert json.loads(assumptions.output)["assumptions"][0]["assumption_id"] == "ASSUMPTION-1"


def test_strategy_compare_reports_declared_changes_without_ranking(tmp_path: Path) -> None:
    before = tmp_path / "before.md"
    after = tmp_path / "after.md"
    before.write_text(_analysis(capability_state="PARTIAL", continuity=False), encoding="utf-8")
    after.write_text(_analysis(capability_state="ESTABLISHED"), encoding="utf-8")

    result = CliRunner().invoke(
        cli,
        ["strategy", "compare", "--before", str(before), "--after", str(after), "--json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["capability_changes"][0]["before"] == "PARTIAL"
    assert payload["capability_changes"][0]["after"] == "ESTABLISHED"
    assert payload["quality_ranked_by_command"] is False
    assert payload["continuity_after"]["disposition"] == "CONTINUE"


def test_strategy_drift_detects_git_head_change_without_invalidating_strategy(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    (repo / "docs").mkdir()
    (repo / "docs" / "product-strategy.md").write_text("strategy", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()

    artifact = tmp_path / "analysis.md"
    artifact.write_text(_analysis(source_identity=f"sha:{head}"), encoding="utf-8")
    runner = CliRunner()

    current = runner.invoke(
        cli, ["strategy", "drift", "--artifact", str(artifact), "--repo", str(repo), "--json"]
    )
    assert current.exit_code == 0, current.output
    payload = json.loads(current.output)
    assert payload["source_identity_status"] == "CURRENT"
    assert payload["strategy_invalidated_by_command"] is False

    (repo / "next.txt").write_text("next", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "next"], cwd=repo, check=True, capture_output=True)

    drifted = runner.invoke(
        cli, ["strategy", "drift", "--artifact", str(artifact), "--repo", str(repo), "--json"]
    )
    assert drifted.exit_code == 0, drifted.output
    payload = json.loads(drifted.output)
    assert payload["source_identity_status"] == "DRIFTED"
    assert payload["mechanical_drift_detected"] is True
    assert payload["reanalysis_required_by_command"] is False
