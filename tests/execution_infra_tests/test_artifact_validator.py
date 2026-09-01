"""CampaignBriefValidator tests (Phase 6 correction, #122).

The validator delegates to the PINNED canonical ``validate-brief.py`` and
classifies its error codes into structural / substantive / environmental
categories so the execution report can emit separate pass rates. The
happy path uses a genuinely VALID brief (built from the framework's own
runtime skeleton) validated against a real target checkout.
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sensemaking_skills.exploratory_execution import CampaignBriefValidator

REPO_ROOT = Path(__file__).resolve().parents[2]


class _TargetRepo:
    def __init__(self, tmp_path: Path):
        self.path = tmp_path / "target"
        self.path.mkdir()
        subprocess.run(["git", "init", "-q", str(self.path)], check=True)
        subprocess.run(
            ["git", "-C", str(self.path), "config", "user.email", "t@e.i"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.path), "config", "user.name", "T"], check=True
        )
        self.source = self.path / "src" / "main.py"
        self.source.parent.mkdir(parents=True)
        self.source.write_text(
            "def analyze(repo):\n    return 'diagnosis'\n", encoding="utf-8"
        )
        subprocess.run(
            ["git", "-C", str(self.path), "add", "."], check=True
        )
        subprocess.run(
            ["git", "-C", str(self.path), "commit", "-q", "-m", "init"], check=True
        )


def _build_valid_brief(target: _TargetRepo) -> str:
    """A brief that passes the pinned canonical validator: complete handoff
    block, logic trace, grounded evidence excerpt, registry-valid workflow
    id and weakness type, built on the framework's own runtime skeleton."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import brief_skeleton

    text = brief_skeleton.build_skeleton()

    # Evidence excerpt with a VERBATIM quote from the target repo.
    quote = "    return 'diagnosis'"
    excerpts = (
        "```yaml\n"
        "evidence_excerpts:\n"
        "  - file: src/main.py\n"
        "    lines: L2\n"
        f"    quote: \"{quote}\"\n"
        "    supports_claim: \"Confirms the analysis entry point.\"\n"
        "```\n"
    )
    start = text.index("<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->")
    end = text.index("<!-- MODEL_SECTION:evidence_excerpts:END -->")
    text = (
        text[:start]
        + "<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->\n"
        + excerpts
        + "<!-- MODEL_SECTION:evidence_excerpts:END -->"
        + text[end + len("<!-- MODEL_SECTION:evidence_excerpts:END -->"):]
    )

    # Logic-trace paragraph in the evidence prose.
    text = text.replace(
        "<!-- REQUIRED: this section's prose must include a paragraph",
        (
            "Logic trace: the evidence excerpt confirms the target's "
            "analysis entry point exists, which grounds the diagnosis "
            "below.\n\n"
            "<!-- REQUIRED: this section's prose must include a paragraph"
        ),
        1,
    )
    # Weakest-boundary prose names the weakness type.
    text = text.replace(
        "## 6. Weakest boundary\n\n",
        "## 6. Weakest boundary\n\nThe weakest boundary is Vocabulary Drift.\n\n",
        1,
    )

    # Fill the Section 13 handoff YAML model fields.
    text = text.replace(
        "user_implied_fog_type:  # model fills: product_fog | ui_fog | docs_fog | architecture_fog | unknown",
        "user_implied_fog_type: unknown",
    )
    text = text.replace(
        "primary_fog_type:  # model fills: product_fog | ui_fog | docs_fog | architecture_fog",
        "primary_fog_type: architecture_fog",
    )
    text = text.replace(
        "diagnosis_conflict:  # model fills: true | false",
        "diagnosis_conflict: false",
    )
    text = text.replace(
        "escalation_recommended:  # model fills: true | false",
        "escalation_recommended: false",
    )
    text = text.replace(
        "evidence: []  # model fills: list of \"path/to/file (lines Lx-Ly): citation\"",
        'evidence:\n  - "src/main.py (lines L2): analysis entry point"',
    )
    text = text.replace(
        "recommended_workflow_id:  # model fills: MUST match an id in workflow-registry.yaml",
        "recommended_workflow_id: fast-path-workflow",
    )
    text = text.replace(
        "recommended_execution_mode:  # model fills: plan_only | guided_execution",
        "recommended_execution_mode: plan_only",
    )
    text = text.replace(
        "weakest_boundary:  # model fills: short slug",
        "weakest_boundary: vocabulary-drift",
    )
    text = text.replace(
        "weakness_type:  # model fills: one of the registered types in "
        "skills/repo-sensemaker/references/weakness-types.md, or 'Other'",
        "weakness_type: Vocabulary Drift",
    )
    return text


def _validator(tmp_path: Path) -> CampaignBriefValidator:
    return CampaignBriefValidator(
        framework_checkout=REPO_ROOT,
        target_checkout=_TargetRepo(tmp_path).path,
    )


def test_valid_brief_passes_with_full_rates(tmp_path: Path) -> None:
    target = _TargetRepo(tmp_path)
    validator = CampaignBriefValidator(
        framework_checkout=REPO_ROOT, target_checkout=target.path
    )
    outcome = validator(_build_valid_brief(target).encode("utf-8"))
    assert outcome.passed is True, outcome.details
    assert outcome.details["structural"] == {"passed": 1, "total": 1, "errors": []}
    assert outcome.details["substantive"] == {"passed": 1, "total": 1, "errors": []}
    assert outcome.details["environmental"] == []
    assert outcome.artifact_content is not None
    assert "```yaml" in outcome.artifact_content


def test_no_yaml_fails_fast_with_structural_error(tmp_path: Path) -> None:
    validator = _validator(tmp_path)
    outcome = validator(b"this response contains no YAML handoff block")
    assert outcome.passed is False
    assert outcome.details["structural"]["errors"] == ["MISSING_HANDOFF_BLOCK"]
    assert outcome.details["structural"]["passed"] == 0
    # The raw response is still preserved as the artifact content.
    assert outcome.artifact_content == (
        "this response contains no YAML handoff block"
    )


def test_no_logic_trace_is_classified_substantive(tmp_path: Path) -> None:
    target = _TargetRepo(tmp_path)
    validator = CampaignBriefValidator(
        framework_checkout=REPO_ROOT, target_checkout=target.path
    )
    brief = _build_valid_brief(target).replace("Logic trace:", "Observations:")
    outcome = validator(brief.encode("utf-8"))
    assert outcome.passed is False
    assert "NO_LOGIC_TRACE" in outcome.details["substantive"]["errors"]
    assert outcome.details["substantive"]["passed"] == 0


def test_hallucinated_citation_is_classified_substantive(tmp_path: Path) -> None:
    target = _TargetRepo(tmp_path)
    validator = CampaignBriefValidator(
        framework_checkout=REPO_ROOT, target_checkout=target.path
    )
    brief = _build_valid_brief(target).replace(
        "file: src/main.py", "file: src/does-not-exist.py"
    )
    outcome = validator(brief.encode("utf-8"))
    assert outcome.passed is False
    errors = outcome.details["substantive"]["errors"]
    assert any("HALLUCINATED" in e for e in errors), errors


def test_malformed_handoff_fence_is_classified_structural(tmp_path: Path) -> None:
    target = _TargetRepo(tmp_path)
    validator = CampaignBriefValidator(
        framework_checkout=REPO_ROOT, target_checkout=target.path
    )
    brief = _build_valid_brief(target).replace(
        "```yaml\nartifact_id: repository_sensemaking_brief",
        "```\nartifact_id: repository_sensemaking_brief",
    )
    outcome = validator(brief.encode("utf-8"))
    assert outcome.passed is False
    errors = outcome.details["structural"]["errors"]
    assert errors, "expected at least one structural error"
