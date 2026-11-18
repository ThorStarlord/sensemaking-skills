# Receiving-agent adaptation: #909 record (2026-11-18)

**Status:** record for [#909](https://github.com/ThorStarlord/sensemaking-skills/issues/909) under parent [#906](https://github.com/ThorStarlord/sensemaking-skills/issues/906). One fresh receiving-agent episode on a real engineering responsibility. The engineering change merged as [PR #913](https://github.com/ThorStarlord/sensemaking-skills/pull/913) (merge `6f27122b`). The receiving agent's own interpretation is retained as an attributed `observation` claim. It is **not** a lesson, a rule or a shared policy. Independent later-agent reuse, predecision benefit and comparative value remain NOT QUALIFIED under [#872](https://github.com/ThorStarlord/sensemaking-skills/issues/872) and [#874](https://github.com/ThorStarlord/sensemaking-skills/issues/874).

**Source boundary:** `origin/main` at `c8859a2f`, the commit the receiving agent started from. Its worktree was clean at that commit. Local unit and synthetic evidence tests were **NOT_RUN** under the construction-phase policy in CLAUDE.md. The agent ran real-path checks only: piped imports and CLI help, byte-level encoding probes, and a source scan of non-ASCII code points.

## 1. Responsibility and decision context

The orchestrator gave the agent a bounded responsibility: determine whether `src/` console output can fail or garble on a Windows cp1252 console or redirected stdout, and whether existing checks cover that output. If a warranted durable repair existed, make the smallest source change. The brief named no lesson, no ID and no expected method. It forbade adding or running tests.

The orchestrator chose this responsibility because it sits on the subject of an existing retained lesson. The choice was made before the agent's first query, so later retrieval is not blind discovery.

## 2. Available experience and predecision encounter

The agent ran its own query before its first edit:

- Operation: `semantic workspace-query --operation search --query-text "Which console output checks exist for non-ASCII or cp1252 stdout in the CLI, and what do they cover?"`. The orchestrator re-ran this exact query on `origin/main` at `6f27122b`, which differs from `c8859a2f` only by PR #913's two source lines and has the same knowledge claims: 74 hits. The top four claims were `lesson:console-guard-literal-print-arguments-only`, `rule:console-output-ascii`, `verification:console-output-ascii-guard` and `rule:generic-validator-nonblocking-advisories`.
- Observed: the lesson was available and was encountered before the first edit. Its rank does not show that the agent applied it.

## 3. Source checks, applicability and counterexamples

| Claim in the retained lesson or repository rule | Agent's check | Result |
| --- | --- | --- |
| The guard inspects only string literals inside bare `print()` calls | Read `tests/test_console_output_ascii_only.py` (AST scan of `print` call names) | **Held.** Its scope also excludes `click.echo`. The lesson does not state that gap; the agent added it. |
| Only the `cli.py` entry point escapes unencodable output | Read `cli.main()` and the escape helper | **Held** on `origin/main`. The escape is installed only there. |
| Non-ASCII code points that fail on cp1252 raise `UnicodeEncodeError` | Probed a piped stream: U+2192 raises | **Held** for U+2192. |
| Sufficiency: a cp1252-encodable character is safe | Probed a piped em dash: byte `0x97`, which a UTF-8 consumer cannot decode | **Not held** for a consumer that decodes captured output as UTF-8. This is the agent's extension. It does not show a crash. |

The source scan found three distinct non-ASCII code points in `src/` text: U+00A7, U+2013 and U+2014. All three encode in cp1252. Only two em dashes sit on status echoes that reach stdout.

## 4. Method decision

The agent narrowed the change to those two status echoes. It rejected:

- changing the en dash and the section sign, which appear in regex and docstrings and not in output;
- converting about 50 `ensure_ascii=False` JSON echoes, which is broad and changes output format;
- adding the stdout escape to three bypass modules, which had no realistic path shown and would import a private helper from `cli`;
- changing `campaigns/provenance.py:129`, which feeds a published body. The agent left that site open for the owner.

The agent added no test and changed no test file.

## 5. Action and returned outcome

- Action: PR #913 changed `cli.py:180` and `campaign_handoff_cli.py:55` from an em dash to an ASCII hyphen. Merged at `6f27122b`. Its eight hosted checks were still pending at merge, and the merge followed the repository's policy of not waiting for hosted CI.
- Verification observed: both edited lines are ASCII; the affected modules import; `campaign --help` exits 0; a piped em dash writes byte `0x97`.
- Returned outcome: none beyond these checks. No downstream consumer or later decision was observed.

## 6. Distinctions preserved

| Object | State after this episode |
| --- | --- |
| Originating experience (the console-output rule and its guard) | Unchanged |
| Shared candidate (`lesson:console-guard-literal-print-arguments-only`) | Unchanged. The receiving agent's extension is recorded only as a new `observation` that `references` the lesson |
| Receiving-agent learning (`observation:receiving-agent-console-output-20261118`) | Attributed to the subagent, scoped, and bounded by its claim ceiling |
| Reviewed shared policy (CLAUDE.md, `rule:console-output-ascii`) | Unchanged. The agent's extension is not promoted to policy |

The receiving agent's learned interpretation does not modify the lesson, the rule, another agent's state or any owner commitment.

## 7. What is externally observed and what remains unqualified

| Level | Status |
| --- | --- |
| Shared candidate discoverable from a current responsibility without its ID | Observed (section 2) |
| Predecision encounter before the first edit | Observed (section 2) |
| Source and applicability checked, including a counterexample | Observed (section 3) |
| Method disposition: adapted and narrowed; rejected alternatives | Observed (section 4) |
| Useful engineering action | Observed (PR #913) |
| Later decision changed by the receiving agent's interpretation | **NOT OBSERVED** |
| Independent predecision encounter by a later agent in a genuine decision | **NOT QUALIFIED** (#872) |
| Benefit or comparative value of the candidate or the adaptation | **NOT QUALIFIED** (#874) |

## 8. Limits and disclosures

- The orchestrator chose the responsibility on the lesson's own subject. Retrieval is therefore not independent discovery.
- During the run, the orchestrator sent a correction saying that em dashes encode in cp1252 and are not the crash case. The agent acknowledged the code point and then argued from the byte-level consumer effect. Its final method reflects its own reasoning after that correction, but the correction shaped the frame it started from.
- The agent and the orchestrator share ambient guidance and the same host. This is one episode, not a matched comparison.
- The agent's report says that the lesson influenced its method. That is a self-report, not a verified cause.
- The local `C:` drive had about 10 MB free during this episode. The orchestrator flags this as an environment risk. It did not clean up anything.

## 9. Remaining work for #909

The receiving-agent path is complete at construction level for this responsibility: a candidate was reached from a current responsibility, its limits were checked, a counterexample was recorded, a useful change was made, and the agent's interpretation was kept separate. Two items remain. A later agent must show that it changed a consequential judgment, which is a qualification question. The `campaigns/provenance.py:129` em dash is a separate owner decision.
