# Version 1.0 Public Surface (reduced-scope `1.0.0rc3` target; development source `1.0.0rc3.dev0`)

This document is the operator-facing interpretation of
[`release-v1.0.yaml`](../release-v1.0.yaml). The machine-readable release
contract in [`release-v1.0-contract.md`](release-v1.0-contract.md) remains
authoritative for exact IDs and claim statuses.

## Stable product surface

The active `1.0.0rc3` Version 1.0 target is classified as **reduced scope**. Current source `1.0.0rc3.dev0` is development; the previously qualified `1.0.0rc2` candidate remains immutable historical provenance. This document defines the surface intended for the next candidate. The target promises the
local-first, mechanically qualified product surface below. Native harness
compatibility, cross-harness portability, and semantic usefulness are not
Version 1.0 support promises.

The supported command groups are:

```text
sensemaking-skills campaign
sensemaking-skills release
sensemaking-skills semantic
sensemaking-skills setup-skills
sensemaking-skills validate
sensemaking-skills analyze
```

The command-level compatibility contract, including the retained `test`
command and stable exit-code categories, is frozen in
[`cli-contract-v1.0.yaml`](cli-contract-v1.0.yaml).

Failure translation and fail-closed behavior are defined in
[`error-boundaries-v1.0.md`](error-boundaries-v1.0.md).

Successful and error JSON response fields are frozen in
[`cli-json-contract-v1.0.yaml`](cli-json-contract-v1.0.yaml).

The stable Python modules are:

```text
sensemaking_skills.campaign_semantics
sensemaking_skills.campaigns
sensemaking_skills.semantic_architecture
sensemaking_skills.setup_skills
```

The exact exported Python names are frozen in
[`public-api-v1.0.yaml`](public-api-v1.0.yaml). Names not listed by a module's
`__all__` are outside the Version 1.0 compatibility promise, and the manifest
also pins callable signatures and public value kinds.

Campaign schema v2 is the durable representation baseline. Supported v1 input
is migrated deterministically and does not receive new semantic interpretation.

## Public agent entrypoint

Version 1.0 declares the following public compositional agent entrypoint:

```text
strategic-sensemaking-loop
```

This is the normal one-prompt front door for starting or resuming a strategic
repository Sensemaking episode from durable state. The public-entrypoint
contract means the canonical Skill is shipped in the generic Skill-format
distribution, registered, documented, and mechanically covered by the release
contract.

The entrypoint deliberately remains classified as `internal` in the semantic
Skill inventory. That classification preserves the architecture: the loop owns
no new semantic responsibility or master artifact and instead composes existing
specialized responsibilities.

```text
public agent entrypoint
!= independent semantic capability

public entrypoint support
!= native-harness empirical qualification

one front door
!= one semantic responsibility
```

Native harness discovery/invocation, cross-harness portability, and semantic
usefulness remain outside the Version 1.0 support promise unless separately
qualified.

## Compatibility-only surface

`src/sensemaking_skills/runner.py`, `scripts/workflow-runtime.py`, legacy
workflow registries, and retained prompt-chain execution are compatibility-only
until separately promoted. They may coordinate already-selected work, resolve
paths, validate artifacts, and preserve historical integrations. They do not
own semantic routing authority, automatic uncertainty ranking, or automatic
Skill selection.

Compatibility behavior must remain covered by dedicated tests while it exists.
Deprecation requires a migration note and a release decision; removal requires
an explicit major-version compatibility decision.

## source-only laboratory surface

The following modules are retained for research and qualification work but are
not part of the shipped product contract:

```text
sensemaking_skills.campaign_validation
sensemaking_skills.campaign_accounting
sensemaking_skills.exploratory_authorization
sensemaking_skills.exploratory_execution
```

Their tests run in the lab lane and must not determine the meaning of the
stable Campaign API.

## Skill classification

Every canonical Skill is classified exactly once in `release-v1.0.yaml` as
either supported, internal, or experimental. Supported Skills have a manifest,
an artifact identity, and a resolved Domain Pack or explicit product-domain
entry. Internal Skills may ship for operator support without being a public
capability promise.

The supported engineering analysis surface includes
`strategic-repository-analysis`, which produces the mechanically validated
`strategic_repository_analysis` artifact.

Strategic Continuity v1 adds a root `strategy` CLI projection surface for
already-authored strategic analyses:

```text
strategy inspect
strategy paths
strategy uncertainty
strategy assumptions
strategy compare
strategy drift
strategy history
strategy graph
```

These commands inspect authored representation/currentness/history only.
`strategy drift` may emit typed mechanical observations; `strategy history`
and `strategy graph` preserve caller-supplied order and declared relationships.
They do not generate, rank, select, authorize, invalidate, semantically
reinterpret, or automatically reopen strategy.

The supported strategic companion surface also includes:

- `strategic-repository-reconciliation` -> `strategic_reconciliation`;
- `owner-decision-capsule` -> `owner_decision_capsule`;
- `thesis-review-packet` -> `thesis_review_packet`;
- `external-evidence-packet` -> `external_evidence_packet`.

These are explicit semantic-agent packets, not runtime engines or authority
tokens.

The supported Level-3 engineering surface also includes
`multi-repository-strategic-analysis` -> `multi_repository_strategic_analysis`.
It operates only on an explicitly selected repository set and may reuse declared
multi-target relations as evidence. It does not discover repositories, mutate
Campaign target sets, rank boundary paths numerically, or coordinate
cross-repository transactions.

The supported engineering analysis surface also includes
`change-impact-analysis` -> `change_impact_analysis`. It maps
decision-relevant affected code/contracts/artifacts/tests/docs/claims/authority/
release/cross-repository surfaces around a bounded change and records required
verification/reconciliation or higher-scope review. It does not authorize the
change, generate an automatic backlog, or expand repository scope. It models current capability state,
0–5 materially real repository construction paths, qualitative tradeoffs,
decision-changing uncertainty, and a semantic strategic disposition while
preserving:

```text
strategic analysis != implementation authorization
currentness observation != semantic consequence
path transition != roadmap item
history projection != strategic judgment
path comparison != numeric ranking
mechanically valid != semantically correct
```

The Skill is a semantic-agent capability, not a CLI planner or automatic
repository-work selector.

## Claim ceiling

Mechanical qualification establishes representation and integrity properties.
It does not establish semantic truth, usefulness, native harness discovery,
native invocation, or cross-harness portability. Those claims remain absent
from the stable promise until their evidence packages pass the corresponding
qualification protocol.