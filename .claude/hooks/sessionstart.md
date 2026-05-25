---
id: using-sensemaking-bootstrap
trigger: session-start
description: Load sensemaking-skills bootstrap skill for agent-native orchestration
platform: ["Claude Code", "Cursor (planned)", "OpenCode (planned)"]
---

# SessionStart: Load Sensemaking Bootstrap Skill

When a session starts in this repository, the **using-sensemaking** bootstrap skill becomes available to agents.

## SessionStart Bootstrap Reminder

When a session starts, this hook surfaces a brief reminder:

---

**🔧 sensemaking-skills Bootstrap Available**

Before diagnosing a codebase with sensemaking-skills, read the bootstrap skill:

```
/skill using-sensemaking
```

**Or read directly:**
```
skills/using-sensemaking/SKILL.md
```

This skill teaches:
- Fog classification (4 types: product, ui, docs, architecture)
- 3-step diagnosis pattern
- How to read artifact outputs
- How to handle validation errors
- Bounded retry logic (3 attempts, graceful escalation)
- When to auto-fix vs. escalate

**Then**, when asked to diagnose a codebase:
1. Invoke `repo-sensemaker` skill
2. Read the artifact: `primary_fog_type`, `evidence`, `recommended_workflow`
3. Validate the artifact (see Handling Validation Errors in the skill)
4. Report findings or escalate if validation fails

---

## How Agents Use This Skill

### Invoke via Skill Tool
```
User: "Diagnose my codebase"
Agent: [reads using-sensemaking skill via /skill using-sensemaking]
Agent: [understands 3-step pattern and validation rules]
Agent: [invokes repo-sensemaker skill]
```

### Direct File Read
Agents can read the skill file directly:
```
Skill file: skills/using-sensemaking/SKILL.md
Agent: [parses YAML metadata + Markdown teaching content]
Agent: [applies fog classification rules]
Agent: [invokes repo-sensemaker]
```

### No Passive Loading

The reminder is **active** — it tells agents to read the skill before starting diagnosis. It does NOT:
- Automatically run diagnosis
- Parse the codebase
- Invoke workflows
- Validate artifacts

Those are agent responsibilities, taught by the skill.

## What This Hook Does

1. **Registers the skill** — Makes `using-sensemaking` discoverable to agents
2. **Surfaces availability** — Agents know the skill exists and can invoke it
3. **Does NOT inspect the repo** — Hook doesn't run fog classification
4. **Does NOT orchestrate** — Hook doesn't invoke workflows or validate artifacts

## Platform Status

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | ✅ Implemented | Primary platform; skill is discoverable via Skill tool |
| Cursor | 📋 Planned | Hook mechanism may differ; documentation in progress |
| OpenCode | 📋 Planned | Hook mechanism may differ; documentation in progress |
| CLI | ℹ️ Compatibility | CLI can import skill and parse artifacts, but uses skill-led orchestration |

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
# Verify the skill teaches DEFINITION B (graceful escalation):
grep -n "Bounded Retry with Graceful Escalation" skills/using-sensemaking/SKILL.md

# Verify the skill enforces PATH B (transient validation):
grep -n "validation_status NOT read from the artifact" skills/using-sensemaking/SKILL.md
# OR search for: "Validation results are separate"
```

### Test 4: Hook doesn't orchestrate
```bash
# Verify the hook file does NOT contain:
grep -v "Do NOT.*inspect\|Do NOT.*orchestrate" .claude/hooks/sessionstart.md
# Should find the "What This Hook Does" section showing NO orchestration
```

## How the Hook Injects the Skill

**Method: Skill discovery via platform mechanisms**

1. **Claude Code**: 
   - Hook registers skill in `.claude/hooks/sessionstart.md`
   - Claude Code's Skill tool discovers `skills/using-sensemaking/SKILL.md`
   - Agent invokes via `/skill using-sensemaking` or Skill tool
   - Skill content is loaded from the live file (not cached)

2. **Cursor/OpenCode** (when implemented):
   - Similar mechanism adapted to platform-specific hook system
   - Skill file location remains the same
   - Agent invocation method may vary

## Constraints & Limitations

### Intentional Constraints

- **Hook scope**: Limited to skill availability only
  - ✅ Registers/surfaces skill
  - ❌ Does NOT inspect repo
  - ❌ Does NOT classify fog
  - ❌ Does NOT invoke workflows
  - ❌ Does NOT validate artifacts

- **Skill responsibility**: Bootstrap skill teaches orchestration
  - Skill tells agents WHEN and HOW to invoke repo-sensemaker
  - Skill tells agents HOW to interpret validator output
  - Skill tells agents HOW to retry and escalate
  - Agent decides whether to follow these rules (they're not enforced)

### Platform Limitations

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| Claude Code hook loading | May take 1-2 seconds at session start | Lazy load; skill only loaded when invoked |
| Skill content caching | Old version might be cached | Always read live file, not cached metadata |
| Cursor/OpenCode mechanism unknown | Hook may not work as documented | Documented as "planned"; test needed |
| File path availability | Must be relative to repo root | `.claude/` and `skills/` directories standard |

## No Orchestration in This Hook

**This is intentional.** The hook's job is simple:

```
Session starts
  ↓
Hook registers/surfaces using-sensemaking skill
  ↓
Agent can invoke skill when needed
  ↓
Agent reads skill and decides what to do next
  ↓
Agent follows skill's teaching (or doesn't)
```

**NOT:**
```
Session starts
  ↓
Hook inspects repo
  ↓
Hook classifies fog type
  ↓
Hook invokes workflows
  ↓
Hook validates artifacts
```

That second flow belongs to Phase 2 or to agents using the skill. Not here.

## Next Steps

1. **Verify hook is discoverable** — Run Test 1 above
2. **Verify skill content is correct** — Run Test 2 above
3. **Verify behavior teaching** — Run Test 3 above
4. **Document platform adaptations** — When Cursor/OpenCode mechanism is known
5. **Test with real agents** — Task 3.1 (End-to-end test)

## References

- **Bootstrap skill**: `skills/using-sensemaking/SKILL.md`
- **Hook implementation**: `.claude/hooks/sessionstart.md` (this file)
- **Hook registration**: `CLAUDE.md` (SessionStart section, below)
- **Validation**: `docs/validator-json-refactor-guide.md`
- **Orchestration model**: `docs/adr/0013-agent-native-orchestration-primary.md`
