---
id: using-sensemaking-bootstrap
trigger: session-start
note: "descriptive only -- no executable Claude Code hook is configured in this repository (.claude/settings.json is {}); see docs/decision-orchestration-boundary.md, section 'Deterministic machinery and hooks'"
description: Load sensemaking-skills bootstrap skill for agent-native orchestration
platform: ["Claude Code", "Cursor (planned)", "OpenCode (planned)"]
---

# SessionStart: Load Sensemaking Bootstrap Skill

When a session starts in this repository, the **using-sensemaking** bootstrap skill becomes available to agents.

## SessionStart Bootstrap Reminder

This file describes the reminder below; no hook executes it. Nothing runs at
session start in this repository (`.claude/settings.json` is `{}`). The
reminder reaches agents through `CLAUDE.md` (its "SessionStart hook" section)
and through the installed `using-sensemaking` skill. Disposition:
`docs/decision-orchestration-boundary.md`, section "Deterministic machinery
and hooks".

---

**sensemaking-skills Bootstrap Available**

Before using sensemaking-skills in a repository, read the bootstrap skill:

```
/skill using-sensemaking
```

**Or read directly:**
```
skills/using-sensemaking/SKILL.md
```

This skill teaches (section numbers refer to `skills/using-sensemaking/SKILL.md`):
- When repository sensemaking is warranted, and when it is not (section 2)
- Select responsibility before Skill (section 5)
- How to read a Repository Sensemaking Brief; `recommended_workflow_id` is a
  recommendation/planning field, not execution authority (section 6)
- Validate mechanically without confusing PASS with truth or closure (section 9)
- Reconcile material work claims; verify repairs against the original finding
  (sections 10-11)
- Authority: KNOW vs. DECIDE vs. ACT vs. PUBLISH (section 12)
- Continue, stop, or escalate (section 13); durable continuation (section 14)

**Then**, when a request arrives:
1. Decide whether repository sensemaking is warranted (section 2); if not, do bounded work
2. If warranted, produce the `repository_sensemaking_brief` with `repo-sensemaker` and validate it mechanically (section 9)
3. Read the brief (section 6): fog type is diagnostic metadata; `recommended_workflow_id` does not authorize execution
4. Select the next responsibility before any Skill, workflow, or patch (section 5)
5. Continue, stop, or escalate (section 13); a validator PASS is not closure

---

## How Agents Use This Skill

### Invoke via Skill Tool
```
User: "Diagnose my codebase"
Agent: [reads using-sensemaking skill via /skill using-sensemaking]
Agent: [decides whether repository sensemaking is warranted -- section 2]
Agent: [if so, invokes repo-sensemaker; then selects responsibility before Skill -- section 5]
```

### Direct File Read
Agents can read the skill file directly:
```
Skill file: skills/using-sensemaking/SKILL.md
Agent: [parses YAML metadata + Markdown teaching content]
Agent: [applies the operating loop: warrant -> responsibility -> capability]
Agent: [invokes repo-sensemaker only when warranted]
```

### No Passive Loading

The reminder is **descriptive** -- it tells agents to read the skill before starting; nothing loads it automatically. It does NOT:
- Automatically run diagnosis
- Parse the codebase
- Invoke workflows
- Validate artifacts

Those are agent responsibilities, taught by the skill.

## What This Hook Does

1. **Describes a convention** -- read `using-sensemaking` before using the skills; this file does not register anything
2. **Surfaces availability** -- via `CLAUDE.md` and the installed skill, agents know the skill exists and can invoke it
3. **Does NOT inspect the repo** -- nothing runs fog classification at session start
4. **Does NOT orchestrate** -- nothing invokes workflows or validates artifacts at session start

## Platform Status

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Described (no executable hook) | Primary platform; the skill is reached via the Skill tool from an installed skills directory, or by direct file read |
| Cursor | Planned | No hook mechanism exists to port; the same file-based convention applies |
| OpenCode | Planned | No hook mechanism exists to port; the same file-based convention applies |
| CLI | Compatibility | CLI can import skill and parse artifacts, but uses skill-led orchestration |

No row describes an executable hook. On every platform the bootstrap is reached by reading the skill file, directly or from an installed skills directory.

## Testing This Hook

### Test 1: Skill is discoverable
```bash
# In Claude Code, verify you can invoke the skill:
# → Open chat
# → Ask: "Can you help me understand sensemaking-skills?"
# → Use Skill tool: /skill using-sensemaking
# → Verify skill content loads
```

### Test 2: Skill content is current
```bash
# Verify the skill file exists and has metadata:
ls -la skills/using-sensemaking/SKILL.md

# Check the file has correct metadata:
head -10 skills/using-sensemaking/SKILL.md
# Should show: name: using-sensemaking, description, tags
```

### Test 3: Skill teaches correct behavior
```bash
# Verify the skill teaches responsibility before Skill (section 5):
grep -n "Select responsibility before Skill" skills/using-sensemaking/SKILL.md

# Verify the skill separates validation from closure (section 9):
grep -n "!= closure" skills/using-sensemaking/SKILL.md

# Verify the skill treats recommended_workflow_id as a recommendation, not execution authority (section 6):
grep -n "recommendation/planning field" skills/using-sensemaking/SKILL.md
```

### Test 4: Hook doesn't orchestrate
```bash
# Verify the hook file does NOT contain:
grep -v "Do NOT.*inspect\|Do NOT.*orchestrate" .claude/hooks/sessionstart.md
# Should find the "What This Hook Does" section showing NO orchestration
```

## How the Bootstrap Is Discovered

**Method: file-based discovery; nothing is injected at session start**

1. **Claude Code**:
   - No hook is configured: `.claude/settings.json` is `{}`; this file is a description
   - `CLAUDE.md` ("SessionStart hook" section) names the skill and points here
   - The skill tree is copied into an agent-discoverable skills directory (`~/.claude/skills` per `INSTALLATION.md`; `~/.agents/skills` or the Superpowers plugin cache per `src/sensemaking_skills/setup_skills.py`, which never silently overwrites an installed copy); `scripts/probe_skill_distribution.py` reports drift between `skills/<skill>/` and the installed copy
   - Agent invokes via `/skill using-sensemaking` or the Skill tool, or reads `skills/using-sensemaking/SKILL.md` directly
   - Skill content is loaded from a file; the repository copy and an installed copy can drift (see the distribution probe)

2. **Cursor/OpenCode**:
   - No hook mechanism exists to port; the same file-based convention applies
   - Skill file location remains the same
   - Agent invocation method may vary

## Constraints & Limitations

### Intentional Constraints

- **Scope of this file**: description of skill availability only
  - YES: describes/surfaces the skill
  - NO: does NOT inspect the repo
  - NO: does NOT classify fog
  - NO: does NOT invoke workflows
  - NO: does NOT validate artifacts
  - NO: does NOT execute anything (no hook is configured)

- **Skill responsibility**: the bootstrap skill teaches the agent-native control loop
  - Skill tells agents WHEN repository sensemaking is warranted (section 2)
  - Skill tells agents to select responsibility before Skill (section 5)
  - Skill tells agents HOW to read the brief; `recommended_workflow_id` is not execution authority (section 6)
  - Skill tells agents HOW to validate mechanically without treating PASS as closure (section 9)
  - Skill tells agents WHEN to continue, stop, or escalate (section 13)
  - Agent decides whether to follow these rules (they're not enforced)

### Platform Limitations

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| No executable hook | Nothing runs at session start; an agent that does not read `CLAUDE.md` will not see the reminder | `CLAUDE.md` names the skill; the installed skill is discoverable via the Skill tool |
| Installed-copy drift | The installed skill copy may lag the repository copy | `scripts/probe_skill_distribution.py` reports drift; `setup_skills.py --force` or the probe's `--sync` replaces it explicitly |
| Cursor/OpenCode | No hook exists on any platform | Same file-based convention: read the skill file |
| File path availability | Must be relative to repo root | `.claude/` and `skills/` directories standard |

## No Orchestration in This Hook

**This is intentional.** The convention is simple:

```
Session starts (no hook runs)
-> CLAUDE.md + installed skill make using-sensemaking discoverable
-> Agent can invoke skill when needed
-> Agent reads skill and selects the next responsibility
-> Agent follows skill's teaching (or doesn't)
```

**NOT:**
```
Session starts
-> Hook inspects repo
-> Hook classifies fog type
-> Hook invokes workflows
-> Hook validates artifacts
```

Nor, if an executable hook is ever warranted, `artifact X -> execute Skill Y`.
The only admissible shape is mechanical (detect artifact -> validate ->
register provenance/state -> signal the agent to reassess), and the reopen
condition is a recurrent continuation event that a manual step keeps missing
in real use: `docs/decision-orchestration-boundary.md`, section "Hooks".

## Next Steps

1. **Verify the skill is discoverable** -- Run Test 1 above
2. **Verify skill content is current** -- Run Test 2 above
3. **Verify behavior teaching** -- Run Test 3 above
4. **Keep this description in sync with the skill** -- when `skills/using-sensemaking/SKILL.md` section numbering changes, update the citations here and in `CLAUDE.md`
5. **Do not add a hook** -- unless the reopen condition in `docs/decision-orchestration-boundary.md` ("Hooks") is observed in real use

## References

- **Bootstrap skill**: `skills/using-sensemaking/SKILL.md`
- **Hook description**: `.claude/hooks/sessionstart.md` (this file; no hook implementation exists)
- **Bootstrap pointer**: `CLAUDE.md` (SessionStart section)
- **Disposition of scripts and hooks**: `docs/decision-orchestration-boundary.md` ("Deterministic machinery and hooks")
- **Validation**: `docs/validator-json-refactor-guide.md`
- **Orchestration model**: `docs/adr/0013-agent-native-orchestration-primary.md`
