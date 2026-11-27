# Long-Horizon Adaptive Strategic Development (v1)

**Purpose:** an integrated, portable agent-facing development experience under the single `using-sensemaking` controller. The owner-ratified definition is recorded in ADR 0038 where the framework repository is available. The active agent owns judgment; this reference does not add an authority source, workflow, schema or controller.

**Load when:** the user delegates sustained product/repository development, a long-horizon outcome, or strategic continuation across responsibilities or sessions. Also load when repeated bounded tasks are part of an explicitly sustained engagement and knowledge maintenance or strategic continuity is materially at risk. For isolated, already-grounded work use the lightest direct path. A terminal mission ends at its authorized outcome or genuine boundary; sustained engagement does not authorize unbounded execution.

## What development means

Long-horizon development is not merely long-running execution. Strategy selects worthwhile directions; prospective reasoning considers consequences and newly enabled futures; continuity preserves the understanding and rationale needed to reconsider those directions across contexts. Support strategy-guided work within accepted direction and strategy-generating exploration when direction is open. A recommendation to alter a reserved commitment must go to its authorized decision maker.

Two mutually reinforcing intended outcomes matter: valuable domain development and attributable cognitive development. Pursue real work even when it yields no new lesson. Preserve procedural adaptations only when actual experience warrants them. Do not privilege an isolated local cost saving if repeated rediscovery, lost assumptions or strategic drift materially increase total cost; do not create artifacts whose expected reuse cannot justify their maintenance.

## Five dimensions of continuity

| Dimension | Decision-time question |
| --- | --- |
| Directional | Does the selected work serve governing purpose and remain worthwhile under changed conditions? |
| Semantic | What relevant understanding is already available, current or missing? |
| Prospective | What possibilities become valuable, feasible, invalidated or newly discovered after real work? |
| Cognitive | What attributable method experience could improve the current reasoning approach? |
| Developmental | What actual benefit does this responsibility create, and how does it alter the next useful responsibility? |

These are properties of the sustained experience, not a score, stage gate or demand for five new artifacts. A clear repair can make a strong contribution to a long trajectory. A lengthy strategic study that does not change understanding or action may contribute little.

## Developmental trajectory reasoning

When future capabilities, enabling conditions, alternative routes, or changes to deferred directions could affect a present strategic decision, load [Developmental Trajectory Reasoning (DTR)](developmental-trajectory-reasoning-v1.md). Cultivate the decision-relevant landscape across selected and unselected futures, using existing strategic artifacts and reviewed possibilities. Reconcile affected trajectories after material developments, not just progress on the selected path. This is a complementary intellectual responsibility, not an additional lifecycle stage, controller, or mandatory record.

## Authority and entry

Determine the repository, exact source revision, actual loaded Skill path/version where the host exposes it, available CLI identity and permissions. Compare intended source, installed files, available executable and loaded content separately. An installed hash is not proof of loaded bytes. If the pinned tooling is unavailable, use the authoritative Skill source explicitly and record the limitation; do not replace a shared installation in another actor's active session. Continue from original sources when possible.

Recover the user's governing purpose and existing product authorities; distinguish stated goals, inferred intent, strategic discretion and protected commitments. For a sustained mission establish explicit knowledge-edit authority as part of the delegation envelope, independently of code-write and merge rights. If withheld, perform read-only recall and provisional modeling and identify the affected stewardship responsibility. Do not treat the absence of that permission as a global construction freeze. The owner may delegate ordinary strategic selection, knowledge review and canonical integration within an agreed scope without approving each task.

## A durable lifecycle, not a fixed sequence

| Surface | Producer / creation trigger | Consumer / use | Update / omission |
| --- | --- | --- | --- |
| Target governing docs and optional `.sensemaking/intent.md`, invariants and decisions | Owner/authorized agent captures non-derivable intent, goals, non-goals and authority links | Entry and strategic decision; inspect actual governing sources | Update on authorized intent change; reuse authoritative existing docs rather than duplicating |
| `.sensemaking/knowledge/*.json` | Repository Semantic Steward BOOTSTRAP when sustained engagement meets inadequate domain/architecture knowledge; RECONCILE for consequential changes | RECALL current task-relevant concepts, goals, relationships, decisions, alternatives, experience; verify cited sources and applicability | Add/revise/supersede affected records via existing knowledge contract, proposal validation and review; NO_MODEL_CHANGE when nothing reusable changed |
| Derived SQLite knowledge index outside checkout | Existing semantic CLI builds/reuses exact-source projection when useful | Source-pinned queries and change/audit candidates; inspect coverage and dirty overlay limits | Rebuild for new revision when needed; not an authority or prerequisite to reading Git-authored knowledge |
| `artifacts/strategic_repository_analysis.md` | Strategic Repository Analysis when product/repository direction is materially open | Current system, possibilities, compared paths, decision-changing uncertainty and disposition | Reuse/reassess prior analysis; no repeat for settled local work |
| `artifacts/strategic_reconciliation.md` or existing dated equivalent | Strategic Repository Reconciliation when evidence materially affects the earlier strategic state | Next strategic decision; reconstruct what changed and why | Reaffirm, revise, reopen, defer or escalate with provenance; preserve historical analysis |
| `.sensemaking/receipts/*.session.yaml` | Controller opens, updates and finalizes one receipt per session (see session receipt contract) | Relevant receipts at entry: unfinished work, prior findings, open questions, next candidate and source pointers | Final receipts immutable; linked successors correct or extend; validate with existing tooling when available and disclose unavailable validator |
| `.sensemaking/receipts/*.query.yaml` | Steward query receipt when applicable under its contract | Inspect retrieval hits, misses, source checks and reconciliation evidence | Same session linkage; a miss does not prove absence and a receipt is not reviewed knowledge |
| Reviewed lesson / method observation and conditional proposal | SCL and existing Method Adaptation guidance when consequential experience changes a reasoning procedure | Later agent retrieves prior procedure with provenance, conditions, counterevidence; adopts, adapts or rejects before a consequential decision | Retain selectively, separate domain fact and method change; authorized review before promotion into shared knowledge or guidance |

Use [the sibling Repository Semantic Steward](../../repository-semantic-steward/SKILL.md), its BOOTSTRAP/RECALL/RECONCILE references, `ontology-first-entry-v1.md`, `session-receipt-v1.md`, and the existing Method Adaptation guidance for actual contracts. Do not infer a schema from this table.

### First sustained engagement

Identify actual product purpose, systems, authority, source revision and existing knowledge. Use BOOTSTRAP for inadequate coverage in the intended sustained scope, retaining a useful reviewable model if authorized (not an exhaustive file catalog). Establish a provisional model otherwise. When direction is materially open, explore and compare possible futures through Strategic Repository Analysis; make adequate possibility coverage and uncertainty explicit. Establish the warranted strategic direction or a justified nonselection, then undertake authorized work. If the first responsibility is already clear, do not block it behind a full repository analysis: establish or deepen knowledge incrementally at a natural boundary.

### Returning engagement

If the CLI is available, `handoff --repo TARGET --expected-source-ref SHA --resume-from .sensemaking/receipts/SESSION.session.yaml --question ...` inventories current paths and validates only explicitly selected receipts. Use its bounded historical projection as a source-reading aid, not an automatic predecessor, strategy or authority. Requested, installed/recorded, executable and loaded identity remain separate. The same handoff separates detached proposal and historical JSON paths from knowledge-directory paths. Where prior exploratory work could change the current choice, inspect the relevant original synthesis or draft and its actual disposition against reviewed knowledge; an old draft may already have been integrated or rejected. Recover, reconsider or review only when warranted. The handoff does not read or validate proposal contents or authorize promotion. Without the bridge, read original artifacts directly.

Read the current request and governing authority; recover relevant earlier receipts, knowledge and strategic artifacts, not all history. The optional receipt reader `python scripts/summarize-receipts.py --repo <target-repo>` is run from the framework checkout/installed runtime, if present, otherwise inspect source YAML. Treat a recorded NEXT as a defeasible candidate. Use RECALL before a decision where previous understanding could matter. With a current CLI, `sensemaking-skills semantic workspace-query --operation product-outline --include-candidates --json` provides a source-pinned goal/candidate view; a narrow lexical question search is `sensemaking-skills semantic workspace-query --operation search --query-text "..." --json`. Review actual query scope and cited source. Use the Steward's existing pinned tool invocation and validation guidance rather than requiring a local package installation. If the CLI is missing, inspect authored knowledge and original evidence directly. Do not claim mechanical validation when it did not run.

### During and after construction

Choose the intellectual approach through AMS in proportion to the decision. Consider future enablers and opportunity cost, compare material alternatives, and retain the decisive rationale where useful. Build, observe and evaluate a real product outcome when authorized. Consequential new facts, corrected assumptions, invalidated possibilities, new opportunities and method experience feed stewardship/SCL and strategic reconciliation as relevant. A minor change can leave the model unchanged; sustained absence or material staleness across substantial work merits attention even if no local task strictly required an ontology edit. Distinguish a real NO_MODEL_CHANGE from an unassessed or unauthorized knowledge responsibility.

Before finalizing, ensure a future consumer can recover relevant knowledge and unresolved decisions without reconstructing the conversation. Validate the receipt using `sensemaking-skills validate --artifact <file> --target-repo <target-repo>` or `python scripts/validate-receipt.py <file> --target-repo <target-repo>` according to the existing contract and available runtime (check exact command help when needed); record NOT_RUN when inaccessible. Keep final receipts immutable and respect current Git/publish permissions.

## What success looks like

A subsequent real responsibility should recover applicable prior understanding, select a warranted next responsibility, use or adapt the appropriate intellectual method, create valuable outcomes, and make the consequential experience available for further work. A useful unchanged decision can be a success; method adaptation requires observed procedural change, not merely a successful repair. Review domain outcomes and cognitive contributions separately. Record what was not assessed; do not assert causality, comparative benefit, longitudinal transfer, host identity or generalized cognitive improvement from a receipt, a new ontology or a merged PR.

Use the target's own development/verification policy. Never import this framework repository's local merge/test exception into another target. No competing write mission in a beneficiary repository; hand off knowledge proposals to its authorized integration owner. Preserve privacy and separate domain-owned records, attributable agent methods and shared reviewed guidance.
