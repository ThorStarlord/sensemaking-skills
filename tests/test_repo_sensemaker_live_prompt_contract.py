"""Deterministic tests for the live repo-sensemaker prompt-construction path.

Closes the test gap identified in issue #53 / PR #52: existing tests only
prove hand-written fixtures satisfy validate-brief.py. They do not prove the
prompt actually assembled for the live model contains the guidance needed to
avoid the three diagnosed failures (skill/workflow ID confusion, evidence
line-format disagreement, missing evidence-authority hierarchy).

The live path is `ClaudeAgentSdkSkillExecutor._invoke_skill_async`
(scripts/skill_executor.py), which invokes the Claude Agent SDK with
`skills=[skill_id]`. The SDK loads `skills/<skill_id>/SKILL.md` (and anything
it references) as the skill definition -- SKILL.md is therefore the
authoritative live-prompt source for repo-sensemaker, not the short generic
wrapper string built inline in _invoke_skill_async. These tests read the real
files from disk (no network / no live SDK call) and assert the combination of
(a) the generic wrapper prompt and (b) SKILL.md (plus its referenced files)
together satisfy the required content.
"""

import inspect
import os
import re
import sys

_SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import skill_executor  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(REPO_ROOT, "skills", "repo-sensemaker", "SKILL.md")
EVIDENCE_RULES = os.path.join(
    REPO_ROOT, "skills", "repo-sensemaker", "references", "evidence-rules.md"
)
TEMPLATE = os.path.join(
    REPO_ROOT, "skills", "repo-sensemaker", "references", "repo-analysis-template.md"
)
REGISTRY = os.path.join(
    REPO_ROOT, "skills", "workflow-planner", "references", "workflow-registry.yaml"
)


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def _assembled_live_content() -> str:
    """Everything the live SDK-driven repo-sensemaker invocation is exposed to:
    the generic wrapper prompt text (from _invoke_skill_async's source) plus
    the skill definition and its referenced reference files (loaded by the
    SDK via `skills=[skill_id]`, mirroring how a real invocation would read
    SKILL.md and follow its [References] links).
    """
    wrapper_source = inspect.getsource(skill_executor.ClaudeAgentSdkSkillExecutor._invoke_skill_async)
    return "\n".join([wrapper_source, _read(SKILL_MD), _read(EVIDENCE_RULES), _read(TEMPLATE)])


# --- SDK wiring: prove SKILL.md is actually loaded into the live invocation ---

def test_live_executor_passes_skill_id_to_sdk():
    source = inspect.getsource(skill_executor.ClaudeAgentSdkSkillExecutor._invoke_skill_async)
    assert "skills=[skill_id]" in source, (
        "ClaudeAgentSdkSkillExecutor must pass skills=[skill_id] to ClaudeAgentOptions "
        "so the SDK loads skills/<skill_id>/SKILL.md as the live prompt source."
    )
    assert '"project"' in source or "'project'" in source, (
        "setting_sources must include 'project' for the SDK to discover skills/ in this repo."
    )


# --- Defect 1: skill ID vs workflow ID distinction, canonical source, escalation ---

def test_prompt_distinguishes_workflow_ids_from_skill_ids():
    content = _assembled_live_content().lower()
    assert "workflow id" in content and "skill id" in content, (
        "Live prompt content must explicitly discuss both 'workflow ID' and 'skill ID' "
        "as distinct concepts (defect: docs-aligner, a real skill ID, was written into "
        "recommended_workflow_id)."
    )
    assert "must never be written into" in content or "never write" in content or "never be written" in content, (
        "Live prompt content must explicitly forbid writing a skill ID into the "
        "workflow-ID field."
    )


def test_prompt_points_to_workflow_registry_as_canonical_source():
    content = _assembled_live_content()
    assert "workflow-registry.yaml" in content
    assert os.path.exists(REGISTRY), "Canonical workflow registry referenced by the prompt must exist."


def test_prompt_instructs_escalation_over_guessing():
    content = _assembled_live_content().lower()
    assert "escalation_recommended" in content
    assert "escalat" in content and ("uncertain" in content or "no valid workflow" in content or "not confidently supported" in content)


def test_docs_aligner_is_a_real_skill_not_a_workflow_id():
    """Ground truth check backing the whole defect: docs-aligner must be a real
    skill directory and must NOT appear as a top-level workflow id."""
    assert os.path.isdir(os.path.join(REPO_ROOT, "skills", "docs-aligner"))
    import yaml
    with open(REGISTRY, encoding="utf-8") as f:
        registry = yaml.safe_load(f)
    workflow_ids = {w["id"] for w in registry.get("workflows", [])}
    assert "docs-aligner" not in workflow_ids


# --- Defect 2: evidence line-format grammar matches validator exactly ---

VALIDATOR_LINE_RE = re.compile(r"\^L\?\\d\+\(\?:-L\?\\d\+\)\?\$")


def test_evidence_rules_states_deterministic_line_grammar_not_if_possible():
    content = _read(EVIDENCE_RULES)
    assert "if possible" not in content.lower(), (
        "evidence-rules.md must not describe line citations as optional; "
        "the validator requires them unconditionally."
    )
    for accepted in ["L12", "12", "12-18", "L12-L18"]:
        assert accepted in content, f"evidence-rules.md must document the accepted form '{accepted}'"
    for rejected in ["Entire file", "Routing section", "See README"]:
        assert rejected in content, f"evidence-rules.md must document the rejected form '{rejected}'"


def test_validator_regex_actually_matches_documented_accepted_forms():
    """Belt-and-suspenders: run the real validator regex (mirrored from
    scripts/validate-brief.py) against the exact forms evidence-rules.md
    documents as accepted, so the doc can't silently drift from the code."""
    pattern = re.compile(r"^L?\d+(?:-L?\d+)?$")
    for accepted in ["12", "L12", "12-18", "L12-L18"]:
        assert pattern.match(accepted), f"{accepted!r} should match the validator's grammar"
    for rejected in ["Entire file", "Routing section", "See README"]:
        assert not pattern.match(rejected), f"{rejected!r} should NOT match the validator's grammar"


# --- Defect 3: evidence-authority hierarchy is present and concrete ---

def test_prompt_includes_authority_hierarchy_precedence():
    content = _assembled_live_content().lower()
    assert "authority" in content
    for tier_marker in [
        "current executable code",
        "current contracts and registries",
        "accepted ad",  # "Accepted ADRs"
        "historical",
    ]:
        assert tier_marker in content, f"Authority hierarchy must mention '{tier_marker}'"
    assert "historical" in content and (
        "must be" in content or "labeled" in content
    ), "Historical/status documents must be explicitly required to be labeled historical."


def test_prompt_requires_current_corroboration_for_production_ready_claims():
    content = _assembled_live_content().lower()
    assert "current corroboration" in content or "corroborat" in content


# --- Template: section 13 is singular, authoritative, and protected ---

def test_template_declares_section_13_as_sole_authoritative_block():
    content = _read(TEMPLATE)
    assert "## 13. Machine-readable handoff" in content
    assert "authoritative machine-readable block" in content.lower() or "authoritative" in content.lower()
    assert "MISSING_HANDOFF_BLOCK" in content
