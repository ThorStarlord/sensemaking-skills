"""Regression tests for issue #40: repo-sensemaker (and sibling skills) ignoring
the runtime-provided `expected_output_path`.

Background: `skills/repo-sensemaker/SKILL.md`'s Execution Protocol used to tell the
model to call `scripts/create-artifact.py` to "resolve the output path" itself,
even though the runtime already resolves and injects a session-scoped path as
`context["expected_output_path"]` (per ADR 0010). During live runs the model
sometimes followed the SKILL.md instruction instead of the runtime-injected path,
and `create-artifact.py` happily overwrote the tracked framework artifact at
`artifacts/repository_sensemaking_brief.md`. The runtime detected the missing
artifact at its expected path and failed the step, but the tracked file had
already been mutated.

These tests lock down the fix:
  1. SKILL.md no longer instructs any skill to recompute/resolve its own output
     path via create-artifact.py (the conflicting-instruction case).
  2. create-artifact.py refuses to overwrite an existing file unless --force is
     passed, so a wrong-path write fails before mutating a tracked artifact.
"""

import glob
import os
import subprocess
import sys
import tempfile
import shutil
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CREATE_ARTIFACT = os.path.join(REPO_ROOT, "scripts", "create-artifact.py")

AFFECTED_SKILLS = [
    "repo-sensemaker",
    "workflow-planner",
    "unknowns-mapper",
    "problem-framer",
    "handoff",
]


class TestSkillMdDoesNotRecomputePath(unittest.TestCase):
    """Ensure no skill's Execution Protocol instructs recomputing the output path."""

    def test_no_skill_instructs_create_artifact_for_path_resolution(self):
        conflicting_phrase = "to resolve the output path"
        offenders = []
        for skill_md in glob.glob(os.path.join(REPO_ROOT, "skills", "*", "SKILL.md")):
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()
            if "create-artifact.py" in content and conflicting_phrase in content:
                offenders.append(skill_md)
        self.assertEqual(
            offenders, [],
            f"These SKILL.md files still instruct recomputing the output path "
            f"via create-artifact.py, conflicting with the runtime-provided "
            f"expected_output_path: {offenders}",
        )

    def test_affected_skills_reference_expected_output_path(self):
        for skill_id in AFFECTED_SKILLS:
            skill_md = os.path.join(REPO_ROOT, "skills", skill_id, "SKILL.md")
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(
                "expected_output_path", content,
                f"{skill_md} should defer to the runtime-provided expected_output_path",
            )


class TestCreateArtifactRefusesOverwrite(unittest.TestCase):
    """create-artifact.py must not silently clobber an existing (tracked) artifact."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        # Minimal repo skeleton: artifact-contracts.yaml + a pre-existing tracked
        # artifact standing in for artifacts/repository_sensemaking_brief.md.
        contracts_dir = os.path.join(
            self.tmp, "skills", "workflow-planner", "references"
        )
        os.makedirs(contracts_dir, exist_ok=True)
        with open(os.path.join(contracts_dir, "artifact-contracts.yaml"), "w", encoding="utf-8") as f:
            f.write(
                "artifacts:\n"
                "  - id: repository_sensemaking_brief\n"
                "    produced_by: repo-sensemaker\n"
                "    required_sections: []\n"
                "    required_machine_fields: []\n"
            )
        os.makedirs(os.path.join(self.tmp, "artifacts"), exist_ok=True)
        self.tracked_artifact = os.path.join(
            self.tmp, "artifacts", "repository_sensemaking_brief.md"
        )
        self.original_content = "# Repository Sensemaking Brief\n\nTRACKED CONTENT - DO NOT LOSE\n"
        with open(self.tracked_artifact, "w", encoding="utf-8") as f:
            f.write(self.original_content)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run_create_artifact(self, extra_args):
        return subprocess.run(
            [sys.executable, CREATE_ARTIFACT,
             "--artifact-id", "repository_sensemaking_brief",
             "--repo-root", self.tmp] + extra_args,
            capture_output=True, text=True,
        )

    def test_wrong_path_write_fails_before_mutating_tracked_artifact(self):
        """Simulates the conflicting-instruction case: the model calls
        create-artifact.py against the flat tracked path instead of using the
        runtime-provided expected_output_path."""
        result = self._run_create_artifact(["--path", self.tracked_artifact])

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        with open(self.tracked_artifact, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), self.original_content)

    def test_force_flag_still_allows_explicit_overwrite(self):
        result = self._run_create_artifact(["--path", self.tracked_artifact, "--force"])

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with open(self.tracked_artifact, "r", encoding="utf-8") as f:
            self.assertNotEqual(f.read(), self.original_content)

    def test_fresh_session_path_is_unaffected(self):
        """A genuine runtime session path is new, so the guard must not block it."""
        session_path = os.path.join(
            self.tmp, "artifacts", "100-orchestration-run", "repository_sensemaking_brief.md"
        )
        result = self._run_create_artifact(["--path", session_path])

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(os.path.exists(session_path))


if __name__ == "__main__":
    unittest.main()
