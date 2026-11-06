# Independent Semantic Transfer — Unfamiliar Atlas Case

**Status:** Planning only; no empirical run or model change. **Plan:** [execution plan](../plans/2026-11-05-unfamiliar-case-semantic-transfer.md).

## Goal and evidence ceiling

Observe whether an agent can author source-faithful records using the existing ontology and whether a distinct fresh-session reader can interpret those records **before** consulting original sources, then independently source-check them. This addresses the interpretive gap in the [first-use PARTIAL readout](../../normal-use/2026-11-05-ontology-author-reader-first-use.md). It does not test creative benefit, unprompted discovery reliability, superiority to source-only reasoning, or generality.

## Authentic unfamiliar case

**Proposed target:** `ThorStarlord/atlas-midgard@2b3556e47daa6110d01c045432e23bf4e041ba49`.

**Neutral question:** “In Atlas, how should companion Shared Memory relate to Saga History and durable player progression, and what is supported by the current repository versus specified or not assessed?”

This topic is outside the six inspected Atlas knowledge packs, which mainly cover co-op and world continuity. An evaluator should inspect `docs/decisions/companion-relationship-continuity.md`, `docs/decisions/companion-identity-and-relationship-model.md`, `docs/implementation/package-16-companion-shared-memory.md`, `docs/architecture/persistent-progression-stack.md`, and relevant `game/scripts/progression/` files. These are **source candidates, not an answer key**. Reconfirm at execution. If already represented or previously exposed to participants, choose and freeze another real unfamiliar case **before** observing agents; never select a case after seeing results.

## Method and independence

1. Operator freezes exact repository, CLI, Skill, agent-session and case identities outside participants' workspaces.
2. Fresh Author A reads existing packs and original sources and writes the smallest supported-v1/v2 candidate on a disposable local target branch; no product edits or schema changes.
3. Validate with `semantic knowledge-proposal-check`, commit at one exact Git revision, build SQLite outside the repository, and reproduce `knowledge-query search/explain`. Mechanical validity does not certify semantic fidelity.
4. Fresh Reader B uses authored semantic knowledge without A's transcript, record names or expected answer. **First pass:** record a source-free explanation of explicit claims, edges, provenance and uncertainty. **Second pass:** open original source files and independently correct unsupported interpretations. Freeze first answer and tool trace before unlocking source reading.
5. Independent Reviewer C compares A, candidate, B's two frozen passes and original sources.

Distinct host sessions and isolated scratchpads are mandatory. Shared model is permissible and disclosed. If B reads original sources before the first-pass account, interpretation is `NOT_OBSERVED/CONTAMINATED`, not a pass. Because B is explicitly asked for a knowledge-first account, label the result `PROMPTED_REPRESENTATION`, never spontaneous discovery.

## Adjudication

Five independent axes: **author fidelity**, **exact-commit mechanical indexing**, **actual candidate use**, **pre-source semantic interpretation**, and **independent source verification**. To claim `OBSERVED_SEMANTIC_TRANSFER_IN_ONE_CASE`, all five must pass and isolation must hold. Otherwise report `PARTIAL` with failed axes, `FAIL` for an observed mechanism defect, `INCONCLUSIVE` for ambiguous traces, or `NOT_RUN/BLOCKED` if fresh sessions or credible observability are unavailable.

Negative checks: `references` never proves necessity; documentation aspiration never proves current code implementation; old package records are not necessarily current authority; missing evidence is `NOT_ASSESSED`; schema validity is not semantic truth. No score, synthetic benchmark or post-hoc oracle adjustment.

## Boundaries and closeout

Use an isolated pinned CLI environment; do not modify the global CLI or installed Skills. Keep the Atlas candidate local/unmerged and do not alter existing packs, game saves or canonical product decisions. Preserve raw traces privately when they contain memory; publish only redacted, reconstructible decisive evidence. A real run may produce a separate Sensemaking readout and docs PR. The historical `PARTIAL` result and PR #767 remain unchanged. `NO_MODEL_CHANGE` is a valid outcome. Publication of this spec and plan is **planning only**.
