# Ontology Author → Persist → Fresh Reader — Bounded Qualification Design

**Status:** Owner-agreed investigative design; **planning only**, not an executed agent observation, schema proposal or authorization to change canonical knowledge. Inspected `ThorStarlord/sensemaking-skills@1efb0f249b23c782f6f16a00155d86159de94a2a` on 2026-11-05. Refresh exact sources/permissions before running.  
**Implementation plan:** [Ontology Author–Reader Qualification](../plans/2026-11-05-ontology-author-reader-qualification.md).

## 1. Question and smallest defensible claim

**Question:** Can a coding agent, using the **existing** Sensemaking semantic ontology, independently author a source-faithful, machine-valid knowledge candidate, persist it at a pinned Git revision, and enable a **fresh coding agent without the author's conversation** to locate, interpret and verify the candidate correctly?

This is a knowledge-representation / producer-consumer **first-use observation**. It does not qualify novel schema design, improved creative reasoning, graph-versus-source superiority, universal cross-agent repeatability, or the graph viewer. It is **not** a mandatory stage for future agent tasks.

Success requires distinguishing **conceptual representation** (ontology definitions in documentary sources), **authored executable records** (validated `.sensemaking/knowledge/*.json`), **mechanical indexing/retrieval**, **agent interpretation**, and **original-source verification**. Valid JSON alone does not establish interpretation; a correct answer read only from source documents does not establish successful use of the new record.

## 2. Why this case, alternatives considered

| Approach | Merit | Main limitation | Decision |
| --- | --- | --- | --- |
| Reuse the known 2026-10-23/24 `PATH-1` / `ASSUMPTION-1` history | Semantically subtle, strong original-source oracle; good for a calibration or negative check | Already extensively reconstructed in `docs/semantic-architecture/premise-sensitive-reconsideration-cases-v1.md` and `docs/normal-use/2026-11-05-premise-sensitive-reconsideration-first-use.md`; reauthoring creates duplicate history and risks answer leakage | **Fallback/calibration only** |
| Use an external target (Atlas Midgard/Auteur) | More transfer-relevant and less self-referential | Increases permissions, identity, Skill-install, source-read and owner-ontology complexity | **Later, only if this smaller case leaves an important portability uncertainty** |
| **Use the current agent-primary / graph-secondary decision and offline viewer contract** | Real recent source case, supported v1/v2 ontology, introduced in PRs #759–762, not explicitly covered as a new viewer decision in the inspected 10 reviewed knowledge packs; bounded write/read with genuine source/authority limits | Sources already explain the design, so B may answer correctly without consuming A's new candidate; record-use attribution must be checked explicitly | **Select as first case** |

**Source material for the candidate** (do not insert expected answer into participant briefs):
- `docs/superpowers/specs/2026-11-05-agent-native-knowledge-graph-reasoning-design.md`: accepted interface hierarchy and authority boundaries;
- `docs/semantic-architecture/agent-native-graph-viewer-v1.md` and `docs/semantic-architecture/premise-sensitive-reconsideration-contract-v1.md`: source-attributed retrieval and hypothetical scenario limits;
- `src/sensemaking_skills/semantic_architecture/knowledge_view.py`, `src/sensemaking_skills/semantic_architecture/view_assets/graph_view.html`, `src/sensemaking_skills/semantic_cli.py`: implementation sources (what is and is not executable);
- `docs/adr/0034-ontology-first-adaptive-sensemaking.md` and `.sensemaking/knowledge/product.json`: already represented public-entrypoint/agent control, whose meaning must not be duplicated or rewritten.

The candidate should express **only the minimal currently uncovered relationship(s)** justified by original sources: the difference between an owner-approved interaction decision, an actually implemented read-only mechanism, what the viewer does not authorize, and what evidence would be needed to extend semantics. Let the author decide source-grounded claim/edge shape under existing vocabularies; the evaluator, not the author task, owns the factual oracle. Source evidence that every relevant distinction is already covered can yield `NO_NEW_DURABLE_KNOWLEDGE` and trigger a *test-only* draft rather than an artificial production addition. Do not revise product strategy.

## 3. Deliberately minimal operating arrangement

One repository, one case, **two genuinely separate coding-agent sessions**, one independent source-aware review. Prefer one real agent host supporting fresh contexts (Codex, OpenCode, Claude Code or equivalent) without building a new orchestration runtime.

- **Author A:** given the bounded question and ordinary installed ``using-sensemaking` / `repository-semantic-steward` guidance, inspects current relevant knowledge and originals, authors the **smallest test-only candidate** in `.sensemaking/knowledge/ontology-author-reader-probe.json` on a disposable `claude/<topic>` branch/worktree. The file's temporary status must be clear; do not replace or edit an existing authored pack.
- **Mechanical persistence:** the existing `semantic knowledge-proposal-check` validates candidate format and source refs while dirty; commit candidate on the disposable branch; build a source-pinned SQLite index outside the repo at the exact committed SHA, using `--temporary-checkout` when the active worktree isn't at that clean SHA. Preserve output/exit status and exact candidate SHA. Do not merge the candidate.
- **Reader B:** fresh context, **no author transcript, output summary, candidate file name, record IDs or answer key**. Same repository/Skill-version availability where practical, receives the exact candidate branch commit and a neutral question about the new viewer's role relative to agent control and source/authority limits. The intended default is to retrieve relevant reviewed semantic knowledge using normal instructions before source checking. If B uses only source docs, mark candidate consumption `NOT_DEMONSTRATED` even if answer is correct. One minimal neutral cue (consult reviewed semantic knowledge) is permitted **after** recording the spontaneous attempt; label the outcome `PROMPTED`, not spontaneous.
- **Independent source reviewer C:** sees the frozen candidate plus A/B traces and original sources; independently assesses author fidelity, explicit relationship roles, mechanical query/record use, source verification and bounded conclusion. Reviewer cannot silently repair the candidate or reinterpret the success rule after evidence appears.

Use exact Git SHAs, real host/model/Skill versions, source file paths and actual query commands. If this environment cannot launch fresh sessions or inspect necessary terminal execution, **STOP at readiness** and record `NOT_RUN/BLOCKED`; running this same assistant twice or drafting hypothetical transcripts is not independence.

## 4. Two-pass reading distinguishes ingestion from faithfulness

**Reader pass 1 — representation:** Without an author explanation, locate/retrieve the proposed candidate through the supported repository knowledge path. Summarize its assertions, explicit relationships, source IDs, reported uncertainty and whether it contains unknown or merely contextual edges. Capture real query IDs and file/source reads. Do not judge source correctness from query result alone.

**Reader pass 2 — source verification:** Check the critical claims against original dated design, implementation, current strategy/ADR and versioned sources. State confirmed, unsupported, uncertain and contradicted elements. A correct rejection of a mistaken candidate counts as evidence of reader verification, not semantic agreement.

Keep the two answers or a clear timestamped boundary. B need not browse the secondary HTML viewer; it is an independent capability and would introduce an unnecessary intervention.

## 5. Observable outcomes and fail-open alternatives

| Axis | What warrants `OBSERVED_PASS` | A meaningful partial/failure |
| --- | --- | --- |
| Author fidelity | Original sources actually support each critical claim/relation at the cited scope; normative decision differs from observed implementation | Schema-valid but unsupported claim; over-asserted necessity, authority or novelty |
| Mechanical write/index | Candidate proposal preflight and exact candidate-commit indexing complete; IDs/sources retrievable with actual `search` + `explain` | Invalid draft, unresolved cited source, wrong SHA, unindexed dirty overlay; **mechanical failure**, not automatically reader failure |
| Reader discovery/consumption | B uses the **candidate** through ordinary indexed query or direct authored record and names the IDs/source, without being handed the answer | Answers correctly from source docs alone: `SOURCE_ONLY_CORRECT / CANDIDATE_USE_NOT_DEMONSTRATED`; after neutral cue: `PROMPTED_USE` |
| Reader interpretation | B correctly distinguishes decision, implemented capability, absence/unknown, and authority/epistemic limits before checking originals | Collapses source vs inference, \`references\` vs necessity, or changes interaction design into owner authorization |
| Reviewer source check | Reviewer independently validates source support and B's critique, preserving any rejected claim as a failure/learning | A and B agree on a misrepresentation; pre-existing docs contain the answer without observed candidate use |

No weighted score or invented pass quota. Overall outcome is `OBSERVED_SUCCESS` only when all five axes pass, **including unprompted candidate consumption**, under their *stated* narrow ceiling. If the candidate is recovered only after the one allowed neutral cue, use `PARTIAL / PROMPTED_USE` even when interpretation and source checking are otherwise faithful; `PARTIAL` names the responsible layer; `FAIL` attaches specific observed defect; `INCONCLUSIVE` covers ambiguous treatment/trace; `NOT_RUN/BLOCKED` covers absent fresh-agent capability. Mechanical checks may succeed while independent interpretation remains unobserved.

**Negative checks:**
1. A generic `references` edge **must not** be read as necessary causal/strategic support.
2. A declared interface decision is **not** an observed successful user benefit; the implemented export is **not** a new owner decision.
3. A viewer scenario never changes reviewed knowledge or triggers work.
4. A missing graph result is `NOT_ASSESSED`, not evidence that no source relationship exists.
5. A correct interpretation obtained only from existing source summaries cannot be credited to reading A's candidate.

## 6. Authority, evidence, retention and scope ceilings

The current `AGENTS.md` says evaluation designs must not quietly select favorable outcomes; `CLAUDE.md` keeps the explicit construction rule against adding/running local unit or synthetic evidence tests. This is a **real-use qualification task**, not permission to introduce a test suite, synthetic answer benchmark or new experimental infrastructure. If the owner later explicitly authorizes this test to run, ordinary product use of `knowledge-proposal-check`, `knowledge-build` and `knowledge-query` is the evidence-producing action; record real outputs and do not misreport them as unit tests.

A test candidate in a disposable branch is *not* permanent ontology evolution. Under `schema-evolution.md`, any actual missing distinction must pass a separate consumer/authority/compatibility gate. A successful author-reader result does not automatically merge a new knowledge pack; the production decision may be `NO_MODEL_CHANGE`. There is no authorized release/deploy, graph-first controller, user-goal promotion or broader creative benchmark.

Preserve a compact evaluation readout only after a real run, preferably `docs/normal-use/<actual-date>-ontology-author-reader-first-use.md` with exact refs, source reads, commands, both agent observations, reviewer outcomes, negative cases and bounded claim. If fresh sessions or evidence capture are unavailable, record readiness/blocker without fabricating author/reader output. Keep evaluator-specific source expectations apart from author/reader invocations: they may be grounded privately by a later reviewer, with an audit trail pointing to source files.

**Completion condition for this plan's execution:** one real author → exact committed candidate → fresh reader → independent source review observation, or a documented genuine host/permission blocker. The plan's creation or merge is **planning only**.
