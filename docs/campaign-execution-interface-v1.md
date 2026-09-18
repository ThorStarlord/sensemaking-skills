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

The deterministic interface only preserves the exact delegation and return
boundary.
