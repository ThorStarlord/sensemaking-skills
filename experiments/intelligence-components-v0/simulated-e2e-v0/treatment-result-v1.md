# StrategicPlanner v0 simulated E2E — repaired treatment candidate set

schema: strategic-planner-simulated-e2e-v0/treatment-result-v1
case: quartz-cli-dry-run-contract
arm: TREATMENT
component: strategic-planner-v0
prompt_repair: collapse contingent/subsumed candidates
evidence_class: SIMULATED_E2E / SAME_MODEL / NON_INDEPENDENT / CONSTRUCTED_CASE

## Candidate A — bounded contract diagnosis

**Responsibility:** Reproduce the clean-directory dry-run behavior outside CI and reconcile the observed cache write against the authoritative dry-run contract before changing code or docs.

**Strategic decision supported:** Determine whether the repository should repair implementation, change the documented contract/test, or treat the failure as environment-specific.

**Decision-changing uncertainty:** Whether `.quartz/cache.json` creation is real current behavior and whether the intended contract forbids it.

**Dependencies:** Reproducible clean-directory run; current contract/docs; code path responsible for cache creation.

**Smallest plausible intervention:** One controlled reproduction plus targeted contract/code inspection.

**Reasons for:** Preserves reversibility; discriminates among downstream repairs; respects the release hold.

**Reasons against:** Adds a diagnostic step if authoritative contract inspection alone resolves the mismatch.

**Stop / invalidation evidence:** Stop when behavior + intended contract are sufficiently clear to select one bounded downstream responsibility. CI-specific reproduction remains a sub-path of this candidate rather than a separate candidate.

## Candidate B — implementation repair for strict no-write semantics

**Responsibility:** Change dry-run execution so no cache metadata is created.

**Strategic decision supported:** Preserve the documented interpretation that dry-run performs no writes of any kind.

**Decision-changing uncertainty:** Whether strict no-write semantics are actually intended and whether the failing integration signal reflects real behavior.

**Dependencies:** Confirmation that the contract forbids cache metadata writes.

**Smallest plausible intervention:** Gate cache-file creation during dry-run and add/repair a focused integration assertion.

**Reasons for:** Directly aligns implementation with the strongest reading of current docs.

**Reasons against:** Premature if cache metadata writes are intentionally outside the user-facing guarantee or if the failure is spurious.

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

## Material alternative easiest for baseline reasoning to miss

Candidate C is the most distinct downstream alternative, but the frozen baseline already acknowledged documentation/test reconciliation. No missing material option is established in this simulated case.

## Ambiguity / evidence insufficiency

The supplied evidence is insufficient to responsibly choose B or C. Candidate A is the evidence-producing responsibility that can discriminate between them.

## Boundary check

- No numeric ranking assigned.
- No winner selected.
- No candidate executed.
- No repository scope or authority expansion.
- No contingent diagnostic sub-path promoted as a separate repository-level candidate.
- The unrelated HTTP dependency upgrade is not promoted because the case supplies no causal link.

`candidate generation != strategic decision`
