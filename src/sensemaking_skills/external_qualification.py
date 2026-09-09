"""Verify frozen evidence from a real external golden-path dogfood run.

The verifier is deliberately mechanical. It checks representation, exact byte
identity, lifecycle coverage, native Skill-invocation evidence, no-repair
policy, and fresh-context handoff evidence. It does not invoke a coding-agent
harness and does not promote a well-formed record into semantic truth.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import yaml

from sensemaking_skills import path_containment as pc

PROTOCOL_ID = "v0.3-external-golden-path-dogfood-v1"
MANIFEST_NAME = "attempt.yaml"
REQUIRED_LIFECYCLE_STEPS = (
    "repository_diagnosis",
    "artifact_admission",
    "responsibility_authority_decision",
    "capability_inspection",
    "bounded_work",
    "work_evidence",
    "reconciliation",
    "reconciliation_disposition",
    "durable_transition",
    "lineage_inspection",
    "handoff",
    "fresh_context_resume",
    "terminal_or_continue",
)

_ALLOWED_HARNESSES = {"claude", "codex", "opencode", "other"}
_ALLOWED_ADAPTERS = {"agents", "generic", "claude", "codex", "opencode", "custom"}
_ALLOWED_SCOPES = {"user", "project"}
_ALLOWED_STEP_STATUS = {"PASS", "FAIL", "NOT_REACHED"}
_ALLOWED_OUTCOMES = {"PASS", "FAIL", "INVALID"}
_NATIVE_SOURCE = {
    "claude": "claude_code_native_log",
    "codex": "codex_native_log",
    "opencode": "opencode_native_log",
    "other": "other_native_log",
}
_HARNESS_ADAPTER = {"claude": "claude", "codex": "codex", "opencode": "opencode"}
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


@dataclass(frozen=True)
class QualificationDiagnostic:
    code: str
    message: str


@dataclass(frozen=True)
class QualificationResult:
    attempt_id: str | None
    manifest_sha256: str | None
    package_valid: bool
    qualified: bool
    outcome: str | None
    verified_evidence: tuple[str, ...]
    diagnostics: tuple[QualificationDiagnostic, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id,
            "manifest_sha256": self.manifest_sha256,
            "package_valid": self.package_valid,
            "qualified": self.qualified,
            "outcome": self.outcome,
            "verified_evidence": list(self.verified_evidence),
            "diagnostics": [asdict(item) for item in self.diagnostics],
        }


class QualificationContractError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader: _UniqueKeyLoader, node, deep: bool = False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise QualificationContractError("DUPLICATE_YAML_KEY", f"duplicate YAML key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


def _fail(code: str, message: str) -> None:
    raise QualificationContractError(code, message)


def _mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        _fail("EXPECTED_MAPPING", f"{path} must be a mapping")
    return dict(value)


def _list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        _fail("EXPECTED_LIST", f"{path} must be a list")
    return value


def _string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("EXPECTED_NONEMPTY_STRING", f"{path} must be a non-empty string")
    return value


def _boolean(value: Any, path: str) -> bool:
    if type(value) is not bool:
        _fail("EXPECTED_BOOLEAN", f"{path} must be a boolean")
    return value


def _required(data: Mapping[str, Any], path: str, *keys: str) -> None:
    missing = [key for key in keys if key not in data]
    if missing:
        _fail("MISSING_FIELD", f"{path} missing required field(s): {missing}")


def _sha(value: Any, path: str, pattern: re.Pattern[str], label: str) -> str:
    text = _string(value, path)
    if not pattern.fullmatch(text):
        _fail(f"INVALID_{label}", f"{path} must be lowercase {label}")
    return text


def _timestamp(value: Any, path: str) -> str:
    if isinstance(value, datetime):
        parsed, text = value, value.isoformat()
    else:
        text = _string(value, path)
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError as exc:
            raise QualificationContractError("INVALID_TIMESTAMP", f"{path} must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        _fail("TIMESTAMP_NOT_UTC", f"{path} must carry an explicit UTC offset")
    return text


def _load_yaml(path: Path, label: str) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            value = yaml.load(handle, Loader=_UniqueKeyLoader)
    except QualificationContractError:
        raise
    except (OSError, yaml.YAMLError) as exc:
        raise QualificationContractError("YAML_READ_ERROR", f"could not read {label}: {exc}") from exc
    return _mapping(value, label)


def _digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def _contained_file(root: Path, raw_path: Any, label: str) -> tuple[str, Path]:
    relative = _string(raw_path, label).replace("\\", "/")
    if relative.startswith("/") or re.match(r"^[A-Za-z]:", relative):
        _fail("EVIDENCE_PATH_ABSOLUTE", f"{label} must be relative to the attempt root")
    parts = [part for part in relative.split("/") if part not in ("", ".")]
    if not parts or ".." in parts:
        _fail("EVIDENCE_PATH_ESCAPE", f"{label} must not escape the attempt root")
    if any(":" in part for part in parts):
        _fail("EVIDENCE_PATH_AMBIGUOUS", f"{label} contains a prohibited ':' component")

    candidate = root.joinpath(*parts)
    if not os.path.lexists(candidate):
        _fail("EVIDENCE_MISSING", f"{label} does not exist: {relative}")
    try:
        resolved, failure = pc.resolve_containment(candidate, root)
    except Exception as exc:
        raise QualificationContractError(
            "EVIDENCE_CONTAINMENT_ERROR", f"could not establish containment for {label}: {exc}"
        ) from exc
    if failure is not None or resolved is None:
        _fail("EVIDENCE_PATH_UNSAFE", f"{label} is not physically contained: {failure}")
    if not resolved.is_file():
        _fail("EVIDENCE_NOT_FILE", f"{label} must resolve to a regular file")
    return "/".join(parts), resolved


def _evidence_ref(
    value: Any,
    *,
    root: Path,
    label: str,
    cache: dict[str, str],
    verified: set[str],
) -> tuple[str, str, Path]:
    ref = _mapping(value, label)
    _required(ref, label, "path", "sha256")
    relative, path = _contained_file(root, ref["path"], f"{label}.path")
    expected = _sha(ref["sha256"], f"{label}.sha256", _SHA256, "SHA256")
    actual = cache.setdefault(relative, _digest(path))
    if actual != expected:
        _fail(
            "EVIDENCE_DIGEST_MISMATCH",
            f"{label} digest mismatch for {relative}: expected {expected}, got {actual}",
        )
    verified.add(relative)
    return relative, actual, path


def _identity(manifest: Mapping[str, Any]) -> dict[str, str]:
    _required(
        manifest,
        "attempt",
        "protocol",
        "attempt_id",
        "started_at",
        "sensemaking_candidate",
        "runtime",
        "external_target",
        "campaign",
        "operator_policy",
        "harness_evidence",
        "lifecycle",
        "fresh_context",
        "outcome",
    )
    if manifest["protocol"] != PROTOCOL_ID:
        _fail("PROTOCOL_MISMATCH", f"attempt.protocol must be {PROTOCOL_ID!r}")
    attempt_id = _string(manifest["attempt_id"], "attempt.attempt_id")
    if not _SAFE_ID.fullmatch(attempt_id):
        _fail("INVALID_ID", "attempt.attempt_id must be a safe identifier")
    _timestamp(manifest["started_at"], "attempt.started_at")

    candidate = _mapping(manifest["sensemaking_candidate"], "sensemaking_candidate")
    _required(candidate, "sensemaking_candidate", "commit_sha", "tree_sha", "distribution_filename", "distribution_sha256", "version")
    _sha(candidate["commit_sha"], "sensemaking_candidate.commit_sha", _SHA40, "GIT_SHA")
    _sha(candidate["tree_sha"], "sensemaking_candidate.tree_sha", _SHA40, "GIT_SHA")
    _string(candidate["distribution_filename"], "sensemaking_candidate.distribution_filename")
    _sha(candidate["distribution_sha256"], "sensemaking_candidate.distribution_sha256", _SHA256, "SHA256")
    _string(candidate["version"], "sensemaking_candidate.version")

    runtime = _mapping(manifest["runtime"], "runtime")
    _required(runtime, "runtime", "os", "python", "harness", "harness_version", "adapter_target", "adapter_scope")
    _string(runtime["os"], "runtime.os")
    _string(runtime["python"], "runtime.python")
    harness = _string(runtime["harness"], "runtime.harness")
    adapter = _string(runtime["adapter_target"], "runtime.adapter_target")
    scope = _string(runtime["adapter_scope"], "runtime.adapter_scope")
    _string(runtime["harness_version"], "runtime.harness_version")
    if harness not in _ALLOWED_HARNESSES:
        _fail("UNSUPPORTED_HARNESS", f"unsupported harness: {harness}")
    if adapter not in _ALLOWED_ADAPTERS:
        _fail("UNSUPPORTED_ADAPTER_TARGET", f"unsupported adapter_target: {adapter}")
    if scope not in _ALLOWED_SCOPES:
        _fail("UNSUPPORTED_ADAPTER_SCOPE", f"unsupported adapter_scope: {scope}")
    if harness in _HARNESS_ADAPTER and adapter != _HARNESS_ADAPTER[harness]:
        _fail("HARNESS_ADAPTER_MISMATCH", f"{harness} harness requires {harness} adapter_target")
    if harness == "other" and adapter not in {"agents", "generic", "custom"}:
        _fail("HARNESS_ADAPTER_MISMATCH", "other harness requires agents, generic, or custom adapter")

    target = _mapping(manifest["external_target"], "external_target")
    _required(target, "external_target", "repository", "branch", "commit_sha", "tree_sha", "engineering_goal")
    repository = _string(target["repository"], "external_target.repository")
    normalized_repo = repository.casefold().rstrip("/")
    if normalized_repo in {
        "thorstarlord/sensemaking-skills",
        "https://github.com/thorstarlord/sensemaking-skills",
        "https://github.com/thorstarlord/sensemaking-skills.git",
    }:
        _fail("SELF_TARGET_PROHIBITED", "qualification target must be external to sensemaking-skills")
    _string(target["branch"], "external_target.branch")
    _sha(target["commit_sha"], "external_target.commit_sha", _SHA40, "GIT_SHA")
    _sha(target["tree_sha"], "external_target.tree_sha", _SHA40, "GIT_SHA")
    _string(target["engineering_goal"], "external_target.engineering_goal")

    campaign = _mapping(manifest["campaign"], "campaign")
    _required(campaign, "campaign", "campaign_id", "workspace", "workspace_outside_target_repo")
    campaign_id = _string(campaign["campaign_id"], "campaign.campaign_id")
    _string(campaign["workspace"], "campaign.workspace")
    if not _boolean(campaign["workspace_outside_target_repo"], "campaign.workspace_outside_target_repo"):
        _fail("CAMPAIGN_WORKSPACE_NOT_ISOLATED", "campaign workspace must be outside target repo")

    policy = _mapping(manifest["operator_policy"], "operator_policy")
    policy_keys = (
        "manual_campaign_repair_allowed",
        "manual_artifact_repair_allowed",
        "manual_validator_output_repair_allowed",
        "prior_chat_supplied_to_fresh_agent",
    )
    _required(policy, "operator_policy", *policy_keys)
    for key in policy_keys:
        if _boolean(policy[key], f"operator_policy.{key}"):
            _fail("PROHIBITED_OPERATOR_REPAIR_OR_CONTEXT", f"operator_policy.{key} must be false")

    fresh = _mapping(manifest["fresh_context"], "fresh_context")
    _required(
        fresh,
        "fresh_context",
        "source_session_id",
        "resume_session_id",
        "original_session_ended",
        "prior_chat_supplied",
        "handoff_receipt",
        "resume_receipt",
    )
    source_session = _string(fresh["source_session_id"], "fresh_context.source_session_id")
    resume_session = _string(fresh["resume_session_id"], "fresh_context.resume_session_id")
    if source_session == resume_session:
        _fail("FRESH_CONTEXT_SESSION_REUSED", "source and resume session IDs must be distinct")
    if not _boolean(fresh["original_session_ended"], "fresh_context.original_session_ended"):
        _fail("SOURCE_SESSION_NOT_ENDED", "original source session must end before resume")
    if _boolean(fresh["prior_chat_supplied"], "fresh_context.prior_chat_supplied"):
        _fail("PRIOR_CHAT_SUPPLIED", "fresh-context agent must not receive prior chat")

    return {
        "attempt_id": attempt_id,
        "harness": harness,
        "adapter": adapter,
        "scope": scope,
        "campaign_id": campaign_id,
        "source_session": source_session,
        "resume_session": resume_session,
    }


def _special_receipts(
    root: Path,
    manifest: Mapping[str, Any],
    identity: Mapping[str, str],
    cache: dict[str, str],
    verified: set[str],
) -> dict[str, str]:
    harness_data = _mapping(manifest["harness_evidence"], "harness_evidence")
    _required(harness_data, "harness_evidence", "native_skill", "native_invocation_observed", "setup_receipt", "invocation_receipt")
    if harness_data["native_skill"] != "repo-sensemaker":
        _fail("WRONG_NATIVE_SKILL", "native_skill must be repo-sensemaker")
    if not _boolean(harness_data["native_invocation_observed"], "harness_evidence.native_invocation_observed"):
        _fail("NATIVE_INVOCATION_NOT_OBSERVED", "native Skill invocation was not observed")

    setup_path, _, setup_file = _evidence_ref(
        harness_data["setup_receipt"], root=root, label="harness_evidence.setup_receipt", cache=cache, verified=verified
    )
    invocation_path, _, invocation_file = _evidence_ref(
        harness_data["invocation_receipt"], root=root, label="harness_evidence.invocation_receipt", cache=cache, verified=verified
    )
    if setup_path == invocation_path:
        _fail("NATIVE_INVOCATION_EVIDENCE_NOT_DISTINCT", "setup evidence cannot substitute for invocation evidence")

    setup = _load_yaml(setup_file, "setup receipt")
    _required(setup, "setup receipt", "evidence_kind", "harness", "adapter_target", "adapter_scope", "skill", "destination")
    expected_setup = {
        "evidence_kind": "skill_setup",
        "harness": identity["harness"],
        "adapter_target": identity["adapter"],
        "adapter_scope": identity["scope"],
        "skill": "repo-sensemaker",
    }
    for key, expected in expected_setup.items():
        if setup[key] != expected:
            _fail("SETUP_RECEIPT_MISMATCH", f"setup receipt {key} must be {expected!r}")
    _string(setup["destination"], "setup receipt.destination")

    invocation = _load_yaml(invocation_file, "native invocation receipt")
    _required(invocation, "native invocation receipt", "evidence_kind", "harness", "skill", "session_id", "invocation_id", "observed_at", "source")
    if invocation["evidence_kind"] != "native_skill_invocation":
        _fail("INVOCATION_RECEIPT_KIND", "invocation evidence_kind must be native_skill_invocation")
    if invocation["harness"] != identity["harness"] or invocation["skill"] != "repo-sensemaker":
        _fail("INVOCATION_RECEIPT_MISMATCH", "native invocation receipt identity mismatch")
    if invocation["session_id"] != identity["source_session"]:
        _fail("INVOCATION_SESSION_MISMATCH", "native invocation must belong to source session")
    _string(invocation["invocation_id"], "native invocation receipt.invocation_id")
    _timestamp(invocation["observed_at"], "native invocation receipt.observed_at")
    if invocation["source"] != _NATIVE_SOURCE[identity["harness"]]:
        _fail("INVOCATION_SOURCE_MISMATCH", "native invocation source does not match harness")

    fresh = _mapping(manifest["fresh_context"], "fresh_context")
    handoff_path, handoff_digest, handoff_file = _evidence_ref(
        fresh["handoff_receipt"], root=root, label="fresh_context.handoff_receipt", cache=cache, verified=verified
    )
    resume_path, _, resume_file = _evidence_ref(
        fresh["resume_receipt"], root=root, label="fresh_context.resume_receipt", cache=cache, verified=verified
    )
    if handoff_path == resume_path:
        _fail("FRESH_CONTEXT_EVIDENCE_NOT_DISTINCT", "handoff and resume need distinct records")

    handoff = _load_yaml(handoff_file, "handoff receipt")
    _required(handoff, "handoff receipt", "evidence_kind", "campaign_id", "source_session_id", "handoff_id")
    if handoff["evidence_kind"] != "campaign_handoff":
        _fail("HANDOFF_RECEIPT_KIND", "handoff evidence_kind must be campaign_handoff")
    if handoff["campaign_id"] != identity["campaign_id"] or handoff["source_session_id"] != identity["source_session"]:
        _fail("HANDOFF_RECEIPT_MISMATCH", "handoff receipt identity mismatch")
    _string(handoff["handoff_id"], "handoff receipt.handoff_id")

    resume = _load_yaml(resume_file, "fresh-context resume receipt")
    _required(resume, "fresh-context resume receipt", "evidence_kind", "campaign_id", "session_id", "handoff_sha256", "prior_chat_supplied")
    if resume["evidence_kind"] != "fresh_context_resume":
        _fail("RESUME_RECEIPT_KIND", "resume evidence_kind must be fresh_context_resume")
    if resume["campaign_id"] != identity["campaign_id"] or resume["session_id"] != identity["resume_session"]:
        _fail("RESUME_RECEIPT_MISMATCH", "fresh-context resume identity mismatch")
    if _sha(resume["handoff_sha256"], "fresh-context resume receipt.handoff_sha256", _SHA256, "SHA256") != handoff_digest:
        _fail("RESUME_HANDOFF_DIGEST_MISMATCH", "resume receipt does not bind exact handoff bytes")
    if _boolean(resume["prior_chat_supplied"], "fresh-context resume receipt.prior_chat_supplied"):
        _fail("PRIOR_CHAT_SUPPLIED", "resume receipt records prior chat as supplied")

    return {
        "setup": setup_path,
        "invocation": invocation_path,
        "handoff": handoff_path,
        "resume": resume_path,
    }


def _lifecycle(
    root: Path,
    manifest: Mapping[str, Any],
    special: Mapping[str, str],
    cache: dict[str, str],
    verified: set[str],
) -> str:
    lifecycle = _mapping(manifest["lifecycle"], "lifecycle")
    _required(lifecycle, "lifecycle", "steps")
    steps = _list(lifecycle["steps"], "lifecycle.steps")
    if len(steps) != len(REQUIRED_LIFECYCLE_STEPS):
        _fail("LIFECYCLE_STEP_COUNT", f"expected {len(REQUIRED_LIFECYCLE_STEPS)} lifecycle steps")

    statuses: list[str] = []
    evidence_by_step: dict[str, set[str]] = {}
    failure_seen = False
    for index, expected_id in enumerate(REQUIRED_LIFECYCLE_STEPS):
        step = _mapping(steps[index], f"lifecycle.steps[{index}]")
        _required(step, f"lifecycle.steps[{index}]", "id", "status", "evidence")
        if step["id"] != expected_id:
            _fail("LIFECYCLE_ORDER_MISMATCH", f"step {index} must be {expected_id!r}")
        status = _string(step["status"], f"lifecycle.steps[{index}].status")
        if status not in _ALLOWED_STEP_STATUS:
            _fail("INVALID_LIFECYCLE_STATUS", f"invalid lifecycle status: {status}")
        if failure_seen and status == "PASS":
            _fail("PASS_AFTER_FAILURE", "failed attempt cannot later return to PASS")
        if status in {"FAIL", "NOT_REACHED"}:
            failure_seen = True
        statuses.append(status)

        refs = _list(step["evidence"], f"lifecycle.steps[{index}].evidence")
        if status in {"PASS", "FAIL"} and not refs:
            _fail("MISSING_STEP_EVIDENCE", f"{expected_id} requires evidence")
        if status == "NOT_REACHED" and refs:
            _fail("UNREACHED_STEP_HAS_EVIDENCE", f"{expected_id} is NOT_REACHED but cites evidence")
        paths: set[str] = set()
        for evidence_index, ref in enumerate(refs):
            relative, _, _ = _evidence_ref(
                ref,
                root=root,
                label=f"lifecycle.steps[{index}].evidence[{evidence_index}]",
                cache=cache,
                verified=verified,
            )
            paths.add(relative)
        evidence_by_step[expected_id] = paths

    if special["invocation"] not in evidence_by_step["repository_diagnosis"]:
        _fail("NATIVE_INVOCATION_NOT_BOUND_TO_DIAGNOSIS", "repository_diagnosis must cite native invocation receipt")
    if special["handoff"] not in evidence_by_step["handoff"]:
        _fail("HANDOFF_NOT_BOUND_TO_LIFECYCLE", "handoff step must cite handoff receipt")
    if special["resume"] not in evidence_by_step["fresh_context_resume"]:
        _fail("RESUME_NOT_BOUND_TO_LIFECYCLE", "fresh_context_resume must cite resume receipt")

    outcome_data = _mapping(manifest["outcome"], "outcome")
    _required(outcome_data, "outcome", "classification")
    outcome = _string(outcome_data["classification"], "outcome.classification")
    if outcome not in _ALLOWED_OUTCOMES:
        _fail("INVALID_OUTCOME", f"invalid outcome: {outcome}")
    if "notes" in outcome_data:
        _string(outcome_data["notes"], "outcome.notes")
    if outcome == "PASS" and any(status != "PASS" for status in statuses):
        _fail("PASS_OUTCOME_WITH_INCOMPLETE_LIFECYCLE", "PASS requires every lifecycle step to PASS")
    if outcome == "FAIL" and "FAIL" not in statuses:
        _fail("FAIL_OUTCOME_WITHOUT_FAILED_STEP", "FAIL outcome must include a failed lifecycle step")
    return outcome


def validate_attempt(attempt_dir: str | Path) -> QualificationResult:
    attempt_id = None
    outcome = None
    manifest_sha256 = None
    verified: set[str] = set()
    try:
        requested = Path(attempt_dir)
        if not requested.is_dir():
            _fail("ATTEMPT_DIR_MISSING", f"attempt directory does not exist: {requested}")
        root = requested.resolve(strict=True)
        _, manifest_path = _contained_file(root, MANIFEST_NAME, "attempt manifest")
        manifest_sha256 = _digest(manifest_path)
        manifest = _load_yaml(manifest_path, "attempt manifest")
        identity = _identity(manifest)
        attempt_id = identity["attempt_id"]
        cache: dict[str, str] = {}
        special = _special_receipts(root, manifest, identity, cache, verified)
        outcome = _lifecycle(root, manifest, special, cache, verified)
    except QualificationContractError as exc:
        return QualificationResult(
            attempt_id,
            manifest_sha256,
            False,
            False,
            outcome,
            tuple(sorted(verified)),
            (QualificationDiagnostic(exc.code, exc.message),),
        )

    if outcome == "PASS":
        return QualificationResult(
            attempt_id, manifest_sha256, True, True, outcome, tuple(sorted(verified)), ()
        )
    return QualificationResult(
        attempt_id,
        manifest_sha256,
        True,
        False,
        outcome,
        tuple(sorted(verified)),
        (QualificationDiagnostic(f"ATTEMPT_RECORDED_{outcome}", f"attempt records outcome {outcome}"),),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify a frozen external golden-path evidence package.")
    parser.add_argument("attempt_dir")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--structural-only", action="store_true")
    args = parser.parse_args(argv)

    result = validate_attempt(args.attempt_dir)
    if args.json:
        print(json.dumps(result.to_dict(), sort_keys=True, separators=(",", ":")))
    else:
        marker = "EXTERNAL_GOLDEN_PATH_QUALIFIED" if result.qualified else "EXTERNAL_GOLDEN_PATH_NOT_QUALIFIED"
        print(marker)
        print(f"attempt_id={result.attempt_id or 'unknown'}")
        print(f"package_valid={str(result.package_valid).lower()}")
        print(f"outcome={result.outcome or 'unknown'}")
        print(f"manifest_sha256={result.manifest_sha256 or 'unknown'}")
        for diagnostic in result.diagnostics:
            print(f"{diagnostic.code}: {diagnostic.message}")

    if args.structural_only:
        return 0 if result.package_valid else 2
    if result.qualified:
        return 0
    return 2 if not result.package_valid else 3


if __name__ == "__main__":
    raise SystemExit(main())
