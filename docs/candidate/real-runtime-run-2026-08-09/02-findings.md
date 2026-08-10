# Findings — real runtime-driven execution, 2026-08-09/10

Answers to the five questions this run was specifically requested to check.

## 1. Did Section 15 survive?

Yes. Present, complete, in `repository_sensemaking_brief.md` lines 159-208. `skeleton_integrity_ok`: True. `handoff_yaml_round_trips`: True. Both real validators (`validate-artifact.py`, `validate-brief.py`) ran against the reconciled file and produced zero blocking errors; `validate-brief.py` reported zero warnings at all, including zero `EXTENDED_ANALYSIS_*` warnings — every Section 15 field value was valid on the first real attempt.

## 2. Did the model populate it coherently?

Yes — all five fields present, each with real content grounded in the same evidence as Sections 1-14, not placeholder or templated text (compare `discovery_confidence.why_bounded`'s specific claim about what was and wasn't separately verified, or `owner_intent_state.known`'s citation of PR #163 as a precedent — genuine reasoning, not filler).

## 3. Did it agree with Sections 1-14?

Yes, and in a way that adds real information rather than restating it. `domain: [architecture]` matches `primary_fog_type: architecture_fog`. `consequential_boundary.is_demonstrated_weakness: true` is consistent with Section 6 stating a concrete `weakness_type` (not the `false`+absent-type pattern used for a legitimate-but-unresolved case). `uncertainty.question` (which of the two registries should become authoritative) is a genuinely different, complementary question from Section 11's recommended next step (which only says "regenerate canonical-vocabulary.yaml from the registry" — Section 15 surfaces that this specific direction is itself a choice, not a fact Section 11 established). No contradiction found between the two levels in this run — but see the note in `docs/candidate/draft-adr-extended-analysis.md`'s Missing Evidence section: this is one clean case, not a stress test of what happens when they *do* disagree, which remains genuinely untested.

## 4. Did architectural-review use it sensibly?

Yes, and precisely — see `01-architectural-review-output.md` in full. Two results stand out beyond a bare "yes":
- It correctly distinguished "Section 15 changed the *justification path*" from "Section 15 changed the *conclusion*" for `is_demonstrated_weakness` — it would have reached `pursue_narrowed` from Boundary Rules 1-5 alone (the base brief's own prose already established reproduced-not-inferred status), and said so explicitly rather than overclaiming Section 15's causal role.
- It self-policed the scope of Boundary Rule 6: it noticed `uncertainty.source`/`owner_intent_state` were relevant and "tempting to lean on," but correctly declined to treat them as licensed decision inputs (Boundary Rule 6 only licenses `is_demonstrated_weakness` and `domain`), using them only as corroboration for a conclusion reached independently via Rule 3. This is exactly the discipline the rule was written to produce, observed working under real isolation, not asserted.

## 5. Did absence remain harmless?

Not re-tested manually in this run — already proven by `tests/test_extended_analysis_end_to_end.py::test_reconciled_brief_without_section_15_is_unaffected`, which runs the identical real producer (`brief_skeleton.reconcile()`) and real specialized validator with Section 15 omitted entirely and asserts zero blocking errors. Citing that automated proof here rather than duplicating it by hand.

---

## A new, real, previously-undiscovered defect found while building this record

**Not part of Section 15's scope, not part of this candidate's changes — found incidentally in `scripts/brief_skeleton.py`'s pre-existing, unmodified `reconcile()` logic.**

`reconcile()`'s generic flat-field splice branch (`MODEL_YAML_FIELDS` loop, the `else` branch that doesn't special-case `evidence`/`required_inputs`) does:

```python
placeholder_re.sub(f"{key}: {value}", out, count=1)
```

When the model's harvested value for a flat field is Python `None` (i.e. the model wrote `null` in YAML, e.g. `weakness_type_explanation: null`), this produces the literal text `weakness_type_explanation: None` — which YAML parses as the **string** `"None"`, not `null`. Confirmed directly: `yaml.safe_load()` on this run's reconciled Section 13 block returns `weakness_type_explanation == 'None'` (`str`), not `None` (`NoneType`).

**Why this matters, concretely**: `validate-brief.py`'s `WEAKNESS_TYPE_OTHER_NO_EXPLANATION` check is `if not explanation or not str(explanation).strip()`. A string `"None"` is truthy and non-empty, so this check would **not** fire for a brief where `weakness_type: Other` and the model explicitly echoed `weakness_type_explanation: null` intending "no explanation given" — the exact case D4 exists to catch. In this run specifically the bug is harmless (`weakness_type` is `Contract Mismatch`, not `Other`, so `weakness_type_explanation` is never checked at all) — but the underlying serialization bug is real, reproducible, and affects every flat `MODEL_YAML_FIELDS` entry, not just this one field.

**Scope discipline**: this is a pre-existing bug in already-shipped, canonical `brief_skeleton.py` logic, unrelated to Section 15/candidate work, found only because this run explicitly echoed a field back with an explicit `null` (something a real model plausibly would do, copying the skeleton's own placeholder text). Not fixed here — flagged, per this session's established practice of recording out-of-scope findings rather than silently expanding the change.
