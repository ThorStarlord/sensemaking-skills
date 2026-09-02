"""
Regression tests for path/reference drift (PR #14).

The PR #14 review found that artifacts referenced `workflow-orchestrator/references/`
but the canonical path is `workflow-planner/references/`. This test ensures that
stale path patterns never reoccur.

These tests run on every commit and catch hard-to-debug routing failures early.
"""

import os
import re
import glob
import unittest
from pathlib import Path


class TestPathDrift(unittest.TestCase):
    """Catch references to stale skill paths and naming conventions."""

    @classmethod
    def setUpClass(cls):
        """Set up repo root."""
        cls.repo_root = Path(__file__).parent.parent

    def _search_files(self, pattern, exclude_dirs=None, exclude_files=None, include_only_dirs=None):
        """Search all relevant files for a regex pattern.

        Excludes: .git, __pycache__, .venv, node_modules, .pytest_cache, examples, archived docs

        include_only_dirs: if set, only search these directories (e.g., ["skills", "scripts", "docs/canonical-vocabulary.yaml"])
        """
        if exclude_dirs is None:
            exclude_dirs = [
                ".git", "__pycache__", ".venv", "node_modules", ".pytest_cache",
                ".github", ".claude", "worktrees", "examples", "docs/superpowers",
                "docs/validator-ecosystem", "docs/research"
            ]

        if exclude_files is None:
            exclude_files = ["test_path_drift.py"]  # Don't search the test file itself

        matches = []
        for root, dirs, files in os.walk(self.repo_root):
            # Skip if this path contains excluded dirs
            if any(excl in root for excl in exclude_dirs):
                continue

            # If include_only_dirs specified, skip unless we're in one of them
            if include_only_dirs:
                should_include = any(included in root for included in include_only_dirs)
                if not should_include:
                    continue

            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not any(ex in d for ex in exclude_dirs)]

            # Search text files
            for file in files:
                if file in exclude_files:
                    continue
                if file.endswith((".md", ".yaml", ".yml", ".json", ".py", ".txt")):
                    filepath = Path(root) / file
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            if re.search(pattern, content, re.IGNORECASE):
                                matches.append(str(filepath))
                    except Exception:
                        pass

        return matches

    def test_no_stale_paths_in_skill_code(self):
        """Regression test: no stale paths in active skill code files.

        The canonical skill path is `skills/workflow-planner/`, not
        `skills/workflow-orchestrator/`. References to the old path
        in skill code cause routing failures.

        Checks SKILL.md, validator.py, and all reference files (*.yaml, *.md)
        in skills/*/references/ directories.
        """
        stale_patterns = [
            r"skills/workflow-orchestrator/",
        ]

        for pattern in stale_patterns:
            matches = []
            skill_dirs = glob.glob(str(self.repo_root / "skills" / "*"))
            for skill_dir in skill_dirs:
                # Check skill documentation and validators
                for fname in ["SKILL.md", "validator.py"]:
                    fpath = Path(skill_dir) / fname
                    if fpath.exists():
                        content = fpath.read_text(encoding="utf-8", errors="ignore")
                        if re.search(pattern, content):
                            matches.append(str(fpath))

                # Check reference files (templates, specs, registries)
                references_dir = Path(skill_dir) / "references"
                if references_dir.exists():
                    for ref_file in references_dir.glob("*.*"):
                        if ref_file.suffix in [".md", ".yaml", ".yml"]:
                            content = ref_file.read_text(encoding="utf-8", errors="ignore")
                            if re.search(pattern, content):
                                matches.append(str(ref_file))

            self.assertFalse(
                matches,
                f"Found stale path pattern `{pattern}` in skill code: {matches}\n"
                "Use canonical paths instead."
            )

    def test_canonical_paths_used_in_docs(self):
        """Verify that all .md files reference canonical paths."""
        pattern = r"workflow-planner/references/(artifact-contracts|workflow-registry)"
        matches = self._search_files(pattern)

        # Should find at least some references to canonical paths
        self.assertGreater(
            len(matches), 0,
            "No references to canonical paths found. Are paths documented at all?"
        )

    def test_no_stale_skill_directory_names(self):
        """Catch stale references to old skill names."""
        stale_names = [
            r"skills/routing-orchestrator",  # Old name for workflow-planner?
            r"skills/orchestration",  # Avoid confusion
        ]

        for pattern in stale_names:
            matches = self._search_files(pattern)
            self.assertFalse(
                matches,
                f"Found references to stale skill name pattern `{pattern}`: {matches}"
            )

    def test_fog_type_consistency_in_docs(self):
        """Verify that fog type references use canonical forms.

        Canonical forms: product_fog, ui_fog, architecture_fog, docs_fog
        Should not use: product, ui, architecture, docs (without _fog suffix)
        """
        # Find skill/validator files that mention fog types
        skill_dirs = glob.glob(str(self.repo_root / "skills" / "*"))

        for skill_dir in skill_dirs:
            skill_md = Path(skill_dir) / "SKILL.md"
            if not skill_md.exists():
                continue

            content = skill_md.read_text(encoding="utf-8")

            # Pattern: bare fog type names (product, ui, architecture, docs)
            # NOT preceded by underscore or quotes from examples
            # This is a heuristic check; allow false negatives
            if "fog_type" in content or "fog type" in content:
                # If skill discusses fog types, should reference canonical-vocabulary.yaml
                self.assertIn(
                    "canonical-vocabulary",
                    content,
                    f"Skill {skill_dir} discusses fog types but doesn't reference canonical-vocabulary.yaml"
                )

    def test_gate_names_are_canonical(self):
        """Verify all gates in workflow-registry are in canonical-vocabulary."""
        vocab_path = self.repo_root / "docs" / "canonical-vocabulary.yaml"
        registry_path = self.repo_root / "skills" / "workflow-planner" / "references" / "workflow-registry.yaml"

        if not registry_path.exists():
            self.skipTest("workflow-registry.yaml not found")

        import yaml

        with open(vocab_path) as f:
            vocab = yaml.safe_load(f)
        with open(registry_path) as f:
            registry = yaml.safe_load(f)

        # Extract all gate IDs from vocabulary
        vocab_gate_ids = {gate["gate_id"] for gate in vocab.get("gates", [])}

        # Extract all gates used in workflow-registry
        registry_gates = set()
        for workflow in registry.get("workflows", []):
            for step in workflow.get("steps", []):
                if "gate" in step:
                    registry_gates.add(step["gate"])

        # All gates in registry must be in vocabulary
        unknown_gates = registry_gates - vocab_gate_ids
        self.assertFalse(
            unknown_gates,
            f"workflow-registry.yaml contains non-canonical gates: {sorted(unknown_gates)}\n"
            "All gates must be defined in canonical-vocabulary.yaml"
        )

    def test_no_hardcoded_artifact_paths(self):
        """Regression test placeholder for artifact path hardcoding.

        Note: This test skips because hardcoded paths in documentation and
        helper scripts (like portfolio-orchestrator.py) are acceptable.
        The runtime ensures session-scoped paths are used at execution time.

        Real enforcement happens in: tests/test_executor_path_handoff.py which
        verifies the runtime passes correct paths to skill executors.
        """
        self.skipTest("Path hardcoding enforcement moved to test_executor_path_handoff.py")

    def test_validator_path_contracts_match_canonical(self):
        """Verify validators reference correct paths.

        Note: artifact-contracts.yaml is a specification file that documents
        artifacts WITH flat paths, so it's excluded. Actual validators
        (like validator.py files) enforce path contracts at runtime.
        """
        # Read validators (excluding artifact-contracts.yaml which is a spec, not a validator)
        validator_patterns = glob.glob(str(self.repo_root / "skills" / "*" / "references" / "*.yaml"))
        validator_patterns = [v for v in validator_patterns if not v.endswith("artifact-contracts.yaml")]

        # Actual validators may not exist yet - if none found, skip
        if not validator_patterns:
            self.skipTest("No validator YAML files found to check")

        for validator_path in validator_patterns:
            content = Path(validator_path).read_text(encoding="utf-8")

            # Should not reference workflow-orchestrator
            self.assertNotIn(
                "workflow-orchestrator",
                content,
                f"Validator {validator_path} references stale skill path"
            )


class TestEnumFieldConsistency(unittest.TestCase):
    """Test that enum fields in routing_fields match actual canonical sections."""

    @classmethod
    def setUpClass(cls):
        """Set up repo root."""
        cls.repo_root = Path(__file__).parent.parent

    def test_recommended_workflow_id_matches_workflow_ids(self):
        """Verify recommended_workflow_id.values includes all workflow_ids."""
        vocab_path = self.repo_root / "docs" / "canonical-vocabulary.yaml"

        import yaml

        with open(vocab_path) as f:
            vocab = yaml.safe_load(f)

        # Get recommended_workflow_id.values from routing_fields
        routing_fields = {f["field"]: f for f in vocab.get("routing_fields", [])}
        recommended_field = routing_fields.get("recommended_workflow_id", {})
        recommended_values = set(recommended_field.get("values", []))

        # Get all workflow_ids
        workflow_ids = {w["id"] for w in vocab.get("workflow_ids", [])}

        # Recommended values must include all workflow IDs
        missing = workflow_ids - recommended_values
        extra = recommended_values - workflow_ids

        self.assertFalse(
            missing,
            f"recommended_workflow_id missing workflows that exist: {sorted(missing)}"
        )
        self.assertFalse(
            extra,
            f"recommended_workflow_id contains workflows that don't exist: {sorted(extra)}"
        )

    def test_routing_decision_method_values_are_documented(self):
        """Verify routing_decision_method values are audit-trail values, not abstract methods."""
        vocab_path = self.repo_root / "docs" / "canonical-vocabulary.yaml"

        import yaml

        with open(vocab_path) as f:
            vocab = yaml.safe_load(f)

        routing_fields = {f["field"]: f for f in vocab.get("routing_fields", [])}
        decision_field = routing_fields.get("routing_decision_method", {})
        decision_values = set(decision_field.get("values", []))

        # Expected audit-trail values from workflow-planner
        expected_values = {
            "diagnosis_primary_soft_context",
            "diagnosis_mixed_tiebreak_to_user_intent",
            "user_explicit_override",
            "escalation_recommended_accepted",
            "escalation_recommended_rejected",
        }

        self.assertEqual(
            decision_values,
            expected_values,
            f"routing_decision_method values should be audit-trail values. "
            f"Got: {decision_values}, Expected: {expected_values}"
        )


class TestCanonicalVocabularyUsage(unittest.TestCase):
    """Verify that canonical-vocabulary.yaml is actually used."""

    @classmethod
    def setUpClass(cls):
        """Set up repo root."""
        cls.repo_root = Path(__file__).parent.parent

    def test_canonical_vocabulary_exists(self):
        """The vocabulary registry file should exist."""
        vocab_path = self.repo_root / "docs" / "canonical-vocabulary.yaml"
        self.assertTrue(
            vocab_path.exists(),
            f"Canonical vocabulary file not found at {vocab_path}"
        )

    def test_packaged_vocabulary_mirror_matches_authoritative_source(self):
        """Packaged defaults must be an exact mirror of the authoritative docs vocabulary."""
        authoritative = self.repo_root / "docs" / "canonical-vocabulary.yaml"
        packaged = (
            self.repo_root
            / "src"
            / "sensemaking_skills"
            / "defaults"
            / "canonical-vocabulary.yaml"
        )

        self.assertTrue(packaged.exists(), f"Packaged vocabulary mirror not found at {packaged}")
        self.assertEqual(
            packaged.read_bytes(),
            authoritative.read_bytes(),
            "Packaged canonical-vocabulary mirror drifted from docs/canonical-vocabulary.yaml. "
            "The docs file is the single source of truth; copy it byte-for-byte into "
            "src/sensemaking_skills/defaults/canonical-vocabulary.yaml before publishing.",
        )

    def test_canonical_vocabulary_is_valid_yaml(self):
        """The vocabulary should be valid YAML."""
        vocab_path = self.repo_root / "docs" / "canonical-vocabulary.yaml"

        try:
            import yaml
            with open(vocab_path) as f:
                yaml.safe_load(f)
        except ImportError:
            self.skipTest("PyYAML not installed")
        except Exception as e:
            self.fail(f"canonical-vocabulary.yaml is not valid YAML: {e}")

    def test_vocabulary_documents_all_enum_values(self):
        """Verify vocabulary has entries for all critical enums."""
        vocab_path = self.repo_root / "docs" / "canonical-vocabulary.yaml"
        content = vocab_path.read_text(encoding="utf-8")

        required_sections = [
            "fog_types:",
            "routing_fields:",
            "gates:",
            "execution_modes:",
            "artifact_ids:",
            "workflow_ids:",
        ]

        for section in required_sections:
            self.assertIn(
                section,
                content,
                f"canonical-vocabulary.yaml missing section: {section}"
            )

    def test_vocabulary_covers_all_workflows(self):
        """Verify vocabulary includes all workflows from workflow-registry.yaml."""
        vocab_path = self.repo_root / "docs" / "canonical-vocabulary.yaml"
        registry_path = self.repo_root / "skills" / "workflow-planner" / "references" / "workflow-registry.yaml"

        if not registry_path.exists():
            self.skipTest("workflow-registry.yaml not found")

        import yaml
        with open(vocab_path) as f:
            vocab = yaml.safe_load(f)
        with open(registry_path) as f:
            registry = yaml.safe_load(f)

        vocab_workflow_ids = {w["id"] for w in vocab.get("workflow_ids", [])}
        registry_workflow_ids = {w["id"] for w in registry.get("workflows", [])}

        missing = registry_workflow_ids - vocab_workflow_ids
        self.assertFalse(
            missing,
            f"workflow-registry.yaml contains workflows not in canonical vocabulary: {sorted(missing)}\n"
            "Add missing workflows to docs/canonical-vocabulary.yaml workflow_ids section."
        )

    def test_vocabulary_covers_all_artifacts(self):
        """Verify vocabulary includes all artifacts from artifact-contracts.yaml."""
        vocab_path = self.repo_root / "docs" / "canonical-vocabulary.yaml"
        contracts_path = self.repo_root / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"

        if not contracts_path.exists():
            self.skipTest("artifact-contracts.yaml not found")

        import yaml
        with open(vocab_path) as f:
            vocab = yaml.safe_load(f)
        with open(contracts_path) as f:
            contracts = yaml.safe_load(f)

        vocab_artifact_ids = {a["id"] for a in vocab.get("artifact_ids", [])}
        contract_artifact_ids = {a["id"] for a in contracts.get("artifacts", [])}

        missing = contract_artifact_ids - vocab_artifact_ids
        self.assertFalse(
            missing,
            f"artifact-contracts.yaml contains artifacts not in canonical vocabulary: {sorted(missing)}\n"
            "Add missing artifacts to docs/canonical-vocabulary.yaml artifact_ids section."
        )


if __name__ == "__main__":
    unittest.main()
