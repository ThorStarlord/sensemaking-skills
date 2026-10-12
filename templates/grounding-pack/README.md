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

- **Provenance.** Every factual line ends with exactly one tag: `[code: path]`, `[test: path]`, `[owner: YYYY-MM-DD or link]`, or `[hypothesis]`. A `[hypothesis]` line never justifies an action alone.
- **Inclusion.** Write a line only if an agent could not recover it from the code in a few minutes. If a rule can be enforced by a test, type, or lint, write that and cite it.
- **Budgets are hard.** Over budget: cut or merge lines. Do not add files.
- **Ratchet.** Before asking the owner, check `intent.md` (open questions and answered questions) and `decisions/`. After an answer, record it in `intent.md` with an `[owner: date]` tag in the same change.
- **Staleness.** A change that alters behavior covered by a line updates that line in the same change.
