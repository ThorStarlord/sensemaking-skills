# coding-agent-native-campaign — run an approved agent-native campaign

Run an approved `coding_agent_native` campaign: the human approves in the
conversation, the coding agent performs every repository operation, and a
Markdown file (`approval.md`) records the decision. The conversation is the
human decision authority; agent-recorded audit artifacts are not independent
proof of human identity.

## The one-word approval contract

> A standalone `approve` from the human authorizes the one and only
> campaign most recently presented in the active conversation, provided
> its digest has not changed. The coding agent records the complete
> authorization in `approval.md`.

`approve` is the human decision. `approval.md` is the agent-generated receipt
containing the precise meaning of that decision. The file is **not**
independent proof of human identity — the conversation is the source of
authority — but the runtime validates the receipt against the exact campaign
envelope before every step.

### The agent MUST refuse to record an approval when

- more than one campaign is pending;
- the campaign changed after it was presented;
- no campaign was presented;
- the policy digest cannot be resolved;
- `approve` appears inside a quotation, example, or hypothetical question
  (the word alone, standalone, is the decision);
- the campaign has already expired.

In those cases respond: `Approval is ambiguous: there are multiple or no
pending campaigns.` and execute nothing.

## When to use

The campaign policy declares a coding-agent-native execution surface and
prohibits external provider APIs. The human has replied with a standalone
`approve` to the presented envelope in THIS conversation.

**Approval and the execution window are separate gates.** The human's
`approve` may be given any time after the final envelope is presented and
before it expires. `approved_at` records the actual approval time: it may
precede `validity_window.not_before`, must not be in the future, and must not
exceed `validity_window.not_after`. The receipt is recorded immediately.
Execution is mechanically gated by the window.

## Hard rules

- NEVER call an external model/provider API when the policy prohibits it.
- NEVER fabricate an approval: only a standalone `approve` from the human,
  for the exact presented envelope, may be recorded.
- NEVER fabricate a platform conversation/session/message identifier.
- NEVER describe an agent-authored GitHub comment as human-authored consent.
- NEVER modify the target checkout/repository when the campaign is read-only.
- NEVER hide, retry, or repair an attempt: failed, validation-failed, and
  interrupted attempts are recorded and reported identically.
- Every result remains in the policy's declared exploratory classification.
- Stop at the campaign's window end; bookkeeping re-checks the clock and
  re-validates the receipt before every step.

## Protocol

1. **Present the full envelope** in the conversation: campaign id,
   `policy_digest`, `maximum_attempts`, `concurrency`,
   `automatic_merge: prohibited`, external-provider rule, classification,
   and the validity window. Confirm there is exactly one pending campaign
   and its digest is unchanged.
2. **The human replies with a standalone `approve`.** Nothing else counts
   (a reaction, a merge, silence, or `approve` inside a question or quote
   does not).
3. **Create a truthful audit locator, then write `approval.md`.** Choose
   exactly one reference form:

   **A. Legacy platform conversation pointer.** Use only when the execution
   surface actually exposes a real concrete `session-id#message-id`. Do not
   infer or invent it. Omit `reference_kind`.

   **B. Connector-native GitHub audit event.** Use when the active execution
   surface can write GitHub but does not expose real platform conversation
   identifiers. Immediately after the valid standalone `approve`, add one
   top-level comment to the campaign's tracking issue containing:

   - `Agent-recorded conversation approval event`;
   - the exact campaign id;
   - the exact presented policy digest;
   - the actual approval timestamp;
   - `approval_text: approve`;
   - an explicit statement that the comment is an agent-authored durable
     transcription/audit locator and is **not independent human-authored
     consent**.

   Use the concrete GitHub permalink returned for that newly created comment,
   then write the receipt with:

   ```yaml
   approval_schema_version: "1"
   status: "approved"
   campaign_id: "EXP-0000-EXAMPLE"
   policy_digest: "<PRESENTED_DIGEST>"
   approval_source: "active_human_conversation"
   approval_text: "approve"
   approved_at: "<APPROVED_AT_RFC3339>"
   maximum_attempts: 3
   concurrency: 1
   automatic_merge: "prohibited"
   external_provider_api_prohibited: true
   classification: "EXPLORATORY_NOT_CANONICAL_EVIDENCE"
   reference_kind: "agent_recorded_github_issue_comment"
   reference: "https://github.com/<owner>/<repo>/issues/<issue-number>#issuecomment-<comment-id>"
   ```

   The receipt frontmatter must use the exact values presented. The GitHub
   comment and `approval.md` are created only **after** the human decision;
   neither may be pre-created as a substitute for approval. The runtime does
   not fetch the comment and does not treat it as identity proof: it validates
   the explicit locator grammar plus every campaign/policy binding. Audit and
   recovery may follow the permalink to inspect the durable transcription.

4. **Validate the receipt immediately, window-independently** using the
   repository's approval-validation path. Expected behavior is an
   `APPROVAL_VALID` result that echoes the campaign id, policy digest, and
   exact audit reference. Validation performs no reservation or invocation.
   The campaign is now `APPROVED_NOT_STARTED`.
5. **Before the window opens, execution preparation refuses by design.**
   That refusal is the mechanical execution gate, not an error: no
   reservation, ledger event, or attempt directory/state is created.
6. Starting inside the valid window, execute each serialized attempt using
   the campaign's frozen execution contract. For connector-native GitHub-
   durable campaigns, follow the repository's durable state protocol exactly:
   commit `RESERVED`, then commit `INVOKED` immediately before the first
   experiment-scoped target read, preserve `OUTPUT_CAPTURED`, validate the
   exact preserved head, then record the terminal validation state.
7. Read and follow the frozen responsibility instructions at the framework
   revision. Perform the responsibility yourself against the exact approved
   target identity and write only the permitted artifact.
8. Repeat only while the durable ledger/state says budget remains and no
   non-terminal attempt exists. Never replay an `INVOKED` attempt silently.
9. Render the complete report, preserve every attempt/state/result on the
   isolated results branch, keep the results PR unmerged, and stop at the
   independent-audit/owner-integration boundary. Never automatically merge.

## Connector-native approval-reference safety

`reference_kind: agent_recorded_github_issue_comment` is intentionally
narrow. The corresponding `reference` must be a concrete permalink shaped as:

`https://github.com/<owner>/<repo>/issues/<positive-number>#issuecomment-<positive-id>`

A GitHub issue-comment URL without that explicit `reference_kind` is invalid;
a placeholder URL, other host, PR URL, missing comment fragment, zero id, or
unknown reference kind is invalid. This prevents the connector-native fix
from collapsing into the old broad "contains a #" rule.

The agent-recorded GitHub event is only an audit locator. It MUST NOT be
presented as a GitHub-native human approval mechanism, reviewer approval,
identity attestation, or corroboration of who typed `approve`. The active
conversation remains the authority.

## If anything refuses

A `REFUSED: ...` message means a precondition failed (receipt missing or
superseded, reference invalid, window closed, budget exhausted, injection
detected, drift). Record it and stop; never bypass the refusal by editing the
policy, receipt, ledger, or historical experiment files.
