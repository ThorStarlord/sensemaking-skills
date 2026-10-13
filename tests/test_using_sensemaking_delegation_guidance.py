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


def test_using_sensemaking_links_delegated_goal_patterns_reference() -> None:
    text = SKILL.read_text(encoding="utf-8")

    assert REFERENCE.exists()
    assert "references/delegated-goal-patterns.md" in text
