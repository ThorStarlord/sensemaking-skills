"""CLI surface for deterministic release-authority inspection."""

from __future__ import annotations

import json
from pathlib import Path

import click

from .release_authority import audit_release_authority, release_authority_payload


def register_release_commands(root: click.Group) -> None:
    @root.group(name="release")
    def release_group() -> None:
        """Inspect repository-owned release authority without publishing."""

    @release_group.command(name="audit")
    @click.option(
        "--repo-root",
        type=click.Path(exists=True, file_okay=False, path_type=Path),
        default=Path("."),
        show_default=True,
    )
    @click.option("--json", "output_json", is_flag=True, help="Emit one JSON object")
    def release_audit(repo_root: Path, output_json: bool) -> None:
        """Reconcile source/target/Git/docs/workflow release identity."""
        result = audit_release_authority(repo_root)
        payload = release_authority_payload(result)
        if output_json:
            click.echo(json.dumps(payload, sort_keys=True, ensure_ascii=False))
        else:
            click.echo(payload["code"])
            click.echo(f"Source: {payload['source_version'] or 'unknown'}")
            click.echo(f"Target: {payload['target_version'] or 'unknown'}")
            click.echo(f"Status: {payload['release_status'] or 'unknown'}")
            click.echo(f"Git HEAD: {payload['git']['head'] or 'unknown'}")
            click.echo(f"Git tree: {payload['git']['tree'] or 'unknown'}")
            click.echo(f"Git dirty: {payload['git']['dirty']}")
            for finding in payload["findings"]:
                click.echo(
                    f"- {finding['severity'].upper()} {finding['code']}: {finding['detail']}"
                )
            click.echo(payload["explicit_limit"])
        if not result.ok:
            raise click.exceptions.Exit(3)
