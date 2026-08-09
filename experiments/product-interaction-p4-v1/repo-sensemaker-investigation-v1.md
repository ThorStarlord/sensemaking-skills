# Repository Sensemaking Brief - renpy_mcp_server (Task P4)

experiment_type: product_interaction
record: repo-sensemaker-investigation-v1
produced_by: canonical repo-sensemaker SKILL.md (sensemaking-skills @ 27aa2442, blob a5cb5dd7)
target_repository: renpy_mcp_server @ a1d6f55af5716a50a8674302466b385711ef513f
owner_question: "What engineering work would create the most value next?"
mode: agent-native, one-shot, read-only (canonical repo-sensemaker, exactly once)
created_at: 2026-08-08

---

## 1. Repository goal

An [Model Context Protocol](https://modelcontextprotocol.io/) server that lets
AI assistants build complete Ren'Py visual novels: AI image generation
(backgrounds and characters via Gemini), script generation, web builds, and
local preview (README.md:3). The repository's front door describes ONE
product, but the repository now contains TWO parallel implementations of that
goal:

- a **Python MCP server** (`src/renpy_mcp_server/`), the declared entrypoint
  (`pyproject.toml:30`), the one the owner's live MCP client config launches
  (`.mcp.json:9`), and the only one the root README documents
  (README.md:140-171);
- a **TypeScript MCP app** (`renpy_mcp_app/`, npm package `renpy-studio`
  v1.0.0, package.json:2-3) that reimplements the same tool groups
  (project/asset/script/build) plus a full React studio UI and its own
  copies of the Python pipeline modules.

## 2. Current shape

- **Git surface**: 4 commits, no tags, no branches beyond `main`, no CI.
  History: `8f782f1` Initial commit (2025-10-14), `6277feb` init commit
  (2025-10-15), `0924bcc` add gif (2025-10-15), `a1d6f55` added renpy_mcp_app
  (2026-02-01). 85 tracked files; 54 (63%) are in `renpy_mcp_app/`.
- **Python server** (`src/renpy_mcp_server/`, 14 tracked files): `server.py`
  (32 KB) registers 11 MCP tools (list_projects, list_project_files,
  read/edit_project_file, create_project, generate_background,
  generate_character, generate_script, build_project, start/stop_web_preview;
  server.py:38-898); helpers `image_service.py`, `background_remover.py`,
  `build_manager.py`, `preview_manager.py`, `project_manager.py`,
  `gemini_provider.py`, `settings.py`; a `templates/basic` Ren'Py starter.
  Version declared `0.1.0` (pyproject.toml:3). Workspace root = env
  `RENPY_MCP_WORKSPACE` or `cwd/workspace` (settings.py:37, settings.py:26-31).
- **TypeScript app** (`renpy_mcp_app/`): npm package `renpy-studio` v1.0.0
  (package.json:2-3), entry `bin/cli.js` for `npx renpy-studio --stdio`;
  MCP server named `renpy-studio` (index.ts:56) registering the same tool
  groups plus `view_studio` UI tool (index.ts:64-69); React UI
  (`src/ui/studio.tsx`, 81 KB), Ren'Py parser (`src/lib/renpy-parser.ts`),
  SDK auto-provisioning (`src/provision/renpy-sdk.ts`), and **its own copies
  of the Python pipeline modules** (`python/image_service.py`,
  `python/background_remover.py`, `python/build_manager.py`,
  `python/preview_manager.py`). Workspace root =
  `~/.renpy-studio/workspace/` (CLAUDE.md:52). Own README.md + CLAUDE.md.
- **Root docs/config**: README.md (documents only the Python server, badge
  claims version 4.1.4 at README.md:5), CONTRIBUTING.md, examples/ (2 agent
  framework examples), setup.sh / test_setup.sh, test_nano_banana.py (live
  Gemini smoke test), media/ (images/gif), .mcp.json.example.
- **Local runtime state (untracked)**: `.mcp.json` wires the Python server:
  `uv run renpy-mcp-server` with `RENPY_SDK_PATH=H:\Renpy\renpy-8.5.2-sdk` and
  `RENPY_MCP_WORKSPACE=H:\GithubRepositories`. `.venv/` and `workspace/` are
  gitignored.

## 3. Strong signals

- **Working product surface, not a stub.** The Python server implements a
  complete tool chain (project -> assets -> script -> build -> preview) and
  the Gemini path is exercised by a real smoke test (test_nano_banana.py).
- **The app is a serious implementation.** Full React studio UI, a real
  Ren'Py parser, SDK/venv auto-provisioning, and a published npm identity
  (`renpy-studio` with its own README and CLAUDE.md) - this is not a throwaway
  spike. (CODE/DOC)
- **Small, single-owner surface.** 85 tracked files, one author, MIT license,
  automated setup scripts - the repo is small enough that one decisive
  architecture decision is cheap to make now and expensive to defer. (CODE/HISTORY)
- **Owner's live config is unambiguous.** The untracked `.mcp.json` on this
  machine launches the Python server; that is the surface the owner actually
  uses today. (RUNTIME-ARTIFACT)

## 4. Missing pieces

- **No declaration of canonical surface.** Nowhere in the repository is the
  relationship between `src/renpy_mcp_server/` and `renpy_mcp_app/` stated:
  replacement? sibling? experimental? legacy? (DOC absence - 0 mentions of
  the app in the root README; verified by search)
- **Zero automated tests.** No test directory, no pytest config, no CI, and
  the app's `package.json` scripts (build/dev/serve/start/prepublishOnly,
  package.json:16-24) contain no `test` script. The only test-like file,
  test_nano_banana.py, requires a live `GEMINI_API_KEY` (test_nano_banana.py:76)
  and network access. (TEST)
- **No release identity.** No tags, no changelog, no releases; the README
  badge claims 4.1.4 while pyproject.toml:3 declares 0.1.0 - the same
  repository cannot even state its own version. (CONFIG/DOC/HISTORY)
- **No cross-referencing docs.** The root README never mentions the app; the
  app's CLAUDE.md says only that it lives in this repo's `renpy_mcp_app/`
  folder (CLAUDE.md:12). (DOC)

## 5. Improvement opportunities

- Align the version claim (badge 4.1.4 vs pyproject 0.1.0) with the chosen
  release process.
- Add an MCP-level contract smoke test asserting both surfaces register the
  same core tool names - a cheap automated drift detector.
- Extract the shared Python pipeline modules to one location both surfaces
  import instead of maintaining parallel copies.
- Add offline unit tests for the deterministic core (project_manager,
  build_manager path handling) that need no API key, and a CI runner.

## 6. Weakest boundary

The repository implements the same product contract twice, in two stacks,
with no declared canonical surface - and the two implementations have already
started to diverge. The Python modules copied into `renpy_mcp_app/python/`
differ from their `src/renpy_mcp_server/` counterparts by hundreds of lines
each (Compare-Object: image_service.py 349 differing lines, build_manager.py
542, background_remover.py 245, preview_manager.py 243). The two surfaces
also disagree on fundamentals: install path (`uv run renpy-mcp-server` vs
`npx renpy-studio --stdio`), workspace root (`RENPY_MCP_WORKSPACE`/cwd
workspace at settings.py:37 vs `~/.renpy-studio/workspace/` at CLAUDE.md:52),
and version identity (README badge 4.1.4 vs pyproject 0.1.0 vs package.json
1.0.0). The root README - the repository's front door - documents one surface
as if the other did not exist.

The decision boundary is therefore: **which surface is the product going
forward, and what is the declared relationship between the two?** Until that
is decided, every fix, feature, and test lands on one surface and widens the
drift; no version claim can be made coherent; and any validation investment
can be misallocated to the surface being abandoned. Repository evidence is
sufficient to discover this boundary but not to resolve it - resolving which
surface wins requires the owner's product intent.

**Weakness type:** Contract Mismatch

## 6.5. Problem classification (fog type)

Primary fog type: `architecture_fog` - the uncertainty is structural: unclear
boundaries between two parallel codebases, duplicated modules, two
entrypoints for one product. The user's generic question implies no specific
fog type (`unknown`); there is no user claim to conflict with
(`diagnosis_conflict: false`). Product intent (which surface is the future
product) is bounded as an explicit uncertainty below - it cannot be inferred
from repository evidence alone.

## 7. Evidence

Files actually read: README.md, pyproject.toml, .mcp.json, .gitignore,
CONTRIBUTING.md, requirements.txt, test_nano_banana.py, setup.sh (header),
examples/README.md, src/renpy_mcp_server/server.py, settings.py,
renpy_mcp_app/README.md, renpy_mcp_app/package.json, renpy_mcp_app/CLAUDE.md,
renpy_mcp_app/src/index.ts, plus `git log`/`git ls-files`/`git check-ignore`
surveys and Compare-Object diffs of the four duplicated Python modules.

**Observed:**

1. CONFIG/DOC - `pyproject.toml:3` declares `version = "0.1.0"`; `README.md:5`
   badges `version-4.1.4`; `renpy_mcp_app/package.json:3` declares `1.0.0`.
   Three version claims, one repository, zero tags.
2. CONFIG - `pyproject.toml:30` maps the console script `renpy-mcp-server` to
   `renpy_mcp_server.__main__:main` (the Python server).
3. RUNTIME-ARTIFACT - the untracked local `.mcp.json:9` launches
   `renpy-mcp-server` via `uv`; the owner's live MCP client uses the Python
   surface.
4. HISTORY - `git log`: `a1d6f55` (2026-02-01) "added renpy_mcp_app" arrived
   as ONE commit 3.5 months after the last Python change `0924bcc`
   (2025-10-15); no tags, 4 commits total; the app is 54 of 85 tracked files.
5. CODE - `renpy_mcp_app/src/index.ts:56` creates an MCP server named
   `renpy-studio`; `index.ts:64-69` registers project/asset/script/build tool
   groups plus `view_studio` - the same core tool surface as the Python
   server (server.py:39 list_projects through server.py:855
   stop_web_preview), plus a UI layer.
6. CODE - Compare-Object of the four modules present in both trees:
   image_service.py 349, build_manager.py 542, background_remover.py 245,
   preview_manager.py 243 differing lines - the duplicated Python code has
   already diverged.
7. DOC - README.md:140-171 ("Usage") documents only the Python server's
   tools; the root README contains zero occurrences of `renpy_mcp_app` or
   `renpy-studio`.
8. DOC/CONFIG - workspace model disagreement: `settings.py:37` reads
   `RENPY_MCP_WORKSPACE` (default `cwd/workspace`) vs `CLAUDE.md:52`
   `~/.renpy-studio/workspace/`.
9. TEST - no test directory, no pytest config, no CI; `package.json:16-24`
   scripts contain no `test`; the only test-like file requires a live API
   key (test_nano_banana.py:76).

**Inference:**

- The app was added in a single commit with no statement of relationship or
  migration plan (INFERENCE from HISTORY 4 + absence of any cross-reference).
  The most consistent reading is a product in transition: a new UI-enabled
  surface landed while the old surface remains the configured/installed one.
- The divergent Python copies mean any bug fix or behavior change made since
  Feb 2026 in one tree is not reflected in the other - the two surfaces are
  already behaviorally drifting, not merely duplicated (INFERENCE from CODE 6).
- The 4.1.4 badge with no matching tag and a pyproject at 0.1.0 suggests the
  versioned release lineage lives outside this git history (the Oct 2025
  "Initial commit" + "init commit" pair hints at a history rewrite)
  (INFERENCE from HISTORY 4 + CONFIG/DOC 1).
- A project created under the Python server (workspace root) is invisible to
  the app (`~/.renpy-studio/workspace/`), so the two surfaces cannot even
  share work-in-progress (INFERENCE from DOC/CONFIG 8).

Logic trace: The observed facts (two complete implementations of the same
tool contract, entrypoints, and workspace models; measurable divergence in
the shared modules; a front-door README that documents one surface and a
version identity that cannot be stated) all converge on a single structural
cause: the repository has no declared canonical surface and no declared
relationship between the two implementations. Every other visible issue -
missing tests, missing CI, version drift, duplicate modules - is either a
symptom of that fork or an investment that cannot be correctly placed until
the fork is resolved (tests written for the abandoned surface are waste; a
version bump on the wrong product identity is noise). Therefore the weakest
boundary, and the decision that should come first, is the canonical-surface
decision; the smallest action that resolves it is a one-commit declaration,
not an implementation.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L5
    quote: "[![Version](https://img.shields.io/badge/version-4.1.4-blue.svg)](https://github.com/banjtheman/renpy_mcp_server)"
    supports_claim: "Root README claims version 4.1.4 while pyproject.toml declares 0.1.0; no tags exist - version identity is incoherent."
  - file: pyproject.toml
    lines: L3
    quote: "version = \"0.1.0\""
    supports_claim: "Python package version does not match the README badge (4.1.4)."
  - file: pyproject.toml
    lines: L30
    quote: "renpy-mcp-server = \"renpy_mcp_server.__main__:main\""
    supports_claim: "The declared/installed entrypoint is the Python server."
  - file: .mcp.json
    lines: L9
    quote: "\"renpy-mcp-server\""
    supports_claim: "The owner's live (untracked) MCP client config launches the Python server."
  - file: renpy_mcp_app/package.json
    lines: L2-L3
    quote: "\"name\": \"renpy-studio\",\n  \"version\": \"1.0.0\","
    supports_claim: "The app is a separately published npm package with its own version identity."
  - file: renpy_mcp_app/src/index.ts
    lines: L56
    quote: "name: 'renpy-studio',"
    supports_claim: "The app registers its own MCP server surface under a different name than the Python server."
  - file: renpy_mcp_app/CLAUDE.md
    lines: L52
    quote: "Projects are stored in `~/.renpy-studio/workspace/` with this structure:"
    supports_claim: "The app uses a different workspace root than the Python server (RENPY_MCP_WORKSPACE / cwd/workspace), so the surfaces cannot share projects."
  - file: src/renpy_mcp_server/settings.py
    lines: L37
    quote: "env_value = os.environ.get(\"RENPY_MCP_WORKSPACE\")"
    supports_claim: "Python server resolves its workspace from env/cwd - a different storage model than the app's."
  - file: src/renpy_mcp_server/server.py
    lines: L39
    quote: "async def list_projects() -> dict:"
    supports_claim: "Python server implements the core tool surface that the app reimplements in TypeScript."
  - file: test_nano_banana.py
    lines: L76
    quote: "print(\"❌ GEMINI_API_KEY is not set. Export your key and retry.\")"
    supports_claim: "The only test-like file requires a live paid API key; there is no offline automated test surface."
```

## 9. Why this boundary matters

If the fork is not resolved, the cost compounds on every axis: (a) each bug
fix or feature must be implemented twice or the surfaces silently diverge -
already measurable in the Python module copies (hundreds of differing lines
each); (b) users and AI clients get two different install paths and two
different workspace roots, so work created through one surface is invisible
to the other; (c) the repository cannot state its own version, which blocks
release engineering, issue triage, and changelogs; (d) any validation or CI
investment made now is a bet on which surface survives - a bet the owner has
not yet made. This outranks the other visible issues (missing tests, missing
CI) because those are amplifiers of the fork, not independent problems: tests
written today against the Python server do not cover the app that is 63% of
the tracked files.

## 10. Candidate next steps

1. **Declare the canonical surface (smallest).** One commit in the root
   README stating which surface is the product going forward (or explicitly
   marking the app experimental, or the Python server legacy) and aligning
   the version claim (4.1.4 badge vs pyproject 0.1.0). No code changes
   required.
2. **Cross-surface contract smoke test.** A script asserting both surfaces
   register the same core tool names via MCP `list_tools` - an automated
   drift detector that costs minutes and never needs an API key.
3. **Consolidate the Python pipeline modules** into a single location both
   surfaces import, eliminating the parallel copies (image_service,
   build_manager, background_remover, preview_manager).
4. **Offline unit tests for the deterministic core** (project_manager,
   build_manager path handling, settings resolution) plus a minimal CI runner
   - zero-validation remediation that does not depend on Gemini.
5. **Defer/do-nothing.** Keep both surfaces alive while the app matures -
   credible only with an explicit, time-boxed decision; without one, drift
   compounds silently.

## 11. Recommended next step

Keep the recommendation at the decision level. The decision sharpened by
the evidence is: **determine which implementation is the canonical product
surface** (Python server `src/renpy_mcp_server` vs TypeScript app
`renpy_mcp_app` / `renpy-studio`). The cheapest discriminator for that
decision is the owner's product intent: does `renpy_mcp_app` / `renpy-studio`
supersede, coexist with, or remain secondary to the Python MCP server?
Only after that decision is made should the follow-through happen: a
one-commit README declaration of the canonical surface plus
version/installation identity alignment (badge 4.1.4 vs pyproject 0.1.0 vs
package.json 1.0.0). No code change is required for either step; the
declaration takes minutes and makes every subsequent engineering decision
(tests, CI, features, release process) placeable. Any larger investment
before the decision risks landing on the surface being abandoned.

## 12. Recommended workflow

`architecture-implementation-workflow` from workflow-registry.yaml (fits
architecture/refactoring problems), executed in `plan_only` mode: the
immediate deliverable is the decision (which surface is canonical); the
declaration commit is follow-through, not implementation.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: experiments/product-interaction-p4-v1/charter-v1.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "README.md (line 5): version badge 4.1.4 vs pyproject.toml 0.1.0 vs package.json 1.0.0 - no coherent version identity"
  - "pyproject.toml (line 30): declared entrypoint is the Python server renpy_mcp_server.__main__:main"
  - ".mcp.json (line 9): owner's live MCP config launches the Python server"
  - "git log a1d6f55 (2026-02-01): 'added renpy_mcp_app' - whole app landed in one commit, 3.5 months after last Python change; 4 commits, no tags"
  - "renpy_mcp_app/src/index.ts (line 56): MCP server named renpy-studio; lines 64-69 register the same tool groups plus view_studio"
  - "Compare-Object src/renpy_mcp_server vs renpy_mcp_app/python: image_service 349, build_manager 542, background_remover 245, preview_manager 243 differing lines"
  - "README.md (lines 140-171): usage documents only the Python server; zero mentions of renpy_mcp_app or renpy-studio in root README"
  - "settings.py (line 37) vs renpy_mcp_app/CLAUDE.md (line 52): different workspace roots (RENPY_MCP_WORKSPACE/cwd vs ~/.renpy-studio/workspace)"
  - "package.json (lines 16-24): no test script; no test dir, no pytest, no CI; test_nano_banana.py (line 76) requires live GEMINI_API_KEY"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: plan_only
weakest_boundary: two parallel implementations of the same MCP product surface (Python server src/renpy_mcp_server vs TypeScript app renpy_mcp_app published as renpy-studio) with no declared canonical surface; shared Python modules already diverged by hundreds of lines
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-08T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

"Plan (do not implement) a decision record for renpy_mcp_server. The
decision to sharpen: which implementation is the canonical product surface -
the Python server `src/renpy_mcp_server` (currently the
configured/installed entrypoint) or the TypeScript app `renpy_mcp_app`
(published as renpy-studio, 63% of tracked files)? State the cheapest
discriminator (owner intent: supersede / coexist / secondary) and the
follow-through that happens only after the decision: a README declaration of
the canonical surface, alignment of the version claim across README badge,
pyproject.toml, and package.json, and a note on how the two workspace roots
relate. Do not change code and do not presume the decision. Output: the
decision framing and the exact file diff plan for the follow-through."
