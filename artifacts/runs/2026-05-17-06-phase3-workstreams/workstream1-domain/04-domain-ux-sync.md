# Domain-UX Synchronization Document

**Date**: 2026-05-17  
**Workstream 1 & 2 Sync**: Domain Model ↔ UX Specification  
**Purpose**: Validate that explicit state machine aligns with user expectations and UX flows  
**Reviewers**: Product Manager (Beatriz Santos), Designer, Backend Engineer  

---

## Executive Summary

This document validates that Workstream 1's explicit domain model (4-state machine, business rules, n8n integration) is **implementable in UX** and **matches user mental models** from Phase 2 operator interviews.

**Validation Approach**:
1. Map each state to UX screens/workflows
2. Validate transitions against user actions
3. Identify new UX requirements (e.g., EM_REVIEW screens)
4. Ensure error messages align with business rules
5. Confirm status labels are unambiguous

**Key Finding**: The 4-state machine (ABERTO, EM_REVIEW, PRONTO, POSTADO) aligns well with operator mental models. **EM_REVIEW state introduction enables** clearer responsibility boundaries (accountant enters → director approves) that users requested.

---

## State-to-UX Mapping

### State 1: ABERTO (Open)
**Meaning**: Month is open for transaction entry and editing

**Current UX Implementation**: ✅ Exists
- Dashboard shows month with no closure badge
- "Livro-Caixa" (Ledger) page shows full CRUD buttons (Create, Edit, Delete)
- "Pendencias de captura" inbox shows active items
- Transaction sheet modal open for new entries
- "Preparar" (Prepare/Send to Review) button shown on Reports page (when all preconditions met)

**Domain Requirement**: No `financial_month_closures` record exists  
**UX Alignment**: ✅ Correct — No closure indicator shown

**Gaps Identified**: None

**Recommendation**: Keep as-is

---

### State 2: EM_REVIEW (In Review)
**Meaning**: Month is under finance director review. Data locked for editing.

**Current UX Implementation**: ❌ **Missing** (Critical Gap)
- No distinct "In Review" status badge
- No review-specific screens
- No clear "under review" workflow

**Domain Requirement**: 
- All transactions must be verified
- All documents attached
- Reconciliation passed
- Finance director in approval phase
- Transactions locked from editing (except admin override)

**Required UX Changes**:

1. **Dashboard Status Badge**
   - New badge: "Em Revisão" (In Review) — orange/yellow tone
   - Shows director name and review start time
   - Shows "Approve" and "Reject" buttons (director only)

2. **New Screen: Review Approval**
   - Lists all transactions with verification status
   - Shows each document status (attached, readable)
   - Shows reconciliation variance (if any)
   - Variance report table (budget performance by department)
   - Two-action CTA: "Approve for Posting" or "Reject & Return to Editing"
   - Optional: Review notes text field

3. **Ledger Page Changes**
   - Status: "Em Revisão" badge replacing "Aberto"
   - All edit buttons disabled
   - All delete buttons disabled
   - Read-only mode for all transactions
   - Message: "Month under review. Editing disabled."
   - (Optional) Show "Request Override" button for admin

4. **Notification Changes**
   - When sent to review: Notify director "Month 2026-05 ready for approval (5 transactions)"
   - When approved: Notify accounting team "Month 2026-05 approved. Ready to post to GL."
   - When rejected: Notify accountant with specific rejection reasons

**UX Alignment**: ⚠️ **Requires New Screens**
- Recommended: Add "Revisão" tab to Reports page
- Alternative: Add modal/drawer for approval workflow
- Risk: Adds navigation complexity; must keep clear

**Recommendation**: 
- Create dedicated approval modal or drawer (not new tab)
- Keep on Reports page workflow
- Show review state on dashboard (not just Reports)

---

### State 3: PRONTO (Ready)
**Meaning**: Month approved for posting. Ready to trigger GL posting.

**Current UX Implementation**: ✅ Exists (partially)
- Reports page shows "Status: Pronto" badge
- "Relatorios" quick link shows status

**Domain Requirement**:
- All prior EM_REVIEW invariants still hold
- Idempotency key generated
- Ready for n8n webhook call
- Data is read-only

**Current UX Limitation**: No explicit "post to GL" button
- System doesn't document how/when posting happens
- No user visibility into GL posting status
- Phase 2 operators asked "How do we know if posting succeeded?"

**Required UX Changes**:

1. **Dashboard Status Badge**
   - "Pronto" badge (indigo tone)
   - Shows approval timestamp
   - Shows "Post to GL" button (if not yet posted)

2. **Reports Page**
   - Show "Post to GL" button
   - After posting: Show GL posting ID and timestamp
   - Show posting status: "Posting in progress..." → "Posted successfully" → "Posting failed"
   - If failed: Show error details + "Retry" button

3. **Posting Progress UI**
   - When user clicks "Post to GL": Show spinner + "Posting month to GL..."
   - Wait 30s for response (matches timeout in domain spec)
   - On success: "Posted successfully. GL ID: GL-2026-05-00123"
   - On timeout: "Posting is taking longer than expected. Checking GL system status..."
   - On failure: "Posting failed: {error message}. Retry?"

4. **Status Badge Lifecycle**
   - Before posting: "Pronto" (indigo)
   - During posting: "Enviando..." (gray/loading)
   - After success: "Postado" (green)
   - After failure: "Erro no envio" (red) + Retry button

**UX Alignment**: ⚠️ **Requires New Features**
- Currently no GL posting visibility
- Need to add posting button and status tracking
- Domain spec clarifies what should happen

**Recommendation**:
- Add "Post to GL" button to Reports page (visible in PRONTO state only)
- Add posting status indicator showing GL posting ID
- For timeout handling: Show "Checking GL system..." message (user-friendly)
- Add audit log showing posting timestamp and GL ID

---

### State 4: POSTADO (Posted)
**Meaning**: Month officially posted to GL. Data immutable and archived.

**Current UX Implementation**: ✅ Exists
- Reports page shows "Status: Fechado" badge
- Month data is read-only

**Domain Requirement**:
- GL posting ID recorded
- Snapshot immutable
- Reopen option available (if reopened_count < 5)

**Current UX Limitation**: "Fechado" label is confusing
- Operators in Phase 2 complained: "Does 'Fechado' mean locked, archived, or posted?"
- Should be "Postado" (Posted) to match domain spec terminology

**Required UX Changes**:

1. **Terminology Update**
   - Change badge from "Fechado" to "Postado" (Posted)
   - Shows GL posting ID and timestamp
   - Shows "Posted on 2026-05-17 at 15:23"

2. **Reopen Workflow**
   - If reopened_count < 5: Show "Reopen for Corrections" button
   - If reopened_count >= 5: Show "Cannot reopen (limit reached). Contact director."
   - When clicked: Modal asking for "Reason for reopening"
   - After reopen: Month transitions to ABERTO; ledger shows full edit mode

3. **Alert for Multiple Reopens**
   - If reopened_count >= 3: Show alert "This month has been reopened 3 times. Any issues?"
   - Director sees alert during reopen attempt

**UX Alignment**: ✅ **Minor terminology change**
- Update label "Fechado" → "Postado"
- Add reopen button (already partially exists in domain)
- Add reopened_count counter and alerts

**Recommendation**:
- Rename badge to "Postado" for clarity
- Add GL posting ID display
- Keep reopen button visible (low risk)
- Add alert for 3+ reopens

---

## Transition Workflows

### Workflow 1: ABERTO → EM_REVIEW (Send to Review)

**User Action**: Finance accountant clicks "Preparar" (Prepare) button on Reports page

**Precondition Checks**:
- All transactions verified ✅
- All documents attached ✅
- Reconciliation balanced ✅

**UX Flow**:
1. User on Reports page, sees month status "Aberto"
2. User clicks "Preparar" button
3. System shows loading spinner "Enviando para revisão..."
4. On success: Toast "Month sent for review"
5. Dashboard updates: Badge changes to "Em Revisão"
6. Transaction ledger becomes read-only
7. Director receives notification email

**Error Scenarios**:
1. **Precondition fails** (e.g., unverified transactions):
   - Toast error: "Cannot send to review: 3 transactions still unverified"
   - Link: "Fix in Livro-Caixa" (takes to ledger filtered to unverified)
   
2. **Reconciliation fails**:
   - Toast error: "Reconciliation variance: R$ 47.33"
   - Link: "Fix in Conciliação" (takes to reconciliation page)
   
3. **Network error**:
   - Retry toast: "Send to review again?"
   - Background: System auto-retries after 5s

**UX Alignment**: ✅ **Mostly exists**
- Button text "Preparar" → suggest rename to "Enviar para Revisão" (Send for Review) for clarity
- Error messages should be more specific (not generic "Error preparing month")

**Recommendation**:
- Keep flow as-is
- Improve error messages (reference specific blockers)
- Rename button to "Enviar para Revisão"

---

### Workflow 2: EM_REVIEW → PRONTO (Approve)

**User Action**: Finance director clicks "Approve" on Review page

**Precondition Checks**:
- Month still in EM_REVIEW state
- All EM_REVIEW invariants still hold
- Director has "admin" role (or new "finance_reviewer" role in Phase 4)

**UX Flow**:
1. Director navigates to Reports page
2. Sees "Em Revisão" badge with "Aprovar" (Approve) button
3. Director reviews month summary (transactions, documents, reconciliation)
4. Director clicks "Aprovar"
5. (Optional) Modal asks for "Review Notes" (optional text field)
6. System shows loading spinner "Aprovando..."
7. On success: Toast "Month approved for posting"
8. Badge changes to "Pronto" (indigo)
9. "Post to GL" button now visible
10. Accounting team receives notification email

**Error Scenarios**:
1. **Data changed since review started**:
   - Error: "Cannot approve. Data changed. Please review again."
   - Action: Refresh and re-review

2. **Invariant violation discovered**:
   - Error: "Reconciliation variance detected: R$ 23.50. Return to editing?"
   - Action: Reject and return to ABERTO

**UX Alignment**: ✅ **New — needs implementation**
- No current screen for approval
- Recommend: Modal on Reports page or new "Revisão" tab

**Recommendation**:
- Add approval modal to Reports page
- Show 30-second review summary (transactions count, reconciliation status, variance)
- Optional approval notes field
- Clearly explain "After approval, month is locked until posted"

---

### Workflow 3: EM_REVIEW → ABERTO (Reject)

**User Action**: Finance director clicks "Reject" on Review page

**UX Flow**:
1. Director on Review page, sees month in EM_REVIEW
2. Director clicks "Rejeitar" (Reject) button
3. Modal opens: "Reason for rejection" (required text field)
4. Director enters reason: "Missing invoice for transaction #47"
5. Director clicks "Rejeitar"
6. System shows loading spinner "Rejeitando revisão..."
7. On success: Toast "Month rejected. Returned to editing."
8. Badge changes back to "Aberto"
9. Ledger becomes editable again
10. Accountant receives notification: "Month rejected. Reason: Missing invoice for transaction #47"

**UX Alignment**: ✅ **New — needs implementation**

**Recommendation**:
- Require reason for rejection (max 250 chars)
- Show reason in notification to accountant
- Clear, non-judgmental wording ("Changes requested" not "Rejected")

---

### Workflow 4: PRONTO → POSTADO (Post to GL)

**User Action**: Accounting team clicks "Postar no GL" (Post to GL) on Reports page

**UX Flow**:
1. Month status is "Pronto"
2. User clicks "Postar no GL" button
3. Confirmation modal: "This will officially post month 2026-05 to GL. Continue?"
4. User clicks "Confirmar"
5. System shows: "Enviando para contabilidade..." (Posting to accounting...)
6. Wait for n8n webhook response (30s timeout)
7. **Success path**:
   - Toast: "Month posted successfully!"
   - Badge changes to "Postado"
   - Shows "GL Posting ID: GL-2026-05-00123" (timestamp)
   - "Reopen for Corrections" button available
8. **Timeout path**:
   - Message: "Posting is taking longer. Checking accounting system..."
   - After check: Either "Posted successfully (GL ID: ...)" or "Posting status unclear"
   - "Retry Posting" button available
9. **Failure path**:
   - Error toast: "Posting failed: {error from n8n}"
   - Button: "Retry" or "Contact support"

**Error Scenarios**:
1. **GL account not found** (400 error from n8n):
   - Message: "GL account configuration error. Contact administrator."
   - No retry button

2. **n8n service down** (503):
   - Message: "Accounting service temporarily unavailable. Retrying..."
   - Auto-retry after 30s

3. **Network timeout**:
   - Message: "Connection lost. Checking if month was posted..."
   - System queries GL system for confirmation
   - Either confirms posting or offers to retry

**UX Alignment**: ⚠️ **Requires new feature**
- No current "Post to GL" button
- Needs timeout handling UI

**Recommendation**:
- Add "Postar no GL" button (prominent, green) when in PRONTO state
- Implement timeout checking (query GL if no response)
- Show GL posting ID prominently (not just in audit log)
- Keep error messages user-friendly ("Service temporarily unavailable" not "503 Service Unavailable")

---

### Workflow 5: POSTADO → ABERTO (Reopen)

**User Action**: Finance director clicks "Reopen for Corrections" on Reports page

**Precondition Checks**:
- Month in POSTADO state
- reopened_count < 5 (or director override)
- User has admin role

**UX Flow**:
1. Month shows "Postado" badge
2. Director clicks "Reabrir para Correções" (Reopen for Corrections)
3. Modal opens: "Reason for reopening" (required)
4. Director enters: "Corrected invoice amount for vendor XYZ"
5. System shows loading spinner
6. On success: Toast "Month reopened for editing"
7. Badge changes back to "Aberto"
8. Ledger becomes editable
9. Snapshot preserved (for comparison)
10. Team receives notification: "Month reopened. Remember to re-post after corrections."

**Alert on High Reopen Count**:
- If reopened_count == 3: Show warning "This is the 3rd reopen. Consider additional review."
- If reopened_count == 5: Block reopen (show "Cannot reopen further without director override")

**UX Alignment**: ✅ **Partially exists**
- Reopen button exists but workflow is unclear
- Need to document the "must re-post after reopen" requirement
- Add alert for excessive reopens

**Recommendation**:
- Add clear notification: "Month reopened. Corrections will require re-posting after completion."
- Show reopened_count: "This is reopen #3 of 5 allowed"
- Add "View snapshot changes" button to show what was changed since posting

---

## Status Labels & Badges

### Current Labels (Implicit)
| Label | Meaning | Tone | Issues |
|---|---|---|---|
| "Aberto" | Open (implicit) | Gray | ✓ Clear |
| "Pronto" | Ready (implicit) | Blue | ⚠️ Doesn't convey "approved" |
| "Fechado" | Locked (implicit) | Green | ❌ Ambiguous with "Reaberto" |
| "Reaberto" | Reopened (shown in text) | Amber | ✓ Clear |
| "Atrasado" | Overdue (separate rule) | Amber | ✓ Clear |

### Proposed Labels (Explicit)
| State | Label | Tone | Meaning |
|---|---|---|---|
| ABERTO | "Aberto" | Gray | Open for editing |
| EM_REVIEW | "Em Revisão" | Orange | Director reviewing |
| PRONTO | "Pronto para Postar" | Indigo | Approved, awaiting GL posting |
| POSTADO | "Postado em GL" | Green | Successfully posted to GL |
| POSTADO (reopened) | "Reaberto - Aguardando Repostagem" | Amber | Reopened, needs re-posting |

**UX Alignment**: ⚠️ **Minor changes**
- Change "Fechado" to "Postado em GL" (clarifies it was posted, not just locked)
- Add "Em Revisão" state (new)
- Change "Pronto" to "Pronto para Postar" (clarifies next action)

**Recommendation**:
- Keep Portuguese labels for clarity (domain expert confirms)
- Add tooltips explaining each state
- Show state with timestamp (when transitioned)

---

## Error Message Alignment

### Example: "Cannot send to review"

**Domain Rule**: All transactions must be verified before EM_REVIEW

**Bad UX**: "Error: precondition failed"  
**Good UX**: "Cannot send to review: 3 transactions still unverified. Fix in Livro-Caixa"

**Current System**: ⚠️ Generic error messages

**Required Changes**:
- Replace generic "Error preparing month" with specific, actionable message
- Link to specific page or action (e.g., "Fix in Livro-Caixa")
- Show count of issues (e.g., "3 transactions", "R$ 47.33 reconciliation variance")

### Error Message Template

```
{ACTION_NAME} failed: {SPECIFIC_REASON}

Reason Details:
- {Issue 1: specific detail}
- {Issue 2: specific detail}

Next Action:
[Link to fix] or [Retry button]
```

**Recommendation**:
- Implement error context in all server actions
- Return structured error response with actionable details
- Map domain rule violations to user-friendly messages

---

## Navigation & Information Architecture

### Current IA Issues
1. **Finance module scattered** across multiple pages:
   - Dashboard (/admin/finance)
   - Ledger (/admin/finance/transactions)
   - Inbox (/admin/financeiro/inbox)
   - Reconciliation (/admin/finance/reconciliation)
   - Reports (/admin/finance/reports)
   - Billing (separate area)

2. **State indicator unclear**:
   - Only Reports page clearly shows month state
   - Dashboard shows status but hard to read
   - Ledger doesn't show state clearly

**Recommendation for Phase 4**:
- Add state indicator to each page breadcrumb or header
- Add "Finance Status" card to dashboard (prominently show month state + next action)
- Create unified "Month Workflow" overview (show all steps, current step highlighted)

---

## Unresolved Questions for UX Team

1. **EM_REVIEW modal location**: Should approval happen in modal, drawer, or new tab?
2. **GL posting confirmation**: Should we show GL posting ID prominently? Where?
3. **Snapshot comparison**: Should users see "before/after" when reopening?
4. **Review notes**: Should director add optional notes during approval?
5. **Rejection reason**: Should rejection reason be visible to accountant during re-editing?

---

## Validation Conclusion

✅ **Domain model is implementable in UX**

**Requires changes**:
- Add EM_REVIEW state screens (approval workflow)
- Add "Post to GL" button and status tracking
- Update status labels for clarity (Fechado → Postado)
- Improve error messages (make specific and actionable)

**Risk level**: Low (mostly adds features, no major redesigns)

**Timeline to implement**: 3-5 days (UX design + frontend development)

---

**Prepared by**: Phase 3 Workstream 1  
**Validated by**: [Product Manager, Designer names - pending signature]  
**Status**: Ready for Technical Workstream (Workstream 3) sync
