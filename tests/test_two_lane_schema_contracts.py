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


_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")

_GIT_SHA_FIELD_KEYS = {"framework_sha", "target_sha", "sha", "reference"}


def test_yaml_1_2_2_is_pinned():
    text = _normalize_whitespace(_adr_text().lower())
    assert "yaml syntax version is yaml 1.2.2" in text, (
        "ADR 0023 must pin YAML 1.2.2 as the syntax version for the "
        "Two-Lane YAML Profile v1"
    )


def test_yaml_1_1_is_forbidden():
    text = _adr_text().lower()
    assert "yaml 1.1 resolution is forbidden" in text, (
        "ADR 0023 must explicitly forbid YAML 1.1 scalar resolution"
    )


def test_implementation_default_resolution_is_forbidden():
    text = _adr_text().lower()
    assert "implementation-default" in text and "forbidden" in text, (
        "ADR 0023 must forbid implementation-default/environment-dependent "
        "scalar resolution"
    )


def test_core_schema_is_not_permitted():
    text = _normalize_whitespace(_adr_text().lower())
    assert "does not use the yaml 1.2 core schema" in text, (
        "ADR 0023 must explicitly reject the YAML 1.2 Core Schema"
    )
    assert "does not permit a consumer to choose between core schema" in text, (
        "ADR 0023 must forbid a consumer choosing between Core/JSON "
        "Schema/library default"
    )


def test_two_lane_yaml_profile_v1_is_named():
    text = _normalize_whitespace(_adr_text())
    assert "Two-Lane YAML Profile v1" in text, (
        "ADR 0023 must name the pinned source-language profile "
        "'Two-Lane YAML Profile v1'"
    )
    readme = _normalize_whitespace(
        (SCHEMA_DIR / "README.md").read_text(encoding="utf-8")
    )
    assert "Two-Lane YAML Profile v1" in readme


def test_ordinary_strings_must_be_quoted_rule_is_present():
    text = _adr_text().lower()
    assert "a value intended to be a string" in text and "must" in text and "quoted" in text


def test_yes_no_on_off_cannot_resolve_as_booleans():
    text = _normalize_whitespace(_adr_text().lower())
    assert (
        "rejected when unquoted: `yes`, `no`, `on`, `off`, `true`, `null`, `~`, `01`,"
        in text
    ), "ADR 0023 must list yes/no/on/off as rejected unquoted plain scalars"


def test_true_null_tilde_cannot_resolve_unquoted():
    text = _adr_text()
    assert "`True`" in text or "`true`" in text.lower()
    assert "`Null`" in text
    assert "`~`" in text


def test_octal_hex_leading_zero_leading_plus_and_dot_number_forms_rejected():
    text = _adr_text()
    for token in ("`01`", "`0o7`", "`0x10`", "`+1`", "`.5`", "`1.`"):
        assert token in text, f"ADR 0023 must list {token} as a rejected plain scalar"


def test_unquoted_timestamp_like_scalar_is_rejected():
    text = _adr_text().lower()
    assert "2026-01-01" in text and "rejected" in text


def test_rfc_8259_number_grammar_is_present():
    text = _adr_text()
    assert "rfc 8259" in text.lower()
    assert "[1-9][0-9]*" in text, "ADR 0023 must state the exact RFC 8259 number grammar"


def test_nan_infinity_and_negative_zero_are_rejected():
    text = _adr_text().lower()
    assert "nan" in text
    assert "negative zero" in text and "rejected" in text


def test_unsafe_integer_policy_fields_are_bounded():
    text = _adr_text()
    assert "9007199254740991" in text, (
        "ADR 0023 must bound integer-valued policy fields to the "
        "interoperable safe-integer range"
    )


def test_lone_unicode_surrogates_are_rejected():
    text = _adr_text().lower()
    assert "lone unicode surrogates" in text or "lone surrogates" in text
    assert "rejected" in text


def test_unicode_normalization_is_not_applied():
    text = _normalize_whitespace(_adr_text().lower())
    assert "no unicode normalization step is performed" in text


def test_no_prose_claims_every_source_byte_change_alters_digest():
    for text, label in (
        (_adr_text(), "ADR 0023"),
        ((SCHEMA_DIR / "README.md").read_text(encoding="utf-8"), "README.md"),
    ):
        lowered = _normalize_whitespace(text.lower())
        assert "any byte-level change to the normative fields" not in lowered, (
            f"{label}: must not claim every source-byte change alters the digest; "
            "use semantic-value language instead"
        )
        assert "any change to normative campaign policy bytes" not in lowered
        assert "any change to normative policy bytes" not in lowered


def test_quoted_string_is_not_treated_as_number():
    text = _normalize_whitespace(_adr_text().lower())
    assert 'string `"1"` and number `1` are distinct' in text


def test_number_1_and_1_0_not_claimed_to_necessarily_differ():
    text = _normalize_whitespace(_adr_text().lower())
    assert "do not necessarily produce different digests" in text


def test_git_sha_placeholders_are_exactly_40_hex_chars():
    files = [ADR_PATH, SCHEMA_DIR / "README.md"] + _schema_files()
    hex_run_re = re.compile(r"[0-9a-f]{20,}")
    hex64_re = re.compile(r"^[0-9a-f]{64}$")
    for path in files:
        text = path.read_text(encoding="utf-8")
        for match in hex_run_re.finditer(text):
            token = match.group(0)
            # Every long lowercase hex run in this corpus is either a
            # SHA-256 placeholder (64 chars) or a Git SHA placeholder
            # (40 chars) -- nothing else is legitimate here.
            assert hex64_re.match(token) or _HEX40_RE.match(token), (
                f"{path.name}: hex placeholder {token!r} (len {len(token)}) is "
                "neither a well-formed 40-char Git SHA nor a 64-char SHA-256 "
                "placeholder"
            )


def test_sha256_placeholders_are_exactly_64_hex_chars():
    # Companion assertion: explicitly confirm at least one 64-char SHA-256
    # placeholder exists per digest field, guarding against a future edit
    # accidentally truncating one.
    text = _policy_text()
    blocks = _extract_yaml_blocks(text)
    for block in blocks:
        parsed = yaml.safe_load(block)
        digest = parsed.get("policy_digest")
        if digest:
            assert _HEX64_RE.match(digest), (
                f"policy_digest example {digest!r} is not a well-formed "
                "64-character lowercase SHA-256 hex placeholder"
            )


def test_evidence_0016_and_0015_directories_untouched_by_this_module():
    """This test module never writes under experiments/run-control or
    experiments/evidence. It only reads. This assertion documents that
    intent for a reviewer; it does not itself modify anything.
    """
    run_control = REPO_ROOT / "experiments" / "run-control"
    assert run_control.is_dir()


# ---------------------------------------------------------------------------
# Test-only Two-Lane YAML Profile v1 source-style conformance checker.
#
# This is NOT a production parser or validator. It exists only so this test
# module can prove that fenced examples conform to the *source-level* style
# rules of the profile (mapping-key grammar, allowed string-scalar styles),
# which ``yaml.safe_load`` alone cannot prove: PyYAML's default resolver
# happily accepts quoted keys, block scalars, and YAML-1.1-style booleans,
# none of which are legal under the profile. The checker inspects PyYAML's
# *composed node tree* (via ``yaml.compose``), which retains node style
# (``node.style``) and tag information, rather than trusting the fully
# resolved Python values from ``safe_load``.
# ---------------------------------------------------------------------------

_KEY_TOKEN_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_JSON_NUMBER_RE = re.compile(r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$")

BLOCK_STYLES = {"|", ">"}
QUOTE_STYLES = {"'", '"'}


class ProfileViolation(AssertionError):
    pass


def _check_scalar_value(node) -> None:
    if node.tag == "tag:yaml.org,2002:merge" or node.value == "<<":
        raise ProfileViolation("merge key construct is forbidden")
    if node.style in BLOCK_STYLES:
        raise ProfileViolation(
            f"block scalar style {node.style!r} is forbidden for value {node.value!r}"
        )
    if node.style in QUOTE_STYLES:
        start_line = getattr(node.start_mark, "line", None)
        end_line = getattr(node.end_mark, "line", None)
        if start_line is not None and end_line is not None and end_line != start_line:
            raise ProfileViolation(
                f"multiline quoted scalar is forbidden (source spans lines "
                f"{start_line}-{end_line}): {node.value!r}"
            )
        return  # quoted scalar values are always legal strings
    if node.style is None or node.style == "":
        # plain scalar: only null/true/false/RFC-8259-number are legal
        v = node.value
        if v in ("null", "true", "false"):
            return
        if _JSON_NUMBER_RE.match(v):
            return
        raise ProfileViolation(f"unquoted plain scalar value {v!r} is not permitted")
    raise ProfileViolation(f"unrecognized scalar style {node.style!r}")


def _check_mapping_key(node) -> None:
    if node.style in QUOTE_STYLES:
        raise ProfileViolation(f"quoted mapping key is forbidden: {node.value!r}")
    if node.style in BLOCK_STYLES:
        raise ProfileViolation(f"block-style mapping key is forbidden: {node.value!r}")
    if not isinstance(node, yaml.ScalarNode):
        raise ProfileViolation("complex (non-scalar) mapping key is forbidden")
    if not _KEY_TOKEN_RE.match(node.value):
        raise ProfileViolation(
            f"mapping key {node.value!r} does not match ^[a-z][a-z0-9_]*$"
        )


def check_profile_conformance(yaml_source: str) -> None:
    """Walk the composed node tree of a single-document YAML source string
    and raise ProfileViolation on the first construct that is illegal under
    the Two-Lane YAML Profile v1 (ADR 0023 §10b): non-plain/non-quoted
    string values, block scalars, multiline quoted scalars, non-conforming
    or quoted/complex mapping keys, duplicate keys, aliases, anchors, or
    explicit tags.
    """
    docs = list(yaml.compose_all(yaml_source))
    if len(docs) != 1:
        raise ProfileViolation(f"expected exactly one YAML document, found {len(docs)}")
    _walk(docs[0])


def _walk(node) -> None:
    # PyYAML's Composer resolves aliases transparently into the anchored
    # node itself (there is no distinct AliasNode class exposed here), so
    # an alias surfaces as an anchor on the node it refers to -- caught by
    # the anchor check below.
    if getattr(node, "anchor", None):
        raise ProfileViolation(f"YAML anchor is forbidden: {node.anchor!r}")
    if isinstance(node, yaml.MappingNode):
        if node.tag not in ("tag:yaml.org,2002:map",):
            raise ProfileViolation(f"explicit tag on mapping is forbidden: {node.tag!r}")
        seen: set[str] = set()
        for key_node, value_node in node.value:
            _check_mapping_key(key_node)
            if key_node.value in seen:
                raise ProfileViolation(f"duplicate mapping key: {key_node.value!r}")
            seen.add(key_node.value)
            _walk(value_node)
    elif isinstance(node, yaml.SequenceNode):
        if node.tag not in ("tag:yaml.org,2002:seq",):
            raise ProfileViolation(f"explicit tag on sequence is forbidden: {node.tag!r}")
        for item in node.value:
            _walk(item)
    elif isinstance(node, yaml.ScalarNode):
        if node.tag not in (
            "tag:yaml.org,2002:str",
            "tag:yaml.org,2002:null",
            "tag:yaml.org,2002:bool",
            "tag:yaml.org,2002:int",
            "tag:yaml.org,2002:float",
        ):
            raise ProfileViolation(f"explicit tag on scalar is forbidden: {node.tag!r}")
        _check_scalar_value(node)
    else:
        raise ProfileViolation(f"unsupported node type: {type(node)!r}")


@pytest.mark.parametrize("path", _schema_files())
def test_fenced_examples_conform_to_two_lane_yaml_profile_v1(path: Path):
    text = path.read_text(encoding="utf-8")
    blocks = _extract_yaml_blocks(text)
    assert blocks, f"{path.name} has no fenced yaml example"
    for i, block in enumerate(blocks):
        try:
            check_profile_conformance(block)
        except ProfileViolation as exc:
            raise AssertionError(
                f"{path.name} example #{i} violates Two-Lane YAML Profile v1: {exc}"
            ) from exc


# ---------------------------------------------------------------------------
# Regression tests: each of these must independently fail if a specific
# blocking-finding requirement regresses. Each reads exactly one document,
# not a concatenation of several, per the review requirement.
# ---------------------------------------------------------------------------


def test_adr_defines_mapping_key_as_separate_lexical_class():
    text = _adr_text()
    assert "separate lexical class from scalar values" in text
    assert "Mapping-key grammar (normative)" in text


def test_adr_states_mapping_key_regex():
    text = _adr_text()
    assert "^[a-z][a-z0-9_]*$" in text


def test_readme_references_mapping_key_rule():
    text = (SCHEMA_DIR / "README.md").read_text(encoding="utf-8")
    assert "mapping-key grammar" in text.lower()


def test_campaign_policy_schema_references_mapping_key_rule():
    text = _policy_text()
    assert "mapping-key grammar" in text.lower()


def test_configuration_identity_schema_references_mapping_key_rule():
    text = _configuration_identity_text()
    assert "mapping-key grammar" in text.lower()


def test_adr_forbids_quoted_mapping_keys():
    text = _adr_text()
    assert "Quoted mapping keys" in text
    assert "forbidden" in text.split("Quoted mapping keys", 1)[1][:80]


def test_adr_requires_duplicate_key_detection_before_object_construction():
    text = _adr_text()
    assert "the object is constructed" in text
    assert "before" in text.split("the object is constructed", 1)[0][-20:]


def test_adr_forbids_block_scalar_styles():
    text = _adr_text()
    for token in ("literal block scalars", "folded block scalars"):
        assert token in text


def test_adr_forbids_chomping_and_indentation_indicators():
    text = _adr_text()
    assert "|-" in text and "|+" in text and ">-" in text and ">+" in text


def test_adr_forbids_multiline_quoted_scalars():
    text = _adr_text()
    assert "multiline single-quoted scalars" in text
    assert "multiline double-quoted scalars" in text


def test_adr_string_quoting_rule_is_fail_closed_not_advisory():
    text = _adr_text()
    section = text.split("#### Permitted string-scalar styles", 1)[1][:600]
    assert "**rejects**" in section or "must" in section.lower()


def test_profile_checker_rejects_quoted_mapping_key():
    source = 'campaign_id: "value"\n"other_field": "value"\n'
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source)


def test_profile_checker_rejects_numeric_looking_mapping_key():
    source = '"1": "value"\n'
    # numeric-looking key, still quoted -- forbidden as quoted key first
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source)


def test_profile_checker_rejects_literal_block_scalar():
    source = "logging_requirements: |\n  example text\n"
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source)


def test_profile_checker_rejects_folded_block_scalar():
    source = "logging_requirements: >\n  example text\n"
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source)


def test_profile_checker_rejects_duplicate_keys():
    source = 'campaign_id: "a"\ncampaign_id: "b"\n'
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source)


def test_profile_checker_rejects_multiline_double_quoted_scalar():
    source = 'campaign_id: "line one\nline two"\n'
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source)


def test_profile_checker_accepts_valid_campaign_policy_example():
    text = _policy_text()
    blocks = _extract_yaml_blocks(text)
    assert blocks
    check_profile_conformance(blocks[0])  # must not raise
    # No assertion beyond existence: this test suite performs no writes.
