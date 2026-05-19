# Domain Alignment Report: Mode Coverage & Hardening Threshold

## Source
- **Session**: docs-aligner (autonomous)
- **Date**: 2026-05-16
- **Goal**: "Evolve sensemaking-skills into a pressure-tested automation system where each workflow mode is proven by live runs, and validation hardening is added only when real execution exposes a repeatable failure boundary."
- **Artifacts consumed**: CONTEXT.md, workflow-registry.yaml, skill-registry.yaml, artifact-contracts.yaml, run logs (guided + YOLO), Domain Alignment Report (previous), PRDs, validator ecosystem docs, execution-modes.md

---

## 1. Current Coverage: What Is Proven vs. Unproven

### Mode Coverage

| Mode | Workflow | Steps | Validators Exercised | Gates Exercised? | Run Log? |
|------|----------|-------|---------------------|-------------------|----------|
| `yolo_execution` | fast-local-diagnostic | 2/2 | Level 1 + Level 2 + Level 3 (brief + prompt-handoff) | No (bypassed) | ✅ Feature branch |
| `guided_execution` | docs-contract-reconciliation | 1/3 (paused at gate) | Level 2 only | No (never approved) | ✅ `runs/` |
| `plan_only` | — | 0 | None | N/A | ❌ None |
| `prompt_chain` | — | 0 | None | N/A | ❌ None |
| `autonomous_execution` | — | 0 | None | No (never attempted) | ❌ None |

### Validator Invocation in Live Runs

| Validator | Fixture Tests | Live (yolo) | Live (guided) | Live (other modes) |
|-----------|:------------:|:-----------:|:-------------:|:------------------:|
| `validate-repo.py` (L1) | Excluded | ✅ Pre-flight | ✅ Pre-flight | ❌ |
| `validate-artifact.py` (L2) | ✅ | ✅ Both steps | ✅ Step 1 | ❌ |
| `validate-brief.py` (L3) | ✅ | ✅ Step 1 (inc. TDD cycle) | ❌ | ❌ |
| `validate-plan.py` (L3) | ✅ | ❌ Never invoked | ❌ | ❌ |
| `validate-prompt-handoff.py` (L3) | ✅ | ✅ Step 2 | ❌ | ❌ |
| `validate-skill-improvement-plan.py` (L3) | ✅ | ❌ Never invoked | ❌ | ❌ |
| `validate-usage-research-report.py` (L3) | ✅ | ❌ Never invoked | ❌ | ❌ |

**Finding:** 3 of 5 Level 3 validators have never run in a live execution context. validate-plan.py has 7 negative fixtures but zero live invocations — its failure modes (hallucinated workflow IDs, missing section 11, approval gate mismatches) have never been tested against real artifacts.

### Gate Gap

**No approval gate has ever been exercised in any live run, in any mode.** Specifically:

- `yolo_execution` bypasses gates by design — recorded as `"N/A (bypassed by yolo_execution)"`
- `guided_execution` paused at `review_drift_diagnosis` before the gate was reached — the gate was never approved or denied
- `plan_only` / `prompt_chain` / `autonomous_execution` have no run logs

The entire gate system — approval prompts, `gate_result: approved_by_user` timestamps, gate_name validation against workflow-registry.yaml — is untested in practice.

---

## 2. Term Alignment: What Was Sharpened

### "Harden Only Where Pressured" → now qualified by "Repeatable Failure Boundary"

| Before | After | Why |
|--------|-------|-----|
| "restrict changes to boundaries the run actually stressed" | "restrict changes to boundaries where live execution exposes a **repeatable failure boundary** (same failure class across independent runs)" | Single-run pressure could be a data-quality fluke. Requiring repeatability prevents over-engineering for one-off issues. Isolated data issues are fixed in the artifact but do not trigger system hardening. |

### "Repeatable Failure Boundary" — new term

Defined as a failure class that recurs across independent live runs, signaling a systemic gap rather than an isolated data-quality issue. Distinguishes between:
- **Single occurrence** → artifact-level fix (correct the data, update CONTEXT.md)
- **Repeatable pattern** → systemic hardening (tooling, validators, contracts)

---

## 3. Gaps Between Goal and Current System

### Gap 1: 3 of 5 modes have zero run evidence

The goal requires "each workflow mode is proven by live runs." Current reality: 1 mode fully proven (yolo), 1 partially proven (guided, 33%), 3 unproven (0%).

**Obstacle to closing:** `plan_only` and `prompt_chain` are trivial to prove (no mutation, low risk). `autonomous_execution` requires opt-in and gate infrastructure that has never been exercised. The `skill-maintenance-loop` workflow only supports `guided_execution` — it cannot be used to prove any other mode.

### Gap 2: validate-plan.py has never run in a live execution

This validator enforces Section 11 (machine-readable plan), approval gate matching, disallowed modes, and subset-run semantics. But no orchestration plan has ever been produced in a live run:
- YOLO skips the plan artifact (executes directly per SKILL.md)
- Guided execution never completed Step 1, so no plan was produced

### Gap 3: Approval gates exist only in theory

The run-log template, SKILL.md, and workflow registry all define gates. But no run log documents:
- A gate approval event (`gate_result: approved_by_user`)
- A gate denial event
- A `gate_behavior: bypassed_by_yolo` field (the YOLO log uses `"N/A (bypassed by yolo_execution)"` instead)

### Gap 4: The "repeatable" threshold changes the hardening calculus

Under the single-run threshold, the first YOLO run's UNKNOWN_WEAKNESS_TYPE and NO_LOGIC_TRACE could theoretically trigger hardening (adding a weakness-type autocomplete, or a logic-trace template enforcement). Under the repeatable threshold, both are correctly classified as isolated data issues requiring artifact-level correction only. But this also means: if UNKNOWN_WEAKNESS_TYPE occurs again in the next run, it triggers systemic hardening — and we won't know until we run again.

---

## 4. Mode Proving Order (Recommended)

| Order | Mode | Workflow | Why This One | Risk |
|:-----:|------|----------|-------------|:----:|
| 1 | `plan_only` | fast-local-diagnostic | Already have the brief; plan_only produces Section 11 plan; exercises validate-plan.py live | None (no mutation) |
| 2 | `prompt_chain` | fast-local-diagnostic | Produces copy-paste prompts for handoff; exercises validate-prompt-handoff.py on chain output | None (no mutation) |
| 3 | `guided_execution` (full) | docs-contract-reconciliation | Already started (Step 1 done). Completing proves gates work end-to-end with human approval | Low (human gates) |
| 4 | `autonomous_execution` | fast-local-diagnostic | 2 steps, all-local, exercises gates with automated approval | Medium (requires opt-in) |
| 5 | `yolo_execution` (2nd workflow) | full-local-sensemaking | 4 steps (problem-framer → unknowns-mapper → repo-sensemaker → handoff). Exercises every core sensemaking skill | High (YOLO mutation) |

**Rationale:** Risk gradient from "no mutation" to "full mutation" ensures the validator ecosystem is proven at every level before the risk increases. Each mode proves a different safety mechanism: `plan_only` validates Section 11 production, `prompt_chain` validates prompt quality, `guided_execution` validates gate protocol, `autonomous_execution` validates opt-in gates, `yolo_execution` validates zero-tolerance post-step verification.

---

## 5. Hardening Decision

**No structural hardening is warranted at this point.**

The first YOLO run's failures (UNKNOWN_WEAKNESS_TYPE, NO_LOGIC_TRACE) were single-occurrence data issues — artifact-level corrections applied in the same run via the TDD Validator Cycle. Under the sharpened "repeatable failure boundary" principle, these do not trigger systemic hardening.

The current hardening candidates (in order of expected need):

| Candidate | Trigger Condition | Current Status |
|-----------|-----------------|----------------|
| Weakness-type autocomplete | UNKNOWN_WEAKNESS_TYPE in 2+ independent runs | Not triggered (1 occurrence) |
| Logic-trace template enforcement | NO_LOGIC_TRACE in 2+ independent runs | Not triggered (1 occurrence) |
| Gate-name validation against registry | Gate mismatch in any run | Not triggered (gates never exercised) |
| validate-plan.py live integration | Plan artifact produced and fails | Not triggered (no plan produced yet) |

---

## 6. CONTEXT.md Updates Applied

- Updated **Harden Only Where Pressured** — added "repeatable failure boundary" qualifier
- Added **Repeatable Failure Boundary** — new term distinguishing systemic vs. isolated failures

---

## 7. Status

- **Domain alignment**: Confirmed with sharpened terms. The existing system (modes, validators, gates, registries) accurately describes the intended behavior. The gap is in execution coverage, not design.
- **Hardening required**: None currently. First candidate would be RE-04 (weakness-type or logic-trace recurrence across runs).
- **CONTEXT.md**: Updated with validated and sharpened terms.
- **ADRs**: None warranted (term clarifications, no hard-to-reverse trade-offs).
