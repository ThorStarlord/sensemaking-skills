"""One-shot provider permit (Phase 6 correction, Issue #122).

The Phase 4 durable boundary issues a single opaque ``ProviderPermit``
AFTER the durable ``INVOKED`` transition and consumes it (atomically, under
the campaign lock) immediately before entering the provider. The real
provider requires a genuine, consumed permit bound to the exact attempt
before it may import the SDK client or issue any provider call.

The invariant this enforces is structural, not conventional:

    no validated bundle
        -> no durable reservation
        -> no capability consumption
        -> no durable INVOKED
        -> no permit issuance
        -> no provider entry

A ``ProviderPermit`` is NOT publicly constructible: instances are produced
ONLY by ``issue_provider_permit``, which stamps a per-process sentinel via
the same closure-sealed pattern as ``AttemptReservation``. Liveness and
one-shot-ness are decided by the DURABLE registry -- the on-disk permit
file plus the append-only ledger -- never by the in-memory object: a
forged, reconstructed, copied, or stale permit object cannot verify as
genuine, cannot be consumed, and cannot open the provider.

Permit registry record (``attempts/<attempt_id>/provider-permit.yaml``):

    permit_schema_version: "1"
    permit_id: <64 hex>
    attempt_id: <uuid>
    campaign_id: <id>
    configuration_id: <64 hex>
    issued_at: <iso>
    consumed: false | true

``is_genuine_provider_permit`` requires ALL of:

* the closure sentinel (object was produced by the issuer);
* the on-disk registry record exists and agrees on every identity field;
* the ledger's latest state event for the attempt is ``INVOKED`` (a permit
  can never outlive the durable INVOKED transition, and a permit observed
  while the attempt is RESERVED proves it was issued before INVOKED);
* the consumption marker agrees with the object's ``consumed`` flag.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .failure_codes import (
    PROVIDER_PERMIT_ALREADY_CONSUMED,
    PROVIDER_PERMIT_ATTEMPT_MISMATCH,
    PROVIDER_PERMIT_CAMPAIGN_MISMATCH,
    PROVIDER_PERMIT_CONFIGURATION_MISMATCH,
    PROVIDER_PERMIT_NOT_CONSUMED,
    PROVIDER_PERMIT_NOT_GENUINE,
    PROVIDER_PERMIT_NOT_ISSUED,
    PROVIDER_PERMIT_REQUIRED,
    CampaignAccountingError,
)
from .ledger import CampaignLedger, campaign_lock
from .models import AttemptState

PERMIT_FILENAME = "provider-permit.yaml"
PERMIT_SCHEMA_VERSION = "1"


@dataclass(frozen=True)
class ProviderPermit:
    """The one-shot provider-entry permit.

    Not publicly constructible: produced ONLY by ``issue_provider_permit``
    after the durable INVOKED transition. A plain construction, a
    ``dataclasses.replace`` copy, or a hand-built reconstruction lacks the
    closure sentinel and fails ``is_genuine_provider_permit``.
    """

    permit_id: str
    attempt_id: str
    campaign_id: str
    configuration_id: str
    issued_at: str
    consumed: bool = False
    permit_schema_version: str = PERMIT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        raise TypeError(
            "ProviderPermit cannot be constructed directly. It is produced "
            "only by issue_provider_permit after the durable INVOKED "
            "transition."
        )

    def to_dict(self) -> dict:
        return {
            "permit_schema_version": self.permit_schema_version,
            "permit_id": self.permit_id,
            "attempt_id": self.attempt_id,
            "campaign_id": self.campaign_id,
            "configuration_id": self.configuration_id,
            "issued_at": self.issued_at,
            "consumed": self.consumed,
        }


def _seal_permit_dataclass(cls: type) -> tuple:
    """Return ``(create, is_genuine)`` for ``ProviderPermit``.

    ``create`` bypasses ``__init__`` entirely via ``object.__new__`` and
    stamps a closure-held sentinel; ``is_genuine`` checks that sentinel by
    identity. A permit obtained any other way fails the check.
    """
    import dataclasses as _dc

    seal = object()
    field_defs = _dc.fields(cls)

    def create(**kwargs: Any) -> Any:
        obj = object.__new__(cls)
        for f in field_defs:
            if f.name in kwargs:
                value = kwargs[f.name]
            elif f.default is not _dc.MISSING:
                value = f.default
            elif f.default_factory is not _dc.MISSING:  # type: ignore[misc]
                value = f.default_factory()  # type: ignore[misc]
            else:
                raise TypeError(
                    f"{cls.__name__} requires field {f.name!r} but it was "
                    "not supplied to the sealed factory"
                )
            object.__setattr__(obj, f.name, value)
        object.__setattr__(obj, "_permit_seal", seal)
        return obj

    def is_genuine(obj: Any) -> bool:
        return isinstance(obj, cls) and getattr(obj, "_permit_seal", None) is seal

    return create, is_genuine


_create_provider_permit, _is_genuine_provider_permit = _seal_permit_dataclass(
    ProviderPermit
)


def _permit_path(campaign_root: Path, campaign_id: str, attempt_id: str) -> Path:
    return (
        Path(campaign_root) / campaign_id / "attempts" / attempt_id / PERMIT_FILENAME
    )


def _read_permit_file(path: Path) -> dict | None:
    if not path.is_file():
        return None
    import yaml

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else None


def _latest_state(events: list, attempt_id: str) -> str | None:
    latest: Optional[str] = None
    for e in events:
        if e.attempt_id == attempt_id and e.event_type in [
            s.value for s in AttemptState
        ]:
            latest = e.event_type
    return latest


def issue_provider_permit(
    *,
    campaign_root: Path,
    campaign_id: str,
    attempt_id: str,
    configuration_id: str,
    now: datetime | None = None,
) -> ProviderPermit:
    """Issue the one-shot provider permit for a durable, INVOKED attempt.

    Fails closed unless the append-only ledger shows the attempt's latest
    state is ``INVOKED`` -- i.e. the permit is created only AFTER the
    durable INVOKED transition, never before it. The registry record is
    written atomically under the campaign lock; a second issuance for the
    same attempt is rejected.
    """
    if now is None:
        now = datetime.now(UTC)
    campaign_dir = Path(campaign_root) / campaign_id
    ledger = CampaignLedger(campaign_dir, campaign_id)
    permit_file = _permit_path(campaign_root, campaign_id, attempt_id)

    with campaign_lock(campaign_dir):
        events = ledger.read_events()
        state = _latest_state(events, attempt_id)
        if state != AttemptState.INVOKED.value:
            raise CampaignAccountingError(
                PROVIDER_PERMIT_NOT_ISSUED,
                f"refusing to issue a provider permit for attempt "
                f"'{attempt_id}': its latest ledger state is '{state}' but "
                "a permit may be issued only after the durable INVOKED "
                "transition",
            )
        if permit_file.exists():
            raise CampaignAccountingError(
                PROVIDER_PERMIT_ALREADY_CONSUMED,
                f"attempt '{attempt_id}' already has a provider permit at "
                f"'{permit_file}'; one permit per attempt",
            )
        import hashlib
        import os

        permit = _create_provider_permit(
            permit_id=hashlib.sha256(os.urandom(32)).hexdigest(),
            attempt_id=attempt_id,
            campaign_id=campaign_id,
            configuration_id=configuration_id,
            issued_at=now.isoformat(),
            consumed=False,
        )
        temp_path = permit_file.with_name(f".tmp-{PERMIT_FILENAME}")
        import yaml

        with open(temp_path, "w", encoding="utf-8") as f:
            yaml.dump(permit.to_dict(), f, sort_keys=False)
            f.flush()
            import os as _os

            _os.fsync(f.fileno())
        temp_path.replace(permit_file)
        return permit


def consume_provider_permit(
    permit: ProviderPermit,
    *,
    campaign_root: Path,
) -> None:
    """Atomically mark the permit consumed (one-shot claim).

    The durable registry is the authority: the on-disk permit file must
    exist, agree with the object on every identity field, carry
    ``consumed: false``, and the ledger must still show the attempt as
    ``INVOKED``. The marker flip happens under the campaign lock and is
    never reversible: once consumed, no provider entry is possible with
    this permit again.
    """
    if not _is_genuine_provider_permit(permit):
        raise CampaignAccountingError(
            PROVIDER_PERMIT_NOT_GENUINE,
            "the supplied provider permit is not a genuine permit produced "
            "by issue_provider_permit (it may be a reconstruction or a "
            "permit-shaped object)",
        )
    campaign_dir = Path(campaign_root) / permit.campaign_id
    ledger = CampaignLedger(campaign_dir, permit.campaign_id)
    permit_file = _permit_path(campaign_root, permit.campaign_id, permit.attempt_id)

    with campaign_lock(campaign_dir):
        events = ledger.read_events()
        state = _latest_state(events, permit.attempt_id)
        if state != AttemptState.INVOKED.value:
            raise CampaignAccountingError(
                PROVIDER_PERMIT_NOT_ISSUED,
                f"cannot consume provider permit for attempt "
                f"'{permit.attempt_id}': its latest ledger state is "
                f"'{state}' (expected INVOKED)",
            )
        on_disk = _read_permit_file(permit_file)
        if on_disk is None:
            raise CampaignAccountingError(
                PROVIDER_PERMIT_NOT_ISSUED,
                f"provider permit for attempt '{permit.attempt_id}' has no "
                "registry record",
            )
        for field in ("permit_id", "attempt_id", "campaign_id", "configuration_id"):
            if on_disk.get(field) != getattr(permit, field):
                raise CampaignAccountingError(
                    PROVIDER_PERMIT_NOT_GENUINE,
                    f"on-disk provider permit disagrees with the supplied "
                    f"permit on '{field}'",
                )
        if on_disk.get("consumed") is True:
            raise CampaignAccountingError(
                PROVIDER_PERMIT_ALREADY_CONSUMED,
                f"provider permit '{permit.permit_id}' is already consumed",
            )
        import yaml

        updated = dict(on_disk)
        updated["consumed"] = True
        temp_path = permit_file.with_name(f".tmp-{PERMIT_FILENAME}")
        with open(temp_path, "w", encoding="utf-8") as f:
            yaml.dump(updated, f, sort_keys=False)
            f.flush()
            import os as _os

            _os.fsync(f.fileno())
        temp_path.replace(permit_file)


def is_genuine_provider_permit(
    permit: Any,
    *,
    campaign_root: Path,
) -> bool:
    """True iff ``permit`` is a genuine, registry-backed, one-shot permit
    currently usable at the provider boundary.

    Checks, all against the durable registry (never the in-memory object's
    own attributes):

    * the closure sentinel (object was produced by ``issue_provider_permit``);
    * the on-disk registry record exists and agrees on every identity field;
    * the on-disk record is marked ``consumed: true`` -- the boundary
      consumes the permit immediately before calling the provider, so a
      provider observed with an unconsumed registry record is a forged or
      misrouted object and is refused (the in-memory object's own flag is
      stale by design: the sealed object is immutable, so the registry
      file is the only consumption authority);
    * the ledger's latest state for the attempt is ``INVOKED`` -- a permit
      cannot be used before the durable INVOKED transition, and cannot be
      used after the attempt has moved to any other state.
    """
    if not _is_genuine_provider_permit(permit):
        return False
    if not isinstance(permit, ProviderPermit):
        return False
    on_disk = _read_permit_file(
        _permit_path(campaign_root, permit.campaign_id, permit.attempt_id)
    )
    if on_disk is None:
        return False
    for field in ("permit_id", "attempt_id", "campaign_id", "configuration_id"):
        if on_disk.get(field) != getattr(permit, field):
            return False
    if on_disk.get("consumed") is not True:
        return False
    campaign_dir = Path(campaign_root) / permit.campaign_id
    ledger = CampaignLedger(campaign_dir, permit.campaign_id)
    try:
        events = ledger.read_events()
    except CampaignAccountingError:
        return False
    return _latest_state(events, permit.attempt_id) == AttemptState.INVOKED.value


def require_usable_provider_permit(
    permit: Any,
    *,
    campaign_root: Path,
    attempt_id: str,
    campaign_id: str,
    configuration_id: str,
) -> None:
    """Fail closed unless ``permit`` is genuine, bound to the exact attempt,
    and already consumed by the boundary.

    This is the provider-side gate: it runs BEFORE any SDK import or client
    construction. ``campaign_root`` names the campaign ledger that issued
    the permit; every identity field must match the caller's invocation.
    """
    if permit is None:
        raise CampaignAccountingError(
            PROVIDER_PERMIT_REQUIRED,
            "no provider permit was supplied; a provider call requires a "
            "one-shot permit issued by the durable boundary after the "
            "durable INVOKED transition",
        )
    if not is_genuine_provider_permit(permit, campaign_root=campaign_root):
        raise CampaignAccountingError(
            PROVIDER_PERMIT_NOT_GENUINE,
            "the supplied provider permit is not a genuine, registry-backed, "
            "consumed permit for a currently-INVOKED attempt (it may be a "
            "forgery, a reconstruction, unconsumed, or stale)",
        )
    if permit.attempt_id != attempt_id:
        raise CampaignAccountingError(
            PROVIDER_PERMIT_ATTEMPT_MISMATCH,
            f"provider permit is bound to attempt '{permit.attempt_id}' "
            f"but the invocation is for attempt '{attempt_id}'",
        )
    if permit.campaign_id != campaign_id:
        raise CampaignAccountingError(
            PROVIDER_PERMIT_CAMPAIGN_MISMATCH,
            f"provider permit is bound to campaign '{permit.campaign_id}' "
            f"but the invocation is for campaign '{campaign_id}'",
        )
    if permit.configuration_id != configuration_id:
        raise CampaignAccountingError(
            PROVIDER_PERMIT_CONFIGURATION_MISMATCH,
            f"provider permit is bound to configuration "
            f"'{permit.configuration_id}' but the invocation is for "
            f"configuration '{configuration_id}'",
        )
