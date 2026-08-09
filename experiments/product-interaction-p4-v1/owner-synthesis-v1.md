# P4 — Owner synthesis (renpy_mcp_server)

record: owner-synthesis-v1
produced_from: repo-sensemaker-investigation-v1 (canonical, read-only)
owner_question: "What engineering work would create the most value next?"

---

## 1. Recommended action (decision level)

**Decision sharpened: determine which implementation is the canonical product
surface.** Your repository contains two full implementations of the same MCP
product — the Python server (`src/renpy_mcp_server/`, what your live
`.mcp.json` launches and the README documents) and the TypeScript app
(`renpy_mcp_app/`, npm package `renpy-studio`, 63% of tracked files, added in
one commit on 2026-02-01). The recommendation is the decision itself, not the
documentation follow-through.

**Cheapest discriminator:** resolve whether `renpy_mcp_app` / `renpy-studio`
is intended to supersede, coexist with, or remain secondary to the Python MCP
server.

**Only after that:** document the canonical surface in the root README and
align version/installation identity (badge, pyproject, package.json). No code
changes are required for any of this.

## 2. Why this matters now

The two implementations have already started to drift: the Python modules
copied into `renpy_mcp_app/python/` differ from their `src/` counterparts by
245–542 lines each, and the surfaces disagree on fundamentals — install path
(`uv run renpy-mcp-server` vs `npx renpy-studio --stdio`), workspace root
(`RENPY_MCP_WORKSPACE`/cwd vs `~/.renpy-studio/workspace/`), and version
identity (README badge 4.1.4 vs pyproject 0.1.0 vs package.json 1.0.0). Every
week of delay doubles the cost: each fix must be made twice, projects are
invisible across the two surfaces, and any test/CI investment is a bet on an
undeclared survivor. The repo is small (85 tracked files) — this decision is
cheap now and compounds if deferred.

## 3. Strongest evidence

- `pyproject.toml:30` declares the Python server as the entrypoint; the
  untracked `.mcp.json:9` on this machine launches it — the surface you
  actually use. (CONFIG / RUNTIME-ARTIFACT)
- `git log`: `a1d6f55` (2026-02-01) "added renpy_mcp_app" landed the entire
  app in one commit, 3.5 months after the last Python change, with no
  statement of relationship anywhere. (HISTORY)
- Compare-Object of the four shared Python modules: 349 / 542 / 245 / 243
  differing lines — divergence is measurable today, not hypothetical. (CODE)
- Root README (README.md:140-171) documents only the Python server; zero
  mentions of `renpy_mcp_app`/`renpy-studio` anywhere in it. (DOC)

## 4. Strongest credible alternative

**Defer/do-nothing while the app matures** — keep both surfaces alive until
`renpy-studio` proves out. This is credible only if you make it an explicit,
time-boxed decision (e.g. "revisit at the app's next milestone"); as an
unspoken state it is exactly the drift trap the evidence already shows
beginning. The cheaper version of the same bet: declare the app
"experimental" in the README and keep the Python server canonical — that is
the recommended action with a label attached.

## 5. Most important uncertainty

**Product intent: is the TypeScript app the future of the product, or a
separate/experimental surface?** This is not inferable from repository
evidence — nothing in the repo states it. The recommendation is deliberately
stack-independent: whichever way you answer, the declaration commit is the
same shape; only the label changes.

## 6. Cheapest credible next move

Answer the discriminator — one question, no code: "Does renpy-studio
supersede, coexist with, or remain secondary to the Python server?" — then
land the one-commit declaration (a short "Canonical surface" section in the
README + version alignment). ~15 minutes, zero code risk, and it makes every
later decision (tests, CI, features, releases) placeable.

## 7. Confidence and why bounded

Medium-high on the diagnosis: the dual-implementation facts are directly
observed (files, diffs, git history, config), not inferred. Confidence is
bounded on the recommendation's content — the repo cannot tell us which
surface should win, only that the fork must be declared. The "why now"
(mesurable drift) is evidence-backed; the direction choice is the owner's.

## 8. What repository evidence cannot establish

- Which surface is the intended future product (owner product intent).
- Whether `renpy-studio` was published/used in the wild (no npm telemetry in
  the repo; the 4.1.4 badge hints at a release lineage outside this git
  history).
- Whether the app's UI is actually desired by users vs. a build-ahead.
- Why the repo history was re-created ("Initial commit" + "init commit"
  pair) — irrelevant to the recommendation, noted for completeness.

**One targeted owner question would materially improve the decision:** "Is
`renpy_mcp_app`/`renpy-studio` the intended future product surface
(replacing the Python server), a parallel product, or an experiment?"
Per P4 protocol this question is recorded here as product-learning evidence
and was NOT asked or acted on in this run.

**Strengthened learning statement (owner review, 2026-08-08):** repository
evidence was sufficient to identify the consequential boundary, but owner
intent may still be required to resolve that boundary. The recommendation is
therefore kept at the decision level: determine the canonical surface; the
intent question is the cheapest discriminator, not a step the repository can
perform.
