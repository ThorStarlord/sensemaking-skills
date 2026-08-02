# SUPERSEDED -- this file is NOT a live owner approval

**VOID for the current authorization-record.yaml. Gate A never reads this
file: it reads only `owner-approval.md`, which does not exist in this
directory.**

This file is the historical governance record of a real owner approval
granted by ThorStarlord on 2026-08-01 (PR #113), preserved for audit
purposes and renamed out of the active-approval path rather than deleted.

That approval bound `authorization_record_sha256: bf31c7b6...`, the digest
of the authorization record as it existed **before** PR #114 (the
artifact-root topology change) merged into main as commit
`98a08d50a0a8dbca4599296e717ab60f1d567d83`. Regenerating the record to pin
the new `execution_framework_sha` produced different record bytes and
therefore a different digest (`28ec6518...`). Because an approval binds only
the exact record bytes that hash to the digest it names, this approval does
not, and cannot, approve the new record. It is void for that record and must
not be read, copied, or treated as if it were current approval.

A fresh owner approval, naming the new digest, is required before any
preflight or invocation against the regenerated record.

---

## Original approval text (historical, preserved verbatim below)

I, the repository owner, explicitly approve the Evidence 0016 authorization
record identified by the exact SHA-256 digest below.

This approval applies only to the exact record bytes producing that digest.
Any modification to the authorization record invalidates this approval.

This approval does not itself authorize dry preflight or live model invocation.
Those remain separate owner-controlled decisions.

approver_github_identity: ThorStarlord
approval_timestamp: 2026-08-01T14:36:00-03:00
authorization_record_sha256: bf31c7b69149965e7156ac1978a40a84e6094a7d1458fa19cf8d165d768b31d6
execution_framework_sha: cad8ef227d6c20a28e786e90c0401f776f4b7b51
target_sha: 0653defb05625f2fcde0ac32eac6e59ccf7eeb90
evidence_number: 0016
evidence_slug: 0016-stage1-auteur-post-remediation-controlled-attempt
exact_model: claude-sonnet-5
authorization_decision: AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION
no_retry_statement: No retry, no rerun, no repair. Exactly one controlled invocation or none.
owner_decision_reference: repository owner decision recorded on 2026-08-01