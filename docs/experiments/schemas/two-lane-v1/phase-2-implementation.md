# Phase 2 implementation notes — campaign policy / approval / configuration validation

Program: Issue #116. This phase: Issue #118 (Phase 2). Governing contract:
ADR 0023 (Two-Lane Experiment Authorization). This document describes the
runtime implementation added in this phase; it is not itself a contract —
ADR 0023 and the six schema-contract Markdown files remain normative.

## Scope

This phase implements **fail-closed validation of data**: campaign policy,
campaign approval, configuration identity, and their conjunctive binding. It
does **not** implement provider invocation, an authorization capability, an
attempt ledger, or campaign execution. A successful validation call returns
an immutable `ValidatedCampaignBundle` — never an invocation capability,
token, provider client, or boolean a later phase could mistake for
authority. Phase 3 (#119) is responsible for building the actual
provider-boundary capability from data this phase validates.

## Production module location

`src/sensemaking_skills/campaign_validation/` — an importable package under
the existing `src/sensemaking_skills/` tree (the repo already ships a
`src/`-layout Python package with a matching `pyproject.toml`
`[tool.setuptools.packages.find]` configuration, so this fits the existing
architecture rather than adding a second, `scripts/`-style ad hoc module
convention).

| File | Responsibility |
|---|---|
| `yaml_profile.py` | Two-Lane YAML Profile v1 parser (`parse_two_lane_yaml`) |
| `jcs.py` | RFC 8785 (JCS) canonicalization -- adapter around the `rfc8785` dependency |
| `digests.py` | `compute_policy_digest`, `compute_configuration_id` |
| `immutable.py` | `freeze()` -- recursive deep-freeze for `ValidatedCampaignBundle`'s nested mappings/sequences |
| `models.py` | Frozen dataclasses: `ValidationContext`, `ValidationResult`, `CampaignPolicy`, `CampaignApproval`, `ConfigurationIdentity`, `ValidatedCampaignBundle` |
| `failure_codes.py` | Frozen `CAMPAIGN_FAILURE_CODES` mapping |
| `schema_validation.py` | JSON Schema (Draft 2020-12) validation against the parsed data model, loaded via `importlib.resources` from `schemas/` |
| `schemas/` | Packaged JSON Schema resources (byte-identical copies of the `docs/` originals) |
| `fs_adapter.py` | Narrow adapter around `sensemaking_skills.path_containment`'s path-containment primitives |
| `validators.py` | `validate_campaign_policy`, `validate_campaign_approval`, `validate_configuration_identity`, `validate_campaign_bundle`, and root-scoped loaders |

Also new, at `src/sensemaking_skills/path_containment.py`: the pure
path-containment primitives (`canonicalize_path`, `resolve_containment`,
etc.), extracted unmodified from `scripts/gate_a_authorization.py` so both
Gate A and this package share one implementation. See "Filesystem /
artifact-root trust boundary" below.

## Parser layers (Two-Lane YAML Profile v1)

Two layers, matching ADR 0023 section 10b exactly, implemented in
`yaml_profile.py`:

* **Layer A** (`_layer_a_validate_tokens`) — inspects the raw `yaml.scan()`
  token stream *before* composition: rejects `AliasToken`, `AnchorToken`,
  `TagToken`, non-`%YAML 1.2` directives (including `%TAG`), block/folded
  scalar styles, and physically multiline quoted scalars. Because this runs
  on tokens rather than a composed tree, it independently catches a bare
  alias with no matching anchor definition, rather than relying on a
  composer error.
* **Layer B** (`_compose` / `_compose_value`) — composes the node graph via
  `yaml.compose_all()` using a `SafeLoader` subclass with every implicit
  resolver removed (so no scalar is silently resolved by PyYAML's
  YAML-1.1-flavored default resolver), then walks the tree applying ADR
  0023's exact lexical scalar-resolution rules (quoted -> string,
  `null`/`true`/`false`/RFC 8259 number grammar -> typed value, anything else
  unquoted -> rejected), the mapping-key grammar
  (`^[a-z][a-z0-9_]*$`, reserved-key rejection, duplicate-key detection
  before construction), and the open-map subtree rule for
  `execution_parameters`.

`yaml.safe_load` is never used as the normative parser anywhere in this
package — every digest-bearing document is parsed exclusively through
`parse_two_lane_yaml`.

## JSON Schema (Draft 2020-12)

Canonical, human-authored source: `docs/experiments/schemas/two-lane-v1/json/`.
Runtime-loaded, packaged copy (byte-identical, diffed by
`test_schema_doc_agreement.py::test_packaged_schemas_are_byte_identical_to_docs_originals`):
`src/sensemaking_skills/campaign_validation/schemas/`, loaded via
`importlib.resources` in `schema_validation.py` -- not via a
`Path(__file__).parents[...] / "docs"` filesystem walk, so the package works
correctly from an installed wheel with no repository checkout available.

Files (identical in both locations):

* `campaign-policy.v1.schema.json`
* `campaign-approval.v1.schema.json` (two-profile `oneOf`: example/template
  vs. operative, discriminated by presence/absence of the `marker` field)
* `configuration-identity.v1.schema.json` (`execution_parameters` is the
  sole open-map subtree, expressed via a recursive
  `executionParameterValue`/`executionParameterMap` `$defs` pair with
  `additionalProperties` and a `propertyNames` key-grammar pattern)

These validate the **parsed, restricted JSON-compatible data model**
produced by `parse_two_lane_yaml` — they do not replace source-token
validation, and cross-field checks the schema language cannot express
cleanly (e.g. `max_provider_invocations <= max_attempt_slots`, the validity
window ordering, `allowed_configuration_ids` sortedness) are enforced in
`validators.py` immediately after schema validation passes.

## JCS (RFC 8785) implementation

**Maintained dependency**: `rfc8785` (Trail of Bits), pinned
`>=0.1.4,<0.2` in `pyproject.toml`. `jcs.py` is a narrow adapter around
`rfc8785.dumps`, plus an independent negative-zero rejection (Python's
`float ==` does not distinguish `+0.0`/`-0.0`, and `rfc8785` collapses
both to `"0"`; negative-zero rejection is schema v1 policy, not an RFC 8785
requirement, so it stays this module's job). An earlier revision of this
module implemented JCS from scratch; it was replaced after review because
`rfc8785` resolves cleanly from the configured package index and removes a
real correctness gap the custom version had: RFC 8785 orders object keys by
their UTF-16 code-unit sequence, not by Unicode code point, and the
custom version used Python's default code-point `sorted()`, which
disagrees with the RFC for key pairs that straddle the Basic Multilingual
Plane boundary. `tests/campaign_validation/test_jcs.py` covers reference
number vectors, presentation-equivalence (`1`/`1.0`/`1e0` canonicalize
identically), negative-zero and non-finite rejection, safe-integer boundary
and overflow, a UTF-16-vs-code-point key-ordering test, lone-surrogate
rejection, and exact-bytes comparisons against the reference library.

## Exact hashed field sets

* **Policy digest** (`POLICY_DIGEST_FIELDS` in `digests.py`): every required
  normative policy field except `policy_digest` itself — restated
  identically from ADR 0023 section 9a / section 10c.
* **Configuration ID** (`CONFIGURATION_ID_FIELDS`): exactly
  `configuration_schema_version`, `framework_sha`, `target_repository`,
  `target_sha`, `model_identifier`, `prompt_or_skill_revision`,
  `validator_revision`, `artifact_type`, `execution_parameters` — excludes
  `configuration_id` itself and `campaign_id`, per ADR 0023 section 10c
  verbatim.

## Numeric / type domain decisions

* **Integer-lexeme policy fields** (`max_attempt_slots`,
  `max_provider_invocations`, `max_attempts_per_configuration`,
  `concurrency_ceiling`, `token_ceiling` when non-null) require the SOURCE
  FORM to be integral: `5` is accepted; `5.0`, `5e0`, `5E+0`, `5.5`, and
  quoted `"5"` are all rejected, even though some are mathematically
  integral. This reuses the int/float type split `parse_two_lane_yaml`
  already produces from the lexeme itself (a lexeme with no `.`/exponent
  parses to a genuine Python `int`; any lexeme with a `.`/exponent parses
  to `float`, regardless of value) -- `validators.py::_require_integer_lexeme`
  checks `type(value) is int` (not `isinstance`, so `bool` is naturally
  excluded too), rather than inventing a separate metadata-tracking type.
* **General JSON numbers elsewhere** (inside `execution_parameters`, or
  `cost_ceiling.amount`) are not integer-lexeme-constrained: `1` and `1.0`
  still canonicalize identically under RFC 8785, per ADR 0023 section 10a/10b
  -- that JCS-level equivalence is a property of the *hashing* stage and is
  unrelated to the integer-lexeme *policy-field* rule above, which is a
  stricter, field-specific schema constraint layered on top.
* **Exact numeric domain** (`yaml_profile.py::_parse_exact_float`): every
  decimal/exponent lexeme is parsed as an exact `Decimal` first, then
  converted to `float`; the conversion is rejected (fails closed) if it
  overflows to infinity, if a nonzero value underflows to zero, or if the
  exact decimal value does not survive a binary64 round-trip
  (`Decimal(raw) != Decimal(repr(float(raw)))`) -- catching lexemes like
  `0.10000000000000001` that Python's bare `float()` would silently round
  with no signal.
* Negative zero is rejected at parse time (`yaml_profile.py`) and, as a
  second independent guard, in `jcs.py`.
* Non-finite values (`NaN`, `+inf`, `-inf`) are unrepresentable — the parser
  never produces them (the RFC 8259 number grammar cannot express them) and
  `jcs.py` fails closed if one ever reaches it.

## Approval example/operative distinction

`campaign-approval.v1.schema.json` expresses two disjoint profiles via
`oneOf`: a document carrying `marker: "EXAMPLE_ONLY_NOT_AUTHORIZATION"`
matches only the example/template profile; a document omitting `marker`
entirely matches only the operative profile (the operative profile's
`additionalProperties: false` has no `marker` property, so a document
carrying it fails that branch). `validate_campaign_approval` additionally
rejects unfilled human-placeholder tokens (e.g. `<HUMAN-FILLS-IN...>`) and a
`approval_provenance.mechanism` of `"none"`.

## Approval provenance — explicit boundary

Phase 2 validates that `approval_provenance.mechanism` and `.reference` are
**present, non-placeholder, and structurally well-formed**. It does **not**
verify a GitHub review event, a signed commit's GPG/SSH signature, or any
external identity ownership claim — no network call is made anywhere in
this package. `claimed_approver_identity` is checked only against a
caller-supplied `ValidationContext.allowed_approver_identities` set; it is
never inferred from merge state, write access, branch ownership, PR
authorship, or silence. Mechanical provenance verification is explicitly
deferred to Phase 3 (#119), per ADR 0023 section 12 item 3.

## Filesystem / artifact-root trust boundary

The pure path-containment primitives (`CanonicalPath`, `canonicalize_path`,
`has_colon_component`, `anchor_output_path`, `resolve_containment`, and the
`GATE_A_OUTPUT_PATH_*` constants) were extracted from
`scripts/gate_a_authorization.py` into
`src/sensemaking_skills/path_containment.py` -- a normal, installable
package module with no dependency on the repository checkout.
`gate_a_authorization.py` now imports these names as a genuine re-export
(`gate_a_authorization.canonicalize_path is path_containment.canonicalize_path`
holds by construction); `resolve_containment` is the one exception, kept as
a real one-line delegating `def` in `gate_a_authorization.py` because an
existing Gate A test performs source-level text inspection expecting that
function to be defined literally in that file.
`tests/test_path_containment_extraction_characterization.py` captured
behavior before the extraction and proves the re-export/delegation
introduces no drift; every existing Gate A test suite passes unchanged (see
the PR body for exact counts).

`fs_adapter.py` is a narrow adapter around this shared module -- a normal
package import, not a filesystem-path load (an earlier revision loaded
`scripts/gate_a_authorization.py` via `importlib.util.spec_from_file_location`,
which does not work from an installed wheel with no `scripts/` directory).
`load_and_validate_policy_from_root` / `..._approval_from_root` /
`..._configuration_from_root` accept explicit candidate paths (never a
glob): zero matches fails as missing, more than one match fails as
ambiguous (policy/configuration identity ambiguity, using distinct codes
for each, or more than one *operative* approval matching a policy). Every
filesystem failure while reading a candidate (permission denied, a
directory in place of the expected file, the file disappearing mid-flight,
malformed UTF-8) is converted to a deterministic `ValidationResult`; none
can escape as a raw exception.

## Stable failure codes

See `failure_codes.py`, frozen and tested in
`tests/campaign_validation/test_failure_codes.py`. Every code carries the
`CAMPAIGN_` prefix; no code collapses two independent failure categories.

## This is not an invocation capability

`ValidatedCampaignBundle` (`models.py`) carries only the three parsed,
validated documents. It has no method, token, or field that grants
provider access. No provider-facing module is imported anywhere in
`src/sensemaking_skills/campaign_validation/` (enforced by
`tests/campaign_validation/test_validators.py::test_bundle_provider_not_imported`,
an AST-based import scan).

It is also **deeply immutable**, not merely a frozen dataclass shell around
mutable dicts/lists: every `.raw` mapping is recursively frozen
(`immutable.py::freeze` -- mappings become detached `types.MappingProxyType`
copies, sequences become tuples) when the bundle is constructed. Mutating
`bundle.policy.raw`, a nested `execution_parameters` value, or an
`allowed_targets` list item all raise `TypeError`; mutating the *original*
parsed dict after validation cannot alter the already-returned bundle,
because `freeze()` copies rather than views.

## Phase 3 handoff

Phase 3 (#119) is expected to:

1. Build the actual exploratory-authorization capability from a
   `ValidatedCampaignBundle`, mirroring Gate A's capability-issuance model
   (ADR 0022) for Lane A specifically.
2. Add mechanical provenance verification (signed-commit signature checks,
   GitHub review API checks) at the provider boundary.
3. Wire attempt reservation before any provider call.

Phase 2 deliberately stops short of all three.
