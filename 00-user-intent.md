# User Intent: Sensemaking Skills Infrastructure Fixes

## User Goal

Fix four structural gaps in the sensemaking skills system to stabilize the framework for production deployment:

1. **Evidence rules dual-mode rendering** — support both investigative (line numbers) and durable (grep-verifiable) output modes
2. **Execution mode for rapid autonomous execution** — document decision criteria for direct skill invocation vs. orchestration
3. **Skill-hygiene validator** — automated checks for npm scripts, skill-registry cross-refs, and artifact-contract compliance
4. **Artifact contracts for PM/engineering** — define schemas for PRD, issue_list, agent_brief, code_patch

## Context

Phase 4 testing revealed that skills produce good output when applied with judgment, but lack formal contracts for handoff artifacts. The framework is production-ready functionally but needs these infrastructure fixes to:
- Prevent ad-hoc format drift across runs
- Reduce manual coordination between downstream skills
- Provide automated validation that breaks before deployment, not in production

## Success Criteria

All four gaps have documented fixes, passing implementations, and integrated validation. Framework ready for 3-week rollout plan starting Week 1.
