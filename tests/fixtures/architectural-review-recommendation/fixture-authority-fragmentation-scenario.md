# Architectural Review Recommendation — Authority Fragmentation Scenario

## Summary

The proposed Author Workspace introduces a second authority model for artifact coordination. This violates the identity model's boundary and creates fragmentation risk. Recommendation: reject and redesign.

## Analysis

### Problem Identified

Brief classifies this as architecture_fog: current system has one clear authority (identity model) but artifact coordination is implicit. Proposed workspace attempts to make coordination explicit by creating a new `AuthorWorkspace` entity with read access to artifact metadata.

**Critical issue**: The workspace would become a second source of truth about "which artifacts belong to which author" — duplicating information from the identity model and potentially becoming inconsistent with it.

### Fragmentation Risk

If the workspace ever acquires write authority (to support sorting, filtering, or favorites), it becomes a competitor authority to the identity model, leading to:
- Conflicting permission decisions
- Data consistency nightmares (identity says user has access; workspace says they don't)
- Debugging complexity (two systems claiming authority over user-artifact relationships)

## Recommendation

### Decision

reject

### Reasoning

While the proposal has merit as a UI coordination layer, the architectural boundary is wrong. Instead of a new workspace entity, the solution should be a read-only query layer that delegates all authority checks to the identity model AND does not duplicate identity information.

### Kill Conditions (Why This Decision Cannot Be Overridden)

1. **Workspace acquires write authority**: If workspace can modify artifact metadata or access permissions, it becomes a second authority model
2. **Consistency diverges**: If identity and workspace disagree about user-artifact relationships, the system is broken
3. **Scope creep to coordination**: If workspace starts making orchestration decisions (e.g., "this artifact should be published in this order"), authority is fragmented

### Redesign Direction

Instead of a workspace entity, create:
- A read-only `PublicationHistory` view that queries identity + artifacts
- All permission checks delegated to identity system
- No duplicate metadata — only views and queries
- Clear contract: workspace is a UI layer, not a data authority

## Machine-readable decision

```yaml
artifact_id: architectural_review_recommendation
decision: reject
confidence: high
risks_identified:
  - "Workspace becomes second authority model if scope expands"
  - "Author-artifact relationships duplicated between identity and workspace"
  - "Maintenance burden increases as two systems must stay consistent"
  - "Future features (sorting, filtering, favorites) could push workspace toward write authority"
reversal_conditions:
  - "Redesign removes workspace entity entirely; use read-only query layer instead"
  - "All permission decisions explicitly routed to identity system"
  - "No data duplication: only views and queries, not stored relationships"
kill_conditions:
  - "Workspace acquires write authority over artifact metadata or access permissions"
  - "Workspace and identity model disagree about user-artifact relationships"
  - "Workspace makes orchestration or coordination decisions independent of identity model"
created_at: "2026-07-18T00:00:00Z"
created_by: "validator-test"
```
