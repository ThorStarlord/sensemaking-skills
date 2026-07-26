"""Regression tests for the validate-brief.py target_repo citation-resolution bug.

Root cause (see issue referenced in PR body / PR #67 evidence):
scripts/validate-brief.py resolved cited evidence file paths against
`repo_root` only, with no notion of `target_repo`. During an external-repo
run (repo_root = sensemaking-skills framework clone, target_repo = the
repository being analyzed), correct citations of real target-repo files were
misclassified as HALLUCINATED_FILE.

These tests exercise validate_brief() directly (unit-level) and also trace
the fix through scripts/validate-and-report.py and the real
workflow-runtime.py invocation path, per repo convention that "done" means
the real execution path, not just a standalone script.
"""
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS_DIR)

spec = importlib.util.spec_from_file_location(
    "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py")
)
validate_brief_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_brief_mod)


BRIEF_TEMPLATE = """# Repository Sensemaking Brief

## 3. Weakest boundary

Some weak boundary description mentioning tight coupling.

## 5. Evidence

See excerpts below, e.g. `{cited_file}:10`.

```yaml
evidence_excerpts:
  - file: {cited_file}
    lines: "10"
    quote: "example"
    supports_claim: "demonstrates the weak boundary"
```

Logic trace: the above excerpt supports the weakest-boundary claim.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: architecture_fog
evidence:
  - "{cited_file}: example citation"
recommended_workflow_id: architecture-implementation-workflow
created_at: "2026-01-01T00:00:00Z"
immutable: true
```
"""


def _write_brief(tmpdir, cited_file):
    path = os.path.join(tmpdir, "brief.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(BRIEF_TEMPLATE.format(cited_file=cited_file))
    return path


class TestTargetRepoCitationResolution(unittest.TestCase):
    def setUp(self):
        self._tmp1 = tempfile.TemporaryDirectory()
        self._tmp2 = tempfile.TemporaryDirectory()
        self.repo_root = self._tmp1.name  # framework clone (does NOT contain the cited file)
        self.target_repo = self._tmp2.name  # target repo (DOES contain the cited file)

        # Create the cited file only inside target_repo, mirroring the real
        # bug: repo_root != target_repo, cited file only exists in target_repo.
        os.makedirs(os.path.join(self.target_repo, "src", "auteur", "structure"), exist_ok=True)
        with open(
            os.path.join(self.target_repo, "src", "auteur", "structure", "diagnostics.py"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("# real file\n")

    def tearDown(self):
        self._tmp1.cleanup()
        self._tmp2.cleanup()

    def test_real_target_repo_citation_passes_with_target_repo_supplied(self):
        """A citation that only exists in target_repo must PASS when --target-repo is given."""
        cited = "src/auteur/structure/diagnostics.py"
        brief_path = _write_brief(self.repo_root, cited)

        errors = validate_brief_mod.validate_brief(
            brief_path, repo_root=self.repo_root, target_repo=self.target_repo
        )
        hallucinated = [e for e in errors if "HALLUCINATED_FILE" in e.get("message", "")]
        self.assertEqual(
            hallucinated, [],
            f"Real target-repo citation was misclassified as hallucinated: {hallucinated}",
        )

    def test_truly_nonexistent_citation_still_fails(self):
        """A citation to a file that exists in NEITHER root must still fail (true negative)."""
        cited = "src/auteur/structure/does_not_exist.py"
        brief_path = _write_brief(self.repo_root, cited)

        errors = validate_brief_mod.validate_brief(
            brief_path, repo_root=self.repo_root, target_repo=self.target_repo
        )
        hallucinated = [e for e in errors if "HALLUCINATED_FILE" in e.get("message", "")]
        self.assertEqual(
            len(hallucinated), 1,
            f"Expected exactly one HALLUCINATED_FILE error for a genuinely missing file, got: {errors}",
        )

    def test_no_target_repo_falls_back_to_repo_root_unchanged(self):
        """Without target_repo, behavior must be identical to the pre-fix single-repo path."""
        # Cited file exists in repo_root itself (single-repo/internal-proof scenario).
        os.makedirs(os.path.join(self.repo_root, "scripts"), exist_ok=True)
        with open(os.path.join(self.repo_root, "scripts", "real.py"), "w", encoding="utf-8") as f:
            f.write("# real\n")

        brief_path = _write_brief(self.repo_root, "scripts/real.py")

        errors_no_target = validate_brief_mod.validate_brief(brief_path, repo_root=self.repo_root)
        errors_target_equals_root = validate_brief_mod.validate_brief(
            brief_path, repo_root=self.repo_root, target_repo=self.repo_root
        )

        hallucinated_no_target = [e for e in errors_no_target if "HALLUCINATED_FILE" in e.get("message", "")]
        hallucinated_target_eq_root = [
            e for e in errors_target_equals_root if "HALLUCINATED_FILE" in e.get("message", "")
        ]
        self.assertEqual(hallucinated_no_target, [])
        self.assertEqual(hallucinated_target_eq_root, [])
        self.assertEqual(errors_no_target, errors_target_equals_root)

    def test_cli_target_repo_flag(self):
        """The --target-repo CLI flag on validate-brief.py itself resolves the fix end-to-end."""
        cited = "src/auteur/structure/diagnostics.py"
        brief_path = _write_brief(self.repo_root, cited)

        validator_script = os.path.join(SCRIPTS_DIR, "validate-brief.py")
        result = subprocess.run(
            [
                sys.executable, validator_script, brief_path,
                "--repo-root", self.repo_root,
                "--target-repo", self.target_repo,
                "--json",
            ],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("HALLUCINATED_FILE", result.stdout)


if __name__ == "__main__":
    unittest.main()
