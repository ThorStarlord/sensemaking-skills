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

Correction: equality with expected_output_path alone is not sufficient
authorization. If an ancestor directory of expected_output_path is a
symlink/junction redirecting outside the session root, both the requested
path and the "authorized" expected_output_path canonicalize to the same
(relocated) location -- an equality-only check passes while the write lands
outside the session. The gate now additionally proves expected_output_path
resolves inside an independently-trusted artifact_session_dir (runtime-owned,
never inferred from expected_output_path itself) via is_within_root(). See
TestSessionRootContainment below for the containment-specific cases.

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

from skill_executor import canonicalize_path, is_within_root, build_artifact_permission_gate


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
        self.session_root = os.path.join(self.tmp, "artifacts", "100-run")
        self.authorized = os.path.join(self.session_root, "problem_frame.md")
        os.makedirs(self.session_root, exist_ok=True)
        self.gate = build_artifact_permission_gate(self.authorized, self.session_root)

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

    def test_missing_session_root_fails_closed_even_with_valid_expected_path(self):
        """expected_output_path alone, with no session root to prove containment
        in, must not be trusted -- this is the case the equality-only check
        used to accept silently."""
        gate_no_root = build_artifact_permission_gate(self.authorized, None)
        result = run_gate(gate_no_root, "Write", {"file_path": self.authorized, "content": "x"})
        self.assertEqual(decision(result), "deny")


class TestIsWithinRoot(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_root_itself_is_within_root(self):
        self.assertTrue(is_within_root(self.tmp, self.tmp))

    def test_child_is_within_root(self):
        child = os.path.join(self.tmp, "sub", "file.md")
        self.assertTrue(is_within_root(child, self.tmp))

    def test_sibling_is_not_within_root(self):
        root = os.path.join(self.tmp, "run-1")
        sibling = os.path.join(self.tmp, "run-1-evil", "file.md")
        self.assertFalse(is_within_root(sibling, root))

    def test_different_drive_is_not_within_root(self):
        if os.name != "nt":
            self.skipTest("drive-letter case only applies on Windows")
        root = os.path.join(self.tmp, "run-1")
        other_drive = "Z:\\some\\other\\place\\file.md"
        self.assertFalse(is_within_root(other_drive, root))


class TestSessionRootContainment(unittest.TestCase):
    """Required cases for the authorized-path-escape correction: equality with
    expected_output_path is not sufficient authorization by itself -- a
    symlinked/junctioned ancestor of expected_output_path could redirect the
    "authorized" path itself outside the session root, so the requested and
    authorized paths would canonicalize equal to each other while the write
    still lands outside the session. The gate must additionally prove
    expected_output_path resolves inside an independently-trusted session
    root (never inferred from expected_output_path itself)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.session_root = os.path.join(self.tmp, "artifacts", "run-1")
        os.makedirs(self.session_root, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # 1. Normal expected path under the canonical session root succeeds.
    def test_expected_path_normally_inside_root_allowed(self):
        expected = os.path.join(self.session_root, "brief.md")
        gate = build_artifact_permission_gate(expected, self.session_root)
        result = run_gate(gate, "Write", {"file_path": expected, "content": "x"})
        self.assertEqual(decision(result), "allow")

    # 2. Expected path with a symlinked ancestor escaping the root fails closed.
    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks not supported")
    def test_expected_path_symlinked_ancestor_escaping_root_denied(self):
        outside = os.path.join(self.tmp, "outside-real")
        os.makedirs(outside, exist_ok=True)
        escape_link = os.path.join(self.session_root, "escape-link")
        try:
            os.symlink(outside, escape_link, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation not permitted in this environment")

        # Both "expected" and "requested" go through the same escaping ancestor,
        # so they canonicalize equal to EACH OTHER -- this is exactly the case
        # an equality-only check would have wrongly allowed.
        expected = os.path.join(escape_link, "brief.md")
        gate = build_artifact_permission_gate(expected, self.session_root)
        result = run_gate(gate, "Write", {"file_path": expected, "content": "x"})
        self.assertEqual(decision(result), "deny")
        self.assertFalse(os.path.exists(os.path.join(outside, "brief.md")))

    # 3. Windows junction ancestor escaping the root fails where supported.
    @unittest.skipUnless(os.name == "nt", "junctions are a Windows-specific mechanism")
    def test_expected_path_junction_ancestor_escaping_root_denied(self):
        outside = os.path.join(self.tmp, "outside-real-junction")
        os.makedirs(outside, exist_ok=True)
        junction_link = os.path.join(self.session_root, "escape-junction")
        # mklink /J does not require the elevated privilege symlinks do on
        # Windows, so this should run in ordinary CI/dev environments; if the
        # platform still refuses it, skip rather than fail the suite.
        rc = os.system(
            f'mklink /J "{junction_link}" "{outside}" > NUL 2>&1'
        )
        if rc != 0 or not os.path.exists(junction_link):
            self.skipTest("could not create a junction in this environment")

        expected = os.path.join(junction_link, "brief.md")
        gate = build_artifact_permission_gate(expected, self.session_root)
        result = run_gate(gate, "Write", {"file_path": expected, "content": "x"})
        self.assertEqual(decision(result), "deny")
        self.assertFalse(os.path.exists(os.path.join(outside, "brief.md")))

    # 4. Expected path on another drive fails.
    def test_expected_path_on_another_drive_denied(self):
        if os.name != "nt":
            self.skipTest("drive-letter case only applies on Windows")
        expected = "Z:\\completely\\different\\drive\\brief.md"
        gate = build_artifact_permission_gate(expected, self.session_root)
        result = run_gate(gate, "Write", {"file_path": expected, "content": "x"})
        self.assertEqual(decision(result), "deny")

    # 5. Missing session-root authority fails closed.
    def test_missing_session_root_fails_closed(self):
        expected = os.path.join(self.session_root, "brief.md")
        gate = build_artifact_permission_gate(expected, None)
        result = run_gate(gate, "Write", {"file_path": expected, "content": "x"})
        self.assertEqual(decision(result), "deny")

    # 6. Requested == expected still fails when expected itself resolves
    #    outside the authorized root (the core equality-is-not-enough case).
    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks not supported")
    def test_requested_equals_expected_but_both_resolve_outside_root_denied(self):
        outside = os.path.join(self.tmp, "outside-real-2")
        os.makedirs(outside, exist_ok=True)
        escape_link = os.path.join(self.session_root, "escape-link-2")
        try:
            os.symlink(outside, escape_link, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation not permitted in this environment")

        expected = os.path.join(escape_link, "brief.md")
        requested = os.path.join(escape_link, "brief.md")
        self.assertEqual(canonicalize_path(expected), canonicalize_path(requested))

        gate = build_artifact_permission_gate(expected, self.session_root)
        result = run_gate(gate, "Write", {"file_path": requested, "content": "x"})
        self.assertEqual(decision(result), "deny")

    # 7. A normal nonexistent final component under the root remains allowed.
    def test_nonexistent_final_component_under_root_allowed(self):
        expected = os.path.join(self.session_root, "brand-new-not-yet-created.md")
        self.assertFalse(os.path.exists(expected))
        gate = build_artifact_permission_gate(expected, self.session_root)
        result = run_gate(gate, "Write", {"file_path": expected, "content": "x"})
        self.assertEqual(decision(result), "allow")
        self.assertFalse(os.path.exists(expected))  # gate decision alone doesn't write


if __name__ == "__main__":
    unittest.main()
