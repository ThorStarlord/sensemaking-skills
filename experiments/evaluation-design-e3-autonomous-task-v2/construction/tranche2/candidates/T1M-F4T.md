candidate_id: T1M-F4T
family: T1
complexity_level: MEDIUM
task_text: |
  This project's own maintainers use this project's own bundled diagnosis-to-plan command-line tool directly against this very repository as part of their day-to-day workflow selection - not through any installed-library API, and not in any way a separate downstream team installing this project would ever see or benefit from.

  They want a new workflow made available to that command-line tool, selectable by id. This workflow isn't one of the four workflows the tool selects by default from a fog-type classification alone, so reaching it in a plan requires an escalation-style routing recommendation inside the diagnostic brief the tool consumes.

  Add a new workflow with id `naming-consistency-audit-workflow`. Its first step must run the `docs-aligner` skill and produce an artifact named `domain_alignment_report`. Its second step must consume that artifact by running the `handoff` skill, producing an artifact named `session_summary`.

  Make this new workflow actually show up - with both steps rendered correctly, including their artifacts - the next time someone runs this project's own bundled command-line tool directly against this repository and asks it to plan for this exact workflow id.
task_text_sha256: b9dcd9d11e3d080473e22e5a3124fbe34be65cbe169a0f7bda6e46e513d61d1e
oracle_spec: |
  Semantic outcome checked: running this project's own bundled diagnosis-to-orchestration-plan command-line script, with its repo-root pointed at the patched clone itself, against a brief fixture that names `naming-consistency-audit-workflow` as the recommended workflow under escalation, must produce a plan whose rendered step table (and machine-readable `workflow_steps` block beneath it) shows exactly two steps: a `docs-aligner` step with output artifact `domain_alignment_report`, followed by a `handoff` step with input artifact `domain_alignment_report` and output artifact `session_summary`.

  Why this is the right check: the described actor - this project's own bundled command-line tool, run directly against this repository - hardcodes exactly one lookup location for workflow step definitions, regardless of `repo_root`'s value and regardless of anything in the separate, packaged-defaults file that a different, library-style consumer would load. Because `naming-consistency-audit-workflow` is a brand-new id with no prior entry anywhere, there is no shared-id merge or precedence question at all here - there is exactly one file this tool will ever open, and the new entry either lives there or the tool cannot see it, full stop.

  Exact commands (run against a patched clone of the frozen-SHA repo, CLONE_DIR, with the fixture brief written to FIXTURE_BRIEF and a scratch output path OUT_PATH):

  ```bash
  cd CLONE_DIR
  python scripts/workflow-planner.py FIXTURE_BRIEF --repo-root . -o OUT_PATH
  echo "exit code: $?"
  ```

  ```python
  from pathlib import Path

  text = Path("OUT_PATH").read_text(encoding="utf-8")

  rows_1 = [line for line in text.splitlines() if line.strip().startswith("|") and " docs-aligner " in line]
  assert len(rows_1) == 1, f"FAIL: expected exactly one docs-aligner row, found {len(rows_1)}"
  assert "domain_alignment_report" in rows_1[0], f"FAIL: docs-aligner row missing output artifact: {rows_1[0]!r}"

  rows_2 = [line for line in text.splitlines() if line.strip().startswith("|") and " handoff " in line]
  assert len(rows_2) == 1, f"FAIL: expected exactly one handoff row, found {len(rows_2)}"
  assert "domain_alignment_report" in rows_2[0] and "session_summary" in rows_2[0], f"FAIL: handoff row missing artifacts: {rows_2[0]!r}"

  lines = text.splitlines()
  found_docs_aligner_block = False
  for i, line in enumerate(lines):
      if line.strip() == "skill: docs-aligner":
          block = "\n".join(lines[i:i + 6])
          assert "output_artifact: domain_alignment_report" in block, f"FAIL: yaml block for docs-aligner missing output artifact: {block!r}"
          found_docs_aligner_block = True
          break
  assert found_docs_aligner_block, "FAIL: no 'skill: docs-aligner' line found in machine-readable block"

  found_handoff_block = False
  for i, line in enumerate(lines):
      if line.strip() == "skill: handoff":
          block = "\n".join(lines[i:i + 6])
          assert "input_artifact: domain_alignment_report" in block, f"FAIL: yaml block for handoff missing input artifact: {block!r}"
          assert "output_artifact: session_summary" in block, f"FAIL: yaml block for handoff missing output artifact: {block!r}"
          found_handoff_block = True
          break
  assert found_handoff_block, "FAIL: no 'skill: handoff' line found in machine-readable block"

  print("PASS")
  ```

  PASS iff the command-line tool exits 0 (no `ERROR:` output, per its own error-prefix convention) and every assertion above holds.

  Negative case (must be rejected): an agent that adds `naming-consistency-audit-workflow` only to the separate, packaged-defaults file - the one that sounds more like "the" canonical library configuration, and the one a library-style consumer would rely on - produces no visible effect for this check at all. The command-line script never reads that file under any circumstances; `get_workflow_steps` for the new id against the file the script actually loads returns an empty list, and the script prints `ERROR: No steps found for workflow: naming-consistency-audit-workflow` to stderr and exits 1, failing the exit-code requirement outright.
oracle_spec_sha256: 9ed2308a5147d52bbc16a08f2c2b24f38e95c3d9a320c2d666228542caab6819
complexity_breakdown: |
  Two reasoning hops: (1) recognize the actor in the task - "this project's own bundled command-line tool, run directly against this repository" - is the standalone script path, which hardcodes exactly one workflow-definitions file regardless of `repo_root`, not the separate registry object with its multi-location override search; (2) recognize that because the workflow id is brand new (not an existing id living in either file today), there is no merge-order or precedence question to resolve - the only thing that matters is placing the new entry in the one file that actor actually reads.

  Not HIGH: no shared-id merge precedence, no requirement to simultaneously satisfy a second, differently-scoped audience, no negative "must not leak elsewhere" check layered on top. Not trivial: the task never names the file or the script, the more prominently-labeled "defaults" file is a plausible first guess for where a project's canonical workflow list lives, and the fixture brief has to correctly trigger escalation-based routing for the check to exercise the new workflow at all (it is not one of the four fog-mapped defaults).
complexity_breakdown_sha256: 85782c92301220b94eaea10cfc921f82c198988a1559f1f5fc98a23f50297fc7
initial_state_or_fixture_spec: |
  Needs one fixture: a brief file, written by the oracle before verification (not part of the frozen repo state) and identical for every scoring run of this candidate, saved to a scratch path (FIXTURE_BRIEF above), containing exactly:

  # Repository Sensemaking Brief (fixture)

  ## 13. Machine-readable summary

  ```yaml
  primary_fog_type: docs_fog
  recommended_workflow_id: naming-consistency-audit-workflow
  escalation_recommended: true
  ```

  Everything else is frozen-SHA repo state; only this one throwaway brief file is fixture content, and the agent never needs to see or create it - it is written directly by the oracle at verification time.
initial_state_or_fixture_spec_sha256: fb43748d1f32a1c0b7cc84cdd31c4801bcc44a78b03ed86944197cc065c041d0
qualification: |
  ADMISSIBLE
