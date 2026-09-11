"""Deterministic Campaign observability, replay, resume, graph, and bundle CLI.

These commands project or transport durable state. They never infer a next
responsibility, rank evidence, or make a semantic recommendation.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable

import click

from .campaign_semantics import ContractError, canonicalize, target_snapshot_sha256
from .campaigns import CampaignService, CampaignWorkspaceError
from .campaigns.bundle import CampaignBundleService
from .semantic_architecture import (
    IntegrityEffect,
    SemanticStateEntry,
    SemanticStateStore,
    audit_semantic_references,
    to_dict as semantic_to_dict,
)

SEMANTIC_STATE_FILENAME = "semantic-state.jsonl"


def _enum(value: Any) -> Any:
    return value.value if value is not None and hasattr(value, "value") else value


def _find_transition(snapshot: Any, transition_id: str) -> Any:
    for transition in snapshot.transitions:
        if transition.id == transition_id:
            return transition
    raise click.ClickException(f"unknown transition id: {transition_id}")


def _changed_fields(left: dict[str, Any], right: dict[str, Any]) -> dict[str, dict[str, Any]]:
    changes: dict[str, dict[str, Any]] = {}
    for key in sorted(set(left) | set(right)):
        if left.get(key) != right.get(key):
            changes[key] = {"from": left.get(key), "to": right.get(key)}
    return changes


def _mermaid_id(value: str) -> str:
    return "N_" + re.sub(r"[^A-Za-z0-9_]", "_", value)


def _semantic_store(workspace: Path) -> SemanticStateStore:
    return SemanticStateStore(workspace / SEMANTIC_STATE_FILENAME)


def _semantic_summary(workspace: Path) -> dict[str, Any]:
    records, diagnostics = _semantic_store(workspace).load_raw()
    latest = records[-1]["entry"] if records else None
    return {
        "present": bool(records) or (workspace / SEMANTIC_STATE_FILENAME).exists(),
        "valid": not diagnostics,
        "entry_count": len(records),
        "latest_entry": latest,
        "diagnostics": [canonicalize(item) for item in diagnostics],
        "schema_in_campaign_state": False,
        "semantic_truth_established": False,
    }


def _campaign_target_ref(snapshot: Any) -> str | None:
    target = snapshot.state.target_snapshot
    if target is None:
        return None
    return f"target-snapshot-sha256:{target_snapshot_sha256(target)}"


def _campaign_reference_audit(snapshot: Any, records: list[dict[str, Any]]):
    active_uncertainty_ids: tuple[str, ...] = ()
    if snapshot.state.active_uncertainty is not None:
        active_uncertainty_ids = (snapshot.state.active_uncertainty.id,)
    return audit_semantic_references(
        records,
        campaign_evidence_refs=snapshot.evidence_refs,
        active_uncertainty_ids=active_uncertainty_ids,
        campaign_target_ref=_campaign_target_ref(snapshot),
    )


def register_campaign_observability_commands(
    campaign_group: click.Group,
    *,
    emit_error: Callable[..., None],
    json_echo: Callable[[dict[str, Any]], None],
) -> None:
    def resume(workspace: Path, output_json: bool):
        try:
            return CampaignService(workspace).resume()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
        raise AssertionError("unreachable")

    @campaign_group.command(name="inspect")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def campaign_inspect(workspace: Path, output_json: bool) -> None:
        """Project the full mechanically reconstructible Campaign snapshot."""
        snapshot = resume(workspace, output_json)
        payload = {
            "ok": True,
            "code": "CAMPAIGN_INSPECT",
            "state": canonicalize(snapshot.state),
            "transitions": [canonicalize(item) for item in snapshot.transitions],
            "evidence_refs": list(snapshot.evidence_refs),
            "policy": canonicalize(snapshot.policy) if snapshot.policy is not None else None,
            "handoff": canonicalize(snapshot.handoff) if snapshot.handoff is not None else None,
            "semantic_companion": _semantic_summary(workspace),
            "semantic_recommendation_included": False,
            "semantic_truth_established": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @campaign_group.command(name="explain")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--ref", "reference", required=True, help="Exact durable id/ref to trace")
    @click.option("--json", "output_json", is_flag=True)
    def campaign_explain(workspace: Path, reference: str, output_json: bool) -> None:
        """Explain deterministic provenance for an exact durable reference."""
        snapshot = resume(workspace, output_json)
        matches: list[dict[str, Any]] = []
        state = snapshot.state
        if state.active_responsibility is not None and state.active_responsibility.id == reference:
            matches.append({"kind": "active_responsibility", "value": canonicalize(state.active_responsibility)})
        if state.active_uncertainty is not None and state.active_uncertainty.id == reference:
            matches.append({"kind": "active_uncertainty", "value": canonicalize(state.active_uncertainty)})
        for item in state.deferred_responsibilities:
            if item.responsibility_id == reference:
                matches.append({"kind": "deferred_responsibility", "value": canonicalize(item)})
        for transition in snapshot.transitions:
            if transition.id == reference:
                matches.append({"kind": "transition", "value": canonicalize(transition)})
            if reference in transition.evidence:
                matches.append({"kind": "transition_evidence_use", "transition_id": transition.id})
        if reference in snapshot.evidence_refs:
            matches.append({"kind": "evidence_ref", "value": reference})
        for index, event in enumerate(snapshot.trace.events):
            if isinstance(event, dict) and reference in {str(value) for value in event.values()}:
                matches.append({"kind": "trace_event", "index": index, "value": dict(event)})

        semantic_records, semantic_diagnostics = _semantic_store(workspace).load_raw()
        for record in semantic_records:
            entry = record["entry"]
            if entry.get("entry_id") == reference:
                matches.append({"kind": "semantic_state_entry", "value": entry, "entry_digest": record.get("entry_digest")})
            for field, kind in (
                ("artifact_ref", "semantic_artifact_ref"),
                ("target_ref", "semantic_target_ref"),
                ("semantic_profile_ref", "semantic_profile_ref"),
            ):
                if entry.get(field) == reference:
                    matches.append({"kind": kind, "entry_id": entry.get("entry_id")})
            for field, kind in (
                ("evidence_refs", "semantic_evidence_ref"),
                ("claim_refs", "semantic_claim_ref"),
                ("uncertainty_refs", "semantic_uncertainty_ref"),
            ):
                if reference in entry.get(field, []):
                    matches.append({"kind": kind, "entry_id": entry.get("entry_id")})

        reference_audit_items = []
        if not semantic_diagnostics:
            audit = _campaign_reference_audit(snapshot, semantic_records)
            reference_audit_items = [
                item for item in audit.items if item.reference == reference
            ]
        reference_integrity_ok = (
            None
            if not reference_audit_items
            else not any(
                item.integrity_effect is IntegrityEffect.FAIL
                for item in reference_audit_items
            )
        )

        payload = {
            "ok": bool(matches) and not semantic_diagnostics,
            "code": "CAMPAIGN_REFERENCE_EXPLAINED" if matches else "CAMPAIGN_REFERENCE_NOT_FOUND",
            "reference": reference,
            "matches": matches,
            "reference_audit": [semantic_to_dict(item) for item in reference_audit_items],
            "reference_integrity_ok": reference_integrity_ok,
            "semantic_companion_diagnostics": [canonicalize(item) for item in semantic_diagnostics],
            "semantic_recommendation_included": False,
            "semantic_truth_established": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not matches:
            raise click.exceptions.Exit(2)
        if semantic_diagnostics:
            raise click.exceptions.Exit(3)

    @campaign_group.command(name="diff")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--from-transition", "from_id", required=True)
    @click.option("--to-transition", "to_id", required=True)
    @click.option("--json", "output_json", is_flag=True)
    def campaign_diff(workspace: Path, from_id: str, to_id: str, output_json: bool) -> None:
        """Mechanically compare two durable transition records."""
        snapshot = resume(workspace, output_json)
        left = canonicalize(_find_transition(snapshot, from_id))
        right = canonicalize(_find_transition(snapshot, to_id))
        payload = {
            "ok": True,
            "code": "CAMPAIGN_TRANSITION_DIFF",
            "from_transition": from_id,
            "to_transition": to_id,
            "changed_fields": _changed_fields(left, right),
            "semantic_recommendation_included": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @campaign_group.command(name="semantic-state-append")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--entry-id", required=True)
    @click.option("--source-skill", required=True)
    @click.option("--artifact-ref", required=True)
    @click.option(
        "--target-ref",
        default=None,
        help="Required for targetless Campaigns; bound repository Campaigns derive and enforce their current TargetSnapshot digest",
    )
    @click.option("--profile-ref", default=None)
    @click.option("--evidence-ref", "evidence_refs", multiple=True)
    @click.option("--claim-ref", "claim_refs", multiple=True)
    @click.option("--uncertainty-ref", "uncertainty_refs", multiple=True)
    @click.option("--parent", "parent_entry_ids", multiple=True)
    @click.option("--note", "notes", multiple=True)
    @click.option("--json", "output_json", is_flag=True)
    def campaign_semantic_state_append(
        workspace: Path,
        entry_id: str,
        source_skill: str,
        artifact_ref: str,
        target_ref: str | None,
        profile_ref: str | None,
        evidence_refs: tuple[str, ...],
        claim_refs: tuple[str, ...],
        uncertainty_refs: tuple[str, ...],
        parent_entry_ids: tuple[str, ...],
        notes: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Append companion semantic refs bound to current Campaign target when present."""
        snapshot = resume(workspace, output_json)
        bound_target = _campaign_target_ref(snapshot)
        if bound_target is not None:
            if target_ref is not None and target_ref != bound_target:
                raise click.ClickException(
                    "--target-ref does not match the Campaign's current TargetSnapshot digest"
                )
            resolved_target = bound_target
        else:
            if target_ref is None or not target_ref.strip():
                raise click.ClickException(
                    "--target-ref is required when the Campaign has no bound TargetSnapshot"
                )
            resolved_target = target_ref.strip()
        try:
            digest = _semantic_store(workspace).append(
                SemanticStateEntry(
                    entry_id=entry_id,
                    source_skill=source_skill,
                    artifact_ref=artifact_ref,
                    target_ref=resolved_target,
                    semantic_profile_ref=profile_ref,
                    evidence_refs=evidence_refs,
                    claim_refs=claim_refs,
                    uncertainty_refs=uncertainty_refs,
                    parent_entry_ids=parent_entry_ids,
                    notes=notes,
                )
            )
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = {
            "ok": True,
            "code": "CAMPAIGN_SEMANTIC_STATE_APPENDED",
            "entry_id": entry_id,
            "entry_digest": digest,
            "target_ref": resolved_target,
            "campaign_schema_changed": False,
            "semantic_truth_established": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True))

    @campaign_group.command(name="semantic-state")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def campaign_semantic_state(workspace: Path, output_json: bool) -> None:
        """Show/validate the optional Campaign semantic companion chain and refs."""
        snapshot = resume(workspace, output_json)
        records, diagnostics = _semantic_store(workspace).load_raw()
        audit = None if diagnostics else _campaign_reference_audit(snapshot, records)
        reference_integrity_failed = audit is not None and not audit.integrity_ok
        if diagnostics:
            code = "CAMPAIGN_SEMANTIC_STATE_INVALID"
        elif reference_integrity_failed:
            code = "CAMPAIGN_SEMANTIC_STATE_REFERENCE_INTEGRITY_FAILED"
        else:
            code = "CAMPAIGN_SEMANTIC_STATE_VALID"
        payload = {
            "ok": not diagnostics and not reference_integrity_failed,
            "code": code,
            "records": records,
            "diagnostics": [canonicalize(item) for item in diagnostics],
            "reference_audit": semantic_to_dict(audit) if audit is not None else None,
            "campaign_schema_changed": False,
            "semantic_truth_established": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if diagnostics or reference_integrity_failed:
            raise click.exceptions.Exit(3)

    @campaign_group.command(name="resume-context")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--recent-transitions", type=click.IntRange(0, 50), default=5, show_default=True)
    @click.option("--json", "output_json", is_flag=True)
    def campaign_resume_context(workspace: Path, recent_transitions: int, output_json: bool) -> None:
        """Emit a deterministic fresh-context capsule from durable Campaign state."""
        snapshot = resume(workspace, output_json)
        state = snapshot.state
        recent = snapshot.transitions[-recent_transitions:] if recent_transitions else ()
        payload = {
            "ok": True,
            "code": "CAMPAIGN_RESUME_CONTEXT",
            "campaign_id": state.campaign_id,
            "mission": state.mission,
            "status": state.status,
            "current_state": state.current_state,
            "target_snapshot": canonicalize(state.target_snapshot) if state.target_snapshot is not None else None,
            "active_responsibility": canonicalize(state.active_responsibility) if state.active_responsibility is not None else None,
            "active_uncertainty": canonicalize(state.active_uncertainty) if state.active_uncertainty is not None else None,
            "authority": _enum(state.authority),
            "terminal_state": _enum(state.terminal_state),
            "established_facts": list(state.established_facts),
            "resolved_questions": list(state.resolved_questions),
            "deferred_responsibilities": [canonicalize(item) for item in state.deferred_responsibilities],
            "external_boundaries": [canonicalize(item) for item in state.external_boundaries],
            "evidence_refs": list(snapshot.evidence_refs),
            "recent_transitions": [canonicalize(item) for item in recent],
            "handoff": canonicalize(snapshot.handoff) if snapshot.handoff is not None else None,
            "semantic_companion": _semantic_summary(workspace),
            "semantic_recommendation_included": False,
            "explicit_limit": "This capsule reconstructs durable declared state and optional companion semantic refs; it does not decide the next warranted action.",
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo("CAMPAIGN_RESUME_CONTEXT")
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @campaign_group.command(name="replay")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--at-transition", required=True)
    @click.option("--json", "output_json", is_flag=True)
    def campaign_replay(workspace: Path, at_transition: str, output_json: bool) -> None:
        """Replay trace order through a transition without inventing historic state fields."""
        snapshot = resume(workspace, output_json)
        prefix = []
        cumulative_evidence: list[str] = []
        found = False
        for transition in snapshot.transitions:
            prefix.append(canonicalize(transition))
            cumulative_evidence.extend(transition.evidence)
            if transition.id == at_transition:
                found = True
                break
        if not found:
            raise click.ClickException(f"unknown transition id: {at_transition}")
        cursor = prefix[-1]
        payload = {
            "ok": True,
            "code": "CAMPAIGN_REPLAY_CURSOR",
            "campaign_id": snapshot.state.campaign_id,
            "at_transition": at_transition,
            "state_label_at_cursor": cursor["to_state"],
            "transition_prefix": prefix,
            "cumulative_evidence_refs": sorted(set(cumulative_evidence)),
            "historic_full_state_reconstructed": False,
            "explicit_limit": "Campaign v2 stores transition lineage, not a full state snapshot after every transition.",
            "semantic_recommendation_included": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @campaign_group.command(name="graph")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--format", "output_format", type=click.Choice(["json", "mermaid"]), default="json", show_default=True)
    def campaign_graph(workspace: Path, output_format: str) -> None:
        """Render deterministic provenance edges between Campaign records."""
        snapshot = resume(workspace, output_json=(output_format == "json"))
        nodes: dict[str, dict[str, str]] = {}
        edges: list[dict[str, str]] = []
        campaign_id = snapshot.state.campaign_id
        nodes[campaign_id] = {"id": campaign_id, "kind": "campaign", "label": campaign_id}
        previous: str | None = None
        for transition in snapshot.transitions:
            nodes[transition.id] = {"id": transition.id, "kind": "transition", "label": transition.id}
            edges.append({"from": campaign_id, "to": transition.id, "relation": "contains_transition"})
            if previous is not None:
                edges.append({"from": previous, "to": transition.id, "relation": "followed_by"})
            previous = transition.id
            for evidence in transition.evidence:
                nodes.setdefault(evidence, {"id": evidence, "kind": "evidence", "label": evidence})
                edges.append({"from": transition.id, "to": evidence, "relation": "references_evidence"})

        semantic_records, semantic_diagnostics = _semantic_store(workspace).load_raw()
        for record in semantic_records:
            entry = record["entry"]
            entry_id = str(entry.get("entry_id"))
            nodes[entry_id] = {"id": entry_id, "kind": "semantic_state_entry", "label": entry_id}
            edges.append({"from": campaign_id, "to": entry_id, "relation": "has_semantic_companion_entry"})
            for parent in entry.get("parent_entry_ids", []):
                edges.append({"from": str(parent), "to": entry_id, "relation": "semantic_parent_of"})
            artifact = entry.get("artifact_ref")
            if isinstance(artifact, str) and artifact:
                nodes.setdefault(artifact, {"id": artifact, "kind": "artifact_ref", "label": artifact})
                edges.append({"from": entry_id, "to": artifact, "relation": "references_artifact"})

        if output_format == "json":
            json_echo(
                {
                    "ok": not semantic_diagnostics,
                    "code": "CAMPAIGN_PROVENANCE_GRAPH",
                    "nodes": list(nodes.values()),
                    "edges": edges,
                    "semantic_companion_diagnostics": [canonicalize(item) for item in semantic_diagnostics],
                    "semantic_truth_established": False,
                }
            )
            if semantic_diagnostics:
                raise click.exceptions.Exit(3)
            return
        if semantic_diagnostics:
            raise click.ClickException("semantic companion state is invalid; refuse to render provenance graph")
        click.echo("graph TD")
        for node in nodes.values():
            click.echo(f'  {_mermaid_id(node["id"])}["{node["label"].replace(chr(34), chr(39))}"]')
        for edge in edges:
            click.echo(
                f'  {_mermaid_id(edge["from"])} -->|{edge["relation"]}| {_mermaid_id(edge["to"])}'
            )

    @campaign_group.command(name="bundle-export")
    @click.option("--workspace", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--output", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def campaign_bundle_export(workspace: Path, output: Path, output_json: bool) -> None:
        """Export exact workspace bytes into a deterministic integrity bundle."""
        try:
            path = CampaignBundleService(workspace).export(output)
        except (OSError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc
        verification = CampaignBundleService.verify(path)
        payload = {
            "ok": verification.valid,
            "code": "CAMPAIGN_BUNDLE_EXPORTED",
            "bundle": str(path),
            "file_count": verification.file_count,
            "semantic_truth_established": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True))

    @campaign_group.command(name="bundle-verify")
    @click.option("--bundle", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def campaign_bundle_verify(bundle: Path, output_json: bool) -> None:
        """Verify bundle path safety, manifest shape, sizes, and SHA-256 bindings."""
        verification = CampaignBundleService.verify(bundle)
        payload = {
            "ok": verification.valid,
            "code": "CAMPAIGN_BUNDLE_VALID" if verification.valid else "CAMPAIGN_BUNDLE_INVALID",
            "file_count": verification.file_count,
            "format_version": verification.format_version,
            "diagnostics": [canonicalize(item) for item in verification.diagnostics],
            "semantic_truth_established": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True))
        if not verification.valid:
            raise click.exceptions.Exit(3)

    @campaign_group.command(name="bundle-import")
    @click.option("--bundle", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def campaign_bundle_import(bundle: Path, workspace: Path, output_json: bool) -> None:
        """Import a verified byte-exact bundle into a new workspace path."""
        try:
            target = CampaignBundleService.import_bundle(bundle, workspace)
        except (OSError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc
        payload = {
            "ok": True,
            "code": "CAMPAIGN_BUNDLE_IMPORTED",
            "workspace": str(target),
            "semantic_truth_established": False,
            "explicit_limit": "Bundle integrity does not prove target availability or semantic correctness.",
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True))
