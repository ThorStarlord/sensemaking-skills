# Strategic Repository Analysis

## 1. Governing Intent and Scope

- **Target:** `ThorStarlord/sensemaking-skills` @ `aa13f40115b52f9e7687d742cbc8430d5a9a4a25`
  (clean; measured by `artifacts/history/2026-10-23-probe-report-observation.yaml`).
- **Owner-supplied intent for this episode:** observe the Skills operating on
  this repository. No strategic direction was supplied by the owner here.
- **Repository-owned strategy (governing):** ADR 0031 (Level 4, owner-selected
  2026-10-15). Its success condition is "better decisions in later, genuinely
  separate engineering episodes, not more ontology rows"
  (`docs/adr/0031-persistent-semantic-stewardship.md:127-128`). It builds
  incrementally (`:82-89`). ADR 0029 is the product boundary. `STATUS.md` is the
  current Level-3 projection: `CONSTRUCT / CURRENT_WORKSPACE_SEMANTIC_STEWARDSHIP`
  (`STATUS.md:238`).
- **Inferred purpose:** none added beyond those sources.
- **Authority boundary:** this request grants analysis only. Implementation,
  commits, PRs, merge and release are not authorized by this artifact.

## 1A. Strategic Continuity

`NEW`. No `strategic_repository_analysis` artifact currently governs. The last
one (`artifacts/history/2026-09-20-strategic-repository-analysis.md`) was
CLOSEd by `artifacts/history/2026-09-22-strategic-reconciliation.md`, and ADR
0031 post-dates both. This analysis tests the current `STATUS.md` projection
against the evidence returned by Stages 2-3. It does not replace the
projection or the owner's Level-4 choice.

**Strategic Exploration Funnel: not run.** Eligibility check
(`skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md`
section 2): Level 3 is current (STATUS reconciled at HEAD via PR #562), and a
new prompt alone does not reopen it. The analysis therefore asks one bounded
question: does the returned evidence reopen or redirect the frontier? Breadth
search is not repeated.

## 2. Current System Model

The product is a set of agent-facing Skills plus a local package. The relevant
systems for the governing intent are:

1. **Decision support:** the `using-sensemaking` loop, `repo-sensemaker`,
   `strategic-repository-analysis`, and validators.
   - *Observed:* the brief contract rejects non-conforming output.
   - *Observed:* the relationship gate separates mechanical from semantic findings.
2. **Persistent semantic knowledge (ADR 0031):** Git-reviewed JSON records, an
   external SQLite index, and orient/build/query/audit/proposal-check.
   - *Observed this episode:* index build, query, workspace disclosure and
     coverage reporting all behaved as documented; 46 tests pass.
3. **In-session context surfaces:** `CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, the
   operating map. These are loaded at session start and carry core product
   contracts directly. Example: runtime-owned artifact paths, `CLAUDE.md:83-90`.
4. **Legacy compatibility surface:** `runner.SkillsOrchestrator` and
   `workflow-runtime.py`.
   - *Observed:* one non-conforming brief producer that overwrites tracked
     artifacts (companion brief `artifacts/history/2026-10-23-repository-sensemaking-brief-observation.md`, Section 6).

**Claim ceiling:** in-session use only. Independent later-session reuse (S5)
and cross-product transfer (S6) are NOT TESTED (`STATUS.md:6`).

## 3. Capability and Limitation Map

| Capability | State | Evidence | Strategic relevance |
| --- | --- | --- | --- |
| knowledge-index-query | ESTABLISHED | session query receipt; 46 semantic tests pass | the substrate ADR 0031 requires exists |
| workspace-recall-disclosure | ESTABLISHED | `workspace_context` observed; `worktree_context.py:1-3` | agents can recall beside active work |
| reviewed-knowledge-semantic-plane | ESTABLISHED | 21 reviewed claims, all about the knowledge plane (`.sensemaking/knowledge/*.json`) | knowledge of the steward itself |
| reviewed-knowledge-product-contracts | MISSING | the other 31 indexed claims are ADR titles; `adr:0010` has 0 relations and no component/verification neighbors | the product outside the plane is unmodeled |
| core-contracts-in-session-context | ESTABLISHED | `CLAUDE.md:83-90` states path ownership; auto-loaded | lowers the cost of the gap above |
| brief-contract-enforcement | ESTABLISHED | `validate-brief.py` rejected the legacy output with 4 blocking errors | integrity checks work when used |
| artifact-path-ownership | PARTIAL | runtime owns paths, but `runner.py:181` -> `paths.py:69` bypasses it | a latent integrity defect |
| independent-session-reuse | DEFERRED | `STATUS.md:6` "Independent S5/S6 qualification remains open for release-stage verification" | the actual ADR 0031 value test |

## 4. Strategic Frontier

**FRONTIER-1: self-referential knowledge coverage.** Every reviewed claim
describes the knowledge plane itself. In this episode the steward answered a
question about itself (Steward RECALL), but contributed nothing to the diagnosis
(the companion brief). That diagnosis needed the path-ownership contract, which existed
only as an ADR title; it was rebuilt from `CLAUDE.md` and source code. This is
an instance of what ADR 0031 wants to prevent: later sessions reconstructing
consequential decisions (`docs/adr/0031-persistent-semantic-stewardship.md:12-17`).

- **Strategicity Gate:** passes. How reviewed coverage grows decides whether the
  ADR 0031 future capability state is reachable on the current construction
  order (dependency/ordering effect).
- **What does not pass the gate:** the legacy producer defect, the ADR
  0014->0029 citation drift, the steward-reference wording, and the
  `validate-artifact.py` Section 15 blind spot. They are bounded repairs, not
  Level-3 boundaries.

**Goal-fit note (GOAL_FIT_WARNING, semantic guidance only):**

- **Stated objective:** use the Steward during genuine engineering (STATUS).
- **Role:** milestone toward ADR 0031's terminal outcome.
- **Counterexample:** every in-session use can succeed while reviewed knowledge
  stays about the plane itself. Later sessions would then still reconstruct
  product decisions.
- **Optimization risk:** further query/infrastructure work. It is mechanically
  legible, and the last three integrated PRs (#558, #560, #561) were query
  mechanics.
- **Frontier consequence:** coverage growth must be represented explicitly.
  The owner's objective is not replaced.

## 5. Candidate Construction Paths

### PATH-1: Accrete product knowledge through genuine responsibilities

- **Future state:** each genuine engineering responsibility RECALLs, works, then
  RECONCILE-ADDs the consequential non-derivable knowledge it needed. That
  includes product contracts outside the plane, not only steward lessons.
- **Why plausible:** this is ADR 0031's incremental rule (`:82-89`) and the
  STATUS boundary. This episode shows a concrete ADD candidate: the path-ownership
  invariant linked to `runner.py`, `paths.py`, the runtime resolver and
  `validate-brief.py`.
- **Frontier grounding:** FRONTIER-1.
- **Builds on:** knowledge-index-query, workspace-recall-disclosure, reviewed-knowledge-semantic-plane.
- **Requires:** reviewed-knowledge-product-contracts (grown one contract at a time).
- **Construction sequence:** pick a genuine responsibility outside the plane ->
  RECALL (expect NOT ASSESSED) -> build -> ADD the source-linked contract with
  `implemented_by`/`tested_by` -> rebuild the index at the clean commit.
- **Path transitions:** `PATH-1/T1`: reviewed knowledge covers one product
  contract outside the semantic plane.
- **Dependencies:** genuine work outside the plane being selected at all.
- **Unlocks:** later RECALLs that return product context instead of NOT ASSESSED.
- **Risks / tradeoffs:** coverage tracks wherever work happens. If work keeps
  concentrating on the plane itself, coverage stays self-referential (the
  observed pattern).
- **Reversibility:** high; records can be superseded.
- **Evidence gaps:** whether accreted knowledge is actually reused by a later,
  separate session (S5).
- **Assumptions:** ASSUMPTION-1, ASSUMPTION-2.
- **Reassessment triggers:** several genuine responsibilities outside the plane
  close without any ADD; or a later session reconstructs a contract that an
  earlier session had touched.

### PATH-2: Bounded product-core BOOTSTRAP, then accrete

- **Future state:** one bounded BOOTSTRAP models the product's core contracts
  first: artifact contracts and path ownership, product boundary, authority
  model, brief/validator contracts. Accretion through use follows.
- **Why plausible:** the steward's BOOTSTRAP mode exists for "materially
  inadequate" knowledge (`skills/repository-semantic-steward/SKILL.md:14`), and
  outside the plane the knowledge is absent rather than thin.
- **Frontier grounding:** FRONTIER-1.
- **Builds on:** knowledge-index-query, reviewed-knowledge-semantic-plane.
- **Requires:** reviewed-knowledge-product-contracts (built up front).
- **Construction sequence:** orient -> model core contracts with competency
  questions -> review via PR -> index -> accrete.
- **Dependencies:** review effort for a larger knowledge PR.
- **Unlocks:** immediate product-wide RECALL coverage.
- **Risks / tradeoffs:** the Auteur first-use lesson warns against "broadening
  the ontology" before a real task benefits
  (`skills/repository-semantic-steward/references/qualification.md:21`). Much
  core-contract knowledge is already in auto-loaded `CLAUDE.md`, so up-front
  modeling may duplicate it. Staleness and maintenance cost.
- **Reversibility:** medium; the review effort is sunk.
- **Evidence gaps:** which core contracts later sessions actually need.
- **Assumptions:** ASSUMPTION-2.
- **Reassessment triggers:** PATH-1 shows no product ADD after several genuine
  responsibilities outside the plane.

**Orthogonality challenge.** Both paths assume more reviewed content helps
later sessions. The premise upstream of both is S5: do separate sessions use
the knowledge at all? "Obtain S5 evidence first" is an evidence state, not a
construction trajectory. The owner has already ruled that S5 does not gate
construction, and an independent executor is reported unavailable. It is
recorded as ASSUMPTION-1, not admitted as a third path.

## 6. Qualitative Path Comparison

| Lens | PATH-1 accrete | PATH-2 bootstrap first |
|---|---|---|
| mission relevance | direct, ADR 0031's own rule | direct |
| decision value | high: tests whether use-driven growth leaves the plane | medium: coverage without a consumer |
| blocking power | low: nothing waits on it | low |
| evidence sufficiency | this episode supplies one concrete ADD | weak: no evidence of which contracts are needed |
| consequence of error | small: slow coverage | moderate: unused, stale records and review cost |
| deferral cost | low per episode; compounds if work stays on the plane | low, since `CLAUDE.md` carries core contracts now |
| reversibility | high | medium |
| authority availability | within STATUS's current responsibility | larger knowledge PR still within ADR 0031, but heavier |
| dependency | needs genuine work outside the plane | needs review capacity |

Commission/omission:

- **Not pursuing PATH-2 risks** more reconstruction per session. That cost is
  bounded because core rules are already in loaded context.
- **Pursuing it wrongly risks** producing exactly the ontology rows ADR 0031
  says are not success.

## 7. Decision-Changing Uncertainty

Whether PATH-1's accretion leaves the semantic plane in practice.

- **Source:** repository_evidence. Knowledge-file history is inspectable as
  future episodes land.
- **Separate inquiry needed?** No. Doing PATH-1's next responsibility produces
  the evidence (reversible build-as-inquiry), so `inquiry_warranted: false`.

## 7A. Decision Assumptions and Reassessment Triggers

- **ASSUMPTION-1:** separately started later sessions will query reviewed
  knowledge when it is relevant. Evidence:
  `docs/adr/0031-persistent-semantic-stewardship.md:127-131`; status NOT TESTED.
  Trigger: an independent-session record shows reviewed knowledge was skipped,
  or was decisive.
- **ASSUMPTION-2:** auto-loaded context (`CLAUDE.md`) continues to carry core
  contracts. Evidence: `CLAUDE.md:83-90`. Trigger: core rules move out of
  auto-loaded files.

## 8. Strategic Synthesis

The returned evidence does not reopen Level 3. ADR 0031 and the STATUS boundary
("use the Steward during a genuine responsibility") still hold. The evidence
does sharpen what "genuine" should mean next: a responsibility **outside** the
knowledge plane, which ADDs the product knowledge it needed. The legacy
producer defect from the companion brief is such a responsibility. Fixing it would exercise
RECALL (expect NOT ASSESSED), a real code change, and a RECONCILE-ADD of the
path-ownership contract. PATH-1 is selected over PATH-2. It is ADR 0031's own
construction rule, more reversible, and this episode already supplies its first
transition. PATH-2's main benefit is partly provided today by auto-loaded
context.

## 9. Warranted Direction

**BUILD**, path `PATH-1`, transition `PATH-1/T1`.

- **Candidate bounded responsibility:** fix the legacy `run_repo_sensemaker_skill`
  producer (owner chooses remove vs fail-closed; the brief's open owner question) as a
  RECALL -> BUILD -> RECONCILE responsibility. In it, ADD a reviewed invariant
  for runtime-owned artifact paths with `implemented_by`/`tested_by` links.
- **Smallest warranted intervention:** the regression test asserting the legacy
  path cannot change tracked `artifacts/` files, plus the single ADD record.

## 10. Authority and Claim Boundaries

- Implementation authority is **not** established by this artifact; this episode
  is observation-only.
- The remove-vs-fail-closed choice is the owner's (public legacy API, `API.md:6`).
- Claim ceiling: in-session observation with manually loaded Skills. No S5,
  comparative or transfer claim.

```text
strategic analysis != implementation authorization
bounded repair != construction path
construction path != backlog
path transition != authorized responsibility
INVESTIGATE != EXPERIMENT
verification legibility != strategic importance
mechanically valid != semantically correct
```

## 11. Evidence

- `.sensemaking/knowledge/stewardship.json`, `.sensemaking/knowledge/repository-bootstrap.json`:
  21 reviewed claims, all about the knowledge plane.
- Index query at `aa13f40`: 52 claims = 21 reviewed + 31 ADR title/status;
  `explain adr:0010` returns 0 relations.
- `docs/adr/0031-persistent-semantic-stewardship.md:12-17, 82-89, 125-143`.
- `STATUS.md:6, 238`; `CLAUDE.md:83-90`.
- `src/sensemaking_skills/runner.py:181`, `src/sensemaking_skills/paths.py:69`
  (companion brief, Section 6).
- `skills/repository-semantic-steward/references/qualification.md:21`.

## 12. Machine-Readable Summary

```yaml
schema_version: 2
artifact_id: strategic_repository_analysis
analysis_ref: "SRA-2026-10-23-observation-aa13f40"
continuity:
  prior_analysis_ref: null
  disposition: NEW
  prior_selected_path_id: null
  reason: "No strategic_repository_analysis governs: the 2026-09-20 analysis was CLOSEd on 2026-09-22 and ADR 0031 post-dates it; this analysis tests the current STATUS.md Level-3 projection."
target_repository: ThorStarlord/sensemaking-skills
target_source_identity: "aa13f40115b52f9e7687d742cbc8430d5a9a4a25"
governing_intent: "ADR 0031 persistent semantic stewardship: better decisions in later, genuinely separate engineering episodes, built incrementally; STATUS.md projects CONSTRUCT / CURRENT_WORKSPACE_SEMANTIC_STEWARDSHIP."
governing_authority_refs:
  - docs/adr/0031-persistent-semantic-stewardship.md
  - docs/adr/0029-current-product-boundary.md
  - STATUS.md
capability_states:
  - capability_id: knowledge-index-query
    state: ESTABLISHED
    evidence_refs:
      - "src/sensemaking_skills/semantic_architecture/knowledge_store.py"
      - "tests/test_semantic_knowledge.py"
  - capability_id: workspace-recall-disclosure
    state: ESTABLISHED
    evidence_refs:
      - "src/sensemaking_skills/semantic_architecture/worktree_context.py:L1-L3"
  - capability_id: reviewed-knowledge-semantic-plane
    state: ESTABLISHED
    evidence_refs:
      - ".sensemaking/knowledge/stewardship.json"
      - ".sensemaking/knowledge/repository-bootstrap.json"
  - capability_id: reviewed-knowledge-product-contracts
    state: MISSING
    evidence_refs:
      - "knowledge-query explain adr:0010 @ aa13f40: 0 relations"
  - capability_id: core-contracts-in-session-context
    state: ESTABLISHED
    evidence_refs:
      - "CLAUDE.md:L83-L90"
  - capability_id: brief-contract-enforcement
    state: ESTABLISHED
    evidence_refs:
      - "scripts/validate-brief.py"
  - capability_id: artifact-path-ownership
    state: PARTIAL
    evidence_refs:
      - "src/sensemaking_skills/runner.py:L181"
      - "src/sensemaking_skills/paths.py:L69"
  - capability_id: independent-session-reuse
    state: DEFERRED
    evidence_refs:
      - "STATUS.md:L6"
strategic_frontier:
  - frontier_id: FRONTIER-1
    statement: "Reviewed knowledge covers only the knowledge plane; product contracts outside it exist only as ADR titles."
    evidence_refs:
      - ".sensemaking/knowledge/stewardship.json"
      - "knowledge-query explain adr:0010 @ aa13f40: 0 relations"
      - "docs/adr/0031-persistent-semantic-stewardship.md:L12-L17"
    affected_capability_ids:
      - reviewed-knowledge-product-contracts
      - independent-session-reuse
    strategic_consequence: "How reviewed coverage grows decides whether ADR 0031's later-session decision benefit is reachable on the current construction order."
construction_paths:
  - path_id: PATH-1
    name: "Accrete product knowledge through genuine responsibilities"
    future_state: "Each genuine responsibility outside the knowledge plane RECONCILE-ADDs the source-linked product knowledge it needed."
    frontier_refs:
      - FRONTIER-1
    why_plausible: "ADR 0031 prescribes incremental construction and STATUS selects genuine Steward use; this episode supplies a concrete first ADD (runtime-owned artifact paths)."
    builds_on_capability_ids:
      - knowledge-index-query
      - workspace-recall-disclosure
      - reviewed-knowledge-semantic-plane
    required_capability_ids:
      - reviewed-knowledge-product-contracts
    construction_sequence:
      - "Select a genuine responsibility outside the knowledge plane"
      - "RECALL, build, then ADD the source-linked contract with implemented_by/tested_by links"
      - "Rebuild the index at the clean commit"
    path_transitions:
      - transition_ref: PATH-1/T1
        transition: "Reviewed knowledge covers one product contract outside the semantic plane"
    dependencies:
      - "Genuine work outside the knowledge plane is selected"
    unlocks:
      - "Later RECALLs return product context instead of NOT ASSESSED"
    risks:
      - "Coverage stays self-referential if work keeps concentrating on the knowledge plane"
    reversibility: "High; reviewed records can be superseded with history preserved."
    evidence_gaps:
      - "Whether a later separate session reuses accreted knowledge (S5)"
    assumptions:
      - "ASSUMPTION-1"
      - "ASSUMPTION-2"
    reassessment_triggers:
      - "Several genuine responsibilities outside the plane close without any ADD"
      - "A later session reconstructs a contract an earlier session already touched"
  - path_id: PATH-2
    name: "Bounded product-core BOOTSTRAP, then accrete"
    future_state: "Core product contracts are modeled up front, then knowledge grows through use."
    frontier_refs:
      - FRONTIER-1
    why_plausible: "The Steward's BOOTSTRAP mode exists for materially inadequate knowledge, and product-contract knowledge is absent rather than thin."
    builds_on_capability_ids:
      - knowledge-index-query
      - reviewed-knowledge-semantic-plane
    required_capability_ids:
      - reviewed-knowledge-product-contracts
    construction_sequence:
      - "Orient and model core contracts against competency questions"
      - "Review via PR, index, then accrete"
    dependencies:
      - "Review capacity for a larger knowledge change"
    unlocks:
      - "Immediate product-wide RECALL coverage"
    risks:
      - "Unused or stale records; duplicates rules already in auto-loaded CLAUDE.md; Auteur lesson against broadening before tasks benefit"
    reversibility: "Medium; review effort is sunk even if records are superseded."
    evidence_gaps:
      - "Which core contracts later sessions actually need"
    assumptions:
      - "ASSUMPTION-2"
    reassessment_triggers:
      - "PATH-1 shows no product ADD after several genuine responsibilities outside the plane"
path_comparison:
  - path_id: PATH-1
    lenses:
      mission_relevance: "Direct; ADR 0031's own incremental rule."
      decision_value: "High; tests whether use-driven growth leaves the plane."
      blocking_power: "Low; nothing waits on it."
      evidence_sufficiency: "This episode supplies one concrete ADD."
      consequence_of_error: "Small; coverage grows slowly."
      deferral_cost: "Low per episode, compounding if work stays on the plane."
      reversibility: "High."
      authority_availability: "Within STATUS's current responsibility."
      dependency: "Needs genuine work outside the plane."
  - path_id: PATH-2
    lenses:
      mission_relevance: "Direct."
      decision_value: "Medium; coverage without a demonstrated consumer."
      blocking_power: "Low."
      evidence_sufficiency: "Weak; no evidence of which contracts are needed."
      consequence_of_error: "Moderate; unused, stale records and review cost."
      deferral_cost: "Low; auto-loaded CLAUDE.md already carries core contracts."
      reversibility: "Medium."
      authority_availability: "Within ADR 0031 but a heavier knowledge change."
      dependency: "Needs review capacity."
decision_changing_uncertainty:
  statement: "Whether PATH-1 accretion actually adds product knowledge outside the semantic plane."
  could_change: "PATH-1 versus PATH-2 selection"
  inquiry_warranted: false
  evidence_needed: "The next genuine responsibility outside the plane, performed as reversible build-as-inquiry"
  source: repository_evidence
decision_assumptions:
  - assumption_id: ASSUMPTION-1
    statement: "Separately started later sessions will query reviewed knowledge when it is relevant."
    evidence_refs:
      - "docs/adr/0031-persistent-semantic-stewardship.md:L127-L131"
    reassessment_triggers:
      - "An independent-session record shows reviewed knowledge was skipped or was decisive"
  - assumption_id: ASSUMPTION-2
    statement: "Auto-loaded context continues to carry core product contracts."
    evidence_refs:
      - "CLAUDE.md:L83-L90"
    reassessment_triggers:
      - "Core rules move out of auto-loaded files"
strategic_disposition: BUILD
selected_path_id: PATH-1
candidate_repository_responsibility: "Fix the legacy run_repo_sensemaker_skill producer (owner chooses remove vs fail-closed) as RECALL -> BUILD -> RECONCILE, adding a reviewed runtime-owned-artifact-path invariant with implemented_by/tested_by links."
candidate_path_transition_ref: PATH-1/T1
smallest_warranted_intervention: "A regression test asserting the legacy path cannot change tracked artifacts/ files, plus one reviewed ADD record."
implementation_authority_established_by_artifact: false
semantic_truth_established: false
created_at: "2026-10-23T06:05:00Z"
immutable: true
```
