# Campaign 3 owner instruction (verbatim)

```
SOURCE:    owner instruction delivered to the active coding agent (lead
           Campaign 3 controller) in conversation on 2026-09-02, launching
           Campaign 3.
AUTHORITY: this is Campaign 3's authority source. It is the owner's
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

You are the lead coding-agent controller responsible for Campaign 3 in the `sensemaking-skills` repository.

Campaign 3 — Durable Architectural Continuity During Coupled Implementation

## Campaign Mission

Advance Sensemaking Skills through the highest-leverage currently warranted product development available within campaign authority.

During real product development, determine whether the naturally warranted work exposes a capability whose smallest coherent implementation requires meaningful semantic coupling across multiple product surfaces.

If it does, deliberately transfer semantic campaign control at a coherent but incomplete architectural boundary to a fresh campaign controller with no access to the predecessor's conversation context or private reasoning.

Determine whether durable repository state is sufficient for the successor to:

* reconstruct the capability being built;
* reconstruct why the capability is strategically warranted;
* reconstruct the architectural intent behind the partial implementation;
* distinguish integrated product authority from campaign candidate decisions;
* distinguish adopted candidate architecture from provisional implementation hypotheses;
* identify intentional transitional inconsistencies;
* identify remaining cross-surface obligations;
* reconstruct relevant authority boundaries from durable sources;
* reverify consequential claims against repository and GitHub evidence;
* independently reassess predecessor decisions;
* continue, refine, redesign, revert, or escalate the partial implementation as warranted;
* and bring the capability to a coherent, qualified product boundary.

The engineering objective is primary.

The succession experiment exists to test whether architectural intent survives controller replacement during real development.

Do not select a lower-value capability merely because it creates a better experiment.

Do not enlarge implementation scope merely to create experimental complexity.

Do not introduce new orchestration or state infrastructure unless a demonstrated failure warrants it.

Maintain:

```text
PRODUCT NEED
→ PRODUCT TASK SELECTION
→ ASSESS NATURAL COUPLING
→ ARCHITECTURAL-CONTINUITY EXPERIMENT IF WARRANTED
```

not:

```text
NEED COUPLED EXPERIMENT
→ SEARCH FOR A TASK THAT FITS IT
```

## Campaign Authority Source and Durable Files

Preserve this complete owner instruction verbatim in an appropriate non-authoritative Campaign 3 location before substantive campaign work begins.

Prefer:

```text
docs/campaigns/<campaign-3-name>/
    OWNER-INSTRUCTION.md
    CHARTER.md
    CAMPAIGN-STATE.md
    STARTUP-PROVENANCE.md
    controllers/
```

The exact path may follow current repository convention.

### `OWNER-INSTRUCTION.md`

Contains this prompt verbatim.

It is immutable campaign provenance.

Do not silently edit it as campaign understanding evolves.

### `CHARTER.md`

Create a concise operational charter derived from the owner instruction containing only:

```text
CAMPAIGN MISSION
AUTHORITY
NON-NEGOTIABLE CONSTRAINTS
SUCCESS CONDITIONS
ALTERNATIVE TERMINAL CONDITIONS
STOPPING RULES
OWNER-RESERVED DECISIONS
```

Reference `OWNER-INSTRUCTION.md` as the authority source.

Do not use the charter to silently alter the owner's mandate.

### `CAMPAIGN-STATE.md`

Maintain the current evolving synthesis:

```text
product direction
capability assessment
candidate architecture
architectural obligations
evidence ceilings
uncertainties
strategic rationale
integration state
controller state
campaign disposition
```

Historical controller conclusions should not be rewritten as though they were always known.

### Controller Checkpoints

Use controller-specific durable files, for example:

```text
controllers/A-selection.md
controllers/A-architecture.md
controllers/A-handoff.md

controllers/B-reconstruction.md
controllers/B-cycle-result.md

controllers/A-B-continuity-audit.md
```

Once committed as temporal evidence, do not rewrite a controller checkpoint merely because later evidence changes the campaign conclusion.

## Starting Point

PR #269 has been merged before this campaign begins.

Do not assume that the PR #269 merge commit itself is still current `main`.

Fetch the authoritative remote state and reconstruct Campaign 2's final integrated status from current `origin/main`, including any post-merge closure or reconciliation commits.

Treat current authoritative `origin/main` at Campaign 3 startup as the integrated starting state.

Do not rely on conversation history from Campaigns 1 or 2.

Reconstruct prior results from durable repository and GitHub evidence.

Campaign 1 established, with explicit ceilings:

```text
durable execution continuity

persistent controller
→ fresh bounded workers
```

Campaign 2 established, with explicit ceilings:

```text
durable strategic continuity

Controller A
→ durable strategic state
→ fresh Controller B
→ independent reconstruction
→ re-verification
→ predecessor-frontier disagreement
→ independent strategic selection
→ qualified product work
```

Campaign 2 did not establish:

* independent process/model succession;
* concurrent controllers;
* universal autonomous repository development;
* deep coupled multi-surface implementation under succession;
* formal Sensemaking Skills self-hosting;
* strict minimality of its durable continuation state.

Campaign 3 exists primarily to pressure-test the next relevant boundary:
durable architectural continuity during genuinely coupled incomplete implementation.

Do not assume that current repository evidence necessarily warrants such a coupled capability.

That is something Campaign 3 must discover.

## Bootstrap Constraint

Sensemaking Skills is the product being developed.

It is not the semantic campaign controller.

Do not use Sensemaking Skills' own:

* `repo-sensemaker`;
* `using-sensemaking`;
* registered workflows;
* workflow routing;
* fog routing;
* Skill-to-Skill orchestration;
* continuation hooks;
* proposed agent-native campaign machinery

as the controller of Campaign 3.

The external coding agent owns semantic campaign control.

Sensemaking Skills MAY be exercised as:

```text
PRODUCT SURFACE UNDER TEST
```

or as:

```text
BOUNDED PRODUCT SUBGRAPH
```

when independently warranted.

It must not become:

```text
CAMPAIGN 3 SEMANTIC ORCHESTRATOR
```

You MAY and SHOULD use ordinary repository engineering infrastructure:

* source inspection;
* authoritative documentation;
* ADRs;
* contracts;
* repository history;
* Git;
* GitHub;
* issues and PRs;
* pytest;
* validators;
* `validate-repo.py`;
* build/package checks;
* CI;
* normal coding tools;
* isolated fresh coding-agent contexts/subagents where the environment genuinely supports them.

## Campaign Control Roles

Distinguish three roles.

### Campaign Owner

The owner:

* launches Campaign 3;
* grants authority;
* retains reserved decisions;
* may expand or narrow campaign authority;
* controls merge, ratification, and publication where repository policy does not already grant them;
* may terminate the campaign.

### Mechanical Campaign Harness

The mechanical harness may:

* create worktrees;
* select exact commits;
* launch fresh controller contexts;
* provide durable-file paths;
* provide Git/GitHub capabilities;
* record bootstrap provenance;
* transfer exact repository state.

It must not:

* choose the product capability;
* rank capability boundaries;
* explain predecessor reasoning;
* tell a successor what implementation step to perform;
* reinterpret campaign state;
* silently revise controller conclusions.

Maintain:

```text
MECHANICAL DISPATCH
!=
SEMANTIC CAMPAIGN CONTROL
```

### Semantic Campaign Controller

The active controller owns:

```text
product-state reconstruction
strategic capability selection
architecture
bounded implementation decisions
evidence interpretation
handoff preparation
campaign reassessment
```

Only one controller should own semantic campaign continuation at a time unless Campaign 3 later produces a separately warranted reason to test concurrency.

## Fresh-Controller Standard

A successor counts as a fresh semantic controller only when the strongest available evidence supports that:

1. it has a new model/agent context;
2. it does not inherit the predecessor's conversation;
3. it does not inherit predecessor private reasoning;
4. no automatic summary supplies predecessor conclusions;
5. the exact bootstrap is recorded;
6. it receives direct access to the committed handoff repository state;
7. it receives durable-source paths rather than semantic answers;
8. it has the Git/GitHub/validation capabilities needed to verify consequential facts;
9. it may reject predecessor architectural conclusions;
10. it owns the next bounded responsibility;
11. predecessor feedback cannot alter its reconstruction checkpoint;
12. the predecessor does not regain semantic campaign control afterward.

A fresh worker performing a predecessor-selected task is not a fresh controller.

A subagent counts only when the execution environment actually supplies the required context isolation and semantic independence.

Record the strongest supported isolation claim:

```text
DEMONSTRATED_CONTEXT_ISOLATION

HARNESS_REPORTED_ISOLATION

CONTROLLER_ASSERTED_ISOLATION

SUCCESSION_ISOLATION_UNVERIFIED
```

Do not claim independent process or model succession unless the environment actually demonstrates it.

## Phase 0 — Mandatory Preflight

Before selecting product work:

1. confirm repository identity;
2. confirm current branch/worktree;
3. fetch authoritative remote state;
4. record exact current `origin/main`;
5. verify PR #269 is integrated;
6. reconstruct Campaign 2's final closure state, including post-#269 updates;
7. inspect repository qualification requirements;
8. reconstruct current product direction from authoritative durable sources;
9. reconcile materially stale strategic summaries if they would corrupt Campaign 3 selection;
10. reconstruct Campaigns 1 and 2 only as necessary;
11. record relevant evidence ceilings;
12. establish mutation authority;
13. establish push/PR authority;
14. establish merge/ratification/owner-reserved boundaries;
15. verify that a fresh Controller B can actually be instantiated;
16. verify B can access the intended repository state;
17. verify B can access Git;
18. verify B can access GitHub evidence where required;
19. verify B can run necessary validation;
20. establish how the exact bootstrap will be recorded;
21. establish what level of isolation the harness can honestly claim;
22. create an isolated Campaign 3 branch/worktree from the recorded baseline;
23. create and commit Campaign 3 durable scaffolding.

If a genuine successor context cannot be created with enough capability to perform the experiment, stop before intentionally creating incomplete architecture with:

```text
EXTERNAL_BLOCKER
```

unless the problem can be repaired mechanically without changing the meaning of the experiment.

Do not create a partial architecture and only afterward discover there is no valid successor mechanism.

## Three Repository-State Planes

Every controller must distinguish three planes.

### Integrated Product State

```text
INTEGRATED PRODUCT STATE
=
current authoritative origin/main
+
accepted product authority
+
merged executable behavior
```

### Campaign Candidate State

```text
CAMPAIGN CANDIDATE STATE
=
current Campaign 3 branch/head
including coherent but possibly incomplete unmerged implementation
```

Candidate implementation is real repository state.

It is not automatically integrated or ratified product state.

### Campaign Architectural State

```text
CAMPAIGN ARCHITECTURAL STATE
=
strategic rationale
architectural rationale
cross-surface obligations
decision status
evidence ceilings
temporary exceptions
reopen conditions
handoff reasoning
```

This is strategic and architectural memory.

It is not executable product authority.

Before major strategic selection and before every controller handoff record:

```text
CURRENT ORIGIN/MAIN:

CAMPAIGN BASE:

CAMPAIGN HEAD:

MAIN DRIFT SINCE CAMPAIGN START:

CANDIDATE CHANGES NOT ON MAIN:

INTEGRATION STATUS:

WHICH CLAIMS APPLY TO MAIN:

WHICH CLAIMS APPLY ONLY TO CAMPAIGN HEAD:

OWNER / RATIFICATION STATUS:
```

## Main-Branch Drift

Before strategic selection, handoff, and final qualification:

1. fetch `origin/main`;
2. compare it with the campaign base;
3. compare it with campaign HEAD;
4. inspect materially relevant intervening changes.

If `main` advanced, explicitly choose:

```text
CONTINUE_AGAINST_RECORDED_BASE

INCORPORATE_MAIN_CHANGE

REASSESS_CAPABILITY

OWNER_DECISION_REQUIRED

EXTERNAL_BLOCKER
```

Do not automatically rebase merely for neatness.

Any incorporated main changes become part of the candidate and must be qualified accordingly.

## Central Campaign Question

Campaign 3 asks:

Can architectural intent—not merely task state or strategic direction—survive semantic campaign-controller replacement while a genuinely coupled product capability is still incomplete?

Supporting questions:

1. What information must be durable for a successor to understand an intentionally transitional architecture?
2. Can it distinguish:

```text
INTENTIONAL INCOMPLETENESS
```

from:

```text
ACTUAL REGRESSION
```

3. Can it distinguish:

```text
INTEGRATED / RATIFIED PRODUCT AUTHORITY

CAMPAIGN-ADOPTED CANDIDATE ARCHITECTURE

PROVISIONAL IMPLEMENTATION HYPOTHESIS
```

4. Can it recover cross-surface obligations created by a semantic change?
5. Can it identify where the predecessor was wrong, incomplete, or unnecessarily restrictive?
6. Can expensive architectural reasoning be preserved durably without requiring blind trust?
7. Which information belongs in durable product/campaign practice, and which exists only because Campaign 3 is an experiment?

## Campaign Control Model

Use:

```text
PRODUCT MISSION
      ↓
RECONSTRUCT CURRENT PRODUCT STATE
      ↓
IDENTIFY HIGHEST-LEVERAGE WARRANTED PRODUCT BOUNDARY
      ↓
SELECT PRODUCT CAPABILITY BASED ON PRODUCT VALUE
      ↓
ASSESS SMALLEST COHERENT IMPLEMENTATION
      ↓
IS IT GENUINELY SEMANTICALLY COUPLED?
      ↓
YES → CAMPAIGN 3 COUPLED IMPLEMENTATION PATH

NO
      ↓
IS ANOTHER COMPARABLY WARRANTED COUPLED CAPABILITY
AVAILABLE WITHOUT DISPLACING MATERIALLY HIGHER-VALUE WORK?
      ↓
YES → SELECT ONLY IF PRODUCT WARRANT REMAINS STRONG

NO
      ↓
NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED
```

For the coupled path:

```text
RESOLVE PRODUCT / ARCHITECTURAL SEMANTICS
      ↓
BEGIN REAL COUPLED IMPLEMENTATION
      ↓
REACH COHERENT BUT INCOMPLETE ENGINEERING CHECKPOINT
      ↓
WRITE DURABLE ARCHITECTURAL HANDOFF
      ↓
CONTROLLER A RELINQUISHES SEMANTIC CONTROL
      ↓
FRESH CONTROLLER B
      ↓
RECONSTRUCT + VERIFY + REASSESS
      ↓
CONTINUE / REFINE / REDESIGN / REVERT / ESCALATE
      ↓
COMPLETE COUPLED CAPABILITY
      ↓
CROSS-SURFACE QUALIFICATION
      ↓
POST-HOC CONTINUITY AUDIT
      ↓
CAMPAIGN DISPOSITION
```

## Phase 1 — Select the Product Capability First

Do not begin by searching for something coupled.

First identify the highest-leverage product capability currently warranted within available authority.

For serious candidates record:

```text
CAPABILITY:

CURRENT LIMITATION:

EVIDENCE THE LIMITATION EXISTS:

INTENDED USER / OPERATOR:

PRODUCT CONSEQUENCE IF SOLVED:

WHY IT MATTERS NOW:

AUTHORITY REQUIRED:

AUTHORITY AVAILABLE:

DECISION-CHANGING UNCERTAINTY:
```

Then select the genuine product frontier.

Only afterward assess:

```text
SMALLEST COHERENT SOLUTION:

LIKELY SEMANTIC SURFACES:

CROSS-SURFACE INVARIANT:

WHY THOSE SURFACES MUST AGREE:

IS THE IMPLEMENTATION GENUINELY COUPLED?:

WHY THE SCOPE IS NATURAL:
```

Do not select a materially lower-value capability merely because it is more architecturally interesting.

A somewhat lower-ranked coupled capability may be selected only when:

* the absolute highest-leverage boundary is genuinely blocked, owner-reserved, or non-engineering;
* the coupled capability is independently high-value;
* solving it does not materially displace more valuable in-authority product work;
* its campaign warrant is strong without reference to the experiment.

## Semantic Coupling Definition

A capability is meaningfully coupled when:

a product invariant spans two or more product surfaces such that each surface may appear locally valid while the product remains semantically incorrect unless the obligated surfaces agree.

Examples of potentially coupled surfaces:

```text
product semantics
domain model
artifact / representation contract
producer
consumer
validator
compatibility behavior
migration behavior
runtime/control behavior
tests
documentation
```

Not every capability needs all of them.

Coupling is semantic, not numerical.

Do NOT classify something as coupled merely because:

* several files change;
* several tests change;
* the implementation is large;
* multiple modules are touched;
* the work can be decomposed;
* you deliberately distribute a small change across components.

Reject experimentally inflated scope.

## Phase 1 Outcomes

After selecting the genuine product frontier and assessing its natural implementation, use one:

```text
COUPLED_CAPABILITY_FOUND

NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED

OWNER_DECISION_REQUIRED

EXTERNAL_BLOCKER

CAMPAIGN_PREMISE_INVALIDATED
```

Use:

```text
NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED
```

when no sufficiently coupled capability can be selected without distorting real product priority.

This is a legitimate campaign result, not a failure.

Do not manufacture coupled work.

## Strategic Selection Gate

Before implementing the selected capability record:

```text
SELECTED CAPABILITY:

CAMPAIGN WARRANT:

CURRENT PRODUCT LIMITATION:

INTENDED USER / OPERATOR:

USER / OPERATOR VALUE:

DECISION-CHANGING UNCERTAINTY:

EVIDENCE:

EXPECTED PRODUCT CAPABILITY AFTER COMPLETION:

SEMANTIC SURFACES:

CROSS-SURFACE INVARIANT:

COUPLING RELATIONSHIPS:

SMALLEST COHERENT IMPLEMENTATION:

WHY THIS IS THE PRODUCT FRONTIER:

WHY THIS IS NOT LOCAL CLEANUP:

WHY THIS IS NOT EXPERIMENTALLY INFLATED:

WHY THIS WOULD REMAIN WARRANTED WITHOUT CAMPAIGN 3:

AUTHORITY REQUIRED:

AUTHORITY AVAILABLE:

STOP / REASSESS CONDITIONS:
```

Do not proceed if campaign warrant cannot be established independently of experimental convenience.

## Three Levels of Warrant

Maintain:

```text
LOCAL WARRANT
Why should this line or behavior change?

TASK WARRANT
Why is this responsibility required for the active capability?

CAMPAIGN WARRANT
Why should this product capability be developed now?
```

A strong local warrant does not substitute for a campaign warrant.

## Architectural Decision Model

Do not represent architectural decisions with one status axis that mixes authority and maturity.

For every consequential architectural decision record two dimensions.

### Authority Basis

Use:

```text
RATIFIED_PRODUCT_AUTHORITY

CAMPAIGN_IMPLEMENTATION_AUTHORITY

OWNER_DECISION_REQUIRED
```

`RATIFIED_PRODUCT_AUTHORITY`
The decision follows accepted ADR/policy/contract/owner authority.
The campaign does not have authority to silently contradict it.

`CAMPAIGN_IMPLEMENTATION_AUTHORITY`
Campaign 3 may adopt an implementation/design decision for the candidate because it falls within granted engineering authority.
This does not ratify the choice as permanent product architecture.

`OWNER_DECISION_REQUIRED`
The campaign cannot safely make the decision.

### Candidate Decision Status

Use:

```text
ADOPTED_FOR_CANDIDATE

PROVISIONAL

REJECTED

SUPERSEDED
```

`ADOPTED_FOR_CANDIDATE`
Current evidence supports using this choice for the Campaign 3 candidate.
A successor should preserve it unless stronger evidence warrants reopening it.

`PROVISIONAL`
A working design hypothesis.
The successor is explicitly free to revise or reject it.

`REJECTED`
Considered and not selected.

`SUPERSEDED`
Previously adopted or provisional but replaced by stronger later reasoning.

These dimensions are not confidence scores.

Example:

```text
DECISION:
Historical document status must be recognized by the consumer.

AUTHORITY BASIS:
CAMPAIGN_IMPLEMENTATION_AUTHORITY

DECISION STATUS:
ADOPTED_FOR_CANDIDATE
```

## Phase 2 — Controller A Resolves Architectural Intent

Before major implementation, Controller A reconstructs:

* relevant current semantics;
* current contracts;
* domain/representation assumptions;
* producer behavior;
* consumer behavior;
* validators;
* compatibility requirements;
* migration requirements;
* authoritative ADRs;
* existing tests;
* integration boundaries;
* repository qualification constraints.

Then determine the smallest coherent architecture.

For each consequential decision record:

```text
DECISION:

PROBLEM:

EVIDENCE:

ALTERNATIVES CONSIDERED:

WHY ALTERNATIVES WERE REJECTED:

AUTHORITY BASIS:

DECISION STATUS:

AFFECTED SURFACES:

CROSS-SURFACE OBLIGATIONS:

INVARIANTS:

REOPEN CONDITION:
```

Do not call something product-ratified merely because Campaign 3 implements it.

## Cross-Surface Obligation Tracking

Track obligations created by semantic changes.

Example:

```text
SEMANTIC CHANGE:
X now means Y.

PRODUCT INVARIANT:
Every producer, consumer, validator, and compatibility path
must interpret Y consistently.

OBLIGATIONS:

[complete] producer A emits Y
[partial] consumer B interprets Y
[pending] validator C validates Y
[pending] compatibility path defines old X behavior
[complete] candidate docs describe intended semantics
[pending] integration tests prove producer → consumer → validator coherence
```

Use the smallest representation that works.

Do not automatically create a formal graph.

The purpose is to preserve:

```text
SEMANTIC OBLIGATIONS
```

not:

```text
EXECUTION ORDER
```

An obligation graph is not necessarily a workflow DAG.

## Phase 3 — Create Genuine Partial Implementation

Controller A must perform real implementation.

The goal is:
a coherent but intentionally incomplete engineering checkpoint
—not an arbitrary interruption.

The checkpoint should be a defensible engineering state even if Campaign 3 did not exist.

A valid checkpoint has:

```text
MEANINGFUL ARCHITECTURE EXISTS

CONSEQUENTIAL PRODUCT CODE / BEHAVIOR EXISTS

COMPLETED SURFACES ARE INTERNALLY COHERENT

AT LEAST ONE GENUINE CROSS-SURFACE OBLIGATION REMAINS

THE REMAINING OBLIGATIONS ARE ENUMERABLE

CORE INVARIANTS ARE PRESERVED OR EXPLICITLY BOUNDED

TEMPORARY EXCEPTIONS ARE KNOWN

THE STATE IS REPRODUCIBLE FROM THE COMMITTED HEAD

CONTINUATION / REVISION / REVERSION REMAINS POSSIBLE
```

Insufficient:

```text
only design notes exist
```

Also insufficient:

```text
the capability is already complete
```

The handoff should require real architectural judgment from B.

### Prefer Green Transitional Checkpoints

Incomplete architecture does not imply that CI should be red.

Prefer a green or appropriately qualified transitional checkpoint when naturally possible.

Expected-red states are acceptable only when the failure is:

```text
CAUSALLY TIED TO KNOWN INCOMPLETENESS
+
NARROWLY SCOPED
+
DURABLY EXPLAINED
+
HAS AN EXPIRATION CONDITION
+
ALLOWED BY REPOSITORY POLICY
```

Never intentionally create broad uncontrolled failure merely to make transitional state obvious.

Do not weaken tests to make the checkpoint appear green.

### Transitional-State Record

Before Controller A relinquishes control record:

```text
INTENDED END STATE:

CURRENT TRANSITIONAL CANDIDATE STATE:

INTEGRATED MAIN STATE:

COMPLETED SURFACES:

PARTIAL SURFACES:

UNTOUCHED BUT OBLIGATED SURFACES:

CROSS-SURFACE INVARIANTS:

KNOWN INTENTIONAL INCONSISTENCIES:

KNOWN UNEXPECTED FAILURES:

EXPECTED-RED / EXPECTED-INCOMPLETE VALIDATION:

TEMPORARY EXCEPTIONS:

INVARIANTS THAT MUST REMAIN TRUE:

ARCHITECTURAL DECISIONS:

AUTHORITY BASIS FOR EACH DECISION:

CANDIDATE STATUS FOR EACH DECISION:

REJECTED ALTERNATIVES:

OUTSTANDING OBLIGATIONS:

AUTHORITY LIMITS:

REOPEN CONDITIONS:

WHAT MUST BE REVERIFIED:
```

Do not include `PREDECESSOR'S LIKELY NEXT ACTIONS` in the bootstrap-visible handoff.

The successor should reconstruct obligations rather than inherit an execution plan.

If comparison with Controller A's predicted next actions would be analytically useful, record those predictions in a separately sealed/post-hoc field or file that B does not read before committing its reconstruction.

Maintain:

```text
ARCHITECTURAL CONTINUITY
!=
PLAN OBEDIENCE
```

### Transitional Validation Record

For every temporary failing or incomplete check record:

```text
TEST / VALIDATOR:

CURRENT RESULT:

EXPECTED OR UNEXPECTED:

WHY:

AFFECTED OBLIGATION:

WHAT FUTURE STATE MAKES IT PASS:

EXPIRY CONDITION:

WHAT WOULD TURN THIS INTO A REAL REGRESSION:
```

Do not normalize uncontrolled red state.

Do not let temporary exceptions silently become permanent baseline failures.

### Mandatory Controller A Checkpoint

Before handoff:

1. complete the chosen partial implementation boundary;
2. commit all intentional repository changes;
3. ensure a clean worktree or record justified exceptions;
4. run the strongest validation appropriate to the transitional state;
5. write Controller A's architectural handoff;
6. record exact campaign HEAD;
7. fetch and record exact `origin/main`;
8. record candidate-vs-main differences;
9. record temporary failures/exceptions;
10. record outstanding obligations;
11. record authority;
12. record handoff provenance;
13. commit the handoff checkpoint;
14. push where authorized and materially useful;
15. explicitly relinquish semantic campaign control.

After this point Controller A is a former controller.

It must not steer Controller B.

### Handoff Provenance

Record:

```text
PREDECESSOR CONTROLLER:

SUCCESSOR CONTROLLER:

LAUNCH MECHANISM:

MODEL / AGENT TYPE, IF AVAILABLE:

SAME OR DIFFERENT MODEL FAMILY:

WHETHER PREDECESSOR PROCESS PERSISTS:

CONTEXT-ISOLATION CLAIM:

EXACT BOOTSTRAP:

FILES / PATHS DISCLOSED:

REPOSITORY HANDOFF HEAD:

CURRENT ORIGIN/MAIN:

WORKTREE / CHECKOUT:

GIT CAPABILITIES:

GITHUB CAPABILITIES:

VALIDATION CAPABILITIES:

AUTOMATIC SUMMARY PRESENT:

OUT-OF-BAND INFORMATION PROVIDED:

SUCCESSOR CHECKPOINT SHA:

PREDECESSOR ACCESS AFTER HANDOFF:

KNOWN ISOLATION LIMITATIONS:
```

## Phase 4 — Fresh Controller B

Launch the genuinely fresh context established during preflight.

Give B only:

* access to the exact committed handoff repository state;
* the Campaign 3 charter path;
* the Campaign 3 state path;
* Controller A's architectural handoff path;
* normal Git/GitHub/validation capabilities.

Do not directly tell B:

* the campaign mission in prose;
* the available authority;
* Controller A's conversation;
* Controller A's private reasoning;
* what implementation step should happen next;
* what architectural decision B should preserve;
* what A predicts B should do.

B must reconstruct mission and authority from durable sources.

This directly tests durable authority reconstruction.

A suitable bootstrap is:

```text
You are now the fresh semantic controller for Campaign 3.

You have access to the committed Campaign 3 candidate repository state.

Campaign 3 durable sources are located at:

CHARTER:
<path>

CAMPAIGN STATE:
<path>

CONTROLLER A HANDOFF:
<path>

You do not have access to Controller A's conversation or private reasoning.

Reconstruct the campaign mission, authority, integrated product state,
candidate architectural state, capability being built, architectural intent,
cross-surface obligations, temporary exceptions, evidence ceilings, and
remaining work from durable sources and current repository/GitHub evidence.

Reverify consequential factual claims before action.

Predecessor architectural choices are evidence-bearing context, not commands.

Before substantial implementation, commit your independent reconstruction
and architectural decision.
```

### Controller B Reconstruction

Before changing substantial product code, B must independently answer:

```text
1. What is Campaign 3 trying to establish?

2. What authority does Campaign 3 possess?

3. What authority remains reserved?

4. What is current integrated product state?

5. What is current Campaign 3 candidate state?

6. What capability is being built?

7. Why was that capability strategically warranted?

8. What product invariant spans the coupled surfaces?

9. What architectural end state appears intended?

10. Which decisions rest on RATIFIED_PRODUCT_AUTHORITY?

11. Which decisions rest on CAMPAIGN_IMPLEMENTATION_AUTHORITY?

12. Which candidate decisions are ADOPTED_FOR_CANDIDATE?

13. Which decisions are PROVISIONAL?

14. Which decisions were rejected or superseded?

15. What implementation exists?

16. What state is intentionally transitional?

17. Which current failures or exceptions are expected?

18. Which failures would represent genuine regression?

19. What semantic obligations remain?

20. Which predecessor assumptions require reverification?

21. Which predecessor decisions appear questionable?

22. What changed on origin/main since handoff, if anything?

23. What is the next warranted bounded responsibility?

24. Is the predecessor architecture still the best candidate?
```

Reverify consequential facts.

Do not blindly trust the handoff.

Do not reopen decisions merely to demonstrate independence.

Do not preserve them merely to demonstrate continuity.

### Controller B Decision

After reconstruction and verification choose exactly one:

```text
CONTINUE_AS_DESIGNED

CONTINUE_WITH_REFINEMENT

REDESIGN_PARTIAL_IMPLEMENTATION

REVERT_PARTIAL_IMPLEMENTATION

OWNER_DECISION_REQUIRED

EXTERNAL_BLOCKER

SUCCESSION_FAILURE_REQUIRES_REDESIGN

CAMPAIGN_PREMISE_INVALIDATED
```

Record:

```text
DECISION:

PREDECESSOR INTENT RECOVERED:

FACTS REVERIFIED:

INTEGRATED / CANDIDATE STATE DISTINCTION:

DECISIONS PRESERVED:

DECISIONS REOPENED:

DECISIONS REJECTED:

EVIDENCE:

AUTHORITY:

REMAINING OBLIGATIONS:

NEXT BOUNDED RESPONSIBILITY:

KNOWN RECONSTRUCTION LIMITATIONS:
```

Commit this checkpoint before substantial implementation and before any predecessor semantic feedback.

This checkpoint is primary succession evidence.

Do not edit it retrospectively because later implementation reveals a different answer.

### Do Not Reward Agreement

Campaign 3 succeeds when B safely reconstructs enough architecture to make a justified decision.

Success does not require agreement with A.

Both may be successful:

```text
B verifies A's architecture and continues it.
```

and:

```text
B finds stronger evidence,
reopens provisional assumptions,
revises the architecture,
and completes a better implementation.
```

Failure is not disagreement.

Failure is inability to reconstruct or reason safely from the durable candidate state.

Also distinguish:

```text
PREDECESSOR_OVERTRUST
```

from:

```text
PREDECESSOR_UNDERTRUST
```

A successor that needlessly redoes all prior reasoning may also reveal insufficiently useful durable architectural state.

## Phase 5 — Controller B Owns Completion

Controller B now owns semantic control.

Execute one bounded responsibility at a time.

For each significant responsibility record:

```text
DECISION:

DECISION-CHANGING UNCERTAINTY:

EVIDENCE:

RESPONSIBILITY:

AFFECTED CROSS-SURFACE OBLIGATIONS:

IMPLEMENTATION:

VALIDATION:

RESULT:

ARCHITECTURAL CONSEQUENCE:

NEXT WARRANTED RESPONSIBILITY:
```

Do not automatically execute Controller A's implied checklist.

Re-evaluate obligations as evidence changes.

Continue until the selected capability reaches its smallest coherent product boundary or a valid campaign terminal state becomes justified.

### Coupled Completion Standard

Before declaring the capability complete ask:

```text
PRODUCT SEMANTICS:
coherent?

CROSS-SURFACE INVARIANT:
satisfied?

REPRESENTATION / CONTRACT:
coherent?

PRODUCERS:
aligned?

CONSUMERS:
aligned?

VALIDATORS:
aligned?

COMPATIBILITY / MIGRATION:
resolved or explicitly not required?

RUNTIME / CONTROL BEHAVIOR:
aligned where applicable?

TESTS:
prove cross-surface behavior?

DOCUMENTATION:
truthful?

TEMPORARY EXCEPTIONS:
closed or legitimately dispositioned?

PROVISIONAL DECISIONS:
resolved, retained with rationale, or explicitly left provisional?

AUTHORITY:
respected?

QUALIFICATION:
complete for the candidate?
```

Do not infer closure merely because targeted tests are green.

## Phase 6 — Post-Hoc Architectural Continuity Audit

Controller B must first finish its reconstruction checkpoint and complete its strategic cycle without semantic steering from A.

Only after B's cycle is frozen may a post-hoc continuity audit occur.

Prefer either:

* the former lead Controller A acting only as retrospective auditor; or
* another fresh audit context if cheaply available.

The auditor may inspect:

```text
A architecture record
A handoff
B reconstruction checkpoint
B implementation
final candidate state
qualification evidence
```

The auditor must not rewrite A or B checkpoints.

Separate:

```text
B SELF-ASSESSMENT
```

from:

```text
POST-HOC CONTINUITY AUDIT
```

The audit asks whether B successfully reconstructed and reasoned from architectural intent—not whether B agreed with A.

### Architectural-Continuity Classification

Classify:

```text
ARCHITECTURAL_CONTINUITY_DEMONSTRATED

ARCHITECTURAL_CONTINUITY_PARTIAL

ARCHITECTURAL_CONTINUITY_FAILED
```

Assess separately:

```text
MISSION_RECONSTRUCTION:

AUTHORITY_RECONSTRUCTION:

INTENT_RECONSTRUCTION:

INTEGRATED_VS_CANDIDATE_STATE_RECONSTRUCTION:

DECISION_AUTHORITY_RECONSTRUCTION:

DECISION_STATUS_RECONSTRUCTION:

TRANSITIONAL_STATE_RECONSTRUCTION:

CROSS_SURFACE_OBLIGATION_RECONSTRUCTION:

EXPECTED_FAILURE_RECONSTRUCTION:

PREDECESSOR_REASSESSMENT:

VALIDATION_BOUNDARY_RECONSTRUCTION:

CONTEXT_COMPRESSION_VALUE:

SUCCESSION_ISOLATION_EVIDENCE:
```

Do not collapse these into a numeric score.

### Failure Taxonomy

Use when warranted:

```text
ARCHITECTURAL_INTENT_LOSS

TRANSITIONAL_STATE_AMBIGUITY

DECISION_AUTHORITY_AMBIGUITY

DECISION_STATUS_AMBIGUITY

PARTIAL_IMPLEMENTATION_MISREAD

PREDECESSOR_OVERTRUST

PREDECESSOR_UNDERTRUST

COUPLED_SURFACE_OMISSION

CROSS_SURFACE_INVARIANT_LOSS

VALIDATION_BOUNDARY_AMBIGUITY

HANDOFF_COST_EXCESSIVE

MISSING_DURABLE_STATE

AUTHORITY_RECONSTRUCTION_FAILURE

HANDOFF_FACT_INCORRECT

HANDOFF_FACT_TRUST_FAILURE

HANDOFF_STATE_CONTAMINATION

SUCCESSION_ISOLATION_UNVERIFIED

PRODUCT_DIRECTION_AMBIGUITY

BASELINE_DRIFT_MATERIAL

OTHER_DEMONSTRATED_FAILURE
```

For each:

```text
FAILURE:

DECISION AFFECTED:

EVIDENCE:

ROOT INFORMATION DEFICIENCY:

CONSEQUENCE:

DID VERIFICATION PREVENT WRONG ACTION:

SMALLEST REPAIR:

RECURRENT OR ONE-OFF:

PRODUCT / HANDOFF / HARNESS FAILURE:

DOES THIS WARRANT NEW INFRASTRUCTURE:
YES / NO / NOT YET
```

Do not jump from one failure to a general framework.

### Context-Compression Analysis

Controller B should record:

```text
WHAT REPOSITORY FACTS WERE CHEAP TO REVERIFY:

WHAT GITHUB FACTS WERE CHEAP TO REVERIFY:

WHAT PRIOR ARCHITECTURAL REASONING WAS EXPENSIVE TO RECONSTRUCT:

WHAT HANDOFF INFORMATION SAVED MATERIAL WORK:

WHAT HANDOFF INFORMATION WAS REDUNDANT:

WHAT HANDOFF INFORMATION WAS WRONG:

WHAT WOULD HAVE BEEN DANGEROUS TO TRUST:

WHAT PREDECESSOR DECISIONS COULD SAFELY REMAIN CLOSED:

WHAT HAD TO BE REOPENED:

WHAT INFORMATION WAS MISSING:

WHAT INFORMATION APPEARS CAMPAIGN-SPECIFIC:

WHAT INFORMATION APPEARS PRODUCT-WORTHY:
```

Test the principle:

```text
cheap facts
→ re-read repository

expensive rationale
→ preserve durably

consequential assumptions
→ reverify

predecessor recommendations
→ reassess

semantic obligations
→ preserve until discharged or superseded
```

## Formalization Rule

Campaigns 1 and 2 found Markdown sufficient.

Presume Markdown remains sufficient until demonstrated failure says otherwise.

Do not create:

* new artifact schemas;
* new artifact types;
* formal obligation graphs;
* dependency graph infrastructure;
* continuation validators;
* orchestration state machines;
* hooks;
* workflow machinery;
* new Skills;
* semantic routers

merely because Campaign 3 carries more complex architectural state.

Formalization becomes warranted only when evidence shows:

```text
RECURRING STATE OR RESPONSIBILITY NEED
+
STABLE SEMANTICS
+
MATERIAL OMISSION / ERROR COST
+
MECHANICALLY USEFUL BOUNDARY
```

Record emergent candidates without automatically implementing them.

### Emergent Product Primitives

Observe concepts such as:

```text
change obligation
architectural decision
decision authority basis
candidate decision status
cross-surface invariant
transitional exception
affected surface
closure obligation
reopen condition
```

Do not immediately canonize them.

A recurring concept becomes a product primitive only when real product evidence warrants first-class representation.

### Workflow Observation

Do not model coupled implementation as a workflow merely because it has multiple stages.

Maintain:

```text
SEMANTIC OBLIGATION
!=
EXECUTION ORDER
```

Producer, consumer, validator, tests, and documentation may all be obligated by one semantic change without requiring a fixed execution order.

If repeated real use reveals a stable useful sequence, record that for later workflow analysis.

Do not formalize it merely because Campaign 3 executed one sequence successfully.

### Skill Observation

Campaign 3 remains externally controlled.

Do not use Sensemaking Skills Skills as campaign orchestration.

Observe recurring bounded responsibilities.

Ask:

```text
Does this responsibility recur?

Are its inputs identifiable?

Are its outputs identifiable?

Is the boundary stable?

Would specialized instructions materially improve execution?

Would durable output help later responsibilities?

Is ordinary coding-agent reasoning already sufficient?
```

Record candidates without creating them unless the product independently warrants doing so.

## Authority Discipline

Maintain:

```text
evidence
!=
authority

warrant
!=
authority

recommendation
!=
selection
!=
execution authorization

candidate implementation
!=
ratification

qualified branch
!=
merged product
```

Do not silently ratify Campaign 3 design choices as permanent architecture.

Ask the owner only when:

* product preference genuinely determines the choice;
* an authority boundary prevents consequential work;
* an irreversible owner-reserved tradeoff is reached;
* credentials/environment are unavailable;
* ratification is explicitly owner-reserved;
* merge/publication authority is required.

Do not ask the owner questions repository evidence can settle.

## Git / PR / Qualification Discipline

Work incrementally.

For each coherent change:

* verify current HEAD;
* inspect current `origin/main` where relevant;
* inspect authority;
* inspect contracts;
* inspect tests;
* implement the smallest coherent change;
* add focused regression coverage;
* run targeted validation;
* inspect the diff;
* run broader qualification as warranted;
* commit coherent provenance;
* push where authorized.

Maintain:

```text
TARGETED LOCAL PASS
!=
COMPLETE LOCAL QUALIFICATION
!=
QUALIFIED CAMPAIGN HEAD
!=
MERGED STATE
!=
POST-INTEGRATION VALIDATED MAIN
```

Do not overstate qualification.

If `main` advances, reassess candidate identity and relevant semantics.

## Controller C Policy

Do not automatically create Controller C.

A third controller is warranted only if:

* meaningful coupled implementation remains;
* another handoff tests a materially new condition;
* B cannot legitimately finish the capability;
* a handoff failure has been repaired and requires a fresh retry;
* another context is necessary for an unbiased continuity audit.

Do not add Controller C merely to increase sample count.

## Campaign Success Conditions

`CAMPAIGN_COMPLETE` requires the strongest currently defensible version of all materially relevant conditions below.

1. **Genuine Product Warrant** — The selected capability was warranted by current product direction independently of the experiment.
2. **Genuine Semantic Coupling** — Its smallest coherent implementation naturally required multiple surfaces to satisfy a shared semantic invariant.
3. **Real Partial Implementation** — Controller A created consequential implementation and stopped at a coherent engineering checkpoint with genuine obligations remaining.
4. **Durable Architectural Handoff** — The committed repository and handoff preserve enough architectural state for a fresh controller to reason safely.
5. **Fresh Semantic Controller Succession** — Controller B begins without A's conversation/private reasoning and assumes semantic control.
6. **Authority Reconstruction** — B reconstructs campaign authority from durable sources rather than being directly told the answer.
7. **Integrated/Candidate Distinction** — B correctly distinguishes integrated product state from Campaign 3's transitional candidate.
8. **Architectural Decision Reconstruction** — B correctly reconstructs both `AUTHORITY BASIS` and `CANDIDATE DECISION STATUS` where materially relevant.
9. **Transitional-State Reconstruction** — B distinguishes intentional incompleteness from genuine regression.
10. **Independent Architectural Reassessment** — B independently chooses whether to continue, refine, redesign, revert, or escalate.
11. **Cross-Surface Obligation Recovery** — B identifies the semantic obligations that remain.
12. **Meaningful Completion** — The capability reaches its smallest coherent product boundary.
13. **Cross-Surface Coherence** — Naturally obligated surfaces agree sufficiently at closure.
14. **Transitional Exceptions Closed** — Temporary failures/exceptions are removed or legitimately dispositioned.
15. **Complete Candidate Qualification** — The final candidate receives the strongest relevant qualification.
16. **Durable State Updated** — Campaign/product surfaces truthfully reflect the final capability and evidence ceiling.
17. **Architectural-Continuity Disposition** — Evidence supports one: `ARCHITECTURAL_CONTINUITY_DEMONSTRATED` / `ARCHITECTURAL_CONTINUITY_PARTIAL` / `ARCHITECTURAL_CONTINUITY_FAILED`.
18. **No Premature Infrastructure** — No schema/hook/router/workflow/Skill/state-machine machinery is added merely for the experiment.
19. **Honest Isolation Ceiling** — Do not generalize same-process or same-model succession into independent process/model succession.
20. **Honest Generalization Ceiling** — One successful campaign does not demonstrate universal autonomous-development reliability.

## Legitimate Alternative Terminal Conditions

Campaign 3 may legitimately terminate without `CAMPAIGN_COMPLETE`.

Use exactly one final disposition:

```text
CAMPAIGN_COMPLETE

NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED

OWNER_DECISION_REQUIRED

EXTERNAL_BLOCKER

CAMPAIGN_PREMISE_INVALIDATED

SUCCESSION_FAILURE_REQUIRES_REDESIGN
```

`CAMPAIGN_COMPLETE`
Use only when a genuinely warranted coupled capability was completed through meaningful incomplete-architecture controller succession and appropriately qualified.

`NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED`
Use when real product prioritization does not currently expose a sufficiently coupled capability without distorting product value.
This is an honest campaign result.

`OWNER_DECISION_REQUIRED`
Use when the next consequential product or architectural move genuinely requires owner authority.

`EXTERNAL_BLOCKER`
Use when required environment, tools, credentials, Git/GitHub capability, or fresh-controller substrate is unavailable.

`CAMPAIGN_PREMISE_INVALIDATED`
Use when evidence shows Campaign 3's architectural-continuity premise is materially wrong or irrelevant to the repository's current development posture.

`SUCCESSION_FAILURE_REQUIRES_REDESIGN`
Use when B cannot safely reconstruct the partial architecture and the smallest warranted next step is redesigning the durable handoff/state model rather than pretending to complete the capability.

## Campaign Closure Rule

Do not continue merely because:

* more product work exists;
* another coupled feature could be built;
* another handoff could be attempted;
* production reliability remains imperfect;
* another Skill/workflow candidate appeared;
* general autonomous self-development remains unsolved.

Close or terminate Campaign 3 once its central architectural-continuity question can be answered at an honest evidence level.

## Durable Campaign State

Maintain at least:

```text
CAMPAIGN MISSION

OWNER-INSTRUCTION PATH

CHARTER PATH

STARTING ORIGIN/MAIN

CURRENT ORIGIN/MAIN

CAMPAIGN BASE

CURRENT CAMPAIGN HEAD

CURRENT PRODUCT DIRECTION

SELECTED PRODUCT CAPABILITY

CAMPAIGN WARRANT

USER / OPERATOR VALUE

CROSS-SURFACE INVARIANT

COUPLED SURFACES

ARCHITECTURAL DECISIONS

DECISION AUTHORITY BASES

CANDIDATE DECISION STATUSES

REJECTED / SUPERSEDED ALTERNATIVES

CURRENT TRANSITIONAL STATE

CHANGE OBLIGATIONS

TEMPORARY EXCEPTIONS

EXPECTED FAILURES

UNEXPECTED FAILURES

AUTHORITY

VALIDATION STATE

CONTROLLER TRACE

HANDOFF PROVENANCE

OPEN UNCERTAINTIES

DEFERRED LOCAL FINDINGS

INTEGRATION STATE

SUCCESSION ISOLATION CEILING

EVIDENCE CEILINGS

CAMPAIGN DISPOSITION
```

Do not formalize this into a machine schema unless demonstrated failure warrants it.

## Final Campaign Report

At legitimate termination produce:

1. **Executive Outcome** — What capability was built, or why no qualifying coupled capability was warranted.
2. **Starting Product State** — starting `origin/main`; Campaign 3 base; Campaign 2 closure state; relevant Campaign 1/2 evidence; inherited evidence ceilings.
3. **Product Capability Selection** — candidates; highest-leverage product boundary; why selected; whether highest-leverage boundary was blocked / owner-reserved; why the coupled capability was or was not selected; why experimental usefulness did not distort product priority.
4. **Coupling Analysis** — cross-surface invariant; naturally obligated surfaces; why local correctness was insufficient; why scope was not experimentally inflated.
5. **Architectural Decisions** — for consequential decisions: decision, authority basis, candidate status, evidence, alternatives, affected surfaces, obligations, reopen condition.
6. **Controller A Implementation** — what A implemented; why the handoff boundary was a defensible engineering checkpoint.
7. **Transitional State** — what remained intentionally incomplete; temporary exceptions; what was expected to remain green/red/incomplete.
8. **Controller Succession Provenance** — launch mechanism; model/context; predecessor process persistence; exact bootstrap; durable sources provided; out-of-band information; isolation claim; known isolation limits; successor checkpoint SHA.
9. **Controller B Reconstruction** — what B recovered; reverified; misunderstood; found stale; found missing; found unnecessarily restrictive.
10. **Architectural Reassessment** — what B preserved; refined; rejected; redesigned; reverted; escalated. Do not score agreement with A as success.
11. **Coupled Implementation Trace** — how semantic obligations were discharged or superseded.
12. **Architectural-Continuity Result** — exactly one classification; the separate assessments.
13. **Post-Hoc Continuity Audit** — compare A's durable architectural intent with B's independent reconstruction; B's candidate decisions; final implementation; final product semantics. Identify actual continuity, justified divergence, and information loss.
14. **Failure Observations** — use the Campaign 3 failure taxonomy.
15. **Durable-State Assessment** — what state proved essential; useful; redundant; stale; incorrect; dangerous to trust; missing; campaign-specific; potentially product-worthy.
16. **Context-Compression Result** — what expensive reasoning survived and what had to be rediscovered.
17. **Emergent Product Primitives** — record any recurring concepts. Do not automatically recommend formalization.
18. **Skill / Workflow Implications** — only evidence-supported observations.
19. **Qualification** — exact: campaign base; current `origin/main`; final candidate head; targeted tests; broader tests; validators; build/package checks; CI; PR state; merge state; post-integration state, if applicable; exceptions. Do not overstate qualification.
20. **Evidence Ceilings** — explicitly state what Campaign 3 does not establish. At minimum consider: independent process succession; independent model-family succession; concurrent controllers; universal architecture continuity; production-grade autonomous development; durability beyond the observed horizon; formal self-hosting.
21. **Remaining Product Limitations and Debt** — separate: strategic product limitations; engineering debt; unvalidated hypotheses; owner decisions; environment blockers; deferred local work.
22. **Owner Decisions** — list only genuine owner-authority questions.
23. **Final Campaign Disposition** — exactly one; explain precisely why.

## Final Operating Principles

Keep these active throughout Campaign 3:

Product priority comes before experimental usefulness.
Select a capability because the product warrants it, then determine whether its natural implementation exposes the Campaign 3 boundary.
Coupling means a cross-surface semantic invariant, not file count.
A coherent partial architecture should be a defensible engineering checkpoint even without the experiment.
Integrated product state, campaign candidate state, and durable architectural state are distinct.
Controller B must reconstruct architecture and authority, not receive the answers out of band.
Architectural continuity is not plan obedience.
Predecessor reasoning is evidence-bearing context, not command authority.
Ratified product authority and campaign implementation authority are different.
Candidate decision maturity and decision authority are different dimensions.
Preserve adopted candidate decisions when evidence supports them.
Reopen provisional decisions when evidence warrants it.
Intentional transitional inconsistency must be explicit and bounded.
Prefer green transitional checkpoints where naturally possible.
Expected-red state must have a cause, scope, and expiry condition.
Semantic changes create obligations; they do not automatically create workflows.
Durable state should preserve expensive architectural rationale without replacing factual reverification.
A successor may prove architectural continuity by correctly disagreeing with the predecessor.
Do not create schemas, hooks, workflows, Skills, graphs, or state machines before demonstrated failure warrants them.
Evidence warrants work. Authority permits action.
Complete the smallest coherent capability rather than the largest impressive implementation.
Do not overclaim process/model independence beyond the harness evidence.
Continue until architectural continuity across a genuinely warranted coupled partial implementation is demonstrated, partially demonstrated, genuinely fails, is blocked, or proves currently unnecessary.

## Three Campaign Aphorisms

It is not a coupled implementation because many surfaces change; it is actually coupled because one semantic invariant obligates those surfaces to agree.

It is not architectural continuity and it is not plan obedience; it is actually the successor recovering enough intent, authority, and obligations to decide whether the predecessor's architecture should survive.

A coherent incomplete architecture is actually a durable engineering state, not merely unfinished work.
