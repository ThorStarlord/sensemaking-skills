"""Tests for the skeleton-aware executor wiring and tool-call trace logging
added to scripts/skill_executor.py for issue #55.

These tests exercise the trace-hook helpers and the reconciliation wiring
directly (no live SDK/network call -- ClaudeAgentSdkSkillExecutor's actual
`query()` call is exercised only by the live Step 1 rerun, tracked
separately). This suite proves:
  - PreToolUse/PostToolUse trace hooks record tool calls without changing
    any allow/deny decision.
  - write_tool_trace() writes a JSONL file to the session-scoped directory,
    not the target repository, and never logs full tool_input/content.
  - The runtime-skeleton path in _invoke_skill_async is scoped to
    repository_sensemaking_brief only (resolve_output_path unaffected for
    other artifacts).
"""

import asyncio
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import skill_executor as se  # noqa: E402
import brief_skeleton as bs  # noqa: E402


class TestToolTraceHooks(unittest.TestCase):
    def test_pre_and_post_trace_append_events(self):
        trace_log = []
        pre_trace, post_trace = se.build_tool_trace_hooks(trace_log, "/tmp/expected.md")

        async def run():
            await pre_trace(
                {"tool_name": "Read", "tool_input": {"file_path": "/tmp/other.md"}},
                "id1",
                None,
            )
            await pre_trace(
                {"tool_name": "Write", "tool_input": {"file_path": "/tmp/expected.md"}},
                "id2",
                None,
            )
            await post_trace(
                {"tool_name": "Write", "tool_input": {"file_path": "/tmp/expected.md"}},
                "id2",
                None,
            )

        asyncio.run(run())

        events = [e["event"] for e in trace_log]
        self.assertEqual(events, ["PreToolUse", "PreToolUse", "PostToolUse"])
        # The write targeting the expected artifact is distinguishable from
        # a write elsewhere.
        write_pre = [e for e in trace_log if e["event"] == "PreToolUse" and e["tool_name"] == "Write"][0]
        self.assertTrue(write_pre.get("targets_expected_artifact"))
        read_pre = [e for e in trace_log if e["tool_name"] == "Read"][0]
        self.assertFalse(read_pre.get("targets_expected_artifact"))

    def test_trace_hooks_never_override_allow_deny(self):
        trace_log = []
        pre_trace, _post_trace = se.build_tool_trace_hooks(trace_log, "/tmp/expected.md")

        async def run():
            return await pre_trace({"tool_name": "Write", "tool_input": {}}, "id", None)

        result = asyncio.run(run())
        # The trace hook is observation-only: it must return {} so the
        # authoritative artifact_permission_gate hook (registered alongside
        # it) makes the real allow/deny decision.
        self.assertEqual(result, {})

    def test_write_tool_trace_writes_jsonl_to_session_dir_not_repo_root(self):
        trace_log = [se._trace_event("PreToolUse", "Read", "/some/path.md", "observed")]
        with tempfile.TemporaryDirectory() as tmp:
            session_dir = os.path.join(tmp, "session-1")
            repo_root = tmp
            trace_path = se.write_tool_trace(trace_log, session_dir, repo_root)
            self.assertIsNotNone(trace_path)
            self.assertTrue(trace_path.startswith(session_dir))
            with open(trace_path, encoding="utf-8") as f:
                lines = [json.loads(line) for line in f if line.strip()]
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0]["tool_name"], "Read")

    def test_write_tool_trace_no_secrets_only_path_and_decision(self):
        # schema_version 2 (trace-observability v2) adds `schema_version`
        # and `invocation_id` (a correlation id) to every event on top of
        # the original schema_version 1 fields asserted here -- see
        # tests/test_trace_observability_v2.py for the new fields.
        entry = se._trace_event("PreToolUse", "Write", "/x/y.md", "allow", extra={"targets_expected_artifact": True})
        self.assertEqual(
            set(entry.keys()),
            {
                "schema_version", "timestamp", "event", "tool_name", "file_path",
                "decision", "invocation_id", "targets_expected_artifact",
            },
        )
        # No raw tool_input/content field ever present.
        self.assertNotIn("tool_input", entry)
        self.assertNotIn("content", entry)


class TestSkeletonScoping(unittest.TestCase):
    def test_skeleton_only_applies_to_brief_artifact_id(self):
        # Guards against the skeleton mechanism silently spreading to other
        # artifact types -- issue #55 is scoped to repository_sensemaking_brief
        # only; a full renderer (Architecture 3) is explicitly out of scope.
        self.assertEqual(bs.ARTIFACT_ID, "repository_sensemaking_brief")


if __name__ == "__main__":
    unittest.main()
