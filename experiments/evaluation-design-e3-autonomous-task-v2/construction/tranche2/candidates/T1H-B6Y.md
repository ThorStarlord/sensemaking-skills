candidate_id: T1H-B6Y
family: T1
complexity_level: HIGH
task_text: |
  This repository already ships a `product-strategy-sprint` workflow. Its execution modes today allow plan-only, prompt-chain, and guided-execution use, but nothing that runs the whole thing autonomously without stopping for review at each step.

  A teammate points out that this project recognizes more than one place inside a repository where local workflow customizations can live, and mentions a second, differently-named location - one organized under an "orchestrator"-style folder rather than the more prominently used "planner"-style folder that most of this repository's own workflow customizations already live under. They suggest making the change there instead: "that folder exists so we don't have to keep touching the main file for small local tweaks."

  Before following that suggestion, work out whether it will actually take effect here, as this repository exists today, and then make whatever change actually works.

  Goal: add a fully autonomous execution mode to the list of execution modes `product-strategy-sprint` allows, alongside its existing ones.

  This must actually take effect the next time anything in this codebase inspects this repository's own workflow registry, pointed at this checkout itself.
task_text_sha256: f2d63a545632e092fd851dd12980487452169ef4c9a990adb62491d205499c4c
oracle_spec: |
  Semantic outcome checked: constructing this project's workflow registry object with the target repository set to the patched clone's own root (this repository pointed at itself) and reading the `product-strategy-sprint` entry back out must show `allowed_execution_modes` containing `autonomous_execution` in addition to its three original values (`plan_only`, `prompt_chain`, `guided_execution`), with everything else about the entry (step count, step wiring) unchanged.

  Why this is the right check: `product-strategy-sprint` is a *shared* id - at the frozen SHA it appears, field-for-field identical, in both files informally called "the workflow registry". The registry object always loads the packaged-defaults copy first, unconditionally, and then, because the patched clone is pointed at itself, discovers its own override file and merges it in as a whole-entry overwrite keyed by id - not a per-field deep merge. For a shared id the override file's entry entirely replaces the packaged-defaults entry, so an edit landing only in packaged defaults is discarded whenever this repository is pointed at itself.

  Separately, this project's registry object searches a short, ordered list of candidate override locations inside whatever target_repo it is pointed at, and stops at the FIRST one found to exist on disk - it does not continue checking the others, and does not combine multiple existing override files into a merged view. This repository already contains the first (most prominent, "planner"-style) candidate location on disk. That means ANY other candidate override location placed inside this same repository - including the "orchestrator"-style one the teammate suggested - is entirely inert for self-reference, regardless of its content, purely because the search returns as soon as the first, already-present location is found. Both facts have to be traced together: the entry must land in a file that (a) actually gets read at all by the self-referencing search (ruling out the orchestrator-style decoy), and (b) is the copy that wins the whole-entry overwrite for this shared id (ruling out packaged defaults).

  Exact commands (run against a patched clone of the frozen-SHA repo, CLONE_DIR):

  ```python
  import sys
  from pathlib import Path

  sys.path.insert(0, str(Path(CLONE_DIR) / "src"))
  from sensemaking_skills.registry import WorkflowRegistry

  reg = WorkflowRegistry(target_repo=Path(CLONE_DIR))
  wf = reg.get_workflow("product-strategy-sprint")
  assert wf is not None

  modes = wf.get("allowed_execution_modes", [])
  assert set(modes) == {"plan_only", "prompt_chain", "guided_execution", "autonomous_execution"}, f"FAIL: {modes!r}"

  steps = wf.get("steps", [])
  assert len(steps) == 5, f"FAIL: expected 5 steps, got {len(steps)}"
  assert [s.get("skill") for s in steps] == ["lean-canvas", "north-star", "okr", "roadmap", "stakeholder-update"], f"FAIL: step wiring changed: {[s.get('skill') for s in steps]!r}"
  print("PASS")
  ```

  PASS iff the snippet completes without an AssertionError.

  Negative cases (must be rejected):
  - An agent that creates a fresh override file under the "orchestrator"-style location the teammate suggested, containing a fully correct `product-strategy-sprint` entry with the new execution mode: fails the check above. This repository's own "planner"-style override file already exists on disk, is found first by the ordered candidate-location search, and the search stops there - the orchestrator-style file is never opened at all, correct content or not.
  - An agent that edits only the packaged-defaults copy, leaving the "planner"-style override file's `product-strategy-sprint` entry unedited: also fails. `WorkflowRegistry(target_repo=Path(CLONE_DIR))` still finds and uses that override file first (the clone is pointed at itself), and its unedited entry for this shared id entirely replaces the edited packaged-defaults entry during the merge - so `allowed_execution_modes` comes back as the original three values, not four.
oracle_spec_sha256: b27bd4f00cabc3caa83b720d1098bd6a15d51e391dddf00a5d7c7221d357f308
complexity_breakdown: |
  HIGH because correctness requires chaining two separate T1 mechanism facts, not picking one file: (1) recognizing `product-strategy-sprint` is a *shared* id, identical today in both files informally called "the workflow registry," so a packaged-defaults-only edit is discarded by the whole-entry overwrite that self-reference performs; and (2) recognizing that this project's override-file search is ordered and stops at the FIRST candidate location found to exist - and because this repository already has the first (most prominent) location on disk, a second, differently-named candidate location placed inside this same repository is never even opened, regardless of what it contains. A MEDIUM version of this substrate only requires recognizing fact (1) - "override beats packaged defaults for a shared id, so edit the override, not the defaults." This candidate additionally requires resisting a concrete, plausible-sounding suggestion to use a *different* override location that would work in an empty repository with no override file at all, but is provably inert here specifically because this repository already has one.

  Not HIGH-by-obscurity: both facts trace to real code - the merge routine's whole-entry-overwrite semantics for a shared id, and the override-search loop's early-return-on-first-match behavior - not to incidental formatting or environment quirks. Not MEDIUM: a MEDIUM version of this substrate asks only "does this land in the file that governs this consumer, defaults or override"; this candidate additionally requires reasoning about *which of several real, existing candidate override locations* the search will actually reach, given this repository's current on-disk state.
complexity_breakdown_sha256: f51d8faa9cbd4aaeeae9f9f91d56b7b255631ecfd25d19bf7fcc3217eb80e877
initial_state_or_fixture_spec: |-
  frozen SHA repo state, no fixture changes required - the oracle points the registry object at the patched clone's own root, which already exists as soon as the clone exists.
initial_state_or_fixture_spec_sha256: a508de16e8eaa11bb12bf9114fa334c339c4390bb50a205fa1c862554b5d793b
qualification: |-
  ADMISSIBLE
