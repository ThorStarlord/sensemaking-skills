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
| `jcs.py` | RFC 8785 (JCS) canonicalization |
| `digests.py` | `compute_policy_digest`, `compute_configuration_id` |
| `models.py` | Frozen dataclasses: `ValidationContext`, `ValidationResult`, `CampaignPolicy`, `CampaignApproval`, `ConfigurationIdentity`, `ValidatedCampaignBundle` |
| `failure_codes.py` | Frozen `CAMPAIGN_FAILURE_CODES` mapping |
| `schema_validation.py` | JSON Schema (Draft 2020-12) validation against the parsed data model |
| `fs_adapter.py` | Narrow adapter around Gate A's path-containment primitives |
| `validators.py` | `validate_campaign_policy`, `validate_campaign_approval`, `validate_configuration_identity`, `validate_campaign_bundle`, and root-scoped loaders |

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

`docs/experiments/schemas/two-lane-v1/json/`:

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

**Custom implementation** (`jcs.py`), not a third-party dependency. At the
time of writing, no maintained PyPI package resolvable from this
environment's configured index implements RFC 8785's ECMAScript-compatible
number formatting; `canonicaljson` (a real, available package) uses Python's
`json` module for number formatting, which does not implement ECMAScript
`Number::toString` — e.g. `json.dumps(1.0)` produces `"1.0"`, not the
JCS-mandated `"1"`, which would silently violate ADR 0023's "1.0 and 1e0
canonicalize identically" requirement for any non-integer-typed field. No
`rfc8785`/`jsoncanonicalizer`/`python-json-canonicalize` distribution was
resolvable either. The custom implementation extracts the shortest
round-tripping decimal digit string from Python's `repr(float)` (which, like
ECMAScript engines, uses a shortest-round-trip algorithm) and re-renders it
using the exact ECMAScript `Number::toString` positional/exponential rules
(RFC 8785 section 3.2.2.3), rather than Python's own float-formatting rules.
Conformance is checked against a table of reference vectors in
`tests/campaign_validation/test_jcs.py`, including presentation-equivalence
(`1`/`1.0`/`1e0` canonicalize identically), negative-zero rejection,
non-finite rejection, Unicode NFC/NFD distinctness, and object-key sorting.

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

* Integer-valued policy fields are validated as mathematically-integral
  JSON numbers in the safe-integer range; `1`, `1.0`, and `1e0` canonicalize
  identically (no source-spelling restriction is invented against
  `1.0`/`1e0`, per explicit ADR 0023 instruction). `1.5` and quoted `"1"`
  are rejected for integer-typed fields by the JSON Schema layer.
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

`fs_adapter.py` is a narrow adapter around
`scripts/gate_a_authorization.py`'s existing `canonicalize_path` /
`resolve_containment` functions, loaded by file path via
`importlib.util.spec_from_file_location` (never via `sys.path` mutation).
**No line of `gate_a_authorization.py` is edited by this phase** — every
existing Gate A test suite passes unchanged (see the PR body for exact
counts). `load_and_validate_policy_from_root` /
`..._approval_from_root` / `..._configuration_from_root` accept explicit
candidate paths (never a glob): zero matches fails as missing, more than one
match fails as ambiguous (policy/configuration identity ambiguity, or more
than one *operative* approval matching a policy).

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

## Phase 3 handoff

Phase 3 (#119) is expected to:

1. Build the actual exploratory-authorization capability from a
   `ValidatedCampaignBundle`, mirroring Gate A's capability-issuance model
   (ADR 0022) for Lane A specifically.
2. Add mechanical provenance verification (signed-commit signature checks,
   GitHub review API checks) at the provider boundary.
3. Wire attempt reservation before any provider call.

Phase 2 deliberately stops short of all three.
