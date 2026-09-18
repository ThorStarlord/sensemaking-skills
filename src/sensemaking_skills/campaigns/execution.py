"""Execution handoff and worker-result companions for Campaign v2.

These append-only companions bind already-selected work to exact durable
Campaign state and returned worker evidence. They do not select a
responsibility, grant authority, execute work, admit returned evidence into the
Campaign, or establish global closure.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Mapping

from sensemaking_skills.campaign_semantics import canonicalize, target_snapshot_sha256

from .companion_io import append_jsonl_fsync, mapping_sha256
from .multi_target import MULTI_TARGET_FILENAME, MultiTargetService
from .target_snapshot import CampaignService


EXECUTION_HANDOFFS_FILENAME = "execution-handoffs.jsonl"
EXECUTION_RESULTS_FILENAME = "execution-results.jsonl"
EXECUTION_COMPANION_VERSION = "1"
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass(frozen=True)
class ExecutionDiagnostic:
    code: str
    detail: str
    record_id: str | None = None
    line_number: int | None = None


@dataclass(frozen=True)
class ExecutionInspection:
    campaign_id: str
    valid: bool
    handoffs: tuple[Mapping[str, Any], ...]
    results: tuple[Mapping[str, Any], ...]
    diagnostics: tuple[ExecutionDiagnostic, ...]
    semantic_truth_established: bool = False


def _safe_id(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be non-empty text")
    resolved = value.strip()
    if not _SAFE_ID.fullmatch(resolved):
        raise ValueError(f"{label} must use only letters, numbers, '.', '_' or '-'")
    return resolved


def _strings(value: Any, label: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{label} must be a list of non-empty strings")
    if not allow_empty and not value:
        raise ValueError(f"{label} must not be empty")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} must not contain duplicates")
    return list(value)


def _enum(value: Any) -> str | None:
    if value is None:
        return None
    return value.value if hasattr(value, "value") else str(value)


def _record_core(record: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key != "record_digest"}


class CampaignExecutionService:
    """Persist and inspect explicit execution delegation/return records."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).resolve()
        self.lifecycle = CampaignService(self.workspace)
        self.handoffs_path = self.workspace / EXECUTION_HANDOFFS_FILENAME
        self.results_path = self.workspace / EXECUTION_RESULTS_FILENAME

    def _snapshot(self):
        return self.lifecycle.resume()

    def _load_jsonl(
        self,
        path: Path,
        *,
        kind: str,
        campaign_id: str,
    ) -> tuple[list[dict[str, Any]], list[ExecutionDiagnostic]]:
        if not path.exists():
            return [], []
        records: list[dict[str, Any]] = []
        diagnostics: list[ExecutionDiagnostic] = []
        previous: str | None = None
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            return [], [ExecutionDiagnostic(f"EXECUTION_{kind}_READ_FAILED", str(exc))]
        for line_number, line in enumerate(lines, start=1):
            if not line.strip():
                diagnostics.append(
                    ExecutionDiagnostic(
                        f"EXECUTION_{kind}_EMPTY_LINE",
                        "blank JSONL records are not allowed",
                        line_number=line_number,
                    )
                )
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                diagnostics.append(
                    ExecutionDiagnostic(
                        f"EXECUTION_{kind}_JSON_INVALID",
                        str(exc),
                        line_number=line_number,
                    )
                )
                continue
            if not isinstance(raw, dict):
                diagnostics.append(
                    ExecutionDiagnostic(
                        f"EXECUTION_{kind}_RECORD_INVALID",
                        "record must be a JSON object",
                        line_number=line_number,
                    )
                )
                continue
            record_id = str(raw.get("handoff_id") or raw.get("result_id") or "") or None
            if raw.get("schema_version") != EXECUTION_COMPANION_VERSION:
                diagnostics.append(
                    ExecutionDiagnostic(
                        f"EXECUTION_{kind}_VERSION_UNSUPPORTED",
                        f"unsupported schema_version {raw.get('schema_version')!r}",
                        record_id,
                        line_number,
                    )
                )
            if raw.get("campaign_id") != campaign_id:
                diagnostics.append(
                    ExecutionDiagnostic(
                        f"EXECUTION_{kind}_CAMPAIGN_ID_MISMATCH",
                        "record campaign_id does not match Campaign state",
                        record_id,
                        line_number,
                    )
                )
            if raw.get("previous_digest") != previous:
                diagnostics.append(
                    ExecutionDiagnostic(
                        f"EXECUTION_{kind}_CHAIN_MISMATCH",
                        "previous_digest does not match prior record",
                        record_id,
                        line_number,
                    )
                )
            try:
                expected = mapping_sha256(_record_core(raw))
            except (TypeError, ValueError):
                expected = ""
            if raw.get("record_digest") != expected:
                diagnostics.append(
                    ExecutionDiagnostic(
                        f"EXECUTION_{kind}_DIGEST_MISMATCH",
                        "record_digest does not match record content",
                        record_id,
                        line_number,
                    )
                )
            if raw.get("semantic_truth_established") is not False:
                diagnostics.append(
                    ExecutionDiagnostic(
                        f"EXECUTION_{kind}_SEMANTIC_AUTHORITY_INVALID",
                        "semantic_truth_established must remain false",
                        record_id,
                        line_number,
                    )
                )
            if isinstance(raw.get("record_digest"), str):
                previous = str(raw["record_digest"])
            records.append(raw)
        return records, diagnostics

    def inspect(self) -> ExecutionInspection:
        snapshot = self._snapshot()
        campaign_id = snapshot.state.campaign_id
        handoffs, diagnostics = self._load_jsonl(
            self.handoffs_path,
            kind="HANDOFF",
            campaign_id=campaign_id,
        )
        results, result_diagnostics = self._load_jsonl(
            self.results_path,
            kind="RESULT",
            campaign_id=campaign_id,
        )
        diagnostics.extend(result_diagnostics)

        handoff_ids: set[str] = set()
        for index, item in enumerate(handoffs, start=1):
            try:
                handoff_id = _safe_id(item.get("handoff_id"), "handoff_id")
                _safe_id(item.get("executor_kind"), "executor_kind")
                _strings(item.get("evidence_requirements"), "evidence_requirements", allow_empty=False)
                _strings(item.get("forbidden_actions"), "forbidden_actions")
                responsibility = item.get("responsibility")
                if not isinstance(responsibility, dict):
                    raise ValueError("responsibility must be an object")
                _safe_id(responsibility.get("id"), "responsibility.id")
                if not isinstance(responsibility.get("statement"), str) or not responsibility["statement"]:
                    raise ValueError("responsibility.statement must be non-empty text")
                _strings(responsibility.get("success_conditions"), "responsibility.success_conditions", allow_empty=False)
                if item.get("selection_performed_by_tool") is not False:
                    raise ValueError("selection_performed_by_tool must remain false")
                if item.get("authorization_granted_by_tool") is not False:
                    raise ValueError("authorization_granted_by_tool must remain false")
                if item.get("parent_closure_established") is not False:
                    raise ValueError("parent_closure_established must remain false")
            except ValueError as exc:
                diagnostics.append(
                    ExecutionDiagnostic(
                        "EXECUTION_HANDOFF_FIELDS_INVALID",
                        str(exc),
                        str(item.get("handoff_id") or "") or None,
                        index,
                    )
                )
                continue
            if handoff_id in handoff_ids:
                diagnostics.append(
                    ExecutionDiagnostic(
                        "EXECUTION_HANDOFF_ID_DUPLICATE",
                        f"duplicate handoff_id {handoff_id}",
                        handoff_id,
                        index,
                    )
                )
            handoff_ids.add(handoff_id)

        result_ids: set[str] = set()
        for index, item in enumerate(results, start=1):
            try:
                result_id = _safe_id(item.get("result_id"), "result_id")
                handoff_id = _safe_id(item.get("handoff_id"), "handoff_id")
                if handoff_id not in handoff_ids:
                    raise ValueError(f"unknown handoff_id {handoff_id}")
                if not isinstance(item.get("worker"), str) or not item["worker"]:
                    raise ValueError("worker must be non-empty text")
                for field in (
                    "changed_paths",
                    "validations",
                    "evidence_refs",
                    "unresolved_uncertainties",
                    "claims_supported",
                    "claims_not_supported",
                ):
                    _strings(item.get(field), field)
                if not isinstance(item.get("authority_exceeded"), bool):
                    raise ValueError("authority_exceeded must be boolean")
                if item.get("worker_completion_establishes_global_closure") is not False:
                    raise ValueError(
                        "worker_completion_establishes_global_closure must remain false"
                    )
                if item.get("campaign_evidence_admitted") is not False:
                    raise ValueError("campaign_evidence_admitted must remain false")
            except ValueError as exc:
                diagnostics.append(
                    ExecutionDiagnostic(
                        "EXECUTION_RESULT_FIELDS_INVALID",
                        str(exc),
                        str(item.get("result_id") or "") or None,
                        index,
                    )
                )
                continue
            if result_id in result_ids:
                diagnostics.append(
                    ExecutionDiagnostic(
                        "EXECUTION_RESULT_ID_DUPLICATE",
                        f"duplicate result_id {result_id}",
                        result_id,
                        index,
                    )
                )
            result_ids.add(result_id)

        return ExecutionInspection(
            campaign_id=campaign_id,
            valid=not diagnostics,
            handoffs=tuple(handoffs),
            results=tuple(results),
            diagnostics=tuple(diagnostics),
        )

    def _targets(self) -> list[dict[str, Any]]:
        snapshot = self._snapshot()
        targets: list[dict[str, Any]] = []
        primary = snapshot.state.target_snapshot
        if primary is not None:
            targets.append(
                {
                    "alias": "primary",
                    "role": "primary Campaign target",
                    "authority": _enum(
                        snapshot.state.active_responsibility.authority
                        if snapshot.state.active_responsibility is not None
                        else snapshot.state.authority
                    ),
                    "repository_id": primary.repository_id,
                    "snapshot_sha256": target_snapshot_sha256(primary),
                    "head_sha": primary.head_sha,
                    "tree_sha": primary.tree_sha,
                    "worktree_sha256": primary.worktree_sha256,
                    "dirty": primary.dirty,
                }
            )
        multi_path = self.workspace / MULTI_TARGET_FILENAME
        if multi_path.exists():
            multi = MultiTargetService(self.workspace).inspect()
            if not multi.valid:
                raise ValueError("multi-target companion is invalid")
            for item in multi.targets:
                snapshot_value = item["snapshot"]
                targets.append(
                    {
                        "alias": item["alias"],
                        "role": item["role"],
                        "authority": item["authority"],
                        "repository_id": snapshot_value["repository_id"],
                        "snapshot_sha256": item["snapshot_sha256"],
                        "head_sha": snapshot_value["head_sha"],
                        "tree_sha": snapshot_value["tree_sha"],
                        "worktree_sha256": snapshot_value["worktree_sha256"],
                        "dirty": snapshot_value["dirty"],
                    }
                )
        if not targets:
            raise ValueError(
                "execution handoff requires at least one explicit target binding"
            )
        return targets

    def create_handoff(
        self,
        *,
        handoff_id: str,
        executor_kind: str,
        evidence_requirements: tuple[str, ...],
        forbidden_actions: tuple[str, ...] = (),
    ) -> str:
        current = self.inspect()
        if not current.valid:
            raise ValueError("execution companion is invalid")
        handoff_id = _safe_id(handoff_id, "handoff_id")
        executor_kind = _safe_id(executor_kind, "executor_kind")
        if handoff_id in {str(item["handoff_id"]) for item in current.handoffs}:
            raise ValueError(f"handoff_id already exists: {handoff_id}")
        evidence = _strings(
            list(evidence_requirements),
            "evidence_requirements",
            allow_empty=False,
        )
        forbidden = _strings(list(forbidden_actions), "forbidden_actions")

        snapshot = self._snapshot()
        responsibility = snapshot.state.active_responsibility
        if responsibility is None:
            raise ValueError("execution handoff requires an active responsibility")
        if not responsibility.success_conditions:
            raise ValueError(
                "execution handoff requires responsibility success_conditions"
            )

        state_payload = canonicalize(snapshot.state)
        previous = (
            str(current.handoffs[-1]["record_digest"])
            if current.handoffs
            else None
        )
        core: dict[str, Any] = {
            "schema_version": EXECUTION_COMPANION_VERSION,
            "campaign_id": snapshot.state.campaign_id,
            "handoff_id": handoff_id,
            "executor_kind": executor_kind,
            "responsibility": {
                "id": responsibility.id,
                "statement": responsibility.statement,
                "authority": _enum(responsibility.authority),
                "decision_blocked": responsibility.decision_blocked,
                "scope": responsibility.scope,
                "success_conditions": list(responsibility.success_conditions),
                "trigger_evidence": list(responsibility.trigger_evidence),
            },
            "campaign_state_sha256": mapping_sha256(state_payload),
            "created_from_transition": (
                snapshot.transitions[-1].id if snapshot.transitions else None
            ),
            "targets": self._targets(),
            "evidence_requirements": evidence,
            "forbidden_actions": forbidden,
            "previous_digest": previous,
            "selection_performed_by_tool": False,
            "authorization_granted_by_tool": False,
            "parent_closure_established": False,
            "semantic_truth_established": False,
        }
        record = {**core, "record_digest": mapping_sha256(core)}
        append_jsonl_fsync(self.handoffs_path, record)
        return str(record["record_digest"])

    def record_result(
        self,
        *,
        result_id: str,
        handoff_id: str,
        worker: str,
        source_before: str,
        source_after: str,
        changed_paths: tuple[str, ...] = (),
        validations: tuple[str, ...] = (),
        evidence_refs: tuple[str, ...] = (),
        unresolved_uncertainties: tuple[str, ...] = (),
        claims_supported: tuple[str, ...] = (),
        claims_not_supported: tuple[str, ...] = (),
        authority_exceeded: bool,
    ) -> str:
        current = self.inspect()
        if not current.valid:
            raise ValueError("execution companion is invalid")
        result_id = _safe_id(result_id, "result_id")
        handoff_id = _safe_id(handoff_id, "handoff_id")
        if handoff_id not in {str(item["handoff_id"]) for item in current.handoffs}:
            raise ValueError(f"unknown handoff_id: {handoff_id}")
        if result_id in {str(item["result_id"]) for item in current.results}:
            raise ValueError(f"result_id already exists: {result_id}")
        if not isinstance(worker, str) or not worker.strip():
            raise ValueError("worker must be non-empty text")
        if not isinstance(source_before, str) or not source_before.strip():
            raise ValueError("source_before must be non-empty text")
        if not isinstance(source_after, str) or not source_after.strip():
            raise ValueError("source_after must be non-empty text")

        previous = (
            str(current.results[-1]["record_digest"]) if current.results else None
        )
        core: dict[str, Any] = {
            "schema_version": EXECUTION_COMPANION_VERSION,
            "campaign_id": current.campaign_id,
            "result_id": result_id,
            "handoff_id": handoff_id,
            "worker": worker.strip(),
            "source_before": source_before.strip(),
            "source_after": source_after.strip(),
            "changed_paths": _strings(list(changed_paths), "changed_paths"),
            "validations": _strings(list(validations), "validations"),
            "evidence_refs": _strings(list(evidence_refs), "evidence_refs"),
            "unresolved_uncertainties": _strings(
                list(unresolved_uncertainties),
                "unresolved_uncertainties",
            ),
            "claims_supported": _strings(
                list(claims_supported),
                "claims_supported",
            ),
            "claims_not_supported": _strings(
                list(claims_not_supported),
                "claims_not_supported",
            ),
            "authority_exceeded": authority_exceeded,
            "previous_digest": previous,
            "worker_completion_establishes_global_closure": False,
            "campaign_evidence_admitted": False,
            "semantic_truth_established": False,
        }
        record = {**core, "record_digest": mapping_sha256(core)}
        append_jsonl_fsync(self.results_path, record)
        return str(record["record_digest"])

    def working_context(self) -> dict[str, Any]:
        snapshot = self._snapshot()
        inspected = self.inspect()
        responsibility = snapshot.state.active_responsibility
        uncertainty = snapshot.state.active_uncertainty
        stop_conditions: list[str] = []
        if snapshot.policy is not None:
            stop_conditions = [_enum(item) or "" for item in snapshot.policy.stop_conditions]
        return {
            "campaign_id": snapshot.state.campaign_id,
            "mission": snapshot.state.mission,
            "current_state": snapshot.state.current_state,
            "active_responsibility": (
                canonicalize(responsibility) if responsibility is not None else None
            ),
            "decision_blocked": (
                responsibility.decision_blocked if responsibility is not None else None
            ),
            "authority": _enum(
                responsibility.authority
                if responsibility is not None
                else snapshot.state.authority
            ),
            "active_uncertainty": (
                canonicalize(uncertainty) if uncertainty is not None else None
            ),
            "targets": (
                self._targets()
                if (
                    snapshot.state.target_snapshot is not None
                    or (self.workspace / MULTI_TARGET_FILENAME).exists()
                )
                else []
            ),
            "evidence_refs": list(snapshot.evidence_refs),
            "stop_conditions": stop_conditions,
            "execution_companion_valid": inspected.valid,
            "latest_execution_handoff": (
                inspected.handoffs[-1] if inspected.handoffs else None
            ),
            "latest_worker_result": (
                inspected.results[-1] if inspected.results else None
            ),
            "semantic_recommendation_included": False,
            "global_closure_established": False,
            "explicit_limit": (
                "Working context projects durable Campaign and execution-companion "
                "state. It does not choose a responsibility, executor, next action, "
                "or closure disposition."
            ),
        }
