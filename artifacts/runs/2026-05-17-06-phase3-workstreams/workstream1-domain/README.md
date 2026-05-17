# Phase 3, Workstream 1: Domain Model Specification

**Status**: ✅ COMPLETE (2026-05-17)  
**Total Output**: 8 documents, 3,000+ lines, 153 KB  
**Critical Gaps Closed**: 5/5 from Phase 2 interviews  

---

## Quick Navigation

### For Reading (Start Here)

**First time?** Read in this order:

1. **[DOMAIN-MODEL-SPEC.md](DOMAIN-MODEL-SPEC.md)** (23 KB, 15 min read)
   - **What**: Consolidated authoritative specification
   - **Why**: Single source of truth for domain model
   - **Contains**: States, transitions, rules, UX alignment, technical approach
   - **Best for**: Understanding the complete picture

2. **[WORKSTREAM-1-SUMMARY.md](WORKSTREAM-1-SUMMARY.md)** (12 KB, 10 min read)
   - **What**: High-level overview of what was delivered
   - **Why**: Quick summary of all documents
   - **Best for**: Getting stakeholder buy-in; executive overview

3. **[COMPLETION-REPORT.md](COMPLETION-REPORT.md)** (16 KB, 12 min read)
   - **What**: Detailed completion status and metrics
   - **Why**: Proof of work and readiness for Phase 4
   - **Best for**: Project tracking and handoff validation

---

### For Deep Dives (By Role)

**Product/UX Team**: Read these

1. **[DOMAIN-MODEL-SPEC.md](DOMAIN-MODEL-SPEC.md)** (Part 1 & 2)
   - States and their user-facing meaning
   - State transition UX flows
   - Error message examples

2. **[04-domain-ux-sync.md](04-domain-ux-sync.md)** (19 KB, 20 min read)
   - State-to-screen mapping
   - UX flow for each transition
   - Status badge design
   - Unresolved UX questions for your team

**Backend/Technical Team**: Read these

1. **[DOMAIN-MODEL-SPEC.md](DOMAIN-MODEL-SPEC.md)** (Part 1 & 3)
   - State definitions and invariants
   - State machine validation algorithm
   - n8n webhook contract

2. **[05-domain-technical-sync.md](05-domain-technical-sync.md)** (32 KB, 25 min read)
   - Database schema changes
   - TypeScript types and validation
   - Server action patterns
   - n8n integration (retry logic, timeout recovery)
   - Testing strategy
   - Implementation effort estimate
   - Unresolved technical questions for your team

**Finance/Domain Expert**: Read these

1. **[DOMAIN-MODEL-SPEC.md](DOMAIN-MODEL-SPEC.md)** (Complete)
   - All states and business rules
   - Reconciliation rules
   - n8n posting workflow

2. **[02-explicit-state-machine-spec.md](02-explicit-state-machine-spec.md)** (25 KB, 20 min read)
   - Detailed state definitions
   - Transition conditions
   - Domain invariants

3. **[03-business-rules-spec.md](03-business-rules-spec.md)** (21 KB, 20 min read)
   - Complete business rules
   - Exception handling
   - Access control

---

### For Comparative Analysis (If Migrating from Old System)

1. **[01-current-state-machine-analysis.md](01-current-state-machine-analysis.md)** (17 KB, 20 min read)
   - **What**: Audit of current implicit state machine
   - **Why**: Shows what was wrong and what we fixed
   - **Best for**: Understanding migration path; why new model is better

---

## Document Map

| Document | Size | Audience | Purpose |
|----------|------|----------|---------|
| **DOMAIN-MODEL-SPEC.md** | 23 KB | Everyone | Consolidated authoritative spec |
| **WORKSTREAM-1-SUMMARY.md** | 12 KB | Stakeholders | High-level overview |
| **COMPLETION-REPORT.md** | 16 KB | Project managers | Metrics and status |
| **01-current-state-machine-analysis.md** | 17 KB | Engineers, domain experts | What was implicit; what we fixed |
| **02-explicit-state-machine-spec.md** | 25 KB | Engineers, domain experts | Detailed state definitions |
| **03-business-rules-spec.md** | 21 KB | Domain experts, engineers | Business rules and exceptions |
| **04-domain-ux-sync.md** | 19 KB | Product, UX, designers | UX flows and state-to-screen mapping |
| **05-domain-technical-sync.md** | 32 KB | Backend engineers | Implementation roadmap |

---

## Key Features of This Specification

### ✅ Explicit State Machine

**4 States**:
- `ABERTO` (Open) — Accepting transactions
- `EM_REVIEW` (In Review) — Director reviewing
- `PRONTO` (Ready) — Approved, awaiting GL posting
- `POSTADO` (Posted) — Officially posted to GL

**5 Documented Transitions**:
- ABERTO → EM_REVIEW (send to review)
- EM_REVIEW → PRONTO (approve)
- EM_REVIEW → ABERTO (reject)
- PRONTO → POSTADO (post to GL)
- POSTADO → ABERTO (reopen for corrections)

### ✅ Complete n8n Integration

- Webhook payload specification
- Success/error response contracts
- 3-retry exponential backoff
- **Timeout recovery**: Queries GL system to verify if posting succeeded
- All error codes documented with handling strategy

### ✅ Data Invariants

- 25+ invariants specified
- State invariants enforced by database CHECK constraints
- All preconditions validated before state change
- All side effects documented

### ✅ UX Alignment

- State-to-screen mapping
- UX flow for each transition
- Error message examples
- Status badge design
- Navigation recommendations

### ✅ Technical Implementation

- Database schema (10+ new columns)
- TypeScript types and validation functions
- Server action patterns
- n8n webhook error handling
- 2-3 week implementation timeline

---

## Critical Gaps Closed

| Gap | Evidence | Document |
|-----|----------|----------|
| **#1: State Machine Not Defined** | 4 explicit states with complete definitions | 02-explicit-state-machine-spec.md |
| **#2: Aggregation Fragility** | Preconditions prevent invalid states | 02 + 03-business-rules-spec.md |
| **#3: Auto-Post Recovery Missing** | Timeout recovery with GL query | 03 + 05-domain-technical-sync.md |
| **#4: Dashboard Semantics Unclear** | Each state has explicit meaning and badge | 04-domain-ux-sync.md |
| **#5: n8n Webhook Undocumented** | Complete webhook contract with error scenarios | 03-business-rules-spec.md |

---

## Next Steps

### For UX Workstream 2
1. Read: `DOMAIN-MODEL-SPEC.md` (Part 2) + `04-domain-ux-sync.md`
2. Design: New EM_REVIEW screens + updated flows + error messages
3. Answer: 7 outstanding UX questions
4. Validate: Against domain spec before implementation

### For Technical Workstream 3
1. Read: `DOMAIN-MODEL-SPEC.md` (Part 3) + `05-domain-technical-sync.md`
2. Plan: Database migration, schema updates, n8n integration
3. Answer: 5 outstanding technical questions
4. Validate: Implementation approach against domain spec

### For Phase 4
1. Merge: Workstream 2 (UX) + Workstream 3 (Technical) outputs
2. Implement: Database schema, backend state machine, UX flows
3. Test: Unit, integration, e2e coverage
4. Deploy: Staged rollout to production

---

## Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| States defined | 4 | 4 | ✅ |
| Transitions documented | 5+ | 5 | ✅ |
| Preconditions specified | All | Yes | ✅ |
| Error scenarios | 5+ | 7+ | ✅ |
| Business rules | 10+ | 15+ | ✅ |
| Data invariants | 20+ | 25+ | ✅ |
| UX flows mapped | 5 | 5 | ✅ |
| Stakeholder validation | 3/3 | 3/3 | ✅ |
| Phase 2 gaps closed | 5/5 | 5/5 | ✅ |

---

## FAQ

**Q: Can I start reading just one document?**  
A: Yes! Read `DOMAIN-MODEL-SPEC.md` first. It's self-contained and references others.

**Q: What if I only care about UX?**  
A: Read `DOMAIN-MODEL-SPEC.md` Part 2 + `04-domain-ux-sync.md`.

**Q: What if I only care about technical implementation?**  
A: Read `DOMAIN-MODEL-SPEC.md` Part 3 + `05-domain-technical-sync.md`.

**Q: When can Phase 4 start?**  
A: Now! UX and Technical can work in parallel using this spec.

**Q: What if I find something wrong in the spec?**  
A: This is before Phase 4 implementation. Now is the time to catch issues! File an issue or comment in the PR.

**Q: How long to implement this?**  
A: 2-3 weeks total (all teams working in parallel). See `COMPLETION-REPORT.md` for detailed timeline.

---

## Git History

```
f656f40 docs: add Workstream 1 completion report
d6a35df feat: complete Workstream 1 (Domain Model) - Phase 3 Finance specification
  ├── 04-domain-ux-sync.md (NEW)
  ├── 05-domain-technical-sync.md (NEW)
  └── DOMAIN-MODEL-SPEC.md (NEW)
```

---

## Document Sizes

```
DOMAIN-MODEL-SPEC.md              23 KB  (600 lines) — Start here
05-domain-technical-sync.md       32 KB  (900 lines) — For engineers
02-explicit-state-machine-spec.md 25 KB  (700 lines) — For deep dive
03-business-rules-spec.md         21 KB  (600 lines) — For business rules
04-domain-ux-sync.md              19 KB  (400 lines) — For UX team
COMPLETION-REPORT.md              16 KB  (380 lines) — For metrics
01-current-state-machine-analysis 17 KB  (400 lines) — For comparison
WORKSTREAM-1-SUMMARY.md           12 KB  (250 lines) — For overview

TOTAL: 165 KB, 3,830 lines
```

---

**Workstream 1 Status**: ✅ COMPLETE  
**Next Review**: UX Workstream 2 — 2026-05-18  
**Next Review**: Technical Workstream 3 — 2026-05-18  
**Phase 4 Ready**: YES ✅

*For questions or clarifications, see outstanding questions in respective workstream docs.*
