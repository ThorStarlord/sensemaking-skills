candidate_id: T1M-Q3F
family: T1
complexity_level: MEDIUM
task_text: |
  A separate downstream team maintains their own repository. That repository has no copy of any part of this project inside it: no local skills directory, no local override registry of any kind. The only way this project reaches their repository is as an installed dependency — their own scripts import this project's workflow registry object directly, construct it by pointing it at the root of their own repository, and read workflow definitions back out of it programmatically. Nothing in their repository is ever inspected by any command-line tool this project ships; they only ever go through the installed library's Python interface.

  That team wants a new workflow to become available to them automatically, with zero setup of their own, the next time they upgrade this project as a dependency. The new workflow must have the id `flaky-test-triage-workflow`. Its first step must run the `repo-sensemaker` skill against the target repository's current state and produce an artifact named `repository_sensemaking_brief`. Its second step must consume that same `repository_sensemaking_brief` artifact by running the `to-issues` skill, producing an artifact named `issue_list`.

  Add this new workflow so that it is genuinely available to that downstream team through the installed-library path described above, with no file changes required in their own repository.
task_text_sha256: 95dab1da6af6cbb268e51592f7e53f06b398c0ab10e1cebe8a8f4e0a829e096c
oracle_spec: |
  Semantic outcome checked: constructing this project's workflow registry object for a target repository that contains none of the three known override-file locations must expose an entry with id `flaky-test-triage-workflow`, whose first step runs skill `repo-sensemaker` with `output_artifact: repository_sensemaking_brief`, and whose second step runs skill `to-issues` with `input_artifact: repository_sensemaking_brief` and `output_artifact: issue_list`.

  Why this is the right check: the scenario describes a consumer that (a) never runs any command-line tool this project ships, and (b) points the registry object at a repository with no scaffolding of its own — i.e. the "packaged defaults, no override present" path. This is exactly the situation that discriminates between the two files both informally called "the workflow registry": one is read only by this project's own bundled command-line tool and only ever affects repositories that already carry a copy of this project's tree; the other is loaded first, unconditionally, by the registry object's own constructor, and is the only one still visible when no override file exists anywhere in the target repository. The task's downstream team is squarely in the second case.

  Exact commands (run against a patched clone of the frozen-SHA repo, CLONE_DIR):

  ```python
  import sys, tempfile
  from pathlib import Path

  sys.path.insert(0, str(Path(CLONE_DIR) / "src"))
  from sensemaking_skills.registry import WorkflowRegistry

  with tempfile.TemporaryDirectory() as bare_repo:
      reg = WorkflowRegistry(target_repo=Path(bare_repo))
      wf = reg.get_workflow("flaky-test-triage-workflow")

      assert wf is not None, "FAIL: not visible to a bare-target-repo library consumer"
      steps = wf.get("steps", [])
      assert len(steps) >= 2, "FAIL: fewer than 2 steps"
      assert steps[0].get("skill") == "repo-sensemaker"
      assert steps[0].get("output_artifact") == "repository_sensemaking_brief"
      assert steps[1].get("skill") == "to-issues"
      assert steps[1].get("input_artifact") == "repository_sensemaking_brief"
      assert steps[1].get("output_artifact") == "issue_list"
      print("PASS")
  ```

  Also confirm on disk that the entry lives in `src/sensemaking_skills/defaults/workflow-registry.yaml` and that no existing entry in that file was removed or renamed:

  ```python
  import yaml
  from pathlib import Path

  defaults_path = Path(CLONE_DIR) / "src" / "sensemaking_skills" / "defaults" / "workflow-registry.yaml"
  data = yaml.safe_load(defaults_path.read_text(encoding="utf-8"))
  ids = [w["id"] for w in data["workflows"]]
  assert "flaky-test-triage-workflow" in ids
  assert len(ids) == 21, f"expected the 20 original defaults entries plus 1 new one, got {len(ids)}"
  ```

  PASS iff both snippets complete without an AssertionError.

  Negative case (must be rejected): an agent that adds `flaky-test-triage-workflow` only to `skills/workflow-planner/references/workflow-registry.yaml` — the file this repo's own bundled CLI tool reads, and the one most likely to catch an agent's eye first since it is larger and more prominently referenced — fails the first check. A bare target repo (no `skills/workflow-planner/`, no `skills/workflow-orchestrator/`, no `.sensemaking/` anywhere inside it) never discovers that file, because the registry object only ever looks for override files *inside the repository it is pointed at*, never inside this project's own checkout. In that wrong-route case `wf` is `None` and the first assert fails.
oracle_spec_sha256: 336ba8df1a5e51f5e43757e050d49fa6c626b6730e8ab6ec441a21a65068d20a
complexity_breakdown: |
  Two reasoning hops: (1) recognize that the consumer described — imports the registry object directly, points it at their own bare repository, never runs any bundled command-line tool — is exactly the "packaged defaults, no override file present" path, as opposed to the "this repo's own tooling" path; (2) having identified that path, identify which of the two same-named "workflow registry" files is the one unconditionally loaded first by the registry object's constructor, and place the new entry there.

  Not HIGH: this is a single lookup-precedence question resolved by a straight, non-branching consumer-to-file mapping — no merge-order reasoning is required (the id is new, not shared), and no second, unrelated kind of check (schema validation, a different registry, a multi-step artifact chain) has to be combined with it. Not trivial: the two files share a name, a directory-shaped naming convention ("references/workflow-registry.yaml" appears under both `skills/workflow-planner/` and, differently, under the package layout), and the file this repo's own tooling reads is the larger, more prominently used one — so guessing "the one this repo uses" is a real, available wrong answer, not a strawman.
complexity_breakdown_sha256: a723697a84e6676068d340de43cc9be4d56b45339b0d551763eb59513d8b05a7
initial_state_or_fixture_spec: |-
  frozen SHA repo state, no fixture changes required — the oracle constructs its own throwaway empty target-repo directory at verification time and discards it afterward.
initial_state_or_fixture_spec_sha256: 46a564128f9366410a7882439e7249b61c3081fe234393e8700bb50e4fcefb84
qualification: |-
  ADMISSIBLE
