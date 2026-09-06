"""Deterministic helpers for exploratory Skill candidate qualification.

This module does not invoke models, authorize experiments, mutate Skills, or make
promotion decisions. It only validates frozen case manifests, creates reproducible
blind A/B assignments, unblinds committed judgments, and summarizes normalized
candidate-vs-baseline judgments.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

REQUIRED_SPLITS = ("diagnostic", "qualification", "test")
REQUIRED_CASE_FIELDS = (
    "case_id",
    "target_repository",
    "target_sha",
    "user_intent",
    "authorized_access_surface",
    "expected_mechanical_properties",
    "decision_quality_rubric",
    "forbidden_assumptions",
    "expected_boundary_behavior",
)
BLIND_PREFERENCES = {"A", "B", "tie", "cannot_determine"}
NORMALIZED_PREFERENCES = {"candidate", "baseline", "tie", "cannot_determine"}
REGRESSION_SIGNALS = {"none", "A", "B", "both", "cannot_determine"}
NORMALIZED_REGRESSION_SIGNALS = {
    "none",
    "candidate",
    "baseline",
    "both",
    "cannot_determine",
}
VALID_MATERIALITY = {"yes", "no", "cannot_determine"}
VALID_DISPOSITIONS = {
    "IMPROVED",
    "EQUIVALENT",
    "MIXED",
    "REGRESSED",
    "INCONCLUSIVE",
}


class QualificationError(ValueError):
    """Raised when frozen qualification inputs violate the protocol contract."""


@dataclass(frozen=True)
class BlindAssignment:
    case_id: str
    variant_a: str
    variant_b: str

    def as_dict(self) -> dict[str, str]:
        return {
            "case_id": self.case_id,
            "variant_a": self.variant_a,
            "variant_b": self.variant_b,
        }


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def manifest_digest(manifest: Mapping[str, Any]) -> str:
    """Return a stable SHA-256 digest for a parsed manifest."""
    return hashlib.sha256(_stable_json(manifest).encode("utf-8")).hexdigest()


def validate_case_manifest(manifest: Mapping[str, Any]) -> None:
    """Validate a D/Q/T case manifest and fail closed on split leakage.

    The helper intentionally validates only experiment integrity properties. It is
    not a product artifact validator and does not judge whether a case is good.
    """
    if manifest.get("classification") != "EXPLORATORY_NOT_CANONICAL_EVIDENCE":
        raise QualificationError(
            "manifest classification must be EXPLORATORY_NOT_CANONICAL_EVIDENCE"
        )

    splits = manifest.get("splits")
    if not isinstance(splits, Mapping):
        raise QualificationError("manifest must contain a splits mapping")

    seen: dict[str, str] = {}
    for split_name in REQUIRED_SPLITS:
        cases = splits.get(split_name)
        if not isinstance(cases, list) or not cases:
            raise QualificationError(f"split {split_name!r} must be a non-empty list")
        for index, case in enumerate(cases):
            if not isinstance(case, Mapping):
                raise QualificationError(f"{split_name}[{index}] must be a mapping")
            missing = [field for field in REQUIRED_CASE_FIELDS if field not in case]
            if missing:
                raise QualificationError(
                    f"case {case.get('case_id', index)!r} missing required fields: "
                    f"{', '.join(missing)}"
                )
            case_id = case["case_id"]
            if not isinstance(case_id, str) or not case_id.strip():
                raise QualificationError("case_id must be a non-empty string")
            if case_id in seen:
                raise QualificationError(
                    f"case_id {case_id!r} appears in both {seen[case_id]!r} "
                    f"and {split_name!r}"
                )
            seen[case_id] = split_name

    unexpected = set(splits) - set(REQUIRED_SPLITS)
    if unexpected:
        raise QualificationError(
            f"unexpected split names: {', '.join(sorted(unexpected))}"
        )


def build_blind_assignments(case_ids: Iterable[str], seed: str) -> list[BlindAssignment]:
    """Create reproducible per-case baseline/candidate A/B assignments.

    Assignment is derived independently per case from SHA-256(seed + NUL + case_id),
    avoiding order dependence. Preserve the assignment map separately from evaluator
    packets until judgments are committed.
    """
    if not seed:
        raise QualificationError("blinding seed must be non-empty")

    result: list[BlindAssignment] = []
    seen: set[str] = set()
    for case_id in case_ids:
        if not isinstance(case_id, str) or not case_id:
            raise QualificationError("case ids must be non-empty strings")
        if case_id in seen:
            raise QualificationError(f"duplicate case id in blinding input: {case_id}")
        seen.add(case_id)
        digest = hashlib.sha256(f"{seed}\0{case_id}".encode("utf-8")).digest()
        if digest[0] & 1:
            assignment = BlindAssignment(case_id, "candidate", "baseline")
        else:
            assignment = BlindAssignment(case_id, "baseline", "candidate")
        result.append(assignment)
    return result


def _unblind_preference(preference: str, assignment: BlindAssignment) -> str:
    if preference not in BLIND_PREFERENCES:
        raise QualificationError(f"invalid blind preference: {preference}")
    if preference in {"tie", "cannot_determine"}:
        return preference
    return assignment.variant_a if preference == "A" else assignment.variant_b


def _unblind_variant_signal(signal: str, assignment: BlindAssignment) -> str:
    if signal not in REGRESSION_SIGNALS:
        raise QualificationError(f"invalid regression signal: {signal}")
    if signal in {"none", "both", "cannot_determine"}:
        return signal
    return assignment.variant_a if signal == "A" else assignment.variant_b


def validate_blind_judgment(judgment: Mapping[str, Any]) -> None:
    """Validate an evaluator record that contains no baseline/candidate identities."""
    required = {
        "case_id",
        "variant_a_mechanical_valid",
        "variant_b_mechanical_valid",
        "evidence_grounding_preferred",
        "decision_quality_preferred",
        "boundary_compliance_preferred",
        "material_difference",
        "regression_signal",
        "original_failure_applicable",
        "original_failure_preferred",
        "correct_negative_applicable",
        "correct_negative_preservation_preferred",
        "rationale",
    }
    missing = sorted(required - set(judgment))
    if missing:
        raise QualificationError(
            f"blind judgment missing required fields: {', '.join(missing)}"
        )

    forbidden_identity_fields = {
        "baseline_mechanical_valid",
        "candidate_mechanical_valid",
        "candidate_boundary_regression",
        "candidate_regression",
        "baseline_regression",
    }
    leaked = sorted(forbidden_identity_fields & set(judgment))
    if leaked:
        raise QualificationError(
            "blind judgment leaks baseline/candidate identity fields: "
            + ", ".join(leaked)
        )

    for key in (
        "variant_a_mechanical_valid",
        "variant_b_mechanical_valid",
        "original_failure_applicable",
        "correct_negative_applicable",
    ):
        if not isinstance(judgment[key], bool):
            raise QualificationError(f"{key} must be boolean")

    for key in (
        "evidence_grounding_preferred",
        "decision_quality_preferred",
        "boundary_compliance_preferred",
        "original_failure_preferred",
        "correct_negative_preservation_preferred",
    ):
        if judgment[key] not in BLIND_PREFERENCES:
            raise QualificationError(f"invalid {key}: {judgment[key]}")

    if judgment["material_difference"] not in VALID_MATERIALITY:
        raise QualificationError("invalid material_difference")
    if judgment["regression_signal"] not in REGRESSION_SIGNALS:
        raise QualificationError("invalid regression_signal")
    if not isinstance(judgment["rationale"], str):
        raise QualificationError("rationale must be a string")


def unblind_judgment(
    judgment: Mapping[str, Any], assignment: BlindAssignment
) -> dict[str, Any]:
    """Convert a committed A/B evaluator judgment to baseline/candidate identities."""
    validate_blind_judgment(judgment)
    if judgment["case_id"] != assignment.case_id:
        raise QualificationError("judgment case_id does not match blind assignment")

    mechanical_by_variant = {
        assignment.variant_a: judgment["variant_a_mechanical_valid"],
        assignment.variant_b: judgment["variant_b_mechanical_valid"],
    }
    normalized = {
        "case_id": judgment["case_id"],
        "baseline_mechanical_valid": mechanical_by_variant["baseline"],
        "candidate_mechanical_valid": mechanical_by_variant["candidate"],
        "evidence_grounding_preferred": _unblind_preference(
            judgment["evidence_grounding_preferred"], assignment
        ),
        "decision_quality_preferred": _unblind_preference(
            judgment["decision_quality_preferred"], assignment
        ),
        "boundary_compliance_preferred": _unblind_preference(
            judgment["boundary_compliance_preferred"], assignment
        ),
        "material_difference": judgment["material_difference"],
        "regression_on": _unblind_variant_signal(
            judgment["regression_signal"], assignment
        ),
        "original_failure_applicable": judgment["original_failure_applicable"],
        "original_failure_preferred": _unblind_preference(
            judgment["original_failure_preferred"], assignment
        ),
        "correct_negative_applicable": judgment["correct_negative_applicable"],
        "correct_negative_preservation_preferred": _unblind_preference(
            judgment["correct_negative_preservation_preferred"], assignment
        ),
        "rationale": judgment["rationale"],
    }
    validate_normalized_judgment(normalized)
    return normalized


def validate_normalized_judgment(judgment: Mapping[str, Any]) -> None:
    required = {
        "case_id",
        "baseline_mechanical_valid",
        "candidate_mechanical_valid",
        "evidence_grounding_preferred",
        "decision_quality_preferred",
        "boundary_compliance_preferred",
        "material_difference",
        "regression_on",
        "original_failure_applicable",
        "original_failure_preferred",
        "correct_negative_applicable",
        "correct_negative_preservation_preferred",
        "rationale",
    }
    missing = sorted(required - set(judgment))
    if missing:
        raise QualificationError(
            f"normalized judgment missing required fields: {', '.join(missing)}"
        )
    for key in (
        "baseline_mechanical_valid",
        "candidate_mechanical_valid",
        "original_failure_applicable",
        "correct_negative_applicable",
    ):
        if not isinstance(judgment[key], bool):
            raise QualificationError(f"{key} must be boolean")
    for key in (
        "evidence_grounding_preferred",
        "decision_quality_preferred",
        "boundary_compliance_preferred",
        "original_failure_preferred",
        "correct_negative_preservation_preferred",
    ):
        if judgment[key] not in NORMALIZED_PREFERENCES:
            raise QualificationError(f"invalid {key}: {judgment[key]}")
    if judgment["material_difference"] not in VALID_MATERIALITY:
        raise QualificationError("invalid material_difference")
    if judgment["regression_on"] not in NORMALIZED_REGRESSION_SIGNALS:
        raise QualificationError("invalid regression_on")
    if not isinstance(judgment["rationale"], str):
        raise QualificationError("rationale must be a string")


def classify_candidate(judgments: Iterable[Mapping[str, Any]]) -> str:
    """Classify a candidate with non-scalar, fail-closed qualification constraints."""
    rows = list(judgments)
    if not rows:
        raise QualificationError("at least one normalized judgment is required")
    for row in rows:
        validate_normalized_judgment(row)

    # Hard regressions dominate directional preferences.
    if any(
        row["baseline_mechanical_valid"] and not row["candidate_mechanical_valid"]
        for row in rows
    ):
        return "REGRESSED"
    if any(row["regression_on"] in {"candidate", "both"} for row in rows):
        return "REGRESSED"
    if any(row["boundary_compliance_preferred"] == "baseline" for row in rows):
        return "REGRESSED"
    if any(
        row["correct_negative_applicable"]
        and row["correct_negative_preservation_preferred"] == "baseline"
        for row in rows
    ):
        return "REGRESSED"

    applicable_original = [row for row in rows if row["original_failure_applicable"]]
    if applicable_original and not any(
        row["original_failure_preferred"] == "candidate" for row in applicable_original
    ):
        if any(
            row["original_failure_preferred"] == "baseline"
            for row in applicable_original
        ):
            return "REGRESSED"
        if any(
            row["original_failure_preferred"] == "cannot_determine"
            for row in applicable_original
        ):
            return "INCONCLUSIVE"
        return "EQUIVALENT"

    directional: list[str] = []
    for row in rows:
        for key in (
            "evidence_grounding_preferred",
            "decision_quality_preferred",
            "boundary_compliance_preferred",
        ):
            pref = row[key]
            if pref in {"candidate", "baseline"}:
                directional.append(pref)
        if row["original_failure_applicable"]:
            pref = row["original_failure_preferred"]
            if pref in {"candidate", "baseline"}:
                directional.append(pref)
        if row["correct_negative_applicable"]:
            pref = row["correct_negative_preservation_preferred"]
            if pref in {"candidate", "baseline"}:
                directional.append(pref)

    if "baseline" in directional and "candidate" in directional:
        return "MIXED"
    if "baseline" in directional:
        return "REGRESSED"
    if "candidate" in directional:
        return "IMPROVED"

    if any(
        "cannot_determine"
        in {
            row["evidence_grounding_preferred"],
            row["decision_quality_preferred"],
            row["boundary_compliance_preferred"],
            row["original_failure_preferred"]
            if row["original_failure_applicable"]
            else "tie",
            row["correct_negative_preservation_preferred"]
            if row["correct_negative_applicable"]
            else "tie",
            row["regression_on"],
        }
        for row in rows
    ):
        return "INCONCLUSIVE"
    return "EQUIVALENT"


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))
