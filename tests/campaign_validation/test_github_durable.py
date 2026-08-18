from copy import deepcopy

import pytest

from sensemaking_skills.campaign_validation.github_durable import (
    GitHubDurableStateError,
    validate_github_durable_state,
)


def _sha(char: str) -> str:
    return char * 40


def _config_id() -> str:
    return "e" * 64


def _base_document() -> dict:
    return {
        "state_schema_version": "1",
        "campaign_id": "EXP-0003-stage1-auteur-github-connector-pilot",
        "classification": "EXPLORATORY_NOT_CANONICAL_EVIDENCE",
        "execution_mode": "coding_agent_native",
        "execution_surface": "github_connector",
        "durability_backend": "github_results_branch_v1",
        "validation_backend": "github_actions_exact_head",
        "invocation_boundary": "before_first_experiment_scoped_target_read",
        "results_branch": "experiment/exp-0003-results",
        "results_pr_number": 999,
        "target_repository": "https://github.com/ThorStarlord/auteur.git",
        "target_sha": _sha("a"),
        "framework_sha": _sha("b"),
        "configuration_id": _config_id(),
        "max_attempt_slots": 3,
        "concurrency_ceiling": 1,
        "external_provider_api_prohibited": True,
        "target_mutation_prohibited": True,
        "fallback_prohibited": True,
        "repair_prohibited": True,
        "automatic_merge_prohibited": True,
        "attempts": [],
    }


def _attempt(
    attempt_id: str,
    states: list[str],
    *,
    terminal_reason=None,
    validation_head_sha=None,
    validation_run_id=None,
) -> dict:
    artifact_path = None
    if "OUTPUT_CAPTURED" in states:
        artifact_path = (
            "experiments/results/EXP-0003-stage1-auteur-github-connector-pilot/"
            f"attempts/{attempt_id}/repository-sensemaking-brief.md"
        )
    return {
        "attempt_id": attempt_id,
        "configuration_id": _config_id(),
        "state": states[-1],
        "state_history": [{"state": state} for state in states],
        "artifact_path": artifact_path,
        "validation_head_sha": validation_head_sha,
        "validation_run_id": validation_run_id,
        "terminal_reason": terminal_reason,
    }


def test_empty_results_pr_state_is_valid_before_first_attempt():
    validate_github_durable_state(_base_document())


@pytest.mark.parametrize(
    "states",
    [
        ["RESERVED"],
        ["RESERVED", "INVOKED"],
        ["RESERVED", "INVOKED", "OUTPUT_CAPTURED"],
    ],
)
def test_nonterminal_lifecycle_checkpoints_are_valid(states):
    document = _base_document()
    document["attempts"] = [_attempt("attempt-001", states)]
    validate_github_durable_state(document)


def test_complete_validation_passed_attempt_is_valid():
    document = _base_document()
    document["attempts"] = [
        _attempt(
            "attempt-001",
            ["RESERVED", "INVOKED", "OUTPUT_CAPTURED", "VALIDATION_PASSED"],
            validation_head_sha=_sha("3"),
            validation_run_id=12345,
        )
    ]
    validate_github_durable_state(document)


def test_failure_terminal_state_requires_reason():
    document = _base_document()
    document["attempts"] = [
        _attempt(
            "attempt-001",
            ["RESERVED", "INVOKED", "OUTPUT_CAPTURED", "VALIDATION_FAILED"],
            validation_head_sha=_sha("3"),
            validation_run_id=12345,
        )
    ]
    with pytest.raises(GitHubDurableStateError, match="terminal_reason"):
        validate_github_durable_state(document)


def test_aborted_before_invocation_is_valid_and_consumes_visible_slot():
    document = _base_document()
    document["attempts"] = [
        _attempt(
            "attempt-001",
            ["RESERVED", "ABORTED_BEFORE_INVOCATION"],
            terminal_reason="workspace interrupted before target access",
        )
    ]
    validate_github_durable_state(document)


def test_unknown_top_level_field_fails_closed():
    document = _base_document()
    document["scheduler"] = "windows-task-scheduler"
    with pytest.raises(GitHubDurableStateError, match="unknown keys"):
        validate_github_durable_state(document)


def test_transition_history_rejects_self_commit_metadata():
    document = _base_document()
    attempt = _attempt("attempt-001", ["RESERVED"])
    attempt["state_history"][0]["commit_sha"] = _sha("1")
    document["attempts"] = [attempt]
    with pytest.raises(GitHubDurableStateError, match="unknown keys"):
        validate_github_durable_state(document)


def test_wrong_execution_surface_is_rejected():
    document = _base_document()
    document["execution_surface"] = "windows_executor"
    with pytest.raises(GitHubDurableStateError, match="execution_surface"):
        validate_github_durable_state(document)


def test_wrong_durability_backend_is_rejected():
    document = _base_document()
    document["durability_backend"] = "local_filesystem"
    with pytest.raises(GitHubDurableStateError, match="durability_backend"):
        validate_github_durable_state(document)


def test_adapter_v1_rejects_concurrency_above_one():
    document = _base_document()
    document["concurrency_ceiling"] = 2
    with pytest.raises(GitHubDurableStateError, match="concurrency_ceiling == 1"):
        validate_github_durable_state(document)


def test_two_nonterminal_attempts_violate_concurrency_one():
    document = _base_document()
    document["attempts"] = [
        _attempt("attempt-001", ["RESERVED"]),
        _attempt("attempt-002", ["RESERVED"]),
    ]
    with pytest.raises(GitHubDurableStateError, match="non-terminal attempt count"):
        validate_github_durable_state(document)


def test_attempt_count_cannot_exceed_policy_slots():
    document = _base_document()
    document["max_attempt_slots"] = 1
    document["attempts"] = [
        _attempt(
            "attempt-001",
            ["RESERVED", "ABORTED_BEFORE_INVOCATION"],
            terminal_reason="first",
        ),
        _attempt("attempt-002", ["RESERVED"]),
    ]
    with pytest.raises(GitHubDurableStateError, match="max_attempt_slots"):
        validate_github_durable_state(document)


def test_history_must_begin_reserved():
    document = _base_document()
    attempt = _attempt("attempt-001", ["RESERVED", "INVOKED"])
    attempt["state_history"] = [{"state": "INVOKED"}]
    document["attempts"] = [attempt]
    with pytest.raises(GitHubDurableStateError, match="must start at RESERVED"):
        validate_github_durable_state(document)


def test_illegal_reserved_to_output_transition_is_rejected():
    document = _base_document()
    document["attempts"] = [
        _attempt("attempt-001", ["RESERVED", "OUTPUT_CAPTURED"])
    ]
    with pytest.raises(GitHubDurableStateError, match="illegal transition"):
        validate_github_durable_state(document)


def test_current_state_must_equal_final_history_state():
    document = _base_document()
    attempt = _attempt("attempt-001", ["RESERVED", "INVOKED"])
    attempt["state"] = "RESERVED"
    document["attempts"] = [attempt]
    with pytest.raises(GitHubDurableStateError, match="final state_history"):
        validate_github_durable_state(document)


def test_output_requires_repository_relative_attempt_artifact_path():
    document = _base_document()
    attempt = _attempt(
        "attempt-001", ["RESERVED", "INVOKED", "OUTPUT_CAPTURED"]
    )
    attempt["artifact_path"] = "../../outside.md"
    document["attempts"] = [attempt]
    with pytest.raises(GitHubDurableStateError, match="inside the repository"):
        validate_github_durable_state(document)


def test_artifact_is_forbidden_before_output_captured():
    document = _base_document()
    attempt = _attempt("attempt-001", ["RESERVED", "INVOKED"])
    attempt["artifact_path"] = (
        "experiments/results/EXP-0003-stage1-auteur-github-connector-pilot/"
        "attempts/attempt-001/repository-sensemaking-brief.md"
    )
    document["attempts"] = [attempt]
    with pytest.raises(GitHubDurableStateError, match="before OUTPUT_CAPTURED"):
        validate_github_durable_state(document)


def test_validation_terminal_requires_exact_head_and_run_id():
    document = _base_document()
    document["attempts"] = [
        _attempt(
            "attempt-001",
            ["RESERVED", "INVOKED", "OUTPUT_CAPTURED", "VALIDATION_PASSED"],
        )
    ]
    with pytest.raises(GitHubDurableStateError, match="validation_head_sha"):
        validate_github_durable_state(document)


def test_validation_head_must_be_a_git_sha():
    document = _base_document()
    document["attempts"] = [
        _attempt(
            "attempt-001",
            ["RESERVED", "INVOKED", "OUTPUT_CAPTURED", "VALIDATION_PASSED"],
            validation_head_sha="not-a-sha",
            validation_run_id=12345,
        )
    ]
    with pytest.raises(GitHubDurableStateError, match="validation_head_sha"):
        validate_github_durable_state(document)


def test_validation_evidence_is_forbidden_before_validation_terminal_state():
    document = _base_document()
    attempt = _attempt(
        "attempt-001", ["RESERVED", "INVOKED", "OUTPUT_CAPTURED"]
    )
    attempt["validation_head_sha"] = _sha("3")
    attempt["validation_run_id"] = 12345
    document["attempts"] = [attempt]
    with pytest.raises(GitHubDurableStateError, match="cannot record validation evidence"):
        validate_github_durable_state(document)


def test_attempt_configuration_must_match_campaign_configuration():
    document = _base_document()
    attempt = _attempt("attempt-001", ["RESERVED"])
    attempt["configuration_id"] = "f" * 64
    document["attempts"] = [attempt]
    with pytest.raises(GitHubDurableStateError, match="campaign configuration_id"):
        validate_github_durable_state(document)


@pytest.mark.parametrize(
    "key",
    [
        "external_provider_api_prohibited",
        "target_mutation_prohibited",
        "fallback_prohibited",
        "repair_prohibited",
        "automatic_merge_prohibited",
    ],
)
def test_safety_prohibitions_are_fail_closed(key):
    document = deepcopy(_base_document())
    document[key] = False
    with pytest.raises(GitHubDurableStateError, match=key):
        validate_github_durable_state(document)
