# 01 — SYSTEM OVERVIEW (DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0)

## What `sensemaking-skills` is (from evidence, not marketing)

An **agent-native engineering sensemaking and control layer for
software-engineering agents** (`CONTEXT.md:5`). It helps an active coding agent
move from repository uncertainty to an *evidence-grounded, warranted next
action*. The product-level question is **not** "which predefined workflow node
runs next?" but "given the current goal, evidence, uncertainty, and authority,
what responsibility is warranted next?" (`CONTEXT.md:7-11`).

The active coding agent owns the recursive top-level control loop
(**ADR 0013**, ACCEPTED). Everything in this repository is one of:

1. a **bounded Skill** that performs one responsibility and emits one contracted
   artifact;
2. **support machinery** the agent uses (probe engine, validators, registries,
   runtime, authorization seams);
3. **research infrastructure** that is explicitly *not* ratified product
   architecture (reasoning slice, campaign accounting/validation, control-model
   research agenda);
4. **canonical documentation** that records what is decided (ADRs), what is the
   operating map (AGW, CONTEXT.md), and what is still a research question.

## The real end-to-end flow (corrected from repository evidence)

The authorization's simplified flow was:

```
intent -> repo-sensemaker -> probing -> brief -> validation/reconciliation
-> representation_sufficiency / MODEL_WARRANT -> responsibility/workflow selection
-> execution coordination -> qualification / closure
```

What the evidence actually shows (`docs/agent-native-operating-workflow.md`
sections 1-5; `CONTEXT.md:54-127`):

```
USER REQUEST / WORK CLAIM
   |
ACTIVE CODING AGENT  (owns the loop; ADR 0013)
   |
ENTRY / TRIAGE: would repository sensemaking materially change how I interpret
   or execute this request?   -- agent judgment, NOT a gate
   |                                   \
   no: bounded work                     yes/uncertain
   |                                        |
   |                              REPO-SENSEMAKER
   |                              (probe engine MANDATORY before synthesis
   |                               -> probe-report.yaml
   |                               -> repository_sensemaking_brief
   |                               [Section 13 machine handoff,
   |                                Section 15 extended_analysis (ADR 0024),
   |                                representation_sufficiency judgment])
   |                                        |
   |                              DETERMINISTIC VALIDATION
   |                              (validate-output.py -> validate-artifact.py
   |                               + validate-brief.py; structured JSON errors)
   |                                        |
   |                              BRIEF REVIEW (agent + human-mediated):
   |                              does the brief support the next consequential
   |                              decision?  schema validity != sufficiency
   |                              != analytical correctness != usefulness
   |                                        |
   |                              [OPT-IN SEAM] MODEL_WARRANT:
   |                              runtime maps representation_sufficiency
   |                              -> NO / PARTIAL / INCONCLUSIVE (FULL deferred);
   |                              INCONCLUSIVE gates routing + representation
   |                              materialization + NO_CHANGE terminalization.
   |                              This seam is warrant_enabled (opt-in), not
   |                              the default product path.
   |                                        |
   |                              SELECT NEXT RESPONSIBILITY
   |                              (responsibility before Skill; AGENT JUDGMENT,
   |                               not automatic routing -- ADR 0014 defers
   |                               routing, ADR 0018 SUPERSEDED)
   |                                        |
   |                              SPECIALIZED WORK (agent reads SKILL.md,
   |                              gathers declared inputs, produces contracted
   |                              artifact -- no second model invocation
   |                              conceptually required, ADR 0013)
   |                                        |
   +----------------------------> VALIDATION (mechanical)
                                            |
                       material claim/handoff? -> OUTPUT RECONCILIATION
                                                  (output-reconciler +
                                                   artifact-reconciliation wf)
                       repair of prior finding? -> REPAIR VERIFICATION
                                                  (repair-verifier +
                                                   docs-contract-reconciliation
                                                   step 3)
                                            |
                              REVIEW / PROMOTE / MAKE DURABLE
                              (produced != validated != reconciled !=
                               repair-verified != authorized != integrated !=
                               closed;  promoted != merged != canonical)
                                            |
                              STOP (stage stop conditions) or CONTINUE
```

### Corrections V0 makes to the authorization's assumed flow

| Authorization assumed | Repository evidence says |
|---|---|
| "brief -> validation/reconciliation -> representation_sufficiency / MODEL_WARRANT" is a linear pipeline | MODEL_WARRANT is an **opt-in seam** (`warrant_enabled`), computed by the runtime AFTER validator PASS + reconciliation, only when enabled; it is not on the default path (`E-RT-routefields`, `E-RT-1438`) |
| "responsibility/workflow selection" is a routing step | Responsibility selection is **agent judgment**, deliberately un-automated; automatic fog-type routing is NOT ratified (`CONTEXT.md:127`, `ADR 0014`, `ADR 0018` SUPERSEDED) |
| "execution coordination" downstream of selection | The runtime *can* chain workflows but that chaining carries **no product-level authority**; a child workflow runs only after a separate explicit authority event (`ADR 0026`) |
| repo-sensemaker chooses the downstream workflow | repo-sensemaker only *recommends*; `recommended_workflow_id` is a planning field, not execution authority (`CONTEXT.md:142`) |
| "qualification / closure" is a pipeline stage | Closure is a distinct lifecycle **state**, not a stage; reconciliation and repair-verification are separate responsibilities with separate triggers (`CONTEXT.md:222`, `AGW:221-252`) |

## Three synchronized views (the architecture is only visible in all three)

- **Responsibility flow** — what question are we answering next? (`AGW:2`)
- **Artifact flow** — what durable information crosses each boundary? (`AGW:3`, `04-ARTIFACT-FLOWS.md`)
- **Authority flow** — who may know / decide / act / publish? (`AGW:4`, `05-AUTHORITY-MAP.md`)

Modeling only one hides the architecture — this is stated explicitly at
`docs/agent-native-operating-workflow.md:33`. V0's central bet is that making
the **authority** and **validation** views *structured and cross-linked* (not
prose) is where the value is.

## Component population (see `02-COMPONENTS.yaml` for the register)

| Kind | Count | Examples |
|---|---|---|
| skill | 17 | repo-sensemaker, workflow-planner, output-reconciler, repair-verifier |
| runtime / execution infra | 6 | workflow-runtime, skill-executor, gate-a-authorization, exploratory-execution |
| probe infra | 3 | probe-repo/repo_probes, probe_relationships |
| validator | 6 | validate-output, validate-artifact, validate-brief, validate-plan, field-contract-agreement tests |
| registry | 6 | artifact-contracts.yaml, workflow-registry.yaml, skill-registry.yaml, canonical-vocabulary.yaml, adr/README.md |
| research infra | 3 | reasoning/ slice, campaign_accounting, campaign_validation |
| canonical / research doc | 7 | CONTEXT.md, AGW, decision-orchestration-boundary, ADR corpus, control-model research agenda, Goal A protocol, CLAUDE.md |

## Load-bearing pairs (where the architecture concentrates)

1. **ADR 0013 + ADR 0014** — agent owns the loop; product core is the
   human-reviewed brief; routing deferred. Nearly every "is X ratified?"
   question resolves against this pair.
2. **artifact-contracts.yaml + validate-artifact.py/validate-brief.py** —
   the declared contract and its mechanical enforcement; the split between
   generic and conditional/blocking rules is itself load-bearing and
   historically defect-prone.
3. **workflow-runtime._resolve_artifact_path + skill-executor.expected_output_path**
   — one owner of path resolution (ADR 0010); a mismatch here once made an
   executor report success while the runtime saw ARTIFACT_NOT_FOUND.
4. **control-model research agenda + reasoning/ slice + runtime warrant seam**
   — research hypothesis, its tested implementation, and its single opt-in
   production hook; the boundary "research supports claims but does not
   authorize product behavior" runs straight through here.
