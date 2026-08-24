candidate_id: T1M-V8N
family: T1
complexity_level: MEDIUM
task_text: |
  This repository already ships a workflow named `setup-sensemaking-repo`, used to configure a target repository for this tooling. Several other workflows already defined in this repository enforce a specific git branch-naming discipline before they are allowed to start: they declare that a branch matching a `yolo/{workflow_id}/{timestamp}` pattern is required.

  `setup-sensemaking-repo` does not yet enforce any branch policy. Add the same requirement to it: `setup-sensemaking-repo` must require a branch matching that `yolo/{workflow_id}/{timestamp}` pattern before it is allowed to run.

  Make sure this actually takes effect for this repository: anything in this codebase that inspects this repository's own workflow registry, pointed at this checkout itself, must see the new branch-policy requirement on `setup-sensemaking-repo`.
task_text_sha256: 2978eadf74b902cbcb05cc3e515f81372c3f702ba7fd4cca234d817d090cae52
oracle_spec: |
  Semantic outcome checked: constructing this project's workflow registry object with the target repository set to the patched clone's own root (i.e. this repository pointed at itself) and reading the `setup-sensemaking-repo` entry back out must show a `branch_policy` of `{required: true, pattern: "yolo/{workflow_id}/{timestamp}"}`.

  Why this is the right check: `setup-sensemaking-repo` is a *shared* id — at the frozen SHA it appears, field-for-field identical, in both files informally called "the workflow registry". The registry object always loads the packaged-defaults copy first, unconditionally, and then — because the patched clone is pointed at itself — discovers its own optional override file and merges it in. That merge is a whole-entry overwrite keyed by id, not a per-field deep merge: for any id the override file already defines (which `setup-sensemaking-repo` is, today, in both files), the override file's copy of that entry entirely replaces the packaged-defaults copy, field by field, rather than layering on top of it. So an edit landing only in the packaged-defaults file is silently discarded for this id whenever this repository is pointed at itself, even though "the defaults file" is, on its face, the more obviously canonical-sounding of the two.

  Exact commands (run against a patched clone of the frozen-SHA repo, CLONE_DIR):

  ```python
  import sys
  from pathlib import Path

  sys.path.insert(0, str(Path(CLONE_DIR) / "src"))
  from sensemaking_skills.registry import WorkflowRegistry

  reg = WorkflowRegistry(target_repo=Path(CLONE_DIR))
  wf = reg.get_workflow("setup-sensemaking-repo")
  assert wf is not None

  bp = wf.get("branch_policy") or {}
  assert bp.get("required") is True, f"FAIL: branch_policy.required is {bp.get('required')!r}"
  assert bp.get("pattern") == "yolo/{workflow_id}/{timestamp}", f"FAIL: branch_policy.pattern is {bp.get('pattern')!r}"
  print("PASS")
  ```

  Also confirm the *other* three workflow steps of `setup-sensemaking-repo` were left untouched (id count and step wiring unchanged), to rule out a rewrite that happens to satisfy `branch_policy` by accident:

  ```python
  steps = wf.get("steps", [])
  assert len(steps) == 3
  assert [s.get("skill") for s in steps] == ["setup-sensemaking-skills", "repo-sensemaker", "handoff"]
  ```

  PASS iff both snippets complete without an AssertionError.

  Negative case (must be rejected): an agent that adds `branch_policy` only to `src/sensemaking_skills/defaults/workflow-registry.yaml`, leaving the other file's `setup-sensemaking-repo` entry unedited, fails the check above. `WorkflowRegistry(target_repo=Path(CLONE_DIR))` still finds the clone's own override file (the clone is pointed at itself), and that unedited entry for the same id entirely replaces the edited packaged-defaults entry during the merge — so `wf.get("branch_policy")` comes back `None`/falsy and the assert fails, even though the requested text was, in fact, written into a real file inside the clone. This is the plausible wrong-route failure this candidate exists to detect: "the defaults file" reads as the authoritative source, but for a shared id inspected via self-reference it is the one file whose edit is provably inert.
oracle_spec_sha256: e5df3a3c3156b7bf6ffff0259897cce8274a2b4d3fe9bc5d49b08ddfd1cd62fb
complexity_breakdown: |
  Two reasoning hops: (1) recognize `setup-sensemaking-repo` is a *shared* id, defined identically today in both files informally called "the workflow registry", not a new id; (2) recognize that the consumer described — "this codebase inspecting its own registry, pointed at this checkout" — is exactly the case where, for a shared id, the override copy entirely replaces the packaged-defaults copy rather than merging field-by-field with it, so the edit has to land in the copy that wins that replacement, not in the one that sounds more canonical.

  Not HIGH: single mechanism family (registry merge precedence for one already-existing id), no chained artifacts, no second unrelated kind of check to combine with it. Not trivial: the two files are field-for-field identical for this id before the edit, "defaults" is a genuinely tempting first guess for where the "real" configuration lives, and the merge behavior (whole-entry overwrite, not deep merge) is not something that can be guessed from either filename — it has to be traced in the merge code to be sure.
complexity_breakdown_sha256: 96bf292c125213d79ce13ee6a73c2d2eb66abf59ffd11259bb464d3a5d5829ae
initial_state_or_fixture_spec: |-
  frozen SHA repo state, no fixture changes required — the oracle points the registry object at the patched clone's own root, which already exists as soon as the clone exists.
initial_state_or_fixture_spec_sha256: 1ee1b9bbf80898d51de23c148788f02f08b2a1375e5b1d65e53963ec00cc02bb
qualification: |-
  ADMISSIBLE
