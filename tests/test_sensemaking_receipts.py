"""Session and semantic query receipts (proposed ADR 0032).

Covers the validator against its fixtures, real whole-file YAML receipts,
router and CLI dispatch, the session-start summarizer, the declared contracts,
the Skill guidance that writes and reads receipts, exclusion from the semantic
knowledge index, and the receipts committed in this repository.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "tests" / "fixtures" / "validate-receipt"
RECEIPTS = ROOT / ".sensemaking" / "receipts"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


validator = _load("validate_receipt", "validate-receipt.py")
summarizer = _load("summarize_receipts", "summarize-receipts.py")


def _run(*args: str, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args], capture_output=True, text=True, cwd=ROOT, check=False, env=env,
    )


def _fixture_body(name: str) -> dict:
    data, problem = validator.load_receipt(FIXTURES / "valid" / name)
    assert data is not None, problem
    return data


def _write_receipt(directory: Path, data: dict, kind: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{data['session_ref']}.{kind}.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def _codes(path: Path, target_repo: Path | None = None) -> list[str]:
    _, checker = validator.validate_receipt(path, target_repo)
    return [f["code"] for f in checker.findings if f["severity"] == "error"]


# -- fixtures (same contract as scripts/test-validators.py) ----------------

FIXTURE_FILES = sorted(FIXTURES.glob("*/*.md"))


def test_fixture_directories_cover_both_cases():
    assert any(p.parent.name == "valid" for p in FIXTURE_FILES)
    assert any(p.parent.name == "invalid" for p in FIXTURE_FILES)


@pytest.mark.parametrize("fixture", FIXTURE_FILES, ids=lambda p: f"{p.parent.name}/{p.name}")
def test_fixture_outcome(fixture: Path):
    meta = yaml.safe_load(fixture.read_text(encoding="utf-8").split("---", 2)[1])
    result = _run(str(SCRIPTS / "validate-receipt.py"), str(fixture), "--repo-root", ".")
    if meta["validator_case"] == "positive":
        assert result.returncode == 0, result.stdout
        assert "RECEIPT_VALID" in result.stdout
    else:
        assert result.returncode == 1, result.stdout
        assert meta["expected_error_contains"] in result.stdout
        errors = [line for line in result.stdout.splitlines() if line.startswith("[RECEIPT_")]
        assert len(errors) == 1, f"negative fixture must fail for exactly one reason: {errors}"


# -- real YAML receipts ----------------------------------------------------

def test_yaml_receipt_must_be_named_after_session_ref(tmp_path: Path):
    data = _fixture_body("session-final-owner-stop.md")
    path = _write_receipt(tmp_path, data, "session")
    assert _codes(path) == []
    wrong = path.with_name("latest.session.yaml")
    path.rename(wrong)
    assert _codes(wrong) == ["RECEIPT_FILENAME"]


def test_target_repo_requires_referenced_artifacts_to_exist(tmp_path: Path):
    data = _fixture_body("session-final-owner-stop.md")
    path = _write_receipt(tmp_path / ".sensemaking" / "receipts", data, "session")
    assert _codes(path, tmp_path) == ["RECEIPT_REF_MISSING"]
    brief = tmp_path / "docs" / "briefs" / "export-endpoint-brief.md"
    brief.parent.mkdir(parents=True)
    brief.write_text("# brief\n", encoding="utf-8")
    assert _codes(path, tmp_path) == []


def test_in_progress_receipt_is_valid_but_flagged(tmp_path: Path):
    path = _write_receipt(tmp_path, _fixture_body("session-in-progress.md"), "session")
    _, checker = validator.validate_receipt(path)
    assert checker.valid
    assert "RECEIPT_NOT_FINAL" in {f["code"] for f in checker.findings}


def test_working_tree_only_persistence_warns(tmp_path: Path):
    data = _fixture_body("session-final-owner-stop.md")
    data["persistence"] = "working_tree_only"
    path = _write_receipt(tmp_path, data, "session")
    _, checker = validator.validate_receipt(path)
    assert checker.valid
    assert "RECEIPT_NOT_DURABLE" in {f["code"] for f in checker.findings}


@pytest.mark.parametrize("ref", [
    "/tmp/run/brief.md", "~/notes.md", "C:/work/brief.md", "file:docs/brief.md", "../outside.md",
])
def test_non_durable_references_rejected(tmp_path: Path, ref: str):
    data = _fixture_body("session-final-owner-stop.md")
    data["responsibilities"][0]["artifact_refs"] = [ref]
    path = _write_receipt(tmp_path, data, "session")
    assert _codes(path) == ["RECEIPT_NON_DURABLE_REF"]


def test_json_output_is_router_envelope_and_ascii(tmp_path: Path):
    data = _fixture_body("session-final-owner-stop.md")
    data["goal"]["statement"] = "Decide \u2014 with care \u2014 how to retire it."
    path = _write_receipt(tmp_path, data, "session")
    result = _run(str(SCRIPTS / "validate-receipt.py"), str(path), "--json")
    assert result.returncode == 0
    result.stdout.encode("ascii")
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["artifact_id"] == "sensemaking_session_receipt"
    assert isinstance(payload["errors"], list)


# -- router and CLI --------------------------------------------------------

def test_router_dispatches_yaml_receipts(tmp_path: Path):
    good = _write_receipt(tmp_path, _fixture_body("query-recall-with-miss.md"), "query")
    result = _run(str(SCRIPTS / "validate-and-report.py"), str(good), "--repo-root", str(ROOT))
    payload = json.loads(result.stdout)
    assert result.returncode == 0, result.stdout
    assert payload["validator"] == "validate-receipt.py"
    assert payload["artifact_id"] == "semantic_query_receipt"

    bad_data = _fixture_body("query-recall-with-miss.md")
    bad_data["misses"] = []
    bad = _write_receipt(tmp_path / "bad", bad_data, "query")
    result = _run(str(SCRIPTS / "validate-and-report.py"), str(bad), "--repo-root", str(ROOT))
    payload = json.loads(result.stdout)
    assert result.returncode == 1
    assert payload["valid"] is False
    assert any(e["error_type"] == "RECEIPT_MISS_NOT_RECORDED" for e in payload["errors"])


def test_router_leaves_other_yaml_unrouted(tmp_path: Path):
    other = tmp_path / "probe-report.yaml"
    other.write_text("artifact_id: something_else\nschema_version: 1\n", encoding="utf-8")
    result = _run(str(SCRIPTS / "validate-and-report.py"), str(other), "--repo-root", str(ROOT))
    payload = json.loads(result.stdout)
    assert result.returncode == 2
    assert payload["validator"] == "validate-and-report.py"


def test_installed_cli_validate_accepts_receipts(tmp_path: Path):
    path = _write_receipt(tmp_path, _fixture_body("session-final-owner-stop.md"), "session")
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    result = _run("-m", "sensemaking_skills.cli", "validate", "--artifact", str(path),
                  "--repo-root", str(ROOT), "--json", env=env)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["valid"] is True


# -- summarizer (the consumer) ---------------------------------------------

def test_summarizer_tracks_open_questions_tombstones_and_repeated_misses(tmp_path: Path):
    receipts = tmp_path / ".sensemaking" / "receipts"
    first = _fixture_body("session-final-owner-stop.md")
    _write_receipt(receipts, first, "session")
    first_query = _fixture_body("query-recall-with-miss.md")
    _write_receipt(receipts, first_query, "query")

    second_query = _fixture_body("query-recall-with-miss.md")
    second_query["session_ref"] = "2026-10-25-fixture-follow-up"
    _write_receipt(receipts, second_query, "query")

    crashed = _fixture_body("session-in-progress.md")
    crashed["session_ref"] = "2026-10-25-fixture-crashed"
    _write_receipt(receipts, crashed, "session")

    summary = summarizer.summarize(receipts)
    assert [q["ref"] for q in summary["open_questions"]] == ["2026-10-24-fixture-owner-stop#Q-1"]
    assert summary["next"]["blocked_on"] == ["Q-1", "authority:merge"]
    assert [u["receipt"] for u in summary["unfinished"]] == ["2026-10-25-fixture-crashed.session.yaml"]
    repeated = {m["key"]: m["sessions"] for m in summary["repeated_misses"]}
    assert repeated["subject:cap:export"] == ["2026-10-24-fixture-owner-stop", "2026-10-25-fixture-follow-up"]
    assert len(summary["pending_misses"]) == 2

    resolver = _fixture_body("session-final-owner-stop.md")
    resolver.update(session_ref="2026-10-26-fixture-resolution", open_questions=[], findings=[])
    resolver["updated_at"] = "2026-10-26T12:00:00Z"
    resolver["continuity"]["resolves_questions"] = ["2026-10-24-fixture-owner-stop#Q-1"]
    resolver["stop"] = {"disposition": "GOAL_SATISFIED", "reason": "Owner chose deprecation; implemented."}
    resolver["next"] = {"warranted_responsibility": None, "blocked_on": []}
    _write_receipt(receipts, resolver, "session")
    summary = summarizer.summarize(receipts)
    assert summary["open_questions"] == []
    assert summary["next"]["from_session"] == "2026-10-26-fixture-resolution"


def test_summarizer_reports_invalid_receipts_and_exit_code(tmp_path: Path):
    receipts = tmp_path / ".sensemaking" / "receipts"
    data = _fixture_body("session-final-owner-stop.md")
    data["action_authorized_by_receipt"] = True
    _write_receipt(receipts, data, "session")
    result = _run(str(SCRIPTS / "summarize-receipts.py"), "--repo", str(tmp_path))
    assert result.returncode == 1
    assert "INVALID RECEIPTS" in result.stdout
    result.stdout.encode("ascii")
    empty = _run(str(SCRIPTS / "summarize-receipts.py"), "--repo", str(tmp_path / "none"))
    assert empty.returncode == 0
    assert "0 valid, 0 invalid" in empty.stdout


# -- contracts and guidance -------------------------------------------------

def test_receipt_contracts_declared():
    contracts = yaml.safe_load(
        (ROOT / "skills/workflow-planner/references/artifact-contracts.yaml").read_text(encoding="utf-8")
    )
    entries = {a["id"]: a for a in contracts["artifacts"]}
    vocabulary = yaml.safe_load((ROOT / "docs/canonical-vocabulary.yaml").read_text(encoding="utf-8"))
    vocab_ids = {a["id"] for a in vocabulary["artifact_ids"]}
    expected = {
        "sensemaking_session_receipt": ("using-sensemaking", ".session.yaml"),
        "semantic_query_receipt": ("repository-semantic-steward", ".query.yaml"),
    }
    for artifact_id, (producer, suffix) in expected.items():
        entry = entries[artifact_id]
        assert entry["produced_by"] == producer
        assert entry["path"] == f".sensemaking/receipts/{{session_id}}{suffix}"
        assert entry["verification"]["generic_validator"] == "python scripts/validate-receipt.py {artifact_path}"
        assert (ROOT / entry["schema_reference"]).is_file()
        assert artifact_id in vocab_ids
        assert validator.FILE_SUFFIX[artifact_id] == suffix


def test_skill_guidance_writes_and_reads_receipts():
    control = (ROOT / "skills/using-sensemaking/SKILL.md").read_text(encoding="utf-8")
    steward = (ROOT / "skills/repository-semantic-steward/SKILL.md").read_text(encoding="utf-8")
    recall = (ROOT / "skills/repository-semantic-steward/references/recall.md").read_text(encoding="utf-8")
    reconcile = (ROOT / "skills/repository-semantic-steward/references/reconciliation.md").read_text(encoding="utf-8")
    for needle in ("references/session-receipt-v1.md", "scripts/summarize-receipts.py",
                   ".sensemaking/receipts/", "working_tree_only"):
        assert needle in control
    assert "(references/query-receipt.md)" in steward
    assert "query-receipt.md" in recall
    assert "summarize-receipts.py" in reconcile


def test_reference_docs_list_every_enforced_enum():
    session_doc = (ROOT / "skills/using-sensemaking/references/session-receipt-v1.md").read_text(encoding="utf-8")
    query_doc = (ROOT / "skills/repository-semantic-steward/references/query-receipt.md").read_text(encoding="utf-8")
    for value in (*validator.STOP_DISPOSITIONS, *validator.AUTHORITY, *validator.PERSISTENCE,
                  *validator.RESPONSIBILITY_STATUS, *validator.EPISTEMIC_STATUS):
        assert value in session_doc, value
    for value in (*validator.STEWARD_MODES, *validator.QUERY_OPERATIONS, *validator.QUERY_OUTCOMES,
                  *validator.MISS_KINDS, *validator.MISS_FOLLOW_UPS, *validator.RECONCILE_DISPOSITIONS):
        assert value in query_doc, value


def test_receipts_are_not_ingested_as_knowledge(tmp_path: Path):
    from sensemaking_skills.semantic_architecture import knowledge_sources

    receipt = tmp_path / ".sensemaking" / "receipts" / "2026-10-24-x.session.yaml"
    receipt.parent.mkdir(parents=True)
    receipt.write_text("artifact_id: sensemaking_session_receipt\n", encoding="utf-8")
    tracked = {".sensemaking/receipts/2026-10-24-x.session.yaml"}
    assert knowledge_sources._grounding_claims(tmp_path, tracked) == []
    assert knowledge_sources._authored_records(tmp_path, tracked) == ([], [])


# -- receipts committed in this repository ----------------------------------

def test_repository_receipts_validate_against_this_repository():
    files = sorted(RECEIPTS.glob("*.yaml"))
    assert files, "this repository records its own sessions"
    for path in files:
        artifact_id, checker = validator.validate_receipt(path, ROOT)
        assert checker.valid, (path.name, checker.findings)
        assert artifact_id in validator.RECEIPT_ARTIFACT_IDS
