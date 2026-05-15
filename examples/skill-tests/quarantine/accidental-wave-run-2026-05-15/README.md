# Quarantine: Accidental Wave 1/Wave 2 Run (2026-05-15)

## Metadata
- **run_type**: uncontrolled_pilot
- **promotion_status**: not official baseline
- **reason**: Wave 2 was executed before the clean compliance audit checkpoint was established and verified.

## Summary of Evidence
This quarantine folder preserves the artifacts and logs from an accidental parallel execution run. While not official, the following evidence is highly useful for repository hardening:

1. **Execution Discipline**: Wave 1 logs (`iso-framer-001`, `iso-mapper-001`) prove that the agents can operate within isolation boundaries and maintain relative path hygiene.
2. **Structural Defect Detection**: The run identified several drifts in `ALL-SKILLS-TEST-PLAN.md`, including missing fixtures and incorrect validator command signatures.
3. **Maintenance Safety Milestone**: The `maint-001` task (Scenario 005) successfully demonstrated "Anti-Causal" resistance by correctly identifying a `fixture_defect` and refusing to patch valid skill logic to match a flawed test.

## Contents
- `WAVE-1-COMPLIANCE-REPORT.md`: Summary of isolated skill verification.
- `WAVE-2-QUALITY-REPORT.md`: Summary of handoff and maintenance loop tests.
- `ACCIDENTAL-RUN-AUDIT.md`: The formal audit of this accidental run.
- Subdirectories containing `TEST-RUN-LOG.md` and generated artifacts for each task.

**Do not use these artifacts as stable baselines. Refer to the formal rerun for official verification.**
