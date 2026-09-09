# Status

**Version:** 0.3.0  
**Release state:** candidate — not yet merged/tagged/published  
**Last updated:** 2026-09-09  
**Current phase:** Productization / release qualification  
**Primary program:** Sensemaking Skills v0.3 Campaign release  
**Current frontier:** P11 — final mechanical release qualification

This is the repository's living status summary. It points at authoritative design sources and current implementation direction; it is not itself an ADR or an execution authorization.

## Product identity

Sensemaking Skills is an **agent-native engineering sensemaking and control layer for software-engineering agents**.

The central abstraction is the **Sensemaking Campaign**: a durable engineering decision process carried across agent sessions. The canonical product model is [`docs/sensemaking-campaign.md`](docs/sensemaking-campaign.md).

The active coding agent owns semantic control. Deterministic machinery owns representation, persistence, validation, provenance, authority checks, structural reconstruction, and mechanically decidable integrity constraints.

The system is not a centralized semantic router, autonomous project manager, or universal multi-agent orchestrator.

## Productization regime

Owner direction remains implementation/productization-first:

```text
identify a user-visible capability
→ implement the smallest complete vertical slice
→ validate deterministically
→ dogfood in ordinary engineering use
→ repair observed friction
→ ship the slice
```

Formal experiments are reserved for consequential uncertainties that ordinary implementation and dogfood cannot resolve.

## Integrated baseline

The productization pivot began at:

```text
main@5c2c807542f7e150d4a031430f59e297ed816b24
```

The current integrated implementation frontier is P10:

```text
main@d833095ab9b37bd9a93d39d286b358061eb913e5
```

That merge has parents:

```text
previous main
0f306cb9f05a70f2b27a64c05f65749534f9f0e1

exact-qualified P10 head
d1676b6f0209eee4c5e2c9fdb7aae07baaa74a1a
```

and exactly the qualified P10 tree:

```text
6143b47f31ccdab2e1bde9be12a31bef9864e71f
```

P11 remains on the release-candidate branch and is not integrated into `main` yet.

## Implemented Campaign milestones

### P0 — Productization pivot — MERGED

Implementation-first direction is durable; historical research retains its actual claim ceilings.

### P1 — Durable Campaign workspace — MERGED

File-backed Campaign persistence with strict typed I/O, atomic state replacement, append-only transitions/trace, physical-containment checks, and non-overwrite initialization.

### P2 — Campaign service — MERGED

Recoverable lifecycle commit intent, structural reconstruction, defer/terminate primitives, handoff generation, resume, and transition/state digest binding.

### P3 — Campaign CLI foundation — MERGED

```text
campaign init
campaign status
campaign validate
campaign history
```

### P4 — Validated artifact ingestion — MERGED

```text
artifact bytes
→ canonical validator router
→ selected validator
→ valid=true
→ content-addressed artifact
→ append-only admission receipt
→ Campaign evidence
```

Therefore:

```text
file exists
!= validated artifact
!= admitted Campaign evidence
```

P11 release hardening now packages a build-derived canonical validator runtime, so installed-wheel `campaign ingest` no longer requires a separate Sensemaking checkout in normal use. See [`docs/artifact-ingestion.md`](docs/artifact-ingestion.md).

### P5 — Agent-authored decisions — MERGED

```text
campaign advance
campaign defer
campaign close
```

The active agent supplies semantic judgment; deterministic Campaign machinery validates and persists the typed decision contract.

### P6 — Capability registry — MERGED

```text
campaign capabilities
```

Results are deterministic and unranked. Catalog membership, runtime availability, and execution authority remain separate facts.

### P7 — Durable handoff/resume — MERGED

```text
campaign handoff
campaign resume
```

P7 integrity-binds reconstruction without inventing next action, responsibility, capability, or authority. Fresh-process and installed-wheel reconstruction are qualified.

### P8 — Artifact/evidence lineage — MERGED

```text
campaign lineage
```

P8 reconstructs exact evidence identity, provenance, and explicit transition consumption without turning lineage into semantic warrant.

### P9 — Reconciliation lifecycle — MERGED

```text
campaign reconciliation
```

P9 mechanically distinguishes `disposition_required`, `disposition_recorded`, and `legacy_unbound`. Report verdict content never automatically mutates Campaign state.

### P10 — Harness adapters — MERGED

`setup-skills` provides explicit user/project installation targets for generic Agent Skills, Claude Code, Codex, and OpenCode.

P10 preserves:

```text
Skill copied to discovery root
!= harness observed Skill
!= Skill selected
!= execution authorized
!= Campaign decision
```

## P11 — v0.3.0 release qualification — CURRENT

P11 is release hardening, packaging, and exact-head qualification. It is not a new semantic product layer.

### P11-A — P10 integration — COMPLETE

P10 is integrated exactly at `main@d833095ab9b37bd9a93d39d286b358061eb913e5` with tree `6143b47f31ccdab2e1bde9be12a31bef9864e71f`.

### P11-B — self-contained artifact admission — EXACT-HEAD QUALIFIED

Historical sub-milestone qualification:

```text
head
87e4c9a04dc778e1590e7917f10f2771c5a72e7e

tree
b562d45000f8e2b51aad8d5290f94f938bbdf89a

Validator Ecosystem #752
run 34295306464
SUCCESS
```

Both Python campaign lanes reported 569 passing tests, with Two-Lane and path-containment suites green. This evidence remains valid for the portability sub-slice, but the final `0.3.0` candidate has additional release metadata/workflow changes and therefore requires a new exact-head qualification.

### P11-C — release claim reconciliation — COMPLETE

The v0.3.0 blocking claim was intentionally weakened to match already qualified evidence and avoid an open-ended experiment loop.

The release claim is:

> **Sensemaking Skills v0.3.0 provides an installable, mechanically qualified Campaign control layer for durable engineering sensemaking: validated evidence admission, explicit agent-authored decisions, capability inspection, reconciliation reconstruction, exact evidence lineage, and integrity-bound handoff/resume. Harness adapters install Skills into declared coding-agent discovery locations; runtime Skill discovery and end-to-end external-repository performance are deliberately outside the v0.3.0 qualification claim.**

The former real-harness/external-repository qualification protocol is preserved as **non-blocking post-release dogfood** in [`docs/v0.3-external-qualification-protocol.md`](docs/v0.3-external-qualification-protocol.md).

### P11-D — `0.3.0` release candidate — CURRENT

The candidate must keep package metadata, CLI version, README/STATUS, CHANGELOG, and publishing instructions consistent at `0.3.0`.

A dedicated release-candidate workflow must prove on the exact PR head:

```text
wheel build
+ sdist build
+ twine check
+ artifact SHA-256 reporting
+ fresh wheel install
+ packaged Skill tree present
+ packaged validator runtime present
+ fresh sdist install
+ CLI 0.3.0
+ Campaign CLI surface present
```

### P11-E — final exact-head qualification — NEXT

Before the P11 PR becomes ready:

```text
release candidate head frozen
→ release-candidate distribution workflow SUCCESS
→ Validator Ecosystem SUCCESS on the same exact head
→ late review surfaces empty/resolved
→ exact tree recorded
→ PR ready
```

Qualification does not imply merge or publication authority.

### P11-F — integration/release — OWNER-GATED

After explicit authorization:

```text
reverify exact head + CI + reviews
→ merge with expected-head protection
→ verify merge parents + exact qualified tree
→ tag v0.3.0
→ publish through tag workflow
→ clean production-PyPI install verification
```

## Semantic-control invariant

Agent:

- What responsibility is warranted?
- Which available capability, if any, should be selected?
- Is execution authorized?
- What does reconciliation evidence mean?
- Should the Campaign advance, defer, or close?

Deterministic machinery:

- Is an artifact admitted evidence?
- What exact identity/provenance does it have?
- Which transition explicitly consumed it?
- Is reconciliation disposition mechanically represented?
- Which explicit harness/scope destination did the caller request?
- Does the installed Skill tree match packaged bytes?
- Is Campaign history reconstructible?

Therefore:

```text
validator passed != conclusion is true
warranted responsibility != available capability
available capability != authorized capability
recommendation != execution authority
handoff != semantic recommendation
lineage != semantic warrant
reconciliation evidence != Campaign decision
harness discovery path != Skill selection or authority
Campaign Controller != semantic router
```

## v0.3.0 claim ceiling

v0.3.0 may claim mechanical qualification of the installed Campaign control layer and deterministic Skill installation adapters.

It must **not** claim:

- universal real-harness Skill discovery;
- universal external-repository end-to-end success;
- automatic capability choice;
- automatic semantic next action;
- semantic truth from validator success;
- guaranteed fresh-agent reasoning quality.

## Non-blocking dogfood after release

A real Claude Code/Codex/OpenCode-style runtime plus an external repository remains valuable empirical validation. It can use the preserved dogfood protocol and may inform v0.3.1/v0.4.

It is **not a v0.3.0 release gate**.

## Explicit non-goals for v0.3

Do not build by default:

- centralized semantic routing;
- HTN/generic planning;
- Skill ranking;
- critic/voting swarms;
- self-modifying Skills;
- autonomous SkillOpt optimization;
- Campaign server/database/cloud backend;
- universal semantic truth validation;
- automatic external mutation authority;
- full multi-repository Campaign control.

## Definition of v0.3.0 success

The first Campaign-based release is ready when the **installed distribution** mechanically demonstrates:

```text
consistent 0.3.0 release metadata
→ wheel + sdist build
→ metadata checks
→ fresh wheel install
→ self-contained artifact admission
→ Campaign lifecycle contracts
→ explicit authored-decision persistence
→ capability inspection contract
→ reconciliation reconstruction
→ exact evidence lineage
→ integrity-bound handoff
→ fresh-process resume
→ honest terminal representation
```

with full exact-head CI green and no Sensemaking source checkout required for the supported installed control surface.

## Where to look

| Topic | Source |
|---|---|
| Product definition / authority model | `CONTEXT.md` |
| Canonical Campaign model | `docs/sensemaking-campaign.md` |
| Active v0.3 delivery plan | `docs/productization-v0.3.md` |
| Post-release external dogfood protocol | `docs/v0.3-external-qualification-protocol.md` |
| Artifact admission | `docs/artifact-ingestion.md` |
| Agent-authored decisions | `docs/campaign-decisions.md` |
| Capability registry | `docs/capability-registry.md` |
| Handoff/resume | `docs/campaign-handoff-resume.md` |
| Evidence lineage | `docs/campaign-lineage.md` |
| Reconciliation lifecycle | `docs/campaign-reconciliation.md` |
| Harness adapters | `docs/harness-adapters.md` |
| Publishing | `docs/PUBLISHING.md` |
| Design decisions | `docs/adr/` |
