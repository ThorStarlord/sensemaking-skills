# A-trace: ontology author probe, graph viewer role and limits

Checkout: H:/codex/worktrees/oar-author, branch claude/ontology-author-reader-probe-20261105, HEAD 6f54a4a7eeb2a2101536f3307c37bb55a46dcbca.
Candidate: .sensemaking/knowledge/ontology-author-reader-probe.json (untracked, uncommitted, unpushed; the only change in the tree).
Final check: exit 0, SEMANTIC_KNOWLEDGE_PROPOSAL_VALID. That is a schema and path check, not semantic review.

## Disclosure

- I read H:/codex/oar-operator/manifest.md and progress.md while diagnosing the CLI failure. The manifest is headed "operator-only; no participant reads this". It told me this is an author-reader qualification with A/B/C roles, the host setup and that the plan and spec are in the tree. It did not contain the frozen question text. Treat this as contamination of this run.
- I did not open docs/superpowers/plans/2026-11-05-ontology-author-reader-qualification.md or its design spec. They appeared only as file names in grep output.
- The candidate's content comes from the product sources below. Knowing about the probe may still have influenced how compact and carefully hedged it is.
- `using-sensemaking` calls for a session receipt, and the Steward for a query receipt. Neither was written, because the task forbids any other repository file.

## Sources read

Named by the task, read in full unless noted:
- docs/semantic-architecture/agent-native-graph-viewer-v1.md
- docs/superpowers/specs/2026-11-05-agent-native-knowledge-graph-reasoning-design.md
- docs/semantic-architecture/premise-sensitive-reconsideration-contract-v1.md
- src/sensemaking_skills/semantic_architecture/knowledge_view.py
- src/sensemaking_skills/semantic_architecture/view_assets/graph_view.html (lines 120-189 and 385-460, plus text search of the rest)
- src/sensemaking_skills/semantic_cli.py (lines 191-241 and 285-386)
- docs/adr/0034-ontology-first-adaptive-sensemaking.md
- .sensemaking/knowledge/product.json

Additional:
- docs/semantic-architecture/persistent-knowledge-cli.md (lines 520-524)
- STATUS.md (lines 534-536, plus matches)
- skills/strategic-repository-analysis/references/premise-sensitive-reconsideration-v1.md (grep only)
- semantic_architecture/knowledge.py (kinds, predicates, authored-record parsers)
- stewardship_validation.py (inspect_knowledge_proposal)
- .sensemaking/receipts/2026-11-05-agent-native-knowledge-graph-reasoning-implementation.session.yaml (first 70 lines)
- pyproject.toml and MANIFEST.in (packaging matches)
- docs/adr/0033 (status line only)
- Installed Steward knowledge-contract reference
- Git log

Not read: docs/superpowers/plans/2026-11-05-agent-native-knowledge-graph-reasoning.md, the cases file, and the example view JSON (existence confirmed only). No hosted run log was opened.

## What existing records cover

I inspected the 10 authored packs directly (JSON parse plus grep). I did not query an index.

- The viewer is ABSENT_FROM_GRAPH. No record mentions knowledge_view, graph_view, knowledge-view, a graph viewer, or GraphExplorationView. No component owns the two viewer files.
- Reusable endpoints exist:
  - component:semantic-cli owns semantic_cli.py, but its statement predates and omits the view commands.
  - cap:semantic-queries and component:knowledge-store cover query_knowledge.
  - con:agent-owns-semantic-control, and decision:ontology-first-adaptive-sensemaking (product.json).
  - layer:knowledge-plane.
- Prior repository decision: the premise contract and STATUS record NO_NEW_SCHEMA / NO_NEW_PREMISE_QUERY / NO_NEW_REVIEWED_PACK for the premise-reconsideration slice. I read that as covering premise and strategic-artifact content, not the viewer's own role. This candidate adds no premise records and is a test artifact, not an accepted pack. The tension is real and unresolved for any future promotion.

## Records chosen (schema_version 2; 5 claims, 8 relations)

Claims:
- cap:source-pinned-graph-view: capability, declared, document authority. The viewer's role.
- component:graph-view-projection: observed, code authority. owned_paths are knowledge_view.py and graph_view.html, so file-level context-for can reach it. This is why the file uses schema 2.
- con:graph-view-secondary-read-only: constraint, declared, document authority. Normative limits.
- observation:graph-view-boundaries-in-source: observed, code authority. What the code actually enforces, including what it does not check. Kept separate from the normative constraint, as the knowledge contract requires.
- observation:graph-view-evidence-ceiling: observed, document authority. What is recorded as passed, failed and NOT_RUN.

Relations from the capability:
- implemented_by the new component, and implemented_by component:semantic-cli (scoped to the two commands)
- requires_capability cap:semantic-queries (scoped to export; render does not need it)
- constrained_by the new constraint, and constrained_by con:agent-owns-semantic-control
- references decision:ontology-first-adaptive-sensemaking (conceptual_relation governedBy)
- references each of the two observations

## Alternatives discarded

- decision record for "agent primary, viewer secondary": the only source is the spec's report of owner approval in conversation, so I did not mint an owner decision. The content lives in the constraint, with an authority_note.
- decided_by ADR 0034: the ADR never mentions the viewer. Used a weaker references edge instead.
- alternative records for the spec's declined approaches (graph-first, docs-only): not needed for role and limits; the spec remains cited.
- contract:graph-exploration-view-v1 with exposes: the contract document says it is not a registered artifact, and a contract record could imply that it is. The component statement names the envelope and cites the document.
- domain_concept for view vs reviewed knowledge: the constraint already carries the distinction.
- verification record or tested_by: text search found no test naming the module, so there is nothing to cite.
- belongs_to layer:knowledge-plane: no source places the viewer in a layer, and that layer's statement does not list presentation. Left NOT_ASSESSED. Consequence: layer-scoped rules will not reach the component through this candidate.
- depends_on component:knowledge-store: knowledge_view.py takes a dict and imports only patterns from knowledge.py, and the CLI does the wiring. A capability-level requires_capability is the accurate level.
- serves_goal: no source states which goal the viewer serves, so it would be my inference.
- Editing component:semantic-cli to mention the view commands: forbidden by the task. The stale omission remains.
- Premise roles and worked PATH-1 / ASSUMPTION-1 records: the sources reject these as graph records.

## Ambiguities and unresolved source roles

1. The spec header says "planning/specification only, not built/qualified", while the viewer doc, STATUS and git (merge e38b4156, PR #761) show it merged. I read the spec's status as stale on build state and used it only for design intent. It is not supersession and nothing says so explicitly.
2. Authority of the role decision: the spec says "owner-agreed" in conversation, no ADR exists for the viewer, and the receipt lists delegated merge and knowledge_edit grants. I used document authority and did not resolve whether it is owner-level policy.
3. Normative or descriptive: the viewer doc's "does not" statements read as both design limits and implementation facts. I split them into a constraint and an observation. Whether the constraint is a durable rule or merely describes v1 is not settled by any source.
4. SOURCE_DECLARED has two meanings in the contract: the class definition says the agent inspected the original, while the envelope rule says "source-declared relationship". The code assigns it from derivation alone, with no inspection. Recorded in the boundaries observation; which meaning governs is unresolved.
5. Evidence reporting differs: viewer doc section 6 names only the two passing hosted runs, and STATUS adds the Product Validation failure (3,634 passed, one failed). I used STATUS as the fuller record, without opening the logs. STATUS says a later PR repairs the enum; I did not confirm that the repair restored a green full suite on the viewer.
6. Hosted CI scope: text search of tests/, .github/ and scripts/ finds no reference to knowledge_view or knowledge-view, so what those runs exercised of the viewer is NOT_ASSESSED. The search cannot see indirect coverage.
7. Premise affordance: the HTML treats kind hypothesis or constraint, or any kind or id matching assumption or premise, as eligible for inversion. The docs say "premise/assumption". This is a small widening and is not in the candidate.
8. ADR 0033 is PROPOSED, but the parser accepts its schema 2 constructs and architecture.json already uses them. I used owned_paths on that existing basis; this does not ratify the ADR.
9. Render-path scope: comparisons and scenarios in curated views get only a list-type check. Not recorded separately beyond the general "validation does not check entailment".

## Expressiveness gaps (nothing extended)

- "Secondary to" and "hands back to" have no predicate. The primary/secondary ordering and the copy-back loop are prose in statements only, so a query cannot traverse them.
- There is no typed way to say "has no authority over X" or "does not write Y". Negative limits are prose under a constrained_by edge.
- No target for the coding-agent conversation or browser user as an actor. Neither is a claim kind.
- NOT_RUN and NOT_ASSESSED have no epistemic status or verification form. A `verification` claim would imply a check exists, so the ceiling is an `observation` about what documents record.
- A command inside an already-owned file cannot be owned or targeted: owned_paths is file-level. The two commands are reachable only through a scoped attribute on the relation.
- Attributes such as scope, conceptual_relation and authority_note are unchecked prose, so their meaning is not machine-enforced.

No semantic loss blocked the candidate. The limits above are all recoverable by reading, but not by traversal.

## Proposal-check results

Exact command in every case except attempt 2, from the checkout:
`sensemaking-skills semantic knowledge-proposal-check --repo . --proposal .sensemaking/knowledge/ontology-author-reader-probe.json --json`

The candidate file was never repaired; it passed on first write.

Pre-check tool state, before the candidate existed: the PATH CLI crashed on `sensemaking-skills --version` with `AttributeError: module 'click' has no attribute 'group'`. The uv tool's click directory held only __pycache__, and its uv-receipt showed rev d67cfe56. This was not a proposal check. By attempt 1 the tool worked and its receipt showed rev 6f54a4a7, with click populated. I did not change the tool, so another process refreshed it concurrently (not observed directly).

Attempt 1, exact PATH command: exit 0. Same payload as attempt 2. Displayed via `| tail -4` with exit taken from PIPESTATUS.

Attempt 2, isolated cross-check, not the requested command (worktree src, Python 3.11, click 8.5.0, pyyaml 6.0.3, via `uv run --no-project ... python -m sensemaking_skills.cli`): exit 0. It was launched because the PATH tool had just been failing. Payload identical.

Attempt 3, exact PATH command repeated after confirming tool identity (version 1.0.0rc5.dev0, rev 6f54a4a7): exit 0. Output discarded, code recorded only.

Exact JSON (attempts 1 and 2):

```json
{"action_authorized": false, "authority_verified": false, "claims_checked": 5, "code": "SEMANTIC_KNOWLEDGE_PROPOSAL_VALID", "existing_endpoints_checked": 4, "head_sha": "6f54a4a7eeb2a2101536f3307c37bb55a46dcbca", "limits": ["The source and referenced paths were inspected in the CURRENT WORKTREE, possibly dirty.", "Schema/path checks are not semantic truth, owner intent or behavioral verification.", "Full semantic knowledge indexing requires an exact clean committed Git HEAD."], "local_evidence_paths_checked": ["STATUS.md", "docs/semantic-architecture/agent-native-graph-viewer-v1.md", "docs/semantic-architecture/persistent-knowledge-cli.md", "docs/semantic-architecture/premise-sensitive-reconsideration-contract-v1.md", "docs/superpowers/specs/2026-11-05-agent-native-knowledge-graph-reasoning-design.md", "src/sensemaking_skills/semantic_architecture/knowledge_view.py", "src/sensemaking_skills/semantic_architecture/view_assets/graph_view.html", "src/sensemaking_skills/semantic_cli.py"], "proposal": ".sensemaking/knowledge/ontology-author-reader-probe.json", "relations_checked": 8, "semantic_truth_established": false, "valid": true, "worktree_clean": false}
```

## Not run

- knowledge-build and knowledge-query on the candidate. Build needs a clean commit, and committing is forbidden, so actual retrievability through search or context-for is untested. It is only supported by the owned_paths and the statement wording.
- Viewer export, render, or any browser use.
- Unit tests.
