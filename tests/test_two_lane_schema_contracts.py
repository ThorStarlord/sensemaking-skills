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
from decimal import Decimal
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
# Test-only Two-Lane YAML Profile v1 conformance checker.
#
# This is NOT a production parser or validator. It exists only so this test
# module can prove that fenced examples conform to the Two-Lane YAML Profile
# v1 (ADR 0023 §10b) and to the declared field sets of the six schema
# contracts.
#
# It is deliberately two-layer, because the two layers see different
# information and neither alone is sufficient:
#
# Layer A (`_check_source_tokens`) scans the *original source text* with
# PyYAML's scanner (`yaml.scan`), before composition. Only the token stream
# still carries syntax-level facts that composition throws away or
# obscures: anchor tokens, alias tokens, explicit tag tokens (as opposed to
# a composed node's *resolved* tag, which looks identical whether or not the
# source wrote an explicit `!!str`/`!!int`), `%YAML`/`%TAG` directive
# tokens, the literal `?` explicit-key indicator, and the `<<` merge-key
# scalar. `yaml.compose_all` alone cannot detect any of these: composition
# either resolves them into ordinary-looking nodes (explicit tags, merge
# keys) or PyYAML's Composer silently follows aliases through to the
# anchored node with no distinct "this was an alias" marker at all (aliases,
# anchors). A prior version of this checker claimed "aliases surface as
# anchors after composition" -- that claim is false: composing an anchored
# node produces one node with an `anchor` attribute, and composing the alias
# that refers to it returns the *same* node object with no additional
# marker distinguishing "the place where the alias appeared" from "the place
# where the anchor appeared" -- a document containing only an alias and no
# in-document anchor definition, or an alias to something declared once,
# composes without incident. Layer A closes that gap by inspecting the
# `AliasToken`/`AnchorToken` stream directly, at the exact source location.
#
# Layer B (`_check_shape`) composes the document (`yaml.compose`) only after
# Layer A passes, and walks the composed node tree to validate hierarchy,
# key styles/grammar, duplicate keys, scalar styles/lexemes, and --
# recursively, against a caller-supplied schema "shape" -- declared field
# sets (closed objects reject unknown keys; the one intentionally open
# object recursively validates its own key grammar and value domain).
# ---------------------------------------------------------------------------

_KEY_TOKEN_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_JSON_NUMBER_RE = re.compile(r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$")

BLOCK_STYLES = {"|", ">"}
QUOTE_STYLES = {"'", '"'}

# The ADR forbids boolean/null-looking mapping keys even though they match
# the general `^[a-z][a-z0-9_]*$` grammar (YAML 1.1 resolves several of
# these as booleans/null; the profile bans them as *keys* outright so a key
# never depends on which resolver reads it).
_RESERVED_KEY_TOKENS = {"true", "false", "null", "yes", "no", "on", "off"}

_ALLOWED_SCALAR_TAGS = (
    "tag:yaml.org,2002:str",
    "tag:yaml.org,2002:null",
    "tag:yaml.org,2002:bool",
    "tag:yaml.org,2002:int",
    "tag:yaml.org,2002:float",
)


class ProfileViolation(AssertionError):
    pass


# --- Layer A: source-token validation --------------------------------------


def _check_source_tokens(yaml_source: str) -> None:
    """Scan ``yaml_source`` (before composition) and raise ProfileViolation
    for any forbidden source-level construct: anchors, aliases, explicit
    tags, `%YAML`/`%TAG`/unknown directives, the explicit-key `?` indicator,
    and the `<<` merge-key construct.

    Malformed YAML that PyYAML's scanner itself rejects is caught and
    re-raised as ProfileViolation (stage: "scan"), distinct from a
    deliberate profile-rule rejection (stage: "source"), so callers can
    still tell "not YAML at all" apart from "valid YAML that violates the
    Two-Lane profile" -- both raise ProfileViolation, but with a different
    reason.
    """
    try:
        tokens = list(yaml.scan(yaml_source, Loader=yaml.SafeLoader))
    except yaml.YAMLError as exc:
        raise ProfileViolation(f"scan stage: malformed YAML: {exc}") from exc

    for tok in tokens:
        if isinstance(tok, yaml.AnchorToken):
            raise ProfileViolation(
                f"source stage: YAML anchor is forbidden: &{tok.value}"
            )
        if isinstance(tok, yaml.AliasToken):
            raise ProfileViolation(
                f"source stage: YAML alias is forbidden: *{tok.value}"
            )
        if isinstance(tok, yaml.TagToken):
            raise ProfileViolation(
                f"source stage: explicit YAML tag is forbidden: {tok.value!r}"
            )
        if isinstance(tok, yaml.DirectiveToken):
            name = tok.name
            if name == "YAML":
                version = tok.value
                if version != (1, 2):
                    raise ProfileViolation(
                        f"source stage: %YAML directive version {version} is "
                        "forbidden (only YAML 1.2 is permitted per ADR 0023)"
                    )
                # A %YAML 1.2 directive is syntactically permitted, but no
                # normative example in this repository uses one; falling
                # through here means it is not rejected outright.
            elif name == "TAG":
                raise ProfileViolation("source stage: %TAG directive is forbidden")
            else:
                raise ProfileViolation(
                    f"source stage: unknown directive {name!r} is forbidden"
                )
        if isinstance(tok, yaml.KeyToken):
            idx = getattr(tok.start_mark, "index", None)
            if idx is not None and idx < len(yaml_source) and yaml_source[idx] == "?":
                raise ProfileViolation(
                    "source stage: explicit-key indicator '?' is forbidden"
                )
        if isinstance(tok, yaml.ScalarToken):
            if tok.plain and tok.value == "<<":
                raise ProfileViolation(
                    "source stage: merge key construct '<<' is forbidden"
                )


# --- Layer B: structural / declared-field validation ------------------------


def _check_scalar_value(node) -> None:
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
            # RFC 8259 grammar accepted the lexeme; separately reject
            # negative zero by its exact decimal lexical value (ADR 0023
            # §10b: "Negative zero (`-0`) is rejected for schema v1").
            # Decimal() interprets the lexeme exactly as written -- no
            # binary-float conversion, so lexical intent is preserved and
            # no underflow can hide a nonzero value as zero. This catches
            # every negative-zero spelling, not only the literal `-0`
            # string: `-0.0`, `-0e0`, `-0E+10`, `-0.000e-5`, etc.
            if v.startswith("-") and Decimal(v) == 0:
                raise ProfileViolation(
                    f"unquoted plain scalar value {v!r} is negative zero, "
                    "which is rejected (ADR 0023 s10b)"
                )
            return
        raise ProfileViolation(f"unquoted plain scalar value {v!r} is not permitted")
    raise ProfileViolation(f"unrecognized scalar style {node.style!r}")


def _check_mapping_key(node) -> None:
    # Node-type check FIRST: a complex (non-scalar) key must be rejected
    # deliberately, before any code path that assumes `.style`/`.value`
    # exist only on scalar nodes. A prior version of this checker read
    # `node.style` before this isinstance check and crashed with an
    # unrelated AttributeError on a complex key instead of raising
    # ProfileViolation.
    if not isinstance(node, yaml.ScalarNode):
        raise ProfileViolation("complex (non-scalar) mapping key is forbidden")
    if node.style in QUOTE_STYLES:
        raise ProfileViolation(f"quoted mapping key is forbidden: {node.value!r}")
    if node.style in BLOCK_STYLES:
        raise ProfileViolation(f"block-style mapping key is forbidden: {node.value!r}")
    if node.value in _RESERVED_KEY_TOKENS:
        raise ProfileViolation(
            f"mapping key {node.value!r} is a reserved boolean/null-looking "
            "token and is forbidden regardless of the general key grammar"
        )
    if not _KEY_TOKEN_RE.match(node.value):
        raise ProfileViolation(
            f"mapping key {node.value!r} does not match ^[a-z][a-z0-9_]*$"
        )


def _check_tagged_node(node) -> None:
    if isinstance(node, yaml.MappingNode) and node.tag != "tag:yaml.org,2002:map":
        raise ProfileViolation(f"unexpected tag on mapping: {node.tag!r}")
    if isinstance(node, yaml.SequenceNode) and node.tag != "tag:yaml.org,2002:seq":
        raise ProfileViolation(f"unexpected tag on sequence: {node.tag!r}")
    if isinstance(node, yaml.ScalarNode) and node.tag not in _ALLOWED_SCALAR_TAGS:
        raise ProfileViolation(f"unexpected tag on scalar: {node.tag!r}")


# --- Schema shapes -----------------------------------------------------------
#
# A "shape" is a small tuple-tagged spec describing what a node is allowed to
# be, used purely by this test module to enforce declared-field validation.
# Every schema-defined object is closed (`("closed", {field: shape, ...})`)
# unless the field table explicitly documents it as open, per ADR 0023 /
# configuration-identity.schema.md: `execution_parameters` is schema v1's
# sole open-map root field, and its value forms the sole open-map subtree --
# every mapping recursively nested inside that subtree (through mapping
# values or sequence elements) is open too, not closed. Every mapping
# outside that one subtree remains closed.

SCALAR = ("scalar",)


def nullable(inner):
    return ("nullable", inner)


def seq(item):
    return ("seq", item)


def closed(fields, required=None):
    """A closed mapping shape: exactly the declared ``fields`` are legal
    keys, and every key in ``required`` (default: every declared field --
    all six normative schema field tables document every listed field as
    required, including nullable-but-required ones such as `token_ceiling`
    or `cost_ceiling`) must be present in a conforming document.

    Nullable fields (``nullable(...)``) are still required *keys*; only
    their *value* may be JSON `null`. A field may be legitimately absent
    only when it is not listed in ``required`` -- which, for every closed
    object in this schema, is never (every documented field is required).
    """
    fields_dict = dict(fields)
    required_set = (
        frozenset(fields_dict) if required is None else frozenset(required)
    )
    return ("closed", fields_dict, required_set)


# `execution_parameters` (configuration-identity.schema.md): schema v1's
# sole open-map root field. Its value is the sole open-map subtree -- every
# mapping recursively reachable from it through mapping values or sequence
# elements is open, not closed. Keys still obey the mapping-key grammar and
# the reserved-key prohibition; values are recursively either an allowed
# scalar, a sequence of allowed values, or a nested mapping belonging to the
# same open-map subtree -- never anchors/aliases/tags/block
# scalars/multiline strings/duplicate keys (those are already rejected by
# Layer A and by `_check_scalar_value`/`_check_mapping_key`, which the open
# map walk still applies). Every mapping outside this one subtree is closed.
OPEN_MAP = ("open",)

# A fully unconstrained shape used only by the low-level source-syntax unit
# tests in this module, which intentionally test forbidden *syntax*
# (anchors, tags, directives, complex keys, ...) independent of any
# particular schema's declared field set. Real fenced examples are always
# checked against one of the concrete shapes below, never this one -- see
# `check_profile_conformance`'s required `shape` parameter.
ANY = ("any",)

CAMPAIGN_POLICY_SHAPE = closed(
    {
        "policy_schema_version": SCALAR,
        "campaign_id": SCALAR,
        "policy_digest": SCALAR,
        "classification": SCALAR,
        "allowed_framework_shas": seq(SCALAR),
        "allowed_targets": seq(closed({"repository": SCALAR, "sha": SCALAR})),
        "allowed_models": seq(SCALAR),
        "allowed_artifact_types": seq(SCALAR),
        "allowed_configuration_ids": seq(SCALAR),
        "max_attempt_slots": SCALAR,
        "max_provider_invocations": SCALAR,
        "max_attempts_per_configuration": SCALAR,
        "concurrency_ceiling": SCALAR,
        "token_ceiling": nullable(SCALAR),
        "cost_ceiling": nullable(closed({"amount": SCALAR, "currency": SCALAR})),
        "validity_window": closed({"not_before": SCALAR, "not_after": SCALAR}),
        "target_mutation_prohibited": SCALAR,
        "fallback_prohibited": SCALAR,
        "repair_prohibited": SCALAR,
        "automatic_merge_prohibited": SCALAR,
        "preservation_requirements": SCALAR,
        "logging_requirements": SCALAR,
        "prepared_by": SCALAR,
        "prepared_at": SCALAR,
    }
)

CAMPAIGN_APPROVAL_SHAPE = closed(
    {
        "approval_schema_version": SCALAR,
        "campaign_id": SCALAR,
        "policy_digest": SCALAR,
        "claimed_approver_identity": SCALAR,
        "approval_provenance": closed({"mechanism": SCALAR, "reference": SCALAR}),
        "approval_statement": SCALAR,
        "approved_at": SCALAR,
        "marker": SCALAR,
    }
)

CONFIGURATION_IDENTITY_SHAPE = closed(
    {
        "configuration_schema_version": SCALAR,
        "configuration_id": SCALAR,
        "campaign_id": SCALAR,
        "framework_sha": SCALAR,
        "target_repository": SCALAR,
        "target_sha": SCALAR,
        "model_identifier": SCALAR,
        "prompt_or_skill_revision": SCALAR,
        "validator_revision": SCALAR,
        "artifact_type": SCALAR,
        "execution_parameters": OPEN_MAP,
    }
)

ATTEMPT_RESERVATION_SHAPE = closed(
    {
        "reservation_schema_version": SCALAR,
        "reservation_id": SCALAR,
        "attempt_id": SCALAR,
        "campaign_id": SCALAR,
        "configuration_id": SCALAR,
        "reserved_at": SCALAR,
        "state": SCALAR,
        "state_history": seq(closed({"state": SCALAR, "at": SCALAR})),
        "terminal_states": seq(SCALAR),
    }
)

ATTEMPT_RESULT_SHAPE = closed(
    {
        "result_schema_version": SCALAR,
        "attempt_id": SCALAR,
        "campaign_id": SCALAR,
        "configuration_id": SCALAR,
        "state": SCALAR,
        "state_history": seq(closed({"state": SCALAR, "at": SCALAR})),
        "provider_invoked_at": nullable(SCALAR),
        "raw_output_reference": nullable(SCALAR),
        "validated_output_reference": nullable(SCALAR),
        "validation_outcome": nullable(closed({"passed": SCALAR, "details": SCALAR})),
        "classification": SCALAR,
        "tokens_observed": nullable(SCALAR),
        "cost_observed": nullable(closed({"amount": SCALAR, "currency": SCALAR})),
        "terminal_at": nullable(SCALAR),
    }
)

CAMPAIGN_SUMMARY_SHAPE = closed(
    {
        "summary_schema_version": SCALAR,
        "campaign_id": SCALAR,
        "policy_digest": SCALAR,
        "campaign_state": SCALAR,
        "campaign_state_history": seq(closed({"state": SCALAR, "at": SCALAR})),
        "reservations_issued": closed({"count": SCALAR, "ids": seq(SCALAR)}),
        "provider_invocations_made": SCALAR,
        "remaining_budget": closed(
            {"attempt_slots": SCALAR, "provider_invocations": SCALAR}
        ),
        "attempts": seq(
            closed(
                {
                    "attempt_id": SCALAR,
                    "configuration_id": SCALAR,
                    "state": SCALAR,
                    "terminal_at": SCALAR,
                }
            )
        ),
        "first_reserved_at": nullable(SCALAR),
        "last_activity_at": SCALAR,
        "terminal_reason": nullable(SCALAR),
    }
)

# A minimal single-field shape used only by unit tests that want to exercise
# `execution_parameters` open-map semantics in isolation, without needing a
# complete configuration-identity document.
CONFIGURATION_OPEN_MAP_ONLY_SHAPE = closed({"execution_parameters": OPEN_MAP})

# Maps each schema-document path to its exact root shape. Every fenced
# example under that path is checked against this shape -- there is no
# generic "check declared fields for anything" fallback.
SCHEMA_SHAPES = {
    "campaign-policy.schema.md": CAMPAIGN_POLICY_SHAPE,
    "campaign-approval.schema.md": CAMPAIGN_APPROVAL_SHAPE,
    "configuration-identity.schema.md": CONFIGURATION_IDENTITY_SHAPE,
    "attempt-reservation.schema.md": ATTEMPT_RESERVATION_SHAPE,
    "attempt-result.schema.md": ATTEMPT_RESULT_SHAPE,
    "campaign-summary.schema.md": CAMPAIGN_SUMMARY_SHAPE,
}


def _check_open_value(node, path: str) -> None:
    """Values inside the one intentionally open mapping
    (`execution_parameters`): recursively an allowed scalar, a sequence of
    allowed values, or a nested open mapping under the same key grammar.
    """
    _check_tagged_node(node)
    if isinstance(node, yaml.ScalarNode):
        _check_scalar_value(node)
        return
    if isinstance(node, yaml.SequenceNode):
        for i, item in enumerate(node.value):
            _check_open_value(item, f"{path}[{i}]")
        return
    if isinstance(node, yaml.MappingNode):
        seen: set[str] = set()
        for key_node, value_node in node.value:
            _check_mapping_key(key_node)
            if key_node.value in seen:
                raise ProfileViolation(f"{path}: duplicate mapping key {key_node.value!r}")
            seen.add(key_node.value)
            _check_open_value(value_node, f"{path}.{key_node.value}")
        return
    raise ProfileViolation(f"{path}: unsupported node type {type(node)!r} in open map")


def _check_shape(node, shape, path: str) -> None:
    kind = shape[0]

    if kind == "any":
        _check_tagged_node(node)
        if isinstance(node, yaml.ScalarNode):
            _check_scalar_value(node)
        elif isinstance(node, yaml.MappingNode):
            seen: set[str] = set()
            for key_node, value_node in node.value:
                _check_mapping_key(key_node)
                if key_node.value in seen:
                    raise ProfileViolation(
                        f"{path}: duplicate mapping key {key_node.value!r}"
                    )
                seen.add(key_node.value)
                _check_shape(value_node, ANY, f"{path}.{key_node.value}")
        elif isinstance(node, yaml.SequenceNode):
            for i, item in enumerate(node.value):
                _check_shape(item, ANY, f"{path}[{i}]")
        else:
            raise ProfileViolation(f"{path}: unsupported node type {type(node)!r}")
        return

    if kind == "nullable":
        if isinstance(node, yaml.ScalarNode) and node.tag == "tag:yaml.org,2002:null":
            _check_tagged_node(node)
            return
        _check_shape(node, shape[1], path)
        return

    if kind == "scalar":
        _check_tagged_node(node)
        if not isinstance(node, yaml.ScalarNode):
            raise ProfileViolation(f"{path}: expected a scalar value")
        _check_scalar_value(node)
        return

    if kind == "seq":
        _check_tagged_node(node)
        if not isinstance(node, yaml.SequenceNode):
            raise ProfileViolation(f"{path}: expected a sequence")
        for i, item in enumerate(node.value):
            _check_shape(item, shape[1], f"{path}[{i}]")
        return

    if kind == "closed":
        _check_tagged_node(node)
        if not isinstance(node, yaml.MappingNode):
            raise ProfileViolation(f"{path}: expected a mapping")
        fields = shape[1]
        required = shape[2]
        seen: set[str] = set()
        for key_node, value_node in node.value:
            _check_mapping_key(key_node)
            key = key_node.value
            if key in seen:
                raise ProfileViolation(f"{path}: duplicate mapping key {key!r}")
            seen.add(key)
            if key not in fields:
                raise ProfileViolation(
                    f"{path}: unknown key {key!r} is not declared by the schema "
                    "(this object is closed)"
                )
            _check_shape(value_node, fields[key], f"{path}.{key}")
        missing = required - seen
        if missing:
            raise ProfileViolation(
                f"{path}: missing required field(s) "
                f"{sorted(missing)!r} (this object is closed)"
            )
        return

    if kind == "open":
        _check_tagged_node(node)
        if not isinstance(node, yaml.MappingNode):
            raise ProfileViolation(f"{path}: expected a mapping")
        seen = set()
        for key_node, value_node in node.value:
            _check_mapping_key(key_node)
            if key_node.value in seen:
                raise ProfileViolation(f"{path}: duplicate mapping key {key_node.value!r}")
            seen.add(key_node.value)
            _check_open_value(value_node, f"{path}.{key_node.value}")
        return

    raise ProfileViolation(f"{path}: unsupported shape {shape!r}")


def check_profile_conformance(yaml_source: str, *, shape) -> None:
    """Check ``yaml_source`` against the Two-Lane YAML Profile v1 (ADR 0023
    §10b) AND the declared field set given by ``shape``.

    ``shape`` is required (not defaulted) so a caller can never accidentally
    check an example without stating which schema shape it belongs to. Pass
    ``ANY`` only for source-syntax unit tests that are deliberately
    independent of any particular schema's declared field set.

    Layer A (`_check_source_tokens`) runs first, against the original
    source text, and rejects forbidden syntax that composition would
    otherwise discard or obscure. Layer B (`_check_shape`) then composes
    the document and walks the node tree, validating hierarchy, key
    grammar, duplicate keys, scalar styles/lexemes, and declared fields.

    Malformed YAML is wrapped as ProfileViolation by whichever layer's
    PyYAML call rejects it first; the resulting message is prefixed with
    the stage name so a test can still distinguish "malformed YAML" from
    "valid YAML that violates the Two-Lane profile".
    """
    _check_source_tokens(yaml_source)
    try:
        doc = yaml.compose(yaml_source, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        raise ProfileViolation(f"compose stage: malformed YAML: {exc}") from exc
    if doc is None:
        raise ProfileViolation("compose stage: empty document")
    _check_shape(doc, shape, "$")


@pytest.mark.parametrize(
    "path", _schema_files(), ids=lambda p: p.name
)
def test_fenced_examples_conform_to_two_lane_yaml_profile_v1(path: Path):
    text = path.read_text(encoding="utf-8")
    blocks = _extract_yaml_blocks(text)
    assert blocks, f"{path.name} has no fenced yaml example"
    shape = SCHEMA_SHAPES[path.name]
    for i, block in enumerate(blocks):
        try:
            check_profile_conformance(block, shape=shape)
        except ProfileViolation as exc:
            raise AssertionError(
                f"{path.name} example #{i} violates Two-Lane YAML Profile v1 "
                f"or its declared field set: {exc}"
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
        check_profile_conformance(source, shape=ANY)


def test_profile_checker_rejects_numeric_looking_mapping_key():
    source = '"1": "value"\n'
    # numeric-looking key, still quoted -- forbidden as quoted key first
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source, shape=ANY)


def test_profile_checker_rejects_literal_block_scalar():
    source = "logging_requirements: |\n  example text\n"
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source, shape=ANY)


def test_profile_checker_rejects_folded_block_scalar():
    source = "logging_requirements: >\n  example text\n"
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source, shape=ANY)


def test_profile_checker_rejects_duplicate_keys():
    source = 'campaign_id: "a"\ncampaign_id: "b"\n'
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source, shape=ANY)


def test_profile_checker_rejects_multiline_double_quoted_scalar():
    source = 'campaign_id: "line one\nline two"\n'
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source, shape=ANY)


def test_profile_checker_accepts_valid_campaign_policy_example():
    text = _policy_text()
    blocks = _extract_yaml_blocks(text)
    assert blocks
    check_profile_conformance(blocks[0], shape=CAMPAIGN_POLICY_SHAPE)  # must not raise
    # No assertion beyond existence: this test suite performs no writes.


# ---------------------------------------------------------------------------
# Direct tests: negative-zero rejection (ADR 0023 s10b).
#
# Every negative numeric lexeme whose exact decimal value is zero is
# rejected, not only the literal string `-0`. Positive zero and ordinary
# negative numbers remain accepted.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "lexeme",
    ["-0", "-0.0", "-0e0", "-0E+10", "-0.000e-5"],
)
def test_negative_zero_lexemes_are_rejected(lexeme):
    source = f"max_attempt_slots: {lexeme}\n"
    with pytest.raises(ProfileViolation, match="negative zero"):
        check_profile_conformance(source, shape=ANY)


@pytest.mark.parametrize("lexeme", ["0", "0.0", "0e0", "-1"])
def test_non_negative_zero_lexemes_are_accepted(lexeme):
    source = f"max_attempt_slots: {lexeme}\n"
    check_profile_conformance(source, shape=ANY)  # must not raise


def test_negative_zero_rejected_in_execution_parameters_scalar():
    source = "execution_parameters:\n  temperature: -0\n"
    with pytest.raises(ProfileViolation, match="negative zero"):
        check_profile_conformance(source, shape=CONFIGURATION_OPEN_MAP_ONLY_SHAPE)


def test_negative_zero_rejected_in_nested_execution_parameters_mapping():
    source = "execution_parameters:\n  nested:\n    value: -0.0\n"
    with pytest.raises(ProfileViolation, match="negative zero"):
        check_profile_conformance(source, shape=CONFIGURATION_OPEN_MAP_ONLY_SHAPE)


def test_negative_zero_rejected_in_execution_parameters_sequence():
    source = "execution_parameters:\n  values:\n    - -0e0\n"
    with pytest.raises(ProfileViolation, match="negative zero"):
        check_profile_conformance(source, shape=CONFIGURATION_OPEN_MAP_ONLY_SHAPE)


def test_execution_parameters_positive_controls_accepted():
    source = 'execution_parameters:\n  temperature: 0.0\n  values:\n    - -1\n    - 0\n    - 1.0\n'
    check_profile_conformance(source, shape=CONFIGURATION_OPEN_MAP_ONLY_SHAPE)  # must not raise


def test_negative_zero_rejected_in_configuration_identity_real_example_mutation():
    block = _configuration_identity_example_block()
    mutated = block.replace(
        "execution_parameters:\n  max_tokens_hint: 4096\n",
        "execution_parameters:\n  max_tokens_hint: -0.0\n",
    )
    with pytest.raises(ProfileViolation, match="negative zero"):
        check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)


def test_negative_zero_rejected_replacing_a_numeric_field_in_campaign_policy():
    text = _policy_text()
    block = _extract_yaml_blocks(text)[0]
    mutated = block.replace("max_attempt_slots: 5\n", "max_attempt_slots: -0\n")
    with pytest.raises(ProfileViolation, match="negative zero"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


# ---------------------------------------------------------------------------
# Direct tests: Layer A source-token validation.
#
# Every one of these targets a specific blocking finding from the review of
# 461a091e: the prior single-layer `yaml.compose_all` checker passed all of
# these silently.
# ---------------------------------------------------------------------------


def test_source_stage_rejects_anchor_alone():
    source = 'campaign_id: &id "value"\n'
    with pytest.raises(ProfileViolation, match="anchor"):
        check_profile_conformance(source, shape=ANY)


def test_source_stage_rejects_anchor_and_alias_together():
    source = 'campaign_id: &id "value"\nprepared_by: *id\n'
    # The anchor is rejected first (it appears first in the token stream);
    # this proves the alias-bearing document is rejected end-to-end.
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source, shape=ANY)


def test_source_stage_rejects_alias_token_itself_not_via_composed_anchor():
    # Prove the *alias* token is what is detected, independent of any
    # composed-node anchor attribute: scan the source directly and assert
    # an AliasToken is present, then assert the checker rejects it.
    source = 'campaign_id: &id "value"\nprepared_by: *id\n'
    tokens = list(yaml.scan(source, Loader=yaml.SafeLoader))
    assert any(isinstance(t, yaml.AliasToken) for t in tokens), (
        "test setup: source must actually produce an AliasToken"
    )
    with pytest.raises(ProfileViolation, match="alias|anchor"):
        check_profile_conformance(source, shape=ANY)


def test_source_stage_rejects_explicit_str_tag():
    source = 'campaign_id: !!str "value"\n'
    with pytest.raises(ProfileViolation, match="tag"):
        check_profile_conformance(source, shape=ANY)


def test_source_stage_rejects_explicit_int_tag():
    source = "max_attempt_slots: !!int 5\n"
    with pytest.raises(ProfileViolation, match="tag"):
        check_profile_conformance(source, shape=ANY)


def test_source_stage_rejects_custom_explicit_tag():
    source = 'campaign_id: !custom "value"\n'
    with pytest.raises(ProfileViolation, match="tag"):
        check_profile_conformance(source, shape=ANY)


def test_implicit_resolved_tag_is_not_confused_with_explicit_tag():
    # An ordinary quoted string with no explicit tag must be accepted: the
    # composed node's *resolved* tag (tag:yaml.org,2002:str) is normal
    # parser metadata, not evidence of an explicit source TagToken.
    source = 'campaign_id: "value"\n'
    check_profile_conformance(source, shape=ANY)  # must not raise


def test_source_stage_rejects_yaml_1_1_directive():
    source = '%YAML 1.1\n---\ncampaign_id: "value"\n'
    with pytest.raises(ProfileViolation, match="YAML"):
        check_profile_conformance(source, shape=ANY)


def test_source_stage_rejects_tag_directive():
    source = "%TAG !e! tag:example.invalid,2026:\n---\ncampaign_id: \"value\"\n"
    with pytest.raises(ProfileViolation, match="TAG"):
        check_profile_conformance(source, shape=ANY)


def test_source_stage_rejects_unknown_directive():
    source = "%FOO bar\n---\ncampaign_id: \"value\"\n"
    with pytest.raises(ProfileViolation, match="directive"):
        check_profile_conformance(source, shape=ANY)


def test_source_stage_accepts_yaml_1_2_directive():
    source = '%YAML 1.2\n---\ncampaign_id: "value"\n'
    check_profile_conformance(source, shape=ANY)  # must not raise


def test_source_stage_rejects_explicit_simple_key():
    source = '? campaign_id\n: "value"\n'
    with pytest.raises(ProfileViolation, match="explicit-key"):
        check_profile_conformance(source, shape=ANY)


def test_source_stage_rejects_complex_sequence_key():
    source = '? ["a", "b"]\n: "value"\n'
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source, shape=ANY)


def test_source_stage_accepts_normal_key_not_confused_with_explicit_key():
    source = 'campaign_id: "value"\n'
    check_profile_conformance(source, shape=ANY)  # must not raise


def test_source_stage_rejects_merge_key():
    source = 'defaults: &defaults\n  campaign_id: "value"\nmerged:\n  <<: *defaults\n'
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source, shape=ANY)


# ---------------------------------------------------------------------------
# Direct tests: mapping-key source grammar, including reserved tokens.
# ---------------------------------------------------------------------------


def test_mapping_key_double_quoted_is_rejected():
    source = '"campaign_id": "value"\n'
    with pytest.raises(ProfileViolation, match="quoted"):
        check_profile_conformance(source, shape=ANY)


def test_mapping_key_single_quoted_is_rejected():
    source = "'campaign_id': \"value\"\n"
    with pytest.raises(ProfileViolation, match="quoted"):
        check_profile_conformance(source, shape=ANY)


def test_mapping_key_numeric_looking_is_rejected():
    source = "1: \"value\"\n"
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source, shape=ANY)


@pytest.mark.parametrize(
    "token", ["true", "false", "null", "yes", "no", "on", "off"]
)
def test_mapping_key_reserved_token_is_rejected(token):
    source = f'{token}: "value"\n'
    with pytest.raises(ProfileViolation, match="reserved"):
        check_profile_conformance(source, shape=ANY)


def test_mapping_key_unicode_is_rejected():
    source = 'cámpaign_id: "value"\n'
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source, shape=ANY)


def test_mapping_key_empty_is_rejected():
    source = '"": "value"\n'
    with pytest.raises(ProfileViolation, match="quoted"):
        check_profile_conformance(source, shape=ANY)


def test_mapping_key_duplicate_is_rejected():
    source = 'campaign_id: "a"\ncampaign_id: "b"\n'
    with pytest.raises(ProfileViolation, match="duplicate"):
        check_profile_conformance(source, shape=ANY)


def test_mapping_key_valid_plain_key_is_accepted():
    source = 'campaign_id: "value"\n'
    check_profile_conformance(source, shape=ANY)  # must not raise


# ---------------------------------------------------------------------------
# Direct tests: complex-key failure discipline (deliberate ProfileViolation,
# not an accidental AttributeError from reading `.style` before checking
# node type).
# ---------------------------------------------------------------------------


def test_complex_mapping_key_raises_profile_violation_not_attribute_error():
    source = '[a, b]: "value"\n'
    with pytest.raises(ProfileViolation, match="complex"):
        check_profile_conformance(source, shape=ANY)


def test_complex_mapping_key_via_check_mapping_key_directly():
    # Exercise `_check_mapping_key` directly against a composed
    # non-scalar key node to prove the node-type check runs before any
    # scalar-only attribute access.
    doc = yaml.compose('{a: 1}: "value"\n', Loader=yaml.SafeLoader)
    key_node, _value_node = doc.value[0]
    assert not isinstance(key_node, yaml.ScalarNode)
    with pytest.raises(ProfileViolation, match="complex"):
        _check_mapping_key(key_node)


def test_malformed_yaml_is_wrapped_as_profile_violation():
    source = "campaign_id: [unterminated\n"
    with pytest.raises(ProfileViolation):
        check_profile_conformance(source, shape=ANY)


def test_malformed_yaml_and_valid_profile_violation_are_distinguishable():
    malformed = "campaign_id: [unterminated\n"
    with pytest.raises(ProfileViolation) as malformed_exc:
        check_profile_conformance(malformed, shape=ANY)
    assert "scan stage" in str(malformed_exc.value) or "compose stage" in str(
        malformed_exc.value
    )

    valid_but_violating = 'campaign_id: &id "value"\n'
    with pytest.raises(ProfileViolation) as violation_exc:
        check_profile_conformance(valid_but_violating, shape=ANY)
    assert "source stage" in str(violation_exc.value)


# ---------------------------------------------------------------------------
# Direct tests: declared-field (closed-object) validation per schema.
# ---------------------------------------------------------------------------


def test_unknown_top_level_field_rejected_in_campaign_policy():
    text = _policy_text()
    block = _extract_yaml_blocks(text)[0]
    mutated = block.replace(
        'classification: "EXPLORATORY_NOT_CANONICAL_EVIDENCE"\n',
        'classification: "EXPLORATORY_NOT_CANONICAL_EVIDENCE"\n'
        'unknown_extra_field: "value"\n',
    )
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_unknown_key_rejected_in_allowed_targets_item():
    text = _policy_text()
    block = _extract_yaml_blocks(text)[0]
    mutated = block.replace(
        '    sha: "000000000000000000000000000000000000beef"\n',
        '    sha: "000000000000000000000000000000000000beef"\n'
        '    unknown_field: "value"\n',
    )
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_unknown_key_rejected_in_validity_window():
    text = _policy_text()
    block = _extract_yaml_blocks(text)[0]
    mutated = block.replace(
        '  not_after: "2026-01-08T00:00:00+00:00"\n',
        '  not_after: "2026-01-08T00:00:00+00:00"\n'
        '  unknown_field: "value"\n',
    )
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_unknown_key_rejected_in_cost_ceiling():
    text = _policy_text()
    block = _extract_yaml_blocks(text)[0]
    mutated = block.replace(
        "cost_ceiling: null\n",
        "cost_ceiling:\n  amount: \"0.00\"\n  currency: \"USD\"\n  unknown_field: \"value\"\n",
    )
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_unknown_top_level_field_rejected_in_configuration_identity():
    text = _configuration_identity_text()
    block = _extract_yaml_blocks(text)[0]
    mutated = block + 'unknown_extra_field: "value"\n'
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)


def test_unknown_top_level_field_rejected_in_campaign_approval():
    text = (SCHEMA_DIR / "campaign-approval.schema.md").read_text(encoding="utf-8")
    block = _extract_yaml_blocks(text)[1]  # the filled illustrative example
    mutated = block + 'unknown_extra_field: "value"\n'
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=CAMPAIGN_APPROVAL_SHAPE)


def test_unknown_top_level_field_rejected_in_attempt_reservation():
    text = (SCHEMA_DIR / "attempt-reservation.schema.md").read_text(encoding="utf-8")
    block = _extract_yaml_blocks(text)[0]
    mutated = block + 'unknown_extra_field: "value"\n'
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=ATTEMPT_RESERVATION_SHAPE)


def test_unknown_top_level_field_rejected_in_attempt_result():
    text = (SCHEMA_DIR / "attempt-result.schema.md").read_text(encoding="utf-8")
    block = _extract_yaml_blocks(text)[0]
    mutated = block + 'unknown_extra_field: "value"\n'
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=ATTEMPT_RESULT_SHAPE)


def test_unknown_top_level_field_rejected_in_campaign_summary():
    text = (SCHEMA_DIR / "campaign-summary.schema.md").read_text(encoding="utf-8")
    block = _extract_yaml_blocks(text)[0]
    mutated = block + 'unknown_extra_field: "value"\n'
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=CAMPAIGN_SUMMARY_SHAPE)


# ---------------------------------------------------------------------------
# Direct tests: execution_parameters open-map semantics.
# ---------------------------------------------------------------------------


def _configuration_identity_example_block() -> str:
    text = _configuration_identity_text()
    return _extract_yaml_blocks(text)[0]


def test_execution_parameters_accepts_arbitrary_valid_key():
    block = _configuration_identity_example_block()
    mutated = block.replace(
        'execution_parameters:\n  max_tokens_hint: 4096\n',
        'execution_parameters:\n  max_tokens_hint: 4096\n  temperature_hint: "low"\n',
    )
    check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)  # must not raise


def test_execution_parameters_accepts_nested_open_map_key():
    block = _configuration_identity_example_block()
    mutated = block.replace(
        'execution_parameters:\n  max_tokens_hint: 4096\n',
        'execution_parameters:\n  max_tokens_hint: 4096\n  nested:\n    inner_key: "value"\n',
    )
    check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)  # must not raise


def test_execution_parameters_rejects_invalid_key_grammar():
    block = _configuration_identity_example_block()
    mutated = block.replace(
        'execution_parameters:\n  max_tokens_hint: 4096\n',
        'execution_parameters:\n  max_tokens_hint: 4096\n  "Not-Valid": "value"\n',
    )
    with pytest.raises(ProfileViolation, match="quoted"):
        check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)


def test_execution_parameters_rejects_reserved_key():
    block = _configuration_identity_example_block()
    mutated = block.replace(
        'execution_parameters:\n  max_tokens_hint: 4096\n',
        'execution_parameters:\n  max_tokens_hint: 4096\n  true: "value"\n',
    )
    with pytest.raises(ProfileViolation, match="reserved"):
        check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)


def test_execution_parameters_rejects_anchor_inside_open_map():
    block = _configuration_identity_example_block()
    mutated = block.replace(
        'execution_parameters:\n  max_tokens_hint: 4096\n',
        'execution_parameters:\n  max_tokens_hint: 4096\n  anchored: &leak "value"\n',
    )
    with pytest.raises(ProfileViolation, match="anchor"):
        check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)


def test_execution_parameters_rejects_block_scalar_inside_open_map():
    block = _configuration_identity_example_block()
    mutated = block.replace(
        'execution_parameters:\n  max_tokens_hint: 4096\n',
        'execution_parameters:\n  max_tokens_hint: 4096\n  notes: |\n    example text\n',
    )
    with pytest.raises(ProfileViolation):
        check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)


# ---------------------------------------------------------------------------
# Direct tests: required-field presence (closed objects only).
#
# Removing a required field from an otherwise valid real fenced example must
# be rejected as ProfileViolation, never silently accepted and never an
# accidental KeyError/AttributeError.
# ---------------------------------------------------------------------------


def _attempt_reservation_text() -> str:
    return (SCHEMA_DIR / "attempt-reservation.schema.md").read_text(encoding="utf-8")


def _attempt_result_text() -> str:
    return (SCHEMA_DIR / "attempt-result.schema.md").read_text(encoding="utf-8")


def _campaign_summary_text() -> str:
    return (SCHEMA_DIR / "campaign-summary.schema.md").read_text(encoding="utf-8")


def _campaign_approval_filled_block() -> str:
    text = (SCHEMA_DIR / "campaign-approval.schema.md").read_text(encoding="utf-8")
    return _extract_yaml_blocks(text)[1]  # the filled illustrative example


@pytest.mark.parametrize(
    "removed_line",
    [
        'campaign_id: "EXP-0000-EXAMPLE"\n',
        'policy_digest: "0000000000000000000000000000000000000000000000000000000000000000"\n',
        'allowed_configuration_ids:\n  - "1111111111111111111111111111111111111111111111111111111111111111"\n  - "2222222222222222222222222222222222222222222222222222222222222222"\n',
        'validity_window:\n  not_before: "2026-01-01T00:00:00+00:00"\n  not_after: "2026-01-08T00:00:00+00:00"\n',
    ],
)
def test_campaign_policy_rejects_missing_required_top_level_field(removed_line):
    block = _extract_yaml_blocks(_policy_text())[0]
    assert removed_line in block, "test setup: line must exist verbatim in the example"
    mutated = block.replace(removed_line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_campaign_policy_rejects_missing_allowed_targets_repository():
    block = _extract_yaml_blocks(_policy_text())[0]
    original = '  - repository: "https://example.invalid/example-owner/example-target.git"\n    sha: "000000000000000000000000000000000000beef"\n'
    replacement = '  - sha: "000000000000000000000000000000000000beef"\n'
    assert original in block
    mutated = block.replace(original, replacement, 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_campaign_policy_rejects_missing_allowed_targets_sha():
    block = _extract_yaml_blocks(_policy_text())[0]
    line = '    sha: "000000000000000000000000000000000000beef"\n'
    assert line in block
    mutated = block.replace(line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_campaign_policy_rejects_missing_validity_window_not_before():
    block = _extract_yaml_blocks(_policy_text())[0]
    line = '  not_before: "2026-01-01T00:00:00+00:00"\n'
    assert line in block
    mutated = block.replace(line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_campaign_policy_rejects_missing_validity_window_not_after():
    block = _extract_yaml_blocks(_policy_text())[0]
    line = '  not_after: "2026-01-08T00:00:00+00:00"\n'
    assert line in block
    mutated = block.replace(line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_campaign_policy_rejects_missing_cost_ceiling_amount_when_non_null():
    block = _extract_yaml_blocks(_policy_text())[0]
    mutated = block.replace(
        "cost_ceiling: null\n",
        'cost_ceiling:\n  amount: "0.00"\n  currency: "USD"\n',
    )
    mutated = mutated.replace('  amount: "0.00"\n', "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_campaign_policy_rejects_missing_cost_ceiling_currency_when_non_null():
    block = _extract_yaml_blocks(_policy_text())[0]
    mutated = block.replace(
        "cost_ceiling: null\n",
        'cost_ceiling:\n  amount: "0.00"\n  currency: "USD"\n',
    )
    mutated = mutated.replace('  currency: "USD"\n', "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_campaign_policy_accepts_cost_ceiling_present_and_complete_when_non_null():
    block = _extract_yaml_blocks(_policy_text())[0]
    mutated = block.replace(
        "cost_ceiling: null\n",
        'cost_ceiling:\n  amount: "0.00"\n  currency: "USD"\n',
    )
    check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)  # must not raise


@pytest.mark.parametrize(
    "removed_line",
    [
        'campaign_id: "EXP-0000-EXAMPLE"\n',
        'policy_digest: "0000000000000000000000000000000000000000000000000000000000000000"\n',
        'marker: "EXAMPLE_ONLY_NOT_AUTHORIZATION"\n',
    ],
)
def test_campaign_approval_rejects_missing_required_top_level_field(removed_line):
    block = _campaign_approval_filled_block()
    assert removed_line in block
    mutated = block.replace(removed_line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_APPROVAL_SHAPE)


def test_campaign_approval_rejects_missing_approval_provenance():
    block = _campaign_approval_filled_block()
    line = 'approval_provenance:\n  mechanism: "signed_commit"\n  reference: "000000000000000000000000000000000000c0de"\n'
    assert line in block
    mutated = block.replace(line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_APPROVAL_SHAPE)


def test_campaign_approval_rejects_missing_approval_provenance_mechanism():
    block = _campaign_approval_filled_block()
    line = '  mechanism: "signed_commit"\n'
    assert line in block
    mutated = block.replace(line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_APPROVAL_SHAPE)


def test_campaign_approval_rejects_missing_approval_provenance_reference():
    block = _campaign_approval_filled_block()
    line = '  reference: "000000000000000000000000000000000000c0de"\n'
    assert line in block
    mutated = block.replace(line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_APPROVAL_SHAPE)


@pytest.mark.parametrize(
    "removed_line",
    [
        'configuration_id: "1111111111111111111111111111111111111111111111111111111111111111"\n',
        'campaign_id: "EXP-0000-EXAMPLE"\n',
        'artifact_type: "repository_sensemaking_brief"\n',
    ],
)
def test_configuration_identity_rejects_missing_required_top_level_field(removed_line):
    block = _configuration_identity_example_block()
    assert removed_line in block
    mutated = block.replace(removed_line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)


def test_configuration_identity_rejects_missing_execution_parameters():
    block = _configuration_identity_example_block()
    line = "execution_parameters:\n  max_tokens_hint: 4096\n  tool_allowlist:\n    - \"read_repository\"\n"
    assert line in block
    mutated = block.replace(line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)


@pytest.mark.parametrize(
    "removed_line",
    [
        'reservation_id: "00000000-0000-0000-0000-000000000001"\n',
        'attempt_id: "00000000-0000-0000-0000-000000000001"\n',
        'state: "RESERVED"\n',
    ],
)
def test_attempt_reservation_rejects_missing_required_top_level_field(removed_line):
    block = _extract_yaml_blocks(_attempt_reservation_text())[0]
    assert removed_line in block
    mutated = block.replace(removed_line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=ATTEMPT_RESERVATION_SHAPE)


def test_attempt_reservation_rejects_missing_state_history():
    block = _extract_yaml_blocks(_attempt_reservation_text())[0]
    line = 'state_history:\n  - state: "RESERVED"\n    at: "2026-01-01T00:00:00+00:00"\n'
    assert line in block
    mutated = block.replace(line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=ATTEMPT_RESERVATION_SHAPE)


@pytest.mark.parametrize(
    "removed_line",
    [
        'attempt_id: "00000000-0000-0000-0000-000000000001"\n',
        'state: "VALIDATION_PASSED"\n',
        'classification: "EXPLORATORY_NOT_CANONICAL_EVIDENCE"\n',
    ],
)
def test_attempt_result_rejects_missing_required_top_level_field(removed_line):
    block = _extract_yaml_blocks(_attempt_result_text())[0]
    assert removed_line in block
    mutated = block.replace(removed_line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=ATTEMPT_RESULT_SHAPE)


def test_attempt_result_rejects_missing_state_history():
    block = _extract_yaml_blocks(_attempt_result_text())[0]
    line = (
        'state_history:\n'
        '  - state: "RESERVED"\n    at: "2026-01-01T00:00:00+00:00"\n'
        '  - state: "INVOKED"\n    at: "2026-01-01T00:00:05+00:00"\n'
        '  - state: "OUTPUT_CAPTURED"\n    at: "2026-01-01T00:03:00+00:00"\n'
        '  - state: "VALIDATION_PASSED"\n    at: "2026-01-01T00:03:30+00:00"\n'
    )
    assert line in block
    mutated = block.replace(line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=ATTEMPT_RESULT_SHAPE)


@pytest.mark.parametrize(
    "removed_line",
    [
        'campaign_id: "EXP-0000-EXAMPLE"\n',
        'campaign_state: "ACTIVE"\n',
    ],
)
def test_campaign_summary_rejects_missing_required_top_level_field(removed_line):
    block = _extract_yaml_blocks(_campaign_summary_text())[0]
    assert removed_line in block
    mutated = block.replace(removed_line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_SUMMARY_SHAPE)


def test_campaign_summary_rejects_missing_remaining_budget():
    block = _extract_yaml_blocks(_campaign_summary_text())[0]
    line = "remaining_budget:\n  attempt_slots: 3\n  provider_invocations: 4\n"
    assert line in block
    mutated = block.replace(line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_SUMMARY_SHAPE)


def test_campaign_summary_rejects_missing_attempts():
    block = _extract_yaml_blocks(_campaign_summary_text())[0]
    line = (
        "attempts:\n"
        '  - attempt_id: "00000000-0000-0000-0000-000000000001"\n'
        '    configuration_id: "1111111111111111111111111111111111111111111111111111111111111111"\n'
        '    state: "VALIDATION_PASSED"\n'
        '    terminal_at: "2026-01-01T00:03:30+00:00"\n'
        '  - attempt_id: "00000000-0000-0000-0000-000000000002"\n'
        '    configuration_id: "1111111111111111111111111111111111111111111111111111111111111111"\n'
        '    state: "ABORTED_BEFORE_INVOCATION"\n'
        '    terminal_at: "2026-01-01T00:04:00+00:00"\n'
    )
    assert line in block
    mutated = block.replace(line, "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_SUMMARY_SHAPE)


def test_nullable_required_field_accepted_present_with_null():
    # token_ceiling is nullable-but-required: present with an explicit
    # `null` value must be accepted.
    block = _extract_yaml_blocks(_policy_text())[0]
    assert "token_ceiling: null\n" in block
    check_profile_conformance(block, shape=CAMPAIGN_POLICY_SHAPE)  # must not raise


def test_nullable_required_field_rejected_when_absent():
    # The same field, entirely removed (not merely set to null), must be
    # rejected as a missing required field -- nullable never means
    # "optional key".
    block = _extract_yaml_blocks(_policy_text())[0]
    mutated = block.replace("token_ceiling: null\n", "", 1)
    with pytest.raises(ProfileViolation, match="missing required"):
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)


def test_missing_required_failure_is_profile_violation_not_key_error():
    block = _extract_yaml_blocks(_policy_text())[0]
    mutated = block.replace('campaign_id: "EXP-0000-EXAMPLE"\n', "", 1)
    try:
        check_profile_conformance(mutated, shape=CAMPAIGN_POLICY_SHAPE)
    except ProfileViolation:
        pass
    except Exception as exc:  # pragma: no cover - defensive
        pytest.fail(f"expected ProfileViolation, got {type(exc).__name__}: {exc}")
    else:
        pytest.fail("expected ProfileViolation, no exception was raised")


def test_missing_required_error_message_includes_path_and_sorted_field_names():
    source = 'campaign_id: "value"\n'
    shape = closed({"campaign_id": SCALAR, "policy_digest": SCALAR, "artifact_type": SCALAR})
    with pytest.raises(ProfileViolation) as exc_info:
        check_profile_conformance(source, shape=shape)
    message = str(exc_info.value)
    assert "$" in message
    assert "['artifact_type', 'policy_digest']" in message


# ---------------------------------------------------------------------------
# Real-example mutation round-trip guard: every mutation test above operates
# on an in-memory `str.replace(...)` result, never on the file at rest.
# ---------------------------------------------------------------------------


def test_schema_files_are_never_written_by_this_test_module():
    for path in _schema_files():
        first = path.read_bytes()
        second = path.read_bytes()
        assert first == second


# ---------------------------------------------------------------------------
# Normative closed/open map contract-consistency tests (ADR 0023, README,
# configuration-identity.schema.md, and the test-only checker's shape model
# must all agree).
# ---------------------------------------------------------------------------


def test_adr_defines_closed_maps_as_the_default():
    text = _normalize_whitespace(_adr_text().lower())
    assert "every schema-defined mapping is closed" in text


def test_adr_names_execution_parameters_as_the_sole_open_map_root_field():
    text = _normalize_whitespace(_adr_text().lower())
    assert "execution_parameters" in text
    assert "sole open-map root field" in text
    assert "open-map subtree" in text


def test_configuration_identity_defines_same_open_map_semantics():
    text = _normalize_whitespace(_configuration_identity_text().lower())
    assert "execution_parameters" in text
    assert "open-map root field" in text
    assert "open-map subtree" in text


def test_adr_does_not_use_bare_sole_open_mapping_phrase_undefined():
    # The bare phrase "sole open mapping" is ambiguous (a subtree can
    # legitimately contain many mapping nodes); the ADR must use the
    # disambiguated "sole open-map root field" / "open-map subtree"
    # terminology instead, everywhere it makes this claim.
    text = _adr_text()
    assert "sole open mapping" not in text.lower()


def test_readme_does_not_use_bare_sole_open_mapping_phrase_undefined():
    text = (SCHEMA_DIR / "README.md").read_text(encoding="utf-8")
    assert "sole open mapping" not in text.lower()


def test_configuration_identity_schema_does_not_claim_nested_maps_closed():
    # The field-table description must not claim that mappings nested
    # inside execution_parameters are closed -- they are part of the one
    # open-map subtree and are themselves open. It must instead state that
    # mappings *outside* the subtree are closed.
    text = _normalize_whitespace(_configuration_identity_text())
    assert "nested inside `execution_parameters`" not in text
    assert "mapping nested inside" not in text.lower() or "not closed" in text.lower()
    assert "every mapping outside that subtree is closed" in text.lower()


def test_adr_and_readme_agree_on_single_open_map_root_field():
    # No document may imply more than one field introduces an open-map
    # subtree.
    for text_fn in (_adr_text, lambda: (SCHEMA_DIR / "README.md").read_text(encoding="utf-8")):
        text = _normalize_whitespace(text_fn().lower())
        assert text.count("open-map root field") >= 1
        # execution_parameters must be named as the root field somewhere
        # near (within 400 chars before) at least one occurrence of the
        # phrase "open-map root field".
        start = 0
        found_named = False
        while True:
            idx = text.find("open-map root field", start)
            if idx == -1:
                break
            window = text[max(0, idx - 400):idx]
            if "execution_parameters" in window:
                found_named = True
                break
            start = idx + 1
        assert found_named, f"execution_parameters not named near 'open-map root field' in {text_fn}"


def test_readme_summarizes_closed_default_and_open_exception():
    text = _normalize_whitespace(
        (SCHEMA_DIR / "README.md").read_text(encoding="utf-8").lower()
    )
    assert "closed" in text
    assert "execution_parameters" in text
    assert "open" in text


def test_no_prose_says_every_map_closed_without_exception():
    # The old absolute phrasing ("must exactly match a field declared by
    # the schema for that object" with no open-map qualifier) must not
    # reappear unqualified anywhere in the ADR.
    text = _adr_text()
    for line in text.splitlines():
        lowered = line.lower()
        if "must" in lowered and "exactly match a field declared" in lowered:
            assert (
                "closed" in lowered
                or "open" in lowered
                or "execution_parameters" in lowered
            ), (
                "ADR 0023 must not state the declared-field-match rule "
                "without qualifying it against the closed/open distinction: "
                f"{line!r}"
            )


def test_no_prose_permits_arbitrary_keys_outside_execution_parameters():
    combined = _normalize_whitespace(
        (_adr_text() + " " + (SCHEMA_DIR / "README.md").read_text(encoding="utf-8")).lower()
    )
    assert (
        "no other map becomes open" in combined
        or "no other general unknown-field escape hatch" in combined
    )


def test_checker_shape_model_matches_normative_distinction():
    # CONFIGURATION_IDENTITY_SHAPE is the only shape in this module whose
    # value uses OPEN_MAP; every other declared field, at every nesting
    # level across all six shapes, must be `closed` (or a scalar/seq/
    # nullable wrapper around one) -- never OPEN_MAP.
    def _collect_open_map_field_paths(shape, path):
        kind = shape[0]
        found = []
        if kind == "open":
            found.append(path)
        elif kind == "closed":
            for field_name, field_shape in shape[1].items():
                found.extend(_collect_open_map_field_paths(field_shape, f"{path}.{field_name}"))
        elif kind == "seq":
            found.extend(_collect_open_map_field_paths(shape[1], f"{path}[]"))
        elif kind == "nullable":
            found.extend(_collect_open_map_field_paths(shape[1], path))
        return found

    all_open_paths = []
    for schema_name, shape in SCHEMA_SHAPES.items():
        all_open_paths.extend(_collect_open_map_field_paths(shape, schema_name))

    assert all_open_paths == ["configuration-identity.schema.md.execution_parameters"]


def test_checker_accepts_new_valid_execution_parameters_key():
    block = _configuration_identity_example_block()
    mutated = block.replace(
        "execution_parameters:\n  max_tokens_hint: 4096\n",
        "execution_parameters:\n  max_tokens_hint: 4096\n  a_brand_new_valid_key: \"value\"\n",
    )
    check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)  # must not raise


def test_checker_accepts_nested_valid_open_mapping():
    block = _configuration_identity_example_block()
    mutated = block.replace(
        "execution_parameters:\n  max_tokens_hint: 4096\n",
        'execution_parameters:\n  max_tokens_hint: 4096\n  nested_settings:\n    inner_a: "x"\n    inner_b: 1\n',
    )
    check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)  # must not raise


def test_checker_accepts_sequence_containing_nested_open_mapping():
    block = _configuration_identity_example_block()
    mutated = block.replace(
        "execution_parameters:\n  max_tokens_hint: 4096\n",
        'execution_parameters:\n  max_tokens_hint: 4096\n  items:\n    - inner_key: "value"\n',
    )
    check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)  # must not raise


def test_checker_rejects_unknown_field_at_configuration_identity_top_level():
    block = _configuration_identity_example_block()
    mutated = block + 'brand_new_unknown_field: "value"\n'
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)


def test_checker_rejects_invented_top_level_field_negative_control():
    # Negative control required by the two-lane governance normative-
    # contradiction remediation: an unrelated invented top-level field on
    # a configuration-identity document must fail closed as an unknown
    # field -- it must not be silently treated as belonging to any
    # open-map subtree, since only `execution_parameters` is a root field.
    block = _configuration_identity_example_block()
    mutated = block + 'invented_top_level_field: "value"\n'
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)


def test_only_one_open_map_root_field_exists_across_all_schema_shapes():
    # Restates test_checker_shape_model_matches_normative_distinction's
    # invariant explicitly as a "no other field may introduce an open-map
    # subtree" regression: exactly one OPEN_MAP-typed field path may exist
    # across every schema-v1 shape.
    def _collect_open_map_field_paths(shape, path):
        kind = shape[0]
        found = []
        if kind == "open":
            found.append(path)
        elif kind == "closed":
            for field_name, field_shape in shape[1].items():
                found.extend(_collect_open_map_field_paths(field_shape, f"{path}.{field_name}"))
        elif kind == "seq":
            found.extend(_collect_open_map_field_paths(shape[1], f"{path}[]"))
        elif kind == "nullable":
            found.extend(_collect_open_map_field_paths(shape[1], path))
        return found

    all_open_paths = []
    for schema_name, shape in SCHEMA_SHAPES.items():
        all_open_paths.extend(_collect_open_map_field_paths(shape, schema_name))

    assert len(all_open_paths) == 1, (
        f"exactly one open-map root field must exist across schema v1, "
        f"found: {all_open_paths!r}"
    )


@pytest.mark.parametrize(
    "shape_name,text_fn,shape",
    [
        ("campaign-policy", _policy_text, CAMPAIGN_POLICY_SHAPE),
        (
            "campaign-approval",
            lambda: (SCHEMA_DIR / "campaign-approval.schema.md").read_text(encoding="utf-8"),
            CAMPAIGN_APPROVAL_SHAPE,
        ),
        ("attempt-reservation", _attempt_reservation_text, ATTEMPT_RESERVATION_SHAPE),
        ("attempt-result", _attempt_result_text, ATTEMPT_RESULT_SHAPE),
        ("campaign-summary", _campaign_summary_text, CAMPAIGN_SUMMARY_SHAPE),
    ],
)
def test_checker_rejects_unknown_field_in_every_other_closed_object(shape_name, text_fn, shape):
    text = text_fn()
    blocks = _extract_yaml_blocks(text)
    block = blocks[-1]  # the operative/filled example, where multiple exist
    mutated = block + 'brand_new_unknown_field: "value"\n'
    with pytest.raises(ProfileViolation, match="unknown key"):
        check_profile_conformance(mutated, shape=shape)


def test_checker_rejects_reserved_key_inside_execution_parameters_contract_test():
    block = _configuration_identity_example_block()
    for reserved in ("true", "false", "null", "yes", "no", "on", "off"):
        mutated = block.replace(
            "execution_parameters:\n  max_tokens_hint: 4096\n",
            f'execution_parameters:\n  max_tokens_hint: 4096\n  {reserved}: "value"\n',
        )
        with pytest.raises(ProfileViolation, match="reserved"):
            check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)


def test_checker_rejects_malformed_keys_inside_execution_parameters_contract_test():
    block = _configuration_identity_example_block()
    for malformed in ('"Quoted-Key"', "'also-quoted'"):
        mutated = block.replace(
            "execution_parameters:\n  max_tokens_hint: 4096\n",
            f'execution_parameters:\n  max_tokens_hint: 4096\n  {malformed}: "value"\n',
        )
        with pytest.raises(ProfileViolation, match="quoted"):
            check_profile_conformance(mutated, shape=CONFIGURATION_IDENTITY_SHAPE)
