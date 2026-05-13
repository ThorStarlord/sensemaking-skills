# Example: Problem Frame (Architecture Docs Fog)

## 1. Raw Fog
"Should I put the new agent routing logic in CONTEXT.md or a new ARCHITECTURE.md?"

## 2. Problem Under the Problem
The project lacks a clear hierarchy for "Long-term System Rules" vs. "Short-term Session Context," leading to a "ball of mud" documentation structure that degrades agent performance as file size grows.

## 3. Object Under Pressure
The `CONTEXT.md` file boundary and RAG discoverability rules.

## 4. Failure Mode
Important architectural rules are ignored by agents because they are buried in a bloated, 500-line context file.

## 5. Success Condition
A documented hierarchy that separates static architecture from dynamic session context, with clear file size limits.

## 6. What Must Be True
- Agents must be able to discover the split files through a central index.
- The maintenance overhead of multiple files must be lower than the "bloat" cost.

## 7. Next Artifact
Unknowns Map

## Expected Behavior Checklist
- [x] Captures the "where does this go?" fog.
- [x] Identifies documentation bloat as the root problem.
- [x] Names CONTEXT.md as the object under pressure.
- [x] Recommends Unknowns Map as the next artifact.
