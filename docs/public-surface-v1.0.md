# Version 1.0 Public Surface (reduced-scope `1.0.0-rc.1` candidate)

This document is the operator-facing interpretation of
[`release-v1.0.yaml`](../release-v1.0.yaml). The machine-readable release
contract in [`release-v1.0-contract.md`](release-v1.0-contract.md) remains
authoritative for exact IDs and claim statuses.

## Stable product surface

This release contract is classified as **reduced scope**: it promises the
local-first, mechanically qualified product surface below. Native harness
compatibility, cross-harness portability, and semantic usefulness are not
Version 1.0 support promises.

The supported command groups are:

```text
sensemaking-skills campaign
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

## Claim ceiling

Mechanical qualification establishes representation and integrity properties.
It does not establish semantic truth, usefulness, native harness discovery,
native invocation, or cross-harness portability. Those claims remain absent
from the stable promise until their evidence packages pass the corresponding
qualification protocol.
