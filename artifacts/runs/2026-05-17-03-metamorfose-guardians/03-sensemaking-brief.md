# Repository Sensemaking Brief: Guardians System

## 1. Repository goal
The Metamorfose Guardians system provides an admin interface for managing guardian-student relationships within an educational platform. It enables educators to:
- Create guardian records (name, contact info)
- Link guardians to user login accounts
- Associate guardians with students and specify relationships (parent, grandparent, etc.)
- Mark guardians as "primary" for a student (likely for school communication)

The system is built on Supabase for persistence and Next.js for the admin UI.

## 2. Current shape

**Admin UI:**
- `app/admin/guardians/page.tsx` (365 lines) — server component with embedded form actions

**Data Layer:**
- `lib/student-store.ts` — Guardian, Student, StudentGuardian types and operations
- `lib/alpha-store.ts` — Re-exports from student-store
- Database tables: `guardians`, `students`, `student_guardians` (in Supabase)

**Auth & Access:**
- `lib/page-auth.ts` — Role-based access control (admin-only checks)
- `lib/dev-auth.ts` — Session management
- `lib/dev-ids.ts` — Stable ID generation from email

**Helper Layer:**
- `lib/alpha-store-helpers.ts` — Email normalization, user existence checks

## 3. Strong signals

✅ **Data model is well-typed**
- Clear TypeScript types for Guardian, Student, StudentGuardian
- All database operations go through typed functions

✅ **Primary guardian conflict resolution is automated**
- Lines 376-382 (student-store.ts): When marking a guardian as primary, the system automatically sets all other guardians for that student to non-primary
- This prevents the "multiple primary" problem that was a top unknown

✅ **Duplicate link prevention is enforced**
- Line 393: Check for error code 23505 (unique constraint violation) in `linkGuardianToStudent`
- Returns `{ ok: false, error: "already_linked" }` rather than silently failing

✅ **User account existence is guaranteed**
- Lines 263-268: `createGuardian` calls `ensureUserExists` if an email is provided
- Lines 299-303: `linkGuardianToUser` calls `ensureUserExists` before updating
- Users are auto-created with stable IDs derived from email (e.g., `user:maria@example.com`)

✅ **Guardian without user account is valid**
- Line 255: `userId` is optional in createGuardian parameters
- Line 261: If no email provided, `userId` remains null
- This allows creating a guardian record without a login account (for offline/paper-based guardians)

✅ **Role-based access control is enforced**
- Page requires admin role (page-auth.ts requirePageRoles)
- Form actions double-check role (getDevSession and roles.includes("admin"))

✅ **Relationship metadata is optional**
- Line 371: `relationship` field is nullable, allowing flexible description (parent, grandparent, etc.)

## 4. Missing pieces

**No documentation of business logic**
- Primary guardian semantics not explained (is it just "contact first" or does it affect access/permissions?)
- Guardian vs. student access patterns not documented
- No README explaining the data model or constraints

**No validation of email uniqueness**
- Email normalization exists (normalizeEmail) but no check that the same email isn't used for multiple guardians within a project
- Potential issue: If two guardians accidentally get the same email, they'd link to the same user account

**No audit trail or logging**
- Guardian-student links are created/deleted but no audit log of who changed what and when
- No soft-delete flag for guardian records (hard delete only)

**No guardian-facing access control**
- The admin page shows admin operations, but there's no code for "what a logged-in guardian can see"
- Assumption: Guardian access is handled elsewhere (separate pages, not in this file)

**No cascading deletion rules**
- If a guardian is deleted, their student links are orphaned (not automatically deleted)
- If a user account is deleted, their guardian record's `userId` is not nulled out (stale reference)

**No conflict resolution UI for primary guardian**
- UI allows marking a guardian primary without showing the other guardians' primary status
- Users might not realize they're demoting another guardian

## 5. Improvement opportunities

1. **Add business logic documentation** — Document what "primary" means operationally and when guardians can access student data
2. **Email uniqueness validation** — Add unique constraint on (projectId, email) in the database or enforce in code
3. **Soft-delete flag for guardians** — Allow marking guardians as inactive rather than hard-deleting, preserving history
4. **Audit logging** — Log guardian-student link changes with timestamp and actor
5. **Guardian access control design** — Document where guardian-facing pages/APIs are defined and what they can access
6. **Primary guardian UX improvement** — Show current primary guardian before allowing a change, with confirmation
7. **Cascade delete handling** — Automatically clean up student_guardians links when a guardian is deleted

## 6. Weakest boundary

**The coupling between user accounts and guardian identity is implicit and fragile:**

- Guardian records link to user accounts via `userId` (a stable ID derived from email)
- If an email changes, the link breaks (userId is tied to the old email)
- If a user is deleted externally, the guardian record's userId becomes stale
- There's no validation that the email in the guardian record matches the user account's email

**This creates two operational risks:**
1. **Email update confusion**: Changing a guardian's email doesn't update their user account link
2. **Orphaned account links**: If a user is deleted, the guardian record still references the old userId

**Secondary weakness:**

The admin UI and the underlying data model have an **unspecified shared understanding** of when a guardian can access student data. The code enforces that:
- Guardians need a user account (`userId`) to log in
- But doesn't specify where guardian-facing pages check guardian access rights

This is not a code bug—it's a **missing contract** between admin data creation and guardian feature implementation. If a new developer adds guardian-specific pages, they might not realize they need to check `student_guardians` links to enforce visibility.

## 7. Evidence

| Claim | File | Lines | Evidence |
|-------|------|-------|----------|
| Primary conflict is auto-resolved | `lib/student-store.ts` | 376-382 | `update().set({is_primary: false})` resets all other primaries before inserting |
| Duplicate links prevented | `lib/student-store.ts` | 393 | Error code 23505 check returns `already_linked` |
| User auto-create on guardian creation | `lib/student-store.ts` | 263-268 | `ensureUserExists` called in createGuardian |
| Guardian without user is valid | `lib/student-store.ts` | 259-261 | `userId` derived from email, can be null |
| Admin-only access | `app/admin/guardians/page.tsx` | 20-23 | `requirePageRoles({...roles: ["admin"]})` |
| Form actions double-check role | `app/admin/guardians/page.tsx` | 42-43 | `if (!session \|\| !session.roles.includes("admin")) return;` |

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: lib/student-store.ts
    lines: L376-L382
    quote: |
      if (params.isPrimary) {
        const { error: resetError } = await supabase
          .from("student_guardians")
          .update({ is_primary: false })
          .eq("project_id", params.projectId)
          .eq("student_id", params.studentId);
        assertSupabaseOk(resetError, "linkGuardianToStudent.resetPrimary");
      }
    supports_claim: "Primary guardian conflict is automatically resolved—when marking a guardian primary, all other guardians for that student are demoted to non-primary"

  - file: lib/student-store.ts
    lines: L393-L396
    quote: |
      if (error && error.code === "23505") {
        return { ok: false, error: "already_linked" };
      }
    supports_claim: "Duplicate guardian-student links are prevented via database unique constraint, not silently allowed"

  - file: lib/student-store.ts
    lines: L263-L268
    quote: |
      if (userId) {
        await ensureUserExists({
          userId,
          email,
          fullName: params.name,
        });
      }
    supports_claim: "If guardian is created with an email, a user account is auto-created; if no email, userId remains null"

  - file: app/admin/guardians/page.tsx
    lines: L39-L48
    quote: |
      async function createGuardianAction(formData: FormData) {
        "use server";
        const session = await getDevSession();
        if (!session || !session.roles.includes("admin")) return;
    supports_claim: "Form actions enforce admin-only access by checking session role"
```

## 9. Why this boundary matters

If the email↔user account coupling remains implicit:

1. **Support burden**: When a guardian's email changes, support staff won't know why their login no longer works (the guardian record email was updated but the user account link wasn't)
2. **Data integrity risk**: Over time, orphaned userId references accumulate, confusing access control queries
3. **Audit difficulty**: When investigating guardian access, unclear whether stale userId means the guardian should/shouldn't have access
4. **Future feature risk**: If roles/permissions are added (e.g., "guardians can view grades"), the implementation might assume every guardian has a valid user account—leading to silent failures for guardians with `userId === null`

The secondary weakness (guardian access not specified) matters because:
- New feature developers might add guardian-facing pages without realizing they must filter by `student_guardians` links
- This could accidentally expose one student's data to another guardian (security risk)

## 10. Candidate next steps

1. **Define guardian access contract** — Document where guardians log in, what they can see, and how student access is determined (via student_guardians links)
2. **Add email uniqueness validation** — Enforce unique (projectId, email) constraint in the database
3. **Fix email↔user account drift** — Add a migration to reconcile guardian email with user account email, and add validation in `linkGuardianToUser` to prevent drift
4. **Add guardian access control** — Audit all guardian-facing pages/APIs and verify they check student_guardians links
5. **Document primary guardian semantics** — Add a comment explaining what "primary" means and when it's used (school communication, grade access, etc.)

## 11. Recommended next step

**Highest leverage, smallest scope:**

Document the **guardian access contract** in a new file (`docs/GUARDIAN_DATA_MODEL.md`):
- What a guardian login experience looks like (entry point, auth method)
- What a guardian can see (only their own linked students, or more?)
- How student access rights are determined (via student_guardians table, checked by guardian-facing pages)
- Email↔user account linking rules and what happens if they drift
- What "primary" guardian means operationally

This unblocks feature development and provides a spec for code review of future guardian-facing pages.

## 12. Recommended workflow

**Workflow ID:** `full-local-sensemaking`

**Rationale:**
- System has medium complexity (3 linked data models, N:N relationships)
- Unknown count (10) exceeds threshold (5), triggering deep research
- Data model is sound but business logic contracts are missing
- This fits "understand the system deeply before implementing new features"

## 13. Machine-readable handoff

```yaml
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: guided_execution
weakest_boundary: "Email↔user account coupling is implicit; primary guardian semantics undefined; guardian access control contract missing"
clarity_assessment: "medium"
unknowns_count: 10
assumptions_count: 6
research_needed: true

required_inputs:
  - repository_sensemaking_brief
  - problem_frame
  - unknowns_map

next_step_type: documentation + feature specification
next_step_description: "Create GUARDIAN_DATA_MODEL.md documenting access patterns, email linking, primary semantics, and cascade delete behavior. Then audit guardian-facing pages to verify they enforce student_guardians access control."
```

## 14. Ready-to-copy prompt

**For:** Product/Implementation teams ready to build guardian-facing features

---

**Context:**

The Guardians admin system has a well-designed data layer but lacks explicit documentation of business logic. The weakest boundary is the **implicit coupling between guardian email and user account identity**, combined with **undefined access control semantics for guardian-facing features**.

**What we know:**
- Guardian-student relationships are N:N via `student_guardians` table
- Primary guardian status is auto-enforced (one primary per student)
- Duplicate guardian-student links are prevented via unique constraint
- Guardian records can exist without a user account (userId=null)
- User accounts are auto-created from guardian email

**What's unclear:**
- Where do guardians log in, and how is their access determined?
- Can a guardian with userId=null ever log in?
- Does "primary guardian" affect what they can see/do?
- What happens if guardian email is updated without updating the user account?
- If a user account is deleted, is the guardian record orphaned?

**Recommended action:**

Before building new guardian-facing features (grades, communications, etc.), create a **GUARDIAN_DATA_MODEL.md** document that specifies:
1. Guardian login entry point and authentication method
2. What a logged-in guardian can access (students they're linked to via student_guardians)
3. Role of the "primary" flag in the business logic (contact person? lead communicator? permissions?)
4. Email↔user account linking rules and drift handling
5. Cascade delete behavior (what happens if guardian is deleted?)

Then, audit all guardian-facing pages to verify they:
- Check student_guardians links before returning student data
- Validate that userId points to a valid user account (not stale)
- Document assumptions about guardian role and permissions

---
