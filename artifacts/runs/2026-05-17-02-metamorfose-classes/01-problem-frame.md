# Problem Frame: Metamorfose Edutech Classes Management System

## 1. Raw Fog

Metamorfose Edutech manages student classes (turmas) within the admin system. The classes interface is minimal: a list view showing all classes with a form to create new classes. Each class has a name (e.g., "1A"), grade level (série), and optional school year. The system appears to use an "alpha store" (alpha-db.json file) for persistence rather than the main Supabase database. The implementation is simple but it's unclear: (1) whether the alpha store is temporary scaffolding or intentional design, (2) what the relationship is between classes and students, (3) whether classes need to support advanced features like archiving, scheduling, or enrollment workflows.

## 2. Problem Under the Problem

The classes system is under-specified. The current implementation is a minimal CRUD interface that lacks:
- **Clear data model relationship**: How do classes relate to students, teachers, and academic calendars?
- **Business logic**: What does "create a class" actually do? Does it create empty enrollment records? Does it reserve time slots?
- **Workflow clarity**: Is there a class lifecycle (draft → active → archived)? Can classes be deleted once students are enrolled?
- **Storage strategy clarity**: Why use alpha-db.json instead of Supabase? Is this intentional or temporary?

The real question is: **Is the classes system intentionally minimal (waiting for future expansion) or accidentally incomplete (missing logic that belongs here)?**

## 3. Object Under Pressure

The **Classes CRUD interface** (`app/admin/classes/page.tsx` and `[classId]/page.tsx`), specifically:
- The create class form (what validation rules, what defaults?)
- The classes list view (what filters, sorting, or bulk operations are needed?)
- The data model (`createClass()` function and storage)
- Relationships to students and teachers (implicit, not documented)

## 4. Failure Mode

If this is not addressed:
- New features (enrollment, scheduling) cannot be added without redesigning the class data model
- The relationship between classes and students remains implicit
- The choice between alpha-db and Supabase creates technical debt (eventually one store will become out-of-sync)
- Classes may end up with data that cannot be safely deleted if relationships are not enforced

## 5. Success Condition

The classes system has:
1. **A clear data model** defining what a Class is, what its properties are, and how it relates to Students and Teachers
2. **A documented lifecycle** showing valid state transitions (draft → active → archived)
3. **Explicit business rules** for what operations are allowed (can classes be deleted? when? what happens to student enrollments?)
4. **A clear storage strategy** (use Supabase, not alpha-db, OR justify why alpha-db is correct)
5. **Error cases documented** (what happens if you try to delete a class with enrolled students?)

## 6. What Must Be True

- The domain experts (product manager, educators) understand and can articulate what classes are for
- The team is willing to design the system properly before adding features
- The alpha-db.json file is inspectable and we can understand its current schema
- The relationship between classes and student enrollment is knowable from code or documentation

## 7. Next Artifact

**Unknowns Map**: Clarify what is uncertain about the classes system's data model, lifecycle, and relationships to other entities (students, teachers, enrollment records).
