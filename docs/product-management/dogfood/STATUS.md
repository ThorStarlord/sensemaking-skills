# PM Customer Discovery dogfood status

**Protocol:** `pm-customer-discovery-v1`  
**Repository implementation:** COMPLETE through merged Packages 1–3  
**Implementation merge frontier:** `main@e7d213e07976a2f269b1479fcc36decdcf0cdeb4` (PR #309 merge)  
**Checked-in non-qualifying preflights:** 1  
**Checked-in real-harness functional attempts:** 0  
**Checked-in second-harness portability attempts:** 0  
**Current functional empirical PASS:** NONE  
**Current portability empirical PASS:** NONE  
**External native-harness action required for stronger support/promotion claims:** YES

## What repository evidence proves

The Package 3 final candidate `897e5850a4ab229eeb2c00e23d91339c3bf8e884` passed Product Validation, Lab Validation, and Release Candidate Distribution. Repository tests prove, among other mechanical contracts:

- the five PM artifact IDs route through the specialized PM validator;
- valid PM artifacts can be admitted as exact Campaign evidence and invalid ones fail closed;
- PM capabilities are declared in the current Campaign capability catalog by explicit responsibility type without semantic ranking;
- the same canonical PM Skill bytes can be installed through generic/Codex, Claude, and OpenCode project adapter roots.

These are repository/structural claims. They are not evidence that a real Claude Code, Codex, OpenCode, or other supported coding-agent harness natively discovered and invoked the Skills.

## Non-qualifying preflight evidence

A repository-side preflight was executed on 2026-09-10 using the exact qualified release-candidate distribution from head `707cf3084e82c10fbff20496950f83d9e5450c15` and repository evidence from `ThorStarlord/Chess-Mentor-Engine@4139e4dda567feeadb5684f51c4a265dfae07330`.

The preflight:

- initialized a durable Campaign and advanced into explicit `problem_discovery` responsibility;
- exposed the unranked canonical `discovery` capability candidate;
- produced a contract-valid `discovery_findings` artifact;
- admitted the exact bytes through `validate-pm-artifact.py`;
- closed with `evidence_insufficient` rather than turning repository roadmap evidence into customer truth;
- wrote a handoff, passed `campaign validate`, reconstructed successfully through `campaign resume`, and preserved transition/evidence lineage.

The environment had no Codex, Claude Code, or OpenCode executable and no configured OpenAI/Anthropic API credential. The artifact therefore was not produced through a supported harness's native Skill discovery/invocation path. This preflight is deliberately **not** counted as a real-harness attempt or empirical PASS.

Preserved evidence lives under:

`docs/product-management/dogfood/preflights/2026-09-10-chess-mentor-engine/`

## Qualification-debt policy

Native-harness and second-harness validation remain required for the corresponding stronger claims, but they no longer block separately authorized repository implementation of additional PM capability waves.

Repository-qualified capabilities may therefore accumulate while these fields remain `NONE`/`pending`. They must not be described as native-harness-qualified, portability-qualified, or promoted until actual evidence exists.

See `../qualification-levels.md`.

## Required future empirical evidence

Follow `docs/product-management/dogfood-runbook.md`:

1. run a real Customer Discovery responsibility/Campaign on one supported native harness;
2. perform a fresh-context reconstruction from durable repository/Campaign state without prior chat;
3. run an equivalent bounded responsibility through a second supported native harness;
4. preserve the exact attempt evidence and classify the result honestly.

Until that evidence exists, do not claim `FUNCTIONAL_PASS_PORTABILITY_PASS`. Continued repository implementation does not retire this qualification debt.