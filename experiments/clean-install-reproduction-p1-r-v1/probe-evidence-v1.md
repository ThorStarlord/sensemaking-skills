# Task P1-R — Probe Evidence (recorded run)

task: Task P1-R — Clean-Install Reproduction Probe
experiment_type: reproduction
record: probe-evidence-v1
recorded_at: 2026-08-07
question: "Does a fresh user following the documented install/setup path receive
and invoke the current canonical repo-sensemaker?"

## 1. Clean environment identity

- Fresh venv (no system packages, no repo on path):
  `C:\Users\Admin\AppData\Local\Temp\p1r-20260807\venv`
- Python: 3.14.3 (venv interpreter)
- OS: Windows (amd64), host user profile redirected for the setup run
  (`USERPROFILE` -> `...\p1r-20260807\fresh-home`) so the probe simulates a
  fresh user and cannot touch the real `~/.agents/skills`.
- Run cwd: outside the repository checkout (temp dir), so the source checkout
  could not shadow the installed package.

## 2. Package/artifact/version installed

- `sensemaking-skills==0.2.1` installed from **PyPI** (only available version:
  `pip index versions` -> 0.2.1). This is the actual distributable a normal
  user receives.
- The repo's local `dist/sensemaking_skills-0.2.1-py3-none-any.whl` (untracked
  local build) was inspected for comparison: 25 entries, identical CLI surface
  (analyze / test / validate only).
- Note: `dist/` is NOT tracked in git (`git ls-files dist/` empty) — the
  repository does not contain the artifact it documents; only PyPI does.

## 3. Exact documented commands followed

From GETTING_STARTED.md:22-27 (the documented install path):

```
pip install sensemaking-skills        -> executed as: pip install sensemaking-skills==0.2.1 (pinned to the only available version)
sensemaking-skills setup-skills       -> executed literally from the clean venv
```

The second command was run with `USERPROFILE` redirected to the probe's
fresh-home, so its target would be the fresh user's `~/.agents/skills`.

## 4. setup-skills exit/result

```
> sensemaking-skills setup-skills
Usage: sensemaking-skills [OPTIONS] COMMAND [ARGS]...
Try 'sensemaking-skills --help' for help.

Error: No such command 'setup-skills'.
EXIT_CODE=2
```

The documented command **does not exist** in the shipped artifact. The shipped
CLI exposes only: `analyze`, `test`, `validate`.

Root cause of the absence (dated): `setup-skills` was added to source in
commit `8584d5a` (2026-05-26, "feat: Add setup-skills command for
agent-discoverable installation"), but the 0.2.1 wheel was built 2026-05-25
(CHANGELOG [0.2.1] - 2026-05-25) and the version was never bumped. PyPI 0.2.1
therefore predates the documented feature. The current source
(`origin/main` @ b580389) DOES contain `@cli.command(name="setup-skills")`
(`src/sensemaking_skills/cli.py:120`) — docs and source agree; the shipped
artifact lags both.

## 5. Files actually installed

`sensemaking_skills/` in site-packages (recursive, excluding `__pycache__`):

```
sensemaking_skills\__init__.py
sensemaking_skills\cli.py
sensemaking_skills\config.py
sensemaking_skills\paths.py
sensemaking_skills\registry.py
sensemaking_skills\runner.py
sensemaking_skills\validation.py
sensemaking_skills\commands\__init__.py
sensemaking_skills\defaults\canonical-vocabulary.yaml
sensemaking_skills\defaults\workflow-registry.yaml
sensemaking_skills\defaults\__init__.py
sensemaking_skills\skills\__init__.py
sensemaking_skills\skills\base.py
sensemaking_skills\skills\repo_sensemaker.py
sensemaking_skills\skills\workflow_planner.py
```

**No SKILL.md anywhere in site-packages** (recursive search: NONE). The
`skills/` subpackage contains only Python modules. Wheel inspection confirms:
`SKILL.md` entries in wheel = 0.

## 6. repo-sensemaker SKILL.md identity/hash/content version

- Canonical target (what the flow is supposed to deliver):
  `origin/main:skills/repo-sensemaker/SKILL.md`
  sha256 prefix `b1a707b4`, 165 lines (164 content + final newline).
- Installed in clean environment: **NONE** (nothing delivered).
- Real machine's `~/.agents/skills/repo-sensemaker/SKILL.md`: sha256 prefix
  `EE1F58F0` — the 119-line variant from commit `178d5f0` (2026-05-22),
  i.e. 4 months stale, still teaching the pre-ADR-0010
  `create-artifact.py` path-recomputation protocol. Untouched by this probe
  (USERPROFILE redirect; verified hash unchanged).

## 7. Which copy normal invocation resolves to

- Fresh user: **nothing** — the documented command does not exist in the
  shipped CLI, so no skill can be installed or invoked.
- This host (observed during P1 setup): the `/repo-sensemaker` skill command
  resolves to the global `C:\Users\Admin\.agents\skills\repo-sensemaker\SKILL.md`
  (the stale 178d5f0 copy above), NOT the canonical in-repo skill.

## 8. Observed errors/warnings

- `Error: No such command 'setup-skills'.` (exit code 2) — blocking.
- pip cache warning (`Cache entry deserialization failed, entry ignored`) —
  harness noise, non-product.
- No files written to the probe fresh-home `~/.agents/skills` (directory does
  not exist after the run) and none to the real profile.

## Delivery vs invocation (tested separately)

- **delivery**: FAIL — the shipped artifact contains zero SKILL.md files, so
  the current canonical `repo-sensemaker/SKILL.md` cannot arrive in any fresh
  environment via the documented path.
- **invocation**: FAIL — the documented command (`sensemaking-skills
  setup-skills`) is absent from the shipped CLI; a fresh user cannot install
  anything, and on this host agent invocation resolves to a 4-month-stale
  global copy instead of the canonical skill.

## Harness-integrity note

First attempt was valid and is the recorded run: the venv was created fresh,
the package came from PyPI (the real user artifact), the command was run
literally, and no repair/retry was performed. No experiment-harness mistake
was detected; no silent correction was needed.
