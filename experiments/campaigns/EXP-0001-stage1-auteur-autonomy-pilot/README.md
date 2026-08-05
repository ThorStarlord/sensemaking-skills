# EXP-0001-stage1-auteur-autonomy-pilot — preparation package (Phase 5 revision, Issue #121/#122)

**STATUS: PREPARATION ONLY. NOT OPERATIVE. NOT APPROVED. NOT EXECUTED.**

This directory is a *proposal package*. It contains the policy,
configuration, digest, and review materials for the first exploratory
campaign under the two-lane program (ADR 0023, Issues #116/#121). It
contains **no human approval, no reservation, no ledger, no raw output, no
attempt result, and no provider call**, and it cannot produce any of those
through the normal runtime until a genuine human approval exists for the
exact policy digest below.

## Pinned values

| Input | Value |
|---|---|
| `campaign_id` | `EXP-0001-stage1-auteur-autonomy-pilot` |
| Framework repository | `ThorStarlord/sensemaking-skills` |
| Framework SHA | `9c01ccd45267058d5f7b4dd5a04fc77bd17efdfa` |
| Target repository | `ThorStarlord/auteur` (`https://github.com/ThorStarlord/auteur.git`) |
| Target SHA | `0653defb05625f2fcde0ac32eac6e59ccf7eeb90` |
| Model | `claude-sonnet-5` |
| Artifact type | `repository_sensemaking_brief` |
| Configurations | exactly 1 (see `configuration-identity.yaml`) |
| `configuration_id` | `9ddb3e0cdbc8cc137ecf42c4d44641b9084ce5d98b2a8fdc2e43785c62119abd` |
| Attempts | 3 (`max_attempt_slots=3`, `max_attempts_per_configuration=3`, `max_provider_invocations=3`) |
| Concurrency | 1 (`concurrency_ceiling=1`) |
| Classification | `EXPLORATORY_NOT_CANONICAL_EVIDENCE` |
| Prohibitions | fallback, hidden retry, target mutation, automatic repair, automatic merge (all `*_prohibited: true`) |
| `policy_digest` | `ef0f79ca831d127bc0ac0af264d6d37209b6310acffcb336ca021aafb332db03` (see `campaign-policy.sha256`) |

The configuration pins `prompt_or_skill_revision` and
`validator_revision` to the framework SHA: the `repo-sensemaker` skill and
the validator stack ship inside the framework repository, so the framework
commit is the exact revision of both.

## Validity window: the frozen interpretation

Issue #121 requires a **seven-day validity window after genuine approval**,
and the program requires **byte-exact policy + digest** that a human
approves *after* the package is reviewed and merged. The two-lane v1 schema
(ADR 0023 §9a, `campaign-policy.schema.md`) supports only **absolute**
`validity_window.not_before`/`not_after` timestamps — there is no
relative-duration field.

Resolution chosen for this package (**Resolution A, with a governed §9c
fallback; Resolution C rejected**):

1. **Frozen absolute window** (part of the approved bytes):

   ```text
   not_before: 2026-08-18T00:00:00+00:00
   not_after:  2026-08-25T00:00:00+00:00   (exactly 7 days later)
   ```

2. **Approval protocol**: the genuine human approval must be recorded
   against this exact `policy_digest` *before* `not_before` whenever the
   full seven days are required. The window is exactly seven days long;
   residual validity after approval is `not_after - max(not_before,
   approval_time)`, so an approval inside the window but after
   `not_before` yields less than seven full days.

3. **Governed fallback (§9c, not an edit in place)**: if approval cannot be
   recorded inside the window, the policy must be revised (new
   `not_before`/`not_after` → new `policy_digest`) and the human must
   approve the new digest. The prior digest stays on record but no longer
   authorizes anything. This is the same path any policy revision takes;
   Phase 5 does not invent a second approval mechanism.

4. **Resolution C (relative `duration_after_approval`) is rejected**: the
   v1 schema has no such field, and inventing one would violate the
   fail-closed schema contract. A future schema revision may add it
   through the normal ADR process, not inside this package.

The window is deliberately anchored AFTER the original August 7-14
window expired (Phase 6 correction): the first window belonged to a
preparation whose execution infrastructure was retired by the PR #129
review (`PR_129_REQUEST_CHANGES`). The corrected, framework-governed
execution boundary (merged at the pinned `framework_sha`) supersedes it;
the new window is anchored with a review buffer so a prompt approval
yields the full seven-day campaign window from `not_before`.

## What makes this package non-operative

- `approval-template.yaml` is a **form, not an approval**. It carries the
  marker `EXAMPLE_ONLY_NOT_AUTHORIZATION` and empty/unfilled fields; the
  Phase 2 validator rejects it
  (`CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE`) and the Phase 3
  issuer additionally rejects any approval carrying a `marker`. No value
  in it resembles a real human decision.
- No operative `campaign-approval` record exists anywhere.
- Without a valid approval, `validate_campaign_bundle` cannot succeed, so
  no `ValidatedCampaignBundle` can be produced, so no capability can be
  minted, no attempt can be reserved, and the provider boundary can never
  be reached (Phase 3 + Phase 4 chain).
- `tests/campaign_preparation/` proves all of the above and proves that no
  runtime state can be created from this package.

## Runtime state that must NOT exist here

At the end of Phase 5 (and after every test in
`tests/campaign_preparation/`), this directory contains only:

```text
campaign-policy.yaml
campaign-policy.sha256
configuration-identity.yaml
approval-template.yaml
scientific-questions.md
README.md
```

It must NOT contain: `ledger.jsonl`, `ledger.lock`, `attempts/`,
`reservation.yaml`, `request-metadata.json`, `raw-output.*`,
`produced-artifact.*`, `validation-result.json`, `attempt-result.yaml`, or
`campaign-summary.yaml`.

## Verification

```bash
python -m pytest tests/campaign_preparation -q
```

The suite re-validates the written files with the real Phase 2 validators,
recomputes both digests, checks every pinned value, proves the approval
template is non-operative, proves drift on any pinned field is detected,
and proves no execution residue exists.

## The human approval step (separate, later, not part of Phase 5)

This package binds the GitHub issue-comment approval mechanism (Lane A
beta, Model B -- ADR 0023 section 21): `approval-template.yaml` names
`approval_provenance.mechanism: github_issue_comment_approval`, and the
operative approval is transcribed from the human's comment on Issue #122
by `scripts/execution_infra/capture_github_approval.py` (mechanical
transcription, never agent-authored consent).

1. This preparation PR is reviewed and merged (the merged `policy_digest`
   below is the digest the human must approve).
2. The human posts ONE approval comment on Issue #122 with the exact
   grammar (`capture_github_approval.py --help` prints it), binding this
   exact `policy_digest`, with `expires_at` inside the validity window.
   The agent never posts the comment.
3. The operator runs `capture_github_approval.py`, which transcribes the
   verified comment into the operative `approval.yaml` in this directory.
4. The runner re-verifies the comment against the live GitHub API before
   the run and before every attempt (comment exists, author is the
   designated maintainer with admin permission, body digest unchanged,
   limits inside the policy envelope).
5. Only then may Phase 6 execute the campaign -- and Phase 6 is a
   separate, future task.

Stop marker for Phase 5: `EXP_0001_PREPARATION_PR_READY_FOR_REVIEW` -- the
package is ready to inspect, not ready to run.
