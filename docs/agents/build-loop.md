# Build Loop: Choosing and Building an Increment

This is the **operational application** of
[Value-Directed Continuous Construction](../value-directed-continuous-construction.md),
which explains the product-value-led Architect + Builder philosophy. `CLAUDE.md`
carries the brief entry trigger and the current PR and local verification rules.
This reference does not add a Skill, runtime, artifact type, planner, or
permission to change a higher-level decision.

The **active coding agent** remains the semantic controller (ADR 0013).
Architect, Builder and Close are complementary responsibilities within one
adaptive engineering loop, not separate agents, mandatory approvals or a
three-stage runtime. They can overlap and revisit one another when new
implementation evidence changes the warranted design.

```text
PRODUCT INTENT + CURRENT EVIDENCE
        -> ARCHITECT: decide the warranted increment (brief decision note)
        -> BUILDER: implement, inspect, revise within authority
        -> CLOSE: PR evidence, relevant reconciliation, next decision
```

**Every PR gets a short decision note in its description.** For an obvious,
low-consequence fix this can be two sentences; substantial architectural
choices require enough detail to reconstruct the selection. No extra
repository artifact, numerical score, minimum candidate count or mandatory
STATUS entry is created by this rule.

## 1. Architect: select a valuable, warranted responsibility

### Orient using the smallest useful context

1. **Previous result first:** inspect the most recent relevant merged PR, its
   source/diff, observed CI and follow-up observations. Consult `STATUS.md`
   if the prior increment changed the strategic or capability state. Do not
   assume the next responsibility from the former PR's proposed backlog.
2. **Product and strategic compass**, proportionately:
   - `CONTEXT.md` ("Current product definition") and
     `docs/product-strategy.md` (accepted purpose and product value);
   - `docs/adr/0029-current-product-boundary.md` (scope, external authority)
     and `docs/adr/0031-persistent-semantic-stewardship.md` (selected
     long-term destination), plus any later applicable accepted decision;
   - `docs/persistent-semantic-stewardship-plan.md` section 12
     (value/claim criteria) and section 14 (illustrative construction order);
   - `STATUS.md` ("Current next step"), latest relevant Level-3 analysis,
     reconciliation and open owner boundaries.
3. **Targeted model and implementation reality:** where materially useful,
   inspect current code, its consumers and contracts, and selective Steward
   RECALL of `.sensemaking/knowledge/` and its original source references.
   Distinguish accepted commitments, observations, inferences, hypotheses,
   supersession and NOT_ASSESSED. Do not read the entire ontology or
   source-of-truth map when a bounded question is already answered.
4. **Authority:** establish the allowed engineering, merge and external
   actions independently of recommendations and retrieved knowledge.

Root `roadmap.md` and `goal.md` are historical, not operative construction
backlogs. Section 14 of the stewardship plan is an indicative trajectory, not
an obligation to implement the next numbered package.

**Product goals, non-goals and authority derive from sources accepted within
their actual scope:** owner-ratified intent, current product strategy, accepted
ADRs (including ADRs 0029 and 0031), and other appropriately authoritative
product records. Product-strategy.md and ADR 0029 were the sources for PR #599,
**not** an exclusive allowlist for subsequent records. Code and a semantic
index do not establish normative authority. Both existing goal records,
`goal:longterm-stewardship` and `goal:compounding-product-knowledge`,
remain as authored; do not silently merge, reclassify or add relationships.

### Explore and converge proportionately

- **Clear, local responsibility:** identify the concrete defect/contract or
  requested outcome and its source; proceed without manufacturing alternatives.
- **Material design uncertainty:** consider genuinely different approaches,
  simplifications, dependencies, and what would make the preferred design
  wrong. Compare qualitatively, not with a numeric score.
- **A genuine Level-3 reopening:** use the existing
  [Strategic Exploration Funnel](../../skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md).
  Do not run a full repository breadth/depth exercise for a known repair or
  an already-selected construction responsibility.

For a consequential choice, ask whether the approach creates user/agent
value, advances an accepted goal or protects a real contract, fits the
selected architecture, has a complete useful slice, preserves authority,
can be revised, and costs less (including omission cost) than worthwhile
alternatives. The best warranted action is not always the smallest patch,
largest feature, easiest test, or next item in a historical plan.

### Write the decision note in the PR

A **small repair** may use:

```text
Increment: Fix <observed problem / affected contract>.
Why: <source of the problem and how this repair serves product integrity>.
```

For **material selection**, expand only fields relevant to the decision:

```text
Increment: <intended useful outcome>
Serves: <accepted goal, contract, owner request or real user problem + source>
Alternatives: <material options and the reason for this choice, if any>
Slice: <in-scope behavior/files, affected consumers and exclusions>
Done when: <observable contract or bounded acceptance condition>
Verify: <source/diff checks, any suitable mechanical checks; CI may finish after merge>
Observe: <what genuine later use could reveal, when decision-relevant>
Authority: <authorized / specific reserved decision>
```

An increment may be legitimate maintenance or a repair even if it does not
correspond to a specific strategy section or plan package. Label it
accurately; do not invent a `Serves` citation to turn it into a roadmap
advance. Where alternatives are immaterial, state that briefly or omit the
field. Where the next action is owner-gated, do not fabricate approval.

## 2. Builder: construct and adapt without silent scope expansion

- Implement the selected useful slice in the active working context. Query
  Steward `context-for` or change impact where source-linked architecture,
  ownership, constraints or history would materially change the edit; no
  mandatory query for every file.
- **Update the decision note within the same PR** when implementation evidence
  warrants a better approach **and** goal, responsibility, authorized scope and
  safety boundaries remain intact. Architect and Builder can reason together;
  do not require a new PR or ceremony merely for a better local design.
- **Return to architectural selection** if a premise fails or the change
  materially alters the outcome, responsibility, relevant authority, or
  affected boundary. Escalate a genuinely reserved owner decision; park
  unrelated discoveries for future selection.
- Inspect current consumers/contracts and the diff. Follow the current
  `CLAUDE.md` construction exception: do not write or manually run local
  unit/synthetic evidence tests; disclose `NOT_RUN`. Do appropriate source,
  static, mechanical or real-path checks when applicable and distinguish
  those observations from unit tests or semantic proof.
- Use **one `claude/<topic>` branch per PR**. Put the decision note,
  implementation evidence, and verification limits in the PR description.

## 3. Close: integrate, reconcile and continue

- After a clean source/diff review and within granted authority, **merge the
  PR promptly without waiting for hosted CI or local unit/evidence tests**.
  Existing GitHub CI and repository protections remain in place. Never
  bypass required checks or knowingly integrate a substantive dangerous
  failure; report pending/failed/successful checks accurately. If CI later
  reveals a material regression, select a warranted repair responsibility.
- Confirm the PR actually merged and identify the new `main` commit.
  A merge is not proof of behavioral correctness, longitudinal improvement,
  release qualification, or repair closure.
- Let the PR and Git history retain **routine** decision notes, technical
  details and findings. Update `STATUS.md` **only when** the increment
  materially changes strategic state, current capabilities, meaningful
  limitations, or the next agent's decision context.
- Reconcile reviewed semantic knowledge only for consequential reusable
  facts, rationales, corrections, constraints, or contradictions. Do not
  generate records solely to increase counts or demonstrate compliance.
- The next Architect reads the relevant prior PR and actual results before
  choosing a new responsibility. When no further warranted, authorized work
  is apparent, stopping is valid.

## Guardrails

| Failure | Proportional guard |
| --- | --- |
| First visible defect substitutes for a strategic frontier | Compare product opportunities at a true Level-3 decision; do not promote routine maintenance |
| Artificially many candidates or scores | Explore only alternatives capable of changing the decision |
| A compulsory two-agent handoff | Architect and Builder are roles of the same active semantic controller |
| Silent redesign | Update the note within scope; reopen the choice if outcome or authority changes |
| Review ritual displaces construction | Two-sentence note for clear, reversible repairs |
| Every PR expands STATUS or ontology | Retain routine evidence in PR/Git; reconcile only consequential durable knowledge |
| Test or CI status becomes semantic proof | Report exact observed checks and their claim ceiling |
