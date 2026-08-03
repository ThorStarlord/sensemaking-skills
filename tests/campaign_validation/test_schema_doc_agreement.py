"""Cross-check the machine-readable JSON schemas against the normative field
tables in the Markdown schema-contract documents, so documentation and
implementation cannot silently drift apart.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MD_DIR = REPO_ROOT / "docs" / "experiments" / "schemas" / "two-lane-v1"
JSON_DIR = MD_DIR / "json"
PACKAGED_SCHEMA_DIR = (
    REPO_ROOT / "src" / "sensemaking_skills" / "campaign_validation" / "schemas"
)

FIELD_ROW_RE = re.compile(r"^\|\s*`([a-z_]+)`\s*\|")


def _md_required_fields(md_filename: str) -> set[str]:
    text = (MD_DIR / md_filename).read_text(encoding="utf-8")
    # Only the "Required fields" table -- stop at the next `##` heading.
    start = text.index("## Required fields")
    end = text.index("\n## ", start + 1) if "\n## " in text[start + 1:] else len(text)
    section = text[start:end]
    fields = set()
    for line in section.splitlines():
        m = FIELD_ROW_RE.match(line)
        if m:
            fields.add(m.group(1))
    return fields


def _json_schema_properties(json_filename: str) -> set[str]:
    schema = json.loads((JSON_DIR / json_filename).read_text(encoding="utf-8"))
    if "properties" in schema:
        return set(schema["properties"].keys())
    # oneOf-discriminated schema (campaign-approval): union of both branches.
    fields: set[str] = set()
    for branch in schema.get("oneOf", []):
        fields |= set(branch.get("properties", {}).keys())
    return fields


def test_campaign_policy_fields_match_doc():
    md_fields = _md_required_fields("campaign-policy.schema.md")
    json_fields = _json_schema_properties("campaign-policy.v1.schema.json")
    assert md_fields == json_fields, (md_fields ^ json_fields)


def test_configuration_identity_fields_match_doc():
    md_fields = _md_required_fields("configuration-identity.schema.md")
    json_fields = _json_schema_properties("configuration-identity.v1.schema.json")
    assert md_fields == json_fields, (md_fields ^ json_fields)


def test_campaign_approval_fields_match_doc_excluding_marker():
    md_fields = _md_required_fields("campaign-approval.schema.md")
    json_fields = _json_schema_properties("campaign-approval.v1.schema.json")
    # `marker` is documented as present-in-examples-only / absent-when-operative,
    # so it legitimately appears in the JSON schema's example branch even
    # though it is one row in the same doc table -- both sides already
    # include it, so a straight equality check is correct here too.
    assert md_fields == json_fields, (md_fields ^ json_fields)


def test_packaged_schemas_are_byte_identical_to_docs_originals():
    """The runtime loads schemas as PACKAGED resources
    (``sensemaking_skills/campaign_validation/schemas/*.json``), not from
    ``docs/``, so an installed wheel works with no repository checkout.
    That packaged copy must never silently drift from the human-authored
    ``docs/`` original -- diff byte-for-byte on every commit.
    """
    for filename in (
        "campaign-policy.v1.schema.json",
        "campaign-approval.v1.schema.json",
        "configuration-identity.v1.schema.json",
    ):
        docs_bytes = (JSON_DIR / filename).read_bytes()
        packaged_bytes = (PACKAGED_SCHEMA_DIR / filename).read_bytes()
        assert docs_bytes == packaged_bytes, (
            f"{filename}: packaged schema resource has drifted from the docs/ original"
        )
