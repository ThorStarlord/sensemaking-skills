# Gate D — Stale-Diagnosis Checklist (Evidence 0016 preparation)

```text
PREPARED_NOT_RUN
```

**Read this document before reading the generated brief.** Reading it
afterwards defeats its purpose: the point is to arm the reviewer with the
specific obsolete claims that the *previous* attempt made, so that a
plausible-sounding repetition of them is recognized as stale rather than
accepted as a finding.

This checklist governs the Gate D substantive audit of the proposed Evidence
0016 attempt described in
`docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md`.

Target pinned for that attempt:

```text
ThorStarlord/auteur @ 0653defb05625f2fcde0ac32eac6e59ccf7eeb90
```

Auteur main has moved beyond the selected target pin (main now resolves to
`d3d12b8dfb501a5e553c3b366df2f349d4438e59`). The intervening change was
inspected and is documentation-only; it does not modify the pinned advisory
implementation or test surface. Evidence 0016 deliberately remains pinned to
`0653def...` for comparability with the completed #38 audit.

**Provenance of this checklist.** This file must be read from `framework_root`
at the finalized `execution_framework_sha`, not from an external or
undocumented copy. It does not exist at `runtime_baseline_sha`
(`1761e42f6786af422e05e128bb6608d33854f1f3`), which is historical preparation
evidence only and must never be used as the execution pin. While
`execution_framework_sha` is `PENDING_POST_MERGE_PIN_FINALIZATION`, the run is
blocked and this checklist governs nothing live.

**Digest provenance.** This checklist's SHA-256 digest, computed over its exact
bytes as read from `framework_root` at the authorized execution SHA, must match
`gate_d_checklist_sha256` in the future authorization record. That
authorization record's own SHA-256 must in turn match the digest approved by
the repository owner in the distinct owner-approval artifact. Both comparisons
happen in **Gate A, before any model invocation**. If either fails — checklist
digest mismatch, authorization-record digest mismatch, missing record, or
missing owner approval — **Gate A fails before Gate D begins**, and no
substantive review takes place. Gate D never runs on an unauthenticated
checklist.

---

## 1. Why this checklist exists

Historical Evidence 0015 diagnosed a "ghost feature" in auteur's
Universe-to-Series advisory path. That diagnosis has since been overtaken by
merged implementation work: PR #40 (Phase 1 characterization), PR #44
(`forbidden_elements` enforcement), PR #46 (`required_elements` enforcement),
PR #48 (`cross_story_constraints` human-review notices), with parent contract
issue #38 closed after an independent completion audit.

A brief that reproduces the Evidence 0015 diagnosis against the pinned
current target is therefore describing code that no longer exists in that
form. The risk is not that the model lies; it is that a stale conclusion is
*fluent*, internally consistent, and superficially well-cited.

Evidence 0015 itself remains an immutable historical Stage 1 FAIL. Nothing in
this checklist reclassifies it.

---

## 2. The eight tripwires

The brief must be **escalated or fail substantive review** if it claims,
without current evidence grounded in the pinned target revision, that:

| # | Stale claim | Reviewer action |
|---|---|---|
| T1 | `forbidden_elements` are not enforced | Escalate / fail unless proven against the pin |
| T2 | `required_elements` are not enforced | Escalate / fail unless proven against the pin |
| T3 | `cross_story_constraints` are silently ignored | Escalate / fail unless proven against the pin |
| T4 | `auteur series diagnose` forwards only structured constraints | Escalate / fail unless proven against the pin |
| T5 | the advisory compiler is the only path capable of representing advisory Universe fields | Escalate / fail unless proven against the pin |
| T6 | cross-story constraints are passed directly into `UniverseToSeriesValidator` | Escalate / fail unless proven against the pin |
| T7 | the Evidence 0015 ghost-feature diagnosis remains unchanged | Escalate / fail unless proven against the pin |
| T8 | the merged Phase 2–4 advisory paths do not exist | Escalate / fail unless proven against the pin |

"Escalate or fail" means: the reviewer stops, records the tripwire number,
performs the contradiction search in §3 against the pinned revision, and
records the outcome. A tripwire hit that the contradiction search confirms
(i.e. the claim really does hold at the pin, with current citations) is a
legitimate finding, not a failure. A tripwire hit that the contradiction
search refutes is a **substantive failure** under Gate D, regardless of how
clean structural validation was.

---

## 3. Mandatory contradiction search

For every tripwire hit, and for every absence / unreachability / dead-code /
ghost-feature / safety claim in the brief, the reviewer must actively search
for contradicting evidence in the pinned target at
`0653defb05625f2fcde0ac32eac6e59ccf7eeb90`:

```text
src/auteur/series/universe_advisory.py
src/auteur/series/handlers.py
src/auteur/universe/models.py
tests/test_forbidden_elements_matching.py
tests/test_required_elements_matching.py
tests/test_cross_story_constraint_notices.py
tests/test_series_universe_integration.py
issue #38 completion audit (ThorStarlord/auteur)
```

All eight sources above were confirmed present at the pinned revision during
preparation. If any is absent at execution time, the pin is wrong — stop and
re-verify the target SHA before auditing anything.

Record, per claim:

```text
Claim: ______________________________________________
Tripwire matched (T1-T8, or none): __________________
Sources searched for contradiction: _________________
Contradicting evidence found: yes / no
Audit result: Confirmed / Rejected / Inconclusive
Reviewer rationale: _________________________________
```

A `Rejected` or `Inconclusive` result on any high-risk claim means Gate D
does not pass.

---

## 4. What the brief is still allowed to say

The future brief **may** identify real limitations in the current
implementation — incomplete enforcement, weak error surfaces, missing
coverage, unclear contracts, advisory semantics that do not match user
expectations. Finding fault with merged code is not a tripwire.

What it must not do is describe the implementation as *absent* when it
exists. The distinction the reviewer is enforcing is:

```text
allowed:    "the advisory path exists but does X poorly / partially / opaquely"
tripwire:   "the advisory path does not exist / is never invoked / is ignored"
```

The brief must acknowledge the implementation that actually exists at the
pinned revision before critiquing it.

---

## 5. Gate D verdict (blank — to be filled only after an authorized run)

```text
Gate D result: ______________________________________
Tripwires triggered: ________________________________
High-risk claims audited: ___________________________
Claims rejected: ____________________________________
Reviewer: ___________________________________________
Date: _______________________________________________
```

This block is intentionally blank. No run has occurred.
