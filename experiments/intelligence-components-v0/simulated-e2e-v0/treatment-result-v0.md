# StrategicPlanner v0 simulated E2E — treatment candidate set

schema: strategic-planner-simulated-e2e-v0/treatment-result-v0
case: quartz-cli-dry-run-contract
arm: TREATMENT
component: strategic-planner-v0
evidence_class: SIMULATED_E2E / SAME_MODEL / NON_INDEPENDENT / CONSTRUCTED_CASE

## Candidate A — bounded contract diagnosis

**Responsibility:** Reproduce the clean-directory dry-run behavior outside CI and reconcile the observed cache write against the authoritative dry-run contract before changing code or docs.

**Strategic decision supported:** Determine whether the repository should repair implementation, change the documented contract/test, or treat the failure as environment-specific.

**Decision-changing uncertainty:** Whether `.quartz/cache.json` creation is real current behavior and whether the intended contract forbids it.

**Dependencies:** Reproducible clean-directory run; current contract/docs; code path responsible for cache creation.

**Smallest plausible intervention:** One controlled reproduction plus targeted contract/code inspection.

**Reasons for:** Preserves reversibility; discriminates among downstream repairs; respects release hold.

**Reasons against:** Adds one diagnostic step if the contract is already unambiguous from authority inspection alone.

**Stop / invalidation evidence:** Stop when behavior + intended contract are sufficiently clear to select one bounded downstream responsibility.

## Candidate B — implementation repair for strict no-write semantics

**Responsibility:** Change dry-run execution so no cache metadata is created.

**Strategic decision supported:** Preserve the documented interpretation that dry-run performs no writes of any kind.

**Decision-changing uncertainty:** Whether strict no-write semantics are actually intended and whether the failing integration signal reflects real behavior.

**Dependencies:** Confirmation that the contract forbids cache metadata writes.

**Smallest plausible intervention:** Gate cache-file creation during dry-run and add/repair a focused integration assertion.

**Reasons for:** Directly aligns implementation with the strongest reading of current docs.

**Reasons against:** Premature if cache metadata writes are intentionally outside the user-facing no-write guarantee or if the CI signal is spurious.

**Stop / invalidation evidence:** Do not proceed if contract authority permits cache metadata or the behavior fails to reproduce.

## Candidate C — documentation/test contract reconciliation

**Responsibility:** Clarify that dry-run prevents user-project mutation while allowing internal cache metadata, and update the integration expectation accordingly.

**Strategic decision supported:** Preserve current implementation behavior while making the user-visible contract truthful.

**Decision-changing uncertainty:** Whether cache metadata creation is intended product behavior and acceptable under the product promise.

**Dependencies:** Product-contract authority or owner intent supporting the narrower interpretation.

**Smallest plausible intervention:** Narrow the documented guarantee and update the failing integration assertion without changing runtime behavior.

**Reasons for:** Avoids unnecessary implementation churn if metadata writes are intentional.

**Reasons against:** Could silently weaken a meaningful user expectation if the current no-write promise was intended literally.

**Stop / invalidation evidence:** Do not proceed if current authority establishes strict no-write semantics.

## Candidate D — CI/test-environment diagnosis

**Responsibility:** Treat the integration failure as potentially environment-specific and isolate why it appears only in clean CI-like conditions before changing product behavior or contract.

**Strategic decision supported:** Determine whether there is any real product mismatch to repair.

**Decision-changing uncertainty:** Whether the observed cache write/failure reproduces outside CI under equivalent clean-directory conditions.

**Dependencies:** Reproduction harness matching the failing integration environment.

**Smallest plausible intervention:** Re-run the isolated integration scenario locally or in an equivalent clean temp environment and compare filesystem effects.

**Reasons for:** Prevents product changes based on a possibly non-product failure mode.

**Reasons against:** Overlaps substantially with Candidate A and is too narrow if the behavior is immediately reproducible.

**Stop / invalidation evidence:** Stop this branch if behavior reproduces consistently outside CI.

## Material alternative easiest for baseline reasoning to miss

Candidate C is the most distinct downstream alternative: the implementation may be acceptable while the documented/test contract is too broad. However, the baseline already acknowledged this possibility, so this treatment does **not** establish missing-option discovery.

## Ambiguity / evidence insufficiency

The supplied evidence is insufficient to responsibly choose B or C. A/D are evidence-producing candidates; B/C are downstream repair candidates contingent on the result.

## Boundary check

- No numeric ranking assigned.
- No winner selected.
- No candidate executed.
- No repository scope or authority expansion.
- The unrelated HTTP dependency upgrade is not promoted because the case supplies no causal link.

`candidate generation != strategic decision`
