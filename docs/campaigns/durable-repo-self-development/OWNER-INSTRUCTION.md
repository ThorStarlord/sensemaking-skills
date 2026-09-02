# Campaign 2 owner instruction (verbatim)

```
SOURCE:    owner instruction delivered to the active coding agent (lead
           Campaign 2 controller) in conversation on 2026-09-02, launching
           Campaign 2.
AUTHORITY: this is Campaign 2's authority source. It is the owner's
           instruction, not an ADR, contract, or ratified product decision.
           Repository policy (accepted ADRs, CONTEXT.md, AGENTS.md, contracts,
           schemas) still governs what may be merged, ratified, or published.
STATUS:    preserved verbatim (outer formatting normalized to Markdown; no
           wording changed). Immutable campaign provenance. Do not silently
           rewrite this file as campaign understanding evolves. Operating
           refinements are recorded in CAMPAIGN-STATE.md, not by editing this
           file.
DERIVED:   CHARTER.md is the concise operating contract derived from this
           instruction and references this file as its authority source.
```

---

You are the lead coding-agent controller responsible for Campaign 2 in the `sensemaking-skills` repository.

Campaign 2 — Durable Repository-Level Self-Development

## Campaign Mission

Advance Sensemaking Skills from demonstrated responsibility-level artifact continuation toward:

Durable repository-level self-development in which independent fresh coding-agent controllers can reconstruct current product-development state, identify the highest-leverage warranted development boundary, perform substantial bounded engineering work, update durable product-development state, and leave the repository in a condition from which another fresh controller can continue without access to prior conversation context.

This is a real product-development campaign with an embedded controller-succession experiment.

The campaign must materially advance Sensemaking Skills.

The succession experiment exists because reliable controller replacement is itself an unresolved product-development capability boundary.

Do not select product work merely to make the experiment succeed.

Maintain:

```text
REAL PRODUCT DEVELOPMENT
+
CONTROLLED CONTROLLER-SUCCESSION EVIDENCE
=
CAMPAIGN 2
```

The campaign mission may be broad.

Execution must remain bounded.

## Authority and Precedence

This prompt is the owner's instruction launching Campaign 2.

Before substantive Campaign 2 work begins, preserve this instruction verbatim in an appropriate non-authoritative campaign location in the repository.

Prefer a structure such as:

```text
docs/campaigns/<campaign-2-name>/
    OWNER-INSTRUCTION.md
    CHARTER.md
    CAMPAIGN-STATE.md
    controllers/
```

The exact location may follow repository convention.

### Owner Instruction

`OWNER-INSTRUCTION.md` preserves this prompt verbatim.

It is immutable campaign provenance.

Do not silently rewrite it as campaign understanding evolves.

### Campaign Charter

Derive a concise `CHARTER.md` from the owner instruction containing only the durable campaign-level operating contract:

```text
MISSION
AUTHORITY
NON-NEGOTIABLE CONSTRAINTS
ACCEPTANCE CONDITIONS
STOPPING RULES
OWNER-RESERVED DECISIONS
```

The charter must reference the preserved owner instruction as its authority source.

The charter is intended to be easier for fresh controllers to reconstruct than the full operating prompt.

Do not use the charter to silently change the owner's instruction.

If an operating detail proves poorly formulated, record the refinement in campaign state rather than retroactively editing the owner instruction.

### Campaign State

`CAMPAIGN-STATE.md` contains evolving interpretation:

```text
capability assessments
evidence
task rationale
uncertainties
strategic alternatives
failure observations
controller observations
evidence ceilings
strategic frontier
integration state
```

The campaign state is not immutable.

Preserve important prior assessments rather than rewriting history as if earlier controllers always knew the current answer.

### Controller Checkpoints

Each semantic controller must produce controller-specific durable checkpoints.

Prefer files such as:

```text
controllers/A-reconstruction-and-selection.md
controllers/A-handoff.md
controllers/B-reconstruction-and-selection.md
controllers/B-cycle-result.md
```

These checkpoints should preserve what the controller believed at that point in time.

Do not retrospectively rewrite them merely because later evidence changes the campaign's understanding.

## Product Authority Remains External to the Campaign

The Campaign 2 charter, campaign state, controller checkpoints, reports, and experimental conclusions are not automatically authoritative product architecture.

Repository policy, accepted ADRs, contracts, schemas, and other currently authoritative product documents continue to govern the product.

Maintain:

```text
CAMPAIGN EVIDENCE
!=
PRODUCT RATIFICATION

CAMPAIGN IMPLEMENTATION
!=
INTEGRATED PRODUCT STATE

CONTROLLER RECOMMENDATION
!=
OWNER DECISION
```

When sources conflict, reason with this precedence:

```text
OWNER-RESERVED DECISION
or accepted repository authority
    ↓
current authoritative repository contracts / ADRs / policies
    ↓
current integrated repository behavior
    ↓
Campaign 2 candidate implementation
    ↓
Campaign 2 semantic state
    ↓
controller inference
```

Do not use this hierarchy mechanically when two sources govern different questions.

Use it to prevent campaign interpretation from silently overriding product authority.

## Campaign Control Roles

Explicitly distinguish three roles.

### 1. Campaign Owner

The owner:

* launches Campaign 2;
* grants campaign authority;
* retains reserved decisions;
* may expand or narrow authority;
* controls merge or publication where not otherwise granted;
* may terminate the campaign.

### 2. Mechanical Campaign Harness

The mechanical campaign harness exists only to make controller succession possible.

It may:

* provision or select an exact repository state;
* create fresh contexts;
* launch successor controllers;
* provide the allowed bootstrap;
* provide paths to durable sources;
* expose Git/GitHub capabilities;
* record handoff provenance;
* transfer mechanical outputs;
* preserve exact commits and worktrees.

It must not:

* interpret the product frontier;
* rank strategic boundaries;
* choose the successor's task;
* summarize predecessor reasoning;
* tell the successor which subsystem matters;
* reinterpret campaign state;
* silently alter the successor's semantic conclusions.

Maintain:

```text
MECHANICAL CAMPAIGN HARNESS
!=
SEMANTIC CAMPAIGN CONTROLLER
```

A persistent mechanical harness does not invalidate controller succession if it performs only mechanical functions.

### 3. Semantic Campaign Controller

The active semantic controller owns:

```text
mission reconstruction
capability reconstruction
strategic boundary assessment
task selection
bounded engineering
validation interpretation
campaign-state synthesis
handoff preparation
campaign closure assessment
```

Only one context should own semantic campaign continuation at a time unless Campaign 2 explicitly discovers a warranted reason to test a different model.

## What Qualifies as a Fresh Controller

A successor qualifies as a genuinely fresh semantic controller only when the strongest available evidence supports all of the following:

1. it has a new model/agent context;
2. it has no inherited conversation transcript from the predecessor;
3. it has no inherited predecessor private reasoning;
4. no automatic summary supplies predecessor strategic conclusions;
5. the exact bootstrap supplied to it is recorded;
6. it has direct access to the handoff repository state;
7. it has access to the durable sources it is allowed to use;
8. it has the necessary Git/GitHub/validation capabilities;
9. it may reject the predecessor's capability-frontier assessment;
10. it owns semantic selection of the next task;
11. the predecessor cannot rewrite the successor's checkpoint;
12. after relinquishment, the predecessor cannot resume campaign direction.

A fresh worker performing a task chosen by a persistent dispatcher is not enough.

Maintain:

```text
FRESH WORKER
!=
FRESH CONTROLLER
```

A child subagent may count as a fresh controller only if the execution environment actually provides the isolation and independent semantic ownership above.

Do not infer isolation merely because the tool calls the context a "subagent."

If isolation cannot be established strongly enough to support the claim, record:

```text
SUCCESSION_ISOLATION_UNVERIFIED
```

and narrow Campaign 2's conclusion accordingly.

## Campaign 2 Execution Authority

The active Campaign 2 controller is explicitly authorized to perform the following actions when warranted.

### Authorized Repository Reads

You MAY:

* inspect source code;
* inspect tests;
* inspect documentation;
* inspect ADRs;
* inspect contracts and schemas;
* inspect Git history;
* inspect branches and commits;
* inspect GitHub issues and pull requests;
* inspect CI results;
* inspect repository configuration;
* run ordinary repository analysis tools.

### Authorized Local Engineering Actions

You MAY:

* create Campaign 2 branches and worktrees;
* modify repository files on the Campaign 2 branch;
* add or modify implementation code;
* add or modify tests;
* modify documentation when warranted by product changes;
* run tests, validators, linters, type checks, build checks, probes, and qualification commands;
* create commits for coherent campaign work;
* maintain Campaign 2 evidence and state.

### Authorized Remote Campaign Actions

You MAY:

* push the Campaign 2 branch;
* push subsequent campaign commits;
* create a draft pull request if useful;
* update the draft PR description as evidence changes;
* inspect CI and qualification evidence associated with the campaign branch.

These permissions do not require every remote action.

Use remote actions only when they materially support product development, qualification, or durable campaign evidence.

### Not Authorized by Default

You MUST NOT, unless separately authorized by the owner or explicitly authorized by current repository policy:

* merge the Campaign 2 PR;
* deploy or publish externally;
* make an ADR accepted merely because Campaign 2 recommends it;
* change an owner-reserved product decision;
* treat campaign conclusions as canonical ratification;
* create, close, reopen, relabel, or materially modify GitHub issues merely for campaign bookkeeping;
* merge unrelated pull requests;
* alter protected repository policy merely to make Campaign 2 pass;
* infer owner preference from repository evidence.

If otherwise warranted progress crosses one of these boundaries, classify it as:

```text
OWNER_DECISION_REQUIRED
```

rather than manufacturing authority.

Maintain:

```text
evidence
!=
authority

recommendation
!=
selection
!=
execution authorization

implementation
!=
ratification

promotion
!=
merge
```

## Bootstrap Constraint

You are building Sensemaking Skills, but Sensemaking Skills must not control Campaign 2 itself.

Do not use as the semantic Campaign 2 controller:

* `repo-sensemaker`;
* `using-sensemaking`;
* registered Sensemaking Skills workflows;
* fog-to-workflow routing;
* workflow-runtime semantic routing;
* Skill-to-Skill continuation;
* proposed continuation hooks;
* any new self-hosted campaign-management mechanism created during Campaign 2.

The external coding agent owns Campaign 2.

Sensemaking Skills is the product under development, not the campaign-management system.

You MAY use existing Skills or workflows as product surfaces under examination or bounded subgraphs under test when independently warranted.

They must not silently take over repository-level strategic control.

You MAY and SHOULD use ordinary engineering infrastructure, including:

* repository documentation;
* ADRs;
* Git history;
* issues and PR history;
* tests;
* pytest;
* validators;
* `validate-repo.py`;
* build/package checks;
* Git;
* GitHub;
* CI;
* ordinary source inspection;
* independent fresh coding-agent contexts where supported.

Do not confuse:

```text
DO NOT SELF-HOST CAMPAIGN 2
```

with:

```text
DO NOT USE NORMAL REPOSITORY ENGINEERING TOOLS
```

## Starting Condition

PR #268 has been merged.

Treat current authoritative `origin/main` at Campaign 2 startup as the baseline repository state.

Do not rely on conversation context that preceded this campaign instruction.

Reconstruct Campaign 1's demonstrated state, limitations, product direction, authority model, and unresolved capability boundaries from durable repository and GitHub evidence.

Prefer current repository evidence over historical summaries.

Campaign 1 established useful evidence but did not establish all of the following:

* a fresh context taking over the complete semantic campaign-controller role;
* cross-controller semantic continuation;
* more than one independent dispatcher/controller;
* general autonomous repository self-development;
* production-grade reliability;
* broad implementation depth across all product surfaces;
* strict minimality of the durable state required for continuation.

Do not silently promote Campaign 1 evidence into those stronger claims.

## Mandatory Campaign Preflight

Before selecting strategic Task A:

1. verify repository identity;
2. inspect remotes;
3. inspect current branch;
4. inspect working-tree state;
5. fetch authoritative remote refs;
6. record exact current `origin/main`;
7. verify that PR #268 is an ancestor of that starting state;
8. verify required Git capabilities;
9. verify GitHub read capability;
10. verify push/PR capability if remote campaign actions are expected;
11. verify the relevant repository qualification commands;
12. verify that a genuinely fresh controller context can be instantiated;
13. verify that the successor can access the required repository, GitHub, and validation tools;
14. establish how the exact successor bootstrap will be recorded;
15. establish how predecessor semantic control will terminate at handoff.

If the defining fresh-controller experiment cannot be executed in the current environment, stop before substantial Task A work with:

```text
EXTERNAL_BLOCKER
```

unless the problem can be repaired mechanically without changing the experiment's meaning.

Do not complete a long first strategic cycle only to discover afterward that genuine controller replacement cannot be tested.

## Initial Repository Setup Order

Use this sequence rather than committing campaign files before a campaign branch exists.

1. complete the mandatory preflight;
2. fetch authoritative remote refs;
3. record exact starting `origin/main` SHA;
4. verify PR #268 is integrated into that baseline;
5. create a clean Campaign 2 branch/worktree from the recorded baseline;
6. preserve this owner instruction verbatim;
7. create the concise Campaign 2 charter;
8. create the initial Campaign 2 state record;
9. establish controller-checkpoint storage;
10. record startup provenance;
11. commit the Campaign 2 bootstrap;
12. push the bootstrap checkpoint if remote publication materially helps;
13. reconstruct current product/capability state;
14. compare plausible strategic boundaries;
15. select Task A.

Do not modify `main` merely to establish Campaign 2.

## Three Authority Planes of Repository State

Every controller must distinguish three planes.

### 1. Integrated Product State

```text
INTEGRATED PRODUCT STATE
=
current authoritative origin/main
+
accepted product authority
+
merged executable behavior
```

This represents what the repository currently has as integrated product state.

### 2. Campaign Candidate State

```text
CAMPAIGN CANDIDATE STATE
=
the exact Campaign 2 branch/head
including validated but unmerged campaign changes
```

Candidate changes are real repository facts.

They are not automatically ratified or integrated product state.

### 3. Campaign Semantic State

```text
CAMPAIGN SEMANTIC STATE
=
rationale
capability assessments
strategic alternatives
evidence ceilings
uncertainties
owner decisions
reopening conditions
controller observations
```

This is strategic memory.

It is not executable product truth.

Before every strategic selection and controller handoff, record at least:

```text
CURRENT ORIGIN/MAIN HEAD:

CAMPAIGN HEAD:

CAMPAIGN BASE:

MAIN DRIFT SINCE CAMPAIGN START:

CANDIDATE CHANGES NOT ON MAIN:

RATIFICATION / MERGE STATUS:

WHICH CAPABILITY CLAIMS APPLY ONLY TO THE CANDIDATE:

WHICH CLAIMS APPLY TO INTEGRATED MAIN:
```

Do not allow an unmerged Campaign 2 implementation to silently become "current product state."

Do not ignore it merely because it is unmerged either.

A successor must reason about both integrated state and the candidate state it actually inherited.

## Main-Branch Drift Policy

Before every new repository-level strategic selection:

1. fetch current remote refs;
2. record current `origin/main`;
3. compare it with the Campaign 2 base and current campaign HEAD;
4. inspect intervening main changes when materially relevant;
5. determine whether they affect the campaign warrant, capability frontier, contracts, or qualification baseline.

Do not automatically merge or rebase `main` merely because it advanced.

If new main changes materially affect Campaign 2, explicitly choose among:

```text
CONTINUE AGAINST RECORDED BASE

INCORPORATE RELEVANT MAIN CHANGE

REPLAN STRATEGIC TASK

OWNER_DECISION_REQUIRED

EXTERNAL_BLOCKER
```

Any incorporated main change must be qualified as part of the new candidate.

## Central Campaign Question

The primary question is:

What is the smallest coherent product capability required for repository-level development direction to survive independent campaign-controller replacement and continue producing strategically warranted engineering work?

Supporting questions:

What durable information is sufficiently valuable for a fresh controller to distinguish the next strategically consequential product capability from merely the nearest visible repository defect?

Which information should survive controller replacement as durable semantic state, and which information should instead be re-derived from authoritative repository or GitHub evidence?

Which part of the demonstrated continuation capability belongs in the product, and which part exists only because Campaign 2 itself requires experimental control?

Do not answer these questions abstractly when real implementation and real controller succession can answer them.

Build and evaluate the product.

## Minimality Claim Ceiling

A successful controller succession using a particular durable-state arrangement demonstrates:

```text
SUFFICIENCY
```

It does not automatically demonstrate:

```text
STRICT MINIMALITY
```

Strict minimality requires comparative evidence.

Examples include:

* a materially smaller state candidate also being tested;
* information being deliberately withheld and producing a classified failure;
* a staged-reveal comparison;
* repeated successor evidence showing specific state fields are unnecessary;
* a real omission or reconstruction failure demonstrating that a missing element matters.

Without comparative evidence, Campaign 2 may conclude:

```text
SMALLEST CURRENTLY SUPPORTED CANDIDATE
```

or:

```text
SUPPORTED BUT NOT FULLY DEMONSTRATED
```

Do not call a rich successful handoff the proven smallest possible capability merely because it worked.

If a lightweight minimality probe can be performed without distorting real product development, prefer it.

Do not create an elaborate experimental framework merely to prove theoretical minimality.

## Core Campaign Architecture

The active semantic controller owns this loop:

```text
PRODUCT MISSION
    ↓
RECONSTRUCT INTEGRATED PRODUCT STATE
    ↓
RECONSTRUCT CAMPAIGN CANDIDATE STATE
    ↓
RECONSTRUCT CAMPAIGN SEMANTIC STATE
    ↓
IDENTIFY HIGHEST-LEVERAGE UNRESOLVED CAPABILITY BOUNDARY
    ↓
IDENTIFY DECISION-CHANGING UNCERTAINTY
    ↓
SELECT ONE BOUNDED REPOSITORY-LEVEL TASK
    ↓
EXECUTE THROUGH BOUNDED RESPONSIBILITIES
    ↓
VALIDATE
    ↓
UPDATE PRODUCT SURFACES WHERE WARRANTED
    ↓
UPDATE CAMPAIGN SEMANTIC STATE
    ↓
REASSESS PRODUCT MISSION
    ↓
MANDATORY FRESH CONTROLLER HANDOFF
    ↓
PREVIOUS CONTROLLER RELINQUISHES SEMANTIC CONTROL
    ↓
FRESH CONTROLLER RECONSTRUCTS CAMPAIGN
    ↓
FRESH CONTROLLER REVERIFIES CONSEQUENTIAL CLAIMS
    ↓
FRESH CONTROLLER INDEPENDENTLY ASSESSES CAPABILITY FRONTIER
    ↓
FRESH CONTROLLER SELECTS NEXT WARRANTED TASK
    ↓
CONTINUE
```

The campaign itself is high-scope and high-complexity.

Individual execution units must remain bounded.

Do not attempt the mission as one monolithic implementation.

## Definitions

Use these meanings consistently.

### Product Capability

A product capability is a repeatable product or operator behavior supported by repository surfaces and evidence.

A campaign assertion by itself is not a product capability.

### Campaign Capability

A campaign capability is something Campaign 2 has demonstrated that its controller/harness arrangement can reliably do.

Campaign capabilities and product capabilities may overlap, but they are not automatically identical.

### Legitimate Task Boundary

A task has reached its legitimate boundary when:

* its decision-changing uncertainty has been resolved sufficiently;
* the warranted change has been implemented, rejected, or ruled unnecessary;
* relevant validation has been completed;
* remaining work requires a new campaign warrant rather than merely extending the current task.

### Independent Selection

Independent selection means:

```text
INDEPENDENT DECISION OWNERSHIP
```

It does not necessarily mean:

```text
NO EXPOSURE TO PREDECESSOR RATIONALE
```

A successor may read predecessor rationale.

It must remain free to reject it.

Claims of blind or unanchored reproduction require separate evidence.

## Strategic Selection Gate

Before promoting anything into an active repository-level campaign task, establish:

```text
PRODUCT CAPABILITY AFFECTED:

CURRENT LIMITATION:

EVIDENCE THE LIMITATION EXISTS:

INTENDED PRODUCT USER OR OPERATOR:

USER- OR OPERATOR-OBSERVABLE VALUE:

WHY IT MATERIALLY CONSTRAINS THE CAMPAIGN MISSION:

WHAT PRODUCT CAPABILITY BECOMES STRONGER IF SOLVED:

WHY THIS IS PRODUCT ADVANCEMENT RATHER THAN CAMPAIGN INSTRUMENTATION:

WHY THIS TASK WOULD REMAIN WARRANTED IF THE SUCCESSION ACCEPTANCE CONDITION
WERE ALREADY SATISFIED:

WHY THIS IS A STRATEGIC DEVELOPMENT TASK RATHER THAN MERELY A NEARBY DEFECT:

DECISION-CHANGING UNCERTAINTY:

BOUNDED TASK:

EXPECTED EVIDENCE THAT WOULD CHANGE THE CAPABILITY ASSESSMENT:
```

Do not select work merely because it is:

* visible;
* easy;
* recently discussed;
* already represented by an issue;
* locally inconsistent;
* stale documentation;
* failing only in an irrelevant local environment;
* adjacent to the last completed task;
* convenient for satisfying Campaign 2 acceptance conditions.

A local defect may become the selected task when resolving it materially advances a campaign-relevant product capability.

## Strategic vs. Local Work

Maintain:

```text
LOCAL WARRANT
Why should this line/file behavior change?

TASK WARRANT
Why is this responsibility necessary to complete the selected task?

CAMPAIGN WARRANT
Why should this repository-level task exist now relative to the product mission?
```

A repository-level task enters the campaign only when its campaign warrant is clear.

Do not allow Campaign 2 to degrade into repository cleanup.

## Strategic Alternatives

For each repository-level strategic selection:

1. identify the capability frontier;
2. identify plausible competing capability boundaries;
3. select the highest-leverage warranted boundary.

When repository evidence genuinely supports multiple serious alternatives, record at least two.

Do not manufacture alternatives merely to satisfy the format.

For each serious alternative:

```text
CANDIDATE BOUNDARY:

WHY IT IS PLAUSIBLE:

WHAT EVIDENCE SUPPORTS IT:

WHY IT IS OR IS NOT WARRANTED NOW:
```

Then record:

```text
SELECTED BOUNDARY:

WHY IT DOMINATES THE ALTERNATIVES:

DECISION-CHANGING UNCERTAINTY:

BOUNDED TASK:
```

Do not use numeric scoring or weighted rankings unless an existing justified repository mechanism requires them.

The goal is strategic discrimination, not artificial mathematics.

## Substantive Product Advancement

At least one Campaign 2 strategic cycle must produce either:

1. substantive product implementation whose complexity arises naturally from the selected capability boundary; or
2. an equivalently consequential product-development result.

A naturally warranted implementation may span coherent surfaces such as:

```text
product semantics
→ domain / artifact representation
→ producer or control behavior
→ consumer behavior
→ validation
→ regression tests
→ documentation
→ qualification
```

Do not require all of these.

Do not require a `src/` change merely because Campaign 1 did not exercise one.

Do not count changed files, lines, or components as a proxy for importance.

Do not enlarge a sufficient implementation merely to make Campaign 2 appear substantial.

### Equivalently Consequential Result

An implementation-light result counts only when it materially changes real product direction.

Examples:

```text
verified premise invalidation

product-boundary correction

authority-bound decision packet that prevents otherwise warranted implementation

architectural conclusion that materially redirects planned engineering
```

Documentation that merely restates already-known facts does not satisfy this requirement.

If the highest-leverage finding genuinely warrants little or no implementation, record the evidence rather than manufacturing a large patch.

## Do Not Predetermine the Product Solution

Do NOT assume repository-level development direction requires:

* a new `repository_development_state` artifact;
* YAML;
* JSON;
* a formal schema;
* a new Skill;
* changes to `repo-sensemaker`;
* a new workflow;
* hooks;
* a state machine;
* a router;
* new registry fields;
* a campaign-specific runtime;
* deterministic strategic selection;
* automatic controller spawning.

Those are hypotheses.

Discover the smallest coherent product change from evidence.

If Markdown remains sufficient, preserve Markdown.

If an existing artifact already carries the needed state, prefer it.

If no additional product mechanism is warranted, do not invent one.

If formal machinery becomes warranted, identify the demonstrated failure that requires it.

## Campaign Instrumentation Is Not Product Architecture

Campaign 2 requires durable campaign records for:

* experimental control;
* succession;
* reproducibility;
* auditability;
* reporting.

Do not infer from this that Sensemaking Skills therefore requires an equivalent production artifact.

Maintain:

```text
CAMPAIGN 2 CONTROL RECORD
=
campaign instrumentation and strategic memory

PRODUCT-LEVEL STATE MECHANISM
=
architectural hypothesis that must independently earn its existence
```

If Campaign 2 state proves useful, determine why before formalizing anything into the product.

## Three Kinds of Information

Distinguish:

### 1. Repository Factual State

Examples:

* source files;
* tests;
* ADRs;
* contracts;
* registries;
* commits;
* exact HEAD;
* CI;
* PR state;
* executable behavior.

This should normally be verified from repository or GitHub evidence.

### 2. Task State

Examples:

* current bounded responsibility;
* active uncertainty;
* implementation state;
* validation state;
* stop condition.

This is short-horizon execution state.

### 3. Campaign Semantic State

Examples:

* mission interpretation;
* demonstrated capabilities;
* material gaps;
* capability-frontier assessment;
* evidence ceilings;
* strategic rationale;
* rejected alternatives;
* owner decisions;
* reopening conditions;
* deferred work;
* capability implications.

This is expensive strategic information useful across controllers.

Do not collapse these classes.

## Durable-State Epistemics

Preserve the Campaign 1 lesson:

Durable state may remain useful even when some recorded factual claims become wrong or stale, provided consequential claims are reverified before action.

Use:

```text
DURABLE SEMANTIC STATE
    ↓
RECONSTRUCT INTENT / PRIOR DECISIONS / RATIONALE
    ↓
IDENTIFY CONSEQUENTIAL FACTUAL CLAIMS
    ↓
VERIFY THOSE CLAIMS
    ↓
UPDATE WARRANT
    ↓
ACT
```

Do not use:

```text
DURABLE STATE
    ↓
ASSUME ALL RECORDED FACTS REMAIN TRUE
    ↓
ACT
```

Durable campaign state should preferentially preserve information expensive to reconstruct, including:

* why a decision was made;
* why one boundary dominated another;
* rejected alternatives;
* evidence ceilings;
* owner decisions;
* reopening conditions;
* task rationale;
* capability implications;
* unresolved uncertainty;
* semantic context unavailable from source code alone.

Avoid unnecessarily duplicating:

* current file contents;
* trivial Git facts;
* volatile test results;
* easily re-derived repository inventory.

## Evidence-Origin Discipline

For strategically consequential conclusions, distinguish when useful:

```text
OWNER-INSTRUCTION-DERIVED

CHARTER-DERIVED

CAMPAIGN-STATE-DERIVED

REPOSITORY-VERIFIED

GITHUB-VERIFIED

CANDIDATE-HEAD-VERIFIED

CONTROLLER INFERENCE

OWNER DECISION
```

A conclusion may have several origins.

Examples:

```text
Campaign mission:
CHARTER-DERIVED

Previous task rationale:
CAMPAIGN-STATE-DERIVED

Previous implementation exists at handoff:
CANDIDATE-HEAD-VERIFIED

Previous work is merged:
GITHUB-VERIFIED

Current highest-leverage capability boundary:
CONTROLLER INFERENCE grounded in verified evidence
```

Do not annotate every sentence mechanically.

Use origin discipline where it materially strengthens controller-succession evidence.

## Candidate Architecture

Treat these as hypotheses.

### H1 — Agent-Owned Semantic Control

Semantic decisions about what repository-level task becomes warranted remain controller-owned.

### H2 — Durable Artifact-Mediated Continuation

Durable repository state may preserve enough expensive semantic information for independent controllers to continue consequential work.

### H3 — Verification-Bearing Handoff

Successors should verify consequential handoff facts rather than blindly trusting them.

### H4 — Strategic Outer Loop

Repository-level product development may benefit from durable representation of:

```text
mission
→ demonstrated capability state
→ material gaps
→ capability frontier
→ bounded task selection
```

distinct from short-horizon task execution.

### H5 — Inner Task Loop

Once a task is selected:

```text
task goal
→ uncertainty
→ bounded responsibility
→ evidence
→ validation
→ reassessment
→ closure
```

may remain sufficient.

### H6 — Deterministic Machinery Remains Mechanical

Scripts may own:

* validation;
* normalization;
* provenance;
* integrity checking;
* deterministic transformations;
* objective refereeing.

Do not assign semantic strategy to scripts unless the transition is demonstrably deterministic.

### H7 — Workflows Remain Optional Bounded Subgraphs

Do not restore workflows as campaign-level controllers.

Retain or formalize them only where real traces show stable useful sequencing.

### H8 — Hooks Remain Unwarranted Until Liveness Failure Exists

Do not implement a continuation hook merely because automatic continuation seems convenient.

First demonstrate a recurrent missed continuation event or comparable operational need.

### H9 — Campaign State and Product State May Differ

The information required to conduct Campaign 2 may exceed what a production controller actually needs.

Campaign 2 should discover that distinction.

### H10 — Successful Rich-State Continuation Proves Sufficiency, Not Minimality

Minimality requires comparative evidence.

Treat this as an explicit evidence ceiling.

## Bounded Responsibility Discipline

For every significant engineering responsibility:

### 1. Decision

What decision does this work support?

### 2. Uncertainty

What unresolved fact could make the apparent action wrong?

### 3. Evidence

Find the cheapest sufficient evidence.

### 4. Responsibility

Define one coherent engineering responsibility.

### 5. Execution

Perform only that responsibility.

### 6. Validation

Use the strongest relevant objective referee.

### 7. Consequence

Determine what changed at:

* local level;
* task level;
* product-capability level;
* campaign-evidence level.

### 8. Durable Update

Record consequential findings and rationale.

### 9. Reassess

Return to the strategic task or campaign mission.

Do not automatically follow the nearest local follow-up.

## Controller A — Initial Reconstruction

Controller A reconstructs:

```text
PRODUCT MISSION

CURRENT INTEGRATED PRODUCT STATE

CURRENT RATIFIED PRODUCT BOUNDARY

DEMONSTRATED PRODUCT CAPABILITIES

DEMONSTRATED CAMPAIGN CAPABILITIES

EVIDENCE CEILINGS

CURRENT MATERIAL GAPS

KNOWN OWNER DECISIONS

KNOWN DEFERRED WORK

LAST KNOWN CAPABILITY FRONTIER

CURRENTLY PLAUSIBLE CAPABILITY BOUNDARIES

AVAILABLE AUTHORITY

CURRENT ORIGIN/MAIN STATE

CAMPAIGN BASE

CURRENT CI / INTEGRATION STATE
```

Prefer current evidence over historical summaries.

Do not turn every defect into a candidate strategic task.

Controller A must durably checkpoint its reconstruction and strategic selection before implementing Task A.

### Controller A Strategic Cycle

Controller A must:

```text
reconstruct
→ compare strategic boundaries
→ select Task A
→ record selection
→ execute bounded responsibilities
→ validate
→ update candidate product state
→ update campaign semantic state
→ complete Task A to its legitimate boundary
```

Task A qualifies for the mandatory handoff because it is a repository-level strategically selected task, not because it meets an arbitrary size threshold.

Do not use the subjective term "major" as the handoff criterion.

### Mandatory Controller Turnover

After Task A reaches its legitimate task-level disposition and surviving state is committed, Controller A must cease owning semantic continuation.

This is a defining Campaign 2 requirement.

It must be genuine controller succession, not another fresh-worker dispatch.

### Pre-Handoff Repository Invariant

Before relinquishment:

1. complete Task A to its legitimate boundary;
2. run relevant validation;
3. update Campaign 2 semantic state;
4. commit all intended surviving campaign changes;
5. commit Controller A's cycle result;
6. create Controller A's handoff checkpoint;
7. record exact handoff SHA;
8. fetch and record current `origin/main`;
9. record candidate-vs-main state;
10. record relevant PR/CI observations;
11. ensure the working tree is clean.

If a clean working tree is genuinely inappropriate, every intentional uncommitted item must be explicitly identified and justified.

Invisible filesystem state must not become continuation state.

Prefer:

```text
FRESH CONTROLLER
→ EXACT COMMITTED HANDOFF STATE
```

over:

```text
FRESH CONTROLLER
→ PREDECESSOR WORKTREE LEFTOVERS
```

### Handoff Provenance

Every controller transfer must record:

```text
PREDECESSOR CONTROLLER ID:

SUCCESSOR CONTROLLER ID:

LAUNCH MECHANISM:

MODEL / AGENT TYPE, IF AVAILABLE:

CONTEXT-ISOLATION CLAIM:

EXACT BOOTSTRAP TEXT:

FILES / PATHS DISCLOSED:

REPOSITORY HANDOFF HEAD:

CURRENT ORIGIN/MAIN HEAD:

WORKTREE / CHECKOUT IDENTITY:

GIT CAPABILITIES:

GITHUB CAPABILITIES:

VALIDATION CAPABILITIES:

OUT-OF-BAND INFORMATION PROVIDED:

START TIME, IF AVAILABLE:

SUCCESSOR CHECKPOINT SHA:

PREDECESSOR ACCESS AFTER LAUNCH:

KNOWN ISOLATION LIMITATIONS:
```

Distinguish:

```text
DEMONSTRATED ISOLATION

HARNESS-REPORTED ISOLATION

CONTROLLER-ASSERTED ISOLATION

UNVERIFIABLE ISOLATION
```

Do not overstate independence beyond what the execution environment can establish.

### Controller A Relinquishment Rule

After the handoff checkpoint, Controller A may perform only the mechanical action required to instantiate Controller B.

Controller A must not:

* tell B what task to choose;
* summarize A's reasoning;
* rank candidate boundaries;
* identify which subsystem B should inspect first;
* explain what A believes the current frontier is;
* reinterpret the campaign state for B;
* critique B's strategic selection;
* give B A's predicted next action;
* revise B's checkpoint;
* veto B's selected task;
* redirect B after selection.

After relinquishment:

```text
CONTROLLER A
=
FORMER CONTROLLER
```

A does not regain semantic campaign ownership.

If retrospective comparison of A and B is useful, perform it only after B completes its selected strategic cycle or reaches a legitimate terminal disposition.

## Allowed Bootstrap for Fresh Controller B

Controller B receives only the minimum mechanical information necessary to locate durable state and operate the repository:

* access to the exact committed handoff repository state;
* the path to the committed Campaign 2 charter;
* the path to the durable Campaign 2 state record;
* notification that B is now the active semantic Campaign 2 controller;
* access to the normal Git/GitHub/validation capabilities required to verify evidence.

B must not receive out-of-band answers for:

* campaign mission;
* previous task rationale;
* capability frontier;
* available authority;
* material gaps;
* recommended next task;
* predecessor predictions.

A suitable bootstrap is:

```text
You are now the fresh independent semantic controller for Campaign 2.

You have access to the current Campaign 2 repository state.

The Campaign 2 charter is at:
<path>

The durable Campaign 2 state is at:
<path>

You do not have access to the previous controller's conversation or private
reasoning.

Reconstruct the campaign mission, authority, integrated product state,
candidate state, demonstrated capabilities, previous strategic work,
evidence ceilings, material gaps, and current development frontier from
durable sources and current repository/GitHub evidence.

Reverify consequential factual claims before acting.

A previously recorded capability frontier or next task is historical evidence,
not a command.

Independently determine the next strategically warranted repository-level task.

Before implementation, commit a controller-specific reconstruction and
selection checkpoint.
```

Do not expand this bootstrap into a hidden semantic handoff.

### Optional Minimality Probe

If the execution harness can cheaply support a staged-reveal reconstruction without compromising the real product-development cycle, Controller B may first perform a bounded repository/charter-only reconstruction before reading Campaign 2 semantic state.

The purpose would be to compare:

```text
WHAT THE REPOSITORY + CHARTER ALONE REVEAL

vs.

WHAT THE CAMPAIGN SEMANTIC STATE MATERIALLY ADDS
```

If performed:

1. checkpoint the repository/charter-only reconstruction first;
2. then read Campaign 2 semantic state;
3. record what materially changed;
4. distinguish saved work from redundant information;
5. proceed with normal strategic selection.

Do not perform this probe if it requires heavy artificial infrastructure.

If no comparative minimality probe occurs, preserve the strict-minimality evidence ceiling.

## Fresh Controller Reconstruction

Controller B must independently answer:

```text
1. What is the Campaign 2 mission?

2. What authority is available?

3. What authority remains reserved?

4. What is current integrated origin/main state?

5. What is the Campaign 2 handoff candidate state?

6. Which candidate changes are not integrated into main?

7. What product capabilities are currently demonstrated?

8. What campaign capabilities are demonstrated?

9. What evidence ceilings remain?

10. What changed during the previous strategic cycle?

11. Why had the previous task been selected?

12. Which consequential durable-state claims required reverification?

13. Which reverified claims were correct?

14. Which claims were incomplete, stale, overstated, or wrong?

15. What material product gaps remain?

16. What did the predecessor last assess as the capability frontier?

17. What capability now appears to constrain progress most after independent
    reassessment?

18. What serious alternative boundaries exist?

19. What bounded repository-level task is warranted next?

20. Does the predecessor's previously recorded candidate remain warranted,
    or should it be rejected or replaced?
```

B does not need to agree with A.

A different selection is valid when current evidence supports it.

### Mandatory Independent Selection Rule

Fields such as:

```text
next_task
recommended_next_action
current_capability_frontier
highest_leverage_boundary
```

must be interpreted as:

```text
LAST ASSESSED CANDIDATE
```

not:

```text
COMMAND
```

Prefer terminology such as:

```text
LAST ASSESSED CAPABILITY FRONTIER
```

The fresh controller owns the new decision.

Campaign continuation succeeds only if B can reconstruct, verify, compare, and justify a strategic decision.

Success does not require B to reproduce A's predicted next task.

### Mandatory Successor Checkpoint

Before Controller B performs Task B, it must write a controller-specific reconstruction and strategic-selection checkpoint.

That checkpoint must be:

* durable;
* committed;
* assigned an exact checkpoint SHA;
* created before Task B implementation;
* created before any predecessor semantic feedback.

Record at least:

```text
CONTROLLER IDENTITY / CONTEXT:

HANDOFF HEAD:

CURRENT ORIGIN/MAIN HEAD:

CAMPAIGN BASE:

MAIN DRIFT:

CANDIDATE CHANGES NOT ON MAIN:

MISSION RECONSTRUCTED:

AUTHORITY RECONSTRUCTED:

PREVIOUS STRATEGIC TASK:

WHY IT HAD BEEN SELECTED:

WHAT CHANGED:

CLAIMS REVERIFIED:

CLAIMS CORRECTED OR NARROWED:

DEMONSTRATED PRODUCT CAPABILITIES:

DEMONSTRATED CAMPAIGN CAPABILITIES:

EVIDENCE CEILINGS:

MATERIAL GAPS:

LAST ASSESSED FRONTIER FROM PRIOR STATE:

INDEPENDENTLY REASSESSED FRONTIER:

PLAUSIBLE ALTERNATIVE BOUNDARIES:

SELECTED BOUNDARY:

CAMPAIGN WARRANT:

WHY THIS IS REAL PRODUCT ADVANCEMENT:

DECISION-CHANGING UNCERTAINTY:

BOUNDED TASK:

MINIMALITY CLAIM CURRENTLY SUPPORTED:
```

Do not retroactively rewrite this checkpoint after Task B reveals whether the selection was successful.

Later campaign state may supersede its conclusions while preserving the historical checkpoint.

### Controller B Strategic Cycle

Controller B executes the independently selected Task B through bounded responsibilities.

Task B must either:

* materially advance a campaign-relevant product capability; or
* produce evidence that materially refines or invalidates the campaign's product-development architecture.

After Task B:

1. validate;
2. update appropriate product surfaces;
3. update campaign semantic state;
4. record what capability changed;
5. record remaining evidence ceilings;
6. record whether the previous frontier hypothesis survived;
7. record which architectural hypotheses strengthened, weakened, or failed;
8. record whether further Campaign 2 work would materially affect the central question.

At minimum Campaign 2 must establish:

```text
Controller A
→ reconstructs campaign
→ independently selects strategic Task A
→ executes Task A
→ validates
→ durable checkpoint
→ relinquishes semantic control

Mechanical harness
→ creates genuinely fresh Controller B
→ provides only allowed bootstrap

Controller B
→ reconstructs campaign
→ reverifies consequential claims
→ distinguishes integrated and candidate state
→ compares strategic boundaries
→ independently selects Task B
→ commits selection checkpoint
→ executes Task B
→ validates
→ updates durable state
```

A Controller C handoff is optional.

Use it only when additional succession evidence would materially change the Campaign 2 conclusion.

Do not perform another handoff merely to increase the count.

## Failure Classification

When controller succession, durable state, strategic selection, or baseline control fails, classify the failure before creating infrastructure.

Use:

```text
CAMPAIGN_STATE_INSUFFICIENT

STRATEGIC_SELECTION_UNSTABLE

HANDOFF_FACT_INCORRECT

HANDOFF_FACT_TRUST_FAILURE

PRODUCT_DIRECTION_AMBIGUITY

CAPABILITY_MODEL_MISSING

AUTHORITY_RECONSTRUCTION_FAILURE

CONTEXT_RECONSTRUCTION_COST_EXCESSIVE

CAPABILITY_DISCOVERY_FAILURE

MISSING_DURABLE_STATE

INCIDENTAL_CONTEXT_LOSS

HANDOFF_STATE_CONTAMINATION

SUCCESSION_ISOLATION_UNVERIFIED

BASELINE_DRIFT_MATERIAL

OTHER_DEMONSTRATED_FAILURE
```

Distinguish:

```text
HANDOFF_FACT_INCORRECT
=
durable state contained a stale or wrong consequential fact,
but verification caught it before wrong action
```

from:

```text
HANDOFF_FACT_TRUST_FAILURE
=
the successor trusted an incorrect consequential fact
and strategic selection or action was affected
```

The first can demonstrate healthy verification-bearing continuation.

The second demonstrates an epistemic failure.

For every meaningful failure:

```text
WHAT FAILED:

WHAT DECISION WAS AFFECTED:

WHAT INFORMATION WAS MISSING, MALFORMED, STALE, OR WRONG:

HOW THE FAILURE WAS DISCOVERED:

DID VERIFICATION PREVENT WRONG ACTION:

SMALLEST POSSIBLE REPAIR:

RECURRENCE EVIDENCE:

WHETHER PRODUCT INFRASTRUCTURE IS WARRANTED:

WHETHER THE FAILURE APPLIES TO PRODUCT, CAMPAIGN HARNESS, OR BOTH:
```

Do not jump from one failure directly to a general framework.

## Context-Cost Observation

For every fresh-controller reconstruction, record qualitatively:

```text
WHAT HAD TO BE REDISCOVERED FROM THE REPOSITORY:

WHAT HAD TO BE REDISCOVERED FROM GITHUB:

WHAT DURABLE STATE SAVED MATERIAL WORK:

WHAT DURABLE STATE WAS REDUNDANT:

WHAT REQUIRED REVERIFICATION:

WHAT WOULD HAVE BEEN DANGEROUS TO TRUST WITHOUT REVERIFICATION:

WHAT PRIOR RATIONALE WOULD HAVE BEEN EXPENSIVE TO RECONSTRUCT:

WHAT INFORMATION WAS CHEAPER TO RECONSTRUCT THAN MAINTAIN:

WHAT INFORMATION APPEARS VALUABLE ENOUGH TO PRESERVE:

WHAT INFORMATION APPEARS CAMPAIGN-SPECIFIC RATHER THAN PRODUCT-SPECIFIC:
```

Look for patterns such as:

```text
expensive semantic reconstruction
+
durable reuse
→ good preserved-state candidate

cheap factual reconstruction
+
high volatility
→ prefer reverification

dangerous if stale
→ preserve rationale/pointer, verify fact
```

Do not prematurely convert these observations into a schema.

## Formalization Rule

Do not formalize a new:

* artifact;
* schema;
* workflow;
* Skill;
* hook;
* router;
* state machine;
* semantic automation;

merely because a concept appears repeatedly.

Formalization becomes warranted when there is evidence of:

```text
RECURRING RESPONSIBILITY OR STATE REQUIREMENT
+
STABLE SEMANTICS
+
REPEATED MANUAL BURDEN / OMISSION / ERROR
+
MECHANICALLY USEFUL BOUNDARY
```

Otherwise preserve the lighter convention.

The existence of `CAMPAIGN-STATE.md` alone is not evidence for a canonical product-state artifact.

## Skill-System Observation

Although Sensemaking Skills' own Skills do not control Campaign 2, observe naturally recurring responsibilities.

Ask:

```text
Does this responsibility recur?

Are its inputs identifiable?

Are its outputs identifiable?

Is its boundary stable?

Would specialized instructions materially improve execution?

Would a Skill provide value beyond ordinary controller reasoning?
```

Do not create a Skill merely because a responsibility has a name.

Skill candidates are by-products of Campaign 2.

They become campaign work only when they independently pass the Strategic Selection Gate.

## Workflow-System Policy

PR #268 established a bounded disposition of the existing workflow system.

Do not reopen the entire workflow question without new evidence.

During Campaign 2:

* note naturally recurring responsibility sequences;
* use existing workflows only as independently useful bounded subgraphs;
* never use them as the semantic campaign controller;
* do not force tasks into workflows;
* do not retire or promote workflows without authority;
* do not turn Campaign 2 into a parallel workflow research campaign.

A future workflow should preferably be recovered from repeated successful traces rather than designed speculatively.

## Git and Engineering Discipline

For every coherent implementation unit:

* inspect current branch and exact HEAD;
* inspect current `origin/main` when strategically relevant;
* understand existing contracts and behavior;
* change the smallest coherent product surface;
* add regression coverage where warranted;
* run targeted validation;
* inspect the diff;
* run required broader qualification;
* preserve exact-head qualification claims accurately.

Maintain:

```text
TARGETED TEST PASS
!=
COMPLETE LOCAL QUALIFICATION
!=
PR-HEAD QUALIFICATION
!=
MERGE
!=
INTEGRATED-MAIN QUALIFICATION
```

Do not weaken tests merely to make Campaign 2 green.

If implementation reveals a deeper mismatch, follow evidence rather than the task's predicted result.

If a proposed change proves unnecessary or wrong, do not force it to preserve plan conformity.

## Campaign Branch Topology

Default to a single cumulative Campaign 2 branch unless strong evidence warrants another topology.

Prefer:

```text
main
  └── Campaign 2 branch
        ├── bootstrap
        ├── Controller A Task A
        ├── Controller A handoff
        ├── Controller B checkpoint
        └── Controller B Task B
```

Reasons:

* Controller B receives Task A's exact candidate state;
* succession evidence remains on one durable lineage;
* campaign qualification is easier to interpret.

Within the cumulative branch, keep strategic tasks as coherent commit ranges.

The final report and PR description must distinguish Task A and Task B clearly.

Do not introduce task branches or a campaign-control branch merely for theoretical cleanliness unless real review, integration, or concurrency needs warrant them.

## Durable Campaign 2 State

Maintain the evolving campaign state in an appropriate non-authoritative repository location.

Do not begin with a formal machine schema.

Preserve at least:

```text
CAMPAIGN MISSION INTERPRETATION

CHARTER PATH / AUTHORITY SOURCE

STARTING ORIGIN/MAIN STATE

CAMPAIGN BASE

CURRENT ORIGIN/MAIN OBSERVATION

CURRENT CAMPAIGN HEAD

CURRENT INTEGRATED PRODUCT ASSESSMENT

CURRENT CANDIDATE PRODUCT ASSESSMENT

DEMONSTRATED PRODUCT CAPABILITIES

DEMONSTRATED CAMPAIGN CAPABILITIES

EVIDENCE CEILINGS

COMPLETED STRATEGIC TASKS

WHY EACH TASK WAS SELECTED

ALTERNATIVES CONSIDERED

CAPABILITIES ADVANCED BY EACH TASK

OPEN MATERIAL GAPS

LAST ASSESSED CAPABILITY FRONTIER

ACTIVE DECISION-CHANGING UNCERTAINTIES

OWNER / AUTHORITY BOUNDARIES

REJECTED OR SUPERSEDED STRATEGIC OPTIONS

DEFERRED LOCAL FINDINGS

RELEVANT OBSERVED INTEGRATION / CI STATE

CONTROLLER-HANDOFF TRACE

FAILURE OBSERVATIONS

CONTEXT-COST OBSERVATIONS

MINIMALITY EVIDENCE / CLAIM CEILING

CAMPAIGN ACCEPTANCE STATUS
```

Prefer durable rationale over duplicated cheap facts.

Preserve historical assessments without pretending they remain current forever.

## Campaign Acceptance Conditions

Campaign 2 is complete only when the strongest defensible version of the materially relevant conditions below is satisfied.

### 1. Fresh Semantic Controller Succession

At least one genuinely fresh controller takes over semantic campaign control without predecessor conversation or private reasoning.

### 2. Isolation Evidence

The campaign records enough handoff provenance to state honestly what level of controller isolation was established.

### 3. Durable Mission Reconstruction

The successor reconstructs the campaign mission from durable sources rather than receiving it as an out-of-band answer.

### 4. Authority Reconstruction

The successor reconstructs available and reserved authority.

### 5. State-Plane Reconstruction

The successor distinguishes:

* integrated product state;
* Campaign 2 candidate state;
* campaign semantic state.

### 6. Strategic Reconstruction

The successor reconstructs:

* demonstrated product capabilities;
* demonstrated campaign capabilities;
* material limitations;
* previous strategic-task rationale;
* changed repository state;
* evidence ceilings;
* relevant owner decisions;
* predecessor frontier assessment.

### 7. Verification-Bearing Continuation

Consequential factual handoff claims are checked before action.

### 8. Independent Next-Task Selection

The successor evaluates plausible strategic boundaries and independently chooses a warranted repository-level task.

### 9. Immutable Successor Checkpoint

The successor's reconstruction and selection are durably committed before implementation and before predecessor semantic feedback.

### 10. Real Product Advancement

Campaign 2 produces substantive product implementation or an equivalently consequential result whose scope arises naturally from strategic product evidence.

### 11. Second Strategic Cycle

Fresh Controller B executes another strategically warranted task against the changed candidate state.

### 12. Strategic/Local Distinction

Task selection demonstrably distinguishes high-leverage capability work from merely nearby defects.

### 13. No Premature Infrastructure

No schema, hook, state machine, semantic router, broad workflow expansion, or equivalent framework is added without demonstrated need.

### 14. Architecture Remains Revisable

Evidence that contradicts Campaign 2's hypotheses results in narrowing, refinement, or rejection.

### 15. Relevant Product Consistency

No known material contradiction remains among product surfaces:

* changed by Campaign 2;
* relied upon by Campaign 2;
* necessary to support its consequential product claims.

Unrelated inconsistencies may be deferred.

### 16. Qualification

The candidate passes the appropriate complete qualification, or remaining unsatisfied conditions are accurately classified.

### 17. Honest Evidence Ceilings

Remaining limitations are explicit.

### 18. Minimality Honesty

Campaign 2 does not claim strict minimality unless comparative evidence supports it.

### 19. Succession Integrity

The predecessor did not resume semantic control over the successor's strategic cycle.

These are evidence conditions, not performative boxes.

If a condition proves poorly formulated, record the reason and use the narrower defensible interpretation without silently rewriting the owner instruction.

## Campaign Closure Rule

Campaign 2 does not need to solve general autonomous repository development.

After the mandatory A → B succession and two strategic cycles, reassess:

What is the smallest coherent product capability currently supported by evidence as sufficient for repository-level development direction to survive independent controller replacement?

Close Campaign 2 when:

1. the central question can be answered at an honest evidence level;
2. controller-succession evidence exists;
3. substantive product advancement occurred or was legitimately ruled unwarranted;
4. no remaining material gap is necessary to evaluate the Campaign 2 question;
5. broader limitations can be recorded as evidence ceilings, deferred work, or future campaign questions.

Do not continue merely because:

* the repository contains defects;
* autonomous development could improve further;
* another useful feature exists;
* production reliability is incomplete;
* another handoff could generate more evidence;
* strict theoretical minimality has not been mathematically proven.

Remaining useful work does not automatically mean Campaign 2 remains open.

## Campaign Stopping Dispositions

Continue autonomously until exactly one becomes justified:

```text
CAMPAIGN_COMPLETE

OWNER_DECISION_REQUIRED

EXTERNAL_BLOCKER

CAMPAIGN_PREMISE_INVALIDATED
```

Do not stop merely because:

* one task finished;
* one PR exists;
* one handoff succeeded;
* one implementation works;
* another local issue appears;
* hidden context becomes large.

If context pressure becomes material:

1. update durable state;
2. commit the current checkpoint;
3. complete the current responsibility to the safest legitimate boundary;
4. terminate semantic ownership;
5. continue through a fresh controller where possible.

## Campaign Premise Invalidation

Use:

```text
CAMPAIGN_PREMISE_INVALIDATED
```

when evidence shows the central Campaign 2 framing is materially wrong.

Examples:

* repository-level strategic direction is already cheaply reconstructible without any additional product capability;
* controller succession cannot meaningfully be distinguished from ordinary repository reconstruction in the available environment;
* Campaign 2's assumed capability frontier came from an incorrect interpretation of Campaign 1;
* an existing product mechanism already solves the proposed gap;
* the state believed necessary proves to be campaign instrumentation with no product relevance.

Do not force implementation merely to preserve the campaign hypothesis.

A well-supported invalidation is legitimate product-development evidence.

## Campaign 2 Final Report

At legitimate termination, produce a final durable report.

### 1. Mission Outcome

What product capability materially changed?

What did Campaign 2 establish about durable repository-level self-development?

What did it not establish?

### 2. Starting State

Report:

* starting `origin/main`;
* Campaign 2 base;
* what Campaign 1 already demonstrated;
* what remained unproven.

### 3. Strategic Task Trace

For each repository-level task:

```text
TASK:

CONTROLLER:

CAMPAIGN WARRANT:

USER / OPERATOR VALUE:

ALTERNATIVE BOUNDARIES:

DECISION-CHANGING UNCERTAINTY:

BOUNDED RESPONSIBILITIES:

PRODUCT CAPABILITY ADVANCED:

EVIDENCE PRODUCED:

EVIDENCE CEILING REMAINING:
```

### 4. Controller Succession Trace

For every controller:

```text
CONTROLLER IDENTITY / CONTEXT:

HANDOFF HEAD:

ORIGIN/MAIN AT HANDOFF:

DURABLE SOURCES RECEIVED:

WHAT WAS RECONSTRUCTED:

WHAT HAD TO BE REDISCOVERED:

WHAT REQUIRED REVERIFICATION:

WHAT PRIOR FACTS WERE STALE OR WRONG:

WHAT PREDECESSOR FRONTIER WAS ACCEPTED OR REJECTED:

ALTERNATIVE CAPABILITY BOUNDARIES:

TASK INDEPENDENTLY SELECTED:

CHECKPOINT SHA:

HANDOFF PRODUCED:
```

### 5. Independence and Harness Assessment

For each succession:

```text
LAUNCH MECHANISM:

ISOLATION EVIDENCE:

EXACT BOOTSTRAP:

OUT-OF-BAND INFORMATION:

INFORMATION INTENTIONALLY WITHHELD:

WHETHER CHECKPOINT PRECEDED FEEDBACK:

WHETHER PREDECESSOR RETAINED SEMANTIC CONTROL:

KNOWN HARNESS LIMITATIONS:

STRONGEST DEFENSIBLE SUCCESSION CLAIM:
```

### 6. Integrated vs Candidate State

Explain:

* current integrated `main`;
* current campaign candidate;
* unmerged changes;
* ratification status;
* which capability conclusions apply only to the candidate.

### 7. Implementation

Describe substantive code/product changes.

Explain why their scope was naturally warranted rather than manufactured.

### 8. Durable-State Assessment

What information:

* was essential;
* saved material work;
* was redundant;
* became stale;
* was wrong;
* required reverification;
* was cheaper to reconstruct;
* appears campaign-specific;
* appears product-worthy.

### 9. Strategic-Selection Assessment

Did controllers:

* distinguish frontier from local defects;
* consider real alternatives;
* independently reassess predecessor conclusions;
* maintain user/operator product value;
* avoid selecting work merely to satisfy the experiment?

Where did strategic selection remain unstable?

### 10. Minimality Assessment

State explicitly:

```text
WHAT STATE ARRANGEMENT WAS SHOWN SUFFICIENT:

WHAT COMPARATIVE EVIDENCE EXISTS:

WHAT WAS SHOWN REDUNDANT:

WHAT WAS SHOWN NECESSARY:

WHAT WAS NOT TESTED:

WHETHER STRICT MINIMALITY WAS DEMONSTRATED:
```

Do not infer minimality from sufficiency.

### 11. Context-Cost Assessment

For each transition:

```text
REPOSITORY REDISCOVERY:

GITHUB REDISCOVERY:

DURABLE-STATE VALUE:

REDUNDANT STATE:

DANGEROUS-TO-TRUST STATE:

EXPENSIVE RATIONALE PRESERVED:
```

Use qualitative evidence.

Do not invent precision that was not measured.

### 12. Failure Assessment

For every material failure:

```text
FAILURE CLASS:

DECISION AFFECTED:

MISSING / STALE / WRONG INFORMATION:

VERIFICATION OUTCOME:

SMALLEST REPAIR:

RECURRENCE EVIDENCE:

PRODUCT OR HARNESS FAILURE:

WHETHER INFRASTRUCTURE IS WARRANTED:
```

### 13. Architecture Consequences

Assess evidence for:

* strategic outer loop;
* inner task loop;
* artifact-mediated continuation;
* independent controller succession;
* campaign-state/product-state distinction;
* Skill formalization;
* workflow role;
* deterministic machinery;
* hooks;
* formal repository-development-state representation;
* strict minimality.

For each important claim classify it as:

```text
DEMONSTRATED

SUPPORTED BUT NOT FULLY DEMONSTRATED

STILL HYPOTHETICAL

REFUTED
```

### 14. Qualification

Report:

* exact candidate branch/head;
* exact current `origin/main`;
* targeted tests;
* broader tests;
* validators;
* build/package checks;
* CI;
* PR state;
* merge state;
* integrated-main state where applicable;
* remaining exceptions.

Do not overstate qualification.

### 15. Remaining Limitations

Separate:

* product limitations;
* engineering debt;
* unvalidated hypotheses;
* owner decisions;
* environment blockers;
* intentionally deferred work;
* Campaign 2 experimental limitations;
* harness limitations;
* isolation limitations;
* minimality limitations.

### 16. Answer to the Central Question

Give the strongest evidence-supported answer to:

What is the smallest coherent product capability required for repository-level development direction to survive independent campaign-controller replacement and continue producing strategically warranted engineering work?

Distinguish clearly:

```text
DEMONSTRATED SUFFICIENT

SUPPORTED AS THE SMALLEST CURRENTLY EVIDENCED CANDIDATE

STRICT MINIMALITY DEMONSTRATED

SUPPORTED BUT NOT FULLY DEMONSTRATED

STILL HYPOTHETICAL

REFUTED
```

Do not make stronger claims than the evidence supports.

### 17. Campaign Disposition

Exactly one:

```text
CAMPAIGN_COMPLETE

OWNER_DECISION_REQUIRED

EXTERNAL_BLOCKER

CAMPAIGN_PREMISE_INVALIDATED
```

Explain why.

## Final Operating Principles

Keep these active throughout Campaign 2:

The campaign mission may be broad; execution must remain bounded.

Product development is the purpose; controller succession is a capability being tested through real product work.

Strategic decomposition chooses the repository-level task.

Task decomposition chooses the bounded engineering responsibility.

Integrated product state, Campaign 2 candidate state, and campaign semantic state are different things.

An unmerged candidate is real repository state but not automatically ratified product state.

A predecessor's recommendation is historical evidence, not a command.

A predecessor's capability frontier is a prior assessment, not current truth.

A fresh controller must reconstruct, verify, compare, and decide.

Independent selection means independent decision ownership.

Repository and GitHub evidence outrank incorrect handoff facts.

Durable state should preserve expensive semantic rationale rather than duplicate cheap facts.

Volatile facts should be reverified at the consequential moment.

Successful rich-state continuation demonstrates sufficiency, not automatically minimality.

Campaign instrumentation is not automatically product architecture.

Mechanical campaign harnesses are not semantic controllers.

Controller replacement succeeds only when justified decision-making authority actually transfers.

The predecessor does not regain semantic campaign control after relinquishment.

Evidence warrants work. Authority permits action.

Semantic decisions remain controller-owned unless they are demonstrably deterministic.

Do not create infrastructure before demonstrated failure warrants it.

Do not mistake local cleanliness for strategic product progress.

Do not enlarge implementation merely to make the campaign look consequential.

Do not make Sensemaking Skills self-host Campaign 2 before the product earns that role.

Do not keep Campaign 2 open merely because further development would be useful.

Continue until independent semantic controller succession, strategically warranted product advancement, and sufficient evidence to answer the Campaign 2 question have been demonstrated, genuinely blocked, or invalidated.

## Three Campaign Aphorisms

It is not controller succession because another context runs; it is actually succession when justified semantic decision-making authority transfers to that context.

It is not repository truth and it is not campaign memory alone; it is actually a disciplined separation between integrated authority, candidate behavior, and preserved strategic rationale.

The smallest continuation capability is actually the smallest one supported by comparative evidence, not merely the first rich handoff that succeeds.
