# GOAL_A_HARNESS_V3_QUALIFICATION (external-process / raw-artifact transport) — NOT QUALIFIED

## GOAL_A_HARNESS_V3_RESULT = EXTERNAL_RUNTIME_UNAVAILABLE

Prior dispositions preserved unchanged:
- Attempt 1: `HARNESS_ENVIRONMENT_FAILURE` (`RUN1-STOP-BOUNDARY.md`)
- Harness qualification v1: `LOSSLESS_ARTIFACT_CAPTURE_UNAVAILABLE` (`GOAL-A-HARNESS-QUALIFICATION.md`)
- Harness qualification v2: `FRAMED_RETURN_NOT_LOSSLESS` (in-session record; task-sub-agent marker
  frame did not arrive in the extractable parent return)

All three remain historically correct.

## What was built and frozen (directive §2–§3)

Operator workspace OUTSIDE both pinned checkouts:
`H:\GithubRepositories\goal-a-harness-v3-workspace` (not committed to any repo).

Minimal harness, frozen before canaries (`evidence/HARNESS_FREEZE.json`):
- `harness/role_runner.py` sha256 `d75f42533e2c9385d5bc59f2cd9ab82f66bd662f9330e35c934eac6c69a163f9`
  — one OS process = one role; `claude_agent_sdk.query()` one-shot, no resume /
  no `continue_conversation`, `setting_sources=[]` (no ambient CLAUDE.md/settings),
  `disallowed_tools=[Edit,Write,NotebookEdit,MultiEdit]`. Takes `ResultMessage.result`,
  UTF-8 encodes, sha256 in memory, binary-writes bytes. No semantic parsing.
- `harness/goal_a_operator.py` sha256 `8ee7a9ada0f03bf4f8dc00ad11d496a1f2fea579632e98182fa7f97a67030310`
  — spawns `role_runner.py` as a separate process, reads persisted bytes back,
  recomputes sha256, asserts in-memory == persisted.

Runtime present: python 3.14.3, `claude` CLI 2.1.101, `claude_agent_sdk` 0.2.82,
`anthropic` 0.116.0, node v24.14.1.
`FINAL_RESULT_SURFACE = claude_agent_sdk.ResultMessage.result` — identified.

## Where it stopped (directive §9 / §17)

The **transport canary (§10)** — the first substantive step — failed at
**child-process authentication**, before any losslessness / freshness / probe-capability
test could run.

Empirical chain:
1. `claude_agent_sdk.query()` in a spawned process → SDK error
   `Claude Code returned an error result: success` (child `claude` exited abnormally).
2. Direct `claude -p --output-format json` in a fresh shell →
   first needs `CLAUDE_CODE_GIT_BASH_PATH` (set it to `H:\Program Files\Git\bin\bash.exe`),
   then returns `is_error:true`, `result: "Not logged in · Please run /login"`.
3. `~/.claude/.credentials.json` → `claudeAiOauth.accessToken` length 0,
   `refreshToken` length 0, `expiresAt` 0.
4. No `ANTHROPIC_API_KEY` in environment. `anthropic.Anthropic()` →
   `Could not resolve authentication method`.
5. `~/.claude/session-env/*` dirs empty; `~/.claude/proxy` has no usable local
   auth endpoint.

**Root cause:** the parent Claude Code session's credentials are host-injected at
runtime over an IPC channel (`CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH` /
`CLAUDE_CODE_SDK_HAS_OAUTH_REFRESH`, `CLAUDE_CODE_MESSAGING_SOCKET`). A genuinely
separate external process starts its own auth resolution, finds no token, and cannot
run. This is not a losslessness problem — the external-process substrate cannot be
instantiated as an authenticated fresh agent session at all in this environment.

Bridging the parent's host-auth IPC to a child was **not** attempted: it is the
"bend the substrate" move the owner has twice declined, and tunnelling host
credentials to a spawned process is a security-sensitive action not to be taken on
agent initiative.

## Disposition / required return (directive §20)

- `GOAL_A_HARNESS_V3_RESULT = EXTERNAL_RUNTIME_UNAVAILABLE`
- `HARNESS_WORKSPACE = H:\GithubRepositories\goal-a-harness-v3-workspace`
- `HARNESS_FILE_SHA256 =` role_runner `d75f4253…`, goal_a_operator `8ee7a9ad…`
- `EXTERNAL_RUNTIME = claude_agent_sdk 0.2.82 → claude CLI 2.1.101` (also probed `claude -p`, `anthropic` 0.116.0)
- `RUNTIME_VERSION = python 3.14.3 / claude-cli 2.1.101 / sdk 0.2.82 / anthropic 0.116.0 / node v24.14.1`
- `EXTERNAL_SESSION_MECHANISM = one OS process/role → sdk.query() one-shot; no resume; setting_sources=[]`
- `RESUME_USED = false`
- `FINAL_RESULT_SURFACE = claude_agent_sdk.ResultMessage.result` ; `FINAL_RESULT_SURFACE_IDENTIFIED = true`
- `RAW_RESULT_CAPTURE_AVAILABLE = false` (child session cannot authenticate)
- `TRANSPORT_CANARY_BYTE_LENGTH = n/a` ; `TRANSPORT_CANARY_IN_MEMORY_SHA256 = n/a` ; `TRANSPORT_CANARY_PERSISTED_SHA256 = n/a`
- `RAW_ARTIFACT_BYTE_EQUIVALENT = false` ; `PRACTICAL_SIZE_CAPTURE_PASS = false`
- `EXTERNAL_SESSION_FRESHNESS = NOT_ESTABLISHED` ; `CROSS_SESSION_CANARY_LEAKED = unknown`
- `PINNED_AUTEUR_OBSERVED_SHA = a6f7ded7d01cfdd149c526a71e0c751af517e0b1` ; `PINNED_AUTEUR_CLEAN = true` (verified before and after; no role ever dispatched against it)
- `PINNED_SENSEMAKING_OBSERVED_SHA = f83fd773f6b9adeb354790b3764cbcb2bd5acbf3`
- `PRODUCER_RUNTIME_HAS_REQUIRED_PROBE_CAPABILITY = NOT_REACHED`
- `FRESH_ROLE_CAN_READ_PERSISTED_ARTIFACT = NOT_REACHED`
- `FRESH_AUTEUR_RUN1_DISPATCHED = false`
- `FAILED_PRIOR_OUTPUT_REUSED = false` ; `FAILED_PRIOR_DIAGNOSIS_SHARED = false`
- `ISSUE_218_MODIFIED = false` ; `ISSUE_226_EXECUTED = false` ; `TARGET2_SELECTED = false`
- `PRODUCT_REPAIR_PERFORMED = false` ; `PROTOCOL_CHANGED = false`
- `NEW_GENERALIZED_HARNESS_FRAMEWORK_CREATED = false`
- `NEXT_WARRANTED_RESPONSIBILITY = OWNER_REVIEW_OF_EXTERNAL_PROCESS_CAPABILITY_BOUNDARY`

## Consequence (matches the owner's stated fallback)

Three execution substrates have now been falsified for the Goal A lossless-frozen-artifact
contract in this environment:
1. isolated task sub-agent, direct file write — blocked;
2. isolated task sub-agent, framed return — frame not delivered to parent recorder;
3. external OS process (`claude_agent_sdk` / `claude` CLI / `anthropic` SDK) —
   cannot authenticate a fresh separate session.

The owner's v3 directive states: "If v3 also fails, I would stop Goal A execution in
this environment entirely rather than design Harness v4." Per that rule, **no Harness
v4 is attempted and no Auteur producer run is consumed.** Goal A execution is halted
in this environment pending an owner decision — the realistic options being an
environment that provides an independent API key / credential for external one-shot
sessions, or running Goal A on a different host where separate authenticated agent
processes are available.
