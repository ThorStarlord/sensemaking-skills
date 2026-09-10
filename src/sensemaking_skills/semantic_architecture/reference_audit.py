"""Bounded semantic-reference resolution over already-authoritative identities.

The audit answers only whether recorded references can be mechanically resolved
against authorities supplied by the caller. It never establishes semantic truth,
currentness, evidential support, decision relevance, or warranted work.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping


class ReferenceResolution(str, Enum):
    RESOLVED = "resolved"
    DANGLING = "dangling"
    AMBIGUOUS = "ambiguous"
    NOT_ADDRESSABLE = "not_addressable"


class ReferenceClass(str, Enum):
    CAMPAIGN_INTERNAL = "campaign_internal"
    LEGACY_OPAQUE = "legacy_opaque"
    UNKNOWN = "unknown"


class IntegrityEffect(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    INFORMATIONAL = "informational"


@dataclass(frozen=True)
class SemanticReferenceAuditItem:
    entry_id: str
    field: str
    reference: str
    resolution: ReferenceResolution
    reference_class: ReferenceClass
    integrity_effect: IntegrityEffect
    resolver: str
    detail: str = ""


@dataclass(frozen=True)
class SemanticReferenceAuditResult:
    items: tuple[SemanticReferenceAuditItem, ...]
    resolved_count: int
    dangling_count: int
    ambiguous_count: int
    not_addressable_count: int
    integrity_failure_count: int
    integrity_ok: bool
    semantic_truth_established: bool = False


_CAMPAIGN_LOCAL_PREFIXES = ("evidence/", "artifacts/", "admissions/")


def _entry_mapping(record: Mapping[str, Any]) -> Mapping[str, Any]:
    entry = record.get("entry")
    return entry if isinstance(entry, Mapping) else record


def _legacy_path_like(reference: str) -> bool:
    return "/" not in reference and "\\" not in reference and "." in reference


def _item(
    *,
    entry_id: str,
    field: str,
    reference: str,
    resolution: ReferenceResolution,
    reference_class: ReferenceClass,
    resolver: str,
    detail: str = "",
) -> SemanticReferenceAuditItem:
    effect = (
        IntegrityEffect.FAIL
        if resolution in {ReferenceResolution.DANGLING, ReferenceResolution.AMBIGUOUS}
        else IntegrityEffect.PASS
        if resolution is ReferenceResolution.RESOLVED
        else IntegrityEffect.INFORMATIONAL
    )
    return SemanticReferenceAuditItem(
        entry_id=entry_id,
        field=field,
        reference=reference,
        resolution=resolution,
        reference_class=reference_class,
        integrity_effect=effect,
        resolver=resolver,
        detail=detail,
    )


def _audit_artifact_ref(
    *,
    entry_id: str,
    reference: str,
    campaign_evidence_refs: set[str] | None,
) -> SemanticReferenceAuditItem:
    if campaign_evidence_refs is None:
        return _item(
            entry_id=entry_id,
            field="artifact_ref",
            reference=reference,
            resolution=ReferenceResolution.NOT_ADDRESSABLE,
            reference_class=(
                ReferenceClass.LEGACY_OPAQUE if _legacy_path_like(reference) else ReferenceClass.UNKNOWN
            ),
            resolver="none",
            detail="no Campaign evidence authority was supplied",
        )

    admitted_artifact_refs = {
        value for value in campaign_evidence_refs if value.startswith("artifacts/")
    }
    if reference in admitted_artifact_refs:
        return _item(
            entry_id=entry_id,
            field="artifact_ref",
            reference=reference,
            resolution=ReferenceResolution.RESOLVED,
            reference_class=ReferenceClass.CAMPAIGN_INTERNAL,
            resolver="campaign.evidence_refs",
            detail="artifact ref is exposed by Campaign evidence only after admission",
        )
    if reference.startswith("artifacts/"):
        return _item(
            entry_id=entry_id,
            field="artifact_ref",
            reference=reference,
            resolution=ReferenceResolution.DANGLING,
            reference_class=ReferenceClass.CAMPAIGN_INTERNAL,
            resolver="campaign.evidence_refs",
            detail="Campaign-local artifact ref is not present in authoritative admitted evidence",
        )
    return _item(
        entry_id=entry_id,
        field="artifact_ref",
        reference=reference,
        resolution=ReferenceResolution.NOT_ADDRESSABLE,
        reference_class=(
            ReferenceClass.LEGACY_OPAQUE if _legacy_path_like(reference) else ReferenceClass.UNKNOWN
        ),
        resolver="none",
        detail="artifact ref is outside the currently addressable admitted-artifact namespace",
    )


def _audit_evidence_ref(
    *,
    entry_id: str,
    field: str,
    reference: str,
    campaign_evidence_refs: set[str] | None,
) -> SemanticReferenceAuditItem:
    if campaign_evidence_refs is None:
        return _item(
            entry_id=entry_id,
            field=field,
            reference=reference,
            resolution=ReferenceResolution.NOT_ADDRESSABLE,
            reference_class=ReferenceClass.UNKNOWN,
            resolver="none",
            detail="no Campaign evidence authority was supplied",
        )
    if reference in campaign_evidence_refs:
        return _item(
            entry_id=entry_id,
            field=field,
            reference=reference,
            resolution=ReferenceResolution.RESOLVED,
            reference_class=ReferenceClass.CAMPAIGN_INTERNAL,
            resolver="campaign.evidence_refs",
        )
    if reference.startswith(_CAMPAIGN_LOCAL_PREFIXES):
        return _item(
            entry_id=entry_id,
            field=field,
            reference=reference,
            resolution=ReferenceResolution.DANGLING,
            reference_class=ReferenceClass.CAMPAIGN_INTERNAL,
            resolver="campaign.evidence_refs",
            detail="reference uses a Campaign-local evidence path but is absent from authoritative evidence",
        )
    return _item(
        entry_id=entry_id,
        field=field,
        reference=reference,
        resolution=ReferenceResolution.NOT_ADDRESSABLE,
        reference_class=ReferenceClass.UNKNOWN,
        resolver="none",
        detail="no authoritative address space is defined for this evidence reference",
    )


def _audit_unaddressable(
    *,
    entry_id: str,
    field: str,
    reference: str,
    legacy_path_like: bool = False,
) -> SemanticReferenceAuditItem:
    return _item(
        entry_id=entry_id,
        field=field,
        reference=reference,
        resolution=ReferenceResolution.NOT_ADDRESSABLE,
        reference_class=(
            ReferenceClass.LEGACY_OPAQUE
            if legacy_path_like and _legacy_path_like(reference)
            else ReferenceClass.UNKNOWN
        ),
        resolver="none",
        detail="B7 v0 has no authoritative resolver for this reference family",
    )


def audit_semantic_references(
    records: Iterable[Mapping[str, Any]],
    *,
    campaign_evidence_refs: Iterable[str] | None = None,
    active_uncertainty_ids: Iterable[str] | None = None,
) -> SemanticReferenceAuditResult:
    """Audit outbound semantic references without inventing missing namespaces.

    ``None`` means an authority is unavailable. An empty iterable means the
    authority is available and currently exposes no identities.
    """

    rows = tuple(_entry_mapping(record) for record in records)
    evidence_refs = (
        None if campaign_evidence_refs is None else set(campaign_evidence_refs)
    )
    uncertainty_ids = (
        None if active_uncertainty_ids is None else set(active_uncertainty_ids)
    )

    items: list[SemanticReferenceAuditItem] = []
    seen_entry_ids: set[str] = set()

    for entry in rows:
        raw_entry_id = entry.get("entry_id")
        entry_id = raw_entry_id if isinstance(raw_entry_id, str) else ""

        artifact_ref = entry.get("artifact_ref")
        if isinstance(artifact_ref, str) and artifact_ref:
            items.append(
                _audit_artifact_ref(
                    entry_id=entry_id,
                    reference=artifact_ref,
                    campaign_evidence_refs=evidence_refs,
                )
            )

        raw_evidence_refs = entry.get("evidence_refs", ())
        if isinstance(raw_evidence_refs, (list, tuple)):
            for index, reference in enumerate(raw_evidence_refs):
                if isinstance(reference, str) and reference:
                    items.append(
                        _audit_evidence_ref(
                            entry_id=entry_id,
                            field=f"evidence_refs[{index}]",
                            reference=reference,
                            campaign_evidence_refs=evidence_refs,
                        )
                    )

        raw_claim_refs = entry.get("claim_refs", ())
        if isinstance(raw_claim_refs, (list, tuple)):
            for index, reference in enumerate(raw_claim_refs):
                if isinstance(reference, str) and reference:
                    items.append(
                        _audit_unaddressable(
                            entry_id=entry_id,
                            field=f"claim_refs[{index}]",
                            reference=reference,
                        )
                    )

        raw_uncertainty_refs = entry.get("uncertainty_refs", ())
        if isinstance(raw_uncertainty_refs, (list, tuple)):
            for index, reference in enumerate(raw_uncertainty_refs):
                if not isinstance(reference, str) or not reference:
                    continue
                if uncertainty_ids is not None and reference in uncertainty_ids:
                    items.append(
                        _item(
                            entry_id=entry_id,
                            field=f"uncertainty_refs[{index}]",
                            reference=reference,
                            resolution=ReferenceResolution.RESOLVED,
                            reference_class=ReferenceClass.CAMPAIGN_INTERNAL,
                            resolver="campaign.active_uncertainty",
                        )
                    )
                else:
                    items.append(
                        _audit_unaddressable(
                            entry_id=entry_id,
                            field=f"uncertainty_refs[{index}]",
                            reference=reference,
                        )
                    )

        profile_ref = entry.get("semantic_profile_ref")
        if isinstance(profile_ref, str) and profile_ref:
            items.append(
                _audit_unaddressable(
                    entry_id=entry_id,
                    field="semantic_profile_ref",
                    reference=profile_ref,
                    legacy_path_like=True,
                )
            )

        raw_parents = entry.get("parent_entry_ids", ())
        if isinstance(raw_parents, (list, tuple)):
            for index, reference in enumerate(raw_parents):
                if not isinstance(reference, str) or not reference:
                    continue
                if reference in seen_entry_ids:
                    items.append(
                        _item(
                            entry_id=entry_id,
                            field=f"parent_entry_ids[{index}]",
                            reference=reference,
                            resolution=ReferenceResolution.RESOLVED,
                            reference_class=ReferenceClass.CAMPAIGN_INTERNAL,
                            resolver="semantic_state.entry_id",
                        )
                    )
                else:
                    items.append(
                        _item(
                            entry_id=entry_id,
                            field=f"parent_entry_ids[{index}]",
                            reference=reference,
                            resolution=ReferenceResolution.DANGLING,
                            reference_class=ReferenceClass.CAMPAIGN_INTERNAL,
                            resolver="semantic_state.entry_id",
                            detail="parent reference does not resolve to a prior semantic-state entry",
                        )
                    )

        if entry_id:
            seen_entry_ids.add(entry_id)

    resolved_count = sum(
        item.resolution is ReferenceResolution.RESOLVED for item in items
    )
    dangling_count = sum(
        item.resolution is ReferenceResolution.DANGLING for item in items
    )
    ambiguous_count = sum(
        item.resolution is ReferenceResolution.AMBIGUOUS for item in items
    )
    not_addressable_count = sum(
        item.resolution is ReferenceResolution.NOT_ADDRESSABLE for item in items
    )
    integrity_failure_count = sum(
        item.integrity_effect is IntegrityEffect.FAIL for item in items
    )

    return SemanticReferenceAuditResult(
        items=tuple(items),
        resolved_count=resolved_count,
        dangling_count=dangling_count,
        ambiguous_count=ambiguous_count,
        not_addressable_count=not_addressable_count,
        integrity_failure_count=integrity_failure_count,
        integrity_ok=integrity_failure_count == 0,
        semantic_truth_established=False,
    )
