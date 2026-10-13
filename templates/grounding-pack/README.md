# Grounding Pack template

Use this template **only when persistent, target-specific knowledge would
improve a consequential decision or avoid repeating a real owner question**.
It is not a mandatory preflight artifact. When warranted, copy only the needed
parts to `.sensemaking/` in the target repository. Reuse an existing
`CONTEXT.md`, `AGENTS.md`, `docs/adr/`, or `CLAUDE.md` by linking to it
instead of duplicating it; avoid empty files and exhaustive ontologies.

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
- **Staleness.** A change that alters behavior covered by a line updates that line in the same change. Verify the **content** of a consequential cited claim; a file existing does not establish that the claim is correct. Markdown links resolve relative to `.sensemaking/` (e.g. `../specification/...`), whereas provenance tags describe paths relative to the repository root.
- **Use.** Retrieve only what matters to the active goal. For a clear authorized change, code directly. After consequential work, update only durable, non-derivable learning; do not summarize every file or commit.
- **Evidence and authority.** Source code shows observed behavior; product/owner decisions show intended behavior. A mismatch is a question to resolve, not permission to delete either. The pack does not create owner, merge, release, or deployment authority.
