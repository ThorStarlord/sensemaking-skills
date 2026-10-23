"""Architecture and ontology vocabulary, version 2 (ADR 0033).

Version-2 constructs are accepted only from reviewed authored documents that
declare schema_version 2, must carry their typed attributes, and rule scopes
must resolve. Version-1 documents and the store version are unchanged.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from sensemaking_skills.semantic_architecture import knowledge, knowledge_sources
from sensemaking_skills.semantic_architecture.knowledge import (
    AUTHORED_SCHEMA_VERSIONS, SCHEMA_VERSION, CLAIM_KINDS, PREDICATES,
    KnowledgeClaim, KnowledgeRelation, KnowledgeSnapshot, read_authored_claim,
    read_authored_relation, validate_snapshot,
)

SHA = "a" * 40


def _claim(**overrides) -> dict:
    data = {
        "id": "component:exporter", "kind": "component", "statement": "Exporter component.",
        "epistemic_status": "declared", "authority_kind": "document",
        "authority_ref": "docs/architecture.md", "evidence_refs": ["file:docs/architecture.md"],
    }
    data.update(overrides)
    return data


def _rule(**attrs) -> dict:
    base = {"rule_type": "dependency_direction", "severity": "warning",
            "applies_to": ["src/exporter/**"], "forbidden_targets": ["component:lab"]}
    base.update(attrs)
    return _claim(id="rule:exporter-no-lab", kind="architecture_rule",
                  statement="Exporter must not import lab code.", attributes=base)


def _snapshot(claims: list[KnowledgeClaim], relations: tuple[KnowledgeRelation, ...] = ()) -> KnowledgeSnapshot:
    return KnowledgeSnapshot(
        repository="owner/repo", target_ref=SHA, claims=tuple(claims), relations=relations,
        source_scope=("tracked authored knowledge JSON",), limits=("test",),
    )


def _claim_obj(data: dict, version: int = 2) -> KnowledgeClaim:
    return read_authored_claim(data, source_ref="file:.sensemaking/knowledge/t.json", schema_version=version)


# -- vocabulary and store stability ----------------------------------------

def test_store_version_is_unchanged_so_existing_indexes_stay_valid():
    assert SCHEMA_VERSION == 1
    assert AUTHORED_SCHEMA_VERSIONS == frozenset({1, 2})


def test_version_one_vocabulary_is_a_strict_subset_of_the_accepted_set():
    assert {"component", "decision", "verification"} <= CLAIM_KINDS
    assert {"tested_by", "implemented_by", "depends_on"} <= PREDICATES
    assert "architecture_rule" not in CLAIM_KINDS
    assert "relates_to" not in PREDICATES


# -- version gating -----------------------------------------------------------

@pytest.mark.parametrize("kind", ["layer", "bounded_context", "lifecycle_state"])
def test_version_two_kinds_are_refused_from_version_one_documents(kind):
    with pytest.raises(ValueError, match="requires schema_version 2"):
        _claim_obj(_claim(id="layer:core", kind=kind), version=1)


def test_version_two_predicate_is_refused_from_version_one_documents():
    data = {"id": "rel:a", "subject": "component:a", "predicate": "relates_to",
            "object": "component:b", "attributes": {"cardinality": "1:N"}, "evidence_refs": ["file:x"]}
    with pytest.raises(ValueError, match="requires schema_version 2"):
        read_authored_relation(data, source_ref="file:x", schema_version=1)


def test_version_one_documents_still_accept_version_one_constructs():
    claim = _claim_obj(_claim(), version=1)
    assert claim.kind == "component"


# -- typed attributes ---------------------------------------------------------

def test_architecture_rule_with_valid_attributes_is_accepted():
    claim = _claim_obj(_rule())
    assert claim.attributes["rule_type"] == "dependency_direction"


@pytest.mark.parametrize("attrs,message", [
    ({"rule_type": "vibes"}, "rule_type"),
    ({"severity": "fatal"}, "severity"),
    ({"applies_to": []}, "applies_to"),
    ({"applies_to": ["/etc/passwd"]}, "repository-relative"),
    ({"applies_to": ["src/../secret"]}, "repository-relative"),
    ({"forbidden_targets": None, "allowed_targets": None}, "allowed_targets or forbidden_targets"),
])
def test_architecture_rule_rejects_bad_attributes(attrs, message):
    with pytest.raises(ValueError, match=message):
        _claim_obj(_rule(**attrs))


def test_placement_rule_requires_pattern():
    with pytest.raises(ValueError, match="needs a pattern"):
        _claim_obj(_rule(rule_type="placement", forbidden_targets=None))


def test_forbidden_term_rule_requires_terms():
    with pytest.raises(ValueError, match="needs terms"):
        _claim_obj(_rule(rule_type="forbidden_term", forbidden_targets=None))


def test_relates_to_requires_cardinality():
    base = {"id": "rel:book-chapter", "subject": "domain_concept:book",
            "predicate": "relates_to", "object": "domain_concept:chapter",
            "evidence_refs": ["file:docs/domain.md"]}
    with pytest.raises(ValueError, match="cardinality"):
        read_authored_relation(base, source_ref="file:x", schema_version=2)
    accepted = read_authored_relation({**base, "attributes": {"cardinality": "1:N"}},
                                      source_ref="file:x", schema_version=2)
    assert accepted.attributes["cardinality"] == "1:N"


# -- snapshot integrity -----------------------------------------------------------

def test_rule_scope_must_name_a_snapshot_claim_or_a_path():
    rule = _claim_obj(_rule(forbidden_targets=["component:missing"]))
    component = _claim_obj(_claim(id="component:exporter"))
    with pytest.raises(ValueError, match="unknown claim"):
        validate_snapshot(_snapshot([component, rule]))


def test_rule_with_resolvable_targets_validates():
    lab = _claim_obj(_claim(id="component:lab", kind="component", statement="Lab package."))
    exporter = _claim_obj(_claim(id="component:exporter"))
    rule = _claim_obj(_rule(forbidden_targets=["component:lab"], applies_to=["src/exporter/**"]))
    validate_snapshot(_snapshot([lab, exporter, rule]))


def test_snapshot_rejects_version_two_kind_with_unknown_status():
    bad = KnowledgeClaim(
        id="layer:core", kind="layer", statement="Core.", epistemic_status="guessed",
        authority_kind="document", authority_ref="docs/a.md", source_ref="file:x",
        evidence_refs=("file:docs/a.md",), attributes={},
    )
    with pytest.raises(ValueError, match="invalid claim kind/status"):
        validate_snapshot(_snapshot([bad]))


# -- authored document integration -------------------------------------------------

def _write_doc(root: Path, name: str, version: int, claims: list[dict], relations: list[dict] | None = None) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    (root / "docs").mkdir()
    (root / "docs" / "architecture.md").write_text("# Architecture\n", encoding="utf-8")
    folder = root / ".sensemaking" / "knowledge"
    folder.mkdir(parents=True)
    (folder / name).write_text(json.dumps(
        {"schema_version": version, "claims": claims, "relations": relations or []}), encoding="utf-8")


def test_authored_document_version_one_with_version_two_kind_is_rejected(tmp_path):
    _write_doc(tmp_path, "bad.json", 1, [_claim(id="layer:core", kind="layer")])
    tracked = {".sensemaking/knowledge/bad.json", "docs/architecture.md"}
    with pytest.raises(ValueError, match="requires schema_version 2"):
        knowledge_sources._authored_records(tmp_path, tracked)


def test_authored_document_version_two_loads_version_two_constructs(tmp_path):
    lab = _claim(id="component:lab")
    exporter = _claim(id="component:exporter")
    rule = _rule(forbidden_targets=["component:lab"])
    _write_doc(tmp_path, "arch.json", 2, [lab, exporter, rule])
    tracked = {".sensemaking/knowledge/arch.json", "docs/architecture.md"}
    claims, relations = knowledge_sources._authored_records(tmp_path, tracked)
    assert {c.id for c in claims} == {"component:lab", "component:exporter", "rule:exporter-no-lab"}
    assert relations == []


def test_unknown_schema_version_is_still_refused(tmp_path):
    _write_doc(tmp_path, "future.json", 3, [_claim()])
    with pytest.raises(ValueError, match="invalid authored knowledge document"):
        knowledge_sources._authored_records(tmp_path, {".sensemaking/knowledge/future.json", "docs/architecture.md"})


def test_version_two_claims_cannot_assert_authority(tmp_path):
    data = _rule()
    data["attributes"]["action_authorized"] = True
    with pytest.raises(ValueError, match="may not assert verified authority"):
        _claim_obj(data)


def test_is_path_scope_separates_paths_from_identifiers():
    assert knowledge.is_path_scope("src/exporter/**")
    assert knowledge.is_path_scope("scripts/validate-*.py")
    assert not knowledge.is_path_scope("component:exporter")

def test_owned_paths_require_v2_and_reject_unsafe_paths():
    owned = _claim(id="component:owned", attributes={"owned_paths": ["src/engine.py"]})
    with pytest.raises(ValueError, match="requires schema_version 2"):
        _claim_obj(owned, version=1)
    assert _claim_obj(owned).attributes["owned_paths"] == ["src/engine.py"]
    for paths in (["../escape.py"], ["/absolute.py"], ["src/*.py"], ["same.py", "same.py"]):
        with pytest.raises(ValueError, match="owned_paths"):
            _claim_obj(_claim(id="component:owned", attributes={"owned_paths": paths}))


def test_graph_rule_scope_requires_correct_endpoint_kinds():
    component = _claim_obj(_claim(id="component:producer"))
    layer = _claim_obj(_claim(id="layer:core", kind="layer"))
    relation = read_authored_relation({"id": "rel:bad", "subject": layer.id,
        "predicate": "applies_to", "object": component.id, "evidence_refs": ["file:docs/architecture.md"]},
        source_ref="file:x", schema_version=2)
    with pytest.raises(ValueError, match="applies_to needs rule"):
        validate_snapshot(_snapshot([component, layer], (relation,)))

def test_authored_contract_flow_detects_wrong_consumer_and_accepts_correct_one(tmp_path):
    producer = _claim(id="component:producer", attributes={
        "owned_paths": ["docs/architecture.md"], "contract_actor": "producer"})
    consumer = _claim(id="component:consumer", attributes={
        "owned_paths": ["docs/architecture.md"], "contract_actor": "consumer"})
    contract = _claim(id="contract:output", kind="contract", attributes={"artifact_id": "output"})
    edge = {"id": "rel:flow", "subject": "component:producer", "predicate": "flows_to",
            "object": "component:consumer",
            "evidence_refs": ["file:skills/workflow-planner/references/artifact-contracts.yaml"],
            "attributes": {"carries": "contract:output"}}
    _write_doc(tmp_path, "arch.json", 2, [producer, consumer, contract], [edge])
    artifact = tmp_path / "skills/workflow-planner/references/artifact-contracts.yaml"
    artifact.parent.mkdir(parents=True)
    artifact.write_text("artifacts:\\n  - id: output\\n    produced_by: producer\\n    consumed_by: [consumer]\\n".replace("\\n", "\n"), encoding="utf-8")
    tracked = {".sensemaking/knowledge/arch.json", "docs/architecture.md",
               "skills/workflow-planner/references/artifact-contracts.yaml"}
    claims, relations = knowledge_sources._authored_records(tmp_path, tracked)
    assert len(relations) == 1
    artifact.write_text("artifacts:\\n  - id: output\\n    produced_by: producer\\n    consumed_by: [elsewhere]\\n".replace("\\n", "\n"), encoding="utf-8")
    with pytest.raises(ValueError, match="contradicts artifact contract"):
        knowledge_sources._authored_records(tmp_path, tracked)

def test_owned_paths_must_refer_to_tracked_source(tmp_path):
    owner = _claim(id="component:real", attributes={"owned_paths": ["src/missing.py"]})
    _write_doc(tmp_path, "arch.json", 2, [owner])
    tracked = {".sensemaking/knowledge/arch.json", "docs/architecture.md"}
    with pytest.raises(ValueError, match="source not tracked"):
        knowledge_sources._authored_records(tmp_path, tracked)


def test_flows_to_carries_must_be_string():
    producer = _claim_obj(_claim(id="component:producer"))
    consumer = _claim_obj(_claim(id="component:consumer"))
    bad = read_authored_relation(
        {"id": "rel:bad", "subject": producer.id, "predicate": "flows_to",
         "object": consumer.id, "attributes": {"carries": ["contract:bad"]},
         "evidence_refs": ["file:x"]}, source_ref="file:x", schema_version=2)
    with pytest.raises(ValueError, match="flows_to must reference a contract"):
        validate_snapshot(_snapshot([producer, consumer], (bad,)))
