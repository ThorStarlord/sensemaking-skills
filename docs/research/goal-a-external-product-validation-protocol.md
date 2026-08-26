# Goal A — External Product Validation Protocol v1.0 FINAL (Canonical)

**Status:** APPROVED — owner approved this protocol v1.0 FINAL in a dedicated protocol design/review session (Decisions 0 and A–E); amended 2026-08-26 by owner decision (§34 owner decision F) to replace the mandatory human-usefulness authority with an independent-evaluator usefulness authority and explicit human claim ceilings.
**Authority:** No episodes are authorized by this document. Episode execution requires a separate, explicit owner authorization.
**Repository mutations:** None authorized by this document.
**Goal A:** ACTIVE — successor product-validation strategy
**A1:** ACTIVE (absolute product utility)
**A2:** DEFERRED / UNAUTHORIZED (incremental value, Decision E)
**Goal B / research-grade E3:** FROZEN / DEFERRED
**Document status:** CANONICAL — this file is the single source of truth for the approved Goal A protocol. Do not redesign or re-litigate the protocol; make bounded revisions only through a fresh owner-approved review.
**Amendment note (2026-08-26):** This version of the protocol (v1.0 FINAL, amended) substitutes the **independent usefulness evaluator** (E1–E7) for the previously mandatory **actual-human decision-owner review** (H1–H7). The amendment is prospective from canonicalization; it does not rewrite or relabel any completed Goal A evidence artifact (§27.3, §30.2, §34 owner decision F).

---

## 1. Relationship to prior governance (Decision 0 — approved)

This protocol reconciles with, but does not subordinate itself to, prior external-validation governance.

**Corrected E4 history (grounded in the committed record):**

- **Issue #83** authorized **one** Stage 1 run. That run **FAILED** and the issue was **closed**.
- **Evidence 0014 and 0015** record **later, separately authorized controlled Stage 1 attempts**. They are **not** what closed Issue #83, and are not described as such here.
- The **only consequential conclusion preserved**: the E4 lineage is **historical** and **grants no Goal A authorization**.

**Governance picture:**

```text
D8
= valuable prior owner-ratified external-validation evidence bar
= inherited as evidence guidance, NOT as a current binding readiness authority

E4 / Issue #83
= historical staged execution program
= one authorized Stage 1 run FAILED and closed; later controlled attempts (0014/0015)
  are historical records
= NOT silently reopened; no execution authorization inherited

ADR 0021
= SUPERSEDED as current product-wide readiness authority
  (retained only as historical rationale for D7/D8/E4)

Issue #218
= the canonical normal-use evidence lane; UNCHANGED by this protocol (see §9.2)

Goal A
= current product-validation responsibility
= reuses the useful D8 evidence requirements
= creates NO competing readiness definition
= inherits NO E4 execution authorization
```

**Consequences:**

- **Goal A is not "E4 resumed."** It proceeds under its own protocol, and any execution requires a **separate, future owner authorization** — this document grants none.
- **`A1_POSITIVE` is a product-validation conclusion used to decide what to build next.** It does **not** automatically change the repository's readiness/maturity label.
- A formal **"Externally Validated"** readiness claim, if later wanted, requires a **separate readiness review** against whatever authority is current at that time. Goal A results inform that review; they do not self-authorize it.

---

## 2. Product questions

### A1 — Absolute product utility (ACTIVE)

> **Does the ratified Sensemaking repository-sensemaking core produce grounded, decision-relevant repository-level decision support, judged useful by an independent usefulness evaluator, on genuinely ambiguous external repositories under fresh-agent use, with acceptable repeatability and without manual artifact repair?**

A1 has **no comparator**. It asks whether the product works usefully on its own, where usefulness is judged by an **independent usefulness evaluator** (not demonstrated usefulness to an actual human decision owner — see §30.2 claim ceilings).

### A2 — Incremental value (DEFERRED, unauthorized — Decision E)

> **Does using Sensemaking produce materially better repository-level decisions than comparable fresh-agent work without the Sensemaking layer?**

A2 has a **comparator**. It is not designed or executed until the owner reviews A1.

```text
A1: Does Sensemaking work usefully (no comparator)?
        ↓ only after owner review of A1
A2: Does Sensemaking improve the decision (vs baseline)?
```

---

## 3. What Goal A tests — product boundary (ADR 0014)

Goal A tests the ratified product boundary: does the **evidence-grounded `repository_sensemaking_brief`** — the brief/diagnosis core — produce decision support that an independent usefulness evaluator judges useful in fresh external use?

It is **not** testing:

- general autonomous software development;
- implementation quality;
- workflow execution;
- **externally validated routing / control / next-workflow selection** (deferred by ADR 0014);
- cost economics / model efficiency;
- E3 R0/R1/R2 regimes;
- causal mechanisms;
- production-scale concurrency.

### 3.1 Boundary guard

- `Next-Skill Readiness` is a **diagnostic rubric dimension only**. Scoring it does **not** constitute evidence that downstream routing or automatic control is externally validated.
- The decision-usefulness evaluation is scoped to the **diagnostic claims and the warranted next action implied by the brief's diagnosis** — not to whether automatic routing/control/stopping behavior is correct. Those remain outside the ratified boundary until separately proven and ratified.

---

## 4. Unit of evidence: the Goal A episode

One **episode** = one fresh agent, one pinned external repository state, one frozen genuinely ambiguous user task, one Sensemaking run, one unmodified resulting brief, followed by independent audit and independent usefulness evaluation.

```text
Episode
=
target repository @ pinned SHA
+ frozen user task
+ Sensemaking @ pinned SHA
+ fresh agent session
+ produced brief
+ validation result
+ evidence audit
+ semantic-quality (rubric) review
+ independent usefulness evaluation
```

Each episode stands on its own. An earlier episode is never retroactively reinterpreted because a later one produced a better answer.

---

## 5. Episode procedure

```text
PRE-EPISODE
↓
eligibility check (repository §6, task §8)
↓
pin target + framework + task (§9)
↓
fresh session (§10)

EXECUTION
↓
agent inspects repository
↓
Sensemaking produces brief
↓
artifact freezes (§14)

POST-EPISODE
↓
mechanical validation (§16)
↓
substantive evidence audit (§17)
↓
usage-research rubric (§18)
↓
independent usefulness evaluation (E1–E7) (§19–21)
↓
episode admissibility disposition (§22)
```

No step after artifact freeze can change the tested output.

---

## 6. Repository eligibility

A target repository is eligible only if all of the following hold.

### 6.1 Actually external

The target must not be `sensemaking-skills` itself. It may be another repository owned by the same person; "external" means external to the product-under-test repository.

### 6.2 Real repository state

Use an actual repository revision, not a synthetic fixture. Record:

```text
repository
target SHA
default branch
date selected
```

### 6.3 Large enough to require sensemaking

Exclude toy repositories where the relevant answer is determined by reading one obvious file. The repository must contain enough architecture, history, documentation, code, tests, issues, or implicit contracts that repository-level diagnosis is meaningful.

### 6.4 Evaluability

Someone must be capable of reviewing the resulting conclusion. This does **not** require an omniscient hidden oracle — only enough repository evidence and/or owner/maintainer knowledge to judge whether the recommendation was sensible.

---

## 7. "Structurally different" repositories

Two repositories are structurally different when they materially differ on **at least two** of these axes:

- language/runtime ecosystem;
- repository organization;
- application type;
- architectural style;
- project maturity;
- testing/CI sophistication;
- repository size;
- release/deployment model;
- contributor/project governance style.

Two similar Python utility libraries do **not** count merely because they have different names.

---

## 8. Task eligibility: "genuinely ambiguous"

A Goal A task is eligible when all of the following hold.

### 8.1 Real consequential decision

The answer could change what work gets done next. Example: *"Make release qualification more deterministic, but first determine whether that is actually the consequential remaining boundary and what the smallest warranted change is."* By contrast, *"Change `timeout=30` to `timeout=60` in `runner.py`"* is implementation work with no repository-level uncertainty and is not eligible.

### 8.2 At least two plausible next responsibilities before investigation

Examples: implementation defect; architecture problem; documentation/contract drift; missing product decision; validation/evidence gap; no change warranted. The correct one(s) need not be known beforehand — the task must genuinely permit alternatives.

### 8.3 The prompt must not leak the preferred answer

Bad: *"Diagnose why the workflow runtime architecture needs refactoring and plan the refactor."* Better: *"Establish from current repository evidence what the consequential boundary is and what work, if any, is warranted next."*

### 8.4 Answerable from available evidence

Do not ask the agent to determine things knowable only from unavailable user interviews, production telemetry, or private organizational context, unless those materials are part of the episode inputs.

---

## 9. Task freeze and evidence-lane boundary

### 9.1 Freeze before dispatch

Preserve the exact user task before the fresh agent starts. No post-hoc prompt improvement after seeing output. Record:

```text
task_id
task_text
target SHA
Sensemaking SHA
date frozen
```

If the task formulation later proves defective, classify the episode appropriately; do not silently rewrite the task and pretend the original episode never occurred.

### 9.2 Evidence type and lane boundary

- Goal A episodes are **constructed external product-validation episodes** — deliberately selected targets, frozen tasks, repeated runs — **not** Issue #218 "normal-use" observations.
- **Issue #218 remains unchanged** and continues collecting naturally-occurring engineering decisions.
- Goal A does **not** use the `EXP-NNNN` namespace (ADR 0023 Lane A) unless a later governance decision explicitly requires it.
- Goal A does **not** touch E3.
- A1 evidence informs product decisions; it is **not** silently promoted to canonical readiness evidence (respecting ADR 0023 §13 — any canonical claim needs its own new run).

---

## 10. Fresh-agent semantics

Goal A does not need E3-style hidden-oracle isolation; there is no hidden intended solution. Freshness is about avoiding **episode contamination**.

### Required

- new conversation/session;
- no previous Goal A episode output in its conversational context;
- no prior target-specific diagnosis supplied;
- no evaluator judgment supplied;
- no earlier run's recommendation supplied;
- target repository begins from the pinned state;
- exact Sensemaking revision recorded.

### Allowed

- ordinary coding knowledge;
- the agent's own model training;
- the Sensemaking Skills instructions;
- **target-repository content available to the agent, whether public or authorized private content**;
- the user's frozen task;
- normal environment information.

### Preferable (when technically possible)

- fresh standalone target clone;
- no previous episode artifacts in that clone;
- separate output directory.

### Agent/runtime neutrality

Record the runtime/model when knowable (agent runtime, provider, model, version/config), but Goal A is agent-agnostic. The product claim is "Sensemaking can be useful through compatible coding-agent environments," not "Sensemaking works because [specific agent] does." Lack of exact token/cost telemetry does not invalidate Goal A — that belongs to Goal B/E3.

---

## 11. Standard episode input

The tested agent receives only what ordinary product use would reasonably provide.

### Minimum

1. frozen user task;
2. target repository;
3. pinned Sensemaking instructions/revision;
4. permission to inspect the repository;
5. instruction to produce the canonical `repository_sensemaking_brief`;
6. standard validation mechanism.

### Do not provide

- an evaluator's expected answer;
- previous Goal A conclusions;
- a preselected weakest boundary;
- manually curated "important files" (unless a normal user would actually provide them);
- a hidden research hint designed to make the run succeed.

---

## 12. Human clarification (Decision C — approved)

Normal products interact with users; Goal A does not forbid useful clarification. Clarification must be distinguished from repair:

```text
TASK CLARIFICATION   → legitimate product interaction; record question and answer verbatim
ARTIFACT REPAIR      → manually fixing the agent's output after production; forbidden (§14)
```

### Before paired evidence runs

Freeze the best current task packet:

```text
original user goal
+ any owner-supplied constraints known beforehand
+ any clarifications already known to be necessary
```

### During a run

If a fresh agent asks a genuine clarification, its effect determines the run's status:

```text
material task clarification (changes task semantics)
→ the run becomes a task-specification / pilot observation,
  NOT a member of the repeatability pair
→ freeze the clarified task
→ restart the evidence pair fresh from the clarified packet

minor factual/environmental clarification (does not change task semantics)
→ log it verbatim
→ the episode remains a valid evidence-bearing run
```

This gives repeatability a clean meaning: a repeat pair is defined only over an identical frozen task semantics.

---

## 13. Target mutation invariant

For the A1 phase: **repository diagnosis must not mutate the target repository.**

The tested agent may: read; search; run safe probes; inspect git history; run tests or validators when warranted.

It must not: edit source files; commit; open PRs; fix the diagnosed problem.

Reason: Goal A validates diagnosis and decision support. Implementation would contaminate the question by turning one episode into diagnosis + repair.

If a violation occurs, the episode record must preserve the violation faithfully (§31 records `target_mutated` as observed, not assumed). A tested-agent target mutation is **negative product evidence** — it is recorded and may drive `A1_MIXED`/`A1_NEGATIVE`; it does **not** by itself make the episode inadmissible (§22), but it does disqualify the run from supporting `A1_POSITIVE` (§27).

---

## 14. No manual artifact repair

Once the tested agent declares its brief complete, **the artifact freezes**. Then: validate it, audit it, score it, review it — in that order, unmodified. If it contains a defect, that defect is evidence. A human may annotate ("This citation is wrong") but may not silently repair the citation and then score the repaired version.

**All Goal A evaluation (validation, audit, rubric, independent usefulness evaluation) must use the original frozen artifact.** A later repaired copy is irrelevant to Goal A **only if** the original is preserved and remains the sole evaluated artifact. If the original is lost, or evaluation uses the repaired artifact, the episode cannot support Goal A.

If a violation occurs, the episode record must preserve that fact faithfully (§31 records `manual_artifact_repair` as observed, not assumed), and the episode's admissibility/evaluability is assessed accordingly (§27).

---

## 15. Four evaluation axes — kept explicitly separate

Every episode produces verdicts on **four independent axes**. A verdict on one axis never substitutes for, or is inferred from, another. Each axis asks one distinct question; no axis encodes another axis's outcome.

### Axis 1 — Episode admissibility: did we validly test the product?

```text
EVIDENTIARY_VALID | PROTOCOL_DEFECT | HARNESS_ENVIRONMENT_FAILURE | TARGET_TASK_INVALID
```

### Axis 2 — Grounding: were its claims grounded?

```text
GROUNDING = STRONG | MIXED | WEAK | INVALID
```

### Axis 3 — Semantic/handoff quality: was the artifact semantically good?

```text
0–21  (0–7 Critical Failure | 8–14 Partial Success | 15–21 Success)
```

### Axis 4 — Evaluator usefulness: was it actually useful?

```text
USEFUL | PARTIALLY_USEFUL | NOT_USEFUL | MISLEADING | INCONCLUSIVE
```

This axis is judged by the **independent usefulness evaluator** (E1–E7, §19), not by demonstrated usefulness to an actual human decision owner.

**Placement rule:** `MISLEADING` belongs to the **evaluator-usefulness** axis only. It is **not** an episode classification and does not appear in Axis 1.

**Product positivity/negativity is derived, never encoded in Axis 1** (see §22.3). Axis 1 records only whether the episode validly instantiated the test.

---

## 16. Evaluation layer 1 — Mechanical validity

Run the normal current validators. Record `VALID` / `INVALID` and the exact failures.

```text
VALID   ≠ useful
INVALID ≠ necessarily semantically worthless
```

If an otherwise excellent brief fails a brittle mechanical rule, that is itself useful product evidence. Do not flatten semantic and structural quality.

A mechanically `INVALID` episode that is nevertheless `EVIDENTIARY_VALID` (Axis 1) **remains Goal A evidence** — it may drive `A1_MIXED` or `A1_NEGATIVE`, but it cannot support `A1_POSITIVE` (§27).

---

## 17. Evaluation layer 2 — Evidence audit

Stronger than validation. **Must run in a fresh, independent review context that did not produce the brief** (Decision B), empowered to reject claims.

### 17.1 Decision-bearing claims to audit

- object/area identified as consequential;
- weakest boundary;
- failure mechanism;
- significant absence/negative claims;
- critical unknowns;
- recommendation / next responsibility;
- claims that materially influence stopping.

### 17.2 Per-claim classification

```text
SUPPORTED | PARTIALLY_SUPPORTED | UNSUPPORTED | CONTRADICTED | NOT_AUDITABLE
```

### 17.3 Audit questions

- **File/path reality** — does cited evidence actually exist?
- **Citation reality** — does the cited range or quoted content actually support what the brief says exists there?
- **Semantic support** — does the evidence genuinely support the claim?
- **Contradiction search** — is there stronger repository evidence contradicting the claim?
- **Claim strength** — does the conclusion overreach the evidence?

### 17.4 Grounding verdict

```text
GROUNDING = STRONG | MIXED | WEAK | INVALID
```

No numeric weighting required.

---

## 18. Evaluation layer 3 — Existing usage-research rubric

Use `docs/usage-research-rubric.md` as the semantic/handoff-quality instrument. It scores seven dimensions from 0–3 (Object Under Pressure; Failure Mode; What Must Be True; Critical Unknowns; Research Paths; Stopping Rule; Next-Skill Readiness), banded 0–7 Critical Failure, 8–14 Partial Success, 15–21 Success.

- Do **not** redesign the rubric for Goal A.
- **Diagnostic only (Decision D):** the rubric never gates campaign success. **21/21 does not prove evaluator usefulness; 13/21 does not disprove it.** A grounded brief can still be judged not useful, and a high rubric score does not automatically imply `USEFUL` (see §23).
- `Next-Skill Readiness` measures handoff quality only and does **not** evidence externally validated routing (§3.1).

---

## 19. Evaluation layer 4 — Independent usefulness evaluation (E1–E7)

The **independent usefulness evaluator** answers these questions **independently of the 0–21 score and of the evidence audit**. The evaluator must be distinct from the producer (fresh/different review context). It should also be made distinct from the evidence auditor when operationally practical, but a second mandatory human role is **not** introduced for A1.

The evaluator determines whether the grounded result constitutes **useful repository-level decision support** — not whether it demonstrated usefulness to an actual human decision owner, and not whether it changed any real human decision (§21, §30). The evaluator is not described as a human surrogate.

### E1 — Substantive correctness

> Is the brief substantively correct enough to support a repository-level decision?

```text
YES | PARTIALLY | NO | INSUFFICIENT_KNOWLEDGE
```

### E2 — Boundary usefulness

> Does the identified consequential boundary materially clarify what matters next in the repository?

```text
YES | WITH_RESERVATIONS | NO
```

### E3 — Recommendation appropriateness

> Given the grounded evidence, is the recommended next responsibility appropriate?

```text
APPROPRIATE | PLAUSIBLE_BUT_NOT_BEST | INAPPROPRIATE | NO_ACTION_CORRECT
```

### E4 — Decision effect

> For a reasonable fresh decision-maker facing the frozen task, what material effect would this brief be expected to have on the decision?

```text
WOULD_CHANGE_DECISION | WOULD_CONFIRM_DECISION_WITH_NEW_EVIDENCE |
WOULD_INCREASE_CONFIDENCE_ONLY | NO_MATERIAL_DECISION_EFFECT |
WOULD_MAKE_DECISION_WORSE
```

This wording is deliberately **counterfactual**. The evaluator must not claim an actual human decision changed.

### E5 — Novel useful information

> Does the brief surface materially useful information beyond what the evaluator would consider obvious from the task framing alone?

```text
YES | PARTIALLY | NO
```

### E6 — Interpretive / repair burden

> How much evaluator intervention is required before the brief becomes decision-usable?

```text
NONE | CLARIFICATION_ONLY | SUBSTANTIVE_INTERPRETATION | MAJOR_REWORK
```

(The rework is never actually performed — this is the evaluator estimating what would have been required.) Normal independent evidence auditing does not itself count as repair burden.

### E7 — Reuse assessment

> Based on this episode, would use of the Sensemaking process be warranted again for a comparable ambiguous repository-level decision?

```text
YES | MAYBE | NO
```

This is an **evaluator judgment**, not evidence of actual human reuse intent.

---

## 20. Review roles (Decision B, amended — approved)

```text
producer agent                          → produces brief
        ↓
independent evidence auditor            → grounding assessment (Axis 2)
        ↓
independent usefulness evaluator        → evaluator usefulness (Axis 4)
```

- **Evidence audit:** mandatory independent context (fresh session / different reviewer), empowered to mark claims `UNSUPPORTED`/`CONTRADICTED` and to reject.
- **Usefulness evaluation:** independently judges whether the grounded result constitutes useful repository-level decision support (E1–E7). The evaluator is distinct from the producer; it should be distinct from the evidence auditor when operationally practical, but no second mandatory human role is added for A1.
- **Actual human decision owner:** optional / deferred, **not required for A1**. A human decision-owner review may later be used to support stronger human-centered claims (§30.2 claim ceilings).

The three responsibilities remain conceptually separate:

```text
producer            → creates the brief
evidence auditor    → determines whether decision-bearing claims are grounded
usefulness evaluator → determines whether the grounded result constitutes
                       useful repository-level decision support
```

---

## 21. Evaluator-usefulness verdict definitions

The overall Axis 4 verdict is the **canonical `evaluator_usefulness`** result:

```text
USEFUL
  The brief is grounded enough to trust, identifies a consequential boundary, and
  would materially change or substantively confirm the next decision without
  major evaluator reconstruction.

PARTIALLY_USEFUL
  Contains genuine decision value but requires reservations, clarification, or
  significant interpretation.

NOT_USEFUL
  Provides no meaningful decision advantage, chooses an inappropriate
  boundary/responsibility, or requires major reconstruction.

MISLEADING
  The artifact appears actionable but its major decision-bearing claims are
  unsupported/contradicted or would lead the decision-maker toward worse work.
  (Worse than merely unhelpful; this is an EVALUATOR-USEFULNESS verdict, not an
  episode classification.)

INCONCLUSIVE
  The evaluator cannot judge usefulness because the repository/task/protocol/
  environment prevented a meaningful evaluation.
```

The protocol requires an explicit E1–E7 judgment by the evaluator. The canonical axis cleanly separates three distinct things:

```text
grounding              (Axis 2)   ≠
diagnostic rubric score (Axis 3) ≠
evaluator usefulness    (Axis 4)
```

A grounded brief can still be judged not useful. A high rubric score does not automatically imply `USEFUL`. `INCONCLUSIVE` here is an Axis 4 verdict, not an episode admissibility class.

---

## 22. Episode admissibility (Axis 1)

A pure evidentiary-admissibility axis: did the episode validly instantiate the intended product-validation test? It encodes **no** product/usefulness outcome — that is derived from Axes 2–4.

### 22.1 Admissibility classes

```text
EVIDENTIARY_VALID
  The episode validly instantiated the intended product-validation test, and
  therefore its outcome — positive or negative — counts as Goal A evidence.

PROTOCOL_DEFECT
  The episode could not meaningfully test the product because the protocol
  itself was ambiguous or defective. Does NOT count as product evidence.
  Fix the protocol before further dispatch.

HARNESS_ENVIRONMENT_FAILURE
  The agent/runtime/repository environment prevented normal execution.
  Does NOT count as product evidence.

TARGET_TASK_INVALID
  After investigation, the supposedly ambiguous task was actually trivial,
  unknowable, pre-decided, or otherwise ineligible. Does NOT count as
  product evidence.
```

This prevents both "experiment broke → product failed" and "product failed → call it an environment issue."

### 22.2 What admissibility does NOT contain

Axis 1 contains no `PRODUCT_NEGATIVE` and no `VALID_POSITIVE` classes. Whether the product did well or poorly is **never** an admissibility question.

### 22.3 Derived product evidence

Product negativity is derived from the other axes, for example:

```text
EVIDENTIARY_VALID
+ NOT_USEFUL or MISLEADING
and/or serious grounding or structural failure
→ negative product evidence
```

Conversely, an episode is not "positive evidence" merely because it was admissible; it must also carry the required Axis 2–4 verdicts (§27).

---

## 23. Semantic score and usefulness remain separate

Both patterns are valid and important:

```text
Usage rubric: 19/21 SUCCESS     →  Sensemaking produces polished handoff-ready
Evaluator verdict: NOT_USEFUL      artifacts that do not actually improve decisions.

Usage rubric: 13/21 PARTIAL     →  Some formal handoff properties are weaker
Evaluator verdict: USEFUL           than desired, but the underlying product
                                   value may already exist.
```

That distinction is exactly what Goal A needs — which is why the rubric is diagnostic, never a gate (§18).

---

## 24. Repeatability

Repeatability means **decision-level stability**, not identical prose.

A repeat episode uses: same repository SHA, same frozen user task, same Sensemaking SHA, fresh independent agent session, and **the same model/runtime configuration when technically controllable**; if configuration identity cannot be held constant, preserve that fact as a limitation on the repeatability claim.

Classify the pair:

```text
CONSISTENT
  Same consequential boundary and substantively same warranted next responsibility.

COMPATIBLE_VARIANCE
  Different wording or secondary findings, but both converge on compatible
  interpretations/actions.

MATERIAL_DIVERGENCE
  Different consequential boundaries or materially different responsibilities.

INCONCLUSIVE
  At least one episode was invalid due to protocol/environment failure.
```

Do **not** automatically treat `MATERIAL_DIVERGENCE` as product failure. Investigate whether: one result is clearly stronger; both are defensible; the task itself is underspecified; or the repository genuinely supports multiple legitimate next actions.

---

## 25. Campaign design (Decision A — approved)

### 2 structurally different repositories × 2 fresh runs each = 4 initial episodes

Documented rationale (what each cell prevents):

```text
second run
→ protects against one lucky model/run

second repository
→ protects against one-repository / one-architecture success

2 × 2
→ smallest campaign testing both repeatability and cross-shape usefulness
```

This does **not** create a statistical generalization claim — it is a bounded decision signal. Both repositories must be eligible (§6) and structurally different (§7).

---

## 26. No automatic repair-and-rerun

If an `EVIDENTIARY_VALID` episode yields negative product evidence: **stop and inspect the finding.** Do not automatically `patch → rerun → patch → rerun`. That would turn Goal A into a self-healing campaign where the product is adapted to the test until it passes. A negative result first answers "What did we learn about the product?"; then the owner decides whether that warrants product work.

---

## 27. A1 success logic (Decision D — approved)

The product-validation chain, in order:

```text
ADMISSIBLE?        Did we genuinely test the product?         (Axis 1)
        ↓
STRUCTURALLY VALID?  Did the ratified artifact contract work? (mechanical validation)
        ↓
SAFE / UNREPAIRED?  Did diagnosis remain read-only and the
                     artifact remain the original frozen one? (invariants)
        ↓
GROUNDED?          Can its decision-bearing claims be trusted? (Axis 2)
        ↓
USEFUL?            Did an independent evaluator judge it useful
                       repository-level decision support?     (Axis 4)
        ↓
REPEATABLE?        Did another fresh run reach a compatible decision?
```

### Per target (both fresh runs)

Both runs must satisfy **all** of the following:

```text
episode_admissibility = EVIDENTIARY_VALID
mechanical_validation = VALID
target_mutated = false
manual_artifact_repair = false
grounding = STRONG or MIXED
evaluator_usefulness != MISLEADING

repeatability = CONSISTENT or COMPATIBLE_VARIANCE

at least one run:
  evaluator_usefulness = USEFUL

other run:
  evaluator_usefulness = USEFUL or PARTIALLY_USEFUL
```

### Notes

- **Operating invariants are gated.** `target_mutated = false` and `manual_artifact_repair = false` are explicit requirements for any run supporting `A1_POSITIVE`, because the A1 claim includes "without manual artifact repair" and a read-only diagnostic contract (§2, §13, §14).
  - **Target mutation by the tested agent remains negative product evidence**, not automatic inadmissibility: it is recorded (Axis 1 stays `EVIDENTIARY_VALID` if the test was otherwise validly instantiated) and may drive `A1_MIXED`/`A1_NEGATIVE`, but it disqualifies the run from supporting `A1_POSITIVE`.
  - **Manual repair:** all audit/scoring must use the original frozen artifact. A later repaired copy is irrelevant only if the original is preserved and remains the sole evaluated artifact; otherwise the episode cannot support Goal A.
- **Mechanical validity is required for `A1_POSITIVE`.** The ratified product is a *validated* brief (ADR 0014) whose usefulness is assessed by an independent evaluator; a mechanically `INVALID` brief cannot prove the validated-brief product works, however useful its reasoning. A mechanically `INVALID` but otherwise admissible episode remains Goal A evidence and may contribute to `A1_MIXED`/`A1_NEGATIVE` — preserving `INVALID ≠ semantically worthless` (§16) without letting an invalid artifact prove the validated product.
- **Grounding must be STRONG or MIXED.** `WEAK` grounding does not validate an evidence-grounded product. `WEAK` remains valid product evidence and may contribute to `A1_MIXED` or, if recurrent/severe, `A1_NEGATIVE` — mirroring the structural rule: *weakly grounded but useful → evidence, but not positive validation*.
- The 0–21 rubric score is always reported alongside as **diagnostic evidence**; it never overrides or substitutes for this categorical logic.

### Campaign-level verdicts

```text
A1_POSITIVE
  Both structurally different targets satisfy the per-target requirements above.

A1_MIXED
  Real evaluator-judged usefulness exists, but one target/repeat exposes a
  meaningful reliability/generalization weakness (including
  mechanically-invalid-but-useful, weakly-grounded-but-useful, or
  invariant-violation evidence patterns).

A1_NEGATIVE
  Valid episodes repeatedly fail to produce useful grounded decision support,
  or produce misleading recommendations.

A1_INCONCLUSIVE
  Protocol/environment/task problems prevent the claim from being tested.
```

### 27.2 Campaign verdicts remain categorical

Campaign verdicts are categorical judgments; they do **not** introduce numeric
aggregation or statistical-significance requirements. The 0–21 rubric remains
diagnostic only (§18).

### 27.3 Transition rule for already-completed evidence

```text
Artifacts, audit records, and evaluator judgments produced before this
amendment retain their original provenance and labels.

They must not be retroactively rewritten to appear as though they were
produced under E1–E7.

A pre-amendment run may be carried forward only after a fresh E1–E7
usefulness evaluation is performed against its preserved, frozen artifact and
completed grounding audit.

That fresh evaluator judgment becomes the canonical evaluator_usefulness
result for the amended A1 campaign.
```

This rule governs any evidence produced under the prior mandatory
human-usefulness authority (e.g. the completed ViralFactory Run 1). It does
**not** require rerunning an already-admissible producer run or independent
evidence audit merely because the usefulness contract changed.

---

## 28. Stop rules

Stop A1 early when:

- **Product failure is already clear** — an admissible early episode exposes a severe systematic problem likely to make later episodes non-informative; stop and decide whether to repair.
- **Protocol invalidity is clear** — fix the protocol before consuming more evidence.
- **The owner decision is already stable** — two repositories + repeats produce strong, consistent evidence and additional same-class episodes are unlikely to change what gets built next.

Do not collect more repositories merely to look more impressive.

---

## 29. A2 — deferred and unauthorized (Decision E — approved)

**A2 is not designed or executed until the owner reviews A1.** Possible A1 outcomes lead to different next work:

```text
A1_POSITIVE   → A2 becomes interesting: does Sensemaking add value over baseline?
A1_MIXED      → investigate the observed weakness first, OR owner may authorize
                a narrowly targeted comparison
A1_NEGATIVE   → product repair/discovery before comparison
A1_INCONCLUSIVE → fix protocol/substrate first
```

For future reference only (not authorization), A2's comparative design, when engaged, would compare fresh agent + ordinary repo reasoning vs fresh agent + Sensemaking on the same target SHA/task/agent family, independent fresh sessions, outputs stripped of condition labels where practical, with a human reviewer asked "Which output would you use to decide what work happens next, and why?" compared on consequential-boundary quality, evidence grounding, uncertainty handling, stopping discipline, appropriateness of next responsibility, and downstream decision usefulness. **"Materially better"** means the Sensemaking condition changes the quality of the repository-level decision in a way the human reviewer considers consequential — not merely stylistically better. No E3 oracle, no 3-regime matrix, no dollar-cost telemetry, no publication-grade causal claim.

---

## 30. What A1 can and cannot justify

### 30.1 Positive A1 claim

A positive A1 can support:

> Sensemaking's ratified repository-sensemaking core has demonstrated grounded external repository decision support across two structurally different targets under fresh-agent use, with acceptable repeatability, mechanically valid artifacts, no target mutation, no manual artifact repair, and independent evaluator judgments of usefulness.

This claim is scoped to the evidence class produced by the amended A1 protocol. It does **not** imply demonstrated usefulness to an actual human decision owner.

### 30.2 Claim ceilings

A1 under this protocol establishes **no** claim on human-centered outcomes. The following are canonically `NOT_TESTED`:

```text
HUMAN_DECISION_OWNER_USEFULNESS  = NOT_TESTED
HUMAN_DECISION_IMPACT            = NOT_TESTED
HUMAN_REUSE_INTENT               = NOT_TESTED
ACTUAL_HUMAN_DECISION_CHANGE     = NOT_TESTED
```

Concretely, A1 under this protocol does **not** establish:

- demonstrated usefulness to actual human decision owners;
- actual human decision change;
- actual human reuse intent;
- comparative superiority versus unsensemade human/agent work.

The last item remains relevant to deferred A2 (§29). A later, separately
authorized human study may raise these claim ceilings.

A positive A1 does **not** justify:

- "Sensemaking makes agents better than baseline" — that is A2;
- "Sensemaking reduces operational cost" — Goal B/E3;
- "routing/control/next-workflow selection is externally validated" — outside ADR 0014; `Next-Skill Readiness` is diagnostic only;
- an automatic "Externally Validated" readiness-label change — any formal readiness claim is a separate review against then-current authority (§1);
- demonstrated usefulness to an actual human decision owner, actual human decision change, or actual human reuse intent (§30.2).

---

## 31. Per-episode evidence record

Each episode produces a compact record. Observational fields are recorded **as observed**, not assumed: if a violation of an invariant (§13, §14) occurred, the record preserves the violation truthfully.

```text
episode_id
target_repository / target_sha
sensemaking_sha
task_text / task_frozen_at
agent_runtime / model_if_known / fresh_session_confirmed
target_mutated = true | false          (observed; invariant requires false)
manual_artifact_repair = true | false  (observed; invariant requires false)
artifact_path
mechanical_validation = VALID | INVALID (+ exact failures)

AXIS 1 — episode_admissibility:
  EVIDENTIARY_VALID | PROTOCOL_DEFECT | HARNESS_ENVIRONMENT_FAILURE | TARGET_TASK_INVALID

AXIS 2 — evidence_audit:
  grounding = STRONG | MIXED | WEAK | INVALID
  high_risk_claims[...]

AXIS 3 — usage_rubric:
  object_under_pressure / failure_mode / what_must_be_true /
  critical_unknowns / research_paths / stopping_rule /
  next_skill_readiness / total

AXIS 4 — evaluator_usefulness:
  substantive_correctness (E1) / boundary_usefulness (E2) /
  recommendation_appropriateness (E3) / decision_effect (E4) /
  novel_useful_information (E5) / interpretive_repair_burden (E6) /
  reuse_assessment (E7) / overall_verdict

repeatability_relation (if applicable)
clarifications logged (if any, verbatim)
configuration_identity_limitation (if model/runtime could not be held constant)
```

This reconstructs what happened without building a new experimental framework.

---

## 32. What is not instrumented

Avoid: token accounting; provider billing; detailed cost telemetry; randomized dispatch; automated blinded evaluators; multiple regimes; elaborate agent adapters; a generalized experiment runner; statistical significance machinery; automatic scoring aggregation. Those belong only if a later decision-changing uncertainty requires them.

---

## 33. Relationship to E3

```text
Goal A — ACTIVE
constructed external product validation

Goal B / E3 — FROZEN / DEFERRED
research-grade comparative/economic experiment
```

Goal A: does not modify E3; does not use E3 cells; does not advance the E3 product-under-test SHA; does not require E3 telemetry; does not claim E3 results; does not unblock the E3 pilot. E3 remains a historical research object until explicitly resumed, retired, or superseded.

Issue #218 remains the actual normal-use evidence lane (§9.2); Goal A episodes are constructed, not normal-use.

---

## 34. Owner decisions carried in this version

| # | Decision | Approved content |
|---|---|---|
| **0** | Governance | Goal A is the current successor product-validation strategy; D8 = inherited evidence guidance; E4/Issue #83 = historical, closed, grants no authorization; ADR 0021 superseded; Issue #218 unchanged |
| **A** | Campaign size | 2 structurally different repositories × 2 fresh evidence-bearing runs = 4 episodes; justified as lucky-run + single-repo protection |
| **B** | Reviewers (amended 2026-08-26) | Mandatory independent evidence-audit context; independent usefulness evaluator required (distinct from producer; preferably distinct from evidence auditor when operationally practical, but no second mandatory human role); actual human decision owner optional/deferred — **not** required for A1 |
| **C** | Clarification | Freeze common task semantics before paired runs; material clarification ⇒ pilot observation + restart pair fresh; minor clarification ⇒ log + valid |
| **D** | A1 success | Categorical judgment; 0–21 rubric diagnostic only, never a hard gate |
| **E** | A2 | Deferred, unauthorized until owner reviews A1 |
| **F** | Usefulness authority (2026-08-26) | Replace mandatory human-usefulness authority with independent evaluator usefulness (E1–E7) plus explicit human claim ceilings (§30.2); prospective from canonicalization; historical evidence unchanged (§27.3) |

### 34.1 Amendment record — independent evaluator usefulness (2026-08-26)

This subsection is the governance record of the protocol amendment that
substitutes the independent-evaluator usefulness authority for the mandatory
human-usefulness authority.

```text
amendment_id        = goal-a-protocol-2026-08-26-usefulness-authority
owner decision      = APPROVED
reason              = reduce recurring human-review bottleneck while preserving
                      grounding, decision relevance, repeatability, and strict
                      claim bounds
trade-off           = A1 no longer demonstrates actual human usefulness or
                      actual human decision impact (§30.2 claim ceilings)
effective boundary  = prospective from canonicalization; historical artifacts,
                      audit records, and evaluator judgments remain unchanged
                      and retain their original provenance and labels (§27.3)
old usefulness authority = mandatory actual-human decision-owner review (H1–H7)
new usefulness authority = independent usefulness evaluator (E1–E7)
human review requirement = OPTIONAL / DEFERRED, NOT REQUIRED FOR A1
canonical axis       = evaluator_usefulness
```

---

## 35. Status

**APPROVED — canonical** (v1.0 FINAL, amended 2026-08-26 by owner decision F).

- No repository mutation authorized by this protocol; none is implied by approval.
- No Goal A episode authorized or executed by this protocol. Approving this protocol does **not** by itself authorize episodes; execution requires a separate, explicit owner authorization.
- This amendment is **prospective from canonicalization**. Completed Goal A evidence, audit records, and evaluator judgments retain their original provenance and labels; they are not rewritten or relabeled to appear as though produced under E1–E7 (§27.3). The previous `USEFUL` auditor opinion under the prior audit prompt is historical/noncanonical for the amended usefulness axis.
- Next responsibility after protocol canonicalization: for any carried-forward run (e.g. **ViralFactory Run 1**), a **fresh E1–E7 independent usefulness evaluation** against the preserved, frozen artifact and completed grounding audit — in a separately authorized responsibility. Run 2 authorization is considered only after that evaluation.

---

## Status disposition

```
PROTOCOL_STATUS                = APPROVED, amended 2026-08-26  (Goal A — External Product Validation Protocol v1.0 FINAL)
Goal A                         = ACTIVE
A1                             = ACTIVE  (absolute product utility; independent evaluator usefulness)
A2                             = DEFERRED / UNAUTHORIZED
Goal B / E3                    = FROZEN / DEFERRED
canonical usefulness axis      = evaluator_usefulness (E1–E7)
human decision-owner review    = OPTIONAL / DEFERRED, NOT REQUIRED FOR A1
claim ceilings                 = HUMAN_DECISION_OWNER_USEFULNESS / HUMAN_DECISION_IMPACT / HUMAN_REUSE_INTENT / ACTUAL_HUMAN_DECISION_CHANGE = NOT_TESTED
Goal A episodes authorized     = NO
repository mutation authorized = NO
Goal A episodes executed       = 0
```
