"""Tests for scripts/brief_skeleton.py -- the runtime-owned artifact skeleton
for repository_sensemaking_brief (issue #55).

Covers:
  - Skeleton integrity: canonical YAML block always exists, runtime-owned
    fields cannot be omitted, required headings remain present.
  - Semantic merge: valid semantic content is inserted correctly; invalid
    workflow ids are preserved verbatim (not silently fixed); missing
    semantic fields fail validate-brief.py clearly.
  - Adversarial model output: no YAML, custom headings, whole-file
    replacement, attempts to overwrite artifact_id/created_at/immutable,
    a skill id used as a workflow id.
  - Cross-check against the real validator (validate-brief.py) so this
    suite proves the producer/consumer handoff, not just internal logic.
"""

import importlib.util
import os
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import brief_skeleton as bs  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "validate_brief", os.path.join(SCRIPTS_DIR, "validate-brief.py")
)
validate_brief_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_brief_module)
validate_brief = validate_brief_module.validate_brief

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))


def _write_tmp(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


VALID_MODEL_OUTPUT = """
Ignore this stray prose the model might emit outside markers.

<!-- MODEL_SECTION:repository_goal:BEGIN -->
This repo builds sensemaking skills for repository diagnosis.
<!-- MODEL_SECTION:repository_goal:END -->

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->
**Weakness type:** Zero Validation
<!-- MODEL_SECTION:weakest_boundary_prose:END -->

<!-- MODEL_SECTION:evidence_prose:BEGIN -->
Logic trace: skills/repo-sensemaker/references/weakness-types.md:5 shows the
taxonomy is unchecked structurally, which is the chain from evidence to the
weakest-boundary conclusion.
<!-- MODEL_SECTION:evidence_prose:END -->

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/references/weakness-types.md
    lines: L5
    quote: "1. **Vocabulary Drift**: Terms used in the README don't match the code or directory structure."
    supports_claim: "supports the diagnosis"
```
<!-- MODEL_SECTION:evidence_excerpts:END -->

```yaml
primary_fog_type: architecture_fog
recommended_workflow_id: architecture-implementation-workflow
escalation_recommended: false
weakness_type: Zero Validation
evidence:
  - "skills/repo-sensemaker/references/weakness-types.md (lines L5): weak boundary"
```
"""


class TestSkeletonIntegrity(unittest.TestCase):
    def test_fresh_skeleton_has_yaml_block(self):
        skel = bs.build_skeleton()
        self.assertIn("```yaml", skel)

    def test_fresh_skeleton_has_runtime_owned_fields(self):
        skel = bs.build_skeleton()
        self.assertIn(f"artifact_id: {bs.ARTIFACT_ID}", skel)
        self.assertIn("schema_version: 1", skel)
        self.assertIn("immutable: true", skel)
        self.assertIn("created_at:", skel)

    def test_fresh_skeleton_has_required_headings(self):
        skel = bs.build_skeleton()
        for _section_id, heading in bs.MODEL_SECTIONS:
            self.assertIn(heading, skel)
        self.assertIn("## 13. Machine-readable handoff", skel)

    def test_integrity_helper_agrees(self):
        self.assertTrue(bs.skeleton_integrity_ok(bs.build_skeleton()))


class TestSemanticMerge(unittest.TestCase):
    def test_valid_semantic_content_inserted(self):
        out = bs.reconcile(VALID_MODEL_OUTPUT)
        self.assertIn("This repo builds sensemaking skills", out)
        self.assertIn("primary_fog_type: architecture_fog", out)
        self.assertIn("recommended_workflow_id: architecture-implementation-workflow", out)

    def test_valid_output_passes_validator(self):
        out = bs.reconcile(VALID_MODEL_OUTPUT)
        path = _write_tmp(out)
        try:
            errors = validate_brief(path, REPO_ROOT)
            # The severity model (Commit 6, 11.4): warnings never invalidate.
            # FOG/WORKFLOW_PROSE_MISMATCH are informational warnings that fire
            # when the synthetic payload's 6.5 prose does not repeat the fog
            # value; only severity=error entries mean the artifact fails.
            self.assertEqual([e for e in errors if e.get("severity") == "error"], [],
                             f"expected no blocking errors, got {errors}")
        finally:
            os.remove(path)

    def test_invalid_workflow_id_preserved_and_rejected(self):
        model_output = """
```yaml
recommended_workflow_id: docs-aligner
primary_fog_type: architecture_fog
evidence:
  - "README.md: vague"
```
"""
        out = bs.reconcile(model_output)
        # Preserved verbatim -- the runtime must not silently substitute a
        # valid-looking workflow id for an invalid (skill-id-shaped) one.
        self.assertIn("recommended_workflow_id: docs-aligner", out)
        path = _write_tmp(out)
        try:
            errors = validate_brief(path, REPO_ROOT)
            codes = [e["message"] for e in errors]
            self.assertTrue(any("HALLUCINATED_WORKFLOW_ID" in m for m in codes))
        finally:
            os.remove(path)

    def test_missing_semantic_fields_fail_clearly(self):
        out = bs.reconcile("no yaml, no markers, nothing useful")
        path = _write_tmp(out)
        try:
            errors = validate_brief(path, REPO_ROOT)
            self.assertGreater(len(errors), 0)
        finally:
            os.remove(path)


class TestAdversarialModelOutput(unittest.TestCase):
    def test_no_yaml_envelope_survives(self):
        out = bs.reconcile("I finished. Everything looks fine, no YAML needed.")
        self.assertTrue(bs.skeleton_integrity_ok(out))

    def test_custom_headings_envelope_survives(self):
        adversarial = "# My Own Report\n\n## Totally Different Structure\nStuff.\n"
        out = bs.reconcile(adversarial)
        self.assertTrue(bs.skeleton_integrity_ok(out))

    def test_whole_file_replacement_envelope_survives(self):
        adversarial = "PRODUCTION READY. All checks passed. Nothing to see here."
        out = bs.reconcile(adversarial)
        self.assertTrue(bs.skeleton_integrity_ok(out))
        path = _write_tmp(out)
        try:
            errors = validate_brief(path, REPO_ROOT)
            # Structure survives, but the empty semantic content must still fail.
            self.assertGreater(len(errors), 0)
        finally:
            os.remove(path)

    def test_cannot_overwrite_artifact_id(self):
        adversarial = """
```yaml
artifact_id: something_else
```
"""
        out = bs.reconcile(adversarial)
        self.assertIn(f"artifact_id: {bs.ARTIFACT_ID}", out)
        self.assertNotIn("artifact_id: something_else", out)

    def test_cannot_overwrite_created_at_or_immutable(self):
        ctx = bs.SkeletonContext(created_at="2026-07-25T00:00:00Z")
        adversarial = """
```yaml
created_at: "2000-01-01T00:00:00Z"
immutable: false
```
"""
        out = bs.reconcile(adversarial, ctx)
        self.assertIn('created_at: "2026-07-25T00:00:00Z"', out)
        self.assertNotIn('created_at: "2000-01-01T00:00:00Z"', out)
        self.assertIn("immutable: true", out)
        self.assertNotIn("immutable: false", out)

    def test_skill_id_used_as_workflow_id_is_a_validator_failure_not_a_runtime_crash(self):
        adversarial = """
```yaml
recommended_workflow_id: repo-sensemaker
primary_fog_type: docs_fog
evidence:
  - "README.md: vague"
```
"""
        out = bs.reconcile(adversarial)
        self.assertIn("recommended_workflow_id: repo-sensemaker", out)
        path = _write_tmp(out)
        try:
            errors = validate_brief(path, REPO_ROOT)
            self.assertTrue(any("HALLUCINATED_WORKFLOW_ID" in e["message"] for e in errors))
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
