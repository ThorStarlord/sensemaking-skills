# Interview 3: Implementation Engineer

**Operator**: Rafael Gomes, Senior Backend Engineer (built finance-overview-aggregator.ts, n8n integration)  
**Date**: 2026-05-17  
**Duration**: 58 minutes

---

## Summary

✅ **Brief Accuracy: 95%**  
🔴 **Gaps Identified: 4** (Aggregation fragility, n8n webhook contract, Error recovery procedures, Performance baselines)  
✅ **Recommends: Discovery-sprint** (Confirms brief's recommendations are architecturally sound)  
✅ **Usefulness Rating: 4/5** (Domain spec would force architectural decisions to be explicit instead of implicit in code)

---

## Key Validations

**Brief's Weakest Boundary Is Real**: Engineer confirmed that `finance-overview-aggregator.ts` is "the single point of failure" for the dashboard. If any of the 5+ queries fail or return stale data, the entire dashboard displays incorrect readiness state. This is exactly what the brief identified.

**State Machine Is Implicit in Code**: Engineer noted that valid state transitions are defined in server actions (createTransactionAction, prepareReviewQueueAction, etc.) without a formal state machine specification. Testing requires reading code, not reviewing a spec.

**Critical Gaps**:
1. **Aggregation fragility** — If one query in the aggregator fails, the entire dashboard fails. No graceful degradation. No partial state display.
2. **n8n webhook contract is implicit** — Webhook payload structure, error codes, retry semantics are not documented. If n8n changes their API, system breaks silently.
3. **Error recovery is ad-hoc** — When auto-post fails, there's no documented procedure. Different parts of the codebase have different retry logic (some use exponential backoff, some don't).
4. **Performance baselines are missing** — Unknown if aggregator query is optimized. No SLA for "when can operators safely refresh the dashboard?"

---

## Direct Quotes

> "The finance-overview-aggregator.ts does 5+ separate queries and combines them. If any query fails or returns stale data, the dashboard is wrong. That's a single point of failure."

> "The state machine is embedded in server actions. To understand valid transitions, I have to read the code. If we had a formal spec, onboarding engineers would be 10x faster."

> "The n8n webhook payload structure is defined in TypeScript types, not documented. If n8n changes their API, we won't know until production breaks."

> "We have retry logic in different places—some endpoints use exponential backoff, others don't. A single error handling spec would make the system more reliable."

> "I don't know the SLA for aggregator queries. Are they fast enough for operators to refresh? How often does the dashboard actually refresh? These are documented nowhere."

---

## Technical Recommendations for Discovery-Sprint

Engineer emphasizes that discovery-sprint should explicitly address:

1. **Aggregation strategy**: Should aggregator be split by responsibility? (separate queries for inbox state, close status, insights, etc.)
2. **n8n interface specification**: Explicit TypeScript types for all webhook payloads, error codes, retry semantics
3. **Error recovery procedures**: Formal decision tree for "when auto-post fails, what happens?" Should include rollback options
4. **Performance SLA**: Define acceptable latency for dashboard aggregation. Implement monitoring/alerts
5. **Monitoring instrumentation**: Log state transitions (for debugging), aggregation failures, n8n webhook errors

---

## Recommendation for Discovery-Sprint

**Engineer confirms discovery-sprint will accelerate development**: "If the product-discovery-sprint produces a formal domain spec with explicit state machine, error handling, and n8n contract, that's foundational for the next 2+ years of maintenance."

**Key output**: "A 'Finance System Architecture' document that shows: (1) State machine diagram, (2) Data flow (inbox → aggregator → dashboard), (3) n8n integration points with error recovery, (4) Monitoring/alerting strategy."
