"""Negative control: which RAW git operations trigger each canary (no Sensemaking code involved)."""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

import os
HERE = Path(os.environ["GITSAFETY_SCRATCH"])  # fixtures go here, never inside the repository
MAKE = Path(__file__).resolve().parent / "make_repo.py"
D, M = HERE / "d-neg", HERE / "m-neg"
OPS = {
    "status_porcelain": ["status", "--porcelain=v1"],
    "ls_files_cached": ["ls-files", "-z"],
    "ls_files_others": ["ls-files", "--others", "--exclude-standard", "-z"],
    "diff_name_only_worktree": ["diff", "--name-only", "-z", "HEAD", "--"],
    "diff_patch_commits": ["diff", "-p", "HEAD~1", "HEAD"],
    "log_patch": ["log", "-p", "-1"],
    "show_blob": ["show", "HEAD:notes.txt"],
    "cat_file_blob": ["cat-file", "-p", "HEAD:notes.txt"],
    "check_attr": ["check-attr", "-z", "--stdin", "filter"],
    "rev_parse": ["rev-parse", "HEAD"],
    "worktree_add": None,
}
results = {}
for name, args in OPS.items():
    subprocess.run([sys.executable, str(MAKE), str(D), str(M)], check=True, capture_output=True)
    if args is None:
        dest = Path(tempfile.mkdtemp(prefix="wt-neg-")) / "checkout"
        cmd = ["git", "-C", str(D), "worktree", "add", "--quiet", "--detach", str(dest), "HEAD"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        subprocess.run(["git", "-C", str(D), "worktree", "remove", "--force", str(dest)], capture_output=True)
        shutil.rmtree(dest.parent, ignore_errors=True)
    else:
        proc = subprocess.run(["git", "-C", str(D), *args], capture_output=True, text=True)
    fired = sorted(p.name for p in M.iterdir()) if M.exists() else []
    results[name] = {"exit": proc.returncode, "canaries_fired": fired}
    for p in list(M.iterdir()):
        p.unlink()
(HERE / "neg_control.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
for k, v in results.items():
    print(f"{k:26s} exit={v['exit']:<4} fired={v['canaries_fired']}")
