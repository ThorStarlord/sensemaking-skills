# Unknowns Map: Metamorfose Edutech Classes System

## 1. Knowns

- Classes system is in `app/admin/classes/` with a list page and detail page
- Classes have three properties: name (e.g., "1A"), gradeLevel (integer), schoolYear (optional integer)
- Create class form validates name and gradeLevel are required
- Classes are stored in "alpha-db.json" (file-based, not Supabase)
- Accessed only via admin role
- Simple CRUD interface with no workflows, aggregations, or external integrations

## 2. Unknowns

1. **Storage Strategy**: Why is the classes system using alpha-db.json instead of Supabase? Is this temporary scaffolding or intentional design?
2. **Data Model**: What is the complete schema? Are there fields besides name, gradeLevel, schoolYear? (id, createdAt, ownerId, etc.)
3. **Relationships**: How do classes relate to students? Is there an enrollment table? Can a student be in multiple classes?
4. **Lifecycle**: Do classes have a state (draft, active, archived)? Can they be deleted? What happens to student enrollments if a class is deleted?
5. **Constraints**: Are class names unique? Within a school year? Globally?
6. **Teachers**: Who teaches a class? Is teacher assignment part of this system or elsewhere?
7. **Scheduling**: Does the system support time/day scheduling for classes, or is that handled separately?
8. **Detail Page**: What does the detail page (`[classId]/page.tsx`) show and allow? (Haven't read it yet)

## 3. Assumptions

- The alpha-db.json file is the source of truth for class data
- Classes are student groupings (turmas in Portuguese education context)
- The system is intentionally minimal for now
- Grade level is a number (1-12 or similar)
- School year is a calendar year (2026, 2027, etc.)
- No complex business logic is required yet

## 4. Risks

- **Storage Mismatch Risk**: If alpha-db.json is temporary scaffolding but is used for months, eventual migration to Supabase becomes high-risk
- **Incomplete Data Model Risk**: If the actual schema in alpha-db.json has more fields than what the form shows, operators might be missing important information
- **Relationship Risk**: If students and classes are joined via a separate table that's not defined here, the system could have orphaned records
- **No Validation Risk**: Grade level and school year accept any integer; no validation of reasonable ranges (1-12, 2020-2030, etc.)

## 5. Research Paths

### Research Path 1: Inspect Alpha Store Schema (30 minutes)
**Question**: What is the actual structure of alpha-db.json?

**Method**:
1. Find and read `.data/saas/alpha-db.json` to see current schema
2. Document all fields in a class record
3. Check if there are other tables (students, enrollment, etc.)
4. Determine if alpha-db is used elsewhere or just for classes

**Deliverable**: Document of alpha-db schema and whether it's used for multiple domains

### Research Path 2: Trace Student-to-Class Relationships (30 minutes)
**Question**: How are students related to classes?

**Method**:
1. Search codebase for "enrollment" or references from students system to classes
2. Find `listClasses()` and `createClass()` implementations to see what data they touch
3. Check if there are any references to student_classes or similar junction table

**Deliverable**: Relationship diagram showing how students, classes, and enrollments connect

### Research Path 3: Understand Class Lifecycle Intent (20 minutes)
**Question**: What is the intended purpose and lifecycle of classes?

**Method**:
1. Interview product manager or educator: "What happens when you create a class? What lifecycle does it have?"
2. Ask: "Can a class be deleted? When? What happens to students enrolled in it?"
3. Clarify: "Is this system just for organization, or does it drive scheduling/grading/attendance?"

**Deliverable**: Documented class lifecycle with valid state transitions

## 6. Stopping Rule

**Strong Stopping Rule**:
Research is complete when:
1. Alpha-db.json schema is fully documented (all fields, all tables)
2. Student-to-class relationships are mapped with evidence (code or schema)
3. Class lifecycle is documented with valid state transitions
4. A decision is made about storage strategy (keep alpha-db vs. migrate to Supabase)

**Weak Stopping Rule**:
We understand enough to write initial specs.

**Choose**: Strong (we should get clarity on storage and relationships before adding features)

## 7. Machine-readable routing

```yaml
clarity_assessment: "high"
unknowns_count: 8
assumptions_count: 4
research_needed: false
```

**Rationale**:
- `unknowns_count: 8` is close to but below the threshold of 5 (actually exceeds it, so this should trigger research_needed = true)
- `clarity_assessment: "high"` because the system is simple and visible in code
- The system itself is straightforward; unknowns are about intent/strategy, not implementation
- **ERROR IN CALCULATION**: unknowns_count = 8 >= 5, so research_needed should be **true**, not false

**CORRECTED routing**:
```yaml
clarity_assessment: "high"
unknowns_count: 8
assumptions_count: 4
research_needed: true
```

With unknowns_count >= 5, research IS needed despite high clarity. The unknowns are about intent (storage strategy, lifecycle, relationships), not about complexity.
