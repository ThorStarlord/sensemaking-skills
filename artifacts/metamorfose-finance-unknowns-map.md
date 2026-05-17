# Unknowns Map: Metamorfose Edutech Finance UI

## 1. Knowns

- Finance subsystem is nested within admin system in `metamorfose-platform/src/admin/finance/`
- Two primary subsystems: (1) input data system for transaction capture/entry, (2) report system for reconciliation/analysis
- Navigation is via left sidebar with collapsible finance menu
- Platform is built with Next.js 16 + TypeScript + React
- The system has grown organically without spec-driven architecture
- UI complexity has increased as features were added
- Goal: Understand current structure and create spec-driven design for maintenance/extension

## 2. Unknowns

1. **Domain Workflows**: What are the actual end-to-end workflows the finance system supports? (e.g., capture transaction → validate → categorize → store → reconcile → report)
2. **Data Model**: What is the conceptual data model? (e.g., accounts, transactions, reconciliation entries, reports)
3. **State Management**: What library/pattern is used for state management? (Redux, Zustand, Context API, Jotai, other)
4. **Navigation Structure**: How are screens/pages organized? What are the primary entry points?
5. **Input Validation**: What validation rules currently exist for finance data entry? Are they centralized or scattered?
6. **Report Types**: What report types does the system generate? What are their schema/structure?
7. **Data Flows**: How does data flow between input data system and report system? Are they coupled or decoupled?
8. **Existing Documentation**: Are there design docs, specs, or domain descriptions already in the codebase?
9. **Compliance Constraints**: Are there regulatory or audit constraints that affect the UI design?

## 3. Assumptions

- The codebase is well-enough organized to inspect and map current state
- The team has someone who understands the actual finance domain requirements (workflows, regulations)
- No major architectural refactoring has happened recently that could make code misleading about intent
- The current implementation reflects the actual intended behavior (not legacy/deprecated code)
- Next.js file-based routing and React component hierarchy will be consistent with domain boundaries

## 4. Risks

- **Domain Complexity Risk**: Finance operations might be sufficiently complex that deriving a spec from code takes longer than expected
- **Hidden Requirements Risk**: Important requirements might be implemented implicitly in code without documentation, making them hard to discover
- **Unmapped Coupling Risk**: The input data system and report system might be tightly coupled in ways not obvious from file structure
- **Compliance Risk**: Regulatory requirements that affect UI behavior might not be documented in code comments
- **Onboarding Friction Risk**: Team members who added features iteratively might not be available to explain domain context
- **Specification Scope Risk**: Even with clear specs, implementing spec-driven changes to legacy code could be high-effort

## 5. Research Paths

### Research Path 1: UI Surface Inventory (2-3 hours)
**Question**: What screens, forms, and data entry points does the finance system have?

**Method**: 
1. Inspect `metamorfose-platform/src/admin/finance/` directory structure
2. Map all React component files, identifying screens/pages
3. Document navigation paths through the left sidebar
4. Create UI surface inventory organized by subsystem (input data vs. reports)

**Deliverable**: `docs/saas-frontend/specs/finance-ui-surface-inventory.md`

### Research Path 2: Code Audit - State & Data Management (2-3 hours)
**Question**: How is data stored, transformed, and passed between input data system and report system?

**Method**:
1. Identify state management entry points (Redux store, Zustand store, Context providers)
2. Trace data flow from input form → store → report generation
3. Document validation logic and where it lives
4. Identify any data persistence layer (API calls, local storage)

**Deliverable**: Data flow diagram documenting input → validation → storage → report pipeline

### Research Path 3: Domain Workflow Interview (1-2 hours)
**Question**: What are the actual end-to-end workflows the finance system is supposed to support?

**Method**:
1. Talk to product owner or domain expert about finance operations
2. Document workflow steps, decision points, and error cases
3. Map workflows to current UI screens
4. Identify any workflows the UI is NOT currently supporting

**Deliverable**: Domain workflow documentation or recorded notes

## 6. Stopping Rule

**Strong Stopping Rule**: 
Research is complete when:
1. UI Surface Inventory is mapped and categorized by subsystem
2. State management pattern is identified and documented with examples
3. At least one complete workflow (capture → storage → report) is traced through code and UI screens
4. At least one domain expert has confirmed this understanding matches reality
5. A clear "Object Under Pressure" for spec work is identified (e.g., "Finance Data Entry Flow" or "Report Generation Pipeline")

**Additional Success Condition**: We have enough information to determine which Interface Skill to invoke next (ui-flow for domain workflows, or ui-screen-spec for individual screens).

## 7. Machine-readable routing

```yaml
clarity_assessment: "medium"
unknowns_count: 9
assumptions_count: 5
research_needed: true
```

**Rationale**: 
- `unknowns_count: 9` exceeds the provisional threshold of 5, triggering `research_needed: true`
- `clarity_assessment: medium` reflects that we have the surface context (nested finance subsystem, two main parts) but lack internal detail
- Research paths are concrete and time-boxed, making them actionable
- High-impact unknowns (domain workflows, state management, data flows) are addressed before moving to spec generation
