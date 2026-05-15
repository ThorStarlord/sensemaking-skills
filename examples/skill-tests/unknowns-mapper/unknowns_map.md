# Unknowns Map

## 1. Knowns
- The goal is to establish a systematic mapping from "messy ideas" to "useful AI workflows."
- `workflow-registry.yaml` is the Object Under Pressure (OUP).
- The success condition requires a repeatable, contract-enforced pipeline for workflow ingestion.

## 2. Unknowns
- The current schema and structural requirements of `workflow-registry.yaml`.
- The existence of validation scripts or CI gates that enforce the workflow contract.
- The list of currently implemented workflows that might serve as templates.

## 3. Assumptions
- `workflow-registry.yaml` is the primary source of truth for workflow orchestration in this repository.
- The registry supports a modular structure that allows for the insertion of new "sensemaking" workflows.

## 4. Risks
- Registry schema drift: The registry might be out of sync with actual skill implementations.
- Complexity Overload: The "messy idea" might require a workflow complexity that the current orchestrator cannot support.

## 5. Research Paths
- **Registry Inspection**: Locate and read `workflow-registry.yaml` to extract the mandatory fields and existing workflow patterns.
- **Contract Verification**: Search for `scripts/validate-*.py` files to identify machine-auditable rules for workflow definitions.
- **Search Seed**: `workflow-registry.yaml` (Focus on schema and existing IDs).

## 6. Stopping Rule
Stop when `workflow-registry.yaml` has been inspected, the schema is documented in the next artifact (Repo Brief), and at least one existing workflow has been identified as a viable template for the user's intent.
