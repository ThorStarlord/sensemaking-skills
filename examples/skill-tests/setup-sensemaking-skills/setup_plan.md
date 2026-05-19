# Setup Plan (Sensemaking Skills)

## 1. Status Audit
The repository is currently unconfigured for automated sensemaking orchestration. 
- **Root Instructions**: `AGENTS.md`, `CLAUDE.md`, and `.cursorrules` are absent. 
- **Documentation Structure**: The `docs/` directory exists but is missing the `docs/agents/` subdirectory for specialized agent configurations.
- **Registries**: `skill-registry.yaml` and `workflow-registry.yaml` are present but are not yet formally linked to the agent's root instructions.

## 2. Missing Components
The following components must be created to fully bootstrap the sensemaking pipeline:
1. **Sensemaking Instruction Block**: Needs to be added to a new `AGENTS.md` file.
2. **Specialized Agent Docs**:
    - `docs/agents/sensemaking.md`: Detailed pipeline logic.
    - `docs/agents/workflow-modes.md`: Definitions for `fast_path` vs `full_fog_path`.
    - `docs/agents/artifact-contracts.md`: Schemas for `problem_frame.md`, `unknowns_map.md`, etc.
    - `docs/agents/downstream-skills.md`: Mapping to domain-specific skills.

## 3. Proposed Edits

### [NEW] AGENTS.md
```markdown
# Agent Instructions
This repository uses the Sensemaking Skills pipeline for all complex tasks.

## Sensemaking Pipeline
1. **Problem Framing**: Use `problem-framer` for any vague request.
2. **Sensemaking**: Use `repo-sensemaker` to diagnose repository shape.
3. **Orchestration**: Use `workflow-planner` to select a workflow.
4. **Maintenance**: Use `skill-maintainer` to improve skills based on logs.

Refer to `docs/agents/sensemaking.md` for detailed protocols.
```

### [NEW] docs/agents/sensemaking.md
*Content based on [Sensemaking Config Template](references/sensemaking-config-template.md).*

### [NEW] docs/agents/workflow-modes.md
*Content based on [Workflow Modes Template](references/workflow-modes-template.md).*

## 4. Interactive Trace
If this were an interactive run, the skill would ask the following questions:
1. "No root instruction file found. Should I create AGENTS.md, CLAUDE.md, or .cursorrules? (Recommended: AGENTS.md)"
2. "Should the default sensemaking path be 'fast_path' (skip unknowns-mapper) or 'full_fog_path' (standard)? (Recommended: full_fog_path)"
3. "Are there any domain-specific skills (e.g., frontend, security) that should be mapped in downstream-skills.md?"
4. "Shall I proceed with creating the 4 documentation artifacts in docs/agents/? [Y/n]"
