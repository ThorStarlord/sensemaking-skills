# ON-DEMAND PROJECTION RECIPE — V1

Implementation-neutral procedure for answering a consequential architecture
question that the thin core (`SEMANTIC-CONTROL-CORE.md`) does not answer
directly. Executed **manually** as an architecture-development step.

**Not** a Skill, workflow, routing path, graph traversal subsystem, or product
runtime machinery (authorization §17, §30). It does not integrate with
MODEL_WARRANT or `repo-sensemaker`.

---

## The loop

```
consequential question
  → 1. pick expansion seeds from the thin core
  → 2. name the missing relationships this question needs
  → 3. inspect current repository evidence for exactly those
  → 4. materialize only that local relationship set (a scratch table)
  → 5. answer the question, carrying authority/lifecycle grades through
  → 6. discard the projection (record it locally; promotion default = NO)
```

## A. Choosing expansion seeds

Start from the smallest set of thin-core rows the question names or implies:

- a **Concern** row (§1) if the question is "who owns / enforces / may change X";
- a **Lifecycle ledger** entry (§2) if it is "is X current / still authoritative";
- an **Enforcement-gap** row (§3) if it is "is X actually checked / consistent";
- the **Research→product** row (§4) if it is "does research affect runtime here";
- if the question names a symbol/file/test not in the core, the seed is
  "core has no row — this is a raw-inspection question" (expected; see F).

## B. Evidence sources to inspect (in rough priority order)

1. `CONTEXT.md` — product definition, authority model, source-of-truth map,
   evidence model, glossary.
2. `docs/agent-native-operating-workflow.md` — responsibility / artifact /
   authority flow + the Reality map (REAL vs CONVENTION).
3. `skills/workflow-planner/references/artifact-contracts.yaml` — artifact
   producer/consumer/section/machine-field/verification contract (the API).
4. `docs/adr/` — ratified/proposed/superseded decisions; `docs/adr/README.md`
   for the status vocabulary.
5. `skills/workflow-planner/references/{workflow,skill}-registry.yaml` (+ the
   `src/sensemaking_skills/defaults/` mirror — diff them if the question
   touches workflow steps or auto-invoke).
6. `scripts/` — `workflow-runtime.py` (path resolution, routing-field reads,
   warrant seam), `validate-*.py` (21 validators), `probe-repo.py` /
   `probe_relationships.py`, `gate_a_authorization.py`, `skill_executor.py`.
7. `src/sensemaking_skills/reasoning/` — only for warrant/representation logic.
8. `docs/research/control-model-research-agenda.md` — for research-thread
   status and claim ceilings.
9. `git log` / specific commits / PRs — only when the boundary is historical
   (e.g. "why was this guard added").

Stop opening sources as soon as step E's condition is met.

## C. Preserving authority / lifecycle semantics in the projection

For every relationship you materialize, record alongside it:

- **who DEFINES** it and **who ENFORCES** it (may be "nothing");
- its **lifecycle** (ACTIVE / PROPOSED / EXPERIMENTAL / DEPRECATED /
  SUPERSEDED / HISTORICAL_ONLY / research-only);
- an **epistemic grade** (DEMONSTRATED / DERIVED / INTERPRETIVE / HYPOTHESIS);
- whether **implementation and policy agree**.

A projection that drops these collapses into an ordinary dependency sketch and
loses the thing V0 showed was valuable.

## D. Distinguishing current vs stale evidence

- An ADR is authoritative only if its `**Status**` is `ACCEPTED` (or a
  compound "ACCEPTED (…)"). `PROPOSED` / `PROVISIONAL` / `SUPERSEDED` /
  `REJECTED` are not current policy.
- A registry field or runtime code path is *capability*, not *authority* —
  cross-check against `CONTEXT.md` ("not automatically ratified merely because
  machinery exists") and the relevant ADR.
- When two files carry the same fact, the `CONTEXT.md` source-of-truth map
  names the canonical one; the other is a mirror (check for drift).
- Prefer a probe measurement (`probe-report.yaml`) over prose for empirical
  repository state; a failed probe observation is **not** an observed absence.

## E. When to stop expanding

Stop when the **consequential** question is answerable — i.e. when the next
piece of evidence could not change the responsibility, the impact set, or the
authority answer. Do not expand to make the projection "complete." If you have
named the affected regions and their authority/lifecycle status, you are done,
even if finer detail exists.

## F. Recording the projection without promoting it

- Write the scratch table + answer into a local note (e.g. a dated file under
  the requesting work's directory, or `COMPRESSION-EVALUATION.md` for this
  prototype's drills). Do not add it to `SEMANTIC-CONTROL-CORE.md`.
- **Promotion default = NO.** A projected relationship enters the thin core
  only after *repeated* usefulness across distinct questions **and** evidence
  that its semantics are stable enough to maintain — the same
  machinery-promotion bar the repo uses elsewhere (`harden only where
  pressured`).
- If a projection was expensive and recovered little the core did not already
  imply, record that too — it is evidence about the recipe, not a failure to
  hide.

## G. Worked shape (illustrative, not a stored answer)

> Q: "If `representation_sufficiency` semantics changed, what must be inspected?"
> Seeds: A2, A6, §4 row.
> Missing relationships: which validator parses the field; which reasoning-slice
> functions map it; whether routing reads it.
> Inspect: `artifact-contracts.yaml` (brief entry, `representation_sufficiency`
> declared OPTIONAL/ADDITIVE) → `validate-brief.py` → `reasoning/warrant_gate.py`
> + `vertical_slice.py` (mapping) → `workflow-runtime.py` INCONCLUSIVE gate +
> `_WORKFLOW_ID_FIELDS` (routing does *not* read the field) → ADR 0015 addendum.
> Stop: affected set = {ADR 0015 addendum, contract declaration, `validate-brief.py`,
> runtime warrant seam + INCONCLUSIVE gate, `reasoning/` mapping module}. ~5 nodes.
> Carry grades: mapping logic INTERPRETIVE until the two reasoning files are read;
> rest DEMONSTRATED.
> Discard. Promotion: NO (single question).
