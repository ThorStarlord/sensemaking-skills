"""Legacy repository-brief producer, retained only as a fail-closed stub.

``RepoSensemakerSkill`` used to generate a file inventory and write it to
``artifacts/repository_sensemaking_brief.md``. That inventory does not satisfy
the ``repository_sensemaking_brief`` contract, and writing it replaced tracked
briefs while the skill reported success. The class stays importable for
compatibility, but ``run()`` touches no files and returns a structured failure
that points callers to the agent-native ``repo-sensemaker`` Skill, the brief's
declared producer in ``skills/workflow-planner/references/artifact-contracts.yaml``.
"""

from typing import Any, Dict
from .base import BaseSkill

_UNSUPPORTED_MESSAGE = (
    "RepoSensemakerSkill is an unsupported legacy producer and wrote nothing. "
    "Its file inventory does not satisfy the repository_sensemaking_brief "
    "contract. Produce the brief with the agent-native repo-sensemaker Skill instead."
)


class RepoSensemakerSkill(BaseSkill):
    """Fail-closed compatibility stub for the retired legacy brief producer.

    Importing, constructing and calling ``run()`` keep working; ``run()`` never
    generates, writes or overwrites ``repository_sensemaking_brief``.
    """

    def run(self, **kwargs) -> Dict[str, Any]:
        """Refuse to produce the brief without touching the target repository.

        Args:
            **kwargs: Accepted for signature compatibility and ignored

        Returns:
            The legacy result shape with:
            - artifact_id: None
            - success: False
            - code: "LEGACY_PRODUCER_UNSUPPORTED"
            - message: Names the agent-native repo-sensemaker Skill
            - authority and capability_recommendation: None
        """
        self.log(_UNSUPPORTED_MESSAGE, level="ERROR")
        return {
            "artifact_id": None,
            "success": False,
            "code": "LEGACY_PRODUCER_UNSUPPORTED",
            "message": _UNSUPPORTED_MESSAGE,
            "repo_summary": None,
            "key_files_found": [],
            "active_uncertainty": None,
            "warranted_responsibility": None,
            "responsibility_basis": None,
            "capability_recommendation": None,
            "capability_availability": "unavailable",
            "authority": None,
            "workflow_id": None,
        }
