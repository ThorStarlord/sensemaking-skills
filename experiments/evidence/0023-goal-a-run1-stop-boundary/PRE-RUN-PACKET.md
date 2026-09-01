# GOAL_A_AUTEUR_TARGET1 — PRE-RUN PACKET + INDEPENDENCE VERIFICATION

## Authorization
- Goal A / A1 Target 1 = ThorStarlord/auteur, authorized by owner (directive #35).
- Execution mode = Mode 1 (isolated task sub-agents for producer / auditor / evaluator), owner-selected.
- AUTEUR_RUN_1 only; AUTEUR_RUN_2 only if no Run-1 stop rule triggers; no Target 2.

## Pins
- TARGET_REPOSITORY = ThorStarlord/auteur
- TARGET_SHA = a6f7ded7d01cfdd149c526a71e0c751af517e0b1 (read-only, clean, HEAD==pinned, 1754 tracked files)
- SENSEMAKING_SHA = f83fd773f6b9adeb354790b3764cbcb2bd5acbf3
- PROTOCOL = docs/research/goal-a-external-product-validation-protocol.md @ f83fd77
- FROZEN TASK (verbatim) = "Establish from the current repository evidence what the most consequential
  remaining boundary is for Auteur and what work, if any, is warranted next. Consider the current code,
  tests, documentation, open work, and repository history as evidence. Do not assume that any existing issue,
  research program, implementation proposal, release concern, or previously important boundary is still
  primary. Distinguish demonstrated facts, derived evidence, interpretation, and unresolved hypotheses.
  Produce the canonical repository_sensemaking_brief. Do not mutate the target repository."
- TASK_TEXT_SHA256 = 4C7574A0B4A90029A96A04A4A6D45A2F0865963A23AFCD9BFC20184C531CB65D
- FREEZE DATE = 2026-08-31 (pinned protocol revision f83fd77)

## SUBAGENT_CONTEXT_ISOLATION = VERIFIED_BY_TOOL_CONTRACT (with documented limitation)
- Mechanism: host `tool:task` sub-agent, per its spec: "The sub-agent runs in its own session";
  "supply arguments describing the concrete task since the subagent has no other context";
  "Only its final answer is returned."
- producer_context_inputs = frozen task + pinned Auteur repo path/SHA + pinned Sensemaking revision + ordinary
  product instructions (canonical brief output; do not mutate target). NO prior Auteur diagnosis, NO Goal A
  results, NO owner conversation, NO Product Hypothesis B goals, NO PARTIAL desire, NO expected implementation.
- auditor_context_inputs = frozen unmodified brief + pinned target repo evidence + canonical audit instructions
  (§17). NO producer reasoning/context beyond the brief, NO evaluator judgment.
- evaluator_context_inputs = frozen unmodified brief + canonical §19 E1-E7 inputs. NO producer context,
  preferably NO auditor reasoning (unless protocol explicitly requires).
- cross_role_hidden_context_inheritance = false (per tool contract: own session, no parent/sibling context,
  only final answer returned).
- Documented limitation / honesty note: I cannot independently introspect a sub-agent's internal session
  state beyond the host tool contract. Isolation is established by the tool's documented semantics
  (own session + dispatched-packet-only + final-answer-only). If the host's task tool does not actually bind
  to that contract, the episode would be non-independent — flagged and cannot support A1_POSITIVE. All
  dispatches avoid leaking Auteur diagnosis or cross-role context.

## Eligibility (pre-dispatch, no substantive sensemaking)
- 6.1 external; 6.2 real revision; 6.3 substantive (1754 files: src/docs/tests/skills/scripts); 6.4 evaluable;
  8.1 real consequential decision; 8.2 >=2 plausible next responsibilities; 8.3 no preferred-boundary leak.
- TARGET_TASK = VALID.

## Disposition if isolation unverifiable before Run 1
GOAL_A_INDEPENDENCE_MECHANISM_UNVERIFIED — would stop before dispatching Run 1.
