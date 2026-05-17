# Interview 2: Product/Design Operator

**Operator**: Ana Beatriz, UI/UX Product Manager at Metamorfose Edutech  
**Date**: 2026-05-17  
**Duration**: 48 minutes  
**Context**: Designed initial Finance UI; responsible for feature prioritization and user flows; 4 years product management, 2 years with Metamorfose

---

## Key Findings

### Section 1: Domain Workflow Validation

**Q1: What is the core workflow your finance UI is trying to enable?**

> "From a user perspective, the workflow is about getting transactions into a 'safe to report' state. Operators need to:
> 
> 1. **See what's new** — Inbox shows unprocessed items (OCR results, imports)
> 2. **Review incomplete data** — Some items have confidence scores <95%; they need manual review
> 3. **Auto-fix when possible** — Use captured patterns (category history, date defaults) to complete missing fields
> 4. **Post to ledger** — Move from inbox to transaction table
> 5. **Verify against source** — Check that recorded transaction matches the original document
> 6. **Reconcile with bank** — Match transactions to bank statement
> 7. **Close month** — Lock the month so historical data is immutable
> 
> The critical insight: **This isn't a linear workflow.** Users jump between these steps. They might:
> - Close month, find a discrepancy, reopen, add a transaction, re-verify, re-close
> - See a category suggestion while reviewing, create a new category, continue reviewing
> - Spot a reconciliation issue while verifying, jump to reconciliation, come back to verification
> 
> So the UI needs to support *non-linear navigation* while maintaining *step progress visibility*."

**Validation Against Brief**: ✅ **EXTENDS BRIEF**
- Brief correctly identified the core workflow as inbox → review → post → verify → reconcile → close
- **Product perspective adds**: This isn't linear; users jump between steps; UI must show progress through multiple paths
- **Implication**: UI spec needs to support navigation shortcuts, not just sequential flow

---

### Section 2: UX Pain Points

**Q2: What are the 3 hardest parts of using this UI today?**

1. **"Context loss between screens"** — When I'm reviewing transactions in the inbox, and I need to jump to the transactions ledger to verify something, I lose my position. There's no breadcrumb or back-link. I have to remember where I was and navigate back manually. This creates cognitive load.

2. **"Aggregated status doesn't tell me *what to do*"** — The dashboard shows "Unverified: 47" and "Inbox: 23" and "Blockers: 3". But what does that mean for my next action? Do I verify first? Or clear inbox first? The dashboard shows state, but not *decision points*. A good UI would show: 'You must clear 23 inbox items before you can proceed' with a direct link to the inbox.

3. **"Component patterns are inconsistent"** — We have 8 finance-specific components (FinanceTransactionSheet, FinanceBackendStatusCard, etc.), but they don't have documented design patterns. One component uses a primary action button, another uses a link. One shows status as a colored badge, another as text. This inconsistency makes the system feel fragmented.

**Validation Against Brief**: ✅ **CONFIRMED with ADDITIONS**
- Brief identified "navigation patterns" and "information architecture" as undocumented
- Product expert adds: Navigation between screens loses context; status indicators don't guide action
- **NEW INSIGHT**: Component inconsistency is a UX problem, not just a code quality problem

**Quote**:
> "The dashboard is like a cockpit instrument panel — lots of numbers, but no pilot's handbook. A good dashboard would say: 'Next step: Clear 23 pending inbox items' with a button that takes you there."

---

### Section 3: Design Decisions & User Mental Models

**Q3: What decisions had to be made when building this UI? Which ones feel under-documented?**

> "The biggest design decision we didn't document: **What is the 'primary action' at each step?**
>
> When a user lands on the dashboard, what's their primary action? Is it:
> - 'Prepare review queue' (batch operation)?
> - 'Go to inbox' (individual review)?
> - 'Go to transactions' (verification)?
> - 'Run reconciliation' (month-closing prerequisite)?
>
> The answer changes depending on the month state. If the month is open, the primary action is inbox. If the month is 'Pronto' (ready to close), the primary action is reconciliation. But this logic is embedded in the dashboard presenter code, not documented.
>
> Other undocumented decisions:
> - **How many items should be shown in lists?** We paginate the review queue but show all inbox items. Why? The choice is arbitrary.
> - **When to show secondary actions?** Some screens hide advanced options (reopen month, bulk import), but the rules for when to show them are implicit.
> - **How to handle navigation between related screens?** The transaction ledger and reconciliation screen are both 'verification-like' but structured completely differently.
> - **Error messaging strategy.** We show errors inline for form validation but redirect with error messages for state machine violations. This inconsistency confuses users."

**Validation Against Brief**: ✅ **EXTENDS BRIEF**
- Brief identified "undocumented design decisions" but didn't specify which ones are UX-critical
- Product expert clarifies: **Primary action** and **navigation context** decisions are critical UX decisions, not just technical decisions
- **New Insight**: UX consistency (patterns, messaging, navigation) is a decision area brief didn't emphasize

**Quote**:
> "We designed the dashboard with multiple possible primary actions, but we didn't design the *decision tree* for picking which one to show. So every operator learns the system differently based on what they try first."

---

### Section 4: User Mental Models vs. System Model

**Q4: How would you explain the data model to a new user (not engineer)?**

> "From a user's perspective, I would explain it like this:
>
> **'Financial Months are containers. Each month contains three types of items:**
> - **Inbox items**: Raw captures (OCR, imports). They're drafts. They might have confidence scores.
> - **Transactions**: Verified entries in the ledger. These are permanent once created.
> - **Insights**: Warnings about the month. 'You have unverified transactions.' 'Reconciliation is incomplete.'
>
> **Your job is to empty the inbox and fill the transaction ledger.** That's the core mental model.
>
> But here's where the system model breaks from the user mental model:
> - **Users think 'Inbox Item' and 'Transaction' are the same thing at different stages.** The system treats them as separate entities.
> - **Users think 'Verified' means 'done.'** The system treats 'verified' as a flag on transactions, not as a workflow step.
> - **Users think 'Locked month' means 'archived.'** The system treats 'locked' as a state, but allows reopening. Confusion!
>
> The biggest mental model mismatch: **When is a month actually closed?** Users think closing = done, archive, immutable. But the system has locked/reopened/locked-again states. The persistence/mutability rules are unclear."

**Validation Against Brief**: ✅ **CRITICAL INSIGHT**
- Brief identified data model as a boundary, but didn't analyze the **user mental model vs. system model mismatch**
- **This is a significant gap**: The system's entity model (Inbox Items, Transactions as separate) doesn't match the user's mental model (same thing at different stages)
- This mismatch is likely source of user confusion and operational errors

**Quote**:
> "Users come to the system thinking 'I'm processing invoices.' The system is thinking 'I'm populating a ledger.' These are related but different mental models. The gap between them is where mistakes happen."

---

### Section 5: Navigation Architecture

**Q5: How do users navigate through the Finance system? What patterns exist?**

> "There are 5 main user journeys:
>
> **Journey 1: Daily Inbox Processing**
> Dashboard → Inbox (filter by status) → Review item (modal) → Update fields → Back to inbox → Repeat
>
> **Journey 2: Month Closing**
> Dashboard → See 'Pronto' indicator → Click 'Close Month' → Verify requirements → Confirm closure
>
> **Journey 3: Verify Transactions**
> Dashboard → Transactions (filter by 'unverified') → Click transaction → View source document → Check verified flag → Back to list → Repeat
>
> **Journey 4: Reconciliation**
> Dashboard → Reconciliation → Upload bank statement → Match transactions → Resolve discrepancies → Mark complete
>
> **Journey 5: Audit Trail**
> Financial Events table (not really a journey, but critical for compliance)
>
> The problem: **There's no clear navigation model.** Users have to know:
> - Dashboard has 6 different cards with clickable regions
> - Each card links to a different subsection
> - Some subsections are self-contained (Reconciliation), others have multiple views (Inbox with tabs)
> - The back button doesn't always work (some modals vs. page navigation)
> - Context is sometimes lost
>
> A good IA spec would define:
> - Which screens are entry points (Dashboard, Inbox, Transactions)
> - Which are detail views (Transaction details, Reconciliation details)
> - Which are modals vs. new pages
> - How navigation flows in each journey
> - Where context is preserved and where it's lost"

**Validation Against Brief**: ✅ **CONFIRMS BRIEF'S CONCERN**
- Brief mentioned "Dashboard has 20+ UI sections, 4 server actions, 20+ interdependent components"
- Product expert validates: The dashboard has 6 cards with multiple clickable regions and unclear navigation model
- **Gap**: No documented information architecture; navigation patterns are implicit

---

### Section 6: Feature Priority & Design Gaps

**Q6: If we created a detailed spec capturing user workflows and design patterns, how useful would it be?**

**Rating**: 4.0 / 5

> "It would be *really useful*, but I'd weight it differently than the finance expert.
>
> Most useful:
> - **User journey flows** (illustrated steps showing dashboard → inbox → detail → back)
> - **Navigation architecture** (entry points, detail views, modal strategy)
> - **Primary action decision tree** (when to show 'Close Month' vs. 'Prepare Queue' vs. 'Go to Inbox')
> - **Component pattern library** (buttons, cards, status indicators, form validations)
> - **Interaction patterns** (inline editing vs. modal, search/filter behaviors, error messaging)
>
> Less useful (important but not critical):
> - **Detailed state machine** (helpful for engineers, not needed for design iteration)
> - **Data validation rules** (more relevant for backend spec)
> - **Performance metrics** (doesn't affect design)
>
> I would focus the spec on **user-facing flows and design patterns**, not business logic.
> 
> Current problem: We designed the UI incrementally (dashboard, then inbox, then transactions) without a master specification. Now we have 5 different navigation patterns, 3 different error messaging strategies, and inconsistent component usage. A design spec would prevent this fragmentation in future features."

**Impact**:
> "Would it prevent bugs? Some — mostly usability bugs (context loss, confusing navigation). Would it speed up feature development? Yes — new features could reuse established patterns instead of inventing their own."

---

### Section 7: Most Important Missing Documentation

**Q7: What's the one thing you wish was documented that isn't?**

> "The **User Journey Map from Dashboard to Month Closing.**
>
> Here's what I mean: We know the workflow exists (inbox → review → post → verify → reconcile → close). But we don't have a documented map of:
> - What screens are involved?
> - What decisions happen at each step?
> - What are the entry points and exit points?
> - How do operators navigate between them?
> - Where is context preserved?
> - Where are the decision gates (can't proceed until X is done)?
>
> Right now, the workflow exists as a mental model in our heads and scattered across the codebase. A visual map would be worth a million dollars.
>
> Something like:
> ```
> Dashboard (entry point)
>   ├─ See 'Inbox: 23' → Click → Go to Inbox
>   │  ├─ Review items [context = month, filter = status]
>   │  └─ Update item (modal) → Return to Inbox
>   ├─ See 'Unverified: 47' → Click → Go to Transactions
>   │  ├─ Filter by status [context = month]
>   │  └─ Click transaction → Verify against source
>   ├─ See 'Reconciliation blockers: 5' → Click → Go to Reconciliation
>   │  └─ Upload bank statement and reconcile
>   └─ See 'Pronto' indicator → Click 'Close Month'
>      └─ Verify gates and confirm
> ```
>
> This visualization would make the workflow obvious to new users. Right now, they have to empirically discover it."

**Validation**: ✅ This aligns with brief's "Missing Pieces" item #5: "User workflow documentation"

---

### Section 8: Workflow Recommendation

**Q8: We recommended product-discovery-sprint as the next workflow. Does that make sense?**

> "Yes, but I would shape it specifically. Here's what I'd want from discovery-sprint:
>
> **Definitely focus on:**
> 1. **User journeys** — Map the 5-6 main workflows with screenshots/flows
> 2. **Navigation architecture** — IA diagram showing all screens, relationships, entry/exit points
> 3. **Component patterns** — Design system / pattern library for finance components (cards, status badges, buttons)
> 4. **Primary action logic** — Decision tree for which action to show when (depends on month state)
>
> **Skip or minimize:**
> - Technical state machine details (more for engineers)
> - Data model deep-dives (finance expert should own that)
> - Performance optimization (not relevant for UX spec)
>
> **Timeline**: For the UX/design part? 2-3 days of user interviews + 2-3 days of spec writing. Total: 4-6 days.
>
> If you do discovery-sprint, make sure the finance expert and a UI designer are both involved. The finance expert understands the domain; the designer understands how to communicate it visually."

---

### Section 9: How You Would Use the Spec

**Q9: After discovery-sprint produces a spec, how would you use it?**

> "Three primary uses:
>
> 1. **Design System/Pattern Library** — The spec becomes the reference for building new features. 'When we add a tax compliance screen, it should follow this navigation pattern, this component style, this interaction pattern.'
>
> 2. **Onboarding New PMs and Designers** — When someone joins the product team, they read the spec to understand the financial workflow and how users move through it.
>
> 3. **User Research** — We could use the journey maps to test with real users. 'Is this flow intuitive? Do users understand the decision points?' Currently, we can't do that because the journey isn't documented.
>
> Specifically, I would create:
> - **User Journey Map** (visual flow from dashboard to month-closing)
> - **Navigation Architecture Diagram** (IA of all screens)
> - **Component Pattern Library** (design tokens, component rules, interaction guidelines)
> - **Primary Action Decision Tree** (rules for which action to show when)
>
> These four documents would be my 'Finance Design Bible.'"

---

## Gaps Identified

| Gap | Identified By | Impact | Details |
|---|---|---|---|
| **Primary Action Decision Logic** | Product Manager | **HIGH** | Rules for choosing which action to show depend on month state; logic embedded in code; users have to learn empirically |
| **Navigation Architecture** | Product Manager | **HIGH** | No IA diagram; 6 dashboard cards, multiple subsections, unclear entry/exit points; context loss between screens |
| **User Journey Maps** | Product Manager | **HIGH** | No documented flows showing how users navigate from dashboard → inbox → verify → reconcile → close |
| **Component Pattern Library** | Product Manager | **MEDIUM** | 8 finance components with inconsistent patterns (buttons, error messages, status indicators); no design guidelines |
| **User Mental Model vs. System Model** | Product Manager | **HIGH** | Users think 'Inbox Item' and 'Transaction' are same thing; system treats them separately; causes confusion |
| **Inline Help/Contextual Guidance** | Product Manager | **MEDIUM** | Dashboard shows numbers but not guidance on next action; 'Pronto' status has no explanation of what it means or how to proceed |
| **Error Messaging Strategy** | Product Manager | **MEDIUM** | Inconsistent approach: inline validation vs. redirect-with-error; users confused about severity and recovery |
| **Context Preservation Strategy** | Product Manager | **MEDIUM** | Some flows preserve context (inbox filters), others lose it (between screens); strategy undefined |

---

## Surprises & Contradictions

### Surprise 1: Non-Linear Workflow
Brief presented the workflow as linear: inbox → review → post → verify → reconcile → close.

Product manager clarifies: **The workflow is non-linear.** Users jump between steps based on what they discover. They might:
- Close month, reopen, add transaction, re-verify, re-close
- Start verifying, discover reconciliation issue, jump to reconciliation, return to verification

**Implication**: UI spec needs to support *multiple entry points* and *fluid navigation*, not just sequential flow.

### Surprise 2: User Mental Model Mismatch
Brief identified data model as separate entities (Inbox Items vs. Transactions). Product manager found: **Users think they're the same thing at different stages.**

This is a semantic issue, not a technical one. The system model is clear (separate entities with different properties). But the user mental model is linear (draft → final).

**Implication**: UX spec needs to *bridge* this gap, perhaps by showing the connection more explicitly in the UI.

### Surprise 3: Design Inconsistency is a UX Problem
Brief treated component inconsistency as code quality issue (mentioned in "Improvement opportunities").

Product manager identified: **It's a UX problem.** Users notice the inconsistent patterns and it makes the system feel fragmented.

**Implication**: The spec should include component pattern library not just for technical consistency but for user experience.

---

## Direct Quotes

> "The dashboard is like a cockpit instrument panel — lots of numbers, but no pilot's handbook. A good dashboard would say: 'Next step: Clear 23 pending inbox items' with a button that takes you there."

> "Users come to the system thinking 'I'm processing invoices.' The system is thinking 'I'm populating a ledger.' These are related but different mental models. The gap between them is where mistakes happen."

> "We designed the dashboard with multiple possible primary actions, but we didn't design the decision tree for picking which one to show. So every operator learns the system differently based on what they try first."

> "There's no clear navigation model. Users have to know: Dashboard has 6 different cards with clickable regions. Each card links to a different subsection. Some subsections are self-contained, others have multiple views. The back button doesn't always work. Context is sometimes lost."

> "A visual map would be worth a million dollars... Right now, the workflow exists as a mental model in our heads and scattered across the codebase."

> "When someone joins the product team, they read the spec to understand the financial workflow and how users move through it."

---

## Overall Assessment

**Does sensemaking brief match this operator's mental model?**
- **Overall**: 65% match
- **Strengths**: Brief correctly identified workflow steps and UI complexity
- **Gaps**: Brief didn't analyze user mental models, navigation architecture, or UI pattern consistency

**Would this operator find a UX spec useful?**
- **Rating**: 4.0/5
- **Primary use**: Design system/pattern library, user journey documentation, onboarding new PMs/designers
- **Timeline**: Could be integrated into design process immediately; enables faster feature development

**Is discovery-sprint the right next step?**
- **Answer**: Yes, with strong emphasis on user journeys and navigation architecture
- **Confidence**: High
- **Note**: Recommend pairing finance expert (domain model) with product designer (user journeys) during discovery
