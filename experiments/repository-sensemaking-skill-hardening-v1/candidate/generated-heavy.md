# Repository Sensemaking Brief — generated-heavy

## 1. Repository goal

The repository presents itself as a protobuf-based project: README.md:2 states the project is "Protobuf-based". The implied goal is a working protobuf project — define message types in a `.proto` schema, expose them through generated bindings (`generated/api_pb2.py`, `generated/api_pb2_grpc.py`), exercise them from a handwritten entry point (`handwritten/main.py`), and ship built artifacts (`dist/`). What the code actually delivers is a stub: the only domain type is an empty class and the gRPC module contains no code.

## 2. Current shape

Runtime flow reconstruction (what actually runs, not the directory layout):

- **Startup path**: `handwritten/main.py` is the only executable entry point. It imports `Message` from `generated.api_pb2` (handwritten/main.py:1), instantiates it (handwritten/main.py:3), and prints it (handwritten/main.py:4). This executes successfully because an empty class is instantiable — nothing else happens.
- **Orchestration**: none. `main.py` is a 4-line script; there are no functions, services, workers, commands, or route registrations (Pass B).
- **Domain/core logic**: none. The only domain type, `Message`, is an empty class (`generated/api_pb2.py:2-3`).
- **Persistence/state**: none. No files, database, cache, queue, or environment variables are read or written anywhere (Pass A/C).
- **External integration points**: none. A protobuf/gRPC project's external boundary would be the gRPC stubs in `generated/api_pb2_grpc.py`, but that file contains only a comment (generated/api_pb2_grpc.py:1) — no `*Stub`/`*Servicer` classes, no server or client wiring.
- **Background work**: none.
- **Output boundary**: stdout via `print(m)` (handwritten/main.py:4). The `dist/` files print fixed strings (dist/app.py:1, dist/bundle.js:1) and are not imported by anything; they are claimed build outputs with no build pipeline behind them.
- **Where responsibility becomes unclear**: the generated/ boundary. `generated/api_pb2.py:1` declares the file is protoc output ("DO NOT EDIT!"), yet no `.proto` source exists anywhere in the repository, so nothing can regenerate it; the only repair path (hand-editing) is what the header forbids.

Dependency semantics (declared vs used vs dead): `generated.api_pb2` is `declared` (import at handwritten/main.py:1), `used` (the import executes), and `runtime` on the proven execution path of `main.py`. `generated.api_pb2_grpc` is neither imported nor executed — a dead module that is *presented* as live generated code. `dist/app.py` and `dist/bundle.js` are not imported by any code (dead as modules) and have no producer. No third-party dependency is declared anywhere: there is no manifest of any kind in the repository.

State model: no state boundaries exist (nothing writes or reads state).

Boundary model: the only real boundary is import-time — `handwritten/main.py:1` → `generated/api_pb2.py:1-3`. It is unvalidated: the importer assumes `Message` is a protobuf message with serialization semantics; the callee provides none.

## 3. Strong signals

- Honest directory naming: `handwritten/` vs `generated/` vs `dist/` encodes the intended separation of authored, generated, and built code (observed via the repository tree).
- The entry-point wiring is real: `from generated.api_pb2 import Message` (handwritten/main.py:1) executes and instantiates successfully — the import contract between handwritten and generated code is functional.
- The "DO NOT EDIT" headers (generated/api_pb2.py:1, generated/api_pb2_grpc.py:1) correctly guard generated code — the right discipline, even though these files are not truly generated.
- The repository is small and fully legible: 6 files; a reader can enumerate the entire system in minutes.

## 4. Missing pieces

- A `.proto` source definition — the canonical input of any protobuf project — does not exist anywhere in the repository (Pass A/C). UNKNOWN where the schema lives; the generated modules cannot be regenerated.
- Real protobuf semantics in `generated/api_pb2.py`: no `google.protobuf` import, no descriptors, no serialization/parsing methods; `Message` is `pass` (generated/api_pb2.py:2-3).
- Any gRPC code in `generated/api_pb2_grpc.py`: no Stub, Servicer, or registration function — the file is one comment line (generated/api_pb2_grpc.py:1).
- Build/packaging configuration: no `pyproject.toml`, `setup.py`, `package.json`, Makefile, or CI config; the `dist/` outputs have no producer and nothing validates them (Pass A/D).
- Tests, schemas, and validation of any kind: none (Pass D).
- Documentation beyond the 3-line README: no architecture, usage, or generation instructions.

## 5. Improvement opportunities

- Add a real `.proto` schema and a documented generation command so `generated/` is reproducible.
- Replace the stub `Message` with protoc-generated bindings — or an explicitly honest hand-written class with real serialization — instead of an empty `pass` class.
- Add a minimal manifest (e.g. `pyproject.toml`) and a test that runs `handwritten/main.py` and asserts a serialization round-trip; that would establish the repository's first validation boundary.
- Either wire `api_pb2_grpc.py` into a real client/server or delete it; a comment-only file labeled "generated" misleads readers.
- Delete or genuinely build `dist/`; one-line print scripts labeled "built"/"minified" are noise for any future reader.

## 6. Weakest boundary

Candidates were generated first (per the skill's Weakest Boundary Reasoning), then scored on evidence strength / severity / blast radius / goal relevance / downstream blocking effect / uncertainty:

| # | Boundary | Evidence | Score |
|---|----------|----------|-------|
| 1 | Fake generated protobuf/gRPC surface: `generated/api_pb2.py` + `generated/api_pb2_grpc.py` documented as protoc output but stubbed/empty | strong | severity high; blast high; goal relevance high; blocking high; uncertainty low |
| 2 | Fake build artifacts with no pipeline: `dist/app.py`, `dist/bundle.js` vs absent build config | strong | severity medium; blast low-medium; goal relevance medium; blocking low |
| 3 | Unwired module: `api_pb2_grpc.py` never imported by any file | strong | severity medium; blast low; goal relevance medium; blocking low |
| 4 | Zero validation/test presence (no tests, CI, manifests) | weak (negative evidence — absence) | severity medium; blast high; goal relevance medium; blocking medium |

Selection:

```text
Boundary: the protobuf/gRPC contract surface — generated/api_pb2.py and generated/api_pb2_grpc.py, presented (by their own headers and by the README) as real protoc-generated modules of a protobuf-based project.
Observed contract: README.md:2 describes the repository as "Protobuf-based project."; generated/api_pb2.py:1 declares the file was produced by "the protocol buffer compiler" and must not be edited; generated/api_pb2_grpc.py:1 declares itself generated; handwritten/main.py:1 imports a Message type from the generated package and uses it as a domain object.
Observed violation or uncertainty: generated/api_pb2.py:2-3 defines `class Message: pass` — an empty stub with no google.protobuf import, no descriptors, no serialization; generated/api_pb2_grpc.py:1 contains only a comment and zero code (no Stub/Servicer); no .proto source file exists anywhere in the repository, so the "generated" files cannot be regenerated; the DO NOT EDIT headers forbid the only remaining repair path.
Evidence: README.md:1-3; generated/api_pb2.py:1-3; generated/api_pb2_grpc.py:1; handwritten/main.py:1-4; dist/app.py:1; dist/bundle.js:1; exhaustive recursive listing showing the absence of any .proto, manifest, build, CI, or test file.
Weakness type: Ghost Features
Logic trace: README.md:2 documents the project as "Protobuf-based", and the generated modules' own headers (generated/api_pb2.py:1, generated/api_pb2_grpc.py:1) document them as compiler-generated protobuf/gRPC code — a documented surface. Opening those files shows the documentation's promise has no reachable implementation: api_pb2.py contains only an empty class (generated/api_pb2.py:2-3) with no protobuf semantics, and api_pb2_grpc.py contains no code at all (generated/api_pb2_grpc.py:1). The entry point (handwritten/main.py:1-4) runs, but only because an empty class is instantiable — nothing serializes, parses, or serves. A full recursive listing confirms no .proto, no manifest, and no generation tooling exists to produce the promised surface. Therefore a documented product/code surface (protobuf project + generated modules) promises functionality with no reachable implementation — Ghost Features, not a wiring ambiguity (Implicit Dependencies) and not a naming mismatch (Vocabulary Drift).
Failure consequence: any consumer or downstream workflow that trusts the README and the generated-file headers will treat the repository as a protobuf/gRPC project and attempt serialization or RPC against a surface that does nothing; regeneration is impossible without a .proto, and the DO NOT EDIT headers actively discourage the only alternative (rewriting the stubs); the project's entire stated purpose is unfulfilled.
Confidence: high — every file in the repository (6 of 6) was opened and cited; the absence of .proto/manifest/test files is established by exhaustive recursive listing, not sampling. What would raise it further: git history proving real protoc output was replaced by stubs (the fixture has no git history).
Alternatives considered:
- Zero Validation (candidate 4): the repository indeed has no automated checks, but absence of validation does not explain the missing protobuf implementation; it is a contributing gap, not the weakest boundary.
- Implicit Dependencies (candidate 3): api_pb2_grpc.py is never imported, but it is DOCUMENTED as present (its header claims it is generated), which per the constrained taxonomy maps to Ghost Features, not undocumented wiring.
- Vocabulary Drift: rejected — the vocabulary aligns (README says protobuf; api_pb2 and Message exist); the defect is absent functionality, not mismatched terms.
- Contract Mismatch: rejected — every file is the format it claims (.py/.js); only provenance and functionality are fabricated, not format.
```

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)

The primary fog type is **product_fog**. Evidence: the README advertises the repository as "Protobuf-based project." (README.md:2) — the deliverable is a protobuf project — while the protobuf/gRPC surface is a stub with no reachable implementation (generated/api_pb2.py:2-3; generated/api_pb2_grpc.py:1). This is a promised deliverable with no implementation: the defect is the promise (product contract), not the docs' wording. It is not architecture_fog: the sole entry point (handwritten/main.py:1-4) boots and runs, so the entry-point-stub rule (a skeletal runtime entry point) does not apply — `main.py` is not skeletal. The UI Fog registry does not apply: the only JavaScript is a one-line `console.log` in `dist/` (dist/bundle.js:1) — no React/Vue/Angular/HTML/CSS, no screens, no flows, no routing, no design system — so all Tier-1 checks are vacuous → NOT ui_fog (ui-fog-signals.md decision tree: no frontend code → not ui_fog). Secondary contributing fog: docs_fog (the "Generated by the protocol buffer compiler" headers misdescribe stub files) — recorded in prose only; product_fog drives routing.

## 7. Evidence

The diagnosis rests on files actually opened in this run:

- README.md:1-3 — the README's only substantive claim is "Protobuf-based project." (README.md:2), the documented product promise.
- generated/api_pb2.py:1 — header claims protoc provenance; generated/api_pb2.py:2-3 — `class Message: pass`, an empty stub with no protobuf semantics.
- generated/api_pb2_grpc.py:1 — a comment-only file claiming to be generated; no gRPC code.
- handwritten/main.py:1 — `from generated.api_pb2 import Message`; handwritten/main.py:3-4 — instantiation and print: the entry point runs but only exercises the stub.
- dist/app.py:1 and dist/bundle.js:1 — claimed built/minified artifacts that are one-line prints with no build pipeline.

Logic trace: the README (README.md:2) and the generated-file headers (generated/api_pb2.py:1, generated/api_pb2_grpc.py:1) document a protobuf/gRPC surface; opening those files shows the implementation is an empty class (generated/api_pb2.py:2-3) and an empty comment (generated/api_pb2_grpc.py:1); the entry point (handwritten/main.py:1-4) proves only that an empty class instantiates; an exhaustive listing proves no .proto source exists to regenerate the surface. A documented surface with no reachable implementation is Ghost Features, and because the defect is the product promise (README.md:2 says "Protobuf-based project"), the primary fog is product_fog — not docs_fog (the headers would be wrong even if the README were deleted) and not architecture_fog (the entry point boots; the system is not structurally prevented from working — it simply has no implementation).

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L1-L3
    quote: "# generated-heavy\n\nProtobuf-based project."
    supports_claim: "README documents the repository as a protobuf-based project — the product promise whose implementation is stubbed."
  - file: generated/api_pb2.py
    lines: L1-L3
    quote: "# Generated by the protocol buffer compiler. DO NOT EDIT!\nclass Message:\n    pass"
    supports_claim: "File documents itself as protoc output yet contains only an empty Message stub — no protobuf semantics."
  - file: generated/api_pb2_grpc.py
    lines: L1
    quote: "# Generated. DO NOT EDIT!"
    supports_claim: "gRPC module is documented as generated but contains no code at all — no Stub/Servicer implementation."
  - file: handwritten/main.py
    lines: L1-L4
    quote: "from generated.api_pb2 import Message\n\nm = Message()\nprint(m)"
    supports_claim: "The only entry point imports and instantiates Message — it runs, proving only that an empty class is instantiable."
  - file: dist/app.py
    lines: L1
    quote: "print('built artifact')"
    supports_claim: "built artifact is a one-line print with no build pipeline behind it."
  - file: dist/bundle.js
    lines: L1
    quote: "console.log('minified');"
    supports_claim: "'minified' artifact is a one-line print; no frontend/UI code exists anywhere in the repository."
```

## 9. Why this boundary matters

If left as-is, anyone — human or workflow — trusting README.md:2 and the generated-file headers will build on a surface that does nothing: serialization and RPC attempts fail at runtime or silently no-op; regeneration is impossible because no `.proto` exists; and the DO NOT EDIT headers (generated/api_pb2.py:1) block the only repair. The repository's entire stated purpose — being a protobuf-based project — remains unfulfilled, and every downstream sensemaking step that assumes the protobuf contract inherits the same false premise. This is the boundary most able to block valuable next work: all other improvements (tests, docs, build pipeline) presuppose a real contract surface.

## 10. Candidate next steps

1. Define the real protobuf contract: author a `.proto` schema (message + service definitions) and a documented generation command, then regenerate `generated/api_pb2.py` and `generated/api_pb2_grpc.py`.
2. Make the entry point meaningful: extend handwritten/main.py to serialize/parse a `Message` and exercise the gRPC stub once it exists.
3. Add a build/packaging manifest (e.g. `pyproject.toml`) and a test that runs main.py and round-trips a message — establishing the repository's first validation boundary.
4. Reconcile the documentation: either fix README.md:2 and the generated headers to describe reality, or delete the comment-only `api_pb2_grpc.py` until real gRPC code exists.
5. Remove or genuinely build the `dist/` artifacts so no future reader mistakes print scripts for build outputs.

## 11. Recommended next step

Step 1: author the `.proto` schema and regenerate the `generated/` modules. This replaces the ghost surface with a real, reachable implementation and is the prerequisite for every other step (the entry point, tests, and docs all depend on the protobuf contract existing). It is the smallest concrete action that directly closes the weakest boundary.

## 12. Recommended workflow

`product-implementation-workflow` (workflow-registry.yaml:644-714) — the registry's workflow for product/feature problems: it aligns domain, researches/synthesizes the requirement, creates a spec, and implements via TDD. Execution mode: `guided_execution`, one of that workflow's `allowed_execution_modes` (workflow-registry.yaml:654-656; `plan_only` is not offered for this workflow, so it is not used). Routing rationale: the weakest boundary is a product-contract defect (promised protobuf surface with no implementation), so the product implementation path fits. Closest alternatives lose on fit: `architecture-implementation-workflow` (workflow-registry.yaml:848) targets structural/refactoring problems and the entry point boots fine here; `docs-implementation-workflow` (workflow-registry.yaml:812) would fix the headers but leave the stubbed surface intact; `ui-diagnostic-workflow`/`ui-implementation-workflow` (workflow-registry.yaml:715,748) do not apply (no frontend). Preconditions missing before it can run: a user-intent statement and agreement on the actual message/service schema (the repository itself offers none); `guided_execution` keeps human gates at each review step. Recommendation of the workflow is diagnostic only — no implementation is performed by this brief.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/generated-heavy
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
user_implied_fog_type: unknown
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "README.md (lines 1-3): repository documented as 'Protobuf-based project.' — the promised deliverable"
  - "generated/api_pb2.py (lines 1-3): header claims protoc generation; body is 'class Message: pass' with no protobuf semantics"
  - "generated/api_pb2_grpc.py (line 1): comment-only file claiming to be generated; no gRPC code"
  - "handwritten/main.py (lines 1-4): entry point imports and instantiates Message and prints — boots, but only exercises the stub"
  - "dist/app.py (line 1) and dist/bundle.js (line 1): claimed build outputs that are one-line prints; no build pipeline"
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T04:06:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

"Repository sensemaking brief for `experiments/repository-sensemaking-skill-hardening-v1/corpus/generated-heavy` is ready (artifact_id: `repository_sensemaking_brief`). Primary fog: `product_fog` — README.md:2 advertises a 'Protobuf-based project', but the protobuf/gRPC surface is a stub: generated/api_pb2.py:2-3 defines only `class Message: pass`, generated/api_pb2_grpc.py:1 is comment-only, and no `.proto` source exists anywhere in the repo. Weakest boundary: Ghost Features (documented surface with no reachable implementation). Recommended route: `product-implementation-workflow` in `guided_execution` mode. First step: author the `.proto` schema (message + service definitions), regenerate the `api_pb2`/`api_pb2_grpc` modules with a documented generation command, and do not hand-edit the DO NOT EDIT files. Note: the Ghost Features classification carries a D5 requirement — a substantive human audit is required before final approval."
