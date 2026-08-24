candidate_id: T1H-K9W
family: T1
complexity_level: HIGH
task_text: |
  This project ships a reusable `skill-evaluation-workflow`, relied on both by downstream teams who install this project purely as a library dependency (no local copy of this project's own skills or scripts anywhere inside their own repository) and by this project's own maintainers. That workflow's final step hands off the completed skill-improvement work to whoever picks it up next; call this the closing handoff step.

  Right now, a downstream team constructing this project's workflow object and pointing it at their own bare repository (no override files of any kind) already sees a one-line description on that closing handoff step. But this project's own bundled diagnosis-to-plan command-line tool, run directly against this repository, currently shows no description at all on that same step. This project's own workflow object, pointed directly at this very repository (its own checkout), also currently shows no description there.

  Change the closing handoff step's description so that ALL THREE of the following show the exact same new text:

  "Completion summary - document changes, next steps, and confirm the improved skill still passes its target scenarios"

  1. A downstream team's install, with their workflow object pointed at their own bare repository (no override files of any kind).
  2. This project's own bundled diagnosis-to-plan command-line tool, run directly against this repository, when asked to plan for this exact workflow (via an escalation-style routing recommendation, since this workflow isn't one of the four workflows this tool selects by default from a fog-type classification alone).
  3. This project's own workflow object, pointed directly at this very repository (its own checkout).

  No gaps: none of the three may show the old text, a blank/missing description, or anything other than the exact new text above.
task_text_sha256: 8eafaa3b2b5da1a9b6ca6a58d6ac2f941708d565d498be32b231e2a1c395f5dc
oracle_spec: |
  Semantic outcome checked: the closing handoff step's description for `skill-evaluation-workflow` must read exactly "Completion summary - document changes, next steps, and confirm the improved skill still passes its target scenarios" in all three of: (a) this project's workflow registry object constructed against a genuinely bare downstream repository (no override files at all), (b) this project's own bundled diagnosis-to-plan command-line tool run directly against this repository, and (c) this project's own workflow registry object constructed against this repository itself (self-reference).

  Why this is the right check: `skill-evaluation-workflow` is a *shared* id that exists, today, in both files informally called "the workflow registry" — but its closing handoff step's description field is not identical between them: one copy already carries a one-line description, the other has no description key on that step at all. The registry object always loads the packaged-defaults copy first, unconditionally, for every target_repo. A genuinely bare target_repo (no override files anywhere inside it) never finds any override, so it sees only the packaged-defaults copy directly. This repository's own bundled command-line tool has exactly one hardcoded file it will ever read, regardless of target_repo, and that file is not the packaged-defaults file. When this repository's own registry object is pointed at itself, it discovers its own override file (the same one the command-line tool reads) and merges it on top of the packaged-defaults copy — but that merge is a whole-entry overwrite keyed by id, not a per-field merge, so for a shared id the override copy entirely replaces the packaged-defaults copy rather than layering on top of it. The practical consequence: a defaults-only edit is invisible to the command-line tool and is silently discarded by self-reference (masked by the override copy's own, unedited step), while an override-only edit is invisible to any genuinely bare downstream install that never has that file at all. Only an edit landing in BOTH files, with matching text, satisfies all three named audiences at once.

  Exact commands (run against a patched clone of the frozen-SHA repo, CLONE_DIR, with the fixture brief written to FIXTURE_BRIEF and a scratch output path OUT_PATH):

  ```python
  import sys, tempfile
  from pathlib import Path

  sys.path.insert(0, str(Path(CLONE_DIR) / "src"))
  from sensemaking_skills.registry import WorkflowRegistry

  NEW_TEXT = "Completion summary - document changes, next steps, and confirm the improved skill still passes its target scenarios"

  # Check 1: bare downstream repo (library-only consumer, no override files anywhere)
  with tempfile.TemporaryDirectory() as bare_repo:
      reg_bare = WorkflowRegistry(target_repo=Path(bare_repo))
      wf_bare = reg_bare.get_workflow("skill-evaluation-workflow")
      assert wf_bare is not None, "FAIL: skill-evaluation-workflow missing entirely for bare downstream repo"
      steps_bare = wf_bare.get("steps", [])
      assert len(steps_bare) == 3, f"FAIL: expected 3 steps, got {len(steps_bare)}"
      assert steps_bare[2].get("skill") == "handoff"
      assert steps_bare[2].get("description") == NEW_TEXT, f"FAIL (bare downstream): {steps_bare[2].get('description')!r}"

  # Check 3: self-reference (this project's own registry object, pointed at itself)
  reg_self = WorkflowRegistry(target_repo=Path(CLONE_DIR))
  wf_self = reg_self.get_workflow("skill-evaluation-workflow")
  assert wf_self is not None
  steps_self = wf_self.get("steps", [])
  assert len(steps_self) == 3, f"FAIL: expected 3 steps, got {len(steps_self)}"
  assert steps_self[2].get("skill") == "handoff"
  assert steps_self[2].get("description") == NEW_TEXT, f"FAIL (self-reference): {steps_self[2].get('description')!r}"

  print("PASS: registry checks")
  ```

  ```bash
  cd CLONE_DIR
  python scripts/workflow-planner.py FIXTURE_BRIEF --repo-root . -o OUT_PATH
  echo "exit code: $?"
  ```

  ```python
  from pathlib import Path

  NEW_TEXT = "Completion summary - document changes, next steps, and confirm the improved skill still passes its target scenarios"
  text = Path("OUT_PATH").read_text(encoding="utf-8")

  # Check 2: this repository's own bundled command-line tool
  table_rows = [line for line in text.splitlines() if line.strip().startswith("|") and " handoff " in line]
  assert len(table_rows) == 1, f"FAIL: expected exactly one handoff table row, found {len(table_rows)}"
  assert NEW_TEXT in table_rows[0], f"FAIL: table row does not carry the new description: {table_rows[0]!r}"

  lines = text.splitlines()
  for i, line in enumerate(lines):
      if line.strip() == "skill: handoff":
          desc_line = next(l for l in lines[i:i + 6] if l.strip().startswith("description:"))
          assert NEW_TEXT in desc_line, f"FAIL: yaml block description does not carry the new text: {desc_line!r}"
          break
  else:
      raise AssertionError("FAIL: no 'skill: handoff' line found in machine-readable block")

  print("PASS: CLI check")
  ```

  PASS iff the command-line tool exits 0 (no `ERROR:` output) and every assertion above holds.

  Negative cases (must be rejected):
  - An agent that edits only the packaged-defaults copy of the description (to the new text) and leaves the other copy's closing handoff step without any description key at all: the bare-downstream check passes, but both the self-reference check and the command-line-tool check fail — self-reference's whole-entry overwrite means the final merged step-3 entry is entirely the unedited override copy (no `description` key at all, so `.get("description")` returns `None`, not `NEW_TEXT`), and the command-line tool never reads the packaged-defaults file in the first place, so its printed row and machine block still carry a blank description.
  - An agent that edits only the override copy (leaving packaged defaults untouched): the command-line-tool and self-reference checks pass, but the bare-downstream check fails, because a genuinely bare repository never discovers that override file and still sees the packaged-defaults copy's original, shorter text ("Completion summary - document changes and next steps"), which does not equal `NEW_TEXT`.
oracle_spec_sha256: eb793d3768c37ea3bf3846009c157c7384af79f326d239aeb4f7ea9f15e03201
complexity_breakdown: |
  HIGH because correctness requires combining two separate T1 mechanism facts, not picking one file: (1) recognizing that `skill-evaluation-workflow` is a *shared* id whose closing-handoff-step description currently differs field-by-field between the two files informally called "the workflow registry" (present with real text in one, entirely absent in the other), rather than being identical or purely new; and (2) tracing that no single-file edit can serve all three named audiences, because self-reference's override merge is a whole-entry overwrite (not a per-field merge) — a defaults-only edit is masked entirely by the override copy's own unedited step for both this repository's own command-line tool and its own self-referencing registry object, while an override-only edit is invisible to any genuinely bare downstream install that never has that file at all. Only an edit landing in BOTH files, with matching text, satisfies all three audiences simultaneously. This also requires an extra escalation-routing hop to reach this workflow via the command-line tool at all, since it is not one of the four fog-type-mapped default workflows.

  Not HIGH-by-obscurity: every step traces to real code (the merge routine's whole-entry overwrite semantics, the command-line tool's single hardcoded read path, the constructor's unconditional default-load), not to incidental formatting or environment quirks. Not MEDIUM: a MEDIUM version of this substrate asks "which one file governs this consumer"; this candidate requires recognizing that two different files must be edited in concert to satisfy three simultaneously-named, differently-scoped consumers, plus an extra routing hop to reach the workflow at all.
complexity_breakdown_sha256: edd9efb130c874d6b43ab806d0143cd60963774228337594e4edea98a27f61f8
initial_state_or_fixture_spec: |
  Two fixtures, both written directly by the oracle at verification time (not part of the frozen repo state, and never seen or created by the agent):

  1. A throwaway empty target-repo directory (no files at all), for the bare-downstream-install check, created and discarded per verification run.
  2. A brief fixture file, saved to a scratch path (FIXTURE_BRIEF above), containing exactly:

  # Repository Sensemaking Brief (fixture)

  ## 13. Machine-readable summary

  ```yaml
  primary_fog_type: docs_fog
  recommended_workflow_id: skill-evaluation-workflow
  escalation_recommended: true
  ```

  Everything else is frozen-SHA repo state; only these two throwaway items are fixture content.
initial_state_or_fixture_spec_sha256: 5d4eaf46d5d30eecda981fe826d4dc082ffa08ac27f36eb100806ca707b5d2e5
qualification: |
  ADMISSIBLE
