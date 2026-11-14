# Worker contract v1: `semantic workspace-query`

## 0. Your role

You are the implementation worker. A separate planner selected this
responsibility, fixed the design decisions in section 4, and will review your
diff and evidence before anything is committed. You own the source edits and
their verification. You may investigate and decide ordinary implementation
details (section 8). If a fixed decision looks wrong or impossible, STOP and
report it; do not change it and do not work around it.

## 1. Workspace

- Repository worktree (work ONLY here):
  `H:/GithubRepositories/sensemaking-skills/.claude/worktrees/frontier-p2-planner`
  on branch `claude/workspace-knowledge-query`, base commit
  `baaec6b92f87a00dbcefdbf865da04f86d5ce59f`.
- Scratch directory for everything temporary (create it):
  `C:/Users/Admin/AppData/Local/Temp/claude/7f91ebcc1962f5dc/49e8512a-dd97-4042-8dc8-f26699400ca1/scratchpad/worker`
  Put scratch repositories, scratch index directories, captured outputs and
  helper scripts there. Create nothing temporary inside the repository.
- Run the CLI from source with the Bash tool:
  `cd <worktree> && PYTHONPATH=src python -m sensemaking_skills.cli semantic ...`
  The `sensemaking-skills` executable on PATH is a stale install. Do not use it.
- Host: Windows 10, Python 3.14, Git Bash. In this repository
  `core.autocrlf=false` and every tracked file is LF. Scratch repositories you
  create may inherit a global autocrlf setting; that is fine.
- The untracked file
  `.sensemaking/receipts/2026-11-10-frontier-p2-planner-executor.session.yaml`
  belongs to the planner. Do not edit, move or delete it.

## 2. Problem

An agent that wants the reviewed knowledge about a file it is about to edit
must run two commands and supply three identity arguments to each:

    sensemaking-skills semantic knowledge-build --repo . --repository OWNER/REPO \
      --target-ref <40-hex HEAD> --db <path outside checkout> [--temporary-checkout] --json
    sensemaking-skills semantic knowledge-query --db <same path> --repository OWNER/REPO \
      --target-ref <same sha> --operation context-for --subject src/x.py --repo . --json

Measured on this host at the base commit: 5.7 s build on a clean checkout,
15.1 s with `--temporary-checkout` (needed whenever the tree is dirty, which
is the normal state during work), plus 3.6 s per query. The Steward's RECALL
reference therefore tells agents to skip the query when no index exists. The
product's open uncertainty is whether reviewed records are reached before a
decision is made; this setup cost is one concrete obstacle.

## 3. Outcome

One new CLI command that needs no prior build and no identity arguments:

    sensemaking-skills semantic workspace-query src/x.py
    sensemaking-skills semantic workspace-query src/a.py src/b.py --json
    sensemaking-skills semantic workspace-query --operation search --term "frozen"
    sensemaking-skills semantic workspace-query --operation workspace-impact --ref origin/main

It resolves the checkout, the commit and a repository label, builds or reuses
a derived SQLite index of that COMMITTED revision in a per-user cache, runs
the existing read operation, and returns the same payload `knowledge-query
--repo .` returns, plus one additive `workspace_index` object.

## 4. Fixed decisions (do not change; escalate instead)

D1. New command name: `workspace-query`, registered in the existing
    `semantic` group inside `register_semantic_commands` in
    `src/sensemaking_skills/semantic_cli.py`.
D2. All new logic lives in ONE new top-level module:
    `src/sensemaking_skills/workspace_knowledge.py`. The CLI function only
    parses options, calls it, converts `(ValueError, OSError, UnicodeError)`
    to `click.ClickException(str(exc))`, and emits with the existing `_emit`.
    Import the new module lazily inside the command function.
D3. It is a front door over EXISTING operations, not a new operation. It must
    call these existing functions and must not reimplement or modify them:
    `build_knowledge_snapshot`, `temporary_commit_checkout`
    (`semantic_architecture/knowledge_sources.py`); `store_snapshot`,
    `query_knowledge`, `query_context_paths`
    (`semantic_architecture/knowledge_store.py`); `inspect_worktree_context`,
    `changed_paths_since_indexed_ref`
    (`semantic_architecture/worktree_context.py`).
D4. Only committed bytes are ever indexed. If the requested commit is the
    current HEAD and the worktree is clean, build from the active checkout;
    in every other case build through `temporary_commit_checkout`. Use
    default build options (no repository structure, no Python imports).
D5. Derived index location: `<index-dir>/<clone-key>/<sha>.sqlite`.
    - `<sha>` is the full 40-hex commit.
    - `<clone-key>` is the first 16 hex characters of the SHA-256 of
      `os.path.normcase` of the resolved absolute Git common directory
      (`git rev-parse --git-common-dir`, resolved against the checkout root
      when relative), so all worktrees of one clone share one cache.
    - default `<index-dir>`: on Windows (`os.name == "nt"`)
      `%LOCALAPPDATA%/sensemaking-skills/index` (fall back to
      `~/AppData/Local/...` when the variable is missing); elsewhere
      `$XDG_CACHE_HOME/sensemaking-skills/index` when that variable is set to
      an absolute path, else `~/.cache/sensemaking-skills/index`.
    - `--index-dir DIR` overrides the default.
    - The index directory must be outside the checkout root: refuse up front
      with a `ValueError` (this must also hold on the reuse path).
    - Refuse when the clone-key directory or the database path is a symlink.
    - On POSIX create the directories with mode `0o700`.
    Never use a predictable path in a shared temp directory.
D6. Ensuring the snapshot (no error-message matching):
    - `--refresh`: delete an existing cache file first, then build.
    - if the cache file does not exist: build and `store_snapshot`.
    - if it exists: try `query_knowledge(..., operation="snapshot", limit=1)`
      for `(label, sha)`. If that raises `ValueError`, build and
      `store_snapshot` into the same file (it is transactional and
      idempotent). If `store_snapshot` then raises, re-raise with a message
      that names the cache file and suggests `--refresh`.
    - never delete a cache file silently except under `--refresh` or the
      retention rule D7.
    - pass `source_root=<real checkout root>` to `store_snapshot`, also when
      the snapshot was built from a temporary checkout.
D7. Retention: after a successful build, keep the 8 most recently modified
    files matching `^[0-9a-f]{40}\.sqlite$` in the clone-key directory and
    delete older ones. Never delete the file in use, never touch other names,
    skip symlinks, ignore `OSError` on deletion. On reuse, update the file's
    mtime (best effort) so recently used snapshots survive.
D8. Options (same meaning as `knowledge-query` where the name matches):
    - positional `PATHS` (0..8): repository-relative files for `context-for`
    - `--operation` choice, default `context-for`: `context-for`, `rules-for`,
      `search`, `explain`, `why`, `impact`, `term`, `orientation-summary`,
      `contradictions`, `snapshot`, `workspace-impact`, `changes`, `history`
    - `--subject`, `--term` (repeatable), `--expect-kind` (repeatable),
      `--limit` (1..250, default 50), `--depth` (0..4, default 2)
    - `--repo DIR` (default `.`): any directory inside the Git working tree;
      resolve the checkout root with `git rev-parse --show-toplevel`
    - `--ref REV` (default `HEAD`): resolved to a full commit SHA
    - `--repository LABEL`: explicit label; otherwise derived (D10)
    - `--index-dir DIR`, `--refresh`, `--json`
D9. Operation rules:
    - `changes` and `history` are refused BEFORE any build with a message
      saying they need several indexed revisions in one database and pointing
      to `knowledge-build` plus `knowledge-query` with an explicit `--db`.
    - `context-for`: the paths are the positional `PATHS`, or the single
      `--subject` when no positional path is given. Both given is an error.
      None given is an error. Normalize each path: replace `\` with `/` and
      strip one leading `./`. One path uses `query_knowledge(...,
      operation="context-for", subject=...)`; 2..8 paths use
      `query_context_paths`. Let the existing functions validate the rest.
    - every other operation rejects positional `PATHS` and passes `--subject`
      through to `query_knowledge`.
    - `workspace_changed_paths` =
      `changed_paths_since_indexed_ref(root, sha)["paths"]` for `context-for`
      and `workspace-impact`; `None` for the others.
D10. Repository label when `--repository` is not given:
    - read `git config --get remote.origin.url`. If present, take only the
      path part (URL form: the path of the URL; scp form `[user@]host:path`:
      the text after the first `:`; anything else, including Windows drive
      paths such as `C:\repos\x`: the string as a filesystem path). Split on
      `/` and `\`, drop empty segments, strip a trailing `.git` from the last
      segment, and join the LAST TWO segments with `/` (one if only one).
      Source name: `origin_remote`.
    - with no origin, or nothing left after parsing: the checkout root's
      directory name. Source name: `local_path`.
    - explicit `--repository`: source name `explicit`.
    - The label must be 1..255 characters.
    - SECURITY: the origin URL may embed credentials. The full URL, its user
      part and its host must never appear in any output or error message.
D11. `--ref` handling: reject a value that starts with `-` or contains
    whitespace or control characters BEFORE calling git. Resolve with
    `git rev-parse --verify --quiet --end-of-options "<ref>^{commit}"` and
    require a 40-hex result. An unresolvable ref (including a repository with
    no commits) is a `ValueError` with a clear message.
D12. Payload: exactly what the existing query function returned, plus
    - `payload["workspace_context"] = inspect_worktree_context(root, sha)`
    - `payload["code"] = "SEMANTIC_KNOWLEDGE_QUERY"`
    - `payload["workspace_index"]` with EXACTLY these keys:
      `indexed_ref` (40-hex), `ref_requested` (the `--ref` text),
      `repository` (label), `repository_identity_source`
      (`explicit` | `origin_remote` | `local_path`),
      `repository_label_verified` (always `False`), `index_path` (string),
      `index_state` (`built` | `reused`), `build_source`
      (`active_checkout` | `temporary_worktree` | `None` when reused),
      `equivalent_operations` (`["build", <operation>]` when built, else
      `[<operation>]`).
D13. Git subprocess calls: argument lists only (never `shell=True`), a
    timeout, `GIT_TERMINAL_PROMPT=0` and `GIT_OPTIONAL_LOCKS=0` in the
    environment, stderr captured. Write your own small private helper in the
    new module; do not import private (`_name`) helpers from other modules.
D14. The command never modifies the checkout: no writes inside the working
    tree, no change to refs, index or config. (The temporary worktree that
    `temporary_commit_checkout` adds and removes is existing behavior.)

## 5. Files you may touch (nothing else)

1. NEW `src/sensemaking_skills/workspace_knowledge.py`
2. EDIT `src/sensemaking_skills/semantic_cli.py`: add the one command. Pure
   addition: `git diff --numstat` must show 0 deleted lines for this file.
3. EDIT `docs/semantic-architecture/persistent-knowledge-cli.md`: insert ONE
   new section `## Zero-setup workspace query (workspace-query)` immediately
   before the heading `## Change granularity and shared authored-pack
   limitation`. Change no other line of this file. Cover, in at most about 60
   lines: what it does and the two main uses (before editing a file; before
   finishing, `--operation workspace-impact --ref <base>`); that only
   committed bytes are indexed and `workspace_context` discloses uncommitted
   changes; where the derived index lives, that it is rebuildable, never
   authority, and pruned to 8 per clone; the `workspace_index` fields; the
   unsupported operations; `--ref`, `--repository`, `--index-dir`,
   `--refresh`; the cost (first call per commit builds, a dirty tree uses a
   temporary worktree); and this claim ceiling: construction evidence only,
   whether agents consult reviewed records earlier because of it is NOT TESTED.
4. EDIT `skills/repository-semantic-steward/references/recall.md`: change
   ONLY numbered step 2 (the line starting `2. Inspect available reviewed
   knowledge records`), appending one or two sentences: when no index exists,
   `semantic workspace-query <file>` builds or reuses a derived index of the
   committed HEAD and answers `context-for` in one command; in a query
   receipt record it as a `build` (when `workspace_index.index_state` is
   `built`) plus the query operation. Touch no other line.
5. EDIT `skills/repository-semantic-steward/SKILL.md`, section
   `## CLI interfaces` only: add one example line at the end of the existing
   bash block (`sensemaking-skills semantic workspace-query path/to/file.py --json`)
   and one sentence in the paragraph right after the block saying that
   `workspace-query` needs neither a prior build nor identity arguments, that
   it indexes the committed HEAD into a per-user derived cache (through a
   temporary worktree when the checkout is dirty), and that uncommitted bytes
   are never indexed. These exact phrases are pinned by tests and must remain
   in the file: `` `knowledge-query --repo .` ``, `clean checked-out`,
   `dirty active checkout`. Do not edit the frontmatter or any other section.

Do NOT touch: `tests/**`, `.sensemaking/**`, `CLAUDE.md`, `STATUS.md`,
`CONTEXT.md`, `docs/public-api-v1.0.yaml`, `pyproject.toml`, anything under
`src/sensemaking_skills/semantic_architecture/`, or any other file. Three
draft pull requests are editing `knowledge_store.py`,
`knowledge_retrieval.py`, `knowledge_architecture.py`, other parts of the two
docs above, and the knowledge JSON files; staying inside the stated lines
keeps this change mergeable with them.

## 6. Invariants that must remain true

I1. Existing commands behave exactly as before; `semantic_cli.py` gains lines
    only.
I2. Frozen public Python API: do not change any `__all__`, and do not edit
    `semantic_architecture/__init__.py`.
I3. No import of source-only packages (`campaign_validation`,
    `campaign_accounting`, `exploratory_authorization`,
    `exploratory_execution`) and no new third-party dependency.
I4. ASCII only in every string the code prints or raises, and in both source
    files (this codebase runs on Windows cp1252). Use `->`, never an arrow.
I5. No bare `except:` and no `except Exception:` that swallows errors.
I6. LF line endings in every touched file. Never rewrite a tracked file with
    a Python script; use the Edit tool for existing files.
I7. Repository policy for this phase: do NOT add unit tests and do NOT run
    pytest. Verification is the real CLI path plus static checks (section 9).
I8. No `git commit`, `git push`, `git stash`, `git clean`, `git reset`,
    branch switch, or `git worktree prune`. The planner commits.

## 7. What success requires

- Every check in section 9 passes, or is reported as FAIL / NOT_RUN with the
  reason. A failing check you could not fix is a valid result when reported.
- `git status --short` lists only the five files of section 5 (plus the
  planner's untracked receipt).
- The report of section 10 is complete and literal.

## 8. You may decide

Private helper names and decomposition; exact wording of help text and error
messages (ASCII, specific, no secrets); how to order the internal steps as
long as section 4 holds; reasonable git timeouts; the layout of the new doc
section; how you script the verification in the scratch directory.

## 9. Verification (real path; report command and key output for each)

Use `--index-dir <scratch>/index` for every check except V1 and V2, which
prove the default location works. `WT` is the worktree, `CLI` is
`PYTHONPATH=$WT/src python -m sensemaking_skills.cli semantic`.

V1.  In WT (dirty because of your edits): `CLI workspace-query
     src/sensemaking_skills/semantic_cli.py --json` exits 0;
     `workspace_index.index_state == "built"`, `build_source ==
     "temporary_worktree"`, `indexed_ref == git rev-parse HEAD`,
     `repository == "ThorStarlord/sensemaking-skills"`,
     `repository_identity_source == "origin_remote"`;
     `workspace_context.worktree_clean == false`; `context.ownership` names
     `component:semantic-cli`. Report the wall time and the index path.
V2.  Same command again: `index_state == "reused"`, `build_source == null`,
     same `indexed_ref`. Report the wall time.
V3.  Equivalence with the existing two-step path: `knowledge-build
     --temporary-checkout --repository ThorStarlord/sensemaking-skills` into
     a scratch database, then `knowledge-query --operation context-for
     --subject src/sensemaking_skills/semantic_cli.py --repo .`. The
     `context`, `claims` and `relations` values must be identical to V1's
     (compare with a small scratch script; report equal/not equal).
V4.  Three positional paths: the payload has `contexts` with 3 entries.
V5.  `--operation search --term frozen` and `--operation explain --subject
     rule:frozen-public-python-api` exit 0 with non-empty `claims`.
V6.  `--operation workspace-impact --ref HEAD~1` exits 0, has a
     `workspace_impact` object, `build_source == "temporary_worktree"`.
V7.  `--operation changes` and `--operation history --subject adr:0031` exit
     non-zero with the D9 message, and create no cache file.
V8.  Scratch repository, one commit, clean, no reviewed records, no origin:
     `workspace-query src/a.py` exits 0; `build_source ==
     "active_checkout"`; `repository_identity_source == "local_path"`; the
     knowledge gaps are NOT_ASSESSED; `git status --porcelain` in the scratch
     repository is empty before and after.
V9.  In scratch repositories set `remote.origin.url` (no network needed) to
     each of: `https://user:s3cretTOKEN@example.invalid/acme/widget.git`,
     `git@example.invalid:acme/widget.git`,
     `ssh://git@example.invalid:2222/acme/widget`, `C:\repos\widget`.
     Labels must be `acme/widget` (first three) and `repos/widget`. For the
     first, neither `s3cretTOKEN` nor `example.invalid` may appear anywhere
     in stdout or stderr, also when you force an error (for example with
     `--ref nope`).
V10. A directory that is not a Git repository, and a Git repository with no
     commits: non-zero exit, a clear one-line error, no Python traceback.
     `--ref -x` and `--ref "a b"` are rejected without running git on them.
V11. `--index-dir <a directory inside the scratch repository>` is refused
     with a non-zero exit and creates nothing in the repository.
V12. Retention: in a scratch repository make 10 commits, running
     `workspace-query src/a.py` after each. At the end the clone-key
     directory holds exactly 8 `<sha>.sqlite` files and the newest commit's
     file is among them.
V13. `--refresh` on a cached commit gives `index_state == "built"`.
V14. `workspace-query 'src\a.py'` (backslash) works in the scratch repository.
V15. `PYTHONIOENCODING=cp1252` with `workspace-query --help` and with one
     query: no `UnicodeEncodeError`. Show that both source files contain no
     non-ASCII byte.
V16. Static checks, all from WT:
     `python -m ruff check --select E4,E7,E9,F src/sensemaking_skills/workspace_knowledge.py src/sensemaking_skills/semantic_cli.py`
     `python scripts/validate-docs-currentness.py --repo-root .`
     `python scripts/validate-error-boundaries.py`
     `python scripts/validate-product-boundary.py`
     `python scripts/validate-skill-hygiene.py`
     `python scripts/validate-repo.py`
     `python scripts/validate-release-contract.py --repo-root .`
     `python scripts/validate-contract-authority.py --repo-root .`
     (all seven validators exit 0 at the base commit).
V17. `git diff --numstat` (0 deletions for `semantic_cli.py`),
     `git status --short`, and `git ls-files --eol` plus
     `git diff --stat` for the touched files (all `w/lf`); for the new
     untracked module show it has no CR byte.
V18. `CLI knowledge-query --help` still lists the same options as before
     (compare with `git show HEAD:src/sensemaking_skills/semantic_cli.py`
     if useful) and `CLI --help` lists `workspace-query`.

## 10. Report format (your final message)

1. STATUS: `COMPLETE`, `COMPLETE_WITH_DEVIATIONS`, or `BLOCKED`.
2. CHANGES: `git status --short`, `git diff --stat`, and two or three
   sentences per file on what you did.
3. VERIFICATION: a table V1..V18 with PASS / FAIL / NOT_RUN, each with the
   command you ran and the decisive output (trimmed, literal, not
   paraphrased). Unit tests: NOT_RUN (policy).
4. DEVIATIONS from this contract, each with the reason.
5. OBSERVATIONS: anything surprising in the existing code or behavior.
6. FAILURES and what you tried.
7. UNRESOLVED QUESTIONS for the planner.
8. The model identity you believe you are running as, if you can tell.

Do not claim a check passed unless you ran it and saw the output. Do not
summarize away a failure.

## 11. Stop and report (escalate) when

- you need to touch a file outside section 5, change an existing function,
  or change a fixed decision;
- an existing function does not behave as section 4 assumes;
- a verification fails and you cannot find the cause after a focused attempt;
- anything would require adding or changing a test, a dependency, the public
  API manifest, or a knowledge record.
