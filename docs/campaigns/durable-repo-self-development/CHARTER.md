# Campaign 2 charter — Durable Repository-Level Self-Development

```
AUTHORITY SOURCE:  docs/campaigns/durable-repo-self-development/OWNER-INSTRUCTION.md
                   (owner instruction delivered 2026-09-02, preserved verbatim).
STATUS:            non-authoritative campaign operating contract. Not an ADR,
                   contract, schema, registry, or ratified product decision.
                   Repository policy (accepted ADRs, CONTEXT.md, AGENTS.md,
                   artifact contracts, canonical vocabulary) continues to govern
                   the product.
PURPOSE:           the smallest durable statement of the campaign's operating
                   contract, so a fresh controller can reconstruct mission,
                   authority, constraints, acceptance conditions, stopping
                   rules, and owner-reserved decisions without re-reading the
                   full owner instruction. Where this charter and the owner
                   instruction appear to differ, the owner instruction governs.
REFINEMENTS:       operating-detail refinements are recorded in CAMPAIGN-STATE.md,
                   never by editing OWNER-INSTRUCTION.md.
```

---

## MISSION

Advance Sensemaking Skills from demonstrated **responsibility-level** artifact
continuation (Campaign 1) toward **durable repository-level self-development**:
independent fresh coding-agent *controllers* can

- reconstruct current product-development state,
- identify the highest-leverage warranted development boundary,
- perform substantial bounded engineering work,
- update durable product-development state, and
- leave the repository so another fresh controller can continue **without prior
  conversation context**.

Campaign 2 is one thing, not two:

```
REAL PRODUCT DEVELOPMENT  +  CONTROLLED CONTROLLER-SUCCESSION EVIDENCE  =  CAMPAIGN 2
```

The campaign must materially advance the product. Do **not** select product work
merely to make the succession experiment succeed. Do not select succession
instrumentation and call it product advancement.

**Central question.** What is the smallest coherent *product* capability required
for repository-level development direction to survive independent
campaign-controller replacement and keep producing strategically warranted
engineering work?

The campaign mission may be broad; execution stays bounded. Never attempt the
mission as one monolithic implementation.

## AUTHORITY

**Source.** The owner instruction (`OWNER-INSTRUCTION.md`). This charter is
derived from it and subordinate to it. Campaign evidence, campaign
implementation, and controller recommendations are **not** product ratification,
integrated product state, or owner decisions.

**Precedence when sources genuinely conflict on the same question:**

```
owner-reserved decision / accepted repository authority
  -> current authoritative repository contracts / ADRs / policies
  -> current integrated repository behavior (origin/main)
  -> Campaign 2 candidate implementation (the campaign branch)
  -> Campaign 2 semantic state (CAMPAIGN-STATE.md)
  -> controller inference
```

(Do not apply mechanically when two sources address different questions.)

**Authorized — reads.** Source, tests, docs, ADRs, contracts, schemas, git
history, branches, commits, GitHub issues/PRs, CI results, repo configuration,
ordinary analysis tools.

**Authorized — local engineering (on the campaign branch only).** Create
Campaign 2 branches/worktrees; modify repository files, implementation code,
tests; modify documentation when a product change warrants it; run tests,
validators, linters, type/build checks, probes, qualification commands; create
commits for coherent campaign work; maintain campaign evidence and state.

**Authorized — remote.** Push the Campaign 2 branch and later campaign commits;
create/maintain a **draft** PR; inspect CI/qualification evidence for the branch.
Use remote actions only when they materially support product development,
qualification, or durable campaign evidence.

**Not authorized by default** (needs a separate owner grant or explicit current
repository policy — otherwise classify as `OWNER_DECISION_REQUIRED`): merging the
Campaign 2 PR; deploying/publishing externally; making an ADR *accepted*;
changing an owner-reserved product decision; treating campaign conclusions as
canonical ratification; creating/closing/reopening/relabelling/materially
modifying GitHub issues for campaign bookkeeping; merging unrelated PRs; altering
protected repository policy to make Campaign 2 pass; inferring owner preference
from repository evidence.

```
evidence != authority
recommendation != selection != execution authorization
implementation != ratification
promotion != merge
```

## NON-NEGOTIABLE CONSTRAINTS

1. **Bootstrap constraint.** Sensemaking Skills must not control Campaign 2. Do
   **not** use as the semantic controller: `repo-sensemaker`, `using-sensemaking`,
   registered workflows, fog-to-workflow routing, workflow-runtime semantic
   routing, Skill-to-Skill continuation, proposed continuation hooks, or any new
   self-hosted campaign-management mechanism. The external coding agent owns
   Campaign 2. Existing Skills/workflows MAY be examined as product surfaces or
   run as bounded subgraphs under test when independently warranted — never as
   strategic control. Normal engineering tools (git, GitHub, pytest, validators,
   `validate-repo.py`, probe engine, CI, build checks) are expected and encouraged.

2. **One active semantic controller at a time.** Mechanical harness `!=` semantic
   controller. A persistent mechanical harness does not invalidate succession if
   it only performs mechanical functions (provision exact state, create fresh
   contexts, pass the allowed bootstrap and durable-source paths, expose
   git/GitHub, record provenance, transfer mechanical outputs). It must not
   interpret the frontier, rank boundaries, choose the successor's task,
   summarize predecessor reasoning, or reinterpret campaign state.

3. **Fresh controller `!=` fresh worker.** A successor counts as a genuinely fresh
   *controller* only with: new model/agent context; no inherited transcript; no
   inherited predecessor private reasoning; no automatic summary of predecessor
   strategic conclusions; recorded exact bootstrap; direct access to the handoff
   repo state and permitted durable sources; git/GitHub/validation capability;
   freedom to reject the predecessor frontier; ownership of next-task selection;
   predecessor cannot rewrite the successor checkpoint; after relinquishment the
   predecessor cannot resume campaign direction. If isolation cannot be
   established strongly enough, record `SUCCESSION_ISOLATION_UNVERIFIED` and
   narrow the conclusion.

4. **Three state planes stay distinct** and are re-recorded before every
   strategic selection and handoff: **integrated product state** (`origin/main` +
   accepted authority + merged behavior); **campaign candidate state** (exact
   campaign branch head, incl. validated-but-unmerged changes — real facts, not
   ratified); **campaign semantic state** (rationale, assessments, alternatives,
   ceilings, uncertainties, owner decisions, reopen conditions).

5. **Predecessor recommendation / frontier / `next_task` = LAST ASSESSED
   CANDIDATE, never a command.** The successor must reconstruct, reverify
   consequential facts, compare boundaries, and independently decide. It may read
   predecessor rationale and must stay free to reject it.

6. **Strategic selection gate before any campaign task** (product capability
   affected; current limitation; evidence it exists; intended user/operator;
   observable value; why it constrains the mission; why it is product advancement
   not campaign instrumentation; why it would still be warranted if succession
   were already solved; why it is strategic not a nearby defect;
   decision-changing uncertainty; bounded task; expected disconfirming
   evidence). Record ≥2 serious alternative boundaries when evidence supports
   them. No numeric scoring.

7. **Do not predetermine the product solution.** A new artifact, YAML/JSON, a
   schema, a new Skill, a `repo-sensemaker` change, a new workflow, hooks, a
   state machine, a router, new registry fields, a campaign runtime, deterministic
   strategic selection, automatic controller spawning — all are hypotheses.
   Discover the smallest coherent product change from evidence. If Markdown
   suffices, keep Markdown. If an existing artifact carries the state, prefer it.
   Formalize only against a demonstrated failure (recurring responsibility/state
   need + stable semantics + repeated manual burden/error + mechanically useful
   boundary).

8. **Campaign instrumentation `!=` product architecture.** `CAMPAIGN-STATE.md`
   existing is not evidence that the product needs an equivalent artifact.

9. **Substantive advancement, honestly sized.** At least one strategic cycle must
   produce substantive product implementation whose complexity arises naturally
   from the boundary, **or** an equivalently consequential result (verified
   premise invalidation, product-boundary correction, an authority-bound decision
   packet that prevents otherwise-warranted implementation, or an architectural
   conclusion that redirects planned engineering). Never enlarge a sufficient
   change, or count files/lines, to look substantial. Never require a `src/`
   change just because Campaign 1 lacked one.

10. **Durable-state epistemics.** Reconstruct intent/rationale from durable state;
    identify consequential factual claims; verify those; update warrant; then act.
    Never assume recorded facts remain true. Durable campaign state preferentially
    preserves expensive-to-reconstruct rationale, not cheap re-derivable facts.

11. **Single cumulative campaign branch** (`campaign/durable-repo-self-development`)
    unless strong evidence warrants another topology. Bootstrap → Controller A
    Task A → A handoff → Controller B checkpoint → Controller B Task B as coherent
    commit ranges. Do **not** modify `main` to establish Campaign 2.

12. **Immutable provenance.** `OWNER-INSTRUCTION.md` is never silently rewritten.
    Controller checkpoints preserve what the controller believed at that time and
    are not retro-edited when later evidence shifts understanding.

13. **Engineering discipline.** Smallest coherent product surface; regression
    coverage where warranted; targeted then broader qualification; inspect the
    diff; never weaken tests to go green; follow evidence over the task's
    predicted result; drop a change that proves unnecessary or wrong.
    `TARGETED TEST PASS != COMPLETE LOCAL QUALIFICATION != PR-HEAD QUALIFICATION
    != MERGE != INTEGRATED-MAIN QUALIFICATION`.

14. **Main-branch drift.** Before each new strategic selection, re-fetch, record
    `origin/main`, compare to base and campaign HEAD, and if intervening changes
    materially affect the campaign choose explicitly among CONTINUE AGAINST
    RECORDED BASE / INCORPORATE RELEVANT MAIN CHANGE / REPLAN / OWNER_DECISION_
    REQUIRED / EXTERNAL_BLOCKER. Do not auto-merge/rebase `main`.

15. **Minimality ceiling.** A successful rich-state handoff demonstrates
    SUFFICIENCY, not STRICT MINIMALITY. Strict minimality needs comparative
    evidence. Absent it, conclude "smallest currently supported candidate" or
    "supported but not fully demonstrated."

## ACCEPTANCE CONDITIONS

Evidence conditions, not performative boxes. Campaign 2 is complete only when the
strongest defensible version of the materially relevant conditions holds:

1. ≥1 genuinely fresh controller takes over semantic control without predecessor
   conversation or private reasoning.
2. Handoff provenance recorded well enough to state the honest isolation level.
3. Successor reconstructs the mission from durable sources (not out-of-band).
4. Successor reconstructs available and reserved authority.
5. Successor distinguishes integrated / candidate / semantic state planes.
6. Successor reconstructs demonstrated product + campaign capabilities, material
   limitations, previous task rationale, changed repo state, evidence ceilings,
   relevant owner decisions, predecessor frontier assessment.
7. Consequential factual handoff claims are verified before action.
8. Successor evaluates plausible boundaries and independently selects a warranted
   repository-level task.
9. Successor reconstruction + selection committed **before** implementation and
   **before** any predecessor semantic feedback.
10. Campaign 2 produces substantive product implementation or an equivalently
    consequential result, naturally sized.
11. Fresh Controller B executes a second strategically warranted task against the
    changed candidate state.
12. Task selection demonstrably distinguishes high-leverage capability work from
    nearby defects.
13. No schema / hook / state machine / semantic router / broad workflow expansion
    / equivalent framework added without demonstrated need.
14. Contradicting evidence narrows, refines, or rejects Campaign 2 hypotheses.
15. No known material contradiction remains among product surfaces changed by,
    relied on by, or needed to support Campaign 2's product claims (unrelated
    inconsistencies may be deferred).
16. Candidate passes appropriate complete qualification, or unsatisfied
    conditions are accurately classified.
17. Remaining limitations explicit.
18. No strict-minimality claim without comparative evidence.
19. The predecessor did not resume semantic control over the successor's cycle.

**Closure rule.** After the mandatory A → B succession and two strategic cycles,
answer the central question at an honest evidence level and close when: succession
evidence exists; substantive advancement occurred or was legitimately ruled
unwarranted; no remaining material gap is needed to evaluate the Campaign 2
question; broader limits can be recorded as ceilings/deferred/future questions. A
Controller C handoff is optional and only if it would materially change the
conclusion. Remaining useful work does not keep Campaign 2 open.

## STOPPING RULES

Continue autonomously until exactly one is justified:

- **CAMPAIGN_COMPLETE** — acceptance conditions materially satisfied at an honest
  evidence level; candidate qualified or exceptions classified.
- **OWNER_DECISION_REQUIRED** — a consequential product/authority decision cannot
  be resolved from repository evidence and no safe bounded work remains before it.
- **EXTERNAL_BLOCKER** — required credentials/systems/infrastructure unavailable;
  in particular, if the defining fresh-controller experiment cannot be executed in
  this environment and cannot be repaired mechanically without changing its
  meaning, stop **before** substantial Task A.
- **CAMPAIGN_PREMISE_INVALIDATED** — evidence shows the central framing is
  materially wrong (e.g. direction is already cheaply reconstructible with no new
  capability; succession is indistinguishable from ordinary reconstruction here;
  the assumed frontier came from a misreading of Campaign 1; an existing mechanism
  already solves the gap; the "necessary" state is pure instrumentation). A
  well-supported invalidation is legitimate evidence — do not force implementation
  to preserve the hypothesis.

Do not stop merely because one task/PR/handoff/implementation finished, another
issue appeared, or context grew. Under context pressure: update durable state,
commit the checkpoint, finish the current responsibility to a safe boundary,
terminate semantic ownership, continue via a fresh controller.

Final report at termination: the 17-section format in `OWNER-INSTRUCTION.md`
("Campaign 2 Final Report"), ending in exactly one disposition.

## OWNER-RESERVED DECISIONS

- Merge / integration of the Campaign 2 PR (and any ADR acceptance, external
  publication, or protected-policy change it implies).
- Any expansion or narrowing of campaign authority.
- Ratifying any Campaign 2 conclusion, recommendation, or candidate
  implementation as product architecture.
- Owner-reserved product decisions surfaced by Campaign 1 that remain open
  (tracked in `CAMPAIGN-STATE.md`), including the nine registry/overlay/doc items
  implied by `docs/workflow-system-disposition.md` section 6, and any Goal A
  execution authorization.
- Terminating the campaign.

Anything otherwise-warranted that crosses these boundaries is recorded as
`OWNER_DECISION_REQUIRED`, not acted on.
