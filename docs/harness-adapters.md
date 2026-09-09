# Coding-agent harness adapters

**Status:** P10 product contract  
**Scope:** explicit Skill discovery-root setup for Claude Code, Codex, OpenCode, portable Agent Skills, and custom environments

## Purpose

P10 makes the packaged Sensemaking Skills easier to install into coding-agent environments without placing harness-specific semantics inside the Sensemaking Campaign core.

The product question is deliberately narrow:

> Given an explicitly selected harness and scope, where should the exact packaged Skill trees be copied?

P10 does **not** answer:

> Which harness is currently running, which Skill should be used, or what should the Campaign do next?

## Product surface

```text
sensemaking-skills setup-skills \
  --target agents|generic|claude|codex|opencode|claude-superpowers|all|custom \
  [--scope user|project] \
  [--project-root <repo>] \
  [--skills-dir <custom-root>] \
  [--dry-run] \
  [--force]
```

The caller chooses the adapter explicitly. P10 performs **no active-harness auto-detection**.

## Canonical adapter table

| Target | User/global discovery root | Project discovery root | Notes |
|---|---|---|---|
| `generic` | `~/.agents/skills` | `<project>/.agents/skills` | Portable Agent Skills root. |
| `agents` | same as `generic` | same as `generic` | Backward-compatible alias for the pre-P10 default target. |
| `claude` | `~/.claude/skills` | `<project>/.claude/skills` | Claude Code personal/project Skill roots. |
| `codex` | `$CODEX_HOME/skills`, default `~/.codex/skills` | `<project>/.agents/skills` | Personal Codex home and repository Agent Skills discovery are intentionally different. |
| `opencode` | `~/.config/opencode/skills` | `<project>/.opencode/skills` | Native OpenCode roots. OpenCode also supports Claude/Agent-compatible roots, but the explicit `opencode` adapter uses its native locations. |
| `claude-superpowers` | historical Superpowers plugin-cache path | unsupported | Compatibility target retained from before P10; not the first-class Claude adapter. |
| `custom` | exact `--skills-dir` | n/a | Caller supplies the complete destination explicitly. |

The paths above are setup metadata, not runtime proof that a harness has loaded the Skill.

## Upstream evidence boundary

The P10 adapter paths were checked against current upstream harness documentation/source on 2026-09-08:

- Claude Code repository documentation already used by this repository describes `~/.claude/skills` and `.claude/skills` discovery.
- Codex's current bundled `skill-creator` / `skill-installer` uses `$CODEX_HOME/skills` (default `~/.codex/skills`) for personal Skills, while current Codex project-skill tests exercise `.agents/skills` below the repository working directory.
- OpenCode documents native `.opencode/skills` / `~/.config/opencode/skills` roots and compatibility discovery from `.claude/skills` and `.agents/skills`.

These are versioned product assumptions. If an upstream harness changes its discovery contract, P10 should be updated and requalified explicitly. The runtime must not silently probe alternative roots and call the result authoritative.

## Explicit scope

### User scope

Default:

```text
--scope user
```

The adapter resolves its declared personal/global root.

Codex additionally honors an explicitly configured `CODEX_HOME` environment variable:

```text
CODEX_HOME=/custom/codex
→ /custom/codex/skills
```

Reading `CODEX_HOME` is configuration resolution, not active-harness detection.

### Project scope

```text
--scope project --project-root /path/to/repository
```

Project scope requires an existing explicit project directory. P10 does not infer the project root from the current process, git state, an editor, or a running harness.

This is intentional:

```text
explicit project root
!= guessed current repository
```

## `all` behavior

`--target all` expands the canonical P10 adapters in deterministic order and writes each unique physical destination once.

At project scope:

```text
generic -> .agents/skills
codex   -> .agents/skills
```

share one root, so P10 preserves both logical adapter identities while copying the Skill tree only once.

At user scope, generic and Codex have distinct roots:

```text
~/.agents/skills
~/.codex/skills  (or $CODEX_HOME/skills)
```

The historical user-scope `claude-superpowers` cache is also retained as a compatibility superset of the old `all` behavior. Project-scope `all` never invents a project-local Superpowers cache.

## Exact Skill-tree copying

P10 reuses the pre-existing packaged Skill distribution contract:

```text
repository skills/
→ wheel build packages exact Skill trees
→ setup-skills resolves packaged skill_trees
→ explicit harness adapter resolves destination
→ complete Skill directory copied
```

A Skill is a directory, not only `SKILL.md`. References, scripts, assets, and other files within the packaged tree are copied with it.

## Drift behavior

Existing drift protection remains authoritative.

For each destination Skill tree:

```text
missing
→ copy

current byte-for-byte
→ no-op success

different
→ fail/report drift
→ do not overwrite
```

Replacement requires explicit:

```text
--force
```

Therefore:

```text
harness adapter convenience
!= permission to overwrite local Skill modifications
```

## Dry-run behavior

`--dry-run` resolves and reports the same explicit target/scope paths but must not create destination directories or modify Skill files.

## Compatibility surfaces

P10 preserves the earlier setup entry points:

```text
--target agents
--target claude-superpowers
--target all
--target custom --skills-dir ...
```

`agents` is now an explicit alias for the canonical `generic` adapter.

`claude-superpowers` remains a historical compatibility target. It is deliberately not conflated with the first-class Claude Code adapter:

```text
claude
→ ~/.claude/skills or <project>/.claude/skills

claude-superpowers
→ historical plugin cache
```

## Semantic-control boundary

Harness setup is deterministic packaging/distribution machinery.

The adapter may establish:

- which harness target the caller explicitly named;
- which scope the caller explicitly named;
- the declared filesystem destination for that target/scope;
- whether the packaged Skill tree matches the installed copy;
- whether copying/replacement succeeded mechanically.

The adapter may **not** establish:

- that the harness actually discovered or loaded the Skill;
- that the Skill is available in the current model context;
- that a responsibility is warranted;
- that a particular Skill should be selected;
- that execution is authorized;
- that the Campaign should advance, defer, close, or mutate in any way.

The durable claim ceiling is:

```text
copied to declared discovery root
!= harness observed Skill
!= Skill selected
!= execution authorized
!= Campaign decision
```

## Relationship to Campaign milestones

P10 is outside the Campaign semantic core.

It does not modify:

- `CampaignState`;
- `Responsibility`;
- `Authority`;
- `TransitionRecord`;
- P2 lifecycle transactions/recovery;
- P4 artifact admission;
- P5 agent-authored decisions;
- P6 capability-selection boundaries;
- P7 handoff/resume;
- P8 lineage;
- P9 reconciliation lifecycle.

A harness-specific filesystem path must never leak into those semantic contracts as a decision rule.

## Qualification expectations

A qualified P10 candidate must prove at least:

1. `agents` remains a compatibility alias for the portable `generic` adapter;
2. Claude user/project paths resolve to `.claude/skills` under the explicit scope root;
3. Codex user scope resolves through `$CODEX_HOME/skills` with `~/.codex/skills` as the default, while project scope resolves to `.agents/skills`;
4. OpenCode user/project paths resolve to its native `~/.config/opencode/skills` and `.opencode/skills` roots;
5. project scope fails closed without an explicit existing project root;
6. unknown target/scope combinations fail closed;
7. `all` deduplicates shared project roots deterministically;
8. exact complete packaged Skill trees are copied;
9. divergent installed copies are never overwritten without `--force`;
10. dry-run creates no destination state;
11. setup creates no Campaign state and emits no Skill selection, execution authority, semantic score, or next-action decision;
12. existing `agents`, `custom`, `claude-superpowers`, and user-scope `all` compatibility behavior remains available;
13. a fresh installed wheel exposes the P10 CLI and can install Claude, Codex, and OpenCode project Skills from a working directory outside the source checkout.
