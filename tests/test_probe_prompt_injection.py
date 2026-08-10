from pathlib import Path
import os
import sys
from unittest.mock import MagicMock, patch

from scripts.repo_probes import append_probe_section

scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from skill_executor import ClaudeAgentSdkSkillExecutor, SkillExecutionStatus  # noqa: E402


def test_append_probe_section_adds_report(tmp_path: Path) -> None:
    report = tmp_path / "probe-report.yaml"
    report.write_text("schema_version: 1\n", encoding="utf-8")
    parts: list[str] = ["## Skill Definition", "body"]
    append_probe_section(parts, report)
    joined = "\n".join(parts)
    assert "## Repository Probe Report" in joined
    assert "schema_version: 1" in joined


def test_append_probe_section_skips_missing_report(tmp_path: Path) -> None:
    parts: list[str] = ["## Skill Definition", "body"]
    append_probe_section(parts, tmp_path / "missing.yaml")
    assert len(parts) == 2


def test_append_probe_section_guards_missing_file_and_readable_error(tmp_path: Path) -> None:
    parts: list[str] = ["pre"]
    broken = tmp_path / "report.yaml"
    broken.write_text("{not yaml", encoding="utf-8")  # path exists -> appended as-is
    append_probe_section(parts, broken)
    assert "Repository Probe Report" in "\n".join(parts)


def test_claude_code_executor_injects_probe_report(tmp_path: Path) -> None:
    """The real runtime path (ClaudeAgentSdkSkillExecutor, alias 'claude-code')
    must include the probe report in the prompt sent to query()."""
    report = tmp_path / "probe-report.yaml"
    report.write_text("schema_version: 1\n", encoding="utf-8")
    captured: list = []

    async def mock_query(*args, **kwargs):
        captured.append(kwargs.get("prompt"))
        out = tmp_path / "artifacts" / "probe_inject_test.md"
        out.parent.mkdir(parents=True)
        out.write_text("# fake artifact\n", encoding="utf-8")
        msg = MagicMock()
        msg.is_error = False
        msg.errors = []
        msg.subtype = "success"
        msg.result = "success"
        yield msg

    executor = ClaudeAgentSdkSkillExecutor(repo_root=str(tmp_path))
    import anyio

    with patch("claude_agent_sdk.query", new=mock_query):
        result = anyio.run(
            executor._invoke_skill_async,
            "test-skill",
            "/test-skill",
            [],
            "probe_inject_test",
            {"probe_report_path": "probe-report.yaml"},
        )
    assert result.status == SkillExecutionStatus.EXECUTED
    assert "## Repository Probe Report" in captured[0]
    assert "schema_version: 1" in captured[0]
    # The closing ```yaml fence must not be glued to the next prompt section.
    assert "\n## Your Task" in captured[0]
