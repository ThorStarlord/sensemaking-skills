"""JSON Schema (Draft 2020-12) validation against the restricted data model.

Loads the three machine-readable schemas as **packaged resources** via
``importlib.resources`` -- from ``sensemaking_skills.campaign_validation.schemas``,
a subpackage shipped inside this package's own installed location -- and
validates already-parsed (Two-Lane YAML Profile v1) mappings against them.
Schema validation is a distinct, later stage from source-token parsing:
parsing establishes the restricted JSON-compatible value; schema validation
establishes field/type legality.

These packaged JSON files are byte-identical copies of the canonical,
human-authored originals under
``docs/experiments/schemas/two-lane-v1/json/`` (the docs copy remains the
source of truth for human review/PRs; the packaged copy is what actually
ships and loads at runtime). A dedicated test
(``tests/campaign_validation/test_schema_doc_agreement.py``) diffs the two
copies byte-for-byte so they cannot silently drift apart.

Loading via ``importlib.resources`` (rather than a
``Path(__file__).parents[...] / "docs"`` filesystem walk) is what makes
this module work correctly from an installed wheel: a wheel has no
``docs/`` directory and no repository checkout at all, but it does have
this package's own packaged resource files.
"""

from __future__ import annotations

import json
from importlib import resources
from typing import Any

import jsonschema

_SCHEMA_PACKAGE = "sensemaking_skills.campaign_validation.schemas"

_cache: dict[str, jsonschema.Validator] = {}


def _load_validator(filename: str) -> jsonschema.Validator:
    if filename not in _cache:
        schema_text = resources.files(_SCHEMA_PACKAGE).joinpath(filename).read_text(encoding="utf-8")
        schema = json.loads(schema_text)
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
