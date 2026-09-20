from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-strategic-repository-analysis.py"
GENERIC = ROOT / "scripts" / "validate-artifact.py"
CONTRACTS = ROOT / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"


def _analysis_yaml() -> dict:
    lenses = {
        "mission_relevance": "Directly advances the stated repository mission.",
        "decision_value": "Clarifies the main repository evolution decision.",
        "blocking_power": "Resolves a material boundary before downstream work.",
        "evidence_sufficiency": "Current evidence is adequate for bounded commitment.",
        "consequence_of_error": "A wrong choice creates moderate reversible rework.",
        "deferral_cost": "Deferral leaves the central product surface incomplete.",
        "reversibility": "The first intervention is additive and reversible.",
        "authority_availability": "Repository-only construction authority is available.",
        "dependency": "Depends only on already-established repository diagnosis.",
        "smallest_warranted_intervention": "Add the first-class analysis contract.",
    }
    return {
        "artifact_id": "strategic_repository_analysis",
        "target_repository": "owner/repo",
        "target_source_identity": "commit:abc123",
        "governing_intent": "Improve repository-level strategic sensemaking.",
        "capability_states": [
            {
                "capability_id": "repository-diagnosis",
                "state": "ESTABLISHED",
                "evidence_refs": ["skills/repo-sensemaker/SKILL.md:L1-L20"],
            }
        ],
        "strategic_frontier": [
            {
                "frontier_id": "FRONTIER-1",
                "statement": "Strategic construction paths are not first-class.",
            }
        ],
        "construction_paths": [
            {
                "path_id": "PATH-1",
                "name": "First-class strategic repository analysis",
                "future_state": "Repository evidence becomes a strategic decision space.",
                "builds_on": ["repository diagnosis", "Level-3 strategy"],
                "required_capabilities": ["strategic analysis artifact"],
                "construction_sequence": ["contract", "Skill", "integration"],
                "dependencies": ["ADR 0029"],
                "unlocks": ["explicit repository evolution paths"],
                "risks": ["could become unnecessary planning ceremony"],
                "reversibility": "Additive guidance/contract surface.",
                "evidence_gaps": ["real-world usefulness remains a separate claim"],
            }
        ],
        "path_comparison": [{"path_id": "PATH-1", "lenses": lenses}],
        "decision_changing_uncertainty": {
            "statement": "Whether a first-class artifact can remain non-planner guidance.",
            "could_change": "Implementation shape, not owner-authorized objective.",
            "inquiry_warranted": False,
            "evidence_needed": "Normal engineering qualification is sufficient now.",
            "source": "repository_evidence",
        },
        "strategic_disposition": "BUILD",
        "selected_path_id": "PATH-1",
        "candidate_repository_responsibility": "Implement the strategic analysis contract.",
        "smallest_warranted_intervention": "Artifact + Skill + validator integration.",
        "implementation_authority_established_by_artifact": False,
        "semantic_truth_established": False,
        "created_at": "2026-09-20T00:00:00Z",
        "immutable": True,
    }


def _artifact(data: dict) -> str:
    return (
        "# Strategic Repository Analysis\n\n"
        "## 1. Governing Intent and Scope\n\nIntent.\n\n"
        "## 2. Current System Model\n\nSystem.\n\n"
        "## 3. Capability and Limitation Map\n\nMap.\n\n"
        "## 4. Strategic Frontier\n\nFrontier.\n\n"
        "## 5. Candidate Construction Paths\n\nPaths.\n\n"
        "## 6. Qualitative Path Comparison\n\nComparison.\n\n"
        "## 7. Decision-Changing Uncertainty\n\nUncertainty.\n\n"
        "## 8. Strategic Synthesis\n\nSynthesis.\n\n"
        "## 9. Warranted Direction\n\nBUILD.\n\n"
        "## 10. Authority and Claim Boundaries\n\nNo authority granted.\n\n"
        "## 11. Evidence\n\nEvidence.\n\n"
        "## 12. Machine-Readable Summary\n\n"
        "```yaml\n"
        + yaml.safe_dump(data, sort_keys=False)
        + "```\n"
    )


def _run(path: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR), str(path), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed, json.loads(completed.stdout)


def test_artifact_contract_is_declared() -> None:
    data = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))
    contracts = {item["id"]: item for item in data["artifacts"]}
    contract = contracts["strategic_repository_analysis"]

    assert contract["produced_by"] == "strategic-repository-analysis"
    assert "construction_paths" in contract["required_machine_fields"]
    assert "strategic_disposition" in contract["required_machine_fields"]
    assert {"analysis_ref", "continuity", "decision_assumptions"} <= set(
        contract["recommended_machine_fields"]
    )
    assert any("0-5 real paths" in note for note in contract["notes"])
    assert any(
        "validate-strategic-repository-analysis.py" in command
        for command in contract["verification"]["specialized_validators"]
    )


def test_valid_strategic_analysis_passes_specialized_and_generic_validation(tmp_path: Path) -> None:
    path = tmp_path / "analysis.md"
    path.write_text(_artifact(_analysis_yaml()), encoding="utf-8")

    completed, result = _run(path)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert result["valid"] is True
    assert result["semantic_truth_established"] is False
    assert result["strategy_selected_by_validator"] is False
    assert result["implementation_authorized_by_validator"] is False

    generic = subprocess.run(
        [
            sys.executable,
            str(GENERIC),
            "strategic_repository_analysis",
            str(path),
            "--repo-root",
            str(ROOT),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert generic.returncode == 0, generic.stdout + generic.stderr


def test_non_build_disposition_allows_zero_real_paths(tmp_path: Path) -> None:
    data = _analysis_yaml()
    data["construction_paths"] = []
    data["path_comparison"] = []
    data["strategic_disposition"] = "NO_CHANGE"
    data["selected_path_id"] = None
    data["candidate_repository_responsibility"] = None
    data["smallest_warranted_intervention"] = None
    data["decision_changing_uncertainty"] = {
        "statement": "none",
        "could_change": "none",
        "inquiry_warranted": False,
        "evidence_needed": "none",
        "source": "none",
    }
    path = tmp_path / "analysis.md"
    path.write_text(_artifact(data), encoding="utf-8")

    completed, result = _run(path)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert result["valid"] is True
    assert result["strategy_selected_by_validator"] is False
    assert result["implementation_authorized_by_validator"] is False


def test_build_with_zero_paths_fails_closed(tmp_path: Path) -> None:
    data = _analysis_yaml()
    data["construction_paths"] = []
    data["path_comparison"] = []
    data["selected_path_id"] = None
    path = tmp_path / "analysis.md"
    path.write_text(_artifact(data), encoding="utf-8")

    completed, result = _run(path)
    assert completed.returncode == 1
    ids = {item["error_id"] for item in result["errors"]}
    assert "STRATEGIC_ANALYSIS_BUILD_PATH_REQUIRED" in ids


def test_numeric_path_scoring_fails_closed(tmp_path: Path) -> None:
    data = _analysis_yaml()
    data["path_comparison"][0]["lenses"]["mission_relevance"] = 9
    path = tmp_path / "analysis.md"
    path.write_text(_artifact(data), encoding="utf-8")

    completed, result = _run(path)
    assert completed.returncode == 1
    ids = {item["error_id"] for item in result["errors"]}
    assert "STRATEGIC_ANALYSIS_NUMERIC_SCORING_FORBIDDEN" in ids


def test_explicit_score_or_ranking_fields_are_forbidden(tmp_path: Path) -> None:
    data = _analysis_yaml()
    data["construction_paths"][0]["score"] = 100
    path = tmp_path / "analysis.md"
    path.write_text(_artifact(data), encoding="utf-8")

    completed, result = _run(path)
    assert completed.returncode == 1
    ids = {item["error_id"] for item in result["errors"]}
    assert "STRATEGIC_ANALYSIS_SCORING_FIELD_FORBIDDEN" in ids


def test_unknown_capability_state_and_selected_path_fail(tmp_path: Path) -> None:
    data = _analysis_yaml()
    data["capability_states"][0]["state"] = "BEST"
    data["selected_path_id"] = "PATH-404"
    path = tmp_path / "analysis.md"
    path.write_text(_artifact(data), encoding="utf-8")

    completed, result = _run(path)
    assert completed.returncode == 1
    ids = {item["error_id"] for item in result["errors"]}
    assert "STRATEGIC_ANALYSIS_CAPABILITY_STATE_INVALID" in ids
    assert "STRATEGIC_ANALYSIS_SELECTED_PATH_UNKNOWN" in ids


def test_build_requires_path_and_candidate_responsibility(tmp_path: Path) -> None:
    data = _analysis_yaml()
    data["selected_path_id"] = None
    data["candidate_repository_responsibility"] = None
    path = tmp_path / "analysis.md"
    path.write_text(_artifact(data), encoding="utf-8")

    completed, result = _run(path)
    assert completed.returncode == 1
    ids = {item["error_id"] for item in result["errors"]}
    assert "STRATEGIC_ANALYSIS_BUILD_PATH_REQUIRED" in ids
    assert "STRATEGIC_ANALYSIS_BUILD_RESPONSIBILITY_REQUIRED" in ids


def test_artifact_cannot_self_grant_authority_or_truth(tmp_path: Path) -> None:
    data = _analysis_yaml()
    data["implementation_authority_established_by_artifact"] = True
    data["semantic_truth_established"] = True
    path = tmp_path / "analysis.md"
    path.write_text(_artifact(data), encoding="utf-8")

    completed, result = _run(path)
    assert completed.returncode == 1
    ids = {item["error_id"] for item in result["errors"]}
    assert "STRATEGIC_ANALYSIS_AUTHORITY_BOUNDARY_INVALID" in ids
    assert "STRATEGIC_ANALYSIS_SEMANTIC_AUTHORITY_INVALID" in ids


def test_optional_continuity_and_assumption_metadata_is_mechanically_checked(tmp_path: Path) -> None:
    data = _analysis_yaml()
    data["analysis_ref"] = "SRA-2"
    data["continuity"] = {
        "prior_analysis_ref": "SRA-1",
        "disposition": "CONTINUE",
        "prior_selected_path_id": "PATH-1",
        "reason": "The same path remains material.",
    }
    data["decision_assumptions"] = [
        {
            "assumption_id": "ASSUMPTION-1",
            "statement": "The repository boundary remains stable.",
            "evidence_refs": ["docs/product-strategy.md"],
            "reassessment_triggers": ["The product boundary changes."],
        }
    ]
    data["construction_paths"][0]["assumptions"] = [
        "The repository boundary remains stable."
    ]
    data["construction_paths"][0]["reassessment_triggers"] = [
        "The product boundary changes."
    ]
    path = tmp_path / "analysis.md"
    path.write_text(_artifact(data), encoding="utf-8")

    completed, result = _run(path)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert result["valid"] is True
    assert "optional_continuity_and_assumption_integrity" in result["checks"]


def test_invalid_continuity_metadata_fails_closed(tmp_path: Path) -> None:
    data = _analysis_yaml()
    data["continuity"] = {
        "prior_analysis_ref": "SRA-1",
        "disposition": "AUTO_BEST",
        "prior_selected_path_id": None,
        "reason": "",
    }
    path = tmp_path / "analysis.md"
    path.write_text(_artifact(data), encoding="utf-8")

    completed, result = _run(path)
    assert completed.returncode == 1
    ids = {item["error_id"] for item in result["errors"]}
    assert "STRATEGIC_ANALYSIS_CONTINUITY_DISPOSITION_INVALID" in ids
    assert "STRATEGIC_ANALYSIS_CONTINUITY_REASON_INVALID" in ids
