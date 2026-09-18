# Practical Agent Architecture v0 Reconciliation and Guidance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconcile the approved Practical Agent Architecture v0 against current Sensemaking, then implement only the smallest warranted agent-facing guidance changes while explicitly declining unnecessary runtime, schema, persistence, and orchestration machinery.

**Architecture:** Treat the approved warrant-centered hybrid design as an ownership model, not a new runtime. First classify what current Sensemaking already satisfies. Then add only missing reasoning guidance for explicit warrant targets/dependencies, challenge/exploration triggers, resource-aware stopping, and evidence return from delegated/orchestrated work. Reuse Campaign, Semantic Architecture, authority, validation, and orchestration boundaries unchanged unless reconciliation proves a concrete gap.

**Tech Stack:** Markdown Agent Skills, existing Sensemaking documentation/contracts, repository validation scripts, GitHub CI.

**Spec:** `docs/superpowers/specs/2026-09-17-practical-agent-architecture-v0-design.md`

## Global Constraints

- ADR 0029 remains the current product-boundary authority.
- The five Practical Agent Architecture zones are ownership boundaries, not required services, classes, databases, or runtime engines.
- Warrant remains target-specific and defeasible; it is not a numeric score, ranking, permission token, authorization, or deterministic decision function.
- Persist explicit decision state when continuation warrants it; do not persist hidden chain-of-thought.
- Deterministic machinery may validate mechanically decidable facts but may not select semantic responsibility.
- Decision selects the work; orchestration coordinates selected work; evidence returns upward for semantic reassessment.
- Existing Campaign, Semantic Architecture, Level-3, Level-4, authority, and qualification surfaces must be reused before any new representation is proposed.
- No generic agent runtime, `OuterLoopEngine`, `StrategicPlanner`, universal state database, automatic Skill selection, automatic Campaign creation, automatic critic voting, or numeric warrant scoring.
- No schema/API/code change is authorized unless Task 1 identifies a concrete gap that cannot be satisfied by current structures or guidance.
- Current expected package is documentation/Skill guidance only; if Task 1 contradicts that expectation, stop before implementation and return to architectural review.

---

## File Structure

### Create: `docs/research/practical-agent-architecture-reconciliation-v0.md`

Responsibility: record current-state evidence against the five ownership zones, classify each design requirement as already satisfied, guidance gap, durable-state gap, deterministic-assurance gap, outside-product concern, or unresolved, and identify the smallest warranted package.

### Create: `skills/using-sensemaking/references/practical-agent-architecture-v0.md`

Responsibility: provide detailed agent-facing operational guidance for warrant targets/dependencies, challenge/exploration triggers, resource-aware stopping, delegation evidence return, and architecture boundaries without creating new runtime semantics.

### Modify: `skills/using-sensemaking/SKILL.md`

Responsibility: integrate the minimum practical-agent guidance into the canonical bootstrap while keeping progressive disclosure; link to the detailed reference instead of duplicating the full design.

### Optional Modify only if Task 1 proves necessary: `skills/using-sensemaking/references/adaptive-guidance-v0.md`

Responsibility: add at most one bounded clarification that consequentiality/novelty/irreversibility may warrant stronger challenge and exploration. Do not add modes, scores, or routing rules.

### Update: draft PR #376 body

Responsibility: summarize reconciliation outcome, smallest warranted implementation package, validation results, and explicit non-changes.

---

### Task 1: Reconcile Practical Agent Architecture v0 Against Current Sensemaking

**Files:**
- Create: `docs/research/practical-agent-architecture-reconciliation-v0.md`
- Read/reference: `docs/superpowers/specs/2026-09-17-practical-agent-architecture-v0-design.md`
- Read/reference: `skills/using-sensemaking/SKILL.md`
- Read/reference: `skills/using-sensemaking/references/adaptive-guidance-v0.md`
- Read/reference: `docs/semantic-architecture/reasoning-model.md`
- Read/reference: `docs/sensemaking-campaign.md`
- Read/reference: `docs/strategic-state-contract.md`
- Read/reference: `docs/product-thesis-revision.md`
- Read/reference: `docs/research/warrant-as-control-primitive.md`
- Read/reference: `docs/research/uncertainty-selection.md`
- Read/reference: `docs/research/decision-versus-orchestration.md`
- Read/reference: `docs/adr/0029-current-product-boundary.md`

**Interfaces:**
- Consumes: approved ownership model and current repository authority/contracts.
- Produces: explicit dispositions used to authorize or decline Tasks 2–3.

Use these exact reconciliation dispositions:

```text
ALREADY_SATISFIED
GUIDANCE_GAP
DURABLE_STATE_GAP
DETERMINISTIC_ASSURANCE_GAP
OUTSIDE_PRODUCT
UNRESOLVED
```

- [ ] **Step 1: Create the reconciliation header and evidence ceiling**

Start the artifact with:

```markdown
# Practical Agent Architecture v0 — Sensemaking Reconciliation

**Status:** bounded repository reconciliation / non-authoritative
**Date:** 2026-09-17
**Authority:** research/reconciliation only; does not modify ADR 0029, runtime authority, schema, public API, Campaign semantics, or product strategy

## Research question

> Which parts of Practical Agent Architecture v0 are already satisfied by current Sensemaking, which require only agent-facing guidance, and which—if any—expose a genuine representation or deterministic-assurance gap?
```

State that absence of a first-class runtime component is **not** itself a gap.

- [ ] **Step 2: Build a five-zone coverage table**

For every zone, record repository evidence and disposition.

Use this structure:

```markdown
| Zone | Current Sensemaking surfaces | Disposition | Evidence-based conclusion |
| --- | --- | --- | --- |
| Semantic Agency Plane | using-sensemaking Skill; Semantic Reasoning Model; Level 3/4 guidance | ... | ... |
| Warrant / Decision Control | using-sensemaking recursive loop; warrant research; uncertainty-selection research | ... | ... |
| Durable Decision Substrate | Campaign; STATUS; strategic state; ADRs; evidence/provenance/handoff | ... | ... |
| Deterministic Assurance | validators; target identity/currentness; artifact admission; reference integrity; CI | ... | ... |
| Execution / Orchestration | Skills/tools/workflows + decision-versus-orchestration boundary | ... | ... |
| Authority / Governance | Authority semantics; owner-reserved Level 4/protected transitions | ... | ... |
```

Expected evidence-backed direction:

- Semantic Agency Plane: `GUIDANCE_GAP` only for some new practical vocabulary/operators.
- Warrant / Decision Control: `GUIDANCE_GAP`, because “update warrant” exists but explicit target/dependency formulation is not yet canonical bootstrap guidance.
- Durable Decision Substrate: `ALREADY_SATISFIED` for current repository-domain needs; no generic state/schema gap established.
- Deterministic Assurance: `ALREADY_SATISFIED` at the architecture level; future additions remain pressure-driven.
- Execution / Orchestration: `ALREADY_SATISFIED` as a boundary; agent-facing failure/evidence return can be clarified in guidance.
- Authority / Governance: `ALREADY_SATISFIED`.

If repository evidence contradicts any expected direction, record the contradiction and stop before Tasks 2–3 if it would require code/schema/runtime changes.

- [ ] **Step 3: Reconcile each candidate implementation surface**

Create sections for:

```text
warrant target/dependencies
challenge triggers
exploration triggers
resource-aware stopping
delegation/subagent evidence return
durable decision state
deterministic assurance
orchestration interface
authority
```

For each, record:

```markdown
Current support:
Observed gap:
Decision effect:
Disposition:
Smallest warranted intervention:
Rejected heavier intervention:
```

Expected smallest intervention for the first five items is agent-facing guidance. Expected intervention for durable state/deterministic assurance is no change unless concrete evidence proves otherwise.

- [ ] **Step 4: Re-run the eight design scenarios as implementation pressure tests**

For scenarios A–H from the spec, ask:

1. Does current Sensemaking already support the required behavior?
2. Would the proposed guidance change materially improve agent behavior?
3. Is new persistent state required?
4. Is new deterministic machinery required?
5. Does any behavior belong outside Sensemaking?

Record one bounded result per scenario.

- [ ] **Step 5: Select one implementation disposition**

Choose exactly one:

```text
GUIDANCE_ONLY_WARRANTED
BOUNDED_STATE_CHANGE_WARRANTED
BOUNDED_ASSURANCE_CHANGE_WARRANTED
ARCHITECTURE_REVIEW_REQUIRED
NO_CHANGE_WARRANTED
```

Expected from current evidence: `GUIDANCE_ONLY_WARRANTED`.

Do not force the expected result if repository evidence disagrees.

- [ ] **Step 6: Record the smallest package**

If `GUIDANCE_ONLY_WARRANTED`, explicitly authorize only:

1. a detailed practical-agent reference under `skills/using-sensemaking/references/`;
2. a compact integration into `skills/using-sensemaking/SKILL.md`;
3. an optional small adaptive-guidance clarification only if non-duplicative.

Explicitly decline:

- Campaign schema changes;
- new Python types;
- new validators;
- new public API;
- new planner/runtime;
- automatic critic orchestration;
- automatic option/warrant scoring;
- product-boundary change.

- [ ] **Step 7: Self-review Task 1**

Verify:

- every disposition is supported by a current repository surface;
- no missing runtime object is treated as a gap merely because the theory names a concept;
- no guidance gap is inflated into schema/code;
- ADR 0029 remains unchanged;
- no product-value/general-intelligence claim exceeds evidence.

- [ ] **Step 8: Commit Task 1**

Commit:

```text
docs: reconcile Practical Agent Architecture with Sensemaking
```

---

### Task 2: Add Detailed Agent-Facing Practical Architecture Guidance

**Precondition:** Task 1 disposition is exactly `GUIDANCE_ONLY_WARRANTED`. If not, stop and return to design review.

**Files:**
- Create: `skills/using-sensemaking/references/practical-agent-architecture-v0.md`
- Reference: `docs/research/practical-agent-architecture-reconciliation-v0.md`
- Reference: `docs/superpowers/specs/2026-09-17-practical-agent-architecture-v0-design.md`

**Interfaces:**
- Consumes: Task 1's explicit `GUIDANCE_ONLY_WARRANTED` authorization.
- Produces: detailed agent guidance that Task 3 links from the canonical Skill.

- [ ] **Step 1: Add reference status and scope**

Start with:

```markdown
# Practical Agent Architecture v0 — Agent Reference

**Status:** agent-facing guidance for using Sensemaking; not a runtime specification
**Authority:** interpretive guidance under the current product boundary; ADR 0029 and canonical authority contracts remain controlling

Use this reference when a consequential decision benefits from making warrant, challenge/exploration, delegated work, or stopping logic explicit.
```

- [ ] **Step 2: Define the compact practical loop**

Include:

```text
goal + authority + target
-> name contemplated warrant target
-> identify the few premises that must be true
-> resolve the nearest decision-changing warrant gap
-> choose inquire / act / stop / escalate / verify / close
-> check authority + mechanical preconditions
-> orchestrate selected work
-> treat returned result as evidence
-> update warrant
-> repeat only as warranted
```

State that this is reasoning guidance, not a runtime state machine.

- [ ] **Step 3: Define warrant target guidance**

Use concrete target examples:

```text
claim
inquiry
responsibility
action
continue
stop
escalate
closure
protected transition
```

Require the agent to ask:

```text
What exactly am I trying to justify now?
What must be true for that target to be warranted?
Which missing premise could materially change the next action?
```

Re-state:

```text
warrant != confidence score
warrant != authorization
warrant for target A != warrant for target B
```

- [ ] **Step 4: Define challenge versus exploration**

Add:

```text
Challenge:
Why might the current frame, claim, forecast, option, or closure decision be wrong?

Exploration:
What plausible frame, option, explanation, or intervention is not yet represented?
```

Use triggers from the spec:

- high consequence;
- low reversibility;
- conflicting evidence;
- high confidence from weak evidence;
- novelty;
- repeated failure;
- narrow option set;
- stakeholder/value conflict;
- unstable decision frame;
- protected external commitment.

State that critic outputs are evidence, not automatic veto/approval.

- [ ] **Step 5: Define resource-aware stopping**

Add the qualitative rule:

```text
continue reasoning when expected decision improvement
is worth more than reasoning + information + delay + opportunity cost
```

Then include:

```text
cheap + reversible + informative
-> acting can be better than thinking longer

consequential + irreversible + externally visible
-> stronger evidence / challenge / verification / authority may be warranted
```

Do not introduce numeric thresholds.

- [ ] **Step 6: Define delegation and evidence return**

Require delegated work to specify:

```text
responsibility
scope
authority
expected artifact/evidence
success/stop conditions
```

And state:

```text
worker recommendation != parent decision
worker success != global closure
execution failure -> evidence -> semantic reassessment
retry policy != permission to change responsibility
```

- [ ] **Step 7: Define persistence rule**

Include:

```text
persist only what a fresh context needs to reconstruct the consequential decision:
commitments, decision frame, material evidence/claims, decision-relevant uncertainty,
selected responsibility, authority, concise rationale, stop/reopen conditions,
provenance/currentness.
```

Explicitly say not to persist hidden chain-of-thought and not to create Campaign merely because the practical architecture is being used.

- [ ] **Step 8: Define progressive disclosure**

Use:

```text
trivial + local + reversible
-> keep most architecture implicit

ambiguous responsibility
-> make decision frame / warrant gap explicit

high consequence / low reversibility
-> make warrant, challenge, evidence, authority explicit

cross-context continuation
-> use durable Campaign state when warranted
```

- [ ] **Step 9: Self-review Task 2**

Verify the reference:

- contains no scores/modes/router rules;
- creates no new authority;
- does not require Campaign;
- keeps orchestration external;
- contains no schema/API claims;
- links conceptual behavior to existing Sensemaking vocabulary.

- [ ] **Step 10: Commit Task 2**

Commit:

```text
docs: add Practical Agent Architecture agent reference
```

---

### Task 3: Integrate the Practical Architecture into the Canonical Using-Sensemaking Skill

**Precondition:** Task 2 completed without requiring runtime/schema changes.

**Files:**
- Modify: `skills/using-sensemaking/SKILL.md`
- Optional modify: `skills/using-sensemaking/references/adaptive-guidance-v0.md`
- Read/reference: `skills/using-sensemaking/references/practical-agent-architecture-v0.md`

**Interfaces:**
- Consumes: Task 2 reference.
- Produces: a compact canonical entry point that teaches when to externalize warrant/challenge/exploration/delegation logic.

- [ ] **Step 1: Extend “What this Skill teaches” minimally**

Add these capabilities without renumbering into a new workflow family:

```markdown
- name the contemplated warrant target and the few premises that must be true before consequential action;
- use adversarial challenge or exploration when consequence, irreversibility, conflict, novelty, repeated failure, or option poverty makes premature commitment risky;
- treat delegated/orchestrated results as evidence that returns to the active semantic controller.
```

Keep the existing responsibility-before-Skill and authority boundaries.

- [ ] **Step 2: Refine the recursive operating loop**

Replace the compact form only if the meaning stays backward-compatible.

Target wording:

```text
Orient
-> name the consequential decision / contemplated warrant target
-> locate the nearest decision-changing warrant gap
-> select responsibility
-> perform or delegate bounded work
-> ground returned evidence
-> validate mechanics
-> update warrant
-> continue / stop / escalate / verify / ask owner
```

Do not add a runtime phase requirement.

- [ ] **Step 3: Add one bounded “make warrant explicit when useful” section**

Place it after the existing uncertainty-selection discussion.

Include:

```text
For consequential work, ask:
1. What exactly am I trying to justify now?
2. What must be true for that target to be warranted?
3. Which unresolved premise could change responsibility, scope, authority, continuation, or closure?
4. Is more reasoning worth more than acting now?
```

Then link:

```markdown
For challenge/exploration triggers, delegation evidence return, and persistence guidance, read `references/practical-agent-architecture-v0.md` when those decisions are material.
```

- [ ] **Step 4: Add delegation return rule near capability/work sections**

Add a compact rule:

```text
delegated result
-> evidence for the active agent
-> semantic reassessment

delegation does not transfer responsibility-selection or closure authority
unless that authority was explicitly delegated.
```

- [ ] **Step 5: Add challenge/exploration trigger shorthand**

Add a small progressive-disclosure block:

```text
high consequence / low reversibility / conflict / novelty / repeated failure
-> consider adversarial challenge

narrow or repeatedly failing option set / unstable frame
-> consider exploration

otherwise
-> do not add critique ceremony by default
```

- [ ] **Step 6: Decide whether adaptive-guidance-v0 needs one clarification**

Compare Task 3 edits against `adaptive-guidance-v0.md`.

Modify that reference only if the practical architecture concept would otherwise conflict with or remain absent from the consequentiality guidance.

If modified, add only:

```markdown
As consequentiality, irreversibility, novelty, or evidence conflict rises, stronger adversarial challenge or alternative generation may be warranted before commitment. This is qualitative guidance, not a mode, threshold, or routing rule.
```

If not necessary, record no change in Task 4 review.

- [ ] **Step 7: Run Skill hygiene validation**

Run:

```bash
python scripts/validate-skill-hygiene.py
```

Expected: exit 0.

- [ ] **Step 8: Run product-boundary validation**

Run:

```bash
python scripts/validate-product-boundary.py
```

Expected: exit 0 and no automatic-planner/runtime boundary violation.

- [ ] **Step 9: Commit Task 3**

Commit:

```text
docs: integrate warrant-centered agent guidance
```

---

### Task 4: Package-Level Review and Exact-Head Qualification

**Files:**
- Review: `docs/research/practical-agent-architecture-reconciliation-v0.md`
- Review: `skills/using-sensemaking/references/practical-agent-architecture-v0.md`
- Review: `skills/using-sensemaking/SKILL.md`
- Review if changed: `skills/using-sensemaking/references/adaptive-guidance-v0.md`
- Review: `docs/superpowers/specs/2026-09-17-practical-agent-architecture-v0-design.md`
- Update: PR #376 body

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: verified bounded package and explicit stop point before any runtime/schema work.

- [ ] **Step 1: Reconcile plan outcome with Task 1 disposition**

Verify that implemented changes do not exceed the selected disposition.

For `GUIDANCE_ONLY_WARRANTED`, the branch must contain:

- research reconciliation;
- agent reference;
- canonical Skill guidance;
- optional adaptive-guidance clarification.

It must not contain Python/runtime/schema/API changes.

- [ ] **Step 2: Run placeholder and architecture-boundary scan**

Verify no unresolved placeholders and no language implying:

- warrant score;
- automatic routing;
- automatic Skill selection;
- automatic Campaign creation;
- deterministic responsibility selection;
- automatic critic voting;
- new merge/release authority;
- hidden chain-of-thought persistence.

- [ ] **Step 3: Run Skill hygiene validation again on exact head**

Run:

```bash
python scripts/validate-skill-hygiene.py
```

Expected: exit 0.

- [ ] **Step 4: Run product-boundary validation again on exact head**

Run:

```bash
python scripts/validate-product-boundary.py
```

Expected: exit 0.

- [ ] **Step 5: Run repository/Skill contract CI through GitHub exact-head workflows**

Wait for both configured exact-head workflows on the PR head:

```text
Product Validation
Release Candidate Distribution
```

Expected: both complete with `success`.

If either fails:

1. inspect the failing job;
2. determine whether failure is introduced by this package or inherited baseline drift;
3. fix only introduced failures on this branch;
4. do not absorb unrelated repository repair unless separately warranted.

- [ ] **Step 6: Update PR #376 body**

Record:

- Task 1 disposition;
- exact files changed;
- explicit “no runtime/schema/API change” statement;
- validation commands/results;
- exact-head workflow results;
- what the package intentionally did not implement.

- [ ] **Step 7: Stop at the next gate**

The next decision after this package is:

> Does normal use expose any repeated failure that now warrants a bounded durable-state or deterministic-assurance change?

Default answer at completion should remain **no additional machinery** unless new evidence establishes otherwise.

- [ ] **Step 8: Final commit if review corrections were required**

Use:

```text
docs: close Practical Agent Architecture v0 guidance package
```
