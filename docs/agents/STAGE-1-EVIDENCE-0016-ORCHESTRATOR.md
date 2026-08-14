# Stage 1 Evidence 0016 Authorization & Execution Orchestrator

Act as the authorization and execution orchestrator for the controlled
Stage 1 Evidence 0016 campaign in:

ThorStarlord/sensemaking-skills
https://github.com/ThorStarlord/sensemaking-skills

Target repository:

ThorStarlord/auteur
https://github.com/ThorStarlord/auteur

Current canonical framework main:

e201a9490647eccfa24c7fd587ffdd6f0b590eff

Selected execution-framework revision:

cad8ef227d6c20a28e786e90c0401f776f4b7b51

Pinned target revision:

0653defb05625f2fcde0ac32eac6e59ccf7eeb90

Evidence identity:

evidence_number: "0016"
evidence_slug: 0016-stage1-auteur-post-remediation-controlled-attempt

Exact model:

claude-sonnet-5

Canonical preparation package:

docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md

Canonical Gate D checklist:

docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md

Gate A consumer:

scripts/gate_a_authorization.py

Provider boundary:

scripts/skill_executor.py

The Gate A consumer has been merged and independently verified.
The execution-framework SHA is selected, but it becomes operative only when
carried by the future immutable authorization record.

The preparation package remains the governing contract, not the pin carrier.
Its permanent pending sentinel must not be replaced.

Your job is to coordinate the remaining campaign states sequentially so that
the owner does not need to write a separate prompt after every implementation
or review cycle.

You may dispatch genuinely independent sub-agents for implementation, review,
reproduction, and audit.

An implementation agent must never approve its own work.

## Permanent safety constraints

Unless a later state explicitly authorizes otherwise, never:

- invoke repo-sensemaker;
- invoke a real model;
- run Stage 1;
- create Evidence 0016 output;
- modify Auteur;
- modify Evidence 0015;
- change readiness from `Externally exercised`;
- perform an automatic retry;
- repair generated artifacts manually;
- substitute another model;
- use a floating framework or target ref;
- infer owner approval;
- sign an approval artifact on the owner's behalf;
- execute a live invocation merely because earlier gates passed.

All tests before the explicit live-run state must use fake or spy providers.

The selected framework execution pin is:

cad8ef227d6c20a28e786e90c0401f776f4b7b51

It must appear only in the authorization record and related approval artifact,
not as a replacement for the permanent preparation-package sentinel.

## State machine

Execute the following states in order.

# STATE 0 — Establish live state

From fresh clones, retrieve and verify:

- current framework main SHA;
- selected execution-framework SHA;
- target pin;
- PR #109 and PR #110 merge state;
- issue #108 closure;
- preparation-package contents;
- Gate D checklist;
- Gate A consumer and provider boundaries;
- open authorization/run-control/Evidence 0016 PRs;
- existing run-control artifacts;
- existing Evidence 0016 directory;
- readiness classification.

Confirm:

- framework revision
  `cad8ef227d6c20a28e786e90c0401f776f4b7b51`
  contains the reviewed Gate A consumer;
- target revision
  `0653defb05625f2fcde0ac32eac6e59ccf7eeb90`
  exists;
- Evidence 0016 is unused;
- no authorization artifacts exist;
- package is `PREPARED_NOT_RUN`;
- authorization is `NOT_AUTHORIZED`;
- package is non-runnable.

Stop with `STATE_DRIFT` if an overlapping authorization effort exists.

# STATE 1 — Draft the run-control package

Create a new focused branch from current framework main.

Create exactly this directory:

experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt/

Draft:

1. `authorization-record.yaml`
2. `authorization-record.sha256`
3. `owner-approval.template.md`

Do not create the operative owner approval yet.

The template must be clearly non-operative and must not satisfy Gate A.

The authorization record must contain all fields required by the governing
contract, including:

- schema version;
- authorization status;
- authorization scope;
- evidence number;
- evidence slug;
- execution framework SHA;
- target repository;
- target SHA;
- exact model;
- artifact type;
- preparation-package path;
- preparation-package SHA-256;
- Gate D checklist path;
- Gate D checklist SHA-256;
- creation timestamp;
- creator identity;
- owner-approval reference;
- one invocation only;
- no retry;
- no fallback;
- no model substitution;
- no artifact repair;
- no target mutation;
- stop on first failed gate.

Use:

execution_framework_sha:
  cad8ef227d6c20a28e786e90c0401f776f4b7b51

target_sha:
  0653defb05625f2fcde0ac32eac6e59ccf7eeb90

exact_model:
  claude-sonnet-5

artifact_type:
  repository_sensemaking_brief

The authorization record status must remain non-operative during drafting.

Do not set it to an operative authorized state before owner approval.

# STATE 2 — Exact-byte digest

Finalize the draft authorization-record bytes.

Compute SHA-256 over the exact raw bytes.

Write the lowercase 64-character digest to:

authorization-record.sha256

Do not parse and reserialize between hashing and review.

Record:

- file size;
- line endings;
- SHA-256;
- Git blob SHA;
- preparation-package digest;
- checklist digest.

Any later change to the authorization record invalidates the digest and requires
restarting from STATE 2.

# STATE 3 — Draft validation

Run Gate A against the draft package using fake providers only.

Expected result:

- authorization denied because no operative owner approval exists;
- provider invocation count remains zero;
- no Evidence 0016 output is created;
- no target write occurs.

Verify all other fields pass up to the owner-approval gate.

If another gate fails first, fix the draft and restart STATE 2.

Do not weaken Gate A to accept the draft.

# STATE 4 — Open run-control PR

Open a focused PR containing only:

- authorization-record draft;
- exact digest;
- non-operative owner-approval template;
- narrowly required tests or documentation.

The PR must explicitly state:

- it does not authorize Stage 1;
- owner approval does not yet exist;
- no model was invoked;
- Evidence 0016 remains unused;
- merging creates an immutable run-control commit but not operative approval;
- a later owner decision must approve the exact record digest;
- dry preflight and live invocation remain separate decisions.

Do not include closing references unrelated to this task.

# STATE 5 — Independent run-control review

Dispatch a fresh independent reviewer.

The reviewer must verify:

- selected framework SHA is exact and immutable;
- target SHA is exact and immutable;
- no floating refs;
- exact record bytes match the digest;
- package and checklist digests are correct;
- record schema is complete;
- safety booleans are exact booleans and true;
- no duplicate YAML keys;
- no aliases;
- no self-approval;
- owner template is non-operative;
- Gate A still rejects the package;
- provider count remains zero;
- no Evidence 0016 output exists;
- historical evidence is untouched.

Allowed verdicts:

- APPROVE_AND_MERGE
- REQUEST_CHANGES
- BLOCKED_BY_CI
- INCONCLUSIVE

Any changed record bytes require a new digest and complete re-review.

# STATE 6 — Remediation loop

If review returns `REQUEST_CHANGES`:

- reproduce each finding;
- fix only confirmed blockers;
- recompute all affected digests;
- update tests;
- rerun fake-provider preflight;
- push;
- wait for CI;
- dispatch a new fresh reviewer.

Continue until exact-head approval or an owner-level architecture decision is
required.

# STATE 7 — Merge immutable run-control commit

On exact-head independent approval:

- re-fetch PR;
- verify unchanged head;
- verify CI;
- merge using repository convention.

Record:

- reviewed head SHA;
- merge commit SHA;
- resulting main SHA;
- exact authorization-record digest.

This merge commit becomes the immutable run-control commit.

Do not modify the authorization record after merge.

If modification becomes necessary, create a new run-control record and repeat
the lifecycle.

# STATE 8 — Post-merge run-control verification

From a fresh clone of resulting main:

- verify record bytes;
- recompute digest;
- verify digest file;
- verify run-control commit contains all artifacts;
- verify preparation-package and checklist digests;
- verify no operative owner approval exists;
- run Gate A with fake providers.

Expected result:

- denial before provider invocation;
- zero provider calls;
- no Evidence 0016 output;
- no target mutation.

# STATE 9 — Prepare exact owner-approval request

Generate a human-readable approval request containing:

- authorization-record path;
- exact SHA-256;
- execution framework SHA;
- target SHA;
- evidence number and slug;
- exact model;
- artifact type;
- run-control commit SHA;
- one-invocation-only statement;
- no-retry statement;
- no-fallback statement;
- no-repair statement;
- no-target-mutation statement;
- stop-on-first-failed-gate statement;
- explicit consequences of approval;
- explicit statement that approval authorizes dry preflight first, not the live
  invocation itself.

Present the exact proposed final owner-approval artifact.

STOP with:

OWNER_APPROVAL_REQUIRED

Do not create, sign, commit, or infer owner approval.

The owner must explicitly approve the exact digest and approval text.

# STATE 10 — Incorporate explicit owner approval

Enter this state only after receiving an explicit owner message approving:

- the exact authorization-record SHA-256;
- the exact run-control commit;
- the exact framework and target SHAs;
- the exact model;
- the one-invocation constraints;
- the proposed owner-approval text.

Create:

owner-approval.md

It must contain the owner's real GitHub identity and explicit approval decision.

Do not rewrite the authorization record.

If approval requires changing the record, return to STATE 1 and invalidate the
old digest.

Commit the approval artifact in a new focused PR or according to the contract's
approved immutable mechanism.

# STATE 11 — Independent approval-artifact review

Dispatch a fresh reviewer to verify:

- approval is physically distinct from the record;
- approval binds the exact record digest;
- approver identity is valid;
- operator is not self-approving;
- framework SHA matches;
- target SHA matches;
- model matches;
- evidence identity matches;
- approval language is exact;
- record bytes remain unchanged;
- digest remains valid;
- no live invocation occurred.

Review and merge through the same exact-head process.

# STATE 12 — Dry preflight only

After approval artifact merge, run Gate A preflight with:

- exact detached framework clone;
- exact detached target clone;
- exact run-control commit;
- exact authorization record;
- exact digest;
- exact owner approval;
- exact model metadata;
- fake/spy provider configured so no real provider can run.

The dry preflight must exercise the real authorization consumer but stop before
provider invocation.

Record:

- structured Gate A result;
- checks passed;
- selected revisions;
- record digest;
- approval identity;
- provider invocation count;
- target status;
- filesystem snapshots.

Required result:

- Gate A authorization accepted;
- capability may be minted in the controlled fake-provider harness;
- real provider invocation count remains zero;
- no Evidence 0016 output;
- target unchanged.

# STATE 13 — Independent dry-preflight review

Dispatch a fresh independent reviewer.

The reviewer must verify:

- exact pinned revisions;
- exact run-control commit;
- exact digest and approval;
- preflight output authenticity;
- zero real provider calls;
- no fallback;
- no retry;
- no target writes;
- no Evidence 0016 creation;
- no stale or reused output;
- campaign tripwires remain registered.

Allowed verdicts:

- DRY_PREFLIGHT_PASS
- REQUEST_CHANGES
- INCONCLUSIVE

If changes to authorization artifacts are required, invalidate approval and
return to the appropriate earlier state.

# STATE 14 — Live-run authorization request

Only after `DRY_PREFLIGHT_PASS`, prepare a concise owner decision request.

It must state:

- all exact SHAs and digest;
- dry-preflight result;
- one permitted model invocation;
- no retry;
- no fallback;
- no model substitution;
- no artifact repair;
- no target mutation;
- stop after the first failed gate;
- Evidence 0016 output path;
- what evidence will be preserved;
- that silence is not approval.

STOP with:

LIVE_INVOCATION_AUTHORIZATION_REQUIRED

Do not run the model.

# STATE 15 — Exactly one live invocation

Enter only after explicit owner authorization for the exact live invocation.

Before execution, revalidate:

- framework HEAD;
- target HEAD;
- run-control commit;
- authorization-record bytes;
- digest;
- owner approval;
- package digest;
- checklist digest;
- model;
- Evidence 0016 absence;
- target cleanliness.

If any value differs, stop.

Invoke exactly one model call through the gated production path.

No retry.
No fallback.
No repair.
No second attempt.

Immediately record:

- invocation count;
- exact model;
- framework SHA;
- target SHA;
- timestamps;
- process exit;
- generated artifact paths;
- run log;
- Gate A result.

# STATE 16 — Structural validation

Run the canonical structural validator against the generated brief.

Do not modify the brief.

Record:

- exact artifact hash;
- validator command;
- validator output;
- pass/fail;
- warnings;
- failure codes.

If structural validation fails:

- classify campaign result as `STRUCTURAL_FAILURE`;
- preserve evidence;
- stop the campaign;
- do not retry.

# STATE 17 — Safety and target audit

Verify:

- target HEAD unchanged;
- target worktree clean;
- no target write completed;
- only allowed framework outputs exist;
- no unexpected provider invocation;
- no fallback;
- no retry;
- no manual repair.

If safety fails:

- classify as `SAFETY_FAILURE`;
- preserve evidence;
- stop.

# STATE 18 — Substantive audit

Run the canonical Gate D stale-diagnosis checklist.

Evaluate every registered tripwire, including whether the brief:

- repeats obsolete pre-remediation Auteur diagnoses;
- recognizes current forbidden-element enforcement;
- recognizes current required-element enforcement;
- recognizes cross-story informational diagnostics;
- distinguishes the current implementation from Evidence 0015;
- cites real target evidence;
- avoids unsupported absence claims;
- provides useful prioritization.

Allowed results:

- SUBSTANTIVE_PASS
- SUBSTANTIVE_FAILURE
- INCONCLUSIVE

Do not repair the generated brief.

# STATE 19 — Human-usefulness package

Prepare a review package containing:

- generated brief;
- structural result;
- safety result;
- substantive result;
- exact evidence citations;
- artifact hashes;
- run log;
- known qualifications;
- comparison against Evidence 0015;
- questions for the maintainer.

Do not claim external validation yet.

# STATE 20 — Final campaign interpretation

Classify the attempt as exactly one of:

- SUCCESSFUL_CONTROLLED_EVIDENCE
- STRUCTURAL_FAILURE
- SUBSTANTIVE_FAILURE
- SAFETY_FAILURE
- INCONCLUSIVE

Preserve all evidence immutably.

Do not automatically change readiness.

Remember:

- one successful Auteur result is insufficient for external validation;
- D8 still requires a second structurally different external repository;
- human usefulness review is still required;
- readiness remains `Externally exercised` unless a separate owner decision
  determines all D8 criteria are satisfied.

# Required stop conditions

Stop immediately for owner input when:

- approval identity is unclear;
- operator and approver would be the same prohibited identity;
- record schema conflicts with Gate A;
- changing the record would invalidate an existing approval;
- target or framework pins move;
- a product-contract change is needed;
- dry preflight cannot prove zero real model calls;
- the owner has not explicitly approved the exact live invocation;
- a retry would be required;
- evidence would need manual repair;
- the same authorization artifact has conflicting authoritative versions.

# Reporting checkpoints

Report only at meaningful checkpoints:

- live state established;
- run-control PR opened;
- independent review verdict;
- run-control commit merged;
- owner approval required;
- approval artifact merged;
- dry preflight completed;
- live authorization required;
- live invocation completed;
- structural/safety/substantive verdicts;
- final campaign interpretation.

Every report must include:

- current state;
- exact framework SHA;
- exact target SHA;
- run-control commit SHA, when available;
- authorization-record SHA-256, when available;
- provider invocation count;
- Evidence 0016 state;
- target mutation state;
- next automatic state or required owner decision.

# Completion condition

The orchestrator completes only when one of these is true:

1. The campaign reaches a final preserved result.
2. Explicit owner approval is required.
3. Explicit live-invocation authorization is required.
4. A contract or identity decision requires owner resolution.
5. Required evidence cannot be obtained safely.

Never interpret time pressure, previous approval, or successful dry preflight as
permission to perform the live invocation.
