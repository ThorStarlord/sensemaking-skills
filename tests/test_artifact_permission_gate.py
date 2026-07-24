"""Deterministic tests for the issue #43 runtime artifact-write confinement.

Background: create-artifact.py's overwrite guard (PR #41 / issue #40) only
stops a collision with an existing tracked file -- it never checked WHERE a
fresh path was allowed to be. Nothing structurally confined a runtime-owned
skill invocation's artifact write to the runtime-authorized destination.

This closes that gap in the Claude Agent SDK executor via a `PreToolUse` hook
(`build_artifact_permission_gate` / `artifact_permission_gate` in
scripts/skill_executor.py), NOT `can_use_tool`: the SDK's own contract states
`can_use_tool` is never invoked for a tool already permitted by
`allowed_tools`, so gating Write/Bash/etc. that way would be a fake boundary.
A `PreToolUse` hook with `matcher=None` is documented to observe/gate every
tool call regardless of `allowed_tools`/`permission_mode`.

These tests exercise the hook function directly (no live SDK query) and prove
it returns the correct allow/deny decision for every case in the confinement
matrix. They do NOT by themselves prove the CLI subprocess honors a "deny"
decision or that the hook is actually invoked before dispatch -- that is the
closed-source half of the guarantee, proven separately by the live/empirical
SDK test. Passing these tests supports "the gate function is correct"; it is
not sufficient on its own for "RUNTIME ARTIFACT CONFINEMENT PROVEN".

All file operations use tempfile.mkdtemp(); nothing is written under the
tracked `artifacts/` directory.
"""

import asyncio
import os
import sys
import tempfile
import shutil
import unittest

scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from skill_executor import canonicalize_path, build_artifact_permission_gate


def run_gate(gate, tool_name, tool_input):
    """Invoke the async hook callback synchronously for test convenience."""
    input_data = {"tool_name": tool_name, "tool_input": tool_input}
    return asyncio.run(gate(input_data, "tool-use-1", {"signal": None}))


def decision(result: dict) -> str:
    return result["hookSpecificOutput"]["permissionDecision"]


class TestCanonicalizePath(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_absolute_path_is_stable(self):
        p = os.path.join(self.tmp, "artifacts", "run-1", "out.md")
        self.assertEqual(canonicalize_path(p), canonicalize_path(p))

    def test_relative_and_absolute_equal(self):
        target = os.path.join(self.tmp, "out.md")
        cwd_before = os.getcwd()
        try:
            os.chdir(self.tmp)
            self.assertEqual(canonicalize_path("out.md"), canonicalize_path(target))
        finally:
            os.chdir(cwd_before)

    def test_traversal_normalizes_to_same_target(self):
        base = os.path.join(self.tmp, "artifacts", "run-1")
        os.makedirs(base, exist_ok=True)
        traversal = os.path.join(base, "..", "run-1", "out.md")
        direct = os.path.join(base, "out.md")
        self.assertEqual(canonicalize_path(traversal), canonicalize_path(direct))

    def test_traversal_escaping_denies_via_inequality(self):
        base = os.path.join(self.tmp, "artifacts", "run-1")
        sibling = os.path.join(self.tmp, "artifacts", "run-2", "out.md")
        os.makedirs(base, exist_ok=True)
        os.makedirs(os.path.dirname(sibling), exist_ok=True)
        traversal_out = os.path.join(base, "..", "run-2", "out.md")
        self.assertEqual(canonicalize_path(traversal_out), canonicalize_path(sibling))
        self.assertNotEqual(
            canonicalize_path(traversal_out),
            canonicalize_path(os.path.join(base, "out.md")),
        )

    def test_case_insensitive_on_this_platform(self):
        p = os.path.join(self.tmp, "Artifacts", "Out.md")
        p_lower = os.path.join(self.tmp, "artifacts", "out.md")
        if os.name == "nt":
            self.assertEqual(canonicalize_path(p), canonicalize_path(p_lower))
        else:
            # Non-Windows filesystems are typically case-sensitive; normcase is a no-op.
            self.assertEqual(canonicalize_path(p), os.path.realpath(os.path.abspath(p)))

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks not supported")
    def test_symlink_ancestor_resolves_to_real_target(self):
        real_dir = os.path.join(self.tmp, "real-run")
        os.makedirs(real_dir, exist_ok=True)
        link_dir = os.path.join(self.tmp, "linked-run")
        try:
            os.symlink(real_dir, link_dir, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation not permitted in this environment")
        via_link = os.path.join(link_dir, "out.md")
        via_real = os.path.join(real_dir, "out.md")
        self.assertEqual(canonicalize_path(via_link), canonicalize_path(via_real))

    def test_nonexistent_final_component_is_still_canonicalized(self):
        base = os.path.join(self.tmp, "artifacts", "run-1")
        os.makedirs(base, exist_ok=True)
        not_yet_created = os.path.join(base, "brand-new-artifact.md")
        self.assertFalse(os.path.exists(not_yet_created))
        # Must not raise, and must be stable/idempotent even though the file
        # (the final path component) does not exist yet.
        self.assertEqual(
            canonicalize_path(not_yet_created), canonicalize_path(not_yet_created)
        )


class TestArtifactPermissionGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.authorized = os.path.join(self.tmp, "artifacts", "100-run", "problem_frame.md")
        os.makedirs(os.path.dirname(self.authorized), exist_ok=True)
        self.gate = build_artifact_permission_gate(self.authorized)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # 1-3: read-only tools always allowed
    def test_read_allowed(self):
        result = run_gate(self.gate, "Read", {"file_path": self.authorized})
        self.assertEqual(decision(result), "allow")

    def test_glob_allowed(self):
        result = run_gate(self.gate, "Glob", {"pattern": "**/*.md"})
        self.assertEqual(decision(result), "allow")

    def test_grep_allowed(self):
        result = run_gate(self.gate, "Grep", {"pattern": "foo"})
        self.assertEqual(decision(result), "allow")

    # 4: exact authorized Write allowed
    def test_exact_authorized_write_allowed(self):
        result = run_gate(self.gate, "Write", {"file_path": self.authorized, "content": "x"})
        self.assertEqual(decision(result), "allow")

    # 5: canonically equivalent authorized Write allowed
    def test_canonically_equivalent_write_allowed(self):
        equivalent = os.path.join(
            os.path.dirname(self.authorized), "..", "100-run", "problem_frame.md"
        )
        result = run_gate(self.gate, "Write", {"file_path": equivalent, "content": "x"})
        self.assertEqual(decision(result), "allow")

    # 6: sibling path denied
    def test_sibling_path_denied(self):
        sibling = os.path.join(os.path.dirname(self.authorized), "other_artifact.md")
        result = run_gate(self.gate, "Write", {"file_path": sibling, "content": "x"})
        self.assertEqual(decision(result), "deny")
        self.assertFalse(os.path.exists(sibling))

    # 7: parent path denied
    def test_parent_path_denied(self):
        parent = os.path.dirname(self.authorized)
        result = run_gate(self.gate, "Write", {"file_path": parent, "content": "x"})
        self.assertEqual(decision(result), "deny")

    # 8: traversal outside denied
    def test_traversal_outside_denied(self):
        outside = os.path.join(os.path.dirname(self.authorized), "..", "200-run", "problem_frame.md")
        result = run_gate(self.gate, "Write", {"file_path": outside, "content": "x"})
        self.assertEqual(decision(result), "deny")
        self.assertFalse(os.path.exists(os.path.normpath(outside)))

    # 9: symlink/junction escape denied where supported
    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks not supported")
    def test_symlink_escape_denied(self):
        outside_real = os.path.join(self.tmp, "outside-run")
        os.makedirs(outside_real, exist_ok=True)
        link_path = os.path.join(os.path.dirname(self.authorized), "escape-link")
        try:
            os.symlink(outside_real, link_path, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation not permitted in this environment")
        escaping_path = os.path.join(link_path, "problem_frame.md")
        result = run_gate(self.gate, "Write", {"file_path": escaping_path, "content": "x"})
        self.assertEqual(decision(result), "deny")
        self.assertFalse(os.path.exists(escaping_path))

    # 10: missing file_path denied
    def test_missing_file_path_denied(self):
        result = run_gate(self.gate, "Write", {"content": "x"})
        self.assertEqual(decision(result), "deny")

    # 11: malformed file_path denied
    def test_malformed_file_path_denied(self):
        result = run_gate(self.gate, "Write", {"file_path": "", "content": "x"})
        self.assertEqual(decision(result), "deny")
        result2 = run_gate(self.gate, "Write", {"file_path": 12345, "content": "x"})
        self.assertEqual(decision(result2), "deny")

    # 12: Edit denied
    def test_edit_denied(self):
        result = run_gate(
            self.gate,
            "Edit",
            {"file_path": self.authorized, "old_string": "a", "new_string": "b"},
        )
        self.assertEqual(decision(result), "deny")

    # 13: Bash denied
    def test_bash_denied(self):
        result = run_gate(self.gate, "Bash", {"command": "echo hi"})
        self.assertEqual(decision(result), "deny")

    # 14: unknown tool denied
    def test_unknown_tool_denied(self):
        result = run_gate(self.gate, "NotebookEdit", {"notebook_path": "x.ipynb"})
        self.assertEqual(decision(result), "deny")
        result2 = run_gate(self.gate, "mcp__some_server__do_thing", {"anything": "x"})
        self.assertEqual(decision(result2), "deny")

    # 15: missing authorization fails closed
    def test_missing_authorization_fails_closed(self):
        unauthorized_gate = build_artifact_permission_gate(None)
        result = run_gate(unauthorized_gate, "Write", {"file_path": self.authorized, "content": "x"})
        self.assertEqual(decision(result), "deny")
        result_empty = run_gate(build_artifact_permission_gate(""), "Write", {"file_path": self.authorized, "content": "x"})
        self.assertEqual(decision(result_empty), "deny")
        # Read-only tools remain allowed even with no authorization; they are
        # never a mutation vector.
        result_read = run_gate(unauthorized_gate, "Read", {"file_path": self.authorized})
        self.assertEqual(decision(result_read), "allow")

    def test_no_denied_call_mutates_or_creates_a_file(self):
        """Every deny case above must not have created the file it targeted."""
        for candidate in (
            os.path.join(os.path.dirname(self.authorized), "other_artifact.md"),
            os.path.join(os.path.dirname(self.authorized), "..", "200-run", "problem_frame.md"),
        ):
            run_gate(self.gate, "Write", {"file_path": candidate, "content": "x"})
            self.assertFalse(os.path.exists(os.path.normpath(candidate)))


if __name__ == "__main__":
    unittest.main()
