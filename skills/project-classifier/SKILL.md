---
name: project-classifier
description: analyze a raw project description to classify project type and recommend the optimal workflow. use when you have a project goal but don't know which workflow to use.
---

# project-classifier

Automatically classifies project types from raw descriptions and recommends the optimal orchestration workflow. This skill eliminates the need for users to know which workflow to invoke.

## Workflow

1. **Fog Capture**: Listen to the raw project description (product idea, business goal, technical problem, etc.)
2. **Type Classification**: Identify the project type from predefined categories
3. **Complexity Assessment**: Evaluate scope (MVP vs. scaling, technical depth, stakeholder count)
4. **Execution Mode Selection**: Recommend appropriate mode (plan_only, guided_execution, autonomous_execution)
5. **Workflow Matching**: Select the most suitable workflow from registry
6. **Input Specification**: Identify required inputs for the selected workflow
7. **Synthesis**: Produce a Project Classification Brief with clear routing

## Project Type Classification

Map raw descriptions to these categories. The companion [router.py](router.py) is the
canonical implementation — these names match its keyword-based classification exactly:

- **saas**: Multi-user, recurring revenue, cloud-hosted (e.g., CRM, observability tool, marketplace)
- **content**: Publishing, distribution, audience building (e.g., learning platform, blog network)
- **tool**: CLI, library, package, build system, testing framework
- **consumer**: Mobile-first, retention-focused, gamification (e.g., fitness app, social)
- **enterprise**: Workflow optimization, data aggregation, admin tools
- **marketplace**: Freelance, suppliers, transactions, specialized services
- **research**: Proof-of-concept, validation focus, limited scope (default when no keywords match)

## Workflow Selection Logic

The companion [router.py](router.py) is the canonical source for this mapping.
AI usage should produce output compatible with it. Current mapping:

| Project Type | Primary Workflow | Fallback |
|:---|:---|:---|
| saas | product-discovery-sprint | product-autonomous-sprint |
| content | product-discovery-sprint | full-local-sensemaking |
| tool | full-local-sensemaking | docs-architecture |
| consumer | product-discovery-sprint | product-autonomous-sprint |
| enterprise | autonomous-sprint-preflight | docs-architecture |
| marketplace | product-discovery-sprint | product-autonomous-sprint |
| research | fast-local-diagnostic | full-local-sensemaking |

## Output Format

Every response must follow the [Project Classification Brief](references/project-classification-template.md) structure.
The `recommended_workflow_id` and `recommended_execution_mode` fields must be compatible with
what [router.py](router.py) would produce for the same classification.

## Boundary Rules

1. **No Implementation**: Output is diagnostic only. Do not execute recommended workflows.
2. **Registry Grounding**: All `recommended_workflow_id` values MUST be verified against `skills/workflow-planner/references/workflow-registry.yaml`.
3. **Type Confidence**: If classification confidence is below 70%, recommend `plan_only` mode and note the ambiguity.
4. **Input Clarity**: If critical inputs for the selected workflow are missing from the description, explicitly call them out as "Required Before Execution".

## Companion Reference Implementation

A deterministic keyword-based router lives alongside this skill at [router.py](router.py).
It implements the same classification and workflow selection logic in Python, used by
`scripts/portfolio-orchestrator.py`. When the AI skill and the programmatic router produce
different results, the router is the source of truth for automated routing decisions.

## References

- [Project Classification Brief Template](references/project-classification-template.md)
- [Workflow Registry](../workflow-planner/references/workflow-registry.yaml)
- [Companion Router](router.py) — canonical classification implementation
