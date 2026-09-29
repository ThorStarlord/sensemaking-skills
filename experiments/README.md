# experiments/

Records of the two-lane experiment program (ADR 0023) and other bounded
research trials. Nothing here is product behavior.

| Path | Contents |
| --- | --- |
| `campaigns/EXP-000N-*` | Campaign packages: policy, configuration, approval, attempts, reports. EXP-0001 is preparation only; see each package README for its own status. EXP-0002 used the coding-agent-native path (`docs/coding-agent-native-campaign.md`). |
| `results/` | Committed results for executed campaigns. |
| `run-control/` | Controlled-attempt records. |
| `evidence/` | Numbered evidence records (`00NN-*`) supporting ADR/roadmap claims. |
| `evaluation-design-*`, `product-*`, `solution-interaction-*`, `post-hardening-*`, `clean-install-*`, `intelligence-components-v0` | Pre-registered evaluation designs and probes. |

**Evidence ceiling:** exploratory results are
`EXPLORATORY_NOT_CANONICAL_EVIDENCE` unless a package explicitly records
otherwise. Repository tests passing is not native-harness qualification
(`docs/operations-runbook.md`, "Native-harness / empirical evidence ceiling").
Governance: `docs/experimental-phase-gates.md`, `docs/qualification-evidence.md`,
`docs/experiments/schemas/two-lane-v1/README.md`.
