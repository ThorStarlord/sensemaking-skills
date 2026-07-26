"""Tests for bounded explicit-model enforcement (issue #86).

Covers:
  - --model reaches ClaudeAgentOptions(model=...).
  - --controlled-experiment with no --model fails before any SDK/query()
    invocation.
  - requested_model / reported_models / model_match are recorded.
  - matching / mismatching / multiple / missing AssistantMessage.model
    outcomes.
  - no fallback_model is ever set; query() is invoked at most once (no
    retry).
  - tool permissions and hooks are unchanged by this diff.
  - normal (non-controlled) invocations remain compatible with no model.

The SDK is always mocked here (query() is patched at the package level, the
same way tests/test_executor_environment.py does it) -- no real model is ever
invoked by this suite.
"""

import importlib.util
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from claude_agent_sdk import AssistantMessage, ResultMessage  # noqa: E402

from skill_executor import (  # noqa: E402
    ClaudeAgentSdkSkillExecutor,
    SkillExecutionStatus,
    create_executor,
    validate_model_identifier,
)

# Load scripts/workflow-runtime.py dynamically due to the hyphen in its
# filename (matches the pattern used by tests/test_executor_path_handoff.py).
if "workflow_runtime" in sys.modules:
    workflow_runtime = sys.modules["workflow_runtime"]
else:
    spec = importlib.util.spec_from_file_location(
        "workflow_runtime",
        os.path.join(scripts_dir, "workflow-runtime.py"),
    )
    workflow_runtime = importlib.util.module_from_spec(spec)
    sys.modules["workflow_runtime"] = workflow_runtime
    spec.loader.exec_module(workflow_runtime)

OrchestrationRunner = workflow_runtime.OrchestrationRunner


def _assistant_message(model):
    msg = MagicMock(spec=AssistantMessage)
    msg.model = model
    return msg


def _result_message(is_error=False, subtype="success"):
    msg = MagicMock(spec=ResultMessage)
    msg.is_error = is_error
    msg.errors = []
    msg.subtype = subtype
    msg.result = subtype
    return msg


class ModelEnforcementTestBase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.repo_root = self.tmpdir.name
        self.context = {
            "resolved_inputs": {
                "repository_state": {
                    "type": "repository_state",
                    "data": {"path": self.repo_root},
                }
            }
        }

    def _run(self, executor, messages, write_artifact=True, artifact_name="test_artifact"):
        """Run _invoke_skill_async with a mocked query() yielding `messages`.

        Captures the ClaudeAgentOptions passed to query() on
        captured_options[0] so tests can assert on it.
        """
        captured_options = []

        async def mock_query(*args, **kwargs):
            captured_options.append(kwargs.get("options"))
            if write_artifact:
                out_path = os.path.join(self.repo_root, "artifacts", f"{artifact_name}.md")
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write("# fake artifact\n")
            for msg in messages:
                yield msg

        mock_query.call_count = 0
        orig = mock_query

        async def counting_query(*a, **kw):
            counting_query.calls += 1
            async for m in orig(*a, **kw):
                yield m
        counting_query.calls = 0

        with patch("claude_agent_sdk.query", new=counting_query):
            import anyio
            result = anyio.run(
                executor._invoke_skill_async,
                "test-skill", "/test-skill", [],
                artifact_name, self.context,
            )
        return result, captured_options, counting_query.calls


class TestModelReachesOptions(ModelEnforcementTestBase):
    def test_explicit_model_reaches_claude_agent_options(self):
        """1. --model claude-sonnet-5 reaches ClaudeAgentOptions.model."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model="claude-sonnet-5")
        result, options, calls = self._run(
            executor, [_assistant_message("claude-sonnet-5")]
        )
        self.assertEqual(options[0].model, "claude-sonnet-5")
        self.assertEqual(result.status, SkillExecutionStatus.EXECUTED)


class TestControlledModeRequiresModel(unittest.TestCase):
    def test_controlled_experiment_without_model_raises_before_construction(self):
        """2. Controlled mode with no model fails before any SDK/query()
        invocation -- the executor itself refuses to be constructed."""
        with self.assertRaises(ValueError):
            ClaudeAgentSdkSkillExecutor(repo_root=".", controlled_experiment=True)

    def test_create_executor_propagates_the_same_failure(self):
        with self.assertRaises(ValueError):
            create_executor("claude-code", ".", controlled_experiment=True)

    def test_orchestration_runner_records_error_without_raising(self):
        """Defense-in-depth: OrchestrationRunner itself must not crash; it
        records the failure in self.errors and never builds a skill_executor
        that could reach the SDK."""
        with tempfile.TemporaryDirectory() as tmp:
            runner = OrchestrationRunner(
                workflow_id="full-local-sensemaking",
                mode="plan_only",
                repo_root=tmp,
                controlled_experiment=True,
                model=None,
            )
            self.assertIsNone(runner.skill_executor)
            self.assertTrue(runner.errors, "Expected a MODEL_REQUIRED error to be recorded")
            joined = " ".join(runner.errors)
            self.assertIn("model", joined.lower())

    def test_cli_main_rejects_controlled_experiment_without_model(self):
        """The CLI entry point itself must fail before constructing
        anything -- exercised via workflow_runtime.main()."""
        with tempfile.TemporaryDirectory() as tmp:
            rc = workflow_runtime.main([
                "--controlled-experiment",
                "--mode", "plan_only",
                "--repo-root", tmp,
                "--list-workflows",
            ])
            self.assertEqual(rc, 1)


class TestValidateModelIdentifier(unittest.TestCase):
    def test_empty_string_rejected(self):
        with self.assertRaises(ValueError):
            validate_model_identifier("")

    def test_surrounding_whitespace_rejected(self):
        with self.assertRaises(ValueError):
            validate_model_identifier(" claude-sonnet-5")
        with self.assertRaises(ValueError):
            validate_model_identifier("claude-sonnet-5 ")

    def test_valid_identifier_accepted(self):
        validate_model_identifier("claude-sonnet-5")  # must not raise

    def test_does_not_restrict_to_a_specific_model_name(self):
        """Generic controlled-run infrastructure must accept any explicit,
        well-formed model value -- Stage 1's exact-string requirement is a
        documentation/test convention, not a runtime restriction."""
        validate_model_identifier("some-other-owner-approved-model")  # must not raise


class TestRequestedModelRecorded(ModelEnforcementTestBase):
    def test_requested_model_recorded_on_result(self):
        """3. Requested model is recorded on the result even for a
        successful run."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model="claude-sonnet-5")
        result, _, _ = self._run(executor, [_assistant_message("claude-sonnet-5")])
        self.assertEqual(result.requested_model, "claude-sonnet-5")


class TestMatchingModelPasses(ModelEnforcementTestBase):
    def test_matching_assistant_message_model_passes(self):
        """4. Matching AssistantMessage.model passes."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model="claude-sonnet-5")
        result, _, _ = self._run(executor, [
            _assistant_message("claude-sonnet-5"),
            _result_message(),
        ])
        self.assertEqual(result.status, SkillExecutionStatus.EXECUTED)
        self.assertTrue(result.model_match)
        self.assertEqual(result.reported_models, ["claude-sonnet-5"])


class TestMismatchingModelFails(ModelEnforcementTestBase):
    def test_mismatching_actual_model_fails(self):
        """5. Mismatching actual model fails -- not a retry, a hard FAILED."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model="claude-sonnet-5")
        result, _, calls = self._run(executor, [_assistant_message("claude-opus-4-7")])
        self.assertEqual(result.status, SkillExecutionStatus.FAILED)
        self.assertIn("[model_mismatch]", result.error)
        self.assertFalse(result.model_match)
        self.assertEqual(calls, 1, "must not retry after a mismatch")


class TestMultipleDistinctModelsFail(ModelEnforcementTestBase):
    def test_multiple_distinct_reported_models_fail(self):
        """6. Multiple distinct reported models fail."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model="claude-sonnet-5")
        result, _, _ = self._run(executor, [
            _assistant_message("claude-sonnet-5"),
            _assistant_message("claude-opus-4-7"),
        ])
        self.assertEqual(result.status, SkillExecutionStatus.FAILED)
        self.assertIn("[model_mismatch]", result.error)
        self.assertIn("claude-sonnet-5", result.reported_models)
        self.assertIn("claude-opus-4-7", result.reported_models)


class TestMissingReportedModelFails(ModelEnforcementTestBase):
    def test_no_assistant_message_fails_when_model_requested(self):
        """7. Missing reported model fails where observation is required
        (a model was requested but the SDK never surfaced an
        AssistantMessage.model at all)."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model="claude-sonnet-5")
        result, _, _ = self._run(executor, [_result_message()])
        self.assertEqual(result.status, SkillExecutionStatus.FAILED)
        self.assertIn("[model_mismatch]", result.error)
        self.assertEqual(result.reported_models, [])


class TestNoFallbackNoRetry(ModelEnforcementTestBase):
    def test_fallback_model_never_set(self):
        """8. No fallback occurs: fallback_model is absent/None on every
        constructed ClaudeAgentOptions, mismatch or not."""
        for model, messages in [
            ("claude-sonnet-5", [_assistant_message("claude-sonnet-5")]),
            ("claude-sonnet-5", [_assistant_message("claude-opus-4-7")]),
            (None, [_assistant_message("claude-sonnet-5")]),
        ]:
            executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model=model)
            _, options, _ = self._run(executor, messages)
            self.assertIsNone(options[0].fallback_model)

    def test_query_invoked_at_most_once(self):
        """9. No retry occurs: query() is invoked exactly once per
        invoke_skill call, mismatch or not."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model="claude-sonnet-5")
        _, _, calls = self._run(executor, [_assistant_message("claude-opus-4-7")])
        self.assertEqual(calls, 1)


class TestToolPermissionsAndGatesUnchanged(ModelEnforcementTestBase):
    def test_allowed_tools_unchanged(self):
        """10. Tool permissions remain exactly unchanged."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model="claude-sonnet-5")
        _, options, _ = self._run(executor, [_assistant_message("claude-sonnet-5")])
        self.assertEqual(options[0].allowed_tools, ["Read", "Write", "Glob", "Grep"])

    def test_artifact_permission_hooks_installed(self):
        """11. Artifact permission hooks remain installed."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model="claude-sonnet-5")
        _, options, _ = self._run(executor, [_assistant_message("claude-sonnet-5")])
        hooks = options[0].hooks
        self.assertIn("PreToolUse", hooks)
        self.assertIn("PostToolUse", hooks)
        # Two PreToolUse hooks: the authoritative artifact_permission_gate
        # plus the observation-only pre_trace, same as before this change.
        self.assertEqual(len(hooks["PreToolUse"][0].hooks), 2)

    def test_target_write_confinement_behavior_unchanged(self):
        """12. Target-write confinement is untouched: a write outside the
        expected artifact path is still something build_artifact_permission_gate
        (unchanged by this diff) would police -- this asserts the gate is
        still constructed against the same expected_output_path regardless
        of model."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model="claude-sonnet-5")
        expected_path = os.path.join(self.repo_root, "artifacts", "test_artifact.md")
        with patch(
            "skill_executor.build_artifact_permission_gate",
            wraps=__import__("skill_executor").build_artifact_permission_gate,
        ) as gate_spy:
            self._run(executor, [_assistant_message("claude-sonnet-5")])
            gate_spy.assert_called_once()
            called_path = gate_spy.call_args[0][0]
            self.assertEqual(os.path.normpath(called_path), os.path.normpath(expected_path))


class TestNormalNonControlledCompatible(ModelEnforcementTestBase):
    def test_ambient_default_model_still_works(self):
        """13. Normal (non-controlled) behavior remains compatible: no
        --model supplied means model=None reaches ClaudeAgentOptions (today's
        ambient/default behavior), and no model-mismatch hard-stop fires."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model=None)
        result, options, _ = self._run(executor, [_assistant_message("whatever-ambient-model")])
        self.assertIsNone(options[0].model)
        self.assertEqual(result.status, SkillExecutionStatus.EXECUTED)
        self.assertIsNone(result.model_match)
        self.assertEqual(result.requested_model, None)
        self.assertEqual(result.reported_models, ["whatever-ambient-model"])

    def test_create_executor_defaults_preserve_ambient_behavior(self):
        executor = create_executor("claude-code", self.repo_root)
        self.assertIsNone(executor.model)
        self.assertFalse(executor.controlled_experiment)


class TestSdkAlwaysMocked(ModelEnforcementTestBase):
    def test_query_is_the_mock_not_the_real_sdk(self):
        """14. Confirms the mocking hook actually intercepts the call this
        suite relies on for every other test -- guards against a future
        refactor silently invoking the real SDK."""
        executor = ClaudeAgentSdkSkillExecutor(repo_root=self.repo_root, model="claude-sonnet-5")
        _, _, calls = self._run(executor, [_assistant_message("claude-sonnet-5")])
        self.assertEqual(calls, 1)


if __name__ == "__main__":
    unittest.main()
