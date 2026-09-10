"""Portable, self-verifying Campaign workspace bundles.

Bundles preserve exact durable bytes and a SHA-256 manifest. They do not assert
that Campaign conclusions are semantically true or that an imported workspace
is appropriate for a new target repository.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import stat
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


BUNDLE_FORMAT = "sensemaking_campaign_bundle"
BUNDLE_VERSION = 1
MANIFEST_NAME = "bundle-manifest.json"


@dataclass(frozen=True)
class CampaignBundleDiagnostic:
    code: str
    detail: str
    path: str = ""


@dataclass(frozen=True)
class CampaignBundleVerification:
    valid: bool
    diagnostics: tuple[CampaignBundleDiagnostic, ...]
    file_count: int
    format_version: int | None
    semantic_truth_established: bool = False


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_member(name: str) -> bool:
    if not name or "\\" in name:
        return False
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return False
    return True


def _is_zip_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(mode)


def _write_deterministic_member(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (0o100644 & 0xFFFF) << 16
    archive.writestr(info, data)


class CampaignBundleService:
    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).resolve()

    def export(self, destination: str | Path) -> Path:
        if not self.workspace.is_dir():
            raise ValueError(f"campaign workspace does not exist: {self.workspace}")
        files: list[tuple[str, bytes]] = []
        for path in sorted(self.workspace.rglob("*"), key=lambda value: value.as_posix()):
            if path.is_symlink():
                raise ValueError(f"campaign bundle refuses symlink: {path}")
            if not path.is_file():
                continue
            relative = path.relative_to(self.workspace).as_posix()
            if relative == MANIFEST_NAME:
                raise ValueError(f"campaign workspace may not contain reserved {MANIFEST_NAME}")
            files.append((relative, path.read_bytes()))

        manifest: dict[str, Any] = {
            "format": BUNDLE_FORMAT,
            "format_version": BUNDLE_VERSION,
            "files": [
                {"path": name, "sha256": _sha256(data), "size": len(data)}
                for name, data in files
            ],
            "semantic_truth_established": False,
        }
        manifest_bytes = (
            json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
        ).encode("utf-8")

        output = Path(destination).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w") as archive:
            _write_deterministic_member(archive, MANIFEST_NAME, manifest_bytes)
            for name, data in files:
                _write_deterministic_member(archive, name, data)
        return output

    @staticmethod
    def verify(bundle_path: str | Path) -> CampaignBundleVerification:
        path = Path(bundle_path)
        diagnostics: list[CampaignBundleDiagnostic] = []
        if not path.is_file():
            return CampaignBundleVerification(
                False,
                (CampaignBundleDiagnostic("BUNDLE_NOT_FOUND", f"bundle not found: {path}"),),
                0,
                None,
            )
        try:
            with zipfile.ZipFile(path, "r") as archive:
                infos = archive.infolist()
                names = [info.filename for info in infos]
                if len(names) != len(set(names)):
                    diagnostics.append(CampaignBundleDiagnostic("BUNDLE_DUPLICATE_MEMBER", "bundle contains duplicate member names"))
                for info in infos:
                    if not _safe_member(info.filename):
                        diagnostics.append(CampaignBundleDiagnostic("BUNDLE_UNSAFE_MEMBER", "unsafe archive member path", info.filename))
                    if _is_zip_symlink(info):
                        diagnostics.append(CampaignBundleDiagnostic("BUNDLE_SYMLINK_MEMBER", "symlink members are prohibited", info.filename))
                if MANIFEST_NAME not in names:
                    diagnostics.append(CampaignBundleDiagnostic("BUNDLE_MANIFEST_MISSING", f"missing {MANIFEST_NAME}"))
                    return CampaignBundleVerification(False, tuple(diagnostics), 0, None)
                try:
                    manifest = json.loads(archive.read(MANIFEST_NAME).decode("utf-8"))
                except (UnicodeError, json.JSONDecodeError, KeyError) as exc:
                    diagnostics.append(CampaignBundleDiagnostic("BUNDLE_MANIFEST_INVALID", str(exc), MANIFEST_NAME))
                    return CampaignBundleVerification(False, tuple(diagnostics), 0, None)

                if not isinstance(manifest, dict):
                    diagnostics.append(CampaignBundleDiagnostic("BUNDLE_MANIFEST_INVALID", "manifest must be a mapping", MANIFEST_NAME))
                    return CampaignBundleVerification(False, tuple(diagnostics), 0, None)
                if manifest.get("format") != BUNDLE_FORMAT:
                    diagnostics.append(CampaignBundleDiagnostic("BUNDLE_FORMAT_INVALID", f"format must be {BUNDLE_FORMAT!r}", MANIFEST_NAME))
                version = manifest.get("format_version")
                if version != BUNDLE_VERSION:
                    diagnostics.append(CampaignBundleDiagnostic("BUNDLE_VERSION_INVALID", f"format_version must be {BUNDLE_VERSION}", MANIFEST_NAME))
                entries = manifest.get("files")
                if not isinstance(entries, list):
                    diagnostics.append(CampaignBundleDiagnostic("BUNDLE_FILES_INVALID", "manifest files must be a list", MANIFEST_NAME))
                    return CampaignBundleVerification(False, tuple(diagnostics), 0, version if isinstance(version, int) else None)

                declared: set[str] = set()
                for index, entry in enumerate(entries):
                    if not isinstance(entry, dict):
                        diagnostics.append(CampaignBundleDiagnostic("BUNDLE_FILE_ENTRY_INVALID", f"file entry {index} must be a mapping", MANIFEST_NAME))
                        continue
                    name = entry.get("path")
                    expected_sha = entry.get("sha256")
                    expected_size = entry.get("size")
                    if not isinstance(name, str) or not _safe_member(name) or name == MANIFEST_NAME:
                        diagnostics.append(CampaignBundleDiagnostic("BUNDLE_FILE_PATH_INVALID", f"invalid file entry path at index {index}", str(name)))
                        continue
                    if name in declared:
                        diagnostics.append(CampaignBundleDiagnostic("BUNDLE_FILE_DECLARATION_DUPLICATE", "manifest declares a file more than once", name))
                        continue
                    declared.add(name)
                    if name not in names:
                        diagnostics.append(CampaignBundleDiagnostic("BUNDLE_FILE_MISSING", "declared file is missing from archive", name))
                        continue
                    data = archive.read(name)
                    if expected_sha != _sha256(data):
                        diagnostics.append(CampaignBundleDiagnostic("BUNDLE_DIGEST_MISMATCH", "file SHA-256 mismatch", name))
                    if expected_size != len(data):
                        diagnostics.append(CampaignBundleDiagnostic("BUNDLE_SIZE_MISMATCH", "file size mismatch", name))

                undeclared = sorted(set(names) - declared - {MANIFEST_NAME})
                for name in undeclared:
                    diagnostics.append(CampaignBundleDiagnostic("BUNDLE_UNDECLARED_FILE", "archive member is not declared by manifest", name))
                return CampaignBundleVerification(
                    valid=not diagnostics,
                    diagnostics=tuple(diagnostics),
                    file_count=len(declared),
                    format_version=version if isinstance(version, int) else None,
                )
        except (OSError, zipfile.BadZipFile) as exc:
            return CampaignBundleVerification(
                False,
                (CampaignBundleDiagnostic("BUNDLE_READ_FAILED", str(exc), str(path)),),
                0,
                None,
            )

    @staticmethod
    def import_bundle(bundle_path: str | Path, destination: str | Path) -> Path:
        verification = CampaignBundleService.verify(bundle_path)
        if not verification.valid:
            raise ValueError(
                "campaign bundle verification failed: "
                + ", ".join(item.code for item in verification.diagnostics)
            )
        target = Path(destination).resolve()
        if target.exists():
            raise ValueError(f"bundle import destination already exists: {target}")
        target.mkdir(parents=True, exist_ok=False)
        try:
            with zipfile.ZipFile(bundle_path, "r") as archive:
                manifest = json.loads(archive.read(MANIFEST_NAME).decode("utf-8"))
                for entry in manifest["files"]:
                    name = entry["path"]
                    output = target.joinpath(*PurePosixPath(name).parts)
                    output.parent.mkdir(parents=True, exist_ok=True)
                    output.write_bytes(archive.read(name))
        except Exception:
            shutil.rmtree(target, ignore_errors=True)
            raise
        return target
