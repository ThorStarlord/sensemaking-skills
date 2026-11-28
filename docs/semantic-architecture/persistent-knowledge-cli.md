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
- Optionally bounded literal static ES module imports/re-exports in tracked
  `.js`, `.mjs`, `.jsx`, `.ts` and `.tsx` files through
  `knowledge-build --include-js-module-imports --max-js-imports N`.
  The projection stores source-linked `references` edges to *literal specifiers*,
  not resolved files, installed packages or runtime dependencies.
  A JS/TS module-specifier claim is identified by its **importing source file and
  literal string**, not by the string alone: two `./model.mjs` imports in
  different directories are separate source-grounded claims. Their labels can
  be identical because no relative path or package is resolved. This keeps
  each claim's single source citation and fingerprint truthful.
- Optionally bounded, source-pinned **manifest dependency declarations** from the existing
  `probe_manifest_dependencies` parser (`pyproject.toml`, `package.json`,
  `requirements.txt` supported fields). These are declarations only, not
  resolved/installed/imported runtime dependencies.

It does not infer owner intent from code, infer semantic dependencies from word matches, inspect all TypeScript relationships, fetch external services, or treat absent relations as proof of absence. Empty/sparse output means NOT ASSESSED.

**JS/TS source scope:** The opt-in bounded scanner retains syntactically clear
ES module import and re-export string specifiers, including multiline static
imports. It excludes CommonJS `require()`, dynamic `import()`, `.cjs` files,
imports embedded in template literals, module-alias resolution and bundler or
runtime semantics. Comments and template bodies are masked; source statements
that cannot be conservatively recognized and files above 512 KiB are reported
as partial coverage, never as no dependency. Records retain original file-line
references and source SHA256; full parser equivalence is NOT claimed. This is
an **additional source observation**, not a reviewed architectural decision.

For ordinary source exploration, the zero-setup `workspace-query` can now
construct, reuse and query this opt-in projection without an explicit
`knowledge-build`, database path or preexisting index:

```bash
sensemaking-skills semantic workspace-query --repo . --ref HEAD \
  --operation search --subject "./views/AppView.js" \
  --include-js-module-imports --max-js-imports 1000 --json
```

The opted-in workspace cache lives in a separate `js-module-imports-v1-max-N`
profile underneath the configured `--index-dir` (or ordinary per-user cache).
Its exact-revision files and retention are separate from the default cache,
and distinct `--max-js-imports` limits never silently reuse another profile.
Unflagged `workspace-query` calls retain their original snapshot, outputs
and cost. `--refresh` only rebuilds the selected profile. The opted-in result
identifies its profile and observation limit in `workspace_index`, and its
`source_scope` / `explicit_limits` continue to disclose partial JS coverage.
The source observations remain literal syntax, **not** resolved dependencies,
system architecture or proof of utility for an independent coding agent.

For explicit-index use or combined source-probe configuration, build an opt-in
index outside the checkout (use a **fresh DB path** if the same Git revision was
previously indexed with a different set of probe flags):

```bash
sensemaking-skills semantic knowledge-build --repo . \
  --repository "owner/repository" --target-ref "$REF" \
  --db /tmp/js-module-knowledge.sqlite \
  --include-js-module-imports --max-js-imports 1000 --json
```

## Build and query

From a CLEAN target Git checkout, store the SQLite index outside the checkout.
The command verifies HEAD and refuses tracked or untracked changes itself;
there is no need to run a separate raw `git status` precheck.

**Derived-index integrity:** Every source-pinned query, source audit and indexed
historical comparison rechecks the stored complete-snapshot digest against
actual persisted claim/relation payloads, snapshot scope and limits. Indexed
history rows from other revisions are checked before use, and a repeated
`knowledge-build` may not silently accept changed cached records at the same
repository/revision. An inconsistent SQLite index fails closed: for zero-setup
`workspace-query` or committed review, retry with `--refresh` to rebuild the
derived cache; for an explicit `--db` index, rebuild the affected exact Git
revision into a fresh index. This is a checksum consistency check, **not a
signature or authentication** and not proof that an authored claim is true,
that current Git sources remain unchanged, or that semantic applicability
survives time. The existing SQLite schema and authored knowledge are unchanged.

The source-state checker uses the shared worktree inspector, which disables
configured external Git clean/smudge/process filters and the filesystem
monitor while inspecting source state. It does
not assess nested submodule worktrees (which are outside the indexed
repository's tracked-file source scope).

    cd /path/to/repository
    REF="$(git rev-parse HEAD)"
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
`untracked_count`, `untracked_count_scope`, `working_changes_read` (always
`false`) and `note`, a fixed
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
The import-syntax option is `--include-python-imports` with `--max-imports` cap.
The opt-in Python import syntax projection now attaches the inspected file's
source SHA256 fingerprint to each retained mechanical claim and reference edge.
A module concept shared across files retains its first selected evidence source;
the per-file reference edges preserve their own cited source fingerprints.
These are byte-currentness anchors, not proof of a runtime dependency.

### Opt-in manifest dependency knowledge

The existing manifest dependency probe can now feed the persistent knowledge
index without adding a schema or a language parser. On an exact committed
revision, select `--include-manifest-dependencies` (default off) and
`--max-manifest-dependencies 1000` (0..10000):

```bash
sensemaking-skills semantic knowledge-build --repo . \
  --repository "owner/repository" --target-ref "$REF" \
  --db /outside-checkout/manifest-knowledge.sqlite \
  --include-manifest-dependencies --max-manifest-dependencies 1000 --json

sensemaking-skills semantic knowledge-query \
  --db /outside-checkout/manifest-knowledge.sqlite \
  --repository "owner/repository" --target-ref "$REF" \
  --operation search --term "Declared manifest dependency" --json
```

For each supported declaration, the read-only source projection records a
`domain_concept` claim carrying the declared field and exact dependency
string, plus an observed `references` edge from the tracked manifest's
`source` claim. The claim's identity is scoped to **manifest path + field +
declaration**, preserving dev/optional roles and differing version strings.
Existing source file claim identities are reused; a structural index can be
built with both flags without duplicate source records. Results retain
mechanical authority and original `file:` evidence; statements are not
repository intent or architecture dependencies. The generated manifest source,
declaration and reference records carry the exact cited manifest's SHA256
fingerprint, so a later source audit can distinguish changed or missing bytes
from unchanged bytes rather than automatically returning NOT ASSESSED.

Only supported declaration fields are inspected. `requirements.txt` lines are
not fully resolved, package manifests are not executed, and source imports are
not inferred. Output `source_scope` and `limits` report opt-in scope,
truncation and parse incompleteness. Missing declarations are NOT ASSESSED
outside that scope. Because the index protects the digest at each
repository/revision, use a fresh database for a differently configured snapshot
of a revision that has already been indexed. This option does not affect the
default `workspace-query` cache or any existing index.

To inspect whether the **original source evidence** has drifted since an
indexed revision, while standing in a newer clean target checkout (or, with
`--temporary-checkout`, a dirty one):

    sensemaking-skills semantic knowledge-audit       --db /tmp/semantic-knowledge.sqlite       --repo . --repository "ThorStarlord/sensemaking-skills"       --indexed-ref "$OLD_SHA" --current-ref "$(git rev-parse HEAD)" --json

This audit distinguishes unchanged source bytes, changed evidence sources,
missing/unsafe sources, and unassessed fingerprints. A change is a reason to
inspect the evidence, **not automatic revocation of its original authority**.
New opt-in Python import and manifest dependency snapshots carry inspectable
source fingerprints in their generated claims and relations. Previously indexed
snapshots are **not retroactively backfilled**: missing old fingerprints remain
NOT ASSESSED and should not be claimed as audited evidence. Even with a matching
fingerprint, manifest resolution, import execution and semantic applicability
remain outside the observation.
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
  `untracked_count_scope`, `uncommitted_changes_not_indexed`, and
  `source_alignment_not_semantic_truth`. `untracked_count_scope` is
  `normal_mode_entries`: a wholly untracked directory counts once, and its
  files are not expanded. Expansion can cost tens of seconds on a checkout
  with a large unignored artifact directory; it is not decision-relevant to
  whether uncommitted bytes exist. Path-level untracked names remain in
  `workspace-review-context --include-worktree`, which expands them.
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
  reviewed indexed records cite files I changed?" It compares tracked changed
  file names and Git's untracked entries since `<indexed_ref>` with each
  record's `source_sha256` keys. Entirely untracked directories are not walked
  file by file: Git's normal untracked view represents each as one entry ending
  in `/`. A specific cited source or target path under such an entry is still
  matched exactly. `workspace_impact.change_scope` reports
  `changed_path_granularity` (`all_file_paths` or
  `tracked_files_and_untracked_entries`), `untracked_directory_entry_total`,
  `untracked_directory_files_expanded`, and `untracked_file_total:
  NOT_ASSESSED` when files inside untracked directories were not enumerated.
  A directory entry is not evidence that its contents are irrelevant.
  `workspace_impact.affected_records` separates
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
  `uncited_changed_paths` lists those changed entries that no **reviewed**
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

## Zero-setup first-visit orientation (workspace-orient)

`semantic workspace-orient --json` is the source-path first-visit command.
It resolves the current checkout, committed revision and an **unverified**
repository label without a preceding `git rev-parse`, prebuilt index or
`--temporary-checkout` flag. It uses the same `orient_repository` as
`knowledge-orient`, with the protected exact-source check and automatic
temporary committed checkout on dirty or non-HEAD worktrees. It builds no
SQLite index, interprets no uncommitted bytes and changes no repository
files or Git refs.

The bounded orientation result retains paths, language/manifest/document
examples, source and test examples, truncation and source limitations.
Additive fields identify `source_checkout`, `workspace_context`,
`repository_identity_source`, `repository_label_verified: false`,
`working_changes_read: false` and the orientation code. Submodule worktrees
are not assessed; external Git filters are disabled during source-state
inspection. Neither the path inventory nor a repository label establishes
product architecture, semantic authority or decisions.

Options: `--repo DIR` (default `.`), `--ref REV` (default `HEAD`),
`--repository LABEL`, `--max-files N` (1..20000, default 5000),
`--sample-limit N` (1..50, default 16) and `--json`.
Use the existing `knowledge-orient --db` for optional indexed counts and
`workspace-query` for reviewed claims and relationships.

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
  temporary worktree. Both fast-path selection and exact-HEAD source checks
  reuse filter-safe worktree inspection, without running external Git filter
  commands for status. `workspace_context` discloses uncommitted changes that
  are not indexed; the working overlay is never indexed and never authority.
  Submodule worktree state is not assessed.
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
  `workspace-impact`. `changes` is refused: for a two-revision comparison use
  `semantic workspace-changes --base-ref REV --ref REV` (see below). `history`
  is refused, because it needs several indexed revisions in one database; use
  `knowledge-build` and `knowledge-query` with an explicit `--db` for it.
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

## Zero-setup semantic revision comparison (workspace-changes)

Use `semantic workspace-changes` when an agent needs to know which **reviewed
semantic knowledge records** differ between two committed revisions, without
manually creating a shared multi-revision SQLite database:

```bash
sensemaking-skills semantic workspace-changes --base-ref HEAD~1 --ref HEAD --json
```

The command resolves both refs to exact **local commits**, builds or reuses the
existing per-commit, per-clone cached indexes outside the checkout and reads
them without modifying repository contents or combining mutable index history.
The target defaults to `HEAD`; `--base-ref` is required. Either revision can
be read from a temporary committed worktree when the active checkout is dirty
or points at the other revision. The working overlay is **never** indexed or
used as source truth; `workspace_context` describes its state.

For PR-oriented semantic knowledge deltas, opt in to the same explicit baseline
selection as `workspace-review-context`:

```bash
sensemaking-skills semantic workspace-changes --base-ref BASE_TIP \
  --ref TOPIC_HEAD --pr-merge-base --json
```

This computes the **unique Git merge base** of the supplied commits and
compares that ancestor's reviewed knowledge to the topic head. The direct
two-tree mode remains the default. In PR mode, `workspace_comparison`
preserves the supplied base tip separately from the effective `base_ref`,
labels `comparison_mode: pr_merge_base`, and discloses
`merge_base_calculated: true`. If history is missing, unrelated or
ambiguous, the command rejects the PR mode rather than choosing a baseline.
Fetch sufficient history or use an intentional direct comparison; GitHub PR
identity and its authoritative changed-file list are still not verified.

The result preserves the **existing** `knowledge-query --operation changes`
payload: `claim_delta`, `relation_delta`, `delta_total_counts` and
`change_classification` distinguish raw payload/fingerprint changes from
authored-field and cited-evidence changes, with bounded result counts. Additive
`workspace_comparison`, `workspace_index` and `workspace_base_index`
identify both source revisions, requested refs, cache states and scope.
Default direct mode does **not** establish Git ancestry; PR mode establishes
only the unique shared ancestor, not GitHub PR identity, semantic invalidation,
a historical causal sequence, or better engineering decisions.
For a query of one claim across **multiple** previously indexed revisions,
the original `knowledge-query --operation history` remains available.

Flags: `--base-ref REV` (required), `--ref REV` (default `HEAD`),
`--pr-merge-base` (opt-in PR scope), `--repo DIR`, `--repository LABEL`,
`--index-dir DIR`, `--refresh`, `--limit 1..250` and `--json`. `--refresh` rebuilds both caches.
A reused cache is trusted as written under the same caveat as
`workspace-query`; both commit refs must exist locally. `workspace-query`
continues to refuse `changes` and `history` because its single-query
contract operates on one snapshot.

**Implementation claim ceiling:** this is a source/diff-reviewed construction
capability; decision benefit, independent agent uptake and semantic truth are
not established by its presence. Use it to identify records meriting source
inspection, not to replace that inspection.

## Question-friendly lexical discovery (`--query-text`)

When an agent has a question but not the exact claim ID or literal phrase, the
existing `search` operation offers an **opt-in ranked lexical** mode in both
the zero-setup and explicit-index entrypoints:

```bash
sensemaking-skills semantic workspace-query --operation search \
  --query-text "Which decisions protect repository source knowledge?" --json

sensemaking-skills semantic knowledge-query --operation search \
  --db /tmp/semantic-knowledge.sqlite --repository owner/repository \
  --target-ref <exact-commit-sha> \
  --query-text "Which decisions protect repository source knowledge?" --json
```

This mode tokenizes Unicode letters/numbers (splitting punctuation and
underscores), folds case, removes duplicate tokens and ignores one-character
tokens. Input is bounded to 300 characters and 1..24 distinct words of length
at least two. Common English function words (for example `the`, `and`, `when`,
`before`) are dropped before matching and listed in `ignored_function_words`.
A claim is a candidate when at least one remaining content token is a literal
substring of its statement or of its ID without the claim-kind prefix, provided the
token has five or more letters, or when the token and one of the claim's words
share a simple stem after one common inflection is removed. Shorter tokens match
only as whole words or stems, so `act` does not match `exact`. For example, the
query `subagents` finds a statement that says `subagent`, and `reading` finds `read`.
Results are ordered by number of distinct matching content tokens, then their
combined length, then claim ID. No embedding, language-model call, inferred graph
edge or semantic authority is used.

JSON reports `search_mode: ranked_lexical_tokens_any`,
`search_hit_total`, `query_tokens`, `ignored_function_words` and bounded
`match_details` with each returned claim's literal `matched_tokens`. The normal
`truncated` flag applies when the result exceeds `--limit`; a missing
or weak lexical match is **NOT ASSESSED**, not proof that relevant reviewed
knowledge is absent. A question made only of function words returns no candidates.
Lexical matching is still not semantic, so a broad question may return noisy
candidates. Check exact cited sources before relying on a result.

In search JSON (`workspace-query` and `knowledge-query`, `--operation search`), each
returned claim lists `id` and `statement` first, then its other fields in key order,
so a host that shows only the start of a long result still shows what each claim is
and says. This is presentation only: stored records, snapshot digests, ranking and
parsed values are unchanged. Other operations keep their sorted key order.

Each returned **lesson** claim in search JSON also carries `recall_conditions`:
`scope`, `conditions`, `claim_ceiling`, `counterevidence`, `original_outcome`,
`revisit_when` (or `staleness_condition`) and `decision_link`
(`decision_changed` or `operationalized_by`). Each holds the recorded value or
`NOT_RECORDED`, and `applicability_to_current_question` is always
`NOT_ESTABLISHED`. These are authored claims, not verified current applicability.
`NOT_RECORDED` means the reviewed record states no such condition; it does not
show that none applies. The stored lesson is unchanged, and the search adds
`recall_conditions_limit` whenever a lesson is returned.

Each returned lesson also lists `citing_records`: the reviewed `incident`,
`lesson` and `observation` records at the indexed revision that link to it through
`references`, `learned_from` or `contradicts`. These are typically later
applications, adaptations, narrowings or rejections. Each entry gives the record
`id`, `kind`, `predicate`, the relation `id` and the relation's `relation_scope`
(or `NOT_RECORDED`). Whether a record confirms, adapts, narrows or contests the
lesson is not inferred; read it, for example with `explain`. An empty list does not
show that the lesson was never used. The search adds `citing_records_limit`
whenever a lesson is returned.

`--query-text` works only with `--operation search`, and cannot be combined
with `--subject`, repeated `--term` or multi-file path queries. Existing
literal `--subject` search and explicit OR `--term` search preserve their
original results and ordering; no schema or cache format changes occur.
`workspace-query` continues to index only committed sources and marks working
overlays separately. Ranked lexical matching is **not semantic search** and
does not demonstrate improved agent decision-making.

## Search only reviewed lessons or other claim kinds (`--search-kind`)

When a coding agent needs a historical lesson about a real question, lexical
search may return many unrelated goals, decisions or components. The optional,
repeated `--search-kind` flag limits candidates **before matching, ranking and
bounding** to exact claim kinds supported by the existing authored schema.
This is especially useful for finding source-addressed `lesson` claims without
already knowing a `lesson:` ID:

```bash
sensemaking-skills semantic workspace-query --operation search \
  --search-kind lesson --query-text "query completeness missing evidence" --json

sensemaking-skills semantic knowledge-query --operation search \
  --db /tmp/semantic-knowledge.sqlite --repository owner/repository \
  --target-ref <exact-commit-sha> \
  --search-kind lesson --term "completeness" --json
```

Both existing query entrypoints accept repeated kinds (OR between exact kind
names) with `--subject` literal text, `--term` phrases or `--query-text`
lexical discovery. Search matches are still lexical; no embedding, causal
inference, relevance judgment or owner authority is introduced.
Invalid kinds and use outside `--operation search` are rejected. The optional
`search_kind_filter` field reports the normalized sorted kinds actually
applied; without the filter the prior output contract remains unchanged.
`search_hit_total`, bounded `match_details` and top-level `truncated`
refer to matches **after** the kind filter. A zero-hit filtered search means
**no indexed lexical hit in those kinds**, not that the repository has no
relevant experience. Inspect original source/revision, contextual suitability,
contradictions and negative cases before using a returned lesson.

This is a narrower decision-time discovery aid for [Longitudinal Engineering
Learning](../superpowers/plans/2026-11-02-longitudinal-engineering-learning.md)
and [SCL](../superpowers/specs/2026-11-12-sensemaking-continuous-learning-design.md);
a retrieval improvement does **not** establish independent lesson use or
continuous learning benefit.

The existing [hosted Semantic Context Re-entry consumer](../../.github/workflows/semantic-context-reentry.yml)
now exercises the **real committed knowledge packs** with both
`knowledge-query` and `workspace-query`, restricted and unrestricted
search, repeated kinds, a rejected invalid kind, and exact source identity.
Its passing run qualifies query mechanics at that tested commit only. It
does **not** observe a later agent's predecision encounter or an improved
engineering outcome.

## Product-level goal orientation (`product-outline`)

For an engineering responsibility spanning more than one source file, retrieve
reviewed product intent and the **directly declared and one-hop goal-family**
relationships between its goals, capabilities, opportunities and governing
constraints:

```bash
sensemaking-skills semantic workspace-query --operation product-outline --json

sensemaking-skills semantic knowledge-query --operation product-outline \
  --db /outside-checkout/knowledge.sqlite --repository owner/repository \
  --target-ref <exact-indexed-sha> --json
```

Both entrypoints use the existing exact-commit knowledge index. The
`product_outline` response groups `goal` claims with `serving_records`
reached by explicitly authored `serves_goal` edges and
`governing_constraints` reached by direct `constrained_by` edges to
invariant/constraint claims. It separately lists reviewed `non_goal` claims.
For prospective planning, opt in to explicitly linked **possible futures**:

```bash
sensemaking-skills semantic workspace-query --operation product-outline --include-candidates --json
```

The optional `candidate_opportunities` group contains only direct
`candidate_opportunity_for` links to reviewed `opportunity` claims. It is
separate from `serving_records`, with each candidate's statement, claim
and relation epistemic status, source and bounded omission counts visible.
The grouped candidate also retains `claim_evidence_refs` and
`relation_evidence_refs` separately: these are the authored claim's original
supporting citations and the independent citations for its proposed goal
relationship. Its `source_ref` identifies the authored knowledge-pack
container, **not** necessarily one of those original supporting sources.

Each visible goal also carries `indirect_candidate_opportunities`: opportunities
linked to a specialized goal that explicitly serves this goal, following exactly
one authored `serves_goal` hop (the same one-hop rule used for indirect
implementation routes). A candidate already linked directly is not repeated.
`via_goal_claim_ids` and `via_goal_relations` preserve the authored path;
`family_candidate_total` counts direct plus one-hop candidates. This is not
arbitrary transitive closure, an inferred goal hierarchy, a ranking or a
selection. A missing candidate edge remains `NOT_ASSESSED`.

These fields allow source inspection even when a top-level `claims` or
`relations` envelope is truncated; they neither establish semantic truth
nor prove that the candidate is novel, applicable or valuable. The view does
not imply a selected strategy, implementation readiness, achieved goal or
permission to act. The flag works with both `workspace-query` and
`knowledge-query`, is rejected for other operations, and leaves the default
committed-review outline unchanged.

For a selection that also turns on an intellectual procedure, request the
existing reviewed method context in the same decision-time consumer:

```bash
sensemaking-skills semantic workspace-query --operation product-outline \
  --include-candidates \
  --method-question "Which method should guide this responsibility selection?" --json
```

The optional `method_precedents` section uses the existing reviewed lesson
search and method context. It carries each candidate's authored scope,
conditions, claim ceiling, counterevidence, original outcome, later related
records and `applicability_to_present_task: NOT_ESTABLISHED`. Later related
records include linked later decisions as well as incidents, observations and
lessons; a later decision shows attributed use or reconsideration, not
validation. Each candidate also carries `source_records`: every outgoing
`learned_from` record, whatever its target kind, plus any outgoing `references`
to an observation or prior lesson, with their authored statements, attributes
and relation provenance. A target absent from the indexed revision stays
visible with `NOT_ASSESSED` rather than disappearing by ID prefix. Other
`references` links are not source records. `procedure_change` exposes
`method_before`, `prior_lesson_id` and `method_disposition`.
`related_records_complete` covers both incoming later records and outgoing
source records and is false when the one-hop explain neighborhood is truncated
or any listed record is not indexed. An empty list with the flag true means no
such indexed record at this revision, not that the method was never used. A
method episode written with `semantic method record` may name an authored
`decision` claim at its source revision through `decision_ref`; the producer
then links the episode observation to that decision. Existing
`knowledge-query explain` on the decision and `method context` on the lesson
expose the resulting method-decision chain without a new query surface. The
link is attribution, not causal proof. The section does not rank, select or
establish applicability; a miss is `NOT_ASSESSED`. This composition is
available on `workspace-query` `product-outline` and `possibility-ecology`;
method precedents are read at the outer query's resolved commit rather than
resolving a moving ref again. Use `semantic method context --path` for
source-path-anchored lesson discovery. Add `--include-method-trials` with
`--method-question` (or `semantic method context --include-trials`) to retrieve
a separate `trial_precedents` section. This matches authored trial questions,
procedures, assumptions, expectations and IDs lexically, even without a
lesson link. Each candidate uses the existing exact trial projection; a
truncated or invalid pair is marked NOT_ASSESSED rather than open. Legacy
unanchored pairs remain limited. No trial is promoted to a lesson. The
corpus is bounded at 250 trial decisions and discloses truncation and omitted
matches. `--method-limit` (or method context `--limit`) bounds each candidate
family independently. Without the flag, trial retrieval is not performed.

Each visible goal/non-goal carries its statement, source reference and
authority/epistemic labels. Each linked record carries its actual declared
relation ID and claim kind; an opportunity is **not** a shipped capability.

### Detached methodological experience (`method record --draft-only`)

When an actual method episode warrants retention but review or promotion is
not yet appropriate, use the existing detached proposal lifecycle:

```bash
sensemaking-skills semantic method record --repo . \
  --episode artifacts/history/<episode>.json --draft-only \
  --output .sensemaking/proposals/method-<id>.json --json

sensemaking-skills semantic knowledge-proposal-check --repo . \
  --proposal .sensemaking/proposals/method-<id>.json \
  --destination .sensemaking/knowledge/method-<id>.json --json
```

The producer also accepts a new direct `artifacts/history/*.json` path in
draft-only mode. The originating episode and its evidence must still be
tracked; existing episode, source-revision, identity, disposition and claim
validation rules are unchanged. The draft is not indexed reviewed knowledge
or a pending-work verdict, and the producer never overwrites a prior file.
A `no_change` episode still creates no proposal. Review sources, conditions,
counterevidence and current authority independently of the preflight. Only
when warranted, copy the exact checked bytes into the new authorized
destination, repeat ordinary preflight there, review and integrate through
Git, and build at the exact clean committed revision. No automatic policy
promotion or inference of methodological learning. The ordinary method
record path and method-trial contracts remain unchanged.

### Method trial (`method trial`)

When a method choice has an observable expected result, an optional trial
preserves the predecision commitment and the later result using existing
`decision` and `observation` claims:

```bash
sensemaking-skills semantic method trial open --repo . \
  --episode artifacts/history/<trial>.json \
  --output .sensemaking/knowledge/method-trial-<id>.json --json

sensemaking-skills semantic method trial close --repo . \
  --episode artifacts/history/<trial>-result.json \
  --output .sensemaking/knowledge/method-trial-<id>-result.json --json

sensemaking-skills semantic method trial show --repo . --ref HEAD \
  --trial decision:method-trial-<id> --json
```

The open episode requires a slug, actor, exact source revision, date, method
question, selected method, assumptions, an observable expected result, tracked
evidence and a claim ceiling. It may name a reviewed `prior_lesson_id`; the
producer links the trial decision to that lesson. The decision carries
`trial_status: OPEN`, a SHA-256 `trial_digest` over the predecision content and
`evidence_paths_not_in_source_revision`, which discloses cited paths that did
not yet exist at the declared revision. Commit the decision and episode alone,
before the work; committing them with the implementation only proves that the
decision preceded the result.

The close episode requires the same trial slug, the `decision_commit` that
introduced it (and still contains the same anchored decision), a later
descendant `source_revision`, the observed outcome, a
disposition (`CONFIRMED`, `ADAPTED`, `REJECTED`, `NO_CHANGE` or
`INCONCLUSIVE`), tracked evidence and a claim ceiling. `ADAPTED` also requires
`method_after`. The producer rejects a close at the decision commit, a
non-descendant revision, a decision whose digest does not match, a second
closing observation and an already-used result identifier. It appends a
separate `observation` linked by `closes_trial`; it does not rewrite the
predecision decision. A lesson-informed close also writes
`trial_result_for` to the lesson, so `semantic method context` shows the result
as a later record.

`show` reconstructs the predecision method, assumptions, expected observation,
prior lesson id and later result. It refuses a truncated explain envelope and
ambiguous or mismatched closure. `predecision_commitment_preserved` is true
only when the decision digest matches, the result digest matches and Git
ancestry verifies a later descendant; legacy trials without anchors report
`NOT_ASSESSED` and false. `method_effect_established` remains false. The
disposition is agent-authored and does not prove that the method caused the
outcome. A trial is not a ranking, method selector, mandatory stage or
independent qualification.

### Possibility ecology (`possibility-ecology`)

Goal-level direct candidates remain a flat list. For prospective reasoning
about interacting possible futures, project one goal's or one opportunity's
authored candidate ecology, including exactly one explicit specialized-goal hop:

```bash
sensemaking-skills semantic workspace-query --operation possibility-ecology \
  --subject goal:compounding-product-knowledge --json

sensemaking-skills semantic knowledge-query --operation possibility-ecology \
  --db /outside-checkout/knowledge.sqlite --repository owner/repository \
  --target-ref <exact-indexed-sha> --subject poss:example-opportunity --json
```

The subject must be an indexed `goal` or `opportunity` claim. For a goal, the
response lists its direct `candidate_opportunity_for` opportunities in
`candidates`; for an opportunity it focuses that record. Each candidate carries
its **authored** `dimensions` (alignment, ambition, horizon, realization and
their bases), realization summary, `value_hypothesis`, `revisit_when`, bounded
`disposition_history`, goal links, and up to eight explicit relationships
(`derived_from`, `requires_capability`, `contradicts`, `relates_to`,
`distinct_from`, or conceptual `references`) with direction, other claim,
relation evidence and any authored `conceptual_relation`.

For a goal, the response also carries `descendant_goal_candidates`: candidates
linked to a specialized goal that explicitly serves the focus goal, following
exactly one authored `serves_goal` hop. Direct candidates are not repeated.
Each descendant entry has `candidate_scope: descendant_goal`, `via_goals` with
the authored goal and `serves_goal` relation provenance, and
`intermediate_goal_hops: 1`. `descendant_candidate_total` and
`family_candidate_total` disclose the direct and one-hop family sizes. This is
not arbitrary transitive closure, an inferred hierarchy, a ranking or a
selection.

The response also groups claims that two or more visible direct or descendant
candidates explicitly relate to into `shared_links`, with each candidate's
scope, predicate, direction and relation ID. This is an authored co-reference,
not proof of a shared premise, complement, conflict, dependency, feasibility or
priority; candidates omitted by either limit are not counted.

For an opportunity focus, `required_capability_routes` surfaces the
capabilities the selected possibility explicitly names through
`requires_capability`, together with any explicit `implemented_by` component
route for each capability. Each route keeps the capability and component
statements, authority, source references, authored `claim_ceiling` and
`scope`, both relation IDs and evidence, the component's authored
`owned_paths`, and `implementation_verified: false`.
Up to eight required capabilities and four components per capability are shown;
the corresponding total and omission counts disclose the bound. This is the
construction-bridge view of a selected candidate: it joins the possibility's
declared requirement to the reviewed capability-to-component route without
requiring a separate `product-outline` cross-reference. It does not inspect
code, establish a working consumer, sufficiency, applicability, priority,
readiness or a recommendation; a missing route remains `NOT_ASSESSED`. Goal
focus leaves the section absent.

This is a source-linked projection, not synthesis or selection. It does not
infer shared premises, complements, conflicts, feasibility, priority,
implementation, goal service or a recommendation; hypothetical records remain
hypothetical, and missing dimensions or relations are `NOT_ASSESSED`. One
explicit relationship hop is followed per candidate; use
`knowledge-view-export`/`explain` for deeper traversal. Candidate, relationship
and shared-link omission counts disclose the bound.

### Possibility contrast (`possibility contrast`)

When a consequential choice may be bounded by assumptions, the optional
`semantic possibility contrast` operation projects agent-authored scenarios
over the visible candidate ecology:

```bash
sensemaking-skills semantic possibility contrast --repo . --ref HEAD \
  --subject goal:compounding-product-knowledge \
  --scenarios scenarios.json --json
```

The scenario document carries one or more named scenarios with `held` and
`negated` assumption claim ids:

```json
{
  "scenarios": [
    {"id": "base", "negated": [], "held": []},
    {"id": "no-cross-episode",
     "negated": ["hyp:cross-episode-synthesis-recurs"]}
  ]
}
```

Assumptions are authored `references` relations whose `conceptual_relation` is
`assumes` or `sharesAssumptionWith`. Each scenario marks every visible
candidate `AFFECTED` (it assumes a negated claim), `UNAFFECTED` (it has visible
assumptions, none negated), or `NOT_ASSESSED` (no visible assumption relation).
`held` is used only to report a visible candidate that contradicts a held claim
under `conflicts`; holding an assumption otherwise does not change a
candidate's `AFFECTED`/`UNAFFECTED` classification.
A candidate whose one-hop relationship projection was truncated is marked
`PARTIAL`; use `explain` on that claim before treating an absence as complete.
`coverage.candidate_omitted` and `descendant_candidate_omitted` disclose
candidates cut by the query limit; omitted candidates were not contrasted, so
the candidate set and the scenario result are partial even when every visible
candidate has complete relationship coverage.
`shared_assumptions` groups candidates that share an authored assumption and
reports pairs without a direct relation; those pairs are questions for the
agent, not endorsed combinations.

The operation does not infer assumptions, generate possibilities, rank
scenarios, select a direction or authorize construction. A scenario is a
hypothetical retention or negation, not evidence that an assumption is true or
false. The agent authors scenarios and interprets the result.

### Possibility synthesis producer

After an agent inspects a goal-family ecology and forms a genuinely new
recombination or gap, the optional `semantic possibility record` producer can
materialize its authored synthesis as an unreviewed `opportunity` proposal:

```bash
sensemaking-skills semantic possibility record \
  --repo . --episode path/to/synthesis.json \
  --output .sensemaking/knowledge/possibility-synthesis.json --json
```

The tracked episode must carry `possibility_id`, `actor`, exact
`source_revision`, `origin_date`, title and statement, one to eight existing
`goal:` refs, one to eight existing `poss:` source candidates, optional
`cap:` refs, optional assumption and contradiction refs, the four
ProductPossibility dimensions (`alignment`, `ambition`, `horizon`,
`realization`), a synthesis basis, value hypothesis, revisit condition,
counterevidence, claim ceiling and tracked evidence. The producer validates
every cited claim at the exact source revision and creates:

- a hypothetical `opportunity` claim with `candidate_opportunity_for` links to
  the cited goals;
- `derived_from` links to the source candidates;
- optional `requires_capability`, `assumes` (`references`) and `contradicts`
  links.

For consequential synthesis, an optional `value_prediction` object can
preserve an explicit evaluative frame with the same `value_hypothesis`
statement. It requires exactly these six nonempty text fields:

- `beneficiary`: the agent/person whose outcome matters;
- `criterion`: what would count as valuable in this frame;
- `comparison_baseline`: the credible existing or alternative approach;
- `expected_observation`: an observable effect that would bear on the value claim;
- `would_change_decision_if`: conditions or counterevidence that would prompt revision;
- `cost_and_downside`: relevant costs, risks and tradeoffs.

The producer adds a hypothetical `conseq:<possibility_id>-value` claim
and its explicit `references` relation to the new opportunity in the
same exclusive draft. The prediction's statement is the existing authored
value hypothesis (not generated text); its attributes retain the frame,
assumptions, counterevidence, author, origin and inspected source revision.
The existing [value-feedback view](#product-possibility-value-feedback)
can recover it after ordinary review; absent assessment is NO_ASSESSMENT.
The caller may omit the object; ordinary synthesis output is unchanged.
Detached output is supported by the same `--draft-only` contract.

A frame is a conditional documentary judgment, not a numerical score or
authority. An episode's inspected source revision and origin date do not
prove its authoring time. To make a prospective commitment attributable,
retain the original episode before the relevant outcome, and cite the actual
Git evidence when assessing it later. Neither generating the proposal nor
retrieving it establishes a beneficiary effect or comparative benefit.

A new synthesis must remain `HYPOTHETICAL` or `NOT_ASSESSED`; claiming
implementation requires ordinary reconciliation. The producer does not generate
a candidate, rank possibilities, choose a goal, claim value or authorize work.
The output is an `UNREVIEWED_DRAFT`; ordinary `knowledge-proposal-check` and Git
review remain necessary. After review, existing `product-outline` and
`possibility-ecology` consumers expose the new candidate with its authored
provenance.

### Source-linked capability-to-component routes

The **default** `product-outline` response also groups
`implementation_routes` under each visible goal. Each route joins only the
**explicitly reviewed** path:

```text
goal <- serves_goal - capability - implemented_by -> component
```

A route reports the capability and component statements and their independently
declared source/evidence references, both relation IDs and evidence references,
the component's authority reference and any authored `owned_paths`. This lets
an agent inspect the actual owning code when comparing a goal's intended
capabilities with the implemented consumers. It does **not** follow arbitrary
graph hops, infer capability implementation, check source correctness, prove a
working consumer, or establish that a goal has been achieved.

Per-goal `implementation_route_total` and `implementation_route_omitted`,
plus the top-level `implementation_routes` count and omission count, disclose
bounded reachability. `implementation_link_not_assessed: true` means no direct
reviewed route was found **in the indexed revision**; it must not be reported
as a missing feature or a gap in the real product. Every route states
`implementation_verified: false`. Top-level `claims` and `relations`
remain separately limited; nested routes preserve their own original source
references even when those envelope records are cut.

When a broader goal is served by a more specialized **goal** rather than
directly by a capability, the default response separately exposes
`indirect_implementation_routes` through **exactly one authored goal-to-goal
`serves_goal` link** followed by the same capability-to-component route.
Each item names the intermediate `via_goal_claim_id`, its original evidence,
the intermediate `via_goal_serves_goal_relation_id` and independent link
evidence, along with the complete direct route to the component.

`indirect_implementation_route_total`,
`indirect_implementation_route_omitted` and
`indirect_implementation_link_not_assessed` disclose this second category.
Top-level counts and omissions include it independently. Longer goal chains,
unwritten serving relations and absent component links are **NOT_ASSESSED**;
an indirect path does not certify a capability for the broader goal or infer
transitive implementation. One-hop reachability is deliberately not a generic
graph closure or strategic ranking mechanism.

**Decision-time use:** For an open-ended engineering responsibility, inspect
the governing goal, declared serving capabilities, visible routes and
candidate futures, then verify decisive claims against current code and users.
If a consequential behavior remains unsupported, name that behavior as a
*source-grounded engineering hypothesis*. Compare a credible alternative by
expected product value, omission cost and authority before selecting work.
Retain the intended end-to-end outcome across bounded increments in the
existing PR/continuation records. This query prepares evidence; the active
agent makes the semantic judgment and retains the ability to choose no change.

This is a **read-only projection**, not a planner, a derived ontology, a
dependency inference or an assessment of which goals are achieved. Missing
goals or missing links are `NOT_ASSESSED`; the query cannot discover all
implicit product purposes or establish the applicability of an old decision.
Open original evidence sources and perform warranted engineering comparison
before acting.

`--limit 1..250` bounds each category of goals, non-goals and relationship
rows. `total_counts`, `omitted_counts`, `serving_omitted`,
`constraint_omitted`, optional `candidate_omitted`, `truncated` and
`envelope_reference_coverage`
disclose category and top-level record omissions. The bounded top-level
`claims`/`relations` envelope may omit records referenced in a grouped
entry; their original source and relation identity remain in the grouped
projection. The operation does not accept `--subject` or query-text/term
search options. Empty results are not evidence that the actual product has
no goals or capabilities.

No new reviewed knowledge schema, cache format or authority grant is needed.

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

#### Consequence standing (bounded projection)

`knowledge-audit` also returns an additive `consequence_standing` section over
the same loaded snapshot and the same source-currency result. It joins authored
`conseq:` `hypothesis` claims with authored `observation` assessments that
resolve them through an existing `references` relation, and reports one row per
prediction:

- `standing`: the single assessed status, `NO_ASSESSMENT`, `SUPERSEDED` or
  `MIXED_ASSESSMENTS` when the authored assessments disagree.
- `due_for_recheck` with `recheck_reason`: `NO_ASSESSMENT`,
  `ASSESSMENT_SOURCES_CHANGED` or `PREDICTION_SOURCES_CHANGED`. The reason is
  derived **only** from the audit's existing source-byte currency.
- `source_currency`: `ASSESSED` or `NOT_ASSESSED`; unassessed rows are listed
  under `currency_not_assessed` rather than being reported as due or current.
- bounded `changed_sources` / `missing_sources` with pre-limit totals.

Each record's own authored pack is excluded from its currency comparison: those
bytes are container provenance, not cited evidence. The projection adds no
command or flag, ranks nothing, and establishes no causation, benefit or
failure. `NO_ASSESSMENT` is NOT ASSESSED, not refuted.

Each visible row also carries its authored `source_option`, `analysis_ref`,
`would_change_decision_if`, `decision_changing` and `feedback_outcome`. The
additive `decision_links` section groups visible rows by `source_option` and
carries the option's authored `preference` (status, current scope and bounded
history), each consequence's standing, the decision-changing consequence IDs
and feedback outcomes. `reconsideration` is `AGENT_OWNED`: the link is evidence,
not a verdict, selection or authorization. The link's `reviews` list exposes
authored decision reviews that reference the same option, with `review_total`
and `review_omitted`; reviews are later evidence, not automatic changes to the
option or its preference.

`assessment_statuses` reports only the **active** assessments' statuses.
`assessment_history` reports every linked assessment with its own authored
status, whether it is `active`, and any `superseded_by` replacement. An
assessment is excluded from current standing by a `supersedes` edge whose two
endpoints are assessments of the same `conseq:` prediction, or by an authored
`SUPERSEDED` status for compatibility; its authored status is preserved rather
than rewritten. `MIXED_ASSESSMENTS` therefore means active assessments
genuinely disagree. A supersession cycle is exposed as
`supersession_integrity: CYCLE` and does not erase all standing. A revised
prediction is a new `conseq:` claim with its epistemic status and `supersedes`
relation; the old record remains visible, so inspect that status rather than
treating it as current.

`decision_link_total` counts distinct recorded source-option groups across the
full projection. `decision_link_returned_total` counts groups present in the
bounded view, `decision_link_omitted_total` counts groups with no visible
consequence, and `decision_link_partial_total` counts returned groups with
omitted member consequences. Each link states its `consequence_total`, returned
and omitted member counts, and `complete`; a partial link's consequence IDs,
standings and feedback outcomes describe only its returned members.

Source-byte currency is not experiential currency; a new experience is
represented by a new assessment observation. `context-for` applies the same
same-prediction supersession rule to an anchored assessment, adding `active`
and `superseded_by` to its `consequence_assessment` view.

#### Product possibility value feedback

A product possibility may link a pre-existing or newly authored value
prediction to a later assessment using the existing consequence lifecycle.
The `conseq:` hypothesis carries `attributes.source_possibility` naming one
`poss:` opportunity, with an explicit `references` edge from the hypothesis
to that opportunity. Do not also set `source_option`. Keep the original
prediction source and, if normalized retrospectively, disclose that fact
rather than present the normalized record as a precommitted trial.

Use the existing attributed consequence assessment (`observation` with
`consequence_ref`, `assessment_status`, scope, observed effect, counterevidence,
exact assessed revision and claim ceiling) and reference edge. The same
supersession rules apply. The existing `possibility-ecology` query now adds
`value_feedback` for its visible direct/descendant candidates; it joins up to
eight predictions per possibility, eight assessments per prediction
(active first), and five authored decision reviews per possibility.
Omission counts are explicit. No prediction is NOT_ASSESSED, not negative
evidence. The view does not perform a currency audit or infer realization,
benefit, ranking, applicability or selection. It can be composed with
`--method-question` and `--include-method-trials` at the same source revision.

A tracked review episode for `semantic decision record` may use
`source_possibility` **instead of** `source_option`. The producer requires
the opportunity, each named consequence's explicit source link and any
cited active assessments to resolve at the exact source revision. It
reuses the existing review decision, source evidence, optional method
lesson and proposal preflight. The review is a separate decision record:
it never rewrites the possibility, its realization or disposition history.
Architecture-option episodes and their existing result fields are unchanged.

#### Decision review producer

`semantic decision record` turns an agent-authored review into a new
`decision` claim. The claim references the existing `arch:` option, the
`conseq:` predictions and active assessment observations it reconsidered, and
optionally a `lesson:` method precedent through `learned_from`. It does not
rewrite the option, its preference or any assessment, change standing, commit,
merge or authorize promotion.

The tracked episode carries `review_id`, `actor`, exact `source_revision`,
`source_option`, a disposition (`reaffirm`, `revise`, `reopen`, `investigate`,
`retain_with_limitation`, `reject` or `no_change`), `basis`, `conditions`,
`counterevidence`, `claim_ceiling`, tracked evidence paths, cited consequence
and assessment IDs, and an optional method lesson. The producer reads claims
and relations at the exact `source_revision` and applies the existing
same-prediction supersession rule. It rejects an effectively superseded
assessment even when the assessment retains an older authored status, rejects a
legacy authored `SUPERSEDED` citation, and keeps supersession-cycle members
active as consequence standing does. It also rejects a consequence that does
not belong to the option.

```bash
sensemaking-skills semantic decision record \
  --repo . --episode path/to/review.json \
  --output .sensemaking/knowledge/decision-review.json --json
```

The output is an `UNREVIEWED_DRAFT` with `action_authorized: false`; ordinary
`knowledge-proposal-check` and Git review remain necessary. After review,
`knowledge-audit` shows the record in the link's `reviews` and
`knowledge-query explain` on the option returns the decision claim and its
relations. Review order is deterministic decision-id order, not proven
chronology. A review is attributed evidence, not causal benefit, independent
reuse or promotion authority.

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
  such. Every context item (decisions, alternatives, contracts, constraints, history,
  verification and relevance candidates) whose record states its own limits returns
  them under `recorded_conditions` (any of `scope`, `claim_ceiling`, `known_limits`,
  `exclusion_condition`, `revisit_when`, `staleness_condition`, `decision_changed`,
  `operationalized_by`, `revised`), as written. These are the record's stated conditions, not a determination that they
  apply to the file under review. A **lesson** item in `context.history` also lists
  `citing_records`, in the same shape as lesson search results: the reviewed
  incidents, lessons and observations that link to that lesson, even when they do not
  link to this file. They are pointers to read, not context items, and are not
  added to the top-level claims or relations.
- `context.verification_refs`: verification records linked by `tested_by` from
  an owner or a matched rule. For a file that **no component owns**, a
  verification record whose `authority_ref` is that file, or whose `evidence_refs`
  identify it as `file:<path>` (optionally followed by `:line:<N>` or
  `#<fragment>`), is also returned. Its `matched_by` names the link
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

For a single Python path, the zero-setup consumer can add committed
code-level relationships to the same authored context:

```bash
sensemaking-skills semantic workspace-query --repo . --ref HEAD \
  --operation context-for src/sensemaking_skills/semantic_cli.py \
  --include-source-relationships --json
```

The opt-in `source_relationships` section reads a clean temporary checkout of
the selected revision and adds direct imports, direct importers, test
references, top-level symbols, leading-underscore cross-module imports, parse
failures and a coverage status. Add `--symbol NAME` for one top-level function
or class to receive direct syntactic references, test functions/methods that
mention it, a source-level behavioral surface (signature, decorators,
docstring summary/hash, direct raises/asserts and definition hash), and
guard-derived verification scenario candidates. If the
target cannot be parsed, the authored context and
file-level importer evidence remain available with `PARTIAL` coverage,
`target_parse_error` and `symbol_context: null`; the symbol is not assessed.
Symbol-list truncation also marks the enclosing source relationship and
workspace response as truncated. It is not a
call graph: dynamic imports, runtime dispatch, test coverage and non-Python
references are not assessed. `test_references` is empty when no test directly
imports or mentions the path, not when no test exercises the behavior. The
flag accepts exactly one tracked `.py` path and is available on
`workspace-query`, not on the lower-level `knowledge-query` operation. See
[Change Context v1](../../skills/using-sensemaking/references/change-context-v1.md).

### Change-scoped verification plan

When the question is which existing pytest candidates to inspect or run,
`semantic verification-plan` composes the same evidence into one bounded plan:

```bash
sensemaking-skills semantic verification-plan --repo . --ref HEAD \
  --path src/sensemaking_skills/semantic_architecture/knowledge_sources.py \
  --symbol build_knowledge_snapshot --json
```

- `pytest_candidates` merges test targets derived from
  `context.verification_refs` with `symbol_context.test_candidates`. Each entry
  carries a `pytest_target` (`tests/test_x.py` or
  `tests/test_x.py::test_name`), `scope` (`FILE` or `TEST_FUNCTION`), the
  contributing `sources`, the union of their evidence references and
  `execution_status: NOT_RUN`. Identical targets are merged; counts report how
  many merges occurred.
- `suggested_pytest` gives the deduplicated `test_files`, any `test_functions`
  whose file is not already a file candidate, the subsumed function candidates,
  and a non-executed `argv` (`null` when no target exists). `execution_status`
  is `NOT_RUN`; the invocation is not proof of collection, pass status or
  coverage.
- `scenario_candidates` carries direct guard-derived conditions with
  `pytest_target: null`, `test_mapping: NOT_ASSESSED` and
  `execution_status: NOT_RUN`. No test is generated or mapped to a scenario.
- `workflow_candidates` groups explicit authored `.github/workflows/*.yml`
  or `.yaml` file references by path, retaining their source verification
  records and matching evidence pointers. These are manual inspection
  candidates only: no workflow or job is resolved, dispatched or executed.
  They do not enter pytest targets or establish workflow applicability.
- `unmapped_authored_verification` lists verification records whose references
  did not identify a `tests/*.py` file, including workflow-only records.
  This field remains pytest-specific; a workflow-only record can also
  appear in `workflow_candidates`.
- `gaps` states file-level-only records, unmapped records, absent direct test
  functions, scenarios without executable tests, truncation, `NOT_RUN`
  execution and `NOT_ASSESSED` coverage explicitly.
- `target` pins the committed path, revision, target SHA-256, symbol and
  definition line. `tests_executed`, `test_analysis_established`,
  `test_results_established`, `coverage_established`,
  `semantic_truth_established` and `action_authorized` are all `false`.

Authored verification records can be linked from an owning component or an
applicable rule, not only from this symbol's tests. They remain file-level
unless the record itself names a test node. A candidate target is an invocation
candidate, not proof that pytest collects it, that it exercises the symbol or
that it passes. Helpers, fixtures, parameterization, indirect execution,
runtime relationships, change safety and coverage are not assessed.

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
  a verification claim that identifies the same file in `authority_ref` or
  `evidence_refs` enters `verification_refs` first, not the candidate list;
  an explicit `tested_by` relation is required to reach verified components.
  Other citation-only records remain candidates, never applicable rules or owners.

**File-reference identity contract:** `knowledge_sources._local_evidence_path`
parses supported repository-local evidence references for both retrieval routes:
`file:tests/example.py`, `file:tests/example.py:line:42`, and
`file:tests/example.py#test_case` identify the same tracked source file.
Matching removes only supported line/fragment qualifiers; returned
`evidence_refs` keep their exact authored strings and provenance. The
`authority_ref` file-path route remains exact. Normalized citations do not
establish architectural applicability, runtime correctness or ownership.
Verification relevance applies only to `verification` records on unowned
paths. A component needs a reviewed `tested_by` link to a displayed
verification record and cannot inherit ownership, contracts or rules through
that link. Category-limited verification records stay in that category's
`omitted` totals, not reintroduced as candidates. `NOT_ASSESSED` and
truncation remain explicit.

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
in the local Git checkout, `context.workspace_relevance` compares tracked
changed file names and Git's untracked entries since that exact indexed SHA
against the original source-fingerprint paths of the *selected* context claims
and relations. It reports `target_path_changed`, the count of changed paths,
affected record IDs, the cited sources that changed, omitted affected-record
totals, and the number of records for which there was no fingerprint to
assess. `change_scope` discloses the granularity: a wholly untracked directory
is one entry and its files are not enumerated (`untracked_file_total:
NOT_ASSESSED`), while a specific cited source or the target path under that
entry is still matched exactly. Returned relevance
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

This is a **single-pack draft preflight**, not a prospective commit validator
and not a prediction of `knowledge-build` success. The selected proposal is
read from its current **working-file bytes**, even if differently staged.
Other reviewed knowledge packs are read from **committed HEAD**, so dirty,
untracked or deleted *other* packs do not enter this check. Referenced ordinary
evidence files use current worktree bytes only if Git-index-tracked (including
staged new paths), and must exist safely. The check validates the proposed
records and their outgoing references, checks cross-pack claim/relation ID
collisions, and checks incoming committed relationships affected by changed
or removed claims. It reuses the build-side artifact-contract flow checker
for affected flows; unrelated pack defects remain outside scope.

Success does **not** prove a whole working tree, staging index or hypothetical
commit will build: other dirty packs, deleted or renamed packs, unstaged-vs-staged
content, unrelated cross-pack defects, optional `--include-repository-structure`
and `--include-python-imports` are not simulated. File/directory identity
resolution is only a path preflight, not proof the default or capped structural
build includes a record. Check the JSON `validation_scope`,
`dirty_other_packs_ignored`, `structural_path_endpoints_only` and
`build_equivalence_established: false` fields before relying on a pass.
A removed proposal file cannot be checked by `--proposal`; deletions and
multi-pack edits must be checked by the exact-commit builder after commit.
Neither command establishes semantic truth, current owner authority or
permission to act.
For source-pinned indexing, commit the reviewed source/knowledge changes and rebuild the SQLite snapshot at the exact new SHA in the **same current checkout when naturally clean**. A fresh agent or separate clean-room worktree is not a construction prerequisite.

## Committed-change product and architecture review context

When reviewing an actual committed change, an agent can obtain the baseline
product intent and source-linked context for files changed between two commits
without guessing paths or preparing a knowledge database:

    sensemaking-skills semantic workspace-review-context --base-ref BASE --ref HEAD --json

For a **pull request**, pass the target branch tip as `--base-ref` and opt in
explicitly to the PR's merge-base comparison scope:

    sensemaking-skills semantic workspace-review-context --base-ref MAIN_TIP --ref PR_HEAD --pr-merge-base --json

The default remains an exact two-committed-tree comparison. With
`--pr-merge-base`, Git must identify exactly one common merge base; absent or
ambiguous history fails closed rather than silently choosing a baseline. Fetch
sufficient history in shallow checkouts before invoking it. The result's
`base_ref` and source-pinned context use the effective merge-base commit;
`review_scope.base_tip_ref` preserves the supplied target-branch tip, and
`review_scope.comparison_mode`/`merge_base_calculated` disclose the mode.
This computes a Git comparison scope, **not** the identity of a GitHub PR or
a check against its authoritative file set. A caller reviewing a PR should
still reconcile the returned changed paths with the PR's actual files.

For a focused Python source review, add `--source-path PATH` and optionally
`--source-symbol NAME`. The path must be in the selected review contexts:
increase `--max-paths` or explicitly repeat `--path` as needed. For example:

```bash
sensemaking-skills semantic workspace-review-context --repo . \
  --base-ref BASE --ref HEAD --source-path src/sensemaking_skills/workspace_knowledge.py \
  --source-symbol run_workspace_review_context --json
```

The opt-in `source_relationship_comparison` pairs existing committed Python
source views at the effective BASE and TARGET, with each side's exact ref,
tree-entry status and source evidence. Authored product intent stays BASE-only.
It compares bounded identities of direct-import modules, importer/test files,
top-level symbols (kind:name) and optionally direct symbol reference files
and test candidates (path::test-name). Each identity comparison discloses
`base_only`, `target_only`, `both`, each side's list completeness and
`comparison_status`. When `--source-symbol` is present, the optional
`symbol_behavior_comparison` also pairs source-level signature, decorators,
docstring summary/hash, direct raises/asserts and exact definition source hash,
and reports `changed_fields`, `presence` and `source_changed`. Read
`VISIBLE_ONLY` differences as returned-list differences, not established
additions or removals; even complete identities remain limited to the
syntactic scanner. A shared identity is not proof of unchanged code or
behavior; a behavior-surface difference is not proof of semantic change.
Missing/non-regular tree entries and unavailable
symbol contexts are not compared as empty inventories. Per-side source
truncation propagates to the review packet. The comparison reads committed
bytes only, including when `--include-worktree` is enabled. No new dependency
resolution, runtime call graph, semantic diff or impact verdict is produced.

For **prospective** review, opt in to the already reviewed goal-linked candidate
opportunities without promoting them to existing capabilities or selected work:

```bash
sensemaking-skills semantic workspace-review-context \
  --base-ref MAIN_TIP --ref PR_HEAD --pr-merge-base \
  --include-candidates --json
```

Only in this opt-in mode, `product_outline.goals[].candidate_opportunities`
contains `committed_change_reinspection` for each visible candidate edge,
and `product_outline.candidate_reinspection` accounts for visible, omitted,
matched and unfingerprinted candidates. The comparison matches indexed
**BASE-revision** source fingerprint *paths* to the full committed changed-path
set. `changed_record_containers` separates edited shared knowledge packs from
`changed_supporting_paths`; a shared pack edit can flag many unrelated
possibilities. Missing links, omitted candidate edges and missing fingerprints
remain NOT ASSESSED. The opt-in packet also adds `candidate_reconsiderations`,
which evaluates explicit `file:`, `claim:` and `symbol:` references embedded in
an authored `revisit_when` and reports `FIRED`, `NO_MATCH` or `NOT_ASSESSED`
with evidence. `file:` references match committed (and, with
`--include-worktree`, working-tree) path names. `claim:` references compare the
normalized authored record at BASE and TARGET and check whether its authority or
evidence paths changed. `symbol:` references reuse the existing source-level
behavior surface for one Python definition. Surrounding prose is not
interpreted; conditions without recognized references remain `NOT_ASSESSED`.
A fired reference is a reconsideration prompt, not a staleness verdict,
selection, revival or permission to act. The default review output is
unchanged. These are prompts to reopen original sources and reconsider
**whether** a possibility still matters.

This read-only convenience command resolves both exact local commits, uses Git
diff to list committed changed **path names** (no rename inference), and
retrieves the product outline plus bounded per-file `context-for` results
from the **BASE revision**. The baseline matters for deleted files and prevents
code newly introduced in the target from silently becoming declared intent.
The target revision contributes changed paths, **not** presumed architectural
meaning. Derived BASE SQLite cache resides outside the checkout as in
`workspace-query`; no uncommitted bytes are indexed.

Use `--max-paths` (1..32, default 8), `--limit` (1..100, default 25),
`--depth`, `--repository`, `--index-dir` and `--refresh` when appropriate.
The response reports exact base/target identities, selected and omitted path
counts, invalid/unrepresentable path count, source scope, retrieval omission,
source-linked product goals/non-goals and per-path claims/relations. A path with
no recorded ownership remains NOT_ASSESSED, never "safe". If the diff has more
paths than `--max-paths`, the summary is truncated and omitted paths require
independent inspection. Snapshot truncation is separate from changed-path
truncation; the final flag reports either.

For a known review set, repeat `--path` with 1..32 distinct repository-relative
files. This is an **explicit-scope** mode: Git reads are restricted to those
literal paths, so an unrelated untracked tree is never walked and `--max-paths`
selection does not apply. Every requested path receives BASE context; the
response reports `scope_mode: explicit_paths`, `max_paths_applied: false`,
`requested_paths`, `changed_requested_paths`, `unchanged_requested_paths`,
`not_found_requested_paths`, `ignored_requested_paths`,
`other_changes_assessed: false` and exact counts
for the requested set. A requested path that does not identify a file in the
inspected revisions (and, with `--include-worktree`, the working tree) is
`not_found`, not
`unchanged`. An ignored working-tree path absent from the inspected revisions is
outside the source scope and is reported as ignored, not unchanged. Every
other committed or working change is **NOT_ASSESSED**; the packet is not a
complete PR or worktree review. Cited-source overlap and candidate overlaps
also cover only the requested changed paths.

The `committed_evidence_reinspection` summary reuses the existing
`workspace-impact` fingerprint-overlap calculation, but its source is the
**committed BASE-to-target changed path set**, not a dirty worktree. It covers
**all representable changed paths**, including those omitted from per-file
context by `--max-paths`. The summary reports affected reviewed record IDs,
uncited changed path coverage gaps, mechanical-only overlaps, exact source
revisions and independently capped omission counts. Each selected path's
`context.committed_change_relevance` separately flags whether its BASE
context records and less-certain relevance candidates cite changed sources.

These results are **re-inspection candidates**, not a content comparison,
semantic staleness finding or proof of changed architecture. The original
`workspace-impact` operation continues to describe active worktree overlap.
Committed review passes individual file paths, so its overlap summaries report
`change_scope.changed_path_granularity: all_file_paths`; the same is true for
live worktree review, which expands untracked files for path selection. A
change to an authored JSON pack can flag
many records due to shared-pack fingerprints without changing those records'
authored meaning. An uncited change is a coverage gap, **not clearance**.
Use `workspace-changes` when the review also needs to compare authored records
across two independently indexed source revisions. For a PR, give both
commands `--pr-merge-base` with the same base tip and topic head; verify the
effective base SHA agrees before interpreting the separate outputs.

This is **review evidence preparation**, not a violation classifier, PR
approval, verification of GitHub PR identity or its file list, complete Git
ancestry analysis, source-behavior analysis, observed runtime impact or semantic
truth. Opt-in merge-base selection establishes the comparison's shared
ancestor only; it does not qualify the review or substitute for source
checks. The agent must inspect original sources, actual code changes and
authoritative decisions before making a judgment. Unlike
`workspace-changes`, this command compares code path names rather than
knowledge-record payloads. Neither command replaces the other.

With `--include-worktree` at the checkout's own HEAD, the same packet also
lists staged, unstaged and untracked path names without indexing their bytes.
Per-file context is allocated in `review_scope.selection_order`: committed
changes first, then staged, unstaged and untracked paths, sorted within each
group. A partially staged file belongs to both the staged and unstaged groups;
its first listed group wins the slot. This ordering is a context-budget
policy, not a claim that untracked files are unimportant, and
`omitted_path_sample` reports what the budget excluded.

## Refactor rename preview (patch-only)

`sensemaking-skills semantic refactor-rename --repo . --path FILE --symbol OLD
--to NEW [--patch-out FILE] [--json]` reads one committed revision and computes
a unified patch for renaming one tracked top-level Python function or class. It
rewrites the definition, direct `from module import OLD` imports, unaliased
name loads, module-alias attribute loads and literal `__all__` entries. The
patch is applied in a disposable checkout, every changed file must parse, the
AST delta must contain only the intended identifier/string changes, and a
rescan must find no direct old-name references.

The command is patch-only: it never edits the active checkout. It fails closed
on ambiguous definitions, star imports, rebinding, new-name collisions, dynamic
`getattr`/import sites and exact string constants in related Python files.
`READY` means the generated patch passed those mechanics; it does not establish
runtime behavior, test coverage, API compatibility, generated-code safety,
re-export completeness or repository-wide renaming. `not_rewritten` separately
lists non-module attribute mentions and non-Python file mentions that were not
modified.


## Prospective patch rehearsal

```bash
sensemaking-skills semantic patch-rehearsal --repo . --ref BASE \
  --patch-file proposed.patch --limit 25 --json
```

Use this when the concrete alternative is already an explicit unified Git patch,
but the active checkout should not be changed merely to inspect it. The command
resolves the base commit, validates the patch's text/file scope, checks and
applies it in the existing disposable exact-commit worktree, verifies the actual
changed paths and reports before/after SHA-256 digests and changed Python file
syntax checks. It reuses `workspace-review-context` with the BASE commit as both
committed operands and the actual patched overlay as working changes. All product
claims, source fingerprints and architectural context are from BASE; candidate
reconsiderations are explicit path-overlap prompts only. The derived index is
temporary and no persistent index path is returned. The input patch remains the
caller's source, not an authorized instruction to apply it.

For each modified Python file, `definition_changes` compares unique top-level
function, async-function and class names on both sides of the actual applied
overlay. It includes before/after line spans (including decorators) and SHA-256
digests of exact definition source and attribute-free AST. Classifications are
`ADDED`, `REMOVED`, `AST_CHANGED` and `SOURCE_ONLY_CHANGED`; the last
means only that the parsed AST is equal, not that behavior is equivalent.
`module_context_source_changed` compares residual source outside these spans
and definition order; `module_context_ast_changed` compares non-definition
top-level statements and definition-name order. These signals are independent
of the definition rows, and a file-level change can occur with no changed
definition. Duplicate names, unavailable spans or parse failures return
`NOT_ASSESSED`, not an empty successful comparison. Change rows are bounded
by `--limit`, with total and truncation. Nested-definition identity, dynamic
effects, rename attribution, AST-omitted comments/type comments and semantic
equivalence are not established. AST digests are meaningful within the same
parser runtime, not a cross-Python-version identity contract.

Version 1 deliberately supports only UTF-8 unified patch text up to 256 KiB
modifying 1..8 distinct, existing tracked regular files. It refuses binary,
add/delete/rename/copy/mode changes, symlinks, submodules, Git control files,
unsafe paths, ambiguous scope and failed Git application. Git hooks, fsmonitor
and configured external filter commands are disabled for application; the existing
disposable checkout and guarded worktree readers govern source inspection.
No target code or tests are run; a Python syntax failure is reported as FAIL,
not hidden by the status REHEARSED. The worktree is disposable, not a security
sandbox. Do not use this as an authorization or arbitrary code execution surface.

`REHEARSED` means the patch applied and the scoped review returned; it does not
establish runtime behavior, semantic correctness, architectural conformance,
causal consequences, value, selection, or readiness. Manual isolated application
and existing review remain alternatives. The agent owns evaluation and any
separately authorized integration.


### Opt-in source and knowledge co-design

```bash
sensemaking-skills semantic patch-rehearsal --repo . --ref BASE \
  --patch-file proposed.patch \
  --knowledge-proposal .sensemaking/knowledge/new-capability.json --json
```

Without the option, the existing modification-only contract remains unchanged.
The option requires exactly one newly added direct knowledge pack at the named
path, no other changed knowledge packs, and admits new non-executable regular
files in existing contained directories. The same eight-path and 256 KiB patch
bounds apply. Delete/rename/copy/mode changes, binary changes, links, Git control
files, filter assignments and ambiguous paths are refused. Git applies into
an isolated worktree and its disposable index. New candidate blobs may remain
in the shared Git object store; no active checkout/index or branch is changed.
The temporary checkout is not a security sandbox.

The BASE product and architecture review continues to use only committed
knowledge; the candidate source remains an overlay. Each added file has
`before_sha256: null`; added Python definitions are compared to an empty
module because the file was absent. The separately named candidate pack is
checked with the existing single-pack steward against the candidate's
index-tracked working evidence and other committed BASE packs. It returns
`candidate_knowledge` with proposal SHA-256, `MECHANICALLY_VALID` and the
preflight result, or `NOT_VALIDATED` with a reason (including unavailable
validation). `REHEARSED` describes application and review, not pack validity.
Neither status accepts/promotes the pack, establishes semantic truth, validates
a whole prospective snapshot, executes code/tests, or authorizes integration.
Use ordinary source review and exact committed build before accepting knowledge.


## Source-qualified architectural routes

```bash
sensemaking-skills semantic source-route --repo . --ref HEAD \
  --from-path src/sensemaking_skills/patch_rehearsal.py \
  --to-path src/sensemaking_skills/semantic_architecture/verification_scenarios.py \
  --max-hops 6 --max-files 80 --json
```

Use this for an explicitly selected directional architectural inquiry, not a
repository-wide inferred impact graph. The existing Python import-candidate
reader is applied lazily to reachable tracked files in a disposable exact
committed checkout. Each returned edge has importer path, candidate target
path, candidate module, import syntax/line, source SHA-256 and file citation.
Root/src and relative-import conventions are the same bounded conventions as
source relationships; a package-member candidate may be an attribute or
re-export rather than an actual import. Ambiguous module-to-file mappings are
skipped and disclosed, never resolved by arbitrary first-match choice.

Breadth-first search returns one witnessed path, with hop count, or
`NO_ROUTE_FOUND_WITHIN_BOUNDS` when no witness was found without encountered
read/parse/ambiguity/file-budget gaps. `NOT_ASSESSED` means no witness and at
least one such gap. A found witness remains a positive syntactic observation
even when other explored branches were partial. Search bounds are 1..6 hops
and 1..250 inspected files (defaults 6/80); source parsing is limited to 512
KiB per file. The result discloses counts, queue/frontier, unresolved imports,
parse/read gaps and ambiguous candidates, with bounded detail. It does not
establish global shortestness, complete Python import resolution, actual runtime
coupling, absence of cycles, architectural conformance or semantic impact.
Local/conditional imports are included; dynamic imports, package initialization,
re-exports, non-Python and runtime behavior are not resolved. No target code or
tests are run and no action is authorized. Manual source inspection and
`context-for --include-source-relationships` remain complementary tools.

### Compare architectural source routes across commits

```bash
sensemaking-skills semantic source-route --repo . --base-ref BASE --ref TARGET \
  --from-path src/sensemaking_skills/semantic_architecture/source_relationships.py \
  --to-path src/sensemaking_skills/semantic_architecture/knowledge_sources.py --json
```

The optional `--base-ref` selects `SEMANTIC_SOURCE_ROUTE_COMPARISON`.
Without it the existing single-revision contract is unchanged. Both sides
use the same explicit normalized path pair and the same per-revision search
bounds; the full existing route result is retained at `base.result` and
`target.result` when both endpoints at that revision are regular files.
Each side reports literal committed endpoint status (`REGULAR_FILE`,
`ABSENT_FROM_TREE` or `NOT_REGULAR_FILE`). If either is unavailable,
that side is `ENDPOINT_UNAVAILABLE` and its result is null, not an empty
search. Same-ref comparisons reuse one observation.

The comparison status is `WITNESS_ON_BOTH`,
`BASE_WITNESS_TARGET_NO_WITNESS_WITHIN_BOUNDS`,
`TARGET_WITNESS_BASE_NO_WITNESS_WITHIN_BOUNDS`,
`NO_WITNESS_WITHIN_BOUNDS_ON_EITHER`, or `NOT_COMPARABLE` for an
unavailable endpoint or incomplete negative search. A positive witness
remains positive even if its search disclosed other gaps. With witnesses on
both sides, `same_witness_path_sequence` compares only the ordered path pairs
and `witness_hop_count_delta` is target minus base; otherwise both are null.
Inspect the preserved source hashes, cited lines and search limitations
before making an architectural judgment. This does not match renamed files,
establish all routes, infer dependency addition/removal or establish runtime
behavior, architectural conformance or semantic effects. No snapshot is
constructed by the comparison builder; no target code is executed.
