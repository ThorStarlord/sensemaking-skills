from pathlib import Path

import tomllib
import yaml


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_current_operations_runbook_is_explicit_and_complete_enough_for_navigation() -> None:
    runbook = _read("docs/operations-runbook.md")

    assert ".github/workflows/validation.yml" in runbook
    assert ".github/workflows/lab-validation.yml" in runbook
    assert ".github/workflows/release-candidate.yml" in runbook
    assert "python scripts/validate-strategic-state.py --repo-root ." in runbook
    assert "tests/test_semantic_reference_audit.py" in runbook
    assert "tests/test_strategic_state_validation.py" in runbook


def test_readme_and_context_point_to_current_operations_runbook() -> None:
    readme = _read("README.md")
    context = _read("CONTEXT.md")

    assert "docs/operations-runbook.md" in readme
    assert "docs/operations-runbook.md" in context


def test_milestone_runbooks_point_to_current_operations_runbook() -> None:
    milestone = _read("docs/milestone-runbook.md")
    post_milestone = _read("docs/post-milestone-handoff-runbook.md")

    for text in (milestone, post_milestone):
        assert "docs/operations-runbook.md" in text


def test_historical_v1_prd_is_not_current_repository_authority() -> None:
    prd = _read("docs/PRD-V1-Sensemaking.md")
    validator = _read("scripts/validate-repo.py")

    assert "<!-- doc-status: historical -->" in prd
    assert "docs/product-strategy.md" in prd
    assert "docs/adr/0029-current-product-boundary.md" in prd

    assert '"docs/PRD-V1-Sensemaking.md"' not in validator
    for authority in (
        "STATUS.md",
        "docs/product-strategy.md",
        "docs/adr/0029-current-product-boundary.md",
        "docs/operations-runbook.md",
    ):
        assert f'"{authority}"' in validator


def test_live_faq_uses_current_release_authority_without_historical_roadmap_claims() -> None:
    faq = _read("docs/FAQ.md")
    pyproject = tomllib.loads(_read("pyproject.toml"))
    contract = yaml.safe_load(_read("release-v1.0.yaml"))

    source_version = pyproject["project"]["version"]
    target_version = contract["release"]["version"]

    assert source_version in faq
    assert target_version in faq
    assert f"release phase:** {contract['release']['status']}" in faq.lower()
    assert "`docs/product-strategy.md`" in faq
    assert "`docs/operations-runbook.md`" in faq
