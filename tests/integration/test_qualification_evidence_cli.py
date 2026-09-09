"""CLI qualification evidence smoke and rejection tests."""

from __future__ import annotations

import shutil
from pathlib import Path

from sensemaking_skills.qualification_evidence import main

_FIXTURE = Path(__file__).parents[1] / "fixtures" / "external_golden_path" / "pass"


def test_cli_writes_and_verifies_receipt(tmp_path: Path, capsys) -> None:
    output = tmp_path / "receipt.json"

    assert main([str(_FIXTURE), "--output", str(output)]) == 0
    assert "QUALIFICATION_EVIDENCE_RECEIPT_WRITTEN" in capsys.readouterr().out
    assert output.is_file()

    assert main([str(_FIXTURE), "--verify", str(output)]) == 0
    assert "QUALIFICATION_EVIDENCE_RECEIPT_VALID" in capsys.readouterr().out


def test_cli_rejects_invalid_attempt_without_writing_receipt(tmp_path: Path, capsys) -> None:
    attempt = tmp_path / "attempt"
    shutil.copytree(_FIXTURE, attempt)
    with (attempt / "evidence" / "lifecycle.txt").open("a", encoding="utf-8") as handle:
        handle.write("tampered\n")
    output = tmp_path / "receipt.json"

    assert main([str(attempt), "--output", str(output)]) == 2
    assert "QUALIFICATION_EVIDENCE_RECEIPT_INVALID" in capsys.readouterr().out
    assert not output.exists()
