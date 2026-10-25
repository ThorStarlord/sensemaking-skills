"""Legacy workflow-planner compatibility surface, fail-closed.

The Python ``WorkflowPlannerSkill`` used to read the repository sensemaking
brief, choose a workflow from a static table, and write a simplified plan to
``artifacts/workflow_orchestration_plan.md``. That output did not satisfy the
``workflow_orchestration_plan`` contract, used a flat path rather than the
canonical ``artifacts/plan_{workflow_id}.md``, and reported success, so it could
replace a tracked plan. The class stays importable for compatibility, but
``run()`` touches no files and returns a structured failure that directs callers
to the agent-native ``workflow-planner`` Skill, which owns workflow selection.
"""

from typing import Any, Dict

from .base import BaseSkill

_UNSUPPORTED_MESSAGE = (
    "WorkflowPlannerSkill is an unsupported legacy producer and wrote nothing. "
    "Its static fog and workflow table is not the canonical vocabulary, and its "
    "output does not satisfy the workflow_orchestration_plan contract. Produce the "
    "plan with the agent-native workflow-planner Skill instead."
)


class WorkflowPlannerSkill(BaseSkill):
    """Fail-closed compatibility stub for the retired legacy plan producer.

    Importing, constructing and calling ``run()`` keep working; ``run()`` never
    reads, generates, writes or overwrites a workflow orchestration plan.
    """

    # Retained for import compatibility only. It is not a routing source: workflow
    # selection belongs to the active agent (skills/workflow-planner/SKILL.md).
    WORKFLOW_RECOMMENDATIONS = {
        "Python": {
            "fog_type": "python_codebase",
            "recommended_workflows": ["test_python_codebase", "analyze_python_architecture"],
            "key_files": ["setup.py", "requirements.txt", "pyproject.toml"],
        },
        "JavaScript": {
            "fog_type": "javascript_codebase",
            "recommended_workflows": ["test_js_codebase", "analyze_js_architecture"],
            "key_files": ["package.json", "tsconfig.json", "webpack.config.js"],
        },
        "Go": {
            "fog_type": "go_codebase",
            "recommended_workflows": ["test_go_codebase", "analyze_go_architecture"],
            "key_files": ["go.mod", "go.sum"],
        },
        "Sensemaking": {
            "fog_type": "sensemaking_project",
            "recommended_workflows": ["skill_execution", "workflow_orchestration"],
            "key_files": ["CONTEXT.md", "workflows", "skills"],
        },
    }

    def run(self, brief_artifact_id: str = "repository_sensemaking_brief", **kwargs) -> Dict[str, Any]:
        """Refuse to produce a plan without touching the target repository.

        Args:
            brief_artifact_id: Accepted for signature compatibility and ignored
            **kwargs: Accepted for signature compatibility and ignored

        Returns:
            The legacy result shape with:
            - artifact_id: None
            - success: False
            - code: "LEGACY_PLANNER_UNSUPPORTED"
            - message: Names the agent-native workflow-planner Skill
            - fog_type, recommended_workflows, chosen_workflow_id and authority: empty
        """
        self.log(_UNSUPPORTED_MESSAGE, level="ERROR")
        return {
            "artifact_id": None,
            "success": False,
            "code": "LEGACY_PLANNER_UNSUPPORTED",
            "message": _UNSUPPORTED_MESSAGE,
            "fog_type": None,
            "recommended_workflows": [],
            "chosen_workflow_id": None,
            "authority": None,
        }
