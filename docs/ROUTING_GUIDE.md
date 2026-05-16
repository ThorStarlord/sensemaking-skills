# Workflow Routing Guide

## Automatic Project Classification & Workflow Selection

The `router.py` script eliminates the need to manually select workflows. It automatically classifies your project type and recommends the optimal workflow.

## Quick Start

```bash
# Classify a project and get routing recommendation
python scripts/router.py <path-to-project-description.md>

# Override the recommended mode
python scripts/router.py <path-to-project-description.md> --mode autonomous_execution

# Get output as JSON
python scripts/router.py <path-to-project-description.md> --json
```

## Supported Project Types

| Type | Characteristics | Primary Workflow |
|:---|:---|:---|
| **SaaS/Platform** | Multi-user, recurring revenue, cloud-hosted | product-discovery-sprint |
| **Content/Creator** | Publishing, audience building, education | product-discovery-sprint |
| **Developer Tool** | CLI, library, framework, monitoring | full-local-sensemaking |
| **Consumer App** | Mobile-first, retention-focused, gamification | product-discovery-sprint |
| **Enterprise/Internal** | Workflow optimization, data tools, admin | autonomous-sprint-preflight |
| **Marketplace** | Transaction-based, specialized services | product-discovery-sprint |
| **Research/Experimental** | Proof-of-concept, limited scope | fast-local-diagnostic |

## Execution Modes

- **plan_only**: Just plan (no commitment). Good for validation and initial exploration.
- **guided_execution**: Recommended mode for new project types. User reviews at each step.
- **autonomous_execution**: Automated gates, faster execution. Good for familiar project types.
- **yolo_execution**: No gates, highest speed. Recommended only for experimental work.

## How Classification Works

The router analyzes your project description to detect:

1. **Primary Keywords** (weighted 2x): Core domain terms (e.g., "learning", "crm", "mobile app")
2. **Secondary Keywords** (weighted 1x): Supporting context (e.g., "audience", "users", "integration")
3. **Confidence Score**: Higher score = more certain classification

**Confidence Thresholds:**
- **Below 70%**: Defaults to `plan_only` mode for validation
- **70% or higher**: Uses full workflow in `guided_execution` or `autonomous_execution` mode

## Example: SaaS Project

```bash
$ python scripts/router.py my-saas-idea.md

======================================================================
PROJECT ROUTING ANALYSIS
======================================================================

Input: my-saas-idea.md

CLASSIFICATION
  Type: saas
  Confidence: 100%

WORKFLOW SELECTION
  Primary: product-discovery-sprint
  Fallback: product-autonomous-sprint
  Recommended Mode: guided_execution
  Supported Modes: plan_only, guided_execution, autonomous_execution

NEXT STEP
  $ python scripts/orchestration-runner.py product-discovery-sprint --mode guided_execution
```

## Flow: From Raw Idea to Execution

```
Your Project Description
        ↓
   router.py
        ↓
  Classification
   (Type + Confidence)
        ↓
  Workflow Selection
   (Primary + Fallback)
        ↓
  Mode Recommendation
   (plan_only → guided → autonomous)
        ↓
orchestration-runner.py
        ↓
  Skill Execution Pipeline
        ↓
  Validated Artifacts
```

## Customization

### Override the Recommended Mode

```bash
# Use autonomous execution even for new project types
python scripts/router.py my-idea.md --mode autonomous_execution
```

### Low Confidence Classification

If your project description is ambiguous (confidence < 70%), the router automatically defaults to `plan_only` mode:

```
CLASSIFICATION
  Type: research
  Confidence: 45%

WORKFLOW SELECTION
  Recommended Mode: plan_only
  Rationale: Low confidence (45%) classification. Starting in plan_only mode for validation.
```

**Next Step**: After planning, clarify your project goals and re-run the router with a more specific description.

## Integration with CI/CD

The router can be integrated into pipelines:

```bash
# Classify all projects in a directory and log results
for project in projects/*.md; do
    python scripts/router.py "$project" --json >> routing_results.jsonl
done

# Parse routing results for automation
cat routing_results.jsonl | jq '.workflow_selection.command' | xargs -I {} bash -c '{}'
```

## Troubleshooting

### "Classification Confidence Too Low"

**Problem**: Your project keeps getting classified as "research" (confidence < 70%).

**Solution**: 
1. Add more specific terminology to your description (domain keywords)
2. Mention key characteristics: "SaaS", "mobile app", "internal tool", etc.
3. Explicitly describe the target market and business model

### "Wrong Workflow Selected"

**Problem**: The router selected a workflow that doesn't fit your project.

**Solution**:
1. Override the mode: `python scripts/router.py your-idea.md --mode plan_only`
2. Use `plan_only` to review the plan first
3. Then select a different workflow manually once you confirm your project type
4. File an issue if you think the classification logic needs improvement

## Future Work

- [ ] Support for fine-tuning confidence thresholds per organization
- [ ] Integration with user feedback loop (crowdsourced classification improvements)
- [ ] Support for multi-project portfolio routing
- [ ] ML-based classification after collecting classification examples
