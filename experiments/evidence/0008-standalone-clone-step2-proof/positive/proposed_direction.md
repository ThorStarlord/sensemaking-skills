# Proposed Direction

---
artifact_id: proposed_direction
created_at: '2026-07-25T22:00:00+00:00'
created_by: standalone-clone-step2-proof
---

## summary

The brief identifies the weakest boundary as **unproven multi-phase
orchestration**: Phase 1 (diagnosis) and Phase 2 (routing) are empirically
proven with real agents, but no end-to-end run has exercised a full
implementation workflow (multi-step execute -> validate -> bounded retry ->
escalate -> final artifact) with a real agent. Individual pieces exist and
have unit tests, but the integration/safety boundary between "routing
recommends a workflow" and "a real agent completes that workflow" has not
been walked start-to-finish.

## proposed_response

Rather than building or hardening a fifth implementation workflow (which
would only add another untested surface), prove the existing chain first,
narrowly: pick the smallest already-implemented multi-step workflow
(architectural-review-planning-workflow, which is only two steps: diagnose,
then recommend) and run it end-to-end with a real agent, including a
deliberate negative-path run (missing required artifact) to prove error
handling is not just theoretical.

Concretely:
1. Use a real, previously-approved Step 1 artifact (repository_sensemaking_brief
   with an APPROVED gate) as prewritten resume state, so Step 2
   (architectural-review) is exercised in isolation without re-invoking
   repo-sensemaker.
2. Run the positive case: supply a valid `proposed_direction.md` and confirm
   the runtime resumes past Step 1, invokes architectural-review exactly
   once, and produces a recommendation that passes
   `validate-architectural-review-recommendation.py`.
3. Run the negative case: omit `proposed_direction.md` and confirm the
   runtime reports `ARTIFACT_NOT_FOUND` before invoking architectural-review
   at all, rather than invoking it and failing later or silently
   proceeding.
4. Do this from a standalone clone with no framework write access (Read/
   Write/Glob/Grep only, no Bash/PowerShell for the live agent), so the proof
   cannot be contaminated by the live model reaching outside its session
   directory.

This directly narrows the "unproven multi-phase orchestration" boundary by
converting it from a documentation claim into a reproducible, evidenced run
with both a success path and a failure path, using the smallest available
real workflow rather than expanding scope to untested four-workflow
territory.

## success_criteria

- Step 1 is skipped via resume-state detection (not re-executed) — confirmed
  by an explicit stdout line and zero repo-sensemaker tool-call-trace
  entries in the positive run.
- Step 2 (architectural-review) is invoked exactly once in the positive run
  and produces a recommendation artifact at the runtime-authorized session
  path, using a single triple-backtick yaml fence.
- The recommendation passes
  `scripts/validate-architectural-review-recommendation.py` without manual
  repair.
- In the negative run, the missing `proposed_direction` is reported as
  `ARTIFACT_NOT_FOUND` before any architectural-review tool call appears in
  the trace (zero Step-2 invocations).
- The standalone clone's tracked-file manifest is unchanged outside the
  expected session/log/evidence paths in both runs.
