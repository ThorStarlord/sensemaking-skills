# Agent Instructions

## Core rules

1. **Resolve uncertainty from the right source.** Do not guess. If repository
   evidence can answer the question, inspect it. If reality must be observed,
   use a bounded probe. Ask the owner when the uncertainty is genuinely about
   owner intent or cannot be resolved from authorized evidence.
2. **Select responsibility before solution.** Before implementing the apparent
   fix, identify the nearest unresolved uncertainty that could change the
   correct next action and choose the responsibility warranted by current
   evidence.
3. **Simplest warranted solution first.** Implement the simplest thing that
   satisfies the selected responsibility. Do not add abstractions or
   flexibility that were not earned by the task or evidence.
4. **Don't touch unrelated code.** If a file or function is not directly part
   of the current authorized responsibility, do not modify it merely because
   it could be improved.
5. **Finding is not authorization.** Discovery, diagnosis, or recommendation
   does not silently expand scope or grant authority to repair, publish, merge,
   or otherwise mutate external state.
6. **Flag material uncertainty explicitly.** State uncertainty that could
   change the next responsibility, claim, or authority decision. Do not turn
   unresolved hypotheses into confident claims.

## Current construction orientation

For engineering work, the bundled
[`using-sensemaking` Skill](skills/using-sensemaking/SKILL.md) contains the
**portable** Architect -> Builder -> Reconcile procedure. Invoke/load it
through the coding-agent harness when relevant; this repository instruction
is a discovery aid, not a precondition for the Skill to work elsewhere.
For **this repository's** architect-and-builder phase, read
[Value-Directed Continuous Construction](docs/value-directed-continuous-construction.md)
and the [local build-loop profile](docs/agents/build-loop.md) when selecting
repository-level responsibilities. They supply current product context and
local owner conventions rather than portable requirements. Apply the
explicit verification/merge exception in `CLAUDE.md` here; never export
this repo's no-local-unit-tests or prompt-merge policy to other targets.

## Local verification

Choose local test scope by the change's risk. The full policy is in `CLAUDE.md`, section "Local verification scope"; follow it.

## Evaluation & benchmark work

For evaluation or benchmark work, do not silently resolve an ambiguity that can
affect treatment, selection, scoring, or interpretation — surface it before
consuming evidence. A runnable procedure is not necessarily a measurable one:
verify required observability before execution. See
`docs/experimental-phase-gates.md`.
