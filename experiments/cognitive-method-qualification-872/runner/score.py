#!/usr/bin/env python3
"""Mechanical helpers for #872 episodes: summarize subject transcripts, relabel responses blind, collect evaluator scores,
and join scores to arms only after scoring. No judgment is made here; the subject and evaluator sessions make all judgments.

Subcommands:
  summarize                      write results/summaries/<episode>.json for every subject transcript
  blind --task T --scratch DIR   relabel the final response of each subject transcript R1..Rn in a seeded random order
                                 (key kept in SCRATCH, outside the repository)
  collect --task T --tag TAG --scratch DIR
                                 parse evaluator JSON per blind label; write results/<TAG>-<T>-blind-scores.json
  unblind --task T --tag TAG --scratch DIR
                                 join blind scores to arm and episode using the key; write results/<TAG>-<T>-scores.json
"""
import argparse
import hashlib
import json
import random
import re
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
TRANSCRIPTS = EXP / "transcripts"
RESULTS = EXP / "results"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def events_of(path):
    out = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def final_text(path):
    result = next((e for e in events_of(path) if e.get("type") == "result"), None)
    if result is None:
        return None
    return result.get("result") or ""


def summarize_one(path):
    events = events_of(path)
    init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), None) or {}
    result = next((e for e in events if e.get("type") == "result"), None) or {}
    trace = []
    for e in events:
        if e.get("type") == "assistant":
            for b in e.get("message", {}).get("content") or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use":
                    inp = json.dumps(b.get("input", {}), ensure_ascii=False)
                    trace.append({"step": "tool_use", "name": b.get("name"), "input": inp[:300]})
                elif b.get("type") == "text" and b.get("text", "").strip():
                    trace.append({"step": "assistant_text", "chars": len(b["text"])})
        elif e.get("type") == "user":
            for b in e.get("message", {}).get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    trace.append({"step": "tool_result", "is_error": bool(b.get("is_error"))})
    return {
        "episode": path.stem,
        "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "session_id": init.get("session_id") or result.get("session_id"),
        "model": init.get("model"),
        "claude_code_version": init.get("claude_code_version"),
        "tools": init.get("tools"),
        "skills_count": len(init.get("skills") or []),
        "plugins": [p.get("name") if isinstance(p, dict) else p for p in (init.get("plugins") or [])],
        "mcp_servers_count": len(init.get("mcp_servers") or []),
        "memory_paths": init.get("memory_paths"),
        "result_subtype": result.get("subtype"),
        "is_error": result.get("is_error"),
        "num_turns": result.get("num_turns"),
        "cost_usd": result.get("total_cost_usd"),
        "trace_in_order": trace,
        "final_text": result.get("result"),
    }


def cmd_summarize(_args):
    out = RESULTS / "summaries"
    for p in sorted(TRANSCRIPTS.glob("D*-*.jsonl")):
        s = summarize_one(p)
        write(out / f"{p.stem}.json", json.dumps(s, indent=2, ensure_ascii=False) + "\n")
        print("summarized", p.name, "turns", s["num_turns"], "tool_uses", sum(1 for t in s["trace_in_order"] if t["step"] == "tool_use"))


def cmd_blind(args):
    streams = sorted(TRANSCRIPTS.glob(f"{args.task}-*.jsonl"))
    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(1, 10**9)
    order = list(range(len(streams)))
    random.Random(seed).shuffle(order)
    bdir = Path(args.scratch) / "blind" / f"{args.tag}-{args.task}"
    key = {}
    for n, idx in enumerate(order, start=1):
        src = streams[idx]
        label = f"R{n}"
        text = final_text(src)
        write(bdir / f"{label}.txt", text if text is not None else "NO_RESULT_EVENT")
        key[label] = src.name
    write(bdir / "key.json", json.dumps({"seed": seed, "key": key}, indent=2) + "\n")
    print("blinded", len(key), "responses into", bdir, "seed", seed)


def parse_scores(text):
    if text is None:
        return {"parse_error": "no result event"}
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        return {"parse_error": "no JSON object", "raw": text[:300]}
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError as exc:
        return {"parse_error": str(exc), "raw": text[:300]}


def cmd_collect(args):
    bdir = Path(args.scratch) / "blind" / f"{args.tag}-{args.task}"
    scores = {}
    for label_file in sorted((p for p in bdir.glob("R*.txt") if p.stem[1:].isdigit()), key=lambda p: int(p.stem[1:])):
        label = label_file.stem
        eval_stream = TRANSCRIPTS / f"eval-{args.tag}-{args.task}-{label}.jsonl"
        scores[label] = parse_scores(final_text(eval_stream))
    write(RESULTS / f"{args.tag}-{args.task}-blind-scores.json", json.dumps(scores, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(scores, indent=2, ensure_ascii=False))


def cmd_unblind(args):
    bdir = Path(args.scratch) / "blind" / f"{args.tag}-{args.task}"
    key = json.loads((bdir / "key.json").read_text(encoding="utf-8"))["key"]
    scores = json.loads((RESULTS / f"{args.tag}-{args.task}-blind-scores.json").read_text(encoding="utf-8"))
    joined = []
    for label, episode_file in sorted(key.items(), key=lambda kv: int(kv[0][1:])):
        arm = "treatment" if "-treatment-" in episode_file else "baseline"
        row = {"label": label, "episode": Path(episode_file).stem, "arm": arm}
        s = scores.get(label, {})
        row.update({k: (v.get("score") if isinstance(v, dict) else v) for k, v in s.items()})
        joined.append(row)
    write(RESULTS / f"{args.tag}-{args.task}-scores.json", json.dumps(joined, indent=2, ensure_ascii=False) + "\n")
    for row in joined:
        print(row)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("summarize").set_defaults(fn=cmd_summarize)
    for name, fn in [("blind", cmd_blind), ("collect", cmd_collect), ("unblind", cmd_unblind)]:
        sp = sub.add_parser(name)
        sp.add_argument("--task", required=True)
        sp.add_argument("--tag", required=True)
        sp.add_argument("--scratch", required=True)
        if name == "blind":
            sp.add_argument("--seed", type=int, default=None)
        sp.set_defaults(fn=fn)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
