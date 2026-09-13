from __future__ import annotations

import hashlib
import json
from importlib import import_module
import inspect
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "public-api-v1.0.yaml"


def _exports_digest(exports: list[str]) -> str:
    payload = json.dumps(exports, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _signature_digest(module) -> str:
    signatures = {}
    for name in module.__all__:
        value = getattr(module, name)
        if callable(value):
            try:
                signatures[name] = str(inspect.signature(value))
            except (TypeError, ValueError):
                signatures[name] = f"<callable:{value.__module__}.{value.__qualname__}>"
        else:
            signatures[name] = type(value).__name__
    payload = json.dumps(signatures, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_stable_python_exports_are_explicit_and_frozen() -> None:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1

    for module_name, contract in manifest["modules"].items():
        module = import_module(module_name)
        exports = getattr(module, "__all__", None)
        assert isinstance(exports, list), f"{module_name} must define __all__"
        assert all(isinstance(name, str) and name for name in exports)
        for name in exports:
            assert hasattr(module, name), f"{module_name}.{name} is missing"
        assert _exports_digest(exports) == contract["exports_sha256"]
        assert _signature_digest(module) == contract["signatures_sha256"]


def test_public_api_manifest_is_linked_from_surface_document() -> None:
    text = (ROOT / "docs" / "public-surface-v1.0.md").read_text(encoding="utf-8")
    assert "public-api-v1.0.yaml" in text
