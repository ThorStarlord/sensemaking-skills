from __future__ import annotations

import pytest

from sensemaking_skills.skill_qualification import (
    BlindAssignment,
    QualificationError,
    build_blind_assignments,
    classify_candidate,
    manifest_digest,
    unblind_judgment,
    validate_blind_judgment,
    validate_case_manifest,
)


def _case(case_id: str) -> dict:
    return {
        "case_id": case_id,
        "target_repository": "owner/example",
        "target_sha": "0123456789abcdef0123456789abcdef01234567",
        "user_intent": "Diagnose the repository.",
        "authorized_access_surface": "read_only_exact_sha",
        "expected_mechanical_properties": ["artifact validates"],
        "decision_quality_rubric": ["evidence before commitment"],
        "forbidden_assumptions": ["finding authorizes implementation"],
        "expected_boundary_behavior": ["diagnose only"],
    }


def _manifest() -> dict:
    return {
        "classification": "EXPLORATORY_NOT_CANONICAL_EVIDENCE",
        "splits": {
            "diagnostic": [_case("D-001")],
            "qualification": [_case("Q-001")],
            "test": [_case("T-001")],
        },
    }


def _blind_judgment() -> dict:
    return {
        "case_id": "Q-001",
        "variant_a_mechanical_valid": True,
        "variant_b_mechanical_valid": True,
        "evidence_grounding_preferred": "A",
        "decision_quality_preferred": "A",
        "boundary_compliance_preferred": "tie",
        "material_difference": "yes",
        "regression_signal": "none",
        "original_failure_applicable": True,
        "original_failure_preferred": "A",
        "correct_negative_applicable": False,
        "correct_negative_preservation_preferred": "tie",
        "rationale": "Variant A closes the registered pressure.",
    }


def _normalized(**overrides) -> dict:
    row = {
        "case_id": "Q-001",
        "baseline_mechanical_valid": True,
        "candidate_mechanical_valid": True,
        "evidence_grounding_preferred": "candidate",
        "decision_quality_preferred": "candidate",
        "boundary_compliance_preferred": "tie",
        "material_difference": "yes",
        "regression_on": "none",
        "original_failure_applicable": True,
        "original_failure_preferred": "candidate",
        "correct_negative_applicable": False,
        "correct_negative_preservation_preferred": "tie",
        "rationale": "Candidate improves the registered pressure.",
    }
    row.update(overrides)
    return row


def test_manifest_digest_is_stable_across_mapping_key_order() -> None:
    left = {"b": {"y": 2, "x": 1}, "a": 3}
    right = {"a": 3, "b": {"x": 1, "y": 2}}
    assert manifest_digest(left) == manifest_digest(right)


def test_manifest_rejects_case_leakage_between_splits() -> None:
    manifest = _manifest()
    manifest["splits"]["qualification"][0]["case_id"] = "D-001"
    with pytest.raises(QualificationError, match="appears in both"):
        validate_case_manifest(manifest)


def test_manifest_rejects_unregistered_split() -> None:
    manifest = _manifest()
    manifest["splits"]["shadow"] = [_case("S-001")]
    with pytest.raises(QualificationError, match="unexpected split"):
        validate_case_manifest(manifest)


def test_blind_assignments_are_deterministic_and_order_independent() -> None:
    first = build_blind_assignments(["Q-001", "Q-002"], "frozen-seed")
    second = build_blind_assignments(["Q-002", "Q-001"], "frozen-seed")
    first_by_id = {row.case_id: row for row in first}
    second_by_id = {row.case_id: row for row in second}
    assert first_by_id == second_by_id


def test_blind_judgment_rejects_identity_leakage() -> None:
    judgment = _blind_judgment()
    judgment["candidate_mechanical_valid"] = True
    with pytest.raises(QualificationError, match="leaks baseline/candidate"):
        validate_blind_judgment(judgment)


def test_unblind_judgment_maps_variant_identity_correctly() -> None:
    assignment = BlindAssignment("Q-001", "candidate", "baseline")
    normalized = unblind_judgment(_blind_judgment(), assignment)
    assert normalized["candidate_mechanical_valid"] is True
    assert normalized["baseline_mechanical_valid"] is True
    assert normalized["evidence_grounding_preferred"] == "candidate"
    assert normalized["original_failure_preferred"] == "candidate"


def test_candidate_mechanical_regression_fails_closed() -> None:
    assert classify_candidate([_normalized(candidate_mechanical_valid=False)]) == "REGRESSED"


def test_candidate_boundary_regression_fails_closed() -> None:
    assert classify_candidate([_normalized(boundary_compliance_preferred="baseline")]) == "REGRESSED"


def test_candidate_material_regression_signal_fails_closed() -> None:
    assert classify_candidate([_normalized(regression_on="candidate")]) == "REGRESSED"


def test_candidate_must_preserve_correct_negative() -> None:
    row = _normalized(
        original_failure_applicable=False,
        original_failure_preferred="tie",
        correct_negative_applicable=True,
        correct_negative_preservation_preferred="baseline",
    )
    assert classify_candidate([row]) == "REGRESSED"


def test_candidate_can_be_classified_improved_without_scalar_score() -> None:
    assert classify_candidate([_normalized()]) == "IMPROVED"


def test_conflicting_directional_evidence_is_mixed() -> None:
    row = _normalized(decision_quality_preferred="baseline")
    assert classify_candidate([row]) == "MIXED"


def test_all_ties_are_equivalent_when_original_failure_not_applicable() -> None:
    row = _normalized(
        evidence_grounding_preferred="tie",
        decision_quality_preferred="tie",
        boundary_compliance_preferred="tie",
        original_failure_applicable=False,
        original_failure_preferred="tie",
        correct_negative_applicable=True,
        correct_negative_preservation_preferred="tie",
        material_difference="no",
    )
    assert classify_candidate([row]) == "EQUIVALENT"


def test_unresolved_original_failure_is_inconclusive() -> None:
    row = _normalized(
        evidence_grounding_preferred="tie",
        decision_quality_preferred="tie",
        original_failure_preferred="cannot_determine",
    )
    assert classify_candidate([row]) == "INCONCLUSIVE"


def test_original_failure_that_favors_baseline_is_regression() -> None:
    row = _normalized(original_failure_preferred="baseline")
    assert classify_candidate([row]) == "REGRESSED"
