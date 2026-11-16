"""B6 parity: the sm server's knowledge results must equal a direct orchestrator build at the same path.

Usage: python b6_parity.py <scratch> <cal01_transcript.jsonl> <out.json>
Digests depend on the repository path, so the direct build uses the sandbox repo at <scratch>/sandbox/repo.
Compares: the build digest and claim count, and the claim-id sets of a search and an explain query.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

scratch, transcript, out_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
REPO = scratch / "sandbox" / "repo"
DIRECT = scratch / "direct"
DIRECT.mkdir(parents=True, exist_ok=True)
SRC = Path(__file__).resolve().parents[3] / "src"  # the worktree's src at the pinned commit's code
PIN = "b7ce9e699d63d637c9798da6b15db325a02f7ce8"
BOOT = ("import sys; sys.path.insert(0, sys.argv[1]); "
        "sys.argv = ['sensemaking-skills'] + sys.argv[2:]; from sensemaking_skills.cli import main; main()")


def cli(*args):
    proc = subprocess.run([sys.executable, "-c", BOOT, str(SRC), "semantic", *args],
                          capture_output=True, text=True, timeout=300, cwd=str(DIRECT))
    return json.loads(proc.stdout) if proc.returncode == 0 else {"error": proc.stderr[-300:]}


def claim_ids(obj):
    return sorted({c.get("claim_id") or c.get("id") for c in obj.get("claims", []) if c.get("claim_id") or c.get("id")})


db = DIRECT / "direct.db"
if db.exists():
    db.unlink()
build = cli("knowledge-build", "--repo", str(REPO), "--repository", "sensemaking-skills",
            "--target-ref", PIN, "--db", str(db), "--json")
search = cli("knowledge-query", "--db", str(db), "--repository", "sensemaking-skills", "--target-ref", PIN,
             "--operation", "search", "--repo", str(REPO), "--limit", "10", "--term=lesson", "--json")
explain = cli("knowledge-query", "--db", str(db), "--repository", "sensemaking-skills", "--target-ref", PIN,
              "--operation", "explain", "--repo", str(REPO), "--limit", "50",
              "--subject=lesson:pr-review-merge-base-is-scope-evidence", "--json")

# Server results from the transcript (full text, not the truncated summary head).
server_texts = []
for line in transcript.read_text(encoding="utf-8").splitlines():
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        continue
    message = event.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), list):
        continue
    for item in message["content"]:
        if isinstance(item, dict) and item.get("type") == "tool_result":
            text = item.get("content")
            if isinstance(text, list):
                text = " ".join(part.get("text", "") for part in text if isinstance(part, dict))
            server_texts.append(str(text))


def server_inner(text):
    try:
        outer = json.loads(text)
        return json.loads(outer["stdout"]) if isinstance(outer, dict) and "stdout" in outer else None
    except (json.JSONDecodeError, TypeError, KeyError):
        return None


server_build = server_search = server_explain = None
for text in server_texts:
    inner = server_inner(text)
    if inner is None:
        continue
    if "digest" in inner and "claim_count" in inner and server_build is None:
        server_build = inner
    elif inner.get("claims") and inner.get("operation_authorized") is None and server_search is None and "lesson" in text[:4000] and "explain" not in text[:200]:
        server_search = inner
    elif inner.get("claims") and "pr-review-merge-base-is-scope-evidence" in text and server_explain is None and len(inner["claims"]) <= 5:
        server_explain = inner

result = {
    "pinned": PIN,
    "repo_path": str(REPO),
    "direct_build_digest": build.get("digest"),
    "server_build_digest": (server_build or {}).get("digest"),
    "digest_identical": build.get("digest") is not None and build.get("digest") == (server_build or {}).get("digest"),
    "direct_claim_count": build.get("claim_count"),
    "server_claim_count": (server_build or {}).get("claim_count"),
    "search_claim_ids_identical": claim_ids(search) == claim_ids(server_search or {}) and bool(claim_ids(search)),
    "explain_claim_ids_identical": claim_ids(explain) == claim_ids(server_explain or {}) and bool(claim_ids(explain)),
    "direct_search_ids": claim_ids(search),
    "direct_explain_ids": claim_ids(explain),
    "direct_errors": {k: v for k, v in {"build": build.get("error"), "search": search.get("error"),
                                         "explain": explain.get("error")}.items() if v},
}
result["b6_pass"] = (result["digest_identical"] and result["search_claim_ids_identical"]
                     and result["explain_claim_ids_identical"] and not result["direct_errors"])
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("digest_identical", "search_claim_ids_identical",
                                          "explain_claim_ids_identical", "b6_pass")}, indent=2))
