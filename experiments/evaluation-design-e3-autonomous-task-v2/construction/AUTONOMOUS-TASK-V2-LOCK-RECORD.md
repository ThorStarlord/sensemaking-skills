# Autonomous Task v2 — Lock Record

Pure aggregation of everything produced by Tasks 0 (handoff) through 22
(preflight). No new construction happens in this document.

## 1. Source identity

```
repository: ThorStarlord/sensemaking-skills
frozen SHA: 0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5
```

Isolation / M4 status, unchanged from the design package
(`AUTONOMOUS-TASK-V2-AMBIENT-ISOLATION-AUDIT.md:159`):

```
MITIGATED, AUDITABLE, NOT TECHNICALLY CLOSED
```

## 2. Normative artifact hashes

The 17-file design-review package (read from
`experiments/evaluation-design-e3-autonomous-task-v2/` — never committed
into this isolated construction worktree's own history; see
`00-HANDOFF-VERIFICATION.md` §1), sha256, raw UTF-8 bytes:

| file | sha256 |
|---|---|
| AUTONOMOUS-TASK-V2-AMBIENT-ISOLATION-AUDIT.md | `7875d6d5e98c791bdabb37f36bfb29094af26a90f25d98792b1df0fece2119f6` |
| AUTONOMOUS-TASK-V2-DESIGN-OPTIONS.md | `0dc541ef0206eed7c8154dba448a393718fe0314c5302a20ad8ad0c15437032e` |
| AUTONOMOUS-TASK-V2-DESIGN-REVIEW.md | `9f1b75367913487a4d87510545160cc8bf00f2e1c86b88fa0ea7582391b2d818` |
| AUTONOMOUS-TASK-V2-EVALUATOR-SCORECARD.md | `6bcdce4dc7d87d7a1766e51b7189a043eb2b66a967302fa344a74dcd64d34931` |
| AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md | `dc453c59c4e3a4ed35832e20e570cf580fbda79d7c26fdc28ab88667a3256e35` |
| AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-2.md | `71c580059829e366daa3125a9dbf68066e444fdeaf630f8813b9025e5be94c62` |
| AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-3.md | `18ccce598fc70f5fc504f31e8b5eb88a49c72d024de87c990a59409c9bbfab32` |
| AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-4.md | `11984c22057e1907edf609b7ce0abf8d87765c97d17f44e5963d9b5453c9e5e6` |
| AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE.md | `bff26dc0fa96865b958378854124d2dc9f20085bd6da8391866af402b4a3433f` |
| AUTONOMOUS-TASK-V2-PILOT-PLAN.md | `8709933ed4a906bef77eea4dceae298f0b41eca01f8993b1e0e7f836e2dd25e0` |
| AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh | `6bf4db6b434b4dfef9a3d606234c4b9995ebb604695cb0e8cddfdf2af231ce2f` |
| AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md | `c93adc8bb7f19c1af32a4f6639c991bdcbc820278a8122ecb8e76dd052b19750` |
| AUTONOMOUS-TASK-V2-REGIME-R0-ROBUST.txt | `5cab71b47464ddeb4e3537d26dd58540bd88249b6f44d319f46ca008c0585ea9` |
| AUTONOMOUS-TASK-V2-REGIME-R1-LEAN.txt | `6a7147cdfb726fc6a2f216dd39fdf3335daad08447a98178b5ae7b2dd24f4861` |
| AUTONOMOUS-TASK-V2-REGIME-R2-ESCALATION.txt | `ab94cc5480a8e4410bcc9df1f788f36f622625c277b8c917170caf8e568e3714` |
| AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md | `7a1c6ae78e63164a1f6452c634292ae35a5db0dc8c39bbfeb1aa0293735ad6b7` |
| AUTONOMOUS-TASK-V2-TELEMETRY-SCHEMA.md | `9118a373403d3749ba272c2697cf3507e5037f8141cf6ef3523126bf6a0e4a81` |

Plus this session's own handoff record:

```
00-HANDOFF-VERIFICATION.md sha256 = e8907d091059e4449a97962e04ac0b8b2ef34c6b9cdbd6907527271470548068
```

## 3. Regime hashes

Matches the preflight gate's own independent re-computation at Task 22
(`regime-file-present:*` PASS lines) — same three values, confirmed
twice via two different mechanisms:

```
R0-ROBUST     sha256 = 5cab71b47464ddeb4e3537d26dd58540bd88249b6f44d319f46ca008c0585ea9
R1-LEAN       sha256 = 6a7147cdfb726fc6a2f216dd39fdf3335daad08447a98178b5ae7b2dd24f4861
R2-ESCALATION sha256 = ab94cc5480a8e4410bcc9df1f788f36f622625c277b8c917170caf8e568e3714
```

R1/R2 shared execution-discipline block (items 1-10, lines 3-64 of each
file), confirmed byte-identical at Phase 0 handoff and matching the
design package's own recorded value
(`LOCK-READINESS-RESPONSE-4.md` §1):

```
shared_block_sha256 = a19c6c2c...0cde4c
```

## 4. Pilot identity

```
pilot_manifest_sha256 = d6988ce3acd91bf361b6c63963760262620d089e59033a476238afabf9a7f317
```

All three pilot families (T1, T2, T3) are **ADMISSIBLE** — see
`pilot/PILOT-TASK-MANIFEST.md`. T3's oracle underwent one honest
correction during construction (before the manifest's final freeze — see
that file's own correction record: a run-log-vs-ledger misunderstanding
and a pre-existing-dogfood-directory collision, both found by actually
re-running the recovery sequence, not by re-reading prose) before landing
at the hash above.

Bundle separation audit (Task 21):

```
agent-visible T1 sha256 = 33861682d93c8da480f5bfa3868a000933c77479039eb6284aad636b601b25fb
agent-visible T2 sha256 = 021fcd90156be5c0e87ead018a22d2353620c123765c728c89a8f9018546f525
agent-visible T3 sha256 = 0dce1a825a4e7461c45177f9237892954ce799778a2c032c48a2c3bea90f0f86
evaluator-only T1 sha256 = e4087cb8fbf3d7acaf8a2a1569501765f51e5477a05111a79f45f5fba8ef9902
evaluator-only T2 sha256 = 6e1ef949c962bef21a3562f972dbeecd448746be51ee5d1d9edaf9897d57df30
evaluator-only T3 sha256 = 6e434388da98efb1db979667981a11cae0891b0d52dcf8592b8956f1d2e535e8
```

Leakage audit result: **0 findings** (no oracle sentence over 8 words
appears verbatim in any agent-visible bundle).

## 5. Main-study pools

```
tranche1_manifest_sha256 = bed02782df1c7de194cd249fec9f73ec8432bdb5ab2bcf709c356c74885c0c31
tranche2_manifest_sha256 = f6a08e991956efc646a9f287c12e728597922cb23acd81adadc1651212e56a19
```

Tranche 1's manifest was re-frozen once, from an original hash of
`a01326106c91cafee766f55af35f5a112b68e18c59dd8386ba243d279addabef`,
after three real defects were found and fixed in already-frozen T3M
content (K7X, P4W, R2B) — a `proposed_direction` bootstrap deadlock, a
missing git-commit precondition, and a false run-log-preservation claim —
all discovered while constructing and reviewing Tranche 2's parallel T3
cell, all empirically reproduced before being fixed, all independently
re-verified after. See `tranche1/TRANCHE1-CANDIDATE-MANIFEST.md`'s
correction record for the full account. This happened before any
salt/ranking existed for either tranche — consistent with the
commit-then-salt chronology below.

Full candidate commitment tables (18 candidates × 2 tranches = 36 total,
6 cells × 3 each, no `candidate_id` collision within or across tranches):
`tranche1/TRANCHE1-CANDIDATE-MANIFEST.md`,
`tranche2/TRANCHE2-CANDIDATE-MANIFEST.md`.

T3 (both tranches) remains **pilot-conditional**: these 12 T3 specs are
parameterized, not materialized, and are only promoted into main-study
tasks if the disposable T3 pilot's outcome (a future, out-of-scope-for-
this-plan pilot execution) confirms admissibility. If it does not, the
already-frozen T1/T2-only fallback mapping applies and these specs are
never promoted.

## 6. Selection state

```
tranche1 salt = d7b1cc19908504e97f3620fa933dbc550d0dc515316ecec4ef93cc2dc4541763
tranche2 salt = 01a9c40dc537ef1393022981e9b9aa50853862a0057814b686980907ead5e2d7
```

Full per-cell Rank 1/2/3 ordering for both tranches:
`AUTONOMOUS-TASK-V2-RANKINGS.md`.

Chronology proof (see also §9 below): both manifests were frozen and
committed strictly before either salt was generated — Tranche-1's
manifest was committed at 2026-08-20 21:52:10 -03:00 (re-freeze, commit
`80a1324`), Tranche-2's at 21:53:56 -03:00 (commit `6c908cb`); salt
generation (commit `86ceaeb`) landed at 21:55:07 -03:00, strictly after
both.

## 7. Dispatch state

```
seed_pilot_dispatch    = 0ab5cab61c1703f51f583d2ca527c9c3
seed_tranche1_dispatch = c20edf2241fb8755dc09ec0cf1d7c255
seed_tranche2_dispatch = a4c5145d9078b1e2d4210d1268789f26
```

Independent of manifest/ranking content by design (cryptographic random
bytes, `secrets.token_hex(16)`) — only their *use* (a seeded Fisher-Yates
shuffle over `(task, regime)` pairs) is deferred to a future dispatch
session, out of scope here. See `AUTONOMOUS-TASK-V2-DISPATCH-SEEDS.md`.

## 8. Preflight evidence

Task 22's final result: **CLEAN**. `PASS=17 FAIL=0 UNVERIFIABLE=0`, exit
code 0, against a real standalone clone at the frozen SHA. One genuine
failure was found and fixed on the first attempt (a non-deterministic
self-test command construction, not a gate defect or an environment
limitation) before the clean final run — no waiver was used or available.
Full record, both attempts: `PREFLIGHT-RESULT.md`.

## 9. Chronology

Timestamps from this branch's own commit history
(`git log -- experiments/evaluation-design-e3-autonomous-task-v2/construction/`),
all times `-03:00`:

| Event | Commit | Timestamp |
|---|---|---|
| Phase 0 handoff verified; pilot tasks 1-3 authored, admissible | `2eadb6d` | 2026-08-19 19:33:01 |
| Pilot manifest frozen (Task 4) | `2eadb6d` | 2026-08-19 19:33:01 |
| Tranche-1 candidate cells authored (Tasks 5-10) | `190105b` … `428c8a1` | 2026-08-19 20:18:29 → 2026-08-20 06:33:12 |
| Tranche-1 manifest frozen (Task 11) | `652e0ee` | 2026-08-20 06:34:53 |
| Tranche-2 candidate cells authored (Tasks 12-17) | `ec097e3` … `f639e7b` | 2026-08-20 11:21:13 → 2026-08-20 20:28:46 |
| Defects found in frozen T3M-K7X/P4W/R2B during Tranche-2 T3 construction; fixed | `8ce3d8c` | 2026-08-20 21:51:10 |
| Tranche-1 manifest **re-frozen** (post-fix) | `80a1324` | 2026-08-20 21:52:10 |
| Tranche-2 manifest frozen (Task 18) | `6c908cb` | 2026-08-20 21:53:56 |
| Salts and rankings generated (Task 19) | `86ceaeb` | 2026-08-20 21:55:07 |
| Dispatch seeds generated (Task 20) | `4961ac9` | 2026-08-20 21:55:40 |
| Pilot bundle separation + leakage audit (Task 21) | `d6d9641` | 2026-08-20 21:58:04 |
| Real preflight run, clean (Task 22) | `65bc519` | 2026-08-20 22:03:48 |
| This lock record (Task 23) | (this commit) | (see commit timestamp) |

This chronology establishes, in order:

1. **Candidates authored/qualified before manifest freeze** — every
   Tranche-1 cell (5-10) landed before `652e0ee` (Task 11); every
   Tranche-2 cell (12-17) landed before `6c908cb` (Task 18). The one
   post-freeze content change (the K7X/P4W/R2B defect fix) happened
   *before* the corresponding re-freeze commit (`80a1324`), not after —
   the manifest hash in circulation always reflects the actual, current
   candidate content.
2. **Manifests frozen before salts** — both `80a1324` (21:52:10) and
   `6c908cb` (21:53:56) precede `86ceaeb` (21:55:07).
3. **Salts/rankings before seeds** — `86ceaeb` (21:55:07) precedes
   `4961ac9` (21:55:40). (Per Global Constraints, seeds don't actually
   depend on ranking content — this ordering is incidental, not a hard
   requirement, but holds here anyway.)
4. **Everything before the preflight run** — `65bc519` (22:03:48) is the
   last commit before this one.
5. **Preflight before this lock record** — this document is written and
   committed after `65bc519`.

## 10. Terminal status

Every task from Phase 0 through Task 22 completed cleanly: all pilot
families ADMISSIBLE (with one honest, pre-freeze correction, fully
disclosed); both main-study tranches fully authored, independently
reviewed, and frozen (with one honest, pre-freeze-of-the-next-artifact
correction to already-frozen T3M content, fully disclosed and re-frozen
before this lock record); salts, rankings, and dispatch seeds generated
after their required predecessors; bundle separation audited with zero
leakage; the real preflight gate returned a clean result with zero
failures and zero unverifiable checks.

```
PILOT LOCKED
```

T3 (both tranches, 12 specs total) remains explicitly **pilot-conditional**
per §5 above — this status does not itself constitute a T3 pilot
admissibility determination (that requires actually running the disposable
T3 pilot, out of scope for this plan). If a future T3 pilot execution
rules T3 inadmissible at this frozen SHA, this lock record's status is
still compatible with `PILOT LOCKED` under the already-frozen T1/T2-only
fallback mapping — per `PILOT-INSTRUMENT-VALID-WITH-FAMILY-DROPPED`
framing, applied here pre-emptively to construction, not to a pilot
outcome that has not yet occurred.

Phases 14 and beyond — actual pilot execution, adjudication, and
Tranche-1/Tranche-2 authorization/execution — are explicitly out of scope
for this plan and are not addressed by this lock record.
