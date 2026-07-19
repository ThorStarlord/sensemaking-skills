"""
Deterministic test executor for architectural-review acceptance testing.

This executor produces valid, predictable output artifacts for testing the
full workflow orchestration path (run() method) without depending on real
external model calls or nondeterministic skill behavior.

The executor must be injected directly into the runtime via:
    runner.skill_executor = DeterministicFixtureSkillExecutor(...)

It is NOT registered in the production CLI or executor factory.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add scripts to path for skill_executor import
REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from skill_executor import SkillExecutor, SkillExecutionResult, SkillExecutionStatus


class DeterministicFixtureSkillExecutor(SkillExecutor):
    """
    Deterministic test executor that produces valid fixture artifacts.

    Used exclusively for acceptance testing to prove the full orchestration
    path (run() method, preflight, step iteration, validation routing,
    final-state computation) without external dependencies.

    Supports:
    - Step 1: repo-sensemaker → repository_sensemaking_brief
    - Step 2: architectural-review → architectural_review_recommendation

    Both with deterministic, validated fixture content.
    """

    supports_real_execution = True

    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.invocations = []  # Track all skill invocations for testing

    def invoke_skill(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        """
        Produce deterministic fixture output for test skills.

        Args:
            skill_id: The skill being invoked (e.g., 'repo-sensemaker')
            invocation_command: How it would be invoked
            input_artifacts: Input artifact IDs
            expected_output_artifact: Output artifact ID
            context: Runtime context including expected_output_path

        Returns:
            SkillExecutionResult with status=EXECUTED and output written
        """

        # Track invocation for test verification
        self.invocations.append({
            "skill_id": skill_id,
            "output_artifact": expected_output_artifact,
        })

        # Resolve output path via the runtime-provided location
        output_path = context.get("expected_output_path")
        if not output_path:
            # Fallback only if called outside runtime
            output_path = os.path.join(
                self.repo_root,
                "artifacts",
                f"{expected_output_artifact}.md"
            )

        print(f"[EXECUTOR] {skill_id}: Writing artifact to {output_path}")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Route to skill-specific fixture generator
        if skill_id == "repo-sensemaker":
            return self._invoke_repo_sensemaker(
                output_path, expected_output_artifact, input_artifacts
            )
        elif skill_id == "architectural-review":
            return self._invoke_architectural_review(
                output_path, expected_output_artifact, input_artifacts, context
            )
        else:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.UNSUPPORTED,
                command=invocation_command,
                error=f"DeterministicFixtureSkillExecutor does not support skill '{skill_id}'",
            )

    def _invoke_repo_sensemaker(
        self,
        output_path: str,
        expected_artifact: str,
        input_artifacts: list[str],
    ) -> SkillExecutionResult:
        """Step 1: Produce a valid repository_sensemaking_brief fixture."""

        brief_content = """# Repository Sensemaking Brief

## Summary
This repository implements an agent-native framework for repository diagnosis
and workflow orchestration. It turns repository uncertainty into clear problem
frames, research paths, and actionable next-step prompts.

## Weakest Boundary
The current weakest boundary is in workflow routing: the gap between initial
problem-domain identification and domain-specific implementation workflows.

## Evidence
- File: CONTEXT.md (missing — recommend creating)
- File: skills/workflow-planner/references/workflow-registry.yaml (complete)
- File: scripts/validate-plan.py (alignment enforcement works)

## Recommended Next Step
Implement the architectural-review skill to handle routing decisions when
proposed architectural changes need validation against principal-engineer judgment.

## Machine-readable metadata

```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: architecture_fog
evidence:
  - "Workflow registry defined with 30+ workflows"
  - "Validation framework in place"
  - "routing decision fields present in artifact-contracts.yaml"
  - "Gap: architectural-review skill not yet implemented"
recommended_workflow_id: architectural-review-planning-workflow
created_at: "2026-07-19T12:00:00Z"
created_by: "deterministic-test-executor"
immutable: false
```
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(brief_content)

        return SkillExecutionResult(
            skill_id="repo-sensemaker",
            status=SkillExecutionStatus.EXECUTED,
            command="python skills/repo-sensemaker/repo-sensemaker.py",
            output_artifact=expected_artifact,
            message=f"repo-sensemaker executed (deterministic fixture): "
                    f"brief written to {output_path}",
        )

    def _invoke_architectural_review(
        self,
        output_path: str,
        expected_artifact: str,
        input_artifacts: list[str],
        context: dict,
    ) -> SkillExecutionResult:
        """Step 2: Produce a valid architectural_review_recommendation fixture."""

        # For deterministic testing: Assume inputs are present if we get here.
        # The runtime's preflight validation has already checked input availability,
        # so the executor should proceed to generate the artifact.
        # (The runtime may not always populate step_context in the context dict,
        #  especially for test executors.)

        recommendation_content = """# Architectural Review Recommendation

## Summary
The proposed direction aligns with the repository's architecture-first approach
to workflow orchestration. This recommendation approves the proposed architectural
changes.

## Decision
**pursue** — Implement the proposed architectural direction with suggested refinements.

## Confidence
**high** — The proposed changes are well-aligned with existing patterns and address
real gaps in the current architecture.

## Rationale
The repository's weakest boundary is in architectural routing decisions. The proposed
direction directly addresses this by introducing validation against principal-engineer
judgment (capability abstraction, bottleneck detection, architectural risk mapping).

## Success Measures
- Unified validator passes all acceptance tests within 48 hours
- Architectural-review skill integrated into automated workflow routing
- Team consensus on routing decisions within 3 iterations

## Refinements
1. Ensure all outcome enums (pursue, investigate_first, defer, reject) are validated
2. Include scope_narrowing field when confidence is medium
3. Document architectural patterns that inform the decision

## Next Steps
Implement the architectural-review skill following the workflow-planner handoff
contract. Deploy to production with appropriate validation gates.

## Machine-readable recommendation

```yaml
artifact_id: architectural_review_recommendation
decision: pursue
confidence: high
primary_justification: "Addresses documented weakest boundary in workflow routing"
patterns_aligned:
  - "Capability abstraction over feature enumeration"
  - "Bottleneck detection via weakest-boundary analysis"
  - "Architectural risk mapping at routing decision points"
risk_level: low
implementation_complexity: medium
success_measures:
  metric: "Validator pass rate on architectural review recommendations"
  baseline_status: "0% pass rate (new skill)"
  target: "100% pass rate on deterministic test fixture"
  measurement_method: "Run validate-architectural-review-recommendation.py on all generated artifacts"
created_at: "2026-07-19T12:00:00Z"
created_by: "deterministic-test-executor"
```
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(recommendation_content)

        return SkillExecutionResult(
            skill_id="architectural-review",
            status=SkillExecutionStatus.EXECUTED,
            command="python skills/architectural-review/architectural-review.py",
            output_artifact=expected_artifact,
            message=f"architectural-review executed (deterministic fixture): "
                    f"recommendation written to {output_path}",
        )
