# Scientific questions — EXP-0002-stage1-auteur-coding-agent-pilot

Exploratory (`EXPLORATORY_NOT_CANONICAL_EVIDENCE`), three identical
attempts, concurrency one, executed by the coding agent itself
(`execution_mode: coding_agent_native`, no external model API).

1. **Can a coding agent, executing the `repo-sensemaker` skill directly
   against the Auteur repository at a pinned SHA, produce a
   repository_sensemaking_brief that passes the pinned validator?**
   Each attempt is one independent run of the same skill against the same
   bytes; the aggregate structural/substantive pass rate is reported
   without selection.

2. **How reproducible is the agent-native brief across identical
   attempts?** Three identical-configuration attempts are compared for
   structural and substantive agreement; every attempt (including
   failures) is preserved and reported.

3. **Is the two-phase bookkeeping protocol (prepare / finalize) a sound
   execution boundary for agent-native campaigns?** The ledger must show
   exactly one reservation and INVOKED transition per attempt, a terminal
   state per attempt, and no hidden retries or refunds; the approval
   comment is re-verified before every prepare and finalize.

All results are exploratory and may not be promoted to canonical
evidence.
