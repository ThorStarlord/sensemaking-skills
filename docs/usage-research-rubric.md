# Usage Research Rubric

This rubric is used to score the semantic quality of artifacts produced during usage research scenarios. It moves beyond structural validity to measure "handoff readiness" and "sensemaking utility."

| Dimension | 0 (Absent) | 1 (Vague) | 2 (Partial) | 3 (Concrete/Handoff-Ready) |
| :--- | :--- | :--- | :--- | :--- |
| **Object Under Pressure** | Not identified. | Identifies a general concept (e.g., "the user's confusion"). | Identifies a specific system part but lacks a concrete proxy. | Identifies a specific file/registry/boundary with an inspectable proxy. |
| **Failure Mode** | Not identified. | Describes a general problem or symptom. | Identifies a specific failure case or scenario. | Identifies the underlying failure mechanism and how to observe/verify it. |
| **What Must Be True** | Not identified. | States obvious or generic conditions. | Lists specific technical prerequisites or assumptions. | Lists verifiable conditions with clear evidence requirements. |
| **Critical Unknowns** | Not identified. | Lists general or abstract questions. | Lists specific info gaps directly tied to the problem frame. | Identifies the "hinge" unknowns that determine routing or implementation. |
| **Research Paths** | Not identified. | General "look at code" or "search docs" paths. | Specific file/folder paths or command-based research. | Actionable search seeds with expected evidence and expected location. |
| **Stopping Rule** | Not identified. | Tautological ("stop when done") or purely time-based. | Measurable but broad (e.g., "read all related docs"). | Verifiable condition tied directly to handoff readiness/workflow selection. |
| **Next-Skill Readiness** | No handoff defined. | Names a next skill but provides no context or search seeds. | Provides some context but requires the next skill to "blind scan." | Provides full context, previous findings, and search seeds for the next skill. |

## Scoring Application
- **0-7**: Critical Failure (Artifact is not useful for downstream execution).
- **8-14**: Partial Success (Requires human intervention or clarification).
- **15-21**: Success (Handoff-ready; minimizes hallucination risk).
