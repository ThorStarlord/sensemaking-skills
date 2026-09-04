"""PF-1 regression contract: `user_implied_fog_type` legal-value agreement.

Goal A (evidence 0024) found a deterministic Contract Mismatch: the canonical
producer surfaces (`skills/repo-sensemaker/references/repo-analysis-template.md`,
`scripts/brief_skeleton.py`) and the runtime's authoritative brief validator
(`scripts/validate-brief.py`) all treat `user_implied_fog_type: unknown` as legal,
but the generic artifact validator (`scripts/validate-artifact.py`) rejected it
with INVALID_ENUM_VALUE in 3 of 4 valid external episodes.

`user_implied_fog_type` characterises what the user's *stated intent* implies -- an
input, not the diagnosis. `unknown` means the intent is fog-neutral (implies no
particular fog type) and is legal for THIS field only. `primary_fog_type` is the
diagnosis and is always one of the four canonical fog types -- `unknown` stays
illegal there.

These tests pin the reconciled contract across every relevant surface.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
BASE_BRIEF = REPO_ROOT / "tests" / "fixtures" / "validate-brief" / "valid" / "valid-brief.md"

CANONICAL_FOUR = {"product_fog", "ui_fog", "architecture_fog", "docs_fog"}
USER_IMPLIED_LEGAL = CANONICAL_FOUR | {"unknown"}


def _run(script: str, *args: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args, "--repo-root", str(REPO_ROOT)],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _write_brief(tmp_path: Path, *, user_implied: str | None, primary: str = "architecture_fog") -> str:
    """Return a path to valid-brief.md with the Section 13 fog fields set."""
    text = BASE_BRIEF.read_text(encoding="utf-8")
    text = text.replace(
        "primary_fog_type: architecture_fog",
        f"primary_fog_type: {primary}",
        1,
    )
    if user_implied is not None:
        text = text.replace(
            f"primary_fog_type: {primary}",
            f"primary_fog_type: {primary}\nuser_implied_fog_type: {user_implied}",
            1,
        )
    dest = tmp_path / "brief.md"
    dest.write_text(text, encoding="utf-8")
    return str(dest)


def _machine_readable_artifact(tmp_path: Path, *, primary: str, user_implied: str) -> str:
    dest = tmp_path / "artifact.md"
    dest.write_text(
        "# Artifact\n\n## Machine Readable\n\n"
        "```yaml\n"
        "artifact_id: repository_sensemaking_brief\n"
        f"primary_fog_type: {primary}\n"
        f"user_implied_fog_type: {user_implied}\n"
        "```\n",
        encoding="utf-8",
    )
    return str(dest)


# --------------------------------------------------------------------------- #
# Canonical vocabulary: single source of truth for the field's legal domain
# --------------------------------------------------------------------------- #

def _load_vocab(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_canonical_vocabulary_declares_user_implied_fog_type_domain():
    """docs/canonical-vocabulary.yaml must declare user_implied_fog_type's legal
    values as exactly the four canonical fog types plus `unknown`."""
    vocab = _load_vocab(REPO_ROOT / "docs" / "canonical-vocabulary.yaml")
    routing_fields = {f["field"]: f for f in vocab.get("routing_fields", [])}
    assert "user_implied_fog_type" in routing_fields, (
        "user_implied_fog_type has no routing_fields declaration in "
        "docs/canonical-vocabulary.yaml -- the two validators cannot share a "
        "source of truth for its legal domain."
    )
    values = set(routing_fields["user_implied_fog_type"].get("values", []))
    assert values == USER_IMPLIED_LEGAL, (
        f"user_implied_fog_type.values is {sorted(values)}, expected "
        f"{sorted(USER_IMPLIED_LEGAL)} (the four canonical fog types + unknown)."
    )


def test_primary_fog_type_domain_excludes_unknown():
    """The diagnosis field must NOT gain `unknown` as a side effect of the fix."""
    vocab = _load_vocab(REPO_ROOT / "docs" / "canonical-vocabulary.yaml")
    routing_fields = {f["field"]: f for f in vocab.get("routing_fields", [])}
    values = set(routing_fields["primary_fog_type"].get("values", []))
    assert values == CANONICAL_FOUR, (
        f"primary_fog_type.values is {sorted(values)}; `unknown` must never be legal "
        "for the diagnosis field."
    )


def test_packaged_vocabulary_mirror_still_matches():
    """The packaged default vocab must stay a byte-for-byte mirror of the docs one."""
    docs = (REPO_ROOT / "docs" / "canonical-vocabulary.yaml").read_bytes()
    packaged = (
        REPO_ROOT / "src" / "sensemaking_skills" / "defaults" / "canonical-vocabulary.yaml"
    ).read_bytes()
    assert docs == packaged, "packaged canonical-vocabulary mirror drifted from docs/"


# --------------------------------------------------------------------------- #
# validate-artifact.py (generic validator / validate-output.py stack)
# --------------------------------------------------------------------------- #

def test_validate_artifact_accepts_user_implied_fog_type_unknown(tmp_path):
    """The exact Goal-A-observed case: user_implied_fog_type: unknown must pass."""
    brief = _write_brief(tmp_path, user_implied="unknown")
    code, out = _run("validate-artifact.py", "repository_sensemaking_brief", brief)
    assert code == 0, f"validate-artifact.py rejected a template-legal value:\n{out}"
    assert "user_implied_fog_type" not in out


def test_validate_artifact_accepts_user_implied_fog_type_canonical(tmp_path):
    brief = _write_brief(tmp_path, user_implied="docs_fog")
    code, out = _run("validate-artifact.py", "repository_sensemaking_brief", brief)
    assert code == 0, out


def test_validate_artifact_rejects_illegal_user_implied_fog_type(tmp_path):
    """Genuinely out-of-contract values still fail closed."""
    brief = _write_brief(tmp_path, user_implied="banana")
    code, out = _run("validate-artifact.py", "repository_sensemaking_brief", brief)
    assert code == 1
    assert "INVALID_ENUM_VALUE" in out
    assert "user_implied_fog_type" in out


def test_validate_artifact_still_rejects_primary_fog_type_unknown(tmp_path):
    """`unknown` must NOT become legal for the diagnosis field."""
    brief = _write_brief(tmp_path, user_implied="unknown", primary="unknown")
    code, out = _run("validate-artifact.py", "repository_sensemaking_brief", brief)
    assert code == 1
    assert "INVALID_ENUM_VALUE" in out
    assert "primary_fog_type" in out


# --------------------------------------------------------------------------- #
# validate-brief.py (runtime's authoritative path) -- guard against a future
# over-strict check being added
# --------------------------------------------------------------------------- #

def test_validate_brief_accepts_user_implied_fog_type_unknown(tmp_path):
    brief = _write_brief(tmp_path, user_implied="unknown")
    code, out = _run("validate-brief.py", brief)
    assert code == 0, f"validate-brief.py must accept user_implied_fog_type: unknown:\n{out}"


# --------------------------------------------------------------------------- #
# validate-fog-type-normalization.py
# --------------------------------------------------------------------------- #

def test_fog_normalization_accepts_user_implied_unknown(tmp_path):
    art = _machine_readable_artifact(tmp_path, primary="product_fog", user_implied="unknown")
    code, out = _run("validate-fog-type-normalization.py", art)
    assert code == 0, out
    assert "INVALID_FOG_TYPE" not in out


def test_fog_normalization_still_rejects_primary_unknown(tmp_path):
    art = _machine_readable_artifact(tmp_path, primary="unknown", user_implied="ui_fog")
    code, out = _run("validate-fog-type-normalization.py", art)
    assert code == 1
    assert "INVALID_FOG_TYPE" in out
