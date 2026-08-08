# Task P1-R — Clean-Install Reproduction Probe (v1)

task: Task P1-R — Clean-Install Reproduction Probe
experiment_type: reproduction (spawned directly by Task P1; NOT a product/interaction experiment; NOT Task P2)
status: in_progress
created_at: 2026-08-07

## Question (exactly as authorized)

> Does a fresh user following the documented install/setup path receive and
> invoke the current canonical `repo-sensemaker`?

## Relationship to Task P1

P1 concluded: "The execution/distribution surface is now the leading candidate
for the highest-value next engineering work, conditional on clean-environment
reproduction." P1-R tests exactly that single assumption. It is the cheapest
credible probe: fresh environment -> install the actual distributable package
-> run the documented setup path -> inspect what skill is installed/invoked.

## Precommitted outcome fork (decided BEFORE execution)

```
CONFIRMED
Fresh documented install cannot deliver/invoke the current canonical
repo-sensemaker.
-> focused distribution repair becomes justified.

NOT_REPRODUCED
Fresh documented install correctly delivers and invokes the canonical
repo-sensemaker.
-> deprioritize distribution and return to product/interaction learning.

AMBIGUOUS
Environment/artifact/docs do not permit a clean conclusion.
-> identify exactly one cheapest discriminator; no repair.
```

## Two concepts tested SEPARATELY

- **delivery**: did the current canonical `repo-sensemaker/SKILL.md` actually
  arrive in the fresh environment?
- **invocation**: is that the SKILL.md an ordinary user/agent actually
  resolves?

A system can pass one and fail the other (e.g. correct skill installed + agent
still invokes a stale global copy = invocation defect; skill absent from wheel
= delivery defect).

## Recorded fields (per the probe design)

1. clean environment identity
2. package/artifact/version installed
3. exact documented commands followed
4. setup-skills exit/result
5. files actually installed
6. repo-sensemaker SKILL.md identity/hash/content version
7. which copy normal invocation resolves to
8. observed errors/warnings

## Constraints (frozen)

- Genuinely clean environment (fresh venv OUTSIDE the repository checkout).
- Use the actual distributable artifact a normal user would receive
  (PyPI `sensemaking-skills==0.2.1` — verified available; `dist/` in the repo
  is untracked/local-build-only and is NOT the user-facing artifact).
- Follow the documented installation/setup instructions literally
  (GETTING_STARTED.md:22-27 flow).
- Do NOT modify packaging, `setup-skills`, skills, validators, docs, or
  installed files to make the test pass. No retries after repairs.
- If the first attempt is invalid because of an experiment-harness mistake
  rather than product behavior, STOP and report rather than silently
  correcting it.
- Do not repair anything during the run.
- Commit the P1-R evidence locally only and stop.
- NO distribution repair and NO Task P2 are authorized.

## Artifact set (this directory)

- `charter-v1.md` — this file.
- `probe-evidence-v1.md` — the recorded run (fields 1-8 above).
- `outcome-v1.md` — the precommitted fork verdict (CONFIRMED /
  NOT_REPRODUCED / AMBIGUOUS) with the reason.

## Stop condition

Record `outcome-v1.md`, commit locally, stop. No implementation.
