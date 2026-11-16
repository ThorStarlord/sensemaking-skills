"""Objective checks for episode 552-B (PREREG-EPISODE-552.md section 3, measures 1 to 4 and verdict).

Usage: python episode_check.py <scratch> <transcript.jsonl> <server_log.jsonl> <run_summary.json> <out.json>
Runs before the orchestrator reads the final report's content for judgement.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

scratch, transcript, server_log, summary_path, out_path = (Path(a) for a in sys.argv[1:6])
PIN = "b7ce9e699d63d637c9798da6b15db325a02f7ce8"
REPO = scratch / "sandbox" / "repo"
KNOW = {"knowledge_build", "knowledge_query", "knowledge_audit"}
SRC_READ = {"git_show_file", "Read"}

events = []
for line in transcript.read_text(encoding="utf-8").splitlines():
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        continue
    if isinstance(event, dict):
        events.append(event)

calls = []  # (index, name, input)
texts = []  # (index, text)
for idx, event in enumerate(events):
    message = event.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), list):
        continue
    for item in message["content"]:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "tool_use":
            name = str(item.get("name", "")).split("__")[-1]
            calls.append((idx, name, item.get("input")))
        elif item.get("type") == "text" and event.get("type") == "assistant":
            texts.append((idx, item.get("text", "")))

final_idx, final_text = (texts[-1] if texts else (len(events), ""))
before_final = [c for c in calls if c[0] < final_idx]
knowledge_before = [c for c in before_final if c[1] in KNOW]
source_before = [c for c in before_final if c[1] in SRC_READ]

claim_ids = sorted(set(re.findall(r"\b(?:lesson|incident|decision|observation|component|owner|claim|risk|adr):[A-Za-z0-9_.\-]+", final_text)))
commits = sorted(set(re.findall(r"\b[0-9a-f]{40}\b", final_text)))
paths = sorted(set(p.rstrip(".,;:)") for p in re.findall(r"[A-Za-z0-9_./\-]+\.(?:md|py|json|yml|yaml|sh|txt|toml|cfg)\b", final_text)))

stew = subprocess.run(["git", "-C", str(REPO), "show", f"{PIN}:.sensemaking/knowledge/stewardship.json"],
                      capture_output=True, text=True)
known_claims = set()
if stew.returncode == 0:
    data = json.loads(stew.stdout)
    items = data if isinstance(data, list) else data.get("claims", [])
    known_claims = {c.get("id") for c in items if isinstance(c, dict) and c.get("id")}


def git_ok(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True).returncode == 0


claim_check = {c: (c in known_claims) for c in claim_ids}
commit_check = {c: git_ok("cat-file", "-e", f"{c}^{{commit}}") for c in commits}
path_check = {p: git_ok("cat-file", "-e", f"{PIN}:{p}") for p in paths}
verdict_match = re.findall(r"\b(CHANGE_RECOMMENDED|NO_CHANGE)\b", final_text)

summary = json.loads(summary_path.read_text(encoding="utf-8"))
run_ok = summary.get("result", {}).get("subtype") == "success" and not summary.get("result", {}).get("is_error")

result = {
    "run_completed_within_limits": run_ok,
    "measure1_knowledge_calls_before_final": len(knowledge_before),
    "measure1_knowledge_call_names": [c[1] for c in knowledge_before],
    "measure2_source_reads_before_final": len(source_before),
    "measure3_claim_ids_cited": claim_check,
    "measure3_all_claims_exist": bool(claim_check) and all(claim_check.values()),
    "measure4_commits_cited": commit_check,
    "measure4_paths_cited": path_check,
    "measure4_all_citations_exist": all(commit_check.values()) and all(path_check.values()),
    "verdict_tokens_in_final": sorted(set(verdict_match)),
    "tool_calls_total": len(calls),
    "result": summary.get("result"),
}
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in (
    "run_completed_within_limits", "measure1_knowledge_calls_before_final",
    "measure2_source_reads_before_final", "measure3_all_claims_exist",
    "measure4_all_citations_exist", "verdict_tokens_in_final", "tool_calls_total")}, indent=2))
