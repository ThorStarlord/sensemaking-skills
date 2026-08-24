# T1 Pilot Oracle — Hidden (evaluator-only)

## Verified mechanism (investigated at frozen SHA `0ffb564b`, not assumed)

> **Re-freeze revalidation (a7b957d):** Substrate re-verified at current main `a7b957d`: the load-bearing `defaults/` vs `skills/` registry divergence still holds (defaults = 20 workflows, a strict subset of the 23 in `skills/`; a bare-target `WorkflowRegistry` still sees only `defaults/` content). The defaults-count invariant `len(ids) == 21` (20 defaults + the agent's new entry) remains correct; this oracle is base-independent (no `git diff` against a frozen SHA). Full detail in `RE-FREEZE-PROVENANCE.md`.

Two files both nominally called "the workflow registry" exist in this repo:

- `skills/workflow-planner/references/workflow-registry.yaml` (979 lines at
  frozen SHA, 22 workflow entries)
- `src/sensemaking_skills/defaults/workflow-registry.yaml` (885 lines at
  frozen SHA, 20 workflow entries — a strict subset by ID of the first file)

Read at frozen SHA:

- `scripts/workflow-planner.py:28` — `load_workflow_registry()` hardcodes
  `Path(repo_root) / "skills" / "workflow-planner" / "references" /
  "workflow-registry.yaml"`. It **never** reads
  `defaults/workflow-registry.yaml`, under any circumstance.
- `src/sensemaking_skills/registry.py`'s `WorkflowRegistry.__init__` (lines
  12-100): `_load_package_defaults()` **always** loads
  `src/sensemaking_skills/defaults/workflow-registry.yaml` first (line 48).
  Then `_load_user_registry()` (lines 64-89) checks, in order, whether
  `target_repo/skills/workflow-planner/references/workflow-registry.yaml`,
  `target_repo/skills/workflow-orchestrator/references/workflow-registry.yaml`,
  or `target_repo/.sensemaking/workflow-registry.yaml` exists; the first one
  found is loaded and merged on top of the defaults via `_merge_workflows`
  (line 91-100), which does `self._workflows[workflow_id] = workflow` per
  entry — i.e. entries in the user registry **overwrite** same-ID defaults
  entries and are **added** if the ID is new, but defaults entries whose ID
  is absent from the user registry **survive untouched**.

Consequence, confirmed by tracing the code (not by running it against a
constructed case — the sanity check in Task 1 Step 5 does that): a workflow
added **only** to `defaults/workflow-registry.yaml` is visible via
`WorkflowRegistry(target_repo=<any repo without its own override file>)`
but invisible to `scripts/workflow-planner.py` under all circumstances, and
invisible to `WorkflowRegistry(target_repo=<a repo that does have its own
skills/workflow-planner/references/workflow-registry.yaml, unless that
file also defines the same ID>)` — because in that case the user registry
is loaded and, for IDs it doesn't define, defaults still show through, so
it would actually still be visible there too. The genuinely selective case
is a **bare target repo with none of the three override paths present** —
that is the only place a defaults-only entry is visible and a
skills-copy-only entry is not (a skills-copy-only entry is invisible to any
`WorkflowRegistry` instantiated against a *different* bare repo, since nothing
copies it into that repo's tree or into defaults).

The task requires "available out of the box... even before the target repo
has its own scaffolding" — this is precisely the bare-target-repo case, so
the semantically correct edit location is `src/sensemaking_skills/defaults/workflow-registry.yaml`.
Editing only `skills/workflow-planner/references/workflow-registry.yaml`
satisfies this repo's own dogfood CLI and this repo's own `WorkflowRegistry`
merge, but does **not** satisfy the stated scenario, because that file
travels with *this* repo's tree, not with the installed package.

## Oracle procedure

Run against the agent's final repository state (a patched clone at frozen
SHA):

```python
import sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(CLONE_DIR) / "src"))
from sensemaking_skills.registry import WorkflowRegistry

# 1. POSITIVE CHECK — bare target repo, no scaffolding of its own at all.
with tempfile.TemporaryDirectory() as bare_repo:
    reg = WorkflowRegistry(target_repo=Path(bare_repo))
    wf = reg.get_workflow("duplicate-detection-workflow")
    assert wf is not None, "FAIL: not visible to a bare-target WorkflowRegistry -- defaults/workflow-registry.yaml was not edited (or was edited incorrectly)"
    assert wf.get("display_name") == "Duplicate Detection Workflow"
    assert wf.get("purpose", "").startswith("Scan a repository for duplicated logic")
    steps = wf.get("steps", [])
    assert len(steps) == 1
    assert steps[0].get("skill") == "repo-sensemaker"
    assert steps[0].get("gate") == "review_diagnosis"
    assert steps[0].get("output_artifact") == "repository_sensemaking_brief"
    assert wf.get("allowed_execution_modes") == ["plan_only", "guided_execution"]

# 2. Confirm the entry actually lives in defaults/workflow-registry.yaml on
#    disk (not merely reachable via some other accidental path), and that no
#    unrelated existing entry in that file was removed or renamed.
import yaml
defaults_path = Path(CLONE_DIR) / "src" / "sensemaking_skills" / "defaults" / "workflow-registry.yaml"
data = yaml.safe_load(defaults_path.read_text(encoding="utf-8"))
ids = [w["id"] for w in data["workflows"]]
assert "duplicate-detection-workflow" in ids
assert len(ids) == 21, f"expected the 20 original defaults entries plus 1 new one, got {len(ids)}"
```

## Route-independent framing

The check is on the **merged runtime view** (`WorkflowRegistry` against a
bare target repo), not on "did the agent touch file X" — an agent could in
principle satisfy this via any mechanism that makes
`defaults/workflow-registry.yaml` contain the entry (e.g. writing a small
script that appends it, generating it programmatically, or a direct edit);
all pass equally. What fails is landing the change somewhere that a
bare-target `WorkflowRegistry` never reads.

## Negative case (must be rejected)

An agent that adds `duplicate-detection-workflow` **only** to
`skills/workflow-planner/references/workflow-registry.yaml` (the more
prominently-referenced, docs-heavy file, and the one this repo's own CLI
tool reads) fails Check 1 above: `WorkflowRegistry(target_repo=<bare temp
dir>)` returns `None` for that ID, because a bare repo has none of the three
override paths and therefore only ever sees `defaults/workflow-registry.yaml`
content. This is the plausible wrong-route failure this pilot exists to
detect.

## Qualification

- Two or more plausible mechanisms: **yes** — `skills/workflow-planner/references/workflow-registry.yaml`
  (this repo's own copy, read directly by `workflow-planner.py`) vs.
  `src/sensemaking_skills/defaults/workflow-registry.yaml` (the packaged
  defaults, read by `WorkflowRegistry`).
- Wrong route genuinely plausible: **yes** — the `skills/` copy is the one
  most visibly documented and is what this repo's own tooling reads; an
  agent working inside this repo has every surface reason to reach for it
  first.
- Repo evidence discriminates: **yes** — traced directly in
  `registry.py`/`workflow-planner.py` source, not asserted.
- Oracle is route-independent: **yes** — checks the merged runtime view via
  the actual `WorkflowRegistry` class against a bare target, not which file
  was touched.
- No environment/network constraint forces the route: **yes** — purely a
  local file edit + local Python import.
- Task doesn't name the answer: **yes** — task text never names either file
  path or either Python symbol.

**ADMISSIBLE**

## Sanity check (Task 1 Step 5)

The oracle procedure above is directly executable: `python -c "<snippet>"`
against a clone of this repo with `src/` on `sys.path`, requires only the
stdlib plus `PyYAML` (already a repo dependency, confirmed available in
this worktree: `PyYAML 6.0.3`). No additional fixture construction needed
beyond the clone itself.
