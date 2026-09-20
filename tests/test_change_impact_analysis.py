"""Qualification for Change-Impact Sensemaking v1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SPECIAL = ROOT / "scripts" / "validate-change-impact-analysis.py"
GENERIC = ROOT / "scripts" / "validate-artifact.py"
CONTRACTS = ROOT / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"


def _data() -> dict:
    return {
        "artifact_id": "change_impact_analysis",
        "analysis_ref": "CIA-1",
        "target_repository": "owner/repo",
        "target_source_identity": "main@abc",
        "change": {
            "change_id": "CHANGE-1",
            "state": "IMPLEMENTED",
            "statement": "Change the execution handoff contract.",
            "evidence_refs": ["PR#1"],
        },
        "impact_items": [
            {
                "surface_id": "IMPACT-1",
                "category": "contract",
                "target_ref": "docs/campaign-execution-interface-v1.md",
                "impact_statement": "The contract wording must remain aligned.",
                "evidence_refs": ["docs/campaign-execution-interface-v1.md"],
                "semantic_review_required": True,
                "required_actions": ["Reconcile contract semantics."],
                "authority_boundary": "repository-only",
            },
            {
                "surface_id": "IMPACT-2",
                "category": "test",
                "target_ref": "tests/test_execution_interface_closeout.py",
                "impact_statement": "Closure regression must still describe the new contract.",
                "evidence_refs": ["tests/test_execution_interface_closeout.py"],
                "semantic_review_required": False,
                "required_actions": ["Run the closure regression."],
                "authority_boundary": "repository-only",
            },
        ],
        "cross_repository_impacts": [
            {
                "repository_alias": "factory",
                "repository": "owner/factory",
                "impact_statement": "The consumer adapter may need reconciliation.",
                "evidence_refs": ["docs/integration.md"],
            }
        ],
        "claim_consequences": [
            {
                "claim_ref": "CLAIM-1",
                "effect": "The integration-compatibility claim must be reverified.",
            }
        ],
        "followup_responsibilities": [
            {
                "responsibility_id": "FOLLOWUP-1",
                "statement": "Run finding-specific contract verification.",
                "affected_surface_ids": ["IMPACT-1", "IMPACT-2"],
            }
        ],
        "closure_effect": "ADDITIONAL_VERIFICATION_REQUIRED",
        "automatic_repository_discovery_performed": False,
        "change_authorized_by_artifact": False,
        "followup_execution_authorized_by_artifact": False,
        "semantic_truth_established": False,
        "created_at": "2026-09-20T06:00:00Z",
        "immutable": True,
    }


def _artifact(data: dict) -> str:
    sections = [
        "Change Scope and Authority",
        "Impact Evidence",
        "Affected Surfaces",
        "Cross-Repository Impact",
        "Claim and Verification Consequences",
        "Bounded Follow-Up Responsibilities",
        "Closure Effect",
        "Authority and Claim Boundaries",
    ]
    text = "# Change Impact Analysis\n"
    for index, heading in enumerate(sections, 1):
        text += f"\n## {index}. {heading}\n\nDeclared.\n"
    text += (
        "\n## 9. Machine-Readable Summary\n\n```yaml\n"
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


def test_valid_change_impact_analysis_passes_specialized_and_generic(tmp_path: Path) -> None:
    path = tmp_path / "impact.md"
    path.write_text(_artifact(_data()), encoding="utf-8")
    completed, payload = _run(path)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert payload["valid"] is True
    assert payload["material_impact_selected_by_validator"] is False
    assert payload["change_authorized_by_validator"] is False
    assert payload["followup_execution_authorized_by_validator"] is False

    generic = subprocess.run(
        [
            sys.executable,
            str(GENERIC),
            "change_impact_analysis",
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


def test_followup_must_reference_known_impact_surfaces(tmp_path: Path) -> None:
    data = _data()
    data["followup_responsibilities"][0]["affected_surface_ids"] = ["MISSING"]
    path = tmp_path / "impact.md"
    path.write_text(_artifact(data), encoding="utf-8")
    completed, payload = _run(path)
    assert completed.returncode == 1
    assert "CHANGE_IMPACT_FOLLOWUP_SURFACES_INVALID" in {
        item["error_id"] for item in payload["errors"]
    }


def test_analysis_cannot_authorize_change_followup_or_discovery(tmp_path: Path) -> None:
    data = _data()
    data["automatic_repository_discovery_performed"] = True
    data["change_authorized_by_artifact"] = True
    data["followup_execution_authorized_by_artifact"] = True
    data["semantic_truth_established"] = True
    path = tmp_path / "impact.md"
    path.write_text(_artifact(data), encoding="utf-8")
    completed, payload = _run(path)
    assert completed.returncode == 1
    assert "CHANGE_IMPACT_BOUNDARY_INVALID" in {
        item["error_id"] for item in payload["errors"]
    }


def test_scoring_fields_are_forbidden(tmp_path: Path) -> None:
    data = _data()
    data["impact_items"][0]["severity_score"] = 9
    path = tmp_path / "impact.md"
    path.write_text(_artifact(data), encoding="utf-8")
    completed, payload = _run(path)
    assert completed.returncode == 1
    assert "CHANGE_IMPACT_SCORING_FIELD_FORBIDDEN" in {
        item["error_id"] for item in payload["errors"]
    }


def test_product_surfaces_register_change_impact_analysis() -> None:
    contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))["artifacts"]
    assert "change_impact_analysis" in {item["id"] for item in contracts}

    registry = yaml.safe_load(
        (ROOT / "skills" / "workflow-planner" / "references" / "skill-registry.yaml").read_text(
            encoding="utf-8"
        )
    )
    core = {item["id"] for item in registry["ecosystems"]["core"]["skills"]}
    assert "change-impact-analysis" in core

    domain = yaml.safe_load((ROOT / "domain-packs" / "engineering.yaml").read_text(encoding="utf-8"))
    assert "change_impact_analysis" in domain["artifact_contracts"]
    assert "change_impact_analysis" in domain["responsibility_vocabulary"]

    release = yaml.safe_load((ROOT / "release-v1.0.yaml").read_text(encoding="utf-8"))
    assert "change-impact-analysis" in release["skill_inventory"]["supported"]
