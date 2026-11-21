Planner review 1 of `workspace-query`: accepted in substance; six targeted repairs follow.

Your implementation passed my independent review harness (50 pass, 0 fail, 1
not run for lack of symlink privilege), including payload equality with the
two-step path for seven operations. Deviations 1, 2 and 3 are accepted.
Answers to your questions:

- KeyError/TypeError: keep D2 unchanged. `cli.py` `main()` already reports any
  exception as a one-line `Error: ...` with exit 1, and three malformed-record
  probes (missing id, non-object claim, wrong schema version) all surfaced as
  `ValueError`. No change.
- V18: my wording was ambiguous. `semantic --help` listing the command is what
  was meant. Satisfied.

The repairs below come from probes I ran against your code. Four of them are
gaps in my contract, not in your work. Same workspace, same rules (sections 1,
5, 6 and I1-I8 of the contract still hold; touch only the same five files).
Do NOT use `rm -rf` on a path held in a shell variable (a host safety check
blocks it); use fresh, literally named scratch directories instead.

## Repairs

A. Label must never carry credentials (revises D10).
   Evidence: with `remote.origin.url` set to
   `user:tok3nXYZ@example.invalid:acme/widget.git` (a malformed scp-like form),
   `workspace_index.repository` was `tok3nXYZ@example.invalid:acme/widget`,
   which prints the token and the host.
   Required: if either of the kept label segments contains `@` or `:`, the
   origin is not usable; fall back to the checkout directory name with source
   `local_path`. (So an origin of `C:\widget` also falls back.)

B. Links in the cache path (revises D5).
   Evidence: a Windows directory junction planted as `<index-dir>/<clone-key>`
   is accepted (`Path.is_symlink()` is False for a junction) and the database
   was written into the junction's target.
   Required: refuse the clone-key directory and the database path when either
   is a symlink OR resolves somewhere else. Keep `is_symlink()` and add a
   check that works on Python 3.11 too: with the index base already resolved,
   `candidate.resolve() != candidate` means a link or junction. Same clear
   `ValueError`, raised before anything is created or written.

C. Unreadable cache (revises D6).
   Evidence: a cache file with a valid SQLite header and the right
   `user_version` but no tables gives `Error: no such table: snapshots`: no
   rebuild, no cache path, no `--refresh` hint, because the probe raises
   `sqlite3.OperationalError`, not `ValueError`.
   Required:
   - the snapshot probe treats `sqlite3.Error` like `ValueError` (fall through
     to build and `store_snapshot`);
   - if the final query (`query_knowledge` / `query_context_paths`) raises
     `sqlite3.Error`, convert it to a `ValueError` that names the cache file
     and suggests `--refresh`.
   Importing `sqlite3` from the standard library is fine.

D. `rules-for` path (revises D9).
   Evidence: `--operation rules-for --subject 'src\sensemaking_skills\semantic_cli.py'`
   returns 0 claims; with forward slashes it returns 4. A silent empty result
   reads as "no rule applies".
   Required: apply the same path normalization to `--subject` for `rules-for`
   as for `context-for` paths.

E. Help text (in `semantic_cli.py`; additions only, still 0 deleted lines
   relative to HEAD).
   - `--term` help says `(search, term)`. The `term` operation takes
     `--subject`. Make it `(search operation only)`, as in `knowledge-query`.
   - The command docstring must tell a `--help` reader about the side effect:
     it builds or reuses a derived index of the committed revision in a
     per-user cache outside the checkout (see `--index-dir`), and uncommitted
     bytes are never indexed. Two or three short ASCII lines.

F. Doc section in `persistent-knowledge-cli.md` (only inside the section you
   added): add
   - one bullet: a reused cache file is trusted as written and is not
     re-verified against Git; anyone who can write to the index directory can
     alter answers, so keep the default per-user location or a private
     directory, and use `--refresh` when in doubt;
   - to the label bullet: an origin whose path segments contain `@` or `:` is
     not used and the directory name is used instead.

## Verification to run and report (command + decisive literal output)

W1. Origin `user:tok3nXYZ@example.invalid:acme/widget.git` in a scratch repo:
    `repository_identity_source == "local_path"`, label = directory name, and
    neither `tok3nXYZ` nor `example.invalid` in stdout or stderr. Origin
    `C:\widget`: `local_path`. The four V9 origins still give `acme/widget`,
    `acme/widget`, `acme/widget`, `repos/widget`.
W2. Junction: run once with `--index-dir <scratch>/jA` to read the clone key
    from `index_path`. Create a NEW directory `<scratch>/jB` and a new empty
    `<scratch>/jTarget`, then `cmd /c mklink /J <jB>\<key> <jTarget>` (run it
    through Python `subprocess` with Windows-style paths). `workspace-query
    src/a.py --index-dir <scratch>/jB` must exit non-zero with the refusal
    message and `jTarget` must stay empty.
W3. Plant a database with the right `user_version` and no tables at the cache
    path of a scratch repo commit (use a fresh `--index-dir`; create the file
    with a small Python script: `sqlite3.connect`, `PRAGMA user_version=<
    knowledge_store.SCHEMA_VERSION>`, `CREATE TABLE junk(x)`). The next
    `workspace-query` must exit 0 with `index_state == "built"`. A file of
    garbage bytes must still give the error that names the cache file and
    `--refresh`, and must not be deleted.
W4. `rules-for` with backslashes and with forward slashes on
    `src/sensemaking_skills/semantic_cli.py` in the real repository: same
    number of claims (4 at this commit).
W5. `workspace-query --help` output (paste it).
W6. Regression: ruff on both source files; `validate-error-boundaries`,
    `validate-docs-currentness`, `validate-skill-hygiene`; `git diff --numstat`
    (0 deletions for `semantic_cli.py`); `git status --short`; LF and ASCII
    checks on the two source files; one built-then-reused smoke run with a
    fresh `--index-dir` in the real repository.

Report in the same format as before (status, changes, W1-W6 table,
deviations, observations, failures, questions).
