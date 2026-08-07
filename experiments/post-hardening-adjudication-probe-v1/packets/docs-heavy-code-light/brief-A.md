# Repository Sensemaking Brief — docs-heavy-code-light

## 1. Repository goal
`docs-heavy-code-light` presents itself as a data-processing pipeline: the
documentation defines a three-module architecture — `ingestor.py`,
`transformer.py`, `exporter.py` (`docs/architecture.md:3`) — implementing
three features — ingest, transform, export (`docs/spec.md:3`) — with a
roadmap item promising real-time mode (`docs/roadmap.md:3`), and the README
directs readers to `docs/` as the source of truth (`README.md:3`). In
reality the repository contains exactly one executable statement: a
hello-world print (`src/main.py:1`). The apparent goal — a working
ingest/transform/export pipeline — is documented but entirely unrealized;
the only goal the code itself accomplishes is printing "hello".

## 2. Current shape
Recursive listing of the repository:

```
docs-heavy-code-light/
├── README.md              (3 lines: title + "See docs/.")
├── docs/
│   ├── architecture.md    (3 lines: "Modules: ingestor.py, transformer.py, exporter.py.")
│   ├── roadmap.md         (3 lines: "Q3: real-time mode.")
│   └── spec.md            (3 lines: "Features: ingest, transform, export.")
└── src/
    └── main.py            (1 line: print('hello'))
```

Five files total. No package metadata (`pyproject.toml`, `setup.py`,
`requirements.txt` absent), no tests, no CI configuration, and no other
source files of any kind (structural proof from the directory listing
above).

## 3. Strong signals
- **A documentation skeleton exists and is deliberately organized**:
  `docs/` separates architecture (`docs/architecture.md:1`), spec
  (`docs/spec.md:1`), and roadmap (`docs/roadmap.md:1`) concerns rather
  than dumping everything into the README.
- **Docs-internal consistency**: the module vocabulary in
  `docs/architecture.md:3` (ingest → transform → export modules) matches
  the feature vocabulary in `docs/spec.md:3` (ingest, transform, export) —
  the documentation describes one coherent pipeline, not contradictory
  claims.
- **Forward-looking intent is recorded**: `docs/roadmap.md:3` states a
  concrete planned capability ("Q3: real-time mode"), showing the repo
  author is thinking about evolution.
- **The README is honest about where the truth lives**: `README.md:3`
  ("See docs/.") does not itself invent features — it delegates to the
  docs.

## 4. Missing pieces
- **Every documented module**: `ingestor.py`, `transformer.py`,
  `exporter.py` named in `docs/architecture.md:3` do not exist anywhere in
  the repository (the Section 2 listing shows no such files).
- **Every documented feature**: ingest, transform, export
  (`docs/spec.md:3`) have no implementation, no interfaces, and no stubs.
- **A real entry point**: `src/main.py:1` (`print('hello')`) is a stub,
  not a pipeline entry point; there is no `if __name__ == "__main__"`
  block and no invocation of the documented modules.
- **Tests and packaging**: no test files, no `pyproject.toml`/`setup.py`,
  no dependency manifest — nothing that could verify or install the
  documented system.
- **An implemented/planned distinction**: nothing in the repo marks
  documented functionality as "not yet built"; the docs are phrased in the
  present tense (`Modules:`, `Features:`) as if the system exists.

## 5. Improvement opportunities
- Add a doc↔code validation check (a script or CI step that asserts every
  module/feature named in `docs/architecture.md:3` and `docs/spec.md:3`
  has a corresponding file or symbol), preventing ghost claims from
  re-accumulating.
- Add explicit status markers ("implemented" vs "planned") in
  `docs/architecture.md:3` and `docs/spec.md:3` so readers and agents can
  distinguish reality from aspiration without cross-checking the source
  tree.
- If the pipeline is genuinely the goal, add minimal packaging metadata
  and a stub module layout (`src/ingestor.py`, `src/transformer.py`,
  `src/exporter.py`) so the architecture matches the file system.
- Tie `docs/roadmap.md:3` to an actual issue/tracker so "Q3: real-time
  mode" is a tracked commitment rather than an orphaned line.

## 6. Weakest boundary
The weakest boundary is the **documentation↔code contract**: the
documentation asserts a three-module, three-feature pipeline while the
code contains one print statement. `docs/architecture.md:3` names modules
(`Modules: ingestor.py, transformer.py, exporter.py.`), `docs/spec.md:3`
names features (`Features: ingest, transform, export.`), and
`docs/roadmap.md:3` promises evolution ("Q3: real-time mode") — but the
complete source tree is `src/main.py:1` (`print('hello')`). The README
(`README.md:3`) sends every reader to the docs as the authoritative
description, so the documentation is the only map of the repository and it
describes territory that does not exist. Nothing distinguishes "built" from
"planned"; every documented capability is documentation-only.

Logic trace: `docs/architecture.md:3` and `docs/spec.md:3` enumerate
modules and features in the present tense; the recursive file listing of
the repository (Section 2) shows exactly one source file, `src/main.py`,
whose entire body is `print('hello')` (`src/main.py:1`); `README.md:3`
designates the docs as the reader's guide. From these three observations it
follows that every module and feature the documentation describes has no
corresponding implementation — functionality mentioned in documentation
with no implementation anywhere in the code, which is the definition of the
Ghost Features weakness type.

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)
**docs_fog** — the primary uncertainty is a knowledge gap created by the
documentation: it specifies a system that does not exist, so anyone
(including an agent) who reads `docs/architecture.md:3` or
`docs/spec.md:3` forms a false model of the repository. Per the
repo-sensemaker skill's docs_fog signals ("README, ADR files, architecture
docs, runbooks missing or outdated"), the architecture docs here are
materially false — the strongest form of "outdated".

- Not `ui_fog`: the repository contains no frontend code at all (no
  React/Vue/Angular/HTML/CSS), so per the UI Fog Signals Registry decision
  tree the answer is "NO → Not ui_fog; evaluate other fog types".
- Not `product_fog`: the features are in fact specified
  (`docs/spec.md:3`); the gap is not vague requirements but unrealized
  ones — the problem is not that nobody knows what to build, it is that
  the docs claim it is built.
- Not `architecture_fog`: there is no code structure to be unclear — one
  executable statement cannot have coupling or boundary problems. The
  defect is not in the code's shape but in the claims made about it.

## 7. Evidence
1. `docs/architecture.md:3` — "Modules: ingestor.py, transformer.py,
   exporter.py." The architecture document names three module files; the
   directory listing (Section 2) shows none of them exist.
2. `docs/spec.md:3` — "Features: ingest, transform, export." The spec names
   the pipeline stages; no implementation, interface, or stub exists for
   any of them.
3. `src/main.py:1` — "print('hello')". The entirety of the source code is
   a hello-world stub, providing no entry point for the documented system.
4. `README.md:3` — "See docs/." The README delegates all description to
   the docs, making the documentation the repository's sole source of
   truth.
5. `docs/roadmap.md:3` — "Q3: real-time mode." The roadmap plans evolution
   of a system whose base capabilities do not exist.

Logic trace: the architecture and spec documents (`docs/architecture.md:3`,
`docs/spec.md:3`) are written in the present tense about modules and
features; the source tree contains exactly one Python file whose body is a
single print (`src/main.py:1`); and the README (`README.md:3`) points all
readers at the docs rather than at code. The chain "docs claim → files
absent → no other source of truth" means the documentation is the only
place where the pipeline exists — documentation-only functionality, i.e.
Ghost Features — which in turn is the source of the repository's fog: the
docs create knowledge about a system that does not exist (docs_fog).

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: docs/architecture.md
    lines: L3
    quote: "Modules: ingestor.py, transformer.py, exporter.py."
    supports_claim: "The architecture document names three module files that do not exist anywhere in the repository."
  - file: docs/spec.md
    lines: L3
    quote: "Features: ingest, transform, export."
    supports_claim: "The spec names three features with no implementation, interface, or stub in the source tree."
  - file: src/main.py
    lines: L1
    quote: "print('hello')"
    supports_claim: "The entire source code is a hello-world stub; the documented pipeline has no entry point."
  - file: README.md
    lines: L3
    quote: "See docs/."
    supports_claim: "The README designates the docs as the source of truth, so the ghost claims in the docs become the repository's only description."
  - file: docs/roadmap.md
    lines: L3
    quote: "Q3: real-time mode."
    supports_claim: "The roadmap plans evolution of a system whose base features are unimplemented."
```

## 9. Why this boundary matters
Every consumer of this repository is misled at the first step. A human or
agent reading `docs/architecture.md:3` will attempt to import or edit
`ingestor.py`, `transformer.py`, or `exporter.py` and fail; a planner using
`docs/spec.md:3` will estimate work on features that have no code;
`docs/roadmap.md:3` schedules "real-time mode" for Q3 on a system that
cannot even ingest. The repository's identity — "a data pipeline" — is
fiction, so onboarding, automated analysis, estimation, and the roadmap all
build on false premises, and any agent that trusts the docs will produce
hallucinated analysis of its own (citing modules that do not exist).

## 10. Candidate next steps
1. Run a docs-reality audit: for each claim in `docs/architecture.md:3`
   and `docs/spec.md:3`, verify the file/symbol exists and mark each claim
   implemented or planned (or delete it).
2. Decide the repository's actual intent with the owner — placeholder vs.
   real pipeline — and state it in one sentence in `README.md:3`.
3. If the pipeline is the goal, implement it (ingest → transform →
   export) with a proper entry point in `src/`, then update the docs to
   match; this is a build effort that would route through
   `architecture-implementation-workflow`.
4. Add a doc↔code validation check so documented modules/features must
   exist (or be explicitly marked planned) before a commit is accepted.
5. If the pipeline is deferred, rewrite `docs/architecture.md:3`,
   `docs/spec.md:3`, and `docs/roadmap.md:3` to describe only what exists,
   with planned items clearly labeled.

## 11. Recommended next step
Reconcile the documentation with reality first: rewrite
`docs/architecture.md:3` and `docs/spec.md:3` so every named module/feature
is either backed by a real file or explicitly marked "planned", and add a
one-line status to `README.md:3` (e.g. "docs describe the intended
pipeline; today only src/main.py exists"). This is the smallest change that
makes every claim in the repository testable, unblocks the
build-vs-descope decision, and prevents downstream agents from acting on
ghost modules.

## 12. Recommended workflow
`docs-implementation-workflow` — defined in
`skills/workflow-planner/references/workflow-registry.yaml:812` as "For
documentation/knowledge problems. Aligns domain understanding, creates
documentation architecture, and generates docs." It matches this
diagnosis: the weakest boundary is a documentation-truth problem (docs
asserting functionality that does not exist), so the first fix is aligning
the docs with the actual repository. If the build-vs-descope decision
lands on "build the pipeline", `architecture-implementation-workflow`
(`workflow-registry.yaml:848`) is the correct follow-on — but the docs
must be made truthful before any implementation can be scoped against
them.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/docs-heavy-code-light
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: docs_fog
diagnosis_conflict: false
escalation_required: false
escalation_recommended: false
evidence:
  - "docs/architecture.md:3: names modules ingestor.py, transformer.py, exporter.py — none exist in the repository"
  - "docs/spec.md:3: names features ingest, transform, export — no implementation, interface, or stub exists"
  - "src/main.py:1: entire source code is print('hello') — no pipeline entry point"
  - "README.md:3: 'See docs/.' — docs are designated the source of truth, so ghost claims propagate"
  - "docs/roadmap.md:3: 'Q3: real-time mode.' — roadmap plans evolution of an unimplemented system"
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
recommended_workflow_id: docs-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
> Run workflow `docs-implementation-workflow` with `context_artifacts =
> [this repository_sensemaking_brief]` for repository
> `docs-heavy-code-light`. Scope: make the documentation truthful about the
> actual repository — rewrite `docs/architecture.md:3` and `docs/spec.md:3`
> so every named module (ingestor.py, transformer.py, exporter.py) and
> feature (ingest, transform, export) is either backed by a real file or
> explicitly marked as planned; add a one-line implemented-status statement
> to `README.md:3`; and mark `docs/roadmap.md:3` (real-time mode) as
> contingent on the base pipeline existing. Do not implement the pipeline;
> produce the documentation architecture and copy-paste prompts only.
