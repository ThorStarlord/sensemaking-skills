# PATH-1 Construction Plan: Knowledge-Aware Campaign Continuation

**Status:** Detailed next-construction plan, not implemented. Selected under the owner's 2026-10-25 architect-and-builder direction; implementation decisions remain bounded by current source and accepted authority.
**Prepared:** 2026-10-25.
**Inspected base:** ThorStarlord/sensemaking-skills main@d92a5783f4804ed99ad8a3db0c82347b0af95fb7 (PRs #586 and #587 merged; no open PRs observed when planned).
**Governing Level 4:** ADR 0031; ADR 0029 remains the execution/authority boundary; ADR 0030 remains the compact Grounding Pack contract.
**Governing Level 3:** STATUS.md and artifacts/history/2026-10-23-strategic-repository-analysis.md (PATH-1), reaffirmed by artifacts/history/2026-10-24-strategic-reconciliation.md.
**Implementation posture:** Continuous Construction IS the Probe. The roadmap and strategic analysis guide selection, not a synthetic-testing gate. Do not author, run, or wait for unit tests or synthetic evidence tests as part of this construction sequence. Preserve existing CI configuration and any GitHub-enforced merge restrictions. A source review is not a passing test or release qualification.

## 1. Objective and source-grounded opportunity

Build a useful, read-only bridge between current Campaign responsibility context and reviewed source-pinned architectural knowledge, then use the integrated capability while performing a genuinely valuable non-validator engineering responsibility. The target outcome is that an active coding agent can see both the work it is authorized to do and the relevant earlier product/architecture rationale, with all uncertainties visible and without an automatic next-action recommendation.

Current source facts:

- src/sensemaking_skills/campaigns/execution.py exposes CampaignExecutionService.working_context(), which projects active responsibility, uncertainty, targets, authority, stop conditions, evidence, latest handoff and result; it does not select a next action.
- src/sensemaking_skills/campaign_execution_cli.py exposes campaign working-context --workspace ... --json, with only Campaign/execution-companion state.
- src/sensemaking_skills/semantic_cli.py exposes semantic knowledge-query --operation context-for with a specified repository, indexed Git ref, selected file path(s), optional active worktree and explicit bounds.
- src/sensemaking_skills/semantic_architecture/knowledge_store.py already provides query_knowledge() for one file and query_context_paths() for 2-8 distinct files at the same indexed revision.
- src/sensemaking_skills/campaigns/resume_capsule.py reconstructs declared Campaign state with progressive-disclosure profiles, explicitly excluding semantic recommendations. Do not replace or duplicate that model.
- skills/repository-semantic-steward/references/recall.md and reconciliation.md already define RECALL and RECONCILE, including source/currentness checks and NOT_ASSESSED.
- PRs #586 and #587 repaired the generic validator and extended source-linked knowledge through PATH-1/T15-T16. Neither establishes independent-agent usefulness.

The missing integration is an **opportunity**, not proof of a user-visible defect: the agent currently composes the Campaign view and reviewed knowledge view itself. Joining them may reduce missed rationale and rediscovery; that causal/product benefit remains a hypothesis to be refined through ordinary construction and use.

## 2. Strategic choice and tradeoffs

Selected: a small opt-in read-only knowledge view on the existing Campaign working-context front door, using the existing semantic query implementation.

Alternatives and why not selected now:

1. Another generic semantic query/index feature: possible retrieval value, but repeats the self-referential growth pattern identified by FRONTIER-1 without a new product consumer.
2. Expand the validator/reporting subsystem: the T15/T16 diagnostics could eventually deserve follow-through into run logs, but this is lower leverage than demonstrating knowledge during an actual engineering responsibility.
3. Add an automatic Campaign/Sensemaking planner or inject knowledge into every execution envelope: greater operational coupling, unearned authority ambiguity, extra compatibility cost and risk of duplicating Dark Factory.
4. Require manual query composition forever: minimal implementation cost, but does not improve the natural Campaign continuation entry point; keep it as a valid fallback if the bridge offers no real benefit.

The preferred shape is a **reversible build**: useful if retained, optional, easy to remove, and honest about the source identity of every returned claim. If source review shows existing manual composition is more appropriate, a narrow Skill-level integration rather than a CLI bridge is a valid implementation refinement; record why before expanding scope.

## 3. Non-negotiable boundaries

- No new planner, runtime control loop, semantic authority engine, automatic source selection, recommendation ranking, authorization, or Campaign schema migration.
- No writing to Campaign state, execution companion logs, reviewed knowledge, target repositories, or the SQLite index from the new read-only view.
- No implicit cross-repository association. Repositories, target alias (when necessary), paths and revision must be explicit or mechanically checked against the already-declared Campaign target.
- No loading the full graph into model context; use bounded existing context-for queries. Absence of records is NOT_ASSESSED, never proof of no dependencies.
- A query from an earlier exact revision is historical. An active dirty checkout remains an unindexed overlay. Do not promote source pinning into present semantic truth.
- The agent owns whether a responsibility remains warranted. A Campaign target, graph edge, indexed document or passing validator is not new action/merge/release/deploy permission.
- Do not add knowledge rows for volume, build a generic knowledge-to-Campaign synchronization service, create a second persistence format, change Dark Factory, or reopen ADR 0031 without a real thesis-level trigger.

## 4. Product contract: opt-in Campaign architectural context

### 4.1 Existing default remains stable

The current invocation must keep its existing output and exit semantics:

~~~sh
sensemaking-skills campaign working-context --workspace PATH --json
~~~

No new required arguments, no network dependency, no index requirement and no automatic semantic lookup.

### 4.2 Proposed opt-in syntax (implementation contract, not shipped yet)

~~~sh
sensemaking-skills campaign working-context \
  --workspace CAMPAIGN_WORKSPACE \
  --knowledge-db INDEX.sqlite \
  --knowledge-repository ThorStarlord/sensemaking-skills \
  --knowledge-ref EXACT_INDEXED_SHA \
  --knowledge-repo ACTIVE_CHECKOUT \
  --knowledge-path src/sensemaking_skills/campaigns/execution.py \
  --json
~~~

The four identity/index options and at least one --knowledge-path are an atomic opt-in group. Reject partial options with a clear diagnostic; do not silently fall back to the unaugmented view after an explicitly requested query fails.

Support exactly one source path first. Extend to 2-8 distinct paths by directly reusing query_context_paths() in the next slice. No glob interpretation and no traversal/absolute paths. Preserve the underlying query's limit and source/caveat semantics.

### 4.3 Output contract

Add only when explicitly requested:

- reviewed_knowledge.source_identity: repository ID, exact indexed ref, optional observed worktree HEAD and dirty state;
- reviewed_knowledge.target_binding: the explicit Campaign target alias and whether repository ID and source commit match, mismatch, or are NOT_ASSESSED;
- reviewed_knowledge.selected_paths: caller-selected source files, not inferred responsibility ownership;
- reviewed_knowledge.query: existing unmodified bounded context-for result(s), retaining owner/rule/contract/decision/history/alternative/test links, source refs, truncation and caveats;
- reviewed_knowledge.caveats: explicit historical/dirty/unindexed/coverage status and short actionable original-source inspection advice;
- reviewed_knowledge.semantic_truth_established = false and reviewed_knowledge.action_authorized = false.

Keep the current Campaign payload and all its authority/stop/companion-integrity fields intact. The wrapper must not turn retrieved rules into a selected responsibility or claim completion.

### 4.4 Identity and error behavior

- If multiple Campaign targets are present, require an explicit --target-alias before binding a knowledge query to one. Never guess which target the agent intended.
- Verify the declared repository ID against the selected Campaign target. On mismatch, return an explicit error rather than attributing other-repository knowledge to this Campaign.
- When the indexed source commit differs from the Campaign target head or current checkout head, retain the query only as HISTORICAL with an explicit mismatch disclosure; do not claim current applicability.
- Missing or corrupt indexes produce a visible opt-in query failure, not empty evidence interpreted as no risk.
- Existing context-for omissions, NOT_ASSESSED, returned-envelope limits and source-pinned evidence must remain visible. Do not synthesize implied edges.
- If the current worktree cannot be compared with the indexed commit, report workspace relevance as NOT_ASSESSED and preserve the older source-bound query rather than pretending alignment.
- No hidden remote fetch, credentials, telemetry, target-code execution or index rebuilding.

## 5. Construction sequence and PR boundaries

### T17 / PR A - First useful bridge: one explicit file

**Goal:** A coding agent can opt into one source-verified context-for result while reading an active Campaign's working context.

**Source areas:** src/sensemaking_skills/campaign_execution_cli.py; existing query_knowledge() and inspect_worktree_context() are reused, not reimplemented; a small pure read-only adapter in the Campaign CLI is acceptable. Extract a helper only if its real complexity warrants a separate module. Document the accepted invocation in docs/semantic-architecture/persistent-knowledge-cli.md.

**Implementation steps:**
1. Read the current Campaign working-context and semantic context-for payloads as separate authoritative mechanical views.
2. Keep CLI default unchanged; add explicit grouped knowledge flags for one file.
3. Check target identity and source ref; reuse the existing query without mutating Campaign records.
4. Attach bounded original query data and required historical/dirty/unknown caveats; preserve every original field.
5. RECONCILE-ADD only source-grounded product meaning in .sensemaking/knowledge/architecture.json: Campaign working-context component ownership, opt-in context relationship and the invariant that recalled knowledge cannot grant authority. Point to changed source and relevant accepted docs.
6. Update STATUS.md with the exact implemented scope and what remains unverified.

**Exit on construction evidence:** A reviewable, committed implementation with an opt-in interface and credible source-based contract reasoning, followed by an authorized PR merge. Do not call it tested/qualified or claim a real-user benefit.

**Stop/adjust when:** Source review finds the already-separated calls are sufficient and a combined output would create more misleading coupling than value. In that case ship only a carefully scoped agent-native consumption improvement and explain the rejected bridge; do not build a facade for its own sake.

### T18 / PR B - Multi-file responsibility context and omission honesty

**Dependency:** T17 merged and still worthwhile after source review.

**Source areas:** same opt-in Campaign CLI adapter and src/sensemaking_skills/semantic_architecture/knowledge_store.py query_context_paths() (reuse, modify only for a concrete contract gap); accompanying CLI reference.

**Steps:**
1. Allow 2-8 distinct --knowledge-path inputs; keep the single-file result shape compatible with T17.
2. Compose the existing source-pinned per-file results without inferred cross-file dependencies.
3. Expose per-path owners, rules, decisions, alternatives, omitted IDs/truncation, and shared returned records without implying global coverage.
4. Ensure an invalid path or mixed repository/revision group fails explicitly.
5. Keep output bounded and human-readable without adding new selection logic.
6. Reconcile any new durable architectural contract; NO_MODEL_CHANGE is valid when existing T17 knowledge remains sufficient.

**Exit:** An optional bounded multi-file context view; no change to command behavior for existing callers and no fabricated cross-file relationship.

### T19 / PR C - Agent-native continuation guidance

**Dependency:** T17/T18 provide a stable interface.

**Source areas:** skills/repository-semantic-steward/references/recall.md, skills/repository-semantic-steward/references/reconciliation.md, docs/semantic-architecture/persistent-knowledge-cli.md and GETTING_STARTED.md. Modify using-sensemaking or strategic-sensemaking-loop only if its existing guidance actually omits a decision-relevant boundary.

**Steps:**
1. Demonstrate the optional journey: read Campaign responsibility -> request selected path context -> inspect original authority/source -> build ordinary code -> reconcile consequential knowledge.
2. Show one-file and multi-file command examples with explicit repository/index SHA and active dirty-workspace caveat.
3. Clarify that Campaign resume-profile remains about durable Campaign state; it is not automatically an indexed repository knowledge answer.
4. Document how to continue when the index is absent: read original sources, do ordinary engineering and add reviewed knowledge only when warranted.
5. Explain non-automatic S5/S6 claims and when to skip Campaign entirely for a clear bounded task.

**Exit:** The active coding agent can discover the new optional capability without a new Skill, mandatory onboarding ritual or second planning controller.

### T20 / PR D - Genuine non-validator engineering responsibility

**Dependency:** Normal engineering work exposes a concrete Campaign-facing concern worth fixing; no synthetic problem is to be invented merely to complete this numbered task.

**Candidate inspection surfaces:** src/sensemaking_skills/campaigns/execution.py, src/sensemaking_skills/campaign_execution_cli.py, src/sensemaking_skills/campaign_resume_v2_cli.py and src/sensemaking_skills/campaigns/resume_capsule.py.

**Steps:**
1. Select the smallest real product behavior/invariant with direct source support, observed consumer and bounded correction. For example, check whether current execution handoff and resume views make an existing stop/authority boundary difficult to reconstruct; do not assume that defect exists.
2. RECALL the relevant indexed Campaign contract with the new interface, plus direct code/ADR inspection.
3. Implement the product change in the Campaign/resume/handoff domain, rather than in semantic query mechanics, when warranted.
4. Keep a concrete before/after statement about which code path and user/agent decision improved.
5. RECONCILE: CONFIRM/REVISE/ADD/SUPERSEDE only affected, source-grounded product knowledge. Preserve historical reasons and previously rejected alternatives where actually documented.
6. If no warranted product issue exists, do not fabricate a Campaign patch. Choose the next genuine non-validator responsibility through the existing PATH-1 decision process.

**Exit:** At least one intrinsically valuable engineering responsibility with retained code and relevant reusable understanding; a mere increase in graph-record count is insufficient.

### T21 - Strategic reconciliation and continuation, not a fixed additional PR

**Trigger:** Meaningful T17-T20 delivery evidence returns, an important assumption fails, or a currentness/authority conflict becomes consequential.

**Actions:**
1. Read committed diffs, current STATUS.md, the governing SRA and the dated reconciliation.
2. Compare observed product value with risks of incidental coupling, stale knowledge or unused context.
3. Decide PATH-1 CONTINUE, REVISE or REOPEN_ANALYSIS through ordinary Level-3 judgment. Do not re-run a strategic breadth funnel merely because the next PR merged.
4. Update STATUS.md and a durable reconciliation only when another context needs the conclusion. Do not rewrite the dated source artifacts as though they were current observations.
5. Select the next independent non-validator engineering responsibility when warranted; stop if the only available next work is speculative machinery.

### T22 - Conditional later extensions (NOT admitted implementation work)

Only consider these after real use reveals a concrete recurring limit:

- A source-linked reference in an execution handoff when agents repeatedly lose knowledge across actual worker boundaries; prefer existing evidence_refs and versioned payloads, not automatic graph injection.
- A better compact presentation if bounded query payload volume demonstrably obscures the decision.
- Downstream recording of advisory validation warnings into run logs if warning history becomes necessary for a real Campaign/ingestion decision; do not reopen the validator subsystem by default.
- Cross-repository or Dark Factory adaptation only through a separately selected target scope and owner/runtime authority, never by implicit expansion.

## 6. Review and integration procedure for each construction PR

1. Inspect exact main HEAD and the original source contract before editing. Prefer the current active checkout and context.
2. Select the smallest real responsibility and write code and focused retained knowledge when appropriate. No unit-test authoring, unit-test execution, synthetic evidence test or independent clean-room gate in this construction phase.
3. Review the source diff for boundedness, API compatibility, safety, relevant original documents and truthful currentness. A review is not a test result.
4. Update the current STATUS projection only for consequential new capability/status; keep dated strategic evidence immutable.
5. Open a reviewable PR, inspect its GitHub diff and mergeability, and merge promptly under the owner's explicit instruction without waiting for unit/evidence checks. Respect any actual GitHub-enforced protection and report blockers rather than bypassing them.
6. Check the merged main source identity and record exact claims: code merged, source reviewed, tests NOT RUN, field usefulness NOT ESTABLISHED, S5/S6 NOT ESTABLISHED.
7. Proceed to the next PR only when its dependency and continued product value remain warranted. Do not use a list of PRs as an automatic task executor.

## 7. Success, non-success and stop rules

**Construction success (not empirical qualification):**

- Existing Campaign working-context behavior is unchanged unless opt-in knowledge flags are supplied.
- A selected source file can retrieve explicit reviewed ownership, constraints, decisions and historical rationale beside a Campaign responsibility, preserving original source/authority and bounded coverage.
- Dirty/HISTORICAL/NOT_ASSESSED information remains explicit, and the output never claims permission to act, full architecture completeness or validated semantic truth.
- The agent can choose a genuinely valuable non-validator responsibility and retain any consequential reusable product understanding after implementing it.
- Every claimed merged capability is confirmed at exact integrated GitHub HEAD, without pretending unexecuted tests passed.

**Not established by construction alone:** Runtime correctness, independent agent/Skill attribution, longitudinal S5 reuse, S6 transfer, comparative advantage, release readiness or PyPI/publication permission. Those remain distinct later qualification and authority questions.

**Reassess or stop if:** the optional bridge is unused or creates more misleading source association than value; T17 implementation reveals unnecessary duplicated mechanics; new records routinely become stale; a protected permission/Level-4 boundary appears; or no next intrinsically useful repository responsibility exists.

## 8. Immediate next move

Start with T17, not another strategic analysis or generic evidence-test campaign. Inspect the exact current Campaign working-context and semantic context-for contracts, implement the smallest opt-in single-file source-pinned bridge if the source inspection sustains its value, add only directly useful reviewed knowledge in the same delivery, and merge the resulting construction PR. Continue to T18-T20 without owner prompts only while the next slice remains both warranted and authorized.

**Plan identity:** This file is an implementation compass. It does not create a new canonical roadmap, new state machine, release gate, or automatically authorized backlog.
