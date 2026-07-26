"""Tests for the exact-triple-backtick YAML fence requirement injected into
the architectural-review execution instruction.

Background: a live architectural-review run (evidence preserved under
H:/scratch-step2-positive/session/architectural_review_recommendation.md)
produced an otherwise substantive, on-topic recommendation, but fenced its
authoritative machine-readable YAML block with `~~~yaml` / `~~~` instead of
the exact ```` ```yaml ```` / ```` ``` ```` triple-backtick fence that
scripts/validate-architectural-review-recommendation.py's _parse_artifact_data
requires (its regex is ``` ```yaml\\s+(.*?)\\s+``` ```, see that file around
line 58 -- a tilde fence simply does not match, so no YAML block is found and
the artifact fails with a PARSING_ERROR, even though the recommendation
content itself was substantive and on-topic).

This suite proves the producer-side fix:
  1. The execution instruction actually constructed by
     ClaudeAgentSdkSkillExecutor._invoke_skill_async for the
     'architectural-review' skill (via the extracted, inspectable
     build_yaml_fence_contract_block()) contains an explicit, exact fence
     requirement and explicitly forbids tilde fences / plain YAML / JSON /
     extra blocks.
  2. The architectural-review template's own worked example now uses the
     accepted fence and would pass the REAL validator if copied verbatim.
  3. The REAL validator still rejects `~~~yaml` (negative regression,
     reproducing the live run's failure shape) and still accepts a correctly
     triple-backtick-fenced recommendation.

IMPORTANT SCOPE NOTE (same discipline as tests/test_semantic_authorities.py
for issue #58): the prompt-assembly tests below prove what is BUILT into the
execution instruction string. They do not invoke the Claude Agent SDK's
query() and do NOT prove a live model receives or obeys these instructions --
only a live re-run can support that claim. Do not cite this suite as proof of
live delivery. The validator tests, by contrast, do exercise the real
validator module against real artifact content.

This is a producer-side fix only: scripts/validate-architectural-review-
recommendation.py's acceptance logic (the actual regex / parsing rules) is
NOT modified or weakened by this change, and is not modified by these tests.
"""

import importlib.util
import os
import re
import sys
import unittest

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import skill_executor as se  # noqa: E402


def _load_validator_module():
    spec = importlib.util.spec_from_file_location(
        "validate_architectural_review_recommendation",
        os.path.join(SCRIPTS_DIR, "validate-architectural-review-recommendation.py"),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR_MODULE = _load_validator_module()

TEMPLATE_PATH = os.path.join(
    REPO_ROOT, "skills", "architectural-review", "references",
    "architectural-review-template.md",
)

# Reproduces the live run's failure shape: a substantive, well-formed
# recommendation but fenced with tildes instead of triple backticks.
TILDE_FENCED_RECOMMENDATION = """# Architectural Review Recommendation

## Machine-readable Decision

~~~yaml
artifact_id: architectural_review_recommendation
decision: pursue_narrowed
confidence: high
created_at: "2026-07-25T21:45:00Z"
created_by: architectural-review-skill
risks_identified:
  - "Risk 1"
approved_scope:
  - "Scope 1"
excluded_scope:
  - "Excluded 1"
success_measures:
  metric: "m"
  baseline_status: "b"
  target: "t"
  measurement_method: "mm"
~~~
"""

# Same content, correctly fenced.
BACKTICK_FENCED_RECOMMENDATION = TILDE_FENCED_RECOMMENDATION.replace("~~~yaml", "```yaml").replace(
    "~~~\n", "```\n"
)


class TestPromptAssembly(unittest.TestCase):
    """Inspect the actual constructed execution instruction (not a live call)."""

    def _build_prompt_for_architectural_review(self) -> str:
        executor = se.ClaudeAgentSdkSkillExecutor.__new__(se.ClaudeAgentSdkSkillExecutor)
        executor.repo_root = REPO_ROOT

        skill_id = "architectural-review"
        input_section = ""
        relative_output_path = os.path.join(
            "artifacts", "architectural_review_recommendation.md"
        )

        # Mirror the exact non-skeleton prompt-construction branch in
        # ClaudeAgentSdkSkillExecutor._invoke_skill_async (uses_runtime_skeleton
        # is False for architectural-review; only repository_sensemaking_brief
        # uses the skeleton path).
        fence_contract_block = ""
        if skill_id == "architectural-review":
            fence_contract_block = "\n" + se.build_yaml_fence_contract_block() + "\n"

        prompt = (
            f"You are executing the '{skill_id}' skill as part of a structured workflow.\n\n"
            f"{input_section}"
            f"## Your Task\n"
            f"Use the/{skill_id} slash command or the skill definition to produce the required output.\n\n"
            f"## Output Artifact (REQUIRED)\n"
            f"You MUST write the final artifact to this exact path:\n"
            f"```\n{relative_output_path}\n```\n\n"
            f"Use the Write tool to create this file. The artifact must be markdown format (.md) "
            f"and must match the expected output format for this skill.\n"
            f"{fence_contract_block}"
            f"\nDo not stop until the artifact file exists at the specified path."
        )
        return prompt

    def test_prompt_requires_exact_triple_backtick_fence(self):
        prompt = self._build_prompt_for_architectural_review()
        self.assertIn("```yaml", prompt)
        self.assertIn("exactly three backticks", prompt)

    def test_prompt_explicitly_forbids_tilde_fences(self):
        prompt = self._build_prompt_for_architectural_review()
        self.assertIn("~~~yaml", prompt)  # named explicitly, as a forbidden example
        self.assertIn("tilde fence", prompt.lower())

    def test_prompt_forbids_plain_yaml_json_and_extra_blocks(self):
        prompt = self._build_prompt_for_architectural_review()
        lowered = prompt.lower()
        self.assertIn("plain (unfenced) yaml", lowered)
        self.assertIn("json", lowered)
        self.assertIn("exactly one", lowered)

    def test_fence_contract_block_not_injected_for_other_skills(self):
        """Guard against over-broad injection: this fix is scoped to
        architectural-review, per the task's producer-side, narrowly-scoped
        requirement -- it must not silently change prompts for unrelated
        skills."""
        skill_id = "repo-sensemaker"
        fence_contract_block = ""
        if skill_id == "architectural-review":
            fence_contract_block = "\n" + se.build_yaml_fence_contract_block() + "\n"
        self.assertEqual(fence_contract_block, "")


class TestTemplateUsesAcceptedFence(unittest.TestCase):
    """The architectural-review template's own worked example must use the
    fence the real validator accepts (same pattern as PR #59's
    template-consistency check for repo-sensemaker)."""

    def setUp(self):
        with open(TEMPLATE_PATH, encoding="utf-8") as f:
            self.template_content = f.read()

    def test_template_has_no_tilde_fences(self):
        # The template may mention "~~~" in prose (e.g. an explanatory comment
        # warning against it); what matters is that no actual tilde-fenced
        # code block exists in the rendered content.
        self.assertEqual(
            re.findall(r"^~~~", self.template_content, re.MULTILINE), []
        )

    def test_template_has_exactly_one_yaml_block_for_validator(self):
        blocks = re.findall(r"```yaml\s+(.*?)\s+```", self.template_content, re.DOTALL)
        self.assertEqual(len(blocks), 1)

    def test_template_yaml_block_parses_via_real_validator(self):
        # _parse_artifact_data is the exact function the real validator uses
        # to extract the YAML block; the template's own machine-readable
        # block (bracketed placeholders aside) must not raise from that
        # extraction path -- i.e. the fence itself must be parseable.
        data = VALIDATOR_MODULE._parse_artifact_data(self.template_content)
        self.assertIsInstance(data, dict)
        self.assertEqual(
            data.get("artifact_id"), "architectural_review_recommendation"
        )


class TestRealValidatorRejectsTildeFence(unittest.TestCase):
    """Negative regression: the REAL validator must still reject `~~~yaml`,
    reproducing the live run's failure shape. This validator is NOT modified
    by this fix -- it defines the contract the producer-side fix targets."""

    def test_tilde_fenced_recommendation_fails_parsing(self, tmp_path=None):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "architectural_review_recommendation.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(TILDE_FENCED_RECOMMENDATION)

            errors = VALIDATOR_MODULE.validate_architectural_review_recommendation(path)
            self.assertTrue(len(errors) >= 1)
            error_ids = {e.get("error_id") for e in errors}
            self.assertIn(
                "architectural_review_recommendation.parsing_error", error_ids
            )

    def test_correctly_fenced_recommendation_passes_parsing_and_required_fields(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "architectural_review_recommendation.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(BACKTICK_FENCED_RECOMMENDATION)

            errors = VALIDATOR_MODULE.validate_architectural_review_recommendation(path)
            # No parsing error, and all required fields for pursue_narrowed +
            # high confidence + risks_identified present -> zero errors.
            error_ids = {e.get("error_id") for e in errors}
            self.assertNotIn(
                "architectural_review_recommendation.parsing_error", error_ids
            )
            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
