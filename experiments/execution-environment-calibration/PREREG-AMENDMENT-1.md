# Amendment 1 to PREREG.md: replace `--safe-mode` with verified explicit exclusions

**Status:** committed before any amended-configuration child ran.

## Observation that triggered the amendment

CAL-00 attempt 1 (`cal00-smoke`, `--safe-mode --restricted --strict-mcp-config --mcp-config <sm>`):

- Exit 0, model `claude-haiku-5-5`, tools `Glob, Grep, Read` only, clone clean.
- The `system/init` record reported `mcp_servers: []`. The model replied that no `sm` tool was available, so **B1 failed**: no Git or CLI operation ran.
- Cause: `--safe-mode` disables "MCP servers" as a customization, and an explicit `--mcp-config` does not override it.
- The first analysis run reported `mcp_count_matches_log: true` and `canary_leak_free: true`. Both were **vacuous**. Zero MCP calls matched zero log entries, and no canary was printed because nothing was read. The analysis now requires `sm` status `connected` before any B1 or B7 pass. The superseded summary is kept as `results/cal00-smoke.summary.json` for record, with this note.

The init record of attempt 1 also showed what safe-mode had excluded and what it had not: 17 bundled skills, one builtin plugin (`plugin-authoring`), no user skills, no user agents beyond the built-in four. Safe-mode's exclusion of user memory, CLAUDE.md and user hooks is therefore not yet verified by this record.

## Amended configuration (replaces PREREG.md section 3, flags only)

```text
claude -p "<prompt>" --restricted --strict-mcp-config --disable-slash-commands --setting-sources ""
  --model claude-haiku-5-5 --output-format stream-json --verbose --max-budget-usd <cap>
  --tools "Read,Grep,Glob" --allowedTools "<Read,Grep,Glob and the eight sm tools>"
  --mcp-config <sandbox>/mcp-config.json
  (cwd = <sandbox>/repo, no --add-dir)
```

- `--restricted` ignores user, project and local settings files, confines file tools to the working directory, and removes Bash and web tools unless `--tools` names them. `--strict-mcp-config` loads only the `sm` server.
- `--disable-slash-commands` removes skills. `--setting-sources ""` removes settings sources. Together these are the explicit replacement for safe-mode's exclusion of skills and hooks.
- **Not yet verified and therefore not assumed:** exclusion of user-level CLAUDE.md and auto-memory. Diagnostic `diag00-context` tests these before any MCP calibration. If either still reaches the subject, the scope is **NOT_ADMISSIBLE** for any episode until the exclusion is demonstrated or an alternative is preregistered.
- Repository CLAUDE.md in the pinned clone is not loaded. Its exclusion is a deliberate design choice, as in #873: its pointer to the semantic knowledge process would otherwise act as an instruction rather than an opportunity.

## Diagnostic before the B1 to B9 battery

`diag00-context` asks a no-tool question about skills, plugins, agents, memory or CLAUDE.md-style instructions, and the MCP tools it can call. Pass criteria:

- No user or project skills; no user agents.
- No memory or CLAUDE.md-style instruction reported (the subject quotes the first sentence of anything it was given before the user message, if any).
- `sm` tools present.

Then CAL-00 is rerun. The B1 to B9 battery runs only after CAL-00 passes with `sm` connected.

## Claim ceiling

This amendment changes only the exclusion mechanism. It does not change the consumer, the mechanism A decision, the eight operations, or the stop rules.
