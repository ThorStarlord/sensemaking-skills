# Campaign 2 controller checkpoints

Each semantic Campaign 2 controller writes controller-specific durable
checkpoints here. Checkpoints **preserve what the controller believed at that
point in time** and are **not** retro-edited when later evidence shifts the
campaign's understanding (later `CAMPAIGN-STATE.md` versions may supersede a
checkpoint's conclusions while the checkpoint itself stays intact).

Expected files:

```
A-reconstruction-and-selection.md   Controller A: reconstruction of integrated
                                    product state, candidate state, campaign
                                    semantic state; strategic-boundary
                                    comparison; Task A selection. Committed
                                    BEFORE any Task A implementation.
A-handoff.md                        Controller A: pre-handoff invariant checklist;
                                    handoff provenance; the VERBATIM bootstrap
                                    text supplied to Controller B; handoff SHA.
                                    Committed BEFORE Controller B is instantiated.
B-reconstruction-and-selection.md   Controller B: independent reconstruction
                                    (the 20 fresh-controller questions) + the
                                    mandatory successor-checkpoint fields +
                                    Task B selection. Committed BEFORE any Task B
                                    implementation and BEFORE any predecessor
                                    semantic feedback.
B-cycle-result.md                   Controller B: Task B execution, validation,
                                    capability/hypothesis assessment, and whether
                                    further Campaign 2 work would materially
                                    affect the central question.
```

Additional controllers (C, ...) follow the same `X-*.md` convention. A
Controller C handoff is optional and only performed if it would materially change
the Campaign 2 conclusion.

Authority source: `../OWNER-INSTRUCTION.md`. Operating contract: `../CHARTER.md`.
Evolving semantic state: `../CAMPAIGN-STATE.md`.
