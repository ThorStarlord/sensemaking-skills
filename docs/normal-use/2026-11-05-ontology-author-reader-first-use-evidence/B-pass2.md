# Pass 2: graph-view knowledge records checked against original sources

Repository: `ThorStarlord/sensemaking-skills`, checkout `H:/codex/worktrees/oar-reader`, commit `c7eb21dfc5dc12057300c0bfeb200d659dce89bb`.
Records checked: `.sensemaking/knowledge/ontology-author-reader-probe.json` (5 claims, 8 relations). That file was added by HEAD, whose commit message says "disposable, do not merge".
Checkout state: `git status --short` was empty after all checks.

All paths below are relative to the checkout unless absolute. "Probe" means the file above.

## How I classified

- Each of the 13 records gets one classification: the worst classification among its material clauses. A record marked CONTRADICTED can still be mostly right; the clause tables show which part fails.
- SUPPORTED means the original sources support the record. Caveats about wording, attributes or emphasis are listed separately and do not change the class.
- Attributes are treated as part of the record, but free-text scope notes that disclose a limit count in the record's favor.

## Counts

| Classification | Records (of 13) |
| --- | --- |
| SUPPORTED | 11 |
| UNSUPPORTED | 0 |
| CONTRADICTED | 2 |
| NOT_ASSESSED | 0 |

Clause-level results, claims only (36 clauses in the tables below): SUPPORTED 32, CONTRADICTED 2, NOT_ASSESSED 2, UNSUPPORTED 0.

## What I ran beyond reading

Everything ran from worktree source (`PYTHONPATH=src`, bytecode writing off), with output in my scratchpad. This is not an installed wheel.

- `knowledge-build` at HEAD to an external SQLite file: 225 claims indexed.
- `knowledge-query explain` on `cap:source-pinned-graph-view`: 9 claims, 8 relations, `worktree_clean: true`.
- `knowledge-view-export` at depth 1 (HTML) and depth 2 (JSON, 32 nodes, 45 edges, all 32 nodes `SOURCE_DECLARED`).
- `knowledge-view-render` on the repository's sample JSON, and on a copy I edited so every edge role was `NECESSARY`. The edited copy was accepted.
- Refusal paths: re-export to an existing file; output to `.sensemaking/knowledge/`; and, in a scratch directory, output to a case-variant `.SENSEMAKING/KNOWLEDGE/`. All refused.
- Scripted browser run (Browser pane, Chromium, pages served from `127.0.0.1` out of my scratchpad):
  - clicked every list entry in the indexed export and the sample and read the scenario button state;
  - applied and reset a scenario on the sample.
- Hosted evidence with `gh`: run conclusions and head SHAs, the failed-step log for run 41996212049, PR #761 state, and recent Product Validation runs on `main`.

Not run: real clipboard write, `file://` page behavior (the pane would not script local files), keyboard-only navigation, SVG edge clicks, any human use, any independent-agent use.

## Claims

### 1. `cap:source-pinned-graph-view` (probe lines 5-20): CONTRADICTED in one clause

| Clause | Class | Source |
| --- | --- | --- |
| Optional, secondary, local viewer | SUPPORTED | `docs/semantic-architecture/agent-native-graph-viewer-v1.md:3`; design spec `docs/superpowers/specs/2026-11-05-agent-native-knowledge-graph-reasoning-design.md:17-19` |
| Export projects one exact-revision `explain` or `impact` neighborhood to bounded JSON or offline HTML | SUPPORTED | `src/sensemaking_skills/semantic_cli.py:325-340`; viewer guide `:9`, `:56`; ran at depth 1 and 2 |
| Render displays a separately attributed view JSON | SUPPORTED | `semantic_cli.py:352-386`; viewer guide `:9`. Attribution is not checked by code, only its fields' presence; `_source_refs` in `knowledge_view.py:48-51` |
| Page lets a person inspect records and edges | SUPPORTED for records (ran); edge selection read from source only | `view_assets/graph_view.html:249-255`, `:291`, `:325-369` |
| Page lets a person try a temporary hypothetical premise | **CONTRADICTED for ordinary indexed exports** | `graph_view.html:385-387`, `:395`; browser run below |
| Copy a question back to the coding agent | NOT_ASSESSED for the clipboard write; message preparation ran | `graph_view.html:409-430`, `:445-454` |
| `decision_changed`: agent can answer without index or browser | SUPPORTED | design `:19`; viewer guide `:79`; `docs/semantic-architecture/persistent-knowledge-cli.md:524` |
| `claim_ceiling`: merged via PR #761; browser use and agent benefit not established | SUPPORTED | `STATUS.md:534`, `:536`; `gh pr view 761`: merged as `e38b4156` |

**Overstatement.** The premise test is:

```js
/(^hypothesis$|^constraint$|assumption|premise)/i.test(node.kind+" "+node.id)
```

The test string is always `kind id`, so the anchored `^hypothesis$` and `^constraint$` branches can never match. Only an id or kind containing "assumption" or "premise" enables the button.

- Across the 191 authored claims at this commit, 2 match, and neither is a hypothesis or constraint: `observation:strategy-assumptions-drift-commands` and `poss:assumption-aware-opportunity-ecology`.
- 0 of 12 `hypothesis` claims and 0 of 2 `constraint` claims match.
- In the export of this capability's own neighborhood, the button was disabled on all 9 nodes, including both `constraint` records, while the help text said "Choose an assumption/hypothesis/constraint record" (`graph_view.html:398`).
- In the curated sample it works because the ids contain "assumption". It is also enabled on two `observation` records (`historical:20261024:assumption1-revision`, `-assumption2-confirm`), which are not premises by kind. The banner, the copy text and reset behaved as documented there.

The record repeats its sources here: viewer guide `:15`, `:80` and `STATUS.md:534` state the feature without the limit. So the document authority is quoted accurately, but the present-tense statement about the page is false on the guide's own main path. Only the code and a run show this.

The count covers authored claims. I did not evaluate the 34 additional mechanically indexed claims.

### 2. `con:graph-view-secondary-read-only` (probe lines 42-58): SUPPORTED

| Clause | Class | Source |
| --- | --- | --- |
| Secondary, no authority; conversation primary, needs no browser or index | SUPPORTED | design `:17-19`, `:48`; viewer guide `:3`, `:76-79`; `persistent-knowledge-cli.md:524` |
| View is bounded presentation, not reviewed knowledge | SUPPORTED | `docs/semantic-architecture/premise-sensitive-reconsideration-contract-v1.md:12`; `semantic_cli.py:309` |
| Browser does not fetch, authenticate, update graph, edit strategy, run agents, change evidence, transmit | SUPPORTED as declared | viewer guide `:18`; contract `:95` |
| Scenario or copied question only invites investigation; changed assumption is not proven change | SUPPORTED | viewer guide `:18`, `:92`; `graph_view.html:402`, `:425-426` |
| Plain `references` is not a necessary premise | SUPPORTED | viewer guide `:18`; contract `:20`, `:23`, `:101` |
| Graph miss is `NOT_ASSESSED` | SUPPORTED | viewer guide `:94`; contract `:102` |
| Durable changes through normal review | SUPPORTED | viewer guide `:82`; design `:122` |
| `decision_changed`: rejects required step, authoring surface, host-integrated action trigger, evidence for a conclusion | SUPPORTED, needs careful reading | design `:17`, `:159`, `:216`; viewer guide `:84` |
| `authority_note`: document, not owner | SUPPORTED | design `:3`; `knowledge.py:33-36` |

Caveats:

- **Possible overreading.** "Host-integrated action trigger" is safe only as "a click that silently triggers work" (design `:216`). The design leaves host-specific integration open: "optional later, never a prerequisite or silent background execution" (`:159`). A reader must not treat the record as banning all host integration.
- **Slight understatement of corroboration.** The note cites only the design. The implementation plan also reports owner agreement (`docs/superpowers/plans/2026-11-05-agent-native-knowledge-graph-reasoning.md:13`), and the session receipt gives its goal source as `owner_message` (`.sensemaking/receipts/2026-11-05-agent-native-knowledge-graph-reasoning-implementation.session.yaml:18-20`). These are still reports, not an owner record, so `document` remains the right choice over `owner`.
- **No ADR rules on the viewer.** A word search of `docs/adr/*.md`, `docs/product-strategy.md` and `CONTEXT.md` for viewer, graph view and `knowledge-view` returns nothing.

### 3. `component:graph-view-projection` (probe lines 22-40): SUPPORTED

| Clause | Class | Source |
| --- | --- | --- |
| Projects, validates, renders the envelope from query records or curated JSON | SUPPORTED | `knowledge_view.py:94`, `:185`, `:262`; `semantic_cli.py:331`, `:376`. Validator accepts both: `knowledge_view.py:188-189` |
| Uses packaged offline asset | SUPPORTED | `knowledge_view.py:269-271`; `pyproject.toml:65`; `MANIFEST.in:11` |
| CLI commands live in `semantic_cli.py`, owned by `component:semantic-cli` | SUPPORTED | `semantic_cli.py:291`, `:352`; `.sensemaking/knowledge/architecture.json` `owned_paths` |
| `claim_ceiling`: source inspected at `6f54a4a`, nothing executed | SUPPORTED as far as checkable | HEAD adds only the probe file (`git show --stat HEAD`). What the author actually did is not checkable |

Understatement: `owned_paths` omits the packaging owners the guide lists (`pyproject.toml`, `MANIFEST.in`; viewer guide `:100`). A change to packaging could break the viewer without pointing at this record.

### 4. `observation:graph-view-boundaries-in-source` (probe lines 60-75): CONTRADICTED in one clause

| Clause | Class | Source |
| --- | --- | --- |
| Only mechanical boundaries enforced | SUPPORTED | `knowledge_view.py:186`, `:3-5` |
| Builder and validator reject truth or action flags not false | SUPPORTED | `knowledge_view.py:107-108` (query), `:199-200` (view) |
| Export and render are create-only | SUPPORTED, as a pre-write check | `semantic_cli.py:315`, `:367`; re-export refused. Check then `write_text` (`:340`, `:378`), not an atomic exclusive create |
| Refuse output under `.sensemaking/knowledge` | SUPPORTED | `semantic_cli.py:319-322`, `:371-374`; refused, including case variant on Windows |
| Edge role is `CONTEXT_ONLY` for `references`/`contained_in`, `UNKNOWN` otherwise | **CONTRADICTED as stated** | True only at `knowledge_view.py:85` (`_edge`, indexed path). Validator allows all six roles: `:20-23`, `:233` |
| No `fetch`, `XMLHttpRequest`, remote script, `innerHTML` | SUPPORTED | Text search of `graph_view.html`: only the comment at `:177` and the SVG namespace at `:184`. Run: 0 resource entries on both pages |
| Scenario and copy state only in page memory | SUPPORTED with an omission | `graph_view.html:183`, `:428`; clipboard write at `:449` is a user-triggered exit from the page |
| Validation does not check entailment | SUPPORTED | `knowledge_view.py:186`; viewer guide `:72` |
| Non-mechanical, non-lexical record labelled `SOURCE_DECLARED` unchecked | SUPPORTED | `knowledge_view.py:54-59`; 32 of 32 nodes at depth 2 |

Overstatement on edge roles. The sentence sits under what "the view code enforces", with no input qualifier, but component record 3 says the code also takes curated JSON.

- The repository's own sample has 3 `SUPPORTING` / `SOURCE_DECLARED` edges (`docs/semantic-architecture/premise-sensitive-reconsideration-example-view-v1.json`).
- A copy with every edge set to `NECESSARY` rendered successfully.
- So a curated view can show `NECESSARY` or `SOURCE_DECLARED` with no check at all. A reader relying on this record would trust role labels in rendered views more than the code justifies.

Understatements:

- **Label conflict not flagged.** The record notes the unchecked label but not that it conflicts with a repository definition. Contract `:31` defines `SOURCE_DECLARED` as requiring that "the agent inspected the original"; contract `:84` narrows it to "source-declared relationship". The code follows the narrower reading.
- **Offline is not browser-enforced.** There is no Content-Security-Policy in the asset (`graph_view.html:4-6` are the only metas). Offline behavior comes from what the script does, not from a browser restriction. Escaping covers `&`, `<`, `>` in embedded JSON (`knowledge_view.py:277-278`).

### 5. `observation:graph-view-evidence-ceiling` (probe lines 77-91): SUPPORTED

| Clause | Class | Source |
| --- | --- | --- |
| PR #761 head `37809b7` passed Release Candidate Distribution and Semantic Context Re-entry | SUPPORTED | `STATUS.md:536`; `gh run view` 41996212144, 41996212110: success at `37809b7c...` |
| Product Validation 3,634 passed, 1 failed | SUPPORTED | `STATUS.md:536`; run 41996212049 log: "1 failed, 3634 passed, 25 skipped, 5 xfailed" |
| Failure attributed to an older receipt enum | SUPPORTED | Failed test is `tests/test_sensemaking_receipts.py::test_repository_receipts_validate_against_this_repository` on the strategic-evolution receipt; receipt F-4 (`...implementation.session.yaml:127-133`) |
| Local tests, browser, installed wheel, independent use, comparative benefit `NOT_RUN`/`NOT_ASSESSED` | SUPPORTED as the repository's record | `STATUS.md:536`; viewer guide `:98`; receipt `:86-89`, `:121`, `:154` |
| Text search of `tests/`, `.github/`, `scripts/` finds no reference | SUPPORTED, misattributed | My search for `knowledge_view`, `knowledge-view`, `graph_view`, `GRAPH_VIEW`, `build_graph_exploration`, `view_assets`, `GraphExploration` found nothing. Not in either cited source |
| Indirect coverage not assessed | NOT_ASSESSED, as the record says | I did not trace indirect coverage either |

Problems:

- **Misattribution.** Authority is `document`, `STATUS.md`, and evidence is `STATUS.md` plus the guide, but the search clause is the author's own observation and appears in neither. The clause is true, but its stated source does not back it.
- **Epistemic status slightly high.** `observed` is allowed for document authority (`knowledge.py:287`; `skills/repository-semantic-steward/references/knowledge-contract.md:101`). But the CI facts are secondhand reports, and the author's `claim_ceiling` admits the logs were not inspected. `declared` would fit those clauses better. I inspected the conclusions and failed-step log, and they hold.
- **Understatement.** The record stops at the failure and omits two later facts: `STATUS.md:536` says the receipt repair was in the following PR, and hosted Product Validation on `main` succeeded at `6f54a4a` itself, the commit the record is pinned to. That success does not test the viewer by name, so the ceiling stands, but a reader would wrongly infer the suite was still red.

## Relations

All eight have `epistemic_status: declared`, `derivation: authored` and `authority_verified: false` in the index.

| Relation | Class | Source | Note |
| --- | --- | --- | --- |
| `rel:graph-view-implemented-by-projection` | SUPPORTED | `knowledge_view.py:94-279`; `knowledge-contract.md:65` | |
| `rel:graph-view-implemented-by-semantic-cli` | SUPPORTED | `semantic_cli.py:291-386` | Scope limited to two commands, correctly. Target's statement (`architecture.json`) does not list view commands; only `owned_paths` connects them |
| `rel:graph-view-requires-semantic-queries` | SUPPORTED | `semantic_cli.py:325`; `knowledge-contract.md:102`; `semantic_cli.py:364-376` | Bare predicate overstates: only export needs it, render does not. The scope attribute discloses this, so the meaning depends on reading it |
| `rel:graph-view-constrained-by-secondary-read-only` | SUPPORTED | viewer guide `:18`, `:76-84` | |
| `rel:graph-view-constrained-by-agent-control` | SUPPORTED | design `:5`, `:17`; `docs/adr/0029-current-product-boundary.md:35`, `:45`, `:47`, `:55`; plan `:18` | ADR 0029 never mentions the viewer; the edge is an application of a general rule by the design. In the scope note, "UI is not a master interface" is the design's wording at `:17`, not ADR 0029's, and the sentence can be misread as attributing it to the ADR |
| `rel:graph-view-references-ontology-first` | SUPPORTED | design `:5`; `docs/adr/0034-ontology-first-adaptive-sensemaking.md:36`, `:44` | See below |
| `rel:graph-view-references-boundaries-in-source` | SUPPORTED | `knowledge-contract.md:101` | Pointer only, matches convention. Inherits the problem in claim 4 |
| `rel:graph-view-references-evidence-ceiling` | SUPPORTED | `knowledge-contract.md:101` | Pointer only |

Edge-meaning issues on `rel:graph-view-references-ontology-first`:

- **Borrowed term.** `conceptual_relation: governedBy` appears elsewhere only as `Mission governedBy Goal` (`docs/semantic-architecture/ontology.md:59`). No other knowledge record uses it. Here it links a capability to a decision on the design's say-so ("Governing product", design `:5`). The record correctly avoids `decided_by` and says why, but `governedBy` still sounds stronger than "the design cites this ADR as product context".
- **Non-standard `establishment`.** The value is free text. `knowledge-contract.md:103` lists `inferred`, `ratified`, `hypothesized`, in its product-possibility section, so it may not bind this record. Other records (`possibilities.json`) use the same pointer phrase, so this is an inconsistency, not a violation. The honest value here would be `inferred`.
- **Selective.** The same design line names ADR 0031 as governing too, and plan `:19` gives it the most directly relevant rule (derived HTML is a reproducible read-only projection). The pack has no edge to it, so the viewer's reviewed-knowledge boundary reaches ADR 0034 but not its more relevant ADR.

## Whole-pack observations

- **Disposable status is invisible in the graph.** Nothing in the records marks them as a probe, and the viewer labels them `SOURCE_DECLARED` like merged knowledge. The file name is the only signal.
- **Missing limits.** Nothing states that indexed exports always carry empty `comparisons` and `scenarios` (`knowledge_view.py:169-170`), or that only one of the design's four planned views was built (design `:146-151`; I did not find the other three in the asset, but did not audit this exhaustively).

## What this changes in my first answer

1. **Retract:** "I checked them against sources and found no contradictions." That first check missed two contradictions, the scenario clause and the unscoped edge-role clause.
2. **Correct:** I described a person trying a temporary hypothetical premise, and listed the page as implemented with medium confidence, without a limit. For ordinary indexed exports that control is effectively unavailable: 0 of 9 nodes in the tested export, and 0 of 12 hypotheses and 0 of 2 constraints among authored claims. It works on the curated sample.
3. **Add:** my "Edge roles" point was correctly scoped to indexed edges, but it left out that curated views can claim any role, including `NECESSARY`, unchecked. Listing it under "fixed limits in code" gave too much comfort.
4. **Update:** "I didn't open the HTML" and "I didn't inspect the hosted run logs" are no longer true.
   - Scripted browser selection, a scenario on the sample and zero resource loads have now run, over `127.0.0.1`. The clipboard, `file://`, keyboard use and human use remain unrun, and this is my session evidence, not a repository record.
   - Hosted conclusions and the failing test are confirmed.
5. **Add to hosted CI:** Product Validation later succeeded on `main` at `6f54a4a`. My answer mentioned only the PR-head failure and the `NOT_RUN` entry. The viewer is still not tested by name.
6. **Unchanged:**
   - the viewer's secondary, no-authority role;
   - the weaker-than-ADR authority;
   - the absence of benefit evidence;
   - the `SOURCE_DECLARED` caveat;
   - the note that this was not a blind run.

## Confidence

- **High:** the scenario defect (source and run agree), the edge-role contradiction (source, repository sample and my edited copy agree), and the hosted conclusions.
- **Medium:** my judgment calls on overstatement and epistemic status, especially `governedBy` and `observed` for reported CI. Another reader could reasonably grade these differently.
- **Limits:** the 191-claim count excludes mechanical records. This pass is not independent: I wrote the first answer, and project memory was loaded.
- **No fixes made:** I did not change the checkout, the records or the asset.
