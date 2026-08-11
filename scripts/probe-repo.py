"""Probe engine CLI for repo-sensemaker.

Usage:
    python scripts/probe-repo.py [--repo-root PATH] [--output PATH] [--churn-commits N]

Writes probe-report.yaml (default), prints a bounded summary to stdout, exits 0.
Exit 2: --repo-root does not exist or is not a directory.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from repo_probes import probe_all

SUMMARY_LINES = 6


def _summary(report: dict, output: Path) -> str:
    git = report["git_state"]
    vg = report["verification_gap"]
    ce = report["context_entropy"]
    coll = report["test_collection"]
    fx = report["fixtures_coverage"]
    ch = report["churn"]
    rel = report.get("relationships", {})
    rel_ver = rel.get("version", {}).get("findings", []) if isinstance(rel, dict) else []
    rel_adr = rel.get("adr", {}).get("findings", []) if isinstance(rel, dict) else []
    head = git.get("head_sha") or "no-commits"
    lines = [
        "REPO PROBE SUMMARY%s" % (f" -> {output}" if output else ""),
        f"  git: {git.get('branch') or '-'} @ {head} | "
        f"tracked={git['tracked_file_count']} untracked={git['untracked_file_count']} dirty={git['dirty_file_count']}",
        f"  Vg (verification gap): {vg['vg']} | declared={vg['declared_checks']} enforced={vg['enforced_checks']}",
        f"  Ce (context entropy): {ce['ce']} | {ce['notes']}",
        f"  tests: {coll['test_file_count']} files | pytest-config={coll['pytest_config_present']}",
        f"  fixture coverage: {fx['covered_validators']}/{fx['total_validators']} "
        f"({fx['coverage']}) missing={fx['missing_fixtures']}",
        f"  churn: {ch['commits_scanned']} commits, {ch['changed_files_last_n']} files; top: {ch['top_changed_files']}",
        f"  relationships: version findings={len(rel_ver)} adr findings={len(rel_adr)} "
        f"(evidence candidates, not diagnoses)",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic repository probes.")
    parser.add_argument("--repo-root", default=".", help="Repository to probe (default: current dir)")
    parser.add_argument("--output", default="probe-report.yaml", help="Report output path")
    parser.add_argument("--churn-commits", type=int, default=50, help="Commits to scan for churn")
    parser.add_argument("--no-write", action="store_true", help="Print summary only")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
    except OSError:
        print(f"[probe] ERROR: repo-root path is not accessible: {args.repo_root}", file=sys.stderr)
        return 2
    if not repo_root.is_dir():
        print(f"[probe] ERROR: repo-root is not a directory: {repo_root}", file=sys.stderr)
        return 2

    report = probe_all(repo_root, churn_commits=args.churn_commits)

    output: Path | None = None
    if not args.no_write:
        output = Path(args.output).resolve()
        output.write_text(yaml.safe_dump(report, sort_keys=False), encoding="utf-8")

    print(_summary(report, output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
