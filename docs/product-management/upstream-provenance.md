# PM methodology upstream provenance

## Pinned source

- Repository: `lucasgaravelli/pm-skills-claude-code`
- Default branch at import: `master`
- Pinned commit: `21cbb2903d740d10fc65c667aea97d3ee8657349`
- Commit date: 2026-04-23
- Commit subject: `feat: initial release — 27 PM skills for Claude Code`
- License: MIT
- Copyright notice: `Copyright (c) 2026 Flowgrammers`

The pinned commit is immutable provenance. Later upstream changes do not silently alter Sensemaking behavior.

## Imported source surface

The methodological source consists of the 27 command files under `.claude/commands/`:

`persona`, `discovery`, `interview-synthesis`, `competitive-analysis`, `opportunity-tree`, `hypothesis`, `customer-journey`, `prd`, `user-stories`, `acceptance-criteria`, `prioritize`, `strategy`, `roadmap`, `okr`, `lean-canvas`, `pricing`, `north-star`, `experiment-design`, `measure-pmf`, `ab-test-analysis`, `pre-mortem`, `launch-checklist`, `release-notes`, `stakeholder-update`, `gtm`, `battlecard`, and `ideal-customer-profile`.

The upstream tutorials and templates may be consulted as methodology references, but they are not runtime dependencies.

## Adaptation policy

Sensemaking preserves useful methodology while removing source-runtime coupling. In particular, adaptations may remove or rewrite:

- `/command` invocation syntax;
- `$ARGUMENTS` tokens;
- `~/.claude/commands` installation assumptions;
- copy/paste chaining instructions;
- Claude-specific session or tool assumptions;
- output prose that conflates hypothesis with verified evidence.

The adapted capability may also split long source prompts into a concise `SKILL.md` plus progressive references.

## Independent evolution

After initial adaptation, the Sensemaking version is a separate product capability. Future upstream changes require deliberate review. The migration ledger records whether each source is `ADOPT`, `ADAPT`, `MERGE`, `SUPERSEDE`, `DEFER`, or `REJECT`.

The upstream count of 27 is provenance, not product doctrine.

## License handling

The upstream MIT notice must remain attributable wherever substantial upstream text is copied. The preferred adaptation style is methodological paraphrase plus an explicit provenance reference rather than wholesale duplication of worked examples.
