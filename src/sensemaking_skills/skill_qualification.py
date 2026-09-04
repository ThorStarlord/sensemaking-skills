"""Deterministic helpers for exploratory Skill candidate qualification.

This module does not invoke models, authorize experiments, mutate Skills, or make
promotion decisions. It only validates frozen case manifests, creates reproducible
blind A/B assignments, and summarizes already-recorded evaluator judgments.
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
VALID_PREFERENCES = {"A", "B", "tie", "cannot_determine"}
VALID_MATERIALITY = {"yes", "no", "cannot_determine"}
VALID_REGRESSION = {"yes", "no"}
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
        raise QualificationError("manifest classification must be EXPLORATORY_NOT_CANONICAL_EVIDENCE")

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
                    f"case {case.get('case_id', index)!r} missing required fields: {', '.join(missing)}"
                )
            case_id = case["case_id"]
            if not isinstance(case_id, str) or not case_id.strip():
                raise QualificationError("case_id must be a non-empty string")
            if case_id in seen:
                raise QualificationError(
                    f"case_id {case_id!r} appears in both {seen[case_id]!r} and {split_name!r}"
                )
            seen[case_id] = split_name

    unexpected = set(splits) - set(REQUIRED_SPLITS)
    if unexpected:
        raise QualificationError(f"unexpected split names: {', '.join(sorted(unexpected))}")


def build_blind_assignments(case_ids: Iterable[str], seed: str) -> list[BlindAssignment]:
    """Create reproducible per-case baseline/candidate A/B assignments.

    Assignment is derived independently per case from SHA-256(seed + NUL + case_id),
    avoiding order dependence. The caller should preserve the returned map separately
    from evaluator packets until judgments are committed.
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


def unblind_preference(preference: str, assignment: BlindAssignment) -> str:
    """Translate an evaluator's A/B preference to baseline/candidate identity."""
    if preference not in VALID_PREFERENCES:
        raise QualificationError(f"invalid preference: {preference}")
    if preference in {"tie", "cannot_determine"}:
        return preference
    return assignment.variant_a if preference == "A" else assignment.variant_b


def validate_judgment(judgment: Mapping[str, Any]) -> None:
    required = {
        "case_id",
        "evidence_grounding_preferred",
        "decision_quality_preferred",
        "material_difference",
        "regression_detected",
        "baseline_mechanical_valid",
        "candidate_mechanical_valid",
        "candidate_boundary_regression",
        "original_failure_improved",
        "correct_negative_preserved",
    }
    missing = sorted(required - set(judgment))
    if missing:
        raise QualificationError(f"judgment missing required fields: {', '.join(missing)}")
    for key in ("evidence_grounding_preferred", "decision_quality_preferred"):
        if judgment[key] not in VALID_PREFERENCES:
            raise QualificationError(f"invalid {key}: {judgment[key]}")
    if judgment["material_difference"] not in VALID_MATERIALITY:
        raise QualificationError("invalid material_difference")
    if judgment["regression_detected"] not in VALID_REGRESSION:
        raise QualificationError("invalid regression_detected")
    for key in (
        "baseline_mechanical_valid",
        "candidate_mechanical_valid",
        "candidate_boundary_regression",
        "original_failure_improved",
        "correct_negative_preserved",
    ):
        if not isinstance(judgment[key], bool):
            raise QualificationError(f"{key} must be boolean")


def classify_candidate(judgments: Iterable[Mapping[str, Any]]) -> str:
    """Classify a candidate using pre-registered fail-closed constraints.

    This is deliberately not a scalar score. A candidate cannot be IMPROVED if it
    introduces any mechanical failure, material regression signal, authority/boundary
    regression, fails to improve the original failure pressure, or breaks a correct
    negative. Among surviving cases, directional preferences are used only to
    distinguish IMPROVED/EQUIVALENT/MIXED/INCONCLUSIVE.
    """
    rows = list(judgments)
    if not rows:
        raise QualificationError("at least one judgment is required")
    for row in rows:
        validate_judgment(row)

    if any(not row["candidate_mechanical_valid"] for row in rows):
        return "REGRESSED"
    if any(row["candidate_boundary_regression"] for row in rows):
        return "REGRESSED"
    if any(row["regression_detected"] == "yes" for row in rows):
        return "REGRESSED"
    if any(not row["correct_negative_preserved"] for row in rows):
        return "REGRESSED"

    applicable_original = [row for row in rows if "original_failure_improved" in row]
    if applicable_original and not any(row["original_failure_improved"] for row in applicable_original):
        return "EQUIVALENT"

    directional: list[str] = []
    for row in rows:
        for key in ("evidence_grounding_preferred", "decision_quality_preferred"):
            pref = row[key]
            if pref in {"A", "B"}:
                directional.append(pref)

    if not directional:
        return "INCONCLUSIVE" if any(
            row["evidence_grounding_preferred"] == "cannot_determine"
            or row["decision_quality_preferred"] == "cannot_determine"
            for row in rows
        ) else "EQUIVALENT"

    # Judgments stored after unblinding should encode candidate as A and baseline as B.
    # This convention keeps aggregation deterministic while evaluator packets remain blind.
    candidate_wins = directional.count("A")
    baseline_wins = directional.count("B")
    if candidate_wins and not baseline_wins:
        return "IMPROVED"
    if baseline_wins and not candidate_wins:
        return "REGRESSED"
    if candidate_wins == baseline_wins:
        return "MIXED"
    return "MIXED"


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))
