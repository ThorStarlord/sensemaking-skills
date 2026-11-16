"""Disposable synthetic Git repository with harmless canaries (scratch material only).

Usage: python make_repo.py <repo_dir> <marker_dir> [filter|nofilter]

Canaries append 'x' to one marker file in <marker_dir>. Clean and smudge filters pass bytes through
unchanged (binary stdio, so Windows text-mode newlines cannot alter results). Canary commands contain
no ';' because git config treats ';' as a comment start. Canaries are configured only after the setup
commits. 'nofilter' attaches no filter attribute, so a temporary build can succeed. Nothing outside
<marker_dir> is written.
"""
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

repo, markers = Path(sys.argv[1]), Path(sys.argv[2])
mode = sys.argv[3] if len(sys.argv) > 3 else "filter"


def _clear(func, path, _exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)


for d in (repo, markers):
    if d.exists():
        shutil.rmtree(d, onexc=_clear)
repo.mkdir(parents=True)
markers.mkdir(parents=True)
ID = ["-c", "user.name=canary", "-c", "user.email=canary@invalid", "-c", "commit.gpgsign=false"]


def git(*args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True)


git("init", "-q")
(repo / "notes.txt").write_text("alpha\n", encoding="utf-8")
(repo / "plain.md").write_text("plain\n", encoding="utf-8")
attrs = "notes.txt diff=canary\n" if mode == "nofilter" else "notes.txt filter=canary diff=canary\n"
(repo / ".gitattributes").write_text(attrs, encoding="utf-8")
git(*ID, "add", "-A")
git(*ID, "commit", "-q", "-m", "first")
(repo / "notes.txt").write_text("beta\n", encoding="utf-8")
git(*ID, "commit", "-q", "-am", "second")


def marker(name: str) -> str:
    return (markers / name).as_posix()


def canary(name: str, passthrough: bool) -> str:
    mark = f"open('{marker(name)}','a').write('x')"
    if passthrough:
        body = (f"({mark}, __import__('sys').stdout.buffer.write(__import__('sys').stdin.buffer.read()))")
    else:
        body = mark
    return f'python -c \\"{body}\\"'


with (repo / ".git" / "config").open("a", encoding="utf-8") as fh:
    fh.write("[core]\n\tfsmonitor = " + canary("fsmonitor", passthrough=False) + "\n")
    fh.write('[filter "canary"]\n')
    fh.write("\tclean = " + canary("clean", passthrough=True) + "\n")
    fh.write("\tsmudge = " + canary("smudge", passthrough=True) + "\n")
    fh.write('[diff "canary"]\n')
    fh.write("\ttextconv = " + canary("textconv", passthrough=False) + "\n")
    fh.write("\tcommand = " + canary("extdiff", passthrough=False) + "\n")

hook = repo / ".git" / "hooks" / "post-checkout"
hook.parent.mkdir(exist_ok=True)
hook.write_text('#!/bin/sh\necho x >> "' + marker("post-checkout") + '"\n', encoding="utf-8")

# Stat-dirty with identical content: any command that re-hashes notes.txt runs the clean filter.
os.utime(repo / "notes.txt", None)
print(f"repo={repo} markers={markers} mode={mode} head={git('rev-parse', 'HEAD').stdout.strip()}")
