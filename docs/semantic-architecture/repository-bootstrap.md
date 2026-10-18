# Repository Semantic Bootstrap — staged implementation and use

**Status:** Source-pinned orientation and opt-in structural skeleton are implemented on a candidate branch; the first independent-agent longitudinal-value qualification remains unproven.
**Product authority:** [ADR 0031](../adr/0031-persistent-semantic-stewardship.md).
**Parent roadmap:** [Persistent Semantic Stewardship Plan](../persistent-semantic-stewardship-plan.md).
**Compatibility:** Existing semantic knowledge JSON v1, SQLite index, queries, and Skill authority boundaries are preserved.

## Intended experience

A coding agent entering a repository should learn enough to complete its actual
responsibility while making consequential knowledge recoverable by later agents.

- **Lean:** a narrow task inspects source directly; an index is never mandatory.
- **Stewardship:** a sustained engagement begins with a cheap read-only orientation,
  reconstructs relevant semantic claims when available, and selectively deepens.
- **Deep architecture:** only decision-relevant components, evidence, constraints,
  alternatives and history are expanded and reviewed.

The orientation does not create reviewed semantic claims. A directory name is not
a verified architectural boundary. A filename, import, or test reference is not
proof of product behavior. Missing edges mean NOT ASSESSED.

## First-visit contract — RSB-1

On a **clean checkout**, pin the full Git HEAD. Then run:

\`\`\`bash
REF="$(git rev-parse HEAD)"
sensemaking-skills semantic knowledge-orient \
  --repo . --repository "owner/repository" --target-ref "$REF" --json
\`\`\`

The output reports: repository/revision, tracked and eligible path counts,
inspected count, truncation, top-level tracked-path distribution, recognized file
extensions, candidate product entry documents, manifest examples, and bounded
source/test examples. It does **not** read document content or run repository code.
All entries are paths from the current Git index; source meaning requires
inspection. The command refuses untracked/dirty source bytes and wrong HEAD.

Defaults: maximum 5000 eligible paths inspected, 16 examples per category.
Both have bounded CLI options. Source-tree priority prevents archival files
from starving relevant product source paths when selection is truncated.
Names outside the recognized convention are NOT ASSESSED.

An optional \`--db /outside-checkout/semantic.sqlite\` retrieves exact-revision
counts/scope of a preexisting semantic index. It does not build or change the
database. A DB without that revision produces a clear NOT ASSESSED error.

## Opt-in structural projection — RSB-2

\`\`\`bash
sensemaking-skills semantic knowledge-build \
  --repo . --repository "owner/repository" --target-ref "$REF" \
  --db /outside-checkout/semantic.sqlite \
  --include-repository-structure --max-structural-files 600 \
  --include-python-imports --max-imports 1000 --json
\`\`\`

The existing rebuildable SQLite index retains the current schema and history.
The new additive relation \`contained_in\` describes *lexical Git file/directory
placement only*, not runtime dependency or component responsibility.
Indexed file records store exact source SHA256 fingerprints for later audit.
Structural scope covers recognized entry documents, manifests and Python source
under known source/test roots, with explicit truncation and no broad content
extraction. The Python import probe remains independent and opt-in; both options
may be combined without duplicate source claims.

Path and metadata extraction cannot establish application entrypoints, package
semantics, database correctness, tests executed, or product intent.

## Semantic enrichment — existing S1-S4 facilities

Read source-linked accepted ADRs and Grounding Pack claims with existing
\`knowledge-query search|explain|why\`. Use \`knowledge-query impact\` as a
*declared-edge candidate view* and \`contradictions\` only for **explicitly**
authored contested relationships. Neither operation automatically discovers
all consequences or conflicts.

For genuinely useful product-to-code or test-to-capability relationships, a
coding agent examines cited original files and authors **reviewed** typed
claims/edges in tracked \`.sensemaking/knowledge/*.json\`. Hypotheses stay
hypotheses. Review must not convert a generated inference into owner intent.

After source changes, use existing \`knowledge-audit\`, then rebuild/reconcile
the snapshot at the new clean HEAD. Preserve indexed history; source drift
is not automatic semantic invalidation.

## Delivery sequence and evidence ceiling

| Package | Responsibility | Qualification |
| --- | --- | --- |
| RSB-0 | This contract and existing-roadmap extension | Source/authority review |
| RSB-1 | First-visit bounded orientation | CLI integration and dirty-checkout tests |
| RSB-2 | Rebuildable structural graph | Deterministic/containment/currentness tests |
| RSB-3 | Product-to-code links | Existing authored S1-S4 records; validate a real connection before extending extraction |
| RSB-4 | Contradictions and staleness | Reuse current explicit contradictory-edge and audit queries; extend only for observed gaps |
| RSB-5 | Progressive task-based deepening | Existing Skills' optional consultation guidance |
| RSB-6 | Real independent agent qualification | Fresh agent, meaningful task, grounded query reuse/correction and full cost report |
| RSB-7 | Transfer and specialized adapters | Only when a concrete second product warrants them |

**S5 Issue #552 is the prerequisite independent-session longitudinal test.**
A freshly started Python interpreter is not a fresh coding agent. A local
test suite, hosted CI, synthetically populated graph, or this PR does not
establish engineering usefulness, comprehensive ontology correctness, or
S5/S6 transfer.

**Deferred on purpose:** automatic LLM ontology inference; automatic owner
decision promotion; obligatory repository-wide indexing; complete TypeScript,
SQL or multi-language architecture inference; unscoped model expansion;
cross-repository Dark Factory integration; a second graph database or
autonomous controller.

## Safety and performance boundaries

The index must be rebuilt from committed sources in a *clean* checkout; it
is external to that checkout. The structural reader rejects symlinks, escaping
paths, non-regular files and files above 512 KiB. Extraction and output are
capped. It never executes files from the target repository. Paths, documents
and generated observations are untrusted information, not agent instructions.

Known limitations: tracked inventory does not include ignored source files,
convention-based file categories are incomplete, the path skeleton is not a
call/dependency graph, source fingerprints record bytes not semantic quality,
and no comprehensive automated semantic extraction exists yet.

## Exit criterion

The meaningful product criterion is an independent coding agent that, when
working on a real engineering responsibility, uses source-cited accumulated
knowledge to make a materially better warranted decision or to correct stale
knowledge, preserving accurate history and reporting its costs.
