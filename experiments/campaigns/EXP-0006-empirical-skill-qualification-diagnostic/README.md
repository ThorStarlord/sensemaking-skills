# EXP-0006 — Empirical Skill Qualification diagnostic stage

**STATUS: PREPARATION ONLY. NOT OPERATIVE. NOT APPROVED. NOT EXECUTED.**

EXP-0006 is the first authorization stage of `experiments/empirical-skill-qualification-v1/`. It is tracked by Issue #274 and prepared on draft PR #273. It authorizes only repeated baseline diagnostic evidence for one frozen D case. It does not authorize a candidate Skill, held-out Q/T execution, automatic adoption, or merge.

## Why qualification is not pre-authorized here

Two-Lane v1 configuration identity binds the exact `framework_sha` and `prompt_or_skill_revision`. A candidate does not exist before the diagnostic/maintenance stage, so its exact identity cannot be allowlisted honestly in this immutable campaign. Changing the policy or configuration after approval would change their digests and require new approval.

Therefore:

1. EXP-0006 may produce baseline D evidence only.
2. After all D evidence is preserved, a fresh holdout-custodian context freezes exact Q/T cases under `experiments/empirical-skill-qualification-v1/HOLDOUT-PROTOCOL.md` before candidate generation.
3. This candidate-author context then analyzes only D using `usage-researcher` and `skill-maintainer` responsibilities and freezes either one bounded candidate or `NO_SKILL_CHANGE`.
4. If a candidate exists, Q/T baseline-vs-candidate execution is prepared under a fresh campaign authorization whose exact configuration identities are knowable at that time.
5. No approval transfers between stages.

This staged design is a governance consequence, not a relaxation of the experiment.

## Frozen intended identity

- Campaign: `EXP-0006-empirical-skill-qualification-diagnostic`
- Framework SHA: `969e8eb47144ffdeb27a8d9df02b6a292586e842`
- `repo-sensemaker` revision: `969e8eb47144ffdeb27a8d9df02b6a292586e842`
- Validator revision: `969e8eb47144ffdeb27a8d9df02b6a292586e842`
- Execution mode: `coding_agent_native`
- Execution surface / model identifier: `github_connector`
- Durability backend: `github_results_branch_v1`
- Validation backend: `github_actions_exact_head`
- Invocation boundary: `before_first_experiment_scoped_target_read`
- Target access: `github_connector_read_only`
- Probe backend: `github_connector_exact_sha_v1`
- Approval reference kind: `agent_recorded_github_issue_comment`
- Approval audit issue: #274
- Target repository: `https://github.com/ThorStarlord/auteur.git`
- Target SHA: `0653defb05625f2fcde0ac32eac6e59ccf7eeb90`
- Diagnostic case: `D-001`, exact intent frozen in `configuration-identity.yaml` and `scientific-questions.md`
- Artifact type: `repository_sensemaking_brief`
- Attempts: 3 identical attempts
- Concurrency: 1
- Classification: `EXPLORATORY_NOT_CANONICAL_EVIDENCE`
- External provider API: prohibited
- Target mutation: prohibited
- Fallback: prohibited
- Repair/hidden retry: prohibited
- Candidate execution: prohibited
- Holdout access from candidate-author context: prohibited
- Automatic merge: prohibited
- Validity window: `2026-09-04T21:50:00Z` through `2026-09-11T23:59:59Z`

The `configuration_id` and `policy_digest` are not considered frozen until GitHub Actions' canonical Two-Lane digest implementation has reproduced them exactly and the preparation suite is green.

## Diagnostic execution contract

Only after the final frozen envelope is presented in the active conversation and the human replies with a standalone `approve` may the campaign become operative. The future approval event is recorded on Issue #274 solely as an agent-authored durable audit locator; the conversation remains the authorization authority.

Each of the three attempts must:

1. durably reserve a slot before experiment-scoped target access;
2. durably record `INVOKED` immediately before the first exact-SHA target read;
3. use the identical D-001 user intent and pinned baseline Skill;
4. access only the exact read-only Auteur snapshot;
5. preserve raw request, raw output, produced brief, and state before validation;
6. bind deterministic validation to the exact preserved head;
7. record the terminal result without repair, selection, or hidden retry.

All three attempts remain in the analysis regardless of quality.

## Post-D gate

EXP-0006 ends at a diagnostic evidence boundary. It does **not** itself create or execute a candidate.

After three terminal attempts:

- compare expected vs actual behavior with `usage-researcher`;
- attribute any defect before proposing an edit;
- use `skill-maintainer` only on evidence-supported Skill defects;
- permit `NO_SKILL_CHANGE` as a successful outcome;
- before any candidate text is authored, require a fresh holdout-custodian context to freeze exact Q/T cases and commit their manifest/digest without exposing their substantive content to the candidate-author context;
- if one bounded candidate is then frozen, its exact SHA/digest becomes input to a new qualification authorization envelope.

## Candidate budget inherited from v1

- max target Skills: 1
- max modified files: 1 (`skills/repo-sensemaker/SKILL.md`)
- max instruction regions: 2
- full Skill rewrite: prohibited
- registry change: prohibited
- artifact-contract change: prohibited
- validator change: prohibited
- workflow change: prohibited
- automatic adoption/merge: prohibited

If the evidence requires more than this, stop; do not widen the candidate to make the experiment succeed.

## Claim boundary

EXP-0006 can establish only baseline behavior and whether D supplies an evidence-attributable warrant for one bounded candidate. It cannot establish that Empirical Skill Qualification works, that a candidate improves the Skill, that Q/T would generalize, or that any Skill edit should be promoted.

Stop marker after preparation: `EXP_0006_PREPARATION_READY_FOR_ENVELOPE`.
Stop marker after authorized D execution: `EXP_0006_D_RESULTS_READY_FOR_HOLDOUT_FREEZE`.
