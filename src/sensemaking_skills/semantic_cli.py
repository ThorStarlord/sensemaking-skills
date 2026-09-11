"""CLI surfaces for deterministic Semantic Architecture operations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import click

from .semantic_architecture import (
    Completeness,
    Currentness,
    ObservationKind,
    SemanticObservation,
    SemanticStateEntry,
    SemanticStateStore,
    build_repository_semantic_map,
    build_semantic_catalog,
    probe_exact_search,
    probe_file_containment,
    probe_manifest_dependencies,
    probe_python_imports,
    to_dict,
    validate_conformance,
)


def _emit(payload: dict[str, Any], *, output_json: bool) -> None:
    if output_json:
        click.echo(json.dumps(payload, sort_keys=True, ensure_ascii=False))
    else:
        click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))


def _write_payload(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _observation_from_dict(data: dict[str, Any]) -> SemanticObservation:
    return SemanticObservation(
        id=str(data["id"]),
        kind=ObservationKind(str(data["kind"])),
        subject=str(data["subject"]),
        predicate=str(data["predicate"]),
        object=str(data["object"]),
        evidence_refs=tuple(str(item) for item in data.get("evidence_refs", [])),
        source=str(data["source"]),
        scope=str(data["scope"]),
        completeness=Completeness(str(data["completeness"])),
        currentness=Currentness(str(data["currentness"])),
        target_ref=str(data["target_ref"]),
        metadata=data.get("metadata", {}) if isinstance(data.get("metadata", {}), dict) else {},
    )


def _read_probe_observations(path: Path) -> tuple[SemanticObservation, ...]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise click.ClickException(f"probe result must be a JSON mapping: {path}")
    values = data.get("observations")
    if not isinstance(values, list):
        raise click.ClickException(f"probe result requires observations list: {path}")
    try:
        return tuple(_observation_from_dict(item) for item in values if isinstance(item, dict))
    except (KeyError, ValueError, TypeError) as exc:
        raise click.ClickException(f"invalid observation in {path}: {exc}") from exc


def register_semantic_commands(root_cli: click.Group) -> None:
    @root_cli.group(name="semantic")
    def semantic_group() -> None:
        """Operate mechanical semantic substrate; never decide semantic truth."""

    @semantic_group.command(name="probe")
    @click.option("--repo", "repo_root", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--target-ref", required=True, help="Explicit repository snapshot/ref identity")
    @click.option(
        "--kind",
        type=click.Choice(["file-containment", "python-imports", "manifest-dependencies", "exact-search"]),
        required=True,
    )
    @click.option("--pattern", default=None, help="Literal pattern required by exact-search")
    @click.option("--include-glob", default="*", show_default=True, help="File glob for exact-search")
    @click.option("--output", type=click.Path(path_type=Path), default=None, help="Optional JSON output file")
    @click.option("--json", "output_json", is_flag=True, help="Emit one-line JSON")
    def semantic_probe(
        repo_root: Path,
        target_ref: str,
        kind: str,
        pattern: str | None,
        include_glob: str,
        output: Path | None,
        output_json: bool,
    ) -> None:
        """Collect a declared mechanical observation set from repository bytes."""
        probes: dict[str, Callable[..., Any]] = {
            "file-containment": probe_file_containment,
            "python-imports": probe_python_imports,
            "manifest-dependencies": probe_manifest_dependencies,
        }
        if kind == "exact-search":
            if not pattern:
                raise click.ClickException("--pattern is required for --kind exact-search")
            result = probe_exact_search(
                repo_root,
                target_ref=target_ref,
                pattern=pattern,
                include_glob=include_glob,
            )
        else:
            result = probes[kind](repo_root, target_ref=target_ref)
        payload = to_dict(result)
        payload["code"] = "SEMANTIC_PROBE_COMPLETE"
        _write_payload(output, payload)
        _emit(payload, output_json=output_json)

    @semantic_group.command(name="map-build")
    @click.option("--map-id", required=True)
    @click.option("--target-ref", required=True)
    @click.option(
        "--observations",
        "observation_paths",
        multiple=True,
        required=True,
        type=click.Path(exists=True, dir_okay=False, path_type=Path),
        help="One or more semantic probe JSON results",
    )
    @click.option("--claim-ref", "claim_refs", multiple=True)
    @click.option("--uncertainty-ref", "uncertainty_refs", multiple=True)
    @click.option("--limit", "limits", multiple=True)
    @click.option("--output", type=click.Path(path_type=Path), required=True)
    @click.option("--json", "output_json", is_flag=True)
    def semantic_map_build(
        map_id: str,
        target_ref: str,
        observation_paths: tuple[Path, ...],
        claim_refs: tuple[str, ...],
        uncertainty_refs: tuple[str, ...],
        limits: tuple[str, ...],
        output: Path,
        output_json: bool,
    ) -> None:
        """Build a bounded map from supplied observations; infer no architecture."""
        observations: list[SemanticObservation] = []
        for path in observation_paths:
            observations.extend(_read_probe_observations(path))
        try:
            result = build_repository_semantic_map(
                map_id=map_id,
                target_ref=target_ref,
                observations=observations,
                claim_refs=claim_refs,
                uncertainty_refs=uncertainty_refs,
                explicit_limits=limits,
            )
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        payload = to_dict(result)
        payload["code"] = "REPOSITORY_SEMANTIC_MAP_BUILT"
        _write_payload(output, payload)
        _emit(payload, output_json=output_json)

    @semantic_group.command(name="state-append")
    @click.option("--state-file", required=True, type=click.Path(path_type=Path))
    @click.option("--entry-id", required=True)
    @click.option("--source-skill", required=True)
    @click.option("--artifact-ref", required=True)
    @click.option("--target-ref", required=True)
    @click.option("--profile-ref", default=None)
    @click.option("--evidence-ref", "evidence_refs", multiple=True)
    @click.option("--claim-ref", "claim_refs", multiple=True)
    @click.option("--uncertainty-ref", "uncertainty_refs", multiple=True)
    @click.option("--parent", "parent_entry_ids", multiple=True)
    @click.option("--note", "notes", multiple=True)
    @click.option("--json", "output_json", is_flag=True)
    def semantic_state_append(
        state_file: Path,
        entry_id: str,
        source_skill: str,
        artifact_ref: str,
        target_ref: str,
        profile_ref: str | None,
        evidence_refs: tuple[str, ...],
        claim_refs: tuple[str, ...],
        uncertainty_refs: tuple[str, ...],
        parent_entry_ids: tuple[str, ...],
        notes: tuple[str, ...],
        output_json: bool,
    ) -> None:
        """Append references to semantic work without copying hidden reasoning."""
        store = SemanticStateStore(state_file)
        try:
            digest = store.append(
                SemanticStateEntry(
                    entry_id=entry_id,
                    source_skill=source_skill,
                    artifact_ref=artifact_ref,
                    target_ref=target_ref,
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
        _emit(
            {
                "ok": True,
                "code": "SEMANTIC_STATE_APPENDED",
                "entry_id": entry_id,
                "entry_digest": digest,
                "semantic_truth_established": False,
            },
            output_json=output_json,
        )

    @semantic_group.command(name="state-show")
    @click.option("--state-file", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def semantic_state_show(state_file: Path, output_json: bool) -> None:
        """Show and validate the cross-Skill companion state chain."""
        records, diagnostics = SemanticStateStore(state_file).load_raw()
        _emit(
            {
                "ok": not diagnostics,
                "code": "SEMANTIC_STATE_VALID" if not diagnostics else "SEMANTIC_STATE_INVALID",
                "records": records,
                "diagnostics": [to_dict(item) for item in diagnostics],
                "semantic_truth_established": False,
            },
            output_json=output_json,
        )
        if diagnostics:
            raise click.exceptions.Exit(3)

    @semantic_group.command(name="conformance")
    @click.option("--manifests-dir", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--domain-packs-dir", default=None, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--repo-root", default=None, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def semantic_conformance(
        manifests_dir: Path,
        domain_packs_dir: Path | None,
        repo_root: Path | None,
        output_json: bool,
    ) -> None:
        """Validate manifest/ontology consistency without judging Skill quality."""
        result = validate_conformance(
            manifests_dir,
            domain_packs_dir=domain_packs_dir,
            repo_root=repo_root,
        )
        payload = {
            "ok": result.valid,
            "code": "SEMANTIC_CONFORMANCE_VALID" if result.valid else "SEMANTIC_CONFORMANCE_INVALID",
            "skill_manifest_count": result.skill_manifest_count,
            "domain_pack_count": result.domain_pack_count,
            "diagnostics": [to_dict(item) for item in result.diagnostics],
            "semantic_truth_established": False,
        }
        _emit(payload, output_json=output_json)
        if not result.valid:
            raise click.exceptions.Exit(3)

    @semantic_group.command(name="catalog")
    @click.option("--manifests-dir", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--domain-packs-dir", default=None, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--repo-root", default=None, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--skill-id", default=None, help="Optional exact Skill manifest id filter")
    @click.option("--domain-id", default=None, help="Optional exact Domain Pack/domain filter")
    @click.option("--json", "output_json", is_flag=True)
    def semantic_catalog(
        manifests_dir: Path,
        domain_packs_dir: Path | None,
        repo_root: Path | None,
        skill_id: str | None,
        domain_id: str | None,
        output_json: bool,
    ) -> None:
        """Inspect declared Skill/Domain Pack metadata without selecting a capability."""
        normalized_skill = skill_id.strip() if skill_id else None
        normalized_domain = domain_id.strip() if domain_id else None
        if skill_id is not None and not normalized_skill:
            raise click.ClickException("--skill-id must be non-empty when supplied")
        if domain_id is not None and not normalized_domain:
            raise click.ClickException("--domain-id must be non-empty when supplied")
        result = build_semantic_catalog(
            manifests_dir,
            domain_packs_dir=domain_packs_dir,
            repo_root=repo_root,
            skill_id=normalized_skill,
            domain_id=normalized_domain,
        )
        payload = {
            "ok": not result.diagnostics,
            "code": "SEMANTIC_CATALOG",
            "skill_manifest_count": len(result.skill_manifests),
            "domain_pack_count": len(result.domain_packs),
            "skill_manifests": list(result.skill_manifests),
            "domain_packs": list(result.domain_packs),
            "catalog_diagnostics": [to_dict(item) for item in result.diagnostics],
            "repository_conformance_valid": result.conformance_valid,
            "selection_performed": False,
            "semantic_truth_established": False,
            "explicit_limit": "Catalog inspection exposes declared metadata only; it does not select, rank, or warrant a Skill/capability.",
        }
        _emit(payload, output_json=output_json)
        if result.diagnostics:
            raise click.exceptions.Exit(3)