"""Workflow Planner Skill.

Analyzes repository context and recommends appropriate workflow orchestration
strategy based on repository characteristics and project type.
"""

from pathlib import Path
from typing import Any, Dict, Optional
from .base import BaseSkill


class WorkflowPlannerSkill(BaseSkill):
    """Plans workflow orchestration strategy for target repository.

    This skill reads the repository sensemaking brief, analyzes project
    characteristics, and recommends an appropriate workflow strategy including
    fog type determination and workflow selection.
    """

    # Workflow recommendations based on project characteristics
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
        """Execute workflow planning.

        Reads the repository sensemaking brief and generates a workflow
        orchestration plan.

        Args:
            brief_artifact_id: ID of the repository sensemaking brief artifact
            **kwargs: Optional additional arguments

        Returns:
            Dictionary containing:
            - artifact_id: "workflow_orchestration_plan"
            - success: True if planning completed
            - message: Summary of planning
            - fog_type: Detected project/fog type
            - recommended_workflows: List of recommended workflows
        """
        self.log(f"Starting workflow planning (brief_artifact_id={brief_artifact_id})...")

        try:
            # Read the brief
            brief_content = self.read_artifact(brief_artifact_id)
            if not brief_content:
                return {
                    "artifact_id": None,
                    "success": False,
                    "message": f"Could not read brief artifact: {brief_artifact_id}",
                    "fog_type": None,
                    "recommended_workflows": [],
                }

            # Analyze and determine fog type
            fog_type, confidence = self._determine_fog_type(brief_content)
            recommended_workflows = self._get_recommended_workflows(fog_type)

            # Generate plan
            plan_content = self._generate_workflow_plan(
                fog_type=fog_type,
                confidence=confidence,
                recommended_workflows=recommended_workflows,
            )

            # Write artifact
            artifact_id = "workflow_orchestration_plan"
            self.write_artifact(artifact_id, plan_content)

            return {
                "artifact_id": artifact_id,
                "success": True,
                "message": f"Workflow planning completed: fog_type={fog_type}",
                "fog_type": fog_type,
                "recommended_workflows": recommended_workflows,
            }

        except Exception as e:
            self.log(f"Workflow planning failed: {e}", level="ERROR")
            return {
                "artifact_id": None,
                "success": False,
                "message": f"Planning failed: {e}",
                "fog_type": None,
                "recommended_workflows": [],
            }

    def _determine_fog_type(self, brief_content: str) -> tuple[str, float]:
        """Determine the fog type based on repository characteristics.

        Args:
            brief_content: Content of the repository sensemaking brief

        Returns:
            Tuple of (fog_type, confidence_score) where confidence is 0.0-1.0
        """
        self.log("Determining fog type from brief...")

        # Analyze the brief for project type indicators
        brief_lower = brief_content.lower()

        # Check for Sensemaking project indicators
        if "context.md" in brief_lower and ("workflows" in brief_lower or "skills" in brief_lower):
            self.log("Detected Sensemaking project")
            return ("sensemaking_project", 0.95)

        # Check for Python projects
        if "setup.py" in brief_lower or "requirements.txt" in brief_lower:
            self.log("Detected Python project")
            return ("python_codebase", 0.85)

        # Check for JavaScript/Node.js projects
        if "package.json" in brief_lower:
            self.log("Detected JavaScript project")
            return ("javascript_codebase", 0.85)

        # Check for Go projects
        if "go.mod" in brief_lower:
            self.log("Detected Go project")
            return ("go_codebase", 0.85)

        # Default to generic codebase
        self.log("Could not determine specific fog type, defaulting to generic_codebase")
        return ("generic_codebase", 0.5)

    def _get_recommended_workflows(self, fog_type: str) -> list[str]:
        """Get recommended workflows for a fog type.

        Args:
            fog_type: The detected fog type

        Returns:
            List of recommended workflow IDs
        """
        # Check if fog_type matches a known recommendation
        for project_type, config in self.WORKFLOW_RECOMMENDATIONS.items():
            if config["fog_type"] == fog_type:
                return config["recommended_workflows"]

        # Default workflows for unknown fog types
        return ["general_analysis", "artifact_review"]

    def _generate_workflow_plan(
        self,
        fog_type: str,
        confidence: float,
        recommended_workflows: list[str],
    ) -> str:
        """Generate the workflow orchestration plan.

        Args:
            fog_type: The detected fog type
            confidence: Confidence score (0.0-1.0)
            recommended_workflows: List of recommended workflow IDs

        Returns:
            Formatted plan content as markdown
        """
        plan = [
            "# Workflow Orchestration Plan",
            "",
            "## Fog Type Analysis",
            f"- **Detected Fog Type**: `{fog_type}`",
            f"- **Confidence Score**: {confidence:.1%}",
            "",
        ]

        # Fog type description
        if fog_type == "sensemaking_project":
            plan.extend([
                "## Fog Type Details",
                "This project uses Sensemaking Skills for skill-driven workflow orchestration.",
                "It likely contains structured artifacts, workflows, and skills directories.",
                "",
            ])
        elif fog_type == "python_codebase":
            plan.extend([
                "## Fog Type Details",
                "This is a Python project. Recommended analysis includes:",
                "- Code quality and testing",
                "- Architecture and dependencies",
                "- Performance characteristics",
                "",
            ])
        elif fog_type == "javascript_codebase":
            plan.extend([
                "## Fog Type Details",
                "This is a JavaScript/Node.js project. Recommended analysis includes:",
                "- Package structure and dependencies",
                "- Build and test configuration",
                "- Performance and bundling",
                "",
            ])
        elif fog_type == "go_codebase":
            plan.extend([
                "## Fog Type Details",
                "This is a Go project. Recommended analysis includes:",
                "- Module structure and dependencies",
                "- Build configuration",
                "- Performance characteristics",
                "",
            ])
        else:
            plan.extend([
                "## Fog Type Details",
                "Generic codebase analysis. Specific type detection inconclusive.",
                "",
            ])

        # Recommended workflows
        plan.extend([
            "## Recommended Workflows",
            "",
        ])
        for i, workflow in enumerate(recommended_workflows, 1):
            plan.append(f"{i}. `{workflow}`")
        plan.append("")

        # Execution strategy
        plan.extend([
            "## Recommended Execution Strategy",
            "",
            "1. **Review Plan**: Review this plan and confirm fog type is correct",
            "2. **Execute Primary Workflow**: Run the first recommended workflow",
            "3. **Review Results**: Examine artifacts produced by the workflow",
            "4. **Iterate**: Based on results, execute additional workflows as needed",
            "",
        ])

        plan.extend([
            "## Next Steps",
            "",
            f"- Execute recommended workflow(s) for `{fog_type}` analysis",
            "- Review generated artifacts",
            "- Provide feedback to refine analysis strategy",
            "",
        ])

        return "\n".join(plan)
