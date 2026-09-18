# General Agency Model v0.1 Research Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refine the General Agency research model with explicit memory/provenance substrate, knowledge externalization, conditional exploration policy, and search-state concepts, then reconcile those additions against current Sensemaking without creating unwarranted runtime/product machinery.

**Architecture:** Preserve General Agency Model v0 as the historical baseline and add a successor v0.1 research reference. Reconcile v0.1 against the existing General Agency ↔ Sensemaking crosswalk, Practical Agent Architecture v0, and canonical `using-sensemaking` guidance. Canonical guidance may change only when the reconciliation establishes a bounded `GUIDANCE_GAP`; no runtime, schema, persistence engine, public API, product-boundary, or authority change is permitted by this plan.

**Tech Stack:** Markdown research/reference docs, existing Sensemaking Skills documentation contracts, repository validators, GitHub exact-head CI.

**Spec:** `docs/superpowers/specs/2026-09-18-general-agency-model-v0.1-design.md`

## Global Constraints

- ADR 0029 remains authoritative; this package must not expand the current product boundary.
- Preserve `docs/research/general-agency-model-v0.md` and `docs/research/general-agency-sensemaking-crosswalk-v0.md` as historical baselines.
- Memory / Provenance is a persistent substrate, not a mandatory visible phase.
- Knowledge Externalization / Communication is distinct from storage and remains adaptive.
- Exploration operator and Exploration Policy must remain distinct.
- Search State is a decision-relevant projection of memory/provenance, not a required schema.
- Available capability does not imply warranted activation.
- Hidden chain-of-thought is never a persistence requirement.
- Reuse existing Campaign, ADR, handoff, artifact, STATUS, strategic-state, and provenance surfaces before considering generic machinery.
- No `MemoryEngine`, `KnowledgeExternalizationService`, `SearchState` schema, search-tree database, `ExplorationPolicy` runtime class, numeric exploration scoring, automatic search routing, vector-memory infrastructure, Campaign schema change, public API change, Practical Agent Architecture v1, or product-boundary expansion.
- Product/Skill guidance may change only after Task 3 classifies a concrete `GUIDANCE_GAP`.
- Runtime/state/assurance implementation may not be added under this plan even if Task 3 identifies a possible future gap; such a finding must be recorded as future evidence/reopen criteria instead.
- Keep the package research/reference-first and YAGNI.

---

## File Structure

### Files to create

- `docs/research/general-agency-model-v0.1.md`
  - Successor research/reference model.
  - Carries forward v0 concepts while integrating the approved v0.1 refinements.
  - Does not replace or rewrite the v0 historical baseline.

- `docs/research/general-agency-sensemaking-crosswalk-v0.1.md`
  - Successor crosswalk.
  - Maps the four v0.1 additions and Adaptive Capability Activation onto existing Sensemaking/PAA surfaces.
  - Preserves explicit non-equivalences and product-boundary ceilings.

- `docs/research/general-agency-model-v0.1-reconciliation.md`
  - Repository-specific decision record for whether each conceptual addition exposes an implementation gap.
  - Uses only the fixed disposition vocabulary:
    `ALREADY_SATISFIED`, `GUIDANCE_GAP`, `DURABLE_STATE_GAP`, `DETERMINISTIC_ASSURANCE_GAP`, `OUTSIDE_PRODUCT`, `UNRESOLVED`.
  - Records the smallest warranted intervention and rejected heavier interventions.

### Files that may be modified only if Task 3 proves a guidance gap

- `skills/using-sensemaking/references/practical-agent-architecture-v0.md`
  - Add only bounded conceptual guidance that the reconciliation proves absent and decision-relevant.

- `skills/using-sensemaking/SKILL.md`
  - Add only compact bootstrap-level guidance necessary for ordinary agent operation.
  - Do not duplicate the detailed reference.

### Files that must not be modified by default

- `docs/research/general-agency-model-v0.md`
- `docs/research/general-agency-sensemaking-crosswalk-v0.md`
- `docs/adr/0029-current-product-boundary.md`
- Campaign schemas or Python runtime/state modules
- Public API manifests
- `STATUS.md` unless a later, separately warranted closeout determines the current strategic projection materially changed

---

### Task 1: Create General Agency Model v0.1 successor reference

**Files:**
- Read: `docs/research/general-agency-model-v0.md`
- Read: `docs/superpowers/specs/2026-09-18-general-agency-model-v0.1-design.md`
- Create: `docs/research/general-agency-model-v0.1.md`

**Interfaces:**
- Consumes: General Agency Model v0 terminology, lifecycle, operators, control envelopes, persistent-state model, and the approved v0.1 design.
- Produces: canonical research/reference description of General Agency Model v0.1 for later crosswalk and reconciliation tasks.

- [ ] **Step 1: Copy the v0 conceptual baseline into a successor document without editing the v0 file**

Create `docs/research/general-agency-model-v0.1.md` as a successor document. Its header must explicitly state:

```markdown
# General Agency Model v0.1

**Status:** research/reference model; non-authoritative
**Date:** 2026-09-18
**Supersedes for research/reference use:** General Agency Model v0
**Historical baseline preserved:** `general-agency-model-v0.md`
**Authority:** research only; not an ADR, product-strategy revision, runtime specification, schema, Skill contract, routing rule, or implementation authorization
**Current product boundary:** unchanged; ADR 0029 remains authoritative
**Design:** `../superpowers/specs/2026-09-18-general-agency-model-v0.1-design.md`
```

Do not delete or rewrite v0.

- [ ] **Step 2: Revise the architecture overview so persistent memory is shown as substrate**

The model must explicitly state:

```text
Memory / Provenance
!= final lifecycle phase

Memory / Provenance
= persistent substrate read and written across cycles
```

Include the approved v0.1 architecture diagram from the design spec, preserving:

- core cognitive cycle;
- control envelopes;
- conditional inquiry/search controller;
- lateral cognitive operators;
- Memory / Provenance substrate;
- Knowledge Externalization / Communication as cross-cutting capability.

- [ ] **Step 3: Add the Memory / Provenance substrate section**

Define:

- read/write relationship across cycle stages;
- search history/results as optional persistent content when decision-relevant;
- distinction from epistemic state;
- distinction from documentation/externalization;
- distinction from hidden chain-of-thought;
- provenance/currentness as evidence lineage, not semantic truth.

Required non-identities:

```text
memory != epistemic state
memory != documentation
memory != hidden chain-of-thought
memory != universal database
provenance != truth
stored != decision-relevant
```

- [ ] **Step 4: Add Knowledge Externalization / Communication**

Define it as:

> What selected knowledge should be made explicit, durable, intelligible, and transferable to another actor, in what representation, and with what provenance?

Include:

```text
externalization
=
selection
+ compression
+ structuring
+ explanation
+ audience adaptation
+ provenance attachment
```

Document adaptive triggers:

- cross-context continuation;
- delegation/handoff;
- meaningful rediscovery cost;
- consequential decision rationale;
- governance/audit requirement;
- operational/user need;
- future search quality depends on preserved search history.

Include:

```text
reasoning result
!= durable artifact required
```

- [ ] **Step 5: Refine Metareasoning and Exploration sections**

Preserve the existing exploration operator:

> What plausible frame, option, explanation, or intervention is not yet represented?

Then add Exploration Policy as a separate concept:

> Given the current search state, evidence, uncertainty, resources, and history, where should search effort go next?

Define these candidate search modes without making them mandatory enums:

```text
EXPLOIT
EXPLORE
ADVERSARIAL
DIAGNOSTIC
COMBINATORIAL
RESTART
VERIFY
```

State explicitly:

```text
exploration operator
!= exploration policy

metareasoning
= whether / how to conduct cognition or search

exploration policy
= where iterative search effort goes next once such search is warranted
```

- [ ] **Step 6: Add Search State as a conceptual projection**

Define Search State as a decision-relevant projection of Memory / Provenance for the current investigation.

Candidate content:

- attempts;
- outcomes;
- promising branches;
- abandoned branches/reasons;
- failure attribution;
- unresolved search uncertainty;
- budget;
- verified results;
- relevant provenance.

Required boundary:

```text
Search State
!= mandatory persistent object
!= SearchState.json
!= generic search-tree database
```

- [ ] **Step 7: Name Adaptive Capability Activation as a control principle**

Add the rule:

> A cognitive capability being available does not imply that invoking it is warranted.

Tie activation to:

- metareasoning;
- sufficiency;
- expected decision improvement;
- information/reasoning/delay/opportunity cost;
- consequence;
- reversibility;
- authority;
- continuation complexity.

Apply it to challenge, exploration, exploration policy, forecasting, delegation, persistence, externalization, verification depth, and strategic ascent.

- [ ] **Step 8: Preserve and extend evidence ceilings/non-goals**

The v0.1 document must explicitly reject automatic inference from conceptual model to:

- generic memory runtime;
- exploration runtime;
- search persistence;
- product expansion;
- recursive self-improvement claims;
- model-weight learning;
- automatic documentation;
- deterministic capability activation.

- [ ] **Step 9: Run Task 1 static checks**

Run:

```bash
python - <<'PY'
from pathlib import Path
p = Path("docs/research/general-agency-model-v0.1.md")
text = p.read_text(encoding="utf-8")
required = [
    "Memory / Provenance",
    "Knowledge Externalization / Communication",
    "Exploration Policy",
    "Search State",
    "Adaptive Capability Activation",
    "ADR 0029 remains authoritative",
    "memory != hidden chain-of-thought",
    "reasoning result",
    "exploration operator",
]
missing = [s for s in required if s not in text]
assert not missing, missing
assert "TBD" not in text and "TODO" not in text and "FIXME" not in text
assert Path("docs/research/general-agency-model-v0.md").exists()
print("general-agency-model-v0.1 static checks: PASS")
PY
```

Expected: `general-agency-model-v0.1 static checks: PASS`.

- [ ] **Step 10: Commit Task 1**

```bash
git add docs/research/general-agency-model-v0.1.md
git commit -m "docs: refine General Agency Model v0.1"
```

---

### Task 2: Create General Agency ↔ Sensemaking crosswalk v0.1

**Files:**
- Read: `docs/research/general-agency-sensemaking-crosswalk-v0.md`
- Read: `docs/research/general-agency-model-v0.1.md`
- Read: `docs/superpowers/specs/2026-09-17-practical-agent-architecture-v0-design.md`
- Read: `skills/using-sensemaking/references/practical-agent-architecture-v0.md`
- Create: `docs/research/general-agency-sensemaking-crosswalk-v0.1.md`

**Interfaces:**
- Consumes: v0.1 model concepts plus current PAA/Sensemaking surfaces.
- Produces: domain mapping and explanatory/non-equivalence evidence used by Task 3.

- [ ] **Step 1: Preserve the v0 crosswalk structure and classification discipline**

Carry forward the existing categories:

```text
EXACT
PARTIAL
DOMAIN_SPECIALIZATION
NON_EQUIVALENT
```

State that these are conceptual mapping categories, not Task 3 implementation dispositions.

- [ ] **Step 2: Add/refine crosswalk rows for the v0.1 concepts**

The crosswalk must include explicit rows for:

#### Memory / Provenance substrate

Candidate Sensemaking surfaces:

- Campaign state;
- evidence/provenance/currentness;
- transition history;
- STATUS;
- handoff/resume;
- ADRs;
- strategic-state artifacts.

Expected conceptual mapping: likely `DOMAIN_SPECIALIZATION`, but the executor must verify against current files rather than blindly copy this expectation.

#### Knowledge Externalization / Communication

Candidate surfaces:

- ADRs;
- handoffs;
- repository artifacts;
- Campaign projections;
- reports;
- Skills/reference docs;
- STATUS/reconciliation records.

The crosswalk must state:

```text
durable state exists
!= knowledge is sufficiently transferable
```

#### Exploration Policy

Candidate surfaces:

- PAA exploration triggers/stopping;
- `using-sensemaking` challenge/exploration guidance;
- Strategic Frontier alternatives;
- resource-aware stopping;
- repeated-failure reassessment.

The crosswalk must distinguish:

```text
exploration operator
!= search-allocation policy
```

#### Search State

Candidate surfaces:

- Campaign evidence/transition history;
- uncertainty history;
- strategic alternatives;
- handoff records;
- ordinary repository history.

The crosswalk must state that no generic search-state schema currently follows.

#### Adaptive Capability Activation

Candidate surfaces:

- adaptive guidance;
- "use the lightest process";
- Campaign only when continuation warrants it;
- challenge/exploration triggers;
- minimum necessary ascent;
- smallest warranted intervention.

- [ ] **Step 3: Add explicit non-equivalences**

At minimum:

```text
General memory != Campaign State
Knowledge externalization != documentation phase
Knowledge externalization != store every thought
Exploration operator != Exploration Policy
Exploration Policy != Strategic Frontier ranking
Search State != Campaign schema
Search State != hidden chain-of-thought
Adaptive Capability Activation != deterministic routing
Available capability != selected capability
```

- [ ] **Step 4: Re-run the existing scenario stress tests conceptually**

Update the existing trivial/ambiguous/strategic/product-thesis scenarios and add:

```text
E. Repeated iterative search
F. Fresh-agent continuation of prior search
G. Documentation-heavy release workflow
```

For each scenario, show which v0.1 capability becomes explicit and which remains implicit.

- [ ] **Step 5: Run Task 2 static checks**

Run:

```bash
python - <<'PY'
from pathlib import Path
p = Path("docs/research/general-agency-sensemaking-crosswalk-v0.1.md")
text = p.read_text(encoding="utf-8")
required = [
    "Memory / Provenance",
    "Knowledge Externalization",
    "Exploration Policy",
    "Search State",
    "Adaptive Capability Activation",
    "DOMAIN_SPECIALIZATION",
    "NON_EQUIVALENT",
    "Available capability != selected capability",
]
missing = [s for s in required if s not in text]
assert not missing, missing
assert "TBD" not in text and "TODO" not in text and "FIXME" not in text
print("general-agency-sensemaking-crosswalk-v0.1 static checks: PASS")
PY
```

Expected: `general-agency-sensemaking-crosswalk-v0.1 static checks: PASS`.

- [ ] **Step 6: Commit Task 2**

```bash
git add docs/research/general-agency-sensemaking-crosswalk-v0.1.md
git commit -m "docs: crosswalk General Agency v0.1 to Sensemaking"
```

---

### Task 3: Reconcile v0.1 concepts against current Sensemaking

**Files:**
- Read: `docs/research/general-agency-model-v0.1.md`
- Read: `docs/research/general-agency-sensemaking-crosswalk-v0.1.md`
- Read: `docs/research/practical-agent-architecture-reconciliation-v0.md`
- Read: `skills/using-sensemaking/SKILL.md`
- Read: `skills/using-sensemaking/references/practical-agent-architecture-v0.md`
- Read: current Campaign/strategic-state documentation as needed
- Create: `docs/research/general-agency-model-v0.1-reconciliation.md`

**Interfaces:**
- Consumes: conceptual mappings from Task 2 and current product reality.
- Produces: fixed implementation dispositions that gate Task 4.

- [ ] **Step 1: Use only the fixed disposition vocabulary**

Every v0.1 concept must receive exactly one of:

```text
ALREADY_SATISFIED
GUIDANCE_GAP
DURABLE_STATE_GAP
DETERMINISTIC_ASSURANCE_GAP
OUTSIDE_PRODUCT
UNRESOLVED
```

Do not invent mixed labels such as `ALREADY_SATISFIED_WITH_MINOR_GAP`.

- [ ] **Step 2: Evaluate Memory / Provenance substrate**

Answer:

1. Can current Campaign/STATUS/handoff/provenance surfaces preserve reconstructible decision state when continuation warrants it?
2. Is search history representable using existing evidence/history/handoff surfaces when material?
3. Is any generic memory substrate needed for the current repository domain?
4. Is hidden chain-of-thought being accidentally treated as required state?

A `DURABLE_STATE_GAP` requires repeated normal-use evidence that materially necessary state cannot be reconstructed using current surfaces.

No such gap may be inferred merely because a generic memory architecture is imaginable.

- [ ] **Step 3: Evaluate Knowledge Externalization / Communication**

Answer:

1. Do existing artifacts, ADRs, handoffs, reports, Skills, and Campaign projections already externalize durable knowledge?
2. Does canonical guidance tell the agent when externalization is warranted versus ephemeral reasoning?
3. Is the missing distinction decision-relevant in ordinary use?
4. Would a guidance addition reduce rediscovery/continuation errors without imposing mandatory documentation ceremony?

Classify based on repository evidence.

- [ ] **Step 4: Evaluate Exploration Policy**

First distinguish the existing PAA section from the v0.1 refinement:

```text
existing PAA:
when to explore + when to stop exploring

v0.1 Exploration Policy:
given iterative search history, where should effort go next?
```

Then answer:

1. Does current guidance already cover repeated failure and option-set broadening sufficiently?
2. Does it tell agents how to choose among exploit / explore / diagnose / challenge / recombine / restart / verify when iterative search exists?
3. Is that absence currently a meaningful guidance gap, or merely a useful research distinction?
4. Is there any evidence for a persistent search-tree/runtime need? If not, explicitly reject it.

- [ ] **Step 5: Evaluate Search State**

Answer:

1. Is Search State already derivable as a view over existing evidence/history?
2. Does any ordinary current task require a dedicated durable representation?
3. Would adding a schema create a second truth system or unnecessary ceremony?

A `DURABLE_STATE_GAP` requires evidence of repeated reconstruction failure, not theoretical usefulness.

- [ ] **Step 6: Evaluate Adaptive Capability Activation**

Reconcile against:

- adaptive guidance;
- lightest-process rule;
- challenge/exploration triggers;
- Campaign conditionality;
- resource-aware stopping;
- minimum necessary ascent;
- the two completed normal-use probes.

Determine whether this is already satisfied or whether only wording is missing.

- [ ] **Step 7: Record smallest warranted interventions and rejected heavier interventions**

For every concept classified `GUIDANCE_GAP`, state the exact minimal guidance surface that should change.

For every concept not classified `GUIDANCE_GAP`, state `no canonical guidance change warranted`.

Explicitly reject, unless evidence directly contradicts the spec:

- generic memory engine;
- generic search state schema;
- exploration runtime;
- deterministic capability activator;
- numeric exploration scoring;
- automatic documentation policy;
- automatic Skill/workflow routing;
- new Campaign truth system.

- [ ] **Step 8: Determine package-level disposition**

Use exactly one package-level disposition:

```text
NO_CHANGE_WARRANTED
GUIDANCE_ONLY_WARRANTED
ARCHITECTURE_REVIEW_REQUIRED
```

Expected likely outcome from current evidence is `GUIDANCE_ONLY_WARRANTED` or `NO_CHANGE_WARRANTED`; this expectation is not authority to force the result.

`ARCHITECTURE_REVIEW_REQUIRED` is appropriate only if repository evidence reveals a concrete state/assurance/product-boundary contradiction that cannot be resolved within the approved spec.

- [ ] **Step 9: Run Task 3 static checks**

Run:

```bash
python - <<'PY'
from pathlib import Path
p = Path("docs/research/general-agency-model-v0.1-reconciliation.md")
text = p.read_text(encoding="utf-8")
concepts = [
    "Memory / Provenance",
    "Knowledge Externalization",
    "Exploration Policy",
    "Search State",
    "Adaptive Capability Activation",
]
for c in concepts:
    assert c in text, c
allowed = [
    "ALREADY_SATISFIED",
    "GUIDANCE_GAP",
    "DURABLE_STATE_GAP",
    "DETERMINISTIC_ASSURANCE_GAP",
    "OUTSIDE_PRODUCT",
    "UNRESOLVED",
]
assert any(x in text for x in allowed)
assert "MemoryEngine" in text
assert "SearchState" in text
assert "TBD" not in text and "TODO" not in text and "FIXME" not in text
assert "ADR 0029" in text
print("general-agency-model-v0.1 reconciliation static checks: PASS")
PY
```

Expected: `general-agency-model-v0.1 reconciliation static checks: PASS`.

- [ ] **Step 10: Commit Task 3**

```bash
git add docs/research/general-agency-model-v0.1-reconciliation.md
git commit -m "docs: reconcile General Agency v0.1 with Sensemaking"
```

---

### Task 4: Apply only reconciliation-proven guidance changes

**Files:**
- Read: `docs/research/general-agency-model-v0.1-reconciliation.md`
- Conditionally modify: `skills/using-sensemaking/references/practical-agent-architecture-v0.md`
- Conditionally modify: `skills/using-sensemaking/SKILL.md`

**Interfaces:**
- Consumes: Task 3's package-level and per-concept dispositions.
- Produces: either no canonical guidance diff, or the smallest guidance-only diff established by the reconciliation.

- [ ] **Step 1: Gate on Task 3 disposition**

If Task 3 concludes:

```text
NO_CHANGE_WARRANTED
```

then make **no changes** to Skill/reference guidance and proceed directly to Task 5.

If Task 3 concludes:

```text
GUIDANCE_ONLY_WARRANTED
```

modify only the exact surfaces named by the reconciliation.

If Task 3 concludes:

```text
ARCHITECTURE_REVIEW_REQUIRED
```

stop this plan. Do not invent runtime/state/assurance work inside this package.

- [ ] **Step 2: If Knowledge Externalization has `GUIDANCE_GAP`, add bounded guidance**

Detailed reference guidance may add a compact rule such as:

```text
Externalize decision-relevant knowledge when:
- continuation crosses context/actor boundaries;
- rediscovery would be meaningfully costly;
- consequential rationale/evidence must remain reconstructible;
- governance/operations/user transfer requires it.

reasoning result != durable artifact required
```

The bootstrap should receive only the smallest operational summary if needed.

Do not create a mandatory documentation phase.

- [ ] **Step 3: If Exploration Policy has `GUIDANCE_GAP`, add bounded iterative-search guidance**

Detailed reference guidance may add:

```text
When iterative search has multiple meaningful attempts, use search history to decide whether the next move should:
- exploit;
- explore;
- challenge;
- diagnose;
- recombine;
- restart;
- verify.

Do not formalize this as an enum or score.
For one-shot/local work, keep it implicit.
```

Bootstrap guidance should remain compact and trigger-based.

- [ ] **Step 4: If Search State or Memory is `ALREADY_SATISFIED`, do not add new state requirements**

Ensure no language implies:

- every search needs persistence;
- every task needs a Campaign;
- every thought needs externalization;
- hidden reasoning should be persisted.

- [ ] **Step 5: Verify canonical guidance changes if any**

Run:

```bash
python scripts/validate-skill-hygiene.py
python scripts/validate-repo.py
```

Expected: PASS.

Then run a static anti-ceremony check:

```bash
python - <<'PY'
from pathlib import Path
paths = [
    Path("skills/using-sensemaking/SKILL.md"),
    Path("skills/using-sensemaking/references/practical-agent-architecture-v0.md"),
]
text = "\n".join(p.read_text(encoding="utf-8") for p in paths)
for forbidden in [
    "MemoryEngine",
    "KnowledgeExternalizationService",
    "SearchState.json",
    "must always create a Campaign",
    "must always explore",
]:
    assert forbidden not in text, forbidden
print("canonical guidance anti-ceremony checks: PASS")
PY
```

Expected: `canonical guidance anti-ceremony checks: PASS`.

- [ ] **Step 6: Commit Task 4 only if files changed**

If guidance changed:

```bash
git add skills/using-sensemaking/SKILL.md skills/using-sensemaking/references/practical-agent-architecture-v0.md
git commit -m "docs: integrate bounded General Agency v0.1 guidance"
```

If no guidance changed, do not create an empty commit.

---

### Task 5: Package verification and exact-head qualification

**Files:**
- Verify all changed files from Tasks 1–4.
- Do not add new product/runtime files during this task.

**Interfaces:**
- Consumes: complete v0.1 research/reconciliation package.
- Produces: qualification evidence suitable for PR review and merge decision.

- [ ] **Step 1: Verify expected change surface**

Run:

```bash
git diff --name-only origin/main...HEAD
```

Expected baseline set:

```text
docs/superpowers/specs/2026-09-18-general-agency-model-v0.1-design.md
docs/superpowers/plans/2026-09-18-general-agency-model-v0.1-reconciliation.md
docs/research/general-agency-model-v0.1.md
docs/research/general-agency-sensemaking-crosswalk-v0.1.md
docs/research/general-agency-model-v0.1-reconciliation.md
```

The following may additionally appear **only if Task 3 established `GUIDANCE_GAP`**:

```text
skills/using-sensemaking/SKILL.md
skills/using-sensemaking/references/practical-agent-architecture-v0.md
```

No Python/runtime/schema/public-API file should appear.

- [ ] **Step 2: Run placeholder and boundary scan**

Run:

```bash
python - <<'PY'
from pathlib import Path
paths = [
    Path("docs/superpowers/specs/2026-09-18-general-agency-model-v0.1-design.md"),
    Path("docs/superpowers/plans/2026-09-18-general-agency-model-v0.1-reconciliation.md"),
    Path("docs/research/general-agency-model-v0.1.md"),
    Path("docs/research/general-agency-sensemaking-crosswalk-v0.1.md"),
    Path("docs/research/general-agency-model-v0.1-reconciliation.md"),
]
for p in paths:
    text = p.read_text(encoding="utf-8")
    assert "TBD" not in text, p
    assert "TODO" not in text, p
    assert "FIXME" not in text, p

combined = "\n".join(p.read_text(encoding="utf-8") for p in paths)
required = [
    "ADR 0029",
    "Memory / Provenance",
    "Knowledge Externalization",
    "Exploration Policy",
    "Search State",
    "Adaptive Capability Activation",
]
for item in required:
    assert item in combined, item

print("v0.1 package boundary checks: PASS")
PY
```

Expected: `v0.1 package boundary checks: PASS`.

- [ ] **Step 3: Run repository/Skill validation**

Run:

```bash
python scripts/validate-repo.py
python scripts/validate-skill-hygiene.py
```

Expected: PASS.

If the repository's normal test command is available in the execution environment, run it as well; do not claim local full-suite PASS if the environment cannot execute it.

- [ ] **Step 4: Fresh review against the approved design**

Check line-by-line that:

- v0 is preserved;
- v0.1 includes all four additions;
- Search State remains projection-only;
- externalization remains adaptive;
- exploration policy remains conditional;
- anti-ceremony activation law is explicit;
- no runtime/schema/product authority leaked in;
- crosswalk distinguishes conceptual mapping from implementation disposition;
- reconciliation uses fixed disposition vocabulary;
- canonical guidance changed only if Task 3 proved a guidance gap.

Fix any Critical/Important issue before proceeding.

- [ ] **Step 5: Push branch and open PR**

Create a PR whose summary includes:

```text
General Agency Model v0.1:
- Memory / Provenance as persistent substrate
- Knowledge Externalization / Communication
- conditional Exploration Policy
- Search State as projection
- Adaptive Capability Activation

Reconciliation:
- per-concept dispositions
- package-level disposition
- explicit rejected machinery
```

The PR must state that ADR 0029 and product/runtime boundaries remain unchanged.

- [ ] **Step 6: Wait for exact-head GitHub qualification**

Require the repository's normal exact-head workflows to complete successfully, including:

- Product Validation;
- Release Candidate Distribution.

Do not infer exact-head qualification from an older commit.

- [ ] **Step 7: Merge remains a protected transition**

After exact-head qualification, refresh:

- PR head SHA;
- mergeability;
- review comments;
- workflow conclusions.

Only merge when current authority permits it. Do not equate green CI with merge authority.

---

## Plan Self-Review Checklist

- [ ] The plan preserves v0 rather than rewriting history.
- [ ] Every approved v0.1 concept has an implementation/reconciliation task.
- [ ] Conceptual mapping and product implementation disposition remain separate.
- [ ] Product/runtime work is blocked unless separately authorized.
- [ ] Canonical guidance is conditional on a Task 3 `GUIDANCE_GAP`.
- [ ] No generic memory/search runtime is planned.
- [ ] No placeholder language remains.
- [ ] Exact-head qualification and merge authority remain separate.
