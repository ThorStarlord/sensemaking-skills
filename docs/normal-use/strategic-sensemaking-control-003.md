# Control arm 003 — Jellyfin (no skill, read-only)

Clean control for `strategic-sensemaking-trial-003.md`. Fresh agent context;
the prompt explicitly forbade reading or using any skill/SKILL.md/sensemaking
material. Same objective, same read-only authority. Recorded for artifact-level
comparison, not self-report.

```text
Repository / domain: a2-target-jellyfin (Jellyfin, .NET 10, v12.0 pre-release)
Date: 2026-09-29
Loaded Skill identity: NONE (control arm — skill deliberately excluded)
Chosen responsibility / next action: Bounded, evidence-grounded correctness verification of the recent EF Core query-semantics refactors in the item repository layer (BaseItemRepository.ByName.cs, commit c3a7de54f3) — the result-semantics-changing hotspot with several recent fix commits. Deliverable: a scoped verification write-up plus a proposed regression test, not a code change.
First concrete step: trace every caller of the changed GetItemValues/by-name path; re-derive equivalence of WhereOneOrMany and GroupBy(CleanValue).Select(Min(Value)); check test coverage for multiple itemValueTypes, with/exclude combinations, and duplicate values.
Scope avoided / refused: any code mutation (read-only); wholesale query-layer refactor (no evidenced defect); documentation rewrites (low leverage, docs live out-of-repo); unrelated subsystems.
Alternatives rejected: fix README doc drift; TODO/FIXME sweep (49 hits); investigate historical "Fix master build" commits; chase translation churn; declare "ship nothing".
Confidence: moderate (confident on repo identity/state and the query layer as risk hotspot; not confident a regression exists).
Blocking question: read-only forecloses `dotnet build/test` (a measured conclusion needs execute authority); owner intent (hotspot inferred from commit recency).
```

## Comparison (skill arm vs control arm)

- Responsibility chosen: skill = ESCALATE on the external-maintainer/publication
  boundary; control = bounded, evidence-grounded verification of the hottest,
  recently-refactored subsystem, with a proposed regression test.
- Scope avoided: both refuse mutation and unrelated/doc work.
- Verdict on this task: **control-favorable.** The control produced a concrete,
  authority-respecting, higher-leverage responsibility than the skill arm's
  escalation. The skill's predicted baseline failure (implement an unmergeable
  local improvement) did not occur; the control stayed read-only and
  verification-shaped.
