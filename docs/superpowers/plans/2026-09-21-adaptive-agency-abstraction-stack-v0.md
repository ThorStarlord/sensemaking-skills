# Adaptive Agency Abstraction Stack v0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Add a bounded research/reference model and Sensemaking reconciliation for Root Primitive -> Cognitive Operator -> Capability/Skill -> Organization -> Institution while preserving current product/runtime authority boundaries.

**Architecture:** Implement a three-plane structural model (capability, coordination, governance/persistence) plus a separate promotion/evolution ladder. Integrate the model into General Agency and Practical Agent Architecture only as interpretive guidance, pin the boundary mechanically with a small documentation contract test, and reconcile STATUS back to normal-use/no-active-construction.

**Tech Stack:** Markdown research/design artifacts, existing Python/pytest documentation-contract tests, GitHub repository/PR validation.

**Spec:** docs/superpowers/specs/2026-09-21-adaptive-agency-abstraction-stack-v0-design.md

## Global Constraints

- ADR 0029 remains the product-boundary authority.
- No runtime, schema, Campaign v3, planner, scheduler, team registry, organization state store, communication bus, or automatic worker allocation.
- Use **Root Primitive** and **Cognitive Operator** to avoid existing repository vocabulary collisions.
- Preserve Campaign != Organization.
- Preserve capability growth != authority growth.
- Preserve agent-created abstraction != self-granted permission.
- Preserve repeated successful coordination != automatic canonical promotion.
- No synthetic multi-agent experiment is required.
- Repository qualification may establish representation/integration coherence only, not empirical value or semantic truth.

## Review Focus

- **Terminology collision:** the new research model must not redefine existing Capability, Campaign, human/operator, or lifecycle-primitive semantics; test that the model uses the qualified terms and explicit non-identities.
- **Product-boundary creep:** organization/institution language must not imply a new Sensemaking runtime; test for the explicit organization modeled != organization runtime warranted boundary and ADR 0029 preservation.
- **Campaign conflation:** no wording may imply Campaign owns roles/topology/worker allocation; test for Campaign != Organization in both model and reconciliation.
- **Authority creep:** capability/pattern creation must not imply permission acquisition; test for capability growth != authority growth and agent-created abstraction != self-granted permission.
- **Status drift:** after closeout STATUS must preserve CURRENT CONSTRUCTION RESPONSIBILITY = NONE, NO_CHANGE, and normal-use posture while naming the new research reference.

---

### Task 1: Add the failing abstraction-boundary contract test

**Files:**
- Create: tests/test_adaptive_agency_abstraction_stack_v0.py

**Interfaces:**
- Consumes: paths and boundary phrases defined by the design spec.
- Produces: a mechanical representation contract that later tasks must satisfy.

- [ ] **Step 1: Write the failing test**

~~~python
"""Mechanical boundary checks for Adaptive Agency Abstraction Stack v0.

These tests pin representation and integration claims only. They do not prove
semantic correctness, empirical usefulness, or a need for organization runtime.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "docs" / "research" / "adaptive-agency-abstraction-stack-v0.md"
RECONCILIATION = (
    ROOT / "docs" / "research" / "adaptive-agency-abstraction-stack-v0-reconciliation.md"
)
GENERAL = ROOT / "docs" / "research" / "general-agency-model-v0.1.md"
PRACTICAL = (
    ROOT
    / "skills"
    / "using-sensemaking"
    / "references"
    / "practical-agent-architecture-v0.md"
)
HANDOFF = ROOT / "docs" / "adaptive-agency-abstraction-stack-v0-handoff.md"
STATUS = ROOT / "STATUS.md"


def test_abstraction_stack_uses_three_planes_and_separate_promotion_ladder() -> None:
    model = MODEL.read_text(encoding="utf-8")

    for phrase in (
        "Capability Plane",
        "Coordination Plane",
        "Governance / Persistence Plane",
        "Promotion / Evolution Ladder",
        "Root Primitive",
        "Cognitive Operator",
        "Capability / Skill",
        "Organization",
        "Institution",
    ):
        assert phrase in model

    assert "Campaign != Organization" in model
    assert "capability growth != authority growth" in model
    assert "agent-created abstraction != self-granted permission" in model
    assert "repeated successful coordination != automatic canonical promotion" in model


def test_reconciliation_keeps_organization_outside_current_runtime_authority() -> None:
    reconciliation = RECONCILIATION.read_text(encoding="utf-8")

    assert "organization modeled != organization runtime warranted" in reconciliation
    assert "Campaign != Organization" in reconciliation
    assert "ADR 0029" in reconciliation
    assert "RUNTIME_GAP" in reconciliation
    assert "NO_RUNTIME_GAP_ESTABLISHED" in reconciliation


def test_general_and_practical_architecture_reference_the_bounded_model() -> None:
    general = GENERAL.read_text(encoding="utf-8")
    practical = PRACTICAL.read_text(encoding="utf-8")

    assert "Adaptive Agency Abstraction Stack v0" in general
    assert "Organization is not a mandatory lifecycle stage" in general
    assert "Adaptive Agency Abstraction Stack v0" in practical
    assert "Campaign != Organization" in practical
    assert "organization pattern != execution authority" in practical


def test_closeout_returns_to_normal_use_without_product_expansion() -> None:
    handoff = HANDOFF.read_text(encoding="utf-8")
    status = STATUS.read_text(encoding="utf-8")

    assert "NO_RUNTIME_GAP_ESTABLISHED" in handoff
    assert "NO_PRODUCT_BOUNDARY_CHANGE" in handoff
    assert "NORMAL_USE_VALIDATION" in handoff

    assert "Adaptive Agency Abstraction Stack v0" in status
    assert "CURRENT CONSTRUCTION RESPONSIBILITY = NONE" in status
    assert "Level-3 disposition: NO_CHANGE" in status
    assert "NORMAL_USE_VALIDATION" in status
~~~

- [ ] **Step 2: Run the focused test and verify RED**

Run:

~~~bash
python -m pytest tests/test_adaptive_agency_abstraction_stack_v0.py -q
~~~

Expected: FAIL because the model/reconciliation/handoff files and integration phrases do not yet exist.

- [ ] **Step 3: Commit the red contract test**

~~~bash
git add tests/test_adaptive_agency_abstraction_stack_v0.py
git commit -m "test: pin adaptive agency abstraction boundaries"
~~~

### Task 2: Add the research model and Sensemaking reconciliation

**Files:**
- Create: docs/research/adaptive-agency-abstraction-stack-v0.md
- Create: docs/research/adaptive-agency-abstraction-stack-v0-reconciliation.md

**Interfaces:**
- Consumes: General Agency Model v0.1 cognitive operators; Practical Agent Architecture v0 delegation model; current Capability/Skill, Campaign, Execution Interface, ADR 0029, and authority semantics.
- Produces: canonical non-authoritative research vocabulary and a repository-specific disposition for each rung/plane.

- [ ] **Step 1: Author the research model**

The model must include:

~~~text
Capability Plane
  Root Primitive -> Cognitive Operator -> Capability / Skill

Coordination Plane
  delegation -> team/cell -> Organization

Governance / Persistence Plane
  rules/policy/authority/provenance/continuity -> Institution
~~~

It must separately define:

~~~text
Promotion / Evolution Ladder
ephemeral composition
-> candidate reusable operator
-> packaged capability / Skill
-> repeatable coordination pattern
-> institutionalized practice
~~~

It must answer the five crosswalk questions from the spec and preserve every Required Boundary Law.

- [ ] **Step 2: Author the Sensemaking reconciliation**

Use a disposition table with at least:

~~~text
Root Primitive                  OUTSIDE_PRODUCT / ENVIRONMENT_SUBSTRATE
Cognitive Operator              ALREADY_PRESENT_RESEARCH
Capability / Skill              ALREADY_SATISFIED
Organization                    PARTIAL_CONCEPT / OUTSIDE_RUNTIME
Institution-like continuity     ALREADY_PARTIALLY_REALIZED
Organization runtime            NOT_WARRANTED
Organizational-pattern learning RESEARCH_HYPOTHESIS
~~~

The reconciliation must explicitly conclude:

~~~text
RUNTIME_GAP = NO_RUNTIME_GAP_ESTABLISHED
PRODUCT_BOUNDARY_CHANGE = NONE
CURRENT CONSTRUCTION RESPONSIBILITY = NONE
~~~

- [ ] **Step 3: Re-run the focused test**

Run:

~~~bash
python -m pytest tests/test_adaptive_agency_abstraction_stack_v0.py -q
~~~

Expected: still FAIL only on General/PAA/handoff/STATUS integration assertions; the model/reconciliation assertions pass.

- [ ] **Step 4: Commit the research pair**

~~~bash
git add docs/research/adaptive-agency-abstraction-stack-v0.md docs/research/adaptive-agency-abstraction-stack-v0-reconciliation.md
git commit -m "docs: add adaptive agency abstraction research model"
~~~

### Task 3: Integrate General Agency and Practical Agent Architecture guidance

**Files:**
- Modify: docs/research/general-agency-model-v0.1.md
- Modify: skills/using-sensemaking/references/practical-agent-architecture-v0.md

**Interfaces:**
- Consumes: the research model and reconciliation from Task 2.
- Produces: bounded references that clarify organization/institution placement without creating new runtime authority.

- [ ] **Step 1: Update General Agency Model v0.1**

Add a short research-reference section after cognitive operators/control-envelope discussion stating:

~~~text
Adaptive Agency Abstraction Stack v0
= supporting research model for capability composition, multi-actor coordination,
  and institution-like governance/persistence

Organization is not a mandatory lifecycle stage.
Institution is not a larger agent.
~~~

Clarify that organization can emerge as a metareasoning/decomposition consequence when multiple actors are available, while institution is an outer governance/persistence concept.

- [ ] **Step 2: Update Practical Agent Architecture v0**

Extend the multi-agent delegation section with:

~~~text
Campaign != Organization
delegation != Organization automatically
organization pattern != execution authority
~~~

Reference the research model and state that adaptive organizational formation belongs primarily to the external orchestration/software-factory side unless a future product-boundary decision says otherwise.

- [ ] **Step 3: Re-run the focused test**

Run:

~~~bash
python -m pytest tests/test_adaptive_agency_abstraction_stack_v0.py -q
~~~

Expected: FAIL only on handoff/STATUS assertions.

- [ ] **Step 4: Run adjacent policy contract tests**

Run:

~~~bash
python -m pytest tests/test_policy_hierarchy_contract.py -q
~~~

Expected: PASS.

- [ ] **Step 5: Commit integration guidance**

~~~bash
git add docs/research/general-agency-model-v0.1.md skills/using-sensemaking/references/practical-agent-architecture-v0.md
git commit -m "docs: integrate capability organization institution guidance"
~~~

### Task 4: Close out the package and restore normal-use state

**Files:**
- Create: docs/adaptive-agency-abstraction-stack-v0-handoff.md
- Modify: STATUS.md
- Modify: .github/workflows/validation.yml
- Modify: .github/workflows/release-candidate.yml

**Interfaces:**
- Consumes: completed research model, reconciliation, and integrated guidance.
- Produces: reconstructible completion receipt and current Level-3 projection.

- [ ] **Step 1: Write the handoff**

The handoff must record:

- owner direction / Issue #444;
- files changed;
- exact conceptual disposition;
- no runtime/schema/product-boundary change;
- boundary laws;
- validation evidence;
- future reopen conditions based on normal-use organizational friction;
- terminal markers:

~~~text
RESEARCH_REFERENCE_COMPLETE
RUNTIME_GAP = NO_RUNTIME_GAP_ESTABLISHED
PRODUCT_BOUNDARY = NO_PRODUCT_BOUNDARY_CHANGE
CURRENT CONSTRUCTION RESPONSIBILITY = NONE
NEXT MODE = NORMAL_USE_VALIDATION
~~~

- [ ] **Step 2: Reconcile STATUS.md**

Add the research package to Current capability state / Strategic Frontier as appropriate, but preserve:

~~~text
CURRENT CONSTRUCTION RESPONSIBILITY = NONE
PRIMARY CONSTRUCTION PROGRAM = NONE
Level-3 disposition: NO_CHANGE
NEXT MODE = NORMAL_USE_VALIDATION
~~~

Do not reopen a runtime program.

- [ ] **Step 3: Wire the focused boundary test into hosted qualification**

Add `tests/test_adaptive_agency_abstraction_stack_v0.py` to the existing Stable repository assertion suite in Product Validation and the Release baseline contracts list in Release Candidate Distribution. Do not create a new workflow or runtime gate.

- [ ] **Step 4: Run the focused test and verify GREEN**

Run:

~~~bash
python -m pytest tests/test_adaptive_agency_abstraction_stack_v0.py -q
~~~

Expected: PASS.

- [ ] **Step 5: Run adjacent and repository-level validation**

Run:

~~~bash
python -m pytest tests/test_policy_hierarchy_contract.py tests/test_execution_interface_closeout.py -q
python scripts/validate-repo.py
~~~

Expected: PASS.

- [ ] **Step 6: Commit closeout**

~~~bash
git add STATUS.md docs/adaptive-agency-abstraction-stack-v0-handoff.md
git commit -m "docs: close adaptive agency abstraction stack v0"
~~~

### Task 5: PR qualification and integration

**Files:**
- No new product files unless qualification finds a concrete defect.

**Interfaces:**
- Consumes: branch head from Tasks 1-4.
- Produces: reviewed/integrated repository state or an explicit blocker.

- [ ] **Step 1: Open a PR linked to Issue #444**

PR body must summarize:

- three-plane model;
- promotion ladder;
- Campaign/Organization distinction;
- capability/authority separation;
- no runtime/product expansion;
- local/hosted validation evidence.

- [ ] **Step 2: Verify exact PR-head checks**

Check the current head SHA and hosted statuses. Do not claim qualification from stale commits.

- [ ] **Step 3: Merge only if the required checks are green or no required check is configured**

Use the repository's normal merge method. If GitHub reports a real merge/branch protection blocker, preserve the PR and report the blocker rather than fabricating completion.

- [ ] **Step 4: Close Issue #444 and reconcile final main identity**

Record the merge/main SHA in the issue closeout comment if integration succeeds.
