# PM Customer Discovery non-qualifying preflight — Chess Mentor Engine

**Date:** 2026-09-10
**Protocol context:** `pm-customer-discovery-v1`
**Classification:** NON-QUALIFYING PREFLIGHT / empirical result remains PENDING
**Sensemaking distribution source:** GitHub Actions release-candidate artifact from exact head `707cf3084e82c10fbff20496950f83d9e5450c15`
**Target repository evidence:** `ThorStarlord/Chess-Mentor-Engine@4139e4dda567feeadb5684f51c4a265dfae07330`
**Native coding-agent harness invocation:** ABSENT
**Native setup/invocation evidence:** ABSENT

## Why this does not qualify Gate A

The execution environment had no `codex`, `claude`, or `opencode` executable and no configured OpenAI/Anthropic API credential. The PM artifact was authored by the current assistant using the packaged Skill contract as guidance rather than invoked through a supported harness's native Skill discovery mechanism. Therefore this evidence MUST NOT be counted as a real-harness functional attempt or empirical PASS.

## What the preflight did prove

1. The exact qualified wheel artifact can be installed and its Campaign CLI invoked.
2. A Campaign can be initialized and advanced into an explicit `problem_discovery` responsibility.
3. `campaign capabilities --responsibility-type problem_discovery` returns exactly one unranked declared candidate: `discovery`, with `output_artifact: discovery_findings` and no repository mutation authority.
4. A repository-evidence-only `discovery_findings` artifact can pass the packaged specialized PM validator.
5. `campaign ingest` admits the exact artifact bytes through `validate-pm-artifact.py` and records content-addressed artifact/admission receipts.
6. The Campaign can close honestly with `evidence_insufficient`, write a durable handoff, validate successfully, resume in a fresh process, and reconstruct exact evidence/transition lineage.
7. The PM result does not convert software qualification into customer truth: repository evidence identifies unresolved hypotheses but cannot establish which user-facing problem dominates in actual use.

## Artifact identity

- artifact id: `discovery_findings`
- artifact SHA256: `371a19e90390d24c9f235e41c3e6061f27243e1960d6b48183173a6afc02206c`
- artifact ref: `artifacts/discovery_findings/371a19e90390d24c9f235e41c3e6061f27243e1960d6b48183173a6afc02206c.md`
- admission ref: `admissions/discovery_findings/37b257bed48d94e73e49b07d44355dc1352ef94fb24e43d7a969796defb19af1.yaml`
- specialized validator: `validate-pm-artifact.py`
- validator SHA256: `6799d552214348aa7b227c1fdc152ff184a9aa857bb47f7a7c4a6f44a593bc2d`
- router SHA256: `9c3f97a2055ba9b5c64ebcd5a8ed47ed0dd9103e4d2b98ad3d1b46a1b346457b`
- handoff reconstruction SHA256: `8efe4d89feae93d2efd97a514dd29e482757570512e1c9ce56c846d9304fc99d`
- local preflight package SHA256: `9e1d3a3979c9857b590cd84e816fb55bc1e58c04b7dedd36deaacff6c61898e6`

## Product discovery result

The preflight left three hypotheses explicit:

- H-1: the diagnostic-candidate-to-tutor-session bridge may be a material workflow bottleneck;
- H-2: model-authored mentor output quality/trust may be a material bottleneck once M19 is used in practice;
- H-3: production provider selection should remain deferred until provider-neutral output evaluation criteria exist.

H-1 and H-2 remain untested. H-3 is repository-evidence-backed only as a sequencing constraint, not as customer preference.

## Next legitimate action

Run the same bounded `problem_discovery` responsibility through a real supported native coding-agent harness, preserving native setup and invocation evidence. Then perform fresh-context reconstruction and an equivalent bounded responsibility in a second harness. Until then, `FUNCTIONAL_PASS_PORTABILITY_PASS` remains unsupported.
