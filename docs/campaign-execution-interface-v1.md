# Campaign Execution Interface v1

**Status:** post-RC2 development contract  
**Representation:** additive Campaign companion; Campaign schema v2 is unchanged

## Purpose

The execution interface connects an **already-selected** Campaign responsibility
to an external worker and returns worker evidence to the parent decision context.

```text
selected responsibility
-> execution handoff
-> external worker / scheduler
-> worker result receipt
-> parent reassessment
```

The interface is not a planner, scheduler, queue, retry engine, or semantic
closure mechanism.

## Execution handoff

`campaign execution handoff` records:

- exact Campaign state digest;
- active responsibility ID, statement, scope, authority, trigger evidence, and
  success conditions;
- explicit primary and/or multi-repository target identities;
- caller-selected executor kind;
- required returned evidence;
- explicit forbidden actions;
- append-only companion integrity.

The command refuses to create a handoff without an active responsibility and at
least one explicit target binding.

```text
handoff recorded != work selected by tool
responsibility authority recorded != authority granted by tool
target bound != implementation correct
```

## Worker result

`campaign execution result` records:

- exact handoff ID;
- worker identity;
- source identity before and after work;
- changed paths;
- validation statements;
- returned evidence references;
- unresolved uncertainties;
- claims the worker says are supported or not supported;
- the caller-reported authority-exceeded flag.

Returned evidence is **not automatically admitted** into Campaign evidence.
Worker completion never closes the parent Campaign.

```text
worker success != global closure
returned evidence != admitted evidence
result recorded != result accepted
```

### Result claim ceiling

The result companion preserves **worker-reported assertions** unless another
mechanism independently verifies them. In particular, `source_before`,
`source_after`, `changed_paths`, validation statements, returned claims, and
`authority_exceeded` are declarations made by the caller/worker at import time.
The companion validates their structure, handoff association, and record/envelope
integrity; it does not by itself establish that those assertions are true.

For a result tied to exactly one handoff target, the durable result also records
whether the reported `source_before` equals that target's bound `head_sha`.
This is a cheap mechanical comparison, not a complete source-state verification:
dirty worktree identity, `source_after`, changed paths, validations, claims, and
authority compliance remain independently unverified. Multi-target v1 results
remain worker-reported because the return schema does not identify which target
the single `source_before` field refers to.

The current interface also does not act as a sandbox or security reference
monitor. It records target identity, scope/authority context, evidence
requirements, and forbidden actions, but it does not mechanically prevent a
worker from exceeding them or compare a complete worker action log against those
constraints.

```text
integrity-bound report != verified report
worker-reported source identity != independently observed source identity
worker-reported authority compliance != enforced authority compliance
forbidden action recorded != forbidden action mechanically prevented
```

When exact source identity, changed-path confinement, or authority compliance is
decision-critical, the parent or downstream execution runtime must verify the
relevant fact from an authoritative source before admission, closure, merge,
release, or another protected transition.

## High-delegation working context

`campaign working-context` projects:

- mission and current state;
- active responsibility and decision blocked;
- authority;
- active uncertainty;
- explicit target identities;
- current Campaign evidence refs;
- stop conditions already present in Campaign policy;
- latest execution handoff and worker result.

It deliberately emits no recommended next action.

## Commands

```bash
sensemaking-skills campaign execution handoff \
  --workspace /path/to/CMP-1 \
  --handoff-id H-1 \
  --executor-kind coding-agent \
  --evidence-requirement "exact changed source identity" \
  --evidence-requirement "focused tests" \
  --forbidden-action publish \
  --json

sensemaking-skills campaign execution result \
  --workspace /path/to/CMP-1 \
  --result-id RES-1 \
  --handoff-id H-1 \
  --worker worker-1 \
  --source-before <sha> \
  --source-after <sha> \
  --validation "focused tests: PASS" \
  --authority-exceeded no \
  --json

sensemaking-skills campaign execution inspect \
  --workspace /path/to/CMP-1 \
  --json

sensemaking-skills campaign working-context \
  --workspace /path/to/CMP-1 \
  --json
```

## Authority boundary

The active agent/owner still decides:

- whether the responsibility is warranted;
- which executor to use;
- whether the recorded authority permits the contemplated external action;
- whether returned evidence is credible and relevant;
- whether evidence should be admitted;
- whether to continue, repair, verify, escalate, defer, or close.

The deterministic interface preserves the exact declared delegation and return
boundary. It is a semantic/durable authority-control protocol, not a security
reference monitor.
