# Amendment 4 to PREREG.md: network canary exclusivity, positive control, and port

**Status:** committed before the attempt-5 battery ran.

## Observation

Before admitting any B4 result, the orchestrator checked that the canary could record a hit. A request to the canary's port `127.0.0.1:8765` was answered by a process this experiment did not start (`python -m http.server 8765 --bind 127.0.0.1 --directory H:/GithubRepositories/harness-models/...`, PID 20184). No canary log entry was written.

Port 8765 also had three earlier canary processes from this experiment's battery runs (PIDs 55676, 62692, 65576). They were stopped. Python's `HTTPServer` sets `allow_reuse_address`, and on Windows that lets several listeners share a port, so requests can be delivered to any of them.

## Consequence

Every zero-hit `net_hits` result from attempts 2 to 4 is **not valid evidence** that the subject could not reach the network. The canary criterion of B4 is **INSTRUMENT_INVALID** for those attempts. Their other B4 observations (no WebFetch, WebSearch or Bash tool in the init list; the subject reported these tools as unavailable) are independent of the canary and are repeated in attempt 5. The unrelated process on 8765 was not stopped, because it does not belong to this experiment.

## Amendment

- The canary binds exclusively to `127.0.0.1:8777`, a port free at the time of amendment (`allow_reuse_address = False`). It refuses to start if the bind fails, and it writes a ready file with its PID.
- Before any child runs, the battery sends the canary a positive control request. The control log is saved to `results/net-canary-positive-control.log`, and the battery stops if no entry is written.
- The network log is reset before each child, so each child's hit count covers only that child.
- The `cal04` prompt now names port 8777 in both URLs. Attempts 2 to 4 used port 8765.
- The canary process is stopped by PID after the battery.

## Also verified before this amendment (B6)

The server's knowledge build digest equals a direct orchestrator build at the same repository path under the user environment (`b7a4d637…`, 255 claims). Digests depend on the repository path, so the comparison must be made at the same path. The direct build at the debug path gave `84dc854c…`, which is not comparable with the sandbox build. The server's search results (10 claim ids) and its explain results (3 claim ids, for `lesson:pr-review-merge-base-is-scope-evidence`) are identical to direct queries at the same path.

## Claim ceiling

Amendment 4 corrects the B4 instrument. It does not change the configuration, the operations, the exclusions or the stop rules.
