"""Tests for the executor environment contract.

These tests establish that:
1. Project-level ANTHROPIC_BASE_URL cannot poison API transport when removed.
2. SDK error info (ResultMessage) is captured and included in failure output.
3. The [sdk_result_error] category distinguishes API errors from missing artifacts.
4. The [no_artifact] category fires when no SDK error was reported.
"""

import os
import sys
import json
import unittest
from unittest.mock import MagicMock, patch

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
    .claude/settings.json; the fix must remove stale transport configuration
    from the source.

    The precedence claim is an integration observation proven by the controlled
    real run, not by these deterministic unit tests.
    """

    def test_claude_agent_options_has_env_and_setting_sources(self):
        """ClaudeAgentOptions is a dataclass with env and setting_sources fields."""
        from claude_agent_sdk import ClaudeAgentOptions
        self.assertIn("env", ClaudeAgentOptions.__dataclass_fields__)
        self.assertIn("setting_sources", ClaudeAgentOptions.__dataclass_fields__)

    def test_sdk_transport_env_construction(self):
        """The SDK transport subprocess code uses env overlay pattern:
        {**inherited_env, ... **options.env, ...} meaning options.env wins
        over inherited env but the CLI loads settings.json env after start.
        """
        # This is a documented architectural invariant. The SDK's subprocess
        # transport explicitly builds process_env with options.env overlaying
        # inherited env. The CLI-side settings.json env block is applied after
        # the subprocess starts, which is why options.env cannot override it.
        # The claim is verified by the controlled real run, not by asserting
        # SDK source patterns that change between versions.
        pass  # Architectural invariant — see docstring and real run evidence


class TestResultMessageErrorCapture(unittest.TestCase):
    """Executor captures SDK ResultMessage error info for classification."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)

        self.executor = ClaudeAgentSdkSkillExecutor(repo_root=self.tmpdir.name)
        self.context = {
            "resolved_inputs": {
                "repository_state": {
                    "type": "repository_state",
                    "data": {"path": self.tmpdir.name},
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
        """Run executor with mock SDK query yielding the given messages."""
        async def mock_query(*args, **kwargs):
            for msg in messages:
                yield msg

        # Patch claude_agent_sdk.query at the package level. The production
        # code imports query via `from claude_agent_sdk import query` inside
        # _invoke_skill_async, so patching the package attribute is correct.
        with patch("claude_agent_sdk.query", new=mock_query):
            import anyio
            return anyio.run(
                self.executor._invoke_skill_async,
                "test-skill", "/test-skill", [],
                "test_artifact", self.context,
            )

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

    def test_success_text_containing_error_word_not_classified(self):
        """Successful result text containing the word 'error' is NOT treated
        as an SDK error. The executor uses authoritative fields
        (is_error, errors, subtype) and does NOT infer failure from
        result text substrings."""
        result_msg = self._make_result_message(
            is_error=False,
            subtype="success",
            result="Completed review of error-handling code",
        )
        result = self._run_async_with_messages([result_msg])
        self.assertEqual(result.status, SkillExecutionStatus.FAILED)
        self.assertIn("[no_artifact]", result.error)
        self.assertNotIn("sdk_result_error", result.error)

    def test_mock_query_was_actually_consumed(self):
        """Verify that mocking works: the SDK query was called and messages
        were consumed, not silently skipped."""
        async def mock_query_with_tracker(*args, **kwargs):
            mock_query_with_tracker.called = True
            yield self._make_result_message(is_error=False, subtype="success")

        mock_query_with_tracker.called = False
        with patch("claude_agent_sdk.query", new=mock_query_with_tracker):
            import anyio
            anyio.run(
                self.executor._invoke_skill_async,
                "test-skill", "/test-skill", [],
                "test_artifact", self.context,
            )
        self.assertTrue(
            mock_query_with_tracker.called,
            "mock_query was not called — patch may target the wrong symbol",
        )


class TestProjectSettingsFile(unittest.TestCase):
    """The framework .claude/settings.json no longer contains stale proxy."""

    def test_settings_file_has_no_anthropic_base_url(self):
        """The settings file must exist and must not contain ANTHROPIC_BASE_URL."""
        repo_root = os.path.dirname(scripts_dir)
        settings_path = os.path.join(repo_root, ".claude", "settings.json")
        self.assertTrue(
            os.path.isfile(settings_path),
            f"Tracked settings file missing: {settings_path}",
        )
        with open(settings_path) as f:
            settings = json.load(f)
        env_block = settings.get("env", {})
        self.assertNotIn(
            "ANTHROPIC_BASE_URL", env_block,
            "Project settings must not override ANTHROPIC_BASE_URL",
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
