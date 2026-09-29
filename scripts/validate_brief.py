"""Import-compatible shim for the canonical ``validate-brief.py`` module.

The hyphenated filename remains the CLI and validator identity. This shim
exists for Python callers that need an importable module name and re-exports
the canonical implementation without maintaining a second validator.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


_CANONICAL = Path(__file__).with_name("validate-brief.py")
_SPEC = importlib.util.spec_from_file_location("_canonical_validate_brief", _CANONICAL)
if _SPEC is None or _SPEC.loader is None:  # pragma: no cover - import failure
    raise ImportError(f"cannot load canonical validator: {_CANONICAL}")
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

validate_brief = _MODULE.validate_brief
validation_result_to_json = _MODULE.validation_result_to_json
ValidationError = _MODULE.ValidationError
ValidationResult = _MODULE.ValidationResult

__all__ = [
    "ValidationError",
    "ValidationResult",
    "validate_brief",
    "validation_result_to_json",
]
