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
from .semantic_architecture.impact import build_impact_preview
from .semantic_architecture.knowledge_sources import (
    build_knowledge_snapshot, temporary_commit_checkout, verified_tracked_sources,
)
from .semantic_architecture.repository_bootstrap import orient_repository
from .semantic_architecture.worktree_context import changed_paths_since_indexed_ref, inspect_worktree_context
from .semantic_architecture.stewardship_validation import inspect_knowledge_proposal
from .semantic_architecture.knowledge_store import (
    audit_knowledge_sources, query_context_paths, query_knowledge, store_snapshot,
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

    @semantic_group.command(name="knowledge-build")
    @click.option("--repo", "repo_root", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--repository", "repository_id", required=True, help="Explicit stable repository identity")
    @click.option("--target-ref", required=True, help="Exact 40-character Git HEAD of a CLEAN target checkout (any local commit with --temporary-checkout)")
    @click.option("--db", "db_path", required=True, type=click.Path(path_type=Path), help="Local index outside the repository checkout")
    @click.option("--temporary-checkout", is_flag=True, help="Index --target-ref from a temporary detached worktree outside --repo, so the active checkout may be dirty or at another commit; only committed bytes are read")
    @click.option("--include-repository-structure", is_flag=True, help="Index bounded Git path containment; not architectural dependencies")
    @click.option("--max-structural-files", type=click.IntRange(1, 2000), default=600)
    @click.option("--include-python-imports", is_flag=True, help="Index syntactic Python imports as mechanical observations")
    @click.option("--max-imports", type=click.IntRange(0, 10000), default=1000)
    @click.option("--json", "output_json", is_flag=True)
    def semantic_knowledge_build(
        repo_root: Path, repository_id: str, target_ref: str, db_path: Path, temporary_checkout: bool,
        include_repository_structure: bool, max_structural_files: int,
        include_python_imports: bool, max_imports: int, output_json: bool,
    ) -> None:
        """Index source-pinned knowledge while retaining historical revisions."""
        def build(source_root: Path) -> Any:
            return build_knowledge_snapshot(
                source_root, repository=repository_id, target_ref=target_ref,
                include_python_imports=include_python_imports, max_imports=max_imports,
                include_repository_structure=include_repository_structure,
                max_structural_files=max_structural_files,
            )

        try:
            if temporary_checkout:
                with temporary_commit_checkout(repo_root, target_ref) as checkout:
                    snapshot = build(checkout)
            else:
                snapshot = build(repo_root)
            payload = store_snapshot(db_path, snapshot, source_root=repo_root)
        except (ValueError, OSError, UnicodeError, KeyError, TypeError) as exc:
            raise click.ClickException(str(exc)) from exc
        payload["code"] = "SEMANTIC_KNOWLEDGE_INDEXED"
        payload["source_checkout"] = "temporary_worktree" if temporary_checkout else "active_checkout"
        payload["source_scope"] = list(snapshot.source_scope)
        payload["limits"] = list(snapshot.limits)
        _emit(payload, output_json=output_json)

    @semantic_group.command(name="knowledge-orient")
    @click.option("--repo", "repo_root", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--repository", "repository_id", required=True, help="Explicit repository identity")
    @click.option("--target-ref", required=True, help="Exact 40-character SHA of clean checked-out HEAD")
    @click.option("--max-files", type=click.IntRange(1, 20000), default=5000)
    @click.option("--sample-limit", type=click.IntRange(1, 50), default=16)
    @click.option("--db", "db_path", type=click.Path(exists=True, dir_okay=False, path_type=Path),
                  default=None, help="Optional existing semantic index for revision-specific knowledge counts")
    @click.option("--json", "output_json", is_flag=True)
    def semantic_knowledge_orient(
        repo_root: Path, repository_id: str, target_ref: str,
        max_files: int, sample_limit: int, db_path: Path | None, output_json: bool,
    ) -> None:
        """Orient at pinned Git HEAD without reading unreviewed semantics or mutating sources."""
        try:
            root, tracked = verified_tracked_sources(repo_root, target_ref)
            payload = orient_repository(
                root, tracked, repository=repository_id, target_ref=target_ref,
                max_files=max_files, sample_limit=sample_limit,
            )
            if db_path is not None:
                indexed = query_knowledge(
                    db_path, repository=repository_id, target_ref=target_ref,
                    operation="snapshot", limit=1,
                )
                payload["knowledge_index"] = {
                    "counts": indexed["counts"],
                    "source_scope": indexed["source_scope"],
                    "limits": indexed["explicit_limits"],
                    "semantic_truth_established": False,
                }
        except (ValueError, OSError, UnicodeError, KeyError, TypeError) as exc:
            raise click.ClickException(str(exc)) from exc
        payload["code"] = "SEMANTIC_REPOSITORY_ORIENTATION"
        _emit(payload, output_json=output_json)

    @semantic_group.command(name="knowledge-check-rules")
    @click.option("--repo", "repo_root", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path),
                  help="Exact clean Git checkout whose committed authored rules are checked")
    @click.option("--target-ref", required=True, help="Exact committed HEAD SHA of the checkout")
    @click.option("--json", "output_json", is_flag=True)
    def semantic_knowledge_check_rules(repo_root: Path, target_ref: str, output_json: bool) -> None:
        """Report possible dependency-rule violations. Warning-only; never fails."""
        from .semantic_architecture.knowledge import record_dict
        from .semantic_architecture.knowledge_architecture import check_rule_findings
        from .semantic_architecture.knowledge_sources import _authored_records, _source

        try:
            root, tracked = verified_tracked_sources(repo_root, target_ref)
            claims, relations = _authored_records(root, tracked)
            claim_map = {c.id: record_dict(c) for c in claims}
            payload = check_rule_findings(
                claim_map,
                read_source=lambda rel: _source(root, tracked, rel).read_text(encoding="utf-8", errors="replace"),
                tracked=tracked,
                relations=[record_dict(r) for r in relations],
            )
        except (ValueError, OSError, UnicodeError) as exc:
            raise click.ClickException(str(exc)) from exc
        payload.update({"repository_target_ref": target_ref, "action_authorized": False,
                        "semantic_truth_established": False})
        _emit(payload, output_json=output_json)

    @semantic_group.command(name="knowledge-proposal-check")
    @click.option("--repo", "repo_root", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--proposal", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def semantic_knowledge_proposal_check(
        repo_root: Path, proposal: Path, output_json: bool,
    ) -> None:
        """Validate a dirty/untracked authored proposal without indexing it as fact."""
        try:
            payload = inspect_knowledge_proposal(repo_root, proposal)
        except (ValueError, OSError, UnicodeError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise click.ClickException(str(exc)) from exc
        _emit(payload, output_json=output_json)

    @semantic_group.command(name="knowledge-query")
    @click.option("--db", "db_path", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
    @click.option("--repository", "repository_id", required=True)
    @click.option("--target-ref", required=True, help="Exact indexed revision to examine")
    @click.option("--operation", required=True,
                  type=click.Choice(["snapshot", "search", "explain", "impact", "why", "contradictions", "history", "changes",
                                     "workspace-impact", "rules-for", "term", "orientation-summary", "context-for"]))
    @click.option("--subject", default=None,
                  help="Exact claim id; literal search text (search); one repository-relative "
                       "file path (rules-for, context-for); literal term (term)")
    @click.option("--path", "path_subjects", multiple=True,
                  help="Repeat 2..8 distinct paths for a bounded multi-file context-for query; "
                       "mutually exclusive with --subject")
    @click.option("--base-ref", default=None, help="Exact previously indexed revision for changes")
    @click.option("--repo", "repo_root", type=click.Path(exists=True, file_okay=False, path_type=Path),
                  help="Optional current Git worktree; does not index uncommitted source")
    @click.option("--term", "search_terms", multiple=True,
                  help="Repeat explicit literal OR phrase (search operation only)")
    @click.option("--expect-kind", "expected_kinds", multiple=True,
                  help="Repeat v1/v2 claim kinds to assess in the explicit one-hop explain/why neighborhood")
    @click.option("--limit", type=click.IntRange(1, 250), default=50)
    @click.option("--depth", type=click.IntRange(0, 4), default=2)
    @click.option("--json", "output_json", is_flag=True)
    def semantic_knowledge_query(
        db_path: Path, repository_id: str, target_ref: str, operation: str,
        subject: str | None, path_subjects: tuple[str, ...],
        base_ref: str | None, repo_root: Path | None,
        search_terms: tuple[str, ...], expected_kinds: tuple[str, ...],
        limit: int, depth: int, output_json: bool,
    ) -> None:
        """Read committed semantic records; optionally report active worktree state."""
        try:
            if path_subjects:
                if operation != "context-for":
                    raise ValueError("--path is supported only for context-for")
                if subject is not None:
                    raise ValueError("--path and --subject are mutually exclusive")
                if base_ref is not None:
                    raise ValueError("--base-ref is not used with context-for --path")
            changed_paths = None
            workspace_relevance_error = None
            if operation == "workspace-impact" and repo_root is None:
                raise ValueError("workspace-impact requires --repo (the active Git worktree)")
            if repo_root is not None and operation in {"workspace-impact", "context-for"}:
                try:
                    changed_paths = changed_paths_since_indexed_ref(repo_root, target_ref)["paths"]
                except ValueError as exc:
                    if operation == "workspace-impact":
                        raise
                    # A valid indexed context remains useful even if its historical
                    # Git commit is unavailable in this local worktree.
                    workspace_relevance_error = str(exc)
            if path_subjects:
                payload = query_context_paths(
                    db_path, repository=repository_id, target_ref=target_ref,
                    paths=path_subjects, limit=limit, depth=depth,
                    search_terms=search_terms, expected_kinds=expected_kinds,
                    workspace_changed_paths=changed_paths,
                )
            else:
                payload = query_knowledge(
                    db_path, repository=repository_id, target_ref=target_ref,
                    operation=operation, subject=subject, base_ref=base_ref,
                    limit=limit, depth=depth,
                    search_terms=search_terms, expected_kinds=expected_kinds,
                    workspace_changed_paths=changed_paths,
                )
            if repo_root is not None:
                payload["workspace_context"] = inspect_worktree_context(repo_root, target_ref)
            if workspace_relevance_error is not None:
                unassessed = {
                    "assessment": "NOT_ASSESSED", "overlay_indexed": False,
                    "semantic_staleness_established": False,
                    "note": "Cannot compare worktree changes with the indexed revision: "
                            + workspace_relevance_error,
                }
                if path_subjects:
                    for item in payload["contexts"]:
                        item["context"]["workspace_relevance"] = dict(unassessed)
                else:
                    payload["context"]["workspace_relevance"] = unassessed
        except (ValueError, OSError, UnicodeError) as exc:
            raise click.ClickException(str(exc)) from exc
        payload["code"] = "SEMANTIC_KNOWLEDGE_QUERY"
        _emit(payload, output_json=output_json)

    @semantic_group.command(name="knowledge-audit")
    @click.option("--db", "db_path", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
    @click.option("--repo", "repo_root", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--repository", "repository_id", required=True)
    @click.option("--indexed-ref", required=True, help="Historical snapshot already in SQLite")
    @click.option("--current-ref", required=True, help="Exact clean Git HEAD currently checked out")
    @click.option("--limit", type=click.IntRange(1, 500), default=100)
    @click.option("--json", "output_json", is_flag=True)
    def semantic_knowledge_audit(
        db_path: Path, repo_root: Path, repository_id: str,
        indexed_ref: str, current_ref: str, limit: int, output_json: bool,
    ) -> None:
        """Audit source drift without deciding whether historical claims remain valid."""
        try:
            payload = audit_knowledge_sources(
                db_path, repository=repository_id, indexed_ref=indexed_ref,
                current_repo_root=repo_root, current_ref=current_ref, limit=limit,
            )
        except (ValueError, OSError, UnicodeError) as exc:
            raise click.ClickException(str(exc)) from exc
        payload["code"] = "SEMANTIC_KNOWLEDGE_SOURCE_AUDIT"
        _emit(payload, output_json=output_json)

    @semantic_group.command(name="impact-preview")
    @click.option("--repo", "repo_root", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--target-ref", required=True, help="Full SHA of checked-out clean Git HEAD")
    @click.option("--subject", required=True, help="Explicit literal change subject")
    @click.option("--related-term", "related_terms", multiple=True, help="Additional caller-selected literal term")
    @click.option("--include-glob", "include_globs", multiple=True, default=("*",), help="Explicit source scope glob")
    @click.option("--max-matches", type=click.IntRange(1, 2000), default=100, show_default=True)
    @click.option("--output", type=click.Path(path_type=Path), default=None)
    @click.option("--json", "output_json", is_flag=True)
    def semantic_impact_preview(
        repo_root: Path,
        target_ref: str,
        subject: str,
        related_terms: tuple[str, ...],
        include_globs: tuple[str, ...],
        max_matches: int,
        output: Path | None,
        output_json: bool,
    ) -> None:
        """Preview Grounding Pack claims and candidate source mentions, never infer impacts."""
        try:
            result = build_impact_preview(
                repo_root, target_ref=target_ref, subject=subject,
                related_terms=related_terms, include_globs=include_globs,
                max_matches=max_matches,
            )
        except (ValueError, OSError, UnicodeError) as exc:
            raise click.ClickException(str(exc)) from exc
        payload = to_dict(result)
        payload["code"] = "SEMANTIC_IMPACT_PREVIEW"
        _write_payload(output, payload)
        _emit(payload, output_json=output_json)

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