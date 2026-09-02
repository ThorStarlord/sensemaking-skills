# Sensemaking Agent-Native Operating Workflow v0

**Status**: v0 operating guide -- grounded in current implementation and
prior dogfood (evidence 0016-0020), subject to revision through real use.
This is NOT a canonical orchestration specification.
**Type**: workflow map -- not an ADR, not a registered workflow, not a Skill
**Authority**: ADR 0013 (agent-native orchestration is primary) + ADR 0014
(product boundary: evidence-grounded, human-reviewed brief is the settled core)
**Scope**: how an active coding agent uses Sensemaking Skills end to end

> **Top rule**: This document describes how the active coding agent uses
> Sensemaking Skills. It is not itself an executable orchestration contract.
> Stable subflows may be encoded independently when repeated use earns them.

---

## 0. Why this document exists

The session arc that produced this map: a real Auteur handoff was audited
("read the artifact, not the prose"), that lesson became the
`artifact-reconciliation` workflow and the `output-reconciler` /
`repair-verifier` skills, dogfooding those exposed execution-model ambiguity,
ADR 0013 ratified agent-native execution as primary, and the programmatic
second-model runner was retired (`docs/2026-08-programmatic-runner-retirement-plan.md`,
CLOSED 2026-08-13).

What remained unanswered: one consolidated answer to

> "I am a coding agent working in an unfamiliar repo. How do I actually use
> Sensemaking Skills from beginning to end?"

This document is that answer, expressed as a map. It models three
synchronized views, because modeling only one hides the architecture:

| View | What it answers | Example |
|---|---|---|
| **Responsibility flow** | What question are we trying to answer next? | "What is the consequential boundary?" -> "What specialized responsibility is needed?" -> "Did the work support its claims?" |
| **Artifact flow** | What durable information crosses each boundary? | request -> `repository_sensemaking_brief` -> specialized artifact -> `reconciliation_report` -> `repair_verification_report` |
| **Authority flow** | Who is allowed to know/decide/do this? | inspect repo -> agent; empirical claim -> probe; owner preference -> owner; external mutation -> explicit authority |

---

## 1. The operating flow

The control loop belongs to the **active coding agent** (ADR 0013). The
runtime/scripts are deterministic support machinery. Registered workflows
(`fast-path-workflow`, `artifact-reconciliation`,
`docs-contract-reconciliation`, ...) are potentially **subgraphs inside this
loop**, not the whole loop. The per-workflow disposition of all 23 registered
workflows in campaign vocabulary, with the execution evidence behind each
call, is recorded in [`workflow-system-disposition.md`](workflow-system-disposition.md)
(non-authoritative; ADR 0027 and the liveness overlay remain the liveness
authority).

```text
USER REQUEST / WORK CLAIM
        |
        v
ACTIVE CODING AGENT (owns the control loop; ADR 0013)
        |
        v
ENTRY / TRIAGE: would repository sensemaking materially change
how I should interpret or execute this request?
        |
   +----+-----------------------------+
   no                                yes / uncertain
   |                                     |
   v                                     v
bounded work                      REPO-SENSEMAKER
   |                                (probe engine + brief)
   v                                     |
validation                            repository_sensemaking_brief
   |                                     |
   |                                deterministic validation
   |                                     |
   |                                BRIEF REVIEW: is the consequential
   |                                next decision supported?
   |                                     |
   |                      repository_evidence -> inspect
   |                      empirical        -> probe (bounded)
   |                      owner_intent     -> ask owner (one neutral question)
   |                      external_env     -> inspect outside if authorized
   |                                     |
   |                                SELECT NEXT RESPONSIBILITY
   |                                (responsibility before Skill;
   |                                 agent judgment, not routing)
   |                                     |
   |                                SPECIALIZED WORK
   |                                (read SKILL.md, gather declared
   |                                 inputs, produce contracted artifact)
   |                                     |
   +--------------------------------> VALIDATION (mechanical)
                                             |
                            material claim / handoff?  -> OUTPUT RECONCILIATION
                            repair of prior finding?   -> REPAIR VERIFICATION
                                             |
                                             v
                             REVIEW / PROMOTE / MAKE DURABLE
                                             |
                                             v
                                  STOP (stage stop conditions) or CONTINUE
```

---

## 2. Responsibility flow

### ENTRY / TRIAGE

Question: **would repository sensemaking materially change how I should
interpret or execute this request?**

Use `repo-sensemaker` when:

- intent is unclear against repository reality,
- consequential boundaries are unknown,
- architecture/documentation conflict matters,
- work crosses unfamiliar subsystem boundaries.

Skip it when the task is already mechanically narrow and locally evidenced
(e.g. "rename this field in this known schema and update its two tests").

Otherwise `repo-sensemaker` becomes mandatory ceremony. The closest formal
statement of this policy is `repo-sensemaker`'s Boundary Rule 3 (clarification
policy) and its "Interact" section.

### REPO-SENSEMAKER

Responsibility: turn user intent + repository evidence into an
evidence-grounded account of what the repository actually says, where the
consequential boundary lies, and what uncertainty remains. It does **not**
choose the whole downstream workflow, and a diagnosis is **not**
authorization to modify anything.

Implemented mechanics (REAL):

- Probe engine (`scripts/probe-repo.py` -> `probe-report.yaml`): measured
  current state, mandatory before synthesis; probe failure fallback labels
  claims "documented but not independently verified".
- Weakness types (`skills/repo-sensemaker/references/weakness-types.md`) for
  the weakest boundary.
- Section 13 machine handoff and (optional) Section 15 `extended_analysis`
  (ADR 0024) carrying `uncertainty.source` --
  `repository_evidence | empirical | owner_intent | external_environment` --
  and `owner_intent_state`.
- Output artifact: `repository_sensemaking_brief`
  (`skills/workflow-planner/references/artifact-contracts.yaml`).

### BRIEF REVIEW

Question: **does the Brief actually support a consequential next decision?**
Not "did the validator pass?"

```text
schema validity
!= evidentiary sufficiency
!= analytical correctness
!= decision usefulness
```

The uncertainty taxonomy becomes operational here:

- answer already in the repository -> **inspect** (`repository_evidence`)
- reality must be observed -> **probe** (`empirical`; bounded -- a probe
  that needs its own authorization is not pre-authorized)
- fundamentally the owner's preference -> **ask the owner** (`owner_intent`;
  one neutral, high-information question, default)
- outside this repository -> **inspect the external environment if
  authorized** (`external_environment`)

This prevents asking the owner things the repository can answer, and
prevents inventing owner preference from code.

### NEXT-SKILL SELECTION

Rule: **choose responsibility before choosing Skill**, then keep the choice
agent-reasoned and explicit. Examples:

| Responsibility | Skill |
|---|---|
| architecture uncertainty | `architectural-review` |
| claim about completed work | `output-reconciler` |
| claim that prior findings were fixed | `repair-verifier` |
| docs / implementation disagreement | `sensemaking-docs-reconciler` |
| mechanically narrow implementation | ordinary coding work |

Automatic routing is deliberately **not** ratified: ADR 0014 defers routing
until external proof, and ADR 0018 (deterministic fog-type routing table) is
SUPERSEDED, never accepted. Do not restore automatic routing by accident.

### SPECIALIZED WORK

The active coding agent reads the chosen `SKILL.md`, gathers the declared
inputs, performs the work itself, and produces the contracted output. No
second model invocation is conceptually required (ADR 0013).

Operating rule: **required information crosses the boundary as artifacts /
declared inputs, not as remembered conversational context** (the `work_claim`
fan-in lesson). A Skill must not "work" only because the agent remembers what
happened 30 messages ago.

### VALIDATION

Every consequential artifact is validated as soon as it is produced, via
`scripts/validate-output.py` dispatch -> generic
(`scripts/validate-artifact.py`) + specialized validators
(`validate-brief.py`, `validate-plan.py`, ...), with structured JSON errors.

Mechanical validation establishes: required fields exist, controlled
vocabulary is valid, references resolve, artifact shape is correct, paths
satisfy contracts. It cannot establish: the right evidence was selected, the
conclusion follows, the consequential boundary is useful, the owner should
accept the recommendation.

```text
Skill produces artifact -> mechanical validator -> eligible for semantic use
```

-- not:

```text
validator passed -> artifact is true
```

### OUTPUT RECONCILIATION

Trigger: a **material handoff or consequential claim** ("implemented X",
"fixed Y", "all tests pass", "ready for handoff") -- not every tiny edit.

Mechanics (REAL, dogfooded): `output-reconciler` reads the `work_claim` +
`repository_sensemaking_brief` (+ optional `prior_evidence`), re-derives each
claim from durable artifacts, classifies each `verified | disputed | omitted`,
disposes each disputed/omitted claim `fix | defer (with reason) | file`, and
emits `reconciliation_report`. Registered subgraph:
`artifact-reconciliation` workflow (`workflow-registry.yaml`). This is the
operational form of "read the artifact, not the prose" (evidence 0020).

### REPAIR VERIFICATION

Separate responsibility from reconciliation: reconciliation asks "are the
claims about the work supported?"; repair verification asks **"did this
change actually close the original diagnosis?"**

Mechanics (REAL, dogfooded): `repair-verifier` re-probes the repository,
checks each original finding against the fresh `probe-report.yaml`, and emits
`repair_verification_report` (`findings_closed` / `findings_remaining` with
disposition). Registered subgraph: `docs-contract-reconciliation` workflow
step 3.

Rules:

- generic green tests != finding-specific closure;
- a failed/errored observation is not an observed absence -- the probe engine
  times out rather than raising. v0 note: a formal `unevaluable` verdict
  category is proposed but not yet encoded in the
  `repair_verification_report` contract.

### PROMOTION / DURABILITY

A lifecycle transition, not a synonym for `git add`:

```text
produced -> validate -> review -> worth preserving? -> promote
-> make references durable -> commit/integrate if authorized
```

```text
runtime artifact (scratch, inspectable, regenerable, discardable)
!= durable evidence (tracked, stable-addressed, fresh-clone-resolvable,
   independent of the producer's active session)

promoted != merged != canonical
```

Existing support: `skills/skill-maintainer/references/promotion-criteria.md`
(six gates for skill improvements) and evidence 0019's deferred-items
doctrine. Partially formalized -- see Reality map.

### AUTHORITY GATES

A parallel track, not scattered prompts. See section 4.

### STOP CONDITIONS

Every stage answers "what means enough?":

| Stage | Done when |
|---|---|
| Sensemaking | the brief suffices for the next consequential decision |
| Specialized analysis | the requested decision artifact exists and passes its contract |
| Implementation | the scoped change exists and its relevant mechanical verification passes |
| Reconciliation | material claims have dispositions and consequential omissions/findings are surfaced |
| Repair verification | each scoped original finding is closed or remaining (with disposition) |
| Overall session | next decision is explicit + useful artifacts are durable where warranted + no unresolved decision-blocking uncertainty remains |

"Done" is not "there are no more things I could investigate."

### CONTINUATION

Desired principle:

```text
next agent/run -> reads durable artifacts -> reconstructs state
```

rather than:

```text
next agent/run -> depends on conversation memory
```

Current reality (recorded in the retirement-plan closure): typed fan-in
`CONTRACT_CLOSED`; prior-report selection `CONVENTION` (the caller supplies
which prior report); overall loop `CONVENTION_CLOSED`.

Operating rule (recorded 2026-08-13, carried into normal use): when a
continuation feels awkward, preserve the actual handoff, preserve the
candidate prior reports, record what the agent could and could not
reconstruct, and do not design the fix yet. Reopen trigger: at least one
real agent-native continuation cannot reconstruct the intended prior report
from durable repository state without relying on conversational/session
memory.

#### Responsibility-level continuation from a durable record (demonstrated 2026-09-02)

The cross-run-identity status above is unchanged. A narrower form of
continuation -- one bounded responsibility handed from one coding-agent
context to a fresh one through a durable Markdown record -- has been
demonstrated in real use inside the campaign directory
[`docs/campaigns/agent-native-self-development/`](campaigns/agent-native-self-development/CAMPAIGN-STATE.md).
Two fresh contexts, given only the repository worktree and the path of
`CAMPAIGN-STATE.md` (no conversation history, no Skill invocation, no
workflow runtime), did the following:

- **R1** ([report](campaigns/agent-native-self-development/R1-fresh-context-reconstruction.md))
  reconstructed the mission, the capability state, why the current task had
  been selected over the visible alternatives, what was established vs.
  uncertain, and the warranted next action: questions Q1-Q5 `RECONSTRUCTED`,
  authority (Q6) `PARTIAL`, five omissions listed (Q7); cost 39 files /
  25 tool calls.
- **R2** ([report](campaigns/agent-native-self-development/R2-continuation-trial.md))
  performed a seven-step, three-file documentation responsibility from the
  record alone: established the record's facts from git and CI before
  writing, refreshed the named rows, ran the named validators, committed
  under the required convention, declined plausible-but-unlisted edits
  (report section 5 A2/A4/A5), and wrote a candid report; cost 9 files /
  36 tool calls. Its verification step exposed one wrong fact in the record
  (gate provenance, report M1/F1); it wrote the git-established facts and
  flagged the conflict instead of silently correcting the record.

Durable state that proved necessary (all of it in the record, none of it in
conversation memory):

- the mission;
- a capability-state table with a repository evidence pointer per row;
- known gaps and active constraints;
- authority: every grant traced to a durable source, plus an explicit
  not-authorized list;
- a task spec with numbered steps, verification steps (not only
  assertions), a stop condition, the commit convention, and the expected
  evidence;
- open decision-changing uncertainties and deferred findings;
- remote / integration status (push, PR, CI) recorded, never assumed;
- an append-only responsibility trace.

Beyond the record, the fresh contexts needed only repository state, mostly
named by the record (protocol docs, table conventions, git/CI facts; R2
section 6 F7) -- no conversation state.

Failure classes observed, and how each was repaired at the following
close-out:

- `AUTHORITY_AMBIGUITY` (R1 Q6, narrow: a merge rule sourced to an
  out-of-repository standing instruction; push/PR delegation asserted only
  by the record; no source for who authorizes implementing candidate
  machinery on the branch) -> source every grant: the record now cites a
  durable source per grant (its section 11) and the owner instruction is
  committed verbatim (`CHARTER.md`).
- `MISSING_DURABLE_STATE` (R1 Q7: the charter and a cited standing
  instruction were not in the repository; push/PR status was not recorded;
  some cited evidence lives only in GitHub issues) -> commit the authority
  text; record push/CI status in the record; mark GitHub-only evidence as
  such.
- Not in the taxonomy: durable state that was present but *wrong* on one
  fact (R2 M1). No schema would have caught it; the spec's own "establish
  from git" step did. Task specs therefore carry verification steps.

Not needed at this scale: a continuation schema, a validator, a new artifact
type, or a hook. Both continuation events were explicit dispatches; the
record plus the report sufficed; zero shape errors were observed. Reopen
conditions (campaign record U5/U3): a fresh context fails on a *missing or
malformed section* rather than a wrong fact; more than one dispatcher must
produce such records; or a recurrent continuation event that a manual step
keeps missing is observed (hook).

Observed limitation: documentation-level responsibilities only.
Implementation-class continuation (code + tests + CI) from durable state is
untested (campaign record U7). Nothing here exercises the cross-run
prior-report identity trigger above, which stays unresolved.

---

## 3. Artifact flow

What durable artifact crosses each boundary (field names and paths are the
contract -- `artifact-contracts.yaml`; ADR 0010: one component, the runtime,
resolves paths and passes them as `expected_output_path`; producers never
recompute them):

| Boundary | Artifact | Producer | Consumers (declared) |
|---|---|---|---|
| Request | `user_intent` | workflow-runtime | problem-framer, unknowns-mapper, repo-sensemaker, workflow-planner, docs-aligner, to-prd, to-issues, triage, handoff |
| Triage (optional) | `problem_frame` / `unknowns_map` | problem-framer / unknowns-mapper | repo-sensemaker (+ unknowns-mapper / prompt-handoff) |
| Diagnosis | `repository_sensemaking_brief` | repo-sensemaker | workflow-planner, prompt-handoff, sensemaking-docs-reconciler, output-reconciler |
| Planning (optional) | `workflow_orchestration_plan` | workflow-planner | prompt-handoff |
| Claim to audit | `work_claim` | task-requester (external, promoted) | output-reconciler |
| Reconciliation | `reconciliation_report` | output-reconciler | to-issues, handoff |
| Docs reconciliation | `docs_contract_reconciliation_report` | sensemaking-docs-reconciler | repair-verifier, handoff |
| Repair verification | `repair_verification_report` | repair-verifier | handoff |
| Findings disposition | `issue_list` | to-issues | triage |
| Durable handoff | `session_summary` / `prompt_handoff` | handoff | workflow-planner / external agent |

Mandatory fan-in example (the "artifacts are the API" question, resolved):

```text
repo-sensemaker       -> repository_sensemaking_brief
output-reconciler     <- work_claim (required)
                      <- repository_sensemaking_brief (required)
                      <- prior_evidence (recommended)
repair-verifier       <- docs_contract_reconciliation_report (required)
                      <- prior_evidence (recommended: original brief + probe)
```

---

## 4. Authority flow

| Question | Allowed | Not allowed |
|---|---|---|
| Can the agent **KNOW** this? | repository fact -> inspect/probe; empirical fact -> bounded probe | infer an external environment from inside the repo |
| Can the agent **DECIDE** this? | reversible implementation detail -> possibly yes (scope-dependent) | owner preference, policy, canonical authority -> owner / ADR process |
| Can the agent **ACT** on this? | local reversible work -> scope-dependent; tracker reads | external tracker writes, merge, publish, deploy -> explicit authorization (ADR 0014 out of scope; ADR 0019 PROPOSED) |

Non-identities (each observed as a real failure mode):

```text
finding            != authorization to fix
recommendation     != owner decision
issue_list         != authorization to create tracker issue
implemented        != ratified
diagnosis          != authorization
```

---

## 5. Reality map

| Responsibility | Existing support | Current status | What not to assume |
|---|---|---|---|
| Entry / sensemaking trigger | repo-sensemaker Boundary Rule 3 + agent judgment | CONVENTION / partially encoded | repo-sensemaker is not mandatory for every task |
| Repository diagnosis | `repo-sensemaker` + probe engine | REAL (ratified, ADR 0014) | diagnosis does not authorize repair |
| Brief contract validation | `validate-artifact.py` / `validate-brief.py` / `validate-output.py` | REAL | structural PASS != analytically correct |
| Human review | conversation/process boundary | RATIFIED product boundary, agent-mediated | not an automated gate |
| Next responsibility selection | agent judgment + skill catalog | CONVENTION / unratified automation (ADR 0018 SUPERSEDED); exercised by a fresh context in campaign R1 (report Q3 alternatives table, Q5) | do not restore automatic routing by accident |
| Specialized analysis | individual Skills | REAL per Skill | Skill existence != product need |
| Artifact validation | validators + `artifact-contracts.yaml` | REAL | schema != truth |
| Output reconciliation | `output-reconciler` + `artifact-reconciliation` workflow | REAL + dogfooded (evidence 0018, 0020) | not needed after every trivial action |
| Repair verification | `repair-verifier` + `docs-contract-reconciliation` step 3 | REAL + dogfooded (evidence 0019); `unevaluable` category UNRATIFIED | generic green != closure |
| Promotion / durability | `promotion-criteria.md` + evidence 0019 doctrine | CONVENTION / partially formalized | promotion != canonicalization |
| Authority handling | Skill rules + ADRs (0016 accepted; 0019/0022 PROPOSED; 0023 accepted) + agent discipline | DISTRIBUTED | findings do not grant mutation authority |
| Continuation | typed inputs + durable artifacts | CONVENTION -- responsibility-level continuation DEMONSTRATED (campaign R1/R2, 2026-09-02); cross-run prior-report identity still CONVENTION_CLOSED; machinery not earned | prior-report identity deliberately unresolved |
| Stop conditions | this document (first consolidation) | CONVENTION (no machinery); exercised by a fresh context in campaign R2 (report sections 5 A2/A4/A5 and 8: stopped at the spec's stop condition, declined unlisted edits) | "no more things to investigate" is not done |
| Deterministic machinery | validators (`validate-output.py` -> `validate-artifact.py` + specialized), probe engine (`probe-repo.py`, `repo_probes.py`, `probe_relationships.py`), `gate_relationship_findings.py`, `workflow-runtime.py` + `run-ledger.py`, `validate-repo.py` + `workflow_liveness.py`, `probe_skill_distribution.py` -- roles consolidated in [`decision-orchestration-boundary.md`, "Deterministic machinery and hooks"](decision-orchestration-boundary.md#deterministic-machinery-and-hooks) | REAL as referees: contract validation, measured state, mechanical gate policy, path resolution + ledger, registry/liveness integrity, distribution drift, bounded execution coordination; used exactly so by the campaign fresh contexts R2-R4 (2026-09-02), every judgment left to the agent | scripts do not select responsibilities or uncertainties, decide stop/continue/escalate, grant authority or spawn a next workflow, interpret findings, or route from fog type to implementation |
| Hooks | none executable (`.claude/settings.json` is `{}`); `.claude/hooks/sessionstart.md` is a Markdown description of a session-start convention; `CLAUDE.md` + the installed `using-sensemaking` skill are the actual bootstrap surface -- disposition in [`decision-orchestration-boundary.md`, "Hooks"](decision-orchestration-boundary.md#hooks) | NOT WARRANTED for continuation or liveness: R1-R4 continuations were explicit dispatches from a durable record, each producing its report, no missed event recorded; admissible future shape is mechanical only (detect artifact -> validate -> register provenance/state -> signal the agent to reassess); reopen condition = a recurrent continuation event a manual step keeps missing in real use | a hook is not a router: never `artifact X -> execute Skill Y` (ADR 0026; boundary-doc guardrail 4); the hook doc describes, it does not execute |

---

## 6. What is deliberately not here

- **No new registered workflow** encoding the whole loop -- the top-level
  flow contains real judgment (trigger, uncertainty source, owner intent,
  next responsibility, authorization, stop) that is not stable mechanics yet
  (ADR 0013).
- **No new master Skill** -- the bootstrap skill `using-sensemaking` already
  teaches the entry pattern; this document describes, it does not execute.
- **No new ADR** -- ADR 0013 and ADR 0014 already ratify the architecture
  and product boundary; this document consolidates, it does not decide.
- **Registered workflows stay subgraphs** (`artifact-reconciliation`,
  `docs-contract-reconciliation`) -- the loop is not one giant choreography.
- **No continuation schema, validator, or hook** -- three record-mediated
  handoffs (campaign R0 -> R1, R1 -> R2, R2 -> close-out audit; two of them
  into fresh contexts) produced zero shape errors and one fact error, which
  an in-spec verification step caught and no schema would have; the
  machinery promotion rule (section 7) is not met. Reopen conditions as in
  section 2 "CONTINUATION": a failure on a missing or malformed section
  rather than a wrong fact; more than one producer of such records; or a
  recurrent continuation event that a manual step keeps missing.

---

## 7. Using and revising this document

Reading order for a new agent: section 1 (flow) -> section 2
(responsibilities) -> section 3 (artifacts) -> section 4 (authority) ->
section 5 (what is real vs. convention).

Revision trigger: when a responsibility in the Reality map flips status --
a convention earns machinery, or a deferred item reopens -- update this map
and surface it for owner review. Machinery promotion rule:

```text
repeated useful responsibility
+ stable enough semantics
+ repeated manual burden/error
+ mechanically expressible boundary
        -> candidate for formalization
```

Not:

```text
there is a box in the workflow diagram -> create a Skill/schema/validator
```

(Cross-run identity is the standing example: the "select prior report" box is
visible, but with no demonstrated product failure, the workflow recognizes
the responsibility and the architecture does not automate it yet -- that is
healthy, not a gap.)
