"""Portable target-locator rebinding without rewriting Campaign provenance.

The canonical Campaign v2 ``target_snapshot`` remains unchanged. A rebind only
records a verified local locator for the same repository identity and exact
recorded state. Repository discovery, semantic selection, and target refresh are
outside this companion's authority.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from sensemaking_skills.campaign_semantics import TargetSnapshot, target_snapshot_sha256

from .companion_io import atomic_write_json, mapping_sha256
from .errors import CampaignWorkspaceError
from .target_snapshot import CampaignService, capture_target_snapshot, target_snapshots_equivalent


PRIMARY_TARGET_REBIND_FILENAME = "target-rebind.json"
PRIMARY_TARGET_REBIND_VERSION = "1"


@dataclass(frozen=True)
class TargetRebindDiagnostic:
    code: str
    detail: str


@dataclass(frozen=True)
class TargetRebindVerification:
    campaign_id: str
    valid: bool
    repository_root: str | None
    locator_sha256: str | None
    diagnostics: tuple[TargetRebindDiagnostic, ...]
    semantic_truth_established: bool = False


def _core_payload(
    *,
    campaign_id: str,
    expected: TargetSnapshot,
    previous_repository_root: str,
    repository_root: str,
) -> dict[str, Any]:
    return {
        "schema_version": PRIMARY_TARGET_REBIND_VERSION,
        "campaign_id": campaign_id,
        "repository_id": expected.repository_id,
        "identity_source": expected.identity_source,
        "recorded_snapshot_sha256": target_snapshot_sha256(expected),
        "previous_repository_root": previous_repository_root,
        "repository_root": repository_root,
        "semantic_truth_established": False,
    }


def _load_locator(
    path: Path,
    *,
    expected: TargetSnapshot,
    expected_campaign_id: str | None = None,
) -> tuple[dict[str, Any] | None, list[TargetRebindDiagnostic]]:
    if not path.exists():
        return None, []
    diagnostics: list[TargetRebindDiagnostic] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [TargetRebindDiagnostic("TARGET_REBIND_READ_FAILED", str(exc))]
    if not isinstance(data, dict):
        return None, [TargetRebindDiagnostic("TARGET_REBIND_INVALID", "rebind companion must be an object")]
    required = {
        "schema_version",
        "campaign_id",
        "repository_id",
        "identity_source",
        "recorded_snapshot_sha256",
        "previous_repository_root",
        "repository_root",
        "semantic_truth_established",
        "locator_sha256",
    }
    if set(data) != required:
        diagnostics.append(TargetRebindDiagnostic("TARGET_REBIND_FIELDS_INVALID", f"fields must be exactly {sorted(required)}"))
        return data, diagnostics
    if data.get("schema_version") != PRIMARY_TARGET_REBIND_VERSION:
        diagnostics.append(TargetRebindDiagnostic("TARGET_REBIND_VERSION_UNSUPPORTED", f"unsupported schema_version {data.get('schema_version')!r}"))
    if expected_campaign_id is not None and data.get("campaign_id") != expected_campaign_id:
        diagnostics.append(TargetRebindDiagnostic("TARGET_REBIND_CAMPAIGN_ID_MISMATCH", "rebind campaign_id does not match Campaign state"))
    if data.get("repository_id") != expected.repository_id or data.get("identity_source") != expected.identity_source:
        diagnostics.append(TargetRebindDiagnostic("TARGET_REBIND_IDENTITY_MISMATCH", "rebind repository identity does not match the recorded Campaign target"))
    if data.get("recorded_snapshot_sha256") != target_snapshot_sha256(expected):
        diagnostics.append(TargetRebindDiagnostic("TARGET_REBIND_SNAPSHOT_MISMATCH", "rebind companion is not bound to the current recorded target snapshot"))
    if data.get("semantic_truth_established") is not False:
        diagnostics.append(TargetRebindDiagnostic("TARGET_REBIND_SEMANTIC_AUTHORITY_INVALID", "semantic_truth_established must remain false"))
    for field in ("previous_repository_root", "repository_root"):
        if not isinstance(data.get(field), str) or not data.get(field):
            diagnostics.append(TargetRebindDiagnostic("TARGET_REBIND_LOCATOR_INVALID", f"{field} must be non-empty text"))
    core = {key: data[key] for key in required if key != "locator_sha256" and key in data}
    if data.get("locator_sha256") != mapping_sha256(core):
        diagnostics.append(TargetRebindDiagnostic("TARGET_REBIND_DIGEST_MISMATCH", "locator_sha256 does not match companion content"))
    return data, diagnostics


def resolve_rebound_target_path(workspace: Path, expected: TargetSnapshot) -> Path | None:
    """Return the verified durable locator, or ``None`` when no rebind exists.

    This function validates the companion itself but intentionally does not
    inspect live repository bytes; ``CampaignService`` performs that existing
    live identity/state check immediately afterward.
    """

    data, diagnostics = _load_locator(
        Path(workspace).resolve() / PRIMARY_TARGET_REBIND_FILENAME,
        expected=expected,
    )
    if diagnostics:
        raise CampaignWorkspaceError(
            "primary target rebind companion is invalid: "
            + ", ".join(item.code for item in diagnostics)
        )
    if data is None:
        return None
    return Path(str(data["repository_root"])).expanduser()


class PrimaryTargetRebindService:
    """Verify and persist an explicit new locator for the primary target."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).resolve()
        self.lifecycle = CampaignService(self.workspace)
        self.path = self.workspace / PRIMARY_TARGET_REBIND_FILENAME

    def _state(self) -> tuple[str, TargetSnapshot]:
        snapshot = self.lifecycle.resume_for_transition()
        target = snapshot.state.target_snapshot
        if target is None:
            raise ValueError("Campaign has no primary target_snapshot to rebind")
        return snapshot.state.campaign_id, target

    def inspect(self) -> TargetRebindVerification:
        campaign_id, expected = self._state()
        data, diagnostics = _load_locator(
            self.path,
            expected=expected,
            expected_campaign_id=campaign_id,
        )
        return TargetRebindVerification(
            campaign_id=campaign_id,
            valid=data is not None and not diagnostics,
            repository_root=(str(data["repository_root"]) if data is not None and isinstance(data.get("repository_root"), str) else None),
            locator_sha256=(str(data["locator_sha256"]) if data is not None and isinstance(data.get("locator_sha256"), str) else None),
            diagnostics=tuple(diagnostics if data is not None else [TargetRebindDiagnostic("TARGET_REBIND_NOT_CONFIGURED", "no primary target rebind companion exists")]),
        )

    def rebind(self, target_repo: str | Path) -> TargetRebindVerification:
        campaign_id, expected = self._state()
        actual = capture_target_snapshot(target_repo)
        if actual.repository_id != expected.repository_id or actual.identity_source != expected.identity_source:
            raise ValueError("refuse rebind because candidate repository identity differs from the recorded Campaign target")
        if not target_snapshots_equivalent(expected, actual):
            raise ValueError("refuse rebind because candidate repository state differs from the recorded Campaign target snapshot")
        target_root = Path(actual.repository_root).resolve()
        if self.workspace == target_root or target_root in self.workspace.parents or self.workspace in target_root.parents:
            raise ValueError("Campaign workspace and rebound target repository must be disjoint directory trees")

        previous_root = expected.repository_root
        if self.path.exists():
            current, diagnostics = _load_locator(self.path, expected=expected, expected_campaign_id=campaign_id)
            if diagnostics:
                raise ValueError("existing primary target rebind companion is invalid")
            if current is not None and isinstance(current.get("repository_root"), str):
                previous_root = str(current["repository_root"])

        core = _core_payload(
            campaign_id=campaign_id,
            expected=expected,
            previous_repository_root=previous_root,
            repository_root=actual.repository_root,
        )
        payload = {**core, "locator_sha256": mapping_sha256(core)}
        atomic_write_json(self.path, payload)
        return self.verify()

    def verify(self) -> TargetRebindVerification:
        inspected = self.inspect()
        if not inspected.valid or inspected.repository_root is None:
            return inspected
        campaign_id, expected = self._state()
        diagnostics: list[TargetRebindDiagnostic] = []
        try:
            actual = capture_target_snapshot(inspected.repository_root)
        except CampaignWorkspaceError as exc:
            diagnostics.append(TargetRebindDiagnostic("TARGET_REBIND_REPOSITORY_UNAVAILABLE", str(exc)))
        else:
            if actual.repository_id != expected.repository_id or actual.identity_source != expected.identity_source:
                diagnostics.append(TargetRebindDiagnostic("TARGET_REBIND_LIVE_IDENTITY_MISMATCH", "live rebound repository identity differs from the recorded Campaign target"))
            elif not target_snapshots_equivalent(expected, actual):
                diagnostics.append(TargetRebindDiagnostic("TARGET_REBIND_LIVE_SNAPSHOT_DRIFT", "live rebound repository state differs from the recorded Campaign target snapshot"))
        return TargetRebindVerification(
            campaign_id=campaign_id,
            valid=not diagnostics,
            repository_root=inspected.repository_root,
            locator_sha256=inspected.locator_sha256,
            diagnostics=tuple(diagnostics),
        )
