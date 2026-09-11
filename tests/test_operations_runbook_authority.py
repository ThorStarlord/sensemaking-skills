from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_current_operations_runbook_is_explicit_and_complete_enough_for_navigation() -> None:
    runbook = _read("docs/operations-runbook.md")

    assert "**Status:** current operator-facing operations/qualification runbook" in runbook
    assert ".github/workflows/validation.yml" in runbook
    assert ".github/workflows/lab-validation.yml" in runbook
    assert ".github/workflows/release-candidate.yml" in runbook
    assert "python scripts/validate-strategic-state.py --repo-root ." in runbook
    assert "tests/test_semantic_reference_audit.py" in runbook
    assert "tests/test_strategic_state_validation.py" in runbook
    assert "local reproduction != hosted cross-platform CI proof" in runbook


def test_readme_and_context_point_to_current_operations_runbook() -> None:
    readme = _read("README.md")
    context = _read("CONTEXT.md")

    assert "`docs/operations-runbook.md` — current operator-facing operations and qualification runbook" in readme
    assert "use `docs/operations-runbook.md`" in readme
    assert "`docs/operations-runbook.md` | current operator-facing local validation/qualification/Campaign/release runbook" in context


def test_milestone_runbooks_are_historical_not_current_authority() -> None:
    milestone = _read("docs/milestone-runbook.md")
    post_milestone = _read("docs/post-milestone-handoff-runbook.md")

    for text in (milestone, post_milestone):
        assert "**not current operational authority**" in text
        assert "docs/operations-runbook.md" in text
        assert "post-milestone operational source of truth" not in text


def test_outer_loop_v0_is_frozen_as_operational_baseline() -> None:
    control_model = _read("docs/strategic-outer-loop.md")
    audit = _read("docs/strategic-repository-evolution-audit-2026-09-11.md")

    assert "**Version:** v0" in control_model
    assert "frozen operational baseline" in control_model
    assert "OUTER_LOOP_V0 = FROZEN_OPERATIONAL_BASELINE" in audit
