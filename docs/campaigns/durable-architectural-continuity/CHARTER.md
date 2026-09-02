# Campaign 3 Charter — Durable Architectural Continuity During Coupled Implementation

```
AUTHORITY SOURCE: docs/campaigns/durable-architectural-continuity/OWNER-INSTRUCTION.md
                  (owner instruction, delivered 2026-09-02, preserved verbatim, immutable).
STATUS:           derived operating contract. Subordinate to OWNER-INSTRUCTION.md.
                  Not an ADR, contract, schema, registry, validator input, or
                  registered workflow. Nothing in scripts/, src/, tests/, or
                  .github/ reads this file.
PURPOSE:          a fresh controller should be able to reconstruct the campaign's
                  operating contract from this file faster than from the full
                  owner instruction. It does not replace or narrow the owner's
                  mandate; where this file and OWNER-INSTRUCTION.md differ, the
                  owner instruction governs.
RULE:             operating refinements are recorded in CAMPAIGN-STATE.md, not by
                  editing OWNER-INSTRUCTION.md.
```

---

## CAMPAIGN MISSION

Advance Sensemaking Skills through the **highest-leverage currently warranted
product development available within campaign authority**. During that real
product development, determine whether the naturally warranted work exposes a
capability whose **smallest coherent implementation requires meaningful semantic
coupling across multiple product surfaces**.

If it does: deliberately transfer semantic campaign control at a coherent but
**incomplete** architectural boundary to a **fresh** campaign controller (no
predecessor conversation or private reasoning), and determine whether durable
repository state is sufficient for the successor to reconstruct the capability,
its strategic warrant, the architectural intent behind the partial
implementation, the integrated/candidate/provisional distinctions, intentional
transitional inconsistencies, remaining cross-surface obligations, and relevant
authority boundaries — and to independently continue, refine, redesign, revert,
or escalate it to a coherent qualified product boundary.

The engineering objective is primary. The succession experiment exists to test
whether **architectural intent** survives controller replacement during real
development.

Order of operations is fixed:

```text
PRODUCT NEED -> PRODUCT TASK SELECTION -> ASSESS NATURAL COUPLING
             -> ARCHITECTURAL-CONTINUITY EXPERIMENT IF WARRANTED
```

never `NEED COUPLED EXPERIMENT -> SEARCH FOR A TASK THAT FITS IT`.

**Central question.** Can architectural intent — not merely task state or
strategic direction — survive semantic campaign-controller replacement while a
genuinely coupled product capability is still incomplete?

## AUTHORITY

Granted to the active Campaign 3 semantic controller (source:
`OWNER-INSTRUCTION.md`; consistent with the Campaign 2 grant and repository
policy):

- **Reads:** all source, tests, docs, ADRs, contracts, schemas, registries, Git
  history, branches/commits, GitHub issues/PRs, CI results, repository config;
  run ordinary analysis tools.
- **Local engineering on the Campaign 3 branch/worktree:** create branches and
  worktrees; modify repository files; add/modify implementation code and tests;
  modify documentation warranted by product changes; run tests, validators,
  linters, type checks, build checks, probes, qualification commands; create
  commits for coherent campaign work; maintain campaign evidence and durable
  state.
- **Remote campaign actions:** push the Campaign 3 branch and subsequent
  commits; create and maintain a **draft** PR when it materially helps
  qualification or durable evidence; inspect campaign-branch CI.
- **Fresh-controller instantiation:** create isolated fresh coding-agent
  contexts / subagents / worktrees for the succession experiment where the
  environment genuinely supports them.

Repository policy (accepted ADRs, `CONTEXT.md`, `AGENTS.md`, contracts, schemas)
continues to govern the product. Precedence when sources conflict on the same
question:

```text
owner-reserved decision / accepted repository authority
  -> current authoritative contracts / ADRs / policies
  -> current integrated repository behavior
  -> Campaign 3 candidate implementation
  -> Campaign 3 architectural / semantic state
  -> controller inference
```

## NON-NEGOTIABLE CONSTRAINTS

1. **Bootstrap constraint.** Sensemaking Skills is the product under
   development, not the campaign controller. Do not use `repo-sensemaker`,
   `using-sensemaking`, registered workflows, workflow/fog routing,
   Skill-to-Skill orchestration, continuation hooks, or any proposed
   agent-native campaign machinery as the semantic controller of Campaign 3.
   Sensemaking Skills MAY be a **product surface under test** or a **bounded
   product subgraph** when independently warranted. Ordinary repository
   engineering infrastructure (Git, GitHub, pytest, validators,
   `validate-repo.py`, CI, source inspection, isolated fresh coding-agent
   contexts) is expected and encouraged.
2. **Product priority before experimental usefulness.** Never select a
   lower-value capability because it makes a better experiment. Never enlarge
   implementation scope to create experimental complexity. A somewhat
   lower-ranked coupled capability may be selected **only** when the absolute
   highest-leverage boundary is genuinely blocked / owner-reserved /
   non-engineering, the coupled capability is independently high-value, it does
   not displace materially higher-value in-authority work, and its campaign
   warrant stands without reference to the experiment.
3. **Coupling is semantic, not numerical.** A capability is coupled only when a
   product invariant spans >=2 surfaces such that each surface can look locally
   valid while the product is semantically wrong unless the obligated surfaces
   agree. File count, test count, module count, decomposability, or a
   deliberately-distributed small change do NOT make something coupled.
4. **No premature infrastructure.** Markdown is presumed sufficient (Campaigns 1
   and 2). Do not create new artifact schemas/types, formal obligation or
   dependency graphs, continuation validators, orchestration state machines,
   hooks, workflow machinery, new Skills, or semantic routers merely because
   Campaign 3 carries more complex architectural state. Formalize only on
   evidence of: recurring state/responsibility need + stable semantics +
   material omission/error cost + mechanically useful boundary. Record emergent
   candidates without implementing them.
5. **Two-axis architectural decisions.** Every consequential architectural
   decision carries an **authority basis** (`RATIFIED_PRODUCT_AUTHORITY` /
   `CAMPAIGN_IMPLEMENTATION_AUTHORITY` / `OWNER_DECISION_REQUIRED`) AND a
   **candidate decision status** (`ADOPTED_FOR_CANDIDATE` / `PROVISIONAL` /
   `REJECTED` / `SUPERSEDED`). These are distinct dimensions, not confidence
   scores. Campaign implementation of a choice never ratifies it as permanent
   product architecture.
6. **Three state planes stay distinct.** Integrated product state (`origin/main`
   + accepted authority + merged behavior); Campaign candidate state (Campaign 3
   branch head, incl. incomplete unmerged implementation — real but not
   integrated/ratified); Campaign architectural state (rationale, obligations,
   decision status, ceilings, exceptions, reopen conditions, handoff reasoning —
   strategic memory, not executable authority). Re-record the state-plane block
   before every strategic selection and every handoff.
7. **Fresh-controller standard.** A successor counts as a fresh semantic
   controller only against the 12-point standard in `OWNER-INSTRUCTION.md`
   (new context; no inherited conversation or private reasoning; no automatic
   summary of predecessor conclusions; exact bootstrap recorded; direct access
   to committed handoff state; durable-source paths not semantic answers;
   verification capability; may reject predecessor conclusions; owns the next
   bounded responsibility; predecessor feedback cannot alter its checkpoint;
   predecessor does not regain semantic control). Record the strongest supported
   isolation claim (`DEMONSTRATED` / `HARNESS_REPORTED` / `CONTROLLER_ASSERTED` /
   `SUCCESSION_ISOLATION_UNVERIFIED`). Do not claim independent process/model
   succession the environment does not demonstrate.
8. **Architectural continuity != plan obedience.** The handoff must not contain
   the predecessor's predicted next actions or an execution checklist. B
   reconstructs obligations; it does not inherit a plan. B may prove continuity
   by correctly disagreeing with A. Failure is inability to reconstruct or
   reason safely from durable state — not disagreement.
9. **Transitional state is explicit and bounded.** A partial-implementation
   checkpoint must be a defensible engineering state even if Campaign 3 did not
   exist: meaningful architecture, consequential code/behavior, internally
   coherent completed surfaces, >=1 genuine remaining cross-surface obligation,
   enumerable remaining obligations, preserved-or-bounded core invariants, known
   temporary exceptions, reproducible from the committed head, still
   continuable/revisable/revertible. Prefer green or appropriately-qualified
   transitional checkpoints; expected-red is acceptable only when causally tied
   to known incompleteness + narrowly scoped + durably explained + has an expiry
   condition + allowed by repository policy. Never weaken tests to look green.
10. **Durable-state epistemics.** Durable state preserves expensive rationale
    (why a decision was made, why one option dominated, rejected alternatives,
    ceilings, owner decisions, reopen conditions, obligations). It does not
    replace factual reverification: every consequential factual claim
    (SHAs, PR/CI/issue/ADR state, behavior) is reverified from repository /
    GitHub evidence before action. Avoid duplicating cheap, volatile,
    easily-re-derived facts.
11. **Single semantic controller at a time** unless Campaign 3 separately
    discovers a warranted reason to test concurrency. Controller C is not
    automatic (see `OWNER-INSTRUCTION.md` "Controller C Policy").
12. **Honest ceilings.** Do not generalize same-process or same-model succession
    into independent process/model succession. One successful campaign does not
    demonstrate universal autonomous-development reliability.

## SUCCESS CONDITIONS (`CAMPAIGN_COMPLETE`)

The strongest currently defensible version of every materially relevant
condition (full text: `OWNER-INSTRUCTION.md` "Campaign Success Conditions"):

1. genuine product warrant (independent of the experiment);
2. genuine semantic coupling (shared invariant across >=2 surfaces);
3. real partial implementation stopped at a coherent checkpoint with genuine
   obligations remaining;
4. durable architectural handoff sufficient for safe successor reasoning;
5. fresh semantic controller succession (no predecessor conversation/reasoning);
6. successor reconstructs campaign authority from durable sources;
7. successor distinguishes integrated vs candidate state;
8. successor reconstructs both authority basis and candidate decision status
   where materially relevant;
9. successor distinguishes intentional incompleteness from genuine regression;
10. successor independently chooses continue / refine / redesign / revert /
    escalate;
11. successor identifies remaining cross-surface obligations;
12. capability reaches its smallest coherent product boundary;
13. naturally obligated surfaces agree sufficiently at closure;
14. transitional exceptions closed or legitimately dispositioned;
15. final candidate receives the strongest relevant qualification;
16. durable state truthfully reflects the final capability and evidence ceiling;
17. architectural-continuity disposition recorded
    (`DEMONSTRATED` / `PARTIAL` / `FAILED`);
18. no premature infrastructure added for the experiment;
19. honest isolation ceiling;
20. honest generalization ceiling.

## ALTERNATIVE TERMINAL CONDITIONS

Exactly one final disposition (full text: `OWNER-INSTRUCTION.md`):

- `CAMPAIGN_COMPLETE` — a genuinely warranted coupled capability completed
  through meaningful incomplete-architecture controller succession, qualified.
- `NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED` — real product prioritization does
  not currently expose a sufficiently coupled capability without distorting
  product value. **An honest campaign result, not a failure. Do not manufacture
  coupled work.**
- `OWNER_DECISION_REQUIRED` — the next consequential product/architectural move
  genuinely requires owner authority.
- `EXTERNAL_BLOCKER` — required environment, tools, credentials, Git/GitHub
  capability, or fresh-controller substrate is unavailable.
- `CAMPAIGN_PREMISE_INVALIDATED` — evidence shows the architectural-continuity
  premise is materially wrong or irrelevant to the repository's current
  development posture.
- `SUCCESSION_FAILURE_REQUIRES_REDESIGN` — B cannot safely reconstruct the
  partial architecture and the smallest warranted next step is redesigning the
  durable handoff/state model rather than pretending to complete the capability.

## STOPPING RULES

Close or terminate Campaign 3 once its central architectural-continuity question
can be answered at an honest evidence level. Do **not** continue merely because:
more product work exists; another coupled feature could be built; another handoff
could be attempted; production reliability is imperfect; another Skill/workflow
candidate appeared; general autonomous self-development remains unsolved.

Phase 0 stop: if a genuine successor context with enough capability cannot be
created, stop **before** intentionally creating incomplete architecture, with
`EXTERNAL_BLOCKER` — unless mechanically repairable without changing the
experiment's meaning.

Main-drift stop/choice: before strategic selection, handoff, and final
qualification, re-fetch `origin/main` and choose explicitly among
`CONTINUE_AGAINST_RECORDED_BASE` / `INCORPORATE_MAIN_CHANGE` /
`REASSESS_CAPABILITY` / `OWNER_DECISION_REQUIRED` / `EXTERNAL_BLOCKER`.

## OWNER-RESERVED DECISIONS

Not authorized to the campaign unless separately granted by the owner or already
granted by current repository policy (source: `OWNER-INSTRUCTION.md`; carried
from Campaign 2 `CHARTER.md` + repository policy):

- merging the Campaign 3 PR;
- deploying or publishing externally;
- making an ADR `Accepted` because Campaign 3 recommends it;
- changing an owner-reserved product decision;
- treating campaign conclusions as canonical ratification;
- creating/closing/reopening/relabelling/materially modifying GitHub issues
  merely for campaign bookkeeping;
- merging unrelated PRs;
- altering protected repository policy to make Campaign 3 pass;
- inferring owner preference from repository evidence.

Standing owner-reserved items inherited from Campaign 2 (verify current state
before relying on them):

- the nine `docs/workflow-system-disposition.md` section 6 registry/overlay/
  contract/documentation decisions;
- Goal A execution-substrate authorization (Issue #255);
- ratification of any Campaign 2 conclusion (incl. the `STATUS.md` /
  `doc-status` marker convention — the marker was left **NON-NORMATIVE**) as
  product architecture;
- formal termination of Campaign 2 (already closed).

If otherwise-warranted progress crosses one of these boundaries, classify it as
`OWNER_DECISION_REQUIRED` rather than manufacturing authority.
