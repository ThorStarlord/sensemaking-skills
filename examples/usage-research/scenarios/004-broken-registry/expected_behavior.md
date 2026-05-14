# Expected Behavior: Scenario 004

The agent should recognize that the user's intent is clear (running a specific workflow), but the execution is blocked by a system defect.

## Meta-Sensemaking Outcome
- **Object Under Pressure**: `workflow-registry.yaml`
- **Problem Under the Problem**: The registry contains a malformed entry for `product-discovery-sprint` that is causing an execution error.
- **Success Condition**: The agent identifies the missing or malformed fields in the registry and proposes a registry fix.

## Boundary Guard Success
- The agent **must not** suggest the user needs more "product discovery" or "framing".
- The agent **must** pivot to system diagnostics (registry audit).
