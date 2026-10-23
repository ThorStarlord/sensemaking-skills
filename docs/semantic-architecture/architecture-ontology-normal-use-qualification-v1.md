# Architecture Knowledge: Bounded Normal-Use Qualification

**Scope:** source-inspected development cases from PR #565, with focused tests. This is a construction-phase qualification record, **not** an independent agent-session experiment.

| Task | Decision-changing question | What reviewed knowledge should return | Source/qualification ceiling |
|---|---|---|---|
| Edit `semantic_architecture/knowledge_store.py` | Who owns the file, and can it import lab packages? | `component:knowledge-store` owns the exact path; package boundary lists four source-only packages; checker exposes assessment status. | `test_pilot_provenance_and_explicit_ownership_not_confused` checks routing; static checker cannot establish runtime compliance. |
| Modify `scripts/validate-brief.py` | Is validator placement mandatory? | `component:brief-validator` owns the file; placement rule exists as a **hypothesis**, not documented authority. | Query returns epistemic/authority metadata; no new global placement prohibition is inferred. |
| Modify brief producer-consumer handoff | Does a claimed flow match the artifact contract? | The repo-sensemaker -> workflow-planner `flows_to` carries `repository_sensemaking_brief`. | `_validate_authored_contract_flows` checks the cited manifest's `produced_by` and `consumed_by`; invalid-flow test proves rejection. |

## Evidence boundaries

- The actual remediation used repository-source inspection and GitHub commits. It did **not** compare independent agents with and without these queries.
- Current focused tests establish selected behavior of the representation and checker, not a measured improvement in architecture choices.
- Running these commands on the final committed HEAD and inspecting CI is the remaining mechanical qualification; do not imply an old snapshot reflects the current worktree.
- If a query returns `NOT_ASSESSED`, a hypothetical rule, ambiguous ownership, or incomplete rule assessment, inspect the smallest governing original source needed for the pending edit. Routine edits need not trigger a compulsory knowledge-building phase.

**Next evidence only if warranted:** use the enhanced queries during a future authentic coding task and record the concrete decision changed, avoided error, or time spent. An independent-session benchmark is deferred until release qualification.
