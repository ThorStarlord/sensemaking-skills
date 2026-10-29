# Operational Qualification 001: local continuation addendum

Recorded before dispatching either replacement session. The original
[pre-registration](operational-qualification-001-preregistration.md), question
and qualitative reuse criteria are unchanged.

## Recovery boundary

The original Claude Code comparison branches still contain their installation
commits only (`agent-skills-a@055f96f`, `agent-skills-b@45d0cae`). No matching
transcript was found in this machine's Claude project logs. The browser tool
stopped because it could not establish Chrome's current URL; the local Claude
CLI reports `loggedIn: false`. These observations do not establish whether the
cloud runs finished. Their invocation sequence and outcomes remain unassessed.

The first-use artifacts and review are durable in CME PR #104, merged as
`0c439aab8d098a2184d92d0e1e25b71b72482b3c`. PRs #102 and #103 are closed.
Sensemaking PR #649 is merged as
`99da2ba18b6f6fc5af84a5d353bbe612f89694b5`; both hosted workflows passed.

## Replacement conditions fixed before dispatch

This is a new local Codex pair, not a continuation or reconstruction of either
Claude run. It can establish behavior on this host only.

| Condition | Fixed value |
| --- | --- |
| Host | Windows; Codex CLI 0.153.4; signed-in ChatGPT account |
| Model | `gpt-5.6-sol`, reasoning `max`, requested service tier `fast` |
| Skill source | Sensemaking `99da2ba18b6f6fc5af84a5d353bbe612f89694b5` |
| Prompt | "Use the project-installed using-sensemaking Skill." followed by the exact pre-registered question |
| Product baseline | CME `86866634d92254b91896cff3a6f65b889eb338e6` |
| Retained condition | `r1`: CME `0c439aa`, including the seven reviewed `.sensemaking/` files |
| Source-only condition | `r2`: CME `86866634`, with no `.sensemaking/` |
| Installation | Same 182 project Skill files, through `setup-skills --target codex --scope project` |
| Execution | Separate shallow repositories and Codex homes; no Git remotes, previous transcripts, parent conversation, private reasoning or supplied product summary |
| Authority | Read-only sandbox; no product implementation, commits, PRs or external messages by either participant |
| Tools | Same local shell and trusted source CLI; account plugins/apps disabled for these processes; existing user Skill catalog may still be visible |
| Capture | JSONL command/output and agent-message events; final answer; exit status; post-run source checks |
| Dispatch | Start r1 then r2 without inspecting either answer between launches; no steering or corrective follow-up |

The product-tree manifest excluding `.sensemaking/` is identical in both
conditions: SHA-256
`bf65643c715f4ad90486ccf5336fcfbb2e0c2ff8cb105d0cef884ab7b028af49`.
The installed-Skill manifest is identical:
`c5c2ec132b4876a0ef4d32df743a71c46d6fe642820c26130dc58a9edefbc645`.
The installed entrypoint SHA-256 is
`78dab856311d4c1cf5097177e86de23dbddfb1f4e19101c80df82ef9bb9ce290`.
The runs begin at local installation commits `7bd62b8` (r1) and `7fd9cff` (r2).

No index is prebuilt for either participant. Direct record reading is an
eligible reuse mechanism; a query is not required. The CLI is available from
a copy of the pinned trusted source, without any target-repository knowledge.
An inadequate CLI, permission failure or missing required telemetry is a
limitation of the observation, not evidence that the product improved reasoning.

## Non-evidentiary calibration

The disposable calibration task reads a known marker and attempts one write.
It contains no evaluation question or CME evidence. An initial launch lacked
Windows sandbox configuration and could not run reads. A second launch
disabled the required code-mode host and could not execute tools. Neither is
an evidence-bearing run. With the existing `windows.sandbox="elevated"`
configuration explicitly selected and the code-mode host enabled, the third
calibration read `CALIBRATION_7391`, recorded command/output events, and denied
the attempted file write with `Access ... is denied`. No protection was bypassed.

## Interpretation fixed before dispatch

Assess the exact original four consequential-reuse criteria. Report recovered
facts, assumptions, alternatives, authority boundaries and recommendation
differences with source and transcript support. Do not infer superiority from
record counts, token counts, duration, successful queries or shared conclusions.

Distinguish a native Claude `Skill` call, Codex's installed-Skill discovery,
explicit file loading, and a name-only reference. A controller return is
observed only where the participant actually interprets a specialist result
and decides what responsibility follows; a stated sequence alone is insufficient.

This is one qualitative pair, not randomized replicated evidence. The evaluator
already knows the retained records; that limits adjudicator independence. The
filesystem does not prove that a participant cannot read a sibling checkout;
inspect the recorded commands for leakage and report the actual isolation
boundary. Global user Skills and shortened descriptions are shared host
conditions, not evidence of ordinary-language automatic discovery. Do not
claim long-term product benefit, broad host portability or causal superiority.
