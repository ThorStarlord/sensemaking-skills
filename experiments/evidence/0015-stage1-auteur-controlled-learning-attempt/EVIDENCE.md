# Evidence 0015: Stage 1 Auteur Controlled Learning Attempt

This directory records exactly one authorized, controlled Stage 1 model/workflow
invocation, executed under the owner authorization message accompanying this
attempt and governed by
`docs/experiments/STAGE-1-AUTEUR-EXECUTION-PACKAGE.md` (merged at
`3c7215e5a12dfcbded570b7b369b1f54a69a10f6`, PR #103).

## Configuration

- Package revision: `3c7215e5a12dfcbded570b7b369b1f54a69a10f6`
- Framework execution pin: `bfe84571d782cd4cf4308536fba8213e8d85149c`
- Target pin: `b40db654e0df9e90074f7ad85b40d7362378e07d`
- Requested model: `claude-sonnet-5`
- Canonical target source: `https://github.com/ThorStarlord/auteur.git`
- Framework clone: `C:\scratch\stage1-auteur-attempt-20260727-164125\framework`
- Target execution clone: `C:\scratch\stage1-auteur-attempt-20260727-164125\target-auteur`
- Both clones fresh, outside `.claude/worktrees/`, distinct repositories (verified).

## Evidence-preservation incident (disclosed, corrected before merge)

**What happened:** this repository has `core.autocrlf=true`. The generated
brief (`raw/repository_sensemaking_brief.md`) was produced by the run with
CRLF line endings. When the evidence branch was first staged and committed
(`git add`), Git silently normalized the brief's line endings from CRLF to
LF before storing the blob. The hash recorded in the first version of
`file-hashes-sha256.txt` (`b8f28ba75e32fc53732348b54cf1af73f5963aae86ffef4cd35083d6ebb7dbad`)
was computed *before* that staging step, from the file on disk in the
still-untouched framework clone — so the first committed PR revision
actually contained a normalized copy whose real blob hash was
`cf9b2ec354dbdac59de9a69adefe107efe03179089d03d9e07005fc0ea0a2589`, silently
different from what was recorded and reported. This was **detected before
merge**, during an explicit pre-merge verification pass that compared the
committed blob's hash (via `git cat-file`) against the recorded hash rather
than trusting the recorded hash alone.

**Correction applied:**
- The original CRLF byte sequence was recovered from the still-untouched,
  isolated framework clone
  (`C:\scratch\stage1-auteur-attempt-20260727-164125\framework\artifacts\05-orchestration-run\repository_sensemaking_brief.md`),
  independently re-hashed from disk, and confirmed to equal
  `b8f28ba75e32fc53732348b54cf1af73f5963aae86ffef4cd35083d6ebb7dbad` (21922
  bytes, CRLF) before being used.
- Those exact bytes were copied over the normalized copy in this evidence
  directory and re-staged. The re-staged, committed blob was independently
  re-verified via `git cat-file -p :<path> | sha256sum` and confirmed to
  equal `b8f28ba75e32fc53732348b54cf1af73f5963aae86ffef4cd35083d6ebb7dbad`
  again — i.e. the committed blob, not just the working-tree file, now
  matches the original.
- A scoped `.gitattributes` file was added at
  `experiments/evidence/0015-stage1-auteur-controlled-learning-attempt/.gitattributes`
  containing `raw/repository_sensemaking_brief.md -text`, confined to this
  evidence directory only, to prevent Git from normalizing this specific
  raw artifact again. Repository-wide line-ending policy is unchanged.
- The transient, incorrect hash `cf9b2ec354dbdac59de9a69adefe107efe03179089d03d9e07005fc0ea0a2589`
  is preserved here, in this incident record, for auditability — it is not
  erased from history.

**Secondary finding, same class, lower stakes:** the same pre-staging/
post-commit hash mismatch was also present for `raw/tool-call-trace.jsonl`
(pre-staging: `e097b5c6943045e14c066ad23b2dd65f3e2a72258f19f85e5a6b93f5cb6d2d3e`;
actual committed: `e65bbcf9e93229aaa197b6bb1a2d965613cb1abc244cf6b4bf4b6e0c6ecb559e`)
and `raw/workflow_summary.json` (pre-staging:
`f93ebc0104b55aa535ea9f5fb58570c5aa1a53d357b0ec7e90bf7bc9add7aa3d`; actual
committed: `4c77df8d2153e2bc42081d77c562766f2c16e53b8d5726ab76f0de321b20c6b7`).
Unlike the brief, these files' **content was not restored to their original
bytes** — line-ending normalization does not change the parsed meaning of
JSON/JSONL, and they were not singled out as artifacts requiring
byte-for-byte historical fidelity the way the generated brief is (package
§8: "preserve byte-level hashes where practical," and specifically "the
first generated artifact is historical evidence... preserve byte-level
hashes where practical" refers to the brief). `file-hashes-sha256.txt` has
been corrected to describe the hashes of what is actually committed for
these two files, rather than left pointing at pre-staging hashes that no
longer describe any file in the repository.

**Not affected:** `raw/invocation-ledger.txt` was LF in its original,
pre-staging form (it was authored directly as LF text), so its committed
blob hash (`b80f9ee6ee5995bbabfc076c0ee07a8c452fc6a61f40f4615af8103baa432bd0`)
was correct from the first commit and required no correction. (A working-tree
read of this file after checkout can show a different, CRLF-converted hash
due to the same `core.autocrlf` behavior acting on checkout rather than on
commit — that is a working-tree artifact, not a change to the committed
blob, and does not affect the recorded hash.)

**What this incident is, and is not:** this is an evidence-preservation
process defect in how this evidence record was assembled, caught and fixed
before merge. It is not a change to the Stage 1 result, the brief's content,
the invocation count, the validator outcome, or any conclusion in this
document. Stage 1 result remains FAIL; invocation count remains 1; retry
and fallback counts remain 0; target writes remain 0; the CRLF
quote-grounding hypothesis discussed below remains unconfirmed.

## Raw immutable evidence (unmodified, as produced by the run)

- `raw/repository_sensemaking_brief.md` — the generated artifact. **Not edited,
  normalized, or repaired.**
- `raw/tool-call-trace.jsonl` — 254 lines; 114 `AssistantMessage` events, all
  `reported_model: claude-sonnet-5`.
- `raw/run-ledger.jsonl`
- `raw/00-user-intent.md`, `raw/plan.md`
- `raw/workflow_summary.json`
- `raw/workflow-stdout.txt`, `raw/workflow-stderr.txt` (stderr is empty — 0 bytes,
  preserved as-is, not omitted)
- `raw/invocation-ledger.txt` — append-only ledger; both the pre-invocation and
  post-invocation entries are preserved in one file, in the order written.
- `raw/target-manifest-pre.txt`, `raw/target-manifest-post.txt`
- `raw/file-hashes-sha256.txt` — sha256 of the brief, trace, ledger, and summary

## Derived / diagnostic evidence (produced by validators, not by the model)

- `raw/run_log.md`, `raw/implementation_report.md`, `raw/diagnostic_report.md` —
  runtime-generated logs from the run itself (not hand-written).
- `raw/validation_run_log.md` — the runtime's own validation log entry.
- `raw/validator-output-authoritative.txt` — output of the **corrected**,
  authoritative validator invocation, run explicitly with both
  `--repo-root <framework clone>` and `--target-repo <target clone>` per
  package §9. This is a validator-only, read-only command; it does not
  regenerate or repair the artifact.
- `raw/preflight-test-output.txt` — the six package-named focused tests, run
  inside the isolated framework clone (all passed).

## Human review (this section only — not raw evidence)

Everything below this line is post-hoc human/derived summary, not raw output.

## Invocation integrity (Gate A)

- Invocation count: **1**. No retry, no fallback, no second invocation.
- `authorization consumed: yes` was appended to the ledger immediately before
  the SDK/model call began; `invocations completed: 1` was appended after the
  process exited (exit code 2 — a workflow-level failure exit, not a crash;
  see Structural validation below).
- Requested model `claude-sonnet-5` vs. reported models: uniform
  `claude-sonnet-5` across all 114 `AssistantMessage` events. No mismatch, no
  fallback.
- Target execution clone: HEAD, tree hash (`1ffa0ac4397f193758a4525a362c83a915753145`),
  and file count (1044) are **identical** pre- and post-run.
  `git status --porcelain` and `git diff --stat` are empty in both snapshots.
  **Zero attempted or completed writes to the target clone.**
- Framework clone (not the target) received the expected artifact writes:
  `artifacts/05-orchestration-run/*` (new) and `docs/mode-coverage.yaml`
  (modified, per the runtime's own bookkeeping). This is normal, documented
  runtime behavior — artifacts are written to the framework/session root, not
  the target repo — and is not a target-safety violation.
- No stash was applied, popped, dropped, or modified. The pre-existing
  `sensemaking-skills` working tree and stash list are unchanged from before
  this attempt.

## Structural validation (Gate B)

**FAILED.** Authoritative validator (`validate-brief.py`, both roots
specified) reports 1 WARNING + 4 ERRORS, exit code 1:

- `HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT` (WARNING, non-blocking on its own):
  `weakness_type: Ghost Features` is a D5 high-risk category requiring
  substantive human audit.
- `EVIDENCE_QUOTE_NOT_FOUND` (ERROR) x4: excerpts 0, 1, 2, 4 in the brief's
  Section 8 evidence-excerpts block were not matched verbatim against the
  cited line ranges in the target repository.

Handoff YAML round-trip and generic `artifact_id` routing were not separately
blocking; the unified validator selected `validate-brief.py` correctly and
routing itself succeeded. The failure is specifically in evidence-quote
grounding.

### Substantive spot-check of the quote-mismatch (diagnostic, not part of the
### validator's own output)

Manually inspecting one flagged excerpt (`src/auteur/universe/models.py`
lines 65-67) shows the cited line range and quoted text are byte-identical in
content to the actual file **except that the target repository's source
files use CRLF line endings** (confirmed via `file` and a raw byte read: each
line ends `\r\n`). The validator's own error message states it performs
"line-ending normalization," but on this run the CRLF-checked-out target
still produced `EVIDENCE_QUOTE_NOT_FOUND` for that excerpt. This is a
plausible, not confirmed, root cause — no fix was attempted or should be
inferred as verified from this observation alone; it is recorded as a
diagnostic lead for whoever reviews this evidence, not as an adjudicated
root cause.

Per Gate B failure, no substantive audit (Gate C) or usefulness review
(Gate D) was performed, per package §10. The quality of the brief's actual
content (which appears, on a plain read, to be a well-evidenced "ghost
feature" claim about Universe-to-Series constraint propagation in the
`auteur` target repo) is **not adjudicated** by this evidence record.

## Result classification

**STAGE 1 FAIL** (structural validation failure — Gate B).

This is not a model-enforcement failure, not a safety failure, and not a
preflight stop; execution integrity (Gate A) passed.

## Learning classification

- Primary category: **INFRASTRUCTURE**
- Novelty: Moderate. Evidence 0013 also failed structural validation with
  quote-grounding errors (three `EVIDENCE_QUOTE_NOT_FOUND`, per
  `experiments/evidence/0013-stage1-auteur-run-model-enforcement/EVIDENCE.md`
  line 59) — this run does **not** introduce an entirely new failure
  category. The weakness-type safeguard passed cleanly in this run (it
  correctly flagged, not blocked, the high-risk claim); in 0013,
  weakness-type-adjacent ambiguity was a secondary, script-limitation note
  (a malformed nested fence defeating a duplicate-key checker), not that
  run's primary recorded failure, so it should not be used to distinguish
  0013 from 0015. What may distinguish this run is the *mechanism*: 0013's
  quote mismatches have not been independently re-examined for a CRLF
  cause, while this run's flagged excerpts appear content-identical to
  their cited source ranges except for CRLF line endings. Whether 0013 and
  0015 share the same underlying mechanism, or represent two distinct
  causes within the same quote-grounding boundary, is **not yet
  adjudicated**.
- Materiality: Moderate-to-high if the CRLF hypothesis is confirmed — quote
  grounding is a core structural gate (per this repo's own verification-
  discipline rule: "a validator rule must trace to a real consumer"), and a
  systematic CRLF blind spot would affect any Windows-checked-out target,
  not just `auteur`.
- Transferability: Potentially high if confirmed — not simply "high." Before
  that claim is warranted, a read-only investigation should establish: (1)
  what exact normalization the validator performs; (2) whether it
  normalizes both the source text and the supplied quote; (3) whether line
  slicing happens before or after normalization; (4) whether indentation,
  Markdown escaping, Unicode punctuation, or whitespace differs between the
  quote and source; (5) whether all four of this run's failures share the
  same mechanism; (6) whether a minimal CRLF/LF fixture reproduces the
  failure without a model run. None of this has been done. This
  investigation is a candidate next step, not authorized or performed by
  this evidence record.
- Cost: One controlled invocation (~10 minutes wall-clock), no target
  mutation, no repeat runs.
- Product proximity: Low-to-moderate for this specific run — Gate C/D
  (substantive/usefulness review of the brief's actual claims) was never
  reached, so this run does not by itself answer whether the *product*
  (the brief) is useful; it answers a capability/infrastructure question
  about the validator pipeline.

## Recommendation

**PAUSE.** The CRLF-grounding hypothesis above is plausible but unconfirmed
and is exactly the kind of finding this package's own governance requires
routing back through the owner rather than acting on autonomously (see
package §17, "No remediation in this task"). This run establishes that
routing, YAML handoff, and artifact-id dispatch — the mechanisms Evidence
0014 could not reliably reach — now work; the live boundary has moved back
to evidence-quote grounding, consistent with (not distinct from) Evidence
0013's failure mode, though the underlying cause may differ. A read-only
investigation (see the six open questions under Transferability above) into
whether `validate-brief.py`'s quote-normalization handles CRLF-terminated
source files, and whether it explains 0013 as well as 0015, is a reasonable
next step, but is explicitly **not authorized by this run** and is not
implemented here.

## No further run authorized

This evidence record does not authorize, and should not be read as
authorizing, any further Stage 1 invocation, repair, retry, or Stage 2/3
work. Authorization was consumed exactly once, for exactly this attempt.
