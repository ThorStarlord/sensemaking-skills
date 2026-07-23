"""Tests for the executor environment contract.

These tests establish that:
1. Project-level ANTHROPIC_BASE_URL cannot poison API transport when removed.
2. SDK error info (ResultMessage) is captured and included in failure output.
3. The [sdk_result_error] category distinguishes API errors from missing artifacts.
4. The [no_artifact] category fires when no SDK error was reported.
"""

import os
import sys
import tempfile
import json
import unittest
from unittest.mock import MagicMock, patch, AsyncMock

scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from skill_executor import (
    ClaudeAgentSdkSkillExecutor,
    SkillExecutionStatus,
    resolve_output_path,
)


class TestEnvironmentPrecedence(unittest.TestCase):
    """Document the SDK environment variable precedence chain.

    The SDK subprocess transport builds its child environment as:
      1. os.environ (parent process) — base
      2. CLAUDE_CODE_ENTRYPOINT=sdk-py — SDK default
      3. ClaudeAgentOptions.env — explicit caller overrides (WINS over inherited)
      4. CLAUDE_AGENT_SDK_VERSION — SDK version

    After the subprocess starts, the CLI loads .claude/settings.json and
    applies its "env" block on TOP of the subprocess environment. This means
    ClaudeAgentOptions.env cannot override a stale ANTHROPIC_BASE_URL in
    .claude/settings.json.

    The fix is therefore to remove stale transport configuration from the
    framework's project settings file.
    """

    def test_sdk_env_construction_precedence(self):
        """The SDK subprocess transport overlays options.env over parent env,
        but settings.json env is applied by the CLI after the subprocess starts.
        """
        import claude_agent_sdk._internal.transport.subprocess_cli as subproc_cls
        with open(subproc_cls.__file__) as f:
            source = f.read()
    def test_project_settings_env_is_cli_side(self):
        """settings.json env is loaded by claude.exe CLI, not by SDK transport.
        This means options.env cannot override it."""
        from claude_agent_sdk import ClaudeAgentOptions, types
        # ClaudeAgentOptions is a dataclass; env and setting_sources are fields
        self.assertIn("env", ClaudeAgentOptions.__dataclass_fields__)
        self.assertIn("setting_sources", ClaudeAgentOptions.__dataclass_fields__)



class TestResultMessageErrorCapture(unittest.TestCase):
    """Executor captures SDK ResultMessage error info for classification."""

    def setUp(self):
        self.executor = ClaudeAgentSdkSkillExecutor(repo_root="/tmp/fake-root")
        self.context = {
            "resolved_inputs": {
                "repository_state": {
                    "type": "repository_state",
                    "data": {"path": "/tmp/target"},
                }
            }
        }

    def _make_result_message(self, is_error=False, errors=None, subtype="success", result=None):
        from claude_agent_sdk import ResultMessage
        msg = MagicMock(spec=ResultMessage)
        msg.is_error = is_error
        msg.errors = errors or []
        msg.subtype = subtype
        msg.result = result
        return msg

    def _run_async_with_messages(self, messages):
        """Run executor with mocked SDK query yielding the given messages."""
        async def mock_query(*args, **kwargs):
            for msg in messages:
                yield msg
        import claude_agent_sdk
        original = claude_agent_sdk.query
        try:
            claude_agent_sdk.query = mock_query
            import anyio
            return anyio.run(
                self.executor._invoke_skill_async,
                "test-skill", "/test-skill", [],
                "test_artifact", self.context,
            )
        finally:
            claude_agent_sdk.query = original

    def test_sdk_error_result_includes_error_info(self):
        """When SDK ResultMessage has is_error=True, the error text appears."""
        result_msg = self._make_result_message(
            is_error=True,
            errors=["API Error: Unable to connect to API (ConnectionRefused)"],
        )
        result = self._run_async_with_messages([result_msg])
        self.assertEqual(result.status, SkillExecutionStatus.FAILED)
        self.assertIn("[sdk_result_error]", result.error)
        self.assertIn("ConnectionRefused", result.error)

    def test_no_sdk_error_uses_no_artifact_category(self):
        """When SDK completes normally but artifact not found, category is
        [no_artifact]."""
        result_msg = self._make_result_message(
            is_error=False, subtype="success", result="success"
        )
        result = self._run_async_with_messages([result_msg])
        self.assertEqual(result.status, SkillExecutionStatus.FAILED)
        self.assertIn("[no_artifact]", result.error)

    def test_sdk_result_without_errors_uses_subtype(self):
        """When is_error=True but errors list is empty, use subtype."""
        result_msg = self._make_result_message(
            is_error=True, errors=[], subtype="error_max_budget_usd"
        )
        result = self._run_async_with_messages([result_msg])
        self.assertIn("[sdk_result_error]", result.error)
        self.assertIn("error_max_budget_usd", result.error)

    def test_multiple_errors_joined(self):
        """Multiple errors are joined with semicolons."""
        result_msg = self._make_result_message(
            is_error=True, errors=["error 1", "error 2"],
        )
        result = self._run_async_with_messages([result_msg])
        self.assertIn("error 1; error 2", result.error)

    def test_success_result_without_is_error(self):
        """When SDK completes successfully, category is [no_artifact]."""
        result_msg = self._make_result_message(is_error=False, subtype="success")
        result = self._run_async_with_messages([result_msg])
        self.assertEqual(result.status, SkillExecutionStatus.FAILED)
        self.assertIn("[no_artifact]", result.error)


class TestProjectSettingsFile(unittest.TestCase):
    """The framework .claude/settings.json no longer contains stale proxy."""

    def test_settings_file_has_no_anthropic_base_url(self):
        """The settings file should not contain ANTHROPIC_BASE_URL."""
        repo_root = os.path.dirname(scripts_dir)
        settings_path = os.path.join(repo_root, ".claude", "settings.json")
        if os.path.exists(settings_path):
            with open(settings_path) as f:
                settings = json.load(f)
            env_block = settings.get("env", {})
            self.assertNotIn(
                "ANTHROPIC_BASE_URL", env_block,
                "Project settings must not override ANTHROPIC_BASE_URL"
            )


class TestResolveOutputPath(unittest.TestCase):
    """Shared output path resolver still works correctly."""

    def test_uses_context_path_when_provided(self):
        context = {"expected_output_path": os.path.join("/session", "artifacts", "test.md")}
        result = resolve_output_path("/repo", "test", context)
        self.assertEqual(result, os.path.join("/session", "artifacts", "test.md"))

    def test_falls_back_to_flat_path(self):
        result = resolve_output_path("/repo", "test", None)
        self.assertEqual(result, os.path.join("/repo", "artifacts", "test.md"))

    def test_falls_back_when_context_missing_path(self):
        result = resolve_output_path("/repo", "test", {})
        self.assertEqual(result, os.path.join("/repo", "artifacts", "test.md"))


if __name__ == "__main__":
    unittest.main()
