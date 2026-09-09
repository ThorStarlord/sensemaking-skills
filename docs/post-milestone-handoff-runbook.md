# Post-Milestone Handoff Runbook — Packages #302–#304

**Status:** current handoff companion to `STATUS.md`  
**Applies to:** Post-Milestone Release Contract Reconciliation, Narrative Verification Receipts, Durable Qualification Evidence Receipts  
**Product version:** 0.3.0  
**Repository baseline before this documentation handoff:** `main@cd183827b438107dafd65f48fa23145b2e21fbdd`

This runbook captures the new operational surfaces added after the earlier v0.3 Feature Queue (#298–#300). For full Product Validation, Lab Validation, Release Candidate Distribution, target snapshot, harness setup, filesystem-security, and worktree procedures, continue to use `docs/milestone-runbook.md`.

---

## 1. Package ledger

| Package | PR | Exact candidate head | Result |
|---|---:|---|---|
| Release Contract Reconciliation | #302 | `2cb50eae32516f716d9c62846876e67b1f5741ec` | Product Validation PASS; Release Candidate Distribution PASS. |
| Narrative Verification Receipts | #303 | `a3cede49449ad2857bc348c7ba06877acc113ac0` | Product Validation PASS; Lab Validation PASS; Release Candidate Distribution PASS. |
| Qualification Evidence Receipts | #304 | `86f9a2ec96ed58ce096c71184f03a6ff839f3473` | Product Validation PASS; External Golden Path Qualification PASS; Release Candidate Distribution PASS. |

These are exact-head claims. A later commit does not inherit them automatically.

---

## 2. Narrative verification receipts

Package 2 added a deterministic service that binds an exact current Campaign narrative claim to exact durable evidence bytes.

The claim ceiling is permanent:

```text
claim bound to evidence != evidence proves claim
verification receipt exists != semantic truth
mechanical verification != warranted transition
historical verification != current Campaign state
```

### 2.1 Supported narrative scopes

Only exact membership is supported:

```text
current_state
established_fact
resolved_question
```

No fuzzy matching, entailment, semantic scoring, or inferred claims are accepted.

### 2.2 Python service usage

There is **no new first-class `sensemaking-skills campaign narrative-verify` CLI command** in this milestone. The shipped interface is the Python service/API.

Example:

```python
from sensemaking_skills.campaign_semantics import ClaimEvidence
from sensemaking_skills.campaigns import CampaignNarrativeVerificationService

claim = ClaimEvidence(
    claim="Repository diagnosis is complete",
    scope="established_fact",
    method="agent_cross_check",
    coverage=("repository_sensemaking_brief section 7",),
    claim_strength="supported",
    evidence=("artifacts/repository_sensemaking_brief/<sha>.md",),
)

service = CampaignNarrativeVerificationService("/path/to/campaign-workspace")
result = service.verify(
    receipt_id="NV-001",
    claims=(claim,),
)

for receipt in service.history():
    print(receipt)
```

Receipts are append-only and live beneath:

```text
narrative-verifications/
```

### 2.3 Focused qualification suite

Run the positive and negative/rejection tests together:

```bash
python -m pytest \
  tests/campaign_validation/test_campaign_narrative_verification.py \
  -q
```

This suite covers, among other cases:

- valid exact claim/evidence binding;
- strict YAML claim loading;
- unknown field rejection;
- unknown narrative scope rejection;
- claim-without-evidence rejection;
- invented/non-member claim rejection;
- orphan/unadmitted artifact rejection;
- missing evidence rejection;
- unsafe receipt ID rejection;
- duplicate receipt ID rejection;
- evidence mutation/deletion failure;
- receipt tampering failure;
- historical receipt behavior after a legitimate transition;
- proof that verification does not mutate Campaign state, transitions, or trace.

---

## 3. Qualification evidence receipts

Package 3 added a deterministic receipt for a structurally valid frozen external golden-path attempt.

A receipt binds:

```text
attempt.yaml SHA-256
verified evidence path/SHA-256 bindings
Sensemaking candidate identity
runtime / harness / adapter identity
external target repository identity
Campaign identity
recorded PASS / FAIL / INVALID outcome
package SHA-256
receipt SHA-256
```

The receipt proves only what the deterministic verifier checked.

```text
receipt exists != semantic truth
receipt exists != real-harness origin proven
synthetic fixture != empirical product evidence
qualified receipt != universal repository support
```

### 3.1 Verify a frozen attempt

For a frozen attempt directory:

```bash
python -m sensemaking_skills.external_qualification \
  <attempt-dir> \
  --json
```

For a structural preflight only:

```bash
python -m sensemaking_skills.external_qualification \
  <attempt-dir> \
  --structural-only
```

### 3.2 Generate a qualification evidence receipt

Only structurally valid attempt packages may receive a receipt:

```bash
python -m sensemaking_skills.qualification_evidence \
  <attempt-dir> \
  --output <attempt-dir>/qualification-evidence.json
```

The writer is append-only at the destination. Do not overwrite an existing receipt to change the historical result.

### 3.3 Verify an existing receipt

```bash
python -m sensemaking_skills.qualification_evidence \
  <attempt-dir> \
  --verify <attempt-dir>/qualification-evidence.json
```

Verification rebuilds the expected receipt from the supplied attempt bytes and requires exact equality.

### 3.4 Focused qualification suites

Run the external verifier plus qualification evidence positive/rejection coverage:

```bash
python -m pytest \
  tests/integration/test_external_golden_path_qualification.py \
  tests/integration/test_qualification_evidence.py \
  tests/integration/test_qualification_evidence_cli.py \
  -q
```

The CLI rejection test explicitly proves that a tampered/invalid attempt returns a failure code and does **not** write a receipt.

---

## 4. Checked-in real-harness evidence

Repository-owned real attempt packages belong under:

```text
qualification-evidence/
└── attempts/
    └── <attempt-id>/
        ├── attempt.yaml
        ├── evidence/
        │   └── ...
        └── qualification-evidence.json
```

Each checked-in attempt must satisfy the external protocol and carry a receipt generated from those exact bytes.

Before proposing the evidence PR, run:

```bash
python -m sensemaking_skills.external_qualification \
  qualification-evidence/attempts/<attempt-id> \
  --structural-only

python -m sensemaking_skills.qualification_evidence \
  qualification-evidence/attempts/<attempt-id> \
  --verify qualification-evidence/attempts/<attempt-id>/qualification-evidence.json
```

A change beneath `qualification-evidence/**` triggers the External Golden Path Qualification workflow, which revalidates checked-in attempt structure and receipt equality.

---

## 5. Real-harness dogfood protocol

The next evidence-producing step is external to repository-local implementation.

1. Select a genuine external target repository and a supported coding-agent harness.
2. Use the intended Sensemaking candidate/runtime and explicit harness adapter setup.
3. Start a fresh target-bound Campaign outside the target repository.
4. Complete the canonical lifecycle using durable evidence and explicit agent-authored decisions.
5. Preserve distinct evidence that the harness discovered and natively invoked the Skill; installation alone is insufficient.
6. Do not manually repair Campaign state or qualification artifacts to obtain PASS.
7. Complete handoff/resume in fresh context when required by the protocol.
8. Freeze the attempt package under `v0.3-external-golden-path-dogfood-v1`.
9. Run the external verifier.
10. Generate the qualification evidence receipt for the exact frozen bytes.
11. Preserve PASS, FAIL, or INVALID honestly.

Current empirical state at the time of this handoff:

```text
Checked-in real-harness attempts: 0
Current empirical PASS: NONE
```

Therefore:

```text
repository implementation complete
!= empirical product qualification complete
```

---

## 6. Failure interpretation

### Structurally invalid attempt

Do not create a qualification evidence receipt. Fix the attempt packaging/protocol problem or preserve the invalid run as non-receipted diagnostic material.

### Structurally valid FAIL

Preserve it as `qualified: false` evidence. Do not mutate the package to manufacture a PASS.

### Existing receipt no longer verifies

Treat the mismatch as byte drift/tampering until explained. Do not overwrite the receipt. Reconstruct which attempt bytes changed and why.

### Narrative verification rejects a claim

Do not weaken exact membership checks or invent a fuzzy semantic validator. Either record the intended claim in the normal Campaign narrative through the appropriate agent-authored lifecycle path, or correct the claim/evidence binding.

### Historical narrative receipt

`current_state_match = false` after a legitimate transition means the receipt is historical, not invalid. Do not rewrite history to make it current.

---

## 7. Candidate qualification before merge

For future repository changes that touch these surfaces, use the relevant checked-in workflows as executable authority.

At minimum, the focused local suites are:

```bash
python -m pytest \
  tests/campaign_validation/test_campaign_narrative_verification.py \
  -q

python -m pytest \
  tests/integration/test_external_golden_path_qualification.py \
  tests/integration/test_qualification_evidence.py \
  tests/integration/test_qualification_evidence_cli.py \
  -q
```

Then run the broader commands from `docs/milestone-runbook.md` as warranted by the files and claims being changed.

Never borrow a green result from an older candidate head.

---

## 8. Next-session reading order

Future engineers and chat sessions should read in this order:

1. `STATUS.md` — current milestone/handoff state.
2. `qualification-evidence/STATUS.md` — empirical real-harness qualification state.
3. `docs/post-milestone-handoff-runbook.md` — Package #302–#304 operating procedures.
4. `docs/campaign-narrative-verification.md` — narrative receipt contract.
5. `docs/qualification-evidence.md` — qualification receipt contract.
6. `docs/external-golden-path-verifier.md` — external attempt protocol.
7. `docs/milestone-runbook.md` — earlier v0.3 validation/release/target operations.

If the empirical status still says zero real-harness attempts, the true active bottleneck is evidence collection, not another repository-local implementation package.
