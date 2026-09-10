# Status

**Version:** 0.3.0  
**Last updated:** 2026-09-10  
**Current phase:** PM Customer Discovery repository milestone complete; engineering and PM empirical external qualification remain pending  
**Primary program:** Sensemaking Campaign productization with separately authorized agent-agnostic PM domain pilot  
**Current implementation frontier:** `main@e7d213e07976a2f269b1479fcc36decdcf0cdeb4` (merge of PR #309)  
**Current frontier:** no pre-authorized repository implementation package; next work depends on real-harness evidence or another separately authorized objective

Sensemaking Skills is an **agent-native engineering sensemaking and control layer** whose Campaign substrate now has one repository-implemented, coding-agent-agnostic Product Management vertical slice. The active coding agent owns semantic judgment; deterministic machinery owns representation, persistence, validation, provenance, integrity, authority checks, target identity, evidence binding, and reconstructible state.

## Current PM Customer Discovery milestone

The separately authorized PM milestone is repository-complete.

| Package | PR | Exact final candidate head | Merge commit | Delivered |
|---|---:|---|---|---|
| Package 1 — Agent-Agnostic PM Domain Contract & Migration Ledger | #307 | `967bff480d8681290bc294608695677c06bdb4f5` | `539f85e9f55bae6e1e2b1d190aa5c7395ea19d5f` | Pinned the 27-command upstream provenance, defined PM responsibility/evidence/automation semantics, accepted ADR 0028, and made harness independence a product invariant. |
| Package 2 — Canonical Customer Discovery Capabilities | #308 | `9235e4e550956d9767c2602216eee54274792077` | `a65e596e8afe4e6991be0bbaea4b9427a2ee6de7` | Added canonical `persona`, `discovery`, `interview-synthesis`, `opportunity-tree`, and `hypothesis` Skill trees with evidence-aware methodology/output contracts and no Claude/Codex/OpenCode semantic coupling. |
| Package 3 — Artifact, Campaign & Adapter Integration | #309 | `897e5850a4ab229eeb2c00e23d91339c3bf8e884` | `e7d213e07976a2f269b1479fcc36decdcf0cdeb4` | Added specialized PM artifact validation, Campaign capability registration and admission coverage, multi-adapter canonical-byte parity tests, bounded Customer Discovery workflow semantics, and real-harness dogfood protocol. |

Package 3's final exact candidate passed Product Validation, Lab Validation, and Release Candidate Distribution. Its first candidate (`e88bb904...`) exposed one stale regression test that still expected `discovery_findings` to use the generic validator; the repair moved generic-fallback coverage to `session_summary` rather than weakening the new PM contract.

The canonical PM responsibility slice is:

```text
customer_understanding
-> problem_discovery
-> research_synthesis
-> opportunity_mapping
-> product_hypothesis
```

The implemented Skills are agent-agnostic semantic sources. Existing harness setup machinery renders/copies those same canonical trees into supported discovery roots. Structural parity is tested; native invocation is not yet empirically proven.

See `docs/product-management/milestone-handoff.md` for the full PM handoff and `docs/product-management/dogfood/STATUS.md` for empirical status.

## Two independent empirical gates remain

### 1. Engineering v0.3 external golden path

The existing engineering qualification status remains unchanged:

```text
Checked-in real-harness attempts: 0
Current empirical PASS: NONE
Human/external action required for empirical PASS: YES
```

A real empirical PASS still requires an actual supported external coding-agent harness attempt frozen under `v0.3-external-golden-path-dogfood-v1` and verified against the exact frozen attempt bytes.

### 2. PM Customer Discovery functional + portability dogfood

The PM milestone also has zero checked-in native-harness attempts:

```text
Checked-in real-harness functional PM attempts: 0
Checked-in second-harness portability attempts: 0
Current functional PM empirical PASS: NONE
Current PM portability empirical PASS: NONE
External native-harness action required: YES
```

Repository-local validator tests, Campaign admission tests, wheel packaging, and canonical-byte adapter parity are not substitutes for real native harness discovery/invocation.

Follow `docs/product-management/dogfood-runbook.md`: run one real Customer Discovery responsibility/Campaign, run a fresh-context reconstruction without prior chat, then execute an equivalent bounded responsibility through a second supported harness. Preserve PASS, FAIL, or INVALID honestly.

Until that evidence exists, do not automatically migrate the remaining deferred PM commands.

## Prior completed v0.3 post-milestone

The preceding three-package milestone also remains complete:

| Package | PR | Exact candidate head | Merge commit | Delivered |
|---|---:|---|---|---|
| Post-Milestone Release Contract Reconciliation | #302 | `2cb50eae32516f716d9c62846876e67b1f5741ec` | `7e539dd88742fc7fca27e7a1368682047719bcda` | Reconciled stale v0.3/P11 release documentation and preserved exact-head/product-lab qualification boundaries. |
| Narrative Verification Receipts | #303 | `a3cede49449ad2857bc348c7ba06877acc113ac0` | `732ea14752510dc05352ddcc004010a3e2d9284c` | Added append-only receipts binding exact current Campaign narrative claims to exact durable evidence bytes without claiming semantic truth. |
| Durable Qualification Evidence Receipts | #304 | `86f9a2ec96ed58ce096c71184f03a6ff839f3473` | `cd183827b438107dafd65f48fa23145b2e21fbdd` | Added content-bound receipts for structurally valid frozen external attempts plus CI verification for future checked-in qualification evidence. |

The subsequent #305/#306 documentation handoff finalized that milestone before the separately authorized PM objective began.

## Release architecture continuity

The PM milestone extends rather than replaces the validated v0.3 release architecture:

- Campaign schema v2 remains the current durable representation baseline.
- The shipped product/lab split remains intact.
- Product Validation owns shipped/installed-product claims; retained Lab Validation owns source-only research/lab claims.
- Release Candidate Distribution proves build/install/package identities on exact candidate heads.
- The engineering external golden-path verifier remains separate from PM dogfood.
- Tagging/publication of v0.3.0 remains an explicit owner decision.

## Product and semantic boundaries

Keep these distinctions explicit:

```text
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
admitted evidence != warranted conclusion
narrative claim bound to evidence != evidence proves claim
qualification receipt != real-harness origin proof
synthetic or structural PASS != empirical native-harness PASS
canonical PM capability != harness representation
Skill copied to discovery root != harness observed or invoked Skill
lineage != semantic warrant
handoff != semantic recommendation
```

The Campaign Controller is not a semantic router.

## Current recommended next priorities

These are evidence-gated next actions, not pre-authorized implementation packages:

1. **Run genuine engineering external golden-path dogfood** under the existing `v0.3-external-golden-path-dogfood-v1` protocol.
2. **Run genuine PM Customer Discovery dogfood** under `docs/product-management/dogfood-runbook.md`, including fresh-context reconstruction and second-harness portability evidence.
3. **Derive repository changes from observed failures/results.** PASS can justify promotion/next-wave decisions; FAIL/INVALID must be preserved and should produce only the smallest evidenced repair.
4. **Do not bulk-migrate the remaining PM commands yet.** The migration ledger preserves them as deferred candidates until empirical PM evidence exists.

## Operator handoff / canonical sources

- `STATUS.md` — current cross-program state.
- `docs/product-management/milestone-handoff.md` — completed PM package evidence and next-action handoff.
- `docs/product-management/dogfood-runbook.md` — PM real-harness/fresh-context/second-harness protocol.
- `docs/product-management/dogfood/STATUS.md` — PM empirical qualification status.
- `docs/product-management/capability-migration-matrix.md` — all 27 upstream PM command dispositions.
- `docs/adr/0028-agent-agnostic-product-management-domain.md` — PM architectural authority.
- `docs/post-milestone-handoff-runbook.md` — earlier #302–#304 operational commands and evidence protocol.
- `qualification-evidence/STATUS.md` — engineering empirical external-qualification status.
- `docs/external-golden-path-verifier.md` — engineering external attempt/verifier protocol.
- `docs/milestone-runbook.md` — v0.3 baseline operations and qualification runbook.
- `docs/sensemaking-campaign.md` — canonical Campaign product model.
- `.github/workflows/validation.yml` — Product Validation authority.
- `.github/workflows/lab-validation.yml` — retained Lab Validation authority.
- `.github/workflows/release-candidate.yml` — release distribution authority.

When prose and checked-in executable validation disagree, the executable contract is authority and the documentation should be reconciled.
