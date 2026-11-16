# Amendment 3 to PREREG.md: knowledge-tool environment defects, and rerun

**Status:** committed before the attempt-4 battery ran.

## Observations (attempt 3, after Amendment 2)

- Git tools worked in attempt 3: `git_log`, `git_merge_base`, `git_show_file`, and `git_diff_names` returned exit 0 or the expected refusal. `sm` was connected in all children.
- `cal01-capability`: `knowledge_build` exited 1 with `ModuleNotFoundError: No module named 'click'`. The subsequent three knowledge calls were refused, because no index existed. B1 for the knowledge tools was not met, and B6 could not be evaluated.

## Cause 1 (confirmed)

`_env()` in the server passed only `PATH, SYSTEMROOT, TEMP, TMP` to child processes. `click` is installed in the user site-packages, which Python locates through `APPDATA`. Without `APPDATA`, the CLI child could not import `click`. The fix passes `APPDATA` and `LOCALAPPDATA`, which are path variables only.

## Cause 2 (found when rechecking Cause 1)

After Cause 1 was fixed, the debug sandbox's `knowledge_build` refused with "dirty or untracked worktree: source bytes cannot be pinned". The sandbox clone had been checked out under the host's system Git config, which sets `core.autocrlf=true`, and it lacked `core.longpaths`. The server sets `GIT_CONFIG_NOSYSTEM=1`, so the CLI's status check then saw every file as modified, and long tracked paths failed with "Filename too long".

The fix is in `make_fixtures.py`, which sets `core.autocrlf=false` and `core.longpaths=true` on the sandbox clone before checkout. These are local settings, so they do not depend on the host's system config. In the debug sandbox, a server-like `git status` (with `GIT_CONFIG_GLOBAL=nul` and `GIT_CONFIG_NOSYSTEM=1`) was clean with no stderr. `knowledge_build` then exited 0 in 12.2 s, with claim_count 255 and digest `84dc854c917e932de16b1c391725948a5c2fecb238136f99d8be6179498a198`.

## Consequences

- Attempt-3 records (`transcripts/attempt3-knowledge-env-defect/`, `results/attempt3-knowledge-env-defect/`) are kept as a defect record. They do not count toward B1 for the knowledge tools, or toward B6.
- Their B2 to B4 observations (outside reads and credential-like reads denied, no web or shell tool, no network hit) were also made with the defective sandbox. They are repeated in the clean attempt-4 battery, which is the only battery used for admissibility.
- B6 requires that the server's knowledge build digest equal a direct build by the orchestrator at the same SHA. The orchestrator's direct build is recorded in `results/direct-build-at-pin.json`.

## Configuration

Unchanged in its flags, operations, exclusions and stop rules. Only the server's child environment (path variables) and the sandbox's local Git settings changed.
