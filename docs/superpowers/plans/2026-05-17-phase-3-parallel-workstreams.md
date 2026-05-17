# Phase 3: Parallel Workstreams — Domain, UX, Technical Specification

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to execute 3 parallel workstreams. Fresh subagent per workstream, review between key milestones.

**Goal:** Produce detailed domain specification (state machine, business rules, UX workflows, technical architecture) based on Phase 2 interview findings.

**Architecture:** 3 independent parallel workstreams (Domain Model, UX Discovery, Technical Foundation) that integrate and validate together. Each workstream produces specifications that inform the others. Daily alignment meetings ensure coherence.

**Timeline:** 12-20 days (2.5-4 weeks)  
**Effort:** ~80-120 person-hours distributed across 3 streams

**Success Criteria:**
- ✅ State machine specification with all valid transitions
- ✅ UX workflow diagrams with user journeys and mental models
- ✅ Technical architecture documentation with server patterns
- ✅ Cross-stream validation (specs are consistent and complete)
- ✅ Ready for Phase 4 (implementation planning)

---

## Phase 3 Overview

### 3 Parallel Workstreams

| Workstream | Lead | Focus | Duration | Dependencies |
|---|---|---|---|---|
| **1: Domain Model** | Finance Expert + Engineer | State machine, business rules, data contracts | 2-3 days core, 3-5 days refinement | None (starts immediately) |
| **2: UX Discovery** | Product Manager + Designer | User journeys, navigation, mental models | 4-6 days (longest) | Periodic input from Domain stream |
| **3: Technical Foundation** | Engineer | Server patterns, abstractions, infrastructure | 2-3 days core, 2-3 days refinement | Domain Model (for business rules) |

### Integration Points (Daily)

- **Morning standup** (15 min): Each workstream reports progress and blockers
- **Cross-stream sync** (30 min, 3x/week): Domain → UX, Domain → Technical, cross-validation
- **Integration session** (2 hours, end of each phase): Merge findings, validate consistency

### Timeline

```
Week 1:
├─ Days 1-2: Workstream kick-offs + parallel ramp-up
├─ Days 3-4: First cross-stream sync (Domain → UX/Technical)
└─ Days 5: Mid-week integration checkpoint

Week 2:
├─ Days 6-9: Core work (all 3 streams operating at full capacity)
├─ Day 10: End-of-week integration + validation
└─ Friday: Buffer/iteration day

Week 3:
├─ Days 11-13: Refinement based on integration feedback
├─ Days 14-15: Cross-stream validation (do specs agree?)
└─ Friday: Final integration + readiness for Phase 4

Buffer: 2-5 days for iteration, gaps, unforeseen complexity
```

---

## Workstream 1: Domain Model Specification

**Lead**: Finance Expert + Engineer  
**Duration**: 2-3 days core, 3-5 days refinement  
**Output**: `03-domain-model-spec.md` (state machine, business rules, data contracts)

### Context

Phase 2 identified **State Machine Specification** as the #1 critical gap. This workstream closes it by explicitly defining:
- Valid month states and all transitions
- Business rules for each state
- Data invariants and constraints
- n8n integration contract (webhooks, error handling)

---

### Task 1: Map Current State Machine

**Files:**
- Read: `metamorfose-platform/app/admin/finance` (entire codebase)
- Output: `artifacts/runs/2026-05-17-06-phase3-workstreams/workstream1-domain/01-current-state-machine-analysis.md`

- [ ] **Step 1: Audit codebase for state transitions**

Read all finance UI files. Document every place where month/transaction/invoice state changes.

Look for patterns like:
- If status === "A" then do X
- If status === "B" then do Y
- Cannot transition from "A" to "C" without going through "B"

Create a matrix:

```markdown
# Current State Machine (Implicit)

## Month States

| State | Transitions | Business Logic | Evidence |
|---|---|---|---|
| "Aberto" (Open) | → "Em Review" | User can create transactions | app/admin/finance/[...]/page.tsx:42 |
| "Em Review" | → "Pronto" or "Aberto" | Finance review mode | app/admin/finance/[...]/page.tsx:89 |
| "Pronto" | → "Postado" | After review, post to GL | ... |
| ... | ... | ... | ... |
```

- [ ] **Step 2: Identify implicit business rules**

For each state, document:
- What operations are allowed?
- What data must be valid?
- What triggers transition?
- What side effects occur?

Example:
```markdown
## State: "Pronto" (Ready to Post)

**Preconditions**:
- All transactions reconciled
- No missing receipt documents
- Balance must match GL reconciliation value

**Operations allowed**:
- View month summary
- Trigger posting to GL
- Generate audit report

**Operations blocked**:
- Add new transactions
- Edit posted transactions
- Delete invoices

**Transitions**:
- → "Postado": Manual trigger (user clicks "Post")
- → "Aberto": If error found during review, user can revert
```

- [ ] **Step 3: Document n8n integration**

Current state: Webhook calls to n8n are undocumented (Phase 2 gap #2)

Create section:

```markdown
## n8n Integration Contract

### Webhook: POST /metamorfose/finance/post-month

**Precondition**: Month state = "Pronto"  
**Payload**:
```json
{
  "month_id": "...",
  "transactions": [...],
  "reconciliation_value": "...",
  "audit_trail": [...]
}
```

**Response contract**:
- Success (200): Returns GL posting ID
- Failure (400): Returns error code + message
- Timeout/Network failure: ??? (currently undocumented)

**Error handling**:
- What happens if webhook fails?
- Is retry automatic?
- Does month revert to "Em Review"?
- Who gets notified?
```

- [ ] **Step 4: Create explicit state diagram**

Using the matrix, create a visual state machine:

```
Aberto ←---→ Em Review → Pronto → Postado
  ↓                                    ↓
[Can add txns]               [immutable, archived]
[Can edit/delete]
```

With all transition rules and conditions.

- [ ] **Step 5: Commit analysis**

```bash
git add artifacts/runs/2026-05-17-06-phase3-workstreams/workstream1-domain/01-current-state-machine-analysis.md
git commit -m "docs: analyze current implicit state machine in Finance UI"
```

---

### Task 2: Define Explicit State Machine

**Output**: `02-explicit-state-machine-spec.md`

- [ ] **Step 1: Write formal state definition**

```markdown
# Explicit State Machine Specification

## States

### ABERTO (Open)
**Meaning**: Month is open for transaction entry and editing

**Valid operations**:
- Create transaction
- Edit transaction
- Delete transaction
- View month summary
- Generate draft reports

**Invalid operations**:
- Post to GL
- Send to review (if balance unmatched)
- Export final reports

**Data invariants**:
- All transactions must have: date, amount, account, description
- Month balance = sum of all transactions
- No duplicate transaction IDs

**Transition rules**:
- Can transition to: EM_REVIEW (if user clicks "Send to Review")
- Cannot transition to: POSTADO directly

**Side effects**: None

---

### EM_REVIEW (In Review)
**Meaning**: Month is under finance review, locked for edits

**Valid operations**:
- View all transactions
- View reconciliation data
- View audit trail
- Approve (transition to PRONTO)
- Reject (transition back to ABERTO with feedback)

**Invalid operations**:
- Create/edit/delete transactions
- Post to GL

**Data invariants**:
- All transactions must have receipt documents attached
- Reconciliation value must match GL expectation

**Transition rules**:
- Can transition to: PRONTO (if approved), ABERTO (if rejected)

**Side effects**:
- Lock month from editing
- Send notification to finance director
- Create audit log entry

---

### PRONTO (Ready)
**Meaning**: Month approved and ready to post to GL

**Valid operations**:
- View month data (read-only)
- Trigger posting
- View posting status

**Invalid operations**:
- Any edits (strictly immutable)

**Data invariants**:
- All prior invariants must hold
- No pending reconciliation issues

**Transition rules**:
- Can transition to: POSTADO (via n8n webhook success), ABERTO (if error found)

**Side effects**:
- Call n8n webhook with month data
- Create posting audit record

---

### POSTADO (Posted)
**Meaning**: Month posted to GL, archived and immutable

**Valid operations**:
- View data (read-only)
- Download audit report
- Access historical data

**Invalid operations**:
- Any modifications

**Data invariants**:
- Immutable snapshot of all transactions

**Transition rules**:
- No transitions (final state)

**Side effects**:
- Archive month data
- Generate GL posting confirmation
```

- [ ] **Step 2: Define state transition matrix**

```markdown
## State Transition Matrix

|From / To| ABERTO | EM_REVIEW | PRONTO | POSTADO |
|---|---|---|---|---|
| ABERTO | - | ✅ (send review) | ❌ | ❌ |
| EM_REVIEW | ✅ (reject) | - | ✅ (approve) | ❌ |
| PRONTO | ✅ (error) | ❌ | - | ✅ (post success) |
| POSTADO | ❌ | ❌ | ❌ | - |

**Rules**:
- All transitions require explicit user action or system event
- No implicit transitions
- All transitions logged in audit trail
- Transition failures must be recoverable
```

- [ ] **Step 3: Define n8n webhook contract (explicit)**

```markdown
## n8n Webhook Contract

### Endpoint
`POST https://n8n.metamorfose.io/webhooks/finance-post-month`

### Preconditions
- Month.state == "PRONTO"
- All reconciliation checks passed
- User has "finance_reviewer" role

### Request Payload
```json
{
  "month_id": "2026-05",
  "start_date": "2026-05-01",
  "end_date": "2026-05-31",
  "transactions": [
    {
      "id": "...",
      "date": "2026-05-15",
      "amount": 1234.56,
      "account_id": "...",
      "description": "...",
      "document_id": "..."
    }
  ],
  "reconciliation": {
    "expected_balance": 50000.00,
    "actual_balance": 50000.00,
    "variance": 0.00
  },
  "audit_trail": [
    {"timestamp": "...", "user": "...", "action": "...", "change": "..."}
  ],
  "idempotency_key": "month-2026-05-<timestamp>"
}
```

### Response Contract

**Success (200)**:
```json
{
  "status": "success",
  "gl_posting_id": "GL-2026-05-0001",
  "posting_timestamp": "2026-05-17T14:30:00Z",
  "gl_journal_entries": [...]
}
```

**Validation Error (400)**:
```json
{
  "status": "error",
  "code": "VALIDATION_FAILED",
  "message": "Transaction 12345 has invalid account",
  "details": {...}
}
```

**n8n System Error (503)**:
```json
{
  "status": "error",
  "code": "N8N_UNAVAILABLE",
  "retry_after": 300,
  "message": "n8n is temporarily unavailable"
}
```

### Error Handling

**Case: Webhook succeeds**
- Month transitions to POSTADO
- GL posting ID stored in month record
- Email notification sent to finance team
- Audit log records: "Month posted to GL successfully"

**Case: Webhook validation error (400)**
- Month remains in PRONTO
- Error message displayed to user
- User can fix issues and retry
- Audit log records: "Post attempt failed: [error]"
- Automatic retry: None (requires user action)

**Case: Webhook system error (503)**
- Month remains in PRONTO
- Automatic retry: Yes (exponential backoff, max 3 attempts)
- If all retries fail: Alert finance director
- Audit log records each attempt

**Case: Network timeout**
- Unknown state (unclear if posting succeeded)
- Safety: **Check GL directly before allowing user retry**
- Query: "Is this month's data already in GL?"
- If yes: Mark as POSTADO, don't retry
- If no: Retry or alert director

**Case: Idempotency key collision**
- Prevents duplicate postings
- If webhook receives same idempotency_key twice, returns same response
- Ensures safe retry without double-posting
```

- [ ] **Step 4: Define data invariants**

```markdown
## Data Invariants (Must Always Be True)

### Global Invariants
1. Every transaction has a unique ID
2. Every transaction belongs to exactly one month
3. Transaction date is within month's date range
4. Every transaction has valid account assignment
5. Every transaction has >= 1 supporting document (except journal entries)

### State-Specific Invariants

**ABERTO invariants**:
- All transactions are editable
- No audit immutability constraints

**EM_REVIEW invariants**:
- All transactions must have >= 1 document
- Reconciliation value must be calculated and non-null
- At least one audit entry exists

**PRONTO invariants**:
- Reconciliation variance <= 0.01 (tolerance for rounding)
- No transactions marked as "disputed"
- Budget forecast for period exists

**POSTADO invariants**:
- GL posting ID is non-null
- All data is read-only
- Archive timestamp is set
```

- [ ] **Step 5: Commit explicit spec**

```bash
git add artifacts/runs/2026-05-17-06-phase3-workstreams/workstream1-domain/02-explicit-state-machine-spec.md
git commit -m "docs: define explicit state machine and business rules

Closes critical gap #1 from Phase 2 interviews.
Specifies all states, transitions, data invariants, and n8n contract."
```

---

### Task 3: Define Business Rules and Constraints

**Output**: `03-business-rules-spec.md`

- [ ] **Step 1: Document month lifecycle rules**

```markdown
# Business Rules Specification

## Reconciliation Rules

**Rule 1**: A month in EM_REVIEW cannot transition to PRONTO without reconciliation
- **Check**: total(transactions) == expected_gl_balance
- **Tolerance**: ±0.01 (for rounding)
- **Enforcement**: Automated, UI blocks transition if unmatched

**Rule 2**: Reconciliation must happen before posting
- **Responsibility**: Finance reviewer
- **Timeline**: Usually same day as EM_REVIEW transition
- **Escalation**: If unmatched after 24h, alert director

## Receipt Rules

**Rule 1**: Non-journal transactions must have >= 1 receipt
- **Applies to**: Vendor invoices, employee expenses, transfers
- **Doesn't apply to**: Journal entries, reversals
- **Enforcement**: UI requires document upload before closing month

**Rule 2**: Receipts must be legible and contain date/amount
- **Validation**: Manual review during EM_REVIEW
- **Rejection**: Finance can reject receipt and return to ABERTO

## Budget Rules

**Rule 1**: Transactions cannot exceed department budget
- **Check**: transaction_amount + prior_transactions <= budget_limit
- **Enforcement**: Warning (not block) at post time
- **Escalation**: Alert director if variance > 5%

## Access Control Rules

**Rule 1**: Users can only view/edit months in ABERTO
- **Applies to**: Transaction creators, accountants
- **Applies not to**: Finance reviewers (can see all states)

**Rule 2**: Only finance reviewers can approve/reject
- **Role**: finance_reviewer role required
- **Audit**: All decisions logged with user ID and timestamp
```

- [ ] **Step 2: Document edge cases and exception handling**

```markdown
## Exception Handling

### Scenario: Month needs reversal after posting

**Situation**: Posted month has error discovered 1 week later

**Current behavior**: ???  
**Desired behavior**:
- Create "reversal" entry in same month
- Post reversal entry separately
- Original month stays POSTADO (immutable)
- Create new month for correction entries

**Implementation**: Not in scope for Phase 3, but document for Phase 4

### Scenario: User leaves month in EM_REVIEW for 2 weeks

**Situation**: Month stuck in review, blocking period close

**Current behavior**: ???  
**Desired behavior**:
- Send reminder email after 48h
- Escalate to director after 1 week
- Auto-timeout after 14 days (transition back to ABERTO)

**Implementation**: Procedural, not coded

### Scenario: n8n webhook fails repeatedly

**Situation**: Network issues prevent posting for 3 hours

**Current behavior**: ???  
**Desired behavior**:
- Auto-retry every 5 min (with exponential backoff)
- After 6 failed attempts, alert director with manual retry option
- Detailed error messages logged

**Implementation**: Add to n8n error handling spec
```

- [ ] **Step 3: Commit business rules**

```bash
git add artifacts/runs/2026-05-17-06-phase3-workstreams/workstream1-domain/03-business-rules-spec.md
git commit -m "docs: define business rules, constraints, and exception handling"
```

---

### Task 4: Integrate with UX and Technical Streams (Sync Point)

**Duration**: 2-3 hours (coordination meeting)

- [ ] **Step 1: Domain → UX handoff**

Share Domain Model spec with UX workstream.

UX must validate:
- State machine matches user expectations
- Transitions make sense from user perspective
- Error messages align with business rules

Document: `04-domain-uux-sync.md` — Any conflicts or clarifications

- [ ] **Step 2: Domain → Technical handoff**

Share Domain Model spec with Technical workstream.

Technical must validate:
- Data model in code matches business rules spec
- Current server implementations match state machine
- n8n contract can be implemented with current stack

Document: `05-domain-technical-sync.md` — Any conflicts or gaps

- [ ] **Step 3: Resolve conflicts**

If UX or Technical identify gaps:
- Schedule 30-min clarification call
- Document decision and reasoning
- Update Domain Model spec
- Communicate to other streams

- [ ] **Step 4: Commit sync findings**

```bash
git add artifacts/runs/2026-05-17-06-phase3-workstreams/workstream1-domain/04-domain-uux-sync.md
git add artifacts/runs/2026-05-17-06-phase3-workstreams/workstream1-domain/05-domain-technical-sync.md
git commit -m "docs: domain-UX-technical sync and conflict resolution"
```

---

### Task 5: Refine and Validate Domain Model

**Duration**: 3-5 days (based on feedback)

- [ ] **Step 1: Incorporate UX feedback**

UX stream identifies user-facing implications of state machine.

Example: "Users don't understand 'Pronto' — suggest 'Ready to Post'" 

Update domain model with clearer terminology.

- [ ] **Step 2: Incorporate Technical feedback**

Technical stream identifies implementation constraints.

Example: "Current server can't atomically transition state + call webhook"

Update domain model to work within technical constraints, or document refactoring needed.

- [ ] **Step 3: Final validation**

All 3 workstreams sign off that specs are consistent.

Success criteria:
- State machine is complete (no missing states/transitions)
- All data invariants are testable
- n8n contract is implementable
- UX mental models match domain semantics
- No conflicts between streams

- [ ] **Step 4: Create final Domain Model artifact**

Output: `artifacts/runs/2026-05-17-06-phase3-workstreams/workstream1-domain/DOMAIN-MODEL-SPEC.md`

Contents:
- Executive summary (1 page)
- Complete state machine with all transitions
- Business rules and constraints
- Data model and invariants
- n8n integration contract
- Exception handling procedures
- Sign-off from all 3 workstreams

- [ ] **Step 5: Commit final spec**

```bash
git add artifacts/runs/2026-05-17-06-phase3-workstreams/workstream1-domain/DOMAIN-MODEL-SPEC.md
git commit -m "docs: finalize Domain Model specification (all workstreams aligned)

Closes critical gaps #1, #2, #3 from Phase 2 interviews.
State machine, business rules, and n8n contract fully specified."
git push origin main
```

---

## Workstream 2: UX Discovery & User Journeys

**Lead**: Product Manager + Designer  
**Duration**: 4-6 days  
**Output**: `UX-JOURNEY-MAP.md` (user journeys, navigation, mental models)

### Overview

Phase 2 identified: "User mental models don't match system model. Users think Inbox Item → Transaction are same thing; system treats them as separate entities."

This workstream:
1. Maps actual user journeys (how users think about workflows)
2. Identifies gaps between user mental models and system model
3. Proposes UX improvements to align mental models
4. Documents navigation and information architecture

---

### Task 1: Map Current User Journeys

- [ ] **Step 1: Interview users**

Conduct 3-4 short interviews with actual finance users (accountants, finance reviewers, director).

Key questions:
- "Walk me through closing out a month"
- "How do you think about the relationship between an Inbox item and a Transaction?"
- "What confuses you in the current UI?"
- "What would make this easier?"

Document findings in: `01-user-interview-notes.md`

- [ ] **Step 2: Map actual user journeys**

Based on interviews, create journey maps:

```markdown
# User Journey: Close Out Month (Finance Accountant)

**Actor**: Finance Accountant  
**Goal**: Close out May, send to finance director for review

**Steps**:
1. Log in
2. Navigate to Finance → Months → May
3. (???) How do they see all transactions?
4. (???) How do they reconcile?
5. Click "Send to Review"
6. Wait for director feedback

**Pain points**:
- Step 3: No obvious way to list all transactions for the month
- User scrolls in Inbox looking for May items (mental model)
- Actually they should look in Month detail (system model)

**Mental model**:
- User thinks: "I'm looking at my Inbox items that belong to May"
- System reality: "Inbox and Transactions are separate; must reconcile both"
```

Create 3-4 complete journeys covering all user roles.

- [ ] **Step 3: Identify mental model gaps**

For each journey, document:
- What user expects to see/do
- What system actually shows/does
- Gap analysis (why mismatch?)
- UX improvement needed

Example:

```markdown
## Gap: Invoice ↔ Transaction Relationship

**User mental model**: 
"I uploaded an invoice to the Inbox. Now I need to create a Transaction from it. The Invoice and Transaction are the same thing."

**System reality**:
- Invoice: Document in Inbox (payment proof)
- Transaction: Accounting entry in month (GL posting)
- Relationship: 1 Invoice → 1+ Transactions (invoice can be split across accounts)

**Gap impact**: 
- User expects 1-to-1 mapping
- Causes confusion when 1 invoice = 2 transactions (split expense)
- User doesn't understand where to find related invoice for a transaction

**UX improvement**:
- Add "linked documents" panel in transaction detail
- Show which invoices this transaction is paid from
- Change terminology: "Source Document" not "Attachment"
```

- [ ] **Step 4: Create journey map document**

Output: `02-user-journey-maps.md`

Format:
- Overview of all user journeys
- Detailed journey maps (narrative + diagram)
- Mental model gaps identified
- Impact assessment (high/med/low priority)

- [ ] **Step 5: Commit journey maps**

```bash
git add artifacts/runs/2026-05-17-06-phase3-workstreams/workstream2-ux/01-user-interview-notes.md
git add artifacts/runs/2026-05-17-06-phase3-workstreams/workstream2-ux/02-user-journey-maps.md
git commit -m "docs: map user journeys and identify mental model gaps"
```

---

### Task 2: Design UX Improvements

- [ ] **Step 1: Propose navigation improvements**

Based on journey gaps, propose navigation changes:

```markdown
# UX Improvements: Navigation

## Current Navigation
Finance UI → Months → [Month Detail] → [Transactions Tab] → [Inbox Tab]

**Problem**: Users have to navigate deep to see month data

## Proposed Navigation
Finance UI → Months → [Month Overview] showing:
- Summary stats (total transactions, reconciliation status)
- 3 tabs: Inbox, Transactions, Details
- Quick actions: "Send to Review", "Post"

**Benefit**: All month info on one screen, tab-based navigation

## Change effort**: Low (CSS/layout changes)
```

- [ ] **Step 2: Propose terminology improvements**

Align terminology with user mental models:

```markdown
# Terminology Changes

## Current → Proposed

| Current | Proposed | Reasoning |
|---|---|---|
| "Inbox Item" | "Source Document" | Users think "this is a document to process" |
| "Transaction" | "Accounting Entry" | More precise, aligns with finance domain |
| "Month" | "Period" or "Accounting Period" | Finance terminology |
| "Postado" | "Posted to Ledger" | Users don't know what "Postado" means |
| "Aggregator" | "Reconciliation Engine" | More self-explanatory |
```

- [ ] **Step 3: Create information architecture spec**

Output: `03-information-architecture.md`

Content:
- Proposed page hierarchy
- Component layout for key pages (Month Overview, Transactions, etc.)
- Information grouping (what goes together?)
- Navigation model

---

### Task 3: UX ↔ Domain Sync

- [ ] **Step 1: Validate UX against Domain Model**

When Domain workstream finishes state machine spec, validate:
- Are state transitions clear in the UI?
- Do error states match user expectations?
- Does terminology align?

Document: `04-ux-domain-sync.md`

- [ ] **Step 2: Propose UI changes for state machine**

Example: When month is in "EM_REVIEW", disable transaction editing buttons in UI

```markdown
# UI Changes for State Machine

## Current: No state indicator
User can click "Edit" on any transaction, even if month is in EM_REVIEW

## Proposed: State-aware UI
- If month.state != "ABERTO": Disable "Edit Transaction" button
- Show badge: "Month in Review" (yellow)
- Show tooltip: "Transactions cannot be edited while in review. Contact finance director."
```

Output: `05-ux-domain-integration.md`

---

### Task 4: Finalize UX Specification

- [ ] **Step 1: Create wireframes/mockups** (if tools available)

Visual representation of proposed UX changes.

- [ ] **Step 2: Document all UX decisions**

Final output: `artifacts/runs/2026-05-17-06-phase3-workstreams/workstream2-ux/UX-DISCOVERY-SPEC.md`

Contents:
- User journeys and mental models
- Navigation and information architecture
- Terminology and labeling
- State machine UI implications
- Proposed UX improvements (prioritized)
- Wireframes/mockups
- Implementation notes for Phase 4

- [ ] **Step 3: Get sign-off from UX lead and Product**

Ensure team agrees this UX spec is implementable and solves real problems.

- [ ] **Step 4: Commit final UX spec**

```bash
git add artifacts/runs/2026-05-17-06-phase3-workstreams/workstream2-ux/UX-DISCOVERY-SPEC.md
git commit -m "docs: finalize UX discovery and information architecture

Identifies 5+ mental model gaps and proposes navigation/terminology improvements.
Aligns user journeys with domain state machine spec."
git push origin main
```

---

## Workstream 3: Technical Foundation

**Lead**: Engineer  
**Duration**: 2-3 days core, 2-3 days refinement  
**Output**: `TECHNICAL-ARCHITECTURE-SPEC.md` (server patterns, abstractions, infrastructure)

### Overview

Phase 2 identified: "Server action duplication is architectural debt. Pattern repeated 4+ times without shared abstraction."

This workstream:
1. Documents current server architecture and patterns
2. Identifies technical debt and refactoring opportunities
3. Proposes server abstractions and infrastructure improvements
4. Creates technical implementation roadmap for Phase 4

---

### Task 1: Audit Current Server Architecture

- [ ] **Step 1: Map server-side code structure**

Read: `/app/admin/finance` server code

Document:
- All server actions (functions that modify data)
- Current patterns (duplicated vs. shared)
- Infrastructure (database, external APIs, caching)
- Error handling and validation

Output: `01-server-architecture-audit.md`

Example:

```markdown
# Server Architecture Audit

## Server Actions

| Action | File | Lines | Purpose | Pattern |
|---|---|---|---|---|
| `createTransaction` | [...].ts:45 | 50 | Create new transaction | Custom logic |
| `updateTransaction` | [...].ts:120 | 45 | Edit transaction | Custom logic (duplicates create) |
| `deleteTransaction` | [...].ts:180 | 20 | Delete transaction | Custom logic |
| `createInvoice` | [...].ts:220 | 55 | Create invoice | Similar pattern to transaction |
| ... | ... | ... | ... | ... |

**Pattern observation**: 
- All `create*` actions follow similar pattern (validate, save, audit)
- Duplicated validation logic across 6 different create actions
- Could be abstracted into `createEntity<T>(...)` helper

## Database Patterns

**Current**: Direct Supabase calls
```typescript
const { data, error } = await supabase
  .from("transactions")
  .insert({ ... })
```

**Issues**:
- No validation layer
- No audit logging
- No transaction boundaries
- Duplicated error handling

**Proposed**: Add data access layer with:
- Input validation schema
- Automatic audit logging
- Database transaction support
- Centralized error handling

## Error Handling

**Current**: Inconsistent
- Some actions throw errors
- Some return error objects
- Some silently fail

**Needed**: Consistent error handling with:
- Typed error responses
- User-friendly error messages
- Detailed audit logs for debugging
```

- [ ] **Step 2: Identify server abstraction opportunities**

```markdown
# Abstraction Opportunities

## #1: Create/Update/Delete Pattern (HIGH PRIORITY)

**Current**: 
- 6 create actions (each with duplicate validation)
- 6 update actions (each with duplicate validation)
- 6 delete actions (inconsistent error handling)

**Duplication**: ~150 lines of duplicated validation

**Proposed abstraction**:
```typescript
// Define entity schema once
const transactionSchema = z.object({
  date: z.date(),
  amount: z.number().positive(),
  accountId: z.string(),
  description: z.string(),
  // ...
});

// Generic create action
async function createEntity<T>(
  table: string, 
  schema: ZodSchema, 
  data: unknown,
  userId: string
): Promise<Result<T>> {
  // Validate
  const validated = schema.parse(data);
  // Audit log
  logAudit("CREATE", table, validated, userId);
  // Save
  return await db.from(table).insert(validated);
}

// Usage
const result = await createEntity("transactions", transactionSchema, formData, userId);
```

**Benefit**: 
- Reduce code duplication (saves ~100 lines)
- Consistent error handling
- Automatic audit logging
- Testable abstraction

## #2: Validation Layer (MEDIUM PRIORITY)

**Current**: Validation scattered across 12+ server actions

**Proposed**: Centralized validation with Zod schemas

```typescript
// schemas/finance.ts
export const transactionSchema = z.object({
  date: z.date(),
  amount: z.number().positive(),
  accountId: z.string().uuid(),
  // ...
}).strict();

// In server action
const validated = transactionSchema.parse(data);
```

## #3: Audit Logging (MEDIUM PRIORITY)

**Current**: Audit logging is manual and inconsistent

**Proposed**: Automatic audit decorator

```typescript
@audit("Transaction created by {user}")
async function createTransaction(formData) {
  // Automatic: logs user, timestamp, change
}
```

---

### Task 2: Design Server Architecture Improvements

- [ ] **Step 1: Propose data access layer**

```markdown
# Data Access Layer

## Current problem
Server actions directly call Supabase, duplicating queries.

Example: `getTransactionsByMonth` appears in 3 different server actions.

## Proposed solution

```typescript
// lib/data-access/transactions.ts
export async function getTransactionsByMonth(
  monthId: string, 
  projectId: string
): Promise<Transaction[]> {
  return await supabase
    .from("transactions")
    .select("*")
    .eq("month_id", monthId)
    .eq("project_id", projectId)
    .order("date");
}

// Usage in server action
const transactions = await getTransactionsByMonth(monthId, projectId);
```

**Benefit**:
- Single source of truth for each query
- Easy to add caching later
- Testable in isolation
```

- [ ] **Step 2: Design validation layer**

Create reusable Zod schemas for all domain entities.

Output: `02-validation-schemas.md`

- [ ] **Step 3: Design error handling strategy**

```markdown
# Error Handling Strategy

## Current: Inconsistent
- Some actions return { error: string }
- Some throw exceptions
- Some return null on failure

## Proposed: Consistent Result type

```typescript
type Result<T> = 
  | { ok: true; data: T }
  | { ok: false; error: ErrorDetails };

type ErrorDetails = {
  code: string;         // "VALIDATION_ERROR", "NOT_FOUND", etc.
  message: string;      // User-friendly message
  context?: unknown;    // For debugging
};

// Usage
async function createTransaction(data: unknown): Promise<Result<Transaction>> {
  // Validate
  const valid = transactionSchema.safeParse(data);
  if (!valid.success) {
    return {
      ok: false,
      error: {
        code: "VALIDATION_ERROR",
        message: "Invalid transaction data",
        context: valid.error
      }
    };
  }
  
  // Create and return
  return { ok: true, data: newTransaction };
}
```

Output: `03-error-handling-strategy.md`

---

### Task 3: Technical ↔ Domain Sync

- [ ] **Step 1: Validate n8n integration**

When Domain workstream finishes n8n contract spec, validate:
- Can current server implement this contract?
- Do we need middleware/adapter?
- What error scenarios need handling?

Output: `04-technical-domain-sync.md`

Example:

```markdown
# n8n Integration Implementation Plan

## Domain spec requires:
- Webhook call with month data
- Idempotency key for retry safety
- Error handling for timeouts

## Current server can**:
- Call n8n webhook: ✅ Yes (via fetch)
- Generate idempotency key: ✅ Yes (uuid)
- Handle timeouts: ⚠️ Partially (no retry logic)

## Needed changes**:
- Add retry logic with exponential backoff
- Add webhook timeout handling
- Verify idempotency_key is unique constraint in DB
- Add webhook response validation
```

---

### Task 4: Finalize Technical Specification

- [ ] **Step 1: Create implementation roadmap**

Output: `artifacts/runs/2026-05-17-06-phase3-workstreams/workstream3-technical/TECHNICAL-ARCHITECTURE-SPEC.md`

Contents:
- Server architecture audit
- Abstraction opportunities and proposed solutions
- Data access layer design
- Validation layer design
- Error handling strategy
- n8n integration specification
- Refactoring roadmap (Phase 4)
- Implementation priority (what's critical vs. nice-to-have)

- [ ] **Step 2: Create code examples**

For each proposed abstraction, show before/after code:

```markdown
# Before (Current)
[50-line server action with duplicated validation]

# After (Proposed)
[15-line server action using shared abstraction]
```

- [ ] **Step 3: Get sign-off from engineering lead**

Ensure technical team agrees this roadmap is sound and implementable.

- [ ] **Step 4: Commit final technical spec**

```bash
git add artifacts/runs/2026-05-17-06-phase3-workstreams/workstream3-technical/TECHNICAL-ARCHITECTURE-SPEC.md
git commit -m "docs: finalize technical architecture specification

Proposes 3 major abstractions to eliminate 150+ lines of duplication:
- Create/Update/Delete pattern abstraction
- Centralized validation layer with Zod
- Automatic audit logging

Includes n8n integration contract and implementation roadmap for Phase 4."
git push origin main
```

---

## Phase 3 Integration & Finalization

**Duration**: 3-5 days (after all 3 workstreams complete)

### Task 5: Cross-Workstream Integration

- [ ] **Step 1: Merge all 3 specs into master specification**

Combine:
- Domain Model Spec
- UX Discovery Spec
- Technical Architecture Spec

Create: `artifacts/runs/2026-05-17-06-phase3-workstreams/MASTER-FINANCE-SPECIFICATION.md`

Structure:
- Executive summary
- Domain model (state machine, business rules)
- UX specification (journeys, navigation)
- Technical architecture (server patterns, data access)
- Cross-spec validation (no conflicts)
- Sign-off from all 3 workstreams

- [ ] **Step 2: Validate consistency**

Check:
- Domain states match UX workflows ✅
- Business rules are implementable with proposed server architecture ✅
- Error handling aligns across all 3 specs ✅
- Terminology is consistent ✅

Document any conflicts and resolutions in: `INTEGRATION-NOTES.md`

- [ ] **Step 3: Create Phase 4 handoff**

Output: `PHASE-4-IMPLEMENTATION-PLAN.md`

Content:
- What needs to be built (feature list derived from specs)
- Implementation priority (critical → nice-to-have)
- Estimated effort per feature
- Technical refactoring opportunities
- Risk areas to watch

- [ ] **Step 4: Commit Phase 3 completion**

```bash
git add artifacts/runs/2026-05-17-06-phase3-workstreams/MASTER-FINANCE-SPECIFICATION.md
git add artifacts/runs/2026-05-17-06-phase3-workstreams/INTEGRATION-NOTES.md
git add artifacts/runs/2026-05-17-06-phase3-workstreams/PHASE-4-IMPLEMENTATION-PLAN.md
git commit -m "docs: Phase 3 complete - integrated domain, UX, technical specifications

Master specification combines:
- Domain model (state machine, business rules, data contracts)
- UX discovery (user journeys, information architecture, mental models)
- Technical architecture (server patterns, abstractions, implementation roadmap)

All 3 workstreams aligned and validated.
Ready for Phase 4 (implementation planning and execution)."
git push origin main
```

---

## Success Criteria

**Workstream 1 (Domain)**:
- ✅ Explicit state machine with all states and transitions
- ✅ Complete n8n webhook contract with error handling
- ✅ Data invariants that are testable and enforceable
- ✅ Aligned with UX and Technical specs

**Workstream 2 (UX)**:
- ✅ User journeys documented for all major workflows
- ✅ Mental model gaps identified and UX improvements proposed
- ✅ Information architecture and navigation specified
- ✅ Terminology changes aligned with domain

**Workstream 3 (Technical)**:
- ✅ Server architecture audit complete
- ✅ 3+ major abstraction opportunities documented
- ✅ Data access and validation layer designs created
- ✅ n8n integration technically validated

**Integration**:
- ✅ All 3 specs are consistent (no conflicts)
- ✅ Master specification created and reviewed
- ✅ Phase 4 implementation plan ready
- ✅ All artifacts committed to main branch

---

## Timeline & Dependencies

```
Week 1:
├─ Day 1-2: All 3 workstreams kick off in parallel
├─ Day 3-4: First sync meetings (Domain → UX, Domain → Technical)
└─ Day 5: Buffer for conflict resolution

Week 2:
├─ Day 6-9: Core work continues; specs take shape
├─ Day 10: Mid-phase integration checkpoint
└─ Friday: Iteration on feedback

Week 3:
├─ Day 11-13: Refinement based on integration feedback
├─ Day 14-15: Cross-workstream validation
├─ Day 16: Final integration & Phase 4 handoff planning
└─ Buffer: 2-5 days for unforeseen gaps

Phase 3 Complete: Ready for Phase 4 implementation
```

---

## Execution Model

Use **superpowers:subagent-driven-development**:

1. **Dispatch Workstream 1 subagent** (Domain Model) — 2-3 days
2. **Dispatch Workstream 2 subagent** (UX Discovery) — 4-6 days (parallel)
3. **Dispatch Workstream 3 subagent** (Technical) — 2-3 days (parallel)
4. **Daily standup** (15 min) — Brief progress/blockers
5. **Cross-workstream syncs** (3x/week) — Alignment and conflict resolution
6. **Integration phase** (3-5 days) — Merge specs, validate, create Phase 4 plan

Each subagent works independently with clear deliverables and checkpoints.

---

## Questions Before Execution?

- Resource availability: Can you commit Domain Expert, Product Manager, Engineer for 2-3 weeks?
- Scope: Are there other gaps beyond the top 3 identified in Phase 2?
- Timeline: Is 12-20 days realistic given team availability?
- Success criteria: Are these measurable and agreed?
