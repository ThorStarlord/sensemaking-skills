# Ontology Author–Reader First-Use Qualification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. **Execution requires a genuine fresh-agent host; this plan and its merger are not a completed empirical run.**

**Goal:** Observe one source-faithful knowledge-authoring → persisted-index → fresh-reader → independent-source-verification exchange using Sensemaking's **existing ontology**, without expanding it.

**Architecture:** Use one small real, currently underrepresented repository case (the new agent-primary / read-only graph-secondary experience). An independent coding agent writes a minimal temporary knowledge pack on a disposable branch; the existing validator/index makes it retrievable at the exact candidate commit. A **different fresh session** locates and interprets that persisted candidate before source-checking it, and a separate reviewer assesses fidelity, actual usage and error localization. The candidate never automatically becomes canonical knowledge.

**Tech Stack:** Existing `using-sensemaking` and `repository-semantic-steward` guidance; Git and one available coding-agent host with fresh session creation; Python >=3.11 and Sensemaking's existing Click CLI (`knowledge-proposal-check`, `knowledge-build`, `knowledge-query`) and SQLite index. No new code, test harness, schema migration, web UI, external service or graph dependency.

**Spec:** [Ontology Author → Persist → Fresh Reader Qualification Design](../specs/2026-11-05-ontology-author-reader-qualification-design.md).

**Inspected planning baseline:** `ThorStarlord/sensemaking-skills@1efb0f249b23c782f6f16a00155d86159de94a2a` (2026-11-05). Pin an actual source revision again immediately before execution; do not use moving `main` as a hidden input.

## Global Constraints

- This is an **authentic, small product-use qualification**, not a benchmark or proposal to create new features. The user approved **testing the ability to author and read knowledge using the existing ontology**, **not** authoring new ontology kinds, predicates or universal vocabulary.
- Honor `AGENTS.md` / `CLAUDE.md` and [ADR 0031](../../adr/0031-persistent-semantic-stewardship.md), [ADR 0034](../../adr/0034-ontology-first-adaptive-sensemaking.md) and [the authored knowledge contract](../../../skills/repository-semantic-steward/references/knowledge-contract.md). No automatically elevated knowledge, strategy, product intent or merge/release authority.
- Before working, verify that the target repository and the **installed Skill/CLI versions** are the expected ones. Log repository baseline SHA, candidate SHA, model/host, installed Skill provenance/version and command availability; repository SHA alone does not prove which installed Skill bytes were used.
- All authored test records must use **supported v1/v2 vocabulary and field meanings** in `knowledge.py`. No fabricated `assumption` type, `necessitates` edge, automatic ontology extension, new schema-v3 or revised graph engine. A generic `references` edge cannot establish causal or logically necessary support.
- The **test candidate** is a small, clearly isolated `.sensemaking/knowledge/ontology-author-reader-probe.json` on one disposable `claude/ontology-author-reader-probe-<date>` branch. Never overwrite existing packs or merge the candidate automatically; reviewed source files remain unchanged. A real new knowledge need may be separately proposed **after** evaluation and normal authority review.
- The source case is the existing **agent-primary / graph-secondary** architectural decision and source-pinned offline viewer, from `docs/superpowers/specs/2026-11-05-agent-native-knowledge-graph-reasoning-design.md`, `docs/semantic-architecture/agent-native-graph-viewer-v1.md`, `docs/semantic-architecture/premise-sensitive-reconsideration-contract-v1.md`, `src/sensemaking_skills/semantic_architecture/knowledge_view.py`, and the currently accepted ADRs; first inspect `.sensemaking/knowledge/product.json` to avoid re-authoring `decision:ontology-first-adaptive-sensemaking`.
- **Source evidence:** `knowledge-proposal-check` is **mechanical preflight**, not a semantic acceptance oracle. Build a new index **only from an exact committed revision**; store SQLite and diagnostic data *outside* the target checkout. An active dirty checkout may require `--temporary-checkout`. A missing link means `NOT_ASSESSED`, not “no relationship.”
- **Actual two-context separation is mandatory.** A and B must be distinct fresh coding-agent contexts; a third source-aware reviewer C must not be the producing agent. A summary of A's conversation, its candidate record IDs, filenames or expected conclusions must not appear in B's prompt. Do not simulate independence by restarting this same conversation, drafting sample transcripts, or pretending GitHub access launches an autonomous agent.
- Do not give an expected factual answer to A/B. Preserve the natural installed instructions and source access. The evaluator can read existing historical material and formulate an oracle from original sources; participant use of the stored qualification plan/oracle is an observable contamination to disclose.
- **Verification policy:** The repository's current construction rule prohibits adding/manually running local *unit or synthetic evidence tests*. Use the existing product CLI as actual workflow, record exact outputs, preserve hosted CI when real PRs exist, and label `NOT_RUN`/`NOT_ASSESSED` accurately. The owner's agreement to a small authenticity exercise is not permission for a new test suite or benchmark infrastructure.
- **Stop at actual boundaries:** no usable fresh-agent host, inaccessible sources, invalid index/CLI preventing meaningfully observable reading, authority to create disposable branch absent, or inability to capture B's record use. Declare `BLOCKED` or `INCONCLUSIVE` and preserve evidence; do not lower standards to force a PASS.

## Review Focus — Five ways a seemingly successful run misleads us

| Failure condition | Correct observable behavior | Owning task/check |
| --- | --- | --- |
| Writer invents a new ontology kind/predicate to represent an ordinary concept | Use supported types/attributes, or report precise expressiveness gap; no schema mutation | Task 2, author source/schema review |
| Writer produces valid records but misstates normative authority as observed implementation | Reviewer rejects semantic fidelity even if `knowledge-proposal-check` passes | Tasks 2/5, authority-and-source comparison |
| Reader answers correctly from documentation without consuming the candidate | Classify `SOURCE_ONLY_CORRECT / CANDIDATE_USE_NOT_DEMONSTRATED`; cannot claim handoff succeeded | Task 4, concrete index/query ID trace |
| Reader treats `references`/nearby association as necessity or scenario as a changed decision | Source check must preserve uncertainty and historical scope; mark interpretive defect | Tasks 4/5, negative relation role |
| A/B do not actually have isolated contexts, or the candidate is not indexed at the exact commit | `NOT_RUN`/`INVALID_SETUP`; no simulated fresh-agent success | Tasks 1/3/4, host/session/commit boundary |

---

## Task 1 — Lock source case, provenance and actual execution readiness

**Files:**
- Read: `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, [ontology](../../semantic-architecture/ontology.md), [relations & epistemics](../../semantic-architecture/relations-and-epistemics.md), [knowledge contract](../../../skills/repository-semantic-steward/references/knowledge-contract.md), [first-use readiness precedent](../../normal-use/2026-11-04-independent-inquiry-operation-readiness.md).
- Read: `.sensemaking/knowledge/*.json`, `docs/superpowers/specs/2026-11-05-agent-native-knowledge-graph-reasoning-design.md`, `docs/semantic-architecture/agent-native-graph-viewer-v1.md`.
- Create only in **disposable operator workspace**, not source repo: a compact `ontology-author-reader-case-manifest` holding pins, host capabilities, source candidates, contamination rules and observation disposition.

**Interfaces:**
- Consumes: selected current repository SHA, actual installed Skill/runtime and available independent-agent hosting capability.
- Produces: frozen source-case statement, source/Skill identities, A/B/C execution contexts and a **readiness verdict**. No result/answer key in A/B task materials.

- [ ] **Step 1: Reconfirm the current source baseline.** Record full `git rev-parse HEAD` (not a short name), clean/dirty status, exact source path availability, and whether the new graph-viewer concept is already faithfully represented in reviewed packs. If fully represented, use the same case as a test-only reexpression and flag duplication; never claim production need for it.
- [ ] **Step 2: Resolve the real host.** Record how **two genuinely fresh** coding-agent sessions A and B can run with separate conversation contexts and verifiable original-source access. Record one distinct reviewer C (human or independent agent). Verify host tools are callable rather than merely named in a plan. If unavailable, create a **readiness-only** record and STOP; this is not a failed ontology test.
- [ ] **Step 3: Pin Skill and executable identity.** Inspect `sensemaking-skills --version` and `sensemaking-skills semantic --help`; record installed `using-sensemaking`/Steward origin and corresponding source commit, Python/runtime dependencies, model/host configuration and exact executable. Use the existing [Steward CLI pinning instructions](../../../skills/repository-semantic-steward/SKILL.md) if a global CLI is stale; no unpinned substitutions.
- [ ] **Step 4: Freeze a neutral case.** Set the question to the *role and limits of the offline graph view relative to agent-native control and reviewed knowledge*, with named **source files but no expected conclusions**, source-reading permissions, and no permission to alter source/strategy/schema. Separate evaluator notes from agent invocations and flag that existing docs already discuss the question.
- [ ] **Step 5: Make the start decision.** `READY` only if genuine A/B/C contexts, exact repository/Skill access, isolated branch permission and candidate-consumption observability are available. Otherwise `BLOCKED` with exact environment/permission limitation. Do not start the author session on a merely hypothetical setup.

**Acceptance:** A real executor can say exactly what would be observed and where, and can identify an honest independent host before producing any knowledge candidate.

## Task 2 — Agent A authors the smallest source-grounded candidate

**Files:**
- Create **only in the disposable probe branch**: `.sensemaking/knowledge/ontology-author-reader-probe.json`.
- Do not edit: existing `.sensemaking/knowledge/*.json` packs, canonical strategy/ADR/source, ontology schema/parser or product implementation.
- Read: `skills/repository-semantic-steward/references/knowledge-contract.md` and `.sensemaking/knowledge/product.json`; inspect original sources listed in Task 1.

**Interfaces:**
- Consumes: Task 1 frozen source/host details and installed normal Skills.
- Produces: one *test-only* supported-schema-v1/v2 JSON candidate with source/evidence refs and a compact A trace (source reads, records chosen, discarded alternatives, ambiguities); no merged canonical knowledge.

- [ ] **Step 1: Launch actual fresh author context A.** Give the task at the *outcome level*: “Represent the currently documented role and limits of the new local graph viewer in the smallest source-grounded, retrievable knowledge candidate using the existing Sensemaking ontology.” Permit ordinary Skill/source investigation. Do not enumerate target record IDs, edge predicates, an expected answer or an oracle.
- [ ] **Step 2: Have A inspect existing knowledge before writing.** The trace must show what records already cover, especially the public `using-sensemaking` controller. Avoid redundant duplicates; `NO_NEW_DURABLE_KNOWLEDGE` is legitimate for production even if a reversible test-only candidate is authored for this exercise.
- [ ] **Step 3: Have A author a minimal candidate file.** Use exactly JSON top-level `schema_version`, `claims` and `relations`; each source-linked claim/relation must satisfy the current validator, including supported kinds, endpoint IDs, epistemic/authority status and evidence paths. No global schema change. Prefer the smallest representation that can answer the question (no imposed node quota).
- [ ] **Step 4: Preflight actual proposed content.** In the dirty probe checkout run:

  `sensemaking-skills semantic knowledge-proposal-check --repo . --proposal .sensemaking/knowledge/ontology-author-reader-probe.json --json`

  Capture the JSON, exit code and evidence paths. Mechanical success means `code: SEMANTIC_KNOWLEDGE_PROPOSAL_VALID` and `valid: true`; it specifically returns `semantic_truth_established: false`. An invalid candidate is a useful **authoring failure** unless a minimal bounded repair remains part of the recorded attempt; never silently change test conditions.
- [ ] **Step 5: Freeze writer output before reader exposure.** Save the candidate and A trace, including unresolved source roles and exact original sources. Do not provide the trace, candidate filename/IDs, inferred answers or evaluator notes to B. Record uncommitted → committed boundary for the next task.

**Acceptance:** A genuinely independent A used the existing ontology to produce a source-attributed, proposed candidate, or exposed a concrete authoring/expressiveness failure that can be reviewed. A valid preflight does not establish source meaning.

## Task 3 — Persist exact candidate revision and check retrieval substrate

**Files:**
- Commit on disposable probe branch: `.sensemaking/knowledge/ontology-author-reader-probe.json` **only** (and any branch-local provenance note if genuinely essential; do not change product sources).
- Create only **outside the Git checkout**: a version-labeled `ontology-author-reader-<candidate-sha>.sqlite` index and local CLI output/trace file.
- No GitHub PR / merge for the test candidate. The qualification plan PR is separate.

**Interfaces:**
- Consumes: Task 2 candidate, exact source/candidate Git identities.
- Produces: candidate Git commit SHA and an actual exact-commit indexed snapshot; search and explain observations with original candidate record identities, provenance, and visible truncation/unknowns.

- [ ] **Step 1: Inspect the proposed diff and create a real commit.** Check scope, record IDs, traced evidence and no edits outside the isolated candidate file. Commit the candidate, record full `CANDIDATE_SHA`, keep it separate from the baseline `SOURCE_SHA`. Do not merge it into `main`.
- [ ] **Step 2: Build from committed bytes, not a dirty overlay.** On a naturally clean candidate checkout use:

  `sensemaking-skills semantic knowledge-build --repo . --repository ThorStarlord/sensemaking-skills --target-ref <CANDIDATE_SHA> --db <EXTERNAL_DB_PATH> --json`

  If the active checkout is dirty or not at the candidate SHA, use the existing `--temporary-checkout` flag with the exact candidate SHA. Never commit the SQLite file or treat it as source authority.
- [ ] **Step 3: Demonstrate the candidate is actually retrievable.** Query `semantic knowledge-query --db <EXTERNAL_DB_PATH> --repository ThorStarlord/sensemaking-skills --target-ref <CANDIDATE_SHA> --operation search --term "graph viewer" --json` (or a source-relevant literal term observed in the candidate). Resolve real claim IDs from results; inspect with `--operation explain --subject <ACTUAL_CLAIM_ID> --json`. Record matches, source paths, explicit relations, limits and query outcome. If the candidate is not returned, record **INDEX/RETRIEVAL FAILURE**, not “ontology misunderstood.”
- [ ] **Step 4: Preserve one narrow reader handoff.** Supply B only the target repository identity, exact candidate branch SHA, normal CLI/Skill access and neutral question. The external index may be supplied or B may build it at the same SHA, but the operator must not supply found claim IDs or a writer summary.
- [ ] **Step 5: Recheck no canonical mutations.** Verify that the candidate exists only in the disposable branch and that original source files and shared ontology packs were not rewritten. A successful mechanical index is not a reviewed user-value outcome.

**Acceptance:** A and B can refer to the **same exact committed candidate bytes** and supported indexed search path, without treating the candidate as merged or semantically approved.

## Task 4 — Fresh B reads, interprets, then verifies sources

**Files:** No product/source edits. Only a read-only B session trace, first-pass account, second-pass source-check account and any genuine command output in the disposable operator workspace.

**Interfaces:**
- Consumes: **only** neutral question, original target repository plus candidate SHA, normal installed Skill/CLI access and ordinary source access. Does *not* consume A's transcript, filenames, identifiers, reviewer oracle or expected result.
- Produces: trace of B's spontaneous candidate discovery/use, optional prompted use, independent interpretation, source-verification outcome and uncertainty.

- [ ] **Step 1: Launch B in a genuinely new context.** Record a distinct session ID, host/model/version and its starting task context; confirm no writer message/conversation/answer was inherited and original sources remain accessible. If no independent session exists, STOP `BLOCKED`; do not substitute the author or current assistant.
- [ ] **Step 2: Ask a neutral question.** “From the repository's source-grounded knowledge, what is the new offline graph view meant to do relative to the coding agent, what is implemented, and what is not established?” Do not supply the candidate filename, node/edge IDs, correct answer or explicit step-by-step retrieval instructions.
- [ ] **Step 3: Freeze B's first response and retrieval trace.** Identify whether B actually loaded/retrieved **the test candidate**, exactly which record IDs and original source pointers it used, what unsupported links it declared, and its uncertainty/limitations. A correct answer from ordinary source docs **without candidate consumption** is `CANDIDATE_USE_NOT_DEMONSTRATED`, not a handoff PASS.
- [ ] **Step 4: Optional single neutral discoverability cue.** **Only** if B did not inspect the candidate, the operator may say “Please also inspect reviewed semantic knowledge through the normal repository workflow.” Capture another interpretation. Mark this branch `PROMPTED_USE` separately from spontaneous use; no additional coaching or oracle.
- [ ] **Step 5: Source-check in a second, separately recorded pass.** Ask B to inspect the original design/implementation/ADR sources and identify **supported, unsupported, contradicted and NOT_ASSESSED** parts of the knowledge representation. A reasoned rejection of an invalid authored claim is valid verification evidence; B's agreement with A is not itself correctness.
- [ ] **Step 6: Preserve negative-case boundary observations.** Without giving expected conclusions, review whether B promoted a source citation into truth, ordinary `references` into necessary causality, a hypothetical viewer scenario into a strategic decision, or a merged CLI implementation into verified agent benefit. Record exact claims and sources for any issue.

**Acceptance:** A genuinely fresh reader either consumes and interprets the candidate, or its failure to discover/understand it is observable and attributable. Correct source-only answers and prompted recovery remain distinguishable.

## Task 5 — Independent reviewer adjudicates and performs bounded closeout

**Files:**
- Create **only if a real run occurred**: `docs/normal-use/<actual-date>-ontology-author-reader-first-use.md` on a separate documentation-only branch/PR, or an equally durable source-qualified operator record if repo publishing is not authorized.
- Optionally update the *qualification plan checklist* with actual observations. Do **not** promote a test-only candidate to `main`, alter v1/v2 schema or revise Level 3/4 strategy as automatic follow-up.
- Do not modify authoritative historic source/ADR or the agent-facing prompt to fit the observed answer.

**Interfaces:**
- Consumes: frozen Task 1 case, Task 2 A/record/validator, Task 3 Git/index/query evidence, Task 4 B two passes, and the actual primary sources.
- Produces: an independent five-axis adjudication, narrow observed outcome, source/host identity, failure classification, and warranted `NO_MODEL_CHANGE`/repair question/next separate experiment decision.

- [ ] **Step 1: Give reviewer C source access and the full frozen traces.** C independently inspects the real original source/accepted authority and the **actual** A-authored candidate; do not assume the producer's claims are correct because the proposal checker/index reported success.
- [ ] **Step 2: Evaluate author fidelity independently.** For each pivotal record/edge, check source reference and original meaning, claim status, normative decision versus observed as-built capability, missing/unknown relationships and source revision. Record `AUTHOR_FIDELITY_PASS` only if no material unsupported attribution survives.
- [ ] **Step 3: Verify actual indexed handoff.** Compare exact candidate SHA/DB namespace, returned claim/edge IDs and B's use trace. Mark `MECHANICAL_PASS` separately from `SPONTANEOUS_CANDIDATE_USE` or `PROMPTED_USE`. If a candidate was never consumed, do not credit graph/ontology reading based on a correct general answer.
- [ ] **Step 4: Evaluate reader interpretation and source correction.** Compare B's first-pass description with the candidate, then B's source-checked account against the original sources. Name any conflated authority, invented consequence, missing epistemic qualifier or correct challenge to an A error.
- [ ] **Step 5: Assign an evidence-bounded overall disposition.** Use `OBSERVED_SUCCESS` only if author semantics, mechanical write/index, spontaneous or clearly specified candidate use, semantic interpretation and independent source verification all pass. Otherwise use `PARTIAL` with layer, `FAIL` with source-backed defect, `INCONCLUSIVE` when treatment/trace is ambiguous, or `NOT_RUN/BLOCKED` if the real independent host was unavailable. Do not claim repeatability/generalization.
- [ ] **Step 6: Retain the smallest useful readout.** Record A/B/C distinct sessions, exact Git/Skill/index refs, invoked commands and observed outputs, source-backed conclusions, negative-case check, limitations and next conditional question. Preserve the result even if negative; don't build extra evaluation infrastructure or force a new knowledge pack.
- [ ] **Step 7: Stop or select only warranted next responsibility.** If first-use works, the next question may be an **unfamiliar case** or an ordinary independent DE-A, not automatic ontology expansion. If it fails, identify **discovery**, **authoring**, **schema expressiveness**, **mechanical indexing**, **reading** or **source checking** specifically before proposing a targeted repair. No follow-up implementation is authorized solely by finding a gap.

**Acceptance:** A different reviewer can reconstruct the actual result and its claim ceiling from durable source+trace evidence without trusting an A/B anecdote or treating source-graph availability as proof of creative improvement.

## Exact participant brief boundaries (keep evaluation neutral)

- **A receives:** one practical outcome (“produce the smallest source-grounded, retrievable candidate describing the current local graph viewer's role and limitations using existing ontology”), target branch/source and ordinary Skill access. Do **not** list expected record IDs, types, conclusions, comparator or evaluation rubric.
- **B receives:** neutral source-grounded question, exact candidate SHA and normal tools; **no A transcript, candidate file path or expected answer**. The grader checks where its candidate information actually came from. Any post-response nudge is explicitly recorded as prompted recovery.
- **C receives:** source evidence + A/B raw traces + previously frozen case/evaluation criteria and judges actual fidelity. C is not asked to make the authors' choices retroactively correct.

**Tool/runtime boundary:** A GitHub connector alone does not create a fresh coding-agent session or an installed local CLI execution. When the real host is absent, the proper deliverable is `READY_FOR_EXTERNAL_RUN / NOT_RUN` with the frozen plan, not two simulated agent answers.

## Evidence ceiling and next steps

- `VALID_PROPOSAL` = structural and source-path checks only, *not* a supported semantic assertion.
- `INDEX_QUERY_PASS` = exact-commit persistence/retrieval, *not* proof that a human or agent used the record.
- `B_CANDIDATE_USE_PASS` = one actual consumer recovered and interpreted the record, *not* general retrieval reliability.
- `C_SOURCE_VERIFIED_PASS` = one source-checked exchange in the observed host/context, *not* comparative value or semantic completeness.
- `OBSERVED_SUCCESS` = all applicable first-use dimensions under stated conditions; **not** an improvement claim over source-only or an accepted schema extension.

The viewer exercise, independent Divergent Exploration `DE-A` and a controlled graph-versus-source comparison remain **separate optional investigations**. They need not block this small write/read exercise, nor does this test qualify them.

**Plan closure rule:** Stop after one real A→B exchange and C's verdict, or after the first genuine external/authority blocker that prevents independent observability. A planning-only PR satisfies **planning**, not the observed ontology first-use claim.
