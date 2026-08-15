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

## Addendum — consolidated state (2026-08-14, after review + Auteur vendoring continuation)

### Workflow v0 status

```text
design/documentation                 DONE
first cross-repo dogfood             DONE
deep real engineering dogfood        DONE
repeated-use dogfood                 DONE

current phase:   ongoing normal-use validation
verdict:         KEEP_WITH_WATCH_ITEMS (supported by repeated use, not
                 merely provisional first-use evidence)
v1:              NOT STARTED; specific revision candidates now exist
```

### Auteur vendoring continuation: UNSPECIFIED_VENDORING_CONTRACT -> owner decision now earned

The fresh-run stop was corrected by the workflow itself: the vendoring
*intent* was a mechanically knowable question, so the next responsibility
was targeted repository-evidence acquisition, not owner decision. That
acquisition established (all demonstrated, 2026-08-14):

- old, partial framework snapshot (legacy `skills/workflow-orchestrator/`
  layout; vendored repo-sensemaker predates the probe engine / Interact /
  ADR 0024);
- wired into Auteur's actual validation gate (`check.py` runs the vendored
  test-validators.py + validate-repo.py);
- no sync mechanism for this copy (sync_interface_skills.py targets a
  different source -> .agents/skills);
- no provenance/pinning in the scanned sources of truth (README, CONTEXT.md,
  CLAUDE.md, AGENTS.md);
- not dead vendoring (the gate depends on it).

Owner decision scope (narrow, not "fix vendoring"):

```text
A. Auteur intentionally vendors a curated Sensemaking snapshot
   -> document provenance, define supported subset, pin source revision,
      decide update mechanism
B. Auteur should consume current Sensemaking another way
   -> de-vendor / replace snapshot, update the gate accordingly
```

### F1 — Sensemaking machinery revision candidate (NOT a Workflow-v1 item)

```text
F1: repo-sensemaker / brief-validator contract contradiction
  Skill contract:    no matching workflow -> blank recommended_workflow_id valid
  validator contract: blank recommended_workflow_id -> invalid
  consequence:       agent fabricated the nearest valid workflow id to obtain
                     structural PASS (structural correctness up, semantic
                     truthfulness down - the wrong trade)

evidence status: DEMONSTRATED
recurrence required? NO (a direct normative-instruction vs deterministic-
                     validator disagreement is objectively reproducible)
impact: truthfulness-affecting; NON_BLOCKING in this campaign
bucket:  Sensemaking machinery repair (repo-sensemaker instructions <-> artifact
         schema/validator alignment), NOT Workflow-v1. Workflow v0 only exposed it.
smallest fix candidate: align SKILL.md "leave blank" guidance with
         validate-brief.py's enum requirement (permit empty-with-note, or
         change guidance to closest-match). Not authorized in this campaign.
```

### Responsibility-selection jump — Workflow-v1 wording candidate

```text
occurrence: REPEATED (2 instances, identical shape)
  1. release evidence: diagnosis -> implementation (corrected to investigation)
  2. vendoring:        diagnosis -> owner decision (corrected to investigation)
  shape: "current evidence -> eventual solution class" chosen instead of
         "current evidence -> nearest decision-changing uncertainty ->
          next information-producing responsibility"

decision-blocking: no (workflow discipline corrected both)
candidate principle (wording refinement): select the next responsibility from
  the nearest unresolved decision-changing uncertainty, not from the likely
  eventual action or authority boundary

disposition: observe ONE more time in normal work before editing Workflow v0.
  Both corrections succeeded under the current conceptual model, so the next
  occurrence distinguishes "documentation insufficient" from "ordinary
  reasoning error the workflow already corrects".
third-occurrence trigger: agent identifies a consequential boundary ->
  unresolved repository/empirical uncertainty remains -> agent nevertheless
  jumps directly to implementation or owner decision.
```

### Reality map state (report-only; topology unchanged)

```text
REPOSITORY DIAGNOSIS        REAL     repeated-use evidence strengthened
UNCERTAINTY CLASSIFICATION  REAL     increasingly strong behavioral evidence
NEXT-RESPONSIBILITY SELECTION CONVENTION / agent reasoning; repeated jump pattern observed
MECHANICAL VALIDATION       REAL     useful; one contract contradiction demonstrated (F1)
OUTPUT RECONCILIATION       REAL     prior non-claim friction remains watch-only
REPAIR VERIFICATION         REAL     no new friction
CONTINUATION                CONVENTION_CLOSED   no reopen trigger
AUTOMATIC ROUTING           UNRATIFIED / deferred
V1 MACHINERY                MISSING? NO   (revision candidates exist; no new component earned)
```

### Three separated future-work buckets

```text
A. Auteur product decision     vendored Sensemaking contract -> owner chooses posture
                               (active repository problem)
B. Sensemaking contract repair F1 no-workflow guidance <-> validator enum contradiction
                               (tiny bounded fix, separately authorized)
C. Possible Workflow-v1 learn  responsibility-selection jump pattern
                               (needs one more real-use observation before editing the guide)

Auteur product issue != Sensemaking contract bug != Workflow-v1 learning.
```

### Verdict

```text
Workflow v0: KEEP_WITH_WATCH_ITEMS; continue normal use; accumulate evidence;
             no v1 work yet. The workflow is no longer justified by its design;
             it is accumulating a behavioral track record.
```

## F1 closure (2026-08-14) — bounded contract repair, CLOSED

Owner decision (per review): under the accepted ADR 0014 product boundary,
"no supported workflow recommendation" is a valid Repository Sensemaking
Brief state; a deterministic validator must not require the Brief to name a
workflow unsupported by repository evidence. ADR 0018 remains PROPOSED;
this decision does not ratify routing.

Representation (smallest compatible): `recommended_workflow_id: null`
together with `escalation_recommended: true` = truthful no-match. Null was
chosen because validate-artifact's generic enum check already tolerates
None (no canonical-vocabulary change needed). A null value without
escalation is a contract violation at any artifact size; non-null values
must always be valid registry ids.

Repair (committed separately):
- scripts/validate-brief.py: no-match gating in both workflow-id checks +
  strict `_bool_flag` (quoted "false"/"no"/"0" cannot enable the gate) +
  null-without-escalation check independent of the large-artifact exemption
  (two gate-bypass flaws found by security review, fixed).
- skills/repo-sensemaker/SKILL.md:151: "set escalation_recommended: true
  and emit recommended_workflow_id: null; do not fabricate a closest
  structural match" replaces the non-executable "leave it blank" option;
  skeleton section aligned.
- skills/workflow-planner/references/artifact-contracts.yaml: no-match
  semantics note on repository_sensemaking_brief.
- Validator-harness fixtures: valid/no-match-with-escalation.md (positive),
  invalid/no-match-without-escalation.md and
  invalid/no-match-with-string-false-escalation.md (negative).

Validation: validator harness 77/77 PASS; scripts/validate-repo.py PASS;
tests/test_field_contract_agreement.py 3 passed; focused checks confirmed
truthful no-match PASSES, null-without-escalation FAILS at any size
(verified with a 169-line brief), quoted "false" FAILS; security review
verdict: ship (both bypasses fixed).

Work claim (F1):
- implemented: validate-brief no-match gating; SKILL.md + contract notes;
  3 fixtures.
- mechanically demonstrated: truthful no-match validates; fabrication no
  longer required or instructed; string-"false" and large-artifact bypasses
  closed.
- still interpretive: the null representation (chosen as smallest
  compatible); ADR 0018 semantics remain a separate PROPOSED question.
- deliberately unchanged: routing machinery, canonical vocabulary,
  validate-artifact, ADR 0018, Workflow v0.

Reconciliation: all claims VERIFIED against the artifact/validator behavior;
no omitted or disputed claims. The truthfulness problem F1 exposed
(validator PASS obtained by fabricating the nearest workflow id) is gone:
both contracts now agree no-match = null + escalation.

Repair verification (finding-specific):
- acquisition_status: SUCCEEDED
- observation: a brief with `recommended_workflow_id: null` +
  `escalation_recommended: true` now validates truthfully; the SKILL no
  longer instructs "closest structural match or leave blank"; the validator
  rejects null-without-escalation and non-null hallucinated ids.
- disposition: CLOSED (contract contradiction resolved; fabrication neither
  required nor instructed).

Note: this run exercised the corrected responsibility-selection shape
(nearest unresolved uncertainty -> investigation -> earned action) after the
third-occurrence observation; the v1 wording candidate remains EARNED and
unimplemented.

## Auteur vendoring closure (2026-08-14) — bounded contract, CLOSED

Owner decision (2026-08-14): Auteur intentionally vendors a curated, pinned
subset of Sensemaking Skills. Implement a vendoring contract (source
revision, supported subset, exclusions, sync expectations) and make the
gate validate the supported subset; do NOT blindly upgrade the snapshot and
do NOT introduce an external dependency/distribution architecture.

Implementation (Auteur, committed ab1d6ee):
- skills/VENDORED.yaml — machine-readable contract: source revision
  recorded honestly as UNRECORDED (historical pre-workflow-planner
  snapshot); included subset (16 skills, 24 scripts, 2 framework docs,
  grounded in the vendored validate-repo.py's own expected core files);
  excluded current-era components (workflow-planner, probe engine files,
  brief_skeleton); known characteristics (the vendored validate-repo
  warnings, documented non-critical); manual+gated update policy (record
  upstream SHA at next sync); validation expectations.
- scripts/verify_vendored_contract.py — drift check (included present,
  excluded absent; exit 0/1/2; repo-relative path validation;
  malformed-YAML handled), wired into scripts/check.py.
- tests/test_vendored_contract.py — 7 focused tests.

Validation: drift check "VENDORED CONTRACT: OK" against the real tree;
drift cases unit-tested (missing included -> fail, excluded present ->
fail); check.py --skip-pytest green (26/26 validators, validate-repo PASS
with the documented warnings, drift check OK, ruff clean); focused tests
7/7; security review no blocking issues (2 LOW hardening items fixed).

Work claim + reconciliation: recorded in
Auteur docs/reviews/2026-08-14-vendoring-contract-reconciliation.md
(committed 7b09b3b); all claims VERIFIED (contract exists and matches the
tree; gate validates the subset; no upgrade; no external dependency;
warnings documented); "upstream revision pinned" DISPUTED-by-design
(UNRECORDED until the next intentional update).

Repair verification (finding-specific, evidence 0022 Auteur brief):
- acquisition_status: SUCCEEDED
- observation: the hidden, ungoverned vendoring relationship is now
  explicit and machine-enforced (contract + drift check in the gate);
  included verified present, excluded verified absent.
- disposition: closed (the "no vendoring contract / hidden dependency"
  defect is resolved; snapshot content intentionally unchanged per the
  owner decision, so no content-upgrade claim is made).

Both Bucket B (F1) and Bucket A (Auteur vendoring) are now CLOSED.
Bucket C (responsibility-selection wording) remains an EARNED, unimplemented
Workflow-v1 candidate.
