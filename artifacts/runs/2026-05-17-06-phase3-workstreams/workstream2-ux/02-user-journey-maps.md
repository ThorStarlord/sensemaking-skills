# User Journey Maps - Finance Module

**Execution Date**: 2026-05-17  
**Methodology**: Synthesized from codebase UI structure and phase 2 user interviews  
**Scope**: 4 major user workflows

---

## Journey 1: Close Out Month (Finance Accountant)

**Actor**: Finance Accountant  
**Goal**: Close out May, reconcile all transactions, send to director for review  
**Timeline**: 30-45 minutes  
**Frequency**: Monthly, end-of-month cycle

### Current Journey Map (As-Is)

```
┌─ Step 1: Login ──────────────────────────────────────┐
│ Screen: /admin/finance (Dashboard)                   │
│ Emotion: Ready to work                               │
│ Visual: Large month overview with 4 quick links      │
│ Duration: 30 seconds                                 │
└─ Clicks to next: 1 link click ───────────────────────┘
                        ↓
┌─ Step 2: Review pending inbox items ──────────────────┐
│ Screen: /admin/financeiro/inbox (Inbox page)         │
│ Emotion: "Let me see what needs processing"           │
│ Visual: List of "Pending" and "Needs Review" items   │
│ Data shown: Date created, status, extracted amount   │
│ Action: Review flagged items, apply auto-fixes       │
│ Duration: 10-15 minutes                              │
│ Pain point: Can't see linked transactions from here  │
└─ Clicks to next: 1 page navigation ──────────────────┘
                        ↓
┌─ Step 3: View all transactions in ledger ──────────────┐
│ Screen: /admin/finance/transactions (Transactions)    │
│ Emotion: "Are all my entries recorded correctly?"     │
│ Visual: Paginated list of all GL entries for month   │
│ Data shown: Date, amount, category, verification     │
│ Status shown: Verified (✓) or Unverified (○)          │
│ Action: Mark entries as verified/reconciled          │
│ Duration: 10-15 minutes                              │
│ Pain point: Many clicks to verify each transaction   │
└─ Clicks to next: 1 page navigation ──────────────────┘
                        ↓
┌─ Step 4: Check reconciliation with bank ──────────────┐
│ Screen: /admin/finance/reconciliation                │
│ Emotion: "Does everything match the bank?"           │
│ Visual: Table showing GL entries vs bank statement   │
│ Data shown: Matched entries ✓, Unmatched (?) entries │
│ Action: Click unmatched to fix or explain variance   │
│ Duration: 10-15 minutes                              │
│ Pain point: Must navigate to transactions to fix     │
└─ Clicks to next: 1 page navigation ──────────────────┘
                        ↓
┌─ Step 5: Send to review (lock month) ───────────────┐
│ Screen: /admin/finance/reports                       │
│ Emotion: "Ready to hand off to director?"            │
│ Visual: Month status "Aberto" → Click "Send to Review"│
│ Action: Click "Send to Review" button                │
│ Result: Month state → "Em Review" (locked for edits) │
│ Duration: 1 minute                                   │
│ Pain point: Button on reports page, not visible here │
│ Confirmation: "Month sent for review" message        │
└─ Journey complete ─────────────────────────────────────┘

Total navigation depth: 4 pages visited
Total clicks: 5 major navigation clicks
Mental burden: High (must context-switch between pages)
```

### Journey Emotions & Pain Points

| Step | Emotion | What Works | Pain Point | Why |
|---|---|---|---|---|
| 1 | Ready | Clear dashboard with quick links | Can't see other months at once | Only shows current month |
| 2 | Focused | Inbox items clearly listed | Don't know if item is posted yet | Status labels are unclear (pending vs processed) |
| 3 | Checking | All transactions visible | Must scroll/paginate to find one item | No search or fast filter |
| 4 | Verifying | Reconciliation shows unmatched | Can't see which transaction caused mismatch | Must jump back to transactions to investigate |
| 5 | Ready | Clear "Send to Review" action | Is this on the right page? | Button buried in Reports section |

### Mental Model During Journey

User's inner thoughts:
1. ✓ "I have a list of uploaded invoices"
2. ? "Are these invoices showing up in my transactions yet?"
3. ? "Which transactions came from which invoices?"
4. ✓ "All amounts add up and match the bank"
5. ✓ "Month is ready to close"

### Key Insight

**User expects**: Linear flow: Upload → Process → Verify → Close  
**System provides**: Scattered across 4 different pages requiring navigation

---

## Journey 2: Review Month for GL Posting (Finance Reviewer)

**Actor**: Finance Reviewer (mid-level)  
**Goal**: Validate May data is correct and complete, approve for posting  
**Timeline**: 45-60 minutes  
**Frequency**: Monthly, after accountant sends for review  
**Triggers**: "Month sent for review" notification

### Current Journey Map (As-Is)

```
┌─ Step 1: Receive notification & login ────────────────┐
│ Email: "May is ready for review - 847 transactions"   │
│ Screen: /admin/finance (Dashboard)                    │
│ Emotion: "OK, let me check what needs approval"       │
│ Visual: Month status shows "Em Review"                │
│ Note: No visual indicator that month is in review!    │
│ Duration: 1 minute                                    │
└─ Clicks to next: 1 link click ───────────────────────┘
                        ↓
┌─ Step 2: Check review queue (flagged items) ──────────┐
│ Screen: /admin/financeiro/inbox?status=review_queue   │
│ Emotion: "What items need my attention?"              │
│ Visual: Filtered list showing review queue items      │
│ Items shown: Missing date, missing amount, errors     │
│ Actions: Quick fix buttons or reject                  │
│ Duration: 15-20 minutes                               │
│ Pain point: Can't see linked transactions from here   │
└─ Clicks to next: 1 page navigation ──────────────────┘
                        ↓
┌─ Step 3: Spot-check transaction details ──────────────┐
│ Screen: /admin/finance/transactions (detail modal)    │
│ Emotion: "Does this look right?"                      │
│ Visual: Transaction detail showing all fields         │
│ Missing: No "source document" / "invoice" link shown  │
│ Expected: "This transaction came from invoice 12345"  │
│ Actual: No way to find source document from here      │
│ Duration: 15-20 minutes (multiple transactions)       │
│ Pain point: Can't verify document-to-transaction link │
└─ Clicks to next: 1 page navigation ──────────────────┘
                        ↓
┌─ Step 4: Verify reconciliation ──────────────────────┐
│ Screen: /admin/finance/reconciliation                │
│ Emotion: "Do the numbers match the bank?"            │
│ Visual: Side-by-side comparison                       │
│ Status: All matched ✓ OR Some unmatched ?             │
│ If unmatched: Back to transactions to fix            │
│ Duration: 10 minutes                                 │
│ Pain point: Back-and-forth between pages            │
└─ Clicks to next: 1 page navigation ──────────────────┘
                        ↓
┌─ Step 5: Approve month (state transition) ───────────┐
│ Screen: /admin/finance/reports (or Dashboard?)        │
│ Emotion: "Where's the approve button?"                │
│ Action: Find and click "Approve" or "Ready to Post"  │
│ Result: Month state → "Pronto" (Ready to post)        │
│ Duration: 2-5 minutes (searching for button!)         │
│ Pain point: Approval action location unclear          │
│ Confirmation: "Month approved and ready for posting"  │
└─ Journey complete ─────────────────────────────────────┘

Total navigation depth: 4 pages visited
Total clicks: 5+ major navigations
Back-and-forth navigation: Very high (verification requires jumping between pages)
Frustration point: No single "review mode" view
```

### Journey Emotions & Pain Points

| Step | Emotion | What Works | Pain Point | Why |
|---|---|---|---|---|
| 1 | Alert | Clear notification | Month state not visible in dashboard | Badge missing |
| 2 | Focused | Review queue clearly marked | Status labels unclear (processed vs ready) | Multiple statuses confuse workflow |
| 3 | Checking | Detail view shows most fields | No source document visible | Can't verify document→transaction link |
| 4 | Verifying | Reconciliation shows variance | Must navigate back to fix issues | No integrated workflow |
| 5 | Uncertain | Need to find approve button | Button location unclear | Scattered across multiple pages |

### Critical Gap: Document Linking

**User's expectation**:
```
Reviewer sees transaction: "R$1,000 expense - Office supplies"
Reviewer thinks: "Which invoice is this from?"
Expected UX: "Linked Documents: Invoice #1234, PDF link"
Actual UX: No document links visible; must know to search manually
```

### Mental Model During Journey

User's inner thoughts:
1. ✓ "What items are flagged for review?"
2. ✓ "Are the amounts reasonable?"
3. ✗ "Which invoice is this transaction from?" (STUCK)
4. ? "Do the numbers balance?" (Can't fully verify without documents)
5. ? "Where do I click to approve?" (Hidden button)

---

## Journey 3: Monitor & Post to GL (Finance Director)

**Actor**: Finance Director (leadership)  
**Goal**: Ensure month close is on track; post to GL once approved  
**Timeline**: 10-15 minutes per check (multiple checks throughout month)  
**Frequency**: Multiple times throughout month + end-of-month focus

### Current Journey Map (As-Is)

```
┌─ Step 1: Check close status from dashboard ───────────┐
│ Screen: /admin/finance (Dashboard)                    │
│ Emotion: "What's the status of May?"                  │
│ Visual: "Prontidao" (Readiness) progress bar 4/5      │
│ Question: "What are these 5 steps?"                   │
│ Pain point: No labels for each progress step          │
│ Duration: 1 minute                                    │
│ Visual present: Progress bar only; no step names      │
└─ Clicks to next: 1-2 link clicks (depends on status) ┘
                        ↓
┌─ Step 2a: [IF BLOCKED] Navigate to blocker ───────────┐
│ Screen: /admin/finance/inbox OR /reconciliation       │
│ Emotion: "What's holding up close?"                   │
│ Action: Check which step is incomplete                │
│ Pain point: Dashboard doesn't tell which step blocked  │
│ Duration: 10-15 minutes (investigation)               │
└─ Clicks to next: Depends on finding blocker ─────────┘
                        ↓
┌─ Step 2b: [IF READY] Approve posting ──────────────────┐
│ Screen: /admin/finance/reports                        │
│ Emotion: "Month looks good, ready to post"            │
│ Action: Click "Post to GL" or "Send to GL"            │
│ Result: n8n webhook triggered; GL posting happens    │
│ Duration: 1 minute                                    │
│ Pain point: Unclear if posting is synchronous/async   │
└─ Clicks to next: 1 page navigation ──────────────────┘
                        ↓
┌─ Step 3: Wait for posting status ────────────────────┐
│ Screen: /admin/finance (refresh)                      │
│ Emotion: "Is it posted yet?"                          │
│ Question: "How do I know if it succeeded?"            │
│ Visual: No status indicator for posting progress      │
│ Pain point: No "Posting in progress..." message       │
│ No GL posting ID shown in UI                          │
│ Duration: Variable (director keeps checking)          │
│ Solution: Must check console logs or ask engineer     │
└─ Journey complete or BLOCKED ──────────────────────────┘

Total navigation depth: 2-3 pages
Total clicks: 2-4 navigation clicks
Uncertainty high: No visibility into posting status
Pain: No audit trail visible
```

### Key Gaps for Director

| Gap | Impact | Frequency |
|---|---|---|
| No step-by-step progress labels | Director must guess what's blocking | Every month |
| No audit trail in UI | Can't answer "Who approved this?" | Every review |
| No GL posting status | Don't know if posting succeeded | Every post |
| No multi-month view | Can't see which months are stuck | Multiple times/month |
| No alert for critical issues | Must manually check dashboard | Every day during close |

### Mental Model During Journey

User's inner thoughts:
1. "Progress bar shows 4/5... what does that mean?"
2. "If something's wrong, where do I look?"
3. "I clicked Post... did it work?"
4. "Can I see a history of who did what?"

---

## Journey 4: Record Daily Transactions (Finance Operator)

**Actor**: Finance Operator (data entry)  
**Goal**: Record daily invoices and expenses quickly  
**Timeline**: 5-10 minutes per invoice  
**Frequency**: Daily, throughout the month

### Current Journey Map (As-Is)

```
┌─ Step 1: Access dashboard ────────────────────────────┐
│ Screen: /admin/finance (Dashboard)                    │
│ Emotion: "Got a new invoice to enter"                 │
│ Action: Click "Pendencias de captura" quick link      │
│ Duration: 30 seconds                                  │
└─ Clicks to next: 1 link click ───────────────────────┘
                        ↓
┌─ Step 2: Upload invoice ──────────────────────────────┐
│ Screen: /admin/financeiro/inbox (Inbox page)         │
│ Emotion: "Let me upload this file"                    │
│ Visual: File upload form in modal or sidebar          │
│ Action: Select file → Click upload                    │
│ Result: File uploaded to Inbox status="pending"       │
│ Duration: 2-3 minutes                                 │
│ Confirmation: File appears in list below             │
│ Status shown: "pending"                               │
│ Pain point: "Is it processing or just waiting?"       │
└─ Clicks to next: Wait for auto-process OR fill form ─┘
                        ↓
┌─ Step 3a: [AUTO] Wait for auto-extraction ────────────┐
│ Emotion: "System extracting data now..."              │
│ Visual: File status changes (pending → processed?)    │
│ Duration: 30 seconds to 2 minutes                     │
│ Pain point: No progress indicator visible             │
│ User action: Refresh page or wait                     │
└─ If auto-extraction succeeds: Skip to Step 4 ────────┘
                  ↓                      ↓
        [Continue]                  [Manual entry]
                  ↓                      ↓
┌─ Step 3b: [MANUAL] Fill in extracted data ─────────────┐
│ Emotion: "Some data is missing, I need to enter it"   │
│ Form fields: Description, Amount, Date, Category, ... │
│ Visual: Form shows auto-extracted values as defaults   │
│ Action: Fill missing fields, correct errors           │
│ Pain point: Not clear which fields are required       │
│ Duration: 3-5 minutes                                 │
│ Validation: Errors shown inline? Or on submit?        │
└─ Clicks to next: 1 submit button ────────────────────┘
                        ↓
┌─ Step 4: Submit and confirm ──────────────────────────┐
│ Screen: Same Inbox page (refreshed)                   │
│ Emotion: "Is it saved?"                               │
│ Action: Click "Save" or "Submit" button               │
│ Result: Entry added to transactions (maybe?)          │
│ Confirmation: Unclear - just redirect to dashboard?   │
│ Pain point: No clear success message                  │
│ Duration: 1 minute                                    │
│ User question: "Did my entry get recorded?"           │
└─ Journey complete ─────────────────────────────────────┘

Total navigation depth: 1-2 pages
Total clicks: 2-3 clicks
Feedback loop: Weak (no confirmation of success)
Pain: Status ambiguity throughout
```

### Journey Emotions & Pain Points

| Step | Emotion | What Works | Pain Point | Why |
|---|---|---|---|---|
| 1 | Energized | Quick link visible | Can't navigate from dashboard | Must use quick link |
| 2 | Ready | File upload works | No progress indicator | Unknown processing time |
| 3 | Patient | Auto-extract saves time | "Is it working?" | No loading state shown |
| 4 | Hesitant | Form appears | Field requirements unclear | Required vs optional ambiguous |
| 5 | Uncertain | Redirect to dashboard | "Was that saved?" | No success confirmation |

### Critical Gap: Status Ambiguity

**Current statuses in system**:
- pending
- needs_review  
- processed
- error
- posted
- archived

**Operator mental model**:
- "Processing" = system is working on it
- "Posted" = done, recorded in ledger

**What operator needs**:
```
Clear status path:
  Uploaded → Auto-extracting → Ready for review → Accepted → Posted

Visual feedback at each step:
  ✓ File received
  ⚙ Extracting data...
  ⏳ Waiting for human review
  ✓ Approved and posted
```

---

## Cross-Journey Summary

### Common Pain Points (All Roles)

1. **Navigation fragmentation** (Appears in all 4 journeys)
   - Inbox scattered across multiple pages
   - Transactions in separate page from Inbox
   - Reconciliation requires yet another page
   - Reports/closing actions on yet another page
   - **UX fix**: Consolidate to single "Month Overview" with tabs

2. **State machine invisibility** (Appears in journeys 2, 3)
   - Month state not clearly visible during review
   - Transitions not labeled
   - User can't tell "Why is this button disabled?"
   - **UX fix**: Add state badges and grayed-out buttons with tooltips

3. **Document-to-transaction linking** (Appears in journeys 2, 4)
   - No way to see which invoice created which transaction
   - Reviewer can't verify document authenticity
   - Operator doesn't know if entry was recorded
   - **UX fix**: Add "Source Document" panel in transaction detail

4. **Terminology misalignment** (Appears in all 4 journeys)
   - "Postado" means different things to different roles
   - Status labels use system terminology, not user terminology
   - "pending" is unclear (processing? waiting? error?)
   - **UX fix**: Use clearer labels aligned with user mental models

### Summary by Role

| Role | Primary Frustration | Secondary Frustration | Tertiary Frustration |
|---|---|---|---|
| Accountant | Navigation between 4 pages | Status ambiguity | Term confusion |
| Reviewer | Can't find source documents | Month state not visible | Approval button hidden |
| Director | Progress steps unlabeled | GL posting status opaque | No audit trail |
| Operator | Status ambiguity | Weak feedback loop | Field requirements unclear |

---

## Recommended Journey Optimizations

### For Accountant:
```
Current: Dashboard → Inbox → Transactions → Reconciliation → Reports
Proposed: Dashboard → Month Overview (Inbox/Transactions/Details tabs)
Benefit: 4 pages → 1 page; 5 clicks → 1 click
```

### For Reviewer:
```
Current: Dashboard → Inbox (review queue) → Transactions (details) → Reconciliation → Reports
Proposed: Dashboard → Month Overview in "Review" mode with document panel
Benefit: Shows source documents inline; reduce context-switching
```

### For Director:
```
Current: Dashboard (unclear steps) → Blocker investigation
Proposed: Dashboard with labeled progress steps + drill-down to blockers
Benefit: Clear status; know exactly what's blocking
```

### For Operator:
```
Current: Dashboard → Inbox → Upload/form → Unclear confirmation
Proposed: Dashboard → Quick upload modal with real-time feedback
Benefit: Single-page workflow; clear success/error states
```

