# Grounding Pack template

Copy this directory to `.sensemaking/` in a target repository. Reuse an existing `CONTEXT.md`, `docs/adr/`, or `CLAUDE.md` instead of duplicating it; link to it from the pack.

Files and hard budgets:

| File | Budget |
| --- | --- |
| `intent.md` | 800 words |
| `context.md` | 800 words |
| `invariants.md` | 600 words |
| `decisions/NNNN-title.md` | 250 words each |

Rules:

- **Provenance.** Every factual line carries exactly one primary tag: `[policy: path]` (authority document), `[code: path]` (source file), `[test: path]`, `[owner: YYYY-MM-DD]` (owner intent), `[delegated: YYYY-MM-DD]` (agent choice under delegation), or `[hypothesis]` (agent inference). Supporting sources go in a Markdown link, not a second tag. A `[hypothesis]` never justifies an action alone.
- **Inclusion.** Write a line only if an agent could not recover it from the code in a few minutes. If a rule can be enforced by a test, type, or lint, write that and cite it.
- **Budgets are hard.** Over budget: cut or merge lines. Do not add files.
- **Ratchet.** Before asking the owner, check `intent.md` and `decisions/`. Reuse a recorded answer while it still applies to the current scope. Ask again only if the scope changed, the decision was superseded, or new evidence materially challenges it. Record each answer with its date in the same change.
- **Staleness.** A change that alters behavior covered by a line updates that line in the same change.
