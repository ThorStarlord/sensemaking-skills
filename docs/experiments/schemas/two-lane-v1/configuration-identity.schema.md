# Schema: Configuration Identity (v1)

The frozen, hashable set of every execution-relevant input for one kind of
attempt. See ADR 0023 §9d, Terminology, §10. Computed once per distinct
configuration, referenced by `configuration_id` from every attempt that
shares it.

**This schema is not enforced by any runtime component in this phase.**

## Required fields

| Field | Type | Immutable | Description |
|---|---|---|---|
| `configuration_schema_version` | string | yes | Must be `"1"`. |
| `configuration_id` | string (sha256 hex) | computed | Digest of every other normative field below, canonical serialization per ADR 0023 §10. |
| `campaign_id` | string | yes | The campaign this configuration was computed under. Configurations are not shared across campaigns even if byte-identical, so budget accounting stays campaign-scoped. |
| `framework_sha` | string (exact commit SHA) | yes | Must be a member of the campaign policy's `allowed_framework_shas`. Never a branch name or `HEAD`. |
| `target_repository` | string (URL) | yes | Must be a member of the campaign policy's `allowed_targets`. |
| `target_sha` | string (exact commit SHA) | yes | Must pair with `target_repository` in the policy's `allowed_targets`. |
| `model_identifier` | string | yes | Must be a member of the campaign policy's `allowed_models`. |
| `prompt_or_skill_revision` | string | yes | Exact revision identifier (e.g. commit SHA, skill version tag) of the prompt/skill used. |
| `validator_revision` | string | yes | Exact revision identifier of the validator that will assess the output. |
| `artifact_type` | string | yes | Must be a member of the campaign policy's `allowed_artifact_types`. |
| `execution_parameters` | object | yes | Any other execution-relevant parameter that can affect output (e.g. temperature, max tokens, tool allowlist). Empty object is valid; absent is not. |

## Identity rule

Two attempts share one `configuration_id` **only** when every field above
(excluding `configuration_id` itself and `campaign_id`, which is contextual
not normative-to-the-hash — see note) is byte-identical. Any change to any
field — including an `execution_parameters` value — produces a new
`configuration_id`. There is no partial-match or fuzzy-equivalence mode.

> Note: `campaign_id` is included in the document for context and is part of
> what scopes budget accounting, but implementations MUST compute
> `configuration_id` from the execution-relevant fields only, so that the
> same underlying configuration is recognizably "the same bytes" if it were
> ever compared across campaigns, even though campaigns never share attempt
> budgets.

## Fail-closed rules

- Any field using a mutable ref (branch name, tag that can move, `HEAD`,
  `latest`): reject at preparation time.
- `framework_sha`, `target_repository`+`target_sha`, `model_identifier`, or
  `artifact_type` not present in the governing policy's allowlists: reject
  (this is a policy-conformance check performed by the future consumer, not
  by this schema alone, but the schema's fields are what that check reads).
- The recomputed `configuration_id` must be checked against **both**: (1)
  the `configuration_id` value carried by this document (they must match
  exactly, or the document is corrupt/tampered), and (2) independently,
  membership in the governing policy's `allowed_configuration_ids`
  (`campaign-policy.schema.md`). Matching only one of the two is not
  sufficient authorization — see that schema's "Conjunctive authorization
  semantics" for the full check list.

## Example — EXAMPLE_ONLY_NOT_OPERATIVE

```yaml
configuration_schema_version: "1"
configuration_id: "1111111111111111111111111111111111111111111111111111111111111111"
campaign_id: EXP-0000-EXAMPLE
framework_sha: "0000000000000000000000000000000000dead"
target_repository: "https://example.invalid/example-owner/example-target.git"
target_sha: "0000000000000000000000000000000000beef"
model_identifier: "example-model-identifier"
prompt_or_skill_revision: "example-skill@v0.0.0-example"
validator_revision: "example-validator@v0.0.0-example"
artifact_type: repository_sensemaking_brief
execution_parameters:
  max_tokens_hint: 4096
  tool_allowlist:
    - "read_repository"
```
