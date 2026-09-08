"""First-class P7 handoff/resume over the existing P2 lifecycle primitives.

A handoff is a reconstruction artifact, not a semantic recommendation. P7 binds
the exact handoff guidance to the reconstructible campaign components using a
SHA-256 marker stored as a YAML comment in ``campaign-handoff.yaml``. The
comment does not create a second semantic schema: existing strict
``CampaignHandoff`` loading remains authoritative, while P7 resume requires the
binding and recomputes it from durable state, trace, transitions, evidence,
policy, and the handoff contract itself.

The binding is an integrity checksum, not a cryptographic signature or authority
grant. It detects accidental/stale/tampered durable content under the same trust
model as the repository's other digest checks.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sensemaking_skills.campaign_semantics import (
    CampaignHandoff,
    TerminalState,
    canonicalize,
)

from .errors import (
    CampaignIntegrityError,
    CampaignTransactionError,
)
from .service import CampaignService, CampaignSnapshot


HANDOFF_REF = "campaign-handoff.yaml"
_BINDING_PROTOCOL = "sensemaking-p7-handoff-v1"
_BINDING_PREFIX = "# p7_reconstruction_sha256: "
_BINDING_RE = re.compile(r"^# p7_reconstruction_sha256: ([0-9a-f]{64})$")


@dataclass(frozen=True)
class CampaignResumeEnvelope:
    """Mechanically reconstructed context for a fresh agent/process."""

    snapshot: CampaignSnapshot
    handoff: CampaignHandoff
    handoff_ref: str
    reconstruction_sha256: str


def _digest_payload(value: Any) -> str:
    encoded = json.dumps(
        canonicalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _normalized_actions(values: tuple[str, ...]) -> tuple[str, ...]:
    normalized: list[str] = []
    for index, value in enumerate(values):
        if not isinstance(value, str) or not value.strip():
            raise CampaignTransactionError(
                f"allowed_next_actions[{index}] must be a non-empty agent-authored string"
            )
        normalized.append(value.strip())
    if len(normalized) != len(set(normalized)):
        raise CampaignTransactionError("allowed_next_actions must not contain duplicates")
    return tuple(normalized)


def _canonical_artifacts(snapshot: CampaignSnapshot) -> tuple[str, ...]:
    """Enumerate only durable reconstruction inputs already known to the store."""
    refs = ["campaign-state.yaml", "trace.yaml"]
    if snapshot.policy is not None:
        refs.append("campaign-policy.yaml")
    refs.extend(
        f"transitions/{transition.id}.yaml" for transition in snapshot.transitions
    )
    refs.extend(snapshot.evidence_refs)
    return tuple(sorted(dict.fromkeys(refs)))


def _reconstruction_digest(
    snapshot: CampaignSnapshot,
    handoff: CampaignHandoff,
) -> str:
    payload = {
        "protocol": _BINDING_PROTOCOL,
        "campaign_id": snapshot.state.campaign_id,
        "state": canonicalize(snapshot.state),
        "transitions": [canonicalize(item) for item in snapshot.transitions],
        "trace": canonicalize(snapshot.trace),
        "evidence_refs": list(snapshot.evidence_refs),
        "policy": canonicalize(snapshot.policy) if snapshot.policy is not None else None,
        "handoff": canonicalize(handoff),
    }
    return _digest_payload(payload)


def _write_binding(path: Path, digest: str) -> None:
    if path.is_symlink() or not path.is_file():
        raise CampaignIntegrityError(
            "campaign handoff is missing or not a regular file",
            diagnostic_codes=("HANDOFF_FILE_INVALID",),
        )
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines(keepends=True)
    if lines and lines[0].startswith(_BINDING_PREFIX):
        raw = "".join(lines[1:])
    bound = f"{_BINDING_PREFIX}{digest}\n{raw}"

    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.p7-", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(bound)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _read_binding(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise CampaignIntegrityError(
            "campaign handoff is missing or not a regular file",
            diagnostic_codes=("HANDOFF_FILE_INVALID",),
        )
    with path.open("r", encoding="utf-8") as handle:
        first_line = handle.readline().rstrip("\r\n")
    match = _BINDING_RE.fullmatch(first_line)
    if match is None:
        raise CampaignIntegrityError(
            "campaign handoff is not bound for fresh-context reconstruction",
            diagnostic_codes=("HANDOFF_RECONSTRUCTION_BINDING_MISSING",),
        )
    return match.group(1)


class CampaignHandoffService:
    """Create and verify P7-bound handoffs without semantic routing."""

    def __init__(self, workspace: str | Path) -> None:
        self.lifecycle = CampaignService(workspace)

    def create(
        self,
        *,
        allowed_next_actions: tuple[str, ...] = (),
        stop_conditions: tuple[TerminalState, ...] = (),
    ) -> CampaignResumeEnvelope:
        """Create a handoff from durable facts and explicit agent guidance only."""
        actions = _normalized_actions(allowed_next_actions)
        if len(stop_conditions) != len(set(stop_conditions)):
            raise CampaignTransactionError("stop_conditions must not contain duplicates")
        if any(not isinstance(item, TerminalState) for item in stop_conditions):
            raise CampaignTransactionError(
                "stop_conditions must contain only TerminalState values"
            )

        snapshot = self.lifecycle.resume()
        handoff = self.lifecycle.generate_handoff(
            canonical_artifacts=_canonical_artifacts(snapshot),
            allowed_next_actions=actions,
            stop_conditions=stop_conditions,
        )

        # Reconstruct once after the canonical P2 write so the binding is computed
        # from exactly the durable components a fresh process will observe.
        rebound = self.lifecycle.resume()
        if rebound.handoff != handoff:
            raise CampaignIntegrityError(
                "stored campaign handoff differs from the handoff just generated",
                diagnostic_codes=("HANDOFF_WRITE_MISMATCH",),
            )
        digest = _reconstruction_digest(rebound, handoff)
        _write_binding(self.lifecycle.store.workspace.handoff_path, digest)
        return self.resume()

    def resume(self) -> CampaignResumeEnvelope:
        """Require and verify a current P7-bound handoff for fresh-context use."""
        snapshot = self.lifecycle.resume()
        handoff = snapshot.handoff
        if handoff is None:
            raise CampaignTransactionError(
                "fresh-context campaign resume requires a current campaign handoff; "
                "run 'campaign handoff' after the latest lifecycle transition"
            )

        path = self.lifecycle.store.workspace.handoff_path
        actual = _read_binding(path)
        expected = _reconstruction_digest(snapshot, handoff)
        if actual != expected:
            raise CampaignIntegrityError(
                "campaign handoff reconstruction binding does not match durable campaign context",
                diagnostic_codes=("HANDOFF_RECONSTRUCTION_BINDING_MISMATCH",),
            )

        return CampaignResumeEnvelope(
            snapshot=snapshot,
            handoff=handoff,
            handoff_ref=HANDOFF_REF,
            reconstruction_sha256=expected,
        )
