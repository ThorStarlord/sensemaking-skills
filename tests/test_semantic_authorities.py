"""Tests for the canonical semantic-authorities injection added to
scripts/skill_executor.py for issue #58.

Background: a live run (experiments/evidence/0005-runtime-skeleton-live-step1/)
passed structural validation but failed three semantic checks -- an invented
composite workflow ID, a fog-type value used where a weakness-type value was
required, and evidence citations placed only in Sections 8/13 instead of also
in Section 7's own prose. This suite proves the fix: the execution
instruction actually built by ClaudeAgentSdkSkillExecutor.build_skeleton_prompt
(the same method _invoke_skill_async calls before the SDK query()) contains
the current workflow IDs, the current weakness-type enum, and the Section 7
citation rule -- generated dynamically from the authoritative files, not
hardcoded.

IMPORTANT SCOPE NOTE: these tests inspect the prompt STRING this executor
constructs. They do not invoke the Claude Agent SDK's query() and therefore do
NOT prove the model receives or obeys these instructions in a live call --
only the one bounded live Step 1 rerun (Phase 7 of issue #58, evidence under
experiments/evidence/0006-semantic-authorities-live-step1/) can support that
claim. Do not cite this suite as proof of live delivery.
"""

import importlib.util
import os
import shutil
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, SCRIPTS_DIR)

import skill_executor as se  # noqa: E402
import brief_skeleton as bs  # noqa: E402
from _validator_utils import load_workflow_registry, load_weakness_types  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py")
)
validate_brief_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_brief_module)
validate_brief = validate_brief_module.validate_brief


class TestPromptAssembly(unittest.TestCase):
    """Inspect the actual constructed execution instruction."""

    @classmethod
    def setUpClass(cls):
        cls.executor = se.ClaudeAgentSdkSkillExecutor.__new__(se.ClaudeAgentSdkSkillExecutor)
        cls.executor.repo_root = REPO_ROOT
        cls.prompt = cls.executor.build_skeleton_prompt(
            "repo-sensemaker", "", "artifacts/repository_sensemaking_brief.md"
        )
        cls.workflow_ids = se.get_allowed_workflow_ids(REPO_ROOT)
        cls.weakness_types = se.get_allowed_weakness_types(REPO_ROOT)

    def test_prompt_contains_every_current_workflow_id(self):
        for wid in self.workflow_ids:
            self.assertIn(wid, self.prompt, f"workflow id '{wid}' missing from prompt")

    def test_prompt_workflow_id_list_excludes_skill_and_step_ids(self):
        # Skill/step ids in the registry are small integers or skill names
        # like "repo-sensemaker" / "workflow-planner" used as `skill:` values,
        # not top-level workflow ids. Assert the injected list itself (not
        # the whole prompt, which legitimately mentions the skill by name
        # elsewhere) only contains the top-level ids.
        registry = load_workflow_registry(REPO_ROOT)
        top_level_ids = {w["id"] for w in registry["workflows"]}
        self.assertEqual(set(self.workflow_ids), top_level_ids)
        # Step ids (small ints) must not appear as entries of the injected list.
        for wid in self.workflow_ids:
            self.assertNotIsInstance(wid, int)

    def test_prompt_contains_all_seven_weakness_types(self):
        self.assertEqual(len(self.weakness_types), 7)
        for wt in self.weakness_types:
            self.assertIn(wt, self.prompt, f"weakness type '{wt}' missing from prompt")

    def test_prompt_states_section_7_citation_rule(self):
        self.assertIn("Section 7", self.prompt)
        low = self.prompt.lower()
        self.assertIn("section 7", low)
        self.assertIn("evidence_excerpts", self.prompt)
        self.assertTrue(
            "does not satisfy" in low or "not satisfy" in low or "not the same" in low,
            "prompt should explicitly state 8/13 citations alone are insufficient",
        )

    def test_prompt_distinguishes_fog_type_from_weakness_type_from_workflow_id(self):
        low = self.prompt.lower()
        self.assertIn("primary_fog_type", low)
        self.assertIn("weakest_boundary", low)
        self.assertIn("recommended_workflow_id", low)
        self.assertIn("not the same", low)

    def test_prompt_is_not_hardcoded_duplicate_of_static_file_content(self):
        # The block is built at call time from the loader functions, not a
        # string literal copy-pasted elsewhere in skill_executor.py.
        with open(os.path.join(SCRIPTS_DIR, "skill_executor.py"), encoding="utf-8") as f:
            source = f.read()
        # The workflow ids should not appear as a hardcoded list literal in
        # source (only reachable via get_allowed_workflow_ids' dynamic read).
        self.assertNotIn('"fast-path-workflow", "full-fog-workflow"', source)


class TestRegistryFreshness(unittest.TestCase):
    """Adding/removing a workflow id in a test copy of the registry changes
    the injected list deterministically -- not a hardcoded duplication."""

    def setUp(self):
        self.tmp_root = tempfile.mkdtemp()
        wf_dir = os.path.join(self.tmp_root, "skills", "workflow-planner", "references")
        os.makedirs(wf_dir, exist_ok=True)
        self.registry_path = os.path.join(wf_dir, "workflow-registry.yaml")
        rs_dir = os.path.join(self.tmp_root, "skills", "repo-sensemaker", "references")
        os.makedirs(rs_dir, exist_ok=True)
        shutil.copy(
            os.path.join(REPO_ROOT, "skills", "repo-sensemaker", "references", "weakness-types.md"),
            os.path.join(rs_dir, "weakness-types.md"),
        )

    def tearDown(self):
        shutil.rmtree(self.tmp_root, ignore_errors=True)

    def _write_registry(self, ids):
        with open(self.registry_path, "w", encoding="utf-8") as f:
            f.write("workflows:\n")
            for i in ids:
                f.write(f"- id: {i}\n  display_name: test\n  steps: []\n")

    def test_adding_a_workflow_id_changes_injected_list(self):
        self._write_registry(["alpha-workflow", "beta-workflow"])
        ids1 = se.get_allowed_workflow_ids(self.tmp_root)
        self.assertEqual(set(ids1), {"alpha-workflow", "beta-workflow"})

        self._write_registry(["alpha-workflow", "beta-workflow", "gamma-workflow"])
        ids2 = se.get_allowed_workflow_ids(self.tmp_root)
        self.assertEqual(set(ids2), {"alpha-workflow", "beta-workflow", "gamma-workflow"})

    def test_removing_a_workflow_id_changes_injected_list(self):
        self._write_registry(["alpha-workflow", "beta-workflow"])
        self._write_registry(["alpha-workflow"])
        ids = se.get_allowed_workflow_ids(self.tmp_root)
        self.assertEqual(set(ids), {"alpha-workflow"})

    def test_missing_registry_raises_loudly(self):
        self._write_registry(["alpha-workflow"])
        os.remove(self.registry_path)
        with self.assertRaises(RuntimeError):
            se.get_allowed_workflow_ids(self.tmp_root)


class TestWeaknessEnumFreshness(unittest.TestCase):
    def setUp(self):
        self.tmp_root = tempfile.mkdtemp()
        rs_dir = os.path.join(self.tmp_root, "skills", "repo-sensemaker", "references")
        os.makedirs(rs_dir, exist_ok=True)
        self.path = os.path.join(rs_dir, "weakness-types.md")

    def tearDown(self):
        shutil.rmtree(self.tmp_root, ignore_errors=True)

    def _write(self, terms):
        with open(self.path, "w", encoding="utf-8") as f:
            for i, t in enumerate(terms, 1):
                f.write(f"{i}. **{t}**: description.\n")

    def test_adding_a_weakness_type_changes_injected_list(self):
        self._write(["Vocabulary Drift", "Contract Mismatch"])
        types1 = se.get_allowed_weakness_types(self.tmp_root)
        self.assertEqual(types1, ["Vocabulary Drift", "Contract Mismatch"])

        self._write(["Vocabulary Drift", "Contract Mismatch", "Zero Validation"])
        types2 = se.get_allowed_weakness_types(self.tmp_root)
        self.assertEqual(types2, ["Vocabulary Drift", "Contract Mismatch", "Zero Validation"])

    def test_missing_file_raises_loudly(self):
        # Never written -- file does not exist.
        with self.assertRaises(RuntimeError):
            se.get_allowed_weakness_types(self.tmp_root)

    def test_real_repo_has_exactly_seven_weakness_types(self):
        types = load_weakness_types(REPO_ROOT)
        self.assertEqual(len(types), 7)


class TestTemplateConsistency(unittest.TestCase):
    """The template's own worked examples, run through the real validator
    logic, would pass."""

    def test_complete_example_yaml_uses_real_workflow_id_and_weakness_type(self):
        template_path = os.path.join(
            REPO_ROOT, "skills", "repo-sensemaker", "references", "repo-analysis-template.md"
        )
        with open(template_path, encoding="utf-8") as f:
            content = f.read()

        import re
        import yaml

        match = re.search(r"### Complete Example\s*```yaml\s*(.*?)```", content, re.DOTALL)
        self.assertIsNotNone(match, "Complete Example yaml block not found")
        data = yaml.safe_load(match.group(1))

        registry = load_workflow_registry(REPO_ROOT)
        valid_ids = {w["id"] for w in registry["workflows"]}
        self.assertIn(data["recommended_workflow_id"], valid_ids)

        weakness_types = load_weakness_types(REPO_ROOT)
        self.assertTrue(
            any(wt.lower() in str(data["weakest_boundary"]).lower() for wt in weakness_types),
            f"weakest_boundary example {data['weakest_boundary']!r} does not contain a "
            f"recognized weakness type",
        )

    def test_section_6_and_7_examples_pass_the_real_validator_checks(self):
        # Build a minimal brief using the template's own worked strings for
        # Section 6 and Section 7, and confirm validate-brief's structural
        # checks (weakness type, file citation) accept them.
        brief = (
            "## 6. Weakest boundary\n"
            "The most ambiguous part of the repo.\n\n"
            "**Weakness type:** Zero Validation\n\n"
            "## 7. Evidence\n"
            "`scripts/validate-brief.py:259` shows the Evidence-section check "
            "runs independently of the evidence_excerpts block in Section 8, "
            "which is why a citation must also appear here in Section 7's own "
            "prose.\n\n"
            "Logic trace: connects the evidence above to the weakest boundary.\n"
        )
        from _validator_utils import extract_sections
        sections = extract_sections(brief)
        weakness_types = load_weakness_types(REPO_ROOT)
        weakest_boundary = sections.get("weakest boundary", "")
        self.assertTrue(any(k.lower() in weakest_boundary.lower() for k in weakness_types))
        evidence_section = sections.get("evidence", "")
        self.assertRegex(evidence_section, validate_brief_module.FILE_CITATION_RE)


class TestNegativeRegressions(unittest.TestCase):
    """Existing fixtures (PR #52/#54) already cover these; confirm they
    still fail validation post-change -- no validator weakening occurred."""

    FIXTURES_DIR = os.path.join(REPO_ROOT, "tests", "fixtures", "validate-brief", "invalid")

    def _validate(self, filename):
        path = os.path.join(self.FIXTURES_DIR, filename)
        return validate_brief(path, repo_root=REPO_ROOT)

    def test_hallucinated_workflow_id_fixture_still_fails(self):
        errors = self._validate("repo-sensemaker-id-hallucination.md")
        self.assertTrue(any("HALLUCINATED_WORKFLOW_ID" in e["message"] for e in errors))

    def test_unknown_weakness_type_fixture_still_fails(self):
        errors = self._validate("unknown-weakness-type.md")
        self.assertTrue(any("UNKNOWN_WEAKNESS_TYPE" in e["message"] for e in errors))

    def test_no_file_citations_fixture_still_fails(self):
        errors = self._validate("no-file-citations.md")
        self.assertTrue(any("NO_EVIDENCE_FILE_CITATIONS" in e["message"] for e in errors))


if __name__ == "__main__":
    unittest.main()
