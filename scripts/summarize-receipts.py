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
  - receipts whose declared persistence is non-durable and whose current content
    HEAD does not hold (the declared value is historical: session-receipt-v1 section 3);
  - declared non-durable receipts whose current content HEAD does hold (reported
    separately);
  - where each receipt's current content is recorded in Git: a remote-tracking ref
    (as of the last fetch), local refs only, or no ref holding that exact content
    (declared persistence is not changed by this);
  - receipts that fail validation.

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
    question = query.get("query_text")
    if isinstance(question, str) and question.strip():
        # A repeated question is a literal historical observation, not a
        # semantic-similarity or inferred-relevance judgment.
        keys.append(f"question:{' '.join(question.split()).casefold()}")
    return keys


_NON_DURABLE = ("pending", "working_tree_only")


def _relative_receipt_dir(repo_root: Path | None, receipt_dir: Path) -> str | None:
    """The receipt directory relative to the repository root, or None when Git cannot say."""
    if repo_root is None:
        return None
    try:
        return receipt_dir.resolve().relative_to(repo_root.resolve()).as_posix()
    except (ValueError, OSError):
        return None


def _is_receipt_child(path: str, prefix: str) -> bool:
    """True when a repository path is a direct child of the receipt directory."""
    return path.startswith(prefix) and "/" not in path[len(prefix):]


def _head_receipt_blobs(repo_root: Path | None, receipt_dir: Path) -> dict[str, str] | None:
    """Receipt file name -> blob id that HEAD holds for it, or None when Git cannot say."""
    relative = _relative_receipt_dir(repo_root, receipt_dir)
    if relative is None:
        return None
    prefix = "" if relative == "." else f"{relative}/"
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "ls-tree", "-r", "--full-tree", "HEAD", "--", relative],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    blobs: dict[str, str] = {}
    for line in result.stdout.splitlines():
        meta, _, path = line.partition("\t")
        fields = meta.split()
        if len(fields) == 3 and fields[1] == "blob" and _is_receipt_child(path, prefix):
            blobs[path[len(prefix):]] = fields[2]
    return blobs


def _history_receipt_blobs(repo_root: Path | None, receipt_dir: Path,
                           scope: str) -> set[tuple[str, str]] | None:
    """(file name, blob id) for each receipt version that a commit on the given refs adds, or None.

    ``scope`` is ``--remotes`` (remote-tracking refs as of the last fetch) or ``--all``. A version
    counts only with its exact content: a commit that merely touched the file name is not enough.
    ``-m`` diffs a merge against every parent, so content that a merge introduces is included.
    Deletions are skipped.
    """
    relative = _relative_receipt_dir(repo_root, receipt_dir)
    if relative is None:
        return None
    prefix = "" if relative == "." else f"{relative}/"
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "log", scope, "-m", "--root", "--no-renames",
             "--raw", "--no-abbrev", "--format=", "--", relative],
            capture_output=True, text=True, timeout=60, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    versions: set[tuple[str, str]] = set()
    for line in result.stdout.splitlines():
        if not line.startswith(":"):
            continue
        meta, _, path = line.partition("\t")
        fields = meta.split()
        if len(fields) != 5 or set(fields[3]) == {"0"} or not _is_receipt_child(path, prefix):
            continue
        versions.add((path[len(prefix):], fields[3]))
    return versions


def _working_receipt_blobs(repo_root: Path | None, receipt_dir: Path,
                           names: list[str]) -> dict[str, str] | None:
    """Receipt file name -> blob id of its current working-tree content, or None when Git cannot say.

    ``git hash-object`` applies the same clean filters as ``git add``, so each id is the id a
    commit of the current content would store.
    """
    if not names:
        return {}
    relative = _relative_receipt_dir(repo_root, receipt_dir)
    if relative is None:
        return None
    prefix = "" if relative == "." else f"{relative}/"
    try:
        # Bytes input avoids newline translation of paths on Windows.
        result = subprocess.run(
            ["git", "-C", str(repo_root), "hash-object", "--stdin-paths"],
            input="".join(f"{prefix}{name}\n" for name in names).encode("utf-8"),
            capture_output=True, timeout=60, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    hashes = result.stdout.decode("ascii", "replace").split()
    if result.returncode != 0 or len(hashes) != len(names):
        return None
    return dict(zip(names, hashes))


def _remote_durability(records: list[dict], current_blobs: dict[str, str] | None,
                       remote_versions: set[tuple[str, str]] | None,
                       any_ref_versions: set[tuple[str, str]] | None,
                       checked_out_names: set[str]) -> dict[str, Any]:
    """Where each receipt's current content is recorded in Git, separately from its declared persistence.

    ``on_remote_ref``: a commit reachable from a remote-tracking ref in this clone (as of the
    last fetch) holds the receipt's exact current content. ``local_git_only``: only local refs
    hold that content, so it is lost with this clone. ``uncommitted``: no ref holds it, which
    includes a receipt edited after its last commit. Counts only. ``local_only_not_checked_out``:
    receipt names that local refs hold but this checkout does not contain; their content is not
    read or validated here.
    """
    if current_blobs is None or remote_versions is None or any_ref_versions is None:
        return {"available": False, "on_remote_ref": [], "local_git_only": [], "uncommitted": [],
                "local_only_not_checked_out": []}
    remote_names = {name for name, _ in remote_versions}
    buckets: dict[str, list[dict[str, str]]] = {"on_remote_ref": [], "local_git_only": [], "uncommitted": []}
    for record in records:
        version = (record["file"], current_blobs[record["file"]])
        entry = {"receipt": record["file"], "persistence": record["data"]["persistence"]}
        if version in remote_versions:
            buckets["on_remote_ref"].append(entry)
        elif version in any_ref_versions:
            buckets["local_git_only"].append(entry)
        else:
            buckets["uncommitted"].append(entry)
    not_checked_out = sorted(
        name for name in {name for name, _ in any_ref_versions}
        if name not in remote_names and name not in checked_out_names
        and name.endswith((".session.yaml", ".query.yaml"))
    )
    return {"available": True, **buckets,
            "local_only_not_checked_out": [{"receipt": name} for name in not_checked_out]}


def summarize(receipt_dir: Path, repo_root: Path | None = None) -> dict[str, Any]:
    files = sorted(
        p for p in receipt_dir.glob("*.yaml")
        if p.name.endswith(".session.yaml") or p.name.endswith(".query.yaml")
    ) if receipt_dir.is_dir() else []
    head_blobs = _head_receipt_blobs(repo_root, receipt_dir)
    current_blobs = _working_receipt_blobs(repo_root, receipt_dir, [p.name for p in files])
    remote_versions = _history_receipt_blobs(repo_root, receipt_dir, "--remotes")
    any_ref_versions = _history_receipt_blobs(repo_root, receipt_dir, "--all")

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
            # HEAD must hold this receipt's current content, not merely a file of this name.
            "committed_in_head": None if head_blobs is None or current_blobs is None
            else head_blobs.get(path.name) == current_blobs[path.name],
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
    # HEAD holds the file's current content; when Git cannot answer, the
    # declaration stands.
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
        "remote_durability": _remote_durability(
            sessions + queries, current_blobs, remote_versions, any_ref_versions, {p.name for p in files}),
        "invalid": invalid,
    }


_ENTRY_LIST_LIMIT = 25


def _entry_lines(entries: list[dict[str, str]]) -> list[str]:
    lines = [f"    {n['receipt']} persistence={n['persistence']}" for n in entries[:_ENTRY_LIST_LIMIT]]
    if len(entries) > _ENTRY_LIST_LIMIT:
        lines.append(f"    ... and {len(entries) - _ENTRY_LIST_LIMIT} more")
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
    lines.append(f"REPEATED MISSES (same subject/term/question in 2+ sessions): {len(summary['repeated_misses'])}")
    lines.extend(f"  {m['key']}: {', '.join(m['sessions'])}" for m in summary["repeated_misses"])
    lines.append(f"NOT DURABLE (declared non-durable; not confirmed committed in HEAD): {len(summary['not_durable'])}")
    lines.extend(f"  {n['receipt']} persistence={n['persistence']}" for n in summary["not_durable"])
    lines.append(
        "DECLARED NON-DURABLE BUT COMMITTED IN HEAD (historical declaration; "
        f"receipts are immutable): {len(summary['declared_but_committed'])}"
    )
    lines.extend(f"  {n['receipt']} persistence={n['persistence']}" for n in summary["declared_but_committed"])
    durability = summary["remote_durability"]
    if durability["available"]:
        lines.append(
            "REMOTE DURABILITY (current file content matched against Git history in this clone; "
            "remote-tracking refs as of the last fetch; declared persistence unchanged):"
        )
        lines.append(f"  on a remote-tracking ref: {len(durability['on_remote_ref'])}")
        lines.append(
            "  committed on local refs only (lost with this clone): "
            f"{len(durability['local_git_only'])}"
        )
        lines.extend(_entry_lines(durability["local_git_only"]))
        lines.append(
            "  no ref holds this content (uncommitted, or edited since its last commit): "
            f"{len(durability['uncommitted'])}"
        )
        lines.extend(_entry_lines(durability["uncommitted"]))
        lines.append(
            "  on local refs but not in this checkout (names only, not read or validated): "
            f"{len(durability['local_only_not_checked_out'])}"
        )
        lines.extend(f"    {n['receipt']}" for n in durability["local_only_not_checked_out"][:_ENTRY_LIST_LIMIT])
        if len(durability["local_only_not_checked_out"]) > _ENTRY_LIST_LIMIT:
            lines.append(f"    ... and {len(durability['local_only_not_checked_out']) - _ENTRY_LIST_LIMIT} more")
    else:
        lines.append("REMOTE DURABILITY: Git could not answer (no repository or no readable history)")
    if summary["invalid"]:
        lines.append("INVALID RECEIPTS (run scripts/validate-receipt.py for detail):")
        lines.extend(f"  {i['file']}: {'; '.join(i['errors'])}" for i in summary["invalid"])
    print(_ascii("\n".join(lines)))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Summarize Sensemaking receipts for session start")
    parser.add_argument("--repo", default=".", help="Target repository root (default: current directory)")
    parser.add_argument("--dir", default=None, help=f"Receipt directory (default: <repo>/{_validator.RECEIPT_DIR})")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args(argv)

    receipt_dir = Path(args.dir) if args.dir else Path(args.repo) / _validator.RECEIPT_DIR
    summary = summarize(receipt_dir, Path(args.repo))
    if args.json:
        print(_ascii(json.dumps(summary, indent=2)))
    else:
        _print_text(summary)
    return 1 if summary["invalid"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
