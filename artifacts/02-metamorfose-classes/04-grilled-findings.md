# Grill-with-Docs Execution: Classes System Storage Strategy

## 1. Executive Summary

**Workflow Executed**: grill-with-docs on Classes system to clarify storage strategy  
**Key Finding**: Classes system IS using Supabase (not alpha-db.json), but the documentation was scattered and the code had stale UI labels  
**Outcome**: Added inline documentation and removed misleading UI text; misunderstanding resolved

---

## 2. The Investigation

### Initial Question
The sensemaking brief identified that the classes system's storage strategy was "undocumented" — it appeared to use `.data/saas/alpha-db.json` instead of Supabase, but no explanation was provided.

### Investigation Steps (via grill-with-docs codebase exploration)
1. **Found the store imports**: Classes imported from `lib/alpha-store`
2. **Inspected alpha-store.ts**: Discovered it's a **re-export facade**, not the actual implementation
3. **Traced the real implementations**: 
   - `class-store.ts` — Uses Supabase client, queries `classes` table
   - `student-store.ts` — Uses Supabase client, queries `students` and `class_enrollments` tables
4. **Found the decision documentation**: 
   - `ADR-2026-02-21-persistence-before-new-ui.md` — Explains alpha-db.json was temporary scaffolding
   - `alpha-execution-playbook-2026-02-21.md` — States core SaaS entities should migrate to Supabase
5. **Located the stale UI text**: 
   - Both `classes/page.tsx` (line 109) and `classes/[classId]/page.tsx` (line 249) displayed "Storage alpha: `.data/saas/alpha-db.json`"

### The Truth Discovered
```
What the code ACTUALLY does:
  ┌─────────────────────────────────────┐
  │ classes/page.tsx                    │
  │ import { createClass } from         │
  │   "@/lib/alpha-store"  ←─────┐      │
  └─────────────────────────────┼───────┘
                                │
                    ┌───────────┴──────────┐
                    │ alpha-store.ts       │
                    │ (facade/re-export)   │
                    │ export { createClass │
                    │   from "./class-     │
                    │   store" }           │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │ class-store.ts      │
                    │ (real impl)         │
                    │ async function      │
                    │ createClass(...) {  │
                    │   return            │
                    │   supabase.from(    │
                    │   "classes")...     │
                    │ }                   │
                    └─────────────────────┘
```

**But the UI said**: "Storage alpha: `.data/saas/alpha-db.json`" ← STALE LABEL

---

## 3. Lessons from Execution

### Lesson 1: Documentation Drift is Real
- **The decision**: Migrate classes to Supabase ✅
- **The implementation**: Classes use Supabase ✅  
- **The UI labels**: Still say alpha-db.json ❌

This is **artifact drift** — code was updated, docs were not.

### Lesson 2: Grill-with-Docs Forced Truth-Finding
The sensemaking brief said "storage strategy is undocumented" — technically wrong, but *pragmatically correct*. The documentation existed (in ADR files) but was:
- Not in the code (no inline comments)
- Not in the UI (labels contradict reality)
- Not discoverable by reading the classes code alone

Grill-with-docs forced exploration that uncovered the contradiction.

### Lesson 3: Re-export Facades Can Confuse
The `alpha-store.ts` facade has a misleading name:
- It sounds like it imports the "alpha store" (file-based)
- It actually re-exports Supabase-backed implementations
- This naming choice made the storage strategy appear unclear

**Better naming would be**: `lib/saas-store.ts` or `lib/academic-store.ts` (reflects what it actually exports)

---

## 4. Changes Made

### 1. Added Clarifying Comments
**File**: `classes/page.tsx` and `[classId]/page.tsx`

```typescript
// Note: alpha-store is a facade that exports Supabase-backed stores (class-store, student-store).
// Classes data is persisted to Supabase, not to .data/saas/alpha-db.json (which is legacy local-file storage).
// See ADR-2026-02-21-persistence-before-new-ui.md for migration context.
```

This makes the storage strategy explicit and points to the rationale document.

### 2. Removed Stale UI Label
Deleted the misleading "Storage alpha: `.data/saas/alpha-db.json`" text from both pages.

**Impact**: Users no longer see contradictory information about where their data is stored.

---

## 5. Validation of Sensemaking Brief Diagnosis

The sensemaking brief said: **"Storage strategy is undocumented"**

**Verdict**: ✅ CORRECT (pragmatically)
- The decision IS documented (in ADR files)
- But the code and UI DO NOT reflect it
- So from a developer's perspective reading the classes page, the strategy IS invisible

This validates that the sensemaking system correctly identified that knowledge is **hard to access**, not missing.

---

## 6. What This Teaches the Sensemaking System

### Pattern Recognition
When a system has **contradictory signals**:
- Code says one thing (uses Supabase)
- UI labels say another (alpha-db.json)
- Documentation exists but is elsewhere (ADR files)

**This is a "hidden knowledge" problem**, not a "missing knowledge" problem. The sensemaking brief correctly diagnosed this as "undocumented" — the documentation exists but is not discoverable from the code.

### Implication
The routing heuristic should trigger research when:
- Knowledge exists but is scattered/hidden (not just when it's missing)
- Documentation contradicts implementation (not just when docs don't exist)

**Current system**: Captures this via "unknowns_count" (8 for classes system) based on missing knowledge  
**Future system**: Could refine to distinguish "hidden vs. missing" knowledge

---

## 7. Next Steps

### For Metamorfose Codebase
1. ✅ **Done**: Clarified classes storage implementation with inline comments
2. ✅ **Done**: Removed contradictory UI labels
3. **TODO**: Rename `alpha-store.ts` → `saas-store.ts` to reduce confusion
4. **TODO**: Audit other systems for similar documentation drift

### For Sensemaking System
1. **Validate**: Run grill-with-docs on other systems to see if this pattern repeats
2. **Refine**: Consider adding a "documentation clarity" signal in future unknowns-maps
3. **Catalog**: Track whether "hidden knowledge" is as common as "missing knowledge"

---

## 8. Evidence

### Evidence 1: Implementation Uses Supabase
**File**: `lib/class-store.ts:35-40`
```typescript
const { data, error } = await supabase
  .from("classes")
  .insert({ project_id: projectId, name, grade_level: gradeLevel, school_year: schoolYear })
  .select()
  .maybeSingle();
```
**Supports**: Classes actually use Supabase

### Evidence 2: Facade Pattern
**File**: `lib/alpha-store.ts:26-42`
```typescript
export type { AlphaClass, AlphaClassEnrollment, AlphaTeacherClassAssignment } from "./class-store";
export {
  listClasses,
  getClassById,
  createClass,
  // ... (all re-exported from class-store)
} from "./class-store";
```
**Supports**: alpha-store is a re-export facade, not a separate implementation

### Evidence 3: UI Contradiction
**File**: `app/admin/classes/page.tsx:109` (BEFORE FIX)
```typescript
<p className="text-xs text-gray-500 mt-3">
  Storage alpha: `.data/saas/alpha-db.json`
</p>
```
**Supports**: UI label contradicted actual implementation

### Evidence 4: Decision Documentation
**File**: `docs/human/current/decisions/saas/ADR-2026-02-21-persistence-before-new-ui.md`
**Quote**: "Local file storage was only a temporary early-alpha setup... core SaaS data should be migrated to Supabase/Postgres"
**Supports**: Migration decision was documented, just not visible in code

---

## 9. System-Proving Validation

This execution provides data on:

✅ **Grill-with-docs effectiveness**: Successfully uncovered hidden knowledge and contradictions  
✅ **Sensemaking brief accuracy**: Correctly identified "undocumented" knowledge (even when it was hidden vs. missing)  
✅ **Artifact drift pattern**: Demonstrated that code + docs + UI can contradict without being obviously broken  
✅ **Facade naming confusion**: Showed how naming choices can make architecture unclear  

**Status**: Second successful workflow execution. System working correctly on real problems.

---

## 10. Summary

| Aspect | Finding |
|--------|---------|
| **Storage Strategy** | Classes use Supabase (not alpha-db.json) |
| **Documentation Status** | Decision documented in ADRs, but not visible in code or UI |
| **Root Cause** | Facade naming was confusing; UI labels were stale |
| **Resolution** | Added inline comments explaining storage; removed stale labels |
| **Workflow Success** | ✅ Grill-with-docs successfully clarified the design decision |
| **Sensemaking Validation** | ✅ Brief was correct: knowledge was hidden, not missing |
