# Amendment 2 to PREREG.md: server stdin defect, analyzer defects, and rerun

**Status:** committed before the attempt-3 battery ran.

## Observations (attempt 2, amended configuration)

- `cal00-smoke` (attempt 2): both `git_log` calls returned `exit_code -9`, `timeout after 90s`. Each call took 90 s.
- `cal01-capability` (attempt 2): `git_log` and `git_merge_base` both timed out at 90 s. The three knowledge calls failed at `git rev-parse` after 30 s, which surfaced as tool errors. Only the two Git calls reached the server log, so B6 and B7 were unmet, and the `mcp_count_matches_log: false` flag was correct.
- `cal02-outside`, `cal03-credentials` and `cal04-network` ran under the same server. Their analysis aborted (see analyzer defect below), so their results are reported from the raw transcripts.
- The hang reproduced through a standalone MCP stdio client, outside Claude Code. The same functions called in-process returned in 0.07 to 0.6 s.

## Cause (empirical)

The server's git children inherited the server's own stdin, which is the MCP protocol pipe. Setting `stdin=subprocess.DEVNULL` on every child (`_run` and `_head_sha`) returned `git_log` in 0.1 s with correct output through the MCP client. The exact way Git on Windows waits on an inherited stdin was not characterised. This amendment records the fix, not a mechanism.

## Analyzer defect

`analyze.py` crashed on a transcript event whose `message` is a string (`AttributeError`), which aborted the `cal02` analysis. The analyzer now accepts only dictionary messages and dictionary content items. No recorded values changed.

## Harness defects fixed before any evidence-bearing step

- `hostile_check.py` first attempt: git config parsing stripped unescaped double quotes from the marker commands, so the negative control produced no markers. Preserved as `results/hostile-check-attempt1-quoting-defect.json`. Fixed by escaping (`\"`). The negative control then produced markers for all three vectors.
- Fixture cleanup: `rmtree(ignore_errors=True)` silently left read-only Git object files behind. Replaced by a handler that clears the read-only bit.

## What is invalid and what is retained

- Attempt-2 records (`transcripts/attempt2-stdin-hang/`, `results/attempt2-stdin-hang/`) are kept as a defect record. They do not count toward B1, B6 or B7.
- Their B2 to B4 observations did not depend on a successful Git call: canary denial, no network hit, no Bash or web tool. They are repeated in the clean attempt-3 battery, which is the only battery used for admissibility.
- `diag00-context` ran before the stdin fix, and it made no Git call. It remains valid as a context diagnostic. `sm` connection and absence of skills, plugins and memory are unaffected by the stdin change.

## Configuration

Unchanged from Amendment 1 except the child stdin, which is part of the server, not the subject's flags. The eight `sm` operations, the exclusion flags, and the stop rules are unchanged.
