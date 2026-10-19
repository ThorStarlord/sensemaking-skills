# Typed, source-bound knowledge contract

The canonical model and validator live in `src/sensemaking_skills/semantic_architecture/knowledge.py` and `knowledge_sources.py`. **Use the implementation's actual currently accepted types**; do not invent an unvalidated ontology. Current v1 families include goal, non_goal, domain_concept, capability, constraint, invariant, contract, component, source, verification, decision, alternative, incident, lesson, hypothesis, opportunity and observation. The bootstrap candidate adds a mechanically observed `directory` kind.

Relations include `serves_goal`, `requires_capability`, `constrained_by`, `depends_on`, `implemented_by`, `tested_by`, `decided_by`, `supersedes`, `contradicts`, `derived_from`, `affected_by_change`, `learned_from`, `candidate_opportunity_for`, `defines`, `references`; the bootstrap candidate adds lexical `contained_in`.

## Authoring

Write a reviewed, Git-tracked file under `.sensemaking/knowledge/*.json`:

```json
{
  "schema_version": 1,
  "claims": [
    {
      "id": "cap:book-reentry",
      "kind": "capability",
      "statement": "Show the current Book and its working Chapter state when reopening the workspace",
      "authority_kind": "document",
      "authority_ref": "docs/product/book-workspace.md",
      "evidence_refs": ["file:docs/product/book-workspace.md"],
      "epistemic_status": "declared"
    }
  ],
  "relations": []
}
```

The example path is illustrative, not a claim that the document exists. All `file:` references and authority paths must resolve to legitimate tracked evidence on the target repository before a committed index is built.

### Hard boundaries

- `epistemic_status=observed` requires source-inspected evidence, not a design aspiration.
- A declared decision/status may be a *document observation*, without thereby verifying policy authority.
- `authority_verified`, `semantic_truth_established` and `action_authorized` cannot be author-promoted.
- Evidence must be locally source-linked, currentness-reconciled and properly scoped. Histories and uncertainty are legitimate first-class outcomes.
- A dependency relation must be sourced in actual architecture/code evidence; same-directory placement and syntax-only imports are insufficient.
- Only accepted domain ownership workflows can change target-repository canonical/product state.

## Existing CLI

```bash
sensemaking-skills semantic knowledge-orient --repo . --repository owner/repo --target-ref "$REF" --json
sensemaking-skills semantic knowledge-build --repo . --repository owner/repo --target-ref "$REF" --db /outside/index.sqlite --include-repository-structure --json
sensemaking-skills semantic knowledge-query --db /outside/index.sqlite --repository owner/repo --target-ref "$REF" --operation explain --subject cap:book-reentry --json
sensemaking-skills semantic knowledge-audit --db /outside/index.sqlite --repo . --repository owner/repo --indexed-ref "$OLD_SHA" --current-ref "$REF" --json
```

No `knowledge-build` operation accepts a dirty checkout; use a clean detached snapshot/worktree. The database path must stay outside target checkout; the generated SQLite file is not a reviewed semantic source. Query results describe declared edges and indexed source, not a validated complete graph.
