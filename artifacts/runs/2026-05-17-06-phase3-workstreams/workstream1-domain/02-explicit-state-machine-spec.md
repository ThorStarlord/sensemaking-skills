# Explicit State Machine Specification

**Date**: 2026-05-17  
**Workstream**: Workstream 1 — Domain Model Specification  
**Status**: Complete  
**Closes Critical Gap #1**: State Machine Specification from Phase 2 interviews

---

## Executive Summary

This document defines the **formal, unambiguous state machine** for financial month closure in Metamorfose Finance.

**Core Principle**: A month progresses through exactly 4 states, each with explicit preconditions, operations, invariants, and transitions.

```
ABERTO (Open)
    ↓
EM_REVIEW (In Review)
    ↓ (approve) or ↗ (reject)
PRONTO (Ready) ↙ ABERTO
    ↓
POSTADO (Posted)
    
Exception path:
POSTADO →[reopen] ABERTO (for corrections)
```

---

## Formal State Definitions

### State 1: ABERTO (Open)

**Meaning**: Month is open for transaction entry and editing. All data is mutable.

**Valid Operations**:
- Create transaction
- Edit transaction amount, date, description, category
- Delete transaction
- Mark transaction as verified/unverified
- Add receipt documents
- View month summary
- Generate draft reports

**Invalid Operations**:
- Send month to review (until all transactions verified)
- Post to GL
- Export official report
- Lock month
- Access historical snapshots

**Data Invariants**:
- No `financial_month_closures` record exists for this month
- All transactions have: `reference_date`, `amount`, `account`, `description`
- No duplicate transaction IDs
- No transaction post-dated beyond month end + 5 days

**Transition Rules**:
- Can transition to: `EM_REVIEW` (when user clicks "Send to Review")
- Cannot transition to: `PRONTO` or `POSTADO` directly
- Back-transition: None (once left ABERTO, cannot return directly; must go through full cycle)

**Side Effects on Entry**:
- None

**Side Effects on Exit**:
- Lock transactions from further editing (until state exits `EM_REVIEW`)
- Create audit log entry: "Month sent to review"
- Notify finance director

---

### State 2: EM_REVIEW (In Review)

**Meaning**: Month is under finance review. Data is locked for editing. Finance director validates completeness and correctness.

**Valid Operations**:
- View all transactions (read-only)
- View reconciliation data
- View audit trail
- Approve (transition to `PRONTO`)
- Reject (transition back to `ABERTO`)
- Download reconciliation report

**Invalid Operations**:
- Create/edit/delete transactions
- Post to GL
- Export official report
- Edit transaction verification status

**Data Invariants** (must all be true):
- `financial_month_closures` record exists with state = "EM_REVIEW"
- All transactions must have `is_verified = true`
- All transactions must have receipt documents attached (if `transaction_type != 'reversal'`)
- Reconciliation variance <= 0.01 (balance check passed)
- At least one audit entry exists showing month entered review
- No transactions can be created/edited (DB constraint enforces this)

**Transition Rules**:
- Can transition to: `PRONTO` (user clicks "Approve")
- Can transition to: `ABERTO` (user clicks "Reject")
- Cannot transition to: `POSTADO`

**Side Effects on Entry**:
- Create `financial_month_closures` record with `state = "EM_REVIEW"`
- Set `entered_review_at` timestamp
- Lock all transactions from editing (set `month_locked = true`)
- Create audit entry: "Month entered review"
- Send notification to finance director with review summary

**Side Effects on Exit** (either direction):
- Audit entry recorded: "Month exited review" or "Month approved from review"
- Dashboard updated with new state

---

### State 3: PRONTO (Ready)

**Meaning**: Month has been reviewed and approved. Ready to post to GL. Data is read-only.

**Valid Operations**:
- View month data (read-only)
- Trigger GL posting (calls n8n webhook)
- View posting status/history
- Download official report
- View snapshot comparison (before/after reopen)

**Invalid Operations**:
- Any data modifications
- Create/edit/delete transactions
- Send back to review (already approved)
- Unlock transactions

**Data Invariants** (must all be true):
- `financial_month_closures` record exists with `state = "PRONTO"`
- `approved_at` timestamp is set and non-null
- `approved_by` user ID is recorded
- All preconditions from `EM_REVIEW` still hold (no data changed)
- No `posted_at` timestamp (not yet posted)
- Idempotency key generated and unique

**Transition Rules**:
- Can transition to: `POSTADO` (automatic on n8n webhook success)
- Can transition to: `ABERTO` (if n8n fails or user manually reverts due to error)
- Cannot transition to: `EM_REVIEW`

**Side Effects on Entry**:
- Update `financial_month_closures` record: `state = "PRONTO"`, `approved_at = NOW()`, `approved_by = user_id`
- Generate idempotency key: `month-{month_key}-{timestamp}`
- Create audit entry: "Month approved for posting by {user}"
- Send email notification to accounting team

**Side Effects on Exit** (transition to POSTADO):
- Call n8n webhook (documented in separate n8n contract section)
- If successful: transition to POSTADO
- If failed: audit entry "Posting failed"; stay in PRONTO until retry

---

### State 4: POSTADO (Posted)

**Meaning**: Month has been officially posted to GL. Data is immutable and archived.

**Valid Operations**:
- View month data (read-only)
- Download official report
- Download audit trail
- View GL posting confirmation (GL posting ID)
- Access historical data

**Invalid Operations**:
- Any modifications whatsoever
- Transitions to other states (except ABERTO for reopening)
- Edit snapshot
- Delete month

**Data Invariants** (must all be true):
- `financial_month_closures` record exists with `state = "POSTADO"`
- `posted_at` timestamp is set and non-null
- `gl_posting_id` is recorded and references external GL system
- Snapshot is immutable (no further edits)
- Archive timestamp is set
- All prior invariants from PRONTO hold

**Transition Rules**:
- Can transition to: `ABERTO` (user clicks "Reopen for Corrections")
  - CRITICAL: This bypasses EM_REVIEW and PRONTO states
  - Used when: Error discovered post-posting (e.g., GL rejects entry, typo found)
- Cannot transition to: PRONTO or EM_REVIEW directly

**Side Effects on Entry** (from PRONTO):
- Update `financial_month_closures`: `state = "POSTADO"`, `posted_at = NOW()`, `gl_posting_id = {id}`
- Save transaction snapshot in immutable field
- Archive month data
- Create audit entry: "Month posted to GL. GL posting ID: {id}"
- Send email confirmation to finance director with GL posting details
- Revalidate dashboard (month now shows as closed)

**Side Effects on Exit** (transition to ABERTO):
- Update `financial_month_closures`: `state = "ABERTO"`, `reopened_at = NOW()`, `reopened_count += 1`
- Unlock transactions for editing
- Create audit entry: "Month reopened for corrections"
- Preserve snapshot (for comparison)
- Send notification: "Month reopened. Remember to re-post after corrections"

**Exception Handling**:
- If `reopened_count >= 3`: Send alert to director "This month has been reopened 3+ times. Consider additional review process."
- If `reopened_count >= 5`: Block further reopens; require director override

---

## State Transition Matrix

| From / To | ABERTO | EM_REVIEW | PRONTO | POSTADO |
|---|---|---|---|---|
| **ABERTO** | - | ✅ (send review) | ❌ | ❌ |
| **EM_REVIEW** | ✅ (reject) | - | ✅ (approve) | ❌ |
| **PRONTO** | ❌ | ❌ | - | ✅ (post) |
| **POSTADO** | ✅ (reopen) | ❌ | ❌ | - |

### Transition Conditions & Guard Clauses

#### ABERTO → EM_REVIEW (Send to Review)

```
PRECONDITIONS:
  ✓ No financial_month_closures record exists for this month
  ✓ All transactions have is_verified = true
  ✓ All non-journal transactions have source_file_url set
  ✓ Reconciliation balance check: |actual - expected| <= 0.01
  ✓ User has "admin" role
  
OPERATION:
  INSERT INTO financial_month_closures (
    project_id, month_key, state="EM_REVIEW", 
    entered_review_at=NOW(), entered_review_by=user_id
  );
  UPDATE financial_transactions SET month_locked=true WHERE month_key=...;
  INSERT INTO finance_audit_log (...);
  NOTIFY finance_director(...);
  
FAILURE BEHAVIOR:
  • If any precondition fails: return error to UI
  • UI shows: "Cannot send to review: [specific reason]"
  • Month remains in ABERTO state
  • Suggest corrective action to user
```

#### EM_REVIEW → PRONTO (Approve)

```
PRECONDITIONS:
  ✓ financial_month_closures record exists with state="EM_REVIEW"
  ✓ User has "admin" role (or new "finance_reviewer" role)
  ✓ All EM_REVIEW invariants still hold
  ✓ Review notes (optional) provided
  
OPERATION:
  UPDATE financial_month_closures SET 
    state="PRONTO", 
    approved_at=NOW(), 
    approved_by=user_id,
    idempotency_key="month-{month_key}-{timestamp}"
  WHERE state="EM_REVIEW";
  INSERT INTO finance_audit_log (...);
  NOTIFY accounting_team(...);
  
FAILURE BEHAVIOR:
  • If review state not found: error "Month review not found"
  • If invariants violated: error with specific violation
  • Month remains in EM_REVIEW
```

#### EM_REVIEW → ABERTO (Reject)

```
PRECONDITIONS:
  ✓ financial_month_closures record exists with state="EM_REVIEW"
  ✓ User has "admin" role (or "finance_reviewer")
  ✓ Rejection reason provided (required)
  
OPERATION:
  UPDATE financial_month_closures SET state="ABERTO", 
    rejected_at=NOW(), 
    rejected_by=user_id,
    rejection_reason=...
  WHERE state="EM_REVIEW";
  UPDATE financial_transactions SET month_locked=false WHERE month_key=...;
  INSERT INTO finance_audit_log (...);
  NOTIFY transaction_creators(rejection_reason);
  
FAILURE BEHAVIOR:
  • If month not in review: error "Month is not under review"
  • Month reverts to ABERTO; users can edit again
```

#### PRONTO → POSTADO (Post to GL)

```
PRECONDITIONS:
  ✓ financial_month_closures record exists with state="PRONTO"
  ✓ Idempotency key exists (prevents duplicate posts)
  ✓ All PRONTO invariants still hold
  ✓ n8n service is reachable (or queue for retry)
  
OPERATION:
  POST https://n8n.metamorfose.io/webhooks/finance-post-month
    {
      month_id: "2026-05",
      idempotency_key: "month-2026-05-{timestamp}",
      transactions: [...],
      reconciliation: {...},
      audit_trail: [...]
    }
  
  WAIT FOR RESPONSE:
    • If 200 (success):
        UPDATE financial_month_closures SET 
          state="POSTADO", 
          posted_at=NOW(), 
          gl_posting_id={response.gl_posting_id}
        WHERE state="PRONTO";
    
    • If 400 (validation error):
        UPDATE financial_month_closures SET 
          posting_error={error details}
        WHERE state="PRONTO";  // Stay in PRONTO
        NOTIFY admin with error details;
        RETURN error to user: "Posting validation failed. Fix and retry."
    
    • If 503 (temp failure):
        QUEUE for retry (exponential backoff, max 3 attempts);
        NOTIFY admin after final failure;
        // Month stays in PRONTO; retry happens automatically
    
    • If timeout (network):
        UNKNOWN STATE: month might be posted externally
        QUERY GL system: "Is month 2026-05 already posted?"
        IF YES: transition to POSTADO, record GL posting ID
        IF NO: queue for retry
        NOTIFY admin: "Timeout posting month; investigating..."
  
FAILURE BEHAVIOR:
  • Transient error (503): Auto-retry with exponential backoff
  • Validation error (400): Block until user fixes and retries
  • Timeout: Manual check of GL; confirm before retry
  • Critical error: Escalate to director with detailed logs
```

#### POSTADO → ABERTO (Reopen)

```
PRECONDITIONS:
  ✓ financial_month_closures record exists with state="POSTADO"
  ✓ reopened_count < 5 (or override by director)
  ✓ User has "admin" role
  ✓ Reason for reopening provided
  
OPERATION:
  UPDATE financial_month_closures SET 
    state="ABERTO", 
    reopened_at=NOW(), 
    reopened_by=user_id,
    reopened_count = reopened_count + 1,
    reopened_reason=...
  WHERE state="POSTADO";
  UPDATE financial_transactions SET month_locked=false WHERE month_key=...;
  INSERT INTO finance_audit_log (...);
  SAVE snapshot_before_reopen (for comparison);
  NOTIFY team: "Month reopened. Remember to re-post changes.";
  
  IF reopened_count >= 3:
    ALERT director: "This month has been reopened 3 times. Check for recurring issues.";
  
FAILURE BEHAVIOR:
  • If not in POSTADO state: error
  • If reopened_count >= 5: blocked (requires director override)
```

---

## Data Invariants (Complete List)

### Global Invariants (All States)

1. **No duplicate months per project**
   - Only one `financial_month_closures` record per (project_id, month_key)
   - Enforced by database UNIQUE constraint

2. **Valid month key format**
   - `month_key` matches `YYYY-MM` format
   - Year between 2020-2099
   - Month between 01-12

3. **No orphaned transactions**
   - All transactions belong to a month
   - All transactions have `reference_date` within month range
   - No transactions post-dated beyond (month_end + 5 days)

4. **Audit trail immutable**
   - Finance audit logs are append-only
   - Cannot delete or edit audit entries
   - All state transitions logged

5. **Snapshot is immutable when state = POSTADO**
   - Snapshot data cannot be modified
   - Only set once at ABERTO → POSTADO transition
   - Used for read-only comparison if month reopened

### State-Specific Invariants

#### ABERTO State Invariants

```
✓ No financial_month_closures record exists
  OR record.state = "ABERTO"
✓ All transactions editable (no month-level lock)
✓ Transactions can be added/edited/deleted
✓ No snapshot (or snapshot is draft)
✓ No approval/posting timestamps set
✓ reopened_count = 0 (or null)
```

#### EM_REVIEW State Invariants

```
✓ financial_month_closures.state = "EM_REVIEW"
✓ entered_review_at is set (non-null)
✓ entered_review_by is set (user ID)
✓ All transactions: is_verified = true
✓ All non-journal transactions: source_file_url is set (non-null)
✓ Reconciliation check: |actual_balance - expected_balance| <= 0.01
✓ No transactions locked at DB level (but UI prevents editing)
✓ approved_at is NULL (not yet approved)
✓ posted_at is NULL (not yet posted)
✓ No snapshots (or draft snapshot only)
✓ Reopened_count = 0
```

#### PRONTO State Invariants

```
✓ financial_month_closures.state = "PRONTO"
✓ approved_at is set (non-null)
✓ approved_by is set (user ID)
✓ idempotency_key is set (unique, non-null)
✓ All ABERTO and EM_REVIEW invariants still hold
✓ Transactions are immutable (read-only)
✓ posted_at is NULL (not yet posted)
✓ No GL posting ID (not yet posted)
✓ snapshot is empty or draft
✓ reopened_count = 0
```

#### POSTADO State Invariants

```
✓ financial_month_closures.state = "POSTADO"
✓ posted_at is set (non-null)
✓ gl_posting_id is set (references external GL)
✓ Snapshot contains complete transaction data at posting time
✓ snapshot is immutable (read-only)
✓ All prior invariants from PRONTO hold
✓ Transactions are immutable (read-only)
✓ archive_timestamp is set
✓ closed_at is set (for compatibility)
```

---

## n8n Webhook Integration Contract

### Endpoint Specification

**URL**: `POST https://n8n.metamorfose.io/webhooks/finance-post-month`

**Preconditions**:
- Month state = PRONTO
- All reconciliation checks passed
- All transactions verified
- Idempotency key is unique

### Request Payload

```json
{
  "month_id": "2026-05",
  "month_key": "2026-05",
  "start_date": "2026-05-01",
  "end_date": "2026-05-31",
  "idempotency_key": "month-2026-05-1716003600",
  
  "transactions": [
    {
      "id": "txn-uuid-1",
      "date": "2026-05-15",
      "amount": 1234.56,
      "type": "income|expense|reversal",
      "account_id": "acct-uuid",
      "description": "Invoice payment",
      "category": "Sales Revenue",
      "reference": "INV-2026-001",
      "document_url": "https://..."
    }
  ],
  
  "reconciliation": {
    "total_transactions": 42,
    "total_income": 150000.00,
    "total_expense": 95000.00,
    "net_balance": 55000.00,
    "expected_balance": 55000.00,
    "variance": 0.00,
    "variance_tolerance": 0.01,
    "reconciliation_status": "BALANCED"
  },
  
  "audit_trail": [
    {
      "timestamp": "2026-05-16T10:30:00Z",
      "user_id": "user-uuid",
      "action": "month_created",
      "change": "Month 2026-05 created"
    },
    {
      "timestamp": "2026-05-17T14:00:00Z",
      "user_id": "user-uuid",
      "action": "month_sent_to_review",
      "change": "Sent to review"
    }
  ],
  
  "metadata": {
    "project_id": "project-uuid",
    "project_name": "Metamorfose",
    "posted_by_user_id": "user-uuid",
    "posted_by_user_email": "user@metamorfose.io"
  }
}
```

### Response Contract (Success - 200)

```json
{
  "status": "success",
  "gl_posting_id": "GL-2026-05-0001",
  "posting_timestamp": "2026-05-17T15:45:00Z",
  "gl_system": "SAP|Oracle|QuickBooks",
  
  "journal_entries": [
    {
      "entry_id": "JE-001",
      "account": "1000-Cash",
      "debit": 55000.00,
      "credit": 0.00
    }
  ],
  
  "warnings": [
    "Account 2100 has high balance; review for accuracy"
  ]
}
```

### Response Contract (Validation Error - 400)

```json
{
  "status": "error",
  "error_code": "VALIDATION_FAILED",
  "error_message": "Transaction 'txn-uuid-5' has invalid account assignment",
  
  "details": {
    "failed_transaction_id": "txn-uuid-5",
    "field": "account_id",
    "issue": "Account not found in GL chart of accounts",
    "suggestion": "Use account 2000 instead of 9999"
  },
  
  "timestamp": "2026-05-17T15:45:00Z"
}
```

### Response Contract (Temporary Error - 503)

```json
{
  "status": "error",
  "error_code": "N8N_UNAVAILABLE",
  "error_message": "n8n service is temporarily unavailable",
  
  "retry_after": 300,
  "max_retries": 3,
  "retry_strategy": "exponential_backoff",
  
  "timestamp": "2026-05-17T15:45:00Z"
}
```

### Error Handling Specifications

#### Case 1: Webhook Succeeds (HTTP 200)

**Server behavior**:
```
1. Receive response with gl_posting_id
2. Verify idempotency_key (prevent duplicate posts)
3. Update financial_month_closures:
   - state = "POSTADO"
   - gl_posting_id = response.gl_posting_id
   - posted_at = NOW()
4. Create audit entry: "Month posted to GL. GL ID: {gl_posting_id}"
5. Send confirmation email to finance team
6. Update dashboard: show "Fechado" status
7. Return success to user
```

**Idempotency**: If same idempotency_key received twice, return cached result (don't re-post)

#### Case 2: Validation Error (HTTP 400)

**Server behavior**:
```
1. Receive error with failed_transaction_id and issue
2. Month remains in PRONTO state (no state change)
3. Create audit entry: "Posting validation failed: {issue}"
4. Return error to user: "Cannot post: {issue}. Fix and retry."
5. Suggest corrective action: "Use account {suggestion}"
6. Do NOT retry automatically
7. User must fix data and manually trigger retry
```

**User action**: Fix the transaction data and click "Post to GL" again

#### Case 3: Temporary Service Error (HTTP 503, timeout, network error)

**Server behavior**:
```
1. Log error with full context
2. Month remains in PRONTO state (not changed)
3. Queue automatic retry:
   - Attempt 1: Retry immediately (or after 30 seconds)
   - Attempt 2: Retry after 5 minutes (with exponential backoff)
   - Attempt 3: Retry after 30 minutes
4. After all retries exhausted:
   - Create audit entry: "Posting failed after 3 retries"
   - Alert finance director: "Month posting failed. Manual intervention needed."
   - Provide manual retry button for director
5. Do NOT automatically move month to POSTADO
```

**Idempotency guarantee**: Same idempotency_key used for all retries (prevents duplicate posts if retry succeeds)

#### Case 4: Timeout or Unknown State (Network failure mid-request)

**Biggest risk**: Month might be posted in GL but server doesn't know

**Server behavior**:
```
1. Detect timeout (no response within 60 seconds)
2. Create audit entry: "Posting timeout - state unknown"
3. Automatically query GL: "Is month 2026-05 posted?"
4. If YES in GL:
   a. Update financial_month_closures: state="POSTADO", gl_posting_id=...
   b. Send notification: "Month was posted (confirmed in GL). Updating state."
5. If NOT in GL:
   a. Queue for automatic retry (exponential backoff)
   b. Send notification to finance director: "Timeout during posting. Investigating..."
6. Do NOT leave month in undefined state
```

**Key principle**: Query GL system to determine actual state; don't guess

---

## Role-Based State Operations

| Role | ABERTO Actions | EM_REVIEW Actions | PRONTO Actions | POSTADO Actions |
|---|---|---|---|---|
| **Admin** (current) | All operations | Approve/Reject | Post to GL | Reopen |
| **Accountant** (proposed) | Create/edit/verify txns | View | None | None |
| **Finance Reviewer** (proposed) | View | Approve/Reject | View | View |
| **Finance Director** (proposed) | View | View | View | Reopen (with override) |

**Recommendation**: Current system uses single "admin" role. Phase 4 should introduce explicit roles.

---

## Exception Handling Procedures

### Scenario 1: User Leaves Month in EM_REVIEW for 1 Week

**Current**: No timeout documented  
**Proposed**:

```
After 48 hours in EM_REVIEW:
  - Send reminder email to finance director
  - Show "Pending Review" badge on dashboard

After 7 days in EM_REVIEW:
  - Escalate to finance director: "Month review overdue"
  - Show "OVERDUE" badge on dashboard

After 14 days in EM_REVIEW:
  - OPTIONAL: Auto-reject month, move back to ABERTO
  - Send alert: "Auto-rejected; move month back to ABERTO for rework"
  - Document decision rule: is this wanted behavior?
```

### Scenario 2: Month Posted, but Error Found in GL (1 week later)

**Current**: No recovery process documented  
**Proposed**:

```
User discovers error in GL posting:

Option A: Create reversal entry
  - Create new transaction: type="reversal", references GL posting ID
  - Post reversal as separate GL entry
  - Keep original month in POSTADO

Option B: Reopen month
  1. User clicks "Reopen for Corrections"
  2. Month state: POSTADO → ABERTO
  3. Transactions unlocked; user edits data
  4. User sends back to review: ABERTO → EM_REVIEW
  5. Finance director approves: EM_REVIEW → PRONTO
  6. Post corrected month: PRONTO → POSTADO (new GL posting ID)
  7. Both postings in GL (original + corrected)
  
Recommendation: Document which option is preferred
```

### Scenario 3: n8n Webhook Fails 3+ Times

**Current**: No escalation documented  
**Proposed**:

```
After 3 failed posting attempts:
  1. Create alert ticket for engineering team
  2. Email finance director: "Unable to post month. Contact support."
  3. Month remains in PRONTO
  4. Disable automatic retries (prevent cascade failure)
  5. Require manual retry with director confirmation
  
Alert should include:
  - Month ID and date range
  - Last error message from n8n
  - GL system status (is GL reachable?)
  - Retry instructions for manual fix
```

---

## Transition Validation Algorithm

```
FUNCTION validateTransition(currentState, targetState, month, user):
  
  // Check if transition is allowed
  IF NOT isValidTransition(currentState, targetState):
    RETURN error("Invalid state transition: {currentState} → {targetState}")
  
  // Check preconditions based on target state
  SWITCH targetState:
    CASE "EM_REVIEW":
      REQUIRE currentState == "ABERTO"
      REQUIRE allTransactionsVerified(month)
      REQUIRE allReceiptDocumentsPresent(month)
      REQUIRE reconciliationBalanced(month)
      REQUIRE user.roles.includes("admin")
    
    CASE "PRONTO":
      REQUIRE currentState == "EM_REVIEW"
      REQUIRE month.entered_review_at != null
      REQUIRE allPriorInvariantsHold(month)
      REQUIRE user.roles.includes("admin")
    
    CASE "POSTADO":
      REQUIRE currentState == "PRONTO"
      REQUIRE month.approved_at != null
      REQUIRE month.idempotency_key != null
      // n8n webhook success is implicit
    
    CASE "ABERTO":
      REQUIRE currentState in ["EM_REVIEW", "POSTADO"]
      IF currentState == "POSTADO":
        REQUIRE month.reopened_count < 5
        ALERT_IF month.reopened_count >= 3: "Month reopened many times"
      REQUIRE user.roles.includes("admin")
  
  // All preconditions passed
  RETURN success("Transition valid")
```

---

## Summary: The Explicit State Machine

### States (4)
1. **ABERTO**: Mutable, open for editing
2. **EM_REVIEW**: Locked, under review
3. **PRONTO**: Approved, ready to post
4. **POSTADO**: Posted, immutable

### Transitions (5 primary + 1 exception)
- ABERTO → EM_REVIEW (Send to review)
- EM_REVIEW → PRONTO (Approve)
- EM_REVIEW → ABERTO (Reject)
- PRONTO → POSTADO (Post to GL via n8n)
- POSTADO → ABERTO (Reopen for corrections)

### Key Properties
- Each state has explicit preconditions, operations, invariants
- All transitions are documented with guard clauses
- n8n integration is explicit with error handling
- Data immutability is enforced per state
- Audit trail captures all transitions
- Role-based access control (placeholder for Phase 4)

---

## Next Steps

- [ ] Task 3: Define business rules and constraints
- [ ] Task 4: Integrate with UX and Technical workstreams  
- [ ] Task 5: Create final Domain Model Specification

---

**Document Status**: Ready for cross-stream validation with UX and Technical workstreams
