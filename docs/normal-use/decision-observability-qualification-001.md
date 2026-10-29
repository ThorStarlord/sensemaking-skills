# Decision Observability Qualification 001: preflight

**Status: NOT RUN.** Recorded 2026-10-29 before any evidence-bearing
qualification session. This is a qualification design and preflight finding,
not an assessment of the new mode's behavior. The capability under consideration
is integrated at `sensemaking-skills@c981047c033fdd98db7072b252f6465447e3a8b0`
(PRs #652-#654). The historical Operational Qualification 001 used an earlier
controller and did not test decision observability.

## Questions and comparison

Can authentic agent-native work expose checkable, contemporaneous selection
rationales and observable execution without forcing unnecessary specialist
invocations? Does the opt-in instruction appear to affect behavior? A rationale
is self-report, not direct evidence of internal causal computation. A matched
pair can reveal differences, not establish their cause or general superiority.

Before dispatch, pin the target source, complete Skill tree and host/model
configuration for every condition. Use fresh, mutually isolated sessions without
prior transcripts or supplied conclusions. Give the matched pair the same target,
source and task; vary only the transparency request. Capture actual command and
host events, decision text, final output, failure and termination status; preserve
chronology. An independent evaluator should compare claims with events and
sources where available, identify unsupported claims and report unknown causes.
Do not label manual instruction loads native invocations. Missing telemetry or
interruption is a limit, not a negative or positive product result.

## Proposed real missions (not dispatched)

- **Broad:** Give a fresh agent a real repository at a pinned revision and ask it
  to apply `using-sensemaking` to understand the domain and architecture, explore
  materially different futures, and recommend a warranted direction or explain
  why none is selected. Run a matched baseline and transparency condition on the
  same task and revision. The repository's actual sources, permissions, prior
  knowledge and retained artifacts must be fixed before either run.
- **Focused:** Ask a separate fresh agent a genuine, bounded architecture question
  for which current source and governing decisions plausibly suffice. Observe
  whether the audit justifies appropriate restraint and whether the outcome is
  source-grounded. Choose the exact question and target before any evidence run.
- **Cross-system (if feasible):** Ask about a real consequential direction with
  dependencies, alternatives and downstream effects. Observe specialist return
  and controller reassessment; do not require a predetermined set of calls.

Exact tasks, target snapshots and evaluator criteria remain **unlocked**. Before
consuming any evidence, choose and record them, including whether a comparison
session can access retained knowledge; specify the independence and isolation
limits and freeze all treatment-affecting differences. Do not change a condition
silently after observing a participant. This preflight does not claim the
experiment is preregistered, locked, harness-ready or complete.

## Evaluation questions

- **Decision transparency:** Is the specific rationale recorded before the
  action, linked to available evidence, uncertainty, relevant alternatives,
  expected contribution and a stop or revisit condition?
- **Execution fidelity:** Do native invocation, manual loading, failure, skip
  and `NOT_DOCUMENTED` classifications match observable host events?
- **Adaptive judgment:** Does the work meet its actual goal without premature
  stopping or obligatory specialist calls? Explain evaluator disagreements.
- **Product usefulness:** Did the output improve the substance of repository
  understanding or prospective reasoning, beyond generating more narrative?

Report failures separately where supported: responsibility recognition,
discovery, invocation, integration and judgment may overlap. A single host
failure does not establish that mechanical dispatch (A2) or runtime-directed
orchestration (B) is warranted. Do not infer a deliberate skip without a prior
record. No overall score or call-count quota substitutes for evidence.

## Observed preflight and stop

- `codex exec --help` on Codex CLI 0.153.4 exposes `--sandbox read-only`,
  `--ignore-user-config` and `--json`; command availability is not proof that
  all required host events, invocation mechanisms or independent evaluation
  are observable.
- The active Windows host's `gh auth status` reports an authenticated GitHub
  account with repository write scope. This is an ambient credential observation;
  the test did not reveal or copy the token. No evidence establishes that a
  proposed agent sandbox cannot reach the credential or make external writes.
  A filesystem read-only setting alone does not establish that boundary.
- WSL Ubuntu and docker-desktop could not start: the host reported that WSL2
  virtualization was not enabled (`HCS_E_HYPERV_NOT_INSTALLED`). No container
  isolation was established by those probes.
- Earlier local qualification reached a read-only filesystem calibration but
  later exhausted workspace credits. That historical calibration did not prove
  credential isolation for this new instrument and its interrupted sessions do
  not measure this new mode. Current account usage data is not proof that a new
  evaluation run will complete.

**Required before execution:** establish an environment with no GitHub write
credentials or publication authority reachable by participants, demonstrably
read-only target access, independent fresh session state, and sufficient event
telemetry. Run a non-evidentiary calibration against a throwaway task to verify
those properties, including denied writes and observable event types; ensure an
independent evaluator can access permitted evidence. If any prerequisite cannot
be shown, stop and record the limitation. Do not use the real missions for
calibration, relax isolation, or consume partial results as completed evidence.

## Refinement disposition

**NOT ASSESSED.** No new-mode behavioral session ran, so no observed deficiency
supports a targeted change or a `NO_CHANGE` conclusion about behavior. Once
admissible results exist, separate a failure of recognition, discovery,
invocation, integration or judgment and make only the correction warranted by
the evidence. Preserve Approach A unless a separate, evidence-backed product
decision changes that boundary.
