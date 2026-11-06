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
