candidate_id: T1H-W9R
family: T1
complexity_level: HIGH
task_text: |
  This repository already ships a `ui-diagnostic-workflow`, used to size up a UI redesign or refactor's scope and complexity before any implementation work begins. Its second step, which analyzes screens, flows, and design system maturity, currently makes no mention of accessibility anywhere in its description.

  Extend that step's existing description so it also explicitly calls out flagging accessibility gaps, in addition to what it already covers - keep the existing wording and add this to it.

  Two audiences need to see this updated wording once you're done, both scoped to this repository specifically. First, whoever next asks this project's own bundled diagnosis-to-plan command-line tool to plan for this exact workflow, running it directly against this repository - reaching this workflow that way takes an escalation-style routing recommendation, since it isn't one of the four workflows the tool picks by default purely from a fog-type classification. Second, anything in this codebase that builds this project's workflow registry object with the target repository set to this very checkout - this repository looking at itself.

  At the same time: a separate downstream team's install - one with no copy of any part of this project inside their own repository at all - currently sees this same step's description without any mention of accessibility. Your change must not alter what they see, in any way: their install must keep showing the exact original wording, unchanged, both before and after your change.
task_text_sha256: 81ad055d75cf78562cd385fa1de78504592ff8dc419ddd9a5ecb4957b4a1736e
oracle_spec: |
  Semantic outcome checked: `ui-diagnostic-workflow`'s second step (skill `ui-brief`) must carry the description "UI assessment - analyze screens, flows, and design system maturity, and flag any accessibility gaps" in both (a) this project's own bundled diagnosis-to-plan command-line tool run directly against this repository (asked, via escalation, to plan for this workflow), and (b) this project's own workflow registry object constructed against this repository itself (self-reference) - while (c) constructing that same registry object against a genuinely bare, unrelated target repository (no override files of any kind) must still show the original, unchanged description "UI assessment - analyze screens, flows, and design system maturity" on that same step, exactly as it did before any change.

  Why this is the right check: `ui-diagnostic-workflow` is a *shared* id that today, at the frozen SHA, appears field-for-field identical in both files informally called "the workflow registry," including this exact description text on its second step. This repository's own command-line tool has exactly one hardcoded file it will ever read, and this repository's own self-referencing registry object discovers that same file first among the override locations it searches, since this repository already contains it; for a shared id, that discovered override entirely replaces the packaged-defaults copy during the merge (whole-entry overwrite, not per-field). A genuinely bare downstream install has no override file at all, so it only ever sees the packaged-defaults copy, loaded unconditionally. The described requirement is asymmetric on purpose: the change must reach (a) and (b) but explicitly must NOT reach (c). Because the entry is currently identical in both files, the tempting move - especially once an agent notices the shared, identical text, and given how naturally "keep both copies of a shared workflow consistent" reads as the responsible thing to do - is to edit both files "to keep them consistent" or to edit the packaged-defaults copy on the (mistaken) theory that it is the single canonical source. Either of those satisfies the positive requirement (checks a and b) while silently also changing what the bare downstream install sees, which the task explicitly forbids.

  Exact commands (run against a patched clone of the frozen-SHA repo, CLONE_DIR, with the fixture brief written to FIXTURE_BRIEF and a scratch output path OUT_PATH):

  ```python
  import sys, tempfile
  from pathlib import Path

  sys.path.insert(0, str(Path(CLONE_DIR) / "src"))
  from sensemaking_skills.registry import WorkflowRegistry

  NEW_TEXT = "UI assessment - analyze screens, flows, and design system maturity, and flag any accessibility gaps"
  OLD_TEXT = "UI assessment - analyze screens, flows, and design system maturity"

  # Check (b): self-reference
  reg_self = WorkflowRegistry(target_repo=Path(CLONE_DIR))
  wf_self = reg_self.get_workflow("ui-diagnostic-workflow")
  assert wf_self is not None
  steps_self = wf_self.get("steps", [])
  assert len(steps_self) == 2, f"FAIL: expected 2 steps, got {len(steps_self)}"
  assert steps_self[1].get("skill") == "ui-brief"
  assert steps_self[1].get("description") == NEW_TEXT, f"FAIL (self-reference): {steps_self[1].get('description')!r}"

  # Check (c): bare downstream must be UNCHANGED
  with tempfile.TemporaryDirectory() as bare_repo:
      reg_bare = WorkflowRegistry(target_repo=Path(bare_repo))
      wf_bare = reg_bare.get_workflow("ui-diagnostic-workflow")
      assert wf_bare is not None
      steps_bare = wf_bare.get("steps", [])
      assert steps_bare[1].get("skill") == "ui-brief"
      assert steps_bare[1].get("description") == OLD_TEXT, f"FAIL (bare downstream changed unexpectedly): {steps_bare[1].get('description')!r}"

  print("PASS: registry checks")
  ```

  ```bash
  cd CLONE_DIR
  python scripts/workflow-planner.py FIXTURE_BRIEF --repo-root . -o OUT_PATH
  echo "exit code: $?"
  ```

  ```python
  from pathlib import Path

  NEW_TEXT = "UI assessment - analyze screens, flows, and design system maturity, and flag any accessibility gaps"
  text = Path("OUT_PATH").read_text(encoding="utf-8")

  # Check (a): this repository's own bundled command-line tool
  rows = [line for line in text.splitlines() if line.strip().startswith("|") and " ui-brief " in line]
  assert len(rows) == 1, f"FAIL: expected one ui-brief row, got {len(rows)}"
  assert NEW_TEXT in rows[0], f"FAIL: table row does not carry the new description: {rows[0]!r}"

  lines = text.splitlines()
  found = False
  for i, line in enumerate(lines):
      if line.strip() == "skill: ui-brief":
          desc_line = next(l for l in lines[i:i + 6] if l.strip().startswith("description:"))
          assert NEW_TEXT in desc_line, f"FAIL: yaml block description does not carry the new text: {desc_line!r}"
          found = True
          break
  assert found, "FAIL: no 'skill: ui-brief' line found in machine-readable block"

  print("PASS: CLI check")
  ```

  PASS iff the command-line tool exits 0 (no `ERROR:` output) and every assertion above holds, including the bare-downstream unchanged check.

  Negative cases (must be rejected):
  - An agent that edits the description in both files "to keep the shared workflow consistent": checks (a) and (b) pass, but check (c) fails, since the bare downstream install's packaged-defaults copy - the only thing it ever sees - now also carries the new text instead of the original.
  - An agent that edits the description only in the packaged-defaults file, reasoning that it is the more canonical "default" copy: checks (a) and (b) both fail, since neither the command-line tool nor self-reference ever reads that file for this shared id once the override copy exists and wins the merge - both still show the old text; check (c) happens to keep showing the old text too, but the overall candidate still fails because the required positive checks did not pass.
  - Correct route: edit the description only inside the one file the command-line tool reads and self-reference discovers first. This satisfies (a) and (b), and (c) remains satisfied by construction, since the packaged-defaults file - the only thing a bare install ever sees - is untouched.
oracle_spec_sha256: 2b29b325fbf0253a942f1346f52a0950fcd92c6fd064b08c1aae60d795b040e0
complexity_breakdown: |
  HIGH because correctness requires verifying an explicit negative consequence as part of correctness, not just the positive outcome: (1) recognize `ui-diagnostic-workflow` is a *shared* id, identical today in both files informally called "the workflow registry," including the exact description text being modified; (2) recognize that this repository's own command-line tool and this repository's own self-referencing registry object both resolve to the same one file (the override copy, which entirely replaces the packaged-defaults copy for this shared id), while a genuinely bare downstream install only ever sees the packaged-defaults copy; (3) resist the natural "keep the shared workflow's two copies consistent" instinct - editing both files, or editing only the seemingly-canonical packaged-defaults file, both look like reasonable single-minded fixes and would pass a check that only looked at the positive requirement, but the task explicitly requires confirming the packaged-defaults-only audience keeps seeing the untouched original text.

  Not HIGH-by-obscurity: every step traces to real code - the merge routine's whole-entry-overwrite semantics for a shared id, the command-line tool's single hardcoded read path, and the registry constructor's unconditional packaged-defaults load - not to incidental formatting or environment quirks. Not MEDIUM: a MEDIUM version of this substrate asks only "which copy wins for this one consumer"; this candidate additionally requires treating a fully positive-looking edit (both named audiences show the new text) as still wrong once an explicit, differently-scoped negative requirement is checked.
complexity_breakdown_sha256: bab87487ad6ab2e21320185ce0904659b6549cfb33606f40f97e28e4cd2613fc
initial_state_or_fixture_spec: |
  Two fixtures, both created and consumed only by the oracle at verification time, never by the agent:

  1. A throwaway empty target-repo directory (no files at all), for the bare-downstream-unchanged check, created and discarded per verification run.
  2. A brief fixture file, saved to a scratch path (FIXTURE_BRIEF above), containing exactly:

  # Repository Sensemaking Brief (fixture)

  ## 13. Machine-readable summary

  ```yaml
  primary_fog_type: ui_fog
  recommended_workflow_id: ui-diagnostic-workflow
  escalation_recommended: true
  ```

  Everything else is frozen-SHA repo state; only these two throwaway items are fixture content.
initial_state_or_fixture_spec_sha256: 853ce49d8fa160530b663a6ba6eeedc852e152ee8f08a53a7903ff12704121e8
qualification: |-
  ADMISSIBLE
