from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "using-sensemaking" / "SKILL.md"
REFERENCE = (
    ROOT
    / "skills"
    / "using-sensemaking"
    / "references"
    / "delegated-goal-patterns.md"
)


def _frontmatter(text: str) -> dict[str, object]:
    assert text.startswith("---\n")
    _, raw, _ = text.split("---", 2)
    data = yaml.safe_load(raw)
    assert isinstance(data, dict)
    return data


def test_using_sensemaking_frontmatter_is_skill_contract_minimal() -> None:
    text = SKILL.read_text(encoding="utf-8")
    metadata = _frontmatter(text)

    assert set(metadata) == {"name", "description"}
    assert metadata["name"] == "using-sensemaking"
    description = str(metadata["description"]).lower()
    assert "broad delegated repository mission" in description
    assert "authority" in description


def test_using_sensemaking_teaches_bounded_terminal_missions() -> None:
    text = SKILL.read_text(encoding="utf-8")
    reference = REFERENCE.read_text(encoding="utf-8")
    getting_started = (ROOT / "GETTING_STARTED.md").read_text(encoding="utf-8")

    assert "Broad delegated repository missions" in text
    assert "references/delegated-goal-patterns.md" in text

    assert "high delegation != unlimited scope" in reference
    assert "desired delegation != granted authority" in reference
    assert "Complete authoritative product scope" in reference
    assert "Stop conditions:" in reference

    assert "Delegate a complete repository mission" in getting_started
    assert "Desired delegation does not expand granted authority" in getting_started
    assert "no further repository change is warranted" in getting_started


def test_bootstrap_hook_does_not_expect_noncontract_skill_frontmatter() -> None:
    hook = (ROOT / ".claude" / "hooks" / "sessionstart.md").read_text(
        encoding="utf-8"
    )

    assert "frontmatter fields: name and description" in hook
    assert "description, tags" not in hook
