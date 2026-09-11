"""Read-only inspection helpers for verified Campaign bundles."""

from __future__ import annotations

import json
import tempfile
import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .bundle import CampaignBundleService, MANIFEST_NAME


class CampaignBundleInspectionError(ValueError):
    pass


def inspect_bundle(bundle: str | Path) -> dict[str, object]:
    path = Path(bundle)
    verification = CampaignBundleService.verify(path)
    payload: dict[str, object] = {
        "valid": verification.valid,
        "file_count": verification.file_count,
        "format_version": verification.format_version,
        "diagnostics": [
            {"code": item.code, "detail": item.detail, "path": item.path}
            for item in verification.diagnostics
        ],
        "files": [],
        "semantic_truth_established": False,
        "explicit_limit": "Bundle inspection establishes transport/integrity facts only; it does not authorize import or Campaign execution.",
    }
    if not verification.valid:
        return payload
    with zipfile.ZipFile(path, "r") as archive:
        manifest = json.loads(archive.read(MANIFEST_NAME).decode("utf-8"))
    payload["files"] = list(manifest.get("files", []))
    return payload


@contextmanager
def verified_bundle_workspace(bundle: str | Path) -> Iterator[Path]:
    verification = CampaignBundleService.verify(bundle)
    if not verification.valid:
        raise CampaignBundleInspectionError(
            "campaign bundle verification failed: "
            + ", ".join(item.code for item in verification.diagnostics)
        )
    with tempfile.TemporaryDirectory(prefix="sensemaking-bundle-") as temp_root:
        workspace = Path(temp_root) / "campaign"
        CampaignBundleService.import_bundle(bundle, workspace)
        yield workspace
