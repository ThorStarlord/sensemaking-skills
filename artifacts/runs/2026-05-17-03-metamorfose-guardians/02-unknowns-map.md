# Unknowns Map: Metamorfose Guardians System

## 1. Knowns

**Data Model:**
- Guardian has: `id`, `name`, `email` (optional), `phone` (optional), `userId` (nullable)
- Student has: `id`, `firstName`, `lastName`, `gradeLevel`
- Guardian-Student link has: `guardianId`, `studentId`, `relationship` (optional), `isPrimary` (boolean)
- All operations are scoped to a `projectId`

**API Layer:**
- Functions exist in `@/lib/alpha-store`: `createGuardian`, `linkGuardianToUser`, `linkGuardianToStudent`, `listGuardianStudents`, `listGuardians`, `listStudents`, `unlinkGuardianFromStudent`
- Data is persisted in `.data/saas/alpha-db.json` (alpha storage)
- All operations trigger `revalidatePath("/admin/guardians")` for cache invalidation

**Access Control:**
- Guardians page is admin-only (role-checked via `requirePageRoles`)
- All form actions check session and role again (`getDevSession()`)

**UI Patterns:**
- Guardian creation form: name (required), email (optional), phone (optional)
- Guardian-to-user linking: email-based, defaults to guardian's email if present
- Guardian-to-student linking: student dropdown, relationship text field, primary checkbox

## 2. Unknowns

**Data Model Constraints:**
1. **Cardinality**: Can a guardian have multiple user accounts? Code shows single `userId`, but `linkGuardianToUser` doesn't check for duplicates or prevent overwrites.
2. **Primary Guardian Conflict**: What happens if you mark a second guardian as "primary" for the same student? No visible conflict resolution.
3. **Orphaning Behavior**: When unlinking a guardian from a student, is there validation to prevent removing the only guardian? Or the primary guardian without replacement?
4. **User Account Deletion**: If a user is deleted, what happens to their linked guardian record? Is the `userId` nulled out?

**Access & Permissions:**
5. **Guardian Authentication**: How does a guardian log in? Is there a login flow that checks `userId`, or do guardians use some other mechanism?
6. **Guardian Capabilities**: Once logged in, what can a guardian see/do? Only their own linked students, or all students in the project?
7. **Admin vs. Guardian Roles**: Are there separate role checks for admins vs. guardians, or is this purely an admin management interface?

**Integration Points:**
8. **User Account Creation**: Does `linkGuardianToUser` require a pre-existing user account, or does it auto-create one?
9. **Student Access Rights**: How are student-access permissions determined? Is it user→project→student hierarchy?
10. **Audit Trail**: Are guardian-student links logged/audited for compliance or data recovery?

## 3. Assumptions

1. **Single User Per Guardian**: We assume one guardian can have at most one user account (implied by single `userId` field), but this isn't enforced in code.
2. **User Account Exists**: We assume `linkGuardianToUser` expects a pre-existing user account, but there's no validation visible.
3. **Primary Guardian is Functional**: We assume the `isPrimary` flag has semantic meaning (e.g., contact person for school communication), but the UI doesn't enforce mutual exclusivity.
4. **Guardian Without User is Valid**: We assume a guardian can exist with `userId === null` (no login account), but the system might break if they try to access student data.
5. **Project Membership Required**: We assume all guardian-student links are scoped to the active project, and access is determined by project membership.
6. **Email Uniqueness**: We assume email addresses used for login are globally unique across the system (or at least per-project unique).

## 4. Risks

1. **Data Integrity Risk**: Without cardinality constraints, multiple guardians could claim "primary" status for the same student, leading to conflict during student communication or grade access.
2. **Orphaning Risk**: Removing a guardian-student link might leave a student with zero guardians, potentially violating legal/operational requirements.
3. **Access Control Risk**: If guardian authentication relies on `userId` linking, and that link can be overwritten, a guardian might be locked out unexpectedly.
4. **Cascade Deletion Risk**: If a user account is deleted, orphaned guardian records might linger, creating stale data or confusion during reconciliation.
5. **Email Reuse Risk**: If email addresses can be reused across different guardians, or if a guardian's email is updated, `linkGuardianToUser` might silently fail or link to the wrong user.

## 5. Research Paths

**Path 1: Schema & Constraints Audit** (2 hours)
- Inspect `@/lib/alpha-store` source code to see database schema and constraint definitions
- Check if cardinality is enforced at API layer (e.g., before insert/update)
- Verify: Are there unique indexes on (guardianId, studentId)? On (guardianId, userId)?
- **Stopping condition**: Can list all constraints enforced by the data layer.

**Path 2: User Account Integration** (1 hour)
- Find the user login flow (probably in `/auth` or `/login` path)
- Trace: How does a guardian authenticate? Via `userId`? Via email?
- Verify: What happens if a guardian's `userId` is null—can they still log in?
- **Stopping condition**: Understand complete flow from guardian creation → user linking → login.

**Path 3: Guardian Access Control** (1.5 hours)
- Search codebase for guardian role definition and access checks
- Find: Where is guardian role enforced (not just in this admin page)?
- Verify: Are there separate pages/APIs for guardian-facing features?
- **Stopping condition**: Identify guardian access scope (their own students only, or all project students?).

**Path 4: Primary Guardian Semantics** (1 hour)
- Search for `isPrimary` usage in templates, emails, reports, or business logic
- Verify: Is `isPrimary` just UI metadata, or does it affect permissions/access?
- Check: Are there conflict-resolution rules if multiple primaries exist?
- **Stopping condition**: Understand what "primary" means operationally.

**Path 5: Integration Test Walkthrough** (1 hour)
- Create a guardian, link to user, link to student (happy path)
- Attempt: Unlink only guardian from a student (does it block?)
- Attempt: Link same guardian to same student twice (duplicate check?)
- **Stopping condition**: Identify which edge cases are handled vs. allow-all.

## 6. Stopping Rule

**Primary Stopping Rule:**
Stop research when:
- ✅ Source code for `@/lib/alpha-store` is inspected and cardinality constraints (or lack thereof) are documented
- ✅ User authentication flow is traced and guardian login mechanism is clear
- ✅ At least one edge case (orphaning, duplicate primary, reused email) is tested and behavior confirmed
- ✅ Unknown #5 (guardian authentication) and Unknown #2 (primary conflict) are resolved

**Acceptable Stopping Criteria:**
- If schema has explicit constraints (e.g., UNIQUE(guardianId, studentId)), then some of Path 1 is complete and we can skip duplicate-link testing.
- If auth flow shows guardian access is restricted to their own students, then Unknown #6 is resolved.
- If "primary" field is purely informational (no business logic), then Unknown #2 and Path 4 can be deprioritized.

## 7. Machine-readable routing

```yaml
clarity_assessment: "medium"
unknowns_count: 10
assumptions_count: 6
research_needed: true
```

**Reasoning:**
- `unknowns_count: 10` exceeds the threshold of 5, triggering research insertion.
- `clarity_assessment: "medium"` indicates the core problem frame is clear (guardian-student linking), but edge cases and constraints are fuzzy.
- `research_needed: true` because multiple unknowns (cardinality, primary conflict, user account deletion) could cause production bugs if left unresolved.
- This system is more complex than a simple CRUD page; it requires explicit data model verification before safe implementation of guardian features.

**Routing Decision:**
- **Insert research step**: Yes, recommend `repo-sensemaker` to audit the codebase for constraints and produce a detailed brief.
- **Confidence in routing**: Medium-High. The heuristic correctly identifies a system with hidden coupling (user→guardian→student) that needs deeper inspection.
