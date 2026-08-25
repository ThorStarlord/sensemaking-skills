candidate_id: T1H-M2X
family: T1
complexity_level: HIGH
task_text: |
  This repository already offers an `architectural-review-planning-workflow`, used to evaluate a proposed architectural direction against repository diagnostics before committing to it. Its final step, which evaluates the proposed direction and identifies risks, currently completes behind an approval gate that only asks reviewers to review the recommendation.

  Tighten that final step's approval gate so that it explicitly also requires risk sign-off, not just a recommendation review: rename the gate to `review_recommendation_and_risk_signoff`.

  Make this actually take effect for both of the following, for this repository specifically:
  1. This project's own bundled diagnosis-to-plan command-line tool, run directly against this repository, when asked to plan for this exact workflow (via an escalation-style routing recommendation, since this workflow isn't one of the four workflows this tool selects by default from a fog-type classification alone).
  2. This project's own workflow object, pointed directly at this very repository (its own checkout).

  At the same time: a separate downstream team's install — one with absolutely no copy of any part of this project inside their own repository — currently has no workflow with this id at all; nothing about `architectural-review-planning-workflow` is available to them today. Your change must not alter that. After your change, their install must still behave exactly as if a workflow with this id does not exist: no gate name, no partial definition, and no entry under this id showing up for them at all.
task_text_sha256: cf148ee8fac692a2c0243b2c3e95e07bb8d9997b31db3b05b356329ea2d0be86
oracle_spec: |
  Semantic outcome checked: `architectural-review-planning-workflow`'s second step (skill `architectural-review`) must carry `gate: review_recommendation_and_risk_signoff` both (a) in the output of this project's own bundled diagnosis-to-plan command-line tool run directly against this repository (asked, via escalation, to plan for this workflow), and (b) in the entry returned by this project's own workflow registry object constructed against this repository itself (self-reference) — while (c) constructing that same registry object against a genuinely bare, unrelated target repository (no override files of any kind) must return `None` for this workflow id, exactly as it does today.

  Why this is the right check: `architectural-review-planning-workflow` is one of only two workflow ids that exist in the file this repository's own command-line tool always reads and this repository's own self-referencing registry object discovers as its override, but that do not exist at all in the packaged-defaults file loaded unconditionally for every target_repo. Editing the gate only inside that one file is necessary and sufficient for checks (a) and (b): the command-line tool has exactly one hardcoded read path, and self-reference discovers that same file first (and, in this repository, only) among the candidate override locations it searches. Because the id is absent from packaged defaults at the frozen SHA, a genuinely bare downstream install (no override files of its own) has nothing to find for this id today, and must continue to have nothing to find after the change — which holds automatically as long as the edit does not also introduce a same-id entry into the packaged-defaults file. The most tempting wrong move is to "keep the two registries in sync" by mirroring the new gate value, or the whole entry, into the packaged-defaults file too — this would satisfy (a) and (b) while silently breaking (c), since the packaged-defaults file is loaded unconditionally for every target_repo, including a bare one.

  Exact commands (run against a patched clone of the frozen-SHA repo, CLONE_DIR, with the fixture brief written to FIXTURE_BRIEF and a scratch output path OUT_PATH):

  ```python
  import sys, tempfile
  from pathlib import Path

  sys.path.insert(0, str(Path(CLONE_DIR) / "src"))
  from sensemaking_skills.registry import WorkflowRegistry

  reg_self = WorkflowRegistry(target_repo=Path(CLONE_DIR))
  wf = reg_self.get_workflow("architectural-review-planning-workflow")
  assert wf is not None, "FAIL: workflow missing for this repository's own self-referencing registry object"
  steps = wf.get("steps", [])
  assert len(steps) == 2, f"FAIL: expected 2 steps, got {len(steps)}"
  assert steps[0].get("gate") == "review_diagnosis", f"FAIL: step 1 gate changed unexpectedly: {steps[0].get('gate')!r}"
  assert steps[1].get("skill") == "architectural-review"
  assert steps[1].get("gate") == "review_recommendation_and_risk_signoff", f"FAIL (self-reference): {steps[1].get('gate')!r}"

  with tempfile.TemporaryDirectory() as bare_repo:
      reg_bare = WorkflowRegistry(target_repo=Path(bare_repo))
      assert reg_bare.get_workflow("architectural-review-planning-workflow") is None, "FAIL: leaked to a bare downstream install"

  print("PASS: registry checks")
  ```

  ```bash
  cd CLONE_DIR
  python scripts/workflow-planner.py FIXTURE_BRIEF --repo-root . -o OUT_PATH
  echo "exit code: $?"
  ```

  ```python
  from pathlib import Path
  text = Path("OUT_PATH").read_text(encoding="utf-8")

  rows = [line for line in text.splitlines() if line.strip().startswith("|") and " architectural-review " in line]
  assert len(rows) == 1, f"FAIL: expected one architectural-review row, got {len(rows)}"
  assert "review_recommendation_and_risk_signoff" in rows[0], f"FAIL: table row missing new gate name: {rows[0]!r}"

  lines = text.splitlines()
  for i, line in enumerate(lines):
      if line.strip() == "skill: architectural-review":
          gate_line = next(l for l in lines[i:i + 6] if l.strip().startswith("gate:"))
          assert "review_recommendation_and_risk_signoff" in gate_line, f"FAIL: yaml block gate mismatch: {gate_line!r}"
          break
  else:
      raise AssertionError("FAIL: no 'skill: architectural-review' line found in machine-readable block")

  print("PASS: CLI check")
  ```

  PASS iff the command-line tool exits 0 (no `ERROR:` output) and every assertion above holds, including the bare-repo negative check.

  Negative cases (must be rejected):
  - An agent that edits the gate in the one relevant file correctly, but also — out of an instinct to "keep things consistent" — adds a mirrored `architectural-review-planning-workflow` entry (with the new gate) into the packaged-defaults file too: checks (a) and (b) pass, but the bare-repo check fails, since `reg_bare.get_workflow(...)` now returns a real entry instead of `None`.
  - An agent that adds the new gate value only to the packaged-defaults file, mistaking it for the single canonical registry, without touching the file the command-line tool and self-reference actually consult: both (a) and (b) fail (the old gate name `review_recommendation` still shows), and the bare-repo check also fails, since the id now exists there too.
  - Correct route: edit the gate only inside the one file that already carries this id today. This satisfies (a) and (b), and the bare-repo check remains satisfied by construction, since the packaged-defaults file — the only thing a bare install ever sees — is untouched.
oracle_spec_sha256: e670944c84e7030c01effc59a716a4fb90d66b5507d886f2472bc9e787159adf
complexity_breakdown: |
  HIGH because correctness requires combining T1 mechanism-routing reasoning with an explicit negative-consequence check, not just landing an edit in the right place: (1) recognize that `architectural-review-planning-workflow` is one of only two workflow ids absent from the packaged-defaults file entirely at the frozen SHA, so this is a pure single-file add/modify case for the command-line-tool and self-reference audiences, not a shared-id merge question; (2) resist the natural instinct to mirror the change into the packaged-defaults file "for consistency" or "so it's available everywhere" — doing so satisfies the positive requirement but silently breaks the explicit requirement that a genuinely bare downstream install must keep seeing nothing for this id, since packaged defaults are loaded unconditionally for every target_repo regardless of overrides. A fully-passing-looking edit (both the command-line tool and self-reference show the new gate) can still be wrong once the negative check is applied — the task cannot be verified correct by checking the positive outcome alone.

  Not HIGH-by-obscurity: this traces directly to the packaged-defaults file's unconditional, override-independent loading in the registry constructor, not to incidental complexity. Not MEDIUM: a MEDIUM version of this substrate asks only "does this land in the file that governs this consumer"; this candidate additionally requires verifying that a route which looks completely correct on the positive checks alone is still wrong, because of a consequence for a third, unmentioned-in-passing audience that the task explicitly requires checking.
complexity_breakdown_sha256: 98197cb2c3f4e88d5759d2ee1dd72a1787751c70d3399657c022d06ce145d9ca
initial_state_or_fixture_spec: |
  Two fixtures, both created and discarded by the oracle at verification time only, never by the agent:

  1. A throwaway empty target-repo directory (no files at all), for the bare-downstream-negative check.
  2. A brief fixture file, saved to a scratch path (FIXTURE_BRIEF above), containing exactly:

  # Repository Sensemaking Brief (fixture)

  ## 13. Machine-readable summary

  ```yaml
  primary_fog_type: ui_fog
  recommended_workflow_id: architectural-review-planning-workflow
  escalation_recommended: true
  ```

  Everything else is frozen-SHA repo state; only these two throwaway items are fixture content.
initial_state_or_fixture_spec_sha256: e134ae99ae9928d7394e3be91ca4cc1b59725e50324e18e234a8233d4c033f20
qualification: |
  ADMISSIBLE
