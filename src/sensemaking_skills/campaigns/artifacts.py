"""P4 validated-artifact admission into a durable campaign workspace.

The active agent decides whether an artifact should be produced and what it
means. This service performs only the deterministic trust boundary:

1. snapshot the exact source bytes;
2. invoke the repository's canonical ``scripts/validate-and-report.py``;
3. reject invalid artifacts or validator execution failures;
4. copy the validated bytes content-addressed beneath ``artifacts/``;
5. write an append-only admission receipt last.

A file merely appearing beneath ``artifacts/`` is not admitted evidence. The
receipt is what binds exact bytes to an exact validator result.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

from .admission import (
    ArtifactAdmission,
    canonical_json_digest,
    dump_artifact_admission,
    load_artifact_admission,
    sha256_bytes,
    sha256_file,
)
from .errors import (
    ArtifactValidationRejectedError,
    ArtifactValidatorError,
    CampaignIntegrityError,
    CampaignWorkspaceError,
)
from .store import CampaignStore


_SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_SAFE_SUFFIX = re.compile(r"^\.[A-Za-z0-9]{1,12}$")


@dataclass(frozen=True)
class ArtifactAdmissionResult:
    admission: ArtifactAdmission
    admission_ref: str
    validation_result: Mapping[str, Any]

    @property
    def artifact_ref(self) -> str:
        return self.admission.artifact_ref

    @property
    def artifact_id(self) -> str:
        return self.admission.artifact_id

    @property
    def artifact_sha256(self) -> str:
        return self.admission.artifact_sha256


class ArtifactAdmissionService:
    """Admit only canonically validated artifact bytes as campaign evidence."""

    def __init__(self, workspace: str | Path):
        self.store = CampaignStore(workspace)

    @staticmethod
    def _require_regular_file(path: Path, *, label: str) -> Path:
        requested = Path(path).expanduser()
        if requested.is_symlink():
            raise CampaignWorkspaceError(f"{label} must not be a symlink: {requested}")
        try:
            resolved = requested.resolve(strict=True)
        except OSError as exc:
            raise CampaignWorkspaceError(f"could not resolve {label}: {requested}: {exc}") from exc
        if not resolved.is_file():
            raise CampaignWorkspaceError(f"{label} must be a regular file: {resolved}")
        return resolved

    @staticmethod
    def _require_framework_root(framework_root: str | Path) -> tuple[Path, Path]:
        root = Path(framework_root).expanduser().resolve()
        if not root.is_dir():
            raise ArtifactValidatorError(f"framework root is not a directory: {root}")
        router = root / "scripts" / "validate-and-report.py"
        if router.is_symlink() or not router.is_file():
            raise ArtifactValidatorError(
                "canonical validator router is unavailable at "
                f"{router}; P4 requires a Sensemaking framework checkout"
            )
        try:
            router.resolve(strict=True).relative_to(root.resolve(strict=True))
        except (OSError, ValueError) as exc:
            raise ArtifactValidatorError(
                f"canonical validator router escapes framework root: {router}"
            ) from exc
        return root, router

    @staticmethod
    def _assert_write_path(path: Path, root: Path) -> None:
        """Reject a write if an existing parent symlink/reparse point escapes root."""
        try:
            real_root = root.resolve(strict=True)
            resolved_parent = path.parent.resolve(strict=False)
            resolved_parent.relative_to(real_root)
        except (OSError, ValueError) as exc:
            raise CampaignWorkspaceError(
                f"artifact admission write path escapes its physical root: {path}"
            ) from exc

    @staticmethod
    def _parse_validation_output(
        *,
        completed: subprocess.CompletedProcess[str],
        snapshot_path: Path,
    ) -> dict[str, Any]:
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise ArtifactValidatorError(
                "canonical validator did not return JSON; "
                f"exit={completed.returncode} stderr={completed.stderr[:400]!r}"
            ) from exc
        if not isinstance(payload, Mapping):
            raise ArtifactValidatorError("canonical validator result must be a JSON object")
        result = dict(payload)

        required_types = {
            "valid": bool,
            "artifact_id": str,
            "artifact_path": str,
            "validator": str,
            "errors": list,
            "validation_timestamp": str,
        }
        for field, expected_type in required_types.items():
            value = result.get(field)
            if not isinstance(value, expected_type) or (
                expected_type is str and not value
            ):
                raise ArtifactValidatorError(
                    f"canonical validator result field {field!r} has invalid shape"
                )

        try:
            reported_path = Path(result["artifact_path"]).resolve(strict=True)
            expected_path = snapshot_path.resolve(strict=True)
        except OSError as exc:
            raise ArtifactValidatorError(
                "could not verify validator artifact_path binding"
            ) from exc
        if reported_path != expected_path:
            raise ArtifactValidatorError(
                "canonical validator result is not bound to the validated snapshot"
            )

        if result["valid"]:
            if completed.returncode != 0:
                raise ArtifactValidatorError(
                    "validator reported valid=true with a non-zero process exit"
                )
            if result["validator"] == "validate-and-report.py":
                raise ArtifactValidatorError(
                    "router-level result cannot grant artifact admission"
                )
            return result

        if completed.returncode == 1 and result["validator"] != "validate-and-report.py":
            raise ArtifactValidationRejectedError(result)

        raise ArtifactValidatorError(
            "canonical validation boundary failed rather than rejecting the artifact; "
            f"exit={completed.returncode} validator={result['validator']!r}"
        )

    @staticmethod
    def _selected_validator_path(
        framework_root: Path,
        validation_result: Mapping[str, Any],
    ) -> Path:
        validator_name = Path(str(validation_result["validator"])).name
        if not validator_name.endswith(".py") or not _SAFE_COMPONENT.fullmatch(validator_name):
            raise ArtifactValidatorError(
                f"validator identity is not a safe script name: {validator_name!r}"
            )
        path = framework_root / "scripts" / validator_name
        if path.is_symlink() or not path.is_file():
            raise ArtifactValidatorError(
                f"selected validator is unavailable beneath framework root: {path}"
            )
        try:
            path.resolve(strict=True).relative_to(framework_root.resolve(strict=True))
        except (OSError, ValueError) as exc:
            raise ArtifactValidatorError(
                f"selected validator escapes framework root: {path}"
            ) from exc
        return path

    @staticmethod
    def _write_content_addressed_artifact(
        *,
        destination: Path,
        root: Path,
        data: bytes,
        digest: str,
    ) -> None:
        ArtifactAdmissionService._assert_write_path(destination, root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        ArtifactAdmissionService._assert_write_path(destination, root)
        if os.path.lexists(destination):
            if destination.is_symlink() or not destination.is_file():
                raise CampaignIntegrityError(
                    "content-addressed artifact path is not a regular file",
                    diagnostic_codes=("ADMITTED_ARTIFACT_PATH_INVALID",),
                )
            if sha256_file(destination) != digest:
                raise CampaignIntegrityError(
                    "content-addressed artifact no longer matches its path digest",
                    diagnostic_codes=("ADMITTED_ARTIFACT_DIGEST_MISMATCH",),
                )
            return

        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{destination.name}.",
            dir=destination.parent,
        )
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_path, destination)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

        if sha256_file(destination) != digest:
            raise CampaignIntegrityError(
                "artifact copy verification failed after admission write",
                diagnostic_codes=("ADMITTED_ARTIFACT_DIGEST_MISMATCH",),
            )

    @staticmethod
    def _write_receipt(path: Path, admission: ArtifactAdmission, *, root: Path) -> None:
        payload = dump_artifact_admission(admission)
        ArtifactAdmissionService._assert_write_path(path, root)
        path.parent.mkdir(parents=True, exist_ok=True)
        ArtifactAdmissionService._assert_write_path(path, root)
        if os.path.lexists(path):
            if path.is_symlink() or not path.is_file():
                raise CampaignIntegrityError(
                    "artifact admission receipt path is not a regular file",
                    diagnostic_codes=("INVALID_ARTIFACT_ADMISSION",),
                )
            try:
                existing = load_artifact_admission(path)
            except Exception as exc:
                raise CampaignIntegrityError(
                    "existing artifact admission receipt is invalid",
                    diagnostic_codes=("INVALID_ARTIFACT_ADMISSION",),
                ) from exc
            if existing != admission:
                raise CampaignIntegrityError(
                    "artifact admission receipt id collides with divergent content",
                    diagnostic_codes=("INVALID_ARTIFACT_ADMISSION",),
                )
            return

        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            ArtifactAdmissionService._write_receipt(path, admission, root=root)
            return
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=True)
            handle.flush()
            os.fsync(handle.fileno())

    def admit(
        self,
        artifact_path: str | Path,
        *,
        framework_root: str | Path,
        target_repo: str | Path | None = None,
        probe_report: str | Path | None = None,
    ) -> ArtifactAdmissionResult:
        """Validate an immutable snapshot, then durably admit those exact bytes."""
        state = self.store.load_state()
        source = self._require_regular_file(Path(artifact_path), label="artifact source")
        source_bytes = source.read_bytes()
        artifact_digest = sha256_bytes(source_bytes)
        root, router = self._require_framework_root(framework_root)

        target_arg: Path | None = None
        if target_repo is not None:
            target_arg = Path(target_repo).expanduser().resolve()
            if not target_arg.is_dir():
                raise CampaignWorkspaceError(
                    f"target repository is not a directory: {target_arg}"
                )

        probe_arg: Path | None = None
        if probe_report is not None:
            probe_arg = self._require_regular_file(
                Path(probe_report), label="probe report"
            )

        with tempfile.TemporaryDirectory(prefix="sensemaking-artifact-admission-") as tmp:
            suffix = source.suffix if _SAFE_SUFFIX.fullmatch(source.suffix) else ".artifact"
            snapshot = Path(tmp) / f"artifact{suffix}"
            snapshot.write_bytes(source_bytes)
            command = [
                sys.executable,
                str(router),
                str(snapshot),
                "--repo-root",
                str(root),
            ]
            if target_arg is not None:
                command.extend(["--target-repo", str(target_arg)])
            if probe_arg is not None:
                command.extend(["--probe-report", str(probe_arg)])
            completed = subprocess.run(
                command,
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            validation_result = self._parse_validation_output(
                completed=completed,
                snapshot_path=snapshot,
            )

        artifact_id = str(validation_result["artifact_id"])
        if not _SAFE_COMPONENT.fullmatch(artifact_id):
            raise ArtifactValidatorError(
                f"validator returned unsafe artifact_id: {artifact_id!r}"
            )

        selected_validator = self._selected_validator_path(root, validation_result)
        suffix = source.suffix if _SAFE_SUFFIX.fullmatch(source.suffix) else ".artifact"
        artifact_ref = f"artifacts/{artifact_id}/{artifact_digest}{suffix}"
        artifact_destination = self.store.root / artifact_ref

        validation_result_digest = canonical_json_digest(validation_result)
        admission = ArtifactAdmission(
            campaign_id=state.campaign_id,
            artifact_id=artifact_id,
            artifact_ref=artifact_ref,
            artifact_sha256=artifact_digest,
            validator=str(validation_result["validator"]),
            validation_timestamp=str(validation_result["validation_timestamp"]),
            router_sha256=sha256_file(router),
            validator_sha256=sha256_file(selected_validator),
            validation_result_sha256=validation_result_digest,
            validation_result=validation_result,
        )
        receipt_payload = dump_artifact_admission(admission)
        receipt_id = canonical_json_digest(receipt_payload)
        admission_ref = f"admissions/{artifact_id}/{receipt_id}.yaml"
        admission_path = self.store.root / admission_ref

        # Artifact copy first, receipt last. An interruption between these writes
        # leaves only an unadmitted orphan, which CampaignStore deliberately does
        # not expose as evidence.
        self._write_content_addressed_artifact(
            destination=artifact_destination,
            root=self.store.workspace.artifacts_dir,
            data=source_bytes,
            digest=artifact_digest,
        )
        self._write_receipt(
            admission_path,
            admission,
            root=self.store.workspace.admissions_dir,
        )

        refs = set(self.store.evidence_refs())
        if artifact_ref not in refs or admission_ref not in refs:
            raise CampaignIntegrityError(
                "artifact admission did not become reconstructible campaign evidence",
                diagnostic_codes=("ARTIFACT_ADMISSION_NOT_RECONSTRUCTIBLE",),
            )

        return ArtifactAdmissionResult(
            admission=admission,
            admission_ref=admission_ref,
            validation_result=validation_result,
        )
