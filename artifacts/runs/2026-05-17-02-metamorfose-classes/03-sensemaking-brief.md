# Repository Sensemaking Brief: Metamorfose Edutech Classes System

## 1. Repository goal

Metamorfose Edutech is a multi-surface education platform. The classes system manages student groupings (turmas). It provides a minimal CRUD interface to create and list classes with properties: name, grade level, and school year.

## 2. Current shape

**Classes Subsystem Structure:**
- `app/admin/classes/` — Classes management
  - `page.tsx` — List and create interface (150 lines)
  - `[classId]/page.tsx` — Class detail page (not yet examined)
- **Storage:** `.data/saas/alpha-db.json` (file-based, not Supabase)
- **Data Model:** Class { id, name, gradeLevel, schoolYear, createdAt }
- **Functions:** `createClass()`, `listClasses()` from `lib/alpha-store`
- **Access Control:** Admin role required

## 3. Strong signals

**Positive aspects:**
1. **Simple & Clear**: The interface is minimal and easy to understand
2. **Proper Access Control**: Requires admin role, session validation before operations
3. **Validation Present**: Form requires name and gradeLevel; schoolYear is optional
4. **Server-Side Safety**: Uses server actions, no client-side data mutations
5. **Clean UI Pattern**: Simple form + table list is standard and recognizable

## 4. Missing pieces

1. **Storage Strategy Documentation**: Why alpha-db.json instead of Supabase? No explanation or comment
2. **Relationship Documentation**: How do students relate to classes? Unknown
3. **Data Model Completeness**: No documentation of all fields, constraints, or defaults
4. **Lifecycle Definition**: No documented state machine (can classes be archived? deleted?)
5. **Business Logic**: What does "creating a class" actually do beyond storing the record?
6. **Detail Page**: `[classId]/page.tsx` not examined; unknown what it shows
7. **Migration Plan**: If alpha-db is temporary, what's the migration path to Supabase?
8. **Validation Rules**: Why no range validation on gradeLevel (1-12) or schoolYear (2000-2099)?
9. **Uniqueness Constraints**: Are class names unique? Within a year? Required but not enforced in code
10. **Error Handling**: No error messages if create fails; unclear user feedback

## 5. Improvement opportunities

1. **Migrate to Supabase**: Move classes from alpha-db.json to Supabase for consistency with other systems
2. **Define Class Lifecycle**: Add states (draft, active, archived) with explicit transitions
3. **Add Validation**: Range checks for gradeLevel (1-12), schoolYear (reasonable bounds)
4. **Document Relationships**: Explicit schema defining how classes relate to students, teachers, enrollment
5. **Implement Error Handling**: Provide feedback if class creation fails
6. **Add Student Enrollment View**: Show which students are in a class on detail page
7. **Support Bulk Operations**: Archive multiple classes, export class list
8. **Add Search/Filter**: Filter classes by grade, year, or name prefix

## 6. Weakest boundary

**The weakest boundary is the undefined relationship between Classes and Students and the undocumented purpose of the alpha-db.json storage choice.**

Specifically:
- **What it is**: The set of implicit decisions about data ownership (alpha-db vs. Supabase), data relationships (class → students), and lifecycle (what states are valid)
- **Why it's weak**:
  1. **No relationship documentation**: The system doesn't show how students are related to classes. Is there an enrollment table? A junction table? Unknown.
  2. **Storage strategy is unexplained**: Alpha-db.json is used nowhere else (appears to be just for classes); no justification or comment explaining why it's not in Supabase
  3. **Lifecycle is implicit**: No documentation of valid state transitions. Can classes be deleted? Can they be archived? Unknown.
  4. **No migration path**: If alpha-db is scaffolding, there's no documented path to migrate to Supabase (data loss risk)
  5. **Data consistency risk**: If alpha-db exists independently, it can become out-of-sync with actual enrollments

**File locations (evidence):**
- `app/admin/classes/page.tsx:7` — Uses `lib/alpha-store` instead of Supabase
- `app/admin/classes/page.tsx:33` — `createClass()` function called with no visible relationship logic
- `.data/saas/alpha-db.json` — Exists but purpose and schema are undocumented

**Risk if left weak:**
- Adding features (enroll students, schedule classes) requires reverse-engineering the class-to-student relationship
- Migrating from alpha-db to Supabase will be high-risk if not planned upfront
- Data integrity issues (orphaned records, inconsistent state) if relationships are implicit
- Team members won't know if classes can be safely deleted (depends on enrollment logic)

## 7. Evidence

### Evidence Type 1: Storage Strategy Unexplained

**File:** `lib/alpha-store` (used in classes but not imported from Supabase)

**Observation:** Classes use `lib/alpha-store` instead of Supabase like finance system does. No comment explaining why.

**Supports claim**: Storage choice is undocumented; purpose unclear

### Evidence Type 2: Relationship is Implicit

**File:** `app/admin/classes/page.tsx:33`

```typescript
await createClass({
  projectId: project.id,
  name,
  gradeLevel,
  schoolYear: schoolYear !== null && Number.isFinite(schoolYear) ? schoolYear : null,
});
```

**Observation**: Function only accepts project, name, grade, year. No mention of student enrollment, teacher assignment, or any relationship.

**Supports claim**: How students are related to classes is not visible in code

### Evidence Type 3: No Validation on Constraints

**File:** `app/admin/classes/page.tsx:27-30`

```typescript
const gradeLevel = Number.parseInt(String(formData.get("gradeLevel") ?? ""), 10);
if (!name || !Number.isFinite(gradeLevel)) return;
```

**Observation**: Only checks if gradeLevel is a valid number, not if it's in a reasonable range (1-12).

**Supports claim**: Constraints and business rules are not enforced; validation is minimal

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: app/admin/classes/page.tsx
    lines: L7
    quote: "import { createClass, listClasses } from '@/lib/alpha-store';"
    supports_claim: "Classes use alpha-db.json storage instead of Supabase; no explanation why"
    
  - file: app/admin/classes/page.tsx
    lines: L33-38
    quote: "await createClass({ projectId: project.id, name, gradeLevel, schoolYear: ... })"
    supports_claim: "Create function has no parameters for student relationships, teacher assignment, or enrollment"
    
  - file: app/admin/classes/page.tsx
    lines: L27-30
    quote: "const gradeLevel = Number.parseInt(...); if (!name || !Number.isFinite(gradeLevel)) return;"
    supports_claim: "Validation only checks if gradeLevel is a number, not if it's in valid range"
    
  - file: .data/saas/alpha-db.json
    lines: unknown
    quote: "[File exists but schema and purpose are not documented in code]"
    supports_claim: "Storage schema is implicit; no documentation of fields, relationships, or lifecycle"
```

## 9. Why this boundary matters

The classes system is the foundation for student grouping. If the relationship between classes and students is implicit:
- Enrollment workflows cannot be built correctly (depends on how relationship is stored)
- Student lists cannot be shown reliably (depends on understanding how to query class ↔ student mapping)
- Deleting classes becomes dangerous (do you orphan student records? Delete enrollments?)
- Scaling to multiple teachers per class requires redesign if relationships are implicit

The choice of alpha-db vs. Supabase matters because:
- If alpha-db is intentional (separate data store for academic data), then all academic systems must use it
- If alpha-db is temporary scaffolding, migrating to Supabase later will require data migration
- Mixing storage systems (some data in alpha-db, some in Supabase) creates consistency risk

## 10. Candidate next steps

1. **Inspect Alpha-db Schema**: Read `.data/saas/alpha-db.json` to document actual data structure and relationships
2. **Trace Student References**: Search codebase for any existing student-to-class relationships
3. **Interview Educators**: Understand the intended purpose of classes (grouping? scheduling? grading?)
4. **Define Class Lifecycle**: Document valid state transitions (draft → active → archived → deleted)
5. **Decide Storage Strategy**: Commit to alpha-db or plan migration to Supabase

## 11. Recommended next step

**Inspect the Alpha Store and Define Class Lifecycle** — Create a data model documentation defining:
- What fields a Class has (and why)
- How Classes relate to Students
- Valid state transitions for Classes
- Storage strategy justification (why alpha-db, when to migrate to Supabase)

This unblocks: enrollment features, student views, class management workflows.

## 12. Recommended workflow

**`fast-local-diagnostic`** OR **`docs-architecture`** (align stored data model with intended purpose)

Instead of discovery-based (which suits complex, implicit systems), the classes system needs:
1. Clear documentation of current state (what alpha-db contains)
2. Alignment between stored schema and intended model
3. Decision on storage strategy going forward

## 13. Machine-readable handoff

```yaml
recommended_workflow_id: docs-architecture
recommended_execution_mode: plan_only
weakest_boundary: |
  Classes data model & storage strategy
  (Undocumented relationships to Students, unexplained alpha-db choice, implicit lifecycle)
required_inputs:
  - repository_sensemaking_brief
object_under_pressure: |
  Class entity: storage (alpha-db vs. Supabase), relationships (to students/teachers/enrollment),
  lifecycle (valid state transitions), constraints (naming, grade ranges)
storage_concern: |
  Classes stored in .data/saas/alpha-db.json (file-based, not Supabase).
  Unclear if intentional or temporary scaffolding. No migration plan documented.
```

## 14. Ready-to-copy prompt

> **For docs-architecture:** I need to understand and document the classes data model in Metamorfose Edutech. Currently:
> - Classes are stored in `.data/saas/alpha-db.json` (not Supabase like other systems)
> - The relationship between Classes and Students is undocumented
> - Valid state transitions (can classes be archived? deleted?) are unknown
>
> Please:
> 1. Inspect alpha-db.json schema and document all fields in a Class record
> 2. Trace how Students relate to Classes (find enrollment logic if it exists)
> 3. Interview a product manager/educator about class lifecycle and purpose
> 4. Create a domain alignment report documenting the Class entity, its relationships, and storage strategy
>
> This will unblock: enrollment features, student views, class management, migration to Supabase (if needed).
