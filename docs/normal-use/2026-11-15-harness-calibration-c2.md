# Harness calibration C2 and C3 (2026-11-15): non-evidentiary

**Status:** calibration record for the #873 harness-admissibility qualification issue. It uses throwaway canary tokens and planted evaluator inputs. None of these runs is an evidence-bearing study cell, and none supports a cognitive claim. The stream-json transcripts for X1 to X6b, X9, X10a and X10b, the run scripts and the session index are in `experiments/cognitive-method-qualification-872/calibration/C2-transcripts/`. X7 and X8 are withheld from the repository because their answers echo the user's persistent memory index. Their session files are recoverable on this host under `~/.claude/projects/<cwd-key>/<session-id>.jsonl`, and their session ids are in `index-c2.txt`.

**Why this record exists.** C1 (`docs/normal-use/2026-11-15-cognitive-method-learning-construction.md`, section 2) recorded NOT_ADMISSIBLE. Its remedy, per-arm configuration isolation, was untested. This record tests a configuration remedy using the local Claude Code CLI, which is not the Agent-tool subagent path that C1 used.

## 1. Configuration tested

Claude Code `2.1.266`, model `claude-haiku-5-5`, headless `claude -p` with `--output-format stream-json --verbose`, a fresh session id per run (`--session-id`), a fresh empty working directory per arm, and `--max-budget-usd` as a cost cap. Each child receives the same environment wrapper, which removes inherited `CLAUDE*` and `ANTHROPIC*` variables except `ANTHROPIC_BASE_URL`.

Two isolation flags were compared:

- `--safe-mode`: documented as disabling CLAUDE.md, skills, plugins, hooks, MCP servers, custom agents and output styles, while leaving auth, model and built-in tools working.
- `--restricted`: documented as ignoring user, project and local settings files, and confining file tools to the working directories (`--add-dir` included).

## 2. Results

| Run | Purpose | Configuration | Observed | Result |
| --- | --- | --- | --- | --- |
| X1 | Detection positive control: ambient CLAUDE.md | no safe mode, canary CLAUDE.md in cwd | the canary was reported; init lists 198 skills, the superpowers plugin and 2 hook events | PASS (sensitivity) |
| X2 | Isolation negative control: same directory | `--safe-mode` | canary not reported; init lists 16 bundled built-in skills, no user skills, 0 hook events, 0 MCP servers | PASS |
| X3 | Controlled treatment channel, positive | `--safe-mode`, `--append-system-prompt` with a token | only the treatment arm reported the token | PASS |
| X4 | Baseline after treatment, cross-run leakage | `--safe-mode`, no append, run after X3 | token not reported | PASS |
| X5 | Responder blindness | separate session, no treatment channel | treatment-token search returned NONE | PASS (weak: the responder never held the token) |
| X6a/b | Escalation transport | phase 1 emits ESCALATE; a scripted responder answers from a key outside child directories; phase 2 uses `--resume` on the same session id | question emitted, then the answer was used in the same session | PASS (responder was a script, not a model) |
| X7 | Ambient memory positive control | no safe mode, in the main checkout | the persistent memory index was reported | PASS (sensitivity) |
| X8 | Ambient memory negative control | `--safe-mode`, same directory | no memory index reported; init shows 0 MCP servers | PASS |
| X9 | Tool telemetry and ordering | `--safe-mode`, `--tools Read` | one Read tool_use, then tool_result, then the final text, in stream order; session file has per-record timestamps | PASS |
| X10a | File-read confinement without restriction | `--safe-mode`, Read allowed, file outside cwd | the Read succeeded and returned the outside file's content | **FAIL: safe mode alone does not confine file reading** |
| X10b | File-read confinement with restriction | `--safe-mode --restricted`, same request | Read refused: "outside the working directory" (`is_error: true`) | PASS |

All successful runs have a session file on disk. The three failed attempts from the first invocation (a flag-ordering error) have none.

## 3. Findings

1. **Safe mode excludes the ambient instruction, memory and skill surfaces.** Repository CLAUDE.md (X2), persistent memory (X8), user-level skills and superpowers hooks (X2) and MCP connectors (X1 has 4, X2 has 0) are all absent under `--safe-mode`. The 16 built-in bundled skills remain in every arm, so they are a shared condition.
2. **Safe mode does not confine file reading.** X10a read a file outside the working directory. A fixed-method arm with any read tool could reach the reviewed knowledge store or the repository by absolute path. Adding `--restricted` (X10b) refused the same read. The required remedy is therefore `--safe-mode --restricted` together with an explicit tool allowlist.
3. **Self-report is not an instrument.** In X1 the child reported `LINE2 NONE` while its init record listed 198 skills. Skill and memory exposure must be taken from the stream-json `init` record and not from the child's own account.
4. **Telemetry is recoverable.** Stream events, tool_use and tool_result ordering, and per-record timestamps in the session file were all present for every successful run.
5. **A limitation the configuration does not remove.** Every run wrote `[claude-code:unrecognized_model]` to stderr for `claude-haiku-5-5`. The init record still reports that model. The CLI may use fallback metadata for cost or context, so the model identifier is recorded but not independently verified.
6. **Environment dependency.** The superpowers SessionStart hook failed in non-safe runs with "requires bash but Git Bash was not found". The cause was not isolated. The hook is suppressed under safe mode, so it does not affect the arms.

## 4. Evaluator calibration (C3)

C3 tests the blind evaluator protocol on five planted responses whose correct rubric scores were written before the run: three for the D1 rubric and two for the D2 rubric. Each is scored in a separate evaluator session, with `--safe-mode --restricted --tools ""`, and sees only the rubric and one relabelled response.

- **First run:** four of five vectors matched. The one mismatch was `planted-D1-mid` on K3. My expected vector was wrong: K3 requires the response to state what the setting excludes, and that response names `--safe-mode` without saying what it excludes. The evaluator's 0 matches the rubric text.
- **Correction, before any subject run:** the expected vector was changed to `[1,0,0,0,0]`, and the K3 wording was tightened to require a stated exclusion. The change is disclosed in `calibration/C3-evaluator-planted/expected.json`.
- **Final run, under the tightened rubric:** all five planted vectors match.

The evaluator is a separate session from the subject and from the orchestrator. It has no access to arm labels, and it has no tools.

## 5. Gate disposition for this configuration

Against `docs/experimental-phase-gates.md` (HARNESS READY), for `--safe-mode --restricted` with the frozen tools allowlist:

- Frozen conditions reproduced: model, CLI version, flags and init record matched across the safe runs. Partly met: the identifier warning above.
- Telemetry observable: met (finding 4).
- Isolation demonstrated: met for instructions, memory, skills, hooks and MCP servers, and for file reading with `--restricted` (findings 1 and 2). Fresh session per run and no cross-run leakage: met (X4).
- Responder/escalation transport: met as a mechanism, with a scripted responder. An LLM responder has not been exercised.
- Non-evidentiary calibration: met for C2 and C3, with the corrections above.

This record makes no disposition on the evidence-bearing study cells. The subject episodes and their pre-registration are in `experiments/cognitive-method-qualification-872/`.

## 6. Claim ceiling

This record establishes harness behavior for one CLI version, one model identifier and one host. It does not establish cognitive benefit, independence of any model's reasoning, or a result for any real task.
