# Architecture Exploration with Persistent Knowledge

**Status:** optional agent-facing guidance, ADR 0031 / Wave 4  
**Responsibility:** source-grounded architectural option exploration for an already warranted task  
**Authority:** the active engineering agent, never the knowledge index or this reference

## 1. Activation and decision boundary

Use this procedure when a meaningful architecture decision has alternatives, a preferred architecture needs challenge, or cross-session product history could change the choice. It is **not** a mandatory step for ordinary local edits.

- **Exploration-only:** return an opportunity/architecture landscape. Do not select the Strategic Frontier, grant implementation authority or manufacture a backlog.
- **Bounded architecture choice:** the active agent already has a warranted responsibility and may compare candidates inside it. This reference does not select that responsibility.
- **Open Level 3:** use the separate Strategic Exploration Funnel in `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md` for system map → breadth → frontier candidates → depth → construction paths → selection. Architectural options are not automatically frontier candidates.

This procedure operates under the Steward's existing `RECALL` and `RECONCILE` modes. Do not add a fifth Steward mode, a planning engine, a workflow-registry entry, or a new artifact schema.

## 2. Ground before divergent generation

Identify governing user/product intent, non-goals, current engineering scope and relevant authority. Pin the target repository, indexed SHA, current HEAD and dirty overlay. When a reviewed index already exists and could affect the decision, retrieve selectively:

- `context-for --subject PATH --repo .` for one file, or repeated `--path PATH` for 2–8 related paths. Preserve each path's distinct owner, contract, revision, uncertainty and truncation.
- `why --subject DECISION_ID` or `explain --subject CLAIM_ID` for known rationale.
- `contradictions` for competing records, `term` for disputed vocabulary, and `impact` only for candidate declared-edge effects, not proved consequences.
- `orientation-summary` if the system boundary itself is unclear; do not treat it as a complete architecture inventory.

Example with existing commands (paths are illustrative):

~~~bash
sensemaking-skills semantic knowledge-query --db "$db" \
  --repository owner/repo --target-ref "$indexed_sha" \
  --operation context-for \
  --path src/module_a.py --path src/module_b.py --repo . --limit 25 --json

sensemaking-skills semantic knowledge-query --db "$db" \
  --repository owner/repo --target-ref "$indexed_sha" \
  --operation why --subject decision:example --repo . --json
~~~

Read the **original** source of decisive claims (code, contract, owner decision, historical rationale). The index may be historically correct yet incomplete for this choice. `workspace_context` and `workspace_relevance` give source reinspection candidates, not a semantic staleness verdict; uncommitted code is not indexed. Missing indexed ownership/relations mean `NOT_ASSESSED`, not safe, absent, or authorized.

If no suitable index exists, inspect governing and implementation sources directly. Do not require BOOTSTRAP or an artificial test/benchmark as a condition for legitimate exploration.

## 3. Divergent architecture exploration

Start from the desired product/user outcome rather than the most visible defect or the graph's known nodes. Generate **materially distinct** mechanisms, not a prescribed number of cosmetic variants. Consider preservation/simplification, changed component boundaries, recombination of existing leverage, or a newly warranted capability when plausible.

For each serious option, identify:

- **Outcome and mechanism:** the improvement and which responsibility/contract actually changes.
- **Source-grounded present state:** reviewed intent, current code and accepted decisions.
- **Predicted value and tradeoffs:** explicitly hypothetical until supported.
- **Counterfactual premise:** if an existing boundary or assumption is challenged, name it and identify any required owner/Level-4 transition.

Do not suppress novel options just because the index has no matching node. Hypothetical guidance is not a current architectural obligation.

## 4. Convergent comparison

Compare material finalists qualitatively against goal fitness, constraints, owned interfaces and consumers, compatibility, migration, dependencies, reversibility, operating cost, failure modes and verification cost. Preserve explicit `observed` / `declared` / `hypothetical` / `contested` / `superseded` / `NOT_ASSESSED` distinctions.

Ask which original source or normal-use feedback could **change** the preferred choice. Inspect that smallest missing source where worth the cost. A valid graph edge, test-file existence, validator pass or CI check alone cannot establish design correctness or product benefit. Prefer a useful reversible build over a redundant experiment where evidence and authority allow it; do not prescribe experiments merely because alternatives exist.

## 5. Adversarial challenge

For a consequential preferred option, search for:

- unmodeled callers, hidden consumers, lifecycle transitions or external dependencies;
- a remembered decision whose authority/scope no longer applies;
- a synthetic semantic dependency inferred from an import, folder, or shared citation;
- a simpler viable option or a boundary the proposal would duplicate;
- accepted product non-goals, permissions, release promises or owner decisions that it could violate;
- an assumption that a local defect is actually a new Level-3 strategic frontier;
- missing verification falsely described as evidence of correctness.

Use `contradictions` and original source review only as needed. Challenge returns counterevidence and `NOT_ASSESSED` gaps, not a new veto or automatic selection.

## 6. Handoff, authority and memory

Return the smallest decision packet: user outcome, genuinely different options, source-pinned evidence, material tradeoffs/risks, uncertainty, disconfirming evidence, and a recommendation **only when selection was requested and authorized**. Exploration-only ends at possibilities and questions. An architectural option does not silently become a Strategic Frontier or construction path.

If using the existing `architectural-review` Skill downstream, honor its **separate** input contract: a current `repository_sensemaking_brief` and a concrete `proposed_direction`. That Skill evaluates the inherited proposal and does not independently re-diagnose the brief.

Log actual queries, original source checks, and material misses in the existing `semantic_query_receipt` under `RECALL`. On consequential subsequent evidence, apply `RECONCILE` with CONFIRM / REVISE / SUPERSEDE / ADD / CONTEST / NO_MODEL_CHANGE. Persist a chosen decision and useful rejected alternatives only when source-reviewed decision authority exists; proposed alternatives remain attributed hypotheses. Do not make a new database, duplicate full query payloads, or pretend that an agent's generated options were accepted by the owner.

**Claim ceiling:** guidance implemented ≠ usefulness proven; merged guidance ≠ independent-session improvement; selection ≠ merge/release/deployment authorization.
