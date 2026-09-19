# Execution Interface & Agent-Factorization v1 — Milestone Handoff

**Status:** implementation complete; closeout package under qualification  
**Date:** 2026-09-18  
**Release line:** `1.0.0rc3.dev0` development toward `1.0.0rc3`  
**Scope:** release-authority audit, execution delegation/return contracts, high-delegation working context, external-executor interchange, AI Software Factory projection, explicit GitHub provenance publication, and cross-repository execution projection  
**Next mode after closeout:** normal-use validation / real executor dogfood; no additional construction package selected

## 1. Objective

Extend Sensemaking from:

```text
select / preserve the warranted responsibility
```

to a bounded control-plane boundary:

```text
already-selected responsibility
-> explicit execution handoff
-> external worker / factory
-> returned result evidence
-> parent reassessment
```

without turning Sensemaking into a planner, scheduler, coding runtime, merge
controller, or semantic truth engine.

## 2. Package ledger

| Package | PR | Qualified head | Merge SHA |
| --- | --- | --- | --- |
| Post-RC2 development reopen | #387 | `b5b96c988f882949c7f8ab9969094e7d101db68a` | `c5c35be0a1a0a651343716b018be8e3de31f9f1f` |
| Release Authority Auditor | #388 | `c486a69d296ae05e894d70393172e616c47a6295` | `7e2c37d97515531d61585355c1094df729e4cbf5` |
| Execution handoff/result + working context | #389 | `50c5e791e39153fc2970730df665c9097eca520c` | `d4ccf89edd143f126c3815c9861c705c4226c137` |
| Generic executor / AI Software Factory bridge | #390 | `a8ca9f9bbd2f0fe2ac2b73b12d987b6e373400dc` | `df566bbaf34e5abaec5b2fe2e330997fd015a2d1` |
| Explicit GitHub provenance publication | #391 | `ac921c561627e77b759ff9d2cdefb7772ec3aaab` | `2050687909cb19ca20d932ed598c3e2fea1325e8` |
| Cross-repository execution projection | #392 | `97c7cb3fbfc48647c54f7938e33d2401495094d9` | `4f89e92030af4dee5c931b59b839869911e6c366` |

Each implementation package passed its applicable hosted exact-head gates before
merge.

## 3. Integrated feature-head qualification

After PR #392 integrated, exact `main` source
`4f89e92030af4dee5c931b59b839869911e6c366` passed:

- Product Validation — run `35408048842` — PASS;
- Lab Validation — run `35408048855` — PASS;
- Release Candidate Distribution — run `35408048919` — PASS.

This establishes repository integration/mechanical qualification for the
feature set. It does not establish empirical usefulness or native-harness
portability.

## 4. Implemented capability boundaries

### 4.1 Release Authority Auditor

`sensemaking-skills release audit` reconciles repository-owned source/target
identity, local Git identity/state, current release docs, workflow identity
mechanics, and expected artifact names.

It explicitly does not establish CI qualification, publication, semantic truth,
or owner authorization.

### 4.2 Execution Handoff / Worker Result

Campaign v2 remains authoritative and unchanged.

Additive companions preserve:

- selected responsibility and authority;
- exact Campaign-state digest;
- exact primary/multi-target identities;
- success/evidence requirements and forbidden actions;
- worker/source/validation/evidence/claim return metadata;
- append-only digest integrity.

```text
handoff recorded != responsibility selected by tool
authority recorded != authority granted by tool
worker success != global closure
returned evidence != admitted evidence
```

### 4.3 High-delegation working context

`campaign working-context` provides a compact continuation projection over
mission, responsibility, decision blocked, uncertainty, authority, targets,
evidence, stop conditions, and latest worker exchange.

It does not recommend a next action.

### 4.4 External executor interchange

The generic execution interchange exports integrity-bound handoff envelopes and
imports integrity-bound worker-result envelopes.

The result-import boundary still requires parent reassessment and does not
automatically admit evidence.

### 4.5 AI Software Factory bridge

The adapter renders a GitHub Issue payload and command template compatible with
the current factory model.

Repository and workflow are caller supplied. Sensemaking does not select
`archon-ship`, `archon-lifecycle`, or another workflow; it does not publish
or submit the factory run.

### 4.6 GitHub provenance publication

`campaign provenance-publish` is preview-by-default. Actual comment mutation
requires an explicit `--publish` transition plus token environment. Exact
provenance markers suppress duplicate publication.

Publication does not authorize work or establish semantic correctness.

### 4.7 Cross-repository execution projection

`campaign multi-target execution-view` translates only explicit
`depends_on` and `release_after` relations into prerequisite direction and
deterministic topological layers.

Descriptive relationships remain non-ordering.

```text
precedence projection != execution plan
same layer != parallel execution authorized
```

## 5. Architecture preserved

This milestone did not create:

- `StrategicPlanner` / `OuterLoopEngine`;
- `WarrantEngine` or generic `AgentState`;
- Campaign schema v3;
- automatic responsibility, capability, Skill, workflow, or repository
  selection;
- automatic evidence admission;
- scheduler, queue, retry, or worker-allocation engine;
- automatic GitHub issue publication;
- autonomous merge, release, deploy, or PyPI publication;
- cross-repository transactional activation.

The central division remains:

```text
Sensemaking selects/supports the decision boundary
external orchestration coordinates already-selected work
workers return evidence
the parent semantic agent reassesses
```

## 6. Live closeout dogfood

Issue #393 is the live closeout handoff/result record for this milestone. It is
ordinary repository work rather than a synthetic feature fixture.

The issue dogfoods the **operational contract shape**—explicit responsibility,
authority, exact target, evidence requirements, forbidden actions, returned
source/CI evidence, and parent reassessment. It is not claimed as proof that the
new CLI generated its own implementation work.

That distinction preserves:

```text
contract used in real work != every transport path empirically qualified
```

## 7. Release posture

Qualified `1.0.0rc2` remains immutable historical provenance at
`c9b86138d3919c4fce87040f14161364a0c1c3a0`.

Current source remains `1.0.0rc3.dev0` / `development`.

This milestone does not warrant freezing RC3 by itself. A future RC3 freeze is a
separate release decision after later candidate-changing work has converged.

## 8. Residual boundaries

- GitHub branch/ruleset protection remains external Issue #384; this workspace
  still cannot enforce that admin setting.
- native-harness usefulness remains unestablished;
- independent-harness portability remains unestablished;
- comparative/product-value claims remain unestablished;
- external-executor usefulness has mechanical coverage plus one live contract
  dogfood, not a broad empirical corpus;
- the AI Software Factory adapter has not yet executed a live factory run from a
  generated handoff.

These are claim ceilings or future evidence opportunities, not automatic
construction responsibilities.

## 9. Continuation rule

After the closeout package qualifies and integrates:

```text
NEXT MODE = NORMAL_USE_VALIDATION
CURRENT CONSTRUCTION PACKAGE = NONE
```

Use the new interfaces during real repository work. Reopen construction only
from concrete recurring pressure or new explicit owner direction.

Do not add orchestration machinery merely because the handoff boundary now
exists.
