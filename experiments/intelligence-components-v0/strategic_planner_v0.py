"""StrategicPlanner v0: deterministic packet compiler for an advisory lab experiment.

This module does not perform strategic judgment. It validates frozen experiment
cases and renders either the current Sensemaking baseline packet or a treatment
packet that asks an active semantic model to generate a bounded candidate set.

The experiment intentionally lives under experiments/ and is not a shipped
product surface.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


COMPONENT_VERSION = "strategic-planner-v0"
ARMS = {"baseline", "treatment"}
REQUIRED_CASE_FIELDS = {
    "id",
    "title",
    "goal",
    "repository_state",
    "commitments",
    "known_uncertainties",
    "constraints",
}

CASE_CLASSIFICATIONS = {
    "retrospective_real_repository_decisions",
    "simulated_constructed_case",
}


class ExperimentContractError(ValueError):
    """Raised when a frozen experiment case violates the v0 contract."""


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExperimentContractError(f"{label} must be a non-empty string")
    return value.strip()


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ExperimentContractError(f"{label} must be a non-empty list")
    result: list[str] = []
    for index, item in enumerate(value):
        result.append(_nonempty_string(item, f"{label}[{index}]"))
    if len(result) != len(set(result)):
        raise ExperimentContractError(f"{label} must not contain duplicates")
    return result


def validate_case(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ExperimentContractError("case must be a mapping")
    missing = sorted(REQUIRED_CASE_FIELDS - set(raw))
    if missing:
        raise ExperimentContractError(f"case is missing required fields: {missing}")

    case = dict(raw)
    for field in ("id", "title", "goal", "repository_state"):
        case[field] = _nonempty_string(case[field], field)
    if "historical_outcome" in case:
        case["historical_outcome"] = _nonempty_string(
            case["historical_outcome"], "historical_outcome"
        )
    for field in ("commitments", "known_uncertainties", "constraints"):
        case[field] = _string_list(case[field], field)

    forbidden = {
        "priority_score",
        "selected_responsibility",
        "authorized_action",
        "execute",
        "automatic_route",
    }
    present_forbidden = sorted(forbidden & set(case))
    if present_forbidden:
        raise ExperimentContractError(
            "case contains fields that would pre-decide or authorize action: "
            f"{present_forbidden}"
        )
    return case


def load_cases(path: Path) -> list[dict[str, Any]]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ExperimentContractError(f"cannot read case file: {exc}") from exc
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ExperimentContractError("case file version must be 1")
    classification = data.get("classification")
    if classification not in CASE_CLASSIFICATIONS:
        raise ExperimentContractError(
            f"case classification must be one of {sorted(CASE_CLASSIFICATIONS)}"
        )
    if data.get("independent") is not False:
        raise ExperimentContractError(
            "v0 case files must explicitly declare independent: false"
        )
    if data.get("comparative_superiority_claim_allowed") is not False:
        raise ExperimentContractError(
            "v0 case files must forbid comparative superiority claims"
        )

    if classification == "retrospective_real_repository_decisions":
        if data.get("hindsight_contaminated") is not True:
            raise ExperimentContractError(
                "retrospective v0 cases must declare hindsight_contaminated: true"
            )
    else:
        if data.get("hindsight_contaminated") is not False:
            raise ExperimentContractError(
                "simulated v0 cases must declare hindsight_contaminated: false"
            )
    raw_cases = data.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise ExperimentContractError("cases must be a non-empty list")
    cases = [validate_case(item) for item in raw_cases]
    if classification == "retrospective_real_repository_decisions":
        for case in cases:
            if "historical_outcome" not in case:
                raise ExperimentContractError(
                    "retrospective v0 cases must include historical_outcome"
                )
    else:
        for case in cases:
            if "historical_outcome" in case:
                raise ExperimentContractError(
                    "simulated v0 cases must not include historical_outcome"
                )

    ids = [item["id"] for item in cases]
    if len(ids) != len(set(ids)):
        raise ExperimentContractError("case ids must be unique")
    return cases


def _bullet(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _case_context(case: dict[str, Any]) -> str:
    return (
        f"CASE: {case['id']} — {case['title']}\n\n"
        f"GOAL\n{case['goal']}\n\n"
        f"REPOSITORY STATE\n{case['repository_state']}\n\n"
        f"CURRENT COMMITMENTS\n{_bullet(case['commitments'])}\n\n"
        f"KNOWN UNCERTAINTIES\n{_bullet(case['known_uncertainties'])}\n\n"
        f"CONSTRAINTS\n{_bullet(case['constraints'])}\n"
    )


def render_baseline_packet(case: dict[str, Any]) -> str:
    case = validate_case(case)
    return (
        "EXPERIMENT ARM: BASELINE\nCOMPONENT: none\n\n"
        + _case_context(case)
        + """

INSTRUCTION

Use the current Sensemaking Level-3 reasoning model normally. State the
strategic decision to support, identify the nearest decision-changing
uncertainty when one exists, and select one warranted repository-level
responsibility or explicitly decline selection.

Preserve current authority and evidence ceilings. Do not assume that more
construction is warranted merely because implementation is possible.

RETURN

- strategic decision to support
- selected responsibility or explicit no-selection
- decision-changing uncertainty
- why the responsibility is warranted
- smallest warranted intervention
- stop / invalidation evidence
"""
    )


def render_treatment_packet(case: dict[str, Any]) -> str:
    case = validate_case(case)
    return (
        f"EXPERIMENT ARM: TREATMENT\nCOMPONENT: {COMPONENT_VERSION}\n\n"
        + _case_context(case)
        + """

STRATEGICPLANNER V0 — ADVISORY CANDIDATE GENERATION

Before the active semantic agent selects a responsibility, generate 2–4
materially distinct candidate repository-level responsibilities.

Do not split a contingent substep or diagnostic branch into a separate candidate
when it is already subsumed by another candidate. Prefer fewer genuinely distinct
repository-level responsibilities over a larger but overlapping option set.

For each candidate record:

- candidate id
- responsibility statement
- strategic decision it would support
- decision-changing uncertainty
- material dependencies
- smallest plausible intervention
- reasons for
- reasons against
- stop / invalidation evidence

Do not assign a numeric score. Do not rank the candidates. Do not choose a
winner. Do not execute anything. Do not expand repository scope, authority,
workflow selection, release authority, or product-thesis authority.

After generating the candidate set, hand it back to the active semantic agent.

RETURN

- candidate set only
- material alternative that would be easiest for baseline reasoning to miss, if any
- ambiguity or evidence insufficiency that prevents responsible comparison, if any

candidate generation != strategic decision
candidate comparison != authorization
planner output != implementation plan
"""
    )


def render_packet(case: dict[str, Any], arm: str) -> str:
    if arm not in ARMS:
        raise ExperimentContractError(f"arm must be one of {sorted(ARMS)}")
    if arm == "baseline":
        return render_baseline_packet(case)
    return render_treatment_packet(case)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).with_name("cases-v0.yaml"),
        help="frozen case YAML",
    )
    parser.add_argument("--case", required=True, help="case id")
    parser.add_argument("--arm", required=True, choices=sorted(ARMS))
    parser.add_argument("--out", type=Path, help="optional output file")
    args = parser.parse_args()

    cases = {case["id"]: case for case in load_cases(args.cases)}
    if args.case not in cases:
        parser.error(f"unknown case id: {args.case}")
    packet = render_packet(cases[args.case], args.arm)
    if args.out:
        args.out.write_text(packet, encoding="utf-8")
    else:
        print(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
