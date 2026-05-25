# Sensemaking Skills: Roadmap to General Availability

## Current Status: Phase 2.3 Complete ✅

**What's Done:**
- ✅ Phase 4: Production gate passed (Scenario 5 proven)
- ✅ Phase 2.2: CLI development complete (8 tests passing, local installation working)
- ✅ Phase 2.3: PyPI publication readiness complete (distributions built and verified)
- ✅ Documentation: Accurate, honest, agent-native positioning

**Current Installation Method:**
```bash
pip install -e .  # From source only
```

**Current Version:** 0.2.1 (Beta)

---

## Next Steps: Phase 3 — Real-World CLI Testing

### Goal
Validate CLI with real users on their actual repositories before publishing to production PyPI.

### Timeline: 1-2 weeks

**3.1 — Invite Real Users for CLI Testing**
- [ ] Identify 3-5 users/teams who will test the CLI
- [ ] Provide them with:
  - Installation instructions (`pip install -e .`)
  - Real-world workflow guide (GETTING_STARTED.md)
  - How to report issues
- [ ] Document their feedback and use cases

**3.2 — Monitor Real-World Usage**
- [ ] Collect feedback on:
  - CLI usability and error messages
  - Agent-native workflow clarity
  - Documentation completeness
  - Performance on real repositories
- [ ] Track any bugs or issues
- [ ] Measure success: users can diagnose their repositories

**3.3 — Iterate on Feedback**
- [ ] Fix critical bugs (exit Phase 3 if found)
- [ ] Improve documentation if needed
- [ ] Refine CLI command help text
- [ ] Update CHANGELOG.md with 0.2.2 bugfixes if needed

**3.4 — Sign-Off on Real-World Testing**
- [ ] All users successfully diagnosed their repositories
- [ ] CLI is intuitive and helpful
- [ ] Documentation is clear and complete
- [ ] No show-stopping bugs

---

## Phase 4 — PyPI Publication

### Goal
Release sensemaking-skills to production PyPI for general availability.

### Timeline: 1-2 days (after Phase 3 passes)

**4.1 — Create Release on GitHub**
```bash
git tag v0.2.1
git push origin v0.2.1
```

**4.2 — Publish to Production PyPI**
```bash
python -m twine upload dist/*
```

**4.3 — Verify Publication**
```bash
pip install sensemaking-skills==0.2.1
sensemaking-skills --version
```

Expected: `0.2.1`

**4.4 — Update Installation Documentation**
```markdown
## Installation

Install from PyPI:
```bash
pip install sensemaking-skills
```
```

---

## Phase 5 — General Availability (GA)

### Goal
Full public release with support and ongoing development.

### What GA Means
- ✅ Available on PyPI for all Python users
- ✅ Documented and discoverable
- ✅ Supported for real-world usage
- ✅ Roadmap for future versions (0.3.0, 1.0.0)

### Versioning Strategy
- **0.2.1** — Current: CLI utilities + agent-native diagnosis
- **0.3.0** — Planned: Full CLI with agent integration (if feedback supports it)
- **1.0.0** — Stable: Proven in production with user feedback

---

## Success Criteria

### Phase 3 Success (Real-World Testing)
- [ ] 3+ users successfully used CLI to diagnose real repositories
- [ ] No critical bugs discovered
- [ ] Documentation is clear and helpful
- [ ] Agent-native workflow is intuitive
- [ ] CLI commands work as documented

### Phase 4 Success (PyPI Publication)
- [ ] Package published to PyPI
- [ ] Installation via `pip install sensemaking-skills` works
- [ ] Users can find and install it
- [ ] `sensemaking-skills --version` shows 0.2.1

### Phase 5 Success (GA)
- [ ] 10+ users have installed from PyPI
- [ ] Positive feedback on real diagnostics
- [ ] Clear roadmap for 0.3.0 and 1.0.0
- [ ] Community engagement beginning

---

## Final Goal: Production-Ready, User-Accessible Tool

**Vision:**
Sensemaking Skills becomes a standard part of the repository diagnosis workflow:

```bash
# User installs once
pip install sensemaking-skills

# User diagnoses any repository
sensemaking-skills analyze --repo /path/to/my/repo

# Agent reads the skills and produces diagnostics
# User gets a clear problem frame and workflow

# Future: full CLI integration without agent dependency
```

**Long-term (Post-1.0.0):**
- CLI can invoke agents directly (Anthropic SDK integration)
- Standalone diagnosis without requiring Claude Code
- Community contributions and extensions
- Integrations with other tools (GitHub Actions, CI/CD, etc.)

---

## Decision Points

### After Phase 3 Testing:
**Go/No-Go: Should we publish to PyPI?**
- **GO** — Real-world testing passed, users ready
- **NO-GO** — Issues found, iterate more

### After Phase 5 GA:
**Next Investment: What's the 0.3.0 priority?**
- Direct agent integration (Anthropic SDK)?
- GitHub Actions integration?
- VSCode extension?
- Community feedback will guide this

---

## How You Can Help (Real-World Testing)

If you want to be a Phase 3 tester:

1. **Install locally:**
   ```bash
   pip install -e .
   ```

2. **Diagnose a repository:**
   ```bash
   sensemaking-skills analyze --repo /path/to/repo
   ```

3. **Follow the workflow:**
   - Open repo in Claude Code
   - Ask agent to read `skills/using-sensemaking/SKILL.md`
   - Follow the skill to diagnosis

4. **Report feedback:**
   - What worked well?
   - What was confusing?
   - What would make it better?
   - Any bugs?

---

**Current Milestone: Phase 2.3 Complete ✅**
**Next Milestone: Phase 3 Real-World Testing (Ready to Start)**
**Final Goal: Production PyPI Release with User Community**
