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

The original returning and comparison runs remain **UNASSESSED**. Their GitHub
branches preserve the prepared installations, with no later result commits.
Local Claude logs contain no matching runs, and the CLI is signed out. Browser
access was stopped by the computer-use tool's URL-verification restriction.
Absence of committed results is not evidence that a cloud run failed or stopped.

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

## Remaining work and conclusion

First-use artifacts, source-bound persistence, mechanical validity and some
path retrieval are established. Independent retrieval of the retained records
is observed in an interrupted local session. Completed consequential reuse,
comparative superiority, adaptive end-to-end closure, long-term compounding
and portability beyond the tested environments remain unestablished.

When workspace credits are restored, recover the original Claude comparison
transcripts if possible. Otherwise conduct a new, explicitly preregistered pair
under the same question and assess its completed answers; do not silently treat
these interrupted sessions as complete or alter the existing pre-registration.
The original cloud outcomes may already exist and should be checked before
duplicating them. No additional product repair is justified solely by this
resource failure.
