# Problem Frame: Metamorfose Edutech Finance UI Complexity

## 1. Raw Fog

Metamorfose Edutech is a SaaS platform with a complex finance subsystem nested within a larger admin system (alongside pedagogic and academic systems). The finance UI has grown organically with two primary subsystems: (1) an input data system for transaction capture and entry, and (2) a report system for reconciliation and analysis. The UI is navigated via a left sidebar with a collapsible finance menu. As features have been added, the UI has accumulated many elements without a clear specification or structural organization, making it difficult to maintain, extend, and reason about the system's architecture.

## 2. Problem Under the Problem

The finance subsystem lacks a spec-driven architecture. The UI was built iteratively in response to feature requests rather than from a coherent domain model. This has created:
- **Implicit structure**: Navigation, data flows, and state management are embedded in code rather than documented
- **Unclear boundaries**: Input data system and report system interfaces are not formally defined
- **Scaling friction**: Each new feature requires understanding the accumulated history rather than following a clear pattern
- **Risk of regression**: Changes to one part of the finance UI have unclear impact on other parts

The real problem is not the number of UI elements, but the absence of a shared understanding of *what the finance system is supposed to do and why it's organized this way*.

## 3. Object Under Pressure

The **Finance UI subsystem** (located in the admin system module), specifically:
- Input data capture and entry flows
- Report generation and display flows  
- Navigation and routing within the finance menu
- Data handoff between input and report subsystems

File location for audit: `metamorfose-platform/src/admin/finance/`

## 4. Failure Mode

If this is not addressed:
- New engineers cannot onboard quickly to the finance system and introduce bugs due to misunderstanding
- Feature additions become slower as the complexity of interactions grows
- Refactoring becomes high-risk because the system's actual requirements are implicit in code rather than explicit
- The finance system becomes a knowledge silo owned by one or two people
- Maintenance costs increase as technical debt accumulates

## 5. Success Condition

The finance UI has:
1. **A clear specification** documenting what the finance subsystem does, its boundaries, and its key workflows
2. **A spec-driven UI structure** where navigation, screens, forms, and data flows are organized according to the spec rather than historical accidents
3. **Documented patterns** that new engineers can follow when adding features
4. **Observable interfaces** between input data system and report system that can be tested and reasoned about independently
5. **Clear recovery path** for existing code: ability to read the specification and understand which file implements which requirement

## 6. What Must Be True

- The codebase is inspectable and can be analyzed for current implementation state
- The domain (finance operations, capture, reconciliation) is stable enough to define a spec (not actively changing in scope)
- The team is willing to adopt a spec-driven approach and use specifications to guide future changes
- Interface Skills are available and can generate high-fidelity UI specifications from analysis

## 7. Next Artifact

**Unknowns Map**: Clarify what is uncertain about the finance system's current implementation, what the actual domain requirements are, and what unknowns block us from writing a specification.
