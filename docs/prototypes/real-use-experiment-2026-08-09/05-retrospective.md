# Real-use experiment retrospective — 2026-08-09

Full experiment record: `00-pre-registration.md` (exact question, pins,
pre-investigation known intent) → `01-repository-diagnostician-output.md`
(real brief, corrected) → `02-clarification-and-synthesis.md` (real
clarifying question + real owner answer) →
`03-downstream-consumer-attempt-1-FAILED.md` (a real authoring error and
what it revealed) → `04-downstream-consumer-output.md` (corrected,
clean downstream run) → `06-interaction-layer-attempt-1-CONTAMINATED.md`
(a repeat of the same authoring error, preserved, not counted as clean
evidence) → `07-interaction-layer-output.md` (corrected, clean,
independently-isolated interaction-layer run — see addendum below).

**Addendum (post-original-writing)**: section 7 and the REVISE/UNKNOWN/
NEXT EVIDENCE judgments below were written before `07` existed, when the
interaction-layer/diagnostic-core boundary had only been exercised inside
this same conversation. `07` closed that gap with a genuinely separate
subagent invocation. Rather than rewrite the original findings to look
as if they already knew the answer, the relevant sections are appended
with what changed, in place, so the original reasoning stays legible.

## Verification

`scripts/validate-repo.py`: pass. `test_prototype_*` suites: 20/20 pass.
`test_path_drift.py`: same 4 pre-existing, unrelated failures as every
prior check this branch — unchanged. `git status`: only the new
experiment-record directory added; no skill, script, or template file was
touched during this validation run.

---

## 1. Did investigate-first behavior reduce owner burden?

Yes, measurably. The owner's total direct involvement was one multiple-
choice answer, after a 708-second, 57-tool-call autonomous investigation
had already: read 15+ files, checked live GitHub Actions run history,
read a closed GitHub issue's comments, run this branch's own version-drift
tool, and computed real LOC/file counts. The owner did not have to specify
what to look at, prepare a briefing document, or answer any question until
after autonomous investigation had already narrowed the space to one real,
irreducible strategic choice.

## 2. Did the system preserve owner intent without inventing preferences?

Mostly yes, with one real, owner-caught exception. The diagnostician
correctly classified the three-way track-priority question as
`owner_intent`/`thin` rather than guessing an answer, and correctly
distinguished it from the CI-fix (classified `repository_evidence`-
resolved). But the interaction-layer synthesis (this conversation, before
asking) bundled the CI-fix together with a **moratorium recommendation**
as both "ready regardless of the owner's answer" — the owner caught this
live: the moratorium is a policy recommendation the brief supports but
cannot itself authorize, and treating it as already-decided would have
been exactly the "recommendation quietly becomes decision" failure this
project's evidence discipline exists to prevent. **This was not caught by
the prototype's own design — it was caught by the owner, in the
interaction, because a real owner was present to catch it.** That is
itself a finding: the current interaction-layer synthesis step doesn't yet
reliably keep this distinction, and a real human being in the loop is
currently what closes that gap, not the schema.

## 3. Was any clarification genuinely necessary and neutral?

Necessary: yes — repository evidence explicitly could not resolve the
three-way prioritization (checked and ruled out ADR ratification, EXP-0001
executability, and pre-existing green-lights as resolvers, per the brief's
own uncertainty.question text). Neutral: the three options were presented
without labeling any as evidence-preferred, directly applying S1's own
lesson. The owner's answer did not comment on the phrasing as leading,
unlike S1's own recorded defect — a small positive data point, though a
single instance, on the same class of failure S1 flagged.

## 4. Did the Repository Sensemaking Brief sharpen the real decision?

Yes, substantially — and in a way neither party anticipated going in. The
owner's original question ("what should I focus on next") got an answer
the pre-registration's "known owner intent" section had no way to predict:
a specific, currently-live CI failure, traced to a specific line range,
inside a specific subsystem whose total footprint (~40% of tracked source)
had never been measured before this investigation. This is real, new
information that changed the shape of the decision, not a restatement of
what was already believed.

## 5. Could the downstream consumer operate from the brief without reconstructing repository investigation?

Yes, on the corrected run — cleanly. Zero repository files or commands
opened beyond the consumer's own SKILL.md; every fact load-bearing for its
verdict came from the brief text. This is the first methodologically clean
answer to this question this whole line of work has produced — the
earlier self-administered composition test (two turns before this one)
could not distinguish "brief sufficient" from "same agent already knew
everything"; this run used a genuinely separate subagent invocation via
the Agent tool, which removes that confound. **This is real, if
single-instance, evidence for the brief-as-boundary hypothesis specifically
— not yet for the Option A packaging question (see #7).**

## 6. If it needed more information, was that a brief-contract deficiency or an inherently consumer-specific need?

It didn't need more repository information. It DID surface one process gap
in the *consumer skill's own decision procedure* (not the brief's
contract): whether "unresolved uncertainty elsewhere in the brief" should
gate a proposal that doesn't touch that uncertainty's actual question is
not disambiguated by `vnext-review-consumer`'s own documented checks #2/#3.
The subagent resolved it correctly this time by reading the brief's own
prose carefully — but that it had to do so by inference, rather than by a
rule the skill already stated, is a real, named gap in the *consumer's*
design, distinct from anything about the brief.

**Separately, and more importantly**: the first (failed) attempt at this
step surfaced a real gap that has nothing to do with either skill's field
design — the orchestrating layer (this conversation) had no durable,
retrievable artifact path for the brief; the only copy existed in
ephemeral tool-result memory. That's an artifact-persistence gap in how
*this experiment* was run, not in what the brief or the consumer contain.

## 7. Did the two-Skill Option A packaging provide value beyond internal responsibility separation?

**Still not established either way, and this run is honest about why.**
The `repository-diagnostician` step ran as a genuinely separate subagent
invocation (real context isolation, confirmed) and produced a large,
substantive, independently-sourced brief. The `vnext-review-consumer` step
also ran as a genuinely separate subagent and worked from the brief alone.
So this run *did* exercise real invocation-level separation for the first
time in this prototype's history — a step forward from the earlier
composition test. But the *interaction layer* (repo-sensemaker's role —
recovering intent, deciding whether to ask, synthesizing) was performed by
this conversation directly, not as a separate invocation, so the
diagnostic-core/interaction-layer boundary specifically (as opposed to the
diagnostic-core/downstream-consumer boundary) still wasn't tested with real
separation this round. What WAS newly observed: the interaction layer,
running with full context, still made a real synthesis error (bundling the
fix and the moratorium) that a downstream consumer working from the brief
alone did NOT make (it correctly scoped its verdict to only what the
proposal covered). That's a small, real, single-instance signal that the
brief's discipline may be doing useful work independent of who's reading
it — but it's not proof, and it's not about Option A's packaging question.

**Addendum**: `07-interaction-layer-output.md` closed the specific gap
named above — the interaction layer ran as a genuinely separate subagent
invocation, given only its SKILL.md, the owner's question, `known_intent`,
and the brief text, explicitly barred from repository search. It reached
the same split (CI fix = act now; moratorium = recommend, not decide) and
asked the same three-way clarifying question, independently. This is
still not evidence about Option A's packaging question (two Skills vs.
one) — it's evidence about whether the *bundling-avoidance reasoning*
survives real context isolation, which it did, once.

## 8. Which prototype fields actually changed behavior?

- **`uncertainty.source`**: yes, materially. It's the field that let the
  interaction layer distinguish "act now, no owner call needed" (the CI
  fix) from "must ask" (the track-priority question) — the single most
  load-bearing field in this run.
- **`is_demonstrated_weakness`**: yes. It's what let the downstream
  consumer correctly reason that the CI fix alone doesn't close out the
  full identified weakness, producing `pursue_narrowed` instead of
  `pursue` — a real, substantive verdict difference, not decoration.
- **`owner_intent_state.status`**: partially. `thin` (not `sufficient`,
  not `blocking_unknown`) correctly did NOT trigger a hard stop in the
  downstream consumer, and correctly signaled the interaction layer that
  *something* real was unresolved. But it did not, by itself, prevent the
  interaction layer's bundling error — the status field flagged that
  something was open, not precisely what.
- **`domain`**: used, produced one real disclosure (the consumer explicitly
  named product-prioritization as out-of-lens) — genuine behavioral effect,
  though a modest one; it didn't change the verdict, only what the verdict
  disclaimed.
- **`discovery_confidence`**: used but did not change anything — `high`
  triggered no caveat, which is the field working as designed (it's only
  supposed to add a caveat when *low*), but this run supplies no evidence
  about what happens when it's actually low.

## 9. Which fields appeared redundant or decorative?

None were unused this run — every field in `analysis_vnext` was read and
referenced by at least one downstream step. `discovery_confidence` came
closest to decorative in this specific instance (no caveat fired), but
that's because the case happened to be high-confidence, not because the
field has no behavioral path — see `NEXT EVIDENCE` below.

## 10. Which evidence tools materially helped?

`scripts/prototype_version_drift_scan.py` was actually run by the
diagnostician subagent and its output (`README.md:77: 0.2.1 <-- DRIFT`)
is cited directly in the brief — genuine, material use, not incidental.
`prototype_duplicate_authority_scan.py` and
`prototype_tracked_vs_workspace_scan.py` were not run this time — the
investigation's actual findings (CI logs, git history, LOC counts) didn't
call for what they check. This matches the intended pattern exactly:
"real investigative question → mechanically decidable evidence need →
deterministic tool," not "run everything because it exists." No new
evidence tool was built during this run — the investigation never hit a
mechanically-decidable fact it couldn't already obtain.

## Did the resulting recommendation change the owner's likely decision, increase confidence, expose a missing decision, or show a decision should be deferred?

**Exposed a missing decision the owner didn't know existed going in** (the
CI-red state and the execution-governance overinvestment finding), **and**
**resolved a different, pre-existing decision with increased confidence**
(which track is primary — S3 vs. EXP-0001 vs. vNext — now answered:
vNext, with reasoning on record). Not merely confirmatory: the pre-
registration's own "known owner intent" section, written before
investigation, did not anticipate the CI-governance finding at all.

---

## KEEP

- **`uncertainty.source`** — repeatedly, concretely load-bearing across
  both S1 (prior evidence) and this run.
- **`is_demonstrated_weakness`** (paired with `consequential_boundary`) —
  produced a real, correct verdict difference (`pursue_narrowed` vs.
  `pursue`) this run, on top of P4's prior evidence.
- **The brief-as-artifact-boundary design** — cleanly held under a
  genuinely separated invocation for the first time this prototype has
  been tested that way.
- **The neutral-clarification discipline** (S1's rule) — held again, no
  leading-phrasing complaint this time either.

## REVISE

- **The interaction layer's synthesis step** — demonstrated a real
  tendency to bundle an evidence-resolved finding with an evidence-
  *supported-but-unauthorized* recommendation as if both were equally
  ready to act on, in the first (in-conversation) run. **Addendum**: a
  second, cleanly-isolated run (`07-interaction-layer-output.md`)
  independently avoided the bundling error without having seen this
  finding — i.e. SKILL.md's existing flowchart plus the brief's
  `uncertainty.source`/`is_demonstrated_weakness` fields were sufficient
  for a fresh instance to draw the same distinction on its own. This
  downgrades "needs an explicit new rule added" to "the existing design
  handled it correctly under isolation, once — worth one more
  replication under a differently-shaped question before calling this
  KEEP rather than REVISE." Not yet moved to KEEP outright: n=1 clean is
  suggestive, not conclusive, and the first in-conversation run still
  shows the failure mode is reachable under some conditions (e.g. full
  prior context, or reasoning under less structured prompting).
- **`vnext-review-consumer`'s check #2/#3 text** — ambiguous about whether
  "unresolved uncertainty" scopes to the whole brief or the specific
  proposal under review; the subagent had to resolve this by inference
  rather than by a documented rule.
- **`owner_intent_state.status`** — real but partial value; flags that
  something is unresolved without precisely bounding what. Consider
  whether it should reference *which* field(s) the "unresolved" note
  applies to, rather than being a single freestanding note.

## DROP / COLLAPSE

- **Nothing new this run.** No field or mechanism showed complexity that
  wasn't justified by this run's evidence — a genuinely different result
  than a shallower test might have produced, and worth stating plainly
  rather than manufacturing a drop candidate for symmetry.

## UNKNOWN

- **Option A vs. C (packaging)**: still unresolved. `07` exercised the
  interaction-layer/diagnostic-core boundary with real separation for the
  first time (closing the specific gap this section originally named),
  but that tests whether the *behavioral rule* survives isolation, not
  whether two Skills is the right *packaging* for it — per
  [[vnext-three-lane-promotion-strategy]], those are separable claims.
  Packaging remains untested.
- **What happens when `discovery_confidence` is actually low**: no case
  this run.
- **Whether the interaction-layer bundling error is systematic or a
  one-off**: originally n=1, caught by a human. **Addendum**: now n=2
  directionally (contaminated run + clean run, both avoided the error),
  n=1 clean. Moved from "unknown" toward "one clean data point says
  avoided," but a single clean replication on one question shape is not
  enough to call this closed — still listed here rather than promoted to
  KEEP.
- **Whether a real owner (as opposed to this conversation's owner, who is
  also this repository's primary author/reviewer) would experience the
  same low burden** — the familiarity caveat P4 already named applies here
  too.

## NEXT EVIDENCE

**Completed**: the interaction layer was run as a separate subagent
invocation (`07-interaction-layer-output.md`), given only the owner's
question, a recovered known-intent summary, the brief, and an explicit
bar on repository search. It independently avoided the same bundling
error and asked the same neutral clarifying question — see the addendum
in section 7 and the updated REVISE/UNKNOWN entries above. First attempt
at this (`06`) was contaminated by an authoring error (an unfilled
placeholder in the prompt caused the subagent to search for its missing
input and incidentally find the whole prior experiment record); preserved
as-is rather than discarded, since the contamination itself and the
subagent's unprompted self-report of it are real data points.

**New cheapest next observation**: replicate `07` once more against a
*differently-shaped* owner question (not "what's next," e.g. a brief
whose weakest boundary is a straightforward technical defect with no
policy-adjacent companion recommendation at all) to see whether the
bundling-avoidance behavior generalizes or was specific to this brief's
particular two-part Section 11 shape. This is the next thing that would
move the REVISE item to KEEP or reveal it's narrower than currently
believed.
