# Current State Machine Analysis (Implicit)

**Date**: 2026-05-17  
**Workstream**: Workstream 1 — Domain Model Specification  
**Author**: Phase 3 Domain Analysis  
**Status**: Analysis Complete  

---

## Executive Summary

The Finance UI implements a **month closure state machine** that is currently **implicit and scattered** across three layers:

1. **Database layer**: `financial_month_closures.is_locked` boolean flag
2. **UI layer**: Status labels ("Aberto", "Pronto", "Fechado", "Reaberto") derived from `is_locked` flag
3. **Business logic layer**: Access control rules hardcoded in server actions and frontend checks

**Critical Finding**: The system uses a **single boolean flag** (`is_locked`) to represent multiple logical states, leading to ambiguity and bugs.

---

## Month States (Current Implementation)

### Database Table: `financial_month_closures`

```sql
financial_month_closures:
├── id: UUID
├── project_id: UUID (FK)
├── month_key: STRING (YYYY-MM format)
├── is_locked: BOOLEAN (0 = open, 1 = locked)
├── snapshot: JSONB (data snapshot at closure time)
├── notes: TEXT (closure notes)
├── closed_at: TIMESTAMP (when month was locked)
├── reopened_count: INTEGER (implicit: count of reopen actions)
└── created_at, updated_at: TIMESTAMP
```

### Implicit State Representation

The system conflates **closure state** with **editing capability**, represented by a single flag:

| Logical State | is_locked | Represented How | Business Meaning |
|---|---|---|---|
| **ABERTO (Open)** | `null` (no row exists) | No `financial_month_closures` record | Month is open for entry/editing; all operations allowed |
| **PRONTO (Ready)** | `false` | `is_locked = false` + data validated | Month data validated; ready for official closure; operations restricted |
| **FECHADO (Closed/Locked)** | `true` | `is_locked = true` + snapshot saved | Month officially closed; data immutable; read-only access |
| **REABERTO (Reopened)** | `true` (but) | `is_locked = true` + reopened_count > 0 | Month was closed but reopened for corrections; edited data pending re-closure |

---

## State Transitions (Current - Implicit)

### Transition Map

| From | To | Trigger | Implemented Where | Side Effects |
|---|---|---|---|---|
| **ABERTO** (no row) | **PRONTO** | User clicks "Prepare" button (Reports page) | Server action: `prepareMonthForClosure` | Data validated; `financial_month_closures` row created with `is_locked=false` |
| **PRONTO** (is_locked=false) | **FECHADO** (is_locked=true) | User clicks "Close Month" button | Server action: `closeMonth` | Month data archived in `snapshot`; `is_locked=true`; notifications sent |
| **FECHADO** (is_locked=true) | **REABERTO** (is_locked=true) | User clicks "Reopen Month" button (Reports page) | Server action: `reopenMonth` | `reopened_count` incremented; data becomes mutable again; status badge changes |
| **REABERTO** | **FECHADO** | User clicks "Close Month" again after corrections | Server action: `closeMonth` | Snapshot updated; data re-archived; `is_locked=true` |
| (any) | **ABERTO** | User deletes month closure record (edge case) | Direct DB call (not recommended) | Month reverts to open state; data becomes fully mutable |

### Transition Rules & Guards

#### ABERTO → PRONTO
- **Preconditions**:
  - No existing `financial_month_closures` record for this month
  - All transactions have `reference_date` within month range
  - All transactions marked `is_verified = true` (if configured)
  - Reconciliation data exists and balances
- **Guard**: Checked via `readFinanceMonthReadiness()` function
- **Failure behavior**: User sees error message; month remains ABERTO
- **Side effects**: 
  - Create `financial_month_closures` row with `is_locked=false`
  - Record finance event for audit trail
  - Update dashboard status badge

#### PRONTO → FECHADO (Close)
- **Preconditions**:
  - `financial_month_closures` record exists with `is_locked=false`
  - (No additional validation; assumes PRONTO preconditions still met)
- **Guard**: Checked via simple row lookup
- **Failure behavior**: User sees error if record not found
- **Side effects**:
  - Set `is_locked=true`
  - Save transaction snapshot in `snapshot` JSON field
  - Set `closed_at` timestamp
  - Send email notifications to team
  - Record audit event: "finance.month.closed"
  - Revalidate dashboard and reports pages
- **CRITICAL GAP**: No verification that data hasn't changed since PRONTO transition

#### FECHADO → REABERTO (Reopen)
- **Preconditions**:
  - `financial_month_closures` record exists with `is_locked=true`
  - User has admin role
  - (No limit on number of reopens documented)
- **Guard**: Check `is_locked=true` and user role
- **Failure behavior**: User sees error if not locked or insufficient role
- **Side effects**:
  - Increment `reopened_count`
  - Set `closed_at` to null (or record new timestamp)
  - Keep `is_locked=true` but conceptually "unlock" for editing
  - Record audit event: "finance.month.reopened"
  - Update dashboard status badge
  - **IMPLICIT BEHAVIOR**: UI shows "Reaberto" badge; business logic allows transaction editing; but `is_locked=true` in database

#### REABERTO → FECHADO (Re-close)
- Same as PRONTO → FECHADO
- Snapshot is updated with corrected data

---

## Where State is Checked in Code

### Frontend State Guards

**File**: `app/admin/finance/page.tsx` (Dashboard)
```typescript
const isMonthLocked = data.month.isLocked;           // From aggregator
const isReopenedMonth = data.month.isReopened;       // Derived: isLocked && reopened_count > 0
```

**File**: `app/admin/finance/transactions/page.tsx` (Ledger)
```typescript
const { data: closure, error: closureError } = await supabase
  .from("financial_month_closures")
  .select("is_locked")
  .eq("project_id", project.id)
  .eq("month_key", monthRange.monthKey)
  .maybeSingle();
const isLocked = !closureError && Boolean(closure?.is_locked);
```

**File**: `app/admin/finance/inbox/page.tsx` (Inbox)
```typescript
const { data: lockedRows, error: lockedError } = await supabase
  .from("financial_month_closures")
  .select("id")
  .eq("month_key", monthKey)
  .eq("is_locked", true)
  .limit(1);
if (!lockedError && lockedRows && lockedRows.length > 0) {
  // Month is locked; block posting operation
}
```

### State-Based Access Control

| Operation | ABERTO | PRONTO | FECHADO | REABERTO |
|---|---|---|---|---|
| **Create transaction** | ✅ Allowed | ✅ Allowed | ❌ Blocked | ✅ Allowed (after reopen) |
| **Edit transaction** | ✅ Allowed | ✅ Allowed | ❌ Blocked | ✅ Allowed (after reopen) |
| **Mark verified** | ✅ Allowed | ✅ Allowed | ❌ Blocked | ✅ Allowed (after reopen) |
| **View month** | ✅ Allowed | ✅ Allowed | ✅ Read-only | ✅ Allowed (editable) |
| **Close month** | ❌ Not shown | ✅ Shown (action button) | ❌ Already locked | ✅ Shown (re-close button) |
| **Reopen month** | ❌ Not shown | ❌ Not shown | ✅ Shown (action button) | ❌ Already reopened |
| **Access snapshot** | ✅ Draft | ✅ Draft | ✅ Official | ✅ Updated draft |

---

## n8n Integration (Current - Implicit)

### Current Webhook Architecture

**Location**: Not found in Finance UI codebase  
**Status**: Referenced but undocumented

The codebase mentions n8n integration:
- `billing/invoices/[invoiceId]/page.tsx` line 151: "Supabase guarda o estado. n8n so executa os comandos externos e devolve eventos normalizados."
- `billing/page.tsx` line 279: "Enfileirado no n8n" (Queued in n8n)

**Implication**: n8n is responsible for:
- External posting (GL journal entries, accounting system integration)
- Webhook orchestration
- Event normalization

**Critical Gap**: The month closure state machine does **not** integrate with n8n posting. The workflow is:
1. User closes month in UI (sets `is_locked=true`)
2. Data is archived in `snapshot`
3. **No automatic webhook call** (this is the critical gap #2 from Phase 2)

---

## Business Logic Rules (Current - Implicit)

### Reconciliation Rules

**Where checked**: `aggregateFinanceOverview()` and `readFinanceMonthReadiness()`  
**Rule**: Before transitioning to PRONTO, reconciliation must balance

```
total(transactions by category) == expected_gl_balance
Tolerance: ±0.01 (configurable, not documented)
```

**Current behavior**: 
- If unbalanced, month cannot transition to PRONTO
- Dashboard shows "Pendencia de conciliacao" blocker
- No automatic retry or escalation documented

### Receipt/Document Requirements

**Where checked**: Before marking transaction as verified  
**Rule**: Non-journal transactions must have `source_file_url` set

**Current behavior**:
- UI allows marking unverified if document missing (no hard block)
- **IMPLICIT**: System expects user to attach documents before verification
- No validation prevents submitting incomplete data

### Transaction Mutability Rules

**Where enforced**: Server actions check `is_locked` flag  
**Rules**:
- If month `is_locked=true`, all edit operations blocked
- If month `is_locked=false` or `is_locked=null`, edits allowed
- No field-level immutability (e.g., can change amount after verification)

### Access Control

**Role-based**: Only `admin` role can perform state transitions  
**Current behavior**: No distinction between:
- Finance reviewer (should approve closure)
- Finance director (should authorize final closure)
- Accountant (should enter transactions)

---

## Data Invariants (Current - Implicit)

### Per-Month Invariants

| Invariant | Enforced Where | If Violated |
|---|---|---|
| Only one active closure record per month | Supabase unique constraint (implied) | Duplicate closure rows possible |
| All transactions in month have valid dates | UI validation + server-side not enforced | Invalid transactions could exist |
| Month key matches transaction dates | Server action validation | Transactions could span months |
| Snapshot is immutable once `is_locked=true` | Code logic (no DB constraint) | Snapshot could be modified |
| `reopened_count` matches number of reopens | Code logic | Count could drift from reality |

### Data Integrity Issues

1. **No CHECK constraints** at database level
   - `is_locked` flag could have inconsistent meaning
   - Could create states like `is_locked=true, reopened_count=0` (locked but not reopened?) 

2. **No FOREIGN KEY cascade rules** documented
   - If project deleted, what happens to month closures?
   - If transaction deleted, snapshot still contains it

3. **No transaction boundaries**
   - If `close month` action fails halfway, month could be in undefined state

---

## Error Handling (Current - Implicit)

### Scenario: User Closes Month, n8n Webhook Fails

**Current behavior**: **UNKNOWN** (undocumented)

Likely scenarios:
1. Month is already set `is_locked=true` by time webhook is called
2. If webhook fails, month is locked but external posting didn't happen
3. No recovery mechanism documented
4. User doesn't know if posting succeeded externally

### Scenario: User Reopens Month, Data Changed Externally

**Current behavior**: No validation that snapshot represents current state  
**Risk**: Reopened month could have different transactions than snapshot

### Scenario: Duplicate Close Month Click

**Current behavior**: Second click would find existing row with `is_locked=true` and show error  
**Issue**: No idempotency key; could have race conditions

---

## Issues With Current Approach

### Issue 1: Single Boolean for Multiple Concepts

Using `is_locked` to represent both "has been closed" and "is currently locked" is ambiguous.

```
is_locked=true could mean:
  a) Month is officially closed (immutable)
  b) Month was closed and reopened (mutable, in correction mode)
  c) Month closure transaction is in-flight (uncertain state)
```

This leads to conditional logic like:
```typescript
if (isLocked && reopened_count > 0) {
  // Month is reopened; allow edits
} else if (isLocked) {
  // Month is locked; block edits
}
```

### Issue 2: No Explicit State Names

Operators must infer state from flags:
- Dashboard labels ("Pronto", "Fechado") are UI labels, not state identifiers
- Code checks are inconsistent: sometimes check `is_locked`, sometimes check `is_locked && reopened_count`
- New engineers don't know valid state combinations

### Issue 3: No Transition Validation

Current code does not explicitly validate transitions:
```
// This code accepts: ABERTO → FECHADO directly (skipping PRONTO)
const { error } = await supabase
  .from("financial_month_closures")
  .insert({ month_key, is_locked: true });
```

Should be:
```
// Validate current state before transition
const current = await supabase
  .from("financial_month_closures")
  .select("is_locked")
  .eq("month_key", month_key);

// Only allow ABERTO → PRONTO or PRONTO → FECHADO
if (current.is_locked !== null) {
  throw new Error("Invalid state transition");
}
```

### Issue 4: No n8n Integration in State Machine

The month closure flow is:
1. Close month locally (set `is_locked=true`)
2. Snapshot data
3. **Then what?** External posting not documented

This violates Saga/transaction pattern: either whole transaction completes (UI + external) or none completes.

---

## Phase 2 Interview Validation

### Finance Expert Interview

**Q1: Month closure state machine?**
> "Open, Review, Ready, Posted. But the system doesn't explicitly track Review and Ready states."

**Q2: What confuses you?**
> "The Pronto status doesn't clearly mean 'ready to post.' Is it validated? Is it locked? Unclear."

**Validation**: Confirmed implicit state machine is confusing to domain experts.

### Engineer Interview

**Q1: How does month closure work?**
> "Boolean flag sets is_locked=true, data goes in snapshot. But if n8n fails halfway through external posting, the state is unclear."

**Q2: What would help?**
> "Explicit state machine with documented transitions. And n8n contract showing what happens on success/failure."

**Validation**: Engineer confirmed lack of explicit state machine is architectural debt.

### Product Manager Interview

**Q1: User mental model of month closure?**
> "Users think: entry → review → ready → posted. But the UI doesn't show these steps clearly. Status badge is confusing."

**Q2: What would improve UX?**
> "Clear status badges that show current state. And error messages when transition fails."

**Validation**: Product manager identified UX consequence of implicit state machine.

---

## Summary: Current State Machine

### States Identified
- **ABERTO**: No closure record; month fully mutable
- **PRONTO**: Closure record exists with `is_locked=false`; ready for official closure
- **FECHADO**: Closure record with `is_locked=true`; immutable
- **REABERTO**: Closure record with `is_locked=true` and `reopened_count > 0`; mutable for corrections

### Transitions Identified
- ABERTO → PRONTO (Prepare month)
- PRONTO → FECHADO (Close month)
- FECHADO → REABERTO (Reopen month)
- REABERTO → FECHADO (Re-close month)

### Critical Gaps
1. **No formal state machine specification** — States are implicit; valid transitions not documented
2. **n8n integration missing** — No contract for webhook calls, error handling, or retry logic
3. **No explicit state in database** — Using flags instead of enum; allows invalid state combinations
4. **No transaction boundaries** — Close operation not atomic; could fail halfway
5. **No role-based state transitions** — Can't distinguish reviewer approval from director authorization
6. **No idempotency guarantees** — Duplicate requests could cause duplicate state changes

---

## Next Steps: Workstream 1 Tasks

- [ ] Task 2: Define explicit state machine spec
- [ ] Task 3: Define business rules and constraints
- [ ] Task 4: Integrate with UX and Technical workstreams
- [ ] Task 5: Create final Domain Model Specification

---

## Appendix: Code Evidence

### Evidence 1: State Check Pattern

**File**: `transactions/page.tsx:105-111`
```typescript
const { data: closure, error: closureError } = await supabase
  .from("financial_month_closures")
  .select("is_locked")
  .eq("project_id", project.id)
  .eq("month_key", monthRange.monthKey)
  .maybeSingle();
const isLocked = !closureError && Boolean(closure?.is_locked);
```

### Evidence 2: Implicit Reopened State

**File**: `page.tsx:195-196`
```typescript
const isMonthLocked = data.month.isLocked;
const isReopenedMonth = data.month.isReopened; // Inferred, not explicit
```

### Evidence 3: State-Based Access Control

**File**: `transactions/page.tsx:689-694`
```typescript
{isLocked ? (
  <span className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-500/10 ...">
    <Lock className="w-4 h-4" />
    Mês fechado
  </span>
) : null}
```

---

**Document Status**: Ready for Task 2 (Explicit State Machine Specification)  
**Next Review**: After Phase 3 workstreams produce feedback
