# Product Thesis / Strategy Revision Contract

**Status:** canonical conceptual contract for Level-4 strategy revision  
**Primary authority surface:** `docs/product-strategy.md`  
**Current product-boundary authority:** `docs/adr/0029-current-product-boundary.md`  
**Authority:** human owner for product mission, strategic intent, major product decisions, product-boundary expansion, and claim-ceiling expansion  
**Runtime status:** documentation contract only; no autonomous strategy-revision machinery is authorized

## 1. Purpose

This contract defines the slowest and broadest Sensemaking control loop:

> Is the current understanding of the product itself still the right strategic
> commitment?

Level 4 governs product-thesis commitments. It does not choose implementation
tasks directly and does not replace Level-3 Strategic Repository Evolution.

## 2. Product-thesis commitments

The current product thesis includes the commitments represented in
`docs/product-strategy.md`:

- product purpose;
- primary user and anti-persona;
- problem;
- job to be done;
- value proposition;
- product positioning and external boundary;
- strategic principles;
- strategic non-goals;
- success measures;
- strategic hypotheses and bets;
- evidence ceilings.

These commitments change more slowly than repository capability state.

```text
product thesis != current implementation
product thesis != strategic frontier
product thesis != roadmap
product thesis != Campaign mission
```

## 3. Level-4 loop

Canonical shape:

```text
CURRENT PRODUCT THESIS
      |
accumulated material evidence / owner direction
      |
identify thesis-level tension or contradiction
      |
is a thesis commitment now decision-changing?
      |
   no ---> preserve material tension when recurrence could matter
      |     and return control to Level 3
      |
     yes
      |
identify affected strategic commitment
      |
formulate bounded alternatives
      |
attribute recommendation / judgment
      |
reaffirm / reinterpret / revise / retire / supersede
      |
obtain owner ratification when required
      |
update canonical product strategy / authority record
      |
mandatory Level-3 reconciliation
      |
return control to Strategic Repository Evolution
```

The absence of new evidence is not a reason to revise strategy.

## 4. Level-4 activation triggers

Level 4 should activate only when a material product-thesis commitment becomes
decision-changing.

Typical triggers include:

```text
PRIMARY_USER_MISMATCH
PROBLEM_INVALIDATED_OR_MATERIALLY_CHANGED
JTBD_MISMATCH
VALUE_PROPOSITION_MISMATCH
PRODUCT_BOUNDARY_CONTRADICTION
SUCCESS_MEASURE_INVALID_OR_INADEQUATE
STRATEGIC_NON_GOAL_RECONSIDERATION
REPEATED_PRODUCT_ARCHITECTURE_CONFLICT
NEW_PRODUCT_CLASS_OR_CATEGORY
OWNER_CHANGES_STRATEGIC_INTENT
CLAIM_CEILING_EXPANSION_REQUIRED
```

These are explanatory categories, not a required runtime enum.

Ordinary capability gaps, implementation defects, architecture reconciliations,
and feature changes normally remain Level 3.

## 5. Thesis tension before thesis review

Not every product-level signal immediately warrants Level-4 activation. A weak
or ambiguous signal may matter only if it recurs across independent Level-3 or
Level-2 work.

A **Thesis Tension** is a durable, attributed observation that an existing
product-thesis commitment may be generating repeated friction or ambiguity, but
the evidence is not yet strong enough to make revision decision-changing.

A useful documentation-level record contains:

```text
THESIS TENSION
AFFECTED STRATEGY COMMITMENT
OBSERVED INCIDENTS / EVIDENCE
CURRENT INTERPRETATION
WHY LEVEL-4 REVIEW IS NOT YET REQUIRED
WHAT RECURRENCE / EVIDENCE WOULD TRIGGER REVIEW
ATTRIBUTED AUTHOR
```

This is not a runtime object, score, or automatic counter. It may live in
`STATUS.md`, a dated Level-3 audit, an ADR/review note, or another current
authority-linked record when recurrence itself could affect a future decision.

```text
thesis tension != thesis contradiction
thesis tension exists != thesis review required
one weak signal != automatic escalation
repeated weak signals may become material evidence
```

Do not preserve every minor disagreement as a tension. Preserve it only when a
fresh agent losing the recurrence would materially weaken later thesis review.

## 6. Escalation from Level 3

A Level-3 controller should escalate rather than rewrite strategy when the
current repository-level decision depends on changing a thesis commitment.

The escalation should preserve:

```text
THESIS_REVIEW_REQUIRED
AFFECTED_STRATEGY_COMMITMENT
CURRENT COMMITMENT
EVIDENCE / CONTRADICTION
RELATED THESIS TENSIONS, WHEN MATERIAL
WHY LEVEL 3 CANNOT RESOLVE IT
ALTERNATIVES
RECOMMENDED OPTION, IF ANY
AUTHORITY REQUIRED
DOWNSTREAM STATE LIKELY AFFECTED
```

A recommendation does not itself change strategy.

## 7. Active work while Level 4 is unresolved

When Level 3 declares thesis review required, it must identify which current
responsibilities/Campaigns depend materially on the challenged commitment.

```text
THESIS REVIEW REQUIRED
        |
identify dependency on affected commitment
        |
        +-- thesis-dependent strategic advancement
        |      -> suspend until Level-4 disposition + Level-3 reconciliation
        |
        +-- independently warranted bounded work
               -> may continue if still within authority and unaffected
```

This is a **dependency-sensitive hold**, not a global repository freeze.

A thesis-dependent Campaign may still preserve state, gather already-authorized
non-prejudicial evidence, or perform safe mechanical maintenance when those
actions do not assume the disputed strategic commitment. It must not silently
advance the strategic rationale as if review had already resolved.

```text
review pending != all work forbidden
review pending != old thesis safe to assume
```

## 8. Revision dispositions

Level-4 review should end in one explicit disposition.

### REAFFIRM

The current commitment remains authoritative after review.

Use when new evidence creates a legitimate question but does not warrant a
change.

### REINTERPRET

The commitment remains materially the same, but its meaning/scope needs
clarification.

Use when ambiguity, not strategic intent, is the problem.

### REVISE

The commitment changes while the product thesis remains recognizably continuous.

Examples: refine the primary user, narrow a value proposition, change a success
measure, or revise a strategic principle.

### RETIRE

The commitment is no longer current and has no successor commitment of the same
kind.

Retirement should preserve history and rationale rather than deleting evidence.

### SUPERSEDE

A new commitment replaces an earlier one.

Supersession should identify both the old and new authority surfaces or
statements and preserve the reason for replacement. Product Boundary
Reconciliation v1 is the current concrete example: ADR 0014 remains historical
while ADR 0029 carries the operative product boundary.

These dispositions describe semantic revision outcomes. They do not authorize a
new generic lifecycle type in runtime code.

## 9. Authority and ratification

The active agent may:

- detect thesis-level tension;
- gather and classify repository evidence;
- identify which strategic commitment is affected;
- formulate alternatives and consequences;
- recommend a disposition;
- draft a proposed product-strategy revision;
- identify downstream Level-3 state that requires reconciliation.

The active agent may not silently:

- replace the product mission;
- redefine the primary user as a major strategic change;
- expand the ratified external product boundary;
- grant new merge/release/publication authority;
- reverse a major strategic non-goal;
- raise public claim ceilings;
- turn a speculative product direction into current strategy.

When those decisions are owner-reserved, canonical strategy changes require
explicit owner ratification.

## 10. Revision record

A consequential strategy revision should preserve enough durable information to
reconstruct why the product thesis changed.

Minimum conceptual record:

```text
REVISION DATE / IDENTIFIER
AFFECTED COMMITMENT
PREVIOUS COMMITMENT
NEW COMMITMENT OR DISPOSITION
EVIDENCE BASIS
COUNTEREVIDENCE / LIMITS
ATTRIBUTED RECOMMENDATION
OWNER DECISION / RATIFICATION
EFFECTIVE STRATEGY VERSION OR STATE
DOWNSTREAM RECONCILIATION REQUIRED
```

This may live in Git history, an ADR, an owner-decision record, a dedicated
Level-4 review, or the strategy document itself. This contract does not require
a new strategy event store.

## 11. Product-strategy revision semantics

`docs/product-strategy.md` remains the current strategy authority. It should
make three things explicit:

1. it is the Level-4 authority surface;
2. major strategic changes follow this revision contract;
3. repository implementation state is reconciled through Level 3 rather than
   embedded as mutable operational detail in the product thesis.

Strategy should contain current commitments plus appropriate evidence ceilings.
Historical alternatives belong in version history, ADRs, or dated decision
records when retaining them inline would confuse current authority.

## 12. Mandatory downstream reconciliation

After every material Level-4 disposition, Level 3 must reassess rather than
blindly continue the previous frontier. Reconciliation occurs **before
thesis-dependent strategic work resumes**.

At minimum reconsider:

- current Strategic Frontier;
- current Strategic Decision to Support;
- current highest-leverage boundary;
- active repository-level responsibility;
- deferred and rejected directions;
- capability-state relevance;
- architecture assumptions tied to the reviewed commitment;
- open Campaigns whose mission depends on the reviewed commitment;
- public documentation and claim ceilings.

For each materially affected responsibility/Campaign/direction, use an
attributed semantic classification such as:

```text
STILL_RELEVANT
STALE
SUSPECT
CONTRADICTORY
SUPERSEDED
OWNER_DECISION_REQUIRED
```

Then explicitly decide whether to continue, revise, close, supersede, defer, or
seek owner authority.

```text
Level-4 disposition != automatic Level-3 work plan
Level-4 disposition -> Level-3 reassessment -> new/continued responsibility only if warranted
```

These classifications remain semantic judgments unless a narrower mechanical
rule is independently justified.

## 13. What Level 4 does not do

Level 4 does not directly:

- rank implementation tasks;
- choose a Skill;
- edit code as a consequence of a thesis decision;
- open or merge a PR automatically;
- generate Campaigns automatically;
- infer product-market truth from repository structure;
- treat experiments as mandatory before every strategy decision;
- replace owner judgment where authority is reserved.

A Level-4 decision supplies commitments. Level 3 determines what repository
evolution, if any, those commitments warrant.

## 14. Mechanical future boundary

Future tooling may validate representation facts such as:

- the current strategy file exists;
- referenced revision/ADR files resolve;
- declared version/date metadata is well formed;
- Level-3 state points at the current strategy authority;
- superseded current-strategy pointers are not simultaneously active.

It must not decide:

```text
whether a thesis tension is strategically material
whether the product thesis is correct
whether a user segment is strategically better
whether a non-goal should be reversed
whether evidence warrants strategy revision
which strategy alternative should be selected
which active Campaign depends semantically on a challenged commitment
```

No strategy validator or runtime engine is authorized merely by this contract.

## 15. Construction policy

The repository keeps durable Level-4 semantics in existing documentation/ADR
authority first. Further machinery should be added only when a concrete,
mechanically decidable integrity or reconstruction need appears.
