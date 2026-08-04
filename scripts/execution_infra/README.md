# EXP-0001 execution infrastructure (Phase 6 readiness, Issue #122)

**STATUS: INFRASTRUCTURE ONLY. NO EXECUTION. NO APPROVAL.**

This tree contains the injectable execution infrastructure for the EXP-0001
campaign: the production approval-provenance verifier, the real provider
adapter, and the runner that composes them with the frozen framework. It
contains **no campaign approval, no reservation, no ledger, no provider
call, and no output** — and it refuses to run the real campaign unless every
Phase 6 precondition holds (see `runner.py`).

## The framework-SHA question: Approach A (chosen)

The campaign policy pins `framework_sha: 4ba049e...`. Phase 6 needs two
things the pinned framework deliberately does not ship: real signed-commit
corroboration (the framework's `ProductionSignedCommitVerifier` is a
fail-closed stub that refuses to fabricate consent) and a real provider
adapter (the Phase 4 boundary's provider is documented as a test double or
future adapter). Two approaches were considered:

- **Approach B (revise the campaign package):** add the wiring to the
  framework, then re-pin `framework_sha`, `prompt_or_skill_revision`,
  `validator_revision`, `configuration_id`, `allowed_configuration_ids`,
  `policy_digest`, and the validity window — a new preparation revision,
  new exact-head review, merge, and a NEW human approval. Cleaner in the
  abstract, but it invalidates the merged package, requires a new approval
  that cannot be fabricated, and would almost certainly blow the frozen
  window.
- **Approach A (external, independently pinned adapters) — CHOSEN:** run
  the frozen `4ba049e` framework while injecting a separately versioned
  provenance verifier and provider adapter. The framework code
  (`src/` + the canonical executor/Gate A scripts) remains **byte-identical
  to the pinned SHA** — proven by an empty `git diff 4ba049e..HEAD` over
  those paths (`versions.framework_code_unchanged`) and asserted by the
  runner before every run. The adapters are explicitly **infrastructure
  outside the campaign configuration**: they are not framework code, not
  policy fields, and their exact content digests are preserved in the
  execution record (`versions.adapter_versions`).

The pinned framework SHA therefore continues to describe exactly the
framework bytes that will execute. Nothing is labeled `4ba049e` that is not
`4ba049e`.

## What each module is

| Module | Role |
|---|---|
| `versions.py` | Content digests (SHA-256) of every infrastructure module + the framework-drift proof (`git diff <pin>..HEAD` over framework paths) |
| `production_verifier.py` | `ProductionSignedCommitVerifier`: real `signed_commit` corroboration — reference exists as a commit, is an ancestor of the verification repo HEAD, and `git verify-commit` succeeds; every stage fails closed with `ProvenanceVerificationError` |
| `provider_adapter.py` | `ClaudeProviderAdapter`: builds the prompt from the FROZEN framework checkout's repo-sensemaker skill, invokes `claude-sonnet-5` via the Claude Agent SDK, returns the raw model output bytes; raises `ProviderAdapterError` on any failure |
| `runner.py` | `Exp0001Runner` + `build_execution_report`: the full lifecycle (reserve → mint → durable boundary → raw capture → validate → report) with real-campaign refusal guards |

## Real-campaign refusal guards (`Exp0001Runner`)

For `campaign_id == EXP-0001-stage1-auteur-autonomy-pilot` the runner
refuses unless ALL hold:

1. the operative approval file (`approval.yaml`) exists in the campaign
   package — approval is a human act, never inferred from merge,
   ownership, write access, or silence;
2. the injected verifier is the production signed-commit verifier (a test
   verifier can never authorize the real campaign);
3. the injected provider is the real `ClaudeProviderAdapter`;
4. the framework checkout HEAD is exactly the pinned `framework_sha` and
   the framework code diff vs the pin is empty;
5. the current time is inside the policy validity window
   (`2026-08-07T00:00:00+00:00` → `2026-08-14T00:00:00+00:00`).

For any other campaign id (tests, dry runs on test campaigns) injected
doubles are accepted — the guards are keyed on the campaign id of the
package being run.

## Execution record

Every run records: the pinned and actual framework checkout SHAs, the
framework-drift result, the content digest of every infrastructure module,
every attempt and terminal state from the append-only ledger, pass rate,
failure categories, observed cost/tokens, runner-level errors, and the
explicit nothing-omitted statement. Failed and aborted attempts are
reported identically to successful ones; no best-result-only summary can be
produced (the campaign summary has no successes-only mode).

## What this tree does NOT do

- It does not create or record a human approval, and it cannot fill
  `approval-template.yaml` into an operative approval.
- It does not reserve attempts, open a ledger, call a provider, or produce
  campaign output — the runner refuses until the guards above hold, and
  every test injects a spy provider with zero-call assertions.
- It does not modify `src/`, the campaign package bytes, Evidence 0015/0016,
  or canonical Gate A.

The next step after this infrastructure is merged is the genuine human
approval of the exact policy digest, followed by Phase 6 execution only
inside the frozen window.
