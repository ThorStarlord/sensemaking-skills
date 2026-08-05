# coding-agent-native-campaign — run an approved agent-native campaign

Run an approved `coding_agent_native` campaign: the human approves in the
conversation, the coding agent performs every repository operation, a
Markdown file (`approval.md`) records the decision, and no GitHub
comment, capture script, API token, or live comment revalidation is
involved.

## The one-word approval contract

> A standalone `approve` from the human authorizes the one and only
> campaign most recently presented in the active conversation, provided
> its digest has not changed. The coding agent records the complete
> authorization in `approval.md`.

`approve` is the human decision. `approval.md` is the agent-generated
receipt containing the precise meaning of that decision. The file is
**not** independent proof of human identity — the conversation is the
source of authority — but the runtime validates the receipt against the
exact campaign envelope before every step.

### The agent MUST refuse to record an approval when

- more than one campaign is pending;
- the campaign changed after it was presented;
- no campaign was presented;
- the policy digest cannot be resolved;
- `approve` appears inside a quotation, example, or hypothetical
  question (the word alone, standalone, is the decision);
- the campaign has already expired.

In those cases respond: `Approval is ambiguous: there are multiple or no
pending campaigns.` and execute nothing.

## When to use

The campaign policy declares:

```yaml
execution_mode: "coding_agent_native"
execution_surface: "current_coding_agent"
external_provider_api_prohibited: true
allowed_models: []
```

The human has replied with a standalone `approve` to the presented
envelope in THIS conversation, and the policy window is open.

## Hard rules

- NEVER call an external model/provider API; the policy prohibits it and
  the envelope authorizes no external model.
- NEVER fabricate an approval: only a standalone `approve` from the
  human, for the exact presented envelope, may be recorded.
- NEVER modify the target checkout (read-only analysis).
- NEVER hide, retry, or repair an attempt: failed, validation-failed, and
  interrupted attempts are recorded and reported identically.
- Every result is `EXPLORATORY_NOT_CANONICAL_EVIDENCE`.
- Stop at the campaign's window end; the bookkeeping commands re-check
  the clock and re-validate the receipt before every step.

## Protocol

1. **Present the full envelope** in the conversation: campaign id,
   `policy_digest`, `maximum_attempts`, `concurrency`,
   `automatic_merge: prohibited`, `external_provider_api_prohibited:
   true`, classification, and the validity window. Confirm there is
   exactly one pending campaign and its digest is unchanged.
2. **The human replies with a standalone `approve`.** Nothing else
   counts (a reaction, a merge, silence, or `approve` inside a question
   or quote does not).
3. **Write `approval.md`** in the campaign package directory — the exact
   receipt contract (frontmatter + prose):

   ```markdown
   ---
   approval_schema_version: "1"
   status: approved
   campaign_id: EXP-0002-stage1-auteur-coding-agent-pilot
   policy_digest: <PRESENTED_DIGEST>
   approval_source: active_human_conversation
   approval_text: approve
   approved_at: <now, RFC3339>
   maximum_attempts: 3
   concurrency: 1
   automatic_merge: prohibited
   external_provider_api_prohibited: true
   classification: EXPLORATORY_NOT_CANONICAL_EVIDENCE
   reference: <session-id>#<message-id>
   ---

   The human approved the single pending campaign presented in the
   active conversation.
   ```

   The frontmatter must be written with the exact values presented; the
   runtime validates every binding (campaign id, digest, limits, merge
   rule, external-provider prohibition, classification, window) before
   any step.

4. `prepare` the next attempt (durable reservation, frozen instructions,
   durable INVOKED):

   ```bash
   python scripts/execution_infra/agent_native_campaign.py prepare \
       --package-dir experiments/campaigns/EXP-0002-stage1-auteur-coding-agent-pilot \
       --campaign-root <campaign-root> \
       --framework-checkout <pinned-framework-checkout> \
       --target-checkout-root <target-checkout-root> \
       --allowed-approver ThorStarlord
   ```

5. Read the frozen instructions at the printed `INSTRUCTIONS` path; they
   embed the pinned `repo-sensemaker/SKILL.md`, the read-only target
   checkout at the approved SHA, and the delivery path.
6. Perform `repo-sensemaker` yourself against the target checkout and
   write the Repository Sensemaking Brief to the delivery path.
7. `finalize` the attempt (re-validates the receipt + window, preserves
   raw output + artifact, validates, records the terminal state):

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

8. Repeat for the remaining slots (the ledger decides; the commands
   refuse when the budget is exhausted or an attempt is still active).
9. Render the complete report, commit every attempt directory + ledger +
   report on an isolated results branch, open ONE results PR with the
   nothing-omitted statement, and stop at
   `EXP_0002_RESULTS_PR_READY_FOR_INDEPENDENT_AUDIT` for the human's
   review. Never push to `main`; never merge the PR yourself.

## If anything refuses

A `REFUSED: ...` message means a precondition failed (receipt missing or
superseded, window closed, budget exhausted, injection detected, drift).
Record it and stop; never bypass the refusal by editing the policy,
receipt, or ledger files.
