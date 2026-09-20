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
    return refs


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
    """Detect mechanically observable currentness drift; do not invalidate strategy."""
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

    missing_refs = []
    checked_refs = []
    for ref in _evidence_paths(data):
        path_value = _local_ref_path(ref)
        if path_value is None:
            continue
        checked_refs.append(path_value)
        if not (repo / path_value).exists():
            missing_refs.append(path_value)

    payload = {
        "ok": True,
        "code": "STRATEGY_DRIFT_INSPECTION",
        "analysis_ref": _analysis_ref(data, artifact),
        "recorded_source_identity": data.get("target_source_identity"),
        "recorded_source_sha": recorded_sha,
        "current_git_head": current_head,
        "source_identity_status": source_status,
        "checked_local_evidence_refs": sorted(set(checked_refs)),
        "missing_local_evidence_refs": sorted(set(missing_refs)),
        "mechanical_drift_detected": source_status == "DRIFTED" or bool(missing_refs),
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
    click.echo(f"Missing local evidence refs: {len(missing_refs)}")
    if missing_refs:
        for item in sorted(set(missing_refs)):
            click.echo(f"  - {item}")
    click.echo("Mechanical drift detected does not mean the strategy is invalid.")


def register_strategy_commands(root: click.Group) -> None:
    """Register deterministic strategy projections on the root CLI."""
    root.add_command(strategy_group)
