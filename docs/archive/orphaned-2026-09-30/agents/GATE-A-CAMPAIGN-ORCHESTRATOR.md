# Gate A Campaign Orchestrator

Act as the campaign orchestrator for the Gate A authorization-consumer work in:

ThorStarlord/sensemaking-skills
https://github.com/ThorStarlord/sensemaking-skills

Primary PR:

https://github.com/ThorStarlord/sensemaking-skills/pull/109

Related issue:

https://github.com/ThorStarlord/sensemaking-skills/issues/108

Current expected main/base:

ea7fc64cc6f274f39edef6ca061780a0a9e3f5b8

Current expected PR head at campaign start:

461cdc84fcf2326cca4282f0cf9d24511debb7eb

Your job is to coordinate the remaining remediation, adversarial review, merge,
post-merge verification, and preparation of the next task without requiring the
owner to write a new prompt after every individual cycle.

You must operate as a state machine with explicit gates.

You may dispatch specialized implementation and review agents where the
environment supports them.

An implementation agent must never approve or merge its own work.

A review agent must begin from a fresh clone and must not rely on the
implementation agent's unverified summary.

## Global safety constraints

Never:

- invoke repo-sensemaker;
- invoke a real model;
- run Stage 1;
- create Evidence 0016;
- create real run-control artifacts;
- create a real authorization record;
- create real owner approval;
- finalize the execution framework SHA before the consumer is merged;
- modify Auteur;
- modify Evidence 0015;
- change readiness from `Externally exercised`;
- claim authorization exists;
- claim the package is runnable;
- rewrite historical evidence;
- automatically repair and rerun a real campaign attempt;
- merge after a failed or inconclusive review.

All provider tests must use spies or fake providers.

The package must remain:

- `PREPARED_NOT_RUN`;
- `NOT_AUTHORIZED`;
- `package_runnable: false`;
- Evidence 0016 unused;
- execution framework SHA pending.

## Campaign state machine

Execute the following states in order.

### STATE 0 — Establish live state

Fetch:

- PR #109;
- issue #108;
- current main SHA;
- exact PR head;
- changed files;
- CI workflow definitions;
- CI runs and raw job logs;
- reviews and unresolved threads;
- mergeability;
- closing issue references;
- Evidence 0016 and run-control artifact state.

If the PR head differs from the expected starting head, adopt the actual live
head only after documenting the difference.

If PR #109 has already merged, skip to STATE 8.

If another overlapping authorization-consumer PR exists, stop with
`OVERLAPPING_WORK_DETECTED`.

### STATE 1 — Independent fourth review

Dispatch a fresh independent reviewer.

The reviewer must attack, at minimum:

- CWD independence;
- relative path anchoring;
- drive-relative Windows paths;
- relative framework roots;
- UNC paths;
- extended-length paths;
- mapped drives and `subst`;
- trailing dots and spaces;
- NTFS junctions;
- 8.3 short-name aliases;
- ADS and colon-bearing components;
- symlink/junction chains;
- dangling symlinks and loops;
- physical-resolution API failures;
- display-path separation;
- mutation-harness validity;
- actual CI log execution;
- broader clean-main regression baseline.

The reviewer must independently verify:

- exact reviewed head;
- Windows test results;
- Linux symlink results;
- green pristine mutation baseline;
- all 15 mutations;
- exact broader failure node-ID sets;
- campaign safety.

Allowed review verdicts:

- `APPROVE_AND_MERGE`
- `REQUEST_CHANGES`
- `BLOCKED_BY_CI`
- `INCONCLUSIVE`

Do not allow `APPROVE_AFTER_CHANGES`.

Any code change requires a new exact-head review.

### STATE 2 — Review decision

If verdict is `APPROVE_AND_MERGE`, proceed to STATE 7.

If verdict is `REQUEST_CHANGES`, proceed to STATE 3.

If verdict is `BLOCKED_BY_CI` or `INCONCLUSIVE`, attempt only evidence or
environment resolution that does not alter production behavior.

If resolution requires code changes, classify it as `REQUEST_CHANGES` and
proceed to STATE 3.

If the evidence cannot be obtained, stop and report the exact blocker.

### STATE 3 — Narrow remediation planning

Extract only the concrete blockers from the latest review.

Produce a remediation plan containing:

- reproduced defect;
- root cause;
- affected production boundary;
- exact tests that should fail before the fix;
- intended implementation;
- mutation that should be killed;
- campaign-safety constraints.

Do not reopen previously resolved design questions unless a regression directly
invalidates them.

Do not broaden scope into unrelated cleanup.

### STATE 4 — Reproduce before editing

On the exact rejected head:

- reproduce every reported bypass;
- verify real physical aliasing where applicable with `samefile` or an
  appropriate filesystem identity API;
- reproduce test-baseline or CI-evidence defects;
- reproduce surviving mutations.

Record before-state evidence.

Do not implement until reproduction is complete.

If a reported defect cannot be reproduced, dispatch a second independent
reproducer.

If neither can reproduce it, stop with `REPRODUCTION_CONFLICT`.

### STATE 5 — Implement remediation

Implement only the latest confirmed blockers.

Preserve:

- framework-root anchoring;
- physical identity authority;
- shared canonical parser;
- ambiguity floor;
- registry-backed capability issuance;
- atomic single consumption;
- copy/deepcopy/pickle rejection;
- provider-boundary re-derivation;
- both production provider gates;
- zero real model invocation;
- campaign safety.

Add targeted regression tests.

Add or strengthen mutation tests corresponding to the defect.

Do not weaken a guard to make fixtures pass.

Fix the content or implementation instead.

### STATE 6 — Remediation verification

Require all of the following before requesting another review:

1. Exact bypasses fail after the fix.
2. Positive exactly-one fake invocation passes.
3. All denied paths keep both provider counts at zero.
4. Focused pristine baseline is green.
5. Mutation harness explicitly prints and verifies a green baseline.
6. No-op mutation is rejected as not applied.
7. Syntax-error mutation is not counted as a semantic kill.
8. Every intended mutation has specific expected failing tests.
9. Windows Gate A CI passes.
10. Linux Gate A CI passes.
11. Linux symlink tests execute with zero relevant skips.
12. Repository validation passes.
13. Broader main-versus-PR failure and error sets are identical.
14. Evidence 0015 and Evidence 0016 remain untouched.
15. No real model invocation occurred.
16. PR body and ADR are updated honestly.
17. PR remains open and unmerged.

Push the remediation to the existing PR branch.

Wait for all CI jobs.

Record the new exact head SHA.

Then return to STATE 1 with a fresh independent reviewer.

## Review-cycle limit

Do not impose an arbitrary fixed number of review cycles.

Continue while each cycle produces a narrower, reproducible blocker and the
owner's safety constraints remain intact.

However, stop for owner input if any of these occurs:

- two consecutive reviews disagree about the same reproduced fact;
- remediation requires changing the approved product contract;
- remediation would broaden Gate A to ordinary non-campaign workflows;
- remediation requires cryptographic identity infrastructure not present in the
  contract;
- the same defect class reappears after two distinct redesigns;
- reliable Windows or Linux execution evidence cannot be obtained;
- the PR exceeds a maintainability threshold that suggests splitting it;
- a reviewer concludes the architecture should be replaced rather than patched.

Use stop code:

`OWNER_ARCHITECTURAL_DECISION_REQUIRED`

and provide the smallest possible decision question.

### STATE 7 — Merge gate

Merge only when a fresh independent review returns `APPROVE_AND_MERGE` on the
exact current head and confirms:

- all production provider paths are gated;
- controlled Stage 1 cannot classify ordinary;
- filesystem aliases cannot bypass containment;
- relative paths never depend on CWD;
- capabilities permit at most one invocation;
- pristine test baselines are green;
- mutation results are non-vacuous;
- CI logs prove execution;
- broader regressions are neutral;
- documentation is truthful;
- campaign safety is intact.

Before merging, re-fetch the PR.

If the head changed after review, restart STATE 1.

Merge using repository convention.

Record:

- reviewed head SHA;
- merge commit SHA;
- resulting main SHA;
- issue #108 state;
- closing references;
- final CI state.

### STATE 8 — Post-merge verification

From a fresh clone of resulting main:

- rerun focused Gate A tests;
- rerun repository validation;
- verify the consumer remains wired to both provider paths;
- verify no authorization artifacts appeared;
- verify no Evidence 0016 output appeared;
- verify no real model ran;
- verify package remains `PREPARED_NOT_RUN`;
- verify authorization remains `NOT_AUTHORIZED`;
- verify package remains non-runnable;
- verify execution SHA remains pending;
- verify readiness remains `Externally exercised`.

If post-merge verification fails, open a focused regression issue and stop.

Do not silently patch main.

### STATE 9 — Prepare execution-pin finalization task

After successful post-merge verification, prepare—but do not execute—the next
task:

`Finalize the immutable Stage 1 execution-framework pin`

The task must:

- select the canonical resulting main SHA containing the merged consumer;
- update only the authorized preparation and run-control contract locations;
- avoid self-referential commits;
- avoid creating authorization or approval artifacts;
- keep Stage 1 unauthorized;
- keep Evidence 0016 unused;
- receive independent review before merge.

Do not perform pin finalization automatically unless the owner has explicitly
authorized this state in advance.

Default behavior: produce the exact next prompt and stop.

## Reporting behavior

Do not send a message after every trivial command.

Report only at these checkpoints:

- live state established;
- review verdict;
- remediation pushed;
- CI completed;
- merge completed;
- post-merge verification completed;
- owner decision required;
- campaign stopped.

Each checkpoint report must include:

- current state;
- exact head/main SHA;
- what was proven;
- what remains;
- whether any real provider was invoked;
- whether Evidence 0016 or authorization artifacts exist;
- next automatic state.

## Final completion condition

The orchestration task is complete only when one of these is true:

### Completion A — Consumer merged safely

- PR #109 merged after exact-head independent approval;
- post-merge tests pass;
- issue #108 resolved appropriately;
- package remains `PREPARED_NOT_RUN`;
- authorization remains `NOT_AUTHORIZED`;
- execution pin remains pending;
- next pin-finalization prompt produced.

### Completion B — Owner decision required

- a product or architecture decision cannot safely be inferred;
- exact options and consequences are reported;
- no unsafe automatic action occurred.

### Completion C — Evidence unavailable

- required platform or CI evidence cannot be obtained;
- merge did not occur;
- exact missing evidence is reported.

Never treat exhaustion, time pressure, or repeated review cycles as permission
to lower the merge standard.
