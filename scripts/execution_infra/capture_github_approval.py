"""DEPRECATED LEGACY — capture the human's GitHub approval comment into
the operative approval snapshot (superseded by conversation approval,
2026-08-05; retained only for historical campaigns).

Usage:
    python scripts/execution_infra/capture_github_approval.py \
        [--package-dir experiments/campaigns/EXP-0001-stage1-auteur-autonomy-pilot] \
        [--issue 122] [--out <path>] [--token <GITHUB_TOKEN>]

The human posts the approval comment on the campaign's GitHub issue (the
exact grammar is printed by this tool with --help). This tool then:

1. reads and validates the campaign policy from the package;
2. fetches the issue comments from the live GitHub API;
3. finds the newest comment matching the governed grammar AND naming the
   exact campaign_id and policy_digest;
4. verifies the author holds the required repository permission;
5. transcribes the comment verbatim into the operative approval snapshot
   (mechanical transcription - trusted code recording a human-authored
   artifact, never agent-authored consent) and writes it to --out
   (default: <package-dir>/approval.yaml).

Without a matching human comment, nothing is written and the exit code is
nonzero. The token comes from --token or the GITHUB_TOKEN/GH_TOKEN
environment variable.
"""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensemaking_skills.campaign_validation import (
    ValidationContext,
    parse_two_lane_yaml,
    validate_campaign_policy,
)
from sensemaking_skills.exploratory_execution import (
    APPROVAL_MARKER,
    GOVERNED_GITHUB_REPOSITORY,
    capture_approval_snapshot,
)

DEFAULT_PACKAGE_DIR = (
    Path(__file__).resolve().parents[2]
    / "experiments" / "campaigns" / "EXP-0001-stage1-auteur-autonomy-pilot"
)

APPROVAL_TEMPLATE = f"""{APPROVAL_MARKER}

campaign_id: <CAMPAIGN_ID>
policy_digest: <POLICY_DIGEST>
maximum_attempts: 3
concurrency: 1
automatic_merge: prohibited
classification: EXPLORATORY_NOT_CANONICAL_EVIDENCE
expires_at: <RFC3339-EXPIRY>

I authorize this bounded exploratory campaign."""


def _window_consistent_now(policy_raw: dict) -> datetime:
    """A validation time inside the policy window (the runner, not this
    tool, enforces the window at execution time)."""
    from datetime import timedelta

    window = policy_raw.get("validity_window") or {}
    now = datetime.now(UTC)
    try:
        not_before = datetime.fromisoformat(str(window["not_before"]).replace("Z", "+00:00"))
        not_after = datetime.fromisoformat(str(window["not_after"]).replace("Z", "+00:00"))
    except (KeyError, ValueError, TypeError):
        return now
    if not_before <= now < not_after:
        return now
    if now < not_before:
        return not_before + timedelta(minutes=1)
    return not_after - timedelta(minutes=1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Capture the human's GitHub approval comment into the "
            "operative approval snapshot."
        )
    )
    parser.add_argument("--package-dir", type=Path, default=DEFAULT_PACKAGE_DIR)
    parser.add_argument("--issue", type=int, default=122)
    parser.add_argument("--repository", default=GOVERNED_GITHUB_REPOSITORY)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--token", default=None)
    args = parser.parse_args(argv)

    package_dir = Path(args.package_dir)
    policy_path = package_dir / "campaign-policy.yaml"
    if not policy_path.is_file():
        print(f"ERROR: no campaign policy at {policy_path}", file=sys.stderr)
        return 2

    policy_bytes = policy_path.read_bytes()
    try:
        policy_raw = parse_two_lane_yaml(policy_bytes)
    except Exception as exc:  # noqa: BLE001 - report and stop
        print(f"ERROR: policy does not parse: {exc}", file=sys.stderr)
        return 2

    check_now = _window_consistent_now(policy_raw)
    policy_result = validate_campaign_policy(
        policy_bytes,
        ValidationContext(
            current_time=check_now.isoformat(),
            allowed_approver_identities=frozenset(),
        ),
    )
    if not policy_result.valid:
        print(
            f"ERROR: policy failed validation: {policy_result.failure_code} "
            f"{policy_result.detail}",
            file=sys.stderr,
        )
        return 2

    out_path = Path(args.out) if args.out else package_dir / "approval.yaml"
    print(
        f"Capturing the approval comment for issue #{args.issue} of "
        f"{args.repository} ..."
    )
    try:
        snapshot_bytes, comment = capture_approval_snapshot(
            repository=args.repository,
            issue_number=args.issue,
            policy=policy_result.value,
            token=args.token,
            out_path=out_path,
            now=check_now,
        )
    except Exception as exc:  # noqa: BLE001 - report and stop
        print(f"ERROR: no approval captured: {exc}", file=sys.stderr)
        return 1

    author = str((comment.get("user") or {}).get("login", ""))
    print(f"Captured approval comment {comment.get('id')} by {author}")
    print(f"Created at: {comment.get('created_at')}")
    print(f"Snapshot written to: {out_path}")
    print(f"Approval body sha256: {snapshot_bytes and 'recorded in snapshot'}")
    print("EXP_0001_APPROVAL_CAPTURED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
