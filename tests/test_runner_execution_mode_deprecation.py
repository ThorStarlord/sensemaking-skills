"""Regression contract for issue #264 implicit execution-mode deprecation."""

from __future__ import annotations

import warnings
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from sensemaking_skills.runner import SkillsOrchestrator


def _orchestrator(tmp_path: Path) -> SkillsOrchestrator:
    orchestrator = SkillsOrchestrator.__new__(SkillsOrchestrator)
    orchestrator.config = SimpleNamespace(project_root=tmp_path)
    orchestrator._runtime_script = tmp_path / "scripts" / "workflow-runtime.py"
    return orchestrator


def _future_warnings(caught) -> list:
    return [item for item in caught if issubclass(item.category, FutureWarning)]


def _mode_from_subprocess_call(mock_run: Mock) -> str:
    cmd = mock_run.call_args.args[0]
    return cmd[cmd.index("--mode") + 1]


def test_omitted_execution_mode_warns_once_and_preserves_yolo_behavior(tmp_path: Path) -> None:
    orchestrator = _orchestrator(tmp_path)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with patch(
            "sensemaking_skills.runner.subprocess.run",
            return_value=SimpleNamespace(returncode=0),
        ) as mock_run:
            assert orchestrator.run_workflow("fast-path-workflow") == 0

    future = _future_warnings(caught)
    assert len(future) == 1
    assert "Omitting execution_mode is deprecated" in str(future[0].message)
    assert "pass an explicit execution mode" in str(future[0].message)
    assert _mode_from_subprocess_call(mock_run) == "yolo_execution"


def test_explicit_yolo_execution_preserves_behavior_without_deprecation_warning(
    tmp_path: Path,
) -> None:
    orchestrator = _orchestrator(tmp_path)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with patch(
            "sensemaking_skills.runner.subprocess.run",
            return_value=SimpleNamespace(returncode=0),
        ) as mock_run:
            assert orchestrator.run_workflow(
                "fast-path-workflow",
                execution_mode="yolo_execution",
            ) == 0

    assert _future_warnings(caught) == []
    assert _mode_from_subprocess_call(mock_run) == "yolo_execution"


def test_explicit_guided_execution_has_no_deprecation_warning(tmp_path: Path) -> None:
    orchestrator = _orchestrator(tmp_path)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with patch(
            "sensemaking_skills.runner.subprocess.run",
            return_value=SimpleNamespace(returncode=0),
        ) as mock_run:
            assert orchestrator.run_workflow(
                "fast-path-workflow",
                execution_mode="guided_execution",
            ) == 0

    assert _future_warnings(caught) == []
    assert _mode_from_subprocess_call(mock_run) == "guided_execution"


def test_parent_session_path_requests_yolo_explicitly(tmp_path: Path) -> None:
    orchestrator = _orchestrator(tmp_path)
    parent_session = tmp_path / "artifacts" / "parent-session"
    parent_session.mkdir(parents=True)
    (parent_session / "00-user-intent.md").write_text("# intent\n", encoding="utf-8")

    # Keep the current session equal to the parent so the setup path is exercised
    # without introducing irrelevant copy behavior into this assertion.
    orchestrator.path_resolver = SimpleNamespace(
        session_dir=lambda _session_id: parent_session
    )
    orchestrator.run_workflow = Mock(return_value=0)

    assert orchestrator._run_workflow_with_parent_session(
        "implementation-workflow",
        parent_session,
    ) == 0

    orchestrator.run_workflow.assert_called_once_with(
        "implementation-workflow",
        execution_mode="yolo_execution",
        from_session=str(parent_session.resolve()),
    )
