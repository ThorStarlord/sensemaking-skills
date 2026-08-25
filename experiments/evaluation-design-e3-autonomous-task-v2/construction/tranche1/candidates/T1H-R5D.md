candidate_id: T1H-R5D
family: T1
complexity_level: HIGH
task_text: |
  This project already ships one prominent file that defines workflow steps — the file this repository's own tooling actually reads, and the same file any repository can copy into itself to customize workflows locally. Separately, this project's documentation also mentions a second, lighter-weight project-local override location, meant for a repository's own small local customizations, deliberately kept distinct from that first, more prominent file.

  A teammate suggests: "Let's add a brand-new workflow through that lighter-weight, project-local override location instead of touching the big prominent file — that's what it's there for."

  Before following that suggestion, work out whether it will actually achieve the goal below for this repository, as this repository exists today, and then make whatever change actually works — using the lighter-weight location only if it will actually take effect here.

  Goal: add a new workflow with id `dependency-drift-triage-workflow`. Its first step must run the `repo-sensemaker` skill and produce an artifact named `repository_sensemaking_brief`. Its second step must consume that artifact by running the `to-issues` skill, producing an artifact named `issue_list`.

  This new workflow must become visible in BOTH of the following, for this repository specifically:
  1. This project's own bundled diagnosis-to-plan command-line tool, run directly against this repository, when asked to plan for this exact workflow (via an escalation-style routing recommendation, since this isn't one of the four workflows this tool selects by default from a fog-type classification alone).
  2. This project's own workflow object, pointed directly at this very repository (its own checkout).

  At the same time, this new workflow must NOT become visible to a separate downstream team's install — one with no copy of any part of this project inside their own repository at all. Their install must behave exactly as if this workflow doesn't exist, both before and after your change.
task_text_sha256: 7a3926cbb8aa61eb8b489e50fc008b1b6b00960cc2251a8a7fda7d5e8c77c7e0
oracle_spec: |
  Semantic outcome checked: constructing this project's workflow registry object with the target repository pointed at this repository itself (self-reference) must expose a `dependency-drift-triage-workflow` entry with the two steps specified; running this project's own bundled diagnosis-to-plan command-line tool directly against this repository, asked (via escalation) to plan for that same workflow id, must print the same two steps; and constructing the registry object against a genuinely bare, unrelated target repository (no override files of any kind) must NOT expose that workflow id at all.

  Why this is the right check: this repository's own bundled command-line tool has exactly one hardcoded file it will ever read, regardless of target_repo — the same prominent file the task text refers to. Separately, this project's registry object searches a short, ordered list of candidate override locations inside whatever target_repo it is pointed at, and the search stops at the FIRST one found to exist on disk — it does not continue on to check the others, and does not combine multiple existing override files into one merged view. Because this repository's own prominent file already exists inside itself, this repository's self-referencing registry object will always find and use it first; a hypothetical lighter-weight project-local override file placed inside this same repository would exist on disk but would never even be opened, because the search returns as soon as the prominent file is found to exist. So there is exactly one file inside this repository that can possibly make the new workflow visible to either the command-line tool or the self-referencing registry object: the same prominent file both routes actually consult (directly for the command-line tool; discovered-first for self-reference). The negative requirement additionally rules out placing the definition in this project's own packaged defaults instead, since that file is loaded unconditionally for every target_repo, including a genuinely bare one with no override files — which would make the workflow leak to the exact audience the task says must not see it.

  Exact commands (run against a patched clone of the frozen-SHA repo, CLONE_DIR, with the fixture brief written to FIXTURE_BRIEF and a scratch output path OUT_PATH):

  ```python
  import sys, tempfile
  from pathlib import Path

  sys.path.insert(0, str(Path(CLONE_DIR) / "src"))
  from sensemaking_skills.registry import WorkflowRegistry

  # Check 2: self-reference
  reg_self = WorkflowRegistry(target_repo=Path(CLONE_DIR))
  wf = reg_self.get_workflow("dependency-drift-triage-workflow")
  assert wf is not None, "FAIL: not visible to this repository's own self-referencing registry object"
  steps = wf.get("steps", [])
  assert len(steps) == 2, f"FAIL: expected 2 steps, got {len(steps)}"
  assert steps[0].get("skill") == "repo-sensemaker"
  assert steps[0].get("output_artifact") == "repository_sensemaking_brief"
  assert steps[1].get("skill") == "to-issues"
  assert steps[1].get("input_artifact") == "repository_sensemaking_brief"
  assert steps[1].get("output_artifact") == "issue_list"

  # Check 3: bare downstream repo must NOT see it
  with tempfile.TemporaryDirectory() as bare_repo:
      reg_bare = WorkflowRegistry(target_repo=Path(bare_repo))
      assert reg_bare.get_workflow("dependency-drift-triage-workflow") is None, "FAIL: leaked to a bare downstream install"

  print("PASS: registry checks")
  ```

  ```bash
  cd CLONE_DIR
  python scripts/workflow-planner.py FIXTURE_BRIEF --repo-root . -o OUT_PATH
  echo "exit code: $?"
  ```

  ```python
  from pathlib import Path
  text = Path("OUT_PATH").read_text(encoding="utf-8")

  # Check 1: this repository's own bundled command-line tool
  rows = [line for line in text.splitlines() if line.strip().startswith("|") and " repo-sensemaker " in line]
  assert len(rows) == 1, f"FAIL: expected one repo-sensemaker row, got {len(rows)}"
  assert "repository_sensemaking_brief" in rows[0], f"FAIL: row missing output artifact: {rows[0]!r}"

  rows2 = [line for line in text.splitlines() if line.strip().startswith("|") and " to-issues " in line]
  assert len(rows2) == 1, f"FAIL: expected one to-issues row, got {len(rows2)}"
  assert "issue_list" in rows2[0], f"FAIL: row missing output artifact: {rows2[0]!r}"

  print("PASS: CLI check")
  ```

  PASS iff the command-line tool exits 0 (no `ERROR:` output) and every assertion above holds, including the bare-repo negative check.

  Negative cases (must be rejected):
  - An agent that creates only a fresh lighter-weight project-local override file inside the clone (the location the teammate suggested) containing the new workflow, and touches nothing else: the command-line-tool check fails outright, since that tool never reads that location under any circumstances; the self-reference check also fails, since this repository's prominent file already exists and is found first by the search, so the lighter-weight file is never even opened.
  - An agent that adds the new workflow to this project's packaged defaults file instead: the command-line-tool check fails (it never reads defaults); the self-reference check happens to pass (defaults are always loaded as the base); but the bare-repo negative check fails, since a genuinely bare downstream install with no override files of its own would now incorrectly see this workflow too.
  - Correct route: add the new workflow to the one prominent file this repository already has. This satisfies the command-line-tool check (its only read path) and the self-reference check (found first by the search), while the bare-repo negative check remains satisfied by construction, since that file lives inside this repository and is never consulted for a bare, unrelated target_repo.
oracle_spec_sha256: b8f682ba890c1e2e3e2d1d7009a370e88ab799468dcf1c6ad90bc63a1dd62e69
complexity_breakdown: |
  HIGH because the correct answer requires tracing a genuine chain of more than one condition, not a single file choice: (1) recognizing that this project's registry object searches an ORDERED list of candidate override locations inside whatever target_repo it is pointed at, and stops at the first one found to exist — it does not read every candidate location that happens to exist, and does not merge multiple found override files together; (2) recognizing that because this repository already contains the first (most prominent) candidate location, ANY other override location placed inside this same repository is entirely inert for self-reference, regardless of its content, purely because of search order — this is not simply "the override beats the default," it is "only the first-found override is ever consulted at all"; (3) combining that with the override-vs-add distinction to also rule out the packaged-defaults route, which would satisfy the self-reference check but would violate the explicit negative requirement that a bare, unrelated downstream install must not see this workflow at all.

  Not HIGH-by-obscurity: every step traces to the literal loop-and-early-return structure of the override-file search and the separate, always-unconditional loading of packaged defaults, not to incidental formatting. Not MEDIUM: a MEDIUM version of this substrate asks "which of two files governs this consumer"; this candidate additionally requires reasoning about a third candidate location's search-order priority and about ruling out a route that would otherwise look like a clean, uniform fix.
complexity_breakdown_sha256: 5f58107ee64b597ceb1abde30a454d51f74a7facaed0877065b9a45ba2fb434d
initial_state_or_fixture_spec: |
  Two fixtures, both created and consumed only by the oracle at verification time, never by the agent:

  1. A throwaway empty target-repo directory (no files at all), for the bare-downstream-negative check, created and discarded per verification run.
  2. A brief fixture file, saved to a scratch path (FIXTURE_BRIEF above), containing exactly:

  # Repository Sensemaking Brief (fixture)

  ## 13. Machine-readable summary

  ```yaml
  primary_fog_type: product_fog
  recommended_workflow_id: dependency-drift-triage-workflow
  escalation_recommended: true
  ```

  Everything else is frozen-SHA repo state; only these two throwaway items are fixture content.
initial_state_or_fixture_spec_sha256: 1649bbed8a12d219d258eade55cc9d3b2f13e6e94c23060aa03204d14cf47622
qualification: |
  ADMISSIBLE
