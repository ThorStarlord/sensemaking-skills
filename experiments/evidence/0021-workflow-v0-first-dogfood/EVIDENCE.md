# Evidence 0021 — Workflow v0 first dogfood: two independent repo-sensemaker runs

## Purpose

First real use of `docs/agent-native-operating-workflow.md` (Sensemaking
Agent-Native Operating Workflow v0) as the operating guide for the active
coding agent, executed as a two-repository dogfood campaign (2026-08-14):

- an independent `repo-sensemaker` pass on the external Auteur repository; and
- an independent `repo-sensemaker` pass on Sensemaking Skills itself.

Records what was exercised, what was blocked, what the two runs established,
the review corrections adopted afterward, and the current-HEAD recheck of the
Sensemaking finding. Verdict: **KEEP -- provisional**, based on two
independent repository-diagnosis runs.

## Pinned revisions (the finding states)

| Repository | HEAD analyzed | Probe record | Constraints during the run |
|---|---|---|---|
| Sensemaking Skills | `0ff2ea38` (main) | n/a (probe not re-run) | no-mutation / plan-mode: no writes, no bash, no validators |
| Auteur | `c968a747` (main) | 2026-08-11 @ `fbabcb6` (`integration-run-auteur.yaml`) | same constraints |

Neither repository was modified by the campaign. Working-tree state was
preserved as evidence, never normalized.

## Runs

### Auteur (external)

- Consequential boundary: **release-qualification evidence is hand-maintained
  in prose/commit history** (suite counts reconciled by hand across commits;
  28 pre-existing `narrative_realization` failures carried as `xfail`;
  acceptance-report HEAD corrections committed repeatedly) while the product
  promise is deterministic validation and atomic correctness. Weakness type:
  `Contract Mismatch`.
- Supporting (probe-dated 2026-08-11): `ce 2.19` (2392 untracked vs 1094
  tracked), fixtures coverage 0.73, churn concentrated in
  `src/auteur/author_decisions/`, duplicate ADR id 013 in the catalog.
- Next responsibility (reported to the Auteur owner, not taken): a
  deterministic release-qualification gate (CI-derived test counts / xfail
  ledger consumed as artifacts).

### Sensemaking Skills (self-pass, Auteur brief excluded from the diagnosis)

- Consequential boundary: **`CONTEXT.md` -- the agent first-read per
  `docs/agents/domain.md` -- still presents the retired runner-led
  auto-routing architecture as current**: `CONTEXT.md:249` ("Default mode:
  `yolo_execution`") contradicts the committed post-retirement default
  `plan_only`; `CONTEXT.md:201-226` (Fog Type-Aware Auto-Invocation,
  UI-Specific Routing, "chains ... without manual intervention") describes
  routing deferred as unratified by ADR 0014 (ADR 0018 PROPOSED). Weakness
  type: `Vocabulary Drift`.
- Next responsibility (not taken; campaign forbidden from repairing):
  docs-contract reconciliation of `CONTEXT.md`
  (`sensemaking-docs-reconciler` / `docs-contract-reconciliation`).

## Validation status

```text
mechanical validation:     NOT EXECUTED (plan-mode / no-mutation turn; the
                           deterministic validator stack was not runnable)

manual contract inspection: SUPPORTING CHECK ONLY
```

Manual field inspection establishes that an artifact *appears*
contract-conformant; it is **not** an equivalent substitute for the
deterministic validator. Workflow v0 separates mechanical verification from
semantic judgment, and that distinction is preserved here.

## Observational limitations (retained; neither earns new machinery yet)

1. **Probe freshness**: measured claims age. The Auteur brief's sprawl and
   coverage figures are pinned to the 2026-08-11 probe, not re-verified at
   `c968a747`. A freshness/expiry label for probe-dated claims is a candidate
   convention, not a built feature.
2. **Environment-dependent mechanical validation**: the VALIDATION stage
   presumes an executable validator stack; read-only/plan-mode runs cannot
   satisfy it. By-inspection fallback worked but is supporting-only.

## Review corrections adopted

- "validators not runnable ... legitimate fallback" is weakened to
  "mechanical validation NOT EXECUTED; manual contract inspection SUPPORTING
  CHECK ONLY".
- "genuinely missing responsibility: NONE" is weakened to: **no missing
  responsibility was demonstrated by the stages actually exercised** (durability
  blocked, downstream reconciliation not triggered, repair verification not
  triggered, continuation not exercised -- those stages cannot falsify a
  missing responsibility they never ran).
- Workflow-v0 verdict is recorded as **KEEP -- provisional, based on two
  independent repository-diagnosis runs**, not as broad validation.

## What was NOT exercised

```text
ENTRY/TRIAGE                exercised
repo-sensemaker             exercised
Brief semantic review       exercised
responsibility selection    exercised
authority/stop discipline   exercised

deterministic validation    blocked (environment)
specialized downstream work not triggered
output reconciliation       not triggered
repair verification         not triggered
promotion/durability        blocked (environment)
continuation                not exercised
```

Workflow v0 passed its first **partial vertical slice**. Later stages remain
untested by real use; a future dogfood should pick a task that naturally
proceeds sensemaking -> selected responsibility -> bounded work -> validation
-> material work claim -> output reconciliation (and possibly repair
verification -> durability).

## Current-HEAD recheck of the Sensemaking finding (2026-08-14)

The campaign pinned the Sensemaking finding to `0ff2ea38`. Before any repair,
the finding was re-checked at current HEAD:

- `git rev-parse HEAD` = `0ff2ea38` (unchanged since the campaign; no new
  commits, CONTEXT.md has no uncommitted edits).
- Committed `CONTEXT.md` still contains: line 249 "**Default mode:
  `yolo_execution`**"; line 226 "Auto-invocation mechanism: ... chains to it
  without manual intervention"; lines 208/218 "Fog Type-Aware Auto-Invocation
  (Phase 7)" / "UI-Specific Routing (NEW)".

**Verdict: STILL STALE at current HEAD.** The finding is verified current, so
docs-contract-reconciliation of `CONTEXT.md` is earned. The repair was NOT
executed here -- repair remains an owner-authorized follow-up.

## Workflow-v0 verdict

```text
KEEP -- provisional, based on two independent repository-diagnosis runs
```

The two runs produced materially different boundary types (release-evidence
integrity vs documentation/architecture drift), did not force the
repositories into one template, and did not turn findings into implementation
work. Output-reconciler and repair-verifier were correctly not triggered
(diagnoses, not completion claims or repairs) -- evidence against workflow
ceremony, not for it.

## Exactly one next decision

Owner decision: **authorize the narrow docs-contract reconciliation of
`CONTEXT.md`** (the identified lines: yolo-default claim, auto-invocation and
routing framing, runner-era domain language) against the ratified agent-native
architecture (ADR 0013/0014; `plan_only` default), using the existing
`sensemaking-docs-reconciler` responsibility; after it lands, mark this
finding CLOSED. If the owner prefers no docs work this round, the finding
stands as verified-current and the next real engineering task should instead
exercise a deeper portion of Workflow v0 (material work -> validation ->
output reconciliation).

## Remediation (2026-08-14) — CLOSED

Authorized narrow docs-contract reconciliation executed. The record above is
the pre-repair evidence (committed unchanged as `69802c2`; finding pinned to
`0ff2ea38`).

Guardrail 1 — legacy mechanisms mechanically verified at HEAD before being
described as retained compatibility behavior:
- `auto_invoke_next_workflow` / `auto_invoke_source` present in
  `skills/workflow-planner/references/workflow-registry.yaml` (L38-39, 93-94,
  495-497, 816-818);
- `workflow-runtime.py` `_should_auto_invoke_next()` (L1099),
  `_validate_workflow_fog_alignment()` (L1256), auto-invoke execution path
  (L2685-2709);
- workflow ids `ui-implementation-workflow`, `product-implementation-workflow`,
  `docs-implementation-workflow`, `implementation-workflow`,
  `ui-diagnostic-workflow` all present in the registry.
=> "retained as CLI compatibility path" wording is mechanically justified, not
a new ghost feature.

Guardrail 2 — UI fog diagnosis labeled "current diagnosis behavior", not
"ratified"; the repair's normative distinction (diagnosing `ui_fog` !=
routing to `ui-implementation-workflow`) is stated.

Patch applied (CONTEXT.md):
- E1: "Fog-Type Routing (DEFERRED, not ratified)" replaces "Fog Type-Aware
  Auto-Invocation (Phase 7)";
- E2: "UI Fog Detection (current diagnosis behavior)" replaces "UI-Specific
  Routing (NEW)";
- E3: auto-invocation reframed as "legacy compatibility path only";
- E4: default execution mode corrected `yolo_execution` -> `plan_only`;
- E5: YOLO Execution re-labeled opt-in, not default;
- E6: Fog Type Classification now "informs next-responsibility selection";
- E7: Dynamic Chaining labeled legacy runtime mechanism.

Validation:
- `python scripts/validate-repo.py`: PASS;
- `python -m pytest tests/test_field_contract_agreement.py`: 3 passed;
- `git diff --check -- CONTEXT.md`: clean;
- stale-claim scan (Default mode `yolo_execution` / Fog Type-Aware
  Auto-Invocation / UI-Specific Routing / "chains ... without manual
  intervention" / "default execution mode when --mode is not specified" /
  "to enable routing"): zero matches.

Classification: **CLOSED** — all three demonstrated contradictions are gone at
current HEAD.

Deliberately not touched: the `full-local-sensemaking` DEFAULT entry (already
carries its legacy CLI-path caveat), routing-divergence/decision-method
domain entries (document legacy runtime-recorded fields that still exist in
contracts), the ADR 0005 bullet in Orchestration Principles (accepted
historical ADR, mechanism factually described), and all runtime/Skills/
workflows/contracts. No merge. No push.
