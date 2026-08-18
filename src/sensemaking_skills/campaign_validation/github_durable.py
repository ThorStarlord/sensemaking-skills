"""Validation contract for connector-native GitHub-durable campaign state.

This module does not execute campaigns and does not call GitHub. It validates the
repository-resident state document used by a connector-native campaign whose
authoritative lifecycle state is committed to a GitHub results branch.

The contract is intentionally narrow for EXP-0003 research:

* durability backend: ``github_results_branch_v1``
* execution mode: ``coding_agent_native``
* execution surface: ``github_connector``
* validation backend: ``github_actions_exact_head``
* concurrency: exactly one active attempt
* canonical Phase-4 attempt-state vocabulary is reused unchanged

Git commit SHAs for state transitions are deliberately *not* embedded in the
transition content itself: a commit cannot contain its own hash without a
circular dependency. Transition commit identities are derived from GitHub
history during audit/recovery. A later terminal transition may safely record a
*prior* exact head (``validation_head_sha``).

It is a validator, not a universal execution router or readiness gate.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import PurePosixPath
from typing import Any

from sensemaking_skills.campaign_accounting.failure_codes import CampaignAccountingError
from sensemaking_skills.campaign_accounting.models import (
    AttemptState,
    TERMINAL_STATES,
    validate_state_transition,
)

STATE_SCHEMA_VERSION = "1"
CLASSIFICATION = "EXPLORATORY_NOT_CANONICAL_EVIDENCE"
EXECUTION_MODE = "coding_agent_native"
EXECUTION_SURFACE = "github_connector"
DURABILITY_BACKEND = "github_results_branch_v1"
VALIDATION_BACKEND = "github_actions_exact_head"
INVOCATION_BOUNDARY = "before_first_experiment_scoped_target_read"

_SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA64_RE = re.compile(r"^[0-9a-f]{64}$")
_ATTEMPT_ID_RE = re.compile(r"^attempt-[0-9]{3}$")
_GITHUB_REPO_RE = re.compile(r"^https://github\.com/[^/\s]+/[^/\s]+(?:\.git)?$")

_TOP_KEYS = {
    "state_schema_version",
    "campaign_id",
    "classification",
    "execution_mode",
    "execution_surface",
    "durability_backend",
    "validation_backend",
    "invocation_boundary",
    "results_branch",
    "results_pr_number",
    "target_repository",
    "target_sha",
    "framework_sha",
    "configuration_id",
    "max_attempt_slots",
    "concurrency_ceiling",
    "external_provider_api_prohibited",
    "target_mutation_prohibited",
    "fallback_prohibited",
    "repair_prohibited",
    "automatic_merge_prohibited",
    "attempts",
}

_ATTEMPT_KEYS = {
    "attempt_id",
    "configuration_id",
    "state",
    "state_history",
    "artifact_path",
    "validation_head_sha",
    "validation_run_id",
    "terminal_reason",
}

_HISTORY_KEYS = {"state"}
_ALLOWED_STATES = {state.value for state in AttemptState}
_VALIDATION_STATES = {
    AttemptState.VALIDATION_FAILED.value,
    AttemptState.VALIDATION_PASSED.value,
}


class GitHubDurableStateError(ValueError):
    """Raised when a GitHub-durable campaign state document is invalid."""


def validate_github_durable_state(document: Mapping[str, Any]) -> None:
    """Validate one complete GitHub-durable campaign state document.

    The function is deliberately fail-closed: unknown fields, malformed
    identities, illegal state transitions, budget/concurrency violations, and
    premature output/validation evidence are all rejected.

    This function validates document semantics. GitHub-history assertions
    (which commit introduced RESERVED/INVOKED/OUTPUT_CAPTURED, ancestry, and
    whether an Actions run belongs to a claimed exact head) are audit-layer
    checks because commit identity cannot be self-embedded in the commit.
    """

    if not isinstance(document, Mapping):
        raise GitHubDurableStateError("state document must be a mapping")
    _require_exact_keys(document, _TOP_KEYS, "state document")

    _require_equal(document, "state_schema_version", STATE_SCHEMA_VERSION)
    campaign_id = _require_nonempty_string(document, "campaign_id")
    if not campaign_id.startswith("EXP-"):
        raise GitHubDurableStateError("campaign_id must use the EXP- namespace")
    _require_equal(document, "classification", CLASSIFICATION)
    _require_equal(document, "execution_mode", EXECUTION_MODE)
    _require_equal(document, "execution_surface", EXECUTION_SURFACE)
    _require_equal(document, "durability_backend", DURABILITY_BACKEND)
    _require_equal(document, "validation_backend", VALIDATION_BACKEND)
    _require_equal(document, "invocation_boundary", INVOCATION_BOUNDARY)

    results_branch = _require_nonempty_string(document, "results_branch")
    if not results_branch.startswith("experiment/") or any(
        char.isspace() for char in results_branch
    ):
        raise GitHubDurableStateError(
            "results_branch must be a whitespace-free experiment/* branch"
        )
    _require_positive_int(document, "results_pr_number")

    target_repository = _require_nonempty_string(document, "target_repository")
    if not _GITHUB_REPO_RE.fullmatch(target_repository):
        raise GitHubDurableStateError(
            "target_repository must be an https://github.com repository URL"
        )
    _require_sha40(document["target_sha"], "target_sha")
    _require_sha40(document["framework_sha"], "framework_sha")
    configuration_id = document["configuration_id"]
    _require_sha64(configuration_id, "configuration_id")

    max_attempt_slots = _require_positive_int(document, "max_attempt_slots")
    concurrency_ceiling = _require_positive_int(document, "concurrency_ceiling")
    if concurrency_ceiling != 1:
        raise GitHubDurableStateError(
            "github_results_branch_v1 supports concurrency_ceiling == 1 only"
        )

    for key in (
        "external_provider_api_prohibited",
        "target_mutation_prohibited",
        "fallback_prohibited",
        "repair_prohibited",
        "automatic_merge_prohibited",
    ):
        if document[key] is not True:
            raise GitHubDurableStateError(f"{key} must be true")

    attempts = document["attempts"]
    if not isinstance(attempts, list):
        raise GitHubDurableStateError("attempts must be a list")
    if len(attempts) > max_attempt_slots:
        raise GitHubDurableStateError("attempt count exceeds max_attempt_slots")

    seen_attempt_ids: set[str] = set()
    active_attempts = 0
    for index, attempt in enumerate(attempts):
        if not isinstance(attempt, Mapping):
            raise GitHubDurableStateError(f"attempts[{index}] must be a mapping")
        state = _validate_attempt(
            attempt,
            campaign_id=campaign_id,
            configuration_id=str(configuration_id),
            seen_attempt_ids=seen_attempt_ids,
            label=f"attempts[{index}]",
        )
        if state not in TERMINAL_STATES:
            active_attempts += 1

    if active_attempts > concurrency_ceiling:
        raise GitHubDurableStateError(
            "non-terminal attempt count exceeds concurrency_ceiling"
        )


def _validate_attempt(
    attempt: Mapping[str, Any],
    *,
    campaign_id: str,
    configuration_id: str,
    seen_attempt_ids: set[str],
    label: str,
) -> str:
    _require_exact_keys(attempt, _ATTEMPT_KEYS, label)

    attempt_id = _require_nonempty_string(attempt, "attempt_id", prefix=label)
    if not _ATTEMPT_ID_RE.fullmatch(attempt_id):
        raise GitHubDurableStateError(f"{label}.attempt_id must match attempt-NNN")
    if attempt_id in seen_attempt_ids:
        raise GitHubDurableStateError(f"duplicate attempt_id: {attempt_id}")
    seen_attempt_ids.add(attempt_id)

    if attempt["configuration_id"] != configuration_id:
        raise GitHubDurableStateError(
            f"{label}.configuration_id must equal the campaign configuration_id"
        )

    state = attempt["state"]
    if state not in _ALLOWED_STATES:
        raise GitHubDurableStateError(
            f"{label}.state is not a canonical attempt state"
        )

    history = attempt["state_history"]
    if not isinstance(history, list) or not history:
        raise GitHubDurableStateError(
            f"{label}.state_history must be a non-empty list"
        )

    history_states: list[str] = []
    for history_index, entry in enumerate(history):
        history_label = f"{label}.state_history[{history_index}]"
        if not isinstance(entry, Mapping):
            raise GitHubDurableStateError(f"{history_label} must be a mapping")
        _require_exact_keys(entry, _HISTORY_KEYS, history_label)
        entry_state = entry["state"]
        if entry_state not in _ALLOWED_STATES:
            raise GitHubDurableStateError(f"{history_label}.state is invalid")
        history_states.append(str(entry_state))

    if history_states[0] != AttemptState.RESERVED.value:
        raise GitHubDurableStateError(
            f"{label}.state_history must start at RESERVED"
        )
    for current, new in zip(history_states, history_states[1:]):
        try:
            validate_state_transition(current, new)
        except CampaignAccountingError as exc:
            raise GitHubDurableStateError(
                f"{label}.state_history contains illegal transition {current} -> {new}"
            ) from exc

    if state != history_states[-1]:
        raise GitHubDurableStateError(
            f"{label}.state must equal the final state_history state"
        )

    output_captured = AttemptState.OUTPUT_CAPTURED.value in history_states
    artifact_path = attempt["artifact_path"]
    if output_captured:
        _validate_artifact_path(
            artifact_path,
            campaign_id=campaign_id,
            attempt_id=attempt_id,
            label=label,
        )
    elif artifact_path is not None:
        raise GitHubDurableStateError(
            f"{label}.artifact_path must be null before OUTPUT_CAPTURED"
        )

    validation_head_sha = attempt["validation_head_sha"]
    validation_run_id = attempt["validation_run_id"]
    if state in _VALIDATION_STATES:
        _require_sha40(validation_head_sha, f"{label}.validation_head_sha")
        _require_positive_scalar_int(
            validation_run_id, f"{label}.validation_run_id"
        )
        if not output_captured:
            raise GitHubDurableStateError(
                f"{label} cannot reach a validation terminal state without OUTPUT_CAPTURED"
            )
    elif validation_head_sha is not None or validation_run_id is not None:
        raise GitHubDurableStateError(
            f"{label} cannot record validation evidence before a validation terminal state"
        )

    terminal_reason = attempt["terminal_reason"]
    if state in {
        AttemptState.ABORTED_BEFORE_INVOCATION.value,
        AttemptState.PROVIDER_FAILED.value,
        AttemptState.VALIDATION_FAILED.value,
    }:
        if not isinstance(terminal_reason, str) or not terminal_reason.strip():
            raise GitHubDurableStateError(
                f"{label}.terminal_reason is required for failure/abort terminal states"
            )
    elif state == AttemptState.VALIDATION_PASSED.value:
        if terminal_reason is not None:
            raise GitHubDurableStateError(
                f"{label}.terminal_reason must be null for VALIDATION_PASSED"
            )
    elif terminal_reason is not None:
        raise GitHubDurableStateError(
            f"{label}.terminal_reason must be null while the attempt is non-terminal"
        )

    return str(state)


def _validate_artifact_path(
    value: Any, *, campaign_id: str, attempt_id: str, label: str
) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GitHubDurableStateError(
            f"{label}.artifact_path must be a repository-relative path"
        )
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise GitHubDurableStateError(
            f"{label}.artifact_path must remain inside the repository"
        )
    expected_prefix = PurePosixPath(
        "experiments", "results", campaign_id, "attempts", attempt_id
    )
    if path.parts[: len(expected_prefix.parts)] != expected_prefix.parts:
        raise GitHubDurableStateError(
            f"{label}.artifact_path must be under {expected_prefix.as_posix()}/"
        )


def _require_exact_keys(
    mapping: Mapping[str, Any], expected: set[str], label: str
) -> None:
    actual = set(mapping.keys())
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing or unknown:
        raise GitHubDurableStateError(
            f"{label} has missing keys={missing!r} unknown keys={unknown!r}"
        )


def _require_equal(mapping: Mapping[str, Any], key: str, expected: Any) -> None:
    if mapping[key] != expected:
        raise GitHubDurableStateError(f"{key} must equal {expected!r}")


def _require_nonempty_string(
    mapping: Mapping[str, Any], key: str, *, prefix: str | None = None
) -> str:
    value = mapping[key]
    label = f"{prefix}.{key}" if prefix else key
    if not isinstance(value, str) or not value.strip():
        raise GitHubDurableStateError(f"{label} must be a non-empty string")
    return value


def _require_positive_int(mapping: Mapping[str, Any], key: str) -> int:
    value = mapping[key]
    _require_positive_scalar_int(value, key)
    return int(value)


def _require_positive_scalar_int(value: Any, label: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise GitHubDurableStateError(f"{label} must be a positive integer")


def _require_sha40(value: Any, label: str) -> None:
    if not isinstance(value, str) or not _SHA40_RE.fullmatch(value):
        raise GitHubDurableStateError(
            f"{label} must be a 40-character lowercase Git SHA"
        )


def _require_sha64(value: Any, label: str) -> None:
    if not isinstance(value, str) or not _SHA64_RE.fullmatch(value):
        raise GitHubDurableStateError(
            f"{label} must be a 64-character lowercase SHA-256 hex string"
        )
