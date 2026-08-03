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
| `configuration_id` | string (sha256 hex) | computed | SHA-256 over the RFC 8785 (JCS) canonical serialization of exactly these fields: `configuration_schema_version`, `framework_sha`, `target_repository`, `target_sha`, `model_identifier`, `prompt_or_skill_revision`, `validator_revision`, `artifact_type`, `execution_parameters`. Excludes `configuration_id` itself and `campaign_id`. See ADR 0023 §10a–§10c for the exact algorithm. |
| `campaign_id` | string | yes | The campaign this configuration was computed under. Configurations are not shared across campaigns even if byte-identical, so budget accounting stays campaign-scoped. |
| `framework_sha` | string (exact commit SHA) | yes | Must be a member of the campaign policy's `allowed_framework_shas`. Never a branch name or `HEAD`. |
| `target_repository` | string (URL) | yes | Must be a member of the campaign policy's `allowed_targets`. |
| `target_sha` | string (exact commit SHA) | yes | Must pair with `target_repository` in the policy's `allowed_targets`. |
| `model_identifier` | string | yes | Must be a member of the campaign policy's `allowed_models`. |
| `prompt_or_skill_revision` | string | yes | Exact revision identifier (e.g. commit SHA, skill version tag) of the prompt/skill used. |
| `validator_revision` | string | yes | Exact revision identifier of the validator that will assess the output. |
| `artifact_type` | string | yes | Must be a member of the campaign policy's `allowed_artifact_types`. |
| `execution_parameters` | object (open-map root field) | yes | Any other execution-relevant parameter that can affect output (e.g. temperature, max tokens, tool allowlist). Empty object is valid; absent is not. `execution_parameters` is schema v1's **sole open-map root field**. Its value, including every mapping recursively nested through mappings or sequences, forms one **open-map subtree** governed by ADR 0023 §10b. Every mapping outside that subtree is closed. Keys inside the subtree are not declared in advance by this table; instead, every key at every nesting level must match `^[a-z][a-z0-9_]*$` and must not be one of the reserved tokens `true`, `false`, `null`, `yes`, `no`, `on`, `off`. Values may recursively be a permitted scalar, a sequence of permitted values, or a nested mapping — itself part of the same open-map subtree, not closed — under the same rules. A mapping nested inside a sequence inside `execution_parameters` is still part of the open-map subtree. Unknown-key rejection for closed schema objects does not apply anywhere inside this subtree; there is no other general unknown-field escape hatch in schema v1, and no other mapping may be treated as open by analogy. |

## Identity rule

`configuration_id` is computed by hashing exactly this field set — no more,
no fewer:

`configuration_schema_version`, `framework_sha`, `target_repository`,
`target_sha`, `model_identifier`, `prompt_or_skill_revision`,
`validator_revision`, `artifact_type`, `execution_parameters`.

Excluded from the hash: `configuration_id` itself (the field being
computed) and `campaign_id` (contextual, not normative-to-the-hash — see
note below). Two attempts share one `configuration_id` **only** when every
field in that list is byte-identical (after canonicalization, ADR 0023
§10a). Any change to any hashed field — including an `execution_parameters`
value — produces a new `configuration_id`. There is no partial-match or
fuzzy-equivalence mode.

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
campaign_id: "EXP-0000-EXAMPLE"
framework_sha: "000000000000000000000000000000000000dead"
target_repository: "https://example.invalid/example-owner/example-target.git"
target_sha: "000000000000000000000000000000000000beef"
model_identifier: "example-model-identifier"
prompt_or_skill_revision: "example-skill@v0.0.0-example"
validator_revision: "example-validator@v0.0.0-example"
artifact_type: "repository_sensemaking_brief"
execution_parameters:
  max_tokens_hint: 4096
  tool_allowlist:
    - "read_repository"
```

This example is authored under the Two-Lane YAML Profile v1 (ADR 0023
§10b): every string-valued field is a single-line quoted scalar (no block
scalar styles); `max_tokens_hint` is an unquoted RFC 8259 number. Every
mapping key (e.g. `repository`, `sha`, `configuration_id`) is an unquoted,
plain ASCII field-name token per the mapping-key grammar in §10b — a
separate lexical class from scalar values, not an exception to the
string-quoting rule.
