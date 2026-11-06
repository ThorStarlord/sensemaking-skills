# Unfamiliar-Case Semantic Transfer Qualification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to execute this plan task-by-task. Checkboxes record real actions, not hypothetical runs. The operator must launch **genuinely separate agent sessions**, not emulate independent agents by role-playing in one conversation.

**Goal:** Observe whether existing Sensemaking knowledge records preserve source-faithful meaning across distinct coding-agent contexts, with the reader's representation-only interpretation frozen before original-source verification.

**Architecture:** Use a source-pinned, unfamiliar companion-memory case in `ThorStarlord/atlas-midgard`. Agent A writes one minimal **proposed** v1/v2 knowledge file on a disposable branch; the existing CLI validates and indexes its exact commit. Distinct-session Reader B gives a source-free interpretation and then a separately frozen source-checked answer. Independent Reviewer C adjudicates both the authoring and transfer; the candidate is never automatically reviewed or merged.

**Tech Stack:** Git/worktrees, fresh coding-agent host sessions and isolated scratchpads; existing installed `using-sensemaking` / `repository-semantic-steward` guidance; Python >=3.11; pinned Sensemaking Click CLI `knowledge-proposal-check`, `knowledge-build`, `knowledge-query`, SQLite outside both repositories. No new code, data schema, tests, web viewer, benchmark framework or dependencies.

**Spec:** [Independent Semantic Transfer — Unfamiliar Atlas Case](../specs/2026-11-05-unfamiliar-case-semantic-transfer-design.md).
**Planning baselines:** Sensemaking `cb0101f4acd9d07102fd58db57825217a2a66441` (merged viewer repair #767); Atlas `2b3556e47daa6110d01c045432e23bf4e041ba49`. Re-pin at the actual run start; do not silently substitute moving main.
**Execution status:** `PLANNED / NOT_RUN`. This document is not an agent observation, independent qualification or authorization to merge the Atlas candidate.

## Global Constraints

- The **only intended empirical claim** is a bounded, one-case observation of source-faithful authoring and independent **pre-source** interpretation. The previous [PARTIAL first-use](../../normal-use/2026-11-05-ontology-author-reader-first-use.md) is historical evidence, not a pass or a clean control.
- Honor the target's current authoritative rules, and Sensemaking ADR 0029/0031/0034, the current `knowledge.py` vocabulary and `skills/repository-semantic-steward/references/knowledge-contract.md`. No new ontology type, predicate, schema version, authority, plan execution or code repair.
- **Planning and operator materials stay outside the Atlas target checkout and all A/B participant workspaces.** Do not publish an answer key, source-scope conflict list or the prior case's expected answer where a participant can search it.
- A, B and C require **distinct genuine host session identities** and separate scratchpads. Do not silently substitute shared-parent subagents after failed authentication; use `NOT_RUN/BLOCKED`. Record inherited memory and initial context; inherited content that gives the expected case answer invalidates interpretation evidence.
- Use a **pinned isolated environment** for the exact Sensemaking CLI and Skills. Do not mutate global user tools or stop unrelated processes. No experimental SQLite, working notes or transcript files inside the Git-authored target knowledge directory.
- The proposed Atlas file `.sensemaking/knowledge/companion-continuity.json` is **not** reviewed knowledge. Never merge it or edit canonical Atlas packs, code, historical docs or profiles as part of this observation. Do not run Godot against the live save directory.
- A mechanically valid proposal or indexed record is not semantically correct. An ordinary `references` edge is not causal necessity. Preserve declared normative intent, as-built code, historical package status, source evidence and `NOT_ASSESSED` separately.
- The reader is **prompted to represent authored knowledge before checking sources**; do not score that as spontaneous discovery. Source access in pass 1 invalidates the interpretation observation, even if B later answers correctly.
- Record every missing capability, failed command, skipped verification, early source exposure and fidelity defect without replacing the original attempt. This is a first-use qualification, not an experiment to select favorable outcomes.
- Construction policy forbids adding/running local unit or synthetic tests in this Sensemaking phase. Existing product CLI commands are the real workflow being observed; preserve hosted CI on any docs PR.

## Review Focus — Failure cases that must be adjudicated

| Risk | Required observation | Task |
| --- | --- | --- |
| Historical Package 16 design is treated as current runtime truth without checking code | Author/reviewer distinguishes source era, decision status, actual source behavior and unrun tests | 2 / 5 |
| B reads original code or documents before freezing its first account | Interpretation is `NOT_OBSERVED/CONTAMINATED`, never repaired by repeating the same attempt | 4 / 5 |
| Current authored packs already express the case, or participant memory contains its answer | Report duplication/contamination and re-freeze before dispatch or stop | 1 / 5 |
| Branch, imported CLI, index DB and B's candidate refer to different Git snapshots | Treat as `MECHANICAL_FAILURE` or `INVALID_SETUP`; reject apparent retrieval pass | 1 / 3 |
| A or B turns `references` into necessary support or a record into owner ratification | Explicitly reject in author/reader interpretation or independent review | 2 / 4 / 5 |

---

## Task 1 — Freeze real target, clean host and measurement boundary

**Files:** Create only outside Git: `<OPERATOR_ROOT>/case-manifest.md` and `<OPERATOR_ROOT>/case-criteria.md`. No source changes.

**Interfaces:** Produces the exact target/tool/Skill SHAs, neutral case question, session-isolation proof, source inventory and `READY` or `NOT_RUN/BLOCKED` verdict consumed by Tasks 2–5.

- [ ] **Step 1: Inspect authoritative baselines.** Record full Atlas `git rev-parse HEAD`, current clean/dirty status, branch/worktree identity, Sensemaking pinned CLI SHA and the effective instructions for both repositories. Verify all proposed source files exist at the exact target revision.
- [ ] **Step 2: Assess originality before exposure.** Inspect Atlas's existing six `.sensemaking/knowledge/*.json` packs for material coverage of companion Shared Memory. Check available task history and initial prompt/memory context for prior exposure. If this case is already materially covered or spoiled, choose one alternative real unfamiliar case, record the reason and freeze it before opening any A/B session. Do not cherry-pick after an outcome.
- [ ] **Step 3: Freeze participant-neutral question.** Use: “In Atlas, how should companion Shared Memory relate to Saga History and durable player progression, and what is supported by the current repository versus specified or not assessed?” Keep reviewer source inventory and any preliminary source tensions in `case-criteria.md`, not in A/B prompts.
- [ ] **Step 4: Verify host isolation.** Demonstrate that the selected host can spawn A, B and C with separately identifiable sessions and scratchpads; make trace capture possible. Do not treat different agent IDs under the same parent host session as the stronger separation required here.
- [ ] **Step 5: Verify executable without global mutation.** Use a fresh isolated virtual environment populated from a clean Sensemaking checkout at the frozen SHA. Record exact interpreter, package import origin, dependencies, installed Skill paths/digests and successful `sensemaking-skills semantic --help`. Do not force-reinstall a locked global tool.
- [ ] **Step 6: Freeze validity criteria.** Write five independent axes, contamination stop rules, source-scoping negative checks, and a privacy/redaction policy; date and hash the evaluator criteria **before** Agent A starts.
- [ ] **Step 7: Decide readiness.** Continue only if A/B/C genuine isolation, target sources, Git permissions, candidate retrieval and essential trace observability are available. Otherwise stop `NOT_RUN/BLOCKED` with a concise readiness record. **Do not launch Author A while repairing tooling.**

**Acceptance:** One reproducible manifest with genuine readiness and no leaked oracle. An honest blocker ends execution without claiming ontology failure.

## Task 2 — Author A proposes the smallest source-grounded knowledge

**Files:** Create only on a new disposable **Atlas** local worktree/branch: `.sensemaking/knowledge/companion-continuity.json`. Do not edit existing knowledge packs or product files.

**Interfaces:** Consumes Task 1 frozen target/Skill identity and neutral question. Produces candidate bytes, A's raw source-reading trace, record provenance and proposal-check output; it does **not** produce a reviewed truth oracle.

- [ ] **Step 1: Launch genuinely fresh A.** Give the neutral question and outcome-level request to represent the answer in minimal source-grounded authored knowledge using existing ontology. Do not supply target record IDs, the evaluator's source expectations, findings, previous experiment transcripts, or an expected answer.
- [ ] **Step 2: A inspects repository reality.** Have A use normal target instructions and Steward RECALL guidance, existing packs, accepted design documents and decisive current code. Require it to distinguish historical proposals and source-reading evidence from actual execution evidence.
- [ ] **Step 3: A writes the minimal candidate.** Top-level fields are exactly `schema_version`, `claims` and `relations`; use existing v1/v2 kinds/predicates, stable local IDs, evidence refs to tracked Atlas files, and scoped epistemic/authority status. Report real expressiveness limits instead of inventing a schema extension.
- [ ] **Step 4: Run existing proposal preflight.** From the **Atlas** worktree: `sensemaking-skills semantic knowledge-proposal-check --repo . --proposal .sensemaking/knowledge/companion-continuity.json --json`. Capture status, complete JSON and errors. Passing means syntactic/contract validity only; correct supported content remains a reviewer question.
- [ ] **Step 5: Freeze uncorrected A output.** Record candidate SHA-256, A session ID, source reads, choices, uncertainties, discarded alternatives and proposal-check result. Do not edit the candidate to match reviewer expectations, and do not pass A's trace/answer to B.

**Acceptance:** A legitimate independently authored candidate or an attributable concrete authoring failure. Do not promote either to a product-model decision.


---

## Task 3 — Commit candidate, reproduce exact-commit indexing and prove candidate retrieval

**Files:** Modify only the disposable Atlas candidate worktree to commit the single new file. Create `<OPERATOR_ROOT>/index/<CANDIDATE_SHA>.sqlite` and `<OPERATOR_ROOT>/mechanics/` outside both Git checkouts. Do not publish or merge the candidate branch.

**Interfaces:** Consumes frozen candidate bytes and pinned CLI from Tasks 1–2. Produces exact candidate Git SHA, digest, valid index/query outputs and an operator-to-B handoff containing only **repo identity, target commit, neutral question and ordinary CLI/DB access**, not answer/record IDs.

- [ ] **Step 1: Check diff and provenance.** Confirm the candidate branch is based on the frozen Atlas SHA, and the only changed tracked file is `.sensemaking/knowledge/companion-continuity.json`. Record `git diff --name-status <BASE_SHA>` and candidate file checksum. Ensure no source file or existing reviewed pack was modified.
- [ ] **Step 2: Commit candidate with ordinary neutral metadata.** Commit only the JSON file with a descriptive, non-experimental subject such as `docs(knowledge): propose companion continuity representation`. Record full commit SHA, parent SHA, branch and clean status. Do not use `probe`, `test`, `expected answer`, `disposable` or qualification language in participant-visible commit subject/filename.
- [ ] **Step 3: Build exact committed snapshot.** Run `sensemaking-skills semantic knowledge-build --repo . --repository ThorStarlord/atlas-midgard --target-ref <CANDIDATE_SHA> --db <OUTSIDE_DB_PATH> --include-repository-structure --json` from a checkout at the exact clean commit (or use the supported `--temporary-checkout`). Capture process exit, full JSON, digest, claim/edge totals and target revision. Never put SQLite in the repository.
- [ ] **Step 4: Prove search retrieves the candidate.** Run `sensemaking-skills semantic knowledge-query --db <OUTSIDE_DB_PATH> --repository ThorStarlord/atlas-midgard --target-ref <CANDIDATE_SHA> --operation search --term "Shared Memory" --json`. Record actual candidate claim IDs returned. A generic source-only match that does not include the candidate is not a pass.
- [ ] **Step 5: Prove explicit relation retrieval.** Run `sensemaking-skills semantic knowledge-query --db <OUTSIDE_DB_PATH> --repository ThorStarlord/atlas-midgard --target-ref <CANDIDATE_SHA> --operation explain --subject <REAL_RESULT_ID> --json`, using an ID **actually returned by Step 4**. Confirm cited source paths, relation IDs, record status, truncation and limits are present as advertised. No mechanical operation establishes source entailment.
- [ ] **Step 6: Freeze a non-leading B handoff.** Provide only repository identity, exact candidate SHA, neutral question, installed ordinary guidance and supported CLI/DB location. Do not include A's trace, candidate filename, record IDs, index search hits, source-oracle notes or prior output. Record a hash of the handoff and the exact candidate bytes.

**Acceptance:** Same candidate bytes are committed, indexed and queryable at the same exact revision, with no canonical Atlas mutation or semantic-approval claim. A failed build or inconsistent SHA is a **mechanical** finding and blocks B.

## Task 4 — Fresh Reader B: freeze meaning before revealing original sources

**Files:** Create only private operator artifacts: `<OPERATOR_ROOT>/reader/B-pass1.md`, `B-pass1-trace`, `B-pass2.md`, `B-pass2-trace` and metadata. B must leave the target checkout unchanged.

**Interfaces:** Consumes Task 3 non-leading handoff; produces independently observed candidate use, **pre-source** interpretation and a separate source-verification account. No additional answer key or A summary is permitted.

- [ ] **Step 1: Launch a genuinely new session B.** Verify a distinct host/session ID, worktree identity and scratchpad from A. Capture the exact initial task prompt and inherited memory/instructions. If B can see A's scratchpad, author transcript, qualification specification or reviewer expected conclusions, stop `INVALID_SETUP` rather than silently overlooking the leak.
- [ ] **Step 2: Establish source-read boundary.** Prefer a host permission gate or source-occluded, read-only first-pass workspace with the existing query data. If this is unavailable, instruct B explicitly not to open any original source document or code until the second turn, capture **all** tool calls and reject pre-source claims if a source read happens. Do not fabricate a boundary through a drafted transcript.
- [ ] **Step 3: Issue exactly one knowledge-first question.** “Using the repository's authored semantic knowledge at the supplied exact revision, explain how Atlas companion Shared Memory relates to canonical Saga History and durable progression. Before inspecting original documents or code, identify the explicit claims and relationships, their source references, statuses, and what the knowledge does not establish. Stop after this account.” No file name, claim ID, expected conclusion, source-oracle snippet, test label or checklist of desired findings.
- [ ] **Step 4: Freeze the first interpretation and trace.** Record B's actual retrieved candidate record IDs/relations and the order of queries/file opens; preserve its full answer **before** any source-authorization prompt. Judge whether its statements faithfully represent *the candidate*, including provenance, necessary versus contextual edges, declared versus observed facts and explicit uncertainty. If candidate was never consumed, record `CANDIDATE_USE_NOT_DEMONSTRATED` regardless of plausibility.
- [ ] **Step 5: Handle an early source read transparently.** If the trace shows original docs/code were accessed before the first answer, classify the interpretation axis `NOT_OBSERVED/CONTAMINATED`. Preserve the first run; do not retry that same evidence cell for a cleaner-looking outcome. A separate future attempt must be labeled new evidence.
- [ ] **Step 6: Unlock source inspection in the same B session.** Only after the first answer is frozen, request: “Now inspect the original current and historical sources at the exact revision. For each consequential representation, classify `SUPPORTED`, `CONTRADICTED`, `UNSUPPORTED` or `NOT_ASSESSED` and explain any correction, including authority/time scope.” Do not give B the evaluator's oracle or tell it which claims are wrong.
- [ ] **Step 7: Freeze the source-checked answer.** Record B's original source paths actually opened, corrected claims and unsupported inferences, differences from pass 1, and whether it improperly promoted a source pointer into necessity or owner authority. Capture command and session evidence; record the model and host version.

**Acceptance:** Two independently timestamped, source-attributed B accounts with a verifiable boundary, or a precise `PARTIAL` / `NOT_OBSERVED` / `INVALID_SETUP` result. This run is **PROMPTED_REPRESENTATION**, not proof of natural unprompted discovery.


---

## Task 5 — Reviewer C independently adjudicates the five claims

**Files:** Create only private `<OPERATOR_ROOT>/review/C-verdict.md` plus referenceable source/trace excerpts. Do not change participant material or code.

**Interfaces:** Consumes the frozen criteria, A candidate/trace, exact index outputs, B's two frozen answers/traces and the original Atlas sources. Produces one source-grounded verdict with five distinct axes and explicit claim ceiling.

- [ ] **Step 1: Launch genuinely fresh reviewer C.** Record C's separate session and scratchpad IDs. C receives the frozen evaluator rubric, actual candidate, A/B frozen traces and the original target repo at the exact source/candidate revision; C does not retroactively revise the participant instructions.
- [ ] **Step 2: Check author fidelity record by record.** Inspect decisive Atlas decision, implementation, migration and code sources at their exact revision; distinguish declared design, historical package status, current as-built behavior and tests that were written but not executed. For each material claim and relation, classify source support, scope, epistemic/authority classification, missing nuance and contradiction.
- [ ] **Step 3: Reproduce the mechanical handoff.** Independently compare candidate content hash, parent/commit SHA, target index key/digest, search and explain record IDs and relation roles. Reject a wrong-revision index or noncandidate-only query result as a pass.
- [ ] **Step 4: Audit independence and order.** Inspect A/B host IDs, scratchpad visibility, inherited memory, candidate discovery, first-source-read timestamp and first-answer timestamp. Distinguish intentional first-pass knowledge prompting from a purported spontaneous discovery. An early original-source read excludes `OBSERVED` pre-source interpretation.
- [ ] **Step 5: Compare the three meanings without conflation.** Judge (a) **what A actually encoded**, (b) **what B said the candidate meant before sources**, and (c) **what the original sources support**. A false candidate that B accurately paraphrases is a faithful *reading of an error*, not a successful transfer of true repository meaning.
- [ ] **Step 6: Check all five negative controls.** Record concrete evidence on historical-vs-current status, `references`/necessity, declared-vs-observed authority, missing-as-`NOT_ASSESSED` and premature source exposure. Do not turn any mechanically valid record into verified source truth.
- [ ] **Step 7: Assign the frozen disposition.** Mark author fidelity, mechanical write/index, candidate consumption, pre-source interpretation and independent source review separately. Use overall `OBSERVED_SEMANTIC_TRANSFER_IN_ONE_CASE` only if all five pass and session isolation is intact; otherwise identify `PARTIAL`, `FAIL`, `INCONCLUSIVE` or `NOT_RUN/BLOCKED` and the causal/measurement layer. No numeric score or claim of creative advantage.

**Acceptance:** A reviewer-verifiable verdict that could reject the author or reader, grounded in original evidence and complete observation chronology. C's approval is not a license to merge the candidate.

## Task 6 — Preserve a narrow readout, close the experiment and stop

**Files:** If Task 5 actually ran, create a new `docs/normal-use/<ACTUAL-DATE>-unfamiliar-case-semantic-transfer.md` on a separate **Sensemaking documentation branch**. Optionally create a small redacted `...-evidence/` directory with only indispensable provenance and tool-call excerpts. Do **not** add the raw transcripts if they contain private inherited memory. Do not edit historical readouts to improve their verdict.

**Interfaces:** Consumes Task 5's frozen verdict and private traces. Produces a concise durable record sufficient for a later agent to reconstruct exactly what was observed and what was not; leaves no product/model work authorized implicitly.

- [ ] **Step 1: Prepare privacy-safe evidence.** Preserve private unedited raw A/B/C traces in the operator workspace. Extract only decisive session/command chronology, record IDs, source paths, source-verification differences and digest evidence for publication. Redact secrets and unrelated project memory; disclose any gap preventing independent audit of line references.
- [ ] **Step 2: Write the evidence-bounded readout.** Record exact Atlas/Sensemaking SHAs, candidate checksum, agent-session/Skill/CLI identities, source paths, observed commands/exit codes, B's two accounts, C's five-axis verdict, contamination, negative results, and explicit `NOT_RUN` items. Distinguish native semantic meaning from reviewer inference.
- [ ] **Step 3: Retain candidate without promoting it.** Confirm the Atlas proposed JSON exists only on a disposable local branch and has no remote PR or `main` merge. Do not repair A's candidate in place. A separately warranted real knowledge proposal may use a future reviewed path, not this evidence cell.
- [ ] **Step 4: Complete documentation PR if authorized.** Review source/diff for only the readout and necessary sanitized evidence, follow Sensemaking's `CLAUDE.md` PR and hosted-CI rules, merge if allowed and verify the merged SHA. A readout is not proof that the target knowledge became canonical.
- [ ] **Step 5: Reconcile learning without expanding scope.** State whether the observed limit belongs to **authoring fidelity**, **mechanical indexing**, **reader interpretation**, **source verification**, **isolation**, or a **real ontology expressiveness gap**. Prefer `NO_MODEL_CHANGE` unless a concrete, independently warranted model change emerges; do not implement one as part of this task.
- [ ] **Step 6: Stop at one observation.** Deliver the disposition, evidence links, limitations and the smallest justified follow-up. Do not rerun for a favorable result, initiate a source-only creative comparison, broaden to a benchmark, or claim cross-repository generality without a separately selected responsibility.

**Acceptance:** One honest, reproducible-in-scope observation (or a documented readiness blocker), with no unauthorized Atlas/product mutation. The user's request for this **plan** is satisfied before any such execution.

## Frozen participant handoff boundaries (execution operator only)

- **A receives:** target repo/SHA, normal installed Skill guidance and the neutral authoring question. No reviewer expectation or target record ID.
- **B receives:** target repo at candidate SHA, first-pass knowledge-only instruction, normal available CLI/DB and neutral question. No A transcript, candidate filename/IDs, `case-criteria.md`, prior analysis answer or source hints. B receives the source-verification request **only after** pass 1 is frozen.
- **C receives:** original Atlas sources, frozen criteria, candidate A actually authored, exact CLI outputs and A/B immutable traces. C must identify unsupported source claims and possible test invalidity, not merely agree with A/B.

## Evidence ceiling and handoff

This plan is deliberately one-case and does not build a statistical comparison, new orchestration runtime, new knowledge graph representation, automatic source gate, or general assessment infrastructure. If the host cannot provide distinct sessions and traceable pre-source interpretation, **STOP `NOT_RUN/BLOCKED`** and retain the readiness evidence. One observed success would justify the **case-level semantic-transfer claim only**; it would not demonstrate that accumulated knowledge improves new product-goal discovery or architecture decisions.

**Planning deliverables:** this plan and its linked design spec. **Empirical execution:** `NOT_RUN` until an external coding-agent host actually completes the tasks above.
