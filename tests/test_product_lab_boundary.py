from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).parents[1]


def _validator_module():
    path = ROOT / "scripts" / "validate-product-boundary.py"
    spec = importlib.util.spec_from_file_location("validate_product_boundary", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_product_lab_boundary_contract_is_valid():
    validator = _validator_module()
    assert validator.validate() == []


def test_historical_combined_workflow_is_retained_outside_actions_directory():
    archived = ROOT / "docs" / "archive" / "ci" / "validator-ecosystem-pre-core-lab-split.yml"
    assert archived.is_file()
    text = archived.read_text(encoding="utf-8")
    assert "phase3-exploratory-authorization:" in text
    assert "phase4-campaign-ledger:" in text
    assert "phase6-execution-boundary:" in text
