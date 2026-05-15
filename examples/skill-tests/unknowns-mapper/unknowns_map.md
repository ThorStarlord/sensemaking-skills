# Unknowns Map

## 1. Knowns
- The goal is to bridge "messy ideas" into "useful AI workflows" using a predictable pipeline.
- The Object Under Pressure (OUP) is the `workflow-registry.yaml`.
- Current "hallucinated workflows" pass structural validation but fail behavioral expectations.

## 2. Unknowns
- The specific "messy ideas" (scenarios) the user wants to prioritize first.
- The exact current schema and constraints of `workflow-registry.yaml`.
- Which existing skills can be composed into these new workflows.

## 3. Assumptions
- The repository already contains enough specialized skills to fulfill the "useful AI workflows" goal once the bridge is built.
- A standardized "Sensemaking Pipeline" (Framer -> Mapper -> Sensemaker) is the correct architecture for this bridge.

## 4. Risks
- **Overfitting**: Creating a pipeline that only works for the current "messy ideas" but fails on future ones.
- **Ambiguity**: The bridge remains too high-level, failing to produce a truly executable `workflow-registry.yaml` entry.

## 5. Research Paths
- **Path A**: Audit `workflow-registry.yaml` to identify common workflow patterns and required fields for new entries.
- **Path B**: Research the `workflow-orchestrator`'s internal validation logic to understand what constitutes a "behaviorally sound" workflow.

## 6. Stopping Rule
- **Meta-Sensemaking**: Stop when we have identified a specific Search Seed for `workflow-registry.yaml` and the handoff contract for `repo-sensemaker` (as defined in `artifact-contracts.yaml`) is confirmed as satisfied by this map.

---
**Handoff Readiness**:
- **Search Seed**: `workflow-registry.yaml` (Audit for pattern matching)
- **Next Skill**: `repo-sensemaker`
