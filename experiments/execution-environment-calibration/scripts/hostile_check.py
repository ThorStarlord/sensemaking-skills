"""Server-level escape check for B5, with a negative control. No subject episode.

Usage: python hostile_check.py <scratch> <server_dir> <result_json>

1. Build a hostile repository in <scratch>/hostile/repo whose local config would run commands
   through core.fsmonitor, a diff driver's textconv, and a diff driver's external command.
2. Negative control: run raw git (no neutralisation). At least one marker must appear, or the
   instrument cannot detect the escape and B5 is INSTRUMENT_INVALID.
3. Positive test: run the same repository through the server's neutralised tools. No marker may appear.
"""
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

scratch, server_dir, result_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
H = scratch / "hostile"


def _clear_readonly(func, path, _exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)


if H.exists():
    shutil.rmtree(H, onexc=_clear_readonly)  # git object files are read-only on Windows
repo, markers = H / "repo", H / "markers"
repo.mkdir(parents=True)
markers.mkdir(parents=True)
(H / "home").mkdir()
(H / "run").mkdir()
(H / "log").mkdir()
ID = ["-c", "user.name=calibration", "-c", "user.email=calibration@invalid"]


def git(*args, env=None):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, env=env)


def marker_cmd(name: str) -> str:
    # Git's config parser strips unescaped double quotes from values, so they are written as \" .
    target = (markers / name).as_posix()
    return f"python -c \\\"open('{target}','w').write('x')\\\""


git("init", "-q")
(repo / "a.txt").write_text("one\n", encoding="utf-8")
(repo / ".gitattributes").write_text("*.txt diff=evil\n", encoding="utf-8")
git(*ID, "add", "-A")
git(*ID, "commit", "-q", "-m", "first")
(repo / "a.txt").write_text("two\n", encoding="utf-8")
git(*ID, "commit", "-q", "-am", "second")
with (repo / ".git" / "config").open("a", encoding="utf-8") as fh:
    fh.write(f'[core]\n\tfsmonitor = {marker_cmd("fsmonitor")}\n')
    fh.write(f'[diff "evil"]\n\ttextconv = {marker_cmd("textconv")}\n\tcommand = {marker_cmd("extdiff")}\n')

present = lambda: sorted(p.name for p in markers.iterdir())  # noqa: E731
result = {"negative_control": {}, "positive_test": {}}

# 2. Negative control: raw git, no neutralisation.
raw_env = {k: os.environ[k] for k in ("PATH", "SYSTEMROOT", "TEMP", "TMP") if k in os.environ}
for argv in (["log", "-p", "-1"], ["status", "--porcelain"], ["diff", "HEAD~1", "HEAD"]):
    git(*argv, env=raw_env)
result["negative_control"]["markers_after_raw_git"] = present()
for p in markers.iterdir():
    p.unlink()

# 3. Positive test: the server's neutralised tools on the same repository.
os.environ["SM_SANDBOX"] = str(H)
sys.path.insert(0, str(server_dir))
import sm_server  # noqa: E402

calls = {
    "git_log": sm_server.git_log(rev="HEAD", max_count=5),
    "git_show_file": sm_server.git_show_file(rev="HEAD", path="a.txt"),
    "git_diff_names": sm_server.git_diff_names(base="HEAD~1", head="HEAD"),
    "git_merge_base": sm_server.git_merge_base(rev_a="HEAD", rev_b="HEAD~1"),
    "git_ls_tree": sm_server.git_ls_tree(),
    "refused_traversal": sm_server.git_show_file(rev="HEAD", path="../escape"),
    "refused_option_injection": sm_server.git_log(rev="--output=x", max_count=1),
    "refused_colon_path": sm_server.git_show_file(rev="HEAD", path="a.txt:b"),
}
result["positive_test"]["markers_after_server_calls"] = present()
result["positive_test"]["calls"] = {
    k: ({"refused": v["reason"]} if v.get("refused") else {"exit_code": v["exit_code"],
                                                          "stdout_head": v["stdout"][:120]})
    for k, v in calls.items()}
result["negative_control_valid"] = len(result["negative_control"]["markers_after_raw_git"]) > 0
result["b5_pass"] = result["negative_control_valid"] and not result["positive_test"]["markers_after_server_calls"]
result_path.parent.mkdir(parents=True, exist_ok=True)
result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"negative_control_valid": result["negative_control_valid"],
                  "raw_markers": result["negative_control"]["markers_after_raw_git"],
                  "server_markers": result["positive_test"]["markers_after_server_calls"],
                  "b5_pass": result["b5_pass"]}, indent=2))
