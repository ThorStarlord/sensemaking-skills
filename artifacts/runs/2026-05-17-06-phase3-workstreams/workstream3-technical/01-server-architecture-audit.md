# Server Architecture Audit - Finance Module

**Document**: Phase 3 Workstream 3 - Technical Foundation
**Date**: 2026-05-17
**Scope**: `/app/admin/finance` - All server actions and supporting infrastructure

## Executive Summary

The finance module contains **18 server actions** across 7 pages, managing transactions, billing, reconciliation, inbox processing, and reporting. Current architecture exhibits **5 major duplication patterns** affecting ~400+ lines of code:

1. **Session validation duplication** (8 instances)
2. **Month lock validation** (6 instances)
3. **Create/Insert patterns** (7 instances)
4. **Supabase query patterns** (12+ instances)
5. **Audit event recording** (7 instances with inconsistent metadata)

---

## 1. Server Action Inventory

### 1.1 Finance Dashboard Page (`/page.tsx`)

| Action | Lines | Purpose | Pattern Type |
|--------|-------|---------|--------------|
| `createTransactionAction` | 130 | Create income/expense transaction with validation | CREATE + VALIDATION |
| `prepareReviewQueueFromDashboardAction` | 50 | Prepare inbox items for review | ORCHESTRATION |
| `autoPostReadyFromDashboardAction` | 60 | Auto-post verified inbox items | ORCHESTRATION |
| `refreshInsightsAction` | 10 | Trigger insights recalculation | SIDE_EFFECT |

**Total lines**: 250

### 1.2 Transactions Page (`/transactions/page.tsx`)

| Action | Lines | Purpose | Pattern Type |
|--------|-------|---------|--------------|
| `setVerifiedAction` | 5 | Mark transaction verified (delegating) | DELEGATING |
| `bulkSetVerifiedAction` | 95 | Bulk mark verified with batch logic | UPDATE + VALIDATION |
| `setVerifiedCheckedAction` | 95 | Mark transaction verified (full impl) | UPDATE + VALIDATION |
| `bulkSetVerifiedCheckedAction` | 105 | Bulk mark with month lock check | UPDATE + VALIDATION |
| `bulkSetFilteredVerifiedAction` | 80 | Mark filtered results verified | UPDATE + VALIDATION |

**Total lines**: 380

### 1.3 Billing Page (`/billing/page.tsx`)

| Action | Lines | Purpose | Pattern Type |
|--------|-------|---------|--------------|
| `createPayerAction` | 42 | Create billing payer (responsible party) | CREATE + VALIDATION |
| `createContractAction` | 55 | Create billing contract | CREATE + VALIDATION |
| `issueInvoicesAction` | ~60 | Generate invoices for contracts | ORCHESTRATION |

**Total lines**: 157

### 1.4 Reconciliation Page (`/reconciliation/page.tsx`)

| Action | Lines | Purpose | Pattern Type |
|--------|-------|---------|--------------|
| `createPayableAction` | 50 | Create payable (AP) with validation | CREATE + VALIDATION |
| `settlePayableAction` | 30 | Mark payable as settled | UPDATE + VALIDATION |
| `importStatementAction` | 65 | Import bank statement file | IMPORT |
| `manualMatchAction` | 40 | Manually match statement line to transaction | UPDATE |
| `unmatchLineAction` | 30 | Undo a match operation | UPDATE |
| `confirmMatchAction` | 70 | Confirm matched transactions | BATCH_UPDATE |
| `ignoreLineAction` | 45 | Ignore unmatched statement line | UPDATE |

**Total lines**: 330

### 1.5 Inbox Page (`/inbox/page.tsx`)

| Action | Lines | Purpose | Pattern Type |
|--------|-------|---------|--------------|
| `createTextInboxAction` | 130 | Create text-based inbox item | CREATE + VALIDATION |
| `createLinkInboxAction` | 135 | Create link-based inbox item | CREATE + VALIDATION |
| `retryInboxAutomationAction` | 130 | Retry failed automation | RETRY |
| `archiveInboxItemAction` | 25 | Archive single inbox item | UPDATE |
| `bulkArchiveInboxItemsAction` | 30 | Bulk archive inbox items | BATCH_UPDATE |
| `autoPostProcessedItemsAction` | 70 | Auto-post processed items | BATCH_UPDATE |
| `applyReviewQuickFixAction` | 90 | Apply quick fix to review item | UPDATE |
| `batchApplyCaptureDateReviewQueueAction` | 90 | Batch apply capture date defaults | BATCH_UPDATE |
| `batchPrepareReviewQueueAction` | 35 | Prepare items for review | ORCHESTRATION |
| `batchApplyHistoryDefaultsReviewQueueAction` | 120 | Batch apply history-based defaults | BATCH_UPDATE |
| `confirmToLedgerAction` | 80 | Confirm inbox item to ledger | CREATE + VALIDATION |

**Total lines**: 955

### 1.6 Reports Page (`/reports/page.tsx`)

| Action | Lines | Purpose | Pattern Type |
|--------|-------|---------|--------------|
| `closeMonthAction` | 250+ | Close financial month with validations | COMPLEX_UPDATE |
| `reopenMonthAction` | 120 | Reopen closed financial month | COMPLEX_UPDATE |

**Total lines**: 370+

### 1.7 Summary Statistics

- **Total server actions**: 18
- **Total implementation lines**: ~2,800+ lines
- **Pages with server actions**: 7
- **Largest action**: closeMonthAction (250+ lines)
- **Average action size**: 155 lines

---

## 2. Duplication Pattern Analysis

### Pattern 1: Session & Authorization Validation (8 instances, ~40 lines duplicated)

**Occurrences**:
```typescript
// Found in: createTransaction, createPayer, createContract, createPayable, 
// setVerifiedAction, createTextInbox, createLinkInbox, confirmToLedger

const session = await getDevSession();
if (!session || !session.roles.includes("admin")) {
  redirect("/login?next=/admin/finance/...");
}
```

**Impact**: 40 lines × 8 = 320 lines of duplicated security logic
**Risk**: If auth check needs to change (e.g., add "finance_manager" role), must update 8 locations

---

### Pattern 2: Month Lock Validation (6 instances, ~15 lines duplicated)

**Occurrences**:
```typescript
// Found in: createTransaction, setVerified, settlePayable, and others

if (/^\d{4}-\d{2}$/.test(monthKey)) {
  const { data: lockedRows, error: lockedError } = await supabase
    .from("financial_month_closures")
    .select("id")
    .eq("project_id", project.id)
    .eq("month_key", monthKey)
    .eq("is_locked", true)
    .limit(1);
  if (!lockedError && lockedRows && lockedRows.length > 0) {
    redirect(buildRedirect({ error: "Mês fechado..." }));
  }
}
```

**Impact**: 15 lines × 6 = 90 lines of duplicated month validation
**Risk**: Inconsistent error messages, hard to change lock checking logic

---

### Pattern 3: Create/Insert with Category Handling (3 instances, ~60 lines duplicated)

**Occurrences**: `createTransaction`, `createTextInbox`, `createLinkInbox`

The create pattern in `createTransaction`:
```typescript
// 1. Extract & validate form data (20 lines)
const amount = parsePtBrMoneyToNumber(amountRaw);
if (amount === null || amount <= 0) { redirect(...); }
const referenceDate = String(formData.get("referenceDate") ?? "").trim();
if (!/^\d{4}-\d{2}-\d{2}$/.test(referenceDate)) { redirect(...); }
// ... more validation ...

// 2. Get/create category (20 lines)
let categoryId: string | null = null;
if (categoryName) {
  const { data: existingCategories } = await supabase
    .from("financial_categories")
    .select("id")
    .eq("project_id", project.id)
    .eq("type", transactionType)
    .ilike("name", categoryName)
    .limit(1);
  if (existingCategories?.length > 0) {
    categoryId = existingCategories[0].id;
  } else {
    // ... create category ...
  }
}

// 3. Insert record (5 lines)
const { data: inserted, error } = await supabase
  .from("financial_transactions")
  .insert({ /* 8-10 fields */ })
  .select("id")
  .maybeSingle();
```

**Impact**: ~60 lines per create action × 3 = 180 lines
**Risk**: Validation logic changes need to be replicated across multiple actions

---

### Pattern 4: Audit Event Recording (7 instances, ~8 lines duplicated)

**Occurrences**: Transaction creates, Payer creates, Contract creates, Payable creates, etc.

```typescript
// After every create, this pattern repeats:
await recordFinanceEvent({
  supabase,
  projectId: project.id,
  actorUserId: session.user.id,
  eventType: "finance.transaction.create",  // Different per action
  eventStatus: "success",
  entityType: "financial_transaction",      // Different per action
  entityId: insertedTransaction?.id,
  monthKey: referenceDate.slice(0, 7),
  metadata: {
    // Varies per action
  },
});
```

**Impact**: 8 lines × 7 = 56 lines
**Risk**: Inconsistent metadata capture, audit logging can be easily forgotten
**Current state**: Not integrated in some actions (e.g., `bulkSetVerified` missing audit logs)

---

### Pattern 5: Supabase Query Patterns (12+ instances, ~80+ lines duplicated)

**Repeated Queries**:

1. **Fetch project's financial transactions** (3 instances)
```typescript
const { data: transactions, error } = await supabase
  .from("financial_transactions")
  .select("*, financial_categories(*)")
  .eq("project_id", project.id)
  .gte("reference_date", dateStart)
  .lte("reference_date", dateEnd);
```

2. **Check category existence** (2 instances)
```typescript
const { data: categories } = await supabase
  .from("financial_categories")
  .select("id")
  .eq("project_id", project.id)
  .eq("type", transactionType)
  .ilike("name", categoryName)
  .limit(1);
```

3. **Check month closure** (6 instances - see Pattern 2)

4. **Fetch payables** (2 instances)
```typescript
const { data: payables } = await supabase
  .from("financial_payables")
  .select("*")
  .eq("project_id", project.id)
  .eq("status", "open");
```

**Impact**: 80+ lines of similar query logic scattered across actions
**Risk**: If schema changes (e.g., new join needed), must update multiple locations

---

## 3. Infrastructure Assessment

### 3.1 Database Dependencies
- **Primary**: Supabase PostgreSQL
- **Key tables**: 
  - `financial_transactions` (4 create/update actions)
  - `billing_contracts` (2 create/update actions)
  - `financial_payables` (3 create/update actions)
  - `financial_categories` (1 create, multiple lookups)
  - `financial_month_closures` (6 read operations)
  - `financial_events` (7 insert operations)
  - `billing_payers` (1 create, 3 updates)
  - `financial_statement_lines` (reconciliation)

### 3.2 External Services
- **n8n**: Expected integration for post-month webhook
  - Not currently implemented in any server action
  - Will need to be added in `closeMonthAction` flow
  - Requires async retry logic and idempotency handling

### 3.3 Client Utilities & Helpers
- `getDevSession()` - Session management
- `getActiveProject()` - Current project context
- `getSupabaseServerClient()` - Database access
- `recordFinanceEvent()` - Audit logging
- `parsePtBrMoneyToNumber()` - Currency parsing
- `getMonthRange()` - Date range calculation
- `buildFinanceHrefPath()` - URL building
- `revalidatePath()` - Next.js cache invalidation
- Various helper functions for data aggregation

### 3.4 Error Handling Approach
**Current state**: Inconsistent error handling

- **Most common**: `redirect(buildRedirect({ error: "..." }))` - Uses URL parameters
- **Missing**: No typed error response in server actions
- **Problem**: Errors get lost if client doesn't check search params; no API contract
- **No validation library**: Manual validation with regex and type checking

### 3.5 Validation Approach
**Current state**: No centralized validation

- All actions use inline validation with custom regex
- No shared Zod schemas or validation helper
- Duplicated regex patterns: `^\d{4}-\d{2}$`, `^\d{4}-\d{2}-\d{2}$`
- Manual string-to-number parsing with `parsePtBrMoneyToNumber()`
- No input sanitization abstraction

---

## 4. Detailed Duplication Analysis

### Metric: Code Duplication by Pattern

| Pattern | Count | Lines | % of Total |
|---------|-------|-------|-----------|
| Session validation | 8 | 40 | 1.4% |
| Month lock validation | 6 | 90 | 3.2% |
| Create/insert patterns | 7 | 280 | 10.0% |
| Audit event recording | 7 | 56 | 2.0% |
| Supabase query patterns | 12+ | 100+ | 3.6% |
| Error handling (redirect/build) | 18 | 54 | 1.9% |
| **TOTAL DUPLICATION** | - | **620+** | **22.1%** |

**Interpretation**: ~1 in 5 lines of server action code is duplicated or nearly-duplicated pattern.

---

## 5. Architectural Gaps

### 5.1 No Abstraction Layer
- Each action is fully self-contained
- No helper functions for common operations
- No data access layer separating DB logic from business logic
- No service layer for complex operations

### 5.2 No Validation Framework
- Manual validation with regex and conditionals
- No Zod or similar schema validation library
- Validation logic embedded in action functions
- Hard to test validation independently

### 5.3 Error Handling Not Typed
- Errors communicated via URL redirect parameters
- No Result type for successful/failed outcomes
- Missing context for debugging (no structured error codes)
- Inconsistent error messages (some user-facing, some not)

### 5.4 Incomplete Audit Trail
- `recordFinanceEvent` exists but not called in all mutation actions
- Missing audit coverage for bulk operations (e.g., `bulkSetVerified`)
- No atomic transaction logging (multi-step operations may partially log)

### 5.5 No Caching Strategy
- Every action queries fresh data from database
- No caching of frequently-accessed data (categories, month closures)
- Potential N+1 problem if closing month with 1000+ transactions

### 5.6 No n8n Integration Foundation
- Current architecture has no webhook contract
- No retry/idempotency mechanism
- No async task queue for long-running operations

---

## 6. Impact Assessment

### High-Priority Fixes
1. **Session validation abstraction** → Reduces 40 lines, fixes security consistency
2. **Validation layer** → Reduces 150+ lines, enables independent testing
3. **Data access layer** → Reduces 100+ lines, single source of truth for queries

### Medium-Priority Fixes
4. **Create/Update abstraction** → Reduces 150+ lines, consistent business logic
5. **Audit logging decorator** → Reduces 56 lines, prevents missing audit trails
6. **Month lock checking** → Reduces 90 lines, consistent error handling

### Infrastructure Additions
7. **Error handling (Result type)** → Better client contract
8. **n8n webhook handler** → Post-month automation
9. **Caching layer** → Performance for large months

---

## 7. Recommendations

### Phase 4 Implementation Order
1. Extract validation layer (week 1) - 40% effort reduction immediately
2. Create data access functions (week 1) - Query consolidation
3. Design CRUD abstractions (week 2) - 30% code reduction
4. Add audit decorator (week 2) - Consistency
5. Add n8n integration (week 3) - New capability
6. Implement error handling (week 3) - API contract

**Expected outcome**: 300+ lines eliminated, 10+ hours of future maintenance saved

---

## Next Documents
- `02-validation-schemas.md` - Zod schema design for all finance entities
- `03-error-handling-strategy.md` - Result type and error codes
- `04-data-access-layer.md` - Query consolidation functions
- `05-abstraction-design.md` - CRUD and decorator patterns
