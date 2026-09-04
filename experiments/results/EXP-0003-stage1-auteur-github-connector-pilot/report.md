# EXP-0003 campaign report — pre-invocation control-plane failure

**Campaign:** `EXP-0003-stage1-auteur-github-connector-pilot`  
**Classification:** `EXPLORATORY_NOT_CANONICAL_EVIDENCE`  
**Disposition:** `CONCLUDED_PRE_INVOCATION — approved envelope not executable as specified`  
**Policy digest:** `710478c4acf5217a9177ba7cfdca3623929c5f0cbf219d4a407b8e4c28533f2a`

## Executive result

The standalone human approval was received and durably recorded, and the draft results PR existed before attempt 1. The campaign then failed closed during pre-attempt control-plane validation. No attempt was `RESERVED`, no attempt crossed `INVOKED`, and the executor performed no experiment-scoped read of the Auteur target.

This does **not** falsify connector-native GitHub durability in principle. It shows that the exact approved EXP-0003 envelope cannot execute under its own frozen preparation/validation and skill requirements without an unapproved repair.

## Finding 1 — preparation validation contradicts the required results lifecycle

Phase-A research design requires, before attempt 1, an isolated results branch, a campaign state document, a draft results PR, and validation of that empty campaign state. It later requires exact-head validation of the head containing `OUTPUT_CAPTURED` plus the artifact.

However, the integrated Phase-B preparation test `tests/campaign_validation/test_exp0003_preparation.py::test_exp0003_preparation_contains_no_execution_state` asserts that `experiments/results/EXP-0003-stage1-auteur-github-connector-pilot` does not exist at all.

Observed GitHub Actions evidence:

- Validator Ecosystem run #467 (`32143843398`) on approval head `b0838e211686a3b300f1ce8639bb0c3105f07669` failed both Phase-2 campaign-validation lanes because `approval.md` had initially been placed in the immutable preparation package. The receipt was moved pre-invocation into the results namespace and the preparation package was restored exactly.
- Validator Ecosystem run #469 (`32143999970`) on corrected head `e77d51e4201f3c784d8b7af03d7b85232d2235f1` still failed both Phase-2 campaign-validation lanes because the test rejects the existence of the EXP-0003 results directory itself.
- The dedicated Phase-3 exploratory-authorization jobs passed; the blocking failure is the lifecycle contradiction in the preparation test, not a rejected human approval.

Therefore any real EXP-0003 results state necessarily makes the exact-head validation matrix red. Continuing would require changing or bypassing a frozen validation condition, which would be an in-place repair.

## Finding 2 — pinned repo-sensemaker requires a local probe incompatible with target-access mode

The frozen configuration declares `target_access_mode: github_connector_read_only` and pins `prompt_or_skill_revision` to framework SHA `5704a2614222cd1705e0bf7e5174d1418c5d6240`.

At that exact revision, `skills/repo-sensemaker/SKILL.md` states that the Probe Engine is mandatory before synthesis and instructs execution of:

`python scripts/probe-repo.py --repo-root <target-repo> ...`

against a checked-out target repository. This connected workspace has no authorized local checkout/execution surface for the target under the approved configuration. Introducing a GitHub-hosted probe adapter, changing the skill requirement, or using a local executor would change the approved execution contract.

## Accounting

- Approval: recorded.
- Results branch: `experiment/exp-0003-results`.
- Draft results PR: #194.
- Attempt slots authorized: 3.
- Attempt slots reserved: 0.
- Invocations: 0.
- Target mutation: none.
- Experiment-scoped target reads by this executor: 0.
- Hidden retry/repair: none.
- Automatic merge: none.

No canonical attempt-state document was created because the campaign stopped before the first `RESERVED` transition.

## Research interpretation

The current approved envelope is **unsupported/inconclusive as an executable campaign**. The failure happened before the experiment could answer its target-level reproducibility questions, but it produced two actionable control-plane findings:

1. preparation-only assertions must be lifecycle-scoped so real results heads can be exact-head validated;
2. a connector-native campaign needs a deterministic current-state probe that is compatible with connector-only target access, or the skill/configuration contract must explicitly choose another authorized probe surface.

A successor must use a new framework revision, recompute configuration/policy identities, and obtain a new standalone human approval. This EXP-0003 approval must not be reused, and EXP-0003 must not be silently repaired or retried in place.
