"""The runtime guarantees the deterministic source_intent_ref machine field on
produced artifacts (ADR 0010 extended to machine fields).

Regression: the handoff skill produced a session_summary with its own plausible
machine fields but omitted source_intent_ref (the one its contract requires) —
twice, across independent runs. Rather than fight the LLM to emit an exact field
it keeps dropping, the runtime supplies the value it already knows. These tests
lock _ensure_intent_ref's behavior.
"""

import os
import sys
import tempfile
import shutil
import importlib.util
import unittest
from unittest.mock import MagicMock

scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

if "workflow_runtime" in sys.modules:
    workflow_runtime = sys.modules["workflow_runtime"]
else:
    spec = importlib.util.spec_from_file_location(
        "workflow_runtime", os.path.join(scripts_dir, "workflow-runtime.py")
    )
    workflow_runtime = importlib.util.module_from_spec(spec)
    sys.modules["workflow_runtime"] = workflow_runtime
    spec.loader.exec_module(workflow_runtime)

OrchestrationRunner = workflow_runtime.OrchestrationRunner
import yaml  # noqa: E402


class TestEnsureIntentRef(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.runner = MagicMock(spec=OrchestrationRunner)
        self.runner.repo_root = self.tmp
        # session_summary requires source_intent_ref; problem_frame (in this stub) does not.
        self.runner.contracts = {
            "artifacts": [
                {"id": "session_summary", "required_machine_fields": ["source_intent_ref"]},
                {"id": "free_artifact", "required_machine_fields": []},
            ]
        }
        self.runner._ensure_intent_ref = OrchestrationRunner._ensure_intent_ref.__get__(
            self.runner, OrchestrationRunner)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, text):
        path = os.path.join(self.tmp, "artifact.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def _yaml_blocks(self, path):
        import re
        with open(path, encoding="utf-8") as f:
            content = f.read()
        return [yaml.safe_load(b) for b in re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)]

    def test_injects_into_existing_block_when_missing(self):
        path = self._write(
            "# Session Summary\n\n## Machine\n\n```yaml\nartifact_id: session_summary\nsession_id: s-1\n```\n"
        )
        self.runner._ensure_intent_ref("session_summary", path)
        blocks = self._yaml_blocks(path)
        self.assertTrue(any(b.get("source_intent_ref") for b in blocks),
                        "source_intent_ref should have been injected")
        # Existing fields preserved.
        self.assertTrue(any(b.get("session_id") == "s-1" for b in blocks))

    def test_noop_when_already_present(self):
        original = ("# S\n\n```yaml\nartifact_id: session_summary\n"
                    "source_intent_ref: ../../00-user-intent.md\n```\n")
        path = self._write(original)
        self.runner._ensure_intent_ref("session_summary", path)
        with open(path, encoding="utf-8") as f:
            self.assertEqual(f.read(), original, "should not modify an artifact that already has it")

    def test_noop_when_contract_does_not_require_it(self):
        original = "# Free\n\n```yaml\nartifact_id: free_artifact\n```\n"
        path = self._write(original)
        self.runner._ensure_intent_ref("free_artifact", path)
        with open(path, encoding="utf-8") as f:
            self.assertEqual(f.read(), original)

    def test_appends_block_when_no_yaml_present(self):
        path = self._write("# Session Summary\n\nNo machine block here.\n")
        self.runner._ensure_intent_ref("session_summary", path)
        blocks = self._yaml_blocks(path)
        self.assertTrue(blocks and any(b.get("source_intent_ref") for b in blocks))


if __name__ == "__main__":
    unittest.main()
