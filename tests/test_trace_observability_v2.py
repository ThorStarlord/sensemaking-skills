"""Tests for trace-observability v2 (schema_version 2), extending the
PreToolUse/PostToolUse hooks in scripts/skill_executor.py.

Motivation: a forensic review of PR #73's preserved trace
(experiments/evidence/0011-external-repo-auteur-rerun2/EVIDENCE.md) needed
to answer "was a target-directed write attempt made, and did it complete,
and was contradicting evidence ever shown to the model" -- schema_version 1
(PR #57) recorded only timestamp/event/tool_name/file_path/decision, which
was *just* enough to answer the first question by manually diffing
Pre/PostToolUse pairs by hand, but could not answer the rest: what Grep
query was used, what Read range was requested, whether a result was
truncated, or whether the model's Read/Grep calls ever surfaced the
contradicting code that would have falsified its claim.

This suite proves the extended hooks (still the SAME mechanism added in
PR #57 and extended in this fix -- no parallel logging system):
  - PreToolUse/PostToolUse events for the same tool call correlate via a
    new `invocation_id` field.
  - A denied write is distinguishable from a completed one.
  - Read offset/limit are visible.
  - Grep patterns are visible (bounded) or safely hashed.
  - A PreToolUse with no matching PostToolUse -- the exact PR #73 near-miss
    shape -- is programmatically detectable via
    find_unpaired_pretooluse_events().
  - A secret-looking value in a tool argument is redacted before being
    written to the trace.
  - Every event carries an explicit schema_version marker so any future
    consumer can tell schema_version 1 traces (no marker; treat as version
    1) apart from schema_version 2 traces.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import skill_executor as se  # noqa: E402


def _run(coro):
    import asyncio
    return asyncio.run(coro)


class TestSchemaVersionMarker(unittest.TestCase):
    def test_every_trace_event_carries_schema_version(self):
        entry = se._trace_event("PreToolUse", "Read", "/x/y.md", "observed")
        self.assertEqual(entry["schema_version"], se.TRACE_SCHEMA_VERSION)
        self.assertEqual(se.TRACE_SCHEMA_VERSION, 2)


class TestPrePostCorrelation(unittest.TestCase):
    def test_pre_and_post_share_invocation_id(self):
        trace_log = []
        pre_trace, post_trace = se.build_tool_trace_hooks(trace_log)

        async def run():
            await pre_trace({"tool_name": "Read", "tool_input": {"file_path": "/a.md"}}, "inv-1", None)
            await post_trace(
                {"tool_name": "Read", "tool_input": {"file_path": "/a.md"}, "tool_response": "hello"},
                "inv-1",
                None,
            )

        _run(run())
        pre = next(e for e in trace_log if e["event"] == "PreToolUse")
        post = next(e for e in trace_log if e["event"] == "PostToolUse")
        self.assertEqual(pre["invocation_id"], "inv-1")
        self.assertEqual(post["invocation_id"], "inv-1")
        self.assertEqual(pre["invocation_id"], post["invocation_id"])


class TestUnpairedPreToolUseDetection(unittest.TestCase):
    """Directly tests the detector that would have flagged the exact PR #73
    near-miss: a target-directed Write observed at PreToolUse with no
    PostToolUse completion anywhere in the trace."""

    def test_detects_pr73_shaped_near_miss(self):
        trace_log = []
        pre_trace, post_trace = se.build_tool_trace_hooks(trace_log)

        async def run():
            # A Read that completes normally (paired) -- should NOT be flagged.
            await pre_trace({"tool_name": "Read", "tool_input": {"file_path": "/a.md"}}, "inv-read", None)
            await post_trace(
                {"tool_name": "Read", "tool_input": {"file_path": "/a.md"}, "tool_response": "ok"},
                "inv-read",
                None,
            )
            # A Write targeting a path outside the authorized artifact, with
            # NO matching PostToolUse -- the PR #73 near-miss shape.
            await pre_trace(
                {"tool_name": "Write", "tool_input": {"file_path": "/target-clone/artifacts/brief.md"}},
                "inv-write-unpaired",
                None,
            )

        _run(run())
        unpaired = se.find_unpaired_pretooluse_events(trace_log)
        self.assertEqual(len(unpaired), 1)
        self.assertEqual(unpaired[0]["tool_name"], "Write")
        self.assertEqual(unpaired[0]["invocation_id"], "inv-write-unpaired")
        self.assertIn("target-clone", unpaired[0]["file_path"])

    def test_fully_paired_trace_has_no_unpaired_events(self):
        trace_log = []
        pre_trace, post_trace = se.build_tool_trace_hooks(trace_log)

        async def run():
            await pre_trace({"tool_name": "Write", "tool_input": {"file_path": "/x.md"}}, "inv-1", None)
            await post_trace(
                {"tool_name": "Write", "tool_input": {"file_path": "/x.md"}, "tool_response": "ok"},
                "inv-1",
                None,
            )

        _run(run())
        self.assertEqual(se.find_unpaired_pretooluse_events(trace_log), [])

    def test_schema_version_1_style_entries_fall_back_to_shape_matching(self):
        # Older traces (schema_version 1, or hand-authored fixtures) have no
        # invocation_id at all -- the detector must still work by matching
        # (tool_name, file_path) so pre-existing evidence directories remain
        # auditable with the new detector.
        v1_style = [
            {"event": "PreToolUse", "tool_name": "Write", "file_path": "/x.md"},
        ]
        unpaired = se.find_unpaired_pretooluse_events(v1_style)
        self.assertEqual(len(unpaired), 1)

        v1_style_paired = [
            {"event": "PreToolUse", "tool_name": "Write", "file_path": "/x.md"},
            {"event": "PostToolUse", "tool_name": "Write", "file_path": "/x.md"},
        ]
        self.assertEqual(se.find_unpaired_pretooluse_events(v1_style_paired), [])


class TestDeniedVsCompletedDistinguishable(unittest.TestCase):
    def test_denied_write_has_no_post_and_is_flagged_unpaired(self):
        # A denial happens entirely within PreToolUse (build_artifact_permission_gate
        # returns deny and the SDK never invokes the tool) -- so a denied
        # write, correctly, produces no PostToolUse event and is reported as
        # unpaired by the detector, same as an actually-attempted-but-never-
        # completed write. Both are "did not complete"; this test proves the
        # trace records enough to distinguish PreToolUse-only (denied or
        # incomplete) from a genuinely completed write.
        trace_log = []
        pre_trace, post_trace = se.build_tool_trace_hooks(trace_log)

        async def run():
            await pre_trace({"tool_name": "Write", "tool_input": {"file_path": "/denied.md"}}, "inv-denied", None)
            # No post_trace call -- simulates the SDK never invoking the tool.

        _run(run())
        self.assertEqual(len(trace_log), 1)
        self.assertEqual(trace_log[0]["event"], "PreToolUse")
        unpaired = se.find_unpaired_pretooluse_events(trace_log)
        self.assertEqual(len(unpaired), 1)


class TestReadRangeVisible(unittest.TestCase):
    def test_read_offset_and_limit_recorded(self):
        trace_log = []
        pre_trace, _post_trace = se.build_tool_trace_hooks(trace_log)

        async def run():
            await pre_trace(
                {"tool_name": "Read", "tool_input": {"file_path": "/big.py", "offset": 400, "limit": 100}},
                "inv-1",
                None,
            )

        _run(run())
        entry = trace_log[0]
        self.assertEqual(entry["read_offset"], 400)
        self.assertEqual(entry["read_limit"], 100)


class TestGrepPatternVisibleOrHashed(unittest.TestCase):
    def test_grep_pattern_recorded_bounded_and_hashed(self):
        trace_log = []
        pre_trace, _post_trace = se.build_tool_trace_hooks(trace_log)

        async def run():
            await pre_trace(
                {"tool_name": "Grep", "tool_input": {"pattern": "DiagnosticLayer.THEME", "glob": "*.py"}},
                "inv-1",
                None,
            )

        _run(run())
        entry = trace_log[0]
        self.assertEqual(entry["grep_pattern"], "DiagnosticLayer.THEME")
        self.assertEqual(entry["grep_glob_filter"], "*.py")
        self.assertIn("grep_pattern_hash", entry)
        self.assertEqual(len(entry["grep_pattern_hash"]), 16)

    def test_oversized_grep_pattern_is_bounded_and_flagged_truncated(self):
        trace_log = []
        pre_trace, _post_trace = se.build_tool_trace_hooks(trace_log)
        long_pattern = "x" * 500

        async def run():
            await pre_trace({"tool_name": "Grep", "tool_input": {"pattern": long_pattern}}, "inv-1", None)

        _run(run())
        entry = trace_log[0]
        self.assertLessEqual(len(entry["grep_pattern"]), se._MAX_TRACE_STRING)
        self.assertTrue(entry["grep_pattern_truncated"])


class TestGlobPatternVisible(unittest.TestCase):
    def test_glob_pattern_recorded(self):
        trace_log = []
        pre_trace, _post_trace = se.build_tool_trace_hooks(trace_log)

        async def run():
            await pre_trace({"tool_name": "Glob", "tool_input": {"pattern": "**/*.md"}}, "inv-1", None)

        _run(run())
        self.assertEqual(trace_log[0]["glob_pattern"], "**/*.md")


class TestSecretLikeValueRedacted(unittest.TestCase):
    def test_secret_looking_grep_pattern_is_redacted(self):
        trace_log = []
        pre_trace, _post_trace = se.build_tool_trace_hooks(trace_log)

        async def run():
            await pre_trace(
                {"tool_name": "Grep", "tool_input": {"pattern": "api_key=sk-abcdefghijklmnopqrstuvwx"}},
                "inv-1",
                None,
            )

        _run(run())
        entry = trace_log[0]
        self.assertNotIn("sk-abcdefghijklmnopqrstuvwx", entry["grep_pattern"])
        self.assertEqual(entry["grep_pattern"], "[REDACTED:secret-like-value]")

    def test_ordinary_pattern_is_not_redacted(self):
        self.assertEqual(se._redact("run_all_diagnostics"), "run_all_diagnostics")


class TestResultMetadataNeverLogsFullContent(unittest.TestCase):
    def test_post_trace_records_size_not_full_text(self):
        trace_log = []
        _pre_trace, post_trace = se.build_tool_trace_hooks(trace_log)
        big_text = "line\n" * 5000

        async def run():
            await post_trace(
                {"tool_name": "Read", "tool_input": {"file_path": "/big.py"}, "tool_response": big_text},
                "inv-1",
                None,
            )

        _run(run())
        entry = trace_log[0]
        self.assertEqual(entry["result_status"], "ok")
        self.assertEqual(entry["result_size"], len(big_text))
        self.assertNotIn(big_text, json_dump_safe(entry))

    def test_error_result_recorded_as_error_status_not_content(self):
        trace_log = []
        _pre_trace, post_trace = se.build_tool_trace_hooks(trace_log)

        async def run():
            await post_trace(
                {
                    "tool_name": "Write",
                    "tool_input": {"file_path": "/denied.md"},
                    "tool_response": {"is_error": True, "content": "Permission denied: secret internal reason"},
                },
                "inv-1",
                None,
            )

        _run(run())
        entry = trace_log[0]
        self.assertEqual(entry["result_status"], "error")
        self.assertNotIn("Permission denied", json_dump_safe(entry))


def json_dump_safe(entry):
    import json
    return json.dumps(entry, default=str)


class TestExistingConsumerCompatibility(unittest.TestCase):
    """No existing code parses tool-call-trace.jsonl as structured input
    today (checked: only scripts/skill_executor.py writes it; docs/adr and
    skills/repo-sensemaker/SKILL.md only mention it in prose). This test
    documents that check and guards against silently breaking a consumer if
    one is added later without updating this test."""

    def test_no_other_script_parses_trace_file_as_json(self):
        repo_root = os.path.dirname(os.path.dirname(__file__))
        scripts_dir = os.path.join(repo_root, "scripts")
        offending = []
        for name in os.listdir(scripts_dir):
            if not name.endswith(".py") or name == "skill_executor.py":
                continue
            path = os.path.join(scripts_dir, name)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            if "tool-call-trace" in text or "tool_call_trace" in text:
                offending.append(name)
        self.assertEqual(
            offending, [],
            f"found other script(s) referencing the trace file: {offending} -- "
            "if a real consumer now exists, this schema-version-2 change must "
            "be checked for compatibility with it, not just with the writer.",
        )


if __name__ == "__main__":
    unittest.main()
