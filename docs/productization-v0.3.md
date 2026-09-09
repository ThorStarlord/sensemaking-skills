# Sensemaking Skills v0.3 Productization Plan

**Status:** ACTIVE owner direction — release candidate qualification  
**Effective:** 2026-09-08; release claim revised 2026-09-09  
**Base at pivot:** `main@5c2c807542f7e150d4a031430f59e297ed816b24`  
**Current integrated frontier:** P10 merged at `main@d833095ab9b37bd9a93d39d286b358061eb913e5`  
**Current implementation frontier:** P11 — v0.3.0 mechanical release qualification  
**Primary objective:** ship the first usable Campaign-based release without turning release qualification into an open-ended empirical research program.  
**Canonical product model:** [`sensemaking-campaign.md`](sensemaking-campaign.md)

This document is the versioned v0.3 delivery plan. The durable definition of a Sensemaking Campaign belongs in [`sensemaking-campaign.md`](sensemaking-campaign.md).

## 1. Development regime

The repository is implementation/productization-first:

```text
identify a user-visible capability
→ implement the smallest complete vertical slice
→ validate deterministically
→ dogfood in ordinary engineering use
→ repair observed friction
→ ship the slice
```

Formal experiments are reserved for consequential uncertainties that ordinary implementation and dogfood cannot reasonably resolve. Existing research remains evidence and keeps its actual claim ceilings.

The v0.3 release must therefore avoid this anti-pattern:

```text
feature works
→ require a stronger adjacent empirical claim
→ create another experiment
→ move the release boundary again
```

## 2. Product boundary preserved

The productization program does not reverse the accepted agent-native control model.

- The active coding agent owns semantic control.
- Deterministic Python owns representation, persistence, validation, provenance, authority checks, integrity, and structural reconstruction.
- Validator success does not make a semantic conclusion true.
- Capability availability does not select or authorize a capability.
- A handoff reconstructs durable context; it does not decide what a fresh agent should do.
- Provenance/lineage does not establish semantic warrant.
- Reconciliation evidence does not decide the Campaign transition.
- Harness setup/discovery-root mapping does not establish runtime Skill discovery, selection, or execution authority.
- Packaging the validator runtime changes deployment portability, not semantic validator authority.

The durable distinctions remain:

```text
warranted responsibility
!= capability availability
!= execution authority

provenance
!= semantic truth

consumed evidence
!= sufficient evidence

reconciliation evidence
!= semantic disposition

Skill copied to discovery root
!= harness observed Skill
!= Skill selected
!= execution authorized
```

## 3. v0.3.0 release claim

The blocking release claim is intentionally narrower than the optional external dogfood claim:

> **Sensemaking Skills v0.3.0 provides an installable, mechanically qualified Campaign control layer for durable engineering sensemaking: validated evidence admission, explicit agent-authored decisions, capability inspection, reconciliation reconstruction, exact evidence lineage, and integrity-bound handoff/resume. Harness adapters install Skills into declared coding-agent discovery locations; runtime Skill discovery and end-to-end external-repository performance are deliberately outside the v0.3.0 qualification claim.**

This means v0.3.0 claims that the deterministic Campaign machinery and shipped distribution work as specified. It does **not** claim that every coding-agent harness will discover Skills correctly, that every external repository will complete a golden path, or that a fresh model will always make a good semantic continuation decision.

## 4. Mechanically qualified product path

The installed distribution must support the deterministic surfaces needed for the Campaign lifecycle:

```text
fresh distribution
→ campaign init / status / validate / history
→ canonical artifact admission
→ explicit authored advance / defer / close contracts
→ capability inspection
→ reconciliation reconstruction
→ exact evidence lineage inspection
→ handoff
→ fresh-process resume
→ honest stop
```

Semantic work remains agent-owned. The release gate proves the machinery that stores, validates, reconstructs, and exposes those decisions.

## 5. Milestone status

| Milestone | Status | Outcome |
|---|---|---|
| **P0 — Productization pivot** | **MERGED** | Implementation-first direction made durable. |
| **P1 — Durable campaign workspace** | **MERGED** | Isolated file-backed Campaign persistence with strict typed I/O and fail-closed filesystem boundaries. |
| **P2 — Campaign service** | **MERGED** | Recoverable lifecycle commits, reconstruction, defer/terminate, handoff, and resume primitives. |
| **P3 — Campaign CLI foundation** | **MERGED** | `campaign init/status/validate/history`. |
| **P4 — Validated artifact ingestion** | **MERGED** | Canonically validated, content-addressed admission with append-only receipts. |
| **P5 — Agent-authored decisions** | **MERGED** | Explicit `campaign advance/defer/close` without semantic routing. |
| **P6 — Capability registry** | **MERGED** | Deterministic, unranked capability inspection with availability/authority separation. |
| **P7 — Durable handoff/resume** | **MERGED** | Integrity-bound reconstruction and fresh-process/installed-wheel proof. |
| **P8 — Artifact/evidence lineage** | **MERGED** | Exact evidence-byte identity, provenance, and transition-consumption reconstruction. |
| **P9 — Reconciliation lifecycle** | **MERGED** | Mechanical disposition reconstruction without semantic auto-routing. |
| **P10 — Harness adapters** | **MERGED** | Explicit Claude/Codex/OpenCode/generic discovery-root setup without harness auto-detection. |
| **P11 — v0.3 qualification/release** | **CURRENT** | Self-contained distribution, release metadata, wheel+sdist qualification, exact-head CI, then integration/release. |

## 6. Integrated milestone contracts

### P1–P3 — durable Campaign foundation

Campaign state is file-backed, typed, reconstructible, and protected by explicit lifecycle operations. The public CLI exposes initialization, status, validation, and history without introducing a semantic planner.

### P4 — validated artifact admission

```text
artifact bytes
→ canonical validate-and-report.py router
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

P11 release hardening derives the canonical repository validator runtime into the built distribution. Normal installed use of `campaign ingest` no longer requires a separate Sensemaking checkout. The receipt still records the exact router and validator bytes that ran. See [`artifact-ingestion.md`](artifact-ingestion.md).

### P5 — agent-authored decisions

```text
durable evidence
→ agent semantic judgment
→ typed decision
→ CampaignService lifecycle primitive
→ recoverable CampaignState + TransitionRecord + trace
```

P5 never ranks capabilities or turns artifact text into automatic next action. See [`campaign-decisions.md`](campaign-decisions.md).

### P6 — capability inspection

`campaign capabilities` returns deterministic, unranked candidate metadata only after the agent supplies a responsibility classification.

```text
registered
!= available
!= authorized
```

See [`capability-registry.md`](capability-registry.md).

### P7 — handoff/resume

`campaign handoff` and `campaign resume` integrity-bind durable reconstruction without changing the semantic `CampaignHandoff` schema or inventing next action. Fresh-process and installed-wheel reconstruction are mechanically proven. See [`campaign-handoff-resume.md`](campaign-handoff-resume.md).

### P8 — lineage

`campaign lineage` reconstructs exact evidence identity, admission provenance, and explicit transition consumption without asserting semantic sufficiency. Historical transitions without P8 binding remain honestly `legacy_unbound`. See [`campaign-lineage.md`](campaign-lineage.md).

### P9 — reconciliation lifecycle

`campaign reconciliation` distinguishes mechanically:

```text
disposition_required
disposition_recorded
legacy_unbound
```

`disposition_recorded` means only that a committed Campaign transition explicitly consumed the exact report. It does not mean the report was correct or sufficient. See [`campaign-reconciliation.md`](campaign-reconciliation.md).

### P10 — harness adapters

The setup surface supports explicit user/project destinations for generic Agent Skills, Claude Code, Codex, and OpenCode, while retaining compatibility targets.

P10 proves deterministic installation and drift handling, not runtime harness behavior:

```text
copied to declared discovery root
!= harness observed Skill
!= Skill selected
!= execution authorized
!= Campaign decision
```

See [`harness-adapters.md`](harness-adapters.md).

## 7. P11 — v0.3.0 release qualification

P11 is release hardening and qualification, not another semantic product layer.

### P11-A — P10 integration — COMPLETE

P10 was merged from exact-qualified head:

```text
d1676b6f0209eee4c5e2c9fdb7aae07baaa74a1a
```

into:

```text
main@d833095ab9b37bd9a93d39d286b358061eb913e5
```

with the exact qualified tree:

```text
6143b47f31ccdab2e1bde9be12a31bef9864e71f
```

### P11-B — self-contained artifact validation — EXACT-HEAD QUALIFIED

The pre-release portability blocker was:

```text
pip install sensemaking-skills
→ campaign ingest required --framework-root
→ separate Sensemaking source checkout required
```

The installed path is now:

```text
canonical repository scripts/ + skills/
→ build-time derived validator_runtime/
→ installed wheel
→ campaign ingest without --framework-root
→ canonical router / selected validator
→ unchanged P4 admission receipt/provenance
```

The repository-root `scripts/` and `skills/` trees remain the single maintained sources. Explicit `--framework-root` remains a development/compatibility override and fails closed when invalid.

P11-B was exact-head qualified at `87e4c9a04dc778e1590e7917f10f2771c5a72e7e`, tree `b562d45000f8e2b51aad8d5290f94f938bbdf89a`, by Validator Ecosystem #752 / run `34295306464` before the final `0.3.0` release-metadata changes. That run is retained as historical sub-milestone evidence; the final release candidate must receive a new exact-head qualification.

### P11-C — release claim reconciliation — COMPLETE

The stronger real-harness/external-repository experiment is no longer a v0.3.0 release gate.

The former qualification protocol is preserved as [`v0.3-external-qualification-protocol.md`](v0.3-external-qualification-protocol.md), now explicitly classified as **non-blocking post-release dogfood**.

This prevents the release boundary from expanding into an open-ended empirical program while preserving a disciplined method for future runtime validation.

### P11-D — `0.3.0` release metadata and distribution — CURRENT

The final candidate must keep these release authorities consistent:

```text
pyproject.toml
setup.py
src/sensemaking_skills/__init__.py
CLI --version
README / STATUS
CHANGELOG / publishing instructions
```

The dedicated release-candidate workflow must:

1. assert exact-head checkout;
2. build both wheel and sdist;
3. run `twine check` on both;
4. verify exact `0.3.0` artifact filenames;
5. record SHA-256 digests;
6. clean-install the wheel outside the source checkout;
7. verify CLI version and Campaign surface;
8. verify packaged Skill trees and validator runtime;
9. clean-install the sdist and verify CLI version/Campaign surface.

### P11-E — final exact-head qualification — REQUIRED

Before the PR becomes ready:

```text
release candidate head frozen
→ release-candidate distribution workflow SUCCESS
→ Validator Ecosystem SUCCESS on same exact head
→ review threads/reviews/comments checked
→ candidate tree recorded
→ PR marked ready
```

CI success does not itself authorize merge or publication.

### P11-F — integration and publication — OWNER-GATED

After explicit owner authorization:

```text
reverify exact head + CI + reviews
→ merge with expected-head protection
→ verify merge parents and exact qualified tree
→ tag v0.3.0
→ publish through the tag workflow
→ clean production-PyPI install verification
```

If a genuine defect is found after publication, do not rewrite `0.3.0`; repair and qualify `0.3.1`.

## 8. Non-blocking external dogfood

A real supported harness running the complete Campaign golden path on an external repository remains highly valuable, but it is **not required to publish v0.3.0**.

Optional dogfood may later test:

```text
real harness Skill discovery/invocation
→ external repository diagnosis
→ full Campaign lifecycle
→ genuine fresh-agent continuation
```

Those results may justify stronger v0.3.1/v0.4 claims. They must not be retroactively represented as evidence already possessed by v0.3.0.

## 9. v0.3.0 claim ceiling

The release may claim:

- the Campaign persistence/lifecycle machinery is mechanically qualified;
- the installed distribution can execute its deterministic Campaign control surfaces without a Sensemaking source checkout;
- artifact admission preserves canonical validator provenance;
- authored decision, capability inspection, lineage, reconciliation, handoff, and resume contracts are mechanically qualified;
- P10 provides deterministic installation adapters for declared coding-agent discovery roots.

The release must **not** claim:

- universal real-harness Skill discovery;
- universal external-repository end-to-end success;
- automatic capability choice;
- automatic semantic next action;
- semantic truth from validator success;
- guaranteed fresh-agent reasoning quality.

## 10. Explicit non-goals for v0.3

Do not build unless later product pressure warrants it:

- centralized semantic router;
- HTN/generic planner;
- Skill ranking algorithm;
- critic/voting swarm;
- self-modifying Skills;
- autonomous SkillOpt loop;
- Campaign server/database/cloud service;
- generic semantic truth validator;
- automatic external mutation authority;
- full multi-repository Campaign engine.

## 11. Research and experiment disposition

Research remains a laboratory/historical evidence surface rather than the default product-development queue.

EXP-0006 remains stopped at its actual completed boundary under the owner productization pivot. Preserve its diagnostic attempts, frozen holdout identity/integrity record, contamination audit, and claim ceilings. Do not manufacture a Skill candidate merely to complete an experiment mechanism.

The stronger external golden-path runtime protocol is preserved as optional post-release dogfood, not release authority.

## 12. Definition of v0.3.0 done

The first Campaign-based release is ready when the **installed distribution** mechanically demonstrates:

```text
version + packaging consistency
→ wheel + sdist build
→ metadata checks
→ fresh wheel install
→ self-contained artifact admission
→ Campaign lifecycle contracts
→ explicit agent-authored decision persistence
→ capability inspection contract
→ reconciliation reconstruction
→ exact evidence lineage
→ integrity-bound handoff
→ fresh-process resume
→ honest terminal representation
```

with the full exact-head Validator Ecosystem green and without requiring a Sensemaking source checkout for the supported installed control surface.

A real external-repository / real-harness golden-path run is useful post-release dogfood, **not a v0.3.0 blocking gate**.
