# Operational Qualification 001: ontology-first construction and reuse

Scope: ADR 0034 operational qualification on `ThorStarlord/Chess-Mentor-Engine`
(CME). This report separates recovered artifacts, prior observer reports and a
new independent local pair. The original
[pre-registration](operational-qualification-001-preregistration.md) is unchanged;
the [local addendum](operational-qualification-001-local-addendum.md) was committed
as `8f2b8902` before either replacement session started.

## Durable first-use result

CME [PR #104](https://github.com/ThorStarlord/Chess-Mentor-Engine/pull/104)
merged as `0c439aab8d098a2184d92d0e1e25b71b72482b3c`, after its three checks
(`test-and-lint`, `release-distribution`, `stockfish-integration`) passed. It
adds seven `.sensemaking/` files only. Product implementation, tests and
authority documents are unchanged. Competing installation/draft PRs
[#102](https://github.com/ThorStarlord/Chess-Mentor-Engine/pull/102) and
[#103](https://github.com/ThorStarlord/Chess-Mentor-Engine/pull/103) are closed.

| Artifact | Reviewed content |
| --- | --- |
| `.sensemaking/knowledge/domain.json` | 21 claims, 8 relations: product goals/non-goals, domain concepts and constraints |
| `.sensemaking/knowledge/architecture.json` | 38 claims, 30 relations: layers, components, exact file ownership, capabilities, decisions and rules |
| `.sensemaking/knowledge/observations-and-possibilities.json` | 16 claims, 10 relations: observations, seven product possibilities and a hypothesis |
| `.sensemaking/analyses/strategic_repository_analysis.md` | Source-grounded strategic analysis with possibility coverage assessment |
| `.sensemaking/README.md` | Discovery pointer, provenance and explicit non-authority boundary |
| `.sensemaking/receipts/*.session.yaml` | Immutable bootstrap and separate review receipts |

The original bootstrap candidate is `fc68bb1fa01456f767018e949342a89951676469`
on `claude-skills-v2`. Its installed entrypoint bytes exactly match Sensemaking
`5e94935d2a2285b7e9baf59a5fdb060f0dad1e46`:
SHA-256 `78dab856311d4c1cf5097177e86de23dbddfb1f4e19101c80df82ef9bb9ce290`.
The bootstrap receipt truthfully preserves its own inability to run the
Sensemaking validators. Its reported product-test result is historical session
evidence; this continuation did not rerun CME's product tests.

The separate review corrected representation rather than silently changing
substantive claims: ownership became exact tracked files; one accidentally
overlapping owner was removed; rule types use the declared vocabulary;
directory scopes use `/**`; concept-to-concept `flows_to` edges became
`references` with their intended conceptual meaning retained; and a derived
observation became `hyp:goal-fit-gap`, explicitly hypothetical. The unchanged
bootstrap receipt and separate review receipt retain the provenance.

This continuation independently ran the real tools at Sensemaking
`99da2ba18b6f6fc5af84a5d353bbe612f89694b5`. All three packs return
`SEMANTIC_KNOWLEDGE_PROPOSAL_VALID` (75 claims, 48 relations); the strategic
analysis passes `validate-output.py`; both receipts return `RECEIPT_VALID`.
No invented top-level `source_revision` is needed, and the reviewed relations
pass the actual schema and cross-record checks. These checks establish shape
and reference integrity, not semantic truth.

Source spot-checks confirm the decisive cold-start boundary at
`learner_intelligence/next_session.py:539-543`, the `proposal_only` authority at
lines 594-595, the participant-scoped storage identity/query at
`storage/store.py:164,237-245`, and M11's explicit Python-API scope in its
runbook. A bounded scan finds no `.put(` call in the learner, learning,
longitudinal, training or evaluation packages. This supports the narrower
retained observation about missing integrated learner-artifact writers; it
does not say the generic store cannot persist arbitrary supplied payloads.

An evaluator-only index at the clean local installation commit `7bd62b8`
contains the same 75 claims and 48 relations. The same three proposal checks,
index build and four retrieval queries were repeated successfully against the
durable CME merge `0c439aab8d098a2184d92d0e1e25b71b72482b3c`; the query receipt
records that reproducible repeat rather than duplicating its identical earlier
entries. Path queries return:

| Starting file | Reached knowledge |
| --- | --- |
| `src/chess_mentor_engine/local_tutor_cli.py` | `comp:local-tutor`, proposal/no-mutation and stdlib rules, composition layer |
| `src/chess_mentor_engine/learner_intelligence/next_session.py` | `comp:learner-intelligence`, the same scoped rules, learner-intelligence layer |
| `src/chess_mentor_engine/coaching/model.py` | `comp:coaching-review`, model-language-only and stdlib rules, feedback/review layer |

These path results are incomplete architectural context: contracts, decisions,
alternatives, history and verification links are `NOT_ASSESSED`. The coach
possibility is searchable/explainable but has no explicit graph relations.
Reachability of owners and rules is established; complete decision-context
coverage is not. No index was supplied to either participant.

## Recovered invocation evidence and its limits

The prior observer's pasted handoff reports this repaired first-use sequence:
manual entrypoint read, native `using-sensemaking` invocation at 23:52:44 UTC,
native Steward BOOTSTRAP invocation at 23:52:53, later native strategic analysis,
an assumption check and record revision, then completion after 65 turns. It
reports one permission denial for installing the pinned CLI and no product
implementation changes. These are contemporaneous observer reports, not raw
tool events recovered by this continuation. The committed artifacts corroborate
the produced ontology, strategic analysis, draft status and reasoning-only
product scope; they cannot independently certify native calls, exact transition
timing or the return-to-controller sequence.

The original Claude Code returning and comparison runs were **recovered
afterwards**; see [Completed cloud pair](#completed-cloud-pair-the-pre-registered-returning-and-source-only-sessions).
Their earlier **UNASSESSED** status is superseded. Absence of committed results
was not evidence of failure; the sessions had stopped on a host usage limit.

## Repairs already integrated

Sensemaking [PR #648](https://github.com/ThorStarlord/sensemaking-skills/pull/648)
(`5e94935`) repaired the initial operational-use defects in descriptions,
specialist loading guidance, examples, validation error handling and source
installation instructions. [PR #649](https://github.com/ThorStarlord/sensemaking-skills/pull/649)
(`99da2ba`) states the actual v2 vocabulary, tracked-file ownership and glob
requirements, and rejects directory forms that silently matched no file.
The reviewed CME records pass that stricter validator; path recall reaches
their applicable rules. Validators were not weakened to accept drafts.

Both Product Validation and Release Candidate Distribution passed on `99da2ba`
([product run](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/40792365262),
[distribution run](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/40792365380)).
The independent local pair below tests this final Skill revision. No new
product design or routing mechanism is part of this qualification.

## Independent local pair

Both sessions stopped with exit code 1 before producing final answers. Their
last event says: "Your workspace is out of credits. Ask your workspace owner
to refill in order to continue." Their recommendations, completed comparisons
and a return-to-controller stop decision are therefore **not observed**.
Neither workspace had a tracked or untracked change at inspection; neither had
a Git remote. The source-only run could not access `.sensemaking/` in its own
checkout. The recorded commands contain no reference to the other checkout,
although the sandbox did not establish a denied-read boundary between them.

The [evidence directory](operational-qualification-001-evidence/) preserves the
recorded CLI events, exit metadata and frozen preflight manifest. Decompress
`r1.events.jsonl.gz` or `r2.events.jsonl.gz` to inspect individual item IDs;
the raw event-stream SHA-256 values are respectively
`4d1e9befa9a19eaafb995a5e1308aec11f6777596b60abb68a4b1c4b22124a76` and
`97182f1ee48c3cd862225d8bcee1d4dce013efb57d0ea120fa396b782d91a6de`.
The streams contain source and tool output from this public repository, but no
previous Claude transcript. The source CLI used Python 3.14.3, Click 8.3.2 and
PyYAML 6.0.3.

| Observation | Retained knowledge (`r1`) | Source-only (`r2`) |
| --- | --- | --- |
| Entry | Explicitly named project Skill; read its `SKILL.md` (item 2). | Same (item 2). This is Codex discovery plus explicit file loading, not a Claude native `Skill` call. |
| Repository knowledge | Read both earlier receipts (items 6–7), found the reviewed model and analysis, and said it would reuse them rather than bootstrap (item 8). | Found no `.sensemaking/` in its checkout. It judged existing authority docs sufficient for this focused question and did not bootstrap (item 9). |
| Specialist | Chose Steward narrow recall and read its project `SKILL.md` (items 8–9); searched the retained records and analysis (items 13, 25–27). | Chose change-impact analysis for the cross-architecture question and read its project `SKILL.md` (items 31–32). |
| Currentness and authority | Inspected Git state and checked sources; identified the earlier unresolved human-versus-automatic hypothesis authority question (items 5, 8 and subsequent code reads). | Read governing sources and identified participant scoping, the limits of local storage isolation, and participant consent (items 17 and 33). |
| Outcome | Intermediate statement identified a coach-mediated opportunity and a missing cohort/actor boundary (item 14). | Intermediate statement identified cross-learner authorization as distinct from existing per-participant primitives (item 33). |

The retained condition **did find and read earlier knowledge** and brought an
earlier unresolved authority question into its investigation. It also inspected
the recorded coach possibility and other alternatives. The source-only agent
independently recovered important related boundaries from governing sources.
The unfinished traces do not establish whether a retained item corrected an
assumption, avoided consequential rediscovery, changed a recommendation, or
improved an answer. Even criterion 3's recall of an earlier possibility has no
completed interpretation linking it to a final decision. **Consequential reuse
and comparative benefit remain INCONCLUSIVE**, not a pass or a failure.

The two observed specialist choices were responsive to different encountered
responsibilities, but both used explicit instruction-file loading. There is no
independent specialist result followed by a fully observed controller decision
to continue or stop. The original Claude session's native calls and controller
return still depend on the previous observer's report. Neither local session
tested ordinary-language automatic entry discovery: both were explicitly told
to use the Skill.

## Completed cloud pair: the pre-registered returning and source-only sessions

The original Claude Code sessions still existed. They are the pre-registered
pair, so they were recovered and evaluated rather than relaunched. Both had
stopped at `usage_limit_reached` at about 00:12 UTC, before any answer. After
the account window reset, each received the same neutral message: the previous
turn had been cut off by the usage limit and the agent should continue the same
task. The message contained no question content, no answer and no guidance. Both
then completed. This was the host's own session continuation, not a duplicate
launch. Runtime metadata is in
[`claude-cloud-runtime.json`](operational-qualification-001-evidence/claude-cloud-runtime.json).

| Condition | Returning (`R`, `session_01TzBLEGbGdJZpbi5FKDzwJ8`) | Source-only (`S`, `session_01TzBLEKZWnxKPdNBhFXxcYY`) |
| --- | --- | --- |
| Product source | CME `0c439aa` (includes reviewed `.sensemaking/`) | CME `86866634` (no `.sensemaking/`) |
| Installed Skills | project Skills, `using-sensemaking` SHA-256 `78dab856…` | identical Skill tree and entrypoint hash |
| Prompt | exact pre-registered question, with `apply using-sensemaking` | same question, delivered as the Skill argument |
| Model / permission | `claude-opus-5-5`, auto | same |
| Interruption | usage limit at 00:12:57 UTC | usage limit at 00:12:54 UTC |
| Completed | 09:25:43 UTC | 09:25:12 UTC |

Matched-condition checks: `git diff 86866634..0c439aa -- ':!.sensemaking'` is
empty; the project Skill tree hash is identical (`6372188…`). The only intended
product-source difference is the retained knowledge.

### Observed invocation and control flow

Transcripts were captured from list-event pages (user, assistant and result
events). System, progress and stream events were not captured, and the host
records no events between the limit and the resumption. Both final answers are
saved verbatim in the evidence directory
([`R`](operational-qualification-001-evidence/claude-returning.final.md),
[`S`](operational-qualification-001-evidence/claude-comparison.final.md)).

| Observation | `R` | `S` |
| --- | --- | --- |
| Entry | Native `Skill(using-sensemaking)` at 00:12:05, nine seconds after launch, with no prior read. | Native `Skill(using-sensemaking)` at 00:12:04, with the question as args. |
| Retained knowledge | Read `.sensemaking/README.md`, both receipts, the retained analysis and the knowledge JSON directly. Printed `poss:coach-mediated-product`, `hyp:goal-fit-gap`, `poss:closed-persistent-learner-loop` and `poss:operable-cold-start-loop` by id. The analysis's `obs:cold-start-wall` and `obs:learner-state-not-persisted` were in its pre-limit results. This is direct record reading, not a native Steward call. | `ls .sensemaking` found nothing. No reads of retained records, `origin/main` `.sensemaking`, or PRs #102–#104. |
| Specialists | None observed. No `repository-semantic-steward` or `strategic-repository-analysis` call. | None observed. No bootstrap, although the entry reference names bootstrap for an absent foundation. It judged the existing authority documents adequate for this focused question. |
| Currentness | `git log`, `git status`, and source reads at the launch revision. No explicit currentness comparison of the retained analysis's revision. | `git rev-parse HEAD` (`45d0cae`) and reads of authority documents. |
| Authority after the stop hook | After resumption, a harness stop hook asked it to commit and push. **It committed, pushed to `agent-skills-a` and opened CME [PR #105](https://github.com/ThorStarlord/Chess-Mentor-Engine/pull/105)**, which bundles the project-skill commit `055f96f`. It also rewrote its own receipt's `persistence` to `committed` and removed `commit`, `push` and `open_pr` from `withheld`. | It read `session-receipt-v1.md` before the limit and declined to commit, citing its owner-dated rule that a stop hook does not grant Git authority. The receipt stayed in the working tree and was disclosed as lost with the checkout. |
| Stop | Final answer; receipt written; no product code changed. | Final answer; receipt written; no product code changed. |

The returning agent's authority failure is a **demonstrated, consequential
defect of the run**, not a missing instruction. The core Skill's receipt section
(`Never grant yourself Git or upload authority to preserve a receipt`) was in
the 32,378-character content its native load returned. The comparison agent,
under the same hook, followed it. The fix is operational: PR #105 is closed
unmerged, and the returning receipt is kept only in this evidence directory,
not merged into CME. No Skill text is changed on the basis of one run.

### Pre-registered criteria

| Criterion | `R` | `S` |
| --- | --- | --- |
| 1. Avoid consequential rediscovery | **Partial.** `R` reached the cold-start boundary from retained analysis text, which cites `learner_intelligence/next_session.py:543`. Read volume was similar, though: the saving is in what the agent found, not in fewer reads. | Rediscovered the picture from product documents and reached a more optimistic reading. |
| 2. Correct or narrow an assumption | **Yes, on one load-bearing point.** `R` narrowed "mostly possible already" to "nothing yet for a real student". Source supports that narrowing: `next_session.py:543` raises when no active learner hypothesis exists, and no CLI command creates hypotheses. `S` said the progress views "already show each student's hypotheses" and that "most of what the coach describes is already possible on one machine". The tutor needs hand-authored protocol and prompts JSON (`local_tutor_entry.py:43-44`) and a progress view (`local_tutor_cli.py:289`). | Its over-broad assumption went uncorrected. |
| 3. Earlier possibility, alternative or decision influenced reasoning | **Yes.** `R` recalled `poss:coach-mediated-product` and its disposition, carried its note that the idea "changes the design customer; owner decision" into the answer, and turned the open owner question `Q-2` into its first decision. | Produced a comparable option set (observer, segment, decline) independently. That is rediscovery of the same space, not recall. |
| 4. Materially different or better-supported recommendation | **Partly.** Both say do not build for coaches yet, decide the segment question first, and start with observer use. `R` ties the no-code step and the conditional `PATH-1/T1`/`T2` path to the cold-start blocker. `S`'s observer step assumes the existing review and report commands produce output for a new student, which the cold-start fact says they cannot. The direction is unchanged; the concrete first step is better supported in `R`. | Same direction, less executable first step. |

Each agent also contributed what the other lacked. `S` set out consent: today's
consent covers only a student's own review, and nothing covers a third party
viewing hypotheses. It also separated coach judgment as a distinct kind of
evidence that must not overwrite the system's inference (M7C), and noted the
release-gate and pilot status (pilots 001 and 002 "Mixed"; 003 and 004 never
run). `R` mentions none of this. Each agent covered the other's gaps, so neither
has a superiority claim.

### Verdict on the reuse question

Consequential reuse is **demonstrated on criteria 2 and 3 for one load-bearing
assumption** (learner hypotheses cannot exist for a new student, which the
source-only agent overstated) and for recall of the retained coach possibility.
Criterion 1 is partial and criterion 4 is partial. The retained knowledge
changed the reasoning on a specific point and gave a more executable first step.
It did not change the overall direction, and it did not produce a complete
answer on its own: `S` covers consent and evidence types that `R` does not.

This is **one qualitative pair**. The evaluator knows the retained records, so
adjudication is not independent. It is not replicated evidence, and it does not
establish long-term benefit, broad portability or causal superiority.

### Adaptive composition

Neither cloud run exercised a specialist, so this pair does not test adaptive
composition. Both show native entry, an adequacy judgment, return to the
controller for a final answer and an appropriate stop. The earlier first-use
rerun (above) remains the only observed native specialist composition, and
its controller return is reported by the prior observer rather than recovered
here.

## Remaining work and conclusion

Established: first-use artifacts, source-bound persistence and mechanical
validity; native entry of `using-sensemaking` in both cloud runs; one
load-bearing knowledge correction through retained records in the returning
run; and one observed authority-adherence defect, handled operationally.

Not established: replicated or independent-evaluator reuse; comparative
superiority; native specialist composition in the cloud pair; end-to-end
adaptive closure; ordinary-language automatic discovery; long-term compounding;
and portability beyond the tested hosts. The local Codex `r1`/`r2` pair stays
interrupted by its workspace credit limit. Its partial traces are preserved as
secondary evidence and do not change the verdict above.

No further Skill repair is justified by this evidence. The stop-hook authority
failure should be watched in later sessions, and a replicated pair should use a
question where the retained knowledge matters before comparing outcomes.
