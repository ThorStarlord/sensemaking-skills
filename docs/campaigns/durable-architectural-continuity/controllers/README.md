# Campaign 3 controller checkpoints

Controller-specific durable checkpoints. Each preserves what a controller
believed **at that point in time**. Once committed as temporal evidence, a
checkpoint is **not rewritten** merely because later evidence changes the
campaign conclusion — later `CAMPAIGN-STATE.md` versions supersede a checkpoint's
conclusions while the checkpoint file itself stays as written.

Expected files (created as the campaign progresses):

```
A-selection.md            Controller A: Phase 1 product-state reconstruction +
                          highest-leverage capability selection + coupling
                          assessment + Phase 1 disposition.
A-architecture.md         Controller A: Phase 2 architectural intent resolution
                          (only if a coupled capability is selected) — the
                          consequential architectural decisions with authority
                          basis + candidate decision status, alternatives,
                          affected surfaces, cross-surface obligations, invariants,
                          reopen conditions.
A-handoff.md              Controller A: Phase 3 transitional-state record +
                          handoff provenance + the verbatim bootstrap given to B.
                          Contains NO predicted next actions / execution plan.
A-sealed-predictions.md   (optional) Controller A's predicted next actions,
                          sealed — B must NOT read this before committing its
                          reconstruction checkpoint. For the post-hoc audit only.
B-reconstruction.md       Controller B: independent reconstruction + verification
                          + architectural reassessment + one decision
                          (CONTINUE_AS_DESIGNED / CONTINUE_WITH_REFINEMENT /
                          REDESIGN / REVERT / OWNER_DECISION_REQUIRED /
                          EXTERNAL_BLOCKER / SUCCESSION_FAILURE_REQUIRES_REDESIGN
                          / CAMPAIGN_PREMISE_INVALIDATED). Committed BEFORE
                          substantial implementation and BEFORE any predecessor
                          semantic feedback.
B-cycle-result.md         Controller B: completion trace + coupled completion
                          standard + context-compression analysis + remaining
                          ceilings.
A-B-continuity-audit.md   Post-hoc architectural-continuity audit (former
                          Controller A as retrospective auditor, or a fresh audit
                          context). Written only AFTER B's cycle is frozen.
                          Does not rewrite A-* or B-* checkpoints.
```

If Phase 1 concludes `NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED`,
`CAMPAIGN_PREMISE_INVALIDATED`, `OWNER_DECISION_REQUIRED`, or `EXTERNAL_BLOCKER`,
only `A-selection.md` and the final report are produced; the handoff and B-*
checkpoints do not exist because no coupled partial architecture was created.
