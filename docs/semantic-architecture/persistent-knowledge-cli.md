# Persistent Semantic Knowledge — CLI and source contract

**Status:** Candidate S1-S4 implementation on PR #550, stacked on owner strategy PR #549.
**Authority:** ADR 0031 and the Git-reviewed original source documents. The index is never authority.
**Existing interface:** sensemaking-skills semantic (no new runtime or registered Skill).

## Purpose

Build a local, versioned, queryable semantic projection over a specific repository's committed sources and reviewed authored records. Agents can retrieve goals, capabilities, invariants, decisions, architectural links, evidence drift, contradictions and history. Results are source-linked claims and **candidate** impact paths, not instructions or verified architectural consequences.

## Scope

The source builder ingests only:
- Tagged lines from tracked .sensemaking/intent.md, context.md, invariants.md and decisions/*.md.
- Tracked docs/adr/NNNN-*.md title and declared status (not the full rationale; follow the source).
- Git-reviewed, tracked .sensemaking/knowledge/*.json records (schema version 1).
- Optionally bounded Python AST import **syntax** observations through the existing probe.

It does not infer owner intent from code, infer semantic dependencies from word matches, inspect all TypeScript relationships, fetch external services, or treat absent relations as proof of absence. Empty/sparse output means NOT ASSESSED.

## Build and query

From a CLEAN target Git checkout, store the SQLite index outside the checkout:

    cd /path/to/repository
    REF="$(git rev-parse HEAD)"
    test -z "$(git status --porcelain --untracked-files=all)"

    sensemaking-skills semantic knowledge-build --repo . \
      --repository "ThorStarlord/sensemaking-skills" \
      --target-ref "$REF" --db /tmp/semantic-knowledge.sqlite --json

    sensemaking-skills semantic knowledge-query \
      --db /tmp/semantic-knowledge.sqlite \
      --repository "ThorStarlord/sensemaking-skills" \
      --target-ref "$REF" --operation explain \
      --subject "cap:semantic-queries" --json

    sensemaking-skills semantic knowledge-query \
      --db /tmp/semantic-knowledge.sqlite \
      --repository "ThorStarlord/sensemaking-skills" \
      --target-ref "$REF" --operation why --subject "adr:0031" --json

    sensemaking-skills semantic knowledge-query \
      --db /tmp/semantic-knowledge.sqlite \
      --repository "ThorStarlord/sensemaking-skills" \
      --target-ref "$REF" --operation impact \
      --subject "cap:semantic-queries" --depth 2 --json

Other operations: snapshot, search, contradictions, history and changes.
Changes also requires --base-ref with a *previously indexed* revision.
The import-syntax option is --include-python-imports with --max-imports cap.

To inspect whether the **original source evidence** has drifted since an
indexed revision, while standing in a newer clean target checkout:

    sensemaking-skills semantic knowledge-audit       --db /tmp/semantic-knowledge.sqlite       --repo . --repository "ThorStarlord/sensemaking-skills"       --indexed-ref "$OLD_SHA" --current-ref "$(git rev-parse HEAD)" --json

This audit distinguishes unchanged source bytes, changed evidence sources,
missing/unsafe sources, and unassessed fingerprints. A change is a reason to
inspect the evidence, **not automatic revocation of its original authority**.
The command does not update SQLite or mutate the checkout.

## Authored source example

A reviewed .sensemaking/knowledge/sample.json can use this schema:

    {
      "schema_version": 1,
      "claims": [
        {
          "id": "goal:durability",
          "kind": "goal",
          "statement": "Persist authored work across restarts",
          "authority_kind": "policy",
          "authority_ref": "docs/PRODUCT.md",
          "evidence_refs": ["file:docs/PRODUCT.md"],
          "epistemic_status": "declared"
        },
        {
          "id": "cap:save",
          "kind": "capability",
          "statement": "Save the current draft",
          "authority_kind": "policy",
          "authority_ref": "docs/PRODUCT.md",
          "evidence_refs": ["file:docs/PRODUCT.md"]
        }
      ],
      "relations": [
        {
          "id": "rel:save-goal",
          "subject": "cap:save",
          "predicate": "serves_goal",
          "object": "goal:durability",
          "evidence_refs": ["file:docs/PRODUCT.md"]
        }
      ]
    }

The cited files must actually exist and be tracked. The real repository seed at .sensemaking/knowledge/stewardship.json uses ADR 0031, ADR 0030, actual source files and tests, with explicit claim ceilings.

Authored records may declare owner/policy references but cannot assert that authority was *verified*. The query result preserves authority_verified=false. An agent must inspect the cited source, and cannot relabel delegated or hypothesized choices as owner intent.

## Identity, persistence and history

Build checks exact 40-character Git HEAD, clean target worktree, tracked non-symlink input paths, and in-root cited local files. Evidence files are SHA-256 hashed, making an underlying source change visible in a later revision even when the claim statement remains identical.

The SQLite index retains multiple repository/SHA snapshots. Indexing identical inputs is idempotent, and conflicting data under the same source revision is rejected. Authored semantic conclusions remain Git-reviewed; do not commit or manually mutate the generated SQLite file.

- History reports **database indexing order**, not Git ancestry or causal chronology.
- Changes reports set differences, not proved semantic consequences.
- Impact follows explicit edges only; an indexed path is not a transitive or causal proof.
- Contradictions reports explicit conflicts only; missing conflicts means NOT ASSESSED.
- Query results carry currentness/revision, source/evidence provenance, limits and no-authority flags.

## Skill usage

1. Find a relevant claim or decision with search/why/explain.
2. Inspect cited original owner, product, ADR, code and test evidence at its source revision.
3. Use only source-checked relationships to inform architectural alternatives and change-impact analysis.
4. If an edge is stale, missing or contested, state the uncertainty; do not fill it with an invented dependency.
5. On consequential engineering work, update accepted Git semantic records and the relevant source docs, then rebuild the index at the new revision.

No mandatory indexing stage is required for routine local coding. The index is a product capability for recurring long-horizon understanding, not a second source of truth or automatic authorization plane.

## Qualification boundaries

Machine tests can establish schema integrity, deterministic reconstruction, exact source revision binding and query behavior. The real-repository exact-head worktree smoke test establishes only source reconstruction and retrieval, NOT a fresh independent model's reuse of prior lessons. Genuine longitudinal compounding and incremental architectural benefit remain future evidence questions under ADR 0031.

S6 richness (other language adapters, domain-specific graph types, optional visualization or cross-repository fusion) should be driven by real consumers rather than auto-generating a complete ontology from arbitrary code.


## First-visit repository orientation and bounded structural skeleton

Use \`knowledge-orient\` to inspect a clean Git checkout without creating
an index or reading unreviewed product semantics:

\`\`\`bash
REF="$(git rev-parse HEAD)"
sensemaking-skills semantic knowledge-orient --repo . \
  --repository "owner/repository" --target-ref "$REF" --json
\`\`\`

The output contains Git path counts and bounded representative source/test
paths, manifest/document candidates, explicit truncation, source scope and
authority disclaimers. It cannot prove module ownership or application
behavior. \`--max-files\` and \`--sample-limit\` bound output work.
If \`--db /path/outside/repository.sqlite\` is supplied, exact-revision
semantic index counts/source scope are also returned (no index mutation).

Optionally include mechanically observed file/directory containment using
\`knowledge-build --include-repository-structure --max-structural-files 600\`.
The resulting \`contained_in\` relation is purely a tracked path relationship,
not a product dependency. It can coexist with \`--include-python-imports\`.
No new knowledge schema version, database or automatic semantic authority is
introduced.

See [Repository Semantic Bootstrap](repository-bootstrap.md) for scope,
evidence boundaries, source-drift handling and real-world qualification.
