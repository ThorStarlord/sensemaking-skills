# CLI Reference

**Status:** human-readable overview of the `sensemaking-skills` command line.
**Authority:** subordinate to the machine contracts
`docs/cli-contract-v1.0.yaml` and `docs/cli-json-contract-v1.0.yaml`. When this
page and a contract disagree, the contract and the code win. Regenerate exact
option lists with `sensemaking-skills <command> --help`.

Design rule shared by every command family: **the CLI performs mechanical
operations and never makes semantic decisions**. It does not select a
responsibility, rank options, choose a next action, or grant authority. The
active coding agent owns the control loop (ADR 0013).

```text
sensemaking-skills [--version] <command> ...
```

## Command families

| Command | Purpose | Detailed doc |
| --- | --- | --- |
| `setup-skills` | Copy packaged Skill trees to an explicitly chosen harness discovery root. No harness auto-detection. | `docs/harness-adapters.md`, `INSTALLATION.md` |
| `validate` | Validate a repository sensemaking brief or workflow plan (`--artifact`, `--json`). | `docs/validation-workflow.md` |
| `handoff` | Verify an installed `using-sensemaking` Skill, inventory a target repository, and write a ready-to-use handoff prompt (`--repo`, `--output`, `--question`, `--harness`, `--scope`, `--skill-path`, `--expected-source-ref`, `--resume-from`, `--json`). Does not analyze semantics. | `docs/cli-reference.md` (below) |
| `analyze` | Compatibility alias for `handoff`; retained for the Version 1.0 command surface. | `docs/public-surface-v1.0.md` |
| `test` | Shadow-mode validation automation over sample repositories (`--repos`). | `docs/archive/phase-reports/` (historical) |
| `campaign` | Durable Campaign state, handoff/resume, execution companions, lineage, bundles, multi-target, provenance. | `docs/campaign-cli.md` |
| `strategy` | Inspect authored Level-3 strategic analyses. | `docs/strategic-continuity-v1.md` |
| `journey` | Read-only decision-journey projections. | `docs/decision-journey-productization-v1.md` |
| `organization` | **Advanced/optional** read-only role/capability topology; not part of the default control loop. | `docs/capability-organization-tracer-v0.md` |
| `semantic` | Mechanical semantic substrate (catalog, conformance, probes, map build, companion state). | `docs/semantic-architecture/README.md` |
| `release` | Local release-authority audit. | `docs/release-authority-audit.md` |

## `campaign`

Grouped by intent (all read/write only durable Campaign state; none infers a
decision):

- **Lifecycle:** `init`, `advance`, `defer`, `close`, `closeout`, `archive`,
  `completion-receipt`.
- **Inspect:** `status`, `inspect`, `history`, `diff`, `inventory`, `explain`,
  `working-context`.
- **Integrity:** `validate`, `doctor`, `preflight`, `graph`, `graph-integrity`,
  `replay`.
- **Evidence:** `ingest`, `lineage`, `reconciliation`.
- **Continuity:** `handoff`, `resume`, `resume-context`, `resume-profile`.
- **Capabilities:** `capabilities`, `capability-context` (unranked candidates
  after the agent classifies a responsibility).
- **Execution companion:** `execution handoff|inspect|result|result-template|
  result-seal|result-import|export|factory-issue`.
- **Strategy bridge:** `strategy inspect|diff|handoff`.
- **Targets:** `target rebind|verify-rebind`;
  `multi-target add|relate|inspect|verify|refresh|rebind|graph|dependency-check|
  execution-view`.
- **Uncertainty history:** `uncertainty-record|relate|show|history|graph`.
- **Semantic companion:** `semantic-state`, `semantic-state-append`.
- **Bundles:** `bundle-export|verify|inspect|import|graph|resume-context`.
- **Provenance:** `provenance`, `provenance-publish` (preview by default;
  publishing is explicit).
- **Static guidance:** `workflow list|show` - golden paths only; never routes
  or executes.

## `strategy`

`inspect`, `paths`, `uncertainty`, `assumptions`, `compare`, `drift`, `history`,
`graph`. Projections of declared state; no strategic judgment.
For developmental trajectory reasoning, `strategy paths --artifact PATH --json --include-trajectory-context`
also projects authored dependencies, capability references, transitions, unlocks,
risks, assumptions, and other existing path context. Its
`shared_trajectory_context` groups literal typed capability references by
builds-on/required roles and shared declared assumption IDs within one analysis;
legacy prose/missing fields remain unassessed. Shared references are not
validated dependencies, shared causal enablers or a priority ranking.
`strategy graph` scopes path, assumption and transition identifiers to their
original supplied analysis, using exact declared references or exact supplied
file paths; unresolved or ambiguous references remain separate. Graph node
identifiers are presentation-local, not stable semantic IDs. `strategy compare --before OLD --after NEW --json --include-trajectory-context`
also reports changed context fields for matching local path IDs and whether
declared decision assumptions differ. These are opt-in JSON projections, not
semantic path matching, validated dependencies, or automatic reconsideration.
Missing fields remain missing; inspect original artifacts and reconciliation.

## `journey`

`inspect`, `context`, `delta`, `impact-closure`, `guide`. `guide` shows static
guidance for one caller-selected intent and never routes.

## Advanced/optional: `organization`

`inspect`, `role`, `skill-profile`. Explicit topology only; no worker
allocation, Skill selection, execution authority, or default-loop role. Use only
when topology itself is decision-relevant.

## `semantic`

`catalog`, `conformance`, `probe`, `map-build`, `state-append`, `state-show`;
`workspace-orient` (source-pinned path inventory), `workspace-query`
(one-revision knowledge retrieval), and `workspace-changes --base-ref REV`
(two-commit semantic delta without manual index preparation; optional
`--pr-merge-base` for PR-scoped semantic knowledge changes).
`workspace-query --operation context-for PATH --include-source-relationships`
optionally adds committed Python AST importers, direct imports, test
references, top-level symbols and leading-underscore cross-module imports to the authored path context; it is syntactic,
not a runtime call graph or coverage result. Add `--symbol NAME` for direct
references, test functions/methods, a source-level behavior surface and
guard-derived verification scenario candidates; test candidates are not
coverage and scenario hints are not executable tests.
`semantic verification-plan --repo . --ref HEAD --path FILE --symbol NAME`
composes the same authored verification records, direct test-function
candidates and guard scenarios into one change-scoped plan: deduplicated
`pytest_target` candidates (a test file or `file::test` node), a suggested
non-executed pytest invocation that keeps function targets not subsumed by a
file candidate, separate non-executable guard scenarios, authored records that
did not map to a test file, and explicit gaps. It does not execute or generate
tests and does not establish coverage, pass status, test analysis, semantic
truth or authorization.
`workspace-query --operation context-for|workspace-impact --repo .` compares
tracked changed file names and Git's untracked entries, not every file inside a
wholly untracked directory; `change_scope` discloses the granularity and
`untracked_file_total: NOT_ASSESSED`. Cited sources and target paths are still
matched exactly. Use `workspace-review-context --include-worktree` when
individual untracked file names are required for review.
Both `knowledge-query` and `workspace-query` support `--operation product-outline` for a bounded, source-linked view of reviewed goals, non-goals, serving records and constraints. Add `--include-candidates` to expose separately linked possible futures without promoting them to goal service or engineering priority. `workspace-query --operation product-outline --method-question "<decision>"` and `workspace-query --operation possibility-ecology --subject ID --method-question "<decision>"` attach authored method context at the same resolved revision, with `applicability_to_present_task: NOT_ESTABLISHED`; they do not select a method. Add `--include-method-trials` (or `semantic method context --include-trials`) for question-matched historical trial pairs including trials without a lesson link; separate limits, omitted/truncated results and chronology/closure limits remain explicit. `workspace-query --operation possibility-ecology --subject <goal-or-opportunity-id>` projects one goal's or opportunity's authored candidate family with dimensions, realization state, goal links, inter-candidate relationships and claims shared by multiple candidates; for a goal it also follows exactly one explicit specialized-goal `serves_goal` hop into `descendant_goal_candidates` with `via_goals` provenance. `product-outline --include-candidates` mirrors that one-hop family in `indirect_candidate_opportunities`. Neither view infers a hierarchy, rank or selection. `workspace-changes --base-ref OLD --ref NEW --json --include-possibility-evolution` adds a bounded comparison of authored opportunity records, their incident authored relations and directly linked authored claims. It uses exact indexed revisions and existing authored-field/source-fingerprint classifications, preserves before/after source pointers and scope changes, and independently limits each delta category. Changed links/premises invite reconsideration; they do not establish enabling effects, emergence, causal impact or selection. `workspace-review-context --include-candidates` additionally shows BASE candidate evidence paths touched by a committed diff as reinspection signals, never automatic strategic reassessment. It also adds `candidate_reconsiderations`, which evaluates explicit `file:`, `claim:` and `symbol:` references inside an authored `revisit_when` and reports `FIRED`, `NO_MATCH` or `NOT_ASSESSED` with evidence; free text without those refs remains `NOT_ASSESSED`. In explicit `--path` review, excluded or unavailable paths and whole-claim comparison remain `NOT_ASSESSED`; the evaluator does not turn a restricted diff into a whole-repository no-match. A committed symbol comparison without a match cannot assess dirty symbol bytes; it reports `NOT_ASSESSED` when the working path changed. A fired reference is a reconsideration prompt, not a staleness verdict, selection or authorization. `semantic method context|record` reads or materializes optional experience-informed method precedents; `semantic method trial open|close|show` preserves an optional predecision method commitment and a later attributable result, with a content digest, descendant-commit close checks and a fail-closed show surface; a recorded episode may optionally reference an authored `decision` claim at its source revision so the existing decision and method consumers show the method-decision chain. `semantic decision record` materializes an agent-authored consequence-informed review of an existing `arch:` option as a new `decision` claim and relations; it preserves the option and preference and creates an unreviewed proposal. `semantic possibility record` materializes an agent-authored synthesis of existing goals, possibilities, capabilities and assumptions as a new hypothetical `opportunity` proposal with validated provenance; it does not generate, rank or select possibilities. Both `semantic possibility record` and `semantic method record` accept `--draft-only --output .sensemaking/proposals/NAME.json` (or `artifacts/history/NAME.json`) to keep an unreviewed output outside the knowledge index; method episode/evidence tracking, identity and disposition checks remain in force. `semantic knowledge-proposal-check --proposal DRAFT --destination .sensemaking/knowledge/NEW.json --repo . --json` checks a contained detached draft as a new unoccupied pack without writing or promoting it; the result includes the checked draft SHA-256. It does not replace ordinary final-path preflight, semantic review or exact clean-commit `knowledge-build`.
For `knowledge-query` and `workspace-query`, `--operation search --query-text TEXT`
provides opt-in ranked lexical question matching; it never infers semantic
relevance. Existing `--subject` literal and `--term` OR search are unchanged.
Use `semantic workspace-review-context --base-ref BASE --ref HEAD --json` to prepare
BASE-revision product intent and per-changed-file architectural context from two
committed Git revisions. For PR reviews, add `--pr-merge-base` with BASE as the
target-branch tip to select the unique Git merge base; the default remains the
explicit two-commit comparison. Missing or ambiguous merge bases fail closed.
The review also exposes path-level overlaps with BASE cited evidence and
uncited changed-path gaps, without inferring semantic staleness.
This is review evidence, not a drift/violation verdict. Add `--source-path PATH`
for paired BASE/TARGET committed Python relationships for one selected review
path; optionally add `--source-symbol NAME` for direct symbol/test identities
and a source-level `symbol_behavior_comparison` (signature, decorators,
docstring hash, direct raises/asserts, source-body hash). This does not infer
semantic behavior, coverage or impact.

When a rename is the change, `sensemaking-skills semantic refactor-rename
--repo . --path FILE --symbol OLD --to NEW [--patch-out FILE]` previews a
fail-closed unified patch for one tracked top-level Python function or class.
It rewrites direct imports, unaliased name references, module-alias attributes
and literal `__all__` entries, applies the patch in a disposable checkout,
checks that the AST delta is identifiers only and reports unresolved dynamic
sites. A `READY` result is not runtime correctness, test coverage, API
compatibility or complete repository-wide renaming; star imports, rebinding,
dynamic strings/calls and name collisions block the patch.

For an explicit proposed text patch that has not been applied to the active checkout,
`sensemaking-skills semantic patch-rehearsal --repo . --ref BASE --patch-file FILE --json`
applies it in a disposable exact-commit worktree and composes the existing
BASE-only worktree review with candidate reconsideration. It reports patch digest,
actual changed paths, before/after file digests and Python syntax results, not a
runtime or semantic verdict. For modified Python files, it also compares uniquely named top-level definitions
using exact source and normalized AST digests, with separate module-level source
and AST indicators; these are syntactic review signals, not runtime equivalence.
Version 1 accepts at most eight existing tracked
regular-file modifications and 256 KiB UTF-8 patch text; structural changes,
links, binary changes and Git control files are refused. No target code/test
execution, active-checkout application or automatic acceptance. See the
[patch rehearsal contract](semantic-architecture/persistent-knowledge-cli.md#prospective-patch-rehearsal).

For changes **still being edited** in the checkout, add `--include-worktree`
with `--ref HEAD` (or an exact revision equal to the checkout's HEAD).
For example:

```bash
sensemaking-skills semantic workspace-review-context \
  --base-ref HEAD --ref HEAD --include-worktree --repo . --json
```

This opt-in mode assembles baseline product/architecture context for staged,
unstaged and untracked **path names** as well as any committed differences
between the supplied commits. Original product intent and source fingerprints
remain from the committed BASE revision; working file bytes are **not**
indexed. Per-file context is allocated in `review_scope.selection_order`:
committed changes first, then staged, unstaged and untracked paths, sorted
within each group, so incidental untracked artifacts do not displace pending
source edits from `--max-paths`.

For a known pending set, repeat `--path PATH` (1..32) instead. Explicit-scope
review restricts Git reads to those literal paths, so an unrelated untracked
tree is not walked; every requested path gets BASE context and `--max-paths`
selection does not apply. `review_scope` reports `scope_mode:
explicit_paths`, `changed_requested_paths`, `unchanged_requested_paths`,
`not_found_requested_paths`, `ignored_requested_paths` and
`other_changes_assessed: false`: every other committed or working change is
NOT_ASSESSED, not silently treated as reviewed or unchanged. A requested path
that does not identify a file in the inspected revisions (and, with
`--include-worktree`, the working tree) is not-found, never unchanged. An
ignored working-tree path absent from those revisions is reported as ignored,
not unchanged.

The output distinguishes
`committed_evidence_reinspection` from
`working_evidence_reinspection`, and per-path `change_modes` and
`context.change_relevance` indicate which paths need the agent's own
source/diff inspection. A file present in both categories is reported in
both. The existing committed-only behavior and
`context.committed_change_relevance` remain unchanged without the flag.
The checkout must still point at the requested target revision; otherwise
the optional mode refuses rather than mislabeling later commits as local edits.
Neither a changed path nor a source-fingerprint overlap establishes semantic
staleness, a code defect or architectural noncompliance.

For JavaScript/TypeScript source orientation, both `semantic knowledge-build`
and zero-setup `semantic workspace-query` accept
`--include-js-module-imports --max-js-imports N`. The latter keeps its default
index untouched and stores opted-in source observations in a separate,
limit-specific derived cache, including on repeat queries. The opt-in probe
records literal static ESM import/re-export specifiers with source citations,
not module resolution, architecture coupling or complete JS/TS coverage.
See `docs/semantic-architecture/persistent-knowledge-cli.md` for exact scope,
cache, source-identity and evidence limits. Even in PR mode, it does not
verify GitHub PR identity, complete ancestry, semantic truth or Skill quality.

## `release`

`audit [--repo-root] [--json]`. Exit code 3 on error findings. See
`docs/release-authority-audit.md`.

## `handoff`

`sensemaking-skills handoff --repo TARGET [--output DIR] [--question TEXT]
[--harness generic|claude|codex|opencode] [--scope any|user|project]
[--skill-path PATH] [--expected-source-ref SHA] [--resume-from RECEIPT ...] [--json]` verifies an installed `using-sensemaking` Skill,
inventories the target repository's paths, manifests and entry documents, and
writes `handoff.json` and `handoff.md` with a ready-to-use prompt. It does not
analyze repository semantics, select work or authorize action. It fails closed
if no installed copy is found or multiple copies are ambiguous; pass
`--harness`, `--scope` or `--skill-path` to select one. Currency compares the
installed tree with the packaged source or the install record; a stale or
unrecorded copy is reported, not silently trusted. `analyze` is a compatibility
alias with the same options.

The additive handoff fields expose executable code provenance, expected source comparison (direct committed Skill tree when available, otherwise digest-linked record), bounded continuity path inventories and (only on explicit selection) validated prior session receipt projections. `--resume-from` accepts up to five distinct direct repository-relative `.sensemaking/receipts/*.session.yaml` paths. It uses the existing canonical validator against the current target, not a new format or automatic resume selector. Invalid/unavailable receipts are reported without a historical projection. The receipt path inventory returns all paths when at most forty are present; otherwise it returns the first and last twenty in filename order (`path_selection: LEXICOGRAPHIC_ENDS`, with `omitted_count`). No content is opened to choose these hints. Filename order is not update chronology, relevance, strategic precedence or authority; enumerate the directory directly for omitted paths. Other bounded inventories and explicit receipt selection are unchanged. The selected historical projection includes bounded authored responsibilities, reasons, artifact refs and validation entries (command and recorded PASS, FAIL or NOT_RUN result, each with omission counts) alongside goal, stop rationale, next and claim ceiling so an agent can examine consequential continuation without treating a previous stop as a current verdict. Each responsibility projects at most twelve validation entries, with `validation_omitted`; a receipt-level `VALID` is a representation check, not proof that its recorded commands ran or passed. Handoff does not run those commands, aggregate their results or establish present verification. The continuity inventory separately lists bounded direct JSON paths in `.sensemaking/proposals/` and `artifacts/history/` without reading their contents. `speculative_record_review_state: NOT_ASSESSED` means no draft validity, unresolved status, relevance, review or authority is inferred, including for previously promoted historical drafts. The handoff is not a snapshot and does not prove loaded Skill identity, relevance, currentness or permission. See [returning engagement](../GETTING_STARTED.md#re-enter-sustained-development).

## `validate`

`sensemaking-skills validate --artifact PATH [--json] [--repo-root CHECKOUT] [--target-repo TARGET]`
runs the **existing** `scripts/validate-and-report.py` router and its
artifact-specific canonical validator. Unlike the former instruction-only
placeholder, it validates file contents and returns exit code 5 on invalid
artifacts, 6 when canonical validators are unavailable or fail, and 0 on a
valid result. `--json` emits the router's single structured result object.

By default, the command uses the **existing** canonical validator runtime
already bundled in installed wheels for `campaign ingest`. In an editable
checkout it uses that checkout's canonical `scripts/` directory. An explicit
`--repo-root` overrides this resolution with the provided framework checkout.
No arbitrary current-working-directory search is performed. Missing or
untrusted validator runtime files fail **closed** with exit code 6; they never
produce false validation success. This does not add a second validator
implementation or change artifact semantics.

## Exit codes and JSON

Exit-code and JSON-envelope semantics are normative in
`docs/cli-contract-v1.0.yaml` and `docs/cli-json-contract-v1.0.yaml`; campaign
commands additionally follow `docs/campaign-cli.md`. Source-authored console text
stays ASCII-only by repository rule. User-supplied text that the terminal's code
page cannot encode is written as JSON-compatible `\uXXXX` escapes instead of
failing the command after it has written state; text the code page can encode is
written unchanged.

## Scripts that are not CLI commands

Operator scripts (validators, ledger tools, execution infrastructure) are
indexed in `scripts/README.md`.
