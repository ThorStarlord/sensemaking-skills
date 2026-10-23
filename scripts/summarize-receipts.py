"""Read Sensemaking receipts and report what a new session must pick up.

This is the consumer side of the receipt contract: a receipt nobody reads is
documentation theater. At session start, `using-sensemaking` runs this reader
over the target repository's `.sensemaking/receipts/` directory.

It reports, mechanically and without judging meaning:
  - every receipt (session_ref, state, stop disposition, persistence);
  - receipts still `in_progress` (sessions that never finalized: possibly interrupted);
  - open questions not resolved by any later receipt's continuity.resolves_questions;
  - the latest final session's next warranted responsibility and blockers;
  - knowledge misses not yet ADDED or closed as NO_MODEL_CHANGE;
  - misses whose subject or terms recur across two or more sessions;
  - receipts that were not durably persisted;
  - receipts that fail validation.

Exit codes: 0 = every receipt valid (or no receipts), 1 = at least one invalid receipt,
2 = usage error. Output is ASCII-only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
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


def summarize(receipt_dir: Path) -> dict[str, Any]:
    files = sorted(
        p for p in receipt_dir.glob("*.yaml")
        if p.name.endswith(".session.yaml") or p.name.endswith(".query.yaml")
    ) if receipt_dir.is_dir() else []

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
        record = {"file": path.name, "data": data}
        (sessions if artifact_id == _validator.SESSION_RECEIPT_ID else queries).append(record)

    sessions.sort(key=lambda r: (r["data"]["session_ref"], r["data"]["updated_at"]))
    queries.sort(key=lambda r: (r["data"]["session_ref"], r["data"]["updated_at"]))

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
    latest = finals[-1]["data"] if finals else None
    next_step = None
    if latest is not None:
        next_step = {
            "from_session": latest["session_ref"],
            "stop": latest["stop"]["disposition"],
            "warranted_responsibility": latest["next"]["warranted_responsibility"],
            "blocked_on": latest["next"]["blocked_on"],
        }

    unfinished = [
        {"receipt": r["file"], "updated_at": r["data"]["updated_at"]}
        for r in sessions + queries if r["data"]["state"] == "in_progress"
    ]
    not_durable = [
        {"receipt": r["file"], "persistence": r["data"]["persistence"]}
        for r in sessions + queries if r["data"]["persistence"] in ("pending", "working_tree_only")
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
            }
            for r in sessions + queries
        ],
        "unfinished": unfinished,
        "open_questions": open_questions,
        "next": next_step,
        "pending_misses": pending_misses,
        "repeated_misses": repeated_misses,
        "not_durable": not_durable,
        "invalid": invalid,
    }


def _print_text(summary: dict[str, Any]) -> None:
    lines = [f"RECEIPTS in {summary['receipt_dir']}: {len(summary['receipts'])} valid, {len(summary['invalid'])} invalid"]
    for r in summary["receipts"]:
        stop = f" stop={r['stop']}" if r["stop"] else ""
        lines.append(f"  {r['receipt']}: {r['state']}{stop} persistence={r['persistence']}")
    lines.append(f"UNFINISHED (in_progress; possibly interrupted): {len(summary['unfinished'])}")
    lines.extend(f"  {u['receipt']} (last update {u['updated_at']})" for u in summary["unfinished"])
    lines.append(f"OPEN QUESTIONS: {len(summary['open_questions'])}")
    for q in summary["open_questions"]:
        flag = "BLOCKING " if q["blocking"] else ""
        lines.append(f"  {flag}{q['ref']} [{q['source']}] {q['question']}")
        lines.extend(f"    - option: {option}" for option in q["options"])
    nxt = summary["next"]
    if nxt:
        lines.append(f"NEXT (from {nxt['from_session']}, stop={nxt['stop']}): {nxt['warranted_responsibility']}")
        if nxt["blocked_on"]:
            lines.append(f"  blocked on: {', '.join(nxt['blocked_on'])}")
    else:
        lines.append("NEXT: no final session receipt")
    lines.append(f"PENDING KNOWLEDGE MISSES: {len(summary['pending_misses'])}")
    for m in summary["pending_misses"]:
        ref = f" proposal={m['proposal_ref']}" if m["proposal_ref"] else ""
        lines.append(f"  {m['ref']} {m['follow_up']}: {m['needed_for']}{ref}")
    lines.append(f"REPEATED MISSES (same subject/term in 2+ sessions): {len(summary['repeated_misses'])}")
    lines.extend(f"  {m['key']}: {', '.join(m['sessions'])}" for m in summary["repeated_misses"])
    lines.append(f"NOT DURABLE: {len(summary['not_durable'])}")
    lines.extend(f"  {n['receipt']} persistence={n['persistence']}" for n in summary["not_durable"])
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
    summary = summarize(receipt_dir)
    if args.json:
        print(_ascii(json.dumps(summary, indent=2)))
    else:
        _print_text(summary)
    return 1 if summary["invalid"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
