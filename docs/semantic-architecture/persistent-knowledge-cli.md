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

When the active checkout is dirty (an open session receipt is untracked, for
example) or a historical revision is needed as a `changes` base, add
`--temporary-checkout` and pass any local commit as `--target-ref`:

    sensemaking-skills semantic knowledge-build --repo . \
      --repository "ThorStarlord/sensemaking-skills" \
      --target-ref "$(git rev-parse HEAD)" --temporary-checkout \
      --db /tmp/semantic-knowledge.sqlite --json

The command checks out the commit in a temporary detached `git worktree`
outside the repository, indexes it there under the same clean-source checks,
and removes it; the active working tree is never read. The checkout step
disables hooks, the filesystem monitor and configured external
clean/smudge/process filters (the clean-source checks then run as in an
ordinary build), and a commit whose attributes assign a filter to a tracked path is refused,
because its unfiltered bytes would differ from an ordinary checkout. A
snapshot built this way is identical to one built from a clean checkout of
the same commit. A shallow clone indexes only commits it has. An interrupted
run can leave a worktree entry that `git worktree list` marks prunable.
`git clone --shared` was not used, because Git ignores `--shared` for a
shallow source and copies objects instead.

`knowledge-orient`, `knowledge-check-rules` and `knowledge-audit` accept the
same flag under the same checks and limits; audit applies it to
`--current-ref`. The JSON output then gains `source_checkout`
(`temporary_worktree`) and `active_checkout`, which reports `head`,
`head_matches_source_ref`, `worktree_clean`, `modified_tracked_count`,
`untracked_count`, `working_changes_read` (always `false`) and `note`, a fixed
sentence saying that the active checkout was not read and that its uncommitted
and untracked changes are not part of the result. Everything else equals a
clean-checkout run at the same commit. Without the flag, a dirty checkout or a
ref other than the checked-out HEAD is refused, and the refusal ends with a
hint naming `--temporary-checkout`. `knowledge-build` reports
`source_checkout` in both modes and has no `active_checkout` object. These
three commands add their two keys only with the flag. The refusal of
`knowledge-build` ends with the same hint.

The temporary worktree belongs to the same repository, so it uses that
repository's Git configuration and checks out the same bytes as its ordinary
checkout. Source fingerprints are taken from the bytes Git checks out, after
any line-ending conversion that the repository's configuration applies. A
separate clone can differ: under another `core.autocrlf` setting its text
files have other line endings, and `knowledge-audit` then reports cited text
files as changed. Observed on one Windows host on 2026-11-10, in an audit of
an index of commit `53b667c1` run at commit `baaec6b9`: 442 of 442 records
reported changed from such a clone, against 139 of 442 from a worktree of the
repository itself.

Other operations: snapshot, search, contradictions, history, changes and
workspace-impact (see active-workspace recall below).
Changes also requires --base-ref with a *previously indexed* revision.
The import-syntax option is --include-python-imports with --max-imports cap.

To inspect whether the **original source evidence** has drifted since an
indexed revision, while standing in a newer clean target checkout (or, with
`--temporary-checkout`, a dirty one):

    sensemaking-skills semantic knowledge-audit       --db /tmp/semantic-knowledge.sqlite       --repo . --repository "ThorStarlord/sensemaking-skills"       --indexed-ref "$OLD_SHA" --current-ref "$(git rev-parse HEAD)" --json

This audit distinguishes unchanged source bytes, changed evidence sources,
missing/unsafe sources, and unassessed fingerprints. A change is a reason to
inspect the evidence, **not automatic revocation of its original authority**.
The command does not update SQLite or mutate the checkout.

## Construction: active-workspace recall (no clean-room development gate)

Build an index once at a normal clean committed HEAD, outside the checkout,
or from a dirty checkout with `knowledge-build --temporary-checkout`.
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
  cites is a coverage gap, not evidence of no semantic effect.
  `uncited_changed_paths` lists those changed paths that no **reviewed**
  record cites (a mechanical path/containment record does not count), sorted
  and bounded by `--limit`; `uncited_changed_path_total` is the pre-limit
  count, and top-level `truncated` is true when either the affected-record or
  the uncited-path list omits entries. Use
  `knowledge-audit` for byte-level drift once the checkout is clean, or with
  `--temporary-checkout` while it is dirty.
- For source truth, inspect affected current code, owner documentation,
  tests and architectural alternatives. To retain a reusable decision in
  dirty work, preflight JSON with `knowledge-proposal-check`, run local tests
  and commit normally. Rebuild the derived index at the new clean commit.

**Construction claim ceiling:** same-session tests and dogfooding confirm
implementation behavior at the tested revision; they do not establish
independent-session cumulative value, cross-repository transfer, release
readiness, or a benchmark advantage.

## Zero-setup workspace query (workspace-query)

`semantic workspace-query` answers a reviewed-knowledge query without a prior
build and without identity arguments. It resolves the checkout, the commit
(`--ref`, default `HEAD`) and a repository label, builds or reuses a derived
SQLite index of that committed revision, runs one read operation and returns
the same payload as `knowledge-query --repo .` plus one additive
`workspace_index` object.

Two main uses:

- Before editing a file: `semantic workspace-query path/to/file.py --json`
  (`context-for`; up to 8 positional paths are composed as in `context-for --path`).
- Before finishing: `semantic workspace-query --operation workspace-impact --ref <base> --json`
  lists reviewed records whose cited files changed since `<base>`.

Facts that bound its use:

- Only committed bytes are indexed. A dirty checkout is indexed from a
  temporary worktree. `workspace_context` discloses uncommitted changes that
  are not indexed; the working overlay is never indexed and never authority.
- The derived index lives at `<index-dir>/<clone-key>/<sha>.sqlite`. The default
  index directory is `%LOCALAPPDATA%\sensemaking-skills\index` on Windows and
  `$XDG_CACHE_HOME/sensemaking-skills/index` (else `~/.cache/sensemaking-skills/index`)
  elsewhere. The clone key hashes the Git common directory, so all worktrees of one
  clone share one cache. The index is rebuildable, is never authority, and at most
  8 snapshot files are kept per clone (older ones are pruned after a build).
- `workspace_index` fields: `indexed_ref`, `ref_requested`, `repository`,
  `repository_identity_source` (`explicit`, `origin_remote` or `local_path`),
  `repository_label_verified` (always `false`), `index_path`, `index_state`
  (`built` or `reused`), `build_source` (`active_checkout`, `temporary_worktree`,
  or `null` when reused) and `equivalent_operations` (the build plus the operation
  when built; the operation alone when reused).
- The label comes from the `origin` remote path (last two segments, `.git`
  removed) or, without an origin, from the checkout directory name. The origin
  URL, its credentials and its host are never printed. An origin whose kept path
  segments contain `@` or `:` is not used; the directory name is used instead. The
  label is not a verified identity; `--repository` sets it explicitly.
- Supported operations: `context-for`, `rules-for`, `search`, `explain`, `why`,
  `impact`, `term`, `orientation-summary`, `contradictions`, `snapshot` and
  `workspace-impact`. `changes` and `history` are refused, because they need
  several indexed revisions in one database; use `knowledge-build` and
  `knowledge-query` with an explicit `--db` for those.
- Options: `--ref REV` (rejected when it starts with `-` or contains whitespace or
  control characters), `--repository LABEL`, `--index-dir DIR` (must lie outside
  the checkout), `--refresh` (delete this commit's cache file and rebuild it) and
  `--repo DIR` (any directory inside the working tree).
- Cost: the first call for a commit builds the index; a dirty tree uses the
  temporary-worktree path, which takes on the order of 15 seconds on the development
  host. A reused index answers in about 2 seconds. Timing is not a benchmark.
- Cache trust: a reused cache file is trusted as written and is not re-verified
  against Git. Anyone who can write to the index directory can alter answers, so keep
  the default per-user location or a private directory, and use `--refresh` when in doubt.
- Claim ceiling: this is construction evidence that the command exists and returns
  source-pinned answers. Whether agents consult reviewed records earlier because of
  it is NOT TESTED.

## Change granularity and shared authored-pack limitation

Source change and semantic change are different questions:

- **Source-byte drift:** a cited file's bytes differ from a previously indexed committed revision. `knowledge-audit` reports this faithfully but cannot decide whether an authored architectural claim remains applicable.
- **Authored-record content change:** the specific claim's or relation's authored fields have changed; this is not the same as a changed fingerprint of the JSON file containing it.
- **Cited evidence change:** an implementation, test or decision source referenced by the record has changed, with no automatic conclusion about the record's validity.
- **Semantic reinterpretation:** a source-checking agent establishes a consequential change in meaning, rationale, decision status or applicability; neither a hash nor an unchanged file proves this.

**Shared authored-pack source granularity:** `_authored_records()` fingerprints
the entire `.sensemaking/knowledge/*.json` container for every record it holds.
Editing one record still causes the conservative `knowledge-audit` source-byte
result to report drift across the pack. Likewise, `changes` still reports raw
indexed payload differences, including generated fingerprints. Neither signal
alone establishes individual authored changes or semantic invalidity.

**Construction addition (PATH-1/T11):** `knowledge-audit` now returns an
additive `authored_record_audit` for indexed authored claims and relations
whose original JSON container changed or became unavailable at the specified
clean current revision. The current pack is read only through the existing
tracked-source safety checks and each old ID is normalized through the same
authored-record parser. The output distinguishes:

- `authored_fields_changed`: the corresponding record's normalized authored
  fields at the **same previous pack path** differ.
- `authored_fields_unchanged`: the same record's authored fields are unchanged,
  even though its container bytes changed; this is **not** semantic validity.
- `record_absent_from_original_pack`: the old ID is no longer in that file.
  It may have moved; this is **not** proof of deletion from the repository.
- `not_assessed`: current pack or record could not be parsed/compared safely.

`authored_record_audit.records` and original `affected_records` retain the
existing `--limit`; counts are computed before truncation. Per-record rows also
report **other changed/missing supporting source paths** so an unchanged authored
record never clears a changed implementation or governing decision. The original
`source_status_counts` and conservative source-byte audit remain unchanged.
A current snapshot does **not** have to be independently indexed for this
record-level comparison, but must be the exact clean Git HEAD. Inspect
original sources and semantics before RECONCILE. `changes.change_classification`
continues to distinguish the two-index indexed-payload case described below.

### Additive indexed change classification (integrated, PR #561)

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
follow-up. PR #561 (merged as `db6b546f`) implements the per-record
classification for `changes` that this episode called for, without narrowing
source-byte audit, erasing original raw deltas, suppressing real source
changes or establishing semantic truth. The whole-pack fingerprint fanout is
**not** eliminated: `knowledge-audit` remains intentionally conservative and
raw `changed` IDs retain their earlier full-payload semantics.

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

A query may examine the current **dirty active checkout** with `knowledge-query --repo .`, which adds `workspace_context` including current HEAD, indexed revision, modified/untracked counts and a clear flag that uncommitted edits were **not indexed**. This never relaxes the clean HEAD requirement for `knowledge-build` and `knowledge-audit`; `knowledge-build --temporary-checkout` satisfies it in a separate temporary worktree instead.

The SQLite index retains multiple repository/SHA snapshots. Indexing identical inputs is idempotent, and conflicting data under the same source revision is rejected. Authored semantic conclusions remain Git-reviewed; do not commit or manually mutate the generated SQLite file.

- History reports **database indexing order**, not Git ancestry or causal chronology. The merged Episode A fix adds `history_total_entries` and marks `truncated` when the limit omits entries.
- Changes reports set differences, not proved semantic consequences. The merged Episode A fix adds `delta_total_counts` and marks `truncated` if any of the six delta arrays is shortened.
- Impact follows explicit edges only; an indexed path is not a transitive or causal proof. The merged Episode A repair bounds `depth` to one explicit edge per hop in either direction.
- Contradictions reports explicit conflicts only; missing conflicts means NOT ASSESSED.
- Query results carry currentness/revision, source/evidence provenance, limits and no-authority flags.

## Task-specific architectural context (`context-for`)

`knowledge-query --operation context-for` returns the reviewed architecture that
bears on one repository file, as one bounded, read-only result:

```bash
sensemaking-skills semantic knowledge-query --db "$db" --repository "$repository" \
  --target-ref "$sha" --operation context-for \
  --subject src/sensemaking_skills/skills/workflow_planner.py --repo . --limit 25 --json
```

- `context.ownership`: owners declared by `owned_paths`, with `coverage_status`
  (`COVERED` or `NOT_ASSESSED`), `ambiguous` when several owners declare the
  path, and the layers and bounded contexts they belong to.
- `context.architecture_rules`: rules matched by a path scope or a declared
  graph link, computed exactly as `rules-for` computes them.
- `context.contracts`: contracts linked by `exposes`, or by `flows_to` through
  its `carries` attribute.
- `context.constraints`: invariant or constraint records linked by
  `constrained_by` from an owning component or applicable rule. One second hop
  follows `constrained_by` from a linked decision and is labelled as such. An
  empty result means NOT ASSESSED, not that no constraint applies.
- `context.decisions`: decisions linked by `decided_by`.
- `context.alternatives`: source-linked alternatives explicitly attached to
  those decisions by `references` or `contradicts` (either direction). The
  second hop is clearly labelled. A linked alternative is **not** automatically
  rejected, endorsed or made executable; inspect the decision and source text.
  Empty results mean NOT ASSESSED, not that no competing designs existed.
- `context.history`: incidents, lessons and observations linked by `references`,
  `contradicts` or `learned_from`. One second hop follows `derived_from` from a
  linked decision to a recorded incident, lesson or observation, and is labelled as
  such.
- `context.verification_refs`: verification records linked by `tested_by` from
  an owner or a matched rule. For a file that **no component owns**, a
  verification record whose `authority_ref` is that file, or whose `evidence_refs`
  cite `file:<path>`, is also returned. Its `matched_by` names the link
  (`authority_ref` or `evidence_ref`). This is verification relevance, never
  ownership: other claim kinds that merely cite the file do not qualify.
- `context.verified_components`: components that a file-level verification record
  in this response verifies, linked by `tested_by`. The supporting record must be
  in `verification_refs`, so a component supported only by an omitted record is
  not returned. `verification_refs` keeps the first `limit` records in claim-ID
  order across file matches and rule-linked records, so a rule-linked record can
  take a slot, hiding a file match and the component that match supports. Their
  `decided_by` decisions, constraints and history follow the
  usual explicit links. They are not owners: `ownership` stays `NOT_ASSESSED`,
  contracts and rules do not follow from them, and their other verification
  records are not expanded. Relevance is not runtime truth or action authority.
  Owned paths do not use this route.
- `context.knowledge_gaps`: `NOT_ASSESSED`, `AMBIGUOUS`, `EPISTEMIC_CAVEAT`,
  `HYPOTHETICAL_CAVEAT`, `TRUNCATED` and `NOT_AN_OWNER` entries. `NOT_AN_OWNER`
  (category `verification_relevance`) marks a file that no component owns, with
  its verification links recorded as relevance only. A `TRUNCATED` entry on
  `verified_components` marks verified components that were not returned. An
  empty category is reported as not assessed, never as the absence of a contract,
  decision, lesson or test.
- `context.omitted`: how many records each category held beyond `--limit`. For
  `verified_components` it counts every verified component not returned, including
  components supported only by an omitted verification record.
- `context.envelope_reference_coverage`: a **separate** count of claims and
  relations selected by the category context but not returned in the top-level
  query envelope, which is capped globally by `--limit`. The omitted-ID samples
  are bounded to 25 entries per type and are for targeted source inspection,
  not a substitute for the missing full records. An `envelope / TRUNCATED` gap
  explicitly flags that some category entries may reference omitted records.

The top-level relation candidates are limited to links for **visible** context
category items and visible owner/rule/layer relationships. A relation used only
for a category entry omitted by its own `--limit` is not returned as unrelated
evidence in the top-level envelope. Category omission counts and global
`envelope_reference_coverage` limits still apply; omitted links are NOT ASSESSED
by this bounded response, not disproven.

For `context-for` the top-level claim envelope prioritizes reviewed **owners
and applicable rules** before secondary linked context; it remains globally
limited. A `truncated: false` category does not imply the global envelope
contained all referenced claim/relationship records. Raise the limit or inspect
original cited sources when the omitted reference affects the decision.

Each contract, decision, linked alternative, history, verification and rule
item keeps its
`epistemic_status`, `authority_kind`, `authority_ref`, evidence references and
`matched_by`, which names the relation or scope that selected it. Owners and
layers are returned as claim IDs. Superseded, contested and invalidated records
keep that status and add an `EPISTEMIC_CAVEAT` gap. Hypothetical contextual
records add a distinct, non-blocking `HYPOTHETICAL_CAVEAT`; neither is
automatically treated as a current architectural obligation. When ownership
is ambiguous, the note reports how many owners were omitted by the limit.

The subject must have syntactically valid repository-relative path form intended
for a source file. Globs, absolute paths, `..` traversal, backslashes and trailing
slashes are rejected; the query does not inspect the filesystem to establish file
existence or distinguish a directory without a trailing slash from a file.
No heuristic links a file to an owner, rule, decision or test from its name or
its neighbours. The result states
`semantic_truth_established: false` and `action_authorized: false`. With
`--repo`, `workspace_context` reports whether the checkout matches the indexed
revision and whether it has uncommitted changes.

### Relevance candidates (not established context)

Each category above is filled only through the explicit links described for it.
An indexed record can bear on a file without such a link: it may be attached to
a capability the owner implements, or it may cite the file as evidence.
`context.relevance_candidates` lists those records separately, so they are
visible without being presented as context that applies:

- **Capability route:** a `capability` linked to an owning component by
  `implemented_by`, then that capability's `constrained_by` invariants and
  constraints, `decided_by` decisions (either direction), `tested_by`
  verification records, and incidents, lessons and observations linked by
  `references`, `learned_from` or `contradicts`.
- **Citation route:** a contract, invariant, constraint, decision,
  alternative, incident, lesson, observation or verification claim whose
  `evidence_refs` cite `file:<path>` or whose `authority_ref` is the path.
  This route also serves a file that no component owns, such as a test. There,
  verification claims that name the file are returned in `verification_refs`
  by the verification-relevance route, so only citing records of other kinds
  are listed here.

Both routes read fields of indexed records only: authored records, and the
index's own ADR and Grounding Pack claims, which cite their source document. No
name, directory or import heuristic is used, and mechanical claims and relations
never qualify. Records already held by a category above are excluded, including
records that category cut at its limit.

- `status` is `CANDIDATES_NOT_ESTABLISHED` or `NONE_RECORDED`. The second is not
  evidence that nothing else applies.
- `items` are sorted by category and claim ID and cut at `--limit`. Each has
  the usual claim fields, the `category` it would belong to, its `routes`,
  `matched_by` naming the exact relation IDs or cited field, and
  `applicability: NOT_ESTABLISHED`.
- `total`, `omitted` and `by_category` count all candidates before the limit;
  `returned_by_category` counts the returned items.
- `implemented_capabilities` names each capability an owner implements, its
  `epistemic_status`, the `implemented_by` relation IDs, and
  `implementing_component_total`. A capability that several components implement
  can hold a constraint that binds only one of them. The list is cut at
  `--limit`; `implemented_capabilities_omitted` counts the rest, and cutting it
  sets `truncated` even when no candidate was cut.
- `other_citing_kinds` counts citing records of other kinds, for example a
  component that cites the file without owning it. They are not expanded.
- `route_relation_ids` and `route_capability_ids` are the relations and
  capabilities behind the returned capability-route items.

A candidate is never an owner, a rule or an obligation. `ownership` and every
category keep their own status: a category that is `NOT_ASSESSED` stays
`NOT_ASSESSED`, and its note gains a count when candidates of that kind exist.
In addition to the `knowledge_gaps` statuses listed above, the
`relevance_candidates / CANDIDATES_NOT_ESTABLISHED` gap states how many exist
and how many were returned, and `relevance_candidates / TRUNCATED` with
`omitted.relevance_candidates` states what the limit cut. In the top-level
envelope, candidate claims, their capabilities and their route relations come
after every record of the categories, so the global limit cuts them first.
Citations made only by relation records are not searched. To make a candidate
count as context, anchor it to the owner through reviewed knowledge
(RECONCILE); this query does not.

`owner_verification / NOT_ASSESSED` is a separate gap. It appears when every
returned verification record is linked from an applicable rule and none from an
owning component. A rule's own guard test fills `verification_refs` for every
file the rule applies to, which would otherwise hide that the owner's tests are
not linked. One verification link from the owner removes the gap for all of the
owner's files, because ownership is recorded per component.

### Source overlap during active edits (PATH-1/T5)

When `context-for` is called with `--repo` and the indexed commit is available
in the local Git checkout, `context.workspace_relevance` compares changed
tracked/untracked paths since that exact indexed SHA against the original
source-fingerprint paths of the *selected* context claims and relations. It
reports `target_path_changed`, the count of changed paths, affected record IDs,
the cited sources that changed, omitted affected-record totals, and the number
of records for which there was no fingerprint to assess. Returned relevance
candidates, their capabilities and their route relations get the same
comparison in a separate `workspace_relevance.relevance_candidates` block with
its own totals and limit, so they never displace a record of the categories.
Querying an older indexed revision from a newer checkout therefore shows which
candidates cite sources that changed since that revision.

This is a bounded **re-inspection signal**, not an audit of changed bytes and
not proof that any claim is stale or accurate. Authored shared-pack fingerprints
can make multiple records appear affected by one JSON-file change; outside
sources and uncited effects remain NOT ASSESSED. A truncated context cannot
establish full impact coverage. The active workspace is never indexed by the
query. If the indexed SHA cannot be inspected in the local worktree, the
historical context is still returned with `workspace_relevance.assessment:
NOT_ASSESSED`, not an invented clean result. Without `--repo`, no worktree
relevance assessment is made.

For complete changed-path coverage across *all* reviewed records, continue to
use the separate `--operation workspace-impact --repo .` query.

### Multi-file context for one engineering task (PATH-1/T7)

When a genuine task touches several related source paths, repeat `--path` with
**2 through 8 distinct repository-relative paths** instead of using the
single-file `--subject`. This is one bounded request, not a new operation
or a new graph-inference method:

```bash
sensemaking-skills semantic knowledge-query --db "$db" --repository "$repository" \
  --target-ref "$sha" --operation context-for \
  --path src/sensemaking_skills/semantic_cli.py \
  --path src/sensemaking_skills/semantic_architecture/knowledge_store.py \
  --repo . --limit 25 --json
```

- `contexts` contains the **existing single-file context** for each path,
  including its own ownership, rules, decisions, unresolved gaps, and optional
  workspace relevance. A path without a declared owner stays `NOT_ASSESSED`
  even if another path has a known owner.
- Top-level `claims` and `relations` contain the **deduplicated records
  actually returned** by those bounded queries. The per-path `claim_ids` and
  `relation_ids` preserve the selection provenance; `shared_claim_ids`
  identifies repeated claim records without inventing dependencies between files.
- `multi_file_context.per_path_limit` and `truncated_paths` disclose limits.
  The global union may contain up to `8 * --limit` records of each type;
  a non-truncated result still does not prove that the task's architecture
  is semantically complete.
- `--path` is mutually exclusive with `--subject`, cannot be used with any
  other operation, and rejects duplicates. The existing single-file query and
  its JSON response remain unchanged. Worktree changes remain **unindexed**.

A semantic query receipt records **one `context-for` entry per requested
path** with the corresponding returned IDs and caveats; batch convenience
does not change the receipt schema or turn per-path coverage into global
`HIT` evidence.

### Opt-in Campaign working context (PATH-1/T17)

`campaign working-context` can attach `context-for` results for one to eight
distinct files to an active Campaign's working context. Without the knowledge
options the output is unchanged. The four knowledge identity/index options are
all-or-nothing:

```bash
sensemaking-skills campaign working-context --workspace "$CAMPAIGN" --json \
  --knowledge-db "$db" \
  --knowledge-repository ThorStarlord/sensemaking-skills \
  --knowledge-ref "$SHA" \
  --knowledge-repo "$CHECKOUT" \
  --knowledge-path src/sensemaking_skills/campaigns/execution.py \
  --knowledge-path src/sensemaking_skills/campaign_execution_cli.py
```

- `--knowledge-ref` must be the exact 40-character revision the index was built from.
- `--knowledge-repo` is the active checkout. Its repository identity is derived the same
  way target snapshots derive theirs and must match the bound Campaign target.
  `--knowledge-repository` is a caller-declared label; the command does not verify it.
- `--target-alias` selects the target when several are bound. It is valid only with the
  knowledge options.

When requested, the payload gains `reviewed_knowledge`:

- `source_identity`: repository label, indexed ref, identity source, observed checkout
  HEAD, whether that HEAD matches the indexed ref, and worktree cleanliness.
- `target_binding`: target alias, `repository_id_match` (always `MATCH` on success; a
  mismatch is an error), and `source_commit_match` against the target head (`MATCH`,
  `MISMATCH` or `NOT_ASSESSED`).
- `applicability`: `HISTORICAL` when the indexed ref differs from the target head or the
  checkout HEAD; `ALIGNED_TO_INDEXED_REVISION` when both match; `NOT_ASSESSED` when the
  target records no head.
- `query`: for one file, the unmodified `context-for` envelope. For two to eight files, the
  unmodified multi-file envelope: `contexts` with one entry per file, deduplicated `claims`
  and `relations`, and `multi_file_context` (shared record IDs, truncated paths, and
  `coverage_complete: false`). Each file keeps its own owners, rules, contracts, decisions,
  history, verification references, gaps, omitted counts and truncation.
- `caveats`: codes such as `HISTORICAL_TARGET_HEAD`, `HISTORICAL_CHECKOUT_HEAD`,
  `UNINDEXED_WORKTREE_CHANGES`, `TARGET_SNAPSHOT_DIRTY`,
  `WORKSPACE_RELEVANCE_NOT_ASSESSED`, `COVERAGE_NOT_ASSESSED`, `OWNERSHIP_AMBIGUOUS`,
  `EPISTEMIC_CAVEAT`, `TRUNCATED`, `MULTI_FILE_NOT_COMPLETE` (two to eight files; no
  dependency is implied between them) and `INSPECT_ORIGINAL_SOURCE`. In multi-file mode,
  per-file caveats carry a `path` field.
- `semantic_truth_established` and `action_authorized`, both `false`.

Failures are explicit and never fall back to the unaugmented view. Partial options,
`--target-alias` without knowledge options, more than eight paths, or duplicate paths exit 2.
A Campaign with
no bound target, an identity mismatch, an unindexed revision, an invalid path, or a
checkout that is not a Git worktree exit 4 with `CAMPAIGN_WORKSPACE_ERROR`. A Campaign whose
own target snapshot has drifted fails with its existing integrity error (exit 3) before any
knowledge is attached.

Retrieved records describe the indexed revision. They do not select a responsibility or the
next action, grant merge, release or deploy authority, or establish semantic truth. Read the
original source before relying on them.

### Agent journey with the optional Campaign view (PATH-1/T19)

The intended sequence is: read the Campaign responsibility, request the context of
the files that the responsibility will change, inspect the original authority and
source those records cite, build ordinary code, and reconcile only consequential
knowledge. The sequence adds no Skill, planner or mandatory onboarding step.

- If no suitable index exists, read the Git-authored knowledge and the cited source
  directly and do the engineering. Do not wait for an index bootstrap.
- The Campaign resume profile reports durable Campaign state. It is not an answer
  from the repository knowledge index, and the attached view does not change it.
- For a clear bounded task with no continuation need, skip Campaign entirely.
- Attaching the view does not establish S5 longitudinal reuse or S6 transfer; those
  claims need separate qualification.

## Skill usage

1. Find a relevant claim or decision with search/why/explain.
2. Inspect cited original owner, product, ADR, code and test evidence at its source revision.
3. Use only source-checked relationships to inform architectural alternatives and change-impact analysis.
4. If an edge is stale, missing or contested, state the uncertainty; do not fill it with an invented dependency.
5. On consequential engineering work, update accepted Git semantic records and the relevant source docs, then rebuild the index at the new revision.

No mandatory indexing stage is required for routine local coding. The index is a product capability for recurring long-horizon understanding, not a second source of truth or automatic authorization plane.

## Optional source-pinned graph view export (2026-11-05)

The existing `knowledge-query` operations remain authoritative *retrieval contracts*, not semantic truth engines. For an explicitly selected and source-checked inquiry, `knowledge-view-export` projects an **existing exact-revision** `explain` (depth 1) or `impact` neighborhood (depth 2–4) as a bounded JSON view or a self-contained offline HTML page. `knowledge-view-render` displays an explicitly source-attributed view JSON without indexing it as factual graph knowledge. Both exports are read-only, create-only and never permitted to write into `.sensemaking/knowledge/`.

The [Agent-Native Graph Viewer guide](agent-native-graph-viewer-v1.md) gives complete CLI examples, source-only demonstration, view provenance, omissions, security, browser scenario/copy-back behavior, and installation caveats. The [premise-reconsideration contract](premise-sensitive-reconsideration-contract-v1.md) records the `NO_NEW_SCHEMA` / `NO_NEW_PREMISE_QUERY` gate: a plain `references` edge is navigation, not proven premise necessity, and historical `PATH-1` identifiers are scoped to their dated strategic artifact. A hypothetical local scenario **cannot** change indexed truth or authorize agent work. The coding agent remains primary; no browser or graph index is required for ordinary source-grounded reasoning.

## Qualification boundaries

Machine tests can establish schema integrity, deterministic reconstruction, exact source revision binding and query behavior. The subsequent [query-integrity Episode A](../normal-use/semantic-stewardship-episode-a-2026-10-15.md) records an actual bounded development responsibility and a Git-authored lesson; it is NOT an independent-agent longitudinal success. The real-repository exact-head worktree smoke test establishes only source reconstruction and retrieval, NOT a fresh independent model's reuse of prior lessons. Genuine longitudinal compounding and incremental architectural benefit remain future evidence questions under ADR 0031.

S6 richness (other language adapters, domain-specific graph types, optional visualization or cross-repository fusion) should be driven by real consumers rather than auto-generating a complete ontology from arbitrary code.


## First-visit repository orientation and bounded structural skeleton

Use `knowledge-orient` to inspect a clean Git checkout without creating
an index or reading unreviewed product semantics. With `--temporary-checkout`,
it orients a dirty checkout at its committed HEAD:

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
