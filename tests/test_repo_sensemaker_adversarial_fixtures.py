"""Commit 7 - adversarial fixture regressions (12.2).

Each adversarial corpus fixture pins its misleading signal so the diagnosis
target is stable: the brief for these repositories must contend with exactly
these contradictions.
"""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS = REPO_ROOT / "experiments" / "repository-sensemaking-skill-hardening-v1" / "corpus"


class TestAdversarialFixtures(unittest.TestCase):
    def test_adv_misleading_readme_promises_absent_features(self):
        root = CORPUS / "adv-misleading-readme"
        readme = (root / "README.md").read_text(encoding="utf-8")
        app = (root / "src/app.py").read_text(encoding="utf-8")
        for feature in ("sync", "export", "webhooks"):
            self.assertIn(feature, readme, "README must advertise the ghost feature")
            self.assertNotIn(feature, app, f"code must not implement {feature}")

    def test_adv_dead_code_docs_present_legacy_as_core(self):
        root = CORPUS / "adv-dead-code"
        arch = (root / "docs/architecture.md").read_text(encoding="utf-8")
        pipeline = (root / "pipeline.py").read_text(encoding="utf-8")
        self.assertIn("legacy/processor.py", arch)
        self.assertNotIn("legacy", pipeline, "pipeline.py must not import the legacy module")

    def test_adv_duplicated_packages_conflicting_behavior(self):
        root = CORPUS / "adv-duplicated-packages"
        top = (root / "utils.py").read_text(encoding="utf-8")
        nested = (root / "core/utils.py").read_text(encoding="utf-8")
        self.assertIn("'top'", top)
        self.assertIn("'nested'", nested)
        main = (root / "main.py").read_text(encoding="utf-8")
        self.assertIn("fmt2", main, "main must use both duplicate modules")

    def test_adv_misleading_dirs_inverted_contents(self):
        root = CORPUS / "adv-misleading-dirs"
        self.assertIn("def handle", (root / "models/user.py").read_text(encoding="utf-8"),
                      "models/user.py must contain a handler, not a model")
        self.assertIn("class User", (root / "handlers/user.py").read_text(encoding="utf-8"),
                      "handlers/user.py must contain a model, not a handler")

    def test_adv_removed_feature_docs_document_absent_export(self):
        root = CORPUS / "adv-removed-feature-docs"
        doc = (root / "docs/export.md").read_text(encoding="utf-8")
        app = (root / "app.py").read_text(encoding="utf-8")
        self.assertIn("export", doc)
        self.assertNotIn("export", app, "export must be absent from the code")

    def test_adv_partial_impl_core_raises(self):
        root = CORPUS / "adv-partial-impl"
        core = (root / "core.py").read_text(encoding="utf-8")
        readme = (root / "README.md").read_text(encoding="utf-8")
        self.assertIn("NotImplementedError", core)
        self.assertIn("Implements report generation", readme)

    def test_adv_multi_registry_conflicting_ids(self):
        root = CORPUS / "adv-multi-registry"
        runtime = (root / ".workflows/registry.yaml").read_text(encoding="utf-8")
        stale = (root / "docs/workflow-registry.yaml").read_text(encoding="utf-8")
        self.assertIn("architecture-implementation-workflow", runtime)
        self.assertNotIn("architecture-implementation-workflow", stale)
        self.assertIn("arch-implementation-workflow", stale)

    def test_stale_readme_contradicts_code(self):
        root = CORPUS / "stale-readme"
        readme = (root / "README.md").read_text(encoding="utf-8")
        store = (root / "store.py").read_text(encoding="utf-8")
        self.assertIn("SQLite", readme)
        self.assertNotIn("sqlite", store, "code must use JSON, not SQLite")
        self.assertIn("json", store)


if __name__ == "__main__":
    unittest.main()
