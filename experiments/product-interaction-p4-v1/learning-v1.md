# P4 — Learning

record: learning-v1
produced_from: P4 documentation-light transfer probe (renpy_mcp_server)

## Disposition

**STRONG_SHARPENING**

The owner judged the recommendation clearly useful, reported that it
established a direction (rather than confirming an existing one), identified
the decision-changing content as the dual-implementation discovery and the
drift evidence, and rated the grounding as solidly evidence-based. There was
no prior inclination at baseline (NO CLEAR PRE INCLINATION), so this is a
direction-establishing outcome, not confirmation.

## Confidence update

**Question:** "What did P4 change about our confidence that repo-sensemaker's
decision-sharpening value survives documentation-light repositories?"

**Answer: STRENGTHENED**

Explanation: The target was genuinely documentation-light — exactly 5
**tracked** Markdown files (README.md, CONTRIBUTING.md, examples/README.md,
renpy_mcp_app/README.md, renpy_mcp_app/CLAUDE.md; see the documentation-count
reconciliation below), zero ADRs, zero design docs, zero CONTEXT/AGENTS, no
changelog, no tags, no CI. The only narrative was a marketing-style README. Despite that, the
investigation identified a consequential engineering decision boundary (two
parallel implementations of the same MCP product with no declared canonical
surface) and supported it with hard, non-narrative evidence: git history (the
entire app landed in one commit 3.5 months after the last Python change),
configuration (entrypoint vs live client config vs npm package identity),
code comparison (245-542 differing lines in the four copied Python modules),
and workspace-model disagreement. The owner then judged the output clearly
useful and direction-establishing. P4 therefore transfers the P1-P3
decision-sharpening signal to a documentation-light repository, with the
important nuance that the value came from exactly the evidence classes the
hypothesis named: code, tests-absence, configuration, history, and
runtime/product surfaces — not narrative.

Caveats that bound the strengthening: (a) ASSISTED_BASELINE — no independent
PRE capture, so no clean PRE->POST delta is claimable; (b) n=1 on a small
repository (85 tracked files), so transfer to a large doc-light codebase is
untested; (c) the boundary found was structural and highly visible to
read-only code analysis — a doc-light repo whose consequential boundary is
buried in runtime behavior or external integrations might yield weaker
sharpening; (d) the owner is the author of the repo, so familiarity may
inflate perceived usefulness (though it also means the "establish a
direction" outcome was not cheap confirmation of an unknown).

## Preferred product interaction shape

**Autonomous investigation -> recommendation** (primary evidence), with the
one-targeted-question variant recorded as a refinement, not a prerequisite.

Explanation: the recommendation was judged useful and direction-establishing
WITHOUT asking the owner any question — the recommendation was deliberately
shaped to be intent-independent ("which surface" vs "that the fork must be
declared"). The one targeted owner question identified in the synthesis ("Is
renpy_mcp_app the intended future product surface?") would sharpen the
recommendation's content but was not needed for its usefulness. This is
evidence for autonomous-first interaction, with the targeted question as an
optional second turn when the recommendation's content would change
materially under one answer vs the other. Unresolved as a general rule
(n=1); no interaction was implemented.

## Validation record

**Total: two validation runs.** (1) The original canonical run on the
unrevised brief: `valid: true` with one non-blocking warning
(WEAKNESS_TYPE_UNKNOWN for `Contract Mismatch`). (2) A second, explicitly
owner-authorized run after the post-run wording refinements (decision-level
recommendation framing): `valid: true`, same non-blocking warning. The
second run replaced the stored `validation-result-v1.json`; the first run
remains preserved in this narrative. Future summaries should say "two
validation runs, second explicitly owner-authorized after review
refinements", not "validated exactly once".

The warning is an operator-invocation artifact: `--repo-root`
pointed at the target repository, which contains no `weakness-types.md`, so
the validator's taxonomy list loaded empty; `Contract Mismatch` is one of
the canonical seven types in
`skills/repo-sensemaker/references/weakness-types.md`. No repair and no
rerun of the failed path — both runs passed. Validation success is not the
product-value outcome.

## Was owner context necessary?

Partially, but minimally: product intent (which surface is the future
product) is not inferable from repository evidence and was recorded as the
one targeted owner question. However, the actionable recommendation was
intent-independent and delivered value without it — so owner context was
recorded as a refinement input, not a blocking prerequisite.

**Strengthened learning statement (owner review, 2026-08-08):** repository
evidence was sufficient to identify the consequential boundary, but owner
intent may still be required to resolve that boundary. P4 therefore shows a
healthy agent behavior: discover the boundary autonomously, keep the
recommendation at the decision level, and treat the owner-intent question as
the cheapest discriminator rather than making a product-intent choice from
repository evidence alone.

## Strongest positive learning

In a documentation-light repository, the decision-sharpening value shifted
entirely to non-narrative evidence classes: git history (single-commit
arrival of a parallel implementation), configuration identity (entrypoint,
live client config, npm package), and measurable code divergence
(245-542 differing lines in copied modules). The owner's own POST named
exactly these two findings as decision-changing. Sparse docs did not
prevent identifying the consequential boundary — the repo's structure and
history carried the diagnosis.

**The most interesting P4 learning (owner review):** repository evidence may
be sufficient to DISCOVER the decision boundary without being sufficient to
RESOLVE product intent. That separates two roles cleanly: the agent's job is
discovery plus a bounded recommendation; the owner's intent remains the
discriminator when the boundary is intent-dependent. This observation
motivates the investigation -> one high-information owner question ->
recommendation interaction shape, and it holds independently of the
validation result.

## Strongest limitation

The probe cannot distinguish "repo-sensemaker sharpened the decision" from
"the owner had never explicitly framed a fork they were implicitly managing".
With an ASSISTED_BASELINE and no POST-time PRE reconstruction, the
direction-establishing claim rests on the owner's report that no direction
existed. Additionally, n=1 on a small, structurally transparent repo means
transfer to large or behavior-buried documentation-light repositories is
unestablished.

## Frozen identities (end state)

- Target: renpy_mcp_server @ `a1d6f55af5716a50a8674302466b385711ef513f`,
  working tree clean at freeze; not modified by P4.
- Canonical sensemaking-skills: `27aa2442e5395f8793023882d5ed5e94861755e4`
  (unrelated modified `src/sensemaking_skills.egg-info/PKG-INFO` and
  untracked `.reasonix/` present).
- Canonical repo-sensemaker SKILL.md: `skills/repo-sensemaker/SKILL.md`,
  blob `a5cb5dd71fd75adeb879780b9dc47020cecd5ab3`, used exactly once.
- Owner question: "What engineering work would create the most value next?"
- Execution mode: agent-native, one-shot, read-only.
- Timestamp: 2026-08-08.

## Recommendation (carried forward, not implemented)

Decision level: determine which implementation is the canonical product
surface (Python server vs TypeScript app / renpy-studio). Cheapest
discriminator: resolve whether renpy_mcp_app / renpy-studio is intended to
supersede, coexist with, or remain secondary to the Python MCP server.
Only after that: one-commit README declaration of the canonical surface +
version/installation identity alignment. No implementation was performed
per P4 hard stop.

## Documentation-count reconciliation (owner review, refinement 2)

The evidence package used two different counting scopes for "markdown
files"; both are correct, and the distinction is now made explicit:

- **Selection-time scan (charter freeze):** "~8.5k code files, ~30 markdown
  files, 0 ADRs" came from a workspace-level recursive scan that included
  the untracked local `.venv/` directory (25 of the 30 .md files live under
  `.venv/`; 8,525 of the ~8.5k code files are `.py` files under `.venv/`
  site-packages). This scan described the broader tree, not the product
  surface.
- **Tracked product surface (investigation):** `git ls-files` shows 85
  tracked files, of which exactly **5 are Markdown** (README.md,
  CONTRIBUTING.md, examples/README.md, renpy_mcp_app/README.md,
  renpy_mcp_app/CLAUDE.md) and **39 are code files** (.py/.ts/.js). The
  "only 5 markdown files" claim refers to this tracked scope.
- **Both scopes agree on the experimental variable:** zero ADR-style
  decision records exist in either scope, so the documentation-light
  characterization is unaffected by the counting difference.

## Owner review (post-run, 2026-08-08) and P-series status

Owner review of the P4 evidence package:
- **P4 accepted** as STRONG_SHARPENING; documentation-light transfer
  STRENGTHENED (confirmed, not revised).
- Refinement 1 applied: recommendation kept at the decision level (see
  owner-synthesis-v1.md section 1 and investigation section 11); the
  learning statement "repository evidence was sufficient to identify the
  consequential boundary, but owner intent may still be required to resolve
  that boundary" is now recorded.
- Refinement 2 applied: documentation-count scopes reconciled (see above).
- The investigation brief was revised per owner review and re-validated
  once (run 2); validation-result-v1.json reflects the revised artifact.
  The original run (valid: true) is preserved in the narrative above.
- **P-series closed by owner disposition: no P5.** The owner judges that
  P1-P4 have accumulated sufficient qualitative value evidence
  (decision-sharpening capability is credible); further value-validation
  cases have diminishing returns.
- **Task S1 (Owner Interaction Shape Probe) proposed by the owner** —
  compare 2-3 interaction shapes (autonomous / investigate-then-clarify /
  decision-alternatives) on one real repository decision, asking which
  interaction yields most decision value for least cognitive burden.
  Recorded here as the agreed next direction; NOT started (no separate
  authorization, and S1 is a new experiment, not a P-series task).

## Exact file scope

experiments/product-interaction-p4-v1/: charter-v1.md,
assisted-baseline-v1.md, repo-sensemaker-investigation-v1.md,
owner-synthesis-v1.md, owner-post-v1.md, learning-v1.md,
validation-result-v1.json.
