# Holdout protocol — Empirical Skill Qualification v1

**Status:** PRE-REGISTERED PROCEDURE; NO Q/T CASES HAVE BEEN CONSTRUCTED OR OPENED IN THE CANDIDATE-AUTHOR CONTEXT.

This protocol preserves the core D/Q/T separation without pretending this conversation can spawn a genuinely fresh evaluator context. It creates a hard process boundary between the context that diagnoses/authors a candidate (Context A) and the context that constructs and later evaluates held-out cases (Context B).

## Roles

### Context A — diagnostic / candidate author

Context A may read:

- the v1 protocol;
- EXP-0006 and all D evidence;
- `usage_research_report`;
- `skill_improvement_plan`;
- the baseline Skill;
- the bounded candidate it authors.

Context A MUST NOT read, fetch, search, quote, summarize, or otherwise inspect substantive Q/T case content before candidate freeze. After holdout construction it may know only:

- the holdout manifest commit SHA;
- the manifest digest;
- counts by split;
- the pre-registered case-family quotas below;
- whether the holdout integrity checks passed.

Accidental substantive Q/T exposure to Context A before candidate freeze invalidates that candidate cycle. Stop; do not silently regenerate cases.

### Context B — holdout custodian / blind qualifier

Context B must be a fresh conversation that does not receive:

- D outputs;
- `usage_research_report`;
- `skill_improvement_plan`;
- candidate rationale;
- candidate predicted wins/losses;
- baseline/candidate A/B assignment identity.

Before candidate generation begins, Context B receives only this protocol, the frozen baseline identity, the D case definition (not D outputs), and repository access needed to construct Q/T. It constructs and commits exact Q/T cases, computes the manifest digest, and reports only the commit SHA, digest, split counts, and integrity status back to Context A.

After a candidate is frozen, Context B may later act as blind qualifier using case + Variant A + Variant B packets. The A/B assignment map remains separate until each judgment is committed.

## Freeze order

1. EXP-0006 runs D and preserves all three baseline attempts.
2. Context A stops at `EXP_0006_D_RESULTS_READY_FOR_HOLDOUT_FREEZE`; it does not run `skill-maintainer` to candidate text yet.
3. Open fresh Context B.
4. Context B constructs the exact Q/T corpus under the rules below.
5. Context B validates the manifest with `sensemaking_skills.skill_qualification.validate_case_manifest` at the research scaffold revision.
6. Context B computes the canonical stable manifest digest with `manifest_digest` and commits the exact manifest on a dedicated holdout branch or other immutable GitHub commit.
7. Context B returns only commit SHA, manifest digest, Q count, T count, and PASS/FAIL integrity status to Context A.
8. Only after those values are durably recorded may Context A perform D-only `usage-researcher` / `skill-maintainer` reasoning and author one candidate or `NO_SKILL_CHANGE`.
9. Candidate freeze records exact baseline SHA/digest, candidate SHA/digest, patch, source findings, predicted benefit, and predicted regression risks. No candidate edits after Q begins; any edit creates a new candidate identity and invalidates prior comparison results.

## Corpus size

V1 freezes:

- D: the single diagnostic case D-001 with three repeated baseline attempts under EXP-0006;
- Q: 8 distinct held-out cases;
- T: 8 distinct untouched cases.

The D attempt repetitions measure baseline execution variability; Q/T cases test behavioral breadth and generalization. Repetitions are not counted as distinct held-out cases.

## Held-out case families

Context B must construct Q and T so each split contains exactly two cases from each family:

1. **Intent-vs-repository-fog conflict** — the user's implied problem and the repository's strongest evidence point toward different fog/uncertainty; the Skill should surface the conflict rather than simply echo the user.
2. **Correct-negative / authority boundary** — the prompt tempts implementation, routing certainty, or another unauthorized commitment; a good brief diagnoses and recommends without converting a finding into authority to act.
3. **State-currency / evidence hierarchy** — historical status prose, stale self-reporting, or documentary claims could conflict with stronger current executable/exact-SHA evidence; the brief must preserve evidence category and uncertainty rather than treating all sources as equally current.
4. **Workflow-vs-Skill recommendation boundary** — the repository contains plausible Skill names, workflow IDs, or neighboring mechanisms that could be confused; any `recommended_workflow_id` must remain registry-grounded and the analysis must not fabricate routing authority.

The family labels and quotas are visible to Context A. The substantive repositories, intents, traps, evidence expectations, and rubrics are not.

## Target selection constraints

For Q and T:

- use repositories readable through the approved GitHub connector;
- pin every target to an exact 40-character commit SHA before execution;
- use public repositories only for this v1 holdout so no private repository identity or content is exposed by the public research record;
- use at least four distinct repositories across Q+T;
- T must include at least two repositories not used in Q;
- do not use `ThorStarlord/sensemaking-skills` as a Q/T target because Context A has extensive prior knowledge of it;
- do not use the D snapshot `ThorStarlord/auteur@0653defb05625f2fcde0ac32eac6e59ccf7eeb90` in T;
- at most two Q cases may use Auteur, and if they do they must use an exact snapshot and intent distinct from D-001;
- do not select a target because it is known to make a proposed candidate look good or bad; Context B does not know the candidate when cases are frozen.

## Case contract

Every Q/T case must record all fields required by the v1 manifest validator:

- `case_id`;
- `target_repository`;
- `target_sha`;
- `user_intent`;
- `authorized_access_surface`;
- `expected_mechanical_properties`;
- `decision_quality_rubric`;
- `forbidden_assumptions`;
- `expected_boundary_behavior`.

Context B may additionally record case family, expected evidence anchors/non-evidence, known traps, and notes for the blind evaluator. Those additions remain hidden from Context A until the candidate cycle is terminal.

## Split isolation

- Q may be opened for execution only after candidate freeze.
- T may not be opened for execution or evaluation unless Q disposition is exactly `IMPROVED`.
- If Q is `EQUIVALENT`, `MIXED`, `REGRESSED`, or `INCONCLUSIVE`, stop without opening T.
- No Q result may be used to edit the candidate. A post-Q edit is a new candidate and requires a new independently frozen qualification cycle.

## Execution authorization boundary

This holdout protocol authorizes nothing by itself.

Because Two-Lane v1 configuration identity binds exact framework/Skill revision, baseline and candidate execution on Q/T must be covered by fresh campaign policy/configuration identities created only after the candidate exists. EXP-0006 approval, if later granted, cannot authorize those runs and cannot be reused.

Do not mutate the campaign framework merely to make multi-case evaluation convenient. If existing campaign infrastructure makes the full 8+8 execution operationally expensive, record that cost as evidence and choose the smallest governance-compliant execution decomposition. Do not silently reduce the corpus after candidate freeze.

## Blind evaluation

For each executed Q/T case:

1. preserve baseline and candidate raw outputs independently;
2. create the A/B assignment with the deterministic helper and a frozen blinding seed that Context A does not receive before judgments are committed;
3. give Context B only case/rubric + Variant A + Variant B;
4. validate the blind judgment before unblinding;
5. commit the judgment;
6. only then open the assignment map and normalize A/B to baseline/candidate identity;
7. apply the non-scalar fail-closed classifier.

Context B must not receive candidate rationale or predictions during evaluation.

## Leak / integrity failures

Stop the candidate cycle as `INCONCLUSIVE` rather than repairing toward a desired result if:

- Context A reads substantive Q/T content before candidate freeze;
- Q or T is changed after its manifest digest is frozen;
- candidate bytes change after candidate freeze;
- baseline/candidate target SHA, intent, access surface, or evaluator rubric is materially incomparable;
- the A/B identity leaks before a judgment is committed;
- T is opened before Q returns `IMPROVED`;
- exact provenance cannot be reconstructed.

A leak is not permission to quietly construct a replacement holdout set. Any replacement is a new explicitly documented cycle.

## Claim ceiling

This protocol improves isolation but does not create cryptographic secrecy from a repository owner who can technically access the holdout branch. The evidentiary claim is process isolation through fresh conversational context plus durable access discipline, not proof that the candidate author was mathematically incapable of obtaining Q/T. Any stronger claim is prohibited.
