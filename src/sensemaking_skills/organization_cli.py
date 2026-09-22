"""CLI surfaces for Capability & Organization Tracer v0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import click

from .organization import (
    inspect_organization_pattern,
    inspect_organization_role,
    project_skill_capability_profile,
)


def _emit(payload: dict[str, Any], *, output_json: bool) -> None:
    if output_json:
        click.echo(json.dumps(payload, sort_keys=True, ensure_ascii=False))
    else:
        click.echo(
            json.dumps(
                payload,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
        )


def _default_resource(filename: str) -> Path:
    return Path(__file__).resolve().parent / "defaults" / filename


def _resolve_path(value: Path | None, *, default_name: str) -> Path:
    return value if value is not None else _default_resource(default_name)


def register_organization_commands(root_cli: click.Group) -> None:
    @root_cli.group(name="organization")
    def organization_group() -> None:
        """Inspect explicit roles/capabilities without allocating workers."""

    @organization_group.command(name="skill-profile")
    @click.option(
        "--profiles",
        type=click.Path(
            exists=True,
            dir_okay=False,
            path_type=Path,
        ),
        default=None,
        help=(
            "Optional Skill-capability profile overlay. "
            "Defaults to the packaged tracer v0 overlay."
        ),
    )
    @click.option("--skill-id", required=True, help="Exact Skill id to inspect")
    @click.option(
        "--repo-root",
        type=click.Path(
            exists=True,
            file_okay=False,
            path_type=Path,
        ),
        default=None,
        help="Optional repository root for canonical Skill/manifest existence checks.",
    )
    @click.option("--json", "output_json", is_flag=True)
    def organization_skill_profile(
        profiles: Path | None,
        skill_id: str,
        repo_root: Path | None,
        output_json: bool,
    ) -> None:
        """Project non-authoritative capability facets for one declared Skill."""
        normalized = skill_id.strip()
        if not normalized:
            raise click.ClickException("--skill-id must be non-empty")
        try:
            profile = project_skill_capability_profile(
                _resolve_path(
                    profiles,
                    default_name="skill-capability-profiles-v0.yaml",
                ),
                skill_id=normalized,
                repo_root=repo_root,
            )
        except (OSError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc

        _emit(
            {
                "ok": True,
                "code": "ORGANIZATION_SKILL_PROFILE",
                "profile": profile,
                "selection_performed": False,
                "authorization_granted": False,
                "execution_performed": False,
                "explicit_limit": (
                    "Capability facets are a tracer overlay for legibility. "
                    "They are not Skill Contract Manifest authority and do not "
                    "select or warrant a Skill."
                ),
            },
            output_json=output_json,
        )

    @organization_group.command(name="inspect")
    @click.option(
        "--pattern",
        type=click.Path(
            exists=True,
            dir_okay=False,
            path_type=Path,
        ),
        default=None,
        help=(
            "Optional Organization Pattern. "
            "Defaults to packaged Repository Change Cell v0."
        ),
    )
    @click.option(
        "--profiles",
        type=click.Path(
            exists=True,
            dir_okay=False,
            path_type=Path,
        ),
        default=None,
        help="Optional Skill-capability profile overlay.",
    )
    @click.option(
        "--repo-root",
        type=click.Path(
            exists=True,
            file_okay=False,
            path_type=Path,
        ),
        default=None,
        help="Optional repository root for canonical Skill existence checks.",
    )
    @click.option("--json", "output_json", is_flag=True)
    def organization_inspect(
        pattern: Path | None,
        profiles: Path | None,
        repo_root: Path | None,
        output_json: bool,
    ) -> None:
        """Validate one explicit organization topology without routing work."""
        try:
            result = inspect_organization_pattern(
                _resolve_path(
                    pattern,
                    default_name="repository-change-cell-v0.yaml",
                ),
                _resolve_path(
                    profiles,
                    default_name="skill-capability-profiles-v0.yaml",
                ),
                repo_root=repo_root,
            )
        except (OSError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc

        payload = {
            "ok": result.valid,
            "valid": result.valid,
            "code": (
                "ORGANIZATION_PATTERN_VALID"
                if result.valid
                else "ORGANIZATION_PATTERN_INVALID"
            ),
            "organization_id": result.organization_id,
            "objective_class": result.objective_class,
            "roles": list(result.roles),
            "relationships": list(result.relationships),
            "limits": list(result.limits),
            "diagnostics": [
                {
                    "code": item.code,
                    "detail": item.detail,
                    "path": item.path,
                }
                for item in result.diagnostics
            ],
            "selection_performed": result.selection_performed,
            "authorization_granted": result.authorization_granted,
            "execution_performed": result.execution_performed,
            "semantic_truth_established": result.semantic_truth_established,
            "explicit_limit": (
                "Pattern validation checks declared role/capability/reference "
                "coherence only. It does not instantiate actors, select a Skill, "
                "schedule work, or grant authority."
            ),
        }
        _emit(payload, output_json=output_json)
        if not result.valid:
            raise click.exceptions.Exit(3)

    @organization_group.command(name="role")
    @click.option(
        "--pattern",
        type=click.Path(
            exists=True,
            dir_okay=False,
            path_type=Path,
        ),
        default=None,
    )
    @click.option(
        "--profiles",
        type=click.Path(
            exists=True,
            dir_okay=False,
            path_type=Path,
        ),
        default=None,
    )
    @click.option("--role-id", required=True, help="Exact role id to inspect")
    @click.option(
        "--repo-root",
        type=click.Path(
            exists=True,
            file_okay=False,
            path_type=Path,
        ),
        default=None,
    )
    @click.option("--json", "output_json", is_flag=True)
    def organization_role(
        pattern: Path | None,
        profiles: Path | None,
        role_id: str,
        repo_root: Path | None,
        output_json: bool,
    ) -> None:
        """Show one role's explicit capability bindings and evidence edges."""
        normalized = role_id.strip()
        if not normalized:
            raise click.ClickException("--role-id must be non-empty")
        try:
            payload = inspect_organization_role(
                _resolve_path(
                    pattern,
                    default_name="repository-change-cell-v0.yaml",
                ),
                _resolve_path(
                    profiles,
                    default_name="skill-capability-profiles-v0.yaml",
                ),
                role_id=normalized,
                repo_root=repo_root,
            )
        except (OSError, ValueError) as exc:
            raise click.ClickException(str(exc)) from exc

        _emit(
            {
                "ok": payload["organization_valid"],
                "code": "ORGANIZATION_ROLE_VIEW",
                **payload,
            },
            output_json=output_json,
        )
        if not payload["organization_valid"]:
            raise click.exceptions.Exit(3)
