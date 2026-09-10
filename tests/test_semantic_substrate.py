"""Contracts for the build-first Semantic Architecture substrate."""

from __future__ import annotations

import json

from sensemaking_skills.semantic_architecture import (
    Completeness,
    SemanticObservation,
    SemanticStateEntry,
    SemanticStateStore,
    build_repository_semantic_map,
    probe_exact_search,
    probe_manifest_dependencies,
    probe_python_imports,
    to_dict,
)


def test_python_import_probe_reports_syntax_without_architecture_judgment(tmp_path):
    (tmp_path / "app.py").write_text("import json\nfrom pkg import thing\n", encoding="utf-8")
    result = probe_python_imports(tmp_path, target_ref="sha:abc")

    assert result.completeness is Completeness.COMPLETE
    assert {item.object for item in result.observations} == {"json", "pkg"}
    assert all(item.predicate == "contains_import_syntax" for item in result.observations)
    encoded = json.dumps(to_dict(result)).lower()
    assert "architecture_violation" not in encoded
    assert '"semantic_truth_established": false' in encoded


def test_python_import_probe_becomes_partial_on_parse_failure(tmp_path):
    (tmp_path / "good.py").write_text("import os\n", encoding="utf-8")
    (tmp_path / "bad.py").write_text("def nope(:\n", encoding="utf-8")
    result = probe_python_imports(tmp_path, target_ref="sha:abc")

    assert result.completeness is Completeness.PARTIAL
    assert "PYTHON_IMPORT_PARSE_FAILED" in {item.code for item in result.diagnostics}


def test_manifest_probe_reads_supported_dependency_fields(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname="demo"\nversion="0.1"\ndependencies=["click>=8"]\n',
        encoding="utf-8",
    )
    result = probe_manifest_dependencies(tmp_path, target_ref="sha:manifest")

    assert any(item.object == "click>=8" for item in result.observations)
    assert all(item.predicate == "declares_dependency" for item in result.observations)


def test_exact_search_zero_is_bounded_to_declared_utf8_scope(tmp_path):
    (tmp_path / "a.txt").write_text("alpha\n", encoding="utf-8")
    result = probe_exact_search(tmp_path, target_ref="sha:search", pattern="missing")

    summary = result.observations[-1]
    assert summary.object == "0"
    assert "UTF-8" in summary.scope
    assert "generated/vendor roots excluded" in summary.scope
    assert result.semantic_truth_established is False


def test_semantic_map_rejects_mixed_target_observations(tmp_path):
    first = probe_exact_search(tmp_path, target_ref="sha:a", pattern="x").observations
    try:
        build_repository_semantic_map(
            map_id="MAP-1",
            target_ref="sha:b",
            observations=first,
        )
    except ValueError as exc:
        assert "target_ref" in str(exc)
    else:
        raise AssertionError("map accepted observations from a different target")


def test_semantic_map_marks_relations_derived_and_explicitly_incomplete(tmp_path):
    (tmp_path / "a.txt").write_text("needle\n", encoding="utf-8")
    observations = probe_exact_search(
        tmp_path,
        target_ref="sha:a",
        pattern="needle",
    ).observations
    semantic_map = build_repository_semantic_map(
        map_id="MAP-2",
        target_ref="sha:a",
        observations=observations,
        claim_refs=("CLAIM-1",),
    )

    assert semantic_map.relations
    assert all(item.epistemic_status == "DERIVED" for item in semantic_map.relations)
    assert semantic_map.semantic_truth_established is False
    assert any("absence" in item for item in semantic_map.explicit_limits)


def test_cross_skill_semantic_state_is_hash_chained_and_tamper_evident(tmp_path):
    path = tmp_path / "semantic-state.jsonl"
    store = SemanticStateStore(path)
    first_digest = store.append(
        SemanticStateEntry(
            entry_id="S1",
            source_skill="repo-sensemaker",
            artifact_ref="brief.md",
            target_ref="sha:a",
            claim_refs=("C1",),
        )
    )
    second_digest = store.append(
        SemanticStateEntry(
            entry_id="S2",
            source_skill="architectural-review",
            artifact_ref="review.md",
            target_ref="sha:a",
            parent_entry_ids=("S1",),
        )
    )
    assert first_digest != second_digest
    assert store.validate() == ()

    lines = path.read_text(encoding="utf-8").splitlines()
    record = json.loads(lines[0])
    record["entry"]["artifact_ref"] = "tampered.md"
    lines[0] = json.dumps(record, sort_keys=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    codes = {item.code for item in store.validate()}
    assert "SEMANTIC_STATE_DIGEST_MISMATCH" in codes


def test_cross_skill_semantic_state_rejects_future_parent(tmp_path):
    store = SemanticStateStore(tmp_path / "state.jsonl")
    try:
        store.append(
            SemanticStateEntry(
                entry_id="S2",
                source_skill="architectural-review",
                artifact_ref="review.md",
                target_ref="sha:a",
                parent_entry_ids=("S1",),
            )
        )
    except ValueError as exc:
        assert "parent" in str(exc)
    else:
        raise AssertionError("state log accepted a parent that does not exist")
