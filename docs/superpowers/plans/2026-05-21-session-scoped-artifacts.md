# Session-Scoped Artifact Isolation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every workflow run's artifacts go into its own numbered session directory (`artifacts/NN-orchestration-run/`), preventing stale files from previous runs.

**Architecture:** Single responsibility: `_resolve_artifact_path()` prepends the session directory derived from `self.intent_path`. Default output paths (`plan_out`, `log_dir`) also use the session dir. No contract changes needed.

**Tech Stack:** Python 3.14, `workflow-runtime.py` (~1896 lines), existing tests: `tests/test_dynamic_path_resolution.py` (6 pass).

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `scripts/workflow-runtime.py` | Modify | `OrchestrationRunner` class — add `artifact_session_dir`, update `_resolve_artifact_path`, update default paths |
| `tests/test_dynamic_path_resolution.py` | Modify | Add new test cases for session-scoped resolution |

---

### Task 1: Add artifact_session_dir to OrchestrationRunner

**Files:**
- Modify: `scripts/workflow-runtime.py` (constructor + `_create_user_intent_artifact`)

- [ ] **Step 1: Add `artifact_session_dir` to `__init__`**

Locate the constructor (~line 192) and add one line inside `__init__`:

```python
# Add after: self.intent_path: str | None = None
self.artifact_session_dir: str | None = None
```

- [ ] **Step 2: Set `artifact_session_dir` in `_create_user_intent_artifact`**

In `_create_user_intent_artifact` (~line 267), after the intent artifact is successfully created and the path is known, add the session dir assignment. Find the existing `print(f"[OK] Created user intent artifact: ...")` line (~line 313) and add the `artifact_session_dir` assignment just before it:

```python
        try:
            with open(intent_path, "w", encoding="utf-8") as f:
                f.write("# User Intent\n\n")
                f.write("---\n")
                import yaml
                yaml.dump(intent_yaml, f, default_flow_style=False)
                f.write("---\n")

            # ADD: Store session directory for artifact path resolution
            self.artifact_session_dir = os.path.dirname(intent_path)
            print(f"[OK] Created user intent artifact: {os.path.relpath(intent_path, self.repo_root)}")
```

---

### Task 2: Session-scope _resolve_artifact_path()

**Files:**
- Modify: `scripts/workflow-runtime.py` (method `_resolve_artifact_path`)

- [ ] **Step 1: Update `_resolve_artifact_path` to scope under session dir**

Replace the current `_resolve_artifact_path` method. The key change: after resolving the base path (from contract or fallback), if `artifact_session_dir` is set and the resolved path is under `artifacts/`, reparent it under the session directory.

Open and replace the method at line 871:

```python
    def _resolve_artifact_path(self, artifact_id: str) -> str:
        """Resolve the file path for an artifact, scoped to session directory if set."""
        # Check/load contracts dynamically
        contracts = self.contracts
        if not contracts:
            try:
                contracts = load_artifact_contracts(self.repo_root)
            except Exception as e:
                print(f"  ~ Failed to load contracts dynamically: {e}")
                contracts = None

        if contracts:
            artifacts_list = contracts.get("artifacts", [])
            contract = next((a for a in artifacts_list if a.get("id") == artifact_id), None)
            if contract and "path" in contract:
                path_template = contract["path"]
                try:
                    resolved_path = path_template.format(
                        workflow_id=self.workflow_id,
                        session_id=self.session_id
                    )
                except Exception:
                    resolved_path = path_template.replace("{workflow_id}", self.workflow_id).replace("{session_id}", self.session_id)
                resolved = os.path.join(self.repo_root, resolved_path)
                # Session-scope the resolved path
                return self._scope_to_session_dir(resolved)

        # Fallback to default paths if not found/specified in contracts
        if artifact_id == "workflow_orchestration_plan":
            rel = os.path.join("artifacts", f"plan_{self.workflow_id}.md")
        else:
            rel = os.path.join("artifacts", f"{artifact_id}.md")
        resolved = os.path.join(self.repo_root, rel)
        return self._scope_to_session_dir(resolved)

    def _scope_to_session_dir(self, resolved_path: str) -> str:
        """If session dir is set and path is under artifacts/, scope it to the session dir."""
        if not self.artifact_session_dir:
            return resolved_path
        artifacts_base = os.path.join(self.repo_root, "artifacts")
        normalized = os.path.normpath(resolved_path)
        if normalized.startswith(os.path.normpath(artifacts_base)):
            relative = os.path.relpath(normalized, artifacts_base)
            return os.path.join(self.artifact_session_dir, relative)
        return resolved_path
```

---

### Task 3: Session-scope default plan_out and log_dir

**Files:**
- Modify: `scripts/workflow-runtime.py` (constructor + `main()` or `run()`)

- [ ] **Step 1: Update default paths in `_create_user_intent_artifact`**

After setting `self.artifact_session_dir` (in step 2 of Task 1), also update the output defaults:

```python
            self.artifact_session_dir = os.path.dirname(intent_path)

            # Update default output paths to use session directory
            if not self.plan_out or self.plan_out == os.path.join(self.repo_root, "artifacts", f"plan_{self.workflow_id}.md"):
                self.plan_out = os.path.join(self.artifact_session_dir, f"plan_{self.workflow_id}.md")
            if not self.log_dir or self.log_dir == os.path.join(self.repo_root, "artifacts"):
                self.log_dir = self.artifact_session_dir

            print(f"[OK] Created user intent artifact: ...")
```

---

### Task 4: Update tests

**Files:**
- Modify: `tests/test_dynamic_path_resolution.py`

- [ ] **Step 1: Add test case for session-scoped artifact resolution**

Add a new test class or extend the existing one. These tests verify that when `artifact_session_dir` is set, paths resolve under the session dir instead of flat `artifacts/`.

```python
    def test_resolve_with_session_dir(self):
        """Test that artifact path is scoped under session directory when set."""
        session_dir = os.path.join(self.runner.repo_root, "artifacts", "05-orchestration-run")
        self.runner.artifact_session_dir = session_dir

        resolved = self.runner._resolve_artifact_path("prd")

        expected = os.path.join(session_dir, "prd.md")
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected))

    def test_resolve_with_session_dir_workflow_plan(self):
        """Test workflow_orchestration_plan path is scoped under session dir."""
        session_dir = os.path.join(self.runner.repo_root, "artifacts", "05-orchestration-run")
        self.runner.artifact_session_dir = session_dir

        resolved = self.runner._resolve_artifact_path("workflow_orchestration_plan")

        expected = os.path.join(session_dir, "plan_test-wf.md")
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected))

    def test_resolve_without_session_dir(self):
        """Test that path falls back to artifacts/ when no session dir is set."""
        self.runner.artifact_session_dir = None

        resolved = self.runner._resolve_artifact_path("prd")

        expected = os.path.join(self.runner.repo_root, "artifacts", "prd.md")
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected))

    def test_resolve_contract_path_with_session_dir(self):
        """Test contract-based path is also scoped under session dir."""
        session_dir = os.path.join(self.runner.repo_root, "artifacts", "05-orchestration-run")
        self.runner.artifact_session_dir = session_dir
        self.runner.contracts = {
            "artifacts": [
                {
                    "id": "my_custom_artifact",
                    "path": "artifacts/custom_report.md"
                }
            ]
        }

        resolved = self.runner._resolve_artifact_path("my_custom_artifact")

        expected = os.path.join(session_dir, "custom_report.md")
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected))

    @patch("workflow_runtime.load_artifact_contracts")
    def test_resolve_contract_with_template_not_scoped(self, mock_load):
        """Test contract paths with {session_id} template are NOT double-scoped."""
        session_dir = os.path.join(self.runner.repo_root, "artifacts", "05-orchestration-run")
        self.runner.artifact_session_dir = session_dir
        self.runner.contracts = {
            "artifacts": [
                {
                    "id": "my_custom_artifact",
                    "path": "custom_dir/{workflow_id}/{session_id}_report.md"
                }
            ]
        }

        resolved = self.runner._resolve_artifact_path("my_custom_artifact")

        # Template paths under custom_dir (not artifacts/) should NOT be scoped
        expected_rel = os.path.join("custom_dir", "test-wf", "session-123_report.md")
        expected_abs = os.path.join(self.runner.repo_root, expected_rel)
        self.assertEqual(os.path.normpath(resolved), os.path.normpath(expected_abs))
```

---

### Task 5: Run tests and verify

**Files:**
- Run: `tests/test_dynamic_path_resolution.py`

- [ ] **Step 1: Run all path resolution tests**

Run: `python -m pytest tests/test_dynamic_path_resolution.py -v`
Expected: 11 passed (6 existing + 5 new)

- [ ] **Step 2: Run full workflow end-to-end**

Run: `python scripts/workflow-runtime.py --mode plan_only`
Expected: Artifact is created at `artifacts/NN-orchestration-run/00-user-intent.md` and plan at `artifacts/NN-orchestration-run/plan_full-local-sensemaking.md`

- [ ] **Step 3: Verify no stale artifacts**

Check that `artifacts/repository_sensemaking_brief.md` (if it still exists) is no longer referenced — all resolved paths go to the session dir.
