from pathlib import Path
from scripts.repo_probes import append_probe_section


def test_append_probe_section_adds_report(tmp_path: Path) -> None:
    report = tmp_path / "probe-report.yaml"
    report.write_text("schema_version: 1\n", encoding="utf-8")
    parts: list[str] = ["## Skill Definition", "body"]
    append_probe_section(parts, report)
    joined = "\n".join(parts)
    assert "## Repository Probe Report" in joined
    assert "schema_version: 1" in joined


def test_append_probe_section_skips_missing_report(tmp_path: Path) -> None:
    parts: list[str] = ["## Skill Definition", "body"]
    append_probe_section(parts, tmp_path / "missing.yaml")
    assert len(parts) == 2
