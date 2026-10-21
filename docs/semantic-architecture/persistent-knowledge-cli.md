# Persistent Semantic Knowledge — CLI and source contract

**Status:** Source/index foundation, orientation, Repository Semantic Steward and query-integrity repair are integrated (PRs #550/#553/#555/#551). Active-workspace context, explicit multi-phrase literal search and bounded decision-coverage metadata are integrated via PR #558. Local and hosted check receipts remain source-revision-specific; independent release qualification is still unproven.
**Authority:** ADR 0031 and the Git-reviewed original source documents. The index is never authority.
**Existing interface:** sensemaking-skills semantic (no new runtime or registered Skill).

## Purpose

Build a local, versioned, queryable semantic projection over a specific repository's committed sources and reviewed authored records. Agents can retrieve goals, capabilities, invariants, decisions, architectural links, evidence drift, contradictions and history. Results are source-linked claims and **candidate** impact paths, not instructions or verified architectural consequences.

## Scope

The source builder ingests only:
- Tagged lines from tracked .sensemaking/intent.md, context.md, invariants.md and decisions/*.md.
- Tracked docs/adr/NNNN-*.md title, declared status and bounded verbatim rationale/decision excerpts, plus NNN-*.md title/status and bounded literal excerpts (source authority remains unverified; inspect the source).
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

Other operations: snapshot, search, contradictions, history, changes and
workspace-impact (see active-workspace recall below).
Changes also requires --base-ref with a *previously indexed* revision.
The import-syntax option is --include-python-imports with --max-imports cap.

To inspect whether the **original source evidence** has drifted since an
indexed revision, while standing in a newer clean target checkout:

    sensemaking-skills semantic knowledge-audit       --db /tmp/semantic-knowledge.sqlite       --repo . --repository "ThorStarlord/sensemaking-skills"       --indexed-ref "$OLD_SHA" --current-ref "$(git rev-parse HEAD)" --json

This audit distinguishes unchanged source bytes, changed evidence sources,
missing/unsafe sources, and unassessed fingerprints. A change is a reason to
inspect the evidence, **not automatic revocation of its original authority**.
The command does not update SQLite or mutate the checkout.

## Construction: active-workspace recall (no clean-room development gate)

Build an index once at a normal clean committed HEAD, outside the checkout.
While source files are dirty, continue querying the previously indexed SHA;
the result is still a **committed-source snapshot**, not the working overlay.

Example for PowerShell on Windows (the indexed SHA must already exist in
the external database):

```powershell
$repository = 'ThorStarlord/sensemaking-skills'
$indexedSha = (git rev-parse HEAD).Trim()
$db = Join-Path $env:TEMP 'sensemaking-knowledge.sqlite'
sensemaking-skills semantic knowledge-query --db $db --repository $repository `
  --target-ref $indexedSha --operation search `
  --term 'semantic queries' --term 'query integrity' --repo . --json
sensemaking-skills semantic knowledge-query --db $db --repository $repository `
  --target-ref $indexedSha --operation explain `
  --subject 'cap:semantic-queries' --expect-kind alternative `
  --expect-kind verification --repo . --json
```

**Output and safety semantics:**

- Worktree inspection disables Git filesystem-monitor hooks and configured external clean/smudge/process filters; it also ignores submodule working-tree state, rather than execute repository-configured commands. `external_filter_commands_disabled_count` and `submodule_worktrees_not_assessed` disclose those limitations. Filter-managed files may therefore be conservatively reported as modified. Inspect submodules or custom filters separately before relying on a clean claim.
- `--repo .` adds `workspace_context` to any knowledge query. It reports
  `current_head`, `indexed_ref`, `head_matches_indexed_ref`,
  `worktree_clean`, `modified_tracked_count`, `untracked_count`,
  `uncommitted_changes_not_indexed`, and `source_alignment_not_semantic_truth`.
  Without `--repo`, old calls remain valid and omit this object.
- Repeated `--term` accepts 1–8 explicit nonempty phrases of at most 80
  characters, with case-insensitive literal OR semantics over claim ID or
  statement. Do not combine with `--subject`. `search_mode` and
  `search_hit_total` disclose the selection method and pre-limit match count.
  No synonyms, token search, embeddings or claim authority is inferred.
- `--expect-kind` applies only to `explain` and `why`. Its optional
  `bounded_coverage` reports expected claim kinds already returned,
  omitted by `--limit`, or **not assessed in the explicit one-hop
  neighborhood**. This is never a global completeness result.
- `--operation workspace-impact` requires `--repo` and answers "which
  reviewed indexed records cite files I changed?" It compares path names
  from `git diff --no-renames <indexed_ref>` (commits after indexing plus
  staged/unstaged edits) and untracked paths with each record's
  `source_sha256` keys. `workspace_impact.affected_records` separates
  `record_source_changed` (the authored knowledge file itself was edited)
  from `changed_evidence_sources`; mechanical path/containment matches are
  only counted in `mechanical_overlap_counts`. The overlap calculation
  consumes paths only; Git's diff machinery may inspect working-tree bytes
  when finding changed paths. Uncommitted bytes are **not incorporated into
  the indexed semantic snapshot or treated as indexed evidence**
  (`overlay_indexed=false`); the same filter/fsmonitor protections apply,
  and an indexed SHA missing from local Git is NOT ASSESSED. A listed
  record needs re-inspection, not revocation; changed code that no record
  cites is a coverage gap, not evidence of no semantic effect. Use
  `knowledge-audit` for byte-level drift once the checkout is clean.
- For source truth, inspect affected current code, owner documentation,
  tests and architectural alternatives. To retain a reusable decision in
  dirty work, preflight JSON with `knowledge-proposal-check`, run local tests
  and commit normally. Rebuild the derived index at the new clean commit.

**Construction claim ceiling:** same-session tests and dogfooding confirm
implementation behavior at the tested revision; they do not establish
independent-session cumulative value, cross-repository transfer, release
readiness, or a benchmark advantage.

## Change granularity and shared authored-pack limitation

Source change and semantic change are different questions:

- **Source-byte drift:** a cited file's bytes differ from a previously indexed committed revision. `knowledge-audit` reports this faithfully but cannot decide whether an authored architectural claim remains applicable.
- **Authored-record content change:** the specific claim's or relation's authored fields have changed; this is not the same as a changed fingerprint of the JSON file containing it.
- **Cited evidence change:** an implementation, test or decision source referenced by the record has changed, with no automatic conclusion about the record's validity.
- **Semantic reinterpretation:** a source-checking agent establishes a consequential change in meaning, rationale, decision status or applicability; neither a hash nor an unchanged file proves this.

**Known unresolved limitation (self-repository episode, 2026-10-21):**
`_authored_records()` fingerprints the entire `.sensemaking/knowledge/*.json`
container for every record it contains. Editing one record can therefore
cause `knowledge-audit` to flag every record in the pack as having changed
source bytes. Similarly, `knowledge-query --operation changes` compares
full record payloads, including `attributes.source_sha256`, so metadata-only
fingerprint changes can appear as `changed` claim/relation IDs. These
signals remain valid at their **stated** source/revision granularity but
are too coarse to infer which individual authored records changed meaning.
Treat them as re-inspection candidates rather than semantic deltas.

### Additive indexed change classification (PR #561 candidate)

Given two **already indexed committed revisions**, `knowledge-query --operation
changes --base-ref OLD --target-ref NEW` continues returning the original
`claim_delta`, `relation_delta`, `delta_total_counts` and top-level `truncated`.
Raw `changed` IDs still compare entire indexed payloads, including generated
source fingerprints. A new `change_classification` section explains those
raw changes without redefining them:

- `claims` / `relations`: stable-ID, deterministic, separately limited rows for
  records present in both revisions with unequal indexed payloads.
- `counts`: **pre-limit** totals per type, including assessed, NOT_ASSESSED,
  authored-field changes, authoring-location changes, origin-source drift,
  supporting-source differences and provenance-only cases.
- `truncated`: whether either detailed list omitted changed records under
  `--limit` (the original delta lists retain their own truncation semantics).
- Each assessed row includes `authored_fields_changed`,
  `authoring_location_changed`, `authoring_source_changed`,
  `changed_supporting_sources` and `provenance_only`.
- `changed_supporting_sources` reports path-level `fingerprint_changed`,
  `reference_added`, or `reference_removed`. Added/removed references indicate
  that the source was newly cited or no longer cited, **not** that its bytes
  changed.
- `assessment_status=NOT_ASSESSED` and `unassessed_reason` disclose unsupported
  record origin, missing/invalid fingerprints or missing container fingerprint.
  Unassessed facets return `null`, not a false assertion of no change.

`provenance_only=true` means the individual authored fields and location are
unchanged and no separately fingerprinted supporting-source difference was
observed; the full indexed payload difference is limited to generated
provenance fields. It does **not** certify that the architectural claim
remains true or that uncited/external evidence is unchanged.

Example (run from a clean source-index snapshot database containing both refs):

```sh
sensemaking-skills semantic knowledge-query --db /tmp/semantic-knowledge.sqlite \
  --repository ThorStarlord/sensemaking-skills --operation changes \
  --base-ref "$OLD_SHA" --target-ref "$NEW_SHA" --json
```

The classification reads existing SQLite payloads only; it requires no
schema migration and no new source indexer. It does not automatically assess
mechanical/ADR records, changes across different IDs, Git ancestry, semantic
validity, external evidence or unindexed information. `knowledge-audit`
continues its unchanged conservative source-byte drift contract.

See [the self-repository episode](../normal-use/semantic-steward-workspace-impact-2026-10-21.md)
for the agent-reported counts, source explanation and the separately scoped
follow-up. A future improvement should distinguish shared-container
provenance, individual record-content differences and independent evidence
drift without suppressing real source changes, dropping historical context
or treating an unassessed dependency as absent. No such repair is implemented
by the earlier PR #560 documentation follow-up. PR #561 introduces a candidate
per-record classification for `changes`, without narrowing source-byte audit,
erasing original raw deltas or establishing semantic truth.

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

A query may examine the current **dirty active checkout** with `knowledge-query --repo .`, which adds `workspace_context` including current HEAD, indexed revision, modified/untracked counts and a clear flag that uncommitted edits were **not indexed**. This never relaxes the clean HEAD requirement for `knowledge-build` and `knowledge-audit`.

The SQLite index retains multiple repository/SHA snapshots. Indexing identical inputs is idempotent, and conflicting data under the same source revision is rejected. Authored semantic conclusions remain Git-reviewed; do not commit or manually mutate the generated SQLite file.

- History reports **database indexing order**, not Git ancestry or causal chronology. The merged Episode A fix adds `history_total_entries` and marks `truncated` when the limit omits entries.
- Changes reports set differences, not proved semantic consequences. The merged Episode A fix adds `delta_total_counts` and marks `truncated` if any of the six delta arrays is shortened.
- Impact follows explicit edges only; an indexed path is not a transitive or causal proof. The merged Episode A repair bounds `depth` to one explicit edge per hop in either direction.
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

Machine tests can establish schema integrity, deterministic reconstruction, exact source revision binding and query behavior. The subsequent [query-integrity Episode A](../normal-use/semantic-stewardship-episode-a-2026-10-15.md) records an actual bounded development responsibility and a Git-authored lesson; it is NOT an independent-agent longitudinal success. The real-repository exact-head worktree smoke test establishes only source reconstruction and retrieval, NOT a fresh independent model's reuse of prior lessons. Genuine longitudinal compounding and incremental architectural benefit remain future evidence questions under ADR 0031.

S6 richness (other language adapters, domain-specific graph types, optional visualization or cross-repository fusion) should be driven by real consumers rather than auto-generating a complete ontology from arbitrary code.


## First-visit repository orientation and bounded structural skeleton

Use `knowledge-orient` to inspect a clean Git checkout without creating
an index or reading unreviewed product semantics:

```bash
REF="$(git rev-parse HEAD)"
sensemaking-skills semantic knowledge-orient --repo . \
  --repository "owner/repository" --target-ref "$REF" --json
```

The output contains Git path counts and bounded representative source/test
paths, manifest/document candidates, explicit truncation, source scope and
authority disclaimers. It cannot prove module ownership or application
behavior. `--max-files` and `--sample-limit` bound output work.
If `--db /path/outside/repository.sqlite` is supplied, exact-revision
semantic index counts/source scope are also returned (no index mutation).

Optionally include mechanically observed file/directory containment using
`knowledge-build --include-repository-structure --max-structural-files 600`.
The resulting `contained_in` relation is purely a tracked path relationship,
not a product dependency. It can coexist with `--include-python-imports`.
No new knowledge schema version, database or automatic semantic authority is
introduced.

See [Repository Semantic Bootstrap](repository-bootstrap.md) for scope,
evidence boundaries, source-drift handling and real-world qualification.


## Semantic steward — same-session safe draft authoring

`skills/repository-semantic-steward/SKILL.md` provides BOOTSTRAP, RECALL,
RECONCILE and read-only AUDIT instructions. While drafting an untracked
`.sensemaking/knowledge/*.json` file in a dirty working tree, use:

```bash
sensemaking-skills semantic knowledge-proposal-check --repo . \
  --proposal .sensemaking/knowledge/my-domain.json --json
```

This checks schema, endpoints and Git-tracked local evidence. It does NOT
establish semantic truth, current committed evidence, or owner authority.
For source-pinned indexing, commit the reviewed source/knowledge changes and rebuild the SQLite snapshot at the exact new SHA in the **same current checkout when naturally clean**. A fresh agent or separate clean-room worktree is not a construction prerequisite.
