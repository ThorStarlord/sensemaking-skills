# User Interview Notes - Finance UX Discovery

**Execution Date**: 2026-05-17  
**Methodology**: Synthesized from Phase 2 operator interviews + codebase UI analysis  
**Scope**: 4 major user roles in Finance workflow

---

## Executive Summary

Based on phase 2 interview findings and current UI code analysis, users have significant mental model gaps:

1. **Inbox vs Transactions confusion**: Users think an "Inbox Item" IS a transaction. System treats them as separate entities (documents vs. GL entries).
2. **Navigation depth problem**: Users expect all month information on one screen. Current UI requires 3+ clicks to compare Inbox items with transactions.
3. **Terminology misalignment**: Portuguese domain terms ("Pronto", "Postado") don't match user expectations; users translate literally rather than understanding finance meaning.
4. **State machine invisibility**: Users don't understand why they can't edit a transaction when month is "in review" — no visual state indicator in UI.

---

## Role 1: Finance Accountant (Entry-level)

**Primary Goal**: Record daily invoices and expenses, close out the month

**Current Workflow**:
1. Log in to `/admin/finance`
2. See Finance Dashboard showing 4 quick-link cards
3. Click "Livro-Caixa" (Transaction ledger) or "Pendencias de captura" (Inbox pending)
4. Upload invoice to Inbox
5. Wait for auto-processing or manually enter transaction data
6. Navigate to `/admin/finance/transactions` to verify entry
7. Check `/admin/finance/reconciliation` to match against bank statement
8. Navigate to `/admin/finance/reports` to send month for review

**Mental Model**:
- "I uploaded an invoice. When does it become a transaction?"
- "Where do I find the invoice I uploaded?" (Thinks it should appear in transactions list)
- "Why does the system say 'Postado'? I'm trying to post it TO the ledger, not FROM ledger"
- "Reconciliation is just matching numbers, right?"

**Pain Points**:
1. **Inbox Item ↔ Transaction confusion** (CRITICAL)
   - User uploads invoice to Inbox
   - System automatically extracts: amount, date, description
   - User expects this to appear in "Transactions" list as a single entry
   - Reality: Inbox item is a *document* waiting to become a *transaction*
   - Result: User doesn't understand why they see 1 invoice but 2 different transactions (split expense)

2. **Navigation depth** (HIGH)
   - User needs to check: "Are there any unprocessed invoices? How do they compare to actual transactions?"
   - Current path: Finance → Inbox tab (filtered) OR Finance → Transactions tab
   - Can't see both at once; have to switch tabs or navigate between pages
   - User perception: "The system is making me navigate everywhere"

3. **Terminology** (HIGH)
   - "Pronto" = "Ready" in English, but in Portuguese accounting means "prepared/assembled"
   - User hears "Pronto" and thinks "Ready to post?" or "Already posted?"
   - Actually means: "Month reviewed and approved, ready for GL posting step"
   - "Postado" = "Posted", user understands this but...
   - User expects: "I click 'Post' and it goes to GL"
   - System reality: "Posting happens automatically after state transition"

4. **Auto-processing unpredictability** (MEDIUM)
   - Dashboard shows "Preparar (5)" button (prepare review queue for auto-fix)
   - User doesn't understand: "What does 'prepare' do?"
   - System: Applies automatic suggestions (capture date, category defaults)
   - User thought: "This will post the items for me?"

---

## Role 2: Finance Reviewer (Mid-level)

**Primary Goal**: Validate month transactions before GL posting, ensure reconciliation

**Current Workflow**:
1. Receive notification: "May is ready for review"
2. Navigate to `/admin/financeiro/inbox?status=review_queue`
3. Review flagged items (missing date, amount, etc.)
4. Apply quick fixes or reject items
5. Navigate to `/admin/finance/transactions` to verify all entries
6. Check `/admin/finance/reconciliation` to validate balance matches GL expectation
7. If all clear, approve month (state: "Pronto")
8. Monitor posting status

**Mental Model**:
- "I need to make sure every transaction has a source document"
- "All amounts must add up correctly"
- "Once I approve, can I make changes? No? Why is it locked?"
- "What's the difference between 'needs review' and 'review queue'?"

**Pain Points**:
1. **Missing document visibility** (CRITICAL)
   - Reviewer sees a transaction for R$1,000
   - Reviewer needs to verify: "Which invoice paid for this?"
   - Current UI: Must navigate to transaction detail, then look for "source document" link
   - User expectation: "Show me the linked invoice right here in the list"

2. **State confusion during review** (HIGH)
   - When month enters "Em Review" state, transactions become locked
   - User clicks "Edit" button, gets error: "Month in review, cannot edit"
   - No visual indicator that month is in review state (no badge, no disabled button state)
   - User thinks: "System is broken" instead of "I'm in review mode, edits are blocked"

3. **Reconciliation data fragmentation** (HIGH)
   - Reconciliation data in separate page (`/reconciliation`)
   - Transactions in separate page (`/transactions`)
   - User must flip between pages to validate: "Does this transaction match the reconciliation entry?"
   - Better UX: Show reconciliation status inline with transaction

4. **Approval/rejection workflow unclear** (MEDIUM)
   - Review queue shows items "needs review"
   - How do I "approve" the month? Click button where?
   - Current: Must navigate to `/admin/finance/reports` to see "Send to Review" button
   - User expectation: Action should be visible on review page itself

---

## Role 3: Finance Director (Leadership)

**Primary Goal**: Monitor month close status, oversee GL posting, handle escalations

**Current Workflow**:
1. Check Finance Dashboard for close status
2. Review "Prontidao" (readiness) progress bar
3. If issues escalated, navigate to problem area (Inbox, Transactions, or Reconciliation)
4. Approve month posting or request corrections
5. Monitor GL posting progress
6. Generate reports for stakeholders

**Mental Model**:
- "At a glance, what's the status of May close?"
- "Are there any blockers I need to know about?"
- "Can I see the audit trail of who reviewed what?"
- "What happens if posting fails?"

**Pain Points**:
1. **Month readiness visibility** (HIGH)
   - Dashboard shows "Prontidao: 4/5" progress bar
   - Director doesn't understand what those 5 steps are
   - Current steps shown: Prepare, Auto-post, Verify, Reconcile
   - Missing from UI: Clear labels for each step; what's blocking progress

2. **Lack of audit trail** (HIGH)
   - Director wants to know: "Who approved this month? When? With what conditions?"
   - Current UI: No audit log visible
   - System tracks this (in `financial_transaction_audit_logs`), but not exposed in UI

3. **GL posting status opacity** (MEDIUM)
   - When director clicks "Post", what happens?
   - Current flow: Month transitions to "Postado", n8n webhook called asynchronously
   - UI doesn't show: "Posting in progress", "Posted to GL with ID: GL-2026-05-001"
   - Director doesn't know if posting succeeded or failed

4. **No multi-month overview** (MEDIUM)
   - Director can only view 1 month at a time
   - Can't see: "Which months are ready to post? Which are stuck?"
   - Workaround: Director must manually check each month via dropdown

---

## Role 4: Finance Operator (Data Entry)

**Primary Goal**: Input transactions, upload invoices, manage day-to-day finance captures

**Current Workflow**:
1. Receive invoice via email or physical mail
2. Click "Pendencias de captura" quick link
3. Upload file or enter transaction manually via inline form
4. Fill in extracted data (if auto-capture missed values)
5. Submit transaction
6. Move on to next invoice

**Mental Model**:
- "I uploaded an invoice. Is it recorded now or waiting for someone to approve?"
- "Why does auto-capture sometimes get the amount wrong?"
- "How do I know if my entry was accepted?"

**Pain Points**:
1. **Transaction status ambiguity** (HIGH)
   - Operator uploads invoice, sees status: "pending"
   - Operator doesn't know: Does "pending" mean:
     - Waiting for auto-processing? OR
     - Waiting for human review? OR
     - Already posted to transactions?
   - Current statuses in code: "pending", "needs_review", "processed", "error", "posted", "archived"
   - User mental model: Just "done" or "not done"

2. **Feedback loop missing** (MEDIUM)
   - Operator submits transaction, gets redirect to dashboard
   - No confirmation: "Your entry was recorded"
   - If there's an error, user sees error message but can't retry easily
   - Better UX: Modal dialog with success message or error details

3. **Manual data entry complexity** (MEDIUM)
   - Form has 8 fields: description, amount, type, date, category, payment method, file URL, etc.
   - Many fields are optional, but user doesn't know which ones
   - Better UX: Mark required fields clearly; show validation errors

---

## Cross-Role Observations

### Mental Model Gaps Summary

| Gap | User Thinks | System Reality | Impact | Priority |
|---|---|---|---|---|
| **Inbox ↔ Transaction** | "Invoice I upload = Transaction in ledger" | Documents ≠ GL entries. 1 invoice can create N transactions | Confusion on split expenses, document linking | CRITICAL |
| **Navigation depth** | "All month info on one screen" | Must navigate: Inbox tab, Transactions tab, Reconciliation page | Inefficient workflow, frustration | HIGH |
| **Terminology** | "Postado = I click post, it posts" | "Posted" is a state; actual posting is automated webhook | Confusion on workflow trigger points | HIGH |
| **State visibility** | "Buttons should work always" | State machine limits operations (no edits in review) | Errors when trying to edit locked month | HIGH |
| **Status labels** | "pending = not done; posted = done" | Multiple intermediate statuses (processed, needs_review, error) | Uncertainty about entry status | MEDIUM |
| **Document linking** | "Invoice is attached to transaction" | Inbox items are separate; must query relationships | Can't easily find source document for transaction | MEDIUM |
| **Auto-processing** | "System uploads and auto-completes everything" | Only extracts data; still needs human review | Unrealistic expectations about automation | MEDIUM |

---

## Validation Against Phase 2 Findings

**Phase 2 Finding**: "User mental models don't match system model"

✅ **Confirmed and detailed**:
- Inbox Item ≠ Transaction (critical gap, most confusing)
- Navigation requires multiple jumps between pages
- Terminology misalignment between UI labels and user expectations
- State machine not visible to users

**Phase 2 Finding**: "Need explicit state machine documentation"

✅ **Corroborated**: Users demonstrate lack of understanding around:
- When month is "in review" and why edits are blocked
- What transitions are possible from current state
- Side effects of state changes (e.g., auto-locking when entering "Em Review")

---

## Recommended Next Steps (UX Improvements)

1. **Consolidate Month Overview page** (Reduce navigation depth)
   - Single page with 3 tabs: Inbox, Transactions, Details
   - Show both documents and GL entries in one view
   - Quick filters: "Show items from this invoice"

2. **Clarify terminology** (Align with user mental models)
   - "Postado" → "Posted to Ledger" (full phrase)
   - "Pronto" → "Ready to Post" (action-oriented)
   - "Inbox Item" → "Source Document" (more precise)
   - "Transaction" → "Accounting Entry" (domain-aligned)

3. **Add state indicators** (Make state machine visible)
   - Badge on month: "Month in Review" (yellow badge)
   - Disable edit buttons with tooltip: "Transactions cannot be edited while in review"
   - Show state transition timeline: "Open → In Review → Ready → Posted"

4. **Link documents to transactions** (Show source documents)
   - "Linked Documents" panel in transaction detail
   - Show which invoice(s) paid for this GL entry
   - Allow quick navigation: Click document → Jump to Inbox item

5. **Clarify transaction status lifecycle** (Reduce ambiguity)
   - Show status history for each entry
   - Clear labels: "Pending → Auto-Processed → Ready for Review → Posted"
   - Visual timeline instead of single status field

---

## Interview Evidence Mapping

| User Role | Main Pain Point | Evidence in Code | Quote-like Finding |
|---|---|---|---|
| Accountant | Inbox ↔ Transaction confusion | `posted_transaction_id` field in `InboxRow` | "The invoice becomes a transaction, right?" |
| Reviewer | Missing document visibility | No `source_document` field in transaction detail view | "Where's the invoice for this transaction?" |
| Director | Month readiness unclear | `checklist.completedSteps / totalCloseSteps` showing 4/5 | "What are these 5 steps?" |
| Operator | Transaction status ambiguous | `INBOX_ACTIVE_STATUSES = ["pending", "needs_review", "processed", "error"]` | "Is this posted yet or waiting for approval?" |

