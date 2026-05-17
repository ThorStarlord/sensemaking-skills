# Business Rules & Constraints Specification

**Date**: 2026-05-17  
**Workstream**: Workstream 1 — Domain Model Specification  
**Status**: Complete  
**Closes Critical Gap #3**: Business rules and exception handling from Phase 2 interviews

---

## Executive Summary

This document specifies **the business rules and constraints** that govern financial month operations in Metamorfose Finance. These rules ensure data integrity, compliance, and user safety.

**Three layers of enforcement**:
1. **Database layer**: Constraints at table/column level (prevent invalid data at source)
2. **Application layer**: Server-side validation (business logic enforcement)
3. **UI layer**: Frontend validation (user guidance before submission)

---

## Reconciliation Rules

### Rule 1: Month Reconciliation Must Balance

**When**: Before transitioning month from ABERTO to EM_REVIEW  
**Check**: `sum(all_transaction_amounts) == expected_gl_balance`  
**Tolerance**: ±0.01 (to account for floating-point rounding)

**Enforcement**:
```typescript
// Database: No constraint (calculated value)
// Application: In readFinanceMonthReadiness()
const variance = Math.abs(actual_balance - expected_balance);
if (variance > 0.01) {
  return { status: "unbalanced", variance, required_action: "fix_reconciliation" };
}
```

**UI Behavior**:
- Dashboard shows "Conciliacao: {variance}" blocker if unmatched
- "Send to Review" button is disabled if unmatched
- Link to Reconciliation page to fix discrepancy

**User Action**:
- Finance director reviews reconciliation items
- Adjusts transaction amounts or GL expectations
- Retries month preparation

**Escalation**:
- If unmatched for > 24 hours: Alert director
- If variance > 100.00: Alert director immediately
- If variance > 1000.00: Block sending to review; require director override

---

### Rule 2: Reconciliation Items Must Be Resolved

**When**: Before month closure  
**Check**: All reconciliation items in `financial_reconciliation_items` table have `status = "resolved"`

**Enforcement**:
```typescript
// Application: In readFinanceMonthReadiness()
const unresolvedItems = await supabase
  .from("financial_reconciliation_items")
  .select("*")
  .eq("month_key", monthKey)
  .neq("status", "resolved");

if (unresolvedItems.length > 0) {
  return { status: "reconciliation_pending", count: unresolvedItems.length };
}
```

**UI Behavior**:
- Dashboard shows count of unresolved items
- "Send to Review" disabled if any unresolved
- Link to Reconciliation page

**User Action**:
- Review each reconciliation item (e.g., statement balance mismatch)
- Either:
  a) Adjust transaction to match bank statement
  b) Update GL expected balance
  c) Flag as "acceptable difference" with justification

---

## Receipt and Document Requirements

### Rule 1: Non-Journal Transactions Require Documents

**When**: Before marking transaction as verified  
**Check**: `transaction_type != 'reversal' AND source_file_url IS NOT NULL`

**Applies to**:
- Vendor invoices (expense)
- Employee reimbursements (expense)
- Sales invoices (income)
- Bank transfers (both)

**Does NOT apply to**:
- Journal entries (manual adjustments)
- Reversal entries (correction transactions)
- System-generated entries

**Enforcement**:
```typescript
// Application: In setTransactionVerified()
if (transaction.transaction_type !== 'reversal' && !transaction.source_file_url) {
  return error("Document required for this transaction type");
}
```

**UI Behavior**:
- "Mark as Verified" button disabled if document missing
- Tooltip: "Attach document to mark as verified"
- Link to document upload

**User Action**:
- Upload receipt/invoice document
- Provide document date and amount on document
- System validates document is readable (anti-scan-blank-paper check?)

---

### Rule 2: Documents Must Be Legible

**When**: During review (EM_REVIEW state)  
**Check**: Finance director visually confirms documents are legible

**Enforcement**:
```typescript
// UI: Finance director reviews each document
// No automated check (manual process)
// Can reject with: "Document illegible; request from vendor"
```

**User Action**:
- Finance director views each document
- If illegible: Reject month with message "Document {id} illegible"
- Month returned to ABERTO; accountant re-uploads document

---

### Rule 3: Document Retention Period

**When**: After month closure  
**Check**: Documents retained for minimum of 7 years

**Enforcement**:
```sql
-- No automatic deletion; manual retention policy
-- Backup to archive storage after 5 years
-- Delete flag set but not permanent deletion after 7 years
ALTER TABLE financial_transactions ADD archive_retention_until DATE;
```

**Implication**: Document URLs must be permanent or redirected; no bit-rot allowed

---

## Budget Rules

### Rule 1: Department Budget Cannot Be Exceeded

**When**: Creating/editing transaction amount  
**Check**: `sum(transactions by dept, YTD) + new_transaction <= department_budget_limit`

**Enforcement**:
```typescript
// Application: In createTransaction() or updateTransaction()
const departmentBudget = await getDepartmentBudget(transaction.department_id, year);
const ytdSpent = await sumTransactionsByDept(transaction.department_id, year);
const projectedTotal = ytdSpent + transaction.amount;

if (projectedTotal > departmentBudget.limit) {
  // Either block or warn depending on override flag
  if (!user.can_override_budget) {
    return error("Would exceed budget");
  } else {
    recordBudgetOverride(transaction.id, user.id, reason);
  }
}
```

**UI Behavior**:
- When creating transaction: Show projected budget remaining
- If would exceed: Show warning (yellow) or block (red) depending on role
- If blocked: Show "Request override" button (for manager approval)

**User Action**:
- Reduce transaction amount, OR
- Request budget override from manager
- Manager approves in separate workflow (not documented here)

---

### Rule 2: Budget Variance Reporting

**When**: Month closure  
**Check**: Generate variance report for any department > 5% over/under budget

**Enforcement**:
```typescript
// Application: In generateMonthVarianceReport()
const variance = (ytdSpent / departmentBudget.limit) - 1.0;
if (Math.abs(variance) > 0.05) {
  report.push({
    department,
    budget: departmentBudget.limit,
    spent: ytdSpent,
    variance_pct: variance,
    severity: Math.abs(variance) > 0.10 ? "HIGH" : "MEDIUM"
  });
}
```

**UI Behavior**:
- Finance director sees variance report during review
- Can acknowledge and proceed
- If variance > 10%: Requires director sign-off before closure

---

## Access Control Rules

### Rule 1: Month Editing Restricted by State

**When**: Any transaction operation  
**Check**: `month.state != "POSTADO" AND (month.state != "EM_REVIEW" OR user has_override)`

**Enforcement**:
```typescript
// Application: In every transaction mutation
async function validateMonthEditable(monthKey: string, user: User) {
  const closure = await getMonthClosure(monthKey);
  
  if (!closure) {
    // ABERTO state; allow edits
    return true;
  }
  
  if (closure.state === "POSTADO") {
    // POSTADO; never allow edits
    throw new Error("Cannot edit posted month");
  }
  
  if (closure.state === "EM_REVIEW") {
    // EM_REVIEW; only allow with override
    if (!user.roles.includes("admin")) {
      throw new Error("Month under review; cannot edit");
    }
    recordOverride(user.id, "edit_in_review", monthKey);
  }
  
  return true;
}
```

**UI Behavior**:
- If month in EM_REVIEW or POSTADO: Edit buttons disabled
- Tooltip: "Month is [state]; editing not allowed"
- Show "Reopen" button if state = POSTADO

---

### Rule 2: Role-Based State Transitions

**When**: State transition operation  
**Check**: User has required role for transition

**Current roles** (limited; Phase 4 to expand):
- `admin`: All operations

**Proposed roles** (for Phase 4):
- `accountant`: Create/edit/verify transactions
- `finance_reviewer`: Approve/reject month reviews
- `finance_director`: Authorize final closure and reopens
- `admin`: All operations

**Enforcement**:
```typescript
function requireRole(operation: "send_review" | "approve" | "post" | "reopen", user: User) {
  const required: Record<string, string[]> = {
    send_review: ["accountant", "admin"],
    approve: ["finance_reviewer", "admin"],
    post: ["finance_director", "admin"],
    reopen: ["finance_director", "admin"]
  };
  
  if (!user.roles.some(r => required[operation].includes(r))) {
    throw new Error(`Role required for ${operation}: ${required[operation].join(", ")}`);
  }
}
```

---

### Rule 3: View Access by Role

**When**: Viewing month data  
**Check**: User can only view months relevant to their role

**Current behavior** (all users see all months):
- ✅ Accountant: Can view all months
- ✅ Finance reviewer: Can view all months
- ✅ Finance director: Can view all months

**Future rule** (Phase 4):
- Accountant: Can view only their department's months
- Finance reviewer: Can view all months
- Finance director: Can view all months

---

## Exception Handling Procedures

### Exception 1: Month Stuck in EM_REVIEW (No Approval)

**Scenario**: Month sent to review 2 weeks ago; still not approved by director

**Current behavior**: No timeout; month stays in EM_REVIEW indefinitely

**Proposed solution**:

```
Timeline:
48 hours: Send reminder email to finance director
  Subject: "Month 2026-05 awaiting your review"
  Action: Link to review page
  
7 days: Escalate to accounting manager
  Subject: "URGENT: Month review overdue"
  Action: Contact director directly
  
14 days: Auto-reject month, revert to ABERTO
  Subject: "Month 2026-05 auto-rejected due to timeout"
  Action: Accountant must fix issues and re-submit
  
Document policy:
- Director has 14 days to review
- Escalation timeline is configurable
- Directors can request extension (manual override)
```

**Implementation**:
```typescript
// Scheduled job: Check for stale reviews
async function checkStaleMonthReviews() {
  const staleMonths = await supabase
    .from("financial_month_closures")
    .select("*")
    .eq("state", "EM_REVIEW")
    .lt("entered_review_at", now() - 14_days);
  
  for (const month of staleMonths) {
    // Auto-reject
    month.state = "ABERTO";
    month.rejected_at = now();
    month.rejection_reason = "Auto-rejected due to 14-day timeout";
    
    // Notify team
    sendEmail(accountant, "Review timeout; month rejected");
  }
}
```

---

### Exception 2: n8n Webhook Fails Repeatedly

**Scenario**: Attempted to post month 3 times; n8n keeps returning 503 errors

**Current behavior**: No limit; keeps retrying indefinitely

**Proposed solution**:

```
Retry strategy:
Attempt 1: Immediate (or 30 seconds)
  - If fails: Schedule attempt 2
  
Attempt 2: 5 minutes later
  - If fails: Schedule attempt 3
  
Attempt 3: 30 minutes later
  - If fails: ESCALATE
  
Escalation (after 3 failures):
  - Send alert email to engineering team
    Subject: "Finance posting failed: month 2026-05"
    Details: Last error message, month ID, GL system status
  
  - Send email to finance director
    Subject: "Cannot post month; manual intervention needed"
    Action: Manual retry button with engineering approval
  
  - Disable automatic retries
  - Month remains in PRONTO (not posted)
  - Block further automatic attempts until engineering approves
```

**Implementation**:
```typescript
async function postMonthWithRetry(monthId: string, retryCount: number = 0) {
  try {
    return await callN8nWebhook(monthId);
  } catch (error) {
    if (retryCount >= 3) {
      // Escalate
      sendAlert("engineering", "Posting failed", error);
      recordMonthPostingFailure(monthId, error, retryCount);
      return { status: "failed", escalated: true };
    }
    
    const delay = [0, 5 * 60, 30 * 60][retryCount];
    scheduleRetry(monthId, retryCount + 1, delay);
    return { status: "retrying", nextAttempt: delay };
  }
}
```

---

### Exception 3: Timeout During GL Posting (Unknown State)

**Scenario**: Posted month to GL; response never came back (network timeout)

**Current behavior**: Unknown; month state might not match GL reality

**Proposed solution**:

```
Detection (timeout after 60 seconds):
1. Month remains in PRONTO (don't change state)
2. Create audit entry: "Posting timeout; state unknown"
3. Send alert to finance director: "Timeout during posting; investigating..."

Recovery (automatic):
1. Query GL system: "Is month 2026-05 posted?"
   - Call GL API: GET /api/postings?month=2026-05
   - Look for posting_id in response
   
2. If found in GL:
   a. Extract GL posting ID from response
   b. Update financial_month_closures: state="POSTADO", gl_posting_id=...
   c. Send confirmation: "Month was posted; state updated"
   
3. If NOT found in GL:
   a. Schedule retry: exponential backoff, max 3 attempts
   b. If all retries fail: Escalate to engineering
   
4. NEVER leave month in undefined state
```

**Implementation**:
```typescript
async function handlePostingTimeout(monthId: string) {
  // Check if month is already posted in GL
  const glStatus = await queryGLSystem(`month=${monthId}`);
  
  if (glStatus.posted) {
    // Month is posted; update our state
    await updateMonthClosure(monthId, {
      state: "POSTADO",
      gl_posting_id: glStatus.posting_id,
      posted_at: glStatus.posted_at
    });
    
    sendNotification("finance_director", "Month was posted; state synchronized");
    return { status: "recovered", gl_posting_id: glStatus.posting_id };
  }
  
  // Not posted in GL; retry
  scheduleRetry(monthId, { strategy: "exponential_backoff", maxAttempts: 3 });
  return { status: "retrying" };
}
```

---

### Exception 4: User Reopens Month Too Many Times

**Scenario**: Month has been reopened 4 times (originally posted, then corrections, posted again, more corrections, etc.)

**Current behavior**: No limit; user can reopen indefinitely

**Proposed solution**:

```
Limits:
0 reopens: Normal closure
1 reopen: First correction; expected
2 reopens: Second correction; monitor
3 reopens: Alert director: "Month reopened 3 times; check for patterns"
4 reopens: BLOCK reopening; require director override
5+ reopens: BLOCK; require CEO override (clearly something is wrong)

Implementation:
if (reopened_count >= 4) {
  if (!user.roles.includes("director")) {
    return error("Month reopened too many times; director override required");
  }
  
  recordDirectorOverride(monthId, user.id, reason);
}

if (reopened_count >= 5) {
  return error("Month reopened too many times; CEO override required");
}
```

**Alerts**:
- 1 reopen: No alert
- 2 reopens: Silent (expected)
- 3 reopens: Alert to director email
- 4 reopens: Escalate to director (block without override)
- 5 reopens: Escalate to CEO (block without CEO override)

---

### Exception 5: Data Corruption Detected

**Scenario**: Snapshot shows 10 transactions; actual month has 15 transactions (data changed after closure?)

**Current behavior**: No validation; could happen silently

**Proposed solution**:

```
Detection (daily audit job):
1. For each POSTADO month:
   a. Count transactions in snapshot
   b. Count actual transactions in database
   c. If counts differ: ALERT
   
2. Alert includes:
   - Month ID
   - Snapshot count vs actual count
   - List of extra/missing transactions
   - Time of last modification
   
3. Investigation:
   - Query audit trail: Who modified transactions after closure?
   - Was month reopened? (reopened_count > 0)
   - Is this a legitimate reopen, or unauthorized modification?

Action:
- If reopened: Legitimate; mark audit as closed
- If NOT reopened: DATA CORRUPTION; escalate to director
- If unauthorized: Security incident; log and investigate
```

**Implementation**:
```typescript
async function auditDataIntegrity() {
  const postedMonths = await supabase
    .from("financial_month_closures")
    .select("*")
    .eq("state", "POSTADO");
  
  for (const month of postedMonths) {
    const snapshotCount = month.snapshot.transactions.length;
    const actualCount = await countTransactions(month.month_key);
    
    if (snapshotCount !== actualCount) {
      // Data mismatch
      const reopenCount = month.reopened_count || 0;
      
      if (reopenCount > 0) {
        // Expected if reopened; mark as reviewed
        recordAuditNote(month.id, "Data modified after reopen; expected");
      } else {
        // Unexpected; escalate
        sendAlert("director", "Data integrity issue", {
          monthId: month.id,
          snapshotCount,
          actualCount,
          reopens: reopenCount
        });
      }
    }
  }
}
```

---

## Constraint Definitions

### Table-Level Constraints

#### financial_month_closures Table

```sql
CREATE TABLE financial_month_closures (
  id UUID PRIMARY KEY,
  project_id UUID NOT NULL,
  month_key VARCHAR(7) NOT NULL,  -- YYYY-MM format
  state VARCHAR(20) NOT NULL,      -- ABERTO, EM_REVIEW, PRONTO, POSTADO
  
  -- Timestamps
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  entered_review_at TIMESTAMP,      -- When entered EM_REVIEW
  approved_at TIMESTAMP,            -- When approved to PRONTO
  posted_at TIMESTAMP,              -- When posted to GL
  reopened_at TIMESTAMP,            -- When reopened for corrections
  
  -- User tracking
  entered_review_by UUID,           -- Finance director who sent to review
  approved_by UUID,                 -- Finance director who approved
  posted_by UUID,                   -- User who triggered posting
  reopened_by UUID,                 -- User who reopened
  
  -- GL Integration
  gl_posting_id VARCHAR(50),        -- External GL posting ID
  idempotency_key VARCHAR(100) UNIQUE,  -- Prevent duplicate posts
  
  -- Data
  snapshot JSONB,                   -- Immutable snapshot at posting time
  reopened_count INTEGER DEFAULT 0, -- Number of reopens
  
  -- Validation
  reconciliation_status VARCHAR(20), -- BALANCED, UNBALANCED, PENDING
  reconciliation_variance DECIMAL(10,2),
  
  -- Notes
  notes TEXT,
  rejection_reason TEXT,            -- Why month rejected in review
  
  -- Constraints
  UNIQUE (project_id, month_key),
  CHECK (state IN ('ABERTO', 'EM_REVIEW', 'PRONTO', 'POSTADO')),
  CHECK (month_key ~ '^\d{4}-\d{2}$'),  -- YYYY-MM format
  CHECK (reopened_count >= 0 AND reopened_count <= 10),  -- Sanity limit
  
  -- Immutability rules
  CHECK (
    CASE 
      WHEN state = 'POSTADO' THEN snapshot IS NOT NULL
      ELSE TRUE
    END
  ),
  
  -- GL posting requirement
  CHECK (
    CASE
      WHEN state = 'POSTADO' THEN gl_posting_id IS NOT NULL
      ELSE TRUE
    END
  ),
  
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE RESTRICT,
  FOREIGN KEY (entered_review_by) REFERENCES users(id),
  FOREIGN KEY (approved_by) REFERENCES users(id),
  FOREIGN KEY (posted_by) REFERENCES users(id),
  FOREIGN KEY (reopened_by) REFERENCES users(id)
);

-- Indexes for common queries
CREATE INDEX idx_month_closures_by_month_key ON financial_month_closures(project_id, month_key);
CREATE INDEX idx_month_closures_by_state ON financial_month_closures(project_id, state);
```

#### financial_transactions Table Updates

```sql
-- Add month locking support
ALTER TABLE financial_transactions ADD COLUMN month_locked BOOLEAN DEFAULT FALSE;

-- Add reconciliation reference
ALTER TABLE financial_transactions ADD COLUMN reconciliation_item_id UUID REFERENCES financial_reconciliation_items(id);

-- Constraints
ALTER TABLE financial_transactions ADD CONSTRAINT check_verified_requires_document
  CHECK (
    CASE
      WHEN transaction_type != 'reversal' THEN source_file_url IS NOT NULL
      ELSE TRUE
    END
  );
```

---

## Audit Trail Requirements

### Events to Log

Every state transition and exception must be logged in `finance_audit_log` table:

| Event | Details Logged |
|---|---|
| Month created | month_key, created_by |
| Month sent to review | month_key, sent_by, transaction_count |
| Month approved | month_key, approved_by, review_duration |
| Month rejected | month_key, rejected_by, rejection_reason |
| Month posted | month_key, posted_by, gl_posting_id, n8n_response |
| Month posting failed | month_key, attempt_number, error_message, retry_scheduled |
| Month reopened | month_key, reopened_by, reopened_count, reason |
| Month re-closed | month_key, posted_by, new_gl_posting_id |
| Timeout detected | month_key, posting_state, recovery_action |
| Data integrity check failed | month_key, snapshot_count, actual_count |
| Override recorded | month_key, override_type, override_by, reason |

---

## Summary: Business Rules

### Reconciliation
- Must balance within ±0.01 tolerance before EM_REVIEW transition
- All reconciliation items must be resolved

### Documents
- Non-journal transactions require source documents
- Documents must be legible (manual check by finance director)
- Retained for 7 years minimum

### Budget
- Department budgets cannot be exceeded (with admin override)
- Variance reports generated if > 5% variance

### Access Control
- State-based restrictions on editing
- Role-based state transitions (simple in Phase 3; expand in Phase 4)

### Exception Handling
- Stale reviews auto-rejected after 14 days
- n8n failures retry 3x then escalate
- Timeout recovery via GL system query
- Reopen limits (block after 4 without override)
- Data integrity audit (detect unauthorized changes)

---

**Document Status**: Ready for cross-stream validation with UX and Technical workstreams
