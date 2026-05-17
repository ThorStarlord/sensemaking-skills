# UX-Domain Sync: Validating UX Against State Machine

**Execution Date**: 2026-05-17  
**Methodology**: Validation of proposed UX against domain state machine spec  
**Note**: Domain state machine spec from Workstream 1 (under development)  
**Status**: PRELIMINARY - Awaiting full Domain Model spec for final validation

---

## Executive Summary

The proposed UX architecture (Month Overview with 3 tabs, consolidated navigation) aligns well with anticipated domain state machine requirements. Key validation points:

1. ✅ **State visibility**: UI correctly shows month state through badge + disabled buttons
2. ✅ **Operation constraints**: UI respects state-based operation restrictions
3. ✅ **Terminology alignment**: State names will map to user-friendly labels
4. ⚠️ **Error handling**: Need clarification on error states and recovery UI
5. ⚠️ **Audit trail**: Need verification that audit events match domain requirements

---

## State Machine Overview (From Workstream 1 Plan)

Based on phase 3 workstream plan, the anticipated domain state machine is:

```
States:
- ABERTO (Open): Month accepting transactions
- EM_REVIEW (In Review): Month locked for review
- PRONTO (Ready): Approved and ready for posting
- POSTADO (Posted): Final state, immutable

Transitions:
ABERTO ↔ EM_REVIEW → PRONTO → POSTADO
```

---

## UX Validation: State Transitions

### State 1: ABERTO (Open)

**Domain rules**:
- ✅ Create transactions allowed
- ✅ Edit transactions allowed
- ✅ Delete transactions allowed
- ❌ Post to GL blocked
- ❌ Send to review blocked (if balance unmatched)

**UX implementation**:

```
Month Overview Header:
┌──────────────────────────────────────────┐
│ May 2026  [Status Badge: Open]           │
├──────────────────────────────────────────┤
│ [Send to Review] [Post ❌]               │
│                  ↑ Button disabled       │
│                  Tooltip: "Month must be │
│                  approved first. Click   │
│                  'Send to Review'."      │
└──────────────────────────────────────────┘

Inbox Tab:
[✓ Upload documents allowed]
[✓ Manual entry allowed]
[Extracted data editable]

Transactions Tab:
[✓ Edit button active]
[✓ Delete button active]
[Verify status editable]
```

**Validation**: ✅ ALIGNED
- Edit buttons enabled
- Post button disabled with explanation
- Send to Review button visible and enabled

---

### State 2: EM_REVIEW (In Review)

**Domain rules**:
- ❌ Create transactions blocked
- ❌ Edit transactions blocked
- ❌ Delete transactions blocked
- ✅ View all data
- ✅ View reconciliation
- ✅ Approve (→ PRONTO) or Reject (→ ABERTO)

**UX implementation**:

```
Month Overview Header:
┌──────────────────────────────────────────┐
│ May 2026  [Status Badge: In Review ⚠️]  │
├──────────────────────────────────────────┤
│ [Approve ✓] [Reject ❌] [Post ❌]        │
│              ↑ New action               │
│              Approve month for posting   │
└──────────────────────────────────────────┘

Inbox Tab:
[❌ Upload disabled]
Tooltip: "Month is under review. Edits are locked."
[❌ Manual entry disabled]
[Extracted data read-only]

Transactions Tab:
[❌ Edit button disabled]
Tooltip: "Cannot edit while month is in review."
[❌ Delete button disabled]
[✓ View button active]
[✓ Verify checkbox active (view-only verification)]
```

**Validation**: ✅ ALIGNED
- All edit operations disabled with clear tooltips
- Approve/Reject actions visible
- Transactions read-only but viewable

**Potential UX Gap**: 
- How does reviewer reject? Expect: Click "Reject" → Month reverts to ABERTO + optionally add rejection reason
- Need clarification on rejection workflow from Domain spec

---

### State 3: PRONTO (Ready to Post)

**Domain rules**:
- ❌ All edit operations blocked (strictly immutable)
- ✅ Trigger posting to GL
- ✅ View month data
- ✅ View posting status

**UX implementation**:

```
Month Overview Header:
┌──────────────────────────────────────────┐
│ May 2026  [Status Badge: Ready to Post] │
├──────────────────────────────────────────┤
│ [Post to GL ✓]                          │
│ [Reopen ❌] (maybe for emergency revert?)│
└──────────────────────────────────────────┘

Inbox Tab:
[❌ All operations disabled]
[Read-only view]

Transactions Tab:
[❌ All operations disabled]
[Read-only view]

Details Tab:
[✓ Show posting status]
[✓ Show GL posting ID (once successful)]
[✓ Show error if posting failed + retry option]
```

**Validation**: ✅ ALIGNED
- All edit operations disabled
- Post action primary button
- Read-only view of data

**Potential UX Gap**:
- What happens if posting fails? Expect: Error message + retry button, but does month stay in PRONTO or revert to EM_REVIEW?
- Need clarification from Domain spec on error handling

---

### State 4: POSTADO (Posted)

**Domain rules**:
- ❌ All operations blocked (archive/immutable)
- ✅ View data (read-only)
- ✅ Download audit report
- ✅ Access historical data

**UX implementation**:

```
Month Overview Header:
┌──────────────────────────────────────────┐
│ May 2026  [Status Badge: Posted ✓]       │
├──────────────────────────────────────────┤
│ [Download Report] [View GL Entry]        │
│ All other buttons hidden                 │
└──────────────────────────────────────────┘

Inbox Tab:
[❌ All operations disabled]
[Read-only archive view]
[Note: "(Archived for compliance)"]

Transactions Tab:
[❌ All operations disabled]
[Read-only view]
[✓ Show reconciliation metadata]
[✓ Show GL posting ID and timestamp]

Details Tab:
[✓ Show complete audit trail]
[✓ Show GL posting confirmation]
[✓ Download report link]
```

**Validation**: ✅ ALIGNED
- All operations disabled
- Data archived and immutable
- Audit trail accessible

---

## UX Validation: Operation Constraints

### Transaction Edit Operation

**Domain rule**: Can only edit transactions in ABERTO state

**UX implementation**:
```
Transactions Tab:

If state == ABERTO:
  [Edit button ✓ enabled]

If state == EM_REVIEW:
  [Edit button ❌ disabled]
  Tooltip: "Cannot edit transactions while month is under review. 
           Reject the month to make changes."

If state == PRONTO or POSTADO:
  [Edit button ❌ disabled]
  Tooltip: "This month has been approved. 
           To make changes, reopen the month (emergency only)."
```

**Validation**: ✅ ALIGNED

---

### Document Upload Operation

**Domain rule**: Can only upload documents in ABERTO state

**UX implementation**:
```
Inbox Tab:

If state == ABERTO:
  [Upload button ✓ enabled]
  [Manual entry form ✓ enabled]

If state == EM_REVIEW or later:
  [Upload button ❌ disabled]
  Tooltip: "Month is locked. You cannot add new documents 
           while in review. Ask accountant to reopen month."
```

**Validation**: ✅ ALIGNED

---

### Month Approval Operation

**Domain rule**: Can transition from EM_REVIEW → PRONTO only if:
- All transactions have supporting documents
- Reconciliation variance within tolerance (±0.01)
- No disputed transactions

**UX implementation**:
```
Month Overview Header:

If state == EM_REVIEW:
  IF (all_preconditions_met):
    [Approve ✓ enabled]
  ELSE:
    [Approve ❌ disabled]
    Tooltip: "Cannot approve:
      • 3 transactions missing documents
      • Reconciliation variance: R$15.27
      2 disputed transactions"
```

**Validation**: ✅ ALIGNED

---

## UX Validation: Error States

### Critical Gap: Error State Handling

**Domain spec** (from plan) specifies error scenarios:
- n8n webhook timeout → Month stays in PRONTO, retry available
- Validation error → Month stays in PRONTO, user fixes issues
- GL posting error → Month reverts? Or stays in PRONTO?

**Current UX proposal**: 
```
Details Tab:

If posting_in_progress:
  [⏳ Posting to GL in progress...]
  [Loading spinner]

If posting_error:
  [❌ Posting failed]
  [Error message from n8n]
  [Retry button ✓]
  [View logs button]

If posting_success:
  [✓ Posted successfully to GL]
  [GL posting ID: GL-2026-05-001]
  [Posting timestamp]
```

**Validation**: ⚠️ PARTIAL
- ✅ Success state UI defined
- ✅ Error message display
- ❌ Missing: What state is month in if error occurs?
  - Does it revert to EM_REVIEW? Or stay in PRONTO?
  - Can user click "Approve" again to retry?
- ❌ Missing: Timeout handling UI (async operation visibility)

**Recommendation**: Wait for Domain spec on error handling, then update Details tab accordingly.

---

## UX Validation: State Indicators

### Current UX Proposal for State Visibility

```
1. State Badge (Header)
   [May 2026] [Status: Open | In Review | Ready | Posted]
   
2. Disabled Buttons + Tooltips
   [Edit ❌] Tooltip: "Cannot edit while in review"
   
3. Section Headers with State Context
   Inbox Tab: "Source Documents (Read-only during review)"
   Transactions Tab: "GL Entries (Locked in review state)"
   
4. Progress Checklist (Details Tab)
   ✓ Prepare review queue
   ✓ Auto-post items
   ○ Verify transactions (current step based on state)
   ○ Reconcile statement
   ○ Approve for posting
```

**Validation**: ✅ ALIGNED
- State is visible at top (badge)
- Operations disabled at point of action (buttons)
- Context provided through tooltips
- Progress shown in Details tab

---

## Terminology Alignment: State Names

### Domain Names → UX Labels

| Domain State | Domain Meaning | UX Label | UX Meaning | Why |
|---|---|---|---|---|
| ABERTO | Open | "Open" | Month accepting edits | Clear and simple |
| EM_REVIEW | In Review | "In Review" | Month locked for validation | Action-oriented |
| PRONTO | Prepared | "Ready to Post" | Approved, waiting for posting | Action-oriented, clear |
| POSTADO | Posted | "Posted to Ledger" | Final, immutable state | Specific to GL posting context |

**Validation**: ✅ ALIGNED
- Domain terminology preserved in code
- UX terminology aligned with user mental models
- Clear mapping between domain and UX

---

## UX Validation: Audit Trail

### Domain Requirement (Anticipated)

The Domain Model spec will require:
- All state transitions logged with: user, timestamp, reason
- All financial operations logged: create, edit, delete, verify, reconcile
- GL posting confirmation logged

### UX Implementation

```
Details Tab → Audit Trail Section

[Filter by action type]

Timeline view:
┌────────────────────────────────────────────┐
│ 2026-05-17 14:30  [Accountant John]        │
│ "Sent May for review"                      │
│ 847 transactions, balanced, ready          │
├────────────────────────────────────────────┤
│ 2026-05-17 15:45  [Reviewer Jane]          │
│ "Approved May for posting"                 │
│ All checks passed, no exceptions           │
├────────────────────────────────────────────┤
│ 2026-05-18 09:00  [System: n8n webhook]    │
│ "Posted to GL"                             │
│ GL posting ID: GL-2026-05-001              │
└────────────────────────────────────────────┘
```

**Validation**: ✅ ALIGNED
- Audit trail shows state transitions
- User actions logged
- Timestamps present
- Ready for compliance

---

## UX Validation: Data Invariants

### Domain Rule: Invariants

State-specific data invariants (from Domain plan):

| State | Invariant | UX Validation |
|---|---|---|
| ABERTO | All txns must have date + amount | No UI constraint (user error) |
| EM_REVIEW | All txns must have document | UI blocks approval if violated |
| PRONTO | Reconciliation variance ≤ 0.01 | UI blocks approval if violated |
| POSTADO | Immutable snapshot | UI read-only, no changes allowed |

**Current UX**:
```
Details Tab → Pre-approval Checklist

[Approve button]
  ↓ Click
[Validation check]
  IF (missing_documents):
    Error: "3 transactions missing documents. 
           Add documents before approving."
  IF (reconciliation_variance > 0.01):
    Error: "Reconciliation variance R$2.15. 
           Must reconcile before approving."
  IF (disputed_transactions):
    Error: "2 transactions marked as disputed."
  
  IF (all_checks_pass):
    [Confirm approval] → State transition to PRONTO
```

**Validation**: ✅ ALIGNED
- UI enforces invariants at state transition point
- Clear error messages for why approval failed
- User can fix issues and retry

---

## Potential Conflicts & Resolutions

### Conflict 1: Rejection Workflow

**Domain question**: When reviewer rejects a month in EM_REVIEW, does it go back to ABERTO?

**Current UX**: Yes, "Reject" button returns to ABERTO

**Need verification from Domain spec**:
- Should rejection require a reason/comment?
- Should the month show "Reopened with rejection reason"?
- Who gets notified of rejection?

**Proposed UX resolution** (pending Domain spec):
```
EM_REVIEW state:

[Reject button]
  ↓ Click
[Modal dialog]
  Reason (textarea, required):
  "Please check transaction #5 - amount doesn't match invoice"
  
  [Cancel] [Reject]
  
  ↓ Confirm
  Month → ABERTO
  Accountant gets notification with reason
  Audit log: "Rejected by Jane: amount mismatch on txn #5"
```

---

### Conflict 2: Posting Error Recovery

**Domain question**: If GL posting fails, what state is month in?

**Current UX assumption**: Month stays in PRONTO, showing error + retry

**Need verification from Domain spec**:
- Should there be a timeout? (e.g., if posting hasn't completed in 2 hours)
- Should there be automatic retry with backoff?
- Should month revert to EM_REVIEW if posting fails permanently?

**Proposed UX resolution** (pending Domain spec):
```
PRONTO state:

Posting in progress:
  Details Tab shows:
  [⏳ Posting to GL in progress...]
  [Estimated time: 2-5 minutes]

If posting succeeds within timeout:
  [✓ Posted successfully]
  Month → POSTADO

If posting times out after 30 minutes:
  [❌ Posting timeout]
  [Manual retry button] OR
  [Automatic retry in 5 minutes]

If posting fails permanently:
  [❌ Posting failed - GL rejected]
  [Error: "Account 5100 does not exist"]
  [Options: Reopen month / Contact GL admin]
```

---

### Conflict 3: Emergency Reopen

**Domain question**: Can a director reopen a POSTADO month?

**Current UX**: No option to reopen POSTADO (immutable)

**Need verification from Domain spec**:
- Is month reopen allowed in PRONTO state? (Yes, under "Request exception" flow)
- Is month reopen allowed in POSTADO state? (Should be rare emergency only)
- Who has permission to reopen?

**Proposed UX resolution** (pending Domain spec):
```
PRONTO state:
  [Reopen month] (maybe hidden by default, under "Advanced" menu)
  
  Tooltip: "Reopen month only if error found. 
           Requires director approval and creates audit log entry."

POSTADO state:
  No reopen option (hidden)
  
  Instead, offer: "Create reversal entry" workflow
    → New month for correction entries
    → Original month stays immutable
```

---

## Validation Summary

### Green Light ✅ (Validated, no changes needed)
- State visibility through badge and disabled buttons
- Operation constraints enforced by UI
- Terminology mapping clear and user-aligned
- Audit trail structure sound
- Data invariants checked at transitions

### Yellow Light ⚠️ (Validated, need clarification)
- Rejection workflow (need rejection reason flow)
- Posting error handling (timeout, retry, state reversion)
- Emergency reopen procedures (permission model, audit)

### Blockers Identified 🚫
- None; UX can proceed with assumptions pending Domain spec clarification

---

## Next Steps

1. **Await Domain Model spec** (Workstream 1) completion
2. **Cross-reference** this UX doc with final Domain spec
3. **Resolve yellow-light conflicts** with Domain team
4. **Update UX doc** with finalized error handling and recovery flows
5. **Implement** UI reflecting finalized state machine

---

## Sign-Off (Pending Domain Validation)

**UX Lead**: [Pending signature after Domain spec review]  
**Domain Lead**: [Pending signature after UX validation]  
**Technical Lead**: [Pending signature after implementation feasibility check]

