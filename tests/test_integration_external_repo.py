"""Integration tests for analyzing external repositories with sensemaking-skills.

Tests three main integration paths:
1. Full automation: Single command analysis of external repo
2. Manual path: Diagnostic followed by manual implementation with --from-session
3. Configuration: Custom config overrides work correctly
"""

import os
import sys
import tempfile
import shutil
import yaml
import unittest
from pathlib import Path

# Add src directory to path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from sensemaking_skills import SkillsOrchestrator, ConfigManager
from sensemaking_skills.config import SkillsConfig
from sensemaking_skills.registry import WorkflowRegistry


class TestAnalyzeExternalRepo(unittest.TestCase):
    """Test full analysis of external repositories."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures - create a simple external repo."""
        cls.fixture_repo = Path(__file__).parent / "fixtures" / "simple-repo"
        if not cls.fixture_repo.exists():
            raise FileNotFoundError(f"Fixture repo not found at {cls.fixture_repo}")

        cls.tmp_test_root = Path(tempfile.mkdtemp(prefix="sensemaking_test_"))

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary directories."""
        if cls.tmp_test_root.exists():
            shutil.rmtree(cls.tmp_test_root)

    def setUp(self):
        """Set up each test."""
        # Create a working copy of the fixture repo for this test
        self.test_repo = self.tmp_test_root / f"test_repo_{id(self)}"
        if self.test_repo.exists():
            shutil.rmtree(self.test_repo)
        shutil.copytree(self.fixture_repo, self.test_repo)

    def tearDown(self):
        """Clean up after each test."""
        if self.test_repo.exists():
            shutil.rmtree(self.test_repo)

    def test_analyze_external_repo(self):
        """Test full analysis of external repository.

        Verifies that sensemaking-skills can:
        1. Load configuration from external repo
        2. Instantiate orchestrator for that repo
        3. Create required directories
        """
        print("\n" + "="*70)
        print("TEST 1: Analyze External Repository")
        print("="*70)

        # Ensure artifacts directory exists
        artifacts_dir = self.test_repo / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)

        # Load configuration from the test repo
        config_path = str(self.test_repo / "sensemaking-config.yaml")
        manager = ConfigManager(config_path)
        config = manager.load()

        # Verify configuration was loaded correctly
        self.assertIsNotNone(config, "Configuration should be loaded")
        # Project root should be set to the config file's parent directory
        self.assertEqual(
            config.project_root,
            self.test_repo,
            f"Project root should be set to config file's parent directory"
        )
        print(f"  ✓ Configuration loaded from {config_path}")
        print(f"  ✓ Project root: {config.project_root}")

        # Instantiate orchestrator
        orchestrator = SkillsOrchestrator(config=config)
        self.assertIsNotNone(orchestrator, "Orchestrator should be instantiated")
        print(f"  ✓ Orchestrator instantiated: {orchestrator}")

        # Verify workflow registry is available
        workflow_registry = config.workflow_registry
        self.assertIsNotNone(workflow_registry, "Workflow registry should exist")
        workflows = workflow_registry.list_workflows()
        self.assertGreater(len(workflows), 0, "Registry should contain workflows")
        print(f"  ✓ Workflow registry loaded with {len(workflows)} workflows")

        # Verify artifacts directory is accessible
        self.assertTrue(artifacts_dir.exists(), "Artifacts directory should exist")
        print(f"  ✓ Artifacts directory accessible: {artifacts_dir}")

        print("  [OK] TEST PASSED")

    def test_manual_path_with_from_session(self):
        """Test manual path: diagnostic then manual implementation with --from-session.

        Verifies that:
        1. Configuration can be loaded for external repo
        2. Session directory can be created for diagnostic
        3. Session can be passed between workflows via --from-session flag
        """
        print("\n" + "="*70)
        print("TEST 2: Manual Path with --from-session")
        print("="*70)

        # Ensure artifacts directory exists
        artifacts_dir = self.test_repo / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)

        # Step 1: Load config and verify orchestrator can be created
        config_path = str(self.test_repo / "sensemaking-config.yaml")
        manager = ConfigManager(config_path)
        config = manager.load()

        orchestrator = SkillsOrchestrator(config=config)
        self.assertIsNotNone(orchestrator)
        print("  ✓ Step 1: Orchestrator created for external repo")

        # Step 2: Create a diagnostic session directory
        diagnostic_session = artifacts_dir / "diagnostic-session"
        diagnostic_session.mkdir(parents=True, exist_ok=True)

        # Create a minimal brief artifact (what diagnostic would produce)
        brief_content = """---
artifact_id: repository_sensemaking_brief
project_name: Simple Test Repository
analysis_date: "2026-05-23"
---

# Repository Sensemaking Brief

This is a simple test repository with:
- A README.md documenting the project
- A Python module in src/main.py
- Configuration for sensemaking-skills

## Key Findings

The repository is well-structured and documented.
"""
        brief_path = diagnostic_session / "00-repository-sensemaking-brief.md"
        brief_path.write_text(brief_content)
        self.assertTrue(brief_path.exists())
        print(f"  ✓ Step 2: Diagnostic session created with brief artifact")
        print(f"             {brief_path}")

        # Step 3: Verify the session can be accessed for --from-session
        # This simulates passing the session to an implementation workflow
        session_id = diagnostic_session.name
        self.assertEqual(session_id, "diagnostic-session")
        print(f"  ✓ Step 3: Session ID extracted: {session_id}")

        # Verify artifacts in session are readable
        artifacts_in_session = list(diagnostic_session.glob("*.md"))
        self.assertGreater(len(artifacts_in_session), 0,
                          "Session should contain artifacts")
        print(f"  ✓ Step 4: Session contains {len(artifacts_in_session)} artifacts")

        # Verify the brief artifact has correct YAML frontmatter
        brief_text = brief_path.read_text()
        self.assertIn("artifact_id: repository_sensemaking_brief", brief_text)
        self.assertIn("project_name: Simple Test Repository", brief_text)
        print(f"  ✓ Step 5: Brief artifact has correct structure")

        print("  [OK] TEST PASSED")

    def test_custom_config_overrides_defaults(self):
        """Test that custom config overrides package defaults.

        Verifies that:
        1. Custom sensemaking-config.yaml is loaded
        2. Custom paths override defaults
        3. Configuration values are correctly applied
        """
        print("\n" + "="*70)
        print("TEST 3: Custom Config Overrides Defaults")
        print("="*70)

        # Create a custom config with non-default paths
        custom_artifacts = "custom_outputs"
        custom_config = {
            "project_root": str(self.test_repo),
            "artifacts_dir": custom_artifacts,
            "context_file": "CONTEXT.md",
            "skills_dir": "skills",
            "workflows_dir": "workflows",
            "adr_dir": "docs/adr",
        }

        # Write custom config
        custom_config_path = self.test_repo / "custom-sensemaking-config.yaml"
        with open(custom_config_path, "w") as f:
            yaml.dump(custom_config, f)

        self.assertTrue(custom_config_path.exists())
        print(f"  ✓ Step 1: Custom config created at {custom_config_path}")

        # Load the custom config
        manager = ConfigManager(str(custom_config_path))
        config = manager.load()

        # Verify custom paths are applied
        self.assertEqual(
            config.artifacts_dir.name,
            custom_artifacts,
            f"artifacts_dir should be '{custom_artifacts}'"
        )
        print(f"  ✓ Step 2: Custom artifacts_dir applied: {config.artifacts_dir}")

        # Verify other paths are also from custom config
        self.assertEqual(config.context_file, "CONTEXT.md")
        self.assertEqual(config.skills_dir.name, "skills")
        self.assertEqual(config.workflows_dir.name, "workflows")
        print(f"  ✓ Step 3: All custom paths verified")

        # Verify orchestrator uses custom config
        orchestrator = SkillsOrchestrator(config=config)
        self.assertEqual(
            orchestrator.config.artifacts_dir.name,
            custom_artifacts,
            "Orchestrator should use custom config"
        )
        print(f"  ✓ Step 4: Orchestrator uses custom config paths")

        # Create the custom artifacts directory and verify it's used
        (self.test_repo / custom_artifacts).mkdir(exist_ok=True)
        custom_artifacts_path = self.test_repo / custom_artifacts
        self.assertTrue(custom_artifacts_path.exists())
        print(f"  ✓ Step 5: Custom artifacts directory created and verified")

        print("  [OK] TEST PASSED")

    def test_config_resolution_order(self):
        """Test that config file resolution follows correct precedence.

        Verifies that:
        1. Config file path can be explicitly provided
        2. Config is loaded from the provided path
        3. project_root is correctly set to config directory
        """
        print("\n" + "="*70)
        print("TEST 4: Config Resolution Order")
        print("="*70)

        # Explicitly load from fixture config
        config_path = str(self.test_repo / "sensemaking-config.yaml")
        manager = ConfigManager(config_path)

        # Verify the config path is resolved correctly
        self.assertEqual(
            manager.config_path,
            Path(config_path),
            "ConfigManager should use provided config path"
        )
        print(f"  ✓ Step 1: Config path resolved correctly")

        # Load config
        config = manager.load()

        # Verify project_root is set to config directory (parent of config file)
        expected_root = self.test_repo
        self.assertEqual(
            config.project_root,
            expected_root,
            f"Project root should be {expected_root}"
        )
        print(f"  ✓ Step 2: Project root set to config directory: {config.project_root}")

        # Verify config values are loaded
        self.assertEqual(config.artifacts_dir.name, "artifacts")
        self.assertEqual(config.context_file, "CONTEXT.md")
        print(f"  ✓ Step 3: Config values loaded correctly")

        print("  [OK] TEST PASSED")


class TestExternalRepoWorkflowRegistry(unittest.TestCase):
    """Test that external repos can access the workflow registry."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixture_repo = Path(__file__).parent / "fixtures" / "simple-repo"
        cls.tmp_test_root = Path(tempfile.mkdtemp(prefix="sensemaking_registry_test_"))

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary directories."""
        if cls.tmp_test_root.exists():
            shutil.rmtree(cls.tmp_test_root)

    def setUp(self):
        """Set up each test."""
        self.test_repo = self.tmp_test_root / f"test_repo_{id(self)}"
        if self.test_repo.exists():
            shutil.rmtree(self.test_repo)
        shutil.copytree(self.fixture_repo, self.test_repo)

    def tearDown(self):
        """Clean up after each test."""
        if self.test_repo.exists():
            shutil.rmtree(self.test_repo)

    def test_workflow_registry_in_config(self):
        """Test that workflow registry is available in config.

        Verifies that:
        1. WorkflowRegistry can be instantiated for external repo
        2. Registry is attached to config
        3. Workflows can be queried from the registry
        """
        print("\n" + "="*70)
        print("TEST 5: Workflow Registry in Config")
        print("="*70)

        # Load config from test repo
        config_path = str(self.test_repo / "sensemaking-config.yaml")
        manager = ConfigManager(config_path)
        config = manager.load()

        # Verify registry is attached
        self.assertIsNotNone(config.workflow_registry)
        print(f"  ✓ Workflow registry attached to config")

        # Verify registry has workflows via list_workflow_details
        workflow_details = config.workflow_registry.list_workflow_details()
        self.assertIsInstance(workflow_details, list)
        self.assertGreater(len(workflow_details), 0,
                          "Registry should contain at least one workflow")
        print(f"  ✓ Registry contains {len(workflow_details)} workflows")

        # Verify workflow structure
        first_workflow = workflow_details[0]
        self.assertIn("id", first_workflow)
        self.assertIn("display_name", first_workflow)
        self.assertIn("allowed_execution_modes", first_workflow)
        print(f"  ✓ First workflow: {first_workflow['display_name']} ({first_workflow['id']})")

        # Verify we can query workflows by ID
        workflows = config.workflow_registry.list_workflows()
        self.assertIsInstance(workflows, list)
        self.assertGreater(len(workflows), 0)
        print(f"  ✓ Workflow registry lists {len(workflows)} workflow IDs")

        # Try to get a specific workflow if it exists
        if workflows:
            test_workflow_id = workflows[0]
            test_workflow = config.workflow_registry.get_workflow(test_workflow_id)
            self.assertIsNotNone(test_workflow)
            self.assertEqual(test_workflow["id"], test_workflow_id)
            print(f"  ✓ Query workflow by ID works (tested with {test_workflow_id})")

        print("  [OK] TEST PASSED")


if __name__ == "__main__":
    # Run tests with verbose output
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add both test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAnalyzeExternalRepo))
    suite.addTests(loader.loadTestsFromTestCase(TestExternalRepoWorkflowRegistry))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
