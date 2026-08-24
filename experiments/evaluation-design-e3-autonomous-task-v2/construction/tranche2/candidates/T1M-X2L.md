candidate_id: T1M-X2L
family: T1
complexity_level: MEDIUM
task_text: |
  This project's own bundled diagnosis-to-plan command-line tool, run directly against this repository, classifies a documentation-focused diagnosis and today routes it, by default, straight to an existing implementation workflow already built for documentation problems - no escalation routing needed to reach it.

  That workflow's specification step - the one that defines what the documentation work should actually cover - currently describes its job only as defining structure and coverage.

  Change that step's description so it also explicitly calls out defining accessibility requirements. The next time someone runs this project's own bundled command-line tool directly against this repository, on a documentation-focused diagnosis, both the printed step table and the machine-readable plan block beneath it must show the updated description text for that step.
task_text_sha256: fb5083235e521363e8d788d2f94be7dbce056a8c454fedb8b0a0668bcf86ab6e
oracle_spec: |
  Semantic outcome checked: running this project's own bundled diagnosis-to-orchestration-plan command-line script, with its repo-root pointed at the patched clone itself, against a brief fixture classifying the problem as a documentation issue (default routing, no escalation), must produce a plan whose rendered step table row (and machine-readable `workflow_steps` block) for the specification step of the documentation-focused implementation workflow contains description text mentioning accessibility requirements, where the original description text ("Documentation specification - define structure and coverage") did not.

  Why this is the right check: the described actor - this project's own bundled command-line tool, run directly against this repository - hardcodes exactly one lookup location for workflow step definitions, regardless of `repo_root`'s value and regardless of anything in the separate, packaged-defaults file a different, library-style consumer would load instead. The documentation-focused implementation workflow here is *not* a single-file-only id like the two exceptions this substrate is known for - at the frozen SHA it exists field-for-field identical in both files, including this exact step's current description text. That is precisely the trap: an agent can open the packaged-defaults file, find a real, well-formed, editable entry for this exact workflow and this exact step, make the requested change there, and have every part of that edit be individually correct - yet it still has zero effect on this actor, because that actor is never the one that reads that file. Unlike a case where the "wrong" file has no entry at all to edit, here the wrong-route edit is fully expressible and fully plausible; it is simply invisible to the specific consumer the task names.

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
  phrase_re = re.compile(r"accessibility", re.IGNORECASE)

  # Row for the specification (to-prd) step in the markdown table:
  table_rows = [line for line in text.splitlines() if line.strip().startswith("|") and " to-prd " in line]
  assert len(table_rows) == 1, f"FAIL: expected exactly one to-prd table row, found {len(table_rows)}"
  assert phrase_re.search(table_rows[0]), f"FAIL: table row does not mention accessibility: {table_rows[0]!r}"

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

  Negative case (must be rejected): an agent that edits the step's description only inside the separate, packaged-defaults file - a real, pre-existing entry there, correctly and completely edited - fails both assertions. The standalone command-line script never opens that file under any circumstances; it hardcodes a single different lookup path and reads only that. The generated plan still shows the original, unedited description text ("Documentation specification - define structure and coverage"), with no mention of accessibility, so `phrase_re.search(...)` returns `None` in both places and both asserts fail. A second plausible-but-wrong route: editing the entry under a `.sensemaking/workflow-registry.yaml` override inside the clone - a real override path this project's separate registry *object* does search, but one the standalone command-line script never consults at all - produces the identical FAIL.
oracle_spec_sha256: 553839141533d44ba2afc7da72d7175e3e140cd38822ccd2cbd7d5e0f4a0ae26
complexity_breakdown: |
  Two reasoning hops: (1) recognize the actor in the task - "this project's own bundled command-line tool, run directly against this repository" on a documentation-focused, default-routed diagnosis - is the standalone script path, which hardcodes exactly one workflow-definitions file regardless of `repo_root`, not the separate registry object with its multi-location override search; (2) resist treating this as a shared-id merge-precedence question - the workflow is a shared id, identical today in both files, but that fact is a distractor here, not the crux: the actor's single hardcoded read path is unconditional and does not care whether the id is shared, new, or single-file-only, so the only thing that matters is which one file that actor reads, and the edit must land there regardless of what the other, equally real copy says.

  Not HIGH: no negative "must not leak to a third audience" requirement, no chained artifacts, no combination with a second unrelated kind of check - once the actor is correctly identified, there is exactly one file that could possibly work, full stop. Not trivial: the task never names the file, the workflow, or the script; the packaged-defaults file offers a real, completely well-formed, easy-to-mistake-for-sufficient edit target (unlike a case where the wrong file has no matching entry at all to tempt an agent into stopping there); and the fixture brief has to correctly trigger the documentation-fog default routing for the check to exercise the right workflow.
complexity_breakdown_sha256: 7f89219156514a1aa599f221b6a9cd288d349022974f17f01a3efdc759958088
initial_state_or_fixture_spec: |
  Needs one fixture: a brief file, written by the oracle before verification (not part of the frozen repo state) and identical for every scoring run of this candidate, saved to a scratch path (FIXTURE_BRIEF above), containing exactly:

  # Repository Sensemaking Brief (fixture)

  ## 13. Machine-readable summary

  ```yaml
  primary_fog_type: docs_fog
  recommended_workflow_id: docs-implementation-workflow
  escalation_recommended: false
  ```

  Everything else is frozen-SHA repo state; only this one throwaway brief file is fixture content, and the agent never needs to see or create it - it is written directly by the oracle at verification time.
initial_state_or_fixture_spec_sha256: 16b73af5e852f97ecedde41422484c17bb769a405210bf912659cf76e92dd8be
qualification: |-
  ADMISSIBLE
