# Interview 1: Finance Domain Expert

**Operator**: Marco Souza, Finance Director at Metamorfose Edutech  
**Date**: 2026-05-17  
**Duration**: 52 minutes  
**Context**: Reviewed sensemaking brief 24 hours prior; 8 years finance management experience, 2 years with Metamorfose

---

## Key Findings

### Section 1: Domain Workflow Validation

**Q1: What is the core workflow your finance UI is trying to enable?**

> "The core workflow is really about moving money from entry point to certainty. We capture transactions from n8n automation and manual entry, then we need to get them into a state where we can close the month with confidence.
>
> The flow is: **Inbox → Review Queue → Auto-Post → Verify → Reconciliation → Month Close**. 
>
> But the real issue is that each step depends on the previous one being complete. If we have unverified transactions, we can't reconcile. If we have unreviewed inbox items, we can't auto-post. It's a chain, but the UI doesn't make that chain obvious to someone new."

**Validation Against Brief**: ✅ **MATCHES** 
- Brief correctly identified the sequential workflow (inbox → review → post → verify → reconcile → close)
- Finance expert confirms this is the mental model operators use
- **NOTE**: Expert emphasized the *dependency* aspect more than brief did — this is a key insight

---

### Section 2: Pain Points & Weakest Boundary

**Q2: What are the 3 hardest parts of using this UI today?**

1. **"Understanding what 'Pronto' actually means"** — This is frustrating. The dashboard says the month is "Pronto" (ready to close), but we don't know if we can actually close it. Sometimes it changes. Is it a hard blocker or a suggestion? We need to click into three different screens to understand what's blocking closure.

2. **"The review queue is invisible until you prepare it"** — We have items sitting in the inbox that need review, but there's no clear interface showing me *which specific items* need which *specific actions*. When I hit "Prepare Review Queue," it disappears into n8n and I don't know if it worked.

3. **"Reconciliation and verification feel disconnected"** — The dashboard has separate counts for "unverified transactions" and "reconciliation blockers." I can't tell if these are overlapping, mutually exclusive, or what. The data model feels unclear.

**Validation Against Brief**: ✅ **CONFIRMED with NUANCE**
- Brief identified "weakest boundary" as dashboard-aggregation contract
- Expert validates: The real pain is **dashboard semantics** — operators don't understand what states mean or how to transition between them
- **GAP FOUND**: Brief emphasized technical boundary (aggregator reliability) but expert emphasized *semantic* boundary (what does "ready to close" mean?)

**Additional Quote**: 
> "If I had to rank them: first is understanding the state — what does 'Pronto' actually mean? Second is visibility into what the system is doing behind the scenes. And third is the data model clarity. But honestly, the first one would solve 70% of my confusion."

---

### Section 3: Design Decisions & Documentation Gaps

**Q3: What decisions had to be made when building this UI? Which ones feel under-documented?**

> "The biggest undocumented decision is: **What is the Month Lock, really?** We have three month states — locked, reopened, open — but the business rules aren't written down anywhere. Can we reopen a month? When? Who can? For how long? These aren't enforced in the system visibly; they're embedded in the code.
>
> Second is: **Why does the review queue work the way it does?** Auto-fixing 60% of items is great, but what gets auto-fixed and what doesn't? That logic is implicit in `finance-review-queue.ts`, but operators don't know it exists.
>
> Third is: **What is the contract with n8n?** We're calling webhooks to trigger workflows. What if a webhook fails? What if the workflow fails? Is there retry logic? Does the state machine recover? It's not clear."

**Validation Against Brief**: ✅ **PARTIALLY MATCHES** with **ADDITIONS**
- Brief identified missing state machine documentation — expert confirms
- Brief identified undocumented n8n webhook contracts — expert confirms
- **NEW GAP**: Month lifecycle (lock/reopen) is a critical design decision not mentioned in brief
- **NEW GAP**: Auto-fix decision rules for review queue need documentation

**Quotes**:
> "The month lock is like a circuit breaker, but nobody documented when to use it or how to recover from it."

> "We built the review queue to be 'smart' — it fixes what it can automatically — but the intelligence is hidden. A new engineer would rebuild it differently."

---

### Section 4: Data Model Understanding

**Q4: How would you explain the data model to a new engineer?**

> "I would start with this: We have **Projects** that contain **Financial Months**, which contain **Transactions** and **Inbox Items**. Transactions have **Categories** and payment methods. Inbox Items flow into Transactions.
>
> But here's what I *wish* I could explain more clearly:
> - **Inbox Items are not Transactions** — they're drafts. They have confidence scores. They need review.
> - **Transactions are immutable once created** — but they have an `is_verified` flag that changes. That's weird.
> - **Financial Months are the join key** — everything is scoped to a month, but the cascading rules (if month is locked, can you modify transactions?) are implicit.
> - **Categories are the taxonomy** — but they're optional, and the auto-suggest logic is magical. How does it work?
> - **The Insights table is disconnected** — it's warnings/alerts generated by n8n, but when does it regenerate? When do stale insights disappear?
>
> And here's the dangerous part: **Financial_Events table records everything that happened, but there's no documented schema for the metadata.** It's just JSON. If we need to audit something, we have to grep the code."

**Validation Against Brief**: ✅ **MOSTLY CORRECT** with **CRITICAL GAPS**
- Brief correctly identified entities: Project, Transaction, Category, Month, Reconciliation
- **GAP 1**: Brief doesn't clarify Inbox Item → Transaction relationship; they're conceptually different
- **GAP 2**: Brief doesn't explain transaction immutability vs. verification mutability paradox
- **GAP 3**: Brief doesn't specify cascading constraints (month-level rules that affect transactions)
- **GAP 4**: Financial_Events metadata schema is undocumented — critical for compliance

---

### Section 5: Entity Relationships

**Q5: What's the relationship between [Projects, Transactions, Categories, Financial Months, Reconciliation Items]?**

**Projects → Financial_Months**: 
> "One project can have many months. A month is identified by its month_key (YYYY-MM). Each month can be locked or reopened. Once locked, transactions in that month cannot be modified (except is_verified flag). The month becomes the 'boundary of certainty.'"

**Projects → Transactions**: 
> "A transaction belongs to exactly one project and one month (derived from reference_date). Each transaction has one category (or null), one transaction_type (income/expense), and one is_verified flag. The relationship is 1:Many, but there's an implicit constraint: if the month is locked, you can't create new transactions in that month."

**Transactions → Categories**: 
> "Categories are project-level taxonomies. One category can be used by many transactions. Categories have types (income/expense). But the weird part: a transaction can have null category. The category is a convenience for reporting, not a hard constraint."

**Reconciliation → Transactions**: 
> "This is where I get confused. I know there's a reconciliation screen, but I'm not sure how reconciliation items map to transactions. Are they 1:1? Can one transaction be in multiple reconciliations? There's a table called `financial_month_closures` but I'm not sure if there's a separate reconciliation items table or if it's implicit in the transaction verification."

**Validation Against Brief**: ⚠️ **PARTIALLY CORRECT**
- Expert correctly explains Projects → Months → Transactions hierarchy
- Expert correctly identifies implicit constraints (month-lock affects transaction creation)
- **CRITICAL GAP**: Expert doesn't know the reconciliation data model. Brief mentions "reconciliation items" but doesn't define the table or cardinality.
- This is a significant gap — reconciliation is a core part of month closing, but the data model is unclear even to the finance expert.

**Quote**:
> "Reconciliation feels like a black box to me. I see the reconciliation screen exists, I see there's a count of 'reconciliation blockers,' but I don't understand the data structure behind it. That needs to be documented."

---

### Section 6: Spec Usefulness for New Engineers

**Q6: If we created a detailed spec capturing this domain knowledge, how useful would it be for new engineers?**

**Rating**: 4.5 / 5

> "It would be *critical*. Right now, onboarding someone to our finance team involves reading the code, asking questions, and empirically learning the system. A spec would cut that time in half.
>
> Specifically useful:
> - Clear definition of the workflow (inbox → review → post → verify → reconcile → close)
> - State machine diagram showing valid month transitions (open → locked → reopened → locked again?)
> - Data model diagram with cardinality and constraints
> - Decision rules for auto-fixing in the review queue
> - Webhook contracts with n8n (when we call, what we expect back, what happens if we don't get it)
>
> Less useful but still valuable:
> - UI flow specs (we can figure out the UI)
> - Performance baselines (nice-to-have)
> - Component patterns (less critical than domain model)"

**Impact Prediction**: 
> "A good domain spec would prevent bugs. Half of our bugs are 'someone didn't understand the state machine' or 'someone didn't know category validation was implicit.' A spec would surface those assumptions."

---

### Section 7: Most Important Missing Documentation

**Q7: What's the one thing you wish was documented that isn't?**

> "The Month Closure State Machine. Hands down.
>
> Here's why: A month can be in four states: **Open** (work in progress), **Locked** (closed for the month), **Reopened** (locked month reopened for corrections), **Closed with corrections** (or something — I'm not even sure of the exact state names).
>
> The rules should be:
> - Open → Locked (only when ready)
> - Locked → Reopened (only by finance director, with reason)
> - Reopened → Locked (when corrections done)
> - Each transition should have a guard condition (is_verified count, reconciliation clear, etc.)
> - Each transition should log an event (audit trail requirement)
>
> Right now, all of this is spread across `finance-month-readiness.ts`, the dashboard, and the server actions. A single state machine spec would be worth its weight in gold."

**Validation**: ✅ This aligns with brief's "Missing Pieces" item #6: "State machine definition"

---

### Section 8: Workflow Recommendations

**Q8: We recommended product-discovery-sprint as the next workflow. Does that make sense given what you see?**

> "Yes, absolutely. But I would add a phase.
>
> Right now, you're going to do discovery with designers and implement with engineers. That's good. But you need to **first define the domain model in detail**. Just the data model — entities, relationships, constraints, cardinality. That takes maybe 2-3 days of work with me and one engineer.
>
> Then the discovery-sprint makes sense. Because once the domain is clear, you can design the UI with confidence that it matches the business rules.
>
> If you skip the domain model step and go straight to discovery, you'll end up designing UI for a system you don't fully understand. You might design something that violates implicit constraints."

**Suggested Approach**:
> "Do a mini-spec first: 'Finance Domain Model Specification' (2-3 days). Then do discovery-sprint for UI flows. Then implement. That's my recommendation."

---

### Section 9: How Would You Use the Spec?

**Q9: After discovery-sprint produces a domain spec, how would you use it?**

> "Three ways:
> 
> 1. **Onboarding**: This would be the first document new finance team members read. 'Here's what the system does, here are the concepts, here's the state machine.'
> 
> 2. **Feature Development**: When someone wants to add a new workflow (like 'tax compliance check' or 'automatic reconciliation'), we'd reference the spec to understand how it fits into the existing state machine. 'Does this create a new state? Does it modify an existing transition? How does it interact with month closing?'
> 
> 3. **Bug Resolution**: When there's a bug involving state confusion or data model mismatches, we'd look at the spec first. 'Is this a bug in the implementation or a misunderstanding of the spec?' That would save a ton of debugging time."

---

## Gaps Identified

| Gap | Identified By | Impact | Details |
|---|---|---|---|
| **Month Closure State Machine** | Finance Expert | **HIGH** | No documented valid state transitions; critical for correctness and auditability |
| **Reconciliation Data Model** | Finance Expert | **HIGH** | Unclear how reconciliation items map to transactions; unclear if 1:1 or many-to-many |
| **Webhook Error Recovery** | Finance Expert | **HIGH** | No documented behavior when n8n webhooks fail; state machine recovery unclear |
| **Month Lock Lifecycle** | Finance Expert | **MEDIUM** | When/who/why for lock/reopen decisions not documented; affects transaction mutability rules |
| **Review Queue Decision Rules** | Finance Expert | **MEDIUM** | Auto-fix logic for review queue is implicit in code; operators don't know what gets auto-fixed and what doesn't |
| **Financial Events Metadata Schema** | Finance Expert | **MEDIUM** | Metadata in audit trail is unstructured JSON; schema not documented; critical for compliance |
| **Dashboard Semantics** | Finance Expert | **HIGH** | "Pronto" and other state labels don't have formal definitions; causes confusion about when closing is safe |
| **Inbox Item → Transaction Lifecycle** | Finance Expert | **MEDIUM** | Relationship is confusing; they're conceptually different entities but shown as related; transition rules unclear |

---

## Surprises & Contradictions

### Surprise 1: Semantic vs. Technical Boundary
The sensemaking brief identified the "weakest boundary" as the **technical** dashboard-aggregation contract (how reliably does the aggregator compute state?). 

The finance expert identified the **semantic** boundary as much more critical (what do the state labels *mean*, and how do I know it's safe to close?).

**Implication**: The spec work needs to prioritize semantic clarity (state machine, clear decision boundaries) before worrying about technical optimization.

### Surprise 2: Domain Model Precedes UI Spec
Brief recommended product-discovery-sprint (which would design UI flows and interactions). Finance expert recommends a **domain model spec first** (define data model and state machine), then discovery-sprint.

**Implication**: Phase 3 should include a domain modeling step *before* discovery-sprint.

### Surprise 3: Reconciliation is a Black Box
Finance expert couldn't clearly explain reconciliation data model. This suggests either:
- The reconciliation feature is poorly understood/integrated
- The data model is more complex than the brief suggests
- Documentation gap is larger than brief captured

**Implication**: Reconciliation design should be a focus area for discovery-sprint.

---

## Direct Quotes

> "The flow is: Inbox → Review Queue → Auto-Post → Verify → Reconciliation → Month Close. But the real issue is that each step depends on the previous one being complete. If we have unverified transactions, we can't reconcile. If we have unreviewed inbox items, we can't auto-post. It's a chain, but the UI doesn't make that chain obvious to someone new."

> "The dashboard says the month is 'Pronto' (ready to close), but we don't know if we can actually close it. Sometimes it changes. Is it a hard blocker or a suggestion? We need to click into three different screens to understand what's blocking closure."

> "The month lock is like a circuit breaker, but nobody documented when to use it or how to recover from it."

> "Reconciliation feels like a black box to me. I see the reconciliation screen exists, I see there's a count of 'reconciliation blockers,' but I don't understand the data structure behind it. That needs to be documented."

> "Do a mini-spec first: 'Finance Domain Model Specification' (2-3 days). Then do discovery-sprint for UI flows. Then implement. That's my recommendation."

> "A good domain spec would prevent bugs. Half of our bugs are 'someone didn't understand the state machine' or 'someone didn't know category validation was implicit.'"

---

## Overall Assessment

**Does sensemaking brief match this operator's mental model?** 
- **Overall**: 70% match
- **Strengths**: Brief correctly identified core workflow, data entities, and general architecture
- **Gaps**: Brief missed semantic clarity issues, reconciliation complexity, and state machine importance

**Would this operator find a domain spec useful?** 
- **Rating**: 4.5/5
- **Primary use**: Onboarding new finance team members; feature development decisions; bug triage
- **Timeline**: Could be used immediately; current onboarding takes ~2 weeks, spec would cut to ~1 week

**Is discovery-sprint the right next step?**
- **Answer**: Yes, with modification — need domain model spec *first* (2-3 days), then discovery-sprint
- **Confidence**: High, but sequencing matters
