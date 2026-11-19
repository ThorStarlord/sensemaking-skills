# RECALL — Source-verified use during engineering

RECALL is lightweight by default. It does not decide whether a task is warranted.

1. Identify current repository SHA, task and expected decision. Ask which remembered constraints or rationale could materially change implementation.
2. Inspect available reviewed knowledge records and current indexed versions. Prefer existing Git-authored sources when an index is missing. When no index exists, `semantic workspace-query <file>` builds or reuses a derived index of the committed HEAD and answers `context-for` in one command; in a query receipt record it as a `build` (when `workspace_index.index_state` is `built`) plus the query operation.
3. Retrieve narrowly **from the active workspace**. A prior committed index can be queried with `semantic knowledge-query --repo .` even when the checkout is dirty: inspect `workspace_context` for HEAD alignment and unindexed changes. The query still represents only the selected committed revision. When a claim ID is known, use `explain` (or `why` for a decision); otherwise search with a short phrase, inspect IDs, then explain the relevant claims.

   `search` preserves case-insensitive **literal substring matching in a claim statement or ID**; repeated `--term PHRASE` flags (1–8 phrases) preserve explicit literal OR matches. When the agent has a question but not the exact source phrasing, use `semantic workspace-query --operation search --query-text "Which decisions constrain repository knowledge?" --json` (or `knowledge-query` with explicit index identity). This **opt-in lexical** mode tokenizes the question, drops common function words (reported in `ignored_function_words`), and ranks matches by distinct content-word overlap. Plural or tense forms of a word match their stem (`subagents` finds `subagent`); words under five letters match only as whole words or stems. `match_details` disclose each returned hit's matching tokens. It is neither semantic search nor proof of relevance: inspect the original source. The new `--query-text` is mutually exclusive with `--subject` and `--term`; legacy modes are unchanged. A miss or weak match remains **NOT ASSESSED**, not proof that relevant knowledge is absent. Use `impact` only as an explicitly declared-edge **candidate** view.
   For repository-level product orientation, use `semantic workspace-query --operation product-outline --json` to inspect source-linked goals, non-goals and declared serving records/constraints without guessing the right file. For prospective questions, add `--include-candidates` to show explicit goal-linked possible futures separately from serving records; candidate links neither select nor authorize work.
   Open `claim_evidence_refs` and `relation_evidence_refs` independently
   when a candidate's sources or its relationship to a goal would affect
   the next question; the
   `source_ref` is the authored knowledge-pack container, not the supporting
   source. The result is a bounded **explicit-edge** view, not proof that any goal is met or that a proposed opportunity is warranted. Treat missing links as NOT_ASSESSED and open original sources before making a consequential product choice.
   For an architecture-sensitive review of two committed revisions, use the optional
   `semantic workspace-review-context --base-ref BASE --ref HEAD --json` to retrieve
   BASE product goals, non-goals and per-changed-file context without manually
   listing paths. It does not assess code behavior, rename meaning or drift, and
   omitted/unknown paths are not clearance. Inspect original sources and the actual
   diff; inspect `committed_evidence_reinspection` for original citations
   touched by the committed diff, and `context.committed_change_relevance`
   for each path's selected records and unanchored candidates. Neither a
   fingerprint match nor an uncited path establishes changed semantic meaning.
   Use it only when historical intent can change the review. When the change could
   alter the product's possible futures, add `--include-candidates` to this
   committed review to see goal-linked opportunities and which BASE evidence
   sources overlap the committed diff. Inspect original possibilities and
   any `revisit_when` conditions; an overlap is not a feasibility verdict,
   and an omitted/unlinked possibility remains NOT ASSESSED.
   When reviewing **live uncommitted edits before a commit**, optionally add
   `--include-worktree --ref HEAD` to the same `workspace-review-context`
   command. It reuses BASE-revision product/architecture context while listing
   staged, unstaged and untracked path names; no working source bytes enter the
   index. Per-file context follows `review_scope.selection_order`: committed
   paths, then staged, unstaged and untracked paths, sorted within each group,
   so untracked artifacts do not take every `--max-paths` slot from pending
   source edits. Inspect
   `working_evidence_reinspection` separately from
   `committed_evidence_reinspection`, and each path's `change_modes` and
   `context.change_relevance`. It refuses a target ref other than the current
   checkout's HEAD. Absence of a matching path/record is not clearance; use
   actual source and Git diff to understand behavior.
4. Open the cited original source and verify applicability at current SHA. Run `knowledge-audit` against historical index when drift may matter. History order is indexing order, not automatically Git ancestry.
5. Distinguish validated contemporaneous evidence, historically correct but now superseded rationale, contested interpretation and unknown coverage. On `explain` or `why` use `--expect-kind alternative --expect-kind verification` when decision-relevant. Its `bounded_coverage` describes which kinds appear in the returned one-hop neighborhood, which are omitted by limit, and which were NOT ASSESSED **within that neighborhood**. It does not establish global decision completeness. Ask whether the retrieved sources cover the **specific engineering decision**, not merely whether their claims are correct within the modeled area. Name the smallest decision-relevant **NOT ASSESSED** area (for example, an alternative backend, an acceptance owner, or a dependency) and inspect its actual sources only when it could change the handoff.
6. When evidence appears to establish **BLOCKED**, **NO EXECUTION PATH**, or **NO DEFECT**, distinguish a missing particular dependency from absence of *all* authorized alternatives. Check the smallest relevant original architectural decision and owning implementation before passing on such a conclusion. Example from Auteur: missing direct-provider credentials do not alone rule out its documented host-agent-first handoff; the handoff's source existence does not prove the active host runtime can execute it. The active agent or `using-sensemaking` decides whether to inquire, act, or stop; Steward does not select a provider, authorize a model call, or become a second planner.
7. Give the active engineering agent the smallest useful evidence packet: decision, applicable claims, original source paths/revisions, supporting tests, alternative paths actually inspected and explicit uncertainties.
8. If retrieval contradicts current code or current owner intent, preserve the disagreement and initiate RECONCILE only when it would change a consequential future action.
9. Report decision-relevant gaps affecting the current result, source checks and remaining uncertainty in the task output. When a session receipt is available, also record queries, source checks and qualifying misses in its companion [query receipt](query-receipt.md) as work proceeds. Record earlier operations only as supported by available evidence and disclose omissions.

**Do not:** blindly trust retrieved text; load the whole graph into context; promote documentation or generated observations into owner authority; infer that an absent indexed alternative is absent in actual code; block a useful fix merely because indexing is absent. Implement and test in the current context. Fresh independent-agent verification is deferred to release qualification.

**Exit:** A source-checked architectural context that helps the active responsibility, with honest NOT ASSESSED entries instead of false negative results.
10. For an architecture-sensitive edit, use `rules-for` when its existing reviewed records could change the decision. Read the rule's epistemic status, original authority and ownership scope; hypothetical or unsupported rules are not obligations. `NOT_ASSESSED` and checker `rule_assessments` are evidence limits, not clearance. When one repository file's owners, contracts, decisions, history and tests may all matter, start with `knowledge-query --operation context-for --subject <file>`: each item states the explicit link that selected it, and `knowledge_gaps` lists what was not assessed. For a test file that no component owns, verification items name the file as `authority_ref` or `evidence_ref`, and `verified_components` lists the components it verifies whose supporting record is returned; that is relevance, not ownership. With `--repo .`, inspect `context.workspace_relevance` for changed indexed evidence sources before relying on a remembered decision; a source-path overlap is a re-inspection candidate, not a staleness verdict. When a real task spans several related files, use 2..8 repeated `--path` flags with `context-for` instead of `--subject`, retaining each path's independent `NOT_ASSESSED` and truncation limits and recording each in the query receipt when one is used. Use `rules-for` when only the rules are needed. Routine edits should not require an index-building stage.
11. When an active Campaign already binds the target and its responsibility is the edit in progress, `campaign working-context` with the `--knowledge-*` options can attach the same bounded `context-for` view, for one to eight files, beside the Campaign state. Identity mismatches, unindexed revisions and failed queries are explicit errors. Use the attached view only when it could change the decision. It is not a responsibility selection, a next action or permission to act. Without a Campaign, or without a suitable index, use steps 3 to 5 directly.
12. When the decision specifically turns on cross-session learning (whether earlier retained knowledge or a receipt was reused, helped or changed a decision), return the relevant retained claims together with the source, history and receipt or PR records needed to interpret them, and list the links that remain NOT ASSESSED. Do not rank that evidence, classify it as product benefit, or select the engineering responsibility. The active agent synthesizes the longitudinal picture (`../../using-sensemaking/references/ontology-first-entry-v1.md` section 4).
13. Read `context.relevance_candidates` after the `context-for` categories. It lists reviewed records that reach the file only through a capability its owner implements or by citing the file, each with its route and `applicability: NOT_ESTABLISHED`. A candidate is a record to open and judge, not an obligation and not clearance: check its original source, whether the capability has other implementing components, and its entry in `workspace_relevance.relevance_candidates` when a cited source changed. Report a candidate you relied on as a candidate. A category that is `NOT_ASSESSED` stays `NOT_ASSESSED` when candidates exist; if a candidate does apply, RECONCILE can anchor it to the owner. An `owner_verification / NOT_ASSESSED` gap means the returned tests belong to applicable rules, not to the owning component.

## Situation-aware historical lesson recall (optional)

Use this when the current engineering question involves a consequential assumption, repeated failure, historical architectural choice, misleading missing evidence, or a source file whose past incident could change the decision. The active agent decides whether consultation is warranted; a routine local edit does not require a lesson search.

1. **Enter from the current question or file, not a remembered lesson ID.** When an exact-commit index exists, prefer `context-for` for the file so reviewed owning-component `references`/`learned_from`/`contradicts` links can surface an `incident`, `lesson` or `observation` in `context.history`. If a relevant owner relationship is missing, the category can say `NOT_ASSESSED` even though a lesson exists elsewhere. Inspect the original code and authored packs before inferring historical absence. A context item's `recorded_conditions` (the record's own stated scope, claim ceiling, known limits and revisit condition) are the limits to test in step 3, not proof that the record applies here. A lesson item's `citing_records` names records that link to the lesson but not to the file, such as a later adaptation; read them too.
2. **Search narrowly when the path route is incomplete.** The existing `search --term` is literal, not semantic. Try important failure/contract terms and the `lesson:` prefix when useful; inspect reviewed `.sensemaking/knowledge/*.json` and source reports as fallback. For a known `lesson:` ID, use `explain`, then open the `authority_ref` and episode/PR/revision evidence. Neither text similarity nor a link alone proves applicability.
   When the question is about historical lessons but the lesson ID is unknown, an optional `search --query-text "..." --search-kind lesson` in `semantic workspace-query` (or `knowledge-query`) can limit lexical discovery to reviewed lesson claims. This is **not** semantic applicability ranking or a required lookup. Zero filtered matches are NOT ASSESSED outside the indexed lexical scope; source verification and contextual refusal remain necessary. Each returned lesson lists `citing_records`: the reviewed observations, incidents and lessons that link to it. Read them (`explain` on the lesson shows them) before step 3, because they may adapt, narrow or contest it. An empty list does not show that the lesson was never used.
3. **Compare conditions.** Reconstruct the earlier engineering question, belief or design option, evidence, actual result, source revision, interpreted lesson, and stated claim ceiling. Check the present repository's governing decisions, current source implementation, failure mechanism, context differences, and counterexamples. An incident is not automatically a rule, and one failure may have multiple plausible causes.
4. **Return a bounded precedent packet.** Give the active agent the historically verified lesson, applicability conditions, reason to apply/narrow/reject it now, most relevant original sources, remaining `NOT_ASSESSED` areas and what a wrong analogy would risk. Do not decide the engineering responsibility or treat a previous agent's interpretation as owner authority.
5. **Observe use separately from retrieval.** If the active agent later makes a consequential decision, distinguish lesson available, retrieved, source-verified, materially applied or rejected, outcome observed and genuinely fresh-agent reuse. Record only actually evidenced classes; source inspection or the CLI alone cannot establish that the lesson improved the result.

Example: for work on `knowledge_retrieval.py`, `lesson:query-completeness-is-evidence` is a *candidate precedent* because `docs/normal-use/semantic-stewardship-episode-a-2026-10-15.md` reports a historical bounded-query disclosure failure. The agent must still inspect the current query and actual truncation/coverage semantics. It must not infer that the repaired historical defect remains present, that the retrieved lesson is complete, or that merely reading it helped.

## Method Adaptation v0: optional agent-facing lifecycle

Use this when **authentic engineering work** raises a consequential choice of intellectual procedure, or when new evidence could change a prior conditional method. It does not activate for routine edits, mere technical-fact correction, or an effort to fill learning quotas. The host agent retains semantic control.

**Before a method choice, when historical procedure could matter:**

```bash
sensemaking-skills semantic method context \
  --question "How should this responsibility compare source evidence before deciding?" \
  --path docs/adr/0035-sensemaking-continuous-learning.md \
  --repo . --ref HEAD --json
```

This composes the existing exact-commit, zero-setup reviewed index; selects only `lesson` claims with an explicit authored `attributes.method`, uses lexical matching over the statement/procedure/recorded conditions, and includes linked later incidents or observations. The optional repeatable `--path` (up to eight repository-relative files) adds source-anchored discovery from authored evidence references and the existing reviewed `context-for` history: a candidate can surface because its source relates to the current file even without matching the question's words. The result identifies each `AUTHORED_SOURCE_REF` / `REVIEWED_CONTEXT_HISTORY` route, source coverage and truncation; a cited path establishes provenance, **not** file ownership or the method's applicability. All follow-up reads are pinned to the first query's exact commit even if the checkout's HEAD changes during the session. No semantic applicability ranking is performed. Source checks, current worktree differences, contrary evidence, authority and ACT/INQUIRE/CHALLENGE/etc. selection remain the host's work. A miss is `NOT_ASSESSED`, and a bound of 250 reviewed lessons is disclosed.

**After an actual episode, only if a reusable procedural insight merits retention:**

Author a UTF-8 JSON record of the episode and stage or commit it first. It must be a real source record: what decision arose, what intellectual procedure was used before and after, actual returned evidence, relevant scope/conditions/counterevidence, actor, exact source commit and a cautious claim ceiling. These are **authored assertions**, not recovered model reasoning.

The episode JSON has these fields:

```json
{
  "episode_id": "YYYY-MM-DD-unique-episode",
  "actor": "the actual executing agent or actor",
  "source_revision": "40-character Git commit SHA for the cited decision-time source",
  "decision": "consequential question and selected responsibility",
  "disposition": "develop | adapt | apply | reject | no_change",
  "procedure_before": "prior intellectual procedure, not merely a software hypothesis",
  "procedure_after": "changed conditional procedure, if developed or adapted",
  "observed_result": "source-grounded actual task outcome or limitation",
  "scope": "where the proposed method would and would not apply",
  "conditions": "conditions for conditional applicability",
  "counterevidence": "opposing observations, or explicitly NOT_ASSESSED",
  "revisit_when": "conditions for source-checked reconsideration",
  "claim_ceiling": "what the observation cannot show",
  "evidence_refs": ["file:tracked/evidence/path.md"],
  "prior_lesson_id": "lesson:existing-procedure-id, only if adapting/applying/rejecting it"
}
```

`develop` and `adapt` require a genuinely different, explicit before/after *reasoning procedure*; `adapt` requires a checked prior reviewed lesson **already present at the stated `source_revision`** (not merely a lesson introduced later on `HEAD`). The producer reports which tracked evidence paths were not yet present at that source commit: a later result may legitimately cite those paths, but their presence must not be retroactively attributed to the earlier decision. This mechanical history check does not prove a prior agent actually read a lesson. `apply` and `reject` preserve an attributed observation referencing a prior lesson without manufacturing a new method. `no_change` writes nothing. An input that merely changes a factual or technical hypothesis should use ordinary RECONCILE, not manufacture method adaptation.

```bash
git add path/to/actual-episode.json
sensemaking-skills semantic method record \
  --repo . \
  --episode path/to/actual-episode.json \
  --output .sensemaking/knowledge/method-episode-unique.json --json
sensemaking-skills semantic knowledge-proposal-check \
  --repo . --proposal .sensemaking/knowledge/method-episode-unique.json --json
```

The `record` command exclusively creates a **new, unreviewed** Git-authored knowledge proposal; it never overwrites the earlier lesson, commits, merges, edits shared Skills/policy, asserts verified cognitive gain or transfers authority. `develop/adapt` produce an attributed episode observation and a new conditional `lesson` with a `learned_from` edge. `apply/reject` produce only a linked observation. The existing knowledge-proposal checker and ordinary review/commit workflow remain necessary. A later agent can revisit these records through `context` and source-first RECALL.

**Claim ceiling:** This is usable method-development infrastructure plus reviewable evidence. A proposal is not genuine procedural adaptation unless the actual source supports it. Later independent use and comparative cognitive benefit remain separate qualification questions (#872 / #874 in the Sensemaking repository).

**Boundary:** optional, selective, source-grounded. No new query, mandatory protocol, implicit lesson scoring, automatic history ingestion or Skill controller is introduced.
