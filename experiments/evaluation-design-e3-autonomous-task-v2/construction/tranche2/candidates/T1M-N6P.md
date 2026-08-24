candidate_id: T1M-N6P
family: T1
complexity_level: MEDIUM
task_text: |
  A separate downstream team maintains their own repository, with no copy of any part of this project inside it at all - no local skills directory, no local override registry of any kind. They reach this project only as an installed library dependency: their own scripts construct this project's workflow registry object directly, pointing it at the root of their own repository, and read workflow definitions back out of it programmatically. Nothing in their repository is ever inspected by any command-line tool this project ships; they only ever go through the installed library's interface.

  This project already offers a `docs-contract-reconciliation` workflow. Its second step, which reconciles the drift a diagnosis has surfaced, currently carries no description text on it at all.

  Give that step this exact description: "Reconciliation - resolve drift between documentation, registries, contracts, and templates"

  This change must reach that downstream team automatically, with zero setup of their own, the next time they upgrade this project as a dependency - through the installed-library path described above.
task_text_sha256: ad425eff9e041eedc6c6664b8cd9b0841588fe6ecfd2f036ffcc151bab0d4d5f
oracle_spec: |
  Semantic outcome checked: constructing this project's workflow registry object for a target repository that contains none of the three known override-file locations, then reading the `docs-contract-reconciliation` entry back out, must show a second step (skill `sensemaking-docs-reconciler`) whose description reads exactly "Reconciliation - resolve drift between documentation, registries, contracts, and templates" - while the rest of that workflow's step wiring is unchanged.

  Why this is the right check: the scenario describes a consumer that never runs any command-line tool this project ships and points the registry object at a repository with no scaffolding of its own - the "packaged defaults, no override present" path. `docs-contract-reconciliation` is not a new id; at the frozen SHA it already exists, field-for-field identical, in both files informally called "the workflow registry," and neither copy currently has a description on this step. Because the described consumer's target repository never contains any of the three candidate override locations the registry object searches for, the only file that can possibly reach them is the one loaded first, unconditionally, by the registry object's own constructor, independent of any override. An edit to the *other* file - the one this project's own bundled command-line tool reads, and the one this project's own checkout would discover first if it inspected itself - has no effect on this audience at all, no matter how correct the edit looks in isolation.

  Exact commands (run against a patched clone of the frozen-SHA repo, CLONE_DIR):

  ```python
  import sys, tempfile
  from pathlib import Path

  sys.path.insert(0, str(Path(CLONE_DIR) / "src"))
  from sensemaking_skills.registry import WorkflowRegistry

  NEW_TEXT = "Reconciliation - resolve drift between documentation, registries, contracts, and templates"

  with tempfile.TemporaryDirectory() as bare_repo:
      reg = WorkflowRegistry(target_repo=Path(bare_repo))
      wf = reg.get_workflow("docs-contract-reconciliation")

      assert wf is not None, "FAIL: workflow missing entirely for a bare-target-repo library consumer"
      steps = wf.get("steps", [])
      assert len(steps) == 3, f"FAIL: expected 3 steps, got {len(steps)}"
      assert steps[0].get("skill") == "repo-sensemaker"
      assert steps[1].get("skill") == "sensemaking-docs-reconciler"
      assert steps[1].get("description") == NEW_TEXT, f"FAIL: {steps[1].get('description')!r}"
      assert steps[2].get("skill") == "handoff"
      print("PASS")
  ```

  PASS iff the snippet completes without an AssertionError.

  Negative case (must be rejected): an agent that edits the description only inside the file this project's own bundled command-line tool reads - the more prominently-organized, larger file, and the one this repository would find first if it inspected its own registry - fails the check above. A genuinely bare target repository, with none of the three override-file locations present, never discovers that file at all: the registry object's search for override files only ever looks *inside the repository it is pointed at*, never inside this project's own checkout. In that wrong-route case, `wf.get("steps")[1].get("description")` still returns `None`, exactly as it did before the edit, and the assertion fails.
oracle_spec_sha256: cf884e2a707cd0850a4f9f80abb8014213a716134d0756465463fe3035a05d2a
complexity_breakdown: |
  Two reasoning hops: (1) recognize that the consumer described - imports the registry object directly, points it at their own bare repository, never runs any bundled command-line tool - is exactly the "packaged defaults, no override file present" path; (2) recognize that `docs-contract-reconciliation` already exists, identically, in both files today, so this is a field edit on an existing shared id rather than a fresh add - and that "the entry already exists, so just edit it wherever it lives" is not sufficient, because it lives, unedited, in both places, and only one of them is ever visible to this specific audience.

  Not HIGH: a single lookup-precedence question resolved by a straight, non-branching consumer-to-file mapping - no merge-order reasoning is required beyond recognizing the target file, and no second, differently-scoped audience (this project's own command-line tool, or this project inspecting itself) has to be simultaneously satisfied or explicitly ruled out. Not trivial: the workflow already exists and already looks fully defined, which makes "just add the description to it" read as a one-file, no-further-thought edit unless the two-copies fact is actually noticed.
complexity_breakdown_sha256: ca7f395f6f42cf4f434341396e54267ffa292c0cf1c23ae3c0be941996a11855
initial_state_or_fixture_spec: |-
  frozen SHA repo state, no fixture changes required - the oracle constructs its own throwaway empty target-repo directory at verification time and discards it afterward.
initial_state_or_fixture_spec_sha256: 8c20e1248ca8ecf46d55b3faed83428ae4709879dacb911ea80ddab26dcb2cc6
qualification: |-
  ADMISSIBLE
