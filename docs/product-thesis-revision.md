# Product Thesis / Strategy Revision Contract

**Status:** canonical conceptual contract for Level-4 strategy revision  
**Primary authority surface:** `docs/product-strategy.md`  
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
update canonical product strategy
      |
reconcile Level-3 strategic state
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

## 5. Escalation from Level 3

A Level-3 controller should escalate rather than rewrite strategy when the
current repository-level decision depends on changing a thesis commitment.

The escalation should preserve:

```text
THESIS_REVIEW_REQUIRED
AFFECTED_STRATEGY_COMMITMENT
CURRENT COMMITMENT
EVIDENCE / CONTRADICTION
WHY LEVEL 3 CANNOT RESOLVE IT
ALTERNATIVES
RECOMMENDED OPTION, IF ANY
AUTHORITY REQUIRED
DOWNSTREAM STATE LIKELY AFFECTED
```

A recommendation does not itself change strategy.

## 6. Revision dispositions

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
statements and preserve the reason for replacement.

These dispositions describe semantic revision outcomes. They do not authorize a
new generic lifecycle type in runtime code.

## 7. Authority and ratification

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

## 8. Revision record

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

This may initially live in Git history, an ADR, an owner-decision record, or the
strategy document itself. This contract does not require a new strategy event
store.

## 9. Product-strategy revision semantics

`docs/product-strategy.md` remains the current strategy authority. It should
make three things explicit:

1. it is the Level-4 authority surface;
2. major strategic changes follow this revision contract;
3. repository implementation state is reconciled through Level 3 rather than
   embedded as mutable operational detail in the product thesis.

Strategy should contain current commitments plus appropriate evidence ceilings.
Historical alternatives belong in version history, ADRs, or dated decision
records when retaining them inline would confuse current authority.

## 10. Downstream reconciliation

After a Level-4 change, Level 3 must reassess rather than blindly continue the
previous frontier.

At minimum reconsider:

- current Strategic Frontier;
- current highest-leverage boundary;
- active repository-level responsibility;
- deferred and rejected directions;
- capability-state relevance;
- architecture assumptions tied to the old thesis;
- open Campaigns whose mission depends on the changed commitment;
- public documentation and claim ceilings.

Possible Level-3 classifications include:

```text
STILL_RELEVANT
STALE
SUSPECT
CONTRADICTORY
SUPERSEDED
OWNER_DECISION_REQUIRED
```

These remain attributed semantic judgments unless a narrower mechanical rule is
explicitly ratified.

## 11. What Level 4 does not do

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

## 12. Mechanical future boundary

Future tooling may validate representation facts such as:

- the current strategy file exists;
- referenced revision/ADR files resolve;
- declared version/date metadata is well formed;
- Level-3 state points at the current strategy authority;
- superseded current-strategy pointers are not simultaneously active.

It must not decide:

```text
whether the product thesis is correct
whether a user segment is strategically better
whether a non-goal should be reversed
whether evidence warrants strategy revision
which strategy alternative should be selected
```

No strategy validator or runtime engine is authorized merely by this contract.

## 13. Construction policy

The current repository direction is to establish durable Level-4 semantics in
existing documentation first. Further machinery should be added only when a
concrete, mechanically decidable integrity or reconstruction need appears.
