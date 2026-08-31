# 11 — RETROSPECTIVE CHALLENGES (DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0)

Frozen V0 (`ba8968c`, manifest `V0-FREEZE-MANIFEST.md`) is **not modified** for
any challenge. Seven historically consequential episodes where establishing the
boundary required real investigation at the time.

RESULT vocabulary: `DIRECTLY_VISIBLE` · `DERIVABLE_WITH_SMALL_REASONING` ·
`REQUIRES_RAW_REPOSITORY_INVESTIGATION` · `NOT_REPRESENTED` · `MISLEADING`.

Challenges were **not** chosen because V0 obviously contains their answer;
results below include one `NOT_REPRESENTED` and one partial `MISLEADING`.

---

## RC#1 — PR #243: `--probe-report` forwarded on file existence, not authority (MANDATED, authorization §17)

- **KNOWN_EVENTUAL_BOUNDARY:** The runtime guarded `--probe-report` forwarding
  to `validate-brief.py` with `os.path.exists(episode_probe_report)`. If
  `repo-sensemaker` failed to create the allocated same-episode report, the
  check silently dropped the flag, so `validate-brief.py` never learned an
  expected report was missing — defeating the PR's own `PROBE_REPORT_NOT_FOUND`
  fail-closed contract. Fix (`95809eb`): the runtime forwards the exact path
  whenever `self._episode_probe_report_path` is set; **`validate-brief.py` owns
  the existence check.** The boundary: *runtime owns the artifact identity; the
  validator owns enforcement of the artifact contract — the runtime must not
  absorb the validator's authority by pre-checking existence.*
- **ARCHITECTURE_QUERY:** "Who owns the probe-report artifact identity? Who owns
  enforcement that it exists / is cited correctly? Are those the same
  component?" → `05-AUTHORITY-MAP.md` row B (brief contract: DEFINES = 5
  sources; ENFORCES = `validate-artifact.py` + `validate-brief.py`;
  RUNTIME-OWNS = output **path**, session-scoped) + row C (runtime OWNS path
  resolution / identity; producers/consumers RECEIVE it) + `04` probe_report
  row (P = probe engine; C = repo-sensemaker + repair-verifier; V =
  `validate-probe-report.py`) + edge `doc.claude-md GOVERNS
  rel.validator-must-trace-to-consumer`.
- **RESULT:** `DERIVABLE_WITH_SMALL_REASONING`. V0 states, separately, that the
  runtime owns path/identity and that validators own contract enforcement, and
  row B explicitly separates RUNTIME-OWNS (path) from ENFORCES (validators).
  Composing those gives the general rule the fix restates: a runtime that
  gates a validator-bound forward on `os.path.exists` is crossing the
  DEFINES/ENFORCES vs RUNTIME-OWNS line. V0 makes the *family* visible.
- **REPRESENTATION_ELEMENTS_USED:** authority seam (RUNTIME-OWNS vs ENFORCES
  columns), artifact-flow P/C/V row, the "validator must trace to a real
  consumer" authority edge, "multiply-enforced facts" list.
- **WHAT_THE_ARCHITECTURE_SAVED:** Would have flagged, *before* reading any
  code, that "runtime pre-checks existence of a validator-owned artifact" sits
  on a represented authority boundary — turning an open-ended review into
  "check whether the runtime respects the ENFORCES column for probe_report."
- **WHAT_STILL_REQUIRED_RAW_EVIDENCE:** The specific symbol
  `self._episode_probe_report_path`, the `os.path.exists` guard, the
  `PROBE_REPORT_NOT_FOUND` / `HALLUCINATED_FILE` error taxonomy, and the fact
  that this degraded silently — none are in V0 (correctly; §13 forbids building
  a special field for it). Confirming the bug *occurred* needs the commit.

---

## RC#2 — ADR 0010: flat-path vs session-path executor mismatch

- **KNOWN_EVENTUAL_BOUNDARY:** A skill executor computed `artifacts/<id>.md`
  independently while the runtime used a session-scoped path; the executor
  reported success while the runtime saw `ARTIFACT_NOT_FOUND`. Resolution: one
  component (the runtime, `_resolve_artifact_path`) owns path resolution and
  passes `expected_output_path`; producers write exactly there (ADR 0010,
  `CLAUDE.md`).
- **ARCHITECTURE_QUERY:** "Who owns artifact path resolution? Does any producer
  recompute it?" → `05` row C (RUNTIME-OWNS = `_resolve_artifact_path`;
  ENFORCES = path-containment tests + PreToolUse gate) + `02`
  `runtime.skill-executor` `does_not_own`: "Recomputing artifacts/<id>.md
  independently (ADR 0010 — must use expected_output_path)".
- **RESULT:** `DIRECTLY_VISIBLE`. The `does_not_own` line and the authority row
  name the exact anti-pattern and its owner.
- **REPRESENTATION_ELEMENTS_USED:** component `does_not_own` (explicit
  non-ownership), authority seam with ENFORCES mechanism, ADR provenance.
- **WHAT_THE_ARCHITECTURE_SAVED:** The entire diagnosis — "executor success +
  runtime NOT_FOUND" maps straight to "executor violated its represented
  non-ownership of path resolution."
- **WHAT_STILL_REQUIRED_RAW_EVIDENCE:** Which executor, which run, and the
  historical PR — but the *boundary* needs no raw evidence.

---

## RC#3 — `Lx`-only evidence-line validator rule with no downstream consumer

- **KNOWN_EVENTUAL_BOUNDARY:** A validator enforced an `Lx`-prefixed
  evidence-line format that nothing downstream parsed; it repeatedly rejected
  valid bare-number citations until relaxed to accept both (`CLAUDE.md`
  verification discipline).
- **ARCHITECTURE_QUERY:** "Does every validator rule trace to a real consumer?
  Which rules don't?" → edge `doc.claude-md GOVERNS
  rel.validator-must-trace-to-consumer` + `06-VALIDATION-MAP.md` §5 note.
- **RESULT:** `DERIVABLE_WITH_SMALL_REASONING`, tending `NOT_REPRESENTED` for
  the specific rule. V0 represents the *principle* ("a validator rule must
  trace to a real consumer") and lists it as a governing authority edge, but
  V0 does **not** enumerate individual validator rules, so it cannot point at
  the `Lx` rule specifically. It tells you *to ask the question*, not the
  answer.
- **REPRESENTATION_ELEMENTS_USED:** one authority/governance edge.
- **WHAT_THE_ARCHITECTURE_SAVED:** Keeps the "trace to a consumer" test
  present as a first-class relation rather than tribal knowledge.
- **WHAT_STILL_REQUIRED_RAW_EVIDENCE:** Everything specific — which validator,
  which rule, which citations failed. V0 is a prompt here, not a source.

---

## RC#4 — `auto_invoke_next_workflow` treated as execution authority (Issue #230 / ADR 0026)

- **KNOWN_EVENTUAL_BOUNDARY:** A registry boolean plus a workflow id extracted
  from an artifact were effectively acting as execution authority for automatic
  workflow chaining. #230 triage confirmed no ratified material grants that
  authority; ADR 0026 ruled the field is compatibility metadata only, consumers
  fail closed.
- **ARCHITECTURE_QUERY:** "What authorizes one workflow to invoke the next? Is
  the registry flag an authority?" → `05` row F (DEFINES = ADR 0026;
  ENFORCES = fail-closed guard; RUNTIME-OWNS = 2 consumers, 2 registry
  mirrors; POLICY-vs-IMPL = now aligned, field still present) + `03` edge
  `E-ADR-0026 GOVERNS rel.auto-invoke-next-workflow` + `08` OW-1 + `07` RC-9
  context.
- **RESULT:** `DIRECTLY_VISIBLE`. Row F states the ruling, the enforcement
  shape, the residual (2 mirrors + 2 consumers), and the open tracker.
- **REPRESENTATION_ELEMENTS_USED:** authority seam (full row), lifecycle
  `DEPRECATES` edge, open-work item, registry-duplication note.
- **WHAT_THE_ARCHITECTURE_SAVED:** The #230 triage question ("does anything
  actually grant this authority?") is answered by row F's DEFINES/ENFORCES
  cells without re-reading five ADRs.
- **WHAT_STILL_REQUIRED_RAW_EVIDENCE:** The PR #235 merge SHA and the exact
  consumer call sites (V0 gives the ADR + the count, not the line numbers).

---

## RC#5 — ADR 0018 deterministic fog-type routing table: still-live-looking, actually superseded

- **KNOWN_EVENTUAL_BOUNDARY:** ADR 0018 proposed a deterministic
  fog-type→workflow routing table. It was **SUPERSEDED 2026-08-18, never
  Accepted**, yet `fast-path-workflow` / `full-fog-workflow` still carry
  `auto_invoke_next_workflow: true` and the runtime can execute the chain — so
  the routing capability *looks* live.
- **ARCHITECTURE_QUERY:** "Is automatic fog-type routing ratified? What is its
  status and where does the capability physically live?" → `05` row E
  (DEFINES = ADR 0018 SUPERSEDED, never Accepted; ENFORCES = none by design;
  RUNTIME-OWNS = runtime *can* execute the chain; WINS = ADR 0014 + 0026 +
  CONTEXT.md; POLICY-vs-IMPL = **impl ahead of policy, largest divergence**) +
  `03` lifecycle edge `E-ADR-0018 HISTORICAL_ONLY rel.deterministic-fog-routing-table`
  + `02` `cap.automatic-fog-routing` lifecycle note.
- **RESULT:** `DIRECTLY_VISIBLE`. The lifecycle grade + the POLICY-vs-IMPL
  column state exactly the trap: capability present, policy refuses it.
- **REPRESENTATION_ELEMENTS_USED:** lifecycle relation (`HISTORICAL_ONLY`),
  authority seam POLICY-vs-IMPL column, capability lifecycle field, the
  concentration ranking (#2).
- **WHAT_THE_ARCHITECTURE_SAVED:** Prevents the recurring mistake of "there's a
  working route, so routing must be intended" — the divergence is named and
  ranked, not rediscovered.
- **WHAT_STILL_REQUIRED_RAW_EVIDENCE:** None for the boundary. The full ADR 0018
  disposition text if one needs the reasoning.

---

## RC#6 — INFRA-004: PM/engineering contracts stranded in a deprecated file

- **KNOWN_EVENTUAL_BOUNDARY:** `required_sections` / `required_machine_fields`
  for `prd` / `issue_list` / `agent_brief` / `code_patch` live **only** in
  `workflow-orchestrator/references/artifact-contracts.yaml`, whose header says
  "No code should read this file" — while xfail-marked tests track the
  un-ported content. A contract that is simultaneously deprecated and canonical.
- **ARCHITECTURE_QUERY:** "Which file defines the `prd` contract? Is it
  enforced? Is that file deprecated?" → `06-VALIDATION-MAP.md` §2 row
  ("declared only in the DEPRECATED copy … xfail tests … header says delete
  once ported") + §4 registry-duplication table + `05` "Multiply-governed"
  list + `02` `registry.artifact-contracts` `duplicate_at` field + `08` OW-4.
- **RESULT:** `DIRECTLY_VISIBLE`. `06` §2 states the contradiction in one row
  with evidence id `E-CONTRACT-dupe-header`.
- **REPRESENTATION_ELEMENTS_USED:** validation-map "no/weak enforcement" row,
  registry-duplication table, authority "multiply-governed" list, open-work
  item, component `duplicate_at`.
- **WHAT_THE_ARCHITECTURE_SAVED:** This is the clearest case of V0 earning its
  keep: the contradiction spans two files 13 lines apart and only becomes
  visible when you ask "who enforces this contract?" — V0 pre-assembled that
  question and answer.
- **WHAT_STILL_REQUIRED_RAW_EVIDENCE:** The exact list of stranded fields per
  artifact, and whether they are still semantically needed (V0 says "4
  contracts", not their contents).

---

## RC#7 — Auteur handoff: "read the artifact, not the prose" (evidence 0020)

- **KNOWN_EVENTUAL_BOUNDARY:** A real Auteur handoff was audited and found to
  rely on remembered conversational context rather than durable artifacts; the
  lesson ("artifacts are the API"; a Skill must not work only because the agent
  remembers 30 messages ago) became the `artifact-reconciliation` workflow +
  `output-reconciler` / `repair-verifier` skills, and fed ADR 0013.
- **ARCHITECTURE_QUERY:** "Where does required information cross a skill
  boundary — as an artifact or as memory? What must fan in to
  `output-reconciler`?" → `04-ARTIFACT-FLOWS.md` reconciliation_report row
  ("Fan-in resolved: `output-reconciler <- work_claim (required) + brief
  (required) + prior_evidence (recommended)`") + `03` artifact edges (CONSUMES
  work_claim / brief, both required) + `07` RC-9 (second-model runner retired)
  + lifecycle edge `doc.agent-native-operating-workflow HISTORICAL_ONLY
  rel.auteur-handoff-episode`.
- **RESULT:** `DERIVABLE_WITH_SMALL_REASONING` with a **partial `MISLEADING`
  risk**. V0 shows the *resolved* state (mandatory typed fan-in) cleanly, and
  the lifecycle edge records that the Auteur episode motivated it. But V0
  represents the fix as a settled contract and does **not** convey that
  cross-run *prior-report identity* is still `CONVENTION` (the caller supplies
  which prior report) — a reader could over-read "fan-in resolved" as "all
  continuation state is durable." `04`'s session_summary row does note this, so
  the misleading risk is mitigated but depends on the reader reaching that row.
- **REPRESENTATION_ELEMENTS_USED:** artifact fan-in edges (required inputs),
  lifecycle `HISTORICAL_ONLY` motivation edge, research-claim supersession row.
- **WHAT_THE_ARCHITECTURE_SAVED:** The "what must fan in" question is answered
  structurally; the historical motivation is attached to the edge rather than
  buried in `AGW` section 0.
- **WHAT_STILL_REQUIRED_RAW_EVIDENCE:** The retirement-plan closure doc for the
  precise `CONTRACT_CLOSED` / `CONVENTION` / `CONVENTION_CLOSED` status of each
  continuation seam.

---

## Summary

| # | Episode | RESULT |
|---|---|---|
| RC#1 | PR #243 probe-report forward authority | DERIVABLE_WITH_SMALL_REASONING |
| RC#2 | ADR 0010 path-resolution mismatch | DIRECTLY_VISIBLE |
| RC#3 | `Lx` validator rule, no consumer | DERIVABLE (rule-specific: NOT_REPRESENTED) |
| RC#4 | `auto_invoke_next_workflow` authority | DIRECTLY_VISIBLE |
| RC#5 | ADR 0018 routing supersession trap | DIRECTLY_VISIBLE |
| RC#6 | INFRA-004 deprecated-file contract | DIRECTLY_VISIBLE |
| RC#7 | Auteur "read the artifact" handoff | DERIVABLE (partial MISLEADING risk) |

**Pattern:** V0 performs best on **authority / lifecycle / validation-ownership**
boundaries (RC#2, #4, #5, #6 directly visible) — exactly the families a plain
dependency graph handles worst. It performs worst on **rule-level / symbol-level**
questions (RC#3) where it deliberately does not enumerate, and carries a
**staleness/over-read risk** (RC#7) when it shows a resolved state without the
"still convention" caveat attached to the same edge. No challenge was
`REQUIRES_RAW_REPOSITORY_INVESTIGATION` with V0 giving zero help; none was
fully `MISLEADING`.

This is **retrospective reconstruction** — it does **not** establish a causal
productivity improvement. It establishes that the represented relationship
families line up with where these boundaries actually were.
