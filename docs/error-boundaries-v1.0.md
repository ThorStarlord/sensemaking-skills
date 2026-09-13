# Version 1.0 Error-Boundary Policy

The stable product translates failures only at explicit boundaries:

- Click converts malformed command input into exit code `2`.
- Campaign workspace and transaction failures become typed Campaign errors and
  exit codes `3` or `4`.
- Artifact validation failures become typed artifact errors and exit codes `5`
  or `6`.
- Filesystem containment, bundle verification, and schema migration fail
  closed and preserve the underlying exception as context.

Broad catches in the stable product are permitted only when they immediately
re-raise a typed error, return a structured failure result, or perform
best-effort cleanup while preserving the primary exception. They must not turn
an invalid or incomplete operation into success.

The retained runner and laboratory code is outside the stable runtime promise
and is qualified in its own lane.
