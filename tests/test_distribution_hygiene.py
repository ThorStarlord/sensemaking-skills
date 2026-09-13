from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_custom_build_hook_excludes_interpreter_cache_files() -> None:
    setup = (ROOT / "setup.py").read_text(encoding="utf-8")
    manifest = (ROOT / "MANIFEST.in").read_text(encoding="utf-8")

    assert "ignore_patterns(\"__pycache__\", \"*.py[cod]\")" in setup
    assert "global-exclude *.py[cod]" in manifest
    assert "prune __pycache__" in manifest

