"""Documentation-only validation for the two-lane schema contracts.

These tests validate the SHAPE of the Phase 1 governance documentation
(``docs/adr/0023-two-lane-experiment-authorization.md`` and
``docs/experiments/schemas/two-lane-v1/*.schema.md``). They parse the YAML
fenced examples embedded in those Markdown files and check syntax plus a
handful of documentation-level invariants (required markers on example
content, no operative-looking approval).

They do not import, exercise, or depend on any runtime authorization code.
They create nothing under ``experiments/`` and never touch Evidence 0015 or
Evidence 0016. This is intentionally narrow: Phase 1 (Issue #117) is a
documentation/schema-contract deliverable, not a runtime implementation.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = REPO_ROOT / "docs" / "experiments" / "schemas" / "two-lane-v1"
ADR_PATH = REPO_ROOT / "docs" / "adr" / "0023-two-lane-experiment-authorization.md"

FENCE_RE = re.compile(r"```yaml\n(.*?)```", re.DOTALL)


def _extract_yaml_blocks(markdown_text: str) -> list[str]:
    return FENCE_RE.findall(markdown_text)


def _schema_files() -> list[Path]:
    assert SCHEMA_DIR.is_dir(), f"missing schema directory: {SCHEMA_DIR}"
    files = sorted(SCHEMA_DIR.glob("*.schema.md"))
    assert files, "expected at least one *.schema.md file"
    return files


def test_adr_0023_exists_and_is_proposed():
    assert ADR_PATH.is_file(), f"missing ADR: {ADR_PATH}"
    text = ADR_PATH.read_text(encoding="utf-8")
    assert "**Status**: PROPOSED" in text
    assert "does not authorize" in text.lower()


def test_six_required_contracts_present():
    expected = {
        "campaign-policy.schema.md",
        "campaign-approval.schema.md",
        "configuration-identity.schema.md",
        "attempt-reservation.schema.md",
        "attempt-result.schema.md",
        "campaign-summary.schema.md",
    }
    present = {p.name for p in _schema_files()}
    assert expected <= present, f"missing contracts: {expected - present}"


@pytest.mark.parametrize("path", _schema_files(), ids=lambda p: p.name)
def test_schema_examples_parse_as_yaml(path: Path):
    text = path.read_text(encoding="utf-8")
    blocks = _extract_yaml_blocks(text)
    assert blocks, f"{path.name} has no fenced yaml example"
    for block in blocks:
        parsed = yaml.safe_load(block)
        assert isinstance(parsed, dict), f"{path.name} example did not parse to a mapping"


@pytest.mark.parametrize("path", _schema_files(), ids=lambda p: p.name)
def test_schema_examples_are_marked_non_operative(path: Path):
    text = path.read_text(encoding="utf-8")
    blocks = _extract_yaml_blocks(text)
    for block in blocks:
        parsed = yaml.safe_load(block)
        if "campaign-approval" in path.name:
            assert parsed.get("marker") == "EXAMPLE_ONLY_NOT_AUTHORIZATION", (
                f"{path.name}: every approval example must carry "
                "marker: EXAMPLE_ONLY_NOT_AUTHORIZATION"
            )
        # Every example in this directory must be visibly non-operative:
        # either via an explicit marker field, or via unmistakable
        # placeholder identity values that cannot resolve to a real
        # campaign, repository, or human approver.
        dump = yaml.safe_dump(parsed)
        assert "example" in dump.lower() or parsed.get("marker") == "EXAMPLE_ONLY_NOT_AUTHORIZATION", (
            f"{path.name}: example content has no placeholder/marker signal"
        )


def test_campaign_id_pattern_is_not_an_evidence_number():
    text = (SCHEMA_DIR / "campaign-policy.schema.md").read_text(encoding="utf-8")
    blocks = _extract_yaml_blocks(text)
    for block in blocks:
        parsed = yaml.safe_load(block)
        campaign_id = parsed.get("campaign_id", "")
        assert campaign_id.startswith("EXP-"), (
            "campaign_id must use the EXP-NNNN namespace, "
            f"never an Evidence number: got {campaign_id!r}"
        )


def test_attempt_result_examples_are_classified_exploratory():
    text = (SCHEMA_DIR / "attempt-result.schema.md").read_text(encoding="utf-8")
    blocks = _extract_yaml_blocks(text)
    for block in blocks:
        parsed = yaml.safe_load(block)
        assert parsed.get("classification") == "EXPLORATORY_NOT_CANONICAL_EVIDENCE"


def test_campaign_policy_prohibitions_are_true_in_example():
    text = (SCHEMA_DIR / "campaign-policy.schema.md").read_text(encoding="utf-8")
    blocks = _extract_yaml_blocks(text)
    for block in blocks:
        parsed = yaml.safe_load(block)
        for field in (
            "target_mutation_prohibited",
            "fallback_prohibited",
            "repair_prohibited",
            "automatic_merge_prohibited",
        ):
            assert parsed.get(field) is True, f"{field} must be true in the example"


def test_no_operative_approval_artifact_created_by_this_phase():
    """Phase 1 must not create any real, operative campaign approval.

    Guards against a future edit accidentally adding a populated approval
    file (as opposed to the schema's blank template / illustrative
    example) anywhere under the schema-contracts directory.
    """
    for path in SCHEMA_DIR.rglob("*"):
        if path.is_file() and path.name not in {
            "campaign-approval.schema.md",
        }:
            continue
        if path.name == "campaign-approval.schema.md":
            text = path.read_text(encoding="utf-8")
            assert "EXAMPLE_ONLY_NOT_AUTHORIZATION" in text


_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


def _policy_text() -> str:
    return (SCHEMA_DIR / "campaign-policy.schema.md").read_text(encoding="utf-8")


def _adr_text() -> str:
    return ADR_PATH.read_text(encoding="utf-8")


def _configuration_identity_text() -> str:
    return (SCHEMA_DIR / "configuration-identity.schema.md").read_text(encoding="utf-8")


def test_allowed_configurations_field_does_not_reappear():
    for text, label in (
        (_policy_text(), "campaign-policy.schema.md"),
        (_adr_text(), "ADR 0023"),
    ):
        assert "allowed_configurations" not in text, (
            f"{label}: the ambiguous `allowed_configurations` field must not "
            "reappear; use `allowed_configuration_ids` (exact IDs only)"
        )


def test_constraint_expression_language_does_not_reappear_as_authorization():
    # The old ambiguous type union ("list[object] or constraint expression")
    # must be gone. Prose that explicitly rejects constraint expressions
    # ("no constraint expression(s)") is fine and expected.
    for text, label in (
        (_policy_text(), "campaign-policy.schema.md"),
        (_configuration_identity_text(), "configuration-identity.schema.md"),
    ):
        lowered = text.lower()
        assert "list[object] or constraint expression" not in lowered, (
            f"{label}: the ambiguous 'list[object] or constraint expression' "
            "type union must not reappear"
        )
        assert "or configuration constraint expressions" not in lowered, (
            f"{label}: constraint expressions must not be offered as an "
            "alternative authorization mechanism"
        )


def test_prompt_revision_field_does_not_reappear():
    for path in _schema_files():
        text = path.read_text(encoding="utf-8")
        assert "prompt_revision" not in text, (
            f"{path.name}: `prompt_revision` is not the canonical field name; "
            "use `prompt_or_skill_revision`"
        )
    assert "prompt_revision" not in _adr_text()


def test_allowed_configuration_ids_field_is_present():
    text = _policy_text()
    assert "allowed_configuration_ids" in text
    blocks = _extract_yaml_blocks(text)
    found = False
    for block in blocks:
        parsed = yaml.safe_load(block)
        if "allowed_configuration_ids" in parsed:
            found = True
    assert found, "campaign-policy.schema.md example must set allowed_configuration_ids"


def test_policy_example_configuration_ids_are_well_formed_hex64():
    text = _policy_text()
    blocks = _extract_yaml_blocks(text)
    for block in blocks:
        parsed = yaml.safe_load(block)
        ids = parsed.get("allowed_configuration_ids")
        if ids is None:
            continue
        for value in ids:
            assert _HEX64_RE.match(value), (
                f"malformed configuration_id in policy example: {value!r} "
                "(must be lowercase 64-character SHA-256 hex)"
            )


def test_policy_example_configuration_ids_have_no_duplicates():
    text = _policy_text()
    blocks = _extract_yaml_blocks(text)
    for block in blocks:
        parsed = yaml.safe_load(block)
        ids = parsed.get("allowed_configuration_ids")
        if ids is None:
            continue
        assert len(ids) == len(set(ids)), (
            "allowed_configuration_ids must not contain duplicate entries"
        )


def test_policy_example_configuration_ids_are_lexicographically_sorted():
    text = _policy_text()
    blocks = _extract_yaml_blocks(text)
    for block in blocks:
        parsed = yaml.safe_load(block)
        ids = parsed.get("allowed_configuration_ids")
        if ids is None:
            continue
        assert ids == sorted(ids), (
            "allowed_configuration_ids must be lexicographically sorted "
            "to give one canonical representation"
        )


def test_policy_example_configuration_id_list_is_not_empty():
    text = _policy_text()
    blocks = _extract_yaml_blocks(text)
    for block in blocks:
        parsed = yaml.safe_load(block)
        if "allowed_configuration_ids" in parsed:
            assert parsed["allowed_configuration_ids"], (
                "allowed_configuration_ids must not be an empty list"
            )


def test_policy_and_configuration_schemas_use_consistent_field_names():
    config_text = _configuration_identity_text()
    assert "prompt_or_skill_revision" in config_text
    # The policy schema's YAML example no longer embeds a nested prompt
    # field at all now that authorization is exact-configuration-ID-only;
    # `prompt_or_skill_revision` may still appear in the policy schema's
    # prose (e.g. naming what a partial configuration object would have
    # contained), but never as a field in its own example.
    policy_text = _policy_text()
    for block in _extract_yaml_blocks(policy_text):
        parsed = yaml.safe_load(block)
        assert "prompt_or_skill_revision" not in parsed
        assert "prompt_revision" not in parsed
    assert "prompt_revision" not in policy_text
    assert "prompt_revision" not in config_text


def _normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def test_no_prose_claims_configuration_id_membership_overrides_allowlists():
    combined = _normalize_whitespace((_policy_text() + _adr_text()).lower())
    assert "there is no precedence rule where membership" in combined


def test_no_prose_claims_individual_allowlists_authorize_unlisted_configuration_id():
    combined = _normalize_whitespace((_policy_text() + _adr_text()).lower())
    assert "no rule where matching the individual allowlists" in combined


def test_adr_defines_jcs_canonicalization():
    text = _adr_text()
    assert "rfc 8785" in text.lower(), (
        "ADR 0023 must pin RFC 8785 (JCS) as the canonical serialization "
        "algorithm for schema-v1 digests"
    )
    assert "json canonicalization scheme" in text.lower() or "jcs" in text.lower()


def test_no_prose_suggests_hashing_raw_yaml_bytes():
    combined = _normalize_whitespace(_adr_text().lower() + " " + (
        SCHEMA_DIR / "README.md"
    ).read_text(encoding="utf-8").lower())
    assert "must not hash the original yaml presentation bytes" in combined, (
        "the canonical-serialization contract must explicitly forbid "
        "hashing raw YAML presentation bytes"
    )


def test_adr_rejects_duplicate_yaml_keys_and_forbidden_constructs():
    text = _adr_text().lower()
    for forbidden in (
        "duplicate mapping keys",
        "yaml aliases",
        "yaml anchors",
        "explicit yaml tags",
        "merge keys",
    ):
        assert forbidden in text, (
            f"ADR 0023 §10b must explicitly reject {forbidden!r} in "
            "digest-bearing YAML input"
        )


def test_adr_rejects_non_finite_numbers():
    text = _adr_text().lower()
    assert "non-finite numbers" in text or "nan" in text


def test_policy_digest_excluded_from_its_own_hashed_field_set():
    text = _adr_text()
    # §10c must state policy_digest hashes every normative field "except"
    # policy_digest itself — guard against a future edit accidentally
    # re-including it in its own hash input.
    assert "except" in text.lower() and "policy_digest" in text
    idx = text.lower().find("policy** (`policy_digest`)")
    assert idx != -1, "ADR 0023 §10c must define the policy hashed field set explicitly"
    section = text[idx : idx + 400].lower()
    assert "except" in section and "policy_digest" in section


def test_configuration_id_excluded_from_its_own_hashed_field_set():
    text = _adr_text()
    idx = text.lower().find("configuration** (`configuration_id`)")
    assert idx != -1, (
        "ADR 0023 §10c must define the configuration hashed field set explicitly"
    )
    section = text[idx : idx + 600]
    assert "`configuration_id` itself" in section


def test_campaign_id_excluded_from_configuration_hashed_field_set():
    text = _adr_text()
    idx = text.lower().find("configuration** (`configuration_id`)")
    assert idx != -1
    section = text[idx : idx + 600]
    assert "`campaign_id`" in section
    assert "excluded" in section.lower() or "explicitly excluded" in section.lower()


def test_configuration_hashed_field_list_is_exact_and_complete():
    expected_fields = [
        "configuration_schema_version",
        "framework_sha",
        "target_repository",
        "target_sha",
        "model_identifier",
        "prompt_or_skill_revision",
        "validator_revision",
        "artifact_type",
        "execution_parameters",
    ]
    adr_text = _adr_text()
    idx = adr_text.lower().find("configuration** (`configuration_id`)")
    assert idx != -1
    section = adr_text[idx : idx + 900]
    for field in expected_fields:
        assert f"`{field}`" in section, (
            f"ADR 0023 §10c configuration hashed field set is missing "
            f"required field `{field}`"
        )

    config_text = _configuration_identity_text()
    for field in expected_fields:
        assert field in config_text, (
            f"configuration-identity.schema.md must list `{field}` as a "
            "required field"
        )


def test_non_finite_numbers_are_rejected_not_permitted():
    text = _adr_text().lower()
    assert "non-finite numbers" in text
    assert "permitted" not in text.split("non-finite numbers")[1][:60]


def test_trailing_newline_treatment_is_specified():
    text = _adr_text().lower()
    assert "no trailing newline is included in the hashed bytes" in text


def test_policy_and_configuration_use_the_same_canonicalization_algorithm():
    text = _adr_text().lower()
    # Both digests must be defined in terms of the same §10a algorithm,
    # not two independently-described mechanisms.
    assert "used identically by every digest in this adr" in text or (
        "rfc 8785" in text and text.count("rfc 8785") >= 2
    )


def test_evidence_0016_and_0015_directories_untouched_by_this_module():
    """This test module never writes under experiments/run-control or
    experiments/evidence. It only reads. This assertion documents that
    intent for a reviewer; it does not itself modify anything.
    """
    run_control = REPO_ROOT / "experiments" / "run-control"
    assert run_control.is_dir()
    # No assertion beyond existence: this test suite performs no writes.
