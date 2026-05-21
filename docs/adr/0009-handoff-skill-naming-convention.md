# ADR 0009: Handoff Skill Naming Convention

**Status**: Accepted

**Context**: The skill-registry.yaml registers both `prompt-handoff` (id: prompt-handoff, artifact: prompt_handoff) and `handoff` (id: handoff, artifact: session_summary) as separate skills. The skills/ directory contains only `prompt-handoff/`. The workflow-registry.yaml references `handoff` in 10 workflows and `prompt-handoff` in 3 workflows. CONTEXT.md lists only `prompt-handoff` as a flagship skill, creating a documentation-registry mismatch.

**Decision**: The two skill IDs represent the same function — packaging context for the next agent — but produce different artifact types. The canonical resolution is: merge into a single `handoff` skill ID that produces a `session_summary`, and deprecate `prompt-handoff`.

**Rationale**: 10/13 workflows already use `handoff`; the directory must match the majority caller. The `prompt_handoff` artifact type (a copy-paste prompt block) is a subset of `session_summary` (a structured artifact with machine-readable fields plus optional copy-paste block).

**Alternatives considered**: (1) Keep both as separate skills — rejected because the behavioral overlap causes confusion and the discrepancy with the skills/ directory is a runtime failure risk. (2) Rename all references to `prompt-handoff` — rejected because it requires touching 10 workflow definitions and the majority usage already favors `handoff`.

**Consequences**: Positive: resolves a contract mismatch affecting 10 workflows. Negative: 3 existing `prompt-handoff` references must be migrated. Skills that consume `prompt_handoff` artifacts must be updated to read `session_summary` instead.
