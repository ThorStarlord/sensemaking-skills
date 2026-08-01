# TEMPLATE ONLY - NOT AN APPROVAL - Evidence 0016

This file is a **non-operative template**. It is not an owner approval, it does
not authorize anything, and Gate A never reads it.

Gate A reads only `owner-approval.md` in this directory. That file does not
exist and must not be created by any agent. Only the repository owner may
create it, and only after explicitly approving the exact authorization-record
digest recorded below in the approval request.

Every value below is a placeholder. The placeholders are deliberately not
valid: they are not a real identity, not a real timestamp, and not a real
digest. Copying this file to `owner-approval.md` unchanged would be rejected
by Gate A, and would still be an unauthorized act.

## Placeholder field block (DO NOT COPY AS-IS)

    approver_github_identity: PLACEHOLDER
    approval_timestamp: PLACEHOLDER
    authorization_record_sha256: PLACEHOLDER
    execution_framework_sha: PLACEHOLDER
    target_sha: PLACEHOLDER
    evidence_number: PLACEHOLDER
    evidence_slug: PLACEHOLDER
    exact_model: PLACEHOLDER
    authorization_decision: PLACEHOLDER
    no_retry_statement: PLACEHOLDER
    owner_decision_reference: PLACEHOLDER

The block above is indented as a code block precisely so that it documents the
required shape without being usable as an approval.

## What the real approval must do

The real `owner-approval.md`, if the owner ever chooses to create it, must:

- name the approving GitHub identity, which must be the repository owner and
  must not be the identity that authored the authorization record;
- state the exact 64-character SHA-256 digest of
  `authorization-record.yaml` as committed in the immutable run-control commit;
- repeat the pinned execution framework SHA and target SHA verbatim;
- repeat the evidence number, evidence slug, and exact model verbatim;
- carry the decision value defined by the governing contract;
- state that there is no retry, no rerun, and no repair;
- reference the owner decision it derives from.

Any change to `authorization-record.yaml` invalidates its digest and therefore
invalidates any approval that named the old digest.
