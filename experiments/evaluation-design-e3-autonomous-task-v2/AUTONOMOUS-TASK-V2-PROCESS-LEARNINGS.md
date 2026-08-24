# Autonomous Task v2 — Process Learnings

Status: RETROSPECTIVE / NON-NORMATIVE

## Purpose

This document records process-level lessons discovered while taking
Autonomous Task v2 from design review through pilot-lock and pilot-harness
qualification. It does not modify the frozen experiment. It extracts the
*class* of failure each incident represents, not a per-incident account — the
incident-specific chronology lives in the construction/lock artifacts and is
left unchanged.

It is intentionally non-normative: it changes no scope, no frozen task/oracle/
regime/manifest/seed, and no authority decision. See
`docs/experimental-phase-gates.md` for the reusable, methodology-general
version of these lessons.

## 1. Phase readiness is layered

Passing one readiness state does not imply the next. Discovery order across
this study:

```
DESIGN_READY
  → LOCK_READY
  → PILOT_LOCKED
  → HARNESS_READY
  → PILOT_VALID
  → MAIN_STUDY_AUTHORIZED
```

`PILOT_LOCKED` was reached and mechanically verified (hashes matched, preflight
clean), yet the next step — executing the pilot — hit a hard stop because the
execution harness could not expose the instrument's required telemetry. The
transition from "the design is frozen" to "the runtime can instantiate the
frozen instrument" is its own gate (`HARNESS_READY`), and it was not passed.

## 2. Phase boundaries require explicit handoff artifacts

Many consequential defects appeared *between* phases, not inside any single
artifact:

- review → handoff: the package-level `READY FOR PILOT LOCK` verdict lived
  only in conversational state and was not persisted into the handoff artifact
  (provenance ambiguity for a fresh executor).
- protocol → candidate: assumptions in the protocol did not hold against real
  repository source until instantiated.
- candidate → oracle: candidate-specific semantic gaps surfaced at authoring.
- test → hash: a nondeterministic pytest elapsed-time suffix made the oracle
  self-test output hash non-reproducible.
- lock → dispatch: a frozen seed existed without a fully specified seed→shuffle
  implementation (a post-lock researcher degree of freedom).
- experiment → runtime: the design required telemetry the selected runtime
  interface did not expose.

The weakest boundary is not a component; it is the *contract between
components*. Handoffs must be closed by explicit artifacts that preserve every
decision-relevant fact.

## 3. Preserve admissible negative outcomes

Legitimate negatives were preserved as first-class outputs rather than
"fixed":

```
NO ADMISSIBLE TASK C
NOT_ESTABLISHED_WITHIN_BUDGET
NON_TRANSFER
T3 may be dropped
NO_BEHAVIORAL_UPTAKE
PILOT_HARNESS_READY = NO
```

If success is the only allowable outcome, agents optimize toward looking
successful. If admissible negative outcomes exist, agents can instead optimize
toward discovering what is true. The pilot executor stopped before firing nine
cells because doing so could not meet the frozen measurement contract — exactly
the behavior admissible negatives are meant to elicit.

## 4. Freeze all decision-relevant degrees of freedom

A commitment that leaves a decision-relevant parameter unspecified is
incomplete. The clearest instance: the three dispatch seeds were frozen, but
`seeded_fisher_yates` was not pinned to a concrete implementation (RNG family,
seeding convention, shuffle algorithm, input ordering). Two different
reasonable implementations can produce different dispatch orders from the same
seed. Freezing the seed while leaving the seed→shuffle mapping open preserves a
post-lock researcher degree of freedom.

**Post-lock ambiguity rule:** if a frozen instruction admits multiple
reasonable implementations that can change experimental behavior, do not choose
one silently. If no evidence-bearing run has occurred, resolve it through a
transparent pre-dispatch addendum that preserves all previously frozen
experimental choices. After evidence exists, treat the ambiguity as an
instrument-validity problem rather than retroactively repairing the experiment.

## 5. Integrity checks and semantic checks are different

Hashes and byte-equality checks establish *identity and immutability*. They do
not establish that an artifact is *correct* or that it means what its author
intended. Examples from this study:

- A manifest hash matching tells you the candidate set is unchanged, not that a
  candidate is semantically sound.
- The automated `test_field_contract_agreement.py` guardrail unions declared
  fields across *all* artifacts, so it cannot, by itself, prove a field was
  declared on the *correct* artifact — a structural test is insufficient for an
  attribution claim.
- The byte-identical R1/R2 shared block is a mechanical fact; whether R1 and R2
  are behaviorally distinguishable is a separate, empirical question.

Independent semantic review is required even when all mechanistic checks pass.

## 6. Construction is itself an empirical stress test

Authoring real candidates against real repository behavior surfaced defects
that prose review had not: a `proposed_direction` bootstrap deadlock, a missing
git-commit precondition, a false claim that a run log is a distinct new file
(it is overwritten in place), and candidate/oracle semantic gaps. A protocol
can be internally coherent and still fail when instantiated. Instantiation is a
first-class verification activity, not a paperwork step.

## 7. Execution and measurement capability are different

Being able to spawn an agent does not mean the experiment can measure what it
preregistered. The current sub-agent mechanism can execute task work in a fresh
clone, but it does not expose model-call/token/tool telemetry from the first
model call, and (for R2) there is no built-in oracle-blind human responder with
active-human timing capture. Therefore the frozen `TELEMETRY-SCHEMA` fields
required for `PILOT_INSTRUMENT_VALID` cannot be populated, and no valid
adjudication can be produced through that path. This is a harness
qualification problem, not a task-family or design failure.

Three independent readiness questions must each be answered, separately:

```
Can the runtime perform the task?
Can the runtime enforce the experimental treatment?
Can the runtime observe every measurement required for adjudication?
```

## 8. Calibration must be non-evidentiary

Harness/runner testing should never consume one of the actual frozen pilot
cells. A non-evidentiary calibration task (deliberately not any T1/T2/T3 ×
R0/R1/R2 cell, never eligible to enter the evidence set) exercises the full
machinery: fresh clone → fresh agent → regime-like test prompt → telemetry from
first model call → tools → final repo state → evaluator → telemetry record →
teardown. Proving required-telemetry population, agent/evaluator separation,
fresh state, no ambient leakage, and R2 transport calibration is what should
gate `HARNESS_READY`.

## 9. Diminishing-return rule for review

Review within a single layer while new findings can still materially change:
validity, selection, scoring, execution, or interpretation. When remaining
findings are primarily editorial or non-decision-changing, exercise the next
layer instead of adding another prose review.

Justification is required before adding a check: **What concrete false
conclusion could pass without this check?** If that question cannot be
answered, do not add the check. This is a natural anti-bureaucracy mechanism
against rigor becoming an attractor.

## 10. Process-not-person principle: mistakes are probes

Treat errors — human or agent — as evidence about missing safeguards, ambiguous
contracts, or insufficient observability. Blaming an individual does not
prevent recurrence; fixing the process condition that let the error become
consequential does.

```
mistake
  → independent boundary detects it
  → damage bounded
  → cause inspectable
  → process improves
```

If one careful agent makes a mistake, it may be idiosyncratic. If multiple
competent agents can plausibly make it, it is almost certainly a
process/interface problem. Human or agent mistakes are probes for places where
the system still depends on exceptional attention. The objective is not zero
mistakes; it is that a mistake never silently propagates to an authoritative
result.

## Overarching lesson

A trustworthy process does not require humans or agents to stop making
mistakes. It makes consequential assumptions explicit, gives independent
mechanisms permission to contradict earlier work, keeps failures bounded,
preserves legitimate negative outcomes, and moves from review to execution once
further review stops changing decisions. When an error occurs, treat it as
evidence about the process boundary that allowed it to matter.
