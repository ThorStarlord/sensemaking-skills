from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _module():
    path = ROOT / "scripts" / "validate-error-boundaries.py"
    spec = importlib.util.spec_from_file_location("validate_error_boundaries", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_shipped_error_boundaries_have_no_silent_broad_handlers():
    assert _module().validate(ROOT) == []

