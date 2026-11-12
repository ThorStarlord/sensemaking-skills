# Sensemaking Continuous Learning (SCL) — Development and Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL when executing an authorized bounded implementation task: use `superpowers:subagent-driven-development` (when available) or `superpowers:executing-plans`, respecting the repository's current override to **not add or manually run local unit/synthetic tests**. Checklist entries track work; this program is **not an automatic backlog or permission to alter strategy, Skills, schemas, host policy or another repository**.

**Goal:** Evolve Sensemaking from source-linked repository memory into an explicit, eventually routine, experience-driven product capability: every observable engineering episode is considered for learning, consequential learning improves later decisions, and reusable methodology improves only with evidence and authority.

**Architecture:** Reuse `using-sensemaking` as the sole semantic controller, existing Learning/Reconciliation, reviewed Git-authored lesson sources, the repository semantic knowledge CLI/`context-for`, receipts, Campaigns and strategic reconciliation. Prioritize one real later-agent decision-time retrieval-and-feedback vertical; then build selective episode learning into ordinary practice; only afterward consider cross-episode synthesis, broader automation and governed transfer.

**Tech Stack:** Existing Python >=3.11 package, Click `semantic_cli.py`, source-pinned authored schema v1/v2 and knowledge projection, SQLite outside working checkout, Git/PR evidence, portable Markdown Skills, optional existing Campaign/receipt YAML. No new service/database/framework by default.

**Spec:** [SCL Product Design v0](../specs/2026-11-12-sensemaking-continuous-learning-design.md).

**Planning baseline:** `ThorStarlord/sensemaking-skills@3a5658b58029535dd5400388343cac8e760c3468` (2026-11-12); current at planning time; must refresh immediately before any task.

**Prerequisite:** The owner selected SCL as an explicit future capability and learning eligibility across engineering episodes; [ADR 0035](../../adr/0035-sensemaking-continuous-learning.md) records that product-end ratification. All implementation/empirical qualification and protected authority gates remain separate; no future capability is presumed to work merely because it is selected.

## Global Constraints

- Current product thesis, ADR [0029](../../adr/0029-current-product-boundary.md), [0031](../../adr/0031-persistent-semantic-stewardship.md), [0034](../../adr/0034-ontology-first-adaptive-sensemaking.md), [0035](../../adr/0035-sensemaking-continuous-learning.md), `docs/product-thesis-revision.md`, and `STATUS.md` govern. Do not conflate strategy endorsement, implementation permission, knowledge record authority or release authority.
- [Existing Longitudinal Engineering Learning program](2026-11-02-longitudinal-engineering-learning.md), PRs #702–705, [Capability Learning Loop v0](../../research/capability-learning-loop-v0.md), [Learning/Reconciliation](../../../skills/using-sensemaking/references/learning-reconciliation-policy-v0.md) and [adaptive-methodological divergence](../../explorations/2026-11-12-adaptive-methodological-learning-divergent-exploration.md) are inputs, **not** an unexecuted blank slate.
- Retained ≠ retrieved ≠ checked ≠ decision-informing ≠ outcome-supported ≠ independently reused ≠ comparatively beneficial. Do not record a semantic inference as source evidence or a retrospective account as a time-ordered original trace.
- Every *observable* engineering episode is eligible for lightweight interpretation; an episode may warrant `NO_MODEL_CHANGE` and no additional durable document. Learning from every episode ≠ persisting every episode in a central learning log.
- Origin/retention/applicability/authority must be preserved across sessions. Receiving repository intent controls; no automatic foreign-repository mutation, Skills or policy rewrite, model-weight training, universal `LearningEngine` or new mandatory semantic controller.
- Source documents and Git-reviewed authorship govern; SQLite projection is a rebuildable exact-revision index. Do not silently mix target revisions, worktrees, hosts, agent contexts or source and result timestamps. Missing/sparse retrieval is `NOT_ASSESSED`, not proof of no lessons.
- Use the *existing* knowledge schema, `lesson` claim and `learned_from` relationship when suitable. A new field, relation, CLI command, hook or Skill requires a named concrete consumer gap, compatible contract and separate authority.
- Local construction rule in `CLAUDE.md` / `docs/agents/build-loop.md`: **do not add or manually run local unit or synthetic evidence tests now**; inspect actual source/diff and permissible non-test checks, mark `NOT_RUN`, respect hosted verification/protections, and repair material failures. If the owner later lifts this exception, use the deferred test ideas below.
- One bounded `claude/<topic>` branch/PR per valuable increment; explain actual value/alternatives and evidence limits, review exact diff, merge only under applicable authorization and current repository policy. Do not claim hosted CI before it completes.
- Preserve low ceremony, Windows console ASCII-only output and no private chain-of-thought or secret-bearing evidence collection. Do not create a duplicate universal `LEARNINGS.md`, append-only journal or memory ranking scores.

## Review Focus (five probable failure modes)

1. **Historical advice is irrelevant, stale or contradicted:** surface its source and exclusions; permit justified refusal; never blindly suggest a prior method. Owned by Tasks 3–5. Deferred contract case: `test_scl_rejects_stale_or_inapplicable_lesson`.
2. **The agent never actually encountered the stored lesson:** distinguish indexed/retrieved from original predecision read evidence; do not claim influence from search availability. Owned by Tasks 2, 4 and 7. Deferred case: `test_scl_evidence_ceiling_predecision_encounter`.
3. **The method changes which errors become visible:** avoid labeling detection differences as method quality. Preserve negative and ambiguous results. Owned by Tasks 5 and 8. Deferred case: `test_scl_does_not_infer_effectiveness_from_detection_count`.
4. **Knowledge from one repo claims authority over another:** enforce current owner, source and permissions; no automatic application or mutation. Owned by Tasks 6 and 9. Deferred case: `test_scl_cross_repo_transfer_never_grants_authority`.
5. **Learning adds process cost without product value:** allow NO_CHANGE, absence of dedicated artifact, direct ACT and bounded failure; assess overhead and user outcomes. Owned by Tasks 1, 3, 8 and 10. Deferred case: `test_scl_trivial_episode_requires_no_new_artifact`.

No named deferred tests above have been added or run by this plan. They are *review scenarios* until the owner's construction policy changes and a real corresponding executable consumer exists.

---

## Program structure — durable value first, then generality

| Milestone | Deliverable | Gate to next | Evidence status at plan baseline |
| --- | --- | --- | --- |
| M0 — Design and authority alignment | Source-grounded SCL spec, this plan, no strategy overwrite | Owner understands and, where required, ratifies product commitment | This PR is planning only |
| M1 — Decision-time reuse | A fresh real engineering actor encounters and appropriately uses/rejects a historical lesson | Original predecision source exposure and later action are reconstructible | Independent end-to-end evidence **open** |
| M2 — Feedback loop | Consequential results revise, narrow, confirm or retain the historical interpretation without false promotion | Source-current feedback is usable by another actor | **Open** |
| M3 — Default episode learning | Learning eligibility is available to all in-scope observable episodes with justified NO_CHANGE and negligible overhead | Real-use coverage and false-positive/noise cases are inspected | **Open** |
| M4 — Capability learning | Comparable independent episodes justify a bounded reusable methodological improvement | Counterevidence and current authority reviewed; actual downstream guidance consumer | Candidate, **not** general runtime |
| M5 — Long-horizon qualification and transfer | Independent use, acceptable comparative outcomes and explicitly authorized cross-repository analogy | Beneficiary evidence and total cost support continuation | **Open** |
| M6 — Conditional further automation | Only proven missing seams receive mechanized support | Each mechanism has a consumer, review and retirement rule | **Not preselected** |

Each milestone can stop at NO_CHANGE, insufficient evidence or a genuinely protected boundary. Prior milestone success does not authorize all later work.

## Task 0 — Lock the source and authority boundary (planning increment)

**Files:**
- Create: `docs/superpowers/specs/2026-11-12-sensemaking-continuous-learning-design.md`.
- Create: `docs/superpowers/plans/2026-11-12-sensemaking-continuous-learning.md`.
- Read-only: `docs/product-strategy.md`, `docs/product-thesis-revision.md`, ADRs 0029/0031/0034 and `docs/research/capability-learning-loop-v0.md`.

**Interface:** Produces the design and proposed program, not a new API, accepted claim of runtime behavior, strategy mutation or owner approval of all later implementation.

- [ ] Read the current authority and exact `main`; compare with this plan's baseline and reconcile changed scope.
- [ ] Confirm SCL is framed as a **proposed explicit capability**, consistent with semantic stewardship and `using-sensemaking`.
- [ ] Make any genuinely required Level-4 ratification a **separate owner-authorized decision** using `docs/product-thesis-revision.md`; do not sneak it into a local feature PR.
- [ ] Review planning diff and link the existing #702–705 work as pre-existing, not "tasks to redo".
- [ ] PR review outcome: accurate planning text and navigable spec/plan; no behavior or CI qualification claim.

**Completion:** Two reviewed planning artifacts; no product strategy change hidden in their commit.

## Task 1 — Define first consumer question from ordinary work

**Files:**
- Inspect: `.sensemaking/knowledge/stewardship.json`, `skills/repository-semantic-steward/references/recall.md`, `docs/semantic-architecture/persistent-knowledge-cli.md`, `src/sensemaking_skills/semantic_architecture/knowledge_architecture.py` and `src/sensemaking_skills/semantic_architecture/knowledge_store.py`.
- If consequential: create one dated, sourced `docs/normal-use/<date>-scl-decision-time-baseline.md` (use an actual date and evidence sources, not the literal placeholder).

**Interface:** Input = an actual forthcoming task with decision uncertainty and an existing source-qualified relevant prior `lesson`. Output = source-addressed question, target agent/host and available evidence; no proposed answer forced onto the actor.

- [ ] Select a genuine engineering responsibility *independently of the learning demonstration*. Prefer a task that naturally needs a past lesson; do not manufacture an implementation task to make a metric pass.
- [ ] Identify the real source-file/component or concern and current repository revision before choosing a known lesson ID.
- [ ] Source-check historical lesson origin, relation, counterevidence and task applicability. Inspect the #702–705 path before alleging a missing retrieval capability.
- [ ] State the precise uncertainty: does `context-for` already surface what a fresh agent needs at its decision, or is a concrete consumer gap present?
- [ ] If no valid episode/consumer is available, record `NOT_EXECUTED` / `NO_WARRANTED_RETRIEVAL_CHANGE` and stop; do not substitute retrospective self-claims.

**Completion:** An independently meaningful, source-grounded episode question whose value does not depend on proving SCL works.

## Task 2 — Reuse the current source-qualified retrieval path

**Files:**
- Read: `src/sensemaking_skills/semantic_architecture/knowledge_retrieval.py`, `knowledge_architecture.py`, `knowledge_store.py`, `src/sensemaking_skills/semantic_cli.py`, `skills/repository-semantic-steward/references/recall.md`.
- Modify only **if a real decision-time consumer fails**: narrow affected module, corresponding CLI/Skill reference and `docs/semantic-architecture/persistent-knowledge-cli.md`.

**Interface:** Consumer receives historical lesson/source links with explicit target revision and source caveats. No new machine output shape or `learning-context` CLI is presumed.

- [ ] On a clean exact-revision checkout, use the existing `semantic knowledge-build`, `knowledge-query` and, where appropriate, `context-for` operations documented in the CLI contract; no stale database reuse.
- [ ] Compare the returned lesson candidates with actual original-source material; mark missing reachability separately from misleading applicability.
- [ ] If current retrieval already answers the decision question, **make no code change**. Prefer using the existing capability in Task 3.
- [ ] If it fails a real question, select the smallest of: reviewed graph relation correction, bounded RECALL/reference clarification, or narrow existing query behavior repair. A new schema/hook/service is last, conditional and separately warranted.
- [ ] For any bounded change, review exact source/diff, run permissible non-test mechanical/real CLI checks, open its own PR, state local unit tests `NOT_RUN` and record hosted CI separately.

**Completion:** A source-correct decision-time retrieval path exists for the chosen case, whether pre-existing or minimally repaired. Retrieval is not yet learning benefit.

## Task 3 — Make episodic learning consideration ordinary but cheap

**Files:**
- Read/conditionally modify: `skills/using-sensemaking/references/learning-reconciliation-policy-v0.md`, `skills/using-sensemaking/SKILL.md` and `docs/agent-native-operating-workflow.md`.
- Prefer **no new** receipt/schema/mandatory artifact owner.

**Interface:** Active semantic controller, when consequential evidence returns, decides **retain/revise/contest/no change** in the owning surface; a small episode can continue directly.

- [ ] Inspect whether existing Learning/Reconciliation already asks the right post-result questions. Do not introduce an "SCL stage" just to display deliberate activity.
- [ ] If ordinary observed episodes expose a real omission, add one bounded default learning-eligibility reminder at the *existing* evidence-return seam, with the no-change/no-artifact exit and both product/method dimensions explicit.
- [ ] Explain precisely why the reminder needs front-door visibility; otherwise place detail in the existing reference, keeping `using-sensemaking` lightweight.
- [ ] Check three real counterconditions in source/diff review: routine one-line edit, consequential contradictory result, and blocked/unobserved task. They must not automatically produce identical lesson records.
- [ ] Commit only if source-supported value exceeds the prompt/maintenance tax. Else `NO_GUIDANCE_CHANGE`.

**Completion:** Ordinary agent guidance makes episode learning **eligible by default** without requiring work to stop or write additional files. Behavioral prevalence remains unqualified.

## Task 4 — Observe a real later decision and protect the evidence ceiling

**Files:**
- Use the selected task's original PR/receipts/Campaign/source revisions.
- Conditionally create: one bounded `docs/normal-use/<date>-scl-decision-use.md` containing original source anchors and limitations.

**Interface:** Qualitative evidence progression: original fact; retained record; actual read; source-checked applicability; use/adapt/reject; returned result; independence/comparison. No schema enum or inferred invisible thinking.

- [ ] Let an **independent later coding-agent session** perform the real engineering task with normal instructions. Do not pre-instruct it to mention, use or praise the lesson.
- [ ] Determine whether an original accessible predecision event shows lesson exposure; if not, report `RETRIEVAL_NOT_OBSERVED` even if a retrospective receipt says "used".
- [ ] Inspect actual source verification and decision consequence. Justified rejection counts; an unobserved decision cannot be reconstructed from a fluent post-hoc narrative.
- [ ] Compare actual task result with initial purpose and authority; identify omissions, contradictory cases and the cost of prior knowledge.
- [ ] Store only necessary, nonsecret, source-pinned outcome facts; attribute actor, reviewed revision and claim ceiling.
- [ ] If fresh executor is unavailable, **stop at documented independent-use gap**, not a simulated qualifying task.

**Completion:** The strongest genuinely observed evidence rung is named; the next action follows the gap, not the desired success label.

## Task 5 — Close the episode-to-future-episode feedback loop

**Files:**
- Existing owning source as warranted: `.sensemaking/knowledge/stewardship.json` or another already authorized `.sensemaking/knowledge/*.json` record; `docs/normal-use/`, PR history, Campaign/handoff, `STATUS.md` only for material strategy/capability state.
- Relevant guidance: `skills/using-sensemaking/references/learning-reconciliation-policy-v0.md`.

**Interface:** Original observation remains immutable; a distinct later interpretation may confirm, narrow, contest, supersede or decline change.

- [ ] Identify what the later decision **actually** taught: product fact, conditional method applicability, retrieval failure, stale source, authority issue, or nothing generalizable.
- [ ] Reconstruct original sources/revisions and any counterevidence; do not overwrite history to make the lesson appear accurate at all times.
- [ ] Preserve only consequential knowledge in its existing durable owner. If a `lesson` graph claim is warranted, use existing allowed kinds/relationships and validators; do not invent a `MethodLesson` type.
- [ ] For an inapplicable precedent, preserve a justified rejection and `NO_MODEL_CHANGE` when accurate; for a contested lesson, retain dated interpretation and provenance.
- [ ] Check that a still-later session can reconstruct the revision/limits using original source and normal existing lookup.

**Completion:** One real feedback consequence is retained or deliberately left unchanged, with traceable rationale and without a duplicate learning database.

## Task 6 — Productize the capability boundary, not the mechanism count

**Files:**
- Conditional Level-4: `docs/product-strategy.md`, appropriate accepted ADR per `docs/product-thesis-revision.md` (requires actual owner ratification).
- Level-3 and user-facing: `docs/research/capability-learning-loop-v0.md`, `docs/semantic-architecture/persistent-knowledge-cli.md`, `skills/using-sensemaking/SKILL.md` only if its actual consumer needs a front-door pointer.

**Interface:** Publicly explainable SCL promise and clearly qualified current features; no new second controller or automatic policy authority.

- [ ] Once owner-ratified, distinguish **SCL as an intended product capability** from the historical `Capability Learning Loop v0` as a research/architecture model. Reconcile wording, do not erase earlier evidence ceilings.
- [ ] Define a consumer-facing question a user can actually ask ("What did we learn from the last relevant engineering decision, and does it apply here?").
- [ ] Connect that question to real supported behavior and fallback: source-pinned lesson query, original source inspection, conditional application and feedback. Do not advertise autonomous extraction or beneficial use until observed.
- [ ] Update public naming/documentation only for working pathways, and show `NOT_ASSESSED` or unavailable scope accurately.
- [ ] Avoid separate `scl` command, persistent service, ranking/scoring or dashboards unless the ordinary consumer exposes a specific missing capability not solved by the existing CLI.

**Completion:** SCL is a product-defined capability with visible, accurately described integrated behavior, not just a new brand label.

## Task 7 — Qualify default coverage and low overhead

**Files:** Existing normal-use receipts/PR history; a bounded source-pinned `docs/normal-use/<date>-scl-coverage-and-cost.md` only if the evidence materially helps the next decision.

**Interface:** Describe observable episode opportunities, learning attempts/decisions and material omissions. Do not require every task to emit a new report.

- [ ] Inspect a representative spread of actual ordinary episodes (quick direct fix, ambiguous consequential work, failed/blocked work, no-change, strategic reasoning), without manufacturing tasks to fill categories.
- [ ] Determine what was *observable*: source revision, returned evidence, after-result consideration and whether a relevant lesson needed retention.
- [ ] Separate "no observed trace" from "no learning occurred." Report coverage limitations honestly.
- [ ] Identify process cost, repetitive rediscovery, false lesson retention, missed consequential signals and incorrect suppression.
- [ ] Only a demonstrated recurring deficiency warrants bounded instrumentation or repair. Do not require a `NO_CHANGE` artifact from all small tasks merely to improve coverage numerators.

**Completion:** Evidence supports or limits the claim that learning consideration occurs in normal work with acceptable cost. If not, select one concrete correction, not an automatic logger.

## Task 8 — Cross-episode methodological synthesis and guarded improvement

**Files:**
- Existing `docs/research/capability-learning-loop-v0.md` and `skills/using-sensemaking/references/learning-reconciliation-policy-v0.md`.
- Source-appropriate case record or PR rationale if a material synthesis must survive.
- Existing affected Skill/reference/runbook only after a separately warranted change.

**Interface:** Comparable original episodes -> bounded pattern/contrary cases -> context-qualified candidate -> smallest warranted change -> later independent qualification.

- [ ] Select authentically independent comparable episodes; record difference in goals, model/host, code and decisions. Do not make "two episodes" a magic proof threshold.
- [ ] Determine a plausible common mechanism, competing explanations and examples where the proposed rule fails.
- [ ] Address exposure effects (a VERIFY-heavy method may find more defects) and delayed benefit/harm before claiming a method is better.
- [ ] Compare options: existing guidance sufficient, local exception, explicit conditional guidance, deterministic contract, or `NO_CHANGE`. Prefer the smallest useful change.
- [ ] If guidance change warranted, review only the relevant Skill/reference or runbook; never auto-modify universally. Preserve owner/merge/release authority and independent future-use check.
- [ ] Add a separate `capability-learning-analysis` Skill or parsed schema only if repeated real cases demonstrate stable omitted responsibility and a working consumer.

**Completion:** One governed reusable improvement is qualified **or** the evidence-backed conclusion is to avoid generalization. More method changes is not a success metric.

## Task 9 — Optional governed cross-repository experience transfer

**Files:** Only current recipient repository's authorized own artifacts and original source-link references; target changes require distinct approval.

**Interface:** Transfer source-grounded *information and applicability questions*, never normative instructions or permissions from a foreign repository.

- [ ] Verify receiving repository's current purpose, schema, accepted owner intent and privacy constraints before importing a lesson.
- [ ] Identify common causal mechanism and materially different conditions, including what would make transfer wrong.
- [ ] Present candidate historical analogy for active agent judgment; source and revision remain visibly foreign.
- [ ] Require separate authorization for any repository modification or common reusable doctrine update.
- [ ] Observe one independent receiving-agent use or justified rejection; do not infer broad transfer success from one example.

**Completion:** A target-local, properly authorized use or rejection is reconstructible; failure or no-change is a valid result.

## Task 10 — Outcome qualification, learning economy and conditional automation

**Files:** Original engineering outcomes, authorized normal-use evidence and existing `STATUS.md` only when product capability/strategy changes materially.

**Interface:** A qualitative product evidence report about value and cost, not a score-based automatic method router.

- [ ] Examine meaningful outcomes: prevented rediscovery, changed wrong assumption, better product/responsibility selection, lower rework and continued authority compliance.
- [ ] Compare against a credible alternative when the claim needs it: absence of prior lesson, different retrieval exposure, contemporaneous independent observation or bounded same-task reinspection. Do not invent controlled comparisons.
- [ ] Count the *cost of learning activity*, stale/irrelevant context, maintenance burden and opportunity cost of delaying construction.
- [ ] Publish limits as limits: retention only, read-only retrieval, independent use, supported outcome or comparative value.
- [ ] Consider automation only if repeated reliable episodes expose a narrow routine machine-checkable seam whose product benefit outweighs false positives, privacy, cost and authority risk.
- [ ] Choose `RETAIN / REVISE / RETIRE / STOP` with a source-grounded rationale. No presumption that an SCL service must eventually exist.

**Completion:** A defensible keep/change/stop decision for SCL's current implementation scope, including negative results and explicit nonclaims.

---

## Execution sequencing and separate PRs

**Recommended immediate priority:** Tasks **1–2** as one authentic consumer-oriented increment if the case is real; **3** only for a proven guidance gap; **4–5** when an independent task actually happens. Task 0 is completed by creating the planning proposal, not by rewriting authority. Do **not** defer cheap retained product value merely to run a new experiment; the existing query/lesson capability can be used now.

**Suggested independent PR boundaries (conditional):**
1. `SCL-P0` — design and program (this documentation PR).
2. `SCL-P1` — actual decision-time episode source analysis + one smallest useful retrieval repair *if needed*, otherwise a bounded no-change note.
3. `SCL-P2` — inexpensive learning-consideration guidance correction *only when observed omission warrants it*.
4. `SCL-P3` — original-source-grounded later-agent application/rejection and feedback; do not manufacture independent trace.
5. `SCL-P4` — ratified product definition and truthful user-facing behavior, separately from code (owner decision).
6. `SCL-P5+` — cross-episode improvement, coverage assurance, transfer or mechanization **only after their gates**.

**Implementation-specific plans:** Tasks 2, 6 and 8–10 may reveal genuinely different code subsystems. When that happens, author a compact, consumer-derived implementation subplan containing exact function signatures and deferred/allowed verification for that bounded change; never guess an API before the defect is verified. This program is a roadmap of *warranted responsibilities*, not one monolithic build instruction.

## Evidence-based stopping / continuation

- **STOP / NO_CHANGE:** existing knowledge already answers the next relevant choice, no material lesson exists, or new records would just duplicate history.
- **INVESTIGATE:** outcome/consumer is consequential but correct next action hinges on source or read-event uncertainty.
- **BUILD / REVERSIBLE BUILD:** a real user-facing gap is source-proven, small and compatible with authority; deliver retained product value rather than duplicate experimental scaffolding.
- **QUALIFY:** integration is useful but independent actor behavior or causal benefit remains unknown; report exact ceiling.
- **ESCALATE / OWNER DECISION:** Level-4 product ratification, foreign repository writes, autonomous self-modification, protected changes, or other scope conflicts.
- **REVISIT / RETIRE:** recurring negative transfer, noisy memory, stale applicability, accidental authority import, excessive overhead or weaker beneficiary outcomes.

**Success definition:** A later agent can answer *"What did earlier engineering teach us that is applicable here, how do we know, what is different, and did using—or rejecting—that experience improve the next decision?"* using actual sources. Product improvement and warranted restraint both count; a higher artifact count does not.

