"""Read Sensemaking receipts and report what a new session must pick up.

This is the consumer side of the receipt contract: a receipt nobody reads is
documentation theater. At session start, `using-sensemaking` runs this reader
over the target repository's `.sensemaking/receipts/` directory.

It reports, mechanically and without judging meaning:
  - every receipt (session_ref, state, stop disposition, persistence);
  - receipts still `in_progress` (sessions that never finalized: possibly interrupted);
  - open questions not resolved by any later receipt's continuity.resolves_questions;
  - final sessions' next responsibilities and predecessor links, plus the
    latest final session by update time (not a relevance or authority decision);
  - knowledge misses recorded as ADD_PROPOSED or DEFERRED at the time;
  - misses whose subject or terms recur across two or more sessions;
  - receipts whose declared persistence is non-durable and that HEAD does not
    contain (the declared value is historical: session-receipt-v1 section 3);
  - declared non-durable receipts that HEAD does contain (reported separately);
  - receipts that fail validation;
  - the facts that show whether knowledge queries are still being recorded: the
    last query receipt, the latest commit that changed reviewed knowledge and
    how many such commits are dated after that receipt's update, and the
    sessions naming the Steward that left no query receipt.

It does not count which knowledge records receipts list. Those lists are chosen
by the session that wrote them, so a count would measure recording habits, not
retrieval or use.

Exit codes: 0 = every receipt valid (or no receipts), 1 = at least one invalid receipt,
2 = usage error. Output is ASCII-only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_receipt", _HERE / "validate-receipt.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_validator = _load_validator()

_MISS_STATUS_NOTE = (
    "Statuses are historical as recorded in each receipt; later sessions may "
    "have resolved them. Check later receipts and current knowledge."
)


def _ascii(text: Any) -> str:
    return str(text).encode("ascii", "replace").decode("ascii")


def _miss_keys(query: dict | None) -> list[str]:
    if not isinstance(query, dict):
        return []
    keys: list[str] = []
    subject = query.get("subject")
    if isinstance(subject, str) and subject.strip():
        keys.append(f"subject:{subject.strip()}")
    for term in query.get("terms") or []:
        if isinstance(term, str) and term.strip():
            keys.append(f"term:{term.strip().lower()}")
    return keys


_NON_DURABLE = ("pending", "working_tree_only")


def _committed_receipt_names(repo_root: Path | None, receipt_dir: Path) -> set[str] | None:
    """File names of the receipts that HEAD contains, or None when Git cannot say."""
    if repo_root is None:
        return None
    try:
        relative = receipt_dir.resolve().relative_to(repo_root.resolve()).as_posix()
        result = subprocess.run(
            ["git", "-C", str(repo_root), "ls-tree", "-r", "--name-only", "HEAD", "--", relative],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (ValueError, OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    prefix = "" if relative == "." else f"{relative}/"
    return {line[len(prefix):] for line in result.stdout.splitlines() if line.startswith(prefix)}


_KNOWLEDGE_DIR = ".sensemaking/knowledge"
_STEWARD = "repository-semantic-steward"


def _git_lines(repo_root: Path | None, *args: str) -> list[str] | None:
    """Output lines of one read-only Git command, or None when Git cannot answer."""
    if repo_root is None:
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "-c", "color.ui=never", *args], capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=60, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.splitlines() if result.returncode == 0 else None


def _receipt_target(sessions: list[dict], queries: list[dict], override: str | None) -> tuple[str | None, list[str]]:
    """The repository these receipts describe, and the rivals when that is ambiguous.

    Without an override it is the target most receipts declare, which the output
    names so a wrong choice is visible. A tie is reported and nothing is counted.
    """
    if override:
        return override, []
    counts: dict[str, int] = defaultdict(int)
    for record in sessions + queries:
        counts[record["data"]["target_repository"]] += 1
    if not counts:
        return None, []
    top = max(counts.values())
    leaders = sorted(name for name, count in counts.items() if count == top)
    return (leaders[0], []) if len(leaders) == 1 else (None, leaders)


def _knowledge_commits(repo_root: Path | None, receipt_dir: Path, last: dict) -> dict[str, Any]:
    """Commit dates of reviewed-knowledge changes, set beside the last query receipt's update time.

    Dates are compared as instants and every commit is read, so time zones and
    out-of-order dates do not matter. The commit that added the receipt is left
    out. A parallel branch or an imprecise receipt time can still move the count,
    which is why the latest commit is shown as well.
    """
    unknown = {"latest": None, "dated_after_last_query_receipt": None}
    if repo_root is None:
        return {**unknown, "note": "no repository given"}
    shallow = _git_lines(repo_root, "rev-parse", "--is-shallow-repository")
    if shallow is None:
        return {**unknown, "note": "not a Git repository"}
    if shallow and shallow[0].strip() == "true":
        return {**unknown, "note": "shallow clone"}
    try:
        updated = datetime.strptime(last["data"]["updated_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc).timestamp()
        relative = (receipt_dir.resolve() / last["file"]).relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return {**unknown, "note": "receipt time or location could not be read"}
    log = _git_lines(repo_root, "log", "--no-merges", "--full-history", "--format=%H %ct",
                     "--", _KNOWLEDGE_DIR)
    if log is None:
        return {**unknown, "note": "Git could not list knowledge commits"}
    adding = _git_lines(repo_root, "log", "--diff-filter=A", "--format=%H", "-1", "--", relative) or []
    commits = [(line.split()[0], int(line.split()[1])) for line in log if len(line.split()) == 2]
    latest = max(commits, key=lambda item: item[1], default=None)
    return {
        "latest": None if latest is None else {
            "commit": latest[0],
            "committed_at": datetime.fromtimestamp(latest[1], timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "dated_after_last_query_receipt": sum(
            1 for commit, when in commits if when > updated and commit not in adding),
        "note": None,
    }


def _knowledge_recording(
    sessions: list[dict], queries: list[dict], repo_root: Path | None, receipt_dir: Path,
    target: str | None, rivals: list[str],
) -> dict[str, Any]:
    """Facts about whether knowledge queries are still recorded. No verdict and no tally of use."""
    if target is None:
        return {"target_repository": None, "target_ambiguous_between": rivals,
                "query_receipt_total": None, "last_query_receipt": None, "knowledge_commits": None,
                "steward_session_total": None, "steward_sessions_without_query_receipt": None,
                "steward_sessions_without_query_receipt_after_last": None,
                "other_target_query_receipts": None}
    local = [r for r in queries if r["data"]["target_repository"] == target]
    last = max(local, key=lambda r: (r["data"]["updated_at"], r["file"]), default=None)
    # A companion written for another target still shows that the session recorded its queries.
    recorded_refs = {r["data"]["session_ref"] for r in queries}
    steward = [
        r["data"] for r in sessions
        if r["data"]["target_repository"] == target and any(
            _STEWARD in (item.get("capability") or "")
            for item in r["data"].get("responsibilities") or [])
    ]
    missing = [data for data in steward if data["session_ref"] not in recorded_refs]
    return {
        "target_repository": target,
        "target_ambiguous_between": [],
        "query_receipt_total": len(local),
        "last_query_receipt": None if last is None else {
            "receipt": last["file"], "updated_at": last["data"]["updated_at"]},
        "knowledge_commits": None if last is None else _knowledge_commits(repo_root, receipt_dir, last),
        "steward_session_total": len(steward),
        "steward_sessions_without_query_receipt": sorted(data["session_ref"] for data in missing),
        "steward_sessions_without_query_receipt_after_last": None if last is None else sorted(
            data["session_ref"] for data in missing
            if data["updated_at"] > last["data"]["updated_at"]),
        "other_target_query_receipts": sorted(
            r["file"] for r in queries if r["data"]["target_repository"] != target),
    }


def summarize(
    receipt_dir: Path, repo_root: Path | None = None, *, target_repository: str | None = None,
) -> dict[str, Any]:
    files = sorted(
        p for p in receipt_dir.glob("*.yaml")
        if p.name.endswith(".session.yaml") or p.name.endswith(".query.yaml")
    ) if receipt_dir.is_dir() else []
    committed = _committed_receipt_names(repo_root, receipt_dir)

    sessions: list[dict] = []
    queries: list[dict] = []
    invalid: list[dict] = []
    for path in files:
        artifact_id, checker = _validator.validate_receipt(path)
        if not checker.valid:
            invalid.append({
                "file": path.name,
                "errors": [f"{f['code']} {f['field']}" for f in checker.findings if f["severity"] == "error"],
            })
            continue
        data, _ = _validator.load_receipt(path)
        record = {
            "file": path.name,
            "data": data,
            "committed_in_head": None if committed is None else path.name in committed,
        }
        (sessions if artifact_id == _validator.SESSION_RECEIPT_ID else queries).append(record)

    sessions.sort(key=lambda r: (r["data"]["updated_at"], r["data"]["session_ref"]))
    queries.sort(key=lambda r: (r["data"]["updated_at"], r["data"]["session_ref"]))

    resolved: set[str] = set()
    for record in sessions:
        resolved.update(record["data"]["continuity"].get("resolves_questions") or [])

    open_questions = []
    for record in sessions:
        data = record["data"]
        for question in data.get("open_questions") or []:
            qualified = f"{data['session_ref']}#{question['id']}"
            if qualified not in resolved:
                open_questions.append({
                    "ref": qualified,
                    "source": question["source"],
                    "blocking": question["blocking"],
                    "question": question["question"],
                    "options": [o["option"] for o in question.get("options") or []],
                    "durable_ref": question.get("durable_ref"),
                })

    finals = [r for r in sessions if r["data"]["state"] == "final"]
    final_sessions = [
        {
            "from_session": r["data"]["session_ref"],
            "updated_at": r["data"]["updated_at"],
            "resumes": r["data"]["continuity"].get("resumes"),
            "stop": r["data"]["stop"]["disposition"],
            "warranted_responsibility": r["data"]["next"]["warranted_responsibility"],
            "blocked_on": r["data"]["next"]["blocked_on"],
        }
        for r in finals
    ]
    latest = final_sessions[-1] if final_sessions else None
    # A tie is not a chronological ordering; disclose it instead of silently
    # treating the lexicographic tiebreak as a later session.
    latest_ties = [r["from_session"] for r in final_sessions
                   if latest is not None and r["updated_at"] == latest["updated_at"]]
    next_step = latest if len(latest_ties) == 1 else None

    unfinished = [
        {"receipt": r["file"], "updated_at": r["data"]["updated_at"]}
        for r in sessions + queries if r["data"]["state"] == "in_progress"
    ]
    # The declared persistence is written once and never edited (receipts are
    # immutable), so it can lag a later commit. Current durability is whether
    # HEAD contains the file; when Git cannot answer, the declaration stands.
    not_durable = [
        {"receipt": r["file"], "persistence": r["data"]["persistence"],
         "committed_in_head": r["committed_in_head"]}
        for r in sessions + queries
        if r["data"]["persistence"] in _NON_DURABLE and r["committed_in_head"] is not True
    ]
    declared_but_committed = [
        {"receipt": r["file"], "persistence": r["data"]["persistence"]}
        for r in sessions + queries
        if r["data"]["persistence"] in _NON_DURABLE and r["committed_in_head"] is True
    ]

    pending_misses = []
    miss_sessions: dict[str, set[str]] = defaultdict(set)
    for record in queries:
        data = record["data"]
        by_id = {q["id"]: q for q in data.get("queries") or []}
        for miss in data.get("misses") or []:
            query = by_id.get(miss["query_ref"])
            for key in _miss_keys(query):
                miss_sessions[key].add(data["session_ref"])
            if miss["follow_up"] in ("ADD_PROPOSED", "DEFERRED"):
                pending_misses.append({
                    "ref": f"{data['session_ref']}#{miss['id']}",
                    "needed_for": miss["needed_for"],
                    "follow_up": miss["follow_up"],
                    "proposal_ref": miss.get("proposal_ref"),
                })
    repeated_misses = [
        {"key": key, "sessions": sorted(refs)}
        for key, refs in sorted(miss_sessions.items()) if len(refs) >= 2
    ]

    target, rivals = _receipt_target(sessions, queries, target_repository)

    return {
        "receipt_dir": str(receipt_dir),
        "receipts": [
            {
                "receipt": r["file"],
                "kind": "session" if r in sessions else "query",
                "state": r["data"]["state"],
                "stop": r["data"]["stop"]["disposition"] if r in sessions else None,
                "persistence": r["data"]["persistence"],
                "committed_in_head": r["committed_in_head"],
            }
            for r in sessions + queries
        ],
        "unfinished": unfinished,
        "open_questions": open_questions,
        "next": next_step,
        "final_sessions": final_sessions,
        "latest_ties": latest_ties if len(latest_ties) > 1 else [],
        "pending_misses": pending_misses,
        "pending_misses_note": _MISS_STATUS_NOTE,
        "repeated_misses": repeated_misses,
        "not_durable": not_durable,
        "declared_but_committed": declared_but_committed,
        "invalid": invalid,
        "knowledge_recording": _knowledge_recording(sessions, queries, repo_root, receipt_dir,
                                                    target, rivals),
    }


def _recording_lines(recording: dict[str, Any]) -> list[str]:
    if recording["target_ambiguous_between"]:
        return ["KNOWLEDGE QUERY RECORDING: not reported; receipts name several target repositories "
                f"equally often ({', '.join(recording['target_ambiguous_between'])}). "
                "Pass --target-repository."]
    if recording["target_repository"] is None:
        return ["KNOWLEDGE QUERY RECORDING: no receipts"]
    last = recording["last_query_receipt"]
    lines = [f"KNOWLEDGE QUERY RECORDING ({recording['target_repository']}): "
             f"{recording['query_receipt_total']} query receipts; last "
             + (f"{last['receipt']} (updated {last['updated_at']})" if last else "none")]
    commits = recording["knowledge_commits"]
    if commits is not None:
        if commits["note"]:
            lines.append(f"  commits changing {_KNOWLEDGE_DIR}/ since that update: unknown ({commits['note']})")
        elif commits["latest"] is None:
            lines.append(f"  no commit changes {_KNOWLEDGE_DIR}/")
        else:
            lines.append(f"  latest non-merge commit changing {_KNOWLEDGE_DIR}/: "
                         f"{commits['latest']['committed_at']} ({commits['latest']['commit'][:8]}); "
                         f"{commits['dated_after_last_query_receipt']} such commits are dated after "
                         "that update")
    missing = recording["steward_sessions_without_query_receipt"]
    after = recording["steward_sessions_without_query_receipt_after_last"]
    lines.append(f"  sessions naming {_STEWARD} without a query receipt: "
                 f"{len(missing)} of {recording['steward_session_total']}"
                 + ("" if after is None else f" ({len(after)} updated after the last query receipt)"))
    if recording["other_target_query_receipts"]:
        lines.append("  query receipts for another target repository (not counted above): "
                     f"{len(recording['other_target_query_receipts'])}")
    return lines


def _print_text(summary: dict[str, Any]) -> None:
    lines = [f"RECEIPTS in {summary['receipt_dir']}: {len(summary['receipts'])} valid, {len(summary['invalid'])} invalid"]
    for r in summary["receipts"]:
        stop = f" stop={r['stop']}" if r["stop"] else ""
        committed = {True: "yes", False: "no", None: "unknown"}[r["committed_in_head"]]
        lines.append(
            f"  {r['receipt']}: {r['state']}{stop} persistence={r['persistence']}"
            f" committed_in_head={committed}"
        )
    lines.append(f"UNFINISHED (in_progress; possibly interrupted): {len(summary['unfinished'])}")
    lines.extend(f"  {u['receipt']} (last update {u['updated_at']})" for u in summary["unfinished"])
    lines.append(f"OPEN QUESTIONS: {len(summary['open_questions'])}")
    for q in summary["open_questions"]:
        flag = "BLOCKING " if q["blocking"] else ""
        lines.append(f"  {flag}{q['ref']} [{q['source']}] {q['question']}")
        lines.extend(f"    - option: {option}" for option in q["options"])
    lines.append("FINAL SESSIONS (chronological; assess relevance and linked corrections):")
    for session in summary["final_sessions"]:
        predecessor = f" resumes={session['resumes']}" if session["resumes"] else ""
        lines.append(
            f"  {session['from_session']} updated={session['updated_at']}"
            f"{predecessor} stop={session['stop']} next={session['warranted_responsibility']}"
        )
        if session["blocked_on"]:
            lines.append(f"    blocked on: {', '.join(session['blocked_on'])}")
    nxt = summary["next"]
    if nxt:
        lines.append(f"NEXT (from {nxt['from_session']}, stop={nxt['stop']}): {nxt['warranted_responsibility']}")
        if nxt["blocked_on"]:
            lines.append(f"  blocked on: {', '.join(nxt['blocked_on'])}")
    elif summary["latest_ties"]:
        lines.append(f"NEXT: latest update time tied: {', '.join(summary['latest_ties'])}")
    else:
        lines.append("NEXT: no final session receipt")
    lines.append(f"HISTORICAL KNOWLEDGE MISSES (ADD_PROPOSED or DEFERRED): {len(summary['pending_misses'])}")
    lines.append(f"  {_MISS_STATUS_NOTE}")
    for m in summary["pending_misses"]:
        ref = f" proposal={m['proposal_ref']}" if m["proposal_ref"] else ""
        lines.append(f"  {m['ref']} {m['follow_up']}: {m['needed_for']}{ref}")
    lines.append(f"REPEATED MISSES (same subject/term in 2+ sessions): {len(summary['repeated_misses'])}")
    lines.extend(f"  {m['key']}: {', '.join(m['sessions'])}" for m in summary["repeated_misses"])
    lines.append(f"NOT DURABLE (declared non-durable; not confirmed committed in HEAD): {len(summary['not_durable'])}")
    lines.extend(f"  {n['receipt']} persistence={n['persistence']}" for n in summary["not_durable"])
    lines.append(
        "DECLARED NON-DURABLE BUT COMMITTED IN HEAD (historical declaration; "
        f"receipts are immutable): {len(summary['declared_but_committed'])}"
    )
    lines.extend(f"  {n['receipt']} persistence={n['persistence']}" for n in summary["declared_but_committed"])
    lines.extend(_recording_lines(summary["knowledge_recording"]))
    if summary["invalid"]:
        lines.append("INVALID RECEIPTS (run scripts/validate-receipt.py for detail):")
        lines.extend(f"  {i['file']}: {'; '.join(i['errors'])}" for i in summary["invalid"])
    print(_ascii("\n".join(lines)))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Summarize Sensemaking receipts for session start")
    parser.add_argument("--repo", default=".", help="Target repository root (default: current directory)")
    parser.add_argument("--dir", default=None, help=f"Receipt directory (default: <repo>/{_validator.RECEIPT_DIR})")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--target-repository", default=None,
                        help="Repository identity the receipts describe (default: the target most "
                             "receipts declare; a tie is reported, not guessed)")
    args = parser.parse_args(argv)

    receipt_dir = Path(args.dir) if args.dir else Path(args.repo) / _validator.RECEIPT_DIR
    summary = summarize(receipt_dir, Path(args.repo), target_repository=args.target_repository)
    if args.json:
        print(_ascii(json.dumps(summary, indent=2)))
    else:
        _print_text(summary)
    return 1 if summary["invalid"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
