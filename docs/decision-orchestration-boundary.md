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

## Failure, review, and reassessment

A failure, review rejection, validator result, or other abnormal outcome is
**evidence about the current state**. It does not by itself prescribe a rewind,
repair, or downstream route.

Execution/orchestration may perform bounded mechanical recovery — retry, wait,
timeout, fail — when that behavior is already established (see the retry policy
above). When the outcome could change the selected responsibility, the expected
solution, the scope, or the authority, control returns to the Sensemaking
decision layer, which reassesses what responsibility is warranted now. That may
be: retry or local repair; revise an upstream artifact; gather more evidence;
reconcile conflicting artifacts; request an owner decision; or stop.

```text
failure          != rewind command
review finding   != next responsibility
test failure     != implementation-defect proof
recommendation   != execution authority
```

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

## Deterministic machinery and hooks

This section consolidates, in one place, what the repository's deterministic
scripts own, what they must not own, and what hooks are for. It restates
evidence that already exists elsewhere (the ADR 0013 amendment, ADR 0026,
ADR 0027, the retirement plan's responsibility classification,
`docs/enforcement-contract.md` section 4, `CONTEXT.md` "Evidence model");
it ratifies nothing new.

### What deterministic scripts own

One row per responsibility class, not per script. Every script named here
exists under `scripts/` (checked 2026-09-02).

| Responsibility | Script(s) | Authority source |
| --- | --- | --- |
| Contract / schema validation of artifacts | `validate-output.py` reads `artifact-contracts.yaml` and runs `validate-artifact.py` (generic) then the specialized validators registered for the artifact (`validate-brief.py`, `validate-plan.py`, ...) | ADR 0013 amendment item 2: typed artifact contracts + deterministic validators are part of the Skill contract, independent of any harness |
| Measured repository state (evidence candidates with provenance, never diagnoses) | `probe-repo.py` -> `repo_probes.py`, `probe_relationships.py`; writes `probe-report.yaml` | `CONTEXT.md` "Evidence model": the Probe Engine provides measured state for `repo-sensemaker`; a probe that cannot evaluate a fact is not evidence of absence |
| Mechanical gate policy in CI | `gate_relationship_findings.py` -- the only place that decides which probe finding types block (currently `missing_reference`, `missing_status_line`) | `docs/enforcement-contract.md` section 4: a finding type may block only if it is mechanically decidable and the probe marks it `requires_semantic_review: False` |
| Artifact path resolution and run ledger | `workflow-runtime.py` (`_resolve_artifact_path`, session-scoped; appends `run-ledger.jsonl`), `run-ledger.py` | ADR 0010: the runtime owns path resolution and passes `expected_output_path`; retirement plan "Responsibility classification": artifact resolution and session handling / run ledger are KEEP |
| Registry integrity and workflow liveness | `validate-repo.py`, `workflow_liveness.py` | ADR 0027: catalog identity is separate from liveness; planner, runtime, and validators fail closed on non-active workflows |
| Skill distribution drift | `probe_skill_distribution.py` (repository `skills/<skill>/` vs an installed copy; copies only with `--sync`) | `src/sensemaking_skills/setup_skills.py` drift rule: an installed copy is never silently overwritten |
| Bounded execution coordination of an already-selected responsibility | `workflow-runtime.py`: plan generation, step sequencing, validator dispatch (with timeouts), gate management (incl. `GATE_TIMEOUT` and terminal inconclusive gates), execution modes, run-log recording | this document, "Execution and orchestration layer"; retirement plan "Responsibility classification": validation dispatch, gates / execution modes, and plan generation are KEEP, second-model invocation is RETIRE |

On the last row: this document allows execution/orchestration to make
execution-control decisions (retry, wait, timeout, fail) where a policy is
already established. What `workflow-runtime.py` implements today is
timeouts and terminal gate outcomes; it implements no retry policy. "Retry"
is therefore a permitted class of execution-control decision, not a
currently implemented one.

### What deterministic scripts must not own

| Responsibility | Why not | Source |
| --- | --- | --- |
| Responsibility selection and uncertainty selection | the active coding agent owns the control loop; a predetermined sequence must not silently replace evidence-grounded selection | ADR 0013 (agents own the control loop; amendment item 1); guardrail 4 below |
| Stop / continue / escalate decisions | each stage's "done" is a judgment about sufficiency for the next decision, not a mechanical state | `docs/agent-native-operating-workflow.md` section 2, "STOP CONDITIONS" |
| Authority decisions, including spawning a next workflow without a separate explicit authority event | `recommendation != selection != execution authorization`; with no authority event the runtime fails closed (it may surface a candidate, it must not spawn it) | ADR 0026 section 2 |
| Semantic interpretation of findings | anything the probe marks `requires_semantic_review: True` never blocks; the gate blocks on mechanical contradictions and never decides what to fix | `docs/enforcement-contract.md` section 4 |
| Routing from fog type to an implementation workflow | routing is deferred pending its own external proof; the deterministic fog-type routing table was never accepted | ADR 0014; ADR 0018 (SUPERSEDED, never Accepted) |

### Evidence from real use (campaign R2-R4, 2026-09-02)

Three consecutive fresh-context continuations in
[`docs/campaigns/agent-native-self-development/`](campaigns/agent-native-self-development/CAMPAIGN-STATE.md)
used the scripts above only as referees.
[R2](campaigns/agent-native-self-development/R2-continuation-trial.md)
ran `probe-repo.py`, `pytest` on `test_path_drift.py` + `test_cli.py` under
both code pages, and `validate-repo.py` (report section 4).
[R3](campaigns/agent-native-self-development/R3-operating-map-reconciliation.md)
ran `validate-repo.py` and `pytest tests/test_path_drift.py` (report
section 5).
[R4](campaigns/agent-native-self-development/R4-implementation-continuation.md)
ran `pytest` on the named test files and on the CI `core-assertions` set
under both code pages, and `validate-repo.py` (report sections 3-4). Every
judgment stayed with the agent: which rows to refresh and what to write when
the record's fact was wrong (R2 sections 2 and 4); what to narrow and what
to leave unresolved (R3 summary and section 3); repair vs. retire per file,
and revert when the spec's own branch said so (R4 section 2). No script
selected a responsibility, decided a stop, or granted authority.

### Hooks

Mechanism truth (repository state, 2026-09-02):

- No Claude Code hook is configured in this repository: `.claude/settings.json`
  is `{}`, and nothing else under `.claude/` configures one.
- `.claude/hooks/sessionstart.md` is a Markdown description of a
  session-start convention (read the `using-sensemaking` bootstrap skill
  before using the skills). Nothing executes it.
- The bootstrap is discoverable because `CLAUDE.md` names the skill and
  points at that file, and because the skill tree is copied into an
  agent-discoverable skills directory (`~/.claude/skills` per
  `INSTALLATION.md`; `~/.agents/skills` or the plugin cache per
  `src/sensemaking_skills/setup_skills.py`), from which the agent's Skill
  tool or a direct file read reaches `skills/using-sensemaking/SKILL.md`.

Current disposition: **no continuation or liveness hook is warranted.** Each
of the four record-mediated continuations R1-R4 was an explicit dispatch into
a fresh context and produced its report; no missed continuation event is
recorded; the durable Markdown record sufficed. See
`docs/agent-native-operating-workflow.md` section 2, "Responsibility-level
continuation from a durable record", and section 6, "No continuation
schema, validator, or hook" (both written after R1-R2); the R3 and R4
reports linked above cover the later two.

The only admissible future hook shape, per the repository's authority model:

```text
detect artifact
-> validate artifact
-> register provenance / state
-> signal the active agent to reassess
```

Never:

```text
artifact X -> execute Skill Y
```

A hook may do mechanical work and wake the agent. It may not select the next
responsibility or spawn a workflow: that is an authority event the hook does
not hold (ADR 0026 section 2; guardrail 4 below).

Reopen condition: a recurrent continuation event that a manual step keeps
missing, observed in real use.

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
