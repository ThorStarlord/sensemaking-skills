"""Standalone CLI for the distribution-drift probe (spike).

Usage:
    python scripts/probe_skill_distribution.py [--repo-root PATH] [--installed-dir PATH] [--output PATH] [--sync]

Prints an ASCII-only summary to stdout and writes the distribution_drift
payload to distribution-drift.yaml (default). With --sync, missing and
content-drifted skills are copied from skills/<skill>/ into the installed
root first, then the probe re-runs so the payload and summary reflect the
post-sync state. Exit 0 on success, 2 on bad paths or sync failure.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import yaml

from repo_probes import probe_skill_distribution, sync_skills


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Probe drift between repo skills and installed skills.")
    parser.add_argument("--repo-root", default=".", help="Repository to probe (default: current dir)")
    parser.add_argument("--installed-dir", default=None, help="Installed skills root (default: ~/.agents/skills)")
    parser.add_argument("--output", default="distribution-drift.yaml", help="Payload output path")
    parser.add_argument("--no-write", action="store_true", help="Print summary only")
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Copy missing/content-drifted skills from skills/<skill>/ into the installed root",
    )
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
    except OSError:
        print(f"[probe-skill-distribution] ERROR: repo-root path is not accessible: {args.repo_root}", file=sys.stderr)
        return 2
    if not repo_root.is_dir():
        print(f"[probe-skill-distribution] ERROR: repo-root is not a directory: {repo_root}", file=sys.stderr)
        return 2

    installed_root = Path(args.installed_dir).resolve() if args.installed_dir else Path.home() / ".agents" / "skills"

    start = time.perf_counter()
    payload = probe_skill_distribution(repo_root, installed_skills_root=installed_root)

    if args.sync:
        try:
            sync_summary = sync_skills(repo_root, installed_skills_root=installed_root)
        except OSError as exc:
            print(
                f"[probe-skill-distribution] ERROR: sync failed: {exc}",
                file=sys.stderr,
            )
            return 2
        print(f"SYNC SUMMARY -> {installed_root}")
        if sync_summary["synced_skills"]:
            print(
                f"  synced {sync_summary['synced_skill_count']} skill(s): "
                + ", ".join(sync_summary["synced_skills"])
            )
        else:
            print("  nothing to sync")
        payload = probe_skill_distribution(repo_root, installed_skills_root=installed_root)

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    output: Path | None = None
    if not args.no_write:
        output = Path(args.output).resolve()
        output.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    print(f"DISTRIBUTION DRIFT SUMMARY{(' -> ' + str(output)) if output else ''}")
    print(f"  installed root: {installed_root} (exists={installed_root.is_dir()})")
    print(
        f"  skills checked: {payload['total_skills_checked']} | "
        f"synchronized: {payload['synchronized_count']} | "
        f"line-ending-only: {payload['line_ending_drift_count']} | "
        f"content drift: {payload['content_drift_count']} | "
        f"missing: {payload['missing_installed_count']}"
    )
    print(f"  elapsed: {elapsed_ms} ms")
    for entry in payload["drifted_skills"]:
        print(
            f"  drift: {entry['skill_name']} ({entry['drift_type']} "
            f"repo_lines={entry['repo_lines']} installed_lines={entry['installed_lines']} "
            f"hash_match={entry['hash_match']})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
