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
from typing import Any

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
