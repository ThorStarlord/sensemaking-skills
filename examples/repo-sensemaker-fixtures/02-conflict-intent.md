# Repository Sensemaking Brief: Conflict Case

**Scenario**: User intent implies UI/UX focus, but codebase signals suggest architecture issues are blocking it.

---

## Repository Goal

Frontend delivery for customer dashboard redesign to improve customer visibility into usage metrics.

## Current Shape

- React frontend with monolithic state management (Redux, single 2,400-line store)
- API backend relatively clean (REST, proper separation)
- Heavy frontend→backend coupling on real-time data flows
- No event system; polling dominates (12 concurrent intervals in dashboard)

## Strong Signals

- 12 concurrent polling intervals in dashboard component
- Redux store at 2,400 lines (single reducer file)
- State mutations happening outside Redux patterns (3 direct DOM manipulations found)
- No async queue management; race conditions evident in API call logs
- 7 GitHub issues tagged "race condition" in past 6 months
- Customer complaints about dashboard latency and data inconsistency

## Missing Pieces

- No user research on what metrics matter to customers
- No performance baseline or SLA for dashboard responsiveness
- Competitive analysis of dashboard UX not documented

## Improvement Opportunities

- Implement event system to replace polling (would reduce 12 setIntervals to 2-3 subscribers)
- Split Redux store into feature-based modules (reduce complexity)
- Add request queue and backoff logic to prevent concurrent API errors

## Weakest Boundary

The architectural brittleness of the frontend is preventing the UI redesign from being stable. The new designs will multiply polling, race conditions, and state sync issues. **This is a binding constraint** the user intent didn't anticipate.

## Evidence

- `src/components/Dashboard.tsx` line 340-350: 12 setInterval calls
- `src/redux/reducers.ts` 2,400 lines total, single file
- `src/api/client.ts` line 205-225: No queue/backoff logic implemented
- 7 GitHub issues tagged "race condition" in past 6 months
- Production logs show 3-5 data consistency errors per day

## Evidence Excerpts

```yaml
evidence_excerpts:
  - file: src/components/Dashboard.tsx
    lines: 340-350
    quote: "setInterval(() => fetchMetrics(), 5000); setInterval(() => fetchUsers(), 3000); // ... 10 more"
    supports_claim: "12 concurrent polling intervals cause race conditions"
  
  - file: src/redux/reducers.ts
    lines: 1-10
    quote: "export default function reducer(state = initialState, action) { ... } // 2,400 lines total"
    supports_claim: "Monolithic Redux store is difficult to maintain and reason about"
  
  - file: github/issues
    lines: issue-2847
    quote: "Dashboard shows stale data after rapid user actions: TypeError in state sync"
    supports_claim: "Race conditions cause customer-visible bugs"
```

## Why This Boundary Matters

UI redesigns compound architectural problems. Without fixing polling/state sync first, the new design will inherit the same brittleness, causing the new UX to feel slow and unreliable. This is a **hard binding constraint** that blocks the requested UI work.

## Candidate Next Steps

1. Escalate to full-fog-workflow (architecture must be addressed first)
2. Refactor state management before UI redesign begins
3. Implement event system to replace polling
4. Establish dashboard performance SLAs

## Recommended Next Step

Escalate to full-fog-workflow. UI redesign is not blocked by design skill; it's blocked by architectural refactoring of state management and data synchronization.

## Recommended Workflow

full-fog-workflow

## Ready to Copy Prompt

```
You are evaluating a UI redesign request for a dashboard, but the current architecture has fundamental scalability issues.

Context:
- User requested: Dashboard UI redesign for better metrics visibility
- Reality: Frontend uses 12 concurrent polling intervals with no queue management
- Impact: Race conditions cause data inconsistency (3-5 errors/day in production)
- Constraint: Redesigning the UI without fixing architecture will make the problem worse, not better

Task:
1. Document the architectural dependencies blocking the UI work
2. Estimate effort to refactor state management before UI redesign
3. Propose a phased approach: fix architecture first (Sprint 1), then redesign (Sprint 2)
4. Estimate total timeline and risk if architecture is skipped

Deliverable: Decision document with recommended approach (escalation rationale).
```

---

## Machine-Readable Handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: ../../00-user-intent.md
recommended_workflow_id: null
recommended_execution_mode: null
weakest_boundary: frontend_state_architecture
required_inputs:
  - user_intent
  - repository_state
user_implied_fog_type: ui_fog
primary_fog_type: architecture_fog
secondary_fog_type: ui_fog
diagnosis_conflict: true
conflict_type: requested_solution_not_binding_constraint
escalation_recommended: true
escalation_target: full-fog-workflow
escalation_reason: intent_diagnosis_conflict
auto_escalation_allowed: false
created_at: "2026-05-19T16:05:00Z"
```
