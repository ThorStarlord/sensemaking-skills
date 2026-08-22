# Decision and Orchestration Boundary

**Status:** architecture clarification grounded in ADR 0013, ADR 0014, and
`docs/agent-native-operating-workflow.md`  
**Scope:** control ownership in the agent-native operating model  
**Non-goal:** this document does not introduce a new runtime, registered workflow,
Skill, routing table, or automation contract.

## Why this boundary matters

Sensemaking Skills contains both decision-oriented concepts and orchestration
machinery. Without an explicit boundary, it is easy to treat existing runtime
mechanics as if they own the product-level decision loop, or to make the
Sensemaking layer itself grow into a generic workflow engine.

The current model keeps those responsibilities separate:

> **Decision selects the work. Orchestration coordinates the work. Evidence
> determines what becomes warranted next.**

The active coding agent owns the recursive loop between them.

## Decision layer

The Sensemaking decision layer answers:

> **Given the current goal, evidence, uncertainty, and authority, what
> responsibility is warranted next?**

Its responsibilities include:

- interpreting current evidence without flattening observation, interpretation,
  and hypothesis;
- identifying the nearest unresolved uncertainty that could change the correct
  next action;
- choosing a responsibility before choosing a Skill or implementation;
- deciding whether more evidence is warranted before action;
- deciding whether continuation, stopping, escalation, or human decision is
  warranted;
- constraining claims to what the evidence supports;
- respecting authority boundaries between knowing, deciding, acting, and
  publishing.

The decision layer is not required to know the complete path to the final
solution in advance. The path may change when new evidence changes the warrant.

## Execution and orchestration layer

Execution/orchestration answers a different question:

> **How should an already-selected responsibility be coordinated and
> performed?**

Its responsibilities may include:

- invoking the selected Skill, tool, script, or registered subworkflow;
- passing declared inputs and resolved artifact paths;
- sequencing deterministic steps inside an established subflow;
- collecting outputs and validator results;
- handling execution-control outcomes such as retry, wait, timeout, or failure;
- returning resulting artifacts/evidence to the active agent.

Orchestration can make execution-control decisions. For example, a runtime may
retry a failed deterministic command according to an established retry policy.
That does not give it authority to silently decide that a different engineering
responsibility is now warranted.

## Two different meanings of "what next?"

An orchestrator commonly asks:

> **Which already-defined node or step runs next?**

Sensemaking asks:

> **What responsibility should become the next node at all?**

The distinction matters when repository evidence invalidates the expected
implementation path.

Example:

```text
user-visible symptom: validator appears broken

predetermined path:
  inspect -> repair -> test

Sensemaking path:
  inspect
  -> uncertainty: is this still a live responsibility?
  -> provenance / ownership investigation
  -> evidence: responsibility was retired upstream and replacement coverage exists
  -> warranted responsibility changes from repair to retirement/reconciliation
```

A fixed orchestration path would have encoded `repair` too early. The
Sensemaking decision layer keeps the responsibility revisable until the
relevant decision-changing uncertainty is resolved.

## Current ownership model

| Question | Primary owner |
| --- | --- |
| What is the current goal and authorized scope? | user / active agent |
| What repository evidence exists? | active agent + bounded Skills/probes |
| What unresolved uncertainty could change the next action? | Sensemaking decision layer |
| What responsibility is warranted next? | Sensemaking decision layer |
| Which bounded capability can perform it? | active agent using the Skill/capability catalog |
| How is that capability invoked and supplied inputs? | execution/orchestration machinery |
| Should a deterministic execution step retry/wait/fail? | execution/orchestration policy |
| What does the resulting evidence mean for the task? | active agent + relevant domain responsibility |
| Is another responsibility warranted? | Sensemaking decision layer |
| Does the work claim match durable evidence? | reconciliation / verification responsibility |
| Is the original finding actually resolved? | finding-specific / repair verification |
| May the agent decide, mutate, publish, or merge? | authority policy + human owner where required |

## Architectural guardrails

1. **Do not encode the whole operating loop as one registered workflow merely
   because the loop can be drawn as a graph.** The top-level loop contains
   judgment whose semantics are not stable mechanics.
2. **Do not treat automatic routing as ratified product behavior.** Existing
   runtime routing paths are compatibility machinery unless separately
   ratified.
3. **Do not make the decision layer a generic runtime.** Scheduling, queues,
   persistence, worker management, and generic DAG execution are adjacent
   infrastructure, not the current product thesis.
4. **Do not make orchestration own responsibility selection by accident.** A
   predetermined sequence must not silently replace evidence-grounded
   responsibility selection.
5. **Use registered workflows as bounded subgraphs when their semantics are
   stable and mechanically expressible.** They may execute inside the larger
   agent-owned loop.

## Relationship to the operating workflow

The current top-level model is:

```text
DECIDE
  -> select warranted responsibility
EXECUTE / ORCHESTRATE
  -> perform bounded responsibility
OBSERVE
  -> collect artifact/evidence
REASSESS
  -> update warrant; continue / stop / escalate
```

This document clarifies ownership of those transitions. The canonical operating
map remains `docs/agent-native-operating-workflow.md`.
