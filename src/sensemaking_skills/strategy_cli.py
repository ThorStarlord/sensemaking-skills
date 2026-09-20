"""Deterministic projections for strategic_repository_analysis artifacts.

These commands inspect already-authored strategic analyses. They do not generate
strategy, rank paths, infer owner intent, or authorize implementation.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

import click
import yaml


def _extract_machine_block(content: str) -> dict[str, Any]:
    blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
    for block in reversed(blocks):
        try:
            value = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(value, dict) and value.get("artifact_id") == "strategic_repository_analysis":
            return value
    raise click.ClickException(
        "No strategic_repository_analysis YAML machine block was found."
    )


def _load_analysis(path: Path) -> dict[str, Any]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise click.ClickException(str(exc)) from exc
    return _extract_machine_block(content)


def _json_echo(payload: dict[str, Any]) -> None:
    click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))


def _analysis_ref(data: dict[str, Any], path: Path) -> str:
    explicit = data.get("analysis_ref")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip()
    identity = str(data.get("target_source_identity") or "unknown")
    return f"{path.name}@{identity}"


def _normalize_assumptions(data: dict[str, Any]) -> list[dict[str, Any]]:
    assumptions = data.get("decision_assumptions", [])
    if not isinstance(assumptions, list):
        return []
    return [item for item in assumptions if isinstance(item, dict)]


def _continuity(data: dict[str, Any]) -> dict[str, Any] | None:
    value = data.get("continuity")
    return value if isinstance(value, dict) else None


def _git_head(repo: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    head = result.stdout.strip()
    return head or None


def _identity_sha(identity: Any) -> str | None:
    if not isinstance(identity, str):
        return None
    value = identity.strip()
    if "@" in value:
        candidate = value.rsplit("@", 1)[-1]
    elif value.startswith("sha:"):
        candidate = value[4:]
    else:
        candidate = value
    if re.fullmatch(r"[0-9a-fA-F]{7,40}", candidate):
        return candidate.lower()
    return None


def _evidence_paths(data: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for capability in data.get("capability_states", []) or []:
        if not isinstance(capability, dict):
            continue
        for ref in capability.get("evidence_refs", []) or []:
            if isinstance(ref, str):
                refs.append(ref)
    for assumption in _normalize_assumptions(data):
        for ref in assumption.get("evidence_refs", []) or []:
            if isinstance(ref, str):
                refs.append(ref)
    return refs


def _governing_authority_paths(data: dict[str, Any]) -> list[str]:
    refs = data.get("governing_authority_refs", [])
    if not isinstance(refs, list):
        return []
    return [ref for ref in refs if isinstance(ref, str)]


def _git_file_bytes(repo: Path, revision: str, path: str) -> bytes | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "show", f"{revision}:{path}"],
            check=True,
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    return result.stdout


def _extract_supported_strategy_artifact(content: str) -> dict[str, Any]:
    supported = {"strategic_repository_analysis", "strategic_reconciliation"}
    blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
    for block in reversed(blocks):
        try:
            value = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(value, dict) and value.get("artifact_id") in supported:
            return value
    raise click.ClickException(
        "No supported strategic_repository_analysis or strategic_reconciliation YAML block was found."
    )


def _load_supported_strategy_artifact(path: Path) -> dict[str, Any]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise click.ClickException(str(exc)) from exc
    return _extract_supported_strategy_artifact(content)


def _local_ref_path(ref: str) -> str | None:
    value = ref.strip()
    if not value or value.startswith(("http://", "https://")):
        return None
    if value.lower().startswith(("issue #", "pr #", "run ")):
        return None
    value = re.sub(r":L\d+(?:-L\d+)?$", "", value)
    value = value.split("#", 1)[0]
    if not value or value.startswith("/"):
        return None
    if "/" not in value and "." not in value:
        return None
    return value


def _capability_map(data: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in data.get("capability_states", []) or []:
        if isinstance(item, dict):
            cid = item.get("capability_id")
            state = item.get("state")
            if isinstance(cid, str) and isinstance(state, str):
                result[cid] = state
    return result


def _path_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in data.get("construction_paths", []) or []:
        if isinstance(item, dict) and isinstance(item.get("path_id"), str):
            result[item["path_id"]] = item
    return result


def _path_transition_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in data.get("construction_paths", []) or []:
        if not isinstance(path, dict) or not isinstance(path.get("path_id"), str):
            continue
        for transition in path.get("path_transitions", []) or []:
            if not isinstance(transition, dict):
                continue
            ref = transition.get("transition_ref")
            statement = transition.get("transition")
            if isinstance(ref, str) and isinstance(statement, str):
                result[ref] = {
                    "transition_ref": ref,
                    "transition": statement,
                    "path_id": path["path_id"],
                }
    return result


def _mermaid_id(prefix: str, value: Any) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_]", "_", str(value))
    return f"{prefix}_{normalized}"


def _mermaid_label(value: Any) -> str:
    return str(value).replace('"', "'").replace("\n", " ")


@click.group(name="strategy")
def strategy_group() -> None:
    """Inspect authored strategic-analysis artifacts without selecting strategy."""


@strategy_group.command(name="inspect")
@click.option(
    "--artifact",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def inspect_analysis(artifact: Path, output_json: bool) -> None:
    """Project the declared strategic state from one analysis artifact."""
    data = _load_analysis(artifact)
    payload = {
        "ok": True,
        "code": "STRATEGY_ANALYSIS_INSPECT",
        "analysis_ref": _analysis_ref(data, artifact),
        "target_repository": data.get("target_repository"),
        "target_source_identity": data.get("target_source_identity"),
        "strategic_disposition": data.get("strategic_disposition"),
        "selected_path_id": data.get("selected_path_id"),
        "candidate_repository_responsibility": data.get(
            "candidate_repository_responsibility"
        ),
        "capability_count": len(data.get("capability_states", []) or []),
        "frontier_count": len(data.get("strategic_frontier", []) or []),
        "path_count": len(data.get("construction_paths", []) or []),
        "assumption_count": len(_normalize_assumptions(data)),
        "continuity": _continuity(data),
        "mechanical_projection_only": True,
        "strategy_selected_by_command": False,
        "implementation_authorized_by_command": False,
    }
    if output_json:
        _json_echo(payload)
        return
    click.echo("STRATEGY_ANALYSIS_INSPECT")
    click.echo(f"Analysis: {payload['analysis_ref']}")
    click.echo(f"Target: {payload['target_repository']}")
    click.echo(f"Source identity: {payload['target_source_identity']}")
    click.echo(f"Disposition: {payload['strategic_disposition']}")
    click.echo(f"Selected path: {payload['selected_path_id'] or 'none'}")
    click.echo(f"Capabilities: {payload['capability_count']}")
    click.echo(f"Frontier items: {payload['frontier_count']}")
    click.echo(f"Construction paths: {payload['path_count']}")
    click.echo(f"Decision assumptions: {payload['assumption_count']}")
    if payload["continuity"]:
        click.echo(
            "Continuity: "
            f"{payload['continuity'].get('disposition', 'declared')} "
            f"from {payload['continuity'].get('prior_analysis_ref', 'unspecified')}"
        )


@strategy_group.command(name="paths")
@click.option(
    "--artifact",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def show_paths(artifact: Path, output_json: bool) -> None:
    """List declared construction paths without ranking them."""
    data = _load_analysis(artifact)
    paths = []
    for item in data.get("construction_paths", []) or []:
        if not isinstance(item, dict):
            continue
        paths.append(
            {
                "path_id": item.get("path_id"),
                "name": item.get("name"),
                "future_state": item.get("future_state"),
                "assumptions": item.get("assumptions", []),
                "reassessment_triggers": item.get("reassessment_triggers", []),
            }
        )
    payload = {
        "ok": True,
        "code": "STRATEGY_PATHS",
        "analysis_ref": _analysis_ref(data, artifact),
        "selected_path_id": data.get("selected_path_id"),
        "paths": paths,
        "ranked": False,
    }
    if output_json:
        _json_echo(payload)
        return
    click.echo("STRATEGY_PATHS")
    if not paths:
        click.echo("No construction paths declared.")
        return
    for item in paths:
        selected = " [selected]" if item["path_id"] == payload["selected_path_id"] else ""
        click.echo(f"{item['path_id']}: {item['name']}{selected}")
        click.echo(f"  Future state: {item['future_state']}")


@strategy_group.command(name="uncertainty")
@click.option(
    "--artifact",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def show_uncertainty(artifact: Path, output_json: bool) -> None:
    """Show the authored decision-changing uncertainty."""
    data = _load_analysis(artifact)
    uncertainty = data.get("decision_changing_uncertainty")
    payload = {
        "ok": True,
        "code": "STRATEGY_UNCERTAINTY",
        "analysis_ref": _analysis_ref(data, artifact),
        "decision_changing_uncertainty": uncertainty,
        "inquiry_selected_by_command": False,
    }
    if output_json:
        _json_echo(payload)
        return
    click.echo("STRATEGY_UNCERTAINTY")
    if not isinstance(uncertainty, dict):
        click.echo("No structured uncertainty declared.")
        return
    for key in ("statement", "could_change", "inquiry_warranted", "evidence_needed", "source"):
        click.echo(f"{key}: {uncertainty.get(key)}")


@strategy_group.command(name="assumptions")
@click.option(
    "--artifact",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def show_assumptions(artifact: Path, output_json: bool) -> None:
    """Show explicit decision assumptions and reassessment triggers."""
    data = _load_analysis(artifact)
    assumptions = _normalize_assumptions(data)
    payload = {
        "ok": True,
        "code": "STRATEGY_ASSUMPTIONS",
        "analysis_ref": _analysis_ref(data, artifact),
        "assumptions": assumptions,
    }
    if output_json:
        _json_echo(payload)
        return
    click.echo("STRATEGY_ASSUMPTIONS")
    if not assumptions:
        click.echo("No explicit decision assumptions declared.")
        return
    for item in assumptions:
        click.echo(f"{item.get('assumption_id', 'ASSUMPTION')}: {item.get('statement')}")
        for trigger in item.get("reassessment_triggers", []) or []:
            click.echo(f"  Reassess when: {trigger}")


@strategy_group.command(name="compare")
@click.option(
    "--before",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--after",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def compare_analyses(before: Path, after: Path, output_json: bool) -> None:
    """Compare two authored analyses as declared state, not strategic quality."""
    old = _load_analysis(before)
    new = _load_analysis(after)
    old_caps = _capability_map(old)
    new_caps = _capability_map(new)
    old_paths = _path_map(old)
    new_paths = _path_map(new)

    capability_changes = []
    for cid in sorted(set(old_caps) | set(new_caps)):
        if old_caps.get(cid) != new_caps.get(cid):
            capability_changes.append(
                {"capability_id": cid, "before": old_caps.get(cid), "after": new_caps.get(cid)}
            )

    added_paths = sorted(set(new_paths) - set(old_paths))
    removed_paths = sorted(set(old_paths) - set(new_paths))
    changed_paths = []
    for pid in sorted(set(old_paths) & set(new_paths)):
        old_key = (
            old_paths[pid].get("name"),
            old_paths[pid].get("future_state"),
            old_paths[pid].get("construction_sequence"),
        )
        new_key = (
            new_paths[pid].get("name"),
            new_paths[pid].get("future_state"),
            new_paths[pid].get("construction_sequence"),
        )
        if old_key != new_key:
            changed_paths.append(pid)

    payload = {
        "ok": True,
        "code": "STRATEGY_ANALYSIS_COMPARE",
        "before_ref": _analysis_ref(old, before),
        "after_ref": _analysis_ref(new, after),
        "target_repository_changed": old.get("target_repository") != new.get("target_repository"),
        "source_identity_changed": old.get("target_source_identity") != new.get("target_source_identity"),
        "disposition_before": old.get("strategic_disposition"),
        "disposition_after": new.get("strategic_disposition"),
        "selected_path_before": old.get("selected_path_id"),
        "selected_path_after": new.get("selected_path_id"),
        "capability_changes": capability_changes,
        "added_paths": added_paths,
        "removed_paths": removed_paths,
        "changed_paths": changed_paths,
        "uncertainty_changed": old.get("decision_changing_uncertainty")
        != new.get("decision_changing_uncertainty"),
        "continuity_after": _continuity(new),
        "quality_ranked_by_command": False,
    }
    if output_json:
        _json_echo(payload)
        return
    click.echo("STRATEGY_ANALYSIS_COMPARE")
    click.echo(f"Before: {payload['before_ref']}")
    click.echo(f"After:  {payload['after_ref']}")
    click.echo(
        f"Disposition: {payload['disposition_before']} -> {payload['disposition_after']}"
    )
    click.echo(
        f"Selected path: {payload['selected_path_before'] or 'none'} -> "
        f"{payload['selected_path_after'] or 'none'}"
    )
    click.echo(f"Capability state changes: {len(capability_changes)}")
    click.echo(f"Paths added/removed/changed: {len(added_paths)}/{len(removed_paths)}/{len(changed_paths)}")
    click.echo(f"Decision-changing uncertainty changed: {payload['uncertainty_changed']}")


@strategy_group.command(name="drift")
@click.option(
    "--artifact",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--repo",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def inspect_drift(artifact: Path, repo: Path, output_json: bool) -> None:
    """Detect mechanically observable typed currentness drift; do not invalidate strategy."""
    data = _load_analysis(artifact)
    current_head = _git_head(repo)
    recorded_sha = _identity_sha(data.get("target_source_identity"))

    source_status = "NOT_COMPARABLE"
    if current_head and recorded_sha:
        source_status = (
            "CURRENT"
            if current_head.lower().startswith(recorded_sha)
            or recorded_sha.startswith(current_head.lower())
            else "DRIFTED"
        )

    observations: list[dict[str, Any]] = []

    def add_observation(
        kind: str,
        subject_ref: str,
        prior_value: str | None = None,
        current_value: str | None = None,
    ) -> None:
        observations.append(
            {
                "observation_id": f"CURRENTNESS-{len(observations) + 1}",
                "kind": kind,
                "subject_ref": subject_ref,
                "prior_value": prior_value,
                "current_value": current_value,
                "mechanically_established": True,
            }
        )

    if source_status == "DRIFTED":
        add_observation(
            "SOURCE_IDENTITY_CHANGED",
            "repository",
            str(data.get("target_source_identity")),
            current_head,
        )

    governing_paths = {
        path_value
        for ref in _governing_authority_paths(data)
        if (path_value := _local_ref_path(ref)) is not None
    }
    evidence_paths = {
        path_value
        for ref in _evidence_paths(data)
        if (path_value := _local_ref_path(ref)) is not None
    }
    checked_refs = sorted(governing_paths | evidence_paths)
    missing_refs: list[str] = []

    for path_value in checked_refs:
        current_path = repo / path_value
        current_exists = current_path.is_file()
        prior_bytes = (
            _git_file_bytes(repo, recorded_sha, path_value) if recorded_sha else None
        )
        is_governing = path_value in governing_paths

        if not current_exists:
            missing_refs.append(path_value)
            add_observation(
                "GOVERNING_AUTHORITY_REF_CHANGED"
                if is_governing
                else "EVIDENCE_REF_MISSING",
                path_value,
                f"{recorded_sha}:{path_value}" if recorded_sha else None,
                None,
            )
            continue

        if prior_bytes is not None:
            try:
                current_bytes = current_path.read_bytes()
            except OSError:
                current_bytes = None
            if current_bytes is not None and current_bytes != prior_bytes:
                add_observation(
                    "GOVERNING_AUTHORITY_REF_CHANGED"
                    if is_governing
                    else "EVIDENCE_REF_CHANGED",
                    path_value,
                    f"{recorded_sha}:{path_value}" if recorded_sha else None,
                    f"{current_head}:{path_value}" if current_head else path_value,
                )

    payload = {
        "ok": True,
        "code": "STRATEGY_DRIFT_INSPECTION",
        "analysis_ref": _analysis_ref(data, artifact),
        "recorded_source_identity": data.get("target_source_identity"),
        "recorded_source_sha": recorded_sha,
        "current_git_head": current_head,
        "source_identity_status": source_status,
        "checked_local_evidence_refs": checked_refs,
        "missing_local_evidence_refs": sorted(set(missing_refs)),
        "currentness_observations": observations,
        "mechanical_drift_detected": bool(observations),
        "semantic_consequence_inferred_by_command": False,
        "strategy_invalidated_by_command": False,
        "reanalysis_required_by_command": False,
    }
    if output_json:
        _json_echo(payload)
        return
    click.echo("STRATEGY_DRIFT_INSPECTION")
    click.echo(f"Recorded source: {payload['recorded_source_identity']}")
    click.echo(f"Current HEAD: {current_head or 'unavailable'}")
    click.echo(f"Source status: {source_status}")
    click.echo(f"Currentness observations: {len(observations)}")
    for item in observations:
        click.echo(f"  - {item['kind']}: {item['subject_ref']}")
    click.echo("Mechanical currentness observations do not imply a semantic consequence.")


def _history_events(artifacts: tuple[Path, ...]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, artifact in enumerate(artifacts, start=1):
        data = _load_supported_strategy_artifact(artifact)
        artifact_id = data.get("artifact_id")
        if artifact_id == "strategic_repository_analysis":
            events.append(
                {
                    "sequence": index,
                    "artifact_id": artifact_id,
                    "ref": _analysis_ref(data, artifact),
                    "created_at": data.get("created_at"),
                    "continuity": _continuity(data),
                    "strategic_disposition": data.get("strategic_disposition"),
                    "selected_path_id": data.get("selected_path_id"),
                    "assumptions": _normalize_assumptions(data),
                    "path_transitions": list(_path_transition_map(data).values()),
                    "candidate_path_transition_ref": data.get(
                        "candidate_path_transition_ref"
                    ),
                }
            )
        else:
            events.append(
                {
                    "sequence": index,
                    "artifact_id": artifact_id,
                    "ref": f"REC-{index}",
                    "created_at": data.get("created_at"),
                    "prior_analysis_ref": data.get("prior_analysis_ref"),
                    "assumption_updates": data.get("assumption_updates", []),
                    "path_disposition": data.get("path_disposition"),
                    "prior_path_id": data.get("prior_path_id"),
                    "current_path_id": data.get("current_path_id"),
                    "path_transition_effect": data.get("path_transition_effect"),
                    "strategic_effect": data.get("strategic_effect"),
                }
            )
    return events


@strategy_group.command(name="history")
@click.option(
    "--artifact",
    "artifacts",
    required=True,
    multiple=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON")
def show_history(artifacts: tuple[Path, ...], output_json: bool) -> None:
    """Project supplied strategic analyses/reconciliations in caller-declared order."""
    events = _history_events(artifacts)
    payload = {
        "ok": True,
        "code": "STRATEGY_HISTORY",
        "events": events,
        "caller_order_preserved": True,
        "chronology_inferred_by_command": False,
        "strategy_selected_by_command": False,
        "semantic_consequence_inferred_by_command": False,
    }
    if output_json:
        _json_echo(payload)
        return
    click.echo("STRATEGY_HISTORY")
    for event in events:
        if event["artifact_id"] == "strategic_repository_analysis":
            click.echo(
                f"{event['ref']}: disposition={event['strategic_disposition']} "
                f"selected_path={event['selected_path_id'] or 'none'}"
            )
            continuity = event.get("continuity")
            if isinstance(continuity, dict):
                click.echo(
                    f"  continuity={continuity.get('disposition')} "
                    f"from={continuity.get('prior_analysis_ref')}"
                )
            for transition in event.get("path_transitions", []):
                click.echo(
                    f"  transition {transition['transition_ref']}: "
                    f"{transition['transition']}"
                )
        else:
            click.echo(
                f"{event['ref']}: reconcile={event['prior_analysis_ref']} "
                f"effect={event['strategic_effect']}"
            )
            transition = event.get("path_transition_effect")
            if isinstance(transition, dict):
                click.echo(
                    f"  transition {transition.get('transition_ref')}: "
                    f"{transition.get('disposition')}"
                )


@strategy_group.command(name="graph")
@click.option(
    "--artifact",
    "artifacts",
    required=True,
    multiple=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True, help="Emit JSON envelope")
def show_graph(artifacts: tuple[Path, ...], output_json: bool) -> None:
    """Render declared strategic relationships as Mermaid without inference."""
    events = _history_events(artifacts)
    lines = ["graph TD"]
    declared_nodes: set[str] = set()

    def node(node_id: str, label: str) -> None:
        if node_id not in declared_nodes:
            lines.append(f'  {node_id}["{_mermaid_label(label)}"]')
            declared_nodes.add(node_id)

    for event in events:
        if event["artifact_id"] == "strategic_repository_analysis":
            current_ref = event["ref"]
            current_id = _mermaid_id("SRA", current_ref)
            node(current_id, current_ref)
            continuity = event.get("continuity")
            if isinstance(continuity, dict) and continuity.get("prior_analysis_ref"):
                prior_ref = continuity["prior_analysis_ref"]
                prior_id = _mermaid_id("SRA", prior_ref)
                node(prior_id, prior_ref)
                lines.append(
                    f"  {prior_id} -->|{_mermaid_label(continuity.get('disposition'))}| {current_id}"
                )
            selected_path = event.get("selected_path_id")
            if selected_path:
                path_id = _mermaid_id("PATH", selected_path)
                node(path_id, selected_path)
                lines.append(f"  {current_id} -->|selected| {path_id}")
            for assumption in event.get("assumptions", []):
                assumption_ref = assumption.get("assumption_id")
                if assumption_ref:
                    assumption_id = _mermaid_id("ASSUMPTION", assumption_ref)
                    node(assumption_id, assumption_ref)
                    lines.append(f"  {current_id} -->|assumes| {assumption_id}")
            for transition in event.get("path_transitions", []):
                transition_ref = transition.get("transition_ref")
                if transition_ref:
                    transition_id = _mermaid_id("TRANSITION", transition_ref)
                    node(transition_id, transition_ref)
                    lines.append(f"  {current_id} -->|declares| {transition_id}")
        else:
            rec_id = _mermaid_id("REC", event["sequence"])
            node(rec_id, event["ref"])
            prior_ref = event.get("prior_analysis_ref")
            if prior_ref:
                prior_id = _mermaid_id("SRA", prior_ref)
                node(prior_id, prior_ref)
                lines.append(f"  {prior_id} -->|reconciled by| {rec_id}")
            path_ref = event.get("current_path_id") or event.get("prior_path_id")
            if path_ref:
                path_id = _mermaid_id("PATH", path_ref)
                node(path_id, path_ref)
                lines.append(
                    f"  {rec_id} -->|path {_mermaid_label(event.get('path_disposition'))}| {path_id}"
                )
            for update in event.get("assumption_updates", []) or []:
                if not isinstance(update, dict) or not update.get("assumption_id"):
                    continue
                assumption_ref = update["assumption_id"]
                assumption_id = _mermaid_id("ASSUMPTION", assumption_ref)
                node(assumption_id, assumption_ref)
                lines.append(
                    f"  {rec_id} -->|assumption {_mermaid_label(update.get('disposition'))}| {assumption_id}"
                )
            transition = event.get("path_transition_effect")
            if isinstance(transition, dict) and transition.get("transition_ref"):
                transition_ref = transition["transition_ref"]
                transition_id = _mermaid_id("TRANSITION", transition_ref)
                node(transition_id, transition_ref)
                lines.append(
                    f"  {rec_id} -->|transition {_mermaid_label(transition.get('disposition'))}| {transition_id}"
                )

    mermaid = "\n".join(lines)
    payload = {
        "ok": True,
        "code": "STRATEGY_GRAPH",
        "format": "mermaid",
        "mermaid": mermaid,
        "caller_order_preserved": True,
        "causality_inferred_by_command": False,
        "strategy_selected_by_command": False,
        "semantic_consequence_inferred_by_command": False,
    }
    if output_json:
        _json_echo(payload)
        return
    click.echo(mermaid)


def register_strategy_commands(root: click.Group) -> None:
    """Register deterministic strategy projections on the root CLI."""
    root.add_command(strategy_group)