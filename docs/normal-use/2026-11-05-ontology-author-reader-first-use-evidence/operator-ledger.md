# SDD ledger — plan: docs/superpowers/plans/2026-11-05-ontology-author-reader-qualification.md
Ruling: run the plan's A/B/C protocol rather than SDD implementer/reviewer loops; C is the review and no fix rounds repair participant output — fix rounds would contaminate the observation — cost if wrong: less review of operator bookkeeping.
Ruling: ledger lives outside repo (plan: disposable operator workspace) — cost: lost if workspace deleted; readout is durable.
Ruling: Agent-tool fresh subagents stand in for separate host sessions since headless auth expired — cost: same host/model/parent; independence is context-level, disclosed in readout.
Ruling: refresh global uv CLI + two installed Skills to SOURCE_SHA so participant prompts need no pinning cue — cost: machine-wide forward update, disclosed.
Task 1: complete (READY)
Operator incident: first uv refresh failed (os error 32) and briefly broke global CLI; Author A launched in same batch before failure seen. Repaired by retry at 21:10:49Z. Check A trace for any broken-CLI encounter.
Repair: uv tool install --force kept failing on a Lib dir lock (no holder identified); reinstalled in place with uv pip --reinstall at 6f54a4a7eeb2a2101536f3307c37bb55a46dcbca and updated receipt rev. CLI verified working 21:11:01Z.
Repair 2: overlay-copied exact package set from side venv at 6f54a4a7eeb2a2101536f3307c37bb55a46dcbca onto tool site-packages (dir locks blocked removal). Verify below. 21:11:32Z
Ruling: keep Author attempt 1 despite A reading manifest.md/progress.md during operator-caused CLI crash; disclose as contamination, no rerun — manifest held no oracle or expected conclusion and rerunning selects outcomes — cost if wrong: A's hedged style may be inflated by knowing it was a probe; C assesses.
Task 2: complete (candidate valid first write, 5 claims, 8 relations, schema 2)
Task 3: complete (build/search/explain exit 0 at c7eb21df)
Task 3: complete (build/search/explain exit 0 at c7eb21df)
Ruling: no neutral cue sent — B consumed the candidate before any cue; pass 2 still sent — plan requires a separately recorded source check even though pass 1 already mixed in source reading — cost: boundary is softer than designed; C assesses.
Ruling: operator commit message named the probe and filename is plan-mandated; disclosed as discovery aid, not removed post hoc — cost: spontaneity claim weaker.
Task 4: complete (spontaneous candidate read before any cue; pass 2 frozen at raw/B-pass2.md; no neutral cue)
Task 5: complete (C verdict PARTIAL)
