# Cognitive method-learning construction episodes (2026-11-15)

**Status:** construction-track record for issues #860-#864 and #867 under the owner's 2026-11-15 implementation-first authorization. It records **local functional observations** only. It is **not** independent behavioral qualification, a matched comparison, or evidence of cognitive benefit.

**Source baseline:** `origin/main` at `a97439fe` (PR #871 merge). Work branch `claude/cognitive-development-construction`, in a dedicated worktree.

## 1. Functional path for decision-time re-entry (#861) and feedback (#862)

**Episode E1 (local, same context, not independent).** The controller queried reviewed knowledge before deciding whether this program needed any construction change. The queries and their outcomes are recorded in the companion query receipt `.sensemaking/receipts/2026-11-15-cognitive-method-learning-construction.query.yaml`.

| Query | Operation | Result | Outcome |
| --- | --- | --- | --- |
| QY-1 | `semantic workspace-query --operation search --query-text ... --search-kind lesson` | 9 lesson claims. Ranking is distinct literal word overlap. The top hits matched generic tokens (`lesson`, `before`, `re`, `entry`). None addresses method selection. | PARTIAL |
| QY-2 | `context-for --subject src/sensemaking_skills/semantic_architecture/knowledge_retrieval.py` | 28 claims. History includes `lesson:query-completeness-is-evidence` through `component:knowledge-store`, which is the example RECALL names. `contracts` is NOT_ASSESSED. 12 relevance candidates are not established. | PARTIAL |
| QY-3 | `context-for --subject skills/using-sensemaking/SKILL.md` | 11 claims. `owner_verification` is NOT_ASSESSED. | PARTIAL |

**Observed:**

- The file-anchored decision-time path works as RECALL describes. The documented precedent surfaces through the owning component.
- The reviewed knowledge base holds no lesson about **method choice** (when ACT, INQUIRE, CHALLENGE, EXPLORE, VERIFY, ESCALATE or STOP was useful). The nearest candidate is `lesson:pr-review-merge-base-is-scope-evidence`, which its source record itself calls a "candidate methodological caution" about scope measurement.
- Lexical search does not retrieve method-choice precedent for a question that does not share the claim's vocabulary. Its hits on short tokens (`re`, `entry`) are noise. This is documented behavior: a weak match is NOT ASSESSED, not absence.
- Nothing wrote the query receipt automatically. The contract in `skills/repository-semantic-steward/references/query-receipt.md` is manual, and no producer exists under `src/`. Draft PR #797 concerns how query receipts are recorded and is awaiting an owner decision.

**Decision: no code change.** The functional seam exists and works at the public CLI. The observed gap is the absence of methodological content, which an honest source cannot supply without a real method-choice episode. A query-receipt producer would be a new machine contract with no construction-track consumer, and its recording design is owner-pending.

**Feedback (#862), existing chain:** incident -> lesson -> RECALL retrieval has already run once on engineering scope. `incident:pr-review-diverged-tip-scope-20261112` (PR #838, 2026-11-12) led to `lesson:pr-review-merge-base-is-scope-evidence`, and E1 retrieved that lesson. E1 did not apply the lesson to a decision it could change, so its disposition for this episode is `NO_MODEL_CHANGE`. Section 4 covers the one new retained interpretation.

## 2. Harness admissibility (#863): calibration C1, not evidence

**Calibration C1 (non-evidentiary).** One fresh `general-purpose` subagent received a throwaway probe. The probe asked it to report only what was observable in its own context: project instructions, persistent memory, Sensemaking-related Skills, the checkout SHA, its tool-call count and any consultation. It was told not to modify files or run tests. It did not receive any decision task, and it was not offered a Sensemaking entrypoint.

Observed:

- It reported `CLAUDE.md` text in its context, the user's persistent `MEMORY.md` index in its context (with a stale 2026-05 status line), and the user-level Skills `using-sensemaking`, `repository-semantic-steward`, `strategic-repository-analysis`, `strategic-repository-reconciliation` and `strategic-sensemaking-loop`.
- It reported the checkout SHA `a97439fe`, one tool call, and no consultation of Sensemaking knowledge or query tools.
- Its transcript persisted on disk as JSONL under the parent session's `subagents/` folder. It recorded one `Bash` tool use and a `meta.json` naming the model `claude-haiku-5-5`. Telemetry therefore existed after the run, on this host.

Gate check against `docs/experimental-phase-gates.md` (HARNESS READY):

| Criterion | Observed in C1 | Status |
| --- | --- | --- |
| Frozen conditions reproduced (SHA, task, model) | SHA reproduced; model inherited by default, not frozen by the probe | met for this run |
| Required telemetry observable | JSONL transcript with tool uses and request records persisted; model in meta | met after the run, on this host |
| Fresh state, no ambient leakage | CLAUDE.md, MEMORY.md and user-level Skills were present in the subagent | **not met** |
| Agent/evaluator separation | the orchestrator wrote the probe and interprets it | **not met** |
| Responder/escalation transport | not exercised | not assessed |

Execution versus measurement, answered separately (`docs/experimental-phase-gates.md`):

- Can the runtime perform the task? Yes.
- Can it enforce the intended treatment? **No.** A fixed-method arm cannot exclude the repository `CLAUDE.md`, the persistent memory index or the user-level Skills, because they load into every session.
- Can it observe every required measurement? Partly. Transcripts persist, but the arm assignment is not enforced.

**Disposition: NOT_ADMISSIBLE for a matched comparison of experience-informed against fixed-method cognition, in this harness.** HARNESS READY is not met. The smallest remedy I can name, which is not verified, is per-arm configuration isolation together with an oracle-blind evaluator. That remedy belongs to the qualification track.

## 3. Comparison (#864): not run

No evidence-bearing trial exists. The comparison pathway is not built. The instrument gate fails, and a comparator that cannot be enforced would fabricate a matched comparison. The implementation state is **BLOCKED on instrument admissibility**, and the qualification item keeps the comparison open.

## 4. Retained interpretation (#862)

Calibration C1 produced one methodological interpretation that changes how any future comparison must be designed. It is retained as `lesson:subagent-inherits-ambient-context` in `.sensemaking/knowledge/stewardship.json`, learned from `observation:calibration-c1-ambient-context-2026-11-15`, which cites this record. It is scoped to one harness and makes no claim about other harnesses or about cognitive benefit.

## 5. Limits

- E1 is same-context and C1 is same-harness. Neither is independent.
- E1's records are reconstructed from the executed commands and their outputs, not from a live trace.
- No unit test or synthetic evidence test was added or run, under the construction-phase exception in CLAUDE.md. Verification here is source and diff inspection, plus the knowledge proposal check and the receipt validator.
- The stale `MEMORY.md` status line is a finding about ambient context, not a repository defect. It is left unchanged because it is the user's memory, outside this repository.
