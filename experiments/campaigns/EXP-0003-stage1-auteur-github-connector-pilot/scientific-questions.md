# Scientific questions — EXP-0003-stage1-auteur-github-connector-pilot

Exploratory (`EXPLORATORY_NOT_CANONICAL_EVIDENCE`), up to three identical attempts, concurrency one, executed by the current coding agent through the connected GitHub surface. No external model/provider API is authorized.

1. **Can the coding agent execute `repo-sensemaker` against Auteur at the exact pinned SHA using connector reads only and produce a `repository_sensemaking_brief` that passes the pinned deterministic validator?** Every attempt uses the same frozen framework/configuration/target identity and every result is reported without selection.

2. **Can GitHub alone serve as the authoritative durable campaign ledger?** Before target access, the results branch must visibly progress through `RESERVED` and then `INVOKED`; after output, the artifact and `OUTPUT_CAPTURED` state must be durable before exact-head validation.

3. **Does interruption recovery remain unambiguous without executor-local state?** A replacement workspace must be able to reconstruct whether an attempt was never reserved, reserved but not invoked, invoked without preserved output, or output-captured awaiting validation solely from GitHub history and state.

4. **Can the campaign preserve fail-closed accounting with no hidden retry?** Under concurrency one, a non-terminal attempt blocks a new reservation; every reserved slot remains visible, including aborts and failures.

5. **How reproducible is the agent-native brief across identical attempts?** Up to three identical-configuration attempts are compared for structural and substantive agreement, with every attempt included in the aggregate report.

The experiment is falsified or remains inconclusive if machine-local evidence is required to distinguish materially different execution histories. All results remain exploratory and may not silently become canonical evidence.
