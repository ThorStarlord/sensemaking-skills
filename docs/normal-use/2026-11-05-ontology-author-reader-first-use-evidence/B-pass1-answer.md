**Short answer:** the offline graph view is an optional, secondary inspection aid for the coding agent, and it has no authority of its own. The code exists and its CLI path works, but nobody has shown it working in a browser or shown that it helps an agent.

Checked at `c7eb21df`; the checkout is unchanged, and the index and test exports are in my scratchpad.

## What it is meant to do
- **Primary interface:** the coding-agent conversation stays primary, and the agent can answer with no browser, index or viewer.
- **When it's used:** only when seeing a bounded, source-pinned neighborhood helps. A person inspects records and edges, tries a temporary `HYPOTHETICAL / NOT COMMITTED` premise, and copies a question back into the agent chat.
- **What the copied question does:** it only invites investigation. The agent should check it against sources, not accept it.
- **What it must not become:** a required step, an authoring tool, a trigger for actions, or evidence for a conclusion. Changing an assumption doesn't prove any linked judgment changed, a plain `references` edge isn't a necessary premise, and a graph miss means `NOT_ASSESSED`.

*Relied on:* `docs/semantic-architecture/agent-native-graph-viewer-v1.md`, the design spec (sections 1, 7), and `con:graph-view-secondary-read-only`.
*Confidence:* high that this is the documented intent. Its authority is weaker: the design reports owner agreement in conversation, and the only record of that I saw is that design doc. No ADR covers the viewer, and ADR 0034 doesn't mention it, according to the candidate record.

## What is implemented
- **`knowledge-view-export`:** projects one exact-revision neighborhood (`explain` at depth 1, `impact` at depths 2–4) into JSON or offline HTML.
- **`knowledge-view-render`:** turns a separately attributed view JSON into the same HTML page, without indexing it.
- **Fixed limits in code:**
  - `semantic_truth_established` and `action_authorized` must be false.
  - Node and edge counts are capped.
  - Output files are create-only and can't be written under `.sensemaking/knowledge`.
- **Edge roles:** indexed edges only get `CONTEXT_ONLY` or `UNKNOWN`, so this path never produces `NECESSARY` or `DEFEATER`.
- **HTML page:** a search of the asset found no `fetch`, `XMLHttpRequest`, remote script, browser storage or `innerHTML` use (only a comment forbidding it). The one outward path is the clipboard.
- **Packaging:** the HTML asset is declared in `pyproject.toml` and `MANIFEST.in`.

*Relied on:*
- **Source:** I read `knowledge_view.py` and the CLI commands in `semantic_cli.py`, and text-searched `graph_view.html`.
- **Local run (from worktree source):** index build, `explain`, an export (9 nodes, 8 edges), and rendering the historical sample all worked. Overwriting an existing file and writing into `.sensemaking/knowledge` were both refused.

*Confidence:* high for the code and CLI path. Medium for page behavior, which comes from reading the code, not running it.

## What is not established
- **Browser behavior:** interaction, the scenario overlay, clipboard copy and keyboard use have no recorded run, and I didn't open the HTML either.
- **Installed use:** no isolated installed-wheel CLI run is recorded, and mine ran from source.
- **Agent or user benefit:** there is no evidence of independent later-agent use, creative or comparative benefit, or transfer to other repositories. The session receipt leaves these open as Q-1 and Q-2.
- **Semantic correctness:** validation checks structure only, not whether a source supports an interpretation. Indexed records are labelled `SOURCE_DECLARED` without checking the original source (`_establishment`, `knowledge_view.py` line 54).
- **Tests:** a search of `tests/`, `.github/` and `scripts/` finds no reference to `knowledge_view` or `knowledge-view`, and indirect coverage is unassessed.
- **Hosted CI:** PR #761 head `37809b7` passed Release Candidate Distribution and Semantic Context Re-entry. Product Validation reported 3,634 passed and 1 failed, attributed to an older receipt enum. The receipt marks hosted checks on the final PR head as `NOT_RUN`.

*Relied on:* `STATUS.md` (line 536), section 6 of the viewer guide, the implementation session receipt, and my own search. I didn't inspect the hosted run logs.
*Confidence:* high that these are unrecorded at this commit. That doesn't show the viewer fails or doesn't help, only that it hasn't been tested.

## Caveats about the sources
- **Probe records:** all five viewer claims in the knowledge graph are in `.sensemaking/knowledge/ontology-author-reader-probe.json`, added by HEAD and labelled "disposable, do not merge". They aren't merged knowledge, so I checked them against sources and found no contradictions. Their "implemented" claims were pinned at `6f54a4a`.
- **Outdated header:** the design spec's status still says "planning/specification only, not built". That's out of date for the implementation; `STATUS.md` and the viewer guide record the merge.
- **Not a blind run:** this exact question appears in `docs/superpowers/plans/2026-11-05-ontology-author-reader-qualification.md` (line 115), which my first search surfaced. Project memory was also loaded, so this answer shouldn't count as independent evidence for that qualification.

Test exports:
- `C:/Users/Admin/AppData/Local/Temp/claude/283a4123a15423ed/7d85f11d-92e1-4eb9-94ac-2d518e64db7e/scratchpad/view.html`
- `C:/Users/Admin/AppData/Local/Temp/claude/283a4123a15423ed/7d85f11d-92e1-4eb9-94ac-2d518e64db7e/scratchpad/sample.html`