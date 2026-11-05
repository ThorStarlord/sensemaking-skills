# C verdict: ontology author-to-reader first-use exercise

Reviewer: C, fresh-context Agent-tool subagent, same host and model as A and B (Claude Code, claude-opus-5-5). Date 2026-11-05.
Candidate: `c7eb21dfc5dc12057300c0bfeb200d659dce89bb` (parent `6f54a4a7eeb2a2101536f3307c37bb55a46dcbca`), `.sensemaking/knowledge/ontology-author-reader-probe.json` ("the candidate").
Criteria applied as frozen: spec sections 1, 4, 5, 6; plan Review Focus, Task 5 and Evidence ceiling.
Paths are relative to `H:/codex/worktrees/oar-reader` unless absolute. `T:n` means line n of the named JSONL transcript. `B:n` is `raw/B-transcript-full.jsonl`, `A:n` is `raw/A-transcript.jsonl`.
Nothing in the checkout was edited (`git status --short` empty at start and after my runs). My index and exports are in my scratchpad.

## Overall disposition

**PARTIAL.** Responsible layers: **authoring** (a false as-built clause, and an inherited overstatement) and **reader interpretation before source checking** (not observed, because of the run's protocol). `OBSERVED_SUCCESS` requires all five axes to pass and two did not.

| Axis | Result |
| --- | --- |
| 1. Author fidelity | **PARTIAL**, not `AUTHOR_FIDELITY_PASS` |
| 2. Mechanical write/index | **OBSERVED_PASS** (`MECHANICAL_PASS`) |
| 3. Reader discovery/consumption | **OBSERVED_PASS** (`SPONTANEOUS_CANDIDATE_USE`, no neutral cue), not blind |
| 4. Reader interpretation | **PARTIAL**: account correct, but "before checking originals" not observed |
| 5. Reviewer source check | **OBSERVED_PASS** (`C_SOURCE_VERIFIED_PASS`) |
| Negative checks | 1-5 hold for the reader. Check 1 has a candidate-side weakness; check 5 limits credit |
| Setup validity | Valid at context level, disclosed limits. Not `INVALID_SETUP` |

**Most important limitation:** the exchange shows a reader reached and used the record, not that the record produced the reader's understanding. B issued the candidate read in the same assistant message as reads of the original sources, and the first frozen answer came after those reads, with most parts attributed to originals. The candidate's own interpretive contribution is visible only in a few fingerprints.

## 1. Author fidelity: PARTIAL

The structure of the candidate is good. Normative limits (`con:graph-view-secondary-read-only`, `declared`, `document`) are separated from as-built behaviour (`observation:graph-view-boundaries-in-source`, `observed`, `code`) and from evidence state (`observation:graph-view-evidence-ceiling`). A correctly declined to mint an owner decision or a `decided_by` edge. But one authored as-built clause is false as stated, and it bears on a negative check, so the plan's "no material unsupported attribution survives" test is not met.

### Material defects

**D1. Edge-role clause, candidate defect, material.** Candidate line 62, under "the view code enforces only mechanical boundaries": "edge role is CONTEXT_ONLY for references and contained_in and UNKNOWN otherwise". Status `observed`, authority `code`.
- True only for the indexed path: `knowledge_view.py:85`, `_edge`.
- The validator accepts all six roles: `knowledge_view.py:21-23`, and the check at about `:233`. It states it accepts "explicitly curated" views (`:186-189`).
- The guide says "**Default** edge role" (`agent-native-graph-viewer-v1.md`, section 5). A dropped "default".
- The candidate's own component record says the code also takes curated JSON (line 24).
- Reproduced: the repository sample has 3 `SUPPORTING` / `SOURCE_DECLARED` edges. A copy with every edge set to `NECESSARY` rendered with exit 0, `SEMANTIC_GRAPH_VIEW_RENDERED`.
- A read the whole file (A:42) and the guide, so this is an authoring error, not a source problem. It matters because a reader relying on the record would over-trust role labels in curated views, which is the distinction negative check 1 protects.

**D2. Scenario clause, inherited overstatement.** Candidate line 7: the page "lets a person ... try a temporary hypothetical premise". See section 4 for the reproduction. The clause is `declared` with document authority, and it accurately reports `agent-native-graph-viewer-v1.md:15`, `:80` and `STATUS.md:534`. So it is not misattributed. It is unscoped, however, and A had the regex in front of it: trace item 7 reads `graph_view.html:386` as "a small widening" and says "kind hypothesis or constraint" is eligible. That reading is wrong; the code narrows. A flagged an oddity, misread it and left it out of the candidate. Primary fault is product and source; the candidate carries it.

### Lesser defects, not material alone

- **Misattributed clause.** Candidate line 79, "A text search of tests/, .github/ and scripts/ finds no reference", sits in a record with authority `STATUS.md`, evidence `STATUS.md` and the guide, and a ceiling of "Records what the documents state". Neither document says it. It is A's own observation. The clause itself is true (my grep is empty).
- **Understated evidence ceiling.** The record stops at the failed run. `STATUS.md:536` also says the receipt repair came in the next PR, and Product Validation succeeded on `6f54a4a` (`gh run list`, reproduced). A trace item 5 knew of the STATUS sentence. A reader could wrongly infer the suite was still red.
- **`decision_changed` on the constraint.** "Rejects ... a host-integrated action trigger" is safe only as a silent trigger (design `:216`). Design `:159` leaves host integration "optional later, never a prerequisite or silent background execution". This is an author inference presented inside a `declared` record. None of the four listed phrases appears in the cited sources (my grep is empty), though each has source support in other words (design `:17`, `:19`, `:216`).
- **`requires_capability`.** The bare predicate overstates for render, which reads a supplied JSON. The `scope` attribute discloses this correctly (`semantic_cli.py:364-378`).
- **`scenario and copy state live only in page memory`.** Omits the user-triggered clipboard exit (`graph_view.html:448-450`). Immaterial.
- **"create-only"** is a pre-write existence check, not atomic (`semantic_cli.py:315`, `:367`). Immaterial.

### Checked and supported

| Record | Result | Basis |
| --- | --- | --- |
| Capability: export, render, bounded, secondary, copy-back | Supported | `semantic_cli.py:310-340`, `:364-378`; guide `:3`, `:9`; design `:17-19` |
| Capability ceiling: merged via #761, browser and benefit not established | Supported | `gh pr view 761`: merged, `e38b4156`; `STATUS.md:536`; guide section 6 |
| Component record, `owned_paths` | Supported | `knowledge_view.py`, `:269-271`; `claim_ceiling` consistent with A's calls (A ran only proposal check) |
| Constraint body | Supported | guide `:18`, section 4 and 5; contract `:95`; design `:17`, `:19`; CLI doc `:524` |
| `authority_note`: document, not owner | Supported, and correctly conservative | design `:3` reports approval in conversation; no ADR mentions the viewer (grep of ADR 0029, 0031, 0034, `CONTEXT.md`, strategy) |
| Truth and action flags rejected | Supported | `knowledge_view.py:107-108`, `:199-200` |
| Output refused under `.sensemaking/knowledge` | Supported | `semantic_cli.py:319-322`, `:371-374` |
| HTML: no fetch, XHR, remote script, `innerHTML` | Supported by text search | only comment `graph_view.html:177`; not run by me in a browser |
| No entailment check; `SOURCE_DECLARED` without inspection | Supported | `knowledge_view.py:54-59`, `:186`; contract `:31` versus `:84` is a source conflict A noted in its trace |
| #761 head `37809b7` results | Supported | `gh run view`: 41996212144 and 41996212110 success, 41996212049 failure; failed log "1 failed, 3634 passed", the receipts test |
| Eight relations | Mechanically valid, source-supported at scope | predicates in `knowledge.py:51-54`. `constrained_by con:agent-owns-semantic-control` is the design's application of ADR 0029 (`:55`), which never names the viewer; the scope note says so |
| `references decision:ontology-first...`, `governedBy` | Acceptable | design `:5` says "Governing product"; ADR never names the viewer and the attribute says so. B's criticism that `governedBy` sounds strong is fair but a style point |

Vocabulary: no invented kind or predicate. A's expressiveness gaps (no typed "secondary to", no negative-limit type, no `NOT_RUN` form) are real, were reported, and blocked nothing. No schema change is warranted by this run.

## 2. Mechanical write/index: OBSERVED_PASS

All reproduced by me from worktree source at the exact commit, with an external DB:
- Candidate bytes equal A's Write (A:107, exact string match). sha256 `378fa640...2dc` matches `source_sha256` in the operator's search output. `git diff 6f54a4a7 c7eb21df` touches only that file. Commit is on the local probe branch only: no remote ref, not an ancestor of `origin/main`.
- `knowledge-proposal-check`: exit 0, `SEMANTIC_KNOWLEDGE_PROPOSAL_VALID`, 5 claims, 8 relations, `semantic_truth_established: false`, `head_sha` `c7eb21df`.
- `knowledge-build`: exit 0, 225 claims, 225 relations, digest `10f826f6e5e4...`, identical to `raw/T3-build.json`. That matters because the operator's CLI had been repaired by overlay copy (progress.md lines 7-9). The matching digest shows the repair did not affect the index.
- `search --term "graph viewer"`: `cap:source-pinned-graph-view`, `con:graph-view-secondary-read-only`, same as operator. `explain`: 9 claims, 8 relations, ID sets identical to `raw/T3-explain.json`, not truncated.
- The operator's own SQLite also answers `explain` for the constraint record.
- Namespace: querying the same DB at `6f54a4a7` returns "has not been indexed; NOT ASSESSED", so the index does not serve another revision.

Ceiling: exact-commit persistence and retrieval only.

## 3. Reader discovery and consumption: OBSERVED_PASS, SPONTANEOUS, not blind

### Order from the raw transcript

1. **B:1**, 21:15:37. Prompt has repository, SHA, plan-mandated question, "normal Skills and CLI tools". No filename, IDs or answer.
2. **Inherited before any tool call** (B:5-7, B:13): `CLAUDE.md` naming `.sensemaking/knowledge/*.json` and the Steward's RECALL path, the skill listing, and project memory. A search of the first 14 lines finds no viewer content, candidate name, or A material.
3. **First assistant message** `msg_011CgkUU9L...` (B:18, B:20, B:21): Bash with `git log` and `ls .sensemaking/knowledge`, a repo-wide topic grep, and loading `repository-semantic-steward` for RECALL. These three share one message ID, so all were chosen **before any result was seen**. Neither the filename nor the commit message can have caused them.
4. **Results** (B:19, B:22, B:24): commit subject "test(probe): ontology author-reader candidate (disposable, do not merge)", the filename in the listing, and 17 grep hits with the candidate as the only knowledge file.
5. **Second assistant message** `msg_011CgkUUks...` (B:34-B:45), issued as one batch: Read candidate, viewer guide, design, receipt; Grep aimed by name at the qualification plan and spec; `git show HEAD`; grep of `.sensemaking/knowledge`. The candidate is first in the batch, but it was not read before originals in any decision sense.
6. **B:52**: "The only reviewed viewer records sit in the disposable HEAD commit, so I'm checking those claims ... then testing retrieval". **B:57**, **B:65**: build, search and `explain --subject cap:source-pinned-graph-view`. Indexed retrieval was a later check, not the discovery route.
7. **B:74**, 21:17:08: frozen first answer, identical to `raw/B-pass1-answer.md`. It names the path and `con:graph-view-secondary-read-only`. **B:75**, 21:17:48: second-pass request. The only user turns are B:1 and B:75. **No neutral cue was sent.**

### Classification

Criteria: uses the candidate through "ordinary indexed query or direct authored record", names IDs or source, not handed the answer. Met, by direct authored record first and indexed query after. `SPONTANEOUS_CANDIDATE_USE`, not `PROMPTED_USE` and not `SOURCE_ONLY_CORRECT`.

Use is more than opening the file. Fingerprints in the first answer:
- "a required step, an authoring tool, a trigger for actions, or evidence for a conclusion" tracks the constraint's `decision_changed` attribute (candidate line 55). That list appears in none of the sources I grepped.
- "ADR 0034 doesn't mention it, according to the candidate record" is explicit attribution.
- B's search of exactly `tests .github scripts` (B:57) copies the candidate's scope.

### What each cue contributed

| Cue | Contribution | Assessment |
| --- | --- | --- |
| Inherited `CLAUDE.md` and Steward listing, and "source-grounded knowledge" in the plan's question | Sent B to the knowledge directory and Steward before any result | Main route. Ordinary instructions, as the spec intends |
| Topic grep | Candidate is the sole knowledge hit, by content. Baseline `6f54a4a7` has no viewer record (`git grep` empty) | Independently sufficient; filename not needed |
| Filename (plan-mandated) | Visible before the Read decision | Salient; cannot be separated from the grep hit, and hidden thinking blocks prevent resolving it |
| Operator commit message (not plan-mandated) | Visible before the Read decision. Gave "disposable" and exposed the exercise | Did not cause the first retrieval moves. Plausibly contributed to the batch aiming at qualification docs and to B's caveat. Operator disclosed it and I treat it as a real aid |
| Qualification plan text | B targeted it deliberately. Shown at B:43, **after** the candidate Read was issued: plan `:45`, `:52`, `:55`, `:71`, `:115`, `:146`, spec `:10`, `:23-25` (long lines omitted). Includes B's own question at `:115`. No negative checks or oracle conclusion | Cannot have caused discovery. Made B test-aware before its answer. B disclosed it, with one slip: "my first search surfaced" the question, whereas the first search returned only filenames (B:22) and the text came from B:43 |

So: unprompted, as the frozen rule defines it, but neither blind nor cue-free. Salience of the candidate in this tree is high because the plan mandates the name, the plan sits in the tree, and it is the only record on the topic. No retrieval reliability claim follows.

## 4. Reader interpretation: PARTIAL

### First answer compared with the candidate

Faithful: primary/secondary role, the limits, authority weaker than an ADR, declared versus implemented versus not established, no benefit evidence. It kept both "plain `references` is not a necessary premise" and "graph miss means `NOT_ASSESSED`". It flagged the records as unmerged probe content.

Why this is not a pass:
- **"Before checking originals" did not happen.** Spec section 5 asks for the distinctions before checking originals, and section 4 asks pass 1 to summarize assertions, explicit relationships, source IDs and unknown or contextual edges. B read the candidate in the same batch as the guide and design, then read the code and ran the CLI before answering. No candidate-only account exists. Relationships were never summarized in pass 1: one claim ID, "all five viewer claims", no edges. The plan's neutral question (`:115`) does not ask for that summary and the plan forbids step-by-step instruction, so this is mainly a **protocol gap** between spec and plan, not a reader error. The behaviour itself, reading sources at once, is what the Steward's RECALL path teaches.
- **Own-evidence confounding.** B's "Relied on" lines credit originals and its own runs for "implemented" and "not established"; only the first section names a candidate record. "Its CLI path works" comes from B's run, not the candidate, which says nothing was executed. Correctly bounded by B.
- **Adopted the overstatement.** B repeated the scenario capability unscoped and wrote "found no contradictions", though it had read `knowledge_view.py`. It then correctly retracted this in pass 2. On edge roles, B was better than the candidate from the start ("indexed edges only").
- Small imprecision: "inspection aid for the coding agent", while sources describe a human inspecting. The body corrects this.

No collapse of source versus inference, `references` versus necessity, or interaction design versus owner authorization was observed. Had pass 1 been candidate-only and shown the same account, this axis would pass.

### Source-checked account compared with the sources

B's pass 2 is accurate and materially better than the record. Counts check out: 13 records, 11 SUPPORTED, 2 CONTRADICTED; 36 clauses, 32 / 2 / 2. It identifies what A got wrong and what A got right. B ran beyond reading, using a browser the spec said was unnecessary (`spec section 4`). That was B's own choice; the key finding is reachable by source reading alone.

### B's two CONTRADICTED findings, reproduced

**Finding 1, scenario clause. B is correct on the facts; I would narrow the label.**
- `graph_view.html:386`: `/(^hypothesis$|^constraint$|assumption|premise)/i.test(node.kind+" "+node.id)`. The test string always contains a space, so the two anchored branches are dead. Reproduced in Node: `hypothesis hypothesis:x` false, `constraint con:graph-view-secondary-read-only` false, even with empty id false, `observation historical:20261024:assumption1-revision` true.
- My export of this neighborhood: 0 of 9 nodes eligible, including both `constraint` records. Over 191 authored claims: 2 eligible (`observation:strategy-assumptions-drift-commands`, `poss:assumption-aware-opportunity-ecology`), neither a premise by kind; 0 of 12 hypotheses, 0 of 2 constraints. Exports carry empty `comparisons` and `scenarios`. Help text at `:398` promises "assumption/hypothesis/constraint", and the contract says a shared premise is a `hypothesis` claim (`knowledge-contract.md`, Product possibility section), which confirms the intent.
- Not universally false: the curated sample works, because its IDs contain "assumption". So: **contradicted on the guide's main indexed path, true on the curated path**. B's table scopes it exactly that way ("for ordinary indexed exports"). I did not run the page in a browser; button state follows from `:395` and the handler guard.
- **Classification: product defect (primary)**, dead regex branches. **Source defect (secondary)**: guide `:15`, `:80` and `STATUS.md:534` state the feature without the limit. **Candidate defect (tertiary)**: faithfully declared but unscoped, and A misread the line.

**Finding 2, edge-role clause. B is correct.** Reproduced as D1 above. **Classification: candidate defect.** Sources are not at fault: the guide says "Default" and the validator's docstring states its scope. Not a product defect in itself, since accepting curated roles is the documented design, though the absence of any check on `NECESSARY` is a design limit worth knowing.

## 5. Source verification and negative checks: OBSERVED_PASS

I independently checked pivotal claims and both of B's rejections, and both rejections are preserved above as failures of the record, not repaired. A and B did not end up agreeing on a misrepresentation: they did in pass 1 on the scenario clause, and B's own pass 2 corrected it.

| Check | Result | Evidence |
| --- | --- | --- |
| 1. `references` is not necessity | **Holds for reader.** Candidate weakened by D1 | B answer "a plain `references` edge isn't a necessary premise"; pass 2 keeps `references` as pointers. Mine: indexed `references` edges are `CONTEXT_ONLY`, others `UNKNOWN`. Forged `NECESSARY` curated view accepted |
| 2. Declared decision is not benefit; export is not a new owner decision | **Holds** | A used `document` authority; B "no evidence of ... benefit", "authority is weaker"; design `:3`, guide `:3`, `STATUS.md:536` |
| 3. Scenario never changes knowledge or triggers work | **Holds** at source level; browser not run by me | guide `:18`, `:92`, `graph_view.html:402`, `:425-426`, `semantic_cli.py:319-322`; B keeps it as an invitation to investigate; checkout clean after B's runs |
| 4. Missing result is `NOT_ASSESSED` | **Holds** | Candidate and B state it. A left layer membership `NOT_ASSESSED`. Build `limits` and my wrong-ref query return `NOT ASSESSED` |
| 5. Source-only correctness cannot be credited to the candidate | **Holds, applied as a limit** | Only the fingerprints in section 3 are credited. Everything else in B's answer is treated as source-derived or confounded |

The plan's four misleading-success conditions: no invented kind or predicate; the authored normative/observed split survives except D1; no source-only correct answer; no `references` or scenario promotion.

## Validity of the setup

**Separation.** A and B have distinct `agentId`s, and each begins with only the operator's prompt, so no parent conversation was inherited. B's transcript has no reference to `oar-operator` or `oar-author`. B-pass1 is an exact prefix of the full transcript.

Limits on it:
- **Not separate host sessions.** All agents share session ID `7d85f11d...`, and plan Task 4 Step 1 asks for a distinct session ID. Spec section 3 warns against "running this same assistant twice". Headless launch failed (`raw/smoke.err`), and the operator ruled on it and disclosed. The plan's operative rule is "distinct fresh coding-agent contexts", and the transcripts satisfy that, so I do not call this `INVALID_SETUP`. Independence is context-level only: same model, host, parent and filesystem.
- **Shared scratchpad.** A, B and C get the same directory. B's listing at B:66 showed A's `check2.*` by name. No read of them appears. No effect found, but a real boundary leak.
- **Inherited context.** Both inherited `CLAUDE.md` and project memory. Memory has no viewer content. A repository memory precedent treats a memory-loaded session as not independent (#552), and B flags the same. I treat that as a ceiling, not an invalidation, because the plan bars inheriting the writer's material and this is none.
- **Installed identity.** Both Skills match the checkout byte-for-byte (`diff -rq` empty); uv receipt rev `6f54a4a7`. B actually ran the CLI from worktree source, so the installed CLI path was not exercised by the reader.

**Contamination incidents.**
1. **A read `manifest.md` and `progress.md`** (A:63), 21 seconds after starting, during an operator-caused CLI crash. Its headers said operator-only. A disclosed this. A's disclosure is slightly understated: "did not contain the frozen question text" is literally true, but manifest line 10 glosses the question ("viewer role/limits rel. to agent control and reviewed knowledge"), and the ledger named the plan path and C's role. A did not read the plan or spec (A:72 shows filenames only; no Read). No oracle was exposed. **Effect:** A knew it would be read and reviewed, so the careful hedging cannot be credited as natural behaviour, and A is not an unaware author. **Does not invalidate axis 1**, which I judged against sources. Rerunning would have selected outcomes, so the operator's ruling not to rerun was right.
2. **CLI breakage and overlay repair.** No effect on axis 2 (digest reproduced). A's proposal-check attempts came after repair.
3. **Operator commit message.** See section 3. Weakens "spontaneous" as a measure of natural salience. Does not change the classification under the frozen rule, which is defined by the neutral cue.
4. **B's targeted read of qualification text** (B:42-43). Disclosed by B. No answer key exposed. Makes B test-aware, which plausibly raised its diligence in both passes. **Does not invalidate axis 3**, since the Read was already issued. It weakens how far B's vigilance can be generalized.
5. **Pass 1 and pass 2 boundary.** The timestamped boundary is clean (21:17:08 versus 21:17:48), but pass 1 already contained source reading. This is the reason axis 4 cannot pass.
6. **Pass 2 prompt** asks for overstatements explicitly. Neutral on content, but it invites critique. B's result is reproducible regardless.

No incident invalidates an axis. Incidents 1, 3 and 4 lower the ceiling.

## Claim ceiling

Warranted: in one run, on one self-referential repository, using one host and model with fresh-context subagents, one agent authored a schema-valid candidate with existing ontology, which was largely but not wholly source-faithful. It persisted and is retrievable at the exact commit. A second agent, unprompted but not blind, read and used it alongside originals, and in a second pass found and correctly rejected two false or overstated clauses.

Not warranted: that the candidate caused the reader's understanding; retrieval reliability; value compared with source-only reading; independence beyond context level; repeatability; transfer to other repositories or hosts; any browser or user benefit from the viewer beyond B's own scripted session; semantic approval or merge of the candidate; any schema need.

## Warranted next responsibility

1. **Operator:** retain the readout (plan Task 5 Step 6), including this negative result. Do not merge, promote or repair the candidate. Production model decision for this run: `NO_MODEL_CHANGE`.
2. **Surface to the owner, separately:** the product defect at `graph_view.html:386` and the unqualified scenario statements at guide `:15`, `:80` and `STATUS.md:534`. This finding does not authorize the fix (plan Task 5 Step 7); an ordinary bounded repair would need its own authority.
3. **Only if the owner wants the interpretation question answered:** a separate optional run on an unfamiliar case, with a tree that does not contain the plan, a neutral commit message, and a representation step explicitly recorded before source reading. The spec and plan would need reconciling on that step first. Not automatic.

Not warranted: ontology expansion, or further evaluation infrastructure.
