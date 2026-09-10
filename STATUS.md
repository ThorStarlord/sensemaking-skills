# Status

**Version:** 0.3.0  
**Last updated:** 2026-09-10  
**Current phase:** PM repository expansion authorized under explicit qualification levels; engineering and PM empirical external qualification remain pending  
**Primary program:** Sensemaking Campaign productization with agent-agnostic Product Management domain  
**Current implementation frontier:** `main@0c4769710a5473f5a3108fd3206a8ccfd7058547` (merge of PR #311)  
**Current PM frontier:** continue remaining PM waves to `REPOSITORY_QUALIFIED`; native-harness/portability evidence remains qualification debt and promotion gate

Sensemaking Skills is an **agent-native engineering sensemaking and control layer** whose Campaign substrate now supports a repository-implemented, coding-agent-agnostic Product Management vertical slice. The active coding agent owns semantic judgment; deterministic machinery owns representation, persistence, validation, provenance, integrity, authority checks, target identity, evidence binding, and reconstructible state.

## PM maturity policy

The PM program now distinguishes implementation maturity from empirical support claims:

```text
CANDIDATE
-> REPOSITORY_QUALIFIED
-> NATIVE_HARNESS_QUALIFIED
-> PORTABILITY_QUALIFIED
-> PROMOTED
```

Repository qualification requires the relevant canonical Skill, artifact/validation contracts where applicable, rejection coverage, Campaign integration, packaging/install proof, and exact-head CI. Native-harness and second-harness evidence are still required for the corresponding stronger support/promotion claims.

The governing policy is:

```text
dogfood before promotion
!=
dogfood before expansion
```

Missing empirical qualification is tracked as visible qualification debt. It is not silently treated as PASS and no capability may claim a maturity state unsupported by preserved evidence.

See `docs/product-management/qualification-levels.md` and ADR 0028.

## Completed PM Customer Discovery slice

The first repository-qualified responsibility sequence is:

```text
customer_understanding
-> problem_discovery
-> research_synthesis
-> opportunity_mapping
-> product_hypothesis
```

with canonical Skills:

```text
persona
-> discovery
-> interview-synthesis
-> opportunity-tree
-> hypothesis
```

| Package | PR | Exact final candidate head | Merge commit | Delivered |
|---|---:|---|---|---|
| Package 1 — Agent-Agnostic PM Domain Contract & Migration Ledger | #307 | `967bff480d8681290bc294608695677c06bdb4f5` | `539f85e9f55bae6e1e2b1d190aa5c7395ea19d5f` | Pinned upstream provenance, defined PM responsibility/evidence/automation semantics, and made harness independence a product invariant. |
| Package 2 — Canonical Customer Discovery Capabilities | #308 | `9235e4e550956d9767c2602216eee54274792077` | `a65e596e8afe4e6991be0bbaea4b9427a2ee6de7` | Added canonical `persona`, `discovery`, `interview-synthesis`, `opportunity-tree`, and `hypothesis` Skill trees. |
| Package 3 — Artifact, Campaign & Adapter Integration | #309 | `897e5850a4ab229eeb2c00e23d91339c3bf8e884` | `e7d213e07976a2f269b1479fcc36decdcf0cdeb4` | Added specialized PM artifact validation, Campaign registration/admission, adapter parity tests, bounded workflow semantics, and dogfood protocol. |
| Non-qualifying PM preflight | #311 | `4809b1d3fa94396283cccbfca980f0826aaf2191` | `0c4769710a5473f5a3108fd3206a8ccfd7058547` | Preserved a Chess Mentor Engine repository-side discovery preflight while keeping real-harness attempt counts at zero. |

## Empirical gates remain open

### Engineering v0.3 external golden path

```text
Checked-in real-harness attempts: 0
Current empirical PASS: NONE
Human/external action required for empirical PASS: YES
```

A real empirical PASS still requires an actual supported external coding-agent harness attempt frozen under `v0.3-external-golden-path-dogfood-v1` and verified against the exact frozen attempt bytes.

The **real-harness qualification verifier** remains the engineering v0.3 mechanism for checking frozen external attempt packages.

### PM native-harness and portability qualification

```text
Checked-in non-qualifying PM preflights: 1
Checked-in real-harness functional PM attempts: 0
Checked-in second-harness portability attempts: 0
Current functional PM empirical PASS: NONE
Current PM portability empirical PASS: NONE
```

Repository-local validation, Campaign admission, wheel packaging, and canonical-byte adapter parity are not substitutes for real native harness discovery/invocation.

These empirical gates now limit promotion/support claims rather than blocking separately authorized repository implementation.

## Current PM implementation queue

The remaining upstream PM capability inventory is still governed by `docs/product-management/capability-migration-matrix.md`.

Authorized repository-expansion sequence:

1. **Wave 2 — Feature Definition:** reconcile upstream `prd` into current `to-prd`; adapt `user-stories`, `acceptance-criteria`, `pre-mortem`.
2. **Wave 3 — Strategy & Prioritization:** adapt `competitive-analysis`, `strategy`, `prioritize`, `north-star`, `okr`, `roadmap`, `lean-canvas`.
3. **Wave 4 — Experimentation / PMF / Pricing:** adapt `experiment-design`, `ab-test-analysis`, `measure-pmf`, `pricing` with strong evidence-status gates.
4. **Wave 5 — Customer Modeling:** adapt `customer-journey`, `ideal-customer-profile`.
5. **Wave 6 — GTM / Communication:** adapt `launch-checklist`, `gtm`, `battlecard`, `release-notes`, `stakeholder-update` while external execution remains separately authorized.

Each wave must earn `REPOSITORY_QUALIFIED` independently through exact-head CI. No wave may claim native-harness, portability, or promotion status without the corresponding empirical evidence.

## Release architecture continuity

- Campaign schema v2 remains the current durable representation baseline.
- The shipped product/lab split remains intact.
- Product Validation owns shipped/installed-product claims; retained Lab Validation owns source-only research/lab claims.
- Release Candidate Distribution proves build/install/package identities on exact candidate heads.
- The engineering external golden-path verifier remains separate from PM qualification debt.
- Tagging/publication of v0.3.0 remains an explicit owner decision.

## Product and semantic boundaries

```text
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
admitted evidence != warranted conclusion
narrative claim bound to evidence != evidence proves claim
qualification receipt != real-harness origin proof
repository qualified != native-harness qualified
native-harness qualified != portability qualified
portability qualified != promoted
canonical PM capability != harness representation
Skill copied to discovery root != harness observed or invoked Skill
lineage != semantic warrant
handoff != semantic recommendation
```

The Campaign Controller is not a semantic router.

## Operator handoff / canonical sources

- `STATUS.md` — current cross-program state.
- `docs/product-management/README.md` — PM domain status and boundaries.
- `docs/product-management/qualification-levels.md` — PM maturity and qualification-debt policy.
- `docs/product-management/capability-migration-matrix.md` — all 27 upstream PM command dispositions and maturity.
- `docs/product-management/milestone-handoff.md` — first-slice package evidence and policy amendment.
- `docs/product-management/dogfood-runbook.md` — PM native-harness/fresh-context/second-harness protocol.
- `docs/product-management/dogfood/STATUS.md` — PM empirical qualification status.
- `docs/adr/0028-agent-agnostic-product-management-domain.md` — PM architectural authority.
- `qualification-evidence/STATUS.md` — engineering empirical external-qualification status.
- `docs/external-golden-path-verifier.md` — engineering external attempt/verifier protocol.
- `docs/sensemaking-campaign.md` — canonical Campaign product model.
- `.github/workflows/validation.yml` — Product Validation authority.
- `.github/workflows/lab-validation.yml` — retained Lab Validation authority.
- `.github/workflows/release-candidate.yml` — release distribution authority.

When prose and checked-in executable validation disagree, the executable contract is authority and the documentation should be reconciled.