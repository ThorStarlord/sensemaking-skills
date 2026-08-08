# Task P1-R — Outcome (precommitted fork verdict)

task: Task P1-R — Clean-Install Reproduction Probe
experiment_type: reproduction
record: outcome-v1
recorded_at: 2026-08-07
question: "Does a fresh user following the documented install/setup path receive
and invoke the current canonical repo-sensemaker?"

## Verdict

```
CONFIRMED
Fresh documented install cannot deliver/invoke the current canonical
repo-sensemaker.
-> focused distribution repair becomes justified.
```

## Reason (from probe-evidence-v1.md)

- **Delivery fails**: the shipped artifact (PyPI `sensemaking-skills==0.2.1`,
  the only available version) contains **zero SKILL.md files** — the
  `skills/` subpackage ships only Python modules. The current canonical
  `repo-sensemaker/SKILL.md` (sha256 `b1a707b4`, origin/main) cannot arrive in
  a fresh environment via the documented path.
- **Invocation fails**: the documented command `sensemaking-skills
  setup-skills` (GETTING_STARTED.md:23-24) **does not exist** in the shipped
  CLI (`Error: No such command 'setup-skills'.`, exit 2; shipped commands:
  analyze / test / validate only). The feature was added to source on
  2026-05-26 (commit `8584d5a`) but the wheel was built 2026-05-25 and the
  version was never bumped.
- On this host, agent invocation additionally resolves to a 4-month-stale
  global copy (commit `178d5f0`, 2026-05-22) instead of the canonical skill.

The confirmed failure is **stronger and more fundamental than the P1
hypothesis**: P1 predicted the setup-skills *path resolution* would break for
pip installs; the probe found the shipped artifact does not contain the
`setup-skills` command at all, and contains no SKILL.md trees either. Both
layers fail independently.

## What is now justified (per the precommitted fork)

- Focused distribution repair becomes justified: rebuild/re-version the
  distributable so the shipped CLI includes `setup-skills`, ship the canonical
  SKILL.md trees in the artifact, and reconcile stale installed copies.
- This is a CONDITIONAL authorization signal from the probe; the actual repair
  is NOT authorized by this task. Repair requires a separate decision.

## Explicit non-authorizations (unchanged)

- No distribution repair performed or started in this task.
- No packaging, `setup-skills`, skill, validator, or docs modification.
- No Task P2.
- Evidence committed locally only; nothing pushed.

## Deprecated alternative

If the outcome had been NOT_REPRODUCED, distribution would be deprioritized
and the priority would return to product/interaction learning. That branch is
now closed by this verdict.
