# Problem Frame: Metamorfose Guardians System

## 1. Raw Fog
The Guardians admin page (`app/admin/guardians/page.tsx`, 365 lines) is a Next.js server component that manages the creation and linking of guardian records to students. The system appears to handle multiple overlapping relationships:
- Creating guardian profiles (name, email, phone)
- Linking guardians to user login accounts
- Linking guardians to students with relationship labels
- Managing guardian-student links (primary flag, relationship type)

The unclear aspects are around the **data model contracts** and **relationship semantics**: How do these three types of links interact? What are the guardrails preventing inconsistent states?

## 2. Problem Under the Problem
The admin interface exposes a complex data model with implicit constraints that aren't surfaced in the UI. There are at least three different "linking" operations:
1. **Guardian → User** (login account binding)
2. **Guardian → Student** (care relationship)
3. **User ↔ Student** (implied by project membership?)

The problem isn't just UI design—it's **unclear data flow and unspecified cardinality constraints**. For example:
- Can a guardian have multiple login emails? (implied: yes, but code shows single user binding)
- Can a student have multiple guardians? (implied: yes)
- Is a guardian without a user account valid? (yes, but then how do they access the system?)
- What happens if a guardian's user account is deleted?

## 3. Object Under Pressure
**File**: `app/admin/guardians/page.tsx`

**Specific tensions**:
- Lines 26-37: Parallel loading of guardians + students, then mapping guardian→student relationships. The data-loading pattern mixes concerns.
- Lines 83-100: `linkGuardianToUser` operation—no visible validation that the user exists or that only one user per guardian is enforced.
- Lines 60-81: `linkStudentAction` without checking for duplicate relationships or conflict resolution for "isPrimary" flags.
- Lines 102-119: `unlinkStudentAction` operation—no visible handling of orphaning a primary guardian for a student.

## 4. Failure Mode
**If this system's data constraints are not clearly defined**:
- Orphaned guardians with no user account and no linked students
- Multiple "primary" guardians for a single student with no conflict resolution
- Users unable to understand guardian access patterns (can a guardian log in directly?)
- Data integrity violations on account deletion (what happens to guardian records?)
- Confusion during onboarding about which fields are optional vs. required for functional guardian relationships

## 5. Success Condition
A clear **data model contract** that specifies:
- Relationship cardinality (1:N, N:N, etc.)
- Required vs. optional fields for a guardian to be "functional"
- Explicit constraints enforced by UI or validation
- Clear access patterns (how a guardian logs in, what they can see, what they can do)
- Unambiguous handling of edge cases (primary guardian removal, user account deletion)

## 6. What Must Be True
For the success condition to be reachable:
- [ ] The underlying database schema or alpha-store contract is visible/documented
- [ ] The API layer (`/lib/alpha-store` functions) enforces cardinality constraints
- [ ] The UI form logic aligns with backend constraints (no impossible states allowed)
- [ ] Project membership or login mechanics are clear (guardian→user→project relationship)
- [ ] Administrative vs. guardian access patterns are explicitly defined

## 7. Next Artifact
**Unknowns Map** — to systematically identify:
- What we know about guardian data relationships
- What we're assuming but haven't verified
- What research is needed (API contracts, schema inspection, auth flow)
- Routing decision: Does the system need deep repository audit (repo-sensemaker) or targeted research?
