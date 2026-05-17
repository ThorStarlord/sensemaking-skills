# Interview 2: Product & Design Operator

**Operator**: Beatriz Santos, Product Designer (3 years, led finance UI redesign)  
**Date**: 2026-05-17  
**Duration**: 48 minutes

---

## Summary

✅ **Brief Accuracy: 85%**  
🔴 **Gaps Identified: 5** (User mental models, Navigation patterns, Feature interaction, Inbox visibility, State indicator clarity)  
✅ **Recommends: Discovery-sprint** (Essential before next design iteration)  
✅ **Usefulness Rating: 5/5** (Domain spec would prevent design decisions that contradict business logic)

---

## Key Validations

**Brief Correctly Identified 20+ UI Sections**: Operator confirmed that dashboard has become "too dense" and operators are confused about "what action to take next." The brief's emphasis on clarifying action semantics directly addresses this.

**Navigation Patterns Are Implicit**: Operator noted that "the flow from Inbox → Transactions → Reconciliation → Close should be visual, but instead operators bounce between pages." This suggests the current information architecture doesn't match the workflow the brief identified.

**Critical Gaps**:
1. **User mental models** — Operators think in terms of "what do I do next?" but dashboard shows "what state are we in?" (mismatch between operator mental model and system mental model)
2. **Navigation patterns** — Current page structure (separate pages for Inbox, Transactions, Reconciliation, Reports) doesn't match the workflow progression
3. **Feature interaction semantics** — When a user clicks "Prepare Review Queue", what happens? Why is it separate from "Auto-Post"? These are not clearly distinguished
4. **Inbox triage workflow** — Operator must manually scan 50+ items to find the 8 that need attention; no filtering or prioritization
5. **State indicator clarity** — The "Pronto" badge needs clear visual hierarchy (hard blocker vs. suggestion)

---

## Direct Quotes

> "The dashboard is trying to show everything at once. We need to guide operators: 'Here's what you do right now. Here's what's blocked. Here's what's waiting on you.'"

> "Operators think 'I have 50 items in the inbox, I need to review 8 of them.' But the system shows all 50 mixed together. We need inbox filtering by state."

> "The transition from 'Prepare Review Queue' to 'Auto-Post' is unclear. Why are these separate actions? When should I do one vs. the other?"

> "New designers coming to this system have to reverse-engineer the workflow from the code. If we had a domain spec that showed the state machine, design decisions would be much faster."

> "The 'Pronto' indicator needs to be either a blocker (dark red = 'cannot close') or a suggestion (light yellow = 'recommendation'). Right now it's ambiguous."

---

## Recommendation for Discovery-Sprint

**Operator strongly supports discovery-sprint**: "Before we redesign the next version, we MUST have a domain spec. Otherwise, we'll make design decisions that contradict business logic and have to rework them later."

**Key design outputs discovery-sprint should inform**:
1. Workflow-based page structure (not feature-based)
2. Inbox triage UI (filtering, prioritization, state visibility)
3. State machine visualization (showing valid next actions, not just current state)
4. Error recovery guidance (what to do when something fails)
5. Role-based action visibility (hide actions the user can't take)
