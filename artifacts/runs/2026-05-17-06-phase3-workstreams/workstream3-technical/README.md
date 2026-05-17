# Workstream 3: Technical Architecture Specification

**Phase 3 Technical Foundation**  
**Completed**: 2026-05-17

## Overview

This workstream audited the finance module's server architecture, identified duplication patterns, and designed a comprehensive solution with 4 abstraction layers to eliminate 350+ lines of duplicated code while enabling new capabilities like n8n integration.

## Documents

### 1. **TECHNICAL-ARCHITECTURE-SPEC.md** (Executive Summary)
**Start here** - Complete specification with:
- Executive summary of findings and solutions
- 4-layer architecture design with code examples
- Phase 4 implementation roadmap (4 weeks)
- n8n integration design
- Risk assessment and success metrics
- Sign-off checklist for all teams

**Key Stats**:
- ✅ 18 server actions audited
- ✅ 5 duplication patterns identified (620+ lines)
- ✅ 350+ lines of code elimination planned
- ✅ 70-90% code reduction in affected areas

---

### 2. **01-server-architecture-audit.md** (Detailed Audit)
Current state analysis:
- Complete inventory of all 18 server actions (2,800+ lines total)
- 5 major duplication patterns with code examples
- Infrastructure assessment (database, external services, error handling)
- Duplication metrics by pattern
- Architectural gaps and recommendations

**Best for**: Understanding what needs to change and why

---

### 3. **02-validation-schemas.md** (Validation Layer Design)
Zod schema centralization strategy:
- Problem: validation scattered across actions (regex patterns repeated 6+ times)
- Solution: centralized Zod schemas in `lib/schemas/`
- Complete example schemas for all finance entities
- Client-side reuse capability
- 75% reduction in validation code per action
- Testing strategy for schemas
- Migration path (3 weeks)

**Lines Saved**: 150+ lines (75% reduction)

---

### 4. **03-error-handling-strategy.md** (Error Handling Design)
Typed Result pattern for all server actions:
- Problem: errors currently via URL parameters (loseable, untypeable)
- Solution: discriminated union `Result<T>` type with ErrorCode enum
- 15+ error codes covering all scenarios
- Client-side error handling patterns
- Batch operation error handling (partial success)
- Error messages dictionary (ready for i18n)
- Testing error conditions
- Integration with validation layer

**Impact**: Enables sophisticated error handling, analytics, and debugging

---

### 5. **04-data-access-layer.md** (Data Access Design)
Query consolidation into reusable functions:
- Problem: 12+ similar Supabase queries inlined in actions (100+ lines duplicated)
- Solution: `lib/data-access/` with typed query functions
- Functions for transactions, categories, months, payables, etc.
- Each function handles: query logic, error mapping, type safety
- Future caching capability without touching action code
- Transaction queries: `getTransactionsByMonth()`, `getTransaction()`, `setTransactionVerified()`, etc.
- Category queries: `getCategoryByName()`, `getOrCreateCategory()`
- Month queries: `isMonthLocked()`, `lockMonth()`, `unlockMonth()`
- Unit testing data access layer
- 80%+ reduction in query code

**Lines Saved**: 80+ lines (90% reduction per duplicated query)

---

## Key Findings

### Duplication Patterns (620+ lines)
| Pattern | Count | Lines | Solution |
|---------|-------|-------|----------|
| Session validation | 8 | 40 | Helper function |
| Month lock validation | 6 | 90 | Data access function |
| Create/insert patterns | 7 | 280 | CRUD abstraction |
| Audit event recording | 7 | 56 | Automatic logging |
| Supabase queries | 12+ | 100+ | Data access layer |

### Solution Architecture (4 Layers)

```
Layer 1: Validation Layer (Zod schemas)
         → Eliminates inline regex, consistent error messages
         
Layer 2: Error Handling (Result<T> type)
         → Typed responses, structured error codes
         
Layer 3: Data Access Layer (Query functions)
         → Single source of truth for all DB queries
         
Layer 4: CRUD Abstractions (Generic helpers)
         → Automatic audit logging, consistent business logic
```

### Expected Impact

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total code | 2,800+ lines | 2,400 lines | -14% |
| Duplication | 620 lines (22%) | 40 lines (1.5%) | 93% |
| Validation code | 500+ lines | 150 lines | -70% |
| Query consolidation | 12+ similar | 1 function | -100% |
| Test coverage | 20% | 90% | +350% |
| Audit log coverage | Inconsistent | Automatic | +100% |

---

## Phase 4 Implementation

### Timeline: 4-5 weeks

**Week 1**: Foundation (Result type, Zod schemas, data access)
**Week 2**: Layer integration (refactor 3-4 create actions)
**Week 3**: Rollout (refactor remaining actions, testing)
**Week 4**: Advanced features (caching, n8n integration)
**Week 5**: Refinement (documentation, monitoring)

### Deliverables
- ✅ 4 abstraction layers fully implemented
- ✅ All 18 server actions refactored
- ✅ 95%+ test coverage on data access layer
- ✅ n8n webhook integration operational
- ✅ Caching layer (if needed)
- ✅ Team training and documentation

---

## n8n Integration

**Webhook Endpoint**: `POST /api/webhooks/n8n/post-month`

**Workflow**: Month closed → n8n webhook → GL posting → Audit log

**Request Contract**:
```json
{
  "projectId": "uuid",
  "monthKey": "2026-05",
  "summary": {
    "totalIncome": 50000,
    "totalExpense": 35000,
    "transactionCount": 47,
    "unverifiedCount": 0
  }
}
```

**Response**: GL post ID or typed error with retry guidance

---

## Dependencies & Coordination

### Domain Workstream
- Validate state machine can be implemented with these abstractions
- Confirm error codes cover all domain scenarios
- Ensure audit logging meets compliance requirements

### UX/Frontend Team
- Validate error messages are user-friendly
- Confirm error codes enable smart client handling
- Test form validation using same schemas

### DevOps/Integration
- Validate n8n webhook contract
- Set up webhook retry logic monitoring
- Configure GL posting endpoint

---

## Success Criteria

- ✅ **Architecture**: 4 layers designed, documented, ready for implementation
- ✅ **Audit**: 5 duplication patterns identified with metrics
- ✅ **Abstractions**: 3+ major abstractions with code savings >300 lines
- ✅ **Data Access**: Query consolidation functions designed
- ✅ **Validation**: Zod schema library structure defined
- ✅ **Error Handling**: Typed Result pattern specified, 15+ error codes defined
- ✅ **n8n Integration**: Webhook contract defined, implementable
- ✅ **Testing**: Strategy for all 4 layers defined
- ✅ **Roadmap**: Phase 4 implementation plan with weekly checkpoints

---

## Files Summary

```
workstream3-technical/
├── README.md                              (this file)
├── TECHNICAL-ARCHITECTURE-SPEC.md         (1. Executive summary + full spec)
├── 01-server-architecture-audit.md        (2. Current state audit)
├── 02-validation-schemas.md               (3. Zod schema design)
├── 03-error-handling-strategy.md          (4. Result type & error codes)
├── 04-data-access-layer.md                (5. Query consolidation)
└── [Future] 05-abstraction-design.md      (CRUD helpers - Phase 4)
```

---

## How to Use These Documents

### For Engineering Lead
1. Read **TECHNICAL-ARCHITECTURE-SPEC.md** (20 min)
2. Review **01-server-architecture-audit.md** for confidence (20 min)
3. Use success metrics section for sign-off

### For Phase 4 Implementation Team
1. Read **TECHNICAL-ARCHITECTURE-SPEC.md** for overview
2. Deep dive into specific layers (02-04) as you implement
3. Use implementation checklists at end of spec document
4. Follow weekly checkpoints in roadmap section

### For Domain Workstream
1. Review **TECHNICAL-ARCHITECTURE-SPEC.md** section 4 (n8n Integration)
2. Validate error codes in **03-error-handling-strategy.md**
3. Confirm audit logging in **TECHNICAL-ARCHITECTURE-SPEC.md** section 3.2.4

### For UX/Frontend Team
1. Review **03-error-handling-strategy.md** section 3 (client-side handling)
2. Check error messages dictionary and custom alerts
3. Validate Zod schemas in **02-validation-schemas.md** can be reused

---

## Next Steps

1. **Code Review** (2-3 days): Share with team, gather feedback
2. **Sign-offs** (1 week): Engineering lead, Domain lead, UX lead
3. **Phase 4 Planning** (1 week): Detailed task breakdown and sprint planning
4. **Implementation** (4-5 weeks): Follow roadmap in TECHNICAL-ARCHITECTURE-SPEC.md

---

## Contact & Questions

- **Architecture Questions**: Review TECHNICAL-ARCHITECTURE-SPEC.md section 2
- **Audit Questions**: Review 01-server-architecture-audit.md
- **Implementation Questions**: Review specific layer document (02-04)
- **n8n Integration**: See TECHNICAL-ARCHITECTURE-SPEC.md section 4

---

**Status**: ✅ Complete and Ready for Review  
**Date**: 2026-05-17  
**Workstream**: Phase 3, Technical Foundation (Workstream 3)  
**Document Version**: 1.0
