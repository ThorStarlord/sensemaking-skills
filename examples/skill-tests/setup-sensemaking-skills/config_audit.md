# Problem Frame

## 1. Raw Fog
Audit of sensemaking-skills repository configuration for Wave 1 compliance.

## 2. Problem Under the Problem
The repository lacks standard root-level instruction files (`AGENTS.md`, `CLAUDE.md`) and centralized registries, which may lead to agent bootstrap failures or routing ambiguity in clean environments.

## 3. Object Under Pressure
Repository Root Configuration (`AGENTS.md`, `.cursorrules`).

## 4. Failure Mode
Autonomous agents fail to identify the "Sensemaking Block," leading to non-contract-compliant artifact generation or regression into non-hardened behavior.

## 5. Success Condition
Standard instruction files are present in the root, and registries are either centralized or discoverable via a stable path.

## 6. What Must Be True
- `setup-sensemaking-skills` must be run in "interactive mode" to bootstrap these files.
- The `workflow-registry.yaml` must be moved or symlinked to a more discoverable location if it is the global source of truth.

## 7. Next Artifact
Bootstrap Plan
