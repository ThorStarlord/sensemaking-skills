"""Narrow read-only Git and Sensemaking interface (execution-calibration scope, mechanism A).

No shell is exposed to the subject. Each tool builds a fixed argv from validated arguments
and runs it against one pinned repository. The server's own git calls run with a neutralised Git environment. The Sensemaking CLI's internal git calls do not (PREREG.md section 8). Every call,
including refusals and errors, is appended to a server-side log outside the subject's file scope.

Trust model (PREREG-AMENDMENT-5): the boundary is the tool surface and argument validation.
It is NOT operating-system isolation. The server runs git and the Sensemaking CLI with the
operator's OS privileges, and the CLI imports Python code from the pinned repository's src/.
The pinned repository is the object of study and is treated as trusted content. Objects beyond
the pin are absent from the sandbox, because it is built from the pinned ancestry only.

Configuration: environment variable SM_SANDBOX names a sandbox directory containing
  repo/   pinned clean clone (the only repository this server can see)
  index/  SQLite semantic indices written by knowledge_build (sandbox-only)
  run/    neutral working directory for the Sensemaking CLI (keeps the clone off sys.path)
  home/   empty home directory for Git and Python
  log/    mcp-calls.jsonl (server-side attribution log)
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from mcp.server.fastmcp import FastMCP

SANDBOX = Path(os.environ["SM_SANDBOX"]).resolve()
REPO = SANDBOX / "repo"
SRC = REPO / "src"
INDEX = SANDBOX / "index"
RUN = SANDBOX / "run"
HOME = SANDBOX / "home"
LOG = SANDBOX / "log" / "mcp-calls.jsonl"
REPOSITORY_ID = "sensemaking-skills"

GIT_CAP = 120_000
CLI_CAP = 200_000
REV_RE = re.compile(r"^(HEAD|[0-9a-f]{40})(~[0-9]{1,3}|\^[0-9]?)*$")
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
OPERATIONS = {"snapshot", "search", "explain", "impact", "why", "history", "rules-for",
              "term", "orientation-summary", "context-for"}
# Neutralised Git prefix: no fsmonitor, no hooks, no pager. Diff-like calls add
# --no-ext-diff/--no-textconv at the call site. Global and system config are cut off by _env().
GIT = ["git", "--no-pager", "-c", "core.fsmonitor=false", "-c", "core.hooksPath=" + os.devnull,
       "-c", "core.untrackedCache=false"]
BOOT = ("import sys; sys.path.insert(0, sys.argv[1]); "
        "sys.argv = ['sensemaking-skills'] + sys.argv[2:]; "
        "from sensemaking_skills.cli import main; main()")

mcp = FastMCP("sm")


def _env() -> dict[str, str]:
    # APPDATA and LOCALAPPDATA locate the user site-packages where the CLI dependencies (click) live.
    # They are path variables only; no secret values are passed.
    env = {k: os.environ[k] for k in ("PATH", "SYSTEMROOT", "TEMP", "TMP", "APPDATA", "LOCALAPPDATA")
           if k in os.environ}
    env.update({
        "HOME": str(HOME), "USERPROFILE": str(HOME),
        "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "GIT_ATTR_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0", "GIT_PAGER": "cat", "PAGER": "cat",
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    return env


def _rev(value: str) -> str:
    if not REV_RE.fullmatch(value or ""):  # fullmatch: '$' would accept a trailing newline
        raise ValueError("revision must be HEAD or a full 40-hex SHA, optionally with ~n or ^ suffixes")
    return value


def _rel(value: str) -> str:
    if value == "":
        return ""
    if (len(value) > 200 or "\x00" in value or re.search(r"[\r\n]", value)
            or value.startswith(("-", "/", "\\")) or ":" in value
            or ".." in Path(value.replace("\\", "/")).parts):
        raise ValueError("path must be repository-relative, with no '..', ':', or leading '-' or '/'")
    return value.replace("\\", "/")


def _text(value: str, limit: int = 200) -> str:
    if len(value) > limit or re.search(r"[\r\n\x00]", value):
        raise ValueError("argument too long or contains control characters")
    return value


def _log(name: str, args: dict, status, stdout: bytes, started: float) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts_start": dt.datetime.fromtimestamp(started, dt.timezone.utc).isoformat(),
        "ts_end": dt.datetime.now(dt.timezone.utc).isoformat(),
        "tool": name, "args": args, "status": status,
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(), "stdout_bytes": len(stdout),
    }
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def _run(name: str, args: dict, argv: list[str], cwd: Path, cap: int) -> dict:
    started = time.time()
    try:
        # stdin=DEVNULL: children must not inherit this server's stdin, which is the MCP protocol pipe.
        proc = subprocess.run(argv, cwd=cwd, env=_env(), capture_output=True, timeout=90,
                              stdin=subprocess.DEVNULL)
        rc, out, err = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = -9, b"", b"timeout after 90s"
    _log(name, args, rc, out, started)
    return {"exit_code": rc, "stdout": out[:cap].decode("utf-8", "replace"),
            "stderr": err[:4000].decode("utf-8", "replace"), "truncated": len(out) > cap}


def _call(name: str, args: dict, build) -> dict:
    try:
        argv, cwd, cap = build()
    except ValueError as exc:
        _log(name, args, "REFUSED", str(exc).encode(), time.time())
        return {"refused": True, "reason": str(exc)}
    except Exception as exc:  # any other failure is still logged, so the attribution log stays complete
        _log(name, args, f"ERROR:{type(exc).__name__}", str(exc).encode(), time.time())
        return {"error": f"{type(exc).__name__}: {exc}"}
    return _run(name, args, argv, cwd, cap)


def _head_sha() -> str:
    proc = subprocess.run(GIT + ["rev-parse", "--verify", "HEAD^{commit}"], cwd=REPO, env=_env(),
                          capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
    sha = proc.stdout.strip()
    if proc.returncode or not FULL_SHA_RE.fullmatch(sha):
        raise ValueError("cannot resolve HEAD of the pinned repository")
    return sha


def _cli(*args: str) -> list[str]:
    return [sys.executable, "-c", BOOT, str(SRC), "semantic", *args]


# ---- Git: read-only operations -------------------------------------------------------

@mcp.tool()
def git_log(rev: str = "HEAD", max_count: int = 20, path: str = "") -> dict:
    """Commit history for a revision, optionally limited to one repository-relative path."""
    def build():
        n = int(max_count)
        if not 1 <= n <= 100:
            raise ValueError("max_count must be between 1 and 100")
        argv = GIT + ["log", f"--max-count={n}", "--date=short", "--format=%H%x09%ad%x09%s",
                      _rev(rev), "--"]
        p = _rel(path)
        if p:
            argv.append(p)
        return argv, REPO, GIT_CAP
    return _call("git_log", {"rev": rev, "max_count": max_count, "path": path}, build)


@mcp.tool()
def git_merge_base(rev_a: str, rev_b: str) -> dict:
    """All merge bases of two revisions. More than one line means the merge base is not unique."""
    def build():
        return GIT + ["merge-base", "--all", _rev(rev_a), _rev(rev_b)], REPO, GIT_CAP
    return _call("git_merge_base", {"rev_a": rev_a, "rev_b": rev_b}, build)


@mcp.tool()
def git_diff_names(base: str, head: str, path: str = "") -> dict:
    """Changed paths between base and head in merge-base form (base...head). Names only."""
    def build():
        argv = GIT + ["diff", "--no-ext-diff", "--no-textconv", "--name-status",
                      f"{_rev(base)}...{_rev(head)}", "--"]
        p = _rel(path)
        if p:
            argv.append(p)
        return argv, REPO, GIT_CAP
    return _call("git_diff_names", {"base": base, "head": head, "path": path}, build)


@mcp.tool()
def git_show_file(rev: str, path: str) -> dict:
    """Raw contents of one file at a revision (blob bytes, no textconv)."""
    def build():
        p = _rel(path)
        if not p:
            raise ValueError("path is required")
        return GIT + ["cat-file", "-p", f"{_rev(rev)}:{p}"], REPO, GIT_CAP
    return _call("git_show_file", {"rev": rev, "path": path}, build)


@mcp.tool()
def git_ls_tree(rev: str = "HEAD", path: str = "") -> dict:
    """Recursive file names at a revision, optionally under one repository-relative path."""
    def build():
        argv = GIT + ["ls-tree", "-r", "--name-only", _rev(rev), "--"]
        p = _rel(path)
        if p:
            argv.append(p)
        return argv, REPO, GIT_CAP
    return _call("git_ls_tree", {"rev": rev, "path": path}, build)


# ---- Sensemaking: sandbox-only index and read-only queries ---------------------------

@mcp.tool()
def knowledge_build() -> dict:
    """Build a local SQLite semantic index for the pinned repository HEAD. Output stays in the sandbox."""
    def build():
        sha = _head_sha()
        INDEX.mkdir(parents=True, exist_ok=True)
        db = INDEX / f"{sha}.db"
        argv = _cli("knowledge-build", "--repo", str(REPO), "--repository", REPOSITORY_ID,
                    "--target-ref", sha, "--db", str(db), "--json")
        return argv, RUN, CLI_CAP
    return _call("knowledge_build", {}, build)


@mcp.tool()
def knowledge_query(operation: str, subject: str = "", search_terms: list[str] | None = None,
                    limit: int = 50) -> dict:
    """Query the built index for the pinned HEAD. operation: snapshot, search, explain, impact, why,
    history, rules-for, term, orientation-summary or context-for. subject: passed as one argument to
    the CLI. For claim operations it is a claim id; for search and term it is literal text; for
    rules-for and context-for it is a path. These operations do no file I/O on the subject's path."""
    def build():
        if operation not in OPERATIONS:
            raise ValueError("unsupported operation")
        sha = _head_sha()
        db = INDEX / f"{sha}.db"
        if not db.exists():
            raise ValueError("no index for HEAD in this sandbox; call knowledge_build first")
        argv = _cli("knowledge-query", "--db", str(db), "--repository", REPOSITORY_ID,
                    "--target-ref", sha, "--operation", operation, "--repo", str(REPO),
                    "--limit", str(max(1, min(int(limit), 250))), "--json")
        if subject:
            argv.append("--subject=" + _text(subject))
        for term in (search_terms or [])[:8]:
            argv.append("--term=" + _text(term))
        return argv, RUN, CLI_CAP
    return _call("knowledge_query", {"operation": operation, "subject": subject,
                                     "search_terms": search_terms, "limit": limit}, build)


@mcp.tool()
def knowledge_audit(indexed_ref: str) -> dict:
    """Source drift between an index built earlier in this sandbox (indexed_ref, a full SHA) and pinned HEAD."""
    def build():
        if not FULL_SHA_RE.fullmatch(indexed_ref or ""):
            raise ValueError("indexed_ref must be a full 40-hex SHA")
        sha = _head_sha()
        db = INDEX / f"{indexed_ref}.db"
        if not db.exists():
            raise ValueError("no index built for that revision in this sandbox")
        argv = _cli("knowledge-audit", "--db", str(db), "--repo", str(REPO),
                    "--repository", REPOSITORY_ID, "--indexed-ref", indexed_ref,
                    "--current-ref", sha, "--json")
        return argv, RUN, CLI_CAP
    return _call("knowledge_audit", {"indexed_ref": indexed_ref}, build)


if __name__ == "__main__":
    mcp.run(transport="stdio")
