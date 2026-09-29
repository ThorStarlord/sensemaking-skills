# templates/

Starter files for authors and operators.

| File | Use |
| --- | --- |
| `campaign-policy.yaml` | Example Campaign policy (mission, known transitions, dynamic responsibility policy). |
| `campaign-state.yaml` | Example durable Campaign state. |
| `campaign-handoff.yaml` | Example integrity-bound handoff. |
| `transition-record.yaml` | Example transition record. |
| `sensemaking-config.yaml.template` | Template for a repository's `sensemaking-config.yaml`. |

The Campaign templates are loaded through the production loaders and checked
for round-trip equality by `scripts/campaign-contract-roundtrip.py`. They
are examples: copying one creates no Campaign and grants no authority. See
`docs/sensemaking-campaign.md` and `docs/campaign-cli.md`.
