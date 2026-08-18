# EXP-0005 — GitHub-durable connector-native campaign report

## Disposition

**SUPPORTED — bounded exploratory result.**

EXP-0005 supports the frozen hypothesis that a bounded `coding_agent_native` campaign can execute through the connected GitHub surface while preserving truthful conversation-approval auditability, durable attempt accounting, exact-SHA connector-native repository analysis, preserved artifacts, deterministic exact-head validation, and GitHub-only recovery of the campaign facts required by Issue #201.

This result remains `EXPLORATORY_NOT_CANONICAL_EVIDENCE`. It is not a general product-readiness claim and does not promote the target-analysis findings to canonical Evidence automatically.

A scope limit is explicit: GitHub is the durable control plane and observable campaign history, not an independent packet/network audit log of every connector API request. The evidence supports that `INVOKED` was durable before each target-derived artifact was produced under the frozen execution contract; it does not claim that GitHub independently records every target read outside that contract.

## Frozen envelope

- campaign: `EXP-0005-stage1-auteur-github-connector-pilot`
- framework SHA: `c9cb29d467eee82d1d9cc4d4fb89a184c26f27e7`
- target: `ThorStarlord/auteur @ 0653defb05625f2fcde0ac32eac6e59ccf7eeb90`
- configuration ID: `cebe75031440292300aa154ba2ccdc7ec207de503088b28fa340acbec69562aa`
- policy digest: `e4d85d344aac8b55b2444ec3e0eb963493daad2a43ac368d242479b8c21465ac`
- execution mode / surface: `coding_agent_native` / `github_connector`
- target access: `github_connector_read_only`
- probe: `github_connector_exact_sha_v1`
- durability: `github_results_branch_v1`
- validation: `github_actions_exact_head`
- invocation boundary: `before_first_experiment_scoped_target_read`
- approval reference kind: `agent_recorded_github_issue_comment`
- approval audit destination: `ThorStarlord/sensemaking-skills` Issue #201
- max attempt slots: 3
- concurrency ceiling: 1
- target mutation, external provider API, fallback, repair/hidden retry, automatic merge: prohibited
- validity: `2026-08-18T19:00:00+00:00` through `2026-08-25T19:00:00+00:00`

## Approval audit

A standalone human `approve` was received only after presentation of the exact merged envelope.

- approved_at: `2026-08-18T19:04:00+00:00`
- approval source: `active_human_conversation`
- durable locator: `https://github.com/ThorStarlord/sensemaking-skills/issues/201#issuecomment-5332769302`
- receipt: `experiments/results/EXP-0005-stage1-auteur-github-connector-pilot/approval.md`

The Issue #201 comment explicitly identifies itself as agent-authored audit metadata rather than independent human-authored consent. No ChatGPT session/message identifier was inferred or fabricated.

## Durable attempt accounting

| Attempt | RESERVED commit / gate | INVOKED commit | OUTPUT_CAPTURED head / validator | Terminal commit | Result |
|---|---|---|---|---|---|
| `attempt-001` | `9f7523f4d01cc5092d19f3825a5c957a65ef63b5` / Validator #491 (`32174951194`) success | `c6ec594e6cf13e0f246fe724e9570ec30aa1ddc8` | `c4c21538edb35d2870a92e5e1f186806625664e1` / Validator #493 (`32175774164`) success | `a6e552031d4cde7b422ae6cb1c9a563581f4214e` | `VALIDATION_PASSED` |
| `attempt-002` | `90bc0402e42643333432af60b67d3c6aeb62dff3` / Validator #495 (`32175924295`) success | `cf83d7ba8ec75aa70076ce66b1f7d4d69e24ef53` | `7333f6791430685f00bc6fa6a6a7e62c00383b17` / Validator #497 (`32176260337`) success | `d5283d9062fe6c7456b9c7c1edbc4e9dd60ae4d8` | `VALIDATION_PASSED` |
| `attempt-003` | `3394d88a401363748a3d9f9a0f6f49eb0db35ceb` / Validator #499 (`32176437259`) success | `a749bab223c1bcfcf265f790e1aeff728b1a700c` | `5baea7c0a3c07e10c45591c0607e57d90e200bad` / Validator #501 (`32176742318`) success | `d2cd880f7fe650ca543b90d93a88b0581b4e6d21` | `VALIDATION_PASSED` |

The commit graph independently preserves ordering: each `INVOKED` commit has the corresponding `RESERVED` commit as its parent; each output-capture commit has the `INVOKED` commit as its parent; each terminal commit has the preserved output head as its parent. The terminal ledger records each exact output validation head and workflow run ID.

Final accounting:

- attempt slots authorized: **3**
- attempts reserved: **3**
- invocations recorded: **3**
- preserved attempt artifacts: **3**
- `VALIDATION_PASSED`: **3**
- `VALIDATION_FAILED`: **0**
- non-terminal attempts: **0**
- remaining slots: **0**
- concurrency observed by durable state: **1**
- target mutation: **none performed by the campaign**
- external provider API calls: **0**
- hidden retry/repair: **0**
- automatic merges: **0**

## Connector-native target analysis

All three attempts independently resolved the exact target SHA after their own durable `INVOKED` transition and re-read decision-changing evidence at that exact ref.

Every attempt converged on:

- primary fog: `architecture_fog`
- weakness type: **Implicit Dependencies**
- weakest boundary: a `CrossStoryConstraint` may be configured `required`, yet the cross-story advisory intentionally emits only non-blocking `INFO` human-review notices and Series Bible compilation blocks only `ERROR`; the examined deterministic path therefore does not encode whether the required human review has been completed, waived, or remains pending.
- recommended next responsibility: introduce a durable cross-story review-disposition contract (`pending|reviewed|waived` with provenance/current constraint identity), while preserving the existing rule that semantic compliance itself is not automatically evaluated.
- recommended workflow: `implementation-workflow` / `guided_execution`
- secondary hygiene finding: a committed root temp/scratch Python file is outside the repository's configured pytest/Ruff scopes.

The three artifacts preserve the same decision-bearing target blob identities:

- `README.md` — `52babadc6422f5d491d27dd5927c192b6417605b`
- `src/auteur/universe/models.py` — `9292b7da08484916772a2069e0129b1fb898b3a6`
- `src/auteur/series/universe_advisory.py` — `14d11929448bcbd406fbed6cec0eaa0ddd289701`
- `src/auteur/series/handlers.py` — `d44f0d5034a04d31ff670650447595c0598a0f84`
- `tests/test_cross_story_constraint_notices.py` — `43ee358feba8aeaba7305e5ec819eb093189bf15`
- `pyproject.toml` — `c6dcf42f259aae4c912a4f9e0528f6ee0f2ecc59`
- root scratchpad — `7a786becd30233afc01ffb7430518e9b8843e3b5`

Local-only Probe Engine metrics (`verification_gap.vg`, `context_entropy.ce`, `fixtures_coverage.coverage`, `churn`) were not available on the authorized connector-native surface and were left explicitly unmeasured in every attempt rather than fabricated.

## Reproducibility

The three attempt artifacts are not textually identical and were independently synthesized, but they agree structurally and substantively on the primary fog, weakness type, weakest boundary, exact target evidence identities, recommendation, and workflow routing. No attempt was discarded or selected after the fact.

This is strong bounded evidence that the connector-native responsibility is reproducible for this frozen framework/configuration/target snapshot.

## GitHub-only recovery audit

A fresh audit using GitHub-resident data alone can reconstruct the Definition-of-Done facts required by Issue #201:

1. `approval.md` gives the exact campaign/digest, timestamp, limits, reference kind, and real Issue #201 comment permalink.
2. The Issue #201 comment durably records the agent-authored approval audit event and explicitly distinguishes it from human-authored consent.
3. `campaign-state.yaml` gives all three state histories, artifact paths, exact validation heads/run IDs, terminal states, concurrency ceiling, and budget.
4. GitHub commit history establishes `RESERVED -> INVOKED -> OUTPUT_CAPTURED -> terminal` ordering for every attempt.
5. The three artifact paths exist on the results branch and preserve exact-SHA evidence identities.
6. Draft results PR #203 exposes the branch as durable historical evidence and remains unmerged.

No Windows executor-host state, Task Scheduler state, local campaign root, local process history, local checkout, or chat-local repository state is needed to reconstruct those campaign facts.

## Scientific questions

1. **Can `agent_recorded_github_issue_comment` become operative after standalone approval?** Yes. A concrete Issue #201 permalink was recorded and bound into a valid approval receipt.
2. **Can the receipt validate without fabricated ChatGPT IDs?** Yes. The approved empty-state validator passed before any attempt reservation.
3. **Can durable `RESERVED` and `INVOKED` distinguish pre/post-invocation histories?** Yes. Each transition has a separate durable commit; each reservation was exact-head validated before invocation.
4. **Can `repo-sensemaker` run against the pinned target through `github_connector_exact_sha_v1`?** Yes. Three preserved briefs were produced using exact target refs and GitHub blob identities, with unavailable local metrics explicitly unmeasured.
5. **Can recovery rely on GitHub-resident state/history?** Yes for the campaign facts required by Issue #201's DoD.
6. **How reproducible are three identical-configuration attempts?** High substantive agreement: all three independently selected the same primary architectural boundary, weakness type, evidence set, recommendation, and workflow.
7. **Does the final campaign disposition require executor-local authoritative state?** No.

## Interpretation

EXP-0005 closes the specific empirical gap left by EXP-0003 and EXP-0004. It demonstrates a truthful connector-native approval locator and an end-to-end GitHub-durable campaign with three bounded attempts. It does **not** retroactively make EXP-0003 or EXP-0004 successful, and it does not establish universal readiness of the framework or target repository.

The target-analysis finding is itself exploratory. Its strongest repeated result is that Auteur's cross-story implementation is appropriately honest about non-evaluation, but required cross-story review remains an implicit human dependency until review disposition becomes explicit durable state.

## Final status

**EXP-0005: SUPPORTED (bounded, exploratory).**

Results branch: `experiment/exp-0005-results`  
Results PR: #203 — **draft / do not merge automatically**.

Any integration of these exploratory results remains a separate owner decision.
