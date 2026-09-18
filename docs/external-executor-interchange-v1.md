# External Executor Interchange v1

**Status:** post-RC2 development contract  
**Depends on:** Campaign Execution Interface v1  
**Campaign schema:** unchanged at v2

## Purpose

Sensemaking can transport an already-selected responsibility to an external
worker or software factory without becoming that executor.

```text
Sensemaking decision
-> execution handoff companion
-> generic interchange envelope
-> external executor / scheduler
-> generic result envelope
-> Campaign execution result companion
-> parent reassessment
```

The interchange is intentionally implementation-independent. An adapter may
render the same handoff for a particular external system, but adapter-specific
details do not become Campaign truth.

## Generic handoff export

`campaign execution export` emits an integrity-bound
`sensemaking.execution-handoff` envelope containing:

- Campaign and handoff identity;
- the exact execution-handoff record digest;
- caller-selected executor kind;
- already-selected responsibility;
- exact target identities;
- evidence requirements;
- forbidden actions;
- the worker-result contract.

The envelope explicitly records that the tool did not select the work, grant
authority, or execute it.

## Worker-result interchange

`campaign execution result-template` creates the expected shape.

After the external worker fills the required fields,
`campaign execution result-seal` validates and recomputes the envelope digest.
`campaign execution result-import` then:

1. verifies schema/kind/digest;
2. verifies Campaign and handoff identity;
3. verifies the exact handoff record digest;
4. preserves the worker's explicit authority-exceeded report;
5. appends the normal execution-result companion record.

Import does not admit returned refs into Campaign evidence and does not close the
Campaign.

```text
result envelope valid != worker claim true
result imported != evidence admitted
worker completion != parent closure
```

## AI Software Factory adapter

`campaign execution factory-issue` renders a GitHub Issue payload for the
current AI Software Factory / Archon workflow model.

The caller must supply both:

- the exact target repository as `OWNER/REPO`;
- the exact workflow identifier, such as `archon-ship` or
  `archon-lifecycle`.

Sensemaking deliberately does not choose between them.

The projection includes:

- an issue marker: `<!-- sensemaking-execution-handoff:v1 -->`;
- human-readable responsibility, authority, target, success, evidence, and
  forbidden-action sections;
- the full machine-readable generic handoff envelope;
- a command template:

```text
python factory/consumer.py run <caller-selected-workflow> \
  --input target={ISSUE_URL} --detach --json
```

The projection does **not** publish the issue or submit the workflow.

```text
factory issue rendered != issue published
workflow supplied != workflow selected by Sensemaking
factory run possible != factory run authorized
```

## Commands

```bash
sensemaking-skills campaign execution export \
  --workspace /path/to/CMP-1 \
  --handoff-id H-1 \
  --output handoff.json

sensemaking-skills campaign execution result-template \
  --workspace /path/to/CMP-1 \
  --handoff-id H-1 \
  --result-id RES-1 \
  --worker external-worker \
  --output result.json

# worker fills result.json
sensemaking-skills campaign execution result-seal \
  --file result.json

sensemaking-skills campaign execution result-import \
  --workspace /path/to/CMP-1 \
  --file result.json

sensemaking-skills campaign execution factory-issue \
  --workspace /path/to/CMP-1 \
  --handoff-id H-1 \
  --repository OWNER/REPO \
  --workflow archon-lifecycle \
  --output factory-issue.json
```

## Product boundary

Sensemaking owns the delegation/evidence-return contract. The external system
owns worker allocation, scheduling, retries, queues, process execution, and any
system-specific lifecycle.

The active agent/owner remains responsible for deciding whether the exported
responsibility should be executed and whether returned evidence changes the
parent decision.
