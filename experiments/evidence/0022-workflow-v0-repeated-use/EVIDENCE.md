# Evidence 0022 — Workflow v0 repeated-use dogfood: Auteur + Sensemaking Skills (second independent run)

## Purpose

Repeated-use dogfood of Sensemaking Agent-Native Operating Workflow v0 on
the same two repositories at their current HEADs, with fresh independent
sensemaking FIRST and historical comparison ONLY after both Briefs were
frozen. Goal: accumulate repeated-use evidence for a future v1 decision.
No Workflow-v0 / Skill / contract / validator / architecture changes were
made. Nothing was implemented.

## Pinned revisions

| Repository | Branch | HEAD | Notes |
|---|---|---|---|
| Auteur | main | `414435b9` | release-evidence producer + evidence now in committed history |
| Sensemaking Skills | main | `a6239630` | supplies `repo-sensemaker` SKILL.md + Workflow v0 (docs/agent-native-operating-workflow.md); CONTEXT.md repair in HEAD |

Working-tree state preserved, not normalized: Auteur has untracked tooling
dirs + modified .claude/settings.json; Sensemaking has pre-existing
egg-info/settings modifications and untracked auteur dogfood artifacts +
untracked evidence 0016 (all predate this run).

## Fresh runs (frozen before comparison)

### Auteur (intent: most consequential boundary for the next meaningful decision)

- **Current consequential boundary:** partial, diverging **vendored copy of
  Sensemaking Skills** inside the Auteur tree. Demonstrated: 25 skill dirs
  incl. vendored repo-sensemaker/problem-framer/sensemaking-docs-reconciler/
  skill-maintainer/to-issues/to-prd/triage; vendored validator stack
  (scripts/validate-*.py, workflow-execution-engine.py,
  orchestration-runner.py, router.py); no workflow-planner or
  artifact-contracts.yaml at the vendored path; scripts/validate-repo.py
  diverges from the current framework; and `python scripts/check.py
  --skip-pytest` reports the vendored validator warning about recursive
  workflows (fast-path-workflow, full-fog-workflow -> workflow-orchestrator)
  and unregistered artifacts (ui_flows, screen_specs) in
  ui-implementation-workflow, while still printing "Validation passed!".
- Weakness type: Contract Mismatch. uncertainty.source:
  repository_evidence (vendor contract not found in scanned surface) +
  owner_intent (is the divergence acceptable?).
- Recommended next responsibility: owner decision on vendoring posture
  (document the vendoring contract / pinned version, or de-vendor/align) —
  not implemented.
- Validator: validate-artifact.py + validate-brief.py PASS (non-blocking
  warnings only).
- Prior finding classification: release-evidence provenance —
  **CLOSED** (producer defect; green candidate-addressed evidence at
  309a473) with production adoption **NARROWED** (no real release has used
  `check.py --qualify` yet; recorded checklist preserved at 414435b9);
  top boundary **SUPERSEDED** by the vendored-divergence finding.

### Sensemaking Skills (intent: most consequential boundary for the product's next decision)

- **Current consequential boundary:** residual documentation-currency
  drift on the retirement-deferred subset + roadmap. Demonstrated:
  roadmap.md "Current Version: 0.2.1 (Beta)" / "Phase 2.3 Complete" vs
  STATUS.md v0.2.2 (2026-08-10); four runner-era docs explicitly deferred
  by the retirement reconciliation and never verified
  (ROUTING_GUIDE, run-ledger-guide, PORTFOLIO_OPERATIONS,
  PRODUCT-CONTRACT-REVIEW; retirement plan:133-135). The main CONTEXT.md
  drift is CLOSED (evidence 0021).
- Weakness type: Vocabulary Drift. uncertainty.source: owner_intent
  (v1 scope of the retained-but-unratified routing surface, ADR 0014/0018).
- Recommended next responsibility: bounded docs reconciliation of the
  deferred subset + roadmap alignment (sensemaking-docs-reconciler),
  separate from the owner's v1-scope decision — not implemented.
- Validator: validate-artifact.py PASS (warnings), validate-brief.py PASS.
- Prior finding classification: CONTEXT.md runner-era framing —
  **CLOSED**; the docs-currency responsibility continues on a smaller
  surface — **NARROWED**.

## Phase 4 — Read-the-output audit (both Briefs)

- Both recovered decision-material evidence with file:line citations.
- Uncertainty.source correctly separated repository_evidence vs
  owner_intent in both.
- The Auteur Brief correctly did NOT re-anchor on the closed
  release-evidence defect (belief update: it surfaced the vendored
  divergence instead).
- The Sensemaking Brief correctly did not reopen cross-run identity or
  routing and did not treat watch items as active defects.
- Neither proposed implementation before mechanically knowable repository
  questions were exhausted; both stopped at the responsibility/owner
  boundary.

## Phase 5 — Prior-finding comparison

| Prior finding | Classification | Evidence |
|---|---|---|
| Auteur: release-evidence provenance defect | **CLOSED** (+ adoption NARROWED; top boundary SUPERSEDED) | producer in HEAD; green 309a473 artifact; no new release since v0.37.1 |
| Sensemaking: CONTEXT.md runner-era framing | **CLOSED** | a6239630 stale-claim scan empty; evidence 0021 CLOSED |
| Sensemaking: docs-currency responsibility | **NARROWED** | deferred docs + roadmap mismatches remain (this run) |

Changed diagnoses reflect repository evolution, not repo-sensemaker
regression: the framework correctly moved on from a closed problem.

## Phase 6 — Workflow-v0 repeated-use evidence

| Responsibility | What happened | Useful? | Ceremony? | Friction | Repeated? | Blocking? |
|---|---|---|---|---|---|---|
| ENTRY/TRIAGE | both runs triggered | yes | no | none | yes (prior runs) | no |
| repo-sensemaker | two fresh runs, both validated | yes | no | see friction F1 | yes | no |
| Brief semantic review | facts/interpretation/hypotheses separated | yes | no | none | yes | no |
| Responsibility selection | owner-decision + docs-reconciliation identified, no premature implementation | yes | no | none | yes | no |
| Validation | validators executed on fresh briefs | yes | no | see friction F1 | first | no |
| Comparison/stop | frozen-brief discipline held | yes | no | none | yes | no |
| Output reconciliation / repair verification | correctly skipped (no material claims/repairs) | yes | no | none | yes | no |

Friction log:

```text
F1  category: validator gap / documentation ambiguity
    observation: repo-sensemaker SKILL.md instructs "leave recommended_workflow_id
      blank with a note if no matching workflow exists", but validate-brief.py
      rejects '' (INVALID_ENUM_VALUE / HALLUCINATED_WORKFLOW_ID); the brief had to
      select the closest registry match (fast-path-workflow, plan_only) instead.
    occurrence: FIRST_OBSERVED (prior runs could not run validators; this run could)
    impact: NON_BLOCKING (closest-match selection was defensible)
    disposition: recorded only; watch for recurrence
```

Acceptable conventions (no change): skipping reconciliation/repair
verification without material claims; agent-mediated responsibility
selection; probe-less direct-read grounding this run.

## Phase 7 — Watch-item recurrence

- Output-reconciler non-claim classified DISPUTED: **NOT RECURRED** (no
  output-reconciler invocation was warranted this run).
- Candidate-vs-attempt artifact identity: **NOT TRIGGERED** (27c5282 and
  309a473 are distinct candidates; no overwrite/confusion observed).
- Cross-run prior-report identity: **REMAINS DEFERRED** (no real
  continuation failure).

## Phase 8 — Reality map (report-only)

Unchanged from evidence 0021 except: entry/sensemaking trigger, diagnosis,
brief validation, human review, responsibility selection, specialized
work, validation -> REAL/CONVENTION as before; repair verification ->
REAL (not triggered this run); promotion/durability -> REAL (this run
preserved evidence); continuation -> CONVENTION_CLOSED. No row promoted
CONVENTION -> MISSING; F1 not converted into machinery.

## Phase 9 — Workflow-v0 maturity verdict

```text
KEEP_WITH_WATCH_ITEMS
```

Evidence: the workflow again identified warranted responsibilities
correctly, updated its belief as repositories evolved (Auteur moved past a
closed defect; Sensemaking finding narrowed), skipped unnecessary stages,
and stopped at the owner boundary. One FIRST_OBSERVED, NON_BLOCKING
validator/documentation contradiction (F1) is added to the watch list;
no repeated or decision-blocking failure exists yet.

v1 implications: none yet. If F1 recurs on a future brief with no matching
workflow, it becomes a REVISE_CANDIDATE input with the smallest hypothesis:
align repo-sensemaker SKILL.md's "leave blank" guidance with
validate-brief.py's enum requirement (either permit empty-with-note or
change the guidance to closest-match).

## Durability

- Fresh briefs: auteur-repository-sensemaking-brief.md,
  sensemaking-repository-sensemaking-brief.md (this directory), both
  validator-PASSED.
- This record pins every result to revisions above. Prior records
  (evidence 0021, Auteur reconciliation reports) were not rewritten.
- Sensemaking revision supplying repo-sensemaker + Workflow v0: `a6239630`.
