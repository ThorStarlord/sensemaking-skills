# Research Addendum: Prospective Dogfood for Warrant as a Control Primitive

**Status:** research evidence / product-design study  
**Authority:** not an ADR, not a product contract, not a Workflow-v0 change  
**Parent study:** `docs/research/warrant-as-control-primitive.md`  
**Application domain:** agentic software engineering / repository-centered engineering

This addendum records the prospective normal-use evidence requested by Section 16 of the parent study. It preserves the empirical sequence separately so the original hypothesis note remains a chronological record of the model before prospective dogfood.

---

## 1. Research gate being tested

The parent study ended with this gate:

> **Use the warrant framing prospectively on a small number of normal engineering transitions and ask whether it changes, prevents, or clarifies a consequential decision.**

The test should not reward the vocabulary merely for describing a decision after the fact. The framing must either:

- change which responsibility is selected;
- prevent an unwarranted transition;
- constrain a claim to what its evidence actually supports; or
- expose a distinct authority or verification boundary that would otherwise be easy to collapse.

No warrant schema, score, state machine, or runtime mechanism is part of this test.

---

## 2. Prospective case: stale PR #163 and the live `integration_fog` validator defect

### Starting situation

PR #163 had previously identified a real contradiction:

- `docs/canonical-vocabulary.yaml` contained five canonical fog types, including `integration_fog`;
- `scripts/validate-brief.py` still hard-coded only four values for `primary_fog_type`;
- a canonical `integration_fog` brief was therefore rejected.

But by the time the Path-2 study was applied, PR #163 itself was stale and conflicted. It also bundled six files, including historical Skill/template wording that predated later responsibility-first product reconciliation.

The live finding and the old carrying artifact therefore had to be evaluated separately.

### Candidate targets

The prospective warrant check named three different targets:

```text
target A: merge/revive PR #163 as-is

target B: freshly repair the current validator/canonical-vocabulary contradiction

target C: broaden the work into all historical fog-related Skill/template prose
```

### Warrant assessment before implementation

```text
target A
merge/revive PR #163 as-is
-> not warranted
reason: stale/conflicted six-file package was not current evidence of the smallest correct repair

target B
fresh bounded validator repair
-> technically warranted
reason: current canonical registry and current validator directly contradicted each other

target C
full fog-documentation reconciliation
-> not established by this finding alone
reason: broader prose had separate product/history concerns and should not be silently inherited from the stale PR
```

### Decision effect

This changed the engineering action before implementation.

Without naming the target, the reasoning could easily have collapsed:

```text
#163 contains the fix
-> revive #163
```

The warrant framing instead produced:

```text
live finding
!= live carrying artifact

live finding
-> freshly derive the smallest current responsibility
```

That produced fresh PR #183 against current canonical `main`, rather than reviving #163.

### Prospective lesson 1

> **Warrant is not attached to an artifact. A stale artifact can preserve a live finding without itself remaining a warranted implementation vehicle.**

---

## 3. Candidate implementation and finding-specific evidence

Fresh PR #183 was deliberately bounded to two files:

- `scripts/validate-brief.py`;
- `tests/fixtures/validate-brief/valid/integration-fog-brief.md`.

The validator now sources the allowed `primary_fog_type` values from canonical vocabulary through the already-existing `load_canonical_vocabulary()` helper. The positive fixture proves that `integration_fog` is accepted through the repository's normal validator-verification path.

### Exact candidate

```text
base: eca65857b0ac1bc918f688b55d92e0aa88671914
head: cb73b18cecc6fd847b52efd33843b97fb1b6957b
tree: 40da4209b4f3f2a04cabf99e9a71831569144c25
```

Validator Ecosystem run `32073209476` completed with **18 / 18 jobs green**.

Inside Repository validation, `scripts/test-validators.py` reported **78 / 78 cases passed**, including:

```text
validate-brief.py | integration-fog-brief.md | positive | PASS
```

GitHub's PR merge-preview commit had the same tree SHA as the raw candidate head, so the focused fixture evidence applied to the exact candidate content.

### A useful evidence correction during the case

An initial standalone regression test was found not to be load-bearing in the canonical CI subset. The claim target was not merely:

```text
a test exists
```

but:

```text
the configured repository validation actually exercises the repaired behavior
```

That distinction changed the proof strategy: the standalone test was removed and the regression was moved into the existing validator-fixture harness executed by canonical Repository validation.

### Prospective lesson 2

> **A warrant target constrains not only the action but the kind of evidence required. “A regression test exists” and “canonical validation exercises the regression” are different claims.**

---

## 4. Candidate validity did not propagate to merge authority

After exact-head validation, the candidate had strong technical evidence.

That warranted bounded claims such as:

- the validator contradiction had a focused repair candidate;
- `integration_fog` passed the repaired validator through the load-bearing harness;
- the candidate satisfied the configured PR validation ecosystem.

It did **not** warrant:

- claiming the repair was canonical on `main`;
- claiming original-finding closure;
- merging without owner authorization;
- broadening the repair into PR #163's historical six-file scope.

The PR therefore stopped at the owner integration boundary.

### Prospective lesson 3

> **Technical sufficiency and action authority remain distinct even when warrant is used as the common control question.**

Compactly:

```text
candidate validity
!= merge authority
```

---

## 5. Owner authorization, integration, and canonical-state warrant

After explicit owner authorization, PR #183 was marked ready and squash-merged as:

```text
65719b0f2857ca192aad52eb71a9ad232c4dafa5
```

Canonical `main` was then refreshed and verified to point exactly to that SHA.

This changed the state, but merge itself did not warrant a claim that canonical state was healthy.

A separate push-triggered Validator Ecosystem run was required:

```text
run: 32075008182
event: push
branch: main
head: 65719b0f2857ca192aad52eb71a9ad232c4dafa5
result: 18 / 18 jobs green
```

Canonical Repository validation again reported **78 / 78 validator cases passed**, including the positive `integration_fog` fixture.

### Prospective lesson 4

> **Integration changes the warrant target. Candidate validity does not automatically become canonical-state validity merely because the candidate was merged.**

Compactly:

```text
merge
!= canonical validity
```

---

## 6. Finding-specific closure and supersession of PR #163

The canonical push run established both broad canonical health and finding-specific evidence for the original validator contradiction:

```text
canonical main
+ validator harness green
+ integration_fog positive fixture PASS
-> original validator finding repaired on canonical state
```

Only after that evidence was present was PR #163 closed **unmerged** as superseded for the validator defect.

The closure deliberately did **not** claim that PR #163's broader historical Skill/template/documentation package had been merged or independently resolved.

### Prospective lesson 5

> **Canonical validity and original-finding closure are separate targets. Closure is warranted only by evidence relevant to the original finding, not by generic green status alone.**

Compactly:

```text
canonical validity
!= finding-specific closure
```

---

## 7. Full prospective warrant sequence

The case exercised the model across the complete engineering lifecycle:

```text
current evidence shows live canonical contradiction
-> warrants bounded repair responsibility

stale PR contains useful prior evidence
-> does not warrant reviving stale package

fresh candidate implemented
-> warrants implementation claim

focused load-bearing regression + exact-head 18/18
-> warrants candidate-level validation claims

owner authorization
-> permits integration

merge completes
-> warrants integrated-state claim
-> does not yet warrant canonical-health claim

push-triggered canonical 18/18
-> warrants canonical validation claim

canonical integration_fog fixture PASS
-> warrants original validator-finding closure

broader historical docs from #163
-> remain outside this closure unless separately warranted
```

The useful control property is not a new lifecycle sequence. It is the repeated question:

> **What does the current evidence and authority warrant for this specific target now?**

---

## 8. What this prospective case supports

This case supports the parent study's candidate properties:

1. **Target-specific.** The same evidence supported some targets and not others.
2. **Defeasible/state-relative.** Historical #163 evidence remained useful, while #163 itself ceased to be the warranted implementation vehicle.
3. **Evidence-traceable.** The regression proof had to be load-bearing in the configured validation path.
4. **Authority-bounded.** Technical evidence did not grant merge authority.
5. **Non-transitive.** Candidate validity, merge authority, canonical validity, and closure required distinct support.
6. **Proportional.** Broader documentation closure was explicitly withheld because the evidence only closed the validator finding.

Most importantly, the framing was not merely descriptive after the fact. It changed the selected implementation vehicle, changed the regression-proof strategy, and constrained downstream claims.

---

## 9. Research gate conclusion

The dedicated **design-research cycle for Research Path 2 is complete enough to stop theorizing about the basic abstraction.**

The supported qualitative answer is:

> **Warrant is useful as a target-specific, defeasible justification relation for consequential engineering claims and transitions. It can serve as a recurring Sensemaking control question, provided evidence, validation, verification, and authority remain distinct mechanisms rather than being collapsed into a single state or score.**

A compact form is:

```text
candidate target
-> what must be true or permitted for this target to be justified?
-> what current evidence/authority supports or defeats it?
-> what bounded responsibility can change that support?
-> what does the new evidence warrant now?
```

The prospective case gives evidence that this framing can improve real engineering control decisions.

It does **not** establish that `warrant` should become a formal product primitive, persisted artifact, schema, score, state machine, or runtime mechanism.

---

## 10. What remains unratified

Do not infer from this research completion that any of the following is now warranted:

- a `WarrantEngine`;
- a warrant schema or `warrant_gap` field;
- a numeric warrant/confidence score;
- a new workflow lifecycle;
- automatic transition authorization;
- automatic routing;
- a Workflow-v0 rewrite;
- replacement of existing validation, reconciliation, repair-verification, or authority concepts.

The research currently supports **an explanatory/control question**, not new machinery.

---

## 11. Recommended next product behavior

Stop running dedicated warrant experiments for their own sake.

Use the framing during ordinary engineering work only when it clarifies a consequential boundary. Preserve cases where it fails, becomes verbose, produces reviewer disagreement, or collapses distinctions it was supposed to protect.

Promotion should require repeated independent normal-use evidence of a concrete recurring problem that a small product wording change would solve.

If that evidence appears, the smallest plausible promotion would be an operating-model clarification such as:

> **Before a consequential transition or claim, name the target and ensure current evidence and required authority support that target specifically; do not propagate warrant automatically from earlier lifecycle stages.**

Even that wording is **not ratified by this addendum**. It is only a candidate future clarification.

---

## 12. Updated research status

```text
research question                         answered qualitatively
retrospective normal-use evidence          present
candidate qualitative model                present
external conceptual comparison             present
prospective normal-use evidence             present
full prospective lifecycle                 observed
falsification criteria                      defined
basic design-research cycle                 complete
product ratification                        not warranted
mechanical formalization                    not warranted
```

The appropriate next state is therefore:

> **Preserve the research result, return to normal engineering use, and let repeated real friction—not conceptual elegance—decide whether any part should be promoted into the operating contract.**

---

## Evidence references

Repository research:

- `docs/research/warrant-as-control-primitive.md`;
- `docs/research/uncertainty-selection.md`;
- `docs/research/control-model-research-agenda.md`.

Prospective case:

- stale PR #163 (`Drive fog vocabulary from canonical registry, add integration_fog`);
- fresh repair PR #183 (`fix: drive primary fog validation from canonical vocabulary`);
- PR #183 exact candidate `cb73b18cecc6fd847b52efd33843b97fb1b6957b`;
- PR Validator Ecosystem run `32073209476`;
- squash merge `65719b0f2857ca192aad52eb71a9ad232c4dafa5`;
- canonical push Validator Ecosystem run `32075008182`.
