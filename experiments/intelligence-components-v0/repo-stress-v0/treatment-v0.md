# StrategicPlanner repository-grounded stress test — first treatment

schema: strategic-planner-repo-stress-v0/treatment-v0
case: sensemaking-skills-next-responsibility-stress
arm: TREATMENT
component: strategic-planner-v0
prompt_contract: requires 2–4 candidates
evidence_class: SIMULATED_REPOSITORY_GROUNDED_STRESS_TEST / REAL_REPOSITORY_SNAPSHOT / SIMULATED_DECISION_PRESSURE / SAME_MODEL / NON_INDEPENDENT

## Candidate A — WarrantEngine v0 lab experiment

**Responsibility:** Implement a small lab-only WarrantEngine v0 to test whether explicit warrant adjudication improves selection among candidate responsibilities.

**Strategic decision supported:** Determine whether candidate generation should be followed by an explicit warrant-checking mechanism.

**Decision-changing uncertainty:** Whether planner candidate generation creates an adjudication bottleneck that current semantic reasoning handles poorly.

**Dependencies:** Evidence from StrategicPlanner prospective use showing that candidate generation helps but adjudication remains weak.

**Smallest plausible intervention:** One isolated lab experiment with no product promotion.

**Reasons for:** Cheap to prototype; potentially high leverage if adjudication is the next bottleneck.

**Reasons against:** Current StrategicPlanner evidence is still `RESEARCH_MORE`; no prospective case has established an adjudication failure. The current issue authority does not automatically authorize the next component.

**Stop / invalidation evidence:** Do not build if prospective planner evidence does not expose warrant/adjudication pressure.

## Candidate B — RC3 readiness reassessment package

**Responsibility:** Run a bounded release-readiness reassessment to determine whether current `rc3.dev0` development should advance toward an RC3 freeze.

**Strategic decision supported:** Decide whether the repository has converged enough for a new frozen release candidate.

**Decision-changing uncertainty:** Whether current development has reached a stable support boundary with no remaining candidate-changing work.

**Dependencies:** Explicit release-owner authority plus current release-readiness evidence.

**Smallest plausible intervention:** Release audit/readiness review only; no freeze unless separately authorized.

**Reasons for:** The repository is already on `1.0.0rc3.dev0` and several major milestones are complete.

**Reasons against:** Current `STATUS.md` explicitly says do not freeze RC3 merely because milestones completed, and this simulated test grants no release authority.

**Stop / invalidation evidence:** Stop if release-owner authority or convergence evidence is absent.

## Candidate C — prospective-comparison capture helper

**Responsibility:** Add a tiny lab helper that records baseline/treatment/adjudication metadata for future StrategicPlanner prospective cases.

**Strategic decision supported:** Determine whether lower-friction experiment capture would make prospective planner evidence easier to collect.

**Decision-changing uncertainty:** Whether manual experiment capture is currently causing lost, inconsistent, or unusable evidence.

**Dependencies:** Evidence that the present manual protocol is failing or imposing meaningful friction.

**Smallest plausible intervention:** One source-only helper around existing experiment artifacts.

**Reasons for:** Cheap and reversible; could reduce ceremony in future comparisons.

**Reasons against:** No capture failure has been observed. The existing manual protocol already preserved baseline-before-treatment successfully.

**Stop / invalidation evidence:** Do not build without recurring capture friction.

## Material alternative easiest for baseline reasoning to miss

Candidate A is the most strategically interesting construction option because it could test the next intelligence bottleneck if prospective planner use exposes one.

## Ambiguity / evidence insufficiency

All three candidates depend on evidence or authority that the current snapshot does not provide. The current prompt nonetheless requires a 2–4 candidate set.

## Explicit non-candidates

- #384 is not converted into repository code because it is an external GitHub-admin action.
- #255 is not retried or weakened.
- #226 is not treated as normal-use evidence.
- #218 is not treated as a construction package.

`candidate generation != strategic decision`
