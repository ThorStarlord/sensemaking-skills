# Expected Behavior (Scenario: False-Routing Product vs Repo)

To pass this scenario, the `sensemaking-skills` pipeline must resist the "product" keywords and identify that the user is actually struggling with the **Sensemaking Skills Repo's own boundaries and workflow selection**.

## Key Success Criteria

1.  **Object Under Pressure Identification**: 
    *   The `Object Under Pressure` should NOT be "Product Roadmap", "AI App", or "PRD".
    *   It SHOULD be "Workflow Registry", "Skill Boundary", or "Sensemaking Entry Point".
2.  **Routing Accuracy**:
    *   The next recommended step should be a `repo-sensemaking` audit or a guided tour of the `workflow-registry.yaml`, rather than a `product-manager` handoff.
3.  **Stopping Rule**:
    *   Should define a clear boundary for when the user is "unstuck" regarding the repository's own usage.
4.  **No Premature Handoff**:
    *   The framing should explicitly mention that moving to a domain skill (like PM or Engineering) is blocked by a lack of clarity on the current repo's capabilities.
