candidate_id: T1H-J3K
family: T1
complexity_level: HIGH
task_text: |
  This project's own maintainers, running this project's own bundled diagnosis-to-plan command-line tool directly against this very repository, want a new workflow available to that tool, selectable by id - not through any installed-library API, and not in any way a separate downstream team installing this project would ever see or benefit from just by that maintainer-side change alone.

  Independently of that, and requiring its own separate fix, picture a different team altogether - one running their own repository that has never had any part of this project copied into it: no skills directory of their own, no local registry override anywhere. The only way this project touches their world is as a dependency they've installed; their tooling pulls in this project's workflow registry object in code, hands it the root of their own repository, and pulls workflow definitions back out through that programmatic interface.

  Both audiences - this project's own maintainers using the bundled command-line tool against this repository, and that entirely separate downstream team using the installed library against their own bare repository - want the exact same new workflow, with the exact same content, made available to them.

  Add a new workflow with id `stale-example-audit-workflow`. Its first step must run the `docs-aligner` skill and produce an artifact named `domain_alignment_report`. Its second step must consume that artifact by running the `to-issues` skill, producing an artifact named `issue_list`.

  This workflow isn't one of the four workflows the command-line tool selects by default from a fog-type classification alone, so reaching it there requires an escalation-style routing recommendation inside the diagnostic brief the tool consumes.

  Make this workflow, with this exact two-step content, genuinely available to BOTH named audiences at once - the maintainer-side command-line tool run directly against this repository, and the downstream team's bare-repository library consumer - with no gaps for either one.
task_text_sha256: 9d69fd5c1ab56a4feaf460316074a585a3a5132d101a736f1ba954a86fa87e7f
oracle_spec: |
  Semantic outcome checked: (a) running this project's own bundled diagnosis-to-orchestration-plan command-line script, with its repo-root pointed at the patched clone itself, against a brief fixture that names `stale-example-audit-workflow` as the recommended workflow under escalation, must produce a plan whose rendered step table and machine-readable `workflow_steps` block show exactly two steps: a `docs-aligner` step with output artifact `domain_alignment_report`, followed by a `to-issues` step with input artifact `domain_alignment_report` and output artifact `issue_list`; and (b) constructing this project's workflow registry object for a target repository that contains none of the three known override-file locations must expose an entry for the same id with the same two steps.

  Why this is the right check: these two audiences are governed by two entirely separate, non-overlapping reads. The command-line tool hardcodes exactly one lookup location for workflow step definitions, regardless of `repo_root`'s value and regardless of anything in the separate, packaged-defaults file a library-style consumer loads. The bare downstream install, having none of the three override-file locations, never discovers that command-line-tool-only file at all - the registry object's override search only ever looks *inside the repository it is pointed at*, never inside this project's own checkout - so it only ever sees the packaged-defaults file, loaded unconditionally by the registry object's own constructor. Because `stale-example-audit-workflow` is a brand-new id with no prior entry anywhere in either file, there is no override-vs-defaults merge to lean on for either audience: an edit placed in only one of the two files satisfies only the audience whose read path passes through that file, and has zero effect on the other. Satisfying both named audiences at once genuinely requires writing the same two-step content into both files independently.

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

  rows_2 = [line for line in text.splitlines() if line.strip().startswith("|") and " to-issues " in line]
  assert len(rows_2) == 1, f"FAIL: expected exactly one to-issues row, found {len(rows_2)}"
  assert "domain_alignment_report" in rows_2[0] and "issue_list" in rows_2[0], f"FAIL: to-issues row missing artifacts: {rows_2[0]!r}"

  lines = text.splitlines()
  found_docs_aligner_block = False
  for i, line in enumerate(lines):
      if line.strip() == "skill: docs-aligner":
          block = "\n".join(lines[i:i + 6])
          assert "output_artifact: domain_alignment_report" in block, f"FAIL: yaml block for docs-aligner missing output artifact: {block!r}"
          found_docs_aligner_block = True
          break
  assert found_docs_aligner_block, "FAIL: no 'skill: docs-aligner' line found in machine-readable block"

  found_to_issues_block = False
  for i, line in enumerate(lines):
      if line.strip() == "skill: to-issues":
          block = "\n".join(lines[i:i + 6])
          assert "input_artifact: domain_alignment_report" in block, f"FAIL: yaml block for to-issues missing input artifact: {block!r}"
          assert "output_artifact: issue_list" in block, f"FAIL: yaml block for to-issues missing output artifact: {block!r}"
          found_to_issues_block = True
          break
  assert found_to_issues_block, "FAIL: no 'skill: to-issues' line found in machine-readable block"

  print("PASS: CLI check")
  ```

  ```python
  import sys, tempfile
  from pathlib import Path

  sys.path.insert(0, str(Path(CLONE_DIR) / "src"))
  from sensemaking_skills.registry import WorkflowRegistry

  with tempfile.TemporaryDirectory() as bare_repo:
      reg = WorkflowRegistry(target_repo=Path(bare_repo))
      wf = reg.get_workflow("stale-example-audit-workflow")

      assert wf is not None, "FAIL: not visible to a bare-target-repo library consumer"
      steps = wf.get("steps", [])
      assert len(steps) == 2, f"FAIL: expected 2 steps, got {len(steps)}"
      assert steps[0].get("skill") == "docs-aligner"
      assert steps[0].get("output_artifact") == "domain_alignment_report"
      assert steps[1].get("skill") == "to-issues"
      assert steps[1].get("input_artifact") == "domain_alignment_report"
      assert steps[1].get("output_artifact") == "issue_list"
      print("PASS: bare-downstream check")
  ```

  PASS iff the command-line tool exits 0 (no `ERROR:` output) and every assertion above holds, in both snippets.

  Negative cases (must be rejected):
  - An agent that adds `stale-example-audit-workflow` only to the file the command-line tool reads: the CLI check passes, but the bare-downstream check fails outright - `wf` comes back `None`, since a genuinely bare repository never discovers that file (the override search only looks inside the repository it is pointed at, never inside this project's own checkout) and the packaged-defaults file, the only thing it does load, has no entry for this id at all.
  - An agent that adds it only to the packaged-defaults file: the bare-downstream check passes, but the CLI check fails - the command-line script never reads that file under any circumstances, prints `ERROR: No steps found for workflow: stale-example-audit-workflow` to stderr, and exits 1.
  - An agent that reasons "the registry object merges an override on top of defaults, so if I add it to the file this repository's own override search would find, that should cover everything": this covers the command-line tool and this repository examining itself, but still leaves the bare-downstream audience unsatisfied, since a genuinely bare repository has no override file of its own to discover in the first place - the merge only ever happens inside a target_repo that already contains one of the three candidate override files, which this scenario's downstream team's repository, by definition, does not.
oracle_spec_sha256: 6da081e08069a9f9f554de90813478c335f046e1506b51fad97a4aa31db68931
complexity_breakdown: |
  HIGH because satisfying the task requires combining T1 mechanism-routing reasoning with genuine multi-consumer coupling, not a single lookup: (1) recognize that "this project's own bundled command-line tool, run directly against this repository" and "a downstream team's installed-library consumer, pointed at their own bare repository" are two entirely disjoint read paths - one hardcoded and override-independent, the other unconditionally defaults-based and override-search-based but only ever searching *inside the target it's pointed at*; (2) recognize that because the workflow id is brand new, there is no existing entry anywhere for the override-vs-defaults merge to help with - satisfying one audience via one file has literally zero effect on the other, so both files need the same two-step content written into them independently, not merged.

  Not HIGH-by-obscurity: this traces directly to the command-line tool's single hardcoded read path and the registry object's target-repo-scoped override search, both real code, not incidental complexity. Not MEDIUM: a MEDIUM version of this substrate asks "which one file governs this one consumer"; this candidate names two differently-scoped consumers at once and requires recognizing that no merge or override relationship connects their two read paths for a brand-new id, so genuinely separate edits to two files are both required, not merely tempting.
complexity_breakdown_sha256: fa1ddd158e2d971803e02d363e170f0c967525215aec88c8a9854231014e333f
initial_state_or_fixture_spec: |
  Needs one fixture, written by the oracle before verification (not part of the frozen repo state) and identical for every scoring run of this candidate: a brief file saved to a scratch path (FIXTURE_BRIEF above), containing exactly:

  # Repository Sensemaking Brief (fixture)

  ## 13. Machine-readable summary

  ```yaml
  primary_fog_type: docs_fog
  recommended_workflow_id: stale-example-audit-workflow
  escalation_recommended: true
  ```

  The bare-target-repo check additionally needs a throwaway empty target-repo directory (no files at all), created and discarded by the oracle at verification time. The agent never needs to see or create either fixture - both are constructed directly by the oracle at verification time. Everything else is frozen SHA repo state.
initial_state_or_fixture_spec_sha256: 8b625372977715fae77d5af05b29c63431f456ca65c0893c1c7b54cd888c5e8c
qualification: |-
  ADMISSIBLE
