"""Qualification for Multi-Repository Strategic Sensemaking v1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SPECIAL = ROOT / "scripts" / "validate-multi-repository-strategic-analysis.py"
GENERIC = ROOT / "scripts" / "validate-artifact.py"
CONTRACTS = ROOT / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"


def _data() -> dict:
    lenses = {
        "mission_relevance": "Directly clarifies the product boundary.",
        "decision_value": "Changes which repository owns future capability.",
        "blocking_power": "Resolves a boundary before duplicated construction.",
        "evidence_sufficiency": "Repository evidence is sufficient for a bounded choice.",
        "consequence_of_error": "The first step is reversible but later coupling would be costly.",
        "deferral_cost": "Deferral preserves duplicate ambiguity.",
        "reversibility": "The interface-first step is reversible.",
        "authority_availability": "Analysis authority exists; mutation remains separate.",
        "dependency": "Depends on the explicit target set and current interfaces.",
        "smallest_warranted_intervention": "Stabilize the interface boundary first.",
    }
    return {
        "artifact_id": "multi_repository_strategic_analysis",
        "analysis_ref": "MRSA-1",
        "governing_intent": "Clarify decision versus orchestration ownership.",
        "target_repositories": [
            {
                "alias": "sensemaking",
                "repository": "owner/sensemaking",
                "source_identity": "main@abc",
                "role": "decision support",
                "evidence_refs": ["README.md"],
            },
            {
                "alias": "factory",
                "repository": "owner/factory",
                "source_identity": "main@def",
                "role": "execution orchestration",
                "evidence_refs": ["README.md"],
            },
        ],
        "explicit_relations": [
            {
                "relation_id": "REL-1",
                "source_alias": "factory",
                "target_alias": "sensemaking",
                "relation_type": "consumes_interface_from",
                "evidence_refs": ["docs/integration.md"],
            }
        ],
        "capability_ownership": [
            {
                "capability_id": "execution_handoff",
                "current_owner_aliases": ["sensemaking"],
                "state": "ESTABLISHED",
                "evidence_refs": ["docs/campaign-execution-interface-v1.md"],
                "boundary_consequence": "Defines the decision/orchestration seam.",
            }
        ],
        "boundary_tensions": [
            {
                "tension_id": "TENSION-1",
                "statement": "The two products could duplicate execution selection.",
            }
        ],
        "construction_paths": [
            {
                "path_id": "PATH-1",
                "name": "Stable decision/orchestration interface",
                "future_state": "Sensemaking selects bounded responsibility; factory coordinates it.",
                "capability_allocations": [
                    {
                        "capability_id": "execution_handoff",
                        "proposed_owner_aliases": ["sensemaking"],
                        "boundary_pattern": "keep stable interface",
                    }
                ],
                "boundary_changes": ["Make the interface contract explicit."],
                "construction_sequence": ["stabilize interface", "adapt consumer"],
                "dependencies": ["explicit executor interchange"],
                "unlocks": ["independent evolution"],
                "risks": ["interface ossification"],
                "reversibility": "High for the first additive contract step.",
                "evidence_gaps": ["consumer pressure may change the split"],
            }
        ],
        "path_comparison": [{"path_id": "PATH-1", "lenses": lenses}],
        "decision_changing_uncertainty": {
            "statement": "Whether the factory needs semantic responsibility selection.",
            "could_change": "The repository capability boundary.",
            "inquiry_warranted": False,
            "evidence_needed": "No additional evidence for this fixture.",
            "source": "repository_evidence",
        },
        "strategic_disposition": "BUILD",
        "selected_path_id": "PATH-1",
        "candidate_repository_responsibility": "Stabilize the decision/orchestration interface.",
        "affected_target_aliases": ["sensemaking", "factory"],
        "automatic_repository_discovery_performed": False,
        "target_scope_expanded_by_artifact": False,
        "implementation_authority_established_by_artifact": False,
        "semantic_truth_established": False,
        "created_at": "2026-09-20T05:30:00Z",
        "immutable": True,
    }


def _artifact(data: dict) -> str:
    sections = [
        "Governing Intent, Scope, and Authority",
        "Current Multi-Repository System Model",
        "Capability Ownership and Overlap Map",
        "Explicit Relationships and Cross-Repository Evidence",
        "Boundary Tensions",
        "Candidate Boundary / Allocation Paths",
        "Qualitative Path Comparison",
        "Decision-Changing Uncertainty",
        "Strategic Synthesis and Warranted Direction",
        "Authority and Claim Boundaries",
        "Evidence",
    ]
    text = "# Multi-Repository Strategic Analysis\n"
    for index, heading in enumerate(sections, 1):
        text += f"\n## {index}. {heading}\n\nDeclared.\n"
    text += (
        "\n## 12. Machine-Readable Summary\n\n```yaml\n"
        + yaml.safe_dump(data, sort_keys=False)
        + "```\n"
    )
    return text


def _run(path: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
    completed = subprocess.run(
        [sys.executable, str(SPECIAL), str(path), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed, json.loads(completed.stdout)


def test_valid_multi_repository_analysis_passes_specialized_and_generic(tmp_path: Path) -> None:
    path = tmp_path / "multi.md"
    path.write_text(_artifact(_data()), encoding="utf-8")

    completed, payload = _run(path)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert payload["valid"] is True
    assert payload["automatic_repository_discovery_performed"] is False
    assert payload["target_scope_expanded_by_validator"] is False
    assert payload["strategy_selected_by_validator"] is False
    assert payload["implementation_authorized_by_validator"] is False

    generic = subprocess.run(
        [
            sys.executable,
            str(GENERIC),
            "multi_repository_strategic_analysis",
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


def test_unknown_target_relation_and_allocation_fail_closed(tmp_path: Path) -> None:
    data = _data()
    data["explicit_relations"][0]["source_alias"] = "discovered"
    data["construction_paths"][0]["capability_allocations"][0]["proposed_owner_aliases"] = [
        "discovered"
    ]
    path = tmp_path / "multi.md"
    path.write_text(_artifact(data), encoding="utf-8")

    completed, payload = _run(path)
    assert completed.returncode == 1
    codes = {item["error_id"] for item in payload["errors"]}
    assert "MULTI_REPO_ANALYSIS_RELATION_ALIAS_INVALID" in codes
    assert "MULTI_REPO_ANALYSIS_ALLOCATION_OWNER_INVALID" in codes


def test_analysis_cannot_claim_discovery_scope_expansion_or_authority(tmp_path: Path) -> None:
    data = _data()
    data["automatic_repository_discovery_performed"] = True
    data["target_scope_expanded_by_artifact"] = True
    data["implementation_authority_established_by_artifact"] = True
    data["semantic_truth_established"] = True
    path = tmp_path / "multi.md"
    path.write_text(_artifact(data), encoding="utf-8")

    completed, payload = _run(path)
    assert completed.returncode == 1
    assert "MULTI_REPO_ANALYSIS_BOUNDARY_INVALID" in {
        item["error_id"] for item in payload["errors"]
    }


def test_numeric_comparison_is_rejected(tmp_path: Path) -> None:
    data = _data()
    data["path_comparison"][0]["lenses"]["mission_relevance"] = 10
    path = tmp_path / "multi.md"
    path.write_text(_artifact(data), encoding="utf-8")
    completed, payload = _run(path)
    assert completed.returncode == 1
    assert "MULTI_REPO_ANALYSIS_NUMERIC_SCORING_FORBIDDEN" in {
        item["error_id"] for item in payload["errors"]
    }


def test_product_surfaces_register_multi_repository_analysis() -> None:
    contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))["artifacts"]
    assert "multi_repository_strategic_analysis" in {item["id"] for item in contracts}

    registry = yaml.safe_load(
        (ROOT / "skills" / "workflow-planner" / "references" / "skill-registry.yaml").read_text(
            encoding="utf-8"
        )
    )
    core = {item["id"] for item in registry["ecosystems"]["core"]["skills"]}
    assert "multi-repository-strategic-analysis" in core

    domain = yaml.safe_load((ROOT / "domain-packs" / "engineering.yaml").read_text(encoding="utf-8"))
    assert "multi_repository_strategic_analysis" in domain["artifact_contracts"]
    assert "multi_repository_strategic_analysis" in domain["responsibility_vocabulary"]

    release = yaml.safe_load((ROOT / "release-v1.0.yaml").read_text(encoding="utf-8"))
    assert "multi-repository-strategic-analysis" in release["skill_inventory"]["supported"]
