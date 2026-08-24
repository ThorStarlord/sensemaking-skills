candidate_id: T1M-H2R
family: T1
complexity_level: MEDIUM
task_text: |
  This project ships its own command-line tool for turning a repository diagnosis into an orchestration plan. When that tool is run directly from a checkout of this repository against a diagnosis that classifies the problem as an architecture issue, it currently prints a step table whose "define the specification" step is described only as covering refactoring strategy and module boundaries.

  Change that step's description so it also explicitly calls out flagging any breaking changes to public APIs. The next time someone runs this project's own bundled diagnosis-to-plan tool, directly against this repository, on an architecture-classified diagnosis, both the printed step table and the machine-readable plan block beneath it must show the updated description text for that step.
task_text_sha256: b8d5c8f62f3e5b6686a5ef3533b28baf84857c52caf130f954102920df786770
oracle_spec: |
  Semantic outcome checked: running this project's own bundled diagnosis-to-orchestration-plan command-line script, with its repo-root pointed at the patched clone itself, against a brief fixture classifying the problem as an architecture issue, must produce a plan whose rendered step table row (and machine-readable `workflow_steps` block) for the `to-prd` step of `architecture-implementation-workflow` contains description text mentioning breaking changes to public APIs, where the original description text ("Architecture spec - define refactoring strategy and module boundaries") did not.

  Why this is the right check: the described actor — this project's own bundled command-line tool, run directly against this repository — hardcodes exactly one lookup location for workflow step definitions, `<repo_root>/skills/workflow-planner/references/workflow-registry.yaml`, regardless of `repo_root`'s value and regardless of anything in the packaged-defaults file. Critically, `architecture-implementation-workflow` is one of only two workflow ids that exist in that file and do *not* exist at all in the packaged-defaults file at the frozen SHA — so there is no pre-existing "shared id" merge question here at all: the packaged-defaults file has nothing to overwrite or be overwritten by for this id. Any edit that does not land in the one file the script actually reads is entirely invisible to it, unconditionally.

  Fixture (see `initial_state_or_fixture_spec`): a brief file with `primary_fog_type: architecture_fog`, which the script maps to `architecture-implementation-workflow` by default.

  Exact commands (run against a patched clone of the frozen-SHA repo, CLONE_DIR, with the fixture brief written to FIXTURE_BRIEF and a scratch output path OUT_PATH):

  ```bash
  cd CLONE_DIR
  python scripts/workflow-planner.py FIXTURE_BRIEF --repo-root . -o OUT_PATH
  echo "exit code: $?"
  ```

  ```python
  from pathlib import Path
  import re

  text = Path("OUT_PATH").read_text(encoding="utf-8")
  phrase_re = re.compile(r"breaking.{0,20}public API", re.IGNORECASE)

  # Row for the to-prd step in the markdown table:
  table_rows = [line for line in text.splitlines() if line.strip().startswith("|") and " to-prd " in line]
  assert len(table_rows) == 1, f"FAIL: expected exactly one to-prd table row, found {len(table_rows)}"
  assert phrase_re.search(table_rows[0]), f"FAIL: table row does not mention breaking public API changes: {table_rows[0]!r}"

  # Machine-readable block: the description line immediately following "skill: to-prd"
  lines = text.splitlines()
  for i, line in enumerate(lines):
      if line.strip() == "skill: to-prd":
          desc_line = next(l for l in lines[i:i + 6] if l.strip().startswith("description:"))
          assert phrase_re.search(desc_line), f"FAIL: yaml block description does not mention it: {desc_line!r}"
          break
  else:
      raise AssertionError("FAIL: no 'skill: to-prd' line found in machine-readable block")

  print("PASS")
  ```

  PASS iff the script exits 0 (no `ERROR:` output, per `plan_workflow`'s own error-prefix convention) and both assertions above hold.

  Negative case (must be rejected): an agent that edits only `src/sensemaking_skills/defaults/workflow-registry.yaml` — the more "canonical library defaults"-sounding file — cannot even express this edit meaningfully there, since that file has no `architecture-implementation-workflow` entry to modify at all at the frozen SHA (introducing a fresh entry there does not affect this check either way, since the script never reads that file). The generated plan still shows the original, unedited description text, and the phrase-match assertions fail. A second plausible-but-wrong route: adding or editing the entry under a `.sensemaking/workflow-registry.yaml` override inside the clone — a real override path this project's separate registry *object* does search, but one the standalone command-line script never consults at all — produces the identical FAIL.
oracle_spec_sha256: ce2836e396b7cc1874da2772884dc74de2396e3d10531df4d9cd574f7b34b58d
complexity_breakdown: |
  Two reasoning hops: (1) recognize the actor in the task — "this project's own bundled diagnosis-to-plan command-line tool, run directly against this repository" — is the standalone script path, not the separate Python registry object with its multi-location override search; (2) recognize that script hardcodes exactly one workflow-definitions file it will ever read, independent of any packaged defaults, and place the edit there.

  Not HIGH: a single fixed lookup with no precedence or merge reasoning at all (unlike a shared-id scenario) — once the actor is correctly identified, there is only one file that could possibly work. Not trivial: the task never names that file or the script, the more prominently-organized "defaults" file is a plausible first guess for "the" configuration, and the fixture brief has to correctly trigger the architecture-fog routing for the check to exercise the right workflow at all.
complexity_breakdown_sha256: 9253202e6e9be720b237f939c09350508a0898ee1f8a867c63c3c1fc927890c1
initial_state_or_fixture_spec: |
  Needs one fixture: a brief file, written by the oracle before verification (not part of the frozen repo state) and identical for every scoring run of this candidate, saved to a scratch path (FIXTURE_BRIEF above), containing exactly:

  # Repository Sensemaking Brief (fixture)

  ## 13. Machine-readable summary

  ```yaml
  primary_fog_type: architecture_fog
  recommended_workflow_id: architecture-implementation-workflow
  escalation_recommended: false
  ```

  Everything else is frozen-SHA repo state; only this one throwaway brief file is fixture content, and the agent never needs to see or create it — it is written directly by the oracle at verification time.
initial_state_or_fixture_spec_sha256: 8a4583fbdd55aca0c8460dd37f8343f7e17c8803e3eb4d82dd6eeb175646af72
qualification: |-
  ADMISSIBLE
