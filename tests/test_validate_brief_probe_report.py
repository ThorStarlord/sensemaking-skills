"""Regression tests for the external local-probe evidence citation contract.

Root cause (exposed by an EXPLORATORY_EXTERNAL_DOGFOOD run against
ThorStarlord/auteur): skills/repo-sensemaker/SKILL.md directs the local Probe
Engine report to the runtime-owned same-episode `expected_probe_report_path`
(which legitimately sits OUTSIDE the target checkout, so the target stays
clean) AND tells the producer to cite measured probe evidence in Section 8.
But scripts/validate-brief.py, given `--target-repo <external-target>`,
resolved every `evidence_excerpts[].file` beneath `citation_root =
target_repo` only -- so the canonical `file: probe-report.yaml` citation was
misclassified as HALLUCINATED_FILE. The external run had to drop/rewrite
those citations to reach mechanical VALID.

The fix: one explicitly-authorized probe report. `validate-brief.py
--probe-report PATH` binds the single canonical logical citation
`probe-report.yaml` to that exact file. Everything else still resolves
beneath citation_root; there is no heuristic discovery.

Tests A-I map to the owner direction's §9 checklist. They exercise
validate_brief() directly, the validate-brief.py CLI, the
validate-and-report.py dispatcher, and the real workflow-runtime.py
invocation path.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS_DIR)

_spec = importlib.util.spec_from_file_location(
    "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py")
)
vb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vb)


PROBE_REPORT_TEXT = textwrap.dedent(
    """\
    schema_version: 1
    probe_tool: sensemaking-skills probe-repo v1
    verification_gap:
      vg: 0.0
      declared_checks:
      - scripts/check.py
    context_entropy:
      ce: 0.0
    """
)

# Brief body parametrised on the cited evidence file + quote. Kept minimal but
# structurally complete enough for validate_brief() to reach the excerpt checks.
BRIEF_TEMPLATE = """# Repository Sensemaking Brief

## 6. Weakest boundary

Some weak boundary description mentioning tight coupling and unclear contracts.

**Weakness type:** Contract Mismatch

## 7. Evidence

See `{cited_file}:1` and the excerpt below.

Logic trace: the cited evidence supports the weakest-boundary conclusion above.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: {cited_file}
    lines: "{cited_lines}"
    quote: "{cited_quote}"
    supports_claim: "demonstrates the weak boundary"
```

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "{cited_file}: example citation"
recommended_workflow_id: full-fog-workflow
weakness_type: Contract Mismatch
created_at: "2026-01-01T00:00:00Z"
immutable: true
```
"""


def _write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def _write_brief(tmpdir, cited_file, cited_lines="1", cited_quote="real file"):
    return _write(
        os.path.join(tmpdir, "brief.md"),
        BRIEF_TEMPLATE.format(cited_file=cited_file, cited_lines=cited_lines, cited_quote=cited_quote),
    )


def _hallucinated(errors):
    return [e for e in errors if "HALLUCINATED_FILE" in e.get("message", "")]


def _quote_not_found(errors):
    return [e for e in errors if "EVIDENCE_QUOTE_NOT_FOUND" in e.get("message", "")]


def _probe_not_found(errors):
    return [e for e in errors if "PROBE_REPORT_NOT_FOUND" in e.get("message", "")]


class ExternalProbeCitationContract(unittest.TestCase):
    def setUp(self):
        self._fw = tempfile.TemporaryDirectory()   # framework clone (repo_root)
        self._tgt = tempfile.TemporaryDirectory()  # external target repo
        self._epi = tempfile.TemporaryDirectory()  # runtime-owned episode dir (OUTSIDE target)
        self.repo_root = self._fw.name
        self.target_repo = self._tgt.name
        # An ordinary in-target file, to prove ordinary citations are untouched.
        os.makedirs(os.path.join(self.target_repo, "src"), exist_ok=True)
        _write(os.path.join(self.target_repo, "src", "mod.py"), "# real target file\n")
        # The runtime-owned same-episode probe report, deliberately OUTSIDE the target.
        self.probe_report = _write(os.path.join(self._epi.name, "probe-report.yaml"), PROBE_REPORT_TEXT)

    def tearDown(self):
        self._fw.cleanup()
        self._tgt.cleanup()
        self._epi.cleanup()

    # A. external target + external authorized probe report -> probe citation validates
    def test_A_probe_citation_validates_with_explicit_authority(self):
        brief = _write_brief(self.repo_root, "probe-report.yaml",
                             cited_lines="2", cited_quote="probe_tool: sensemaking-skills probe-repo v1")
        errors = vb.validate_brief(brief, repo_root=self.repo_root,
                                   target_repo=self.target_repo, probe_report=self.probe_report)
        self.assertEqual(_hallucinated(errors), [], errors)
        self.assertEqual(_quote_not_found(errors), [], errors)

    # B. exact quoted probe evidence -> quote grounding succeeds against the authorized file
    def test_B_probe_quote_grounding_runs_against_authorized_file(self):
        brief = _write_brief(self.repo_root, "probe-report.yaml",
                             cited_lines="4", cited_quote="vg: 0.0")
        errors = vb.validate_brief(brief, repo_root=self.repo_root,
                                   target_repo=self.target_repo, probe_report=self.probe_report)
        self.assertEqual(_quote_not_found(errors), [], errors)
        # And a quote that is NOT in the probe report still fails grounding.
        brief_bad = _write_brief(self.repo_root, "probe-report.yaml",
                                 cited_lines="4", cited_quote="this text is not in the probe report")
        errors_bad = vb.validate_brief(brief_bad, repo_root=self.repo_root,
                                       target_repo=self.target_repo, probe_report=self.probe_report)
        self.assertTrue(_quote_not_found(errors_bad), errors_bad)

    # C. missing explicit probe file -> fails deterministically
    def test_C_missing_explicit_probe_file_fails_closed(self):
        brief = _write_brief(self.repo_root, "src/mod.py")
        missing = os.path.join(self._epi.name, "does-not-exist.yaml")
        errors = vb.validate_brief(brief, repo_root=self.repo_root,
                                   target_repo=self.target_repo, probe_report=missing)
        pnf = _probe_not_found(errors)
        self.assertEqual(len(pnf), 1, errors)
        self.assertEqual(pnf[0].get("severity", "error"), "error")

    # D. the probe authority is scoped to exactly ONE logical name -- it does not
    #    turn other files in the episode dir into citable evidence, and the
    #    logical name never resolves to some other authorized-adjacent file.
    def test_D_probe_authority_is_scoped_to_one_logical_name(self):
        # A sibling file next to the authorized probe report is NOT citable.
        _write(os.path.join(self._epi.name, "other.yaml"), "not the probe report\n")
        brief = _write_brief(self.repo_root, "other.yaml")
        errors = vb.validate_brief(brief, repo_root=self.repo_root,
                                   target_repo=self.target_repo, probe_report=self.probe_report)
        self.assertTrue(_hallucinated(errors),
                        f"'other.yaml' must not be citable via the probe authority: {errors}")

        # And a bare relative path that is neither in target nor the logical
        # name still fails, even with probe authority supplied.
        brief2 = _write_brief(self.repo_root, "docs/nowhere.md")
        errors2 = vb.validate_brief(brief2, repo_root=self.repo_root,
                                    target_repo=self.target_repo, probe_report=self.probe_report)
        self.assertTrue(_hallucinated(errors2), errors2)

    # E. probe citation without explicit authority -> no filesystem search, fails closed
    def test_E_probe_citation_without_authority_does_not_search(self):
        brief = _write_brief(self.repo_root, "probe-report.yaml")
        errors = vb.validate_brief(brief, repo_root=self.repo_root, target_repo=self.target_repo)
        # citation_root has no probe-report.yaml -> HALLUCINATED_FILE (unchanged behavior).
        self.assertTrue(_hallucinated(errors), errors)

    # F. ordinary external-target citations -> still resolve only against the target repo
    def test_F_ordinary_target_citation_unchanged(self):
        brief = _write_brief(self.repo_root, "src/mod.py", cited_lines="1", cited_quote="real target file")
        errors = vb.validate_brief(brief, repo_root=self.repo_root,
                                   target_repo=self.target_repo, probe_report=self.probe_report)
        self.assertEqual(_hallucinated(errors), [], errors)
        # A genuinely missing target file still fails, even with probe authority present.
        brief_missing = _write_brief(self.repo_root, "src/nope.py")
        errors_missing = vb.validate_brief(brief_missing, repo_root=self.repo_root,
                                           target_repo=self.target_repo, probe_report=self.probe_report)
        self.assertEqual(len(_hallucinated(errors_missing)), 1, errors_missing)

    # G. internal/single-repository validation -> behaviorally unchanged
    def test_G_internal_single_repo_unchanged(self):
        os.makedirs(os.path.join(self.repo_root, "scripts"), exist_ok=True)
        _write(os.path.join(self.repo_root, "scripts", "real.py"), "# real\n")
        brief = _write_brief(self.repo_root, "scripts/real.py", cited_lines="1", cited_quote="# real")
        errors_plain = vb.validate_brief(brief, repo_root=self.repo_root)
        errors_probe_arg_none = vb.validate_brief(brief, repo_root=self.repo_root, probe_report=None)
        self.assertEqual(errors_plain, errors_probe_arg_none)
        self.assertEqual(_hallucinated(errors_plain), [])

    # CLI parity: validate-brief.py --probe-report resolves the fix end-to-end
    def test_cli_probe_report_flag(self):
        real_repo_root = os.path.dirname(SCRIPTS_DIR)
        brief = _write_brief(self.repo_root, "probe-report.yaml",
                             cited_lines="1", cited_quote="schema_version: 1")
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "validate-brief.py"), brief,
             "--repo-root", real_repo_root, "--target-repo", self.target_repo,
             "--probe-report", self.probe_report, "--json"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("HALLUCINATED_FILE", result.stdout)
        self.assertIn("PROBE_REPORT_NOT_FOUND", subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "validate-brief.py"), "--list-codes"],
            capture_output=True, text=True).stdout)

    # Dispatcher parity: validate-and-report.py forwards --probe-report to validate-brief.py
    def test_validate_and_report_forwards_probe_report(self):
        # --repo-root must be a real checkout (registries + scripts/ live there);
        # the brief's evidence resolves via --target-repo / --probe-report.
        real_repo_root = os.path.dirname(SCRIPTS_DIR)
        brief = _write_brief(self.repo_root, "probe-report.yaml",
                             cited_lines="1", cited_quote="schema_version: 1")
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "validate-and-report.py"), brief,
             "--repo-root", real_repo_root, "--target-repo", self.target_repo,
             "--probe-report", self.probe_report],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["valid"], payload)


_wr_spec = importlib.util.spec_from_file_location(
    "workflow_runtime", os.path.join(SCRIPTS_DIR, "workflow-runtime.py")
)
workflow_runtime = importlib.util.module_from_spec(_wr_spec)
_wr_spec.loader.exec_module(workflow_runtime)


class RuntimePassesExactExpectedProbePath(unittest.TestCase):
    """H + I: the runtime hands the validator its exact runtime-owned
    `_episode_probe_report_path` (no rediscovery), and the target checkout is
    never dirtied to satisfy probe-citation validation."""

    def test_H_runtime_reuses_episode_probe_report_path(self):
        Runner = workflow_runtime.OrchestrationRunner
        runner = Runner.__new__(Runner)
        runner.repo_root = os.path.abspath(".")
        runner.target_repo = os.path.abspath("..")  # different from repo_root
        runner.log_dir = None

        episode_dir = tempfile.mkdtemp()
        exact_probe = _write(os.path.join(episode_dir, "probe-report.yaml"), PROBE_REPORT_TEXT)
        runner._episode_probe_report_path = exact_probe

        captured = []

        class _FakeCompletedProcess:
            stdout = '{"valid": true, "errors": []}'
            stderr = ""
            returncode = 0

        def _fake_run(cmd, **kwargs):
            captured.append(cmd)
            return _FakeCompletedProcess()

        orig_run = workflow_runtime.subprocess.run
        workflow_runtime.subprocess.run = _fake_run
        try:
            runner._run_validate_and_report("repository_sensemaking_brief", "brief.md", [])
        finally:
            workflow_runtime.subprocess.run = orig_run

        validate_cmd = next(c for c in captured if any("validate-and-report.py" in str(p) for p in c))
        self.assertIn("--probe-report", validate_cmd, validate_cmd)
        self.assertEqual(
            validate_cmd[validate_cmd.index("--probe-report") + 1], exact_probe, validate_cmd
        )

    def test_H_forwards_exact_path_even_when_the_allocated_report_is_MISSING(self):
        """Contract-critical: if the producer failed to create the allocated
        probe report, the runtime must STILL forward that exact path so the
        validator fails closed (PROBE_REPORT_NOT_FOUND), not silently omit it."""
        Runner = workflow_runtime.OrchestrationRunner
        runner = Runner.__new__(Runner)
        runner.repo_root = os.path.abspath(".")
        runner.target_repo = os.path.abspath("..")
        runner.log_dir = None

        episode_dir = tempfile.mkdtemp()
        missing_exact = os.path.join(episode_dir, "probe-report.yaml")  # deliberately not created
        self.assertFalse(os.path.exists(missing_exact))
        runner._episode_probe_report_path = missing_exact

        captured = []

        class _FakeCompletedProcess:
            stdout = '{"valid": true, "errors": []}'
            stderr = ""
            returncode = 0

        def _fake_run(cmd, **kwargs):
            captured.append(cmd)
            return _FakeCompletedProcess()

        orig_run = workflow_runtime.subprocess.run
        workflow_runtime.subprocess.run = _fake_run
        try:
            runner._run_validate_and_report("repository_sensemaking_brief", "brief.md", [])
        finally:
            workflow_runtime.subprocess.run = orig_run

        validate_cmd = next(c for c in captured if any("validate-and-report.py" in str(p) for p in c))
        self.assertIn("--probe-report", validate_cmd, validate_cmd)
        self.assertEqual(
            validate_cmd[validate_cmd.index("--probe-report") + 1], missing_exact, validate_cmd
        )

    def test_H_missing_allocated_report_yields_PROBE_REPORT_NOT_FOUND_downstream(self):
        """The forwarded missing exact path must surface as PROBE_REPORT_NOT_FOUND
        (environmental / runtime failure), not silent omission and not the old
        HALLUCINATED_FILE-only degradation."""
        real_repo_root = os.path.dirname(SCRIPTS_DIR)
        fw = tempfile.mkdtemp()
        tgt = tempfile.mkdtemp()
        brief = _write_brief(fw, "src/mod.py")  # no probe citation at all
        os.makedirs(os.path.join(tgt, "src"), exist_ok=True)
        _write(os.path.join(tgt, "src", "mod.py"), "# x\n")
        missing_exact = os.path.join(tempfile.mkdtemp(), "probe-report.yaml")
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "validate-and-report.py"), brief,
             "--repo-root", real_repo_root, "--target-repo", tgt,
             "--probe-report", missing_exact],
            capture_output=True, text=True,
        )
        self.assertIn("PROBE_REPORT_NOT_FOUND", result.stdout, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["valid"], payload)

    def test_H_no_flag_when_no_episode_probe_report(self):
        Runner = workflow_runtime.OrchestrationRunner
        runner = Runner.__new__(Runner)
        runner.repo_root = os.path.abspath(".")
        runner.target_repo = os.path.abspath("..")
        runner.log_dir = None
        # No _episode_probe_report_path attribute at all (non-brief steps / older path).

        captured = []

        class _FakeCompletedProcess:
            stdout = '{"valid": true, "errors": []}'
            stderr = ""
            returncode = 0

        def _fake_run(cmd, **kwargs):
            captured.append(cmd)
            return _FakeCompletedProcess()

        orig_run = workflow_runtime.subprocess.run
        workflow_runtime.subprocess.run = _fake_run
        try:
            runner._run_validate_and_report("repository_sensemaking_brief", "brief.md", [])
        finally:
            workflow_runtime.subprocess.run = orig_run

        validate_cmd = next(c for c in captured if any("validate-and-report.py" in str(p) for p in c))
        self.assertNotIn("--probe-report", validate_cmd, validate_cmd)

    def test_I_target_checkout_not_dirtied(self):
        # The whole point: probe report lives OUTSIDE the target; validation of
        # a probe citation writes nothing into the target tree.
        tgt = tempfile.mkdtemp()
        before = sorted(os.listdir(tgt))
        epi = tempfile.mkdtemp()
        probe = _write(os.path.join(epi, "probe-report.yaml"), PROBE_REPORT_TEXT)
        fw = tempfile.mkdtemp()
        brief = _write_brief(fw, "probe-report.yaml", cited_lines="1", cited_quote="schema_version: 1")
        errors = vb.validate_brief(brief, repo_root=fw, target_repo=tgt, probe_report=probe)
        self.assertEqual(_hallucinated(errors), [], errors)
        self.assertEqual(sorted(os.listdir(tgt)), before)


if __name__ == "__main__":
    unittest.main()