# Phase 3 implementation notes — four-lane authorization and the exploratory capability

Program: Issue #116. This phase: Issue #119 (Phase 3). Governing contracts:
ADR 0023 (Two-Lane Experiment Authorization) and ADR 0022 (Gate A
authorization capability). This document describes the runtime
implementation added in this phase; it is not itself a contract — ADR 0023,
ADR 0022, and the schema-contract Markdown files remain normative.

## Scope

This phase implements the **four-lane authorization model** — ORDINARY /
CANONICAL / EXPLORATORY / AMBIGUOUS — and the **exploratory capability**:
a minted, deeply immutable, registry-live invocation capability for the
EXPLORATORY lane whose consumption is atomic and permanently spent at the
real provider boundary in `scripts/skill_executor.py`.

It does **not** implement durable reservations or attempt ledgers, recovery
or replay, campaign-summary mutation, canonical promotion, approval
mechanical signature verification beyond the existing provenance-verifier
abstraction, or any real provider invocation — every test uses a spy
provider and asserts zero provider calls on every denial path.

## Production module location

Two homes, mirroring the Phase 2 split between the packaged library and the
checkout-local Gate A scripts:

| Location | Responsibility |
|---|---|
| `src/sensemaking_skills/exploratory_authorization/` | The capability package: failure codes, digests, models, registry, provenance verifier, issuer, boundary |
| `scripts/gate_a_authorization.py` | Lane derivation (`derive_authorization_lane`) and the `DeclaredExploratory` declaration model |
| `scripts/skill_executor.py` | The enforcement point: `require_invocation_authorization` dispatcher, both real executors, atomic consumption at the narrowest point before the provider call |

Lane derivation lives in `gate_a_authorization.py` — not in the packaged
library — because the Gate A CI job runs checkout-local without installing
the package, and the lane decision is a Gate A decision.

## The four-lane model

`derive_authorization_lane(identity, declared=None) -> (lane, signals)`
classifies every invocation:

* **ORDINARY** — an ordinary path identity with no exploratory declaration.
  No Gate A capability is required.
* **CANONICAL** — a canonical experiment (or stage-1 controlled) path
  identity. The canonical `AuthorizedInvocation` is required, exactly as in
  Phase 1/2 (`CONTROLLED_STAGE1` is always CANONICAL, never downgraded).
* **AMBIGUOUS** — any exploratory *claim* that cannot be cleanly honored:
  a well-formed claim on an identity that is not a clean
  `EXPERIMENTS_NON_EVIDENCE_PATH`, a malformed or partial declaration, a
  contradiction between the declaration and the invocation facts, a
  controlled-stage flavor, or a path-containment signal. AMBIGUOUS requires
  the **canonical** capability — the exploratory capability cannot run it.
* **EXPLORATORY** — a well-formed, contradiction-free declaration whose
  campaign id exactly matches the campaign id extracted from the actual
  invocation path (`experiments/campaigns/<id>`). Requires a live,
  unspent exploratory capability.

The lane is derived from the actual invocation identity plus the declared
facts in the call context — never from a boolean, an attribute, an
environment variable, or `authorized=true`-style marker.

### The fail-closed corner that forced the dispatcher

`derive_authorization_lane` returns AMBIGUOUS for a well-formed declaration
on an identity that is *not* a clean non-evidence experiments path. Before
the dispatcher existed, re-classification inside
`require_authorization_capability` re-derived the mode from the identity
alone and classified such an invocation ORDINARY — silently bypassing Gate
A. `require_invocation_authorization` therefore **forces** the pre-derived
lane's mode into `require_authorization_capability` for every
CANONICAL/AMBIGUOUS invocation, so a declaration-induced AMBIGUOUS demands
the canonical capability. The mixed-declaration boundary tests pin this
behavior.

## The exploratory capability

`ExploratoryInvocationCapability` (package `models.py`) is minted by
`mint_exploratory_capability` from a genuine
`ValidatedCampaignBundle` (verified transitively via
`is_genuine_campaign_bundle`, a validator-owned provenance check added in
Phase 3). It is deeply immutable, detached from its inputs, and not
publicly constructible, copyable, `deepcopy`-able, pickleable,
subclassable, or serializable. A registry singleton is the only liveness
authority; expiry is rechecked at consumption.

Consumption is atomic: `consume_exploratory_capability` binds all 13
invocation facts, and any drift between the capability's bindings and the
actual invocation — or any provider exception after consumption — burns the
capability permanently (`ExploratoryConsumptionDecision.BURNED` /
`DEAD`), so a spent capability can never run twice.

## Enforcement at the provider boundary

`require_invocation_authorization` (in `skill_executor.py`) is the
dispatcher both real executors (`ClaudeAgentSdkSkillExecutor`,
`ApiSkillExecutor`) call — in the constructor, in `invoke_skill` as a
fail-fast pre-check, and in the production invocation path:

* EXPLORATORY → non-consuming availability fail-fast
  (`exploratory_capability_availability`: required, right type, live in the
  registry, state ISSUED), then at the narrowest point before the provider
  call the capability is consumed atomically (wrong type / not live /
  expired / any of the 13 drift categories → typed failure code, burned,
  provider never called).
* ORDINARY → returns before any Gate A machinery.
* CANONICAL / AMBIGUOUS → the canonical `AuthorizedInvocation` path,
  forced-mode, exactly as Phase 1/2.

The invocation context is built from the call (`ExploratoryInvocationContext`
with `target_repository`, `target_sha`, `execution_framework_sha`,
`artifact_type`, output path, campaign id, configuration id, configuration
snapshot digest, policy digest, approval digest, attempt id, model, lane) —
never from executor attributes or from the capability itself. EXPLORATORY
never touches the canonical `authorization.consume` path, and CANONICAL /
AMBIGUOUS never touches the exploratory capability; a lane mismatch fails
closed with zero provider calls.

## Stable failure codes

`failure_codes.py` defines the stable one-trigger failure codes with exact
precedence (availability: required → wrong type → not live → state;
consumption: type → liveness → state → expiry → atomic claim → the 13
binding fields → complete), each with a deterministic detail string. The
executor maps exploratory rejection to
`ExploratoryAuthorizationRequired(GateAAuthorizationRequired)` so
`_is_gate_a_authorization_error` handling stays uniform.

### Canonical-path import isolation (CI correction)

The Gate A CI jobs run a minimal environment that does not install
`rfc8785`. `skill_executor.py` therefore imports
`sensemaking_skills.exploratory_authorization` **lazily**, inside
`_load_exploratory_authorization()`, only from a genuinely EXPLORATORY
branch (dispatcher availability pre-check, invocation-context builder, both
consume sites, both burn sites), caching the loaded module in `_EA_MODULE`.
ORDINARY / CANONICAL / AMBIGUOUS invocations never import the exploratory
component, `campaign_validation`, `rfc8785`, or `jsonschema`.

If the component is missing, the EXPLORATORY lane fails closed with the
stable code `EXPLORATORY_AUTHORIZATION_COMPONENT_UNAVAILABLE` (raised as
`ExploratoryAuthorizationRequired`) before any provider construction, with
zero provider calls; there is no downgrade to ORDINARY or CANONICAL, no
canonical fallback, and no raw `ModuleNotFoundError` as an authorization
result. Precedence on the EXPLORATORY lane: **component availability
precedes capability availability** — a missing component is reported as
component-unavailable, never as a capability-liveness failure.
`tests/test_exploratory_component_isolation.py` covers this with
subprocess-based tests (including a spy-provider test proving zero provider
calls).

## TDD and test layout

All five suites were written red first and are green at the exact head:

| Suite | Coverage |
|---|---|
| `tests/test_exploratory_digests.py` | Independent digest-vector tests (RFC 8785 adapter, configuration snapshot digest including `campaign_id` + `configuration_id`, reference vectors pinned) |
| `tests/test_exploratory_lane_derivation.py` | The four-lane decision table, contradiction signals, malformed declarations, `_extract_campaign_id` path-prefix rule |
| `tests/test_exploratory_capability_lifecycle.py` | Mint / consume / burn lifecycle, deep immutability, registry liveness, expiry recheck |
| `tests/test_exploratory_provider_boundary.py` | REAL executors + spy provider: 12 drift categories, zero-invocation assertions on every denial, mixed-declaration fail-closed behavior |
| `tests/test_exploratory_component_isolation.py` | Subprocess isolation tests: canonical-path zero-import proof, component-unavailable exact code, no-declaration-downgrade, zero-provider-calls fail-closed |
| `tests/exploratory_fixtures.py` | Clock-relative fixture constants (no date flakes) and the shared capability-minting helpers |

## Verification summary

* Phase 3 suites + canonical boundary: 181 passed / 0 failed (incl. the
  isolation suite).
* Gate A CI-like suites (7 files): 794 passed / 12 skipped / 439 subtests —
  byte-identical totals and results at `fcc6772b` (base) and the PR head.
* Full `tests/` tree base-vs-head parity: identical failure set (24,
  all pre-existing environment artifacts such as the installed-wheel smoke
  under a `PYTHONPATH=src` harness and provider-requiring integration
  tests), identical skips (21), identical errors (3), identical subtests
  (786); head = base + 127 new Phase 3 passes. After the import-isolation
  correction the head tree is: 24 failed / 2226 passed / 21 skipped / 3
  errors / 786 subtests — identical failures, +9 passes (isolation suite).
* `scripts/validate-repo.py`: "Validation passed".
* The CI job `phase3-exploratory-authorization` asserts the exact head SHA,
  a clean worktree after the suites, and that no `EXP-*` experiment state
  was created; existing jobs are untouched.

## Phase 4 handoff

Phase 4 is expected to add durable attempt reservations and ledgers
(cross-process), recovery of burned/expired capabilities, and campaign-summary
mutation. Phase 3 deliberately stops short of all three; consumption remains
in-process-atomic with the registry singleton as the only liveness authority.
