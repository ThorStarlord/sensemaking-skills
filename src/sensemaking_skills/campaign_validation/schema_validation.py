"""JSON Schema (Draft 2020-12) validation against the restricted data model.

Loads the three machine-readable schemas under
``docs/experiments/schemas/two-lane-v1/json/`` and validates already-parsed
(Two-Lane YAML Profile v1) mappings against them. Schema validation is a
distinct, later stage from source-token parsing: parsing establishes the
restricted JSON-compatible value; schema validation establishes field/type
legality.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

_SCHEMA_DIR = Path(__file__).resolve().parents[3] / "docs" / "experiments" / "schemas" / "two-lane-v1" / "json"

_cache: dict[str, jsonschema.Validator] = {}


def _load_validator(filename: str) -> jsonschema.Validator:
    if filename not in _cache:
        schema_path = _SCHEMA_DIR / filename
        with schema_path.open(encoding="utf-8") as f:
            schema = json.load(f)
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
        _cache[filename] = validator_cls(schema)
    return _cache[filename]


def validate_against_schema(document: Any, filename: str) -> list[str]:
    """Return a list of human-readable error strings (empty = valid)."""
    validator = _load_validator(filename)
    errors = sorted(validator.iter_errors(document), key=lambda e: list(e.path))
    return [f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}" for e in errors]


def policy_schema_errors(document: Any) -> list[str]:
    return validate_against_schema(document, "campaign-policy.v1.schema.json")


def approval_schema_errors(document: Any) -> list[str]:
    return validate_against_schema(document, "campaign-approval.v1.schema.json")


def configuration_schema_errors(document: Any) -> list[str]:
    return validate_against_schema(document, "configuration-identity.v1.schema.json")
