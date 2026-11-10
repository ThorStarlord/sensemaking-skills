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
  - whether knowledge-query recording is still alive: the last query receipt,
    knowledge commits since it, and Steward sessions that left no query receipt.

With --knowledge-use (opt-in) it also joins the query receipts to the authored
knowledge packs and reports recorded retrieval per record, split by how the
record was reached, with source checks and reconcile dispositions. That view is
descriptive: it shows retention and recorded retrieval only, never that a record
was used, helped a decision or is unused. It gives no score and no ordering by
count.

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
# How a recorded query reached the records it returned. `by_id` operations start
# from a claim ID the agent already held; `listing` operations enumerate records
# mechanically. Everything else found the record from a path, a term or a phrase.
_ROUTE_BY_OPERATION = {
    "explain": "by_id", "why": "by_id", "history": "by_id",
    "snapshot": "listing", "orientation-summary": "listing", "changes": "listing",
    "contradictions": "listing", "audit": "listing", "build": "listing", "orient": "listing",
    "proposal-check": "listing",
}
_ROUTES = ("discovery", "by_id_only", "listing_only")
_ROUTE_LABELS = {
    "discovery": "found from a path, term, phrase or change",
    "by_id_only": "only from a claim ID already held",
    "listing_only": "only in a mechanical listing",
}
_PROPOSING = ("ADD", "REVISE", "SUPERSEDE", "CONTEST")
_USE_LIMITS = (
    "Recorded use only: a session that read the packs directly, ran no recorded query or left no "
    "query receipt is invisible here.",
    "Retrieval is not use: no entry shows that a record informed, helped or changed a decision.",
    "A later day is not a different agent or an independent session.",
    "No recorded retrieval is not non-use and is no reason to remove a record.",
    "Receipts are written by the session that ran the queries; they are not observed host events.",
)
_HIT_RULE_NOTE = (
    "The receipt rules exclude HIT for a file whose ownership or a needed category is NOT_ASSESSED, "
    "so few context-for HIT outcomes do not show that the query failed."
)


def _git_lines(repo_root: Path | None, *args: str) -> list[str] | None:
    """Output lines of one read-only Git command, or None when Git cannot answer."""
    if repo_root is None:
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args], capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=60, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.splitlines() if result.returncode == 0 else None


def _local_target(sessions: list[dict], queries: list[dict], override: str | None) -> str | None:
    """The repository these receipts describe: the override, else the commonest declared target."""
    if override:
        return override
    for records in (sessions, queries):
        counts: dict[str, int] = defaultdict(int)
        for record in records:
            counts[record["data"]["target_repository"]] += 1
        if counts:
            return sorted(counts, key=lambda name: (-counts[name], name))[0]
    return None


def _knowledge_recording(
    sessions: list[dict], queries: list[dict], repo_root: Path | None, target: str | None,
) -> dict[str, Any]:
    """Whether knowledge-query recording is alive. Mechanical facts only."""
    local = [r for r in queries if r["data"]["target_repository"] == target]
    # A companion that targets another repository still shows the session recorded its queries.
    recorded_refs = {r["data"]["session_ref"] for r in queries}
    last = max((r["data"]["updated_at"] for r in local), default=None)
    steward = [
        r["data"]["session_ref"] for r in sessions
        if r["data"]["target_repository"] == target and any(
            _STEWARD in (item.get("capability") or "")
            for item in r["data"].get("responsibilities") or [])
    ]
    commits_since = None
    if last is not None:
        lines = _git_lines(repo_root, "log", "--no-merges", "--format=%H", f"--since={last}",
                           "--", _KNOWLEDGE_DIR)
        commits_since = None if lines is None else len([line for line in lines if line])
    return {
        "target_repository": target,
        "query_receipt_total": len(local),
        "last_query_receipt_updated_at": last,
        "knowledge_commits_since_last_query_receipt": commits_since,
        "steward_session_total": len(steward),
        "steward_sessions_without_query_receipt": sorted(
            ref for ref in steward if ref not in recorded_refs),
        "other_target_query_receipts": sorted(
            r["file"] for r in queries if r["data"]["target_repository"] != target),
    }


def _pack_claim_kinds(repo_root: Path | None) -> dict[str, str] | None:
    """Claim ID -> kind for the authored packs in the checkout, or None when there are none."""
    if repo_root is None:
        return None
    packs = sorted((repo_root / _KNOWLEDGE_DIR).glob("*.json"))
    kinds: dict[str, str] = {}
    for pack in packs:
        try:
            data = json.loads(pack.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        claims = data.get("claims") if isinstance(data, dict) else None
        for claim in claims if isinstance(claims, list) else []:
            if isinstance(claim, dict) and isinstance(claim.get("id"), str):
                kinds[claim["id"]] = str(claim.get("kind"))
    return kinds if packs else None


def _first_commit_days(repo_root: Path | None) -> dict[str, str] | None:
    """Commit day on which each record ID first appeared in a pack (one Git call)."""
    lines = _git_lines(repo_root, "log", "--reverse", "--format=@@%cs", "-p", "--unified=0",
                       "--", _KNOWLEDGE_DIR)
    if lines is None:
        return None
    first: dict[str, str] = {}
    day = None
    for line in lines:
        if line.startswith("@@") and len(line) == 12:
            day = line[2:]
        elif day and line.startswith("+") and '"id": "' in line:
            first.setdefault(line.split('"id": "', 1)[1].split('"', 1)[0], day)
    return first


def _route_class(operations: set[str]) -> str:
    routes = {_ROUTE_BY_OPERATION.get(operation, "discovery") for operation in operations}
    if "discovery" in routes:
        return "discovery"
    return "by_id_only" if "by_id" in routes else "listing_only"


def _knowledge_use(
    queries: list[dict], repo_root: Path | None, target: str | None,
    last_query_at: str | None, wanted: tuple[str, ...],
) -> dict[str, Any]:
    """Join query receipts to the authored packs: recorded retrieval, checks and dispositions."""
    kinds = _pack_claim_kinds(repo_root)
    if kinds is None:
        return {"available": False,
                "reason": f"no authored packs under {_KNOWLEDGE_DIR} in the given repository",
                "limits": list(_USE_LIMITS)}
    first_days = _first_commit_days(repo_root)
    last_day = last_query_at[:10] if last_query_at else None
    returned: dict[str, list[dict]] = defaultdict(list)
    checks: dict[str, list[dict]] = defaultdict(list)
    reconciled: dict[str, list[dict]] = defaultdict(list)
    absent: set[str] = set()
    check_results: dict[str, int] = defaultdict(int)
    dispositions: dict[str, int] = defaultdict(int)
    not_applied = 0
    outcomes: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for record in queries:
        data = record["data"]
        if data["target_repository"] != target:
            continue
        session, day = data["session_ref"], data["updated_at"][:10]
        for query in data.get("queries") or []:
            outcomes[query["operation"]][query["outcome"]] += 1
            ids = list((query.get("result") or {}).get("claim_ids") or [])
            if isinstance(query.get("subject"), str) and query["subject"] in kinds:
                ids.append(query["subject"])
            for cid in dict.fromkeys(ids):
                if cid in kinds:
                    returned[cid].append({"session_ref": session, "day": day,
                                          "operation": query["operation"]})
                else:
                    absent.add(cid)
        for check in data.get("source_checks") or []:
            check_results[check["result"]] += 1
            checks[check["claim_id"]].append({"session_ref": session, "day": day,
                                              "result": check["result"], "sources": check["sources"]})
        for item in data.get("reconcile") or []:
            dispositions[item["disposition"]] += 1
            if item["disposition"] in _PROPOSING and not item.get("applied"):
                not_applied += 1
            if item.get("claim_id"):
                reconciled[item["claim_id"]].append({"session_ref": session, "day": day,
                                                     "disposition": item["disposition"],
                                                     "applied": bool(item.get("applied"))})

    def late(cid: str) -> bool | None:
        if first_days is None or last_day is None:
            return None
        # A record no commit contains yet is newer than every query receipt.
        return cid not in first_days or first_days[cid] > last_day

    by_route = dict.fromkeys(_ROUTES, 0)
    later_by_route = dict.fromkeys(_ROUTES, 0)
    later_known = first_days is not None
    for cid, events in returned.items():
        by_route[_route_class({event["operation"] for event in events})] += 1
        if later_known and cid in first_days:
            later = {event["operation"] for event in events if event["day"] > first_days[cid]}
            if later:
                later_by_route[_route_class(later)] += 1
    unretrieved = [{"id": cid, "kind": kinds[cid], "added_after_last_query_receipt": late(cid)}
                   for cid in sorted(kinds) if cid not in returned]
    unresolved = []
    for cid, events in sorted(checks.items()):
        for event in events:
            if event["result"] not in ("CONTRADICTED", "STALE"):
                continue
            if not any(item["applied"] and item["day"] >= event["day"]
                       and item["disposition"] in ("REVISE", "SUPERSEDE", "CONTEST")
                       for item in reconciled.get(cid, [])):
                unresolved.append({"claim_id": cid, **event})
    records = {
        cid: {
            "kind": kinds.get(cid), "in_current_packs": cid in kinds,
            "first_committed": None if first_days is None else first_days.get(cid),
            "returned": returned.get(cid, []), "source_checks": checks.get(cid, []),
            "reconcile": reconciled.get(cid, []),
        }
        for cid in wanted
    }
    return {
        "available": True,
        "records_total": len(kinds),
        "with_recorded_retrieval": {"total": len(returned), "by_route": by_route},
        "returned_after_first_commit_day": (
            {"total": sum(later_by_route.values()), "by_route": later_by_route}
            if later_known else None),
        "no_recorded_retrieval": {
            "total": len(unretrieved),
            "added_after_last_query_receipt": (
                None if first_days is None or last_day is None
                else sum(1 for item in unretrieved if item["added_after_last_query_receipt"])),
            "records": unretrieved,
        },
        "returned_ids_not_in_current_packs": sorted(absent),
        "source_checks": {
            "total": sum(check_results.values()), "record_total": len(checks),
            "by_result": dict(sorted(check_results.items())),
            "contradicted_or_stale_without_later_applied_revision": unresolved,
        },
        "reconcile": {"by_disposition": dict(sorted(dispositions.items())),
                      "proposed_not_applied": not_applied},
        "query_outcomes": {op: dict(sorted(counts.items())) for op, counts in sorted(outcomes.items())},
        "query_outcome_note": _HIT_RULE_NOTE,
        "records": records,
        "limits": list(_USE_LIMITS),
    }


def summarize(
    receipt_dir: Path, repo_root: Path | None = None, *, knowledge_use: bool = False,
    claims: tuple[str, ...] = (), target_repository: str | None = None,
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

    target = _local_target(sessions, queries, target_repository)
    recording = _knowledge_recording(sessions, queries, repo_root, target)
    use = (
        _knowledge_use(queries, repo_root, target,
                       recording["last_query_receipt_updated_at"], tuple(dict.fromkeys(claims)))
        if knowledge_use or claims else None
    )

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
        "knowledge_recording": recording,
        **({"knowledge_use": use} if use is not None else {}),
    }


def _recording_lines(recording: dict[str, Any]) -> list[str]:
    target = recording["target_repository"] or "no receipts"
    last = recording["last_query_receipt_updated_at"]
    lines = [f"KNOWLEDGE QUERY RECORDING ({target}): {recording['query_receipt_total']} query receipts; "
             f"last updated {last or 'never'}"]
    commits = recording["knowledge_commits_since_last_query_receipt"]
    if last is not None:
        lines.append(f"  commits changing {_KNOWLEDGE_DIR}/ since then: "
                     f"{'unknown (Git could not answer)' if commits is None else commits}")
    missing = recording["steward_sessions_without_query_receipt"]
    lines.append(f"  sessions naming {_STEWARD} without a query receipt: "
                 f"{len(missing)} of {recording['steward_session_total']}")
    if recording["other_target_query_receipts"]:
        lines.append("  query receipts for another target repository (not counted): "
                     f"{len(recording['other_target_query_receipts'])}")
    lines.append("  Recorded retrieval per record: --knowledge-use (descriptive; not evidence of use).")
    return lines


def _counts(mapping: dict[str, int]) -> str:
    return ", ".join(f"{key} {value}" for key, value in mapping.items()) or "none"


def _routes(mapping: dict[str, int]) -> str:
    return "; ".join(f"{_ROUTE_LABELS[route]} {mapping[route]}" for route in _ROUTES)


def _use_lines(use: dict[str, Any]) -> list[str]:
    lines = ["RECORDED KNOWLEDGE RETRIEVAL (query receipts joined to authored packs; recorded use only)"]
    if not use["available"]:
        return [*lines, f"  not available: {use['reason']}"]
    found = use["with_recorded_retrieval"]
    lines.append(f"  records in packs: {use['records_total']}; with a recorded retrieval: "
                 f"{found['total']} ({_routes(found['by_route'])})")
    later = use["returned_after_first_commit_day"]
    lines.append("  returned on a later day than first committed: "
                 + ("unknown (Git could not answer)" if later is None
                    else f"{later['total']} ({_routes(later['by_route'])})")
                 + ". A later day is not a different agent")
    missing = use["no_recorded_retrieval"]
    late = missing["added_after_last_query_receipt"]
    lines.append(f"  NO RECORDED RETRIEVAL: {missing['total']}"
                 + ("" if late is None else f" ({late} added after the last query receipt, marked *)")
                 + "; this is not non-use")
    by_kind: dict[str, list[str]] = defaultdict(list)
    for item in missing["records"]:
        by_kind[item["kind"]].append(item["id"] + ("*" if item["added_after_last_query_receipt"] else ""))
    for kind in sorted(by_kind):
        ids = by_kind[kind]
        more = f" (+{len(ids) - 6} more in --json)" if len(ids) > 6 else ""
        lines.append(f"    {kind} ({len(ids)}): {', '.join(ids[:6])}{more}")
    absent = use["returned_ids_not_in_current_packs"]
    lines.append(f"  returned IDs not in the current packs (index-generated or removed): {len(absent)}")
    checks = use["source_checks"]
    lines.append(f"  SOURCE CHECKS: {checks['total']} over {checks['record_total']} records "
                 f"({_counts(checks['by_result'])}); a SUPPORTED share is not an accuracy rate")
    unresolved = checks["contradicted_or_stale_without_later_applied_revision"]
    lines.append(f"    CONTRADICTED or STALE with no later applied REVISE, SUPERSEDE or CONTEST: {len(unresolved)}")
    lines.extend(f"      {item['claim_id']} {item['result']} in {item['session_ref']}" for item in unresolved)
    reconcile = use["reconcile"]
    lines.append(f"  RECONCILE: {_counts(reconcile['by_disposition'])}; proposed changes not applied: "
                 f"{reconcile['proposed_not_applied']}")
    outcomes = use["query_outcomes"].get("context-for")
    if outcomes:
        lines.append(f"  context-for outcomes: {_counts(outcomes)}. {use['query_outcome_note']}")
    for cid, record in use["records"].items():
        state = "" if record["in_current_packs"] else " (not in the current packs)"
        lines.append(f"  RECORD {cid} [{record['kind']}]{state} first committed "
                     f"{record['first_committed'] or 'unknown'}")
        lines.extend(f"    returned {event['day']} by {event['operation']} in {event['session_ref']}"
                     for event in record["returned"])
        lines.extend(f"    source check {event['day']} {event['result']} in {event['session_ref']}"
                     for event in record["source_checks"])
        lines.extend(f"    reconcile {event['day']} {event['disposition']}"
                     f"{'' if event['applied'] else ' (not applied)'} in {event['session_ref']}"
                     for event in record["reconcile"])
        if not (record["returned"] or record["source_checks"] or record["reconcile"]):
            lines.append("    no recorded retrieval, source check or reconcile entry")
    lines.extend(f"  Limit: {limit}" for limit in use["limits"])
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
    if "knowledge_use" in summary:
        lines.extend(_use_lines(summary["knowledge_use"]))
    if summary["invalid"]:
        lines.append("INVALID RECEIPTS (run scripts/validate-receipt.py for detail):")
        lines.extend(f"  {i['file']}: {'; '.join(i['errors'])}" for i in summary["invalid"])
    print(_ascii("\n".join(lines)))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Summarize Sensemaking receipts for session start")
    parser.add_argument("--repo", default=".", help="Target repository root (default: current directory)")
    parser.add_argument("--dir", default=None, help=f"Receipt directory (default: <repo>/{_validator.RECEIPT_DIR})")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--knowledge-use", action="store_true",
                        help="Also report recorded retrieval per knowledge record (descriptive only)")
    parser.add_argument("--claim", action="append", default=[], metavar="CLAIM_ID",
                        help="Show the recorded history of one knowledge record; repeatable; "
                             "implies --knowledge-use")
    parser.add_argument("--target-repository", default=None,
                        help="Repository identity the receipts describe (default: the commonest "
                             "target_repository among the session receipts)")
    args = parser.parse_args(argv)

    receipt_dir = Path(args.dir) if args.dir else Path(args.repo) / _validator.RECEIPT_DIR
    summary = summarize(receipt_dir, Path(args.repo), knowledge_use=args.knowledge_use,
                        claims=tuple(args.claim), target_repository=args.target_repository)
    if args.json:
        print(_ascii(json.dumps(summary, indent=2)))
    else:
        _print_text(summary)
    return 1 if summary["invalid"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
