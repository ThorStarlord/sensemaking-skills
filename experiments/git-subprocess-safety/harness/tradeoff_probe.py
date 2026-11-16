"""Transforming-filter probe (scratch only): raw Git, the rejected option, and the path the callers now use.

Usage: GITSAFETY_SCRATCH=<scratch> python tradeoff_probe.py
Writes results/tradeoff_probe.json. The filter is configured BEFORE the commit, so the stored blob is the filtered form.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = Path(os.environ["GITSAFETY_SCRATCH"])
SRC = str(HERE.parents[2] / "src")
ID = ["-c", "user.name=t", "-c", "user.email=t@invalid"]
d = S / "tradeoff"
if d.exists():
    shutil.rmtree(d, onexc=lambda f, p, e: (os.chmod(p, 0o700), f(p)))
d.mkdir(parents=True)


def git(*args):
    return subprocess.run(["git", "-C", str(d), *args], capture_output=True, text=True, check=True)


git("init", "-q")
git("config", "core.autocrlf", "false")
git("config", "filter.upper.clean",
    "python -c \"__import__('sys').stdout.buffer.write(__import__('sys').stdin.buffer.read().upper())\"")
git("config", "filter.upper.smudge",
    "python -c \"__import__('sys').stdout.buffer.write(__import__('sys').stdin.buffer.read().lower())\"")
(d / ".gitattributes").write_bytes(b"big.txt filter=upper\n")
(d / "big.txt").write_bytes(b"hello\n")
git(*ID, "add", "-A")
git(*ID, "commit", "-qm", "x")
os.utime(d / "big.txt", (4102444800, 4102444800))  # force a re-hash of the worktree bytes
stored = git("show", "HEAD:big.txt").stdout
raw = git("status", "--porcelain").stdout


def guarded(disable_filters):
    code = (f"import sys; sys.path.insert(0, r'{SRC}'); from pathlib import Path; "
            f"from sensemaking_skills.semantic_architecture.worktree_context import guarded_git_text as g; "
            f"print(repr(g(Path(r'{d}'), 'status', '--porcelain', disable_filters={disable_filters})))")
    return subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=300).stdout.strip()


rejected = guarded(True)   # disable_filters=True: the option that would change output (rejected)
callers = guarded(False)   # disable_filters=False: what impact, proposal check and release audit now use
result = {
    "stored_blob_is_filtered_form": stored == "HELLO\n",
    "raw_status": raw,
    "guarded_status_filters_disabled_rejected_option": rejected,
    "guarded_status_filters_enabled_callers_now_use": callers,
    "callers_output_equals_raw": callers == repr(raw),
}
(HERE.parent / "results" / "tradeoff_probe.json").write_text(json.dumps(result, indent=2) + "\n",
                                                             encoding="utf-8", newline="\n")
print(json.dumps(result, indent=1))
