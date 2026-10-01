# Autonomous Task v2 — Candidate Construction and Pilot Lock Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construct the real experimental objects (3 disposable pilot tasks + hidden oracles, 36 pre-pilot candidate commitments across two tranches, frozen manifests, post-freeze salts and deterministic rankings, three dispatch seeds, agent/evaluator bundle separation, a real preflight run, and a lock record) required to honestly claim `PILOT LOCKED` — or to stop at a specific, named blocker.

**Architecture:** A strict, one-directional chronology enforced by file layout and script order: author → qualify → freeze manifest → hash → salt → rank → seed → bundle → preflight → lock record. Each stage's output is a file whose hash the next stage consumes; nothing later in the chain may cause an earlier file to be rewritten. Candidate content is authored against the repository **as it existed at the frozen SHA** (`git show 0ffb564b...:<path>`), independent of this working tree's current HEAD.

**Tech Stack:** Markdown/YAML content files, Python 3 for hashing/salting/ranking/seed generation (stdlib `hashlib`, `secrets` only — no new dependencies), the existing `bash` preflight gate script.

**Spec:** `experiments/evaluation-design-e3-autonomous-task-v2/` (17-file reviewed package, especially `AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` for the ranking formula and `AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md` for substrates), plus `experiments/evaluation-design-e3-autonomous-task-v2/construction/00-HANDOFF-VERIFICATION.md` (this session's Phase 0 record).

## Global Constraints

- Frozen repo: `ThorStarlord/sensemaking-skills` @ `0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`.
- Hash algorithm: SHA-256 everywhere, hex digest, over raw UTF-8 file bytes (LF line endings, no BOM) for per-artifact hashes; manifest canonicalization defined in Task 8 (this is the one gap the reviewed package left unresolved — resolved here, not re-litigated).
- Candidate IDs must be arbitrary and rank-uninformed (e.g. `T1M-K7Q`), never `best`/`primary`/`fallback`-style labels.
- No salt may be generated before its corresponding manifest is frozen and hashed. No dispatch seed may be generated after any pilot or main-study outcome exists (none exist yet, so all three seeds are generated in this session, before any run).
- T3 remains pilot-conditional: candidates 4-9 (Tranche-1/2 T3 cells) are authored as **parameterized specifications**, not fully materialized tasks, per `AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md`.
- Do not execute any pilot or main-study benchmark cell. This plan stops at the lock record / preflight, never at a dispatched run.
- Do not inspect sibling experiment worktrees or prior Autonomous Task results (isolation boundary from `00-HANDOFF-VERIFICATION.md` §2 and the design package's Phase 1 role boundaries).

---

## File Structure

```
experiments/evaluation-design-e3-autonomous-task-v2/construction/
  00-HANDOFF-VERIFICATION.md            (done — Phase 0)
  pilot/
    T1-PILOT-TASK.md                    (agent-visible task contract)
    T1-PILOT-ORACLE.md                  (evaluator-only hidden oracle)
    T2-PILOT-TASK.md
    T2-PILOT-ORACLE.md
    T3-PILOT-TASK.md                    (or T3-PILOT-INADMISSIBLE.md if the chain fails)
    T3-PILOT-ORACLE.md
    PILOT-TASK-MANIFEST.md              (binds all 3, records manifest hash)
  tranche1/
    candidates/
      <candidate_id>.md                 (18 files: full commitment record per candidate)
    TRANCHE1-CANDIDATE-MANIFEST.md
  tranche2/
    candidates/
      <candidate_id>.md                 (18 files)
    TRANCHE2-CANDIDATE-MANIFEST.md
  scripts/
    hash_utils.py                       (canonicalization + sha256 helpers)
    freeze_manifest.py                  (reads a candidates/ dir, emits manifest + hash)
    generate_salts_and_rankings.py      (post-freeze: salt -> rank_key -> ranking)
    generate_dispatch_seeds.py          (3 seeds, seeded Fisher-Yates preview)
  AUTONOMOUS-TASK-V2-RANKINGS.md
  AUTONOMOUS-TASK-V2-DISPATCH-SEEDS.md
  AUTONOMOUS-TASK-V2-LOCK-RECORD.md     (final deliverable)
```

---

## Task 1: T1 pilot task + hidden oracle

**Files:**
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/T1-PILOT-TASK.md`
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/T1-PILOT-ORACLE.md`

**Interfaces:**
- Consumes: substrate facts from `00-HANDOFF-VERIFICATION.md` §3 (the `workflow-registry.yaml` duplication at frozen SHA).
- Produces: `T1-PILOT-TASK.md` (visible contract, no route named) and `T1-PILOT-ORACLE.md` (route-independent semantic check) — both consumed by Task 4 (manifest freeze) and, eventually, Phase 11 bundle separation.

- [ ] **Step 1: Read the frozen-SHA substrate directly**

Run: `git show 0ffb564b:skills/workflow-planner/references/workflow-registry.yaml` and `git show 0ffb564b:src/sensemaking_skills/defaults/workflow-registry.yaml`, and identify one concrete, plausible edit request (e.g. adding/adjusting a field on an existing workflow entry, or adding a new step) where the *semantically correct* place to apply it depends on which consumer actually governs the requested runtime behavior (`scripts/workflow-planner.py` dogfood path vs. `WorkflowRegistry` installed-package path) — not just "the file that happens to be edited."

- [ ] **Step 2: Author the visible task contract**

Write `T1-PILOT-TASK.md` with: task text (does not name either file or either consumer), initial-state note (frozen SHA, no fixture changes needed beyond the repo itself), and an explicit non-goal statement (do not just edit both files — the oracle checks which mechanism actually governs the outcome).

- [ ] **Step 3: Author the hidden oracle**

Write `T1-PILOT-ORACLE.md` with: the semantic outcome being checked (e.g., "does `scripts/workflow-planner.py <relevant subcommand>` / `WorkflowRegistry(...)` actually reflect the requested change for the consumer the task implies"), a route-independent acceptance check (pass if the right mechanism changed regardless of *how* the agent got there — editing a file directly, writing a script, etc.), and at least one negative case (edited the wrong copy only, or edited both without resolving which one the task's implied consumer reads).

- [ ] **Step 4: Qualify against the T1 checklist**

Record explicitly, in a `## Qualification` section of `T1-PILOT-ORACLE.md`: two-or-more plausible mechanisms (yes — two registry copies), wrong route genuinely plausible (yes — an agent could edit either or both without checking which is read), repo evidence discriminates (yes — consumer code differs), oracle is route-independent (yes, per Step 3), no environment/network constraint forces the route (yes), task doesn't name the answer (yes). Mark `ADMISSIBLE` or `INADMISSIBLE — <reason>`; if inadmissible, return to Step 1 with a different edit request before proceeding.

- [ ] **Step 5: Sanity-check the oracle is actually checkable**

Run: manually trace through what commands would need to execute to verify PASS vs FAIL (e.g. run `python scripts/workflow-planner.py <cmd>` or instantiate `WorkflowRegistry` against a patched frozen-SHA clone) — confirm this is mechanically executable later, not just prose. Note the exact command(s) in the oracle file.

---

## Task 2: T2 pilot task + hidden oracle

**Files:**
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/T2-PILOT-TASK.md`
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/T2-PILOT-ORACLE.md`

**Interfaces:**
- Consumes: `artifact-contracts.yaml` and `tests/test_field_contract_agreement.py` at frozen SHA.
- Produces: same shape as Task 1's outputs.

- [ ] **Step 1: Read the frozen-SHA substrate**

Run: `git show 0ffb564b:skills/workflow-planner/references/artifact-contracts.yaml` and `git show 0ffb564b:tests/test_field_contract_agreement.py`. Identify a constrained-transformation request: add/modify a field declaration in one artifact-contract block such that (a) multiple valid YAML edits satisfy it, (b) `test_field_contract_agreement.py` is the authoritative pass/fail check, (c) at least one unrelated contract block must remain byte-for-byte unchanged (the protected-state requirement), (d) there's a plausible near-miss (e.g. adding the field to the wrong block, or under the wrong producer/consumer role) that must fail.

- [ ] **Step 2: Author the visible task contract**

Write `T2-PILOT-TASK.md`: task text naming the semantic requirement (not the exact YAML diff), the protected-state constraint stated explicitly ("do not modify any other contract block"), initial state = frozen SHA.

- [ ] **Step 3: Author the hidden oracle**

Write `T2-PILOT-ORACLE.md`: the exact structural check (which block, which field, what value/type constraint), the authoritative validator invocation (`pytest tests/test_field_contract_agreement.py` or the specific test function), the protected-state diff check (hash or structural diff of every other block), and the near-miss case that must be rejected.

- [ ] **Step 4: Qualify against the T2 checklist**

Same pattern as Task 1 Step 4, using the T2 criteria from `00-HANDOFF-VERIFICATION.md`/`TASK-CONSTRUCTION.md`: multiple valid strategies, semantic not text-equality oracle, protected-state check present, near-miss rejectable, meaningful repo reasoning required, distinct from prior Autonomous Task D/D′ tasks (confirm by name only — do not inspect prior task content, per the isolation boundary; rely on the reviewed package's own note that this substrate is fresh).

- [ ] **Step 5: Sanity-check the oracle is mechanically executable** (same pattern as Task 1 Step 5).

---

## Task 3: T3 pilot task + hidden oracle (pilot-conditional)

**Files:**
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/T3-PILOT-TASK.md` and `T3-PILOT-ORACLE.md`, **or** `T3-PILOT-INADMISSIBLE.md` recording negative admissibility.

**Interfaces:**
- Consumes: `scripts/workflow-runtime.py` `--resume` mechanism at frozen SHA (`_resumable_terminal_statuses`, `_find_resume_state`, `resume_skip`, ledger).
- Produces: either a qualified T3 pilot pair (same shape as Tasks 1-2) or a recorded inadmissibility that Task 4 and later Tranche construction must respect (T3 candidates become parameterized specs only, never materialized).

- [ ] **Step 1: Trace the real resume mechanism at frozen SHA**

Run: `git show 0ffb564b:scripts/workflow-runtime.py | sed -n '1900,2100p'` (and any other relevant line ranges found via the grep in `00-HANDOFF-VERIFICATION.md` §3) to fully understand: what makes a step reach `FAILED` (which validator failure produces it), what `run-ledger.jsonl` / `handle_audit_run` records, and exactly how `--resume` distinguishes `resume_skip` (completed) from a retried `FAILED` step.

- [ ] **Step 2: Design a concrete workflow run that naturally produces a genuine `FAILED` step**

Identify (or construct, e.g. via a small fixture workflow definition under `construction/pilot/fixtures/`) a run where: step 1 completes successfully, step 2 fails a *real* validator (not an injected/fake failure), and `--resume` is structurally capable of retrying step 2 while skipping step 1.

- [ ] **Step 3: Walk the seven-link chain explicitly**

Write out, in `T3-PILOT-ORACLE.md`, each of the seven links from `AUTONOMOUS-TASK-V2-PILOT-PLAN.md:125-133` with a concrete, named mechanism satisfying it (not a restatement of the requirement). If any link cannot be satisfied by a real mechanism in this repo at the frozen SHA, STOP this task and instead write `T3-PILOT-INADMISSIBLE.md` recording which link fails and why, per the design package's explicit instruction not to manufacture T3.

- [ ] **Step 4: If admissible, author the visible task contract**

Write `T3-PILOT-TASK.md`: task text describing the operational-recovery scenario (start a run, encounter the failure, recover) without pre-narrating the exact failure or fix.

- [ ] **Step 5: If admissible, qualify and sanity-check** (same pattern as Tasks 1-2 Steps 4-5), explicitly confirming: reset-laundering is independently detectable (state before vs. after differs only in the retried step), and replay causes no duplicate semantic work (run-ledger entries for step 1 are not duplicated).

---

## Task 4: Freeze the pilot task manifest

**Files:**
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/PILOT-TASK-MANIFEST.md`
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/scripts/hash_utils.py`

**Interfaces:**
- Consumes: `T1/T2/T3-PILOT-TASK.md` and `-ORACLE.md` (or `T3-PILOT-INADMISSIBLE.md`) from Tasks 1-3.
- Produces: `pilot_manifest_sha256` — consumed by nothing else in-plan (pilot tasks are never ranked/salted; the manifest hash exists purely for lock-record provenance), but its *presence* gates Task 20 (dispatch seed for pilot ordering may reference it).

- [ ] **Step 1: Write `hash_utils.py`**

```python
"""SHA-256 helpers for Autonomous Task v2 candidate/manifest hashing."""
import hashlib
import json


def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_manifest_json(records: list[dict]) -> str:
    """Canonical serialization for manifest hashing: records sorted by
    candidate_id, keys sorted, no extraneous whitespace, LF-only."""
    ordered = sorted(records, key=lambda r: r["candidate_id"])
    return json.dumps(ordered, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_manifest(records: list[dict]) -> str:
    return sha256_text(canonical_manifest_json(records))
```

- [ ] **Step 2: Run it against the three pilot files to sanity-check hashing works**

Run: `python -c "from experiments.evaluation-design-e3-autonomous-task-v2.construction.scripts.hash_utils import sha256_file; print(sha256_file('experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/T1-PILOT-TASK.md'))"` (adjust for actual importability — a plain relative script invocation is fine since this is a standalone tool, not part of the installed package) — Expected: a 64-hex-char digest, run once per pilot file.

- [ ] **Step 3: Write `PILOT-TASK-MANIFEST.md`**

Record for each of the 3 pilot tasks: `pilot_id` (T1/T2/T3), task file path + sha256, oracle file path + sha256 (or `INADMISSIBLE` + reason for T3 if applicable), and the overall `pilot_manifest_sha256` computed via `sha256_manifest()` over the three (or two, if T3 inadmissible) records.

- [ ] **Step 4: Freeze — no further edits to pilot files after this point**

State explicitly in the manifest file: "Frozen at `<ISO 8601 timestamp>`. No further edits to pilot task/oracle content after this hash was computed." This is a documentation commitment, not a filesystem lock, but the chronology matters for the lock record's audit trail.

---

## Task 5-10: Author Tranche-1 candidate pool (6 cells x 3 candidates = 18)

Six sub-tasks, one per cell, each independently completable and independently reviewable:

- **Task 5:** T1 MEDIUM x3 — `tranche1/candidates/T1M-<id>.md` x3
- **Task 6:** T1 HIGH x3 — `tranche1/candidates/T1H-<id>.md` x3
- **Task 7:** T2 MEDIUM x3 — `tranche1/candidates/T2M-<id>.md` x3
- **Task 8:** T2 HIGH x3 — `tranche1/candidates/T2H-<id>.md` x3
- **Task 9:** T3 MEDIUM x3 (parameterized specs) — `tranche1/candidates/T3M-<id>.md` x3
- **Task 10:** T3 HIGH x3 (parameterized specs) — `tranche1/candidates/T3H-<id>.md` x3

**Files (per sub-task):** 3 candidate files under `experiments/evaluation-design-e3-autonomous-task-v2/construction/tranche1/candidates/`.

**Interfaces:**
- Consumes: frozen-SHA substrate (same three files as pilot tasks, but *different concrete edit requests* than the pilot — pilot tasks are disposable and must never reappear as main candidates), the schema from `AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md:242-265` (quoted in `00-HANDOFF-VERIFICATION.md` is not — pull directly from `PROTOCOL-DRAFT.md`), the qualification checklists from `TASK-CONSTRUCTION.md`.
- Produces: candidate records consumed by Task 11 (Tranche-1 manifest freeze).

**Required fields per T1/T2 candidate file** (frontmatter or structured Markdown, machine-parseable):
```
candidate_id: <arbitrary, non-semantic, e.g. T1M-K7Q>
family: T1|T2
complexity_level: MEDIUM|HIGH
task_text: |
  <full visible task text>
task_text_sha256: <computed>
oracle_spec: |
  <full hidden oracle spec: what it checks, why, exact commands>
oracle_spec_sha256: <computed>
complexity_breakdown: |
  <rubric justifying MEDIUM vs HIGH for this candidate>
complexity_breakdown_sha256: <computed>
initial_state_or_fixture_spec: |
  <fixture/starting-state requirement, or "frozen SHA repo state, no fixture">
initial_state_or_fixture_spec_sha256: <computed>
qualification: ADMISSIBLE | INADMISSIBLE — <reason>
```

**Required fields per T3 candidate file** (parameterized spec, per `TASK-CONSTRUCTION.md`):
```
candidate_id: <arbitrary>
family: T3
complexity_level: MEDIUM|HIGH
source_workflow_or_operation: <specific>
verified_failed_boundary: <which validator, which step>
pre_failure_completed_work_expectations: <what must survive resume>
failure_producing_condition: <specific>
recovery_invocation: <exact command>
resume_expectations: <specific>
protected_work: <specific>
forbidden_reset_restart_behavior: <specific>
idempotency_expectations: <specific>
oracle_requirements: <specific>
complexity_breakdown: <rubric>
initial_state_specification: <specific>
spec_sha256: <sha256 over the whole canonical record>
qualification: ADMISSIBLE | INADMISSIBLE — <reason>
```

- [ ] **Step 1 (each sub-task): Draft 3 distinct candidates for the cell** — grounded in the frozen-SHA substrate, each requiring genuinely different task text/oracle/fixture from its siblings (not superficial rewordings), and distinct from both the pilot task and from every other cell already authored in this tranche.
- [ ] **Step 2 (each sub-task): Qualify each of the 3 against the T1/T2/T3 checklist** — mark ADMISSIBLE or INADMISSIBLE; discard and re-author any INADMISSIBLE candidate before moving on (never leave a cell with fewer than 3 admissible candidates).
- [ ] **Step 3 (each sub-task): Compute and fill in all sha256 fields** using `hash_utils.py`.
- [ ] **Step 4 (each sub-task): Verify no candidate_id collides** with any other candidate_id already used across pilot tasks or this tranche so far.

---

## Task 11: Freeze the Tranche-1 candidate manifest

**Files:**
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/tranche1/TRANCHE1-CANDIDATE-MANIFEST.md`
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/scripts/freeze_manifest.py`

**Interfaces:**
- Consumes: all 18 Tranche-1 candidate files from Tasks 5-10.
- Produces: `tranche1_manifest_sha256` — consumed by Task 15 (salt generation must happen strictly after this).

- [ ] **Step 1: Write `freeze_manifest.py`**

```python
"""Freeze a candidates/ directory into a manifest + sha256, per the
Autonomous Task v2 commit-then-salt chronology. Must be run exactly once
per tranche, after all candidates in that tranche are authored and
individually qualified ADMISSIBLE."""
import json
import sys
from pathlib import Path
from hash_utils import sha256_manifest

def load_candidate_record(path: Path) -> dict:
    # Parses the structured Markdown/YAML-frontmatter candidate file into
    # a dict with the required fields (candidate_id, family, level, and
    # the four/one sha256 fields). Raises if qualification != ADMISSIBLE
    # or any required sha256 field is missing.
    ...

def main(candidates_dir: str, out_path: str) -> None:
    records = [load_candidate_record(p) for p in sorted(Path(candidates_dir).glob("*.md"))]
    assert len(records) == 18, f"expected 18 admissible candidates, found {len(records)}"
    manifest_hash = sha256_manifest(records)
    Path(out_path).write_text(
        json.dumps({"manifest_hash": manifest_hash, "records": records}, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(manifest_hash)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

(Fill in `load_candidate_record`'s actual parser once the candidate file format from Task 5 is finalized — this is the one piece intentionally left to implementation time since it depends on exact frontmatter syntax chosen, not a placeholder for logic that should already be decided.)

- [ ] **Step 2: Run it** — `python construction/scripts/freeze_manifest.py construction/tranche1/candidates construction/tranche1/.manifest.json` — Expected: prints a 64-hex-char `tranche1_manifest_sha256`, exits 0, and errors loudly (non-zero exit) if fewer than 18 records or any non-ADMISSIBLE record is found.
- [ ] **Step 3: Write `TRANCHE1-CANDIDATE-MANIFEST.md`** — human-readable table of all 18 `(candidate_id, family, level, task_text_sha256 or spec_sha256)` rows plus the top-level `tranche1_manifest_sha256`, with a "Frozen at `<timestamp>`" line.
- [ ] **Step 4: Freeze** — no further edits to any Tranche-1 candidate file after this point.

---

## Task 12-17: Author Tranche-2 candidate pool (fresh set, 6 cells x 3 = 18)

Same structure as Tasks 5-10, but authored **now**, before any pilot or Tranche-1 outcome exists, using different concrete edit requests than both the pilot tasks and every Tranche-1 candidate (same substrate files are reusable — the design package doesn't forbid reusing the *files*, only forbids reusing the *pilot* tasks as main candidates and forbids duplicate `candidate_id`s).

- **Task 12:** T1 MEDIUM x3 → `tranche2/candidates/`
- **Task 13:** T1 HIGH x3
- **Task 14:** T2 MEDIUM x3
- **Task 15:** T2 HIGH x3
- **Task 16:** T3 MEDIUM x3 (specs)
- **Task 17:** T3 HIGH x3 (specs)

(Renumbered from the original Task 15 slot for salts — salt generation is now Task 19 below to keep this block contiguous.)

Same field schema, same per-sub-task steps as Tasks 5-10.

---

## Task 18: Freeze the Tranche-2 candidate manifest

**Files:**
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/tranche2/TRANCHE2-CANDIDATE-MANIFEST.md`

**Interfaces:**
- Consumes: all 18 Tranche-2 candidate files from Tasks 12-17, reusing `freeze_manifest.py` from Task 11.
- Produces: `tranche2_manifest_sha256`.

- [ ] **Step 1:** Run `python construction/scripts/freeze_manifest.py construction/tranche2/candidates construction/tranche2/.manifest.json`.
- [ ] **Step 2:** Write `TRANCHE2-CANDIDATE-MANIFEST.md` (same shape as Task 11 Step 3).
- [ ] **Step 3:** Freeze — no further edits to any Tranche-2 candidate file after this point.

---

## Task 19: Generate independent salts and apply the frozen ranking formula

**Files:**
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/scripts/generate_salts_and_rankings.py`
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/AUTONOMOUS-TASK-V2-RANKINGS.md`

**Interfaces:**
- Consumes: `tranche1_manifest_sha256` and `tranche2_manifest_sha256` (must both exist — Tasks 11 and 18 must be complete before this task starts, per the chronology constraint).
- Produces: `salt`, `salt_2` (hex-encoded random bytes), and the full Rank 1/2/3 ordering per cell for both tranches — consumed by Task 22 (lock record) and, for T3-survives-pilot materialization, by a future (out-of-scope-for-this-plan) session.

- [ ] **Step 1: Write `generate_salts_and_rankings.py`**

```python
"""Post-manifest-freeze salt generation and deterministic ranking, per
AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md:282-291.

rank_key(candidate_id) = sha256(manifest_hash_hex + salt_hex + candidate_id)
ascending, within each (family, level) cell.
"""
import json
import secrets
from pathlib import Path
from hash_utils import sha256_text

def generate_salt() -> str:
    return secrets.token_hex(32)

def rank_candidates(manifest_hash: str, salt: str, records: list[dict]) -> dict:
    by_cell: dict[tuple[str, str], list[dict]] = {}
    for r in records:
        by_cell.setdefault((r["family"], r["complexity_level"]), []).append(r)
    ranking = {}
    for cell, cands in by_cell.items():
        keyed = sorted(
            cands,
            key=lambda r: sha256_text(manifest_hash + salt + r["candidate_id"]),
        )
        ranking["-".join(cell)] = [c["candidate_id"] for c in keyed]
    return ranking

def main(manifest_json_path: str, out_path: str) -> None:
    manifest = json.loads(Path(manifest_json_path).read_text(encoding="utf-8"))
    salt = generate_salt()
    ranking = rank_candidates(manifest["manifest_hash"], salt, manifest["records"])
    Path(out_path).write_text(
        json.dumps({"manifest_hash": manifest["manifest_hash"], "salt": salt, "ranking": ranking}, indent=2, sort_keys=True),
        encoding="utf-8",
    )

if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2])
```

- [ ] **Step 2: Run once for Tranche 1** — `python construction/scripts/generate_salts_and_rankings.py construction/tranche1/.manifest.json construction/tranche1/.ranking.json` — Expected: exits 0, produces a `salt` and 6 cells each with exactly 3 ranked `candidate_id`s.
- [ ] **Step 3: Run once for Tranche 2** — same command against `tranche2/.manifest.json` → `tranche2/.ranking.json`.
- [ ] **Step 4: Write `AUTONOMOUS-TASK-V2-RANKINGS.md`** — records both salts, both manifest hashes referenced, the full Rank 1/2/3 table per cell per tranche, and a chronology line proving both manifests were frozen (Tasks 11, 18) before either salt was generated (file mtimes plus explicit "Frozen at" timestamps from those tasks).
- [ ] **Step 5: Freeze** — salts and rankings are final; do not regenerate even if a ranking result seems inconvenient.

---

## Task 20: Freeze all three dispatch seeds

**Files:**
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/scripts/generate_dispatch_seeds.py`
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/AUTONOMOUS-TASK-V2-DISPATCH-SEEDS.md`

**Interfaces:**
- Consumes: nothing outcome-dependent (seeds are independent of manifest/ranking content by design — only their *use*, seeded Fisher-Yates over the (task, regime) pairs, is deferred to actual dispatch time, which this plan does not reach).
- Produces: `seed_pilot_dispatch`, `seed_tranche1_dispatch`, `seed_tranche2_dispatch` — consumed by the lock record (Task 22) and by a future dispatch session, never by this one.

- [ ] **Step 1: Write `generate_dispatch_seeds.py`**

```python
import secrets

def main() -> None:
    for name in ("seed_pilot_dispatch", "seed_tranche1_dispatch", "seed_tranche2_dispatch"):
        print(f"{name}={secrets.token_hex(16)}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it once** — `python construction/scripts/generate_dispatch_seeds.py` — Expected: exactly 3 lines, each a `name=32-hex-char` pair.
- [ ] **Step 3: Write `AUTONOMOUS-TASK-V2-DISPATCH-SEEDS.md`** — records all three seed values, generation timestamp, and the seeded Fisher-Yates procedure reference (`PROTOCOL-DRAFT.md:338-341`) that will consume them at actual dispatch time (not now).
- [ ] **Step 4: Freeze** — these three values are final for this experiment; do not regenerate on later activation of Tranche 2 (activation controls *use*, not *generation*, per the design package).

---

## Task 21: Agent/evaluator bundle separation for the pilot package + audit

**Files:**
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/bundles/agent-visible/` (3 files: task text only, per pilot task)
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/bundles/evaluator-only/` (3 files: oracle spec, per pilot task)
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/bundles/BUNDLE-SEPARATION-AUDIT.md`

**Interfaces:**
- Consumes: `T1/T2/T3-PILOT-TASK.md` and `-ORACLE.md` from Tasks 1-3 (frozen by Task 4).
- Produces: two hash-verified, mutually exclusive bundles — consumed by Task 22 (real preflight run) via `--task-bundle`/`--task-bundle-sha256`.

- [ ] **Step 1: Extract agent-visible content** — copy *only* the visible task-contract text from each `*-PILOT-TASK.md` into `bundles/agent-visible/<pilot_id>.md`, stripping any qualification notes or internal commentary.
- [ ] **Step 2: Extract evaluator-only content** — copy the oracle spec into `bundles/evaluator-only/<pilot_id>.md`.
- [ ] **Step 3: Audit for leakage** — grep every file in `bundles/agent-visible/` for oracle-spec terms/phrases that appear in the corresponding `bundles/evaluator-only/` file (exact-substring check of any sentence >8 words); any hit is a leakage finding that must be fixed before proceeding.
- [ ] **Step 4: Write `BUNDLE-SEPARATION-AUDIT.md`** recording the check performed, its result, and the sha256 of each bundle file (via `hash_utils.sha256_file`).

---

## Task 22: Run the real preflight against the locked pilot package

**Files:**
- Modify (invoke, not edit): `experiments/evaluation-design-e3-autonomous-task-v2/AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh`
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/PREFLIGHT-RESULT.md`

**Interfaces:**
- Consumes: a real standalone clone at the frozen SHA (must be created fresh, not this working tree — see Global Constraints), the agent-visible bundle from Task 21, an oracle self-test command, a fresh run-state dir.
- Produces: the preflight's pass/fail/unverifiable report, consumed by Task 23 (lock record).

- [ ] **Step 1: Create a real standalone clone at the frozen SHA** — `git clone --no-local <this-repo-remote-or-path> <fresh-dir> && cd <fresh-dir> && git checkout 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5` (use `--no-local` / a proper `file://` or remote URL, not a plain local path copy, so the `no-known-sibling-experiment-dirs` and `clone-remote-has-no-local-path` checks are meaningfully exercised rather than trivially passed).
- [ ] **Step 2: Construct the oracle self-test command** for at least one pilot task (e.g., T2's `pytest tests/test_field_contract_agreement.py` against the unmodified fixture — expected to reflect the *unsolved* state) and compute `--expected-oracle-self-test-sha`.
- [ ] **Step 3: Run the gate** — `bash AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh --clone-dir <fresh-dir> --frozen-sha 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5 --run-state-dir <fresh-run-state-dir> --task-bundle <agent-visible-bundle-path> --task-bundle-sha256 <sha> --oracle-self-test-command "<cmd>" --expected-oracle-self-test-sha <sha>` — Expected per the script's own logic: `FAIL_COUNT == 0 AND UNVERIFIABLE_COUNT == 0`, exit code 0, with the `ambient-scope-runtime-enforcement` line always reporting `ENV_LIMIT: AMBIENT_SCOPE_NOT_TECHNICALLY_ENFORCED` (this is expected and not a failure — it's a disclosure, per the script's own design).
- [ ] **Step 4: If it fails or reports UNVERIFIABLE** — fix the actual condition (missing arg, dirty clone, wrong SHA, etc.) and rerun; do not waive per the script's explicit no-waiver design. Record every attempt in `PREFLIGHT-RESULT.md`.
- [ ] **Step 5: Record the final clean result** in `PREFLIGHT-RESULT.md` with full command line, full output, exit code, and timestamp.

---

## Task 23: Construct `AUTONOMOUS-TASK-V2-LOCK-RECORD.md`

**Files:**
- Create: `experiments/evaluation-design-e3-autonomous-task-v2/construction/AUTONOMOUS-TASK-V2-LOCK-RECORD.md`

**Interfaces:**
- Consumes: every artifact produced by Tasks 0 (handoff) through 22 (preflight) — this is a pure aggregation task, not new construction.
- Produces: the final deliverable; its completion is the only thing that permits the terminal status `PILOT LOCKED`.

- [ ] **Step 1: Aggregate source identity** — repo, frozen SHA, isolation/M4 status (`MITIGATED, AUDITABLE, NOT TECHNICALLY CLOSED`, unchanged).
- [ ] **Step 2: Aggregate normative artifact hashes** — sha256 of all 17 reviewed-package files plus this session's `00-HANDOFF-VERIFICATION.md`.
- [ ] **Step 3: Aggregate regime hashes** — R0/R1/R2 file hashes, R1/R2 shared-block hash (already known: `a19c6c2c...0cde4c`).
- [ ] **Step 4: Aggregate pilot identity** — `pilot_manifest_sha256` (Task 4), T3 admissible/inadmissible status (Task 3), bundle separation audit result (Task 21).
- [ ] **Step 5: Aggregate main-study pools** — `tranche1_manifest_sha256`, `tranche2_manifest_sha256` (Tasks 11, 18), full candidate commitment tables.
- [ ] **Step 6: Aggregate selection state** — both salts, both full rankings, chronology proof (Task 19).
- [ ] **Step 7: Aggregate dispatch state** — all three seeds (Task 20).
- [ ] **Step 8: Aggregate preflight evidence** — Task 22's final clean result.
- [ ] **Step 9: Write the chronology section** — an explicit, timestamp-ordered list proving: candidates authored/qualified before manifest freeze; manifests frozen before salts; salts/rankings before seeds (or documented as independent/concurrent, per Global Constraints — seeds don't depend on rankings); everything before the preflight run; preflight before this lock record.
- [ ] **Step 10: Declare the terminal status** — exactly one of `PILOT LOCKED`, `CHANGES REQUIRED BEFORE PILOT LOCK`, or `EXPERIMENT NOT ADMISSIBLE AT THIS FROZEN SHA`, based on whether every prior task actually completed cleanly (e.g., if T3 pilot was ruled inadmissible, this is still compatible with `PILOT LOCKED` under the T1/T2-only fallback — but must say so explicitly, per `PILOT-INSTRUMENT-VALID-WITH-FAMILY-DROPPED` framing applied pre-emptively to construction, not pilot outcome).

---

## Self-Review Notes (applied while writing this plan)

- **Spec coverage:** Every phase in the owner's Phase 0-14 instructions maps to a task above (Phase 0→00-HANDOFF+this plan header, Phases 1-2→Tasks 1-3 role/scope discipline embedded in Global Constraints, Phase 3→Tasks 1-3, Phase 4→Tasks 5-18, Phase 5-6→qualification steps within Tasks 5-18, Phase 7→Tasks 11+18, Phase 8→Task 19, Phase 9→Task 20, Phase 10→fallback mapping documented in Task 23 Step 10, Phase 11→Task 21, Phase 12→Task 22, Phase 13→Task 23). Phases 14+ (actual pilot execution, adjudication, Tranche 1 authorization/execution) are explicitly out of scope for this plan — this plan stops at Task 23.
- **Placeholder scan:** `freeze_manifest.py`'s `load_candidate_record` body is intentionally deferred to implementation time because it depends on the exact candidate-file frontmatter format chosen during Task 5 — this is a real, load-bearing decision left to the task that has the information to make it correctly, not a "TODO: handle it later" placeholder. Every other code block is complete and runnable as written.
- **Type consistency:** `sha256_manifest(records)` (Task 4) and `rank_candidates(manifest_hash, salt, records)` (Task 19) both consume the same `records: list[dict]` shape with `candidate_id`/`family`/`complexity_level` keys, consistent with the schema defined in Tasks 5-10.
