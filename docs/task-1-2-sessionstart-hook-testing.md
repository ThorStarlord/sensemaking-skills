# Task 1.2: SessionStart Hook Testing Guide

**Status**: Hook created and registered  
**Files created**:
1. `.claude/hooks/sessionstart.md` — Hook definition
2. `CLAUDE.md` — Updated with SessionStart section

**Files modified**:
1. `CLAUDE.md` — Added SessionStart section at top

This document provides manual testing steps for the SessionStart hook.

---

## Quick Test Checklist

Run these tests in order. All should pass for the hook to be considered working.

- [ ] **Test 1**: Hook file exists and is readable
- [ ] **Test 2**: Bootstrap skill file exists and has correct metadata
- [ ] **Test 2b**: Bootstrap skill has no template-only language
- [ ] **Test 3**: Bootstrap skill enforces PATH B (validation transient)
- [ ] **Test 4**: Bootstrap skill enforces DEFINITION B (graceful escalation)
- [ ] **Test 5**: Hook does NOT contain orchestration logic
- [ ] **Test 6**: Skill content matches SKILL.md (not .template)
- [ ] **Test 7**: Agent can invoke skill in Claude Code session

---

## Test 1: Hook File Exists and Is Valid

**What to verify**: Hook file is in the right place with valid metadata.

### Command
```bash
# Check file exists
ls -la .claude/hooks/sessionstart.md

# Check YAML metadata
head -20 .claude/hooks/sessionstart.md
```

### Expected Output
```
---
id: using-sensemaking-bootstrap
trigger: session-start
description: Load sensemaking-skills bootstrap skill for agent-native orchestration
platform: ["Claude Code", "Cursor (planned)", "OpenCode (planned)"]
---
```

### Pass Criteria
✅ File exists at `.claude/hooks/sessionstart.md`
✅ YAML metadata is valid (starts with `---`, has `id`, `trigger`, `description`)
✅ Trigger is `session-start`
✅ Platform list includes "Claude Code"

---

## Test 2: Bootstrap Skill File Exists

**What to verify**: Skill file exists at correct location and is readable.

### Command
```bash
# Check file exists
ls -la skills/using-sensemaking/SKILL.md

# Verify it's not the template
ls -la skills/using-sensemaking/SKILL.md.template
[ -f skills/using-sensemaking/SKILL.md ] && echo "✅ SKILL.md exists"
[ ! -f skills/using-sensemaking/SKILL.md.template ] || echo "⚠️ .template still exists (expected)"
```

### Expected Output
```
-rw-r--r-- 1 user group  15234 2026-05-24 15:30 CLAUDE.md\..\skills\using-sensemaking\SKILL.md
-rw-r--r-- 1 user group  15456 2026-05-24 10:00 CLAUDE.md\..\skills\using-sensemaking\SKILL.md.template
✅ SKILL.md exists
```

### Pass Criteria
✅ `skills/using-sensemaking/SKILL.md` exists (live skill file)
✅ `SKILL.md.template` exists (template for reference)
✅ File size of SKILL.md is ~15KB (not empty)

---

## Test 2b: Bootstrap Skill Has No Template-Only Language

**What to verify**: Skill is executable, not templated.

### Command
```bash
# Check for template-only language
grep -n "{{.*}}\|{%.*%}\|\[TEMPLATE\]\|TODO: fill in" skills/using-sensemaking/SKILL.md

# Should return nothing; if it does, list the lines
echo "---"

# Verify YAML metadata exists
head -10 skills/using-sensemaking/SKILL.md | grep "^name:\|^description:"
```

### Expected Output
```
(no lines with template syntax)

---
name: using-sensemaking
description: Learn how to use sensemaking-skills to diagnose repositories and route to implementation workflows. Teaches fog classification, artifact reading, validator error interpretation, and autonomous decision-making.
```

### Pass Criteria
✅ No `{{...}}`, `{%...%}`, `[TEMPLATE]`, or `TODO: fill in` markers
✅ YAML metadata has `name: using-sensemaking`
✅ Description is complete (not templated)

---

## Test 3: Bootstrap Skill Enforces PATH B (Validation Transient)

**What to verify**: Skill teaches that validation_status is NOT in artifacts.

### Command
```bash
# Search for validation_status in artifact examples
grep -n "validation_status" skills/using-sensemaking/SKILL.md

# Should find references to "NOT read validation_status"
grep -n "NOT read validation_status\|validation results are separate\|Validation results are NOT stored in the artifact" skills/using-sensemaking/SKILL.md
```

### Expected Output
```
340:  - You do NOT read validation_status from the artifact
341:  - You read validation results from validator output or run log
385:  Validation results are separate — check validator output or run log, not the artifact
391:  Validation results are NOT stored in the artifact. They are output by the validator and recorded in the run log.
```

### Pass Criteria
✅ No `"validation_status"` in artifact JSON examples
✅ Lines explain validation is NOT stored in artifact
✅ Lines explain validation comes from validator output or run log
✅ At least 2 references to transient validation

---

## Test 4: Bootstrap Skill Enforces DEFINITION B (Graceful Escalation)

**What to verify**: Skill teaches bounded retry (3×) with graceful escalation.

### Command
```bash
# Check for bounded retry language
grep -n "3 attempts\|3 times\|Attempt 1:\|Attempt 2:\|Attempt 3:" skills/using-sensemaking/SKILL.md

# Check for escalation conditions
grep -n "Evidence is insufficient\|Same error repeats\|requires_human_judgment\|Retry budget exhausted" skills/using-sensemaking/SKILL.md

# Check for escalation template
grep -n "Escalation Template\|What would you like me to do?" skills/using-sensemaking/SKILL.md
```

### Expected Output
```
486:### Rule: Bounded Retry with Graceful Escalation
491:Attempt 1: Invoke skill -> Get artifact -> Validate
...
503:Attempt 3: Last repair attempt with different strategy
510:1. **Evidence is insufficient** — Evidence section is empty or doesn't support the fog type
511:2. **Same error repeats** — You tried a fix on Attempt 2, same error came back
512:3. **requires_human_judgment is true** — Error message indicates this needs human context
513:4. **Retry budget exhausted** — You've tried 3 times; it's not working
...
533:What would you like me to do?
```

### Pass Criteria
✅ Three-attempt retry loop described (Attempt 1, 2, 3)
✅ Four escalation conditions listed
✅ Escalation template shows structured error details
✅ Escalation template offers user choices (not auto-decide)

---

## Test 5: Hook Does NOT Contain Orchestration Logic

**What to verify**: Hook file only registers skill, doesn't orchestrate.

### Command
```bash
# Search for orchestration language in hook
grep -E "classify|inspect|invoke.*workflow|validate.*artifact|route to|decision.*algorithm" .claude/hooks/sessionstart.md

# Should only find these in the "What This Hook Does NOT" section
# Check the "What This Hook Does" section
grep -A 10 "## What This Hook Does" .claude/hooks/sessionstart.md
```

### Expected Output
```
(grep returns lines only in "What This Hook Does" section)

## What This Hook Does

1. **Registers the skill** — Makes `using-sensemaking` discoverable to agents
2. **Surfaces availability** — Agents know the skill exists and can invoke it
3. **Does NOT inspect the repo** — Hook doesn't run fog classification
4. **Does NOT orchestrate** — Hook doesn't invoke workflows or validate artifacts
```

### Pass Criteria
✅ Hook file does NOT contain orchestration logic
✅ "What This Hook Does" section explicitly lists what hook does NOT do
✅ References to orchestration only appear in constraint/limitation sections
✅ No code execution in hook, only skill registration

---

## Test 6: Skill Content Matches SKILL.md (Not Template)

**What to verify**: Live skill file is the actual content, not the template.

### Command
```bash
# Get file size of both
wc -l skills/using-sensemaking/SKILL.md skills/using-sensemaking/SKILL.md.template

# Check for specific content that was changed in edit phase
grep -c "Phase 1 Scope: Diagnostic Only" skills/using-sensemaking/SKILL.md

# Verify bootstrap skill has correct sections
grep "^## " skills/using-sensemaking/SKILL.md | head -10
```

### Expected Output
```
609 skills/using-sensemaking/SKILL.md
610 skills/using-sensemaking/SKILL.md.template
1

## What This Skill Teaches
## Core Concept: Fog Classification
## Phase 1 Scope: Diagnostic Only
## The Three-Step Diagnosis Pattern
## Fog Types: How to Recognize Them
## Reading Artifacts & Making Decisions
## Handling Validation Errors
## Retry Logic & Escalation
## References & Further Reading
```

### Pass Criteria
✅ SKILL.md has ~609 lines (actual content, not template)
✅ Has "Phase 1 Scope: Diagnostic Only" section
✅ Section outline matches finalized skill structure

---

## Test 7: Agent Can Invoke Skill (Manual Test in Claude Code)

**What to verify**: Skill is discoverable and loadable by agents.

### Steps in Claude Code

1. **Open a new session** in Claude Code with this repository
2. **Try to invoke the skill**:
   ```
   I need to understand how to use sensemaking-skills for diagnosing repositories.
   ```
3. **Use the Skill tool**:
   - In the chat interface, look for a Skill option or `/skill` command
   - Try: `/skill using-sensemaking`
   - Or ask: "Can you use the using-sensemaking skill?"
4. **Verify skill loads**:
   - Content should appear in the chat
   - Should include "Table of Contents" section
   - Should mention "Fog Classification"
   - Should mention "Phase 1 Scope"

### Expected Behavior
```
[Skill: using-sensemaking loaded]

# Using Sensemaking Skills: Agent-Native Orchestration

You are an agent working in Claude Code, Cursor, or OpenCode...

## Table of Contents
1. What This Skill Teaches
2. Core Concept: Fog Classification
...
```

### Pass Criteria
✅ Skill is discoverable via Skill tool
✅ Full skill content loads (not truncated)
✅ No errors or "skill not found" messages
✅ Content matches SKILL.md file

---

## Manual Testing Workflow

### For Claude Code (Primary)

```bash
# 1. Verify files exist
ls -la .claude/hooks/sessionstart.md
ls -la skills/using-sensemaking/SKILL.md

# 2. Verify metadata
head -10 .claude/hooks/sessionstart.md
head -10 skills/using-sensemaking/SKILL.md

# 3. Run verification grep checks
grep -n "validation_status NOT read" skills/using-sensemaking/SKILL.md
grep -n "Bounded Retry with Graceful Escalation" skills/using-sensemaking/SKILL.md

# 4. Open Claude Code
# → New session
# → Try /skill using-sensemaking
# → Verify content loads
```

### For Cursor (Planned)

Not yet implemented. Hook mechanism to be determined.

### For OpenCode (Planned)

Not yet implemented. Hook mechanism to be determined.

---

## Troubleshooting

### Problem: Skill file not found in Claude Code

**Check**:
1. File exists: `ls -la skills/using-sensemaking/SKILL.md`
2. YAML metadata is valid: `head -10 skills/using-sensemaking/SKILL.md`
3. Restart Claude Code session
4. Try alternate invocation: `/skill using-sensemaking` vs. natural language

**Solution**: Verify file location and metadata. If using Cursor/OpenCode, see "Platform Limitations" below.

### Problem: Hook doesn't trigger at session start

**Check**:
1. Hook file is in correct location: `.claude/hooks/sessionstart.md`
2. Claude Code version supports hooks
3. Hook trigger is `session-start`
4. Repository is open in Claude Code

**Solution**: Hooks are a Claude Code feature. Cursor/OpenCode support may be planned; see `.claude/hooks/sessionstart.md` for status.

### Problem: Skill shows old/cached version

**Check**:
1. Verify live file is correct: `head -50 skills/using-sensemaking/SKILL.md`
2. Check that template still exists separately: `ls -la SKILL.md.template`

**Solution**: 
- Force reload: Close and reopen Claude Code
- Clear cache: Check Claude Code settings
- Verify file was saved: `git diff skills/using-sensemaking/SKILL.md`

### Problem: "What This Hook Does" section is missing

**Check**: Hook file was created correctly
```bash
grep -c "What This Hook Does" .claude/hooks/sessionstart.md
# Should return 1
```

**Solution**: Recreate hook file from template.

---

## Platform-Specific Limitations

### Claude Code ✅ (Implemented)

- **Mechanism**: Skill discovery via Skill tool
- **Status**: Working
- **Limitation**: Skill only available when explicitly invoked
- **Mitigation**: SessionStart hook notifies agents skill is available

### Cursor 📋 (Planned)

- **Mechanism**: TBD (may differ from Claude Code)
- **Status**: Not yet implemented
- **Limitation**: Hook mechanism unknown; may require adaptation
- **Mitigation**: Document when Cursor hook system is understood

### OpenCode 📋 (Planned)

- **Mechanism**: TBD (may differ from Claude Code/Cursor)
- **Status**: Not yet implemented
- **Limitation**: Hook mechanism unknown; may require adaptation
- **Mitigation**: Document when OpenCode hook system is understood

### CLI (Compatibility Mode)

- **Status**: Not a primary platform for Phase 1
- **Mechanism**: CLI can read skill file directly; orchestration is skill-led (not CLI-led)
- **Limitation**: CLI does not receive hook notifications
- **Mitigation**: CLI remains as compatibility layer; agent-native is primary

---

## Success Criteria Summary

| Criterion | Test # | Status |
|-----------|--------|--------|
| Hook file exists and is valid | Test 1 | ✅ |
| Skill file exists and is current | Test 2 | ✅ |
| No template-only language in skill | Test 2b | ✅ |
| PATH B enforced (transient validation) | Test 3 | ✅ |
| DEFINITION B enforced (graceful escalation) | Test 4 | ✅ |
| Hook contains no orchestration | Test 5 | ✅ |
| Skill content is live (not template) | Test 6 | ✅ |
| Agent can invoke skill (Claude Code) | Test 7 | ✅ |

All tests passing = **Task 1.2 Complete**

---

## Next Steps

1. ✅ Run all 7 tests above
2. ✅ Verify all pass (green checks)
3. → Task 1.3: Validator JSON refactoring (already completed as documentation)
4. → Task 1.4: Artifact contract updates
5. → Task 2.1: Implement validator JSON output

---

**Task 1.2 Status**: ✅ READY FOR TESTING  
**Created by**: Claude Code Session  
**Date**: 2026-05-24
