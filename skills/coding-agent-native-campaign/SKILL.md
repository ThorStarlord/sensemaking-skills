# coding-agent-native-campaign — run an approved agent-native campaign

Run an approved `coding_agent_native` campaign: perform the `repo-sensemaker`
skill yourself, three bounded attempts, preserve every result, and open the
aggregate results PR. No external model or provider API is used at any
point — skills are instructions for the coding agent, not prompts to
forward to another model.

## When to use

The campaign policy declares:

```yaml
execution_mode: "coding_agent_native"
execution_surface: "current_coding_agent"
external_provider_api_prohibited: true
allowed_models: []
```

The human has posted the approval comment on the campaign's GitHub issue
and the operative `approval.yaml` has been captured. The policy window is
open.

## Hard rules

- NEVER call an external model/provider API; the policy prohibits it and
  the envelope authorizes no external model.
- NEVER post the approval comment yourself; only the human may.
- NEVER modify the target checkout (read-only analysis).
- NEVER hide, retry, or repair an attempt: failed, validation-failed, and
  interrupted attempts are recorded and reported identically.
- Every result is `EXPLORATORY_NOT_CANONICAL_EVIDENCE`.
- Stop at the campaign's `expires_at` and policy window end; the bookkeeping
  commands re-check the clock before every step.

## Protocol (per attempt)

1. Verify the approval is live and unrevoked (the bookkeeping commands
   re-corroborate it against the GitHub API on every prepare and finalize;
   if they refuse, STOP and report).
2. `prepare` the next attempt (creates the durable reservation, freezes
   the instructions, records the durable INVOKED transition):

   ```bash
   python scripts/execution_infra/agent_native_campaign.py prepare \
       --package-dir experiments/campaigns/EXP-0002-stage1-auteur-coding-agent-pilot \
       --campaign-root <campaign-root> \
       --framework-checkout <pinned-framework-checkout> \
       --target-checkout-root <target-checkout-root> \
       --allowed-approver ThorStarlord
   ```

   It prints `ATTEMPT_PREPARED <attempt-id>` and the delivery path.
3. Read the frozen instructions at the printed `INSTRUCTIONS` path
   (it embeds the pinned `repo-sensemaker/SKILL.md`, the target checkout
   at the approved SHA, and the delivery path).
4. Perform `repo-sensemaker` yourself against the read-only target
   checkout. Write the Repository Sensemaking Brief to the delivery path.
5. `finalize` the attempt:

   ```bash
   python scripts/execution_infra/agent_native_campaign.py finalize \
       --package-dir experiments/campaigns/EXP-0002-stage1-auteur-coding-agent-pilot \
       --campaign-root <campaign-root> \
       --framework-checkout <pinned-framework-checkout> \
       --target-checkout-root <target-checkout-root> \
       --attempt-id <attempt-id> \
       --artifact <delivery-path> \
       --allowed-approver ThorStarlord
   ```

   It re-verifies the approval and the window, preserves the raw output and
   the produced artifact, validates the brief with the pinned validator,
   and records the terminal state. `finalize` on an attempt that was never
   prepared, or after the approval was edited/deleted, refuses.

6. Repeat for the remaining slots (the ledger, never memory, decides how
   many remain; the commands refuse when the budget is exhausted).

## After the last attempt

1. Render the complete ledger-derived report:

   ```bash
   python scripts/execution_infra/agent_native_campaign.py report \
       --package-dir experiments/campaigns/EXP-0002-stage1-auteur-coding-agent-pilot \
       --campaign-root <campaign-root> \
       --framework-checkout <pinned-framework-checkout> \
       --allowed-approver ThorStarlord
   ```

2. Commit every attempt directory, the ledger, and the report on an
   isolated results branch (e.g. `experiment/exp-0002-results`); never
   push to `main`.
3. Open ONE results PR containing every attempt (including failures), all
   raw requests/outputs, artifacts, validation results, the report, and an
   explicit nothing-omitted statement with the exploratory classification.
4. Stop at
   `EXP_0002_RESULTS_PR_READY_FOR_INDEPENDENT_AUDIT` and wait for the
   human to review the aggregate result. Do not merge the PR yourself.

## If anything refuses

A `REFUSED: ...` message means a precondition failed (approval revoked,
window closed, budget exhausted, injection detected, drift). Record it and
stop; never bypass the refusal by editing policy, approval, or ledger
files.
