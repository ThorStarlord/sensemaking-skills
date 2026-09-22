# Version 1.0 Release Contract (`1.0.0rc3` reduced-scope target)

This document defines the intended Version 1.0 support surface. The machine-
readable authority is `release-v1.0.yaml`; `scripts/validate-release-contract.py`
checks that the declaration remains consistent with the repository.

## Product identity

Current repository source is `1.0.0rc3.dev0` with release status
`development`, targeting a future frozen `1.0.0rc3`. The qualified
`1.0.0rc2` candidate remains immutable historical provenance at integrated
commit `c9b86138d3919c4fce87040f14161364a0c1c3a0`.
Historical `1.0.0rc1` remains qualified provenance for exact commit
`70542d47412d98ee6dfae5de6df29bf271304568`, but continued development
superseded it as the identity of current `main`.

The `1.0.0rc3` target is a reduced-scope release of the local-first Sensemaking
Campaign control layer and its manifest-backed agent Skills. The active agent
owns semantic judgment. The product owns durable state, evidence references,
mechanical validation, provenance, integrity, and explicit authority metadata.

Release phase semantics are:

```text
development source
!= frozen candidate
!= public distribution
```

While `release.status` is `development`, the source version is the
`.dev0` predecessor of the target. A frozen candidate uses the target version
itself. The current `1.0.0rc3.dev0` source is not a frozen candidate. A future
`1.0.0rc3` freeze requires fresh exact-source qualification before any
candidate qualification claim.

## Stable surface

The stable surface is the Campaign and semantic CLI, generic Skill-format
distribution, Campaign schema v2, the manifest-backed semantic Skills, and the
public agent entrypoints declared in the release contract. Native support for
specific external harnesses is excluded until real harness evidence exists.

Legacy workflow execution remains compatibility machinery until removed or
separately promoted. It must not silently become semantic routing authority.

## Public agent entrypoints

`release-v1.0.yaml.public_surface.agent_entrypoints` names compositional Skills
that are part of the Version 1.0 operator-facing contract even when they do not
own an independent semantic responsibility.

For the current target, `strategic-sensemaking-loop` is the public one-prompt
strategic start/resume entrypoint. It remains `internal` in
`skill_inventory` because its component Skills retain semantic responsibility
and artifact ownership.

The validator requires every public agent entrypoint to name a canonical,
non-experimental Skill. This contract establishes shipped/discoverable product
surface only; it does not establish native-harness invocation, portability,
semantic usefulness, or new semantic authority.

```text
public agent entrypoint
!= supported semantic Skill automatically

entrypoint mechanically present
!= native harness observed/invoked

composition
!= new semantic controller
```

## Package boundary

The following modules remain source-only laboratory infrastructure:

```text
sensemaking_skills.campaign_validation
sensemaking_skills.campaign_accounting
sensemaking_skills.exploratory_authorization
sensemaking_skills.exploratory_execution
```

The release gate must prove this from fresh wheel and sdist installations.

## Claim levels

The release distinguishes four claim states:

- `mechanically-qualified`: structural and integrity behavior is tested.
- `empirically-qualified`: the required real-harness or behavioral evidence exists.
- `not-yet-qualified`: the capability may exist but is not a 1.0 support claim.
- `deferred`: validation is intentionally postponed and must not be implied by
  the stable product claim.

Passing a validator does not establish semantic truth, usefulness, or native
harness compatibility.

## Release gates

Before publishing a final 1.0 release, CI must pass the following independent lanes:

1. Product tests and clean package-boundary checks.
2. Fresh wheel and sdist installation checks.
3. Campaign lifecycle end-to-end checks.
4. Filesystem and path-containment security checks on supported systems.
5. Skill inventory, public agent-entrypoint, manifest, Domain Pack, and contract-authority checks.
6. Required real-harness evidence for every capability advertised as native.
7. Documentation/status reconciliation and a clean working tree.

Capabilities whose evidence is absent must be labelled deferred or excluded
rather than silently included in the 1.0 promise.

## Candidate identity invariant

A frozen release candidate is an evidence-bound source identity:

```text
candidate version
+ exact source identity
+ qualification result
+ distribution hashes
= candidate identity
```

Continued development may not silently reuse that frozen identity. Qualification
of one exact source does not transfer to later source bytes merely because the
version string was left unchanged.

## Compatibility policy

Campaign schema v2 is the 1.0 durable representation. Supported v1 input is
accepted only through deterministic migration. Breaking changes to Campaign
artifacts, CLI behavior, or manifest contracts require a documented migration
path and a versioned release decision.

The supported Python versions, operating systems, and harnesses are declared
only in `release-v1.0.yaml`. Adding support requires new verification evidence.

## Verification command

```text
python scripts/validate-release-contract.py --repo-root .
```
