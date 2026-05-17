# Information Architecture & Navigation Redesign

**Execution Date**: 2026-05-17  
**Methodology**: Journey-based IA synthesis from user interviews and codebase analysis  
**Scope**: Proposed improvements to Finance module structure

---

## Executive Summary

**Current IA Problem**: Finance UI is fragmented across 4 separate pages (`/dashboard`, `/inbox`, `/transactions`, `/reconciliation`, `/reports`), requiring users to navigate between contexts to complete a single workflow.

**Proposed Solution**: Consolidate to unified "Month Overview" with content organized into tabs (Inbox, Transactions, Details), reducing navigation depth from 4 pages to 1 primary page.

**Expected Impact**:
- Reduce navigation clicks from 5+ to 1-2
- Improve task completion time by 30-40%
- Reduce cognitive load (less context switching)
- Align UI structure with user mental models

---

## Current IA (As-Is)

```
Finance Root
├── /admin/finance (Dashboard)
│   ├── Quick links (Inbox, Transactions, Reconciliation, Reports)
│   ├── Review queue preview
│   ├── Close status progress bar
│   └── Financial metrics (income, expense, balance)
│
├── /admin/financeiro/inbox (Inbox Page)
│   ├── Filtered views by status (active, review_queue, pending, processed, etc.)
│   ├── Item list (date, extracted amount, confidence)
│   ├── Automation hints (suggested fixes)
│   └── [Modal] Upload/manual entry form
│
├── /admin/finance/transactions (Transactions Page)
│   ├── Month selection
│   ├── Transaction list (date, amount, category, verified status)
│   ├── Quick filters (verified, category)
│   └── [Modal] Transaction detail (with edit capability)
│
├── /admin/finance/reconciliation (Reconciliation Page)
│   ├── Month selection
│   ├── Reconciliation table (GL entry vs bank entry)
│   ├── Matched/unmatched indicators
│   └── [Modal] Detail/edit unmatched items
│
└── /admin/finance/reports (Reports Page)
    ├── Month status ("Aberto", "Em Review", "Pronto", "Postado")
    ├── Action buttons (Send to Review, Post, Reopen, Download)
    ├── Audit trail (optional)
    └── [Modal] Confirmation dialogs
```

**Problems with current IA**:
1. Users must visit 4-5 different pages to close a month
2. Information is scattered (can't compare Inbox items with transactions on same screen)
3. State transitions are on Reports page (separate from data pages)
4. Reconciliation is isolated (can't see which transaction caused mismatch)
5. No unified entry point for workflow management

---

## Proposed IA (To-Be)

```
Finance Root
├── /admin/finance (Dashboard - unchanged)
│   ├── Quick stats (income, expense, balance)
│   ├── Close status with labeled progress steps
│   ├── Quick links (Month Overview, Multi-month View)
│   ├── Alerts/blockers (if any)
│   └── Recent activities
│
└── /admin/finance/month/:monthKey (NEW: Month Overview)
    │
    ├── [Header] Month selector + State badge ("Open" / "In Review" / "Ready to Post" / "Posted")
    ├── [Action Bar] Primary actions (Send to Review, Post, Reopen, Download)
    │
    └── [Tab 1: Inbox] Source Documents
    │   ├── Filter by status (Pending, Processing, Review, Posted)
    │   ├── Document list (date, filename, auto-extracted amount, status, confidence)
    │   ├── [Inline] Quick fix buttons (Apply date, Apply category, etc.)
    │   ├── [Inline] Link to posted transaction (if available)
    │   └── [Action] Upload new document OR manual entry
    │
    ├── [Tab 2: Transactions] Accounting Entries
    │   ├── Filter by status (Unverified, Verified, Reconciled)
    │   ├── Transaction list (date, amount, category, description, verified)
    │   ├── [Inline] Source document badge (shows which Inbox item created this)
    │   ├── [Inline] Reconciliation status (Matched to bank? Yes/No/Pending)
    │   └── [Modal] Transaction detail with source document panel
    │
    ├── [Tab 3: Details] Month Reconciliation & Status
    │   ├── Summary metrics
    │   │   ├── Total transactions (count)
    │   │   ├── Total amount (income vs expense)
    │   │   ├── GL balance expected
    │   │   ├── GL balance actual
    │   │   └── Variance
    │   │
    │   ├── Reconciliation table (bank entries vs GL entries)
    │   │   ├── Matched entries ✓
    │   │   ├── Unmatched entries ?
    │   │   └── [Action] Reconcile button → link to transaction
    │   │
    │   ├── Progress steps (visual checklist)
    │   │   ├── ✓ Prepare review queue
    │   │   ├── ✓ Auto-post ready items
    │   │   ├── ○ Verify transactions
    │   │   ├── ○ Reconcile statement
    │   │   └── ○ Send to review
    │   │
    │   ├── Audit trail (read-only)
    │   │   ├── "2026-05-17 14:30 - Accountant John sent for review"
    │   │   ├── "2026-05-17 15:45 - Reviewer Jane approved"
    │   │   └── "2026-05-18 09:00 - Posted to GL ID: GL-2026-05-001"
    │   │
    │   └── Alerts (if any)
    │       ├── ⚠ 5 items need manual review
    │       ├── ⚠ Reconciliation variance: R$15.27
    │       └── ✓ Month ready to post
    │
    └── [Additional] Multi-month View (Optional enhancement)
        ├── Grid view: All months with status
        ├── Columns: Month, Status, Items pending, Reconciliation variance
        └── [Action] Filter by status to find stuck months
```

---

## Component Layout: Month Overview (Desktop View)

```
┌─────────────────────────────────────────────────────────────────────┐
│ [Month Selector] May 2026  [Status Badge: "In Review"]             │
├─────────────────────────────────────────────────────────────────────┤
│ [Primary Actions Bar]                                              │
│ [Send to Review] [Post to GL] [Reopen] [Download Report]           │
│ [Alerts: ⚠ 5 items need review] [✓ Ready to post after fixes]     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ [TAB 1: Inbox]  [TAB 2: Transactions]  [TAB 3: Details]           │
│                                                                     │
│ ┌─────────────────────────────────────────────────────────────┐   │
│ │ INBOX TAB (Active)                                          │   │
│ │ [Filter: All] [Status: Pending (5), Processing (3), ...]   │   │
│ ├─────────────────────────────────────────────────────────────┤   │
│ │ Date        │ File        │ Amount    │ Status    │ Actions │   │
│ ├─────────────────────────────────────────────────────────────┤   │
│ │ 2026-05-10  │ Invoice.pdf │ R$1,500   │ Pending   │ ⚙ ✓ ✗  │   │
│ │             │ (Linked to Txn #123)                              │   │
│ ├─────────────────────────────────────────────────────────────┤   │
│ │ 2026-05-12  │ Receipt.jpg │ R$ 250    │ Processed │ ✓      │   │
│ │             │ (Not linked yet)        │ ⚠ Review  │        │   │
│ ├─────────────────────────────────────────────────────────────┤   │
│ │ [+ Upload new document] [+ Manual entry]                    │   │
│ └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Information Hierarchy

### Level 1: Global Context (Always visible)
- Current month + state
- Primary actions (Send to review, Post, etc.)
- Critical alerts (5 items need review, reconciliation failed, etc.)

### Level 2: Tabbed content (Select by role/task)
- **Inbox tab**: For operators entering data; reviewers checking source docs
- **Transactions tab**: For accountants verifying entries; reviewers spot-checking
- **Details tab**: For reconciliation and close readiness verification

### Level 3: Item-level detail (On demand)
- Click transaction → Show source document panel + transaction details
- Click Inbox item → Show linked transactions + suggested fixes
- Click unmatched reconciliation entry → Link to transaction detail

### Level 4: Meta information (Secondary)
- Audit trail (who did what when)
- Confidence scores (for auto-extracted data)
- Processing metadata (error details if any)

---

## Navigation Model

### Primary Navigation Path (Most users)
```
Dashboard → Month Overview → Choose tab → Review/enter data → Complete
```

### Alternative Navigation Paths

**For quick status check**:
```
Dashboard → (view status on dashboard, no need to click through)
```

**For multi-month management**:
```
Dashboard → Multi-month View → Click month → Month Overview
```

**For focused audit**:
```
Dashboard → Month Overview → Details tab → Audit trail
```

---

## Terminology Alignment with IA

| Old Term | New Term | Where It Appears | Reasoning |
|---|---|---|---|
| "Inbox Item" | "Source Document" | Inbox tab header | More precise; users understand "document" better |
| "Transaction" | "Accounting Entry" | Transactions tab header | Aligns with finance domain language |
| "Postado" | "Posted to Ledger" | State badge | Full phrase is clearer than Portuguese abbreviation |
| "Pronto" | "Ready to Post" | State badge | Action-oriented; clear what "ready" means |
| "Aberto" | "Open" | State badge | Familiar term |
| "Em Review" | "In Review" | State badge + header badge | English clear; consistent across UI |
| "pending" | "Awaiting Processing" | Status filters | Clear what "pending" means |
| "processed" | "Ready for Review" | Status filters | Indicates next step |
| "needs_review" | "Requires Attention" | Status badge | Action-oriented |
| "error" | "Processing Error" | Status badge | Clear that something went wrong |
| "posted" | "Posted to Ledger" | Status badge | Aligns with state machine terminology |

---

## Page Type Definitions

### 1. Dashboard (High-level overview)
**Purpose**: Quick status check and navigation entry point  
**Content**: Quick links, alerts, progress, metrics  
**Actions**: Open Month Overview, view multi-month status  
**For whom**: All roles, multiple times per day

### 2. Month Overview (Primary work area)
**Purpose**: Single unified space for all month-related work  
**Content**: 3 tabs (Inbox, Transactions, Details) + action bar  
**Actions**: Upload documents, verify transactions, reconcile, send to review, post  
**For whom**: Accountants, reviewers, operators (role-specific tab focus)

### 3. Transaction Detail Modal (Deep dive)
**Purpose**: Inspect one transaction with full context  
**Content**: Transaction fields + source document panel + reconciliation status  
**Actions**: Edit (if allowed by state), view document, mark reconciled  
**For whom**: Reviewers, accountants (verification workflow)

### 4. Document Detail Modal (Deep dive)
**Purpose**: Inspect one source document with linked transactions  
**Content**: Document image/preview + auto-extracted data + linked transactions  
**Actions**: Verify extraction, apply to transaction, reprocess  
**For whom**: Operators, reviewers (verification workflow)

---

## State-Aware UI Rules

The proposed IA must reflect the domain state machine (from Workstream 1).

### Month states and UI implications

| Month State | Inbox Tab | Transactions Tab | Actions Bar | Edit Buttons |
|---|---|---|---|---|
| **ABERTO** (Open) | Upload ✓ | Edit ✓ | Send to Review | Active |
| **EM_REVIEW** | Read-only | Read-only | (none) | Disabled + tooltip |
| **PRONTO** | Read-only | Read-only | Post to GL | Disabled + tooltip |
| **POSTADO** | Read-only | Read-only | (none) | Disabled + archived |

**UI treatment for disabled actions**:
```
[Edit button - disabled]
  ↓ (on hover)
"Transactions cannot be edited while month is in review. 
 Contact finance director to reopen the month."
```

---

## Mobile Responsiveness

### Desktop (1200px+)
- Full tabbed layout with all content visible
- Side-by-side comparison possible (Inbox + Transactions)
- Action bar sticky at top

### Tablet (768px - 1199px)
- Single column, tabs stack
- List items more compact
- Modals full screen for detail

### Mobile (< 768px)
- Single column, strict stacking
- Tabs become dropdown selector or swiped
- Modals full screen
- Actions become floating action button
- Document preview in modal only

---

## Search & Filter Strategy

### Inbox Tab Filters
- By status (Pending, Processing, Ready, Error, Posted)
- By confidence (Show only low-confidence items)
- By document type (Invoices, receipts, etc.)
- By date range
- By linked transaction (None / Has transaction)

### Transactions Tab Filters
- By verification (Unverified, Verified)
- By category
- By amount range
- By date range
- By reconciliation (Matched, Unmatched, Pending)

### Details Tab Filters
- Audit trail search by user or action type
- Reconciliation filter (Show only unmatched)

---

## Progressive Disclosure

### Essential Information (Always shown)
- Date
- Amount
- Status
- Verification/reconciliation indicator

### Important Information (Click to expand)
- Description/notes
- Source document (for transactions)
- Linked transactions (for documents)
- Confidence score (for auto-extracted data)

### Advanced Information (In details modal)
- Audit trail
- Processing metadata
- Error details
- Raw extracted data (for debugging)

---

## Proposed Implementation Phases

### Phase 4.1: MVP (Weeks 1-2)
1. Create `/admin/finance/month/:monthKey` route
2. Implement Inbox tab (copy/refactor existing inbox page)
3. Implement Transactions tab (copy/refactor existing transactions page)
4. Implement basic Details tab (checklist + summary)
5. Add state badge + primary actions bar
6. Migrate from old pages to new unified page

**Not included in MVP**:
- Source document panel in transactions detail
- Document preview modal
- Full audit trail (basic version only)
- Multi-month view

### Phase 4.2: Enhanced (Weeks 3-4)
1. Add source document panel to transaction detail modal
2. Implement document preview modal
3. Expand audit trail UI
4. Add document type filtering
5. Implement multi-month view (optional)

### Phase 4.3: Polish (Weeks 5-6)
1. Accessibility audit and fixes
2. Mobile responsiveness refinement
3. Performance optimization
4. User testing and feedback incorporation

---

## Validation Checklist

### IA Validation Against User Journeys

- [ ] **Accountant**: Reduce month close from 4 pages to 1 page ✓
- [ ] **Reviewer**: Show source documents inline without navigation ✓
- [ ] **Director**: Label progress steps clearly ✓
- [ ] **Operator**: Single upload workflow with clear feedback ✓

### IA Validation Against Mental Models

- [ ] Inbox (documents) separate from Transactions (GL entries), but linked ✓
- [ ] State machine visible through badges and disabled buttons ✓
- [ ] Navigation depth reduced from 4 pages to 1 ✓
- [ ] Terminology aligned with user expectations ✓

### IA Validation Against Domain Model (Workstream 1)

- [ ] State transitions visible in UI (state badge) ✓
- [ ] Operations blocked by state machine (disabled buttons) ✓
- [ ] State-specific information shown (e.g., no edits in review) ✓
- [ ] Audit trail accessible for compliance ✓

---

## Success Metrics

After implementation, measure:

1. **Navigation efficiency**: Clicks to complete month close (target: 5 → 2)
2. **Task completion time**: Month close workflow (target: 45 min → 25 min)
3. **Error rate**: Mistakes in transaction entry (target: -40%)
4. **User satisfaction**: NPS on Finance module (target: +20 points)
5. **Audit compliance**: Time to generate audit trail (target: <1 min)

