# Status

**Version:** 0.3.0  
**Last updated:** 2026-09-10  
**Current phase:** PM upstream source-methodology migration complete at repository qualification; Semantic Architecture Phase 10 complete with Outcome A; first bounded Phase 15 conformance rule qualified; engineering and PM empirical external qualification remain pending  
**Primary program:** Sensemaking Campaign productization with agent-agnostic domain capabilities and evidence-governed repository reasoning  
**Current implementation frontier:** Use Git `main` HEAD as exact repository identity; this status file intentionally does not self-pin a commit that becomes stale when the file itself changes  
**Current semantic frontier:** no broad semantic phase is automatically active; additional work requires an observed trigger  
**Current PM frontier:** Waves 1–6 are `REPOSITORY_QUALIFIED`; the pinned 27-command source migration is complete and the next PM frontier is native-harness/portability qualification plus evidence-derived product improvement

Sensemaking Skills is an **agent-native engineering sensemaking and control layer**. Its Campaign substrate supports agent-agnostic Product Management capabilities and an evidence-governed Semantic Architecture. The active coding agent owns semantic judgment; deterministic machinery owns mechanically decidable representation, persistence, validation, provenance, integrity, authority checks, target identity, evidence binding, conformance checks, and reconstructible state.

## Semantic Architecture state

The architecture has four explicit layers:

```text
Semantic Model
  = what entities, relations, and epistemic statuses mean

Reasoning Model
  = how observations become evidence, claims, uncertainty,
    responsibility, capability use, validation, and decisions

Capability / Skill Layer
  = bounded semantic work performed by repo-sensemaker,
    architectural-review, repair-verifier, output-reconciler,
    and domain Skills

Executable Substrate
  = mechanically decidable contracts, probes, validators,
    bounded conformance checks, Campaign persistence,
    provenance, and handoff
```

The formalization ladder remains:

```text
Level 1 — Vocabulary
Level 2 — Ontology
Level 3 — Executable semantic contract / bounded conformance rule
```

Level-1/2 concepts are not runtime authority. Level-3 behavior requires a demonstrated need, a mechanically expressible subset, rejection coverage, and preservation of the agent/deterministic authority boundary.

### Phase 9 — complete

PR #318 operationalized the Reasoning Model across contrasting engineering Skills. The stable shared core was:

```text
target/currentness
observations or inherited observations
material claims
epistemic status
evidence references
bounded scope / claim limits
decision-relevant uncertainty
explicit limits / non-claims
```

Skill-local vocabularies remain local rather than being flattened into a universal schema.

Phase 9 introduced the experimental `semantic_reasoning_profile` v1 representation validator. Its structured result preserves:

```text
semantic_truth_established: false
```

### Phase 10 — complete / Outcome A

PR #323 tested the companion profile in three additional real-repository episodes:

```text
Chess Mentor Engine
  repo-sensemaker / direct diagnosis

React incremental game
  output-reconciler / exact-SHA handoff + live PR currentness

ViralFactory
  PM pre-mortem / canonical risk_analysis + companion profile
```

The qualified decision is:

> Keep `semantic_reasoning_profile` v1 as an **optional companion audit/reconstruction artifact**.

The strongest positive signal was currentness-sensitive reconciliation: immutable exact-SHA evidence and independently mutable live PR metadata must not be silently collapsed into one current-state claim.

The strongest negative embedding signal was PM `risk_analysis`, which already represents the decision-changing evidence, uncertainty, mitigation, recommendation boundaries, and unresolved questions. Mandatory generic embedding would duplicate domain state.

Therefore:

- keep the profile optional;
- keep it outside Campaign artifact admission;
- do not create a universal analytical-artifact envelope;
- do not infer Campaign schema promotion, Repository Semantic Map work, or a central reasoning engine.

Exact Phase 10 candidate `89258bd77bc2d234f54e03264c68d3c6de7f6de5` passed Product Validation run `34469270069` and Release Candidate Distribution run `34469270281` before PR #323 merged as `22d249e34a39f75e8052de4d4d50d7aca44b3175`.

PR #324 reconciled the durable Phase 10 handoff and merged as `38255e400e6a968d29b0db35eb5fdff68b019a71` after exact-head Product Validation and Release Candidate Distribution passed.

### Phase 15 — first bounded liveness-conformance rule qualified

After Phase 10 closed, a trigger audit found no evidence warranting Phases 11–14, but it did find a repeated maintenance defect class: compatibility Skill-registry liveness prose had required manual reconciliation after canonical Skill implementations changed.

PR #325 therefore activated a **narrow Phase 15 pilot out of sequence**, based on observed maintenance pressure rather than phase numbering.

Qualified validator:

`scripts/validate-skill-registry-liveness.py`

It can reject only mechanically decidable contradictions such as:

```text
duplicate registry Skill IDs
status: proposed while skills/<id>/SKILL.md exists
explicit no-current-implementation note while that SKILL.md exists
wrong current-canonical skills/<id>/ reference
broken current-canonical skills/<id>/ reference
```

It explicitly permits historical `status: deprecated` metadata to coexist with a current canonical Skill when the note correctly distinguishes old invocation metadata from the live implementation.

The checker returns:

```text
semantic_truth_established: false
```

and does **not** establish Skill correctness, repository qualification, native-harness support, portability, promotion, or arbitrary documentation truth.

Exact candidate `1ff498b8fd57c85d590db249a43e8c17a13f5bda` passed Product Validation run `34470534713` and Release Candidate Distribution run `34470534631` before PR #325 merged as `d24e9bda18225bf7aa338df1decb5c201474a66e`.

Phase 15 is now:

```text
INCREMENTAL / TRIGGER-DRIVEN
one bounded liveness rule qualified
broad semantic linter not authorized
```

Any additional Phase 15 rule requires its own observed defect, bounded mechanical claim, rejection coverage, and exact-head qualification.

### Other semantic phases remain deferred

```text
Phase 11 — Mechanical Semantic Probes       DEFERRED pending repeated demand
Phase 12 — Repository Semantic Map          DEFERRED
Phase 13 — Campaign/control-plane promotion DEFERRED
Phase 14 — Domain-pack extraction           DEFERRED
```

The Phase 15 pilot does not change their evidence state.

## PM source-methodology migration — repository complete

All six planned PM waves are `REPOSITORY_QUALIFIED` against pinned upstream:

```text
lucasgaravelli/pm-skills-claude-code
21cbb2903d740d10fc65c667aea97d3ee8657349
```

### Wave 1 — Customer Discovery

`persona`, `discovery`, `interview-synthesis`, `opportunity-tree`, `hypothesis`.

### Wave 2 — Feature Definition — PR #313

`to-prd` (upstream `prd` methodology MERGED), `user-stories`, `acceptance-criteria`, `pre-mortem`.

Upstream `prd` does not become a duplicate execution authority.

### Wave 3 — Strategy & Prioritization — PR #316

`competitive-analysis`, `strategy`, `prioritize`, `north-star`, `okr`, `roadmap`, `lean-canvas`.

### Wave 4 — Experimentation / PMF / Pricing — PR #317

`experiment-design`, `ab-test-analysis`, `measure-pmf`, `pricing`.

### Wave 5 — Customer Modeling — PR #320

`customer-journey`, `ideal-customer-profile`.

### Wave 6 — Launch / GTM / Enablement / Communication — PR #321

`launch-checklist`, `gtm`, `battlecard`, `release-notes`, `stakeholder-update`.

The final PM source-migration handoff merged through PR #322.

For the pinned 27-command migration:

```text
source inventory reconciled: COMPLETE
agent-agnostic canonical adaptation: COMPLETE
artifact/validator integration: COMPLETE where mechanically warranted
Campaign capability registration: COMPLETE
repository qualification: COMPLETE
native-harness qualification: PENDING
portability qualification: PENDING
promotion: PENDING
```

There is no implied Wave 7.

## Empirical qualification gates remain open

### Engineering v0.3 external golden path

```text
Checked-in real-harness attempts: 0
Current empirical PASS: NONE
Human/external action required for empirical PASS: YES
```

A real PASS requires an actual supported external coding-agent harness attempt frozen under the canonical external golden-path protocol. The **real-harness qualification verifier** can mechanically check a frozen attempt package; it cannot manufacture real-harness origin evidence.

### PM native-harness and portability qualification

```text
Checked-in non-qualifying PM preflights: 1
Checked-in real-harness functional PM attempts: 0
Checked-in second-harness portability attempts: 0
Current functional PM empirical PASS: NONE
Current PM portability empirical PASS: NONE
```

Repository-local validation, Campaign admission, wheel packaging, connector-side reasoning, and adapter parity do not substitute for real native-harness discovery/invocation.

The next PM qualification program should use the existing dogfood protocol through a real supported harness, prove fresh-context continuation from durable state, then repeat a bounded equivalent responsibility through a second harness before claiming portability or promotion.

## Release architecture continuity

- Campaign schema v2 remains the durable representation baseline.
- The shipped product/lab split remains intact.
- Product Validation owns shipped/installed-product claims; retained Lab Validation owns source-only research/lab claims.
- Release Candidate Distribution proves build/install/package identities on exact candidate heads.
- `semantic_reasoning_profile` remains outside Campaign artifact admission.
- the Skill-registry liveness checker is repository CI conformance, not Campaign state.
- tagging/publication of v0.3.0 remains an explicit owner decision.

## Product and semantic boundaries

```text
observation != interpretation
evidence != truth
support != proof
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
semantic profile valid != reasoning semantically correct
registry liveness valid != Skill semantically correct
canonical Skill tree exists != native harness observed or invoked Skill
companion reconstruction value != Campaign promotion warrant
Phase N complete != Phase N+1 authorized
one Phase 15 rule qualified != broad Phase 15 authorized
admitted evidence != warranted conclusion
repository changed != repair succeeded
document says X != X is current
immutable snapshot evidence != live mutable metadata
no search result != absence unless completeness is established
ontology term documented != runtime-enforced concept
repository qualified != native-harness qualified
native-harness qualified != portability qualified
portability qualified != promoted
checklist complete != launch authorization
GTM plan != campaign execution
release draft != publication
proposed owner != assignment
lineage != semantic warrant
handoff != semantic recommendation
```

The Campaign Controller is not a semantic router. The Reasoning Model is not a central semantic controller.

## Current next step

No broad semantic implementation package is automatically authorized.

Reconcile actual repository/product pressure. If no new trigger is demonstrated, **stop semantic formalization** rather than inventing Phase 11–15 work.

The strongest explicit unresolved evidence frontier is real native-harness qualification for the engineering and PM systems. That work requires actual harness-origin evidence and cannot be manufactured by repository CI or connector-only execution.

## Canonical sources

- `STATUS.md` — current cross-program state.
- `docs/semantic-architecture/README.md` — Semantic Architecture index.
- `docs/semantic-architecture/implementation-plan.md` — phase states and promotion gates.
- `docs/semantic-architecture/common-semantic-contract.md` — optional companion semantic profile contract.
- `docs/semantic-architecture/phase-10-handoff.md` — qualified Phase 10 result.
- `docs/semantic-architecture/phase-15/README.md` — bounded liveness-conformance pilot.
- `docs/semantic-architecture/phase-15-handoff.md` — Phase 15 pilot qualification evidence.
- `docs/product-management/capability-migration-matrix.md` — PM capability maturity ledger.
- `docs/product-management/milestone-handoff.md` — complete six-wave PM source migration handoff.
- `docs/product-management/dogfood/STATUS.md` — PM empirical qualification status.
- `qualification-evidence/STATUS.md` — engineering empirical external-qualification status.
- `docs/sensemaking-campaign.md` — canonical Campaign model.
- `.github/workflows/validation.yml` — Product Validation authority.
- `.github/workflows/release-candidate.yml` — Release Candidate Distribution authority.

When prose and checked-in executable validation disagree, executable behavior is authority for what the software currently enforces; semantic documentation remains authority for intended concept meaning unless superseded by a later ratified decision. Documentation should then be reconciled rather than used to hide the mismatch.
