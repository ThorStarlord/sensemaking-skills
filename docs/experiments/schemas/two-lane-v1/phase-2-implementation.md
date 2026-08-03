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
* **Negative zero is rejected globally, at the parser boundary, for every
  numeric field** -- not just floats. `-0.0`/`-0e0`/etc. are caught in the
  float-lexeme path (`_parse_exact_float`); a bare integer-lexeme `-0` is
  caught separately and explicitly in `_resolve_scalar` (the integer-lexeme
  grammar has exactly one zero spelling, `"0"`, so `-0` is the only
  negative-signed integer-lexeme string that can equal zero, and
  `int("-0")` would otherwise silently discard the sign and become ordinary
  `0`). This applies uniformly to policy integer fields, `cost_ceiling.amount`,
  every level of `execution_parameters` nesting, and any other numeric
  field -- rejection happens once, at the parser, not per-field. `jcs.py`
  also independently rejects negative zero as a second guard, but the
  parser-level rejection is the primary, authoritative one (a value that
  never parses can never reach JCS at all).
* Non-finite values (`NaN`, `+inf`, `-inf`) are unrepresentable — the parser
  never produces them (the RFC 8259 number grammar cannot express them) and
  `jcs.py` fails closed if one ever reaches it.

## Approval example/operative distinction

`campaign-approval.v1.schema.json` expresses two **fully independent**
`oneOf` branches -- each branch defines its own fields from scratch, with no
shared field-schema reference between them. An earlier revision had both
branches `allOf`-reference one shared `commonFields` definition (with
strict RFC3339/sha256-hex patterns); because `allOf` constituents are
evaluated independently and ALL must pass, that shared reference silently
forced the strict, operative-grade patterns onto the example/template
branch too -- which made the documented blank template (whose `approved_at`
is the literal placeholder string `"<HUMAN-FILLS-IN RFC3339 timestamp>"`)
fail its own documentation schema. Now:

* the **example/template branch** requires `marker: "EXAMPLE_ONLY_NOT_AUTHORIZATION"`
  and accepts any non-empty string for every other field (a human has not
  filled them in yet);
* the **operative branch** forbids `marker` entirely and retains every
  strict pattern (`campaign_id`, RFC3339 `approved_at`, non-empty
  provenance fields).

`validate_campaign_approval` detects the `marker` key **before** running
any operative-grade schema check at all -- a template can never become
operative no matter what else is (deliberately) blank or malformed about
it; this ordering is exercised directly in
`tests/campaign_validation/test_second_correction.py`. The validator
additionally rejects unfilled human-placeholder tokens (e.g.
`<HUMAN-FILLS-IN...>`) and an `approval_provenance.mechanism` of `"none"`
on the operative path.

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

## Checkout-local Gate A loading

`scripts/gate_a_authorization.py` deterministically loads
`sensemaking_skills.path_containment` from its OWN checkout, never from an
ambient/pre-imported installation that happens to resolve first. Sequence
(`_load_checkout_local_path_containment`): resolve the expected `src/`
directory and exact `path_containment.py` file from
`Path(__file__).resolve()` (never the current working directory); put that
`src/` directory at the front of `sys.path` and invalidate import caches;
if `sensemaking_skills` is ALREADY imported from somewhere else, fail
closed immediately (`ImportError`) rather than silently evict-and-reimport;
import fresh and verify the loaded module's resolved `__file__` is exactly
the expected checkout-local file, failing closed on any mismatch before any
security decision is possible.
`tests/test_gate_a_checkout_local_containment.py` proves this with real
subprocesses against a deliberately conflicting fake ambient package (both
"conflicting package earlier on PYTHONPATH" and "conflicting package
pre-imported before Gate A" cases), and confirms the separate
`campaign_validation` package's installed-wheel support is unaffected (it
already imports `sensemaking_skills.path_containment` as a normal package
import, never a filesystem-path load).

## Validator-owned CampaignPolicy provenance

`CampaignPolicy`/`CampaignApproval`/`ConfigurationIdentity` cannot be
constructed by ordinary public API use -- `CampaignPolicy(...)` raises
`TypeError`. Instances are created only by a module-private factory
(`models.py::_seal_dataclass`), which stamps a per-process sentinel object
-- held only in a closure, never exported -- onto the instance via
`object.__setattr__` (bypassing the disabled constructor). A paired
module-private verifier checks that sentinel by identity.
`validate_campaign_approval`/`validate_configuration_identity` call the
verifier (`_is_genuine_campaign_policy`), not a bare `isinstance` check,
before trusting a `policy` argument -- so a plain mapping, a hand-built
instance via `object.__new__` guessing at a `_provenance_seal` attribute,
or a `dataclasses.replace()` copy all fail closed with
`CAMPAIGN_INTERNAL_VALIDATION_ERROR`. This is not a claim of protection
against hostile arbitrary code in the same interpreter (which could import
the private factory directly) -- it prevents normal API misuse and
accidental nominal-type forgery.

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

## Stable failure codes and deterministic precedence

See `failure_codes.py`, frozen and tested in
`tests/campaign_validation/test_failure_codes.py` (39 codes, calculated
programmatically via `len(CAMPAIGN_FAILURE_CODES)` -- never a manually
carried-forward number). Every code carries the `CAMPAIGN_` prefix; no code
collapses two independent failure categories.
`tests/campaign_validation/test_failure_code_reachability.py` is the actual
reachability matrix: one direct trigger per code, executing the real
parser/validator/root-loader and asserting exact equality -- not merely a
membership check against the frozen mapping.

**Numeric-domain preflight** (`numeric_domain.py`): arbitrary-precision
integer lexemes parse as genuine Python `int` (no truncation), but
`rfc8785` only accepts the interoperable safe-integer domain
(+/-9007199254740991). `find_out_of_domain_path` recursively walks a parsed
document (mappings and sequences, booleans never treated as integers)
BEFORE digest computation, so an oversized value is an ordinary,
deterministic `CAMPAIGN_POLICY_LIMITS_INVALID` (policy fields, including
`cost_ceiling.amount`) or `CAMPAIGN_CONFIGURATION_NUMERIC_DOMAIN_INVALID`
(anywhere inside `execution_parameters`, at any nesting depth) -- never
`CAMPAIGN_INTERNAL_VALIDATION_ERROR`. `jcs.JCSError`/
`rfc8785.CanonicalizationError`/`OverflowError` are also caught explicitly
around the digest-computation calls themselves as defense in depth.

**Exact version-field precedence** (policy/approval/configuration): a
MISSING or non-string version field is a structural fault
(`*_SCHEMA_INVALID`); only a well-formed string naming an unsupported
version gets `*_SCHEMA_UNSUPPORTED`. `.get()` alone would conflate "absent"
with "unsupported" -- presence and type are checked explicitly first.
`CAMPAIGN_CONFIGURATION_SCHEMA_UNSUPPORTED` is a new code added for this.

**Precedence is deterministic by construction, not a race against
jsonschema's error ordering.** The three JSON Schemas are deliberately loose
(base type only, no value-level constraint) on every field whose exact
VALUE -- not just its scalar type -- is owned exclusively by Python (see
each schema's own `$comment`): `policy_digest`/`configuration_id` format
and correctness, the four `*_prohibited` boolean VALUES, and every
policy numeric limit/range/cross-field rule, including the
integer-lexeme-source-form rule the schema language cannot express at all.
A malformed value in one of those fields therefore always produces its own
specific code (e.g. `CAMPAIGN_POLICY_DIGEST_MALFORMED`, never
`CAMPAIGN_POLICY_SCHEMA_INVALID`); only a genuine structural violation
(wrong scalar type, a missing required field, an unknown closed-object
field) ever reaches jsonschema for those particular fields.
`tests/campaign_validation/test_second_correction.py` freezes this with
exact-equality assertions, including multi-fault fixtures proving the
precedence order (source-profile -> schema/version -> Python-owned
digest/format -> Python-owned limits/range) stays deterministic even when
several faults are present in the same document at once.

## This is not an invocation capability

`ValidatedCampaignBundle` (`models.py`) carries only the three validated
documents. It has no method, token, or field that grants provider access.
No provider-facing module is imported anywhere in
`src/sensemaking_skills/campaign_validation/` (enforced by
`tests/campaign_validation/test_validators.py::test_bundle_provider_not_imported`,
an AST-based import scan).

**Every successful public validator returns an immutable, typed model --
never a plain, mutable `dict`.** `validate_campaign_policy` returns
`CampaignPolicy`; `validate_campaign_approval` returns `CampaignApproval`;
`validate_configuration_identity` returns `ConfigurationIdentity`;
`validate_campaign_bundle` returns `ValidatedCampaignBundle` (composed
directly from the three already-validated, already-immutable typed objects
the single-artifact validators returned -- it never reconstructs new
wrappers from mutable mappings). Every one of these is deeply immutable,
not merely a frozen dataclass shell around mutable dicts/lists: every
`.raw` mapping is recursively frozen (`immutable.py::freeze` -- mappings
become detached `types.MappingProxyType` copies, sequences become tuples)
at the public boundary, exactly once, on the way out. Mutating `.raw`, a
nested `execution_parameters` value, or an `allowed_targets` list item all
raise `TypeError`; mutating the *original* parsed dict after validation
cannot alter the already-returned model, because `freeze()` copies rather
than views.

`validate_campaign_approval` and `validate_configuration_identity` now
consume an already-validated `CampaignPolicy` object as their `policy`
argument -- never an arbitrary caller-supplied mapping. Passing anything
else (a plain dict, `None`, ...) fails closed with
`CAMPAIGN_INTERNAL_VALIDATION_ERROR` rather than silently trusting
unvalidated data as though it conferred authority.

## Phase 3 handoff

Phase 3 (#119) is expected to:

1. Build the actual exploratory-authorization capability from a
   `ValidatedCampaignBundle`, mirroring Gate A's capability-issuance model
   (ADR 0022) for Lane A specifically.
2. Add mechanical provenance verification (signed-commit signature checks,
   GitHub review API checks) at the provider boundary.
3. Wire attempt reservation before any provider call.

Phase 2 deliberately stops short of all three.
