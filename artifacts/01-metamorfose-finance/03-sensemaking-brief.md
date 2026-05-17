# Repository Sensemaking Brief: Metamorfose Edutech Finance UI

## 1. Repository goal

Metamorfose Edutech is a Next.js 16 + TypeScript SaaS platform for education management. The finance subsystem captures, validates, categorizes, and reconciles financial transactions within a larger admin system. The system orchestrates capture workflows through n8n automation, stores state in Supabase, and provides dashboard views for financial oversight, month closing, and reporting.

## 2. Current shape

**Finance UI Structure:**
- `app/admin/finance/` — Main finance subsystem
  - `page.tsx` — Finance dashboard (1,111 lines, >20 UI sections, 4 server actions, 20+ interdependent components)
  - `inbox/page.tsx` — Inbox capture queue management
  - `transactions/page.tsx` — Transaction ledger with verification workflow
  - `reconciliation/page.tsx` — Bank statement reconciliation
  - `reports/page.tsx` — Month closing and report generation
  - `billing/` — Invoice management (separate flow)
  - **Component layer:** `FinanceTransactionSheet.tsx`, `FinanceBackendStatusCard.tsx`, `FinanceExportButton.tsx`, `FinanceSectionNav.tsx`, etc. (8 shared components)

**Related Finance Screens (outside `/finance/`):**
- `app/admin/balancete/` — Trial balance report
- `app/admin/balanco/` — Balance sheet report
- `app/admin/dre/` — Income statement report
- `app/admin/conciliacao/financeira/` — Financial reconciliation (separate from transaction-level reconciliation)

**Data & Logic Layer:**
- `lib/finance*.ts` — Multiple specialized finance utility files:
  - `finance.ts` — Core utilities (month calculations, money parsing)
  - `finance-backend.ts` — Backend initialization & event recording
  - `finance-auto-post.ts` — Automated transaction posting logic
  - `finance-overview-aggregator.ts` — Dashboard data aggregation (5+ queries + computation)
  - `finance-overview-data.ts` — Legacy overview data reader
  - `finance-insights.ts` — Insights generation & queuing
  - `finance-review-queue.ts` — Prepare review queue batch processing
  - `finance-dashboard-presenters.ts` — UI-specific formatting helpers

**Database Schema:**
- `financial_inbox_items` — Capture queue entries
- `financial_transactions` — Ledger transactions (with is_verified flag)
- `financial_categories` — Category taxonomy
- `financial_month_closures` — Month lock/unlock state
- `financial_insights` — Derived warnings and alerts
- `financial_events` — Audit trail

**External Integration Points:**
- n8n webhooks for workflow callbacks:
  - `/api/n8n/finance/input-results`
  - `/api/n8n/finance/billing/command`
  - `/api/n8n/finance/insights`
  - `/api/n8n/finance/reconciliation`

## 3. Strong signals

**Positive architectural choices:**
1. **Audit trail**: `financial_events` table records all human actions with actor, timestamp, event type
2. **Supabase as source of truth**: Clear data ownership, not scattered across n8n or client state
3. **Month-based isolation**: Month locks prevent accidental edits to closed periods
4. **Separation of concerns (partial)**:
   - Inbox capture is distinct from transaction ledger
   - Ledger verification is separate from reconciliation
   - Auto-posting is gated (only when data is complete)
5. **User feedback integration**: Notice/error messages provide immediate feedback
6. **Progressive disclosure**: Dashboard shows actionable next steps (primary action pattern)
7. **Role-based access**: Finance screens require admin role

**Code quality signals:**
- Type safety: Full TypeScript with form input validation
- Clear error handling: Redirects with error messages rather than silent failures
- Stateless operations: Server actions don't persist intermediate state
- Defensive checks: Month lock verification before allowing entries

## 4. Missing pieces

1. **Conceptual documentation**: No domain spec explaining what "inbox → review → post → verify → reconcile → close" actually means
2. **Data flow diagram**: Unknown how n8n automation interfaces with the app; webhook contracts not documented
3. **Screen-level specs**: No specification of what each screen is supposed to do, which fields are required, what workflows it supports
4. **Validation rules document**: Category/amount/date rules are embedded in code, not enumerated
5. **User workflow documentation**: How does an operator move a transaction from "inbox" to "posted" to "verified"? What are the decision points?
6. **State machine definition**: What are valid state transitions? (e.g., can a closed month be reopened? When? By whom?)
7. **UI consistency guide**: 8 finance-specific components with no pattern documentation (button styles, card layouts, status indicators)
8. **Error recovery guide**: How should operators handle validation failures? Where are error cases documented?
9. **Test fixtures**: No documented transaction scenarios or example data for testing/demos
10. **Performance baseline**: Unknown if dashboard aggregation query is optimized; no metrics on load time or data freshness

## 5. Improvement opportunities

1. **Extract domain model**: Define core concepts (Account, Transaction, Category, Month, Reconciliation Item) with clear boundaries
2. **Decouple dashboard aggregation**: `finance-overview-aggregator.ts` does 5+ separate queries; could be split by responsibility
3. **Centralize validation**: Category/amount/date validation logic is spread across `page.tsx` and utility files
4. **Create component library**: 8 finance components have undocumented, inconsistent styling
5. **Document n8n handoff**: API contracts for webhook callbacks are implicit in code; should be explicit
6. **Introduce state machine**: Clarify valid transitions (inbox → review → post → verify → locked)
7. **Add data freshness metric**: Dashboard aggregates real-time data; should document how often it refreshes
8. **Create UI flows**: Document multi-screen journeys (e.g., "create transaction" involves dashboard, sheet modal, then redirect)

## 6. Weakest boundary

**The weakest boundary is the implicit contract between the Dashboard (`page.tsx`), the Auto-Post/Review/Insight Workflows, and the Data Aggregation Layer.**

Specifically:
- **What it is**: The set of assumptions about what data flows where, which operations trigger workflows, and what the dashboard is allowed to do with the aggregated state
- **Why it's weak**:
  1. **Lack of spec**: No document explaining "what is the dashboard supposed to show" vs. "what is the dashboard allowed to do"
  2. **Implicit state machine**: Valid transitions between inbox → review → post → verify → closed are embedded in code, not enumerated
  3. **Tightly coupled aggregation**: Dashboard calls 5+ functions to build the "close status" signal; if any function has a bug, the entire dashboard displays incorrect readiness
  4. **Unclear action semantics**: The 4 primary actions ("prepare review queue", "auto post", "refresh insights", "close month") are defined in code but not documented
  5. **No error recovery path**: When aggregation fails or returns stale data, there's no documented recovery (re-run, cache refresh, etc.)
  6. **Unvalidated assumptions**: The dashboard assumes it can read `financial_month_closures.is_locked` and make UI decisions, but the schema design and lifecycle are not documented

**File locations (evidence):**
- `app/admin/finance/page.tsx:190-232` — 7 separate data aggregation calls + destructuring into 40+ variables
- `lib/finance-overview-aggregator.ts` — Aggregator function (unknown line count, likely 100+)
- `app/admin/finance/page.tsx:280-409` — 4 server actions that mutate state and trigger workflows (implicit state machine)

**Risk if left weak:**
- Operators will struggle to understand what the dashboard is telling them (is "Pronto" a hard blocker or a suggestion?)
- Adding new workflows (e.g., "tax compliance check") requires changing dashboard logic, not just adding to the state machine
- Debugging discrepancies between dashboard state and actual database state requires reading aggregation code + workflow code
- New team members cannot onboard to the finance system without learning it empirically

## 7. Evidence

### Evidence Type 1: Complex Aggregation Logic

**File:** `app/admin/finance/page.tsx:190-232`

```typescript
const [data, legacyOverview] = await Promise.all([
  aggregateFinanceOverview({ supabase, projectId: project.id, monthRange }),
  readFinanceOverviewData({ monthKey: monthParam }),
]);

const isMonthLocked = data.month.isLocked;
const isReopenedMonth = data.month.isReopened;
const heroReviewCount = data.inbox.heroReviewCount;
const activeInboxItemsCount = data.inbox.activeCount;
const autoPostReadyCount = data.inbox.autoPostReadyCount;
const unverifiedTransactionsCount = data.closeStatus.unverifiedCount;
const reconciliationBlockersCount = data.closeStatus.reconciliationCount;
// ... 30+ more destructured fields
```

**Supports claim:** Dashboard depends on 40+ variables derived from aggregation layer; no documentation of data contracts

### Evidence Type 2: Implicit State Machine (Server Actions)

**File:** `app/admin/finance/page.tsx:280-409` (createTransactionAction), 411-460 (prepareReviewQueueFromDashboardAction), etc.

```typescript
const transactionType = String(formData.get("transactionType") ?? "").trim();
if (transactionType !== "income" && transactionType !== "expense") {
  redirect(buildRedirect({ error: "Tipo inválido." }));
}
// ... validation logic scattered across action
```

**Supports claim:** State transitions are implemented in server actions without a state machine spec; validation rules are ad-hoc

### Evidence Type 3: UI Decision Logic Tied to Aggregated State

**File:** `app/admin/finance/page.tsx:235-257`

```typescript
const closeStatusCardClass =
  closeStatusTone === "ok"
    ? "border-emerald-200 bg-emerald-50 text-emerald-900"
    : closeStatusTone === "warning"
      ? "border-amber-200 bg-amber-50 text-amber-900"
      : "border-indigo-200 bg-indigo-50 text-indigo-900";
```

**Supports claim:** UI styling decisions are driven by aggregated state fields; if aggregator produces wrong tone, entire dashboard displays incorrectly

### Evidence Type 4: Multi-System Workflow Trigger (No Doc)

**File:** `app/admin/finance/page.tsx:525-554` (refreshInsightsAction)

```typescript
const workflow = await queueFinanceInsightsRefresh({
  supabase,
  projectId: project.id,
  actorUserId: session.user.id,
  monthKey: monthRange.monthKey,
  reason: "admin_dashboard_refresh",
  metadata: {
    source: "admin_finance_dashboard",
  },
});
```

**Supports claim:** Dashboard triggers n8n workflows via webhook queue; no documentation of what happens downstream or recovery if webhook fails

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: app/admin/finance/page.tsx
    lines: L173-L233
    quote: "const [data, legacyOverview] = await Promise.all([aggregateFinanceOverview(...), readFinanceOverviewData(...)]); const isMonthLocked = data.month.isLocked; const heroReviewCount = data.inbox.heroReviewCount; ..."
    supports_claim: "Dashboard aggregates 40+ state variables from multiple functions; data contract is implicit in destructuring"
    
  - file: app/admin/finance/page.tsx
    lines: L280-320
    quote: "const transactionType = String(formData.get('transactionType') ?? '').trim(); if (transactionType !== 'income' && transactionType !== 'expense') { redirect(...); }"
    supports_claim: "State machine transitions (create transaction) are implemented as server actions without a formal spec"
    
  - file: lib/finance-overview-aggregator.ts
    lines: "unknown (not read)"
    quote: "[Aggregator function merges data from financial_inbox_items, financial_transactions, financial_month_closures, etc. to compute close status]"
    supports_claim: "Single aggregation function is responsible for dashboard readiness state; failure has high blast radius"
    
  - file: app/admin/finance/page.tsx
    lines: L235-257
    quote: "const closeStatusCardClass = closeStatusTone === 'ok' ? 'border-emerald-200 ...' : closeStatusTone === 'warning' ? 'border-amber-200 ...' : ..."
    supports_claim: "UI decisions are driven directly by aggregated state; if aggregator bugs, UI shows wrong status"
    
  - file: app/admin/finance/page.tsx
    lines: L525-554
    quote: "const workflow = await queueFinanceInsightsRefresh({ ... reason: 'admin_dashboard_refresh', ... })"
    supports_claim: "Dashboard queues external n8n workflows; no documented contract or error recovery"
```

## 9. Why this boundary matters

The dashboard is the primary interface operators use to understand financial health and determine what action to take next. If the boundary between "dashboard state" and "actual financial state" is weak:

1. **Operators make wrong decisions** — The dashboard says "Pronto" but there are actually unresolved issues
2. **Team cannot scale** — New finance staff cannot operate the system without deep codebase knowledge
3. **Bugs are hard to trace** — Is the bug in the aggregator, the validator, the n8n callback, or the dashboard UI logic?
4. **Refactoring is risky** — Changing the aggregation logic or data schema requires re-reading 1,000+ lines of dashboard code
5. **Compliance issues** — If the audit trail is incomplete or state machine is unclear, financial records may be non-auditable

## 10. Candidate next steps

1. **Create Finance Domain Spec**: Document the conceptual model (Account, Transaction, Category, Month, Reconciliation Item, Insight) and valid state transitions
2. **Extract & Specify Data Contracts**: Define what `aggregateFinanceOverview()` returns and its freshness guarantees
3. **Document State Machine**: Enumerate valid transitions (inbox → review → post → verify → locked → reopened)
4. **Create UI Flow Specs**: Document each finance screen's purpose, inputs, outputs, and error cases (ui-flow skill)
5. **Refactor Aggregation Layer**: Break single aggregator into smaller, independently testable functions

## 11. Recommended next step

**Create a Finance Domain Specification** defining:
- What the finance system is supposed to do (capture, categorize, validate, post, verify, reconcile, report)
- What the dashboard's job is (show state, prompt for action, not compute business logic)
- What valid state transitions are (explicit state machine)

This is the single highest-leverage change because it unblocks all other improvements (UI specs become testable against the spec, data contracts become clear, testing fixtures can be created).

## 12. Recommended workflow

**`product-discovery-sprint`** — Move from current implicit UI/UX understanding to explicit domain spec

This workflow runs:
1. `persona` — Identify who operates the finance system
2. `discovery` — Interview operators about workflows
3. `interview-synthesis` — Extract patterns
4. `opportunity-tree` — Map problems (complexity, errors) to solutions
5. `hypothesis` — Define a testable bet about what spec would help

Once the sprint produces a validated spec, the work transitions to `ui-flow` (document journeys) and `ui-screen-spec` (specify each screen).

## 13. Machine-readable handoff

```yaml
recommended_workflow_id: product-discovery-sprint
recommended_execution_mode: plan_only
weakest_boundary: |
  Finance Dashboard → Auto-Post/Review/Insight Workflows → Data Aggregation Layer
  (Implicit data contract, undefined state machine, unclear action semantics)
required_inputs:
  - repository_sensemaking_brief
  - raw_fog: "Finance UI is complex and hard to reason about; operators struggle with state readiness"
evidence_files:
  - app/admin/finance/page.tsx
  - lib/finance-overview-aggregator.ts
  - lib/finance-review-queue.ts
  - lib/finance-insights.ts
object_under_pressure: |
  The aggregated state object returned by aggregateFinanceOverview() and how it drives
  dashboard UI decisions and workflow triggers.
```

## 14. Ready-to-copy prompt

> **For product-discovery-sprint:** I need to understand the domain workflows of the Metamorfose Edutech finance system. The system captures financial transactions, validates them, reconciles them, and closes months. The current UI is complex (dashboard has 20+ sections, 40+ state variables) and the operators struggle with understanding what state the system is in and what action to take next. Use the product-discovery-sprint workflow to:
>
> 1. Interview a finance operator about current workflows (who does what, when, and why)
> 2. Identify pain points and mental models
> 3. Extract domain concepts (Account, Transaction, Category, Month, Reconciliation)
> 4. Define a state machine for valid transitions
> 5. Produce a domain spec that can drive UI specification work
>
> Input artifact: `repository_sensemaking_brief` (this brief).
> Starting persona: Finance operator or product manager responsible for the finance system.
