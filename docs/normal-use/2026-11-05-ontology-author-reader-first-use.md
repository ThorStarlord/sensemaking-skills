# Ontology author-to-reader first use (2026-11-05)

**Disposition: `PARTIAL`.** Responsible layers: authoring, and reader interpretation before source checking. This is not `OBSERVED_SUCCESS`, because two of the five axes did not pass.

This records one real run of the [qualification plan](../superpowers/plans/2026-11-05-ontology-author-reader-qualification.md) under its [design](../superpowers/specs/2026-11-05-ontology-author-reader-qualification-design.md). It is a first-use observation, not a benchmark. The test candidate is not reviewed knowledge and was not merged.

## Result by axis

Reviewer C assigned these results against the frozen criteria. Its full reasoning and evidence are in [C-verdict.md](2026-11-05-ontology-author-reader-first-use-evidence/C-verdict.md).

| Axis | Result | Why |
| --- | --- | --- |
| Author fidelity | PARTIAL | One as-built clause is false as stated, and one clause carries an overstatement inherited from the sources (both below) |
| Mechanical write and index | OBSERVED_PASS | The proposal check passed on first write. C reproduced the exact-commit build digest and the `search` and `explain` results |
| Reader discovery and consumption | OBSERVED_PASS, `SPONTANEOUS_CANDIDATE_USE` | No cue was sent. Discovery was unprompted but not blind (see Setup limits) |
| Reader interpretation | PARTIAL | The account was correct, but no account from the candidate alone exists, so "before checking originals" was not observed |
| Source verification | OBSERVED_PASS | B found two contradicted clauses, and C reproduced both, narrowing one to the indexed path. All five negative checks hold for the reader |

**Most important limitation:** the run shows that a reader reached and used the record, not that the record produced the reader's understanding. B requested the candidate in the same batch as the original sources and answered after reading both. Only a few fingerprints in B's answer can be credited to the candidate.

## What happened

- **Author A** used only existing vocabulary and wrote [5 claims and 8 relations](2026-11-05-ontology-author-reader-first-use-evidence/candidate-c7eb21d.json) in schema 2. It kept normative limits separate from as-built observations, and it declined to mint an owner decision for the viewer. It also reported real expressiveness gaps, such as no typed "secondary to" and no form for `NOT_RUN`. None of them blocked the candidate, and this run does not warrant a schema change.
- **Persistence:** candidate commit `c7eb21dfc5dc12057300c0bfeb200d659dce89bb` on parent `6f54a4a7eeb2a2101536f3307c37bb55a46dcbca`. The candidate file's sha256 is `378fa6405055a7a9916ac584e3d906af70190e96bf90b6c1c1a984a36cd742dc`. The index holds 225 claims and 225 relations, with digest `10f826f6e5e44b9e63ee46d9381fdb399eaca27448a37176ab8284bcf48fd4dd`. Querying it at another revision returns `NOT ASSESSED`.
- **Reader B** received only the repository, the SHA and the plan's neutral question. It [first answered](2026-11-05-ontology-author-reader-first-use-evidence/B-pass1-answer.md) with "found no contradictions". Its [separately requested source check](2026-11-05-ontology-author-reader-first-use-evidence/B-pass2.md) classified 13 records as 11 SUPPORTED and 2 CONTRADICTED, and it retracted that statement.
- **Reviewer C** checked the sources and raw transcripts independently.

## Defects found

| Finding | Class | Evidence |
| --- | --- | --- |
| The candidate says edge role "is CONTEXT_ONLY for references and contained_in and UNKNOWN otherwise". That holds only on the indexed path; curated views can carry all six roles, and a view with every edge set to `NECESSARY` was accepted | Candidate defect | `src/sensemaking_skills/semantic_architecture/knowledge_view.py:85`, `:21-23`; the guide says "Default edge role" |
| The hypothetical-premise control is unavailable on ordinary indexed exports, though it works on the curated sample because those IDs contain "assumption". The test string is `kind + " " + id`, so the `^hypothesis$` and `^constraint$` branches can never match. C found 0 of 9 nodes eligible in the candidate capability's own neighborhood, and 2 of 191 authored claims eligible overall. B saw the disabled button in a scripted browser run; C derived the button state from source and did not run a browser | **Product defect** (primary); the guide and `STATUS.md` state the feature without this limit (secondary); the candidate repeats it unscoped (tertiary) | `src/sensemaking_skills/semantic_architecture/view_assets/graph_view.html:386`; `docs/semantic-architecture/agent-native-graph-viewer-v1.md:15`, `:80`; `STATUS.md:534` at `6f54a4a` |

Lesser candidate defects, including one clause attributed to the wrong authority and an evidence ceiling that stops before the later green run, are listed in C's verdict. As the plan requires, neither the candidate nor the product was repaired in this work.

## Setup limits

- **Independence is context-level only.** Headless `claude -p` could not authenticate (`OAuth session expired`), so A, B and C ran as fresh Agent-tool subagents. Each has a distinct agent ID and started with only its prompt, but they share a parent session ID, host, model (`claude-opus-5-5`), filesystem and scratchpad. Plan Task 4 asks for a distinct session ID, which this run did not meet. C ruled the setup valid under the plan's "distinct fresh coding-agent contexts" rule.
- **Inherited context.** A and B inherited `CLAUDE.md`, the Skill listing and project memory. C found no viewer content in that inherited context.
- **Shared scratchpad.** A, B and C got the same scratchpad directory, and a listing by B showed A's `check2.*` files by name. No read of them appears, but C calls this a real boundary leak.
- **Precedent on memory.** A repository memory precedent (#552) treats a memory-loaded session as not independent. C treats this as a ceiling, not an invalidation, because the memory holds none of the writer's material.
- **Operator incident.** The installed CLI and Skills were stale, so the operator updated them machine-wide to the source SHA. The first CLI refresh failed on a Windows file lock and left the CLI broken, and A had already been launched in the same batch. The CLI was repaired by copying the pinned packages over the tool directory. While diagnosing the crash, A read the operator's `manifest.md` and `progress.md` (retained here as `operator-manifest.md` and `operator-ledger.md`). The manifest glosses the frozen question, and the ledger named the plan path and C's role, so A knew it would be read and reviewed. No oracle was exposed, and A did not read the plan or spec. A disclosed the read, though C finds that disclosure slightly understated. A's careful hedging cannot be credited as natural behavior. The attempt was kept because rerunning would select outcomes. C treats this as lowering the ceiling, not as invalidating axis 1. C's matching digest shows the repaired CLI did not affect the index.
- **Reader cues.** B's first moves came from inherited instructions, before any result was visible. It then saw the operator's commit message ("disposable, do not merge") and the plan-mandated filename before deciding to read the candidate. After that read was issued, B searched for and saw qualification plan text, including its own question, and disclosed this, though it wrongly said its first search surfaced that text. That made it test-aware before it answered, which plausibly raised its diligence in both passes. The pass 2 prompt also asked explicitly for overstatements.
- **Installed CLI not exercised by the reader.** B ran the CLI from worktree source, so this run does not show a reader using the installed CLI.
- **Protocol gap.** The spec asks for a representation pass before source checking, but the plan's neutral question does not ask for one and bars step-by-step instruction.

## Claim ceiling

**Warranted:** in one run, on one self-referential repository, with one host and model using fresh-context subagents, one agent authored a schema-valid candidate with the existing ontology. The candidate was largely but not wholly source-faithful, and it persisted and was retrievable at the exact commit. A second agent, unprompted but not blind, read and used it alongside the originals, then found and correctly rejected two false or overstated clauses.

**Not warranted:** that the candidate caused the reader's understanding, retrieval reliability, value compared with source-only reading, independence beyond context level, repeatability, transfer to other repositories or hosts, any browser or user benefit from the viewer beyond B's own scripted session, semantic approval of the candidate, or any schema need.

## Conclusion and next step

Production model decision: `NO_MODEL_CHANGE`. The candidate stays on local branch `claude/ontology-author-reader-probe-20261105`, which was never pushed. This directory keeps a byte-identical copy so the result can be checked.

Conditional next questions, none authorized by this result:

1. Repair `graph_view.html:386` and qualify the guide and status statements as an ordinary bounded fix.
2. Only if the interpretation question matters: run an unfamiliar case on a tree without the plan, with a neutral commit message and a representation step recorded before source reading. Reconcile the spec and plan on that step first.

Ontology expansion and further evaluation infrastructure are not warranted.

## Retained evidence

[The evidence directory](2026-11-05-ontology-author-reader-first-use-evidence/) holds the candidate, A's trace, B's two passes, C's verdict and the operator's manifest and ledger, all unedited. These are test records, not reviewed knowledge, and they should not be read as architectural authority. The raw JSONL transcripts stay in the operator workspace and are not published, because they contain inherited private project memory. C's verdict cites them by line number, so those citations cannot be checked from this repository alone.

**Verification:** the only product commands run were `knowledge-proposal-check`, `knowledge-build`, `knowledge-query` and, by B and C, `knowledge-view-export` and `knowledge-view-render`. Local unit and synthetic tests: `NOT_RUN`, per the current construction rule.
