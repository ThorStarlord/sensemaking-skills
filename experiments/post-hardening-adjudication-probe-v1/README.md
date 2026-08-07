# Post-hardening adjudication probe v1 (Task D) - run protocol

## What this is
Execution of the probe designed in experiments/post-hardening-decision-probe-v1/probe-design-v1.md
(Task C). A blinded, human-adjudicated comparison of baseline vs hardened repo-sensemaker briefs
on the contested corpus repositories. The owner (human) is the measurement instrument; nothing here
decides 'candidate is more useful' on the owner's behalf.

## Sample (frozen artifacts only)
- 12 primary packets: backend-service, full-stack, multi-language, poorly-documented, multi-executable,
  hidden-coupling, strong-ui-fog, tiny-lib, unusual-layout, adv-unused-dep, web-frontend, generated-heavy
- 4 calibration packets: adv-misleading-readme, docs-heavy-code-light, monorepo, stale-readme
- Sources (read-only, from origin/hardening/repository-sensemaking-v1): corpus/<id>/** fixtures,
  baseline/<id>.md and candidate/<id>.md briefs. Copies live in packets/<id>/; identities are blinded.

## Protocol
1. For each packet: read fixture/ (all files), then brief-A.md, then brief-B.md.
2. Answer Q1-Q6 in the packet's worksheet.md or the master worksheet.
3. Do NOT open ground-truth.yaml, phase15-comparison-v1.yaml, phase18/19 reports, the disposition,
   or sealed-key.yaml until all 16 packets are judged. Blinding is procedural; keep it honest.
4. Per-repo time and confidence are part of the record.
5. After all 16 rows are complete: open sealed-key.yaml, map A/B -> baseline/candidate, then apply
   the precommitted decision rules (probe-design-v1.md section 6).

## Precommitted decision rules (from probe-design-v1.md, summarized)
- H_rubric confirmed (regression mainly rubric/taxonomy disagreement): adjudicator's label agrees with
  the CANDIDATE label on >= 5 of the 7 boundary-regressed repos, AND candidate >= baseline usefulness
  (Q2: candidate or no-material-difference) on >= 6 of the 10 boundary-changed repos, AND >= 3 of the 4
  fog flips adjudicated defensible -> next: evaluation redesign (E) then salvage (B)/deterministic (D).
- Regression real: adjudicator agrees with GROUND TRUTH on >= 5 of the 7 regressed repos, AND baseline
  judged more useful on >= 7 of the 10 boundary-changed repos, AND < 2 of 4 fog flips defensible
  -> next: retain baseline (A), optionally a simplification experiment (C).
- Ambiguous (neither branch, or 'undecidable' on >= 3 primary packets): inconclusive; second reviewer +
  claim-level rubric; no skill change.
- Invariant: no implementation; hardening workstream stays closed; candidate skill is not merged or copied.

## Cost
~3-5 h total (12-16 packets x 10-15 min + ~1 h analysis). Zero tooling; all artifacts frozen.
