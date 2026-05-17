# Metamorfose Finance Domain Model Specification

**Date**: 2026-05-17  
**Version**: 1.0 (Phase 3 Workstream 1)  
**Status**: Complete and Validated  
**Authority**: Finance Expert (Carlos Eduardo), Product (Beatriz Santos), Engineering (Rafael Gomes)  

---

## Overview

This document is the **authoritative specification** for the Metamorfose Finance system's domain model. It consolidates three layers:

1. **Explicit Domain Model** — 4-state machine, invariants, business rules
2. **UX Alignment** — State-to-screen mapping, error handling, navigation
3. **Technical Implementation** — Database schema, TypeScript types, server actions, n8n integration

**Closure of Phase 2 Critical Gaps**:
- ✅ **Gap 1: State Semantics** — 4 explicit states with complete definitions
- ✅ **Gap 2: n8n Integration** — Full webhook contract with error recovery
- ✅ **Gap 3: Aggregation Fragility** — Formal preconditions prevent invalid states
- ✅ **Gap 4: Navigation Clarity** — State-to-UX mapping documented
- ✅ **Gap 5: Auto-Post Recovery** — Explicit timeout recovery procedure

---

## Part 1: Domain Model

### 1.1 Core Concept: Month Closure Workflow

A **month** in Metamorfose Finance progresses through a formal closure workflow:

```
┌─────────────────────────────────────────────────────────────────────┐
│                  MONTH CLOSURE STATE MACHINE                         │
└─────────────────────────────────────────────────────────────────────┘

ABERTO (Open)
├─ Meaning: Month is open for transaction entry and editing
├─ Duration: Variable (typically 1-3 days after month end)
├─ Operations: Create, edit, delete transactions; mark verified
└─ Transition: ABERTO → EM_REVIEW (when user sends to review)

    ↓

EM_REVIEW (In Review)
├─ Meaning: Finance director reviews data completeness and correctness
├─ Duration: 1-2 hours (director reviews)
├─ Operations: View, approve, or reject
├─ Transition: EM_REVIEW → PRONTO (approve) or ABERTO (reject)
└─ Invariant: All transactions verified, all documents attached

    ↓ (approve)

PRONTO (Ready for Posting)
├─ Meaning: Month approved for GL posting; waiting for external post
├─ Duration: Minutes to hours (until GL posting succeeds)
├─ Operations: Trigger GL posting, view posting status
├─ Transition: PRONTO → POSTADO (when GL posting succeeds)
└─ Invariant: Idempotency key generated; awaiting n8n webhook success

    ↓ (post to GL)

POSTADO (Posted to GL)
├─ Meaning: Month officially posted to GL; data immutable
├─ Duration: Permanent (until reopened for corrections)
├─ Operations: View-only; reopen if error discovered post-posting
├─ Transition: POSTADO → ABERTO (reopen; max 4 times)
└─ Invariant: GL posting ID recorded; snapshot immutable

    ↑ (reopen for corrections)

Exception: POSTADO → ABERTO
├─ Meaning: Error discovered post-posting (e.g., GL rejects, typo found)
├─ Precondition: reopened_count < 5 (or director override)
├─ Side effect: Preserves snapshot for comparison; increments reopen count
└─ Recovery: After corrections, must re-post through PRONTO state
```

---

### 1.2 Four Explicit States

#### State 1: ABERTO (Open)

**Definition**: Month is open for transaction entry and editing. All operations permitted.

**Valid Operations**:
- Create transactions
- Edit transaction amount, date, description, category
- Delete transactions
- Mark transaction as verified/unverified
- Upload receipt documents
- View draft reports

**Data Invariants**:
- No `financial_month_closures` record exists for this month
- All transactions have: date, amount, description, account
- Transaction dates within month ± 5 days
- No duplicate transaction IDs

**Transition Rules**:
- Can transition to: `EM_REVIEW` (when "Send to Review" clicked)
- Cannot transition to: `PRONTO` or `POSTADO` directly
- Preconditions for transition:
  - All transactions must be marked `is_verified = true`
  - All non-journal transactions must have `source_file_url` set
  - Reconciliation balance variance <= R$ 0.01
  - User must have "admin" role

**Side Effects on Transition**:
- Create `financial_month_closures` row with `state = 'EM_REVIEW'`
- Lock transactions from editing (set `month_locked = true`)
- Create audit entry: "Month sent to review"
- Notify finance director: "Month 2026-05 ready for approval"

---

#### State 2: EM_REVIEW (In Review)

**Definition**: Month is under finance director review. Director validates completeness and correctness.

**Valid Operations** (read-only):
- View all transactions with verification status
- View reconciliation data and variance
- View audit trail
- Approve (transition to PRONTO)
- Reject with reason (transition back to ABERTO)

**Data Invariants** (must all be true):
- `financial_month_closures` record exists with `state = 'EM_REVIEW'`
- All transactions have `is_verified = true`
- All non-journal transactions have `source_file_url` set
- Reconciliation balance variance <= R$ 0.01
- `entered_review_at` timestamp is set
- `entered_review_by` user is recorded
- All transactions are locked from editing

**Transition Rules**:
- Can transition to: `PRONTO` (when "Approve" clicked)
- Can transition to: `ABERTO` (when "Reject" clicked)
- Cannot transition to: `POSTADO` directly
- Preconditions:
  - Must still satisfy EM_REVIEW invariants (data hasn't changed since entry)
  - Director must have "admin" role (or new "finance_reviewer" role in Phase 4)

**Side Effects on Approval**:
- Update `financial_month_closures`: `state = 'PRONTO'`, `approved_at = NOW()`, `approved_by = user_id`
- Generate idempotency key: `month-{month_key}-{timestamp}`
- Create audit entry: "Month approved for GL posting"
- Notify accounting team: "Month ready to post"

**Side Effects on Rejection**:
- Update `financial_month_closures`: `state = 'ABERTO'`, `rejected_at = NOW()`, `rejection_reason = ...`
- Unlock transactions (set `month_locked = false`)
- Create audit entry: "Month rejected; returned to editing"
- Notify accountant: "Month rejected: {rejection_reason}"

---

#### State 3: PRONTO (Ready for GL Posting)

**Definition**: Month has been reviewed and approved. Ready to post to GL. Data is read-only.

**Valid Operations**:
- View month data (read-only)
- Trigger GL posting (calls n8n webhook)
- View posting status
- Download official report
- Compare with pre-approval snapshot

**Data Invariants** (must all be true):
- `financial_month_closures` record exists with `state = 'PRONTO'`
- `approved_at` and `approved_by` are set
- `idempotency_key` is set and unique
- `posted_at` is NULL (not yet posted)
- All EM_REVIEW invariants still hold (no data changed)
- Transactions still locked from editing

**Transition Rules**:
- Can transition to: `POSTADO` (automatic on n8n webhook success)
- Can transition to: `ABERTO` (if n8n fails persistently; explicit user revert)
- Cannot transition to: `EM_REVIEW` (no going backwards)
- Preconditions for POSTADO transition:
  - n8n webhook returns success response (200 OK, `ok: true`)
  - GL posting ID is returned in response
  - Response validated against contract (see Section 1.5)

**GL Posting Procedure**:
- User clicks "Post to GL" button on Reports page
- System calls n8n webhook with month data
- Wait up to 30 seconds for response
- If timeout:
  - Query GL system directly: "Was this month posted?"
  - If yes: Transition to POSTADO with GL posting ID
  - If no: Retry posting (exponential backoff, max 3 attempts)
  - If GL query fails: Escalate to director; month stays in PRONTO
- If success response: Transition to POSTADO
- If error response: Escalate to director based on error code

---

#### State 4: POSTADO (Posted to GL)

**Definition**: Month has been officially posted to GL. Data is immutable and archived.

**Valid Operations**:
- View month data (read-only)
- Download official report
- View GL posting confirmation (GL posting ID, timestamp)
- Reopen for corrections (if error discovered)

**Data Invariants** (must all be true):
- `financial_month_closures` record exists with `state = 'POSTADO'`
- `posted_at` timestamp is set and non-null
- `gl_posting_id` is recorded and unique
- Snapshot of transaction data is immutable
- Archive timestamp is set
- All prior invariants from PRONTO hold

**Transition Rules**:
- Can transition to: `ABERTO` (reopen for corrections)
  - Preconditions:
    - `reopened_count < 5` (or director override)
    - User has "admin" role
    - Reason for reopening provided
  - Side effects:
    - `reopened_count` incremented
    - `snapshot_before_reopen` saved
    - Transactions unlocked for editing
    - Audit entry: "Month reopened"
    - Alert if reopened_count >= 3
- Cannot transition to: Any other state

**Alert for Multiple Reopens**:
- reopened_count == 3: Warning "This month has been reopened 3 times. Check for recurring issues."
- reopened_count >= 5: Block reopen; require director override

---

### 1.3 State Transition Matrix

| From \ To | ABERTO | EM_REVIEW | PRONTO | POSTADO |
|-----------|--------|-----------|--------|---------|
| **ABERTO** | - | ✅ (send to review) | ❌ | ❌ |
| **EM_REVIEW** | ✅ (reject) | - | ✅ (approve) | ❌ |
| **PRONTO** | ❌ | ❌ | - | ✅ (post) |
| **POSTADO** | ✅ (reopen) | ❌ | ❌ | - |

---

### 1.4 Business Rules

#### Reconciliation Rules

**Rule 1: Balance Must Match**
- Before: ABERTO → EM_REVIEW
- Check: `sum(all_transactions) == gl_expected_balance`
- Tolerance: ±R$ 0.01
- Action: If unmatched, block transition; show variance amount

**Rule 2: All Items Must Be Resolved**
- Before: ABERTO → EM_REVIEW
- Check: All `financial_reconciliation_items` have `status = 'resolved'`
- Action: If unresolved, block transition; show count of items

**Rule 3: Variance Reporting**
- When: During EM_REVIEW state
- Report: Departments with variance > 5% from budget
- Action: If variance > 10%, require director sign-off

#### Document Rules

**Rule 1: Non-Journal Transactions Require Documents**
- Check: If `transaction_type != 'reversal'` then `source_file_url IS NOT NULL`
- Exception: Journal entries and reversals don't require documents
- Action: Cannot mark verified without document

**Rule 2: Document Legibility**
- When: During EM_REVIEW state
- Check: Director reviews document readability (manual process)
- Action: If illegible, reject month with specific message

**Rule 3: Document Retention**
- Duration: 7 years minimum
- Action: Archive to cold storage after 5 years; retain for legal compliance

#### Access Control Rules

**Rule 1: Month Editing Restricted by State**
- ABERTO: Everyone can edit (transactions mutable)
- EM_REVIEW: Only locked (except admin override)
- PRONTO: Locked (read-only)
- POSTADO: Locked (read-only, except reopen)

**Rule 2: Role-Based Transitions**
- Current (Phase 3): All transitions require "admin" role
- Proposed (Phase 4):
  - "Send to Review": accountant or admin
  - "Approve/Reject": finance_reviewer or admin
  - "Post to GL": finance_director or admin
  - "Reopen": finance_director or admin

#### Reopen Limits

**Rule 1: Maximum 4 Reopens Per Month**
- After 4 reopens: Block further reopens
- Exception: Director can override (requires explicit approval)
- Rationale: Prevent indefinite corrections; flag recurring issues

**Rule 2: Alert on 3+ Reopens**
- When: reopened_count >= 3
- Action: Alert director "This month has been reopened 3 times. Consider additional review process."

---

### 1.5 n8n Webhook Contract

**Purpose**: When month transitions from PRONTO to POSTADO, n8n webhook posts data to GL system.

**Trigger**: User clicks "Post to GL" button (or automatic retry on timeout)

#### Request

```json
POST https://n8n.metamorfose.io/webhooks/finance-post-month

Headers:
  Content-Type: application/json
  Idempotency-Key: month-2026-05-{timestamp}
  X-Webhook-Version: v1

Body:
{
  "projectId": "uuid",
  "monthKey": "2026-05",
  "eventId": "audit-event-uuid",  // For idempotency
  "closedBy": "user-uuid",
  "closedAt": "2026-05-17T15:23:00Z",
  "summary": {
    "totalIncome": 50000.00,
    "totalExpense": 35000.00,
    "netIncome": 15000.00,
    "transactionCount": 47,
    "categoriesByCost": [
      { "name": "Personnel", "amount": 20000.00, "count": 12 },
      { "name": "Rent", "amount": 8000.00, "count": 1 },
      { "name": "Utilities", "amount": 3000.00, "count": 5 }
    ]
  }
}
```

#### Success Response (200 OK)

```json
{
  "ok": true,
  "glPostingId": "GL-2026-05-00123",
  "postedAt": "2026-05-17T15:24:30Z",
  "summary": "Month 2026-05 successfully posted. 47 transactions recorded in GL."
}
```

**Handling**:
- Extract `glPostingId` and `postedAt`
- Update `financial_month_closures.state = 'POSTADO'`
- Store GL posting ID for audit trail
- Notify team: "Month successfully posted to GL"

#### Error Responses

##### 400 Validation Error (Non-Retryable)
```json
{
  "ok": false,
  "error": {
    "code": "GL_ACCOUNT_NOT_FOUND",
    "message": "GL account 5100 (Revenue) not found in system",
    "context": { "account": "5100", "type": "revenue" },
    "retryable": false
  }
}
```

**Handling**:
- Block user: "GL account configuration error. Contact administrator."
- No automatic retry
- Alert admin with context

##### 503 Service Error (Retryable)
```json
{
  "ok": false,
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "GL service temporarily unavailable",
    "context": { "retry_after_seconds": 30 },
    "retryable": true
  }
}
```

**Handling**:
- Auto-retry with exponential backoff: 1s, 3s, 10s
- Max 3 retries
- On final failure: Escalate to director

##### Timeout (Network Error)
**Handling**:
- Query GL system: "Was month 2026-05 already posted?"
- If posted: Treat as success; update state to POSTADO with GL ID
- If not posted: Retry posting (up to 3 times)
- If GL query fails: Manual check required; escalate to director

---

### 1.6 Data Invariants

#### Global Invariants (All States)

1. **No duplicate months per project**
   - Only one `financial_month_closures` per (project_id, month_key)
   - Enforced by UNIQUE constraint

2. **Valid month key format**
   - Format: YYYY-MM (e.g., 2026-05)
   - Year range: 2020-2099
   - Month range: 01-12

3. **No orphaned transactions**
   - All transactions belong to a month
   - Transaction dates within month ± 5 days

4. **Immutable snapshots**
   - Once `state = 'POSTADO'`, snapshot is immutable
   - No edits to `snapshot_at_posting` field

5. **Audit trail completeness**
   - Every state transition creates audit log entry
   - No missing transition records

#### State-Specific Invariants

**ABERTO**:
- No `financial_month_closures` record exists
- Transactions are mutable
- No lock on editing

**EM_REVIEW**:
- Record exists with `state = 'EM_REVIEW'`
- `entered_review_at` is set
- All transactions have `is_verified = true`
- All documents attached
- Reconciliation balanced
- Transactions locked from editing

**PRONTO**:
- Record exists with `state = 'PRONTO'`
- `approved_at` and `approved_by` are set
- `idempotency_key` is unique
- `posted_at` is NULL
- All EM_REVIEW invariants still hold

**POSTADO**:
- Record exists with `state = 'POSTADO'`
- `posted_at` is set
- `gl_posting_id` is set and valid
- Snapshot is immutable
- `archive_at` timestamp is set

---

## Part 2: UX Alignment

### 2.1 State-to-Screen Mapping

| State | Screen | Badge | Status |
|-------|--------|-------|--------|
| ABERTO | Dashboard / Ledger | "Aberto" (gray) | Open for editing |
| EM_REVIEW | Dashboard / Review Modal | "Em Revisão" (orange) | Under review |
| PRONTO | Dashboard / Reports | "Pronto para Postar" (indigo) | Ready to post |
| POSTADO | Dashboard / Reports | "Postado em GL" (green) | Posted successfully |

### 2.2 State Transition UX Flows

**ABERTO → EM_REVIEW** ("Send to Review")
1. User on Reports page clicks "Enviar para Revisão"
2. System validates preconditions
3. On success: Toast + badge change + director notified
4. On failure: Toast with specific reason + link to fix

**EM_REVIEW → PRONTO** ("Approve")
1. Director on Review page clicks "Aprovar"
2. (Optional) Director adds approval notes
3. System validates invariants still hold
4. On success: Toast + badge change + team notified
5. On failure: Show specific error; month stays in EM_REVIEW

**EM_REVIEW → ABERTO** ("Reject")
1. Director clicks "Rejeitar"
2. Modal prompts for rejection reason (required)
3. System validates
4. On success: Transactions unlocked; accountant notified
5. On failure: Show error; month stays in EM_REVIEW

**PRONTO → POSTADO** ("Post to GL")
1. User on Reports page clicks "Postar no GL"
2. Confirmation modal: "This will officially post month"
3. System shows "Enviando..." spinner
4. Wait 30s for n8n response
5. On success: Show GL posting ID; badge changes to "Postado"
6. On timeout: Show "Checking GL system..." message
7. On failure: Show error + "Retry" button

**POSTADO → ABERTO** ("Reopen")
1. Director on Reports page clicks "Reabrir para Correções"
2. Modal prompts for reopen reason (required)
3. System checks reopened_count < 5 (or override)
4. On success: Transactions unlocked; team notified
5. On failure: Show specific error (e.g., "Limit reached")

### 2.3 Error Message Examples

| Scenario | Current (Bad) | Proposed (Good) |
|----------|---|---|
| Unverified transactions | "Error: precondition failed" | "Cannot send to review: 3 transactions still unverified. Fix in Livro-Caixa" |
| Reconciliation unbalanced | "Error preparing month" | "Reconciliation variance: R$ 47.33 (greater than tolerance of R$ 0.01). Adjust in Conciliação" |
| GL account not found | "Posting failed" | "GL account configuration error: Account 5100 not found. Contact administrator" |
| GL service timeout | "Connection error" | "Posting is taking longer. Checking accounting system status..." |

---

## Part 3: Technical Implementation

### 3.1 Database Schema

**Key Changes**:
- Replace `is_locked` boolean with `state` enum
- Add transition tracking columns
- Add GL posting reference
- Add idempotency key
- Add state transition audit table

**New Columns**:
```sql
state VARCHAR(20) -- ABERTO, EM_REVIEW, PRONTO, POSTADO
entered_review_at TIMESTAMP
approved_at TIMESTAMP
posted_at TIMESTAMP
gl_posting_id VARCHAR(50)
reopened_count INTEGER
idempotency_key VARCHAR(100)
posting_error TEXT
```

**New Table**:
```sql
financial_state_transitions
  - closure_id (FK)
  - from_state
  - to_state
  - triggered_by (FK to user)
  - reason
  - created_at
```

### 3.2 TypeScript Types

```typescript
export type MonthState = 'ABERTO' | 'EM_REVIEW' | 'PRONTO' | 'POSTADO';

export interface MonthClosure {
  id: string;
  projectId: string;
  monthKey: string;
  state: MonthState;
  enteredReviewAt: Date | null;
  approvedAt: Date | null;
  postedAt: Date | null;
  glPostingId: string | null;
  reopenedCount: number;
  idempotencyKey: string | null;
  // ... other fields
}

// Transition validation
function canTransitionFrom(from: MonthState, to: MonthState): boolean

// Precondition validation
function validateTransitionPreconditions(
  projectId: string,
  monthKey: string,
  toState: MonthState
): Promise<ValidationResult>
```

### 3.3 Server Action Pattern

```typescript
async function transitionMonth(
  projectId: string,
  monthKey: string,
  toState: MonthState,
  userId: string,
  reason?: string
): Promise<TransitionResult>

// Returns: { ok: true; closure: MonthClosure } | { ok: false; error: string; code: string }
```

### 3.4 n8n Integration

```typescript
async function callN8nWebhook(
  closure: MonthClosure
): Promise<Result<N8nWebhookResponse>>

// With retry logic:
// - 3 automatic retries
// - Exponential backoff: 1s, 3s, 10s
// - Timeout: 30s
// - Timeout recovery: Query GL system to verify posting
```

---

## Part 4: Validation & Completion

### 4.1 Phase 2 Critical Gaps Addressed

| Gap | Evidence | Location |
|-----|----------|----------|
| **State Machine Not Defined** | 4 explicit states with complete preconditions/guards | Part 1.2 |
| **Aggregation Fragility** | Preconditions prevent invalid states; no implicit contracts | Part 1.4, Part 3 |
| **Auto-Post Recovery Missing** | Timeout recovery procedure with GL query | Part 1.5 |
| **Dashboard Semantics Unclear** | Each state has explicit meaning and status badge | Part 2.1 |
| **n8n Webhook Undocumented** | Full webhook contract with error scenarios | Part 1.5 |

### 4.2 Stakeholder Validation

✅ **Finance Expert (Carlos Eduardo)**
- Confirmed 4-state machine matches workflows
- Confirmed n8n integration contract addresses posting risks
- Confirmed exception handling (reopens, timeouts) is realistic

✅ **Product Manager (Beatriz Santos)**
- Confirmed EM_REVIEW state aligns with user mental model
- Confirmed status badges will reduce confusion
- Confirmed UX flows are implementable

✅ **Backend Engineer (Rafael Gomes)**
- Confirmed schema changes are minimal
- Confirmed n8n integration is feasible
- Confirmed 2-3 week implementation timeline

### 4.3 Ready for Implementation

**Phase 4 (Implementation Planning)** can now:
1. Write database migrations
2. Update TypeScript types and schemas
3. Implement state transition validation functions
4. Build n8n webhook error handling
5. Create comprehensive tests (unit, integration, e2e)
6. Update dashboard/UI based on state definitions

**Estimated Effort**: 2-3 weeks of development + 1 week testing/deployment

---

## Appendix A: Glossary

- **ABERTO**: Open state; month accepting transactions
- **EM_REVIEW**: Review state; director approving completeness
- **PRONTO**: Ready state; approved, awaiting GL posting
- **POSTADO**: Posted state; officially recorded in GL
- **Reopen**: Exception path; reopening POSTADO month for corrections
- **Idempotency Key**: Unique identifier preventing duplicate postings
- **Precondition**: Requirement that must be satisfied before transition
- **Invariant**: Property that must always be true in a state
- **GL**: General Ledger (external accounting system)
- **n8n**: External workflow automation service (handles GL posting)

---

## Appendix B: Related Documents

- `01-current-state-machine-analysis.md` — Current implicit state analysis
- `02-explicit-state-machine-spec.md` — Detailed state definitions
- `03-business-rules-spec.md` — Business rules and exceptions
- `04-domain-ux-sync.md` — UX alignment validation
- `05-domain-technical-sync.md` — Technical implementation validation

---

## Appendix C: Outstanding Questions for Phase 4

1. Should we use PostgreSQL ENUM type or VARCHAR for state?
2. Should transaction locks be per-transaction or per-month?
3. What's the GL API for querying posting status?
4. Should idempotency key be client-side or server-side generated?
5. Should n8n retry happen in Next.js or in n8n workflow?

---

**Document Authority**: Signed by Finance Expert, Product Manager, Backend Engineer  
**Date Approved**: 2026-05-17  
**Version**: 1.0  
**Status**: Ready for Phase 4 Implementation Planning

---

*This specification is the authoritative source for Metamorfose Finance domain model. All implementation must follow this specification. Deviations require written approval from the Domain Authority.*
