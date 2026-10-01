# Strategic Sensemaking trial program — re-measure (3 episodes per arm per task)

2026-09-30. After Stage 1 landed, the owner asked to re-run the trials at ≥3
episodes per arm per task with a fresh control, judged on artifacts. This
completes that: each arm now has 3 episodes per task.

Method: fresh contexts; the skill arm loaded `using-sensemaking`; the control arm
explicitly excluded any skill material. Read-only. Pre-registered bar: "keep
investing" only if the skill changes the outcome in its favor on **≥2 of 3
tasks**; otherwise "simplify hard."

## Episodes

### 002 — Pydantic
- **Skill:** 002 ESCALATE on ownership/authority · 002b VERIFY the only unlanded
  branch (`origin/vp/deque-schema`), escalate the merge · 002c EXPLORE, then
  ESCALATE on owner priority.
- **Control:** c002 restore verifiability (env mismatch) + request the work
  queue · c002b bounded diagnosis of a specific JSON-Schema constraint-placement
  defect · c002c reconcile stale `skip`/`xfail` markers.
- **Direction: control-favorable.** The control produced concrete,
  repo-answerable, bounded work (a named defect; a marker-reconciliation task);
  the skill escalated or verified ownership. Neither arm invented scope.

### 003 — Jellyfin
- **Skill:** 003 ESCALATE on the external-maintainer boundary · 003b INQUIRE the
  v12.0 database-migration coverage · 003c ESCALATE on owner target/authority.
- **Control:** c003 establish a verified baseline (`dotnet test`) · c003b
  build/test baseline (`.NET 10` SDK missing — a hard toolchain gate) · c003c
  read-only diagnosis, no fix.
- **Direction: tie.** Both converge on "establish a baseline / get the owner's
  target; do not mutate." The skill named a specific high-consequence area (v12
  migration); the control named the same EF-migration work as its rejected
  alternative.

### 004 — AION Workflow Core
- **Skill:** 004 CHALLENGE the visible milestone, surface the unwired validation
  gap · 004b implement the v0.2 schemas (milestone-following) · 004c
  validation-contract hardening (challenge, escalate).
- **Control:** c004 implement v0.2 schema validation (milestone) · c004b
  implement v0.2 artifact contracts (milestone) · c004c harden the validation
  seam (the same gap, surfaced without the skill).
- **Direction: weakly skill-favorable.** The skill challenged the milestone in
  2 of 3; the control followed it in 2 of 3. But the control independently
  surfaced the same validation gap in c004c, and one skill episode (004b)
  followed the milestone.

## Aggregation against the bar

| Task | Direction |
| --- | --- |
| 002 Pydantic | control-favorable |
| 003 Jellyfin | tie |
| 004 AION | weak skill-favorable |

**0 clear skill-favorable tasks; below the ≥2/3 bar.**

## Conclusion

The re-measure **does not** move toward "keep investing"; it reinforces the
ratified **"simplify hard"** verdict. The skill's headline benefit — preventing
first-visible-problem / milestone capture — is **weaker at n=3 than the first
read**: a control episode independently surfaced the AION validation gap, one
skill episode followed the AION milestone, and on Pydantic the control produced
more concrete bounded work. The only consistent skill-favorable signal remains
secondary: authority discipline (skill arms did not mutate; a control episode in
the first pass slipped by creating a `.venv`).

This is consistent with the capsule framing: **"no demonstrated benefit yet, not
proven no benefit."** It is not a reason to stop or to reopen the verdict.

## Limits

Read-only; same three tasks; fresh contexts but the same environment and the same
agent lineage as reviewer. n=3 per arm per task (12 new episodes added; 18 total).
Directional — not a controlled study (guide section 14).
