# Guardians System Sensemaking Run

**Date:** 2026-05-17  
**System:** Metamorfose Guardians (`metamorfose-edutech/metamorfose-platform/app/admin/guardians/page.tsx`)  
**Pipeline:** Full sensemaking (problem-framer → unknowns-mapper → repo-sensemaker)  
**Task:** Option A validation of routing heuristic (unknowns_count >= 5 triggers research)

## Artifacts

### 01-problem-frame.md
Defines the guardian-student linking problem and identifies the core unknowns:
- Raw fog: Guardian system manages 3 types of links (guardian→user, guardian→student, student→user)
- Object under pressure: Data model constraints and cardinality rules
- Failure mode: Orphaned guardians, multi-primary conflicts, access control issues
- Stopping rule: Identifies need for API contract inspection and edge case testing

### 02-unknowns-map.md
Maps 10 unknowns and 6 assumptions, defines research paths:
- **unknowns_count: 10** (exceeds threshold of 5)
- **clarity_assessment: medium** (good data model, fuzzy business logic)
- **research_needed: true** (triggers repo-sensemaker)

Key unknowns:
1. Can a guardian have multiple user accounts? (Answer: No, single userId field)
2. What happens if a second guardian is marked primary? (Answer: Auto-conflict resolution in code)
3. What if you remove the only guardian for a student? (Answer: System allows orphaning, no checks)
4. User account deletion cascade? (Answer: Stale reference left behind)
5. How do guardians log in? (Answer: Via userId, but entry point not in this file)

### 03-sensemaking-brief.md
Deep repository audit identifying the "weakest boundary":
- **Strong signals:** Well-typed data model, conflict resolution, duplicate prevention, role-based access
- **Missing pieces:** Business logic documentation, email uniqueness validation, audit trail, cascade delete rules
- **Weakest boundary:** Email↔user account coupling is implicit and fragile
- **Recommendation:** Create GUARDIAN_DATA_MODEL.md documenting access patterns before building guardian features

### 04-run-analysis.md
Validation analysis of the routing heuristic:
- Confirms unknowns_count >= 5 threshold is appropriate
- Compares Guardians (10 unknowns) to Finance (9) and Classes (8) — all triggered correctly
- Pattern analysis: Guardians has implicit coupling (like Finance), not clear modeling (like Classes)
- No false positives detected across 3 systems
- Ready for Task 2 (pedagogico) to test false-negative boundary

## Key Findings

### Routing Signal Validated ✅
- **unknowns_count: 10** → exceeds threshold of 5
- **clarity_assessment: medium** → system is sound but has implicit contracts
- **research_needed: true** → repo-sensemaker executed
- **Result:** Heuristic works correctly for medium-complexity systems

### System Complexity Signature
Guardians exhibits "good architecture, fuzzy contracts" pattern:
- Sound data model (Supabase constraints, type-safe operations)
- Implicit business logic (primary guardian semantics undefined)
- Missing access control contract (where do guardians log in?)
- Result: 10 unknowns despite 365-line codebase

### Unexpected Complexity
Guardians (365 lines) has MORE unknowns than Finance (500 lines) because:
- Data relationships are more ambiguous than sequential workflows
- N:N cardinality with implied business logic is fuzzier than async sequencing

## Comparison to Other Systems

| System | Lines | Unknowns | Clarity | Research |
|--------|-------|----------|---------|----------|
| Finance | ~500 | 9 | medium | YES |
| Classes | ~400 | 8 | high | YES |
| Guardians | 365 | 10 | medium | YES |
| Pedagogico* | 12 | ~1-3 | high | NO (expected) |

*Expected from validation plan; not yet executed

## Validation Coverage

**Option A Progress:**
- ✅ Task 1: Guardians (full pipeline) — Complete
- ⏳ Task 2: Pedagogico (full pipeline) — Pending
- ⏳ Task 3: Comunicacao (edge case) — Pending

**Criteria:**
- ✅ Unknowns-count >= 5 triggers research correctly (3 of 3 systems)
- ⏳ Simple systems (< 5 unknowns) correctly skip research (awaiting pedagogico run)

## Recommended Next Steps

### For Implementation Teams
1. **Create GUARDIAN_DATA_MODEL.md** documenting:
   - Where guardians log in and how access is determined
   - What "primary" guardian means operationally
   - Email↔user account linking rules
   - Cascade delete behavior
2. **Audit guardian-facing pages** to verify they enforce student_guardians access control

### For Validation Plan
1. **Execute Task 2** (pedagogico, 12 lines, expected < 5 unknowns)
   - Verify simple systems correctly have research_needed=false
   - Test boundary condition of threshold (unknowns = 4 or 5?)
2. **Execute Task 3** (comunicacao, 7 lines, ultra-simple)
   - Test lower boundary (what happens with 1-2 unknowns?)
3. **Consolidate findings** in meta-analyses report

## Methodology

This run follows the **full sensemaking pipeline**:
1. **Problem-framer:** Converts raw fog (3 types of links) into structured problem frame
2. **Unknowns-mapper:** Maps 10 unknowns, calculates routing signal
3. **Repo-sensemaker:** Audits codebase, identifies weakest boundary (email↔user coupling)
4. **Run analysis:** Validates heuristic and compares to prior systems

**Time to completion:** ~2.5 hours

**Quality assurance:**
- Deep source code inspection (student-store.ts fully analyzed)
- Evidence citations with line numbers
- Comparison to prior runs (Finance, Classes)
- Pattern recognition (identifies "implicit coupling" as complexity signature)
