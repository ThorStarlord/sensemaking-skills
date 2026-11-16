"""Caller-visible text and output of the three non-knowledge callers, origin/main against the final source (scratch only).

Usage: GITSAFETY_SCRATCH=<scratch> GITSAFETY_OLD_SRC=<exported origin/main src> python error_text_check.py
Writes results/error_text_check.json. A failing `required` filter is committed BEFORE the filter exists,
because git add would fail otherwise.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = Path(os.environ["GITSAFETY_SCRATCH"])
OLD = os.environ["GITSAFETY_OLD_SRC"]
NEW = str(HERE.parents[2] / "src")
ID = ["-c", "user.name=t", "-c", "user.email=t@invalid"]


def fresh(name):
    d = S / name
    if d.exists():
        shutil.rmtree(d, onexc=lambda f, p, e: (os.chmod(p, 0o700), f(p)))
    d.mkdir(parents=True)
    g = lambda *a: subprocess.run(["git", "-C", str(d), *a], capture_output=True, text=True, check=True)  # noqa: E731
    g("init", "-q")
    g("config", "core.autocrlf", "false")
    return d, g


def mk_required(name):
    d, g = fresh(name)
    (d / "notes.txt").write_bytes(b"alpha\n")
    g(*ID, "add", "-A")
    g(*ID, "commit", "-qm", "x")
    g("config", "filter.req.clean", 'python -c "raise SystemExit(1)"')
    g("config", "filter.req.required", "true")
    (d / ".gitattributes").write_bytes(b"notes.txt filter=req\n")
    os.utime(d / "notes.txt", (4102444800, 4102444800))
    return d


def mk_filtered(name):
    d, g = fresh(name)
    g("config", "filter.upper.clean",
      "python -c \"__import__('sys').stdout.buffer.write(__import__('sys').stdin.buffer.read().upper())\"")
    g("config", "filter.upper.smudge",
      "python -c \"__import__('sys').stdout.buffer.write(__import__('sys').stdin.buffer.read().lower())\"")
    (d / ".gitattributes").write_bytes(b"notes.txt filter=upper\n")
    (d / "notes.txt").write_bytes(b"hello\n")
    g(*ID, "add", "-A")
    g(*ID, "commit", "-qm", "x")
    os.utime(d / "notes.txt", (4102444800, 4102444800))
    return d


def probe(src, d):
    code = (f"import sys,json; sys.path.insert(0, r'{src}'); from pathlib import Path\n"
            "from sensemaking_skills.semantic_architecture import impact as I, stewardship_validation as SV\n"
            "from sensemaking_skills import release_authority as R\n"
            f"d=Path(r'{d}'); out={{}}\n"
            "def t(name, f):\n"
            "    try: out[name]={'ok': f()}\n"
            "    except Exception as e: out[name]={'exc': type(e).__name__, 'msg': str(e)}\n"
            "t('impact', lambda: I._git(d,'status','--porcelain'))\n"
            "t('stewardship', lambda: SV._git(d,'status','--porcelain'))\n"
            "t('release', lambda: R._git(d,'status','--porcelain'))\n"
            "print(json.dumps(out))")
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=300)
    return json.loads(p.stdout.strip().splitlines()[-1]) if p.stdout.strip() else {"stderr": p.stderr[-400:]}


req, ok = mk_required("err-req"), mk_filtered("err-ok")
res = {"required_failing": {"origin_main": probe(OLD, req), "final": probe(NEW, req)},
       "filtered_success": {"origin_main": probe(OLD, ok), "final": probe(NEW, ok)}}
res["identical"] = {k: res[k]["origin_main"] == res[k]["final"] for k in ("required_failing", "filtered_success")}
(HERE.parent / "results" / "error_text_check.json").write_text(json.dumps(res, indent=2) + "\n",
                                                              encoding="utf-8", newline="\n")
print(json.dumps(res["identical"]))
