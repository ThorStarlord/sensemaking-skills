# Coding-agent and harness independence

## Product contract

Canonical Product Management semantics must remain independent of the coding agent that executes them.

```text
canonical PM domain
  responsibility + methodology + evidence + artifact + authority
                       |
                       v
                Campaign substrate
                       |
                       v
                harness adapters
          /------------|-------------\
       Claude        Codex        OpenCode
                       |
                 future harness
```

## Canonical capability restrictions

A canonical PM capability must not require, to express its semantics:

- Claude `/command` syntax;
- `$ARGUMENTS` or another vendor placeholder;
- `~/.claude`, `$CODEX_HOME`, `.opencode`, or another discovery root;
- a proprietary tool name;
- vendor-specific session state;
- OpenAI UI metadata;
- a particular chat-history implementation.

A capability may document a generic requirement such as "read the supplied evidence" or "return the artifact to the active agent". The harness decides how those operations are represented.

## Adapter responsibilities

A harness adapter may:

- resolve a target discovery directory;
- copy/render the canonical Skill tree;
- add required target metadata that does not change semantics;
- report availability;
- capture native setup/invocation evidence;
- translate benign invocation conventions.

An adapter may not:

- change methodology;
- change PM responsibility semantics;
- weaken evidence requirements;
- change the canonical output artifact contract;
- grant authority;
- rank capabilities;
- declare semantic success.

## Existing setup architecture

Sensemaking already uses explicit adapters for generic Agent Skills, Claude Code, Codex, and OpenCode. PM capability installation should flow through the same source-tree packaging and setup machinery rather than creating a second PM installer.

## Portability qualification

Structural independence is necessary but not sufficient. After the Customer Discovery implementation is complete:

1. run a real functional PM Campaign on one supported harness;
2. run an equivalent bounded canonical responsibility on a second supported harness;
3. compare invariant behavior: capability identity, responsibility, artifact type, evidence rules, validator, authority boundary, and stop semantics;
4. record material divergence honestly.

The model prose need not be byte-identical. The product contract must be invariant.
