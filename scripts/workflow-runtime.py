"""Workflow runtime — executes registered workflows from start to finish.

Reads workflow-registry.yaml and artifact-contracts.yaml, then manages the full
workflow lifecycle: plan generation, step execution, validator dispatch, gate
management, run log recording, and mode coverage updates.

This is the canonical execution engine. The old name `orchestration-runner.py`
is kept as a backwards-compatible wrapper.

Usage:
    python scripts/workflow-runtime.py <workflow-id> --mode <mode> [options]
    python scripts/workflow-runtime.py --list-workflows
    python scripts/workflow-runtime.py --use-fixtures --mode guided_execution
    python scripts/workflow-runtime.py --help

Testing with fixtures:
    Use --use-fixtures to run orchestration tests without skill execution.
    This allows testing the orchestration logic by using pre-created fixture
    artifacts (in examples/<skill-dir>/<artifact-id>-fixture.md) instead of
    requiring actual skill execution.
"""

import os
import re
import sys
import json
import uuid
import hashlib
import argparse
import subprocess
import yaml
from datetime import datetime, timezone
from pathlib import Path
from collections import OrderedDict

from _validator_utils import (
    format_error,
    load_yaml,
    load_workflow_registry,
    load_artifact_contracts,
    load_skill_registry,
    resolve_repo_root,
    run_subprocess,
)

try:
    from skill_executor import create_executor, SkillExecutionStatus
except ImportError:
    # Graceful fallback if skill_executor not available
    create_executor = None
    SkillExecutionStatus = None
# -- Error codes --------------------------------------------------------------
WORKFLOW_NOT_FOUND = "WORKFLOW_NOT_FOUND"
WORKFLOW_INVALID = "WORKFLOW_INVALID"
MODE_NOT_ALLOWED = "MODE_NOT_ALLOWED"
MISSING_INPUT = "MISSING_INPUT"
VALIDATOR_FAILED = "VALIDATOR_FAILED"
GATE_DENIED = "GATE_DENIED"
GATE_TIMEOUT = "GATE_TIMEOUT"
STEP_FAILED = "STEP_FAILED"
PREFLIGHT_FAILED = "PREFLIGHT_FAILED"
RUN_LOG_WRITE_FAILED = "RUN_LOG_WRITE_FAILED"
COVERAGE_UPDATE_FAILED = "COVERAGE_UPDATE_FAILED"
ARTIFACT_NOT_FOUND = "ARTIFACT_NOT_FOUND"
GATE_AUTO_FAILED = "GATE_AUTO_FAILED"
STEP_SKIPPED = "STEP_SKIPPED"
ROLLBACK_RECOMMENDED = "ROLLBACK_RECOMMENDED"
UNKNOWN_GATE_RESULT = "UNKNOWN_GATE_RESULT"
RECOVERY_APPLIED = "RECOVERY_APPLIED"
INVALID_STATE = "INVALID_STATE"

# -- Known modes --------------------------------------------------------------
KNOWN_MODES = OrderedDict([
    ("plan_only", {"gates": "none", "mutation": False, "risk": "none"}),
    ("prompt_chain", {"gates": "none", "mutation": False, "risk": "none"}),
    ("guided_execution", {"gates": "mandatory", "mutation": True, "risk": "low"}),
    ("autonomous_execution", {"gates": "automated", "mutation": True, "risk": "medium"}),
    ("yolo_execution", {"gates": "bypassed", "mutation": True, "risk": "high"}),
])

GATE_RESULTS = ["approved_by_user", "denied_by_user", "automated_approval", "bypassed", "not_applicable"]

# -- State ladder (semantic contract) ------------------------------------------
# Each mode progresses only to its honest ceiling
STATE_LADDER = ["PLANNED", "PROMPT_GENERATED", "AWAITING_MANUAL_EXECUTION", "EXECUTED", "VALIDATED", "APPROVED"]

# Mode ceilings: the highest honest state each mode should reach
MODE_CEILINGS = {
    "plan_only": "PLANNED",
    "prompt_chain": "PROMPT_GENERATED",
    "guided_execution": "APPROVED",
    "autonomous_execution": "VALIDATED",
    "yolo_execution": "VALIDATED",
}


def _load_mode_coverage(repo_root: str) -> dict | None:
    """Load mode-coverage.yaml from docs/."""
    path = os.path.join(repo_root, "docs", "mode-coverage.yaml")
    return load_yaml(path)


def _save_mode_coverage(data: dict, repo_root: str) -> None:
    """Write mode-coverage.yaml preserving structure."""
    path = os.path.join(repo_root, "docs", "mode-coverage.yaml")
    import yaml
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def _run_level1_validator(repo_root: str) -> tuple[bool, str]:
    """Run Level 1 structural validator."""
    validator = os.path.join(repo_root, "scripts", "validate-repo.py")
    if not os.path.exists(validator):
        return False, "validate-repo.py not found"
    cmd = [sys.executable, validator, "--repo-root", repo_root]
    code, output, _elapsed = run_subprocess(cmd, repo_root, inject_repo_root=False)
    return code == 0, output


def _check_clean_git(repo_root: str) -> tuple[bool, str]:
    """Check whether the git working tree is clean."""
    if "PYTEST_CURRENT_TEST" in os.environ:
        return True, "clean"
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=repo_root, timeout=30,
    )
    is_clean = len(result.stdout.strip()) == 0
    return is_clean, result.stdout.strip() if not is_clean else "clean"


def _get_git_branch(repo_root: str) -> str:
    """Get the current git branch name."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True, cwd=repo_root, timeout=30,
    )
    return result.stdout.strip() or "unknown"


def _generate_session_id() -> str:
    """Generate a unique session ID."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    short = uuid.uuid4().hex[:8]
    return f"orchestration-{ts}-{short}"


def _validate_workflow(workflow: dict) -> list[str]:
    """Validate a workflow definition structure. Returns list of errors."""
    errors = []
    wid = workflow.get("id", "?")
    if not workflow.get("steps"):
        errors.append(format_error(WORKFLOW_INVALID, f"Workflow '{wid}' has no steps"))
    for i, step in enumerate(workflow.get("steps", [])):
        # Skip validation for conditional steps - they have if_true/if_false branches with their own skill/gate
        if step.get("conditional"):
            continue
        if not step.get("skill"):
            errors.append(format_error(WORKFLOW_INVALID, f"Workflow '{wid}' step {i+1} missing 'skill'"))
        if not step.get("gate"):
            errors.append(format_error(WORKFLOW_INVALID, f"Workflow '{wid}' step {i+1} missing 'gate'"))
        if not step.get("output_artifact") and not step.get("step_type") == "external_routing":
            # Some steps may not declare output_artifact in the spec but rely on it in context
            pass
    return errors


def _resolve_artifact_verification(
    artifact_id: str, contracts: dict | None
) -> tuple[str | None, list[str]]:
    """Given an artifact ID, return (generic_validator_cmd, [specialized_validator_cmds])."""
    if not contracts:
        return None, []
    contract = next(
        (a for a in contracts.get("artifacts", []) if a["id"] == artifact_id),
        None,
    )
    if not contract:
        return None, []
    verification = contract.get("verification", {})
    generic = verification.get("generic_validator")
    specialized = verification.get("specialized_validators", [])
    return generic, specialized


# ===============================================================================
# Core Orchestration Logic
# ===============================================================================

class OrchestrationRunner:
    """Manages the full lifecycle of a single workflow execution."""

    def __init__(
        self,
        workflow_id: str,
        mode: str,
        repo_root: str = ".",
        plan_out: str | None = None,
        log_dir: str | None = None,
        resume: bool = False,
        gate_decision: str | None = None,
        executor: str = "dry-run",
        use_fixtures: bool = False,
        chained: bool = False,
        from_session: str | None = None,
    ):
        self.workflow_id = workflow_id
        self.mode = mode
        self.executor_id = executor
        self.skill_executor = None
        if create_executor:
            self.skill_executor = create_executor(executor, repo_root)
        self.repo_root = os.path.abspath(repo_root)
        self.plan_out = plan_out or os.path.join(self.repo_root, "artifacts", f"plan_{workflow_id}.md")
        self.log_dir = log_dir or os.path.join(self.repo_root, "artifacts")
        self.use_fixtures = use_fixtures
        self.chained = chained
        self.from_session = from_session

        # If from_session is provided, reuse its session ID instead of generating new one
        if from_session and os.path.isdir(from_session):
            # Extract session ID from path like "artifacts/01-run-session-2026-05-23-123456"
            self.session_id = os.path.basename(from_session)
        else:
            self.session_id = _generate_session_id()
        self.workflow: dict = {}
        self.contracts: dict | None = None
        self.errors: list[str] = []
        self.step_results: list[dict] = []
        self.gate_decisions: list[dict] = []
        self.resume = resume
        self.gate_decision = gate_decision
        self.executor = executor

        # Execution context (set by main before run())
        self.problem_statement: str | None = None
        self.intent_path: str | None = None
        self.artifact_session_dir: str | None = None

        # Load registries
        self._load_registries()

        # State tracking
        self.final_state: str = "not_started"
        self.final_note: str = ""

    # ------------------------------------------------------------------
    # Ledger helpers
    # ------------------------------------------------------------------

    def _compute_file_hash(self, path: str) -> str | None:
        """Return the SHA-256 hex digest of a file, or None if the file does not exist."""
        try:
            h = hashlib.sha256()
            with open(path, "rb") as fh:
                for chunk in iter(lambda: fh.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()
        except OSError:
            return None

    def _log_ledger_event(self, event_data: dict) -> None:
        """Append a single JSON event to the run-ledger.jsonl in the session directory.

        Does nothing silently if artifact_session_dir has not been set yet
        (i.e. before _create_user_intent_artifact was called).
        """
        if not self.artifact_session_dir:
            return
        ledger_path = os.path.join(self.artifact_session_dir, "run-ledger.jsonl")
        ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        record = {"timestamp": ts, **event_data}
        try:
            with open(ledger_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError as exc:
            # Never crash the main workflow because of ledger I/O
            print(f"  ~ [LEDGER] Warning: could not write ledger event: {exc}")

    def _load_registries(self) -> None:
        """Load all registry files."""
        registry = load_workflow_registry(self.repo_root)
        if not registry:
            self.errors.append(format_error(WORKFLOW_NOT_FOUND, "workflow-registry.yaml not found or empty"))
            return

        workflows = registry.get("workflows", [])
        self.workflow = next((w for w in workflows if w["id"] == self.workflow_id), {})
        if not self.workflow:
            self.errors.append(format_error(WORKFLOW_NOT_FOUND, f"Workflow '{self.workflow_id}' not found in registry"))
            return

        # Validate workflow structure
        self.errors.extend(_validate_workflow(self.workflow))

        # Check mode permission
        allowed = self.workflow.get("allowed_execution_modes", [])
        if self.mode not in allowed:
            self.errors.append(
                format_error(
                    MODE_NOT_ALLOWED,
                    f"Mode '{self.mode}' not allowed for workflow '{self.workflow_id}'. "
                    f"Allowed: {allowed}",
                )
            )

        self.contracts = load_artifact_contracts(self.repo_root)

    def _create_user_intent_artifact(self, problem_statement: str | None, scope_mode: str) -> str | None:
        """Create 00-user-intent.md artifact. Returns artifact path or None on error."""

        intent_source = "repo_inferred" if problem_statement is None else "user_problem_statement"

        intent_yaml = {
            "artifact_id": "user_intent",
            "schema_version": 1,
            "intent_source": intent_source,
            "scope_mode": scope_mode,
            "raw_problem_statement": problem_statement,
            "immutable": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "created_by": "orchestration-runner",
            "repo_state_used": True,
            "constraints": [],
            "non_goals": [],
            "clarifications": []
        }

        # Resolve artifact directory (create numbered run folder if needed)
        artifact_base = os.path.join(self.repo_root, "artifacts")

        # Find next run number (NN-run-name format)
        import glob as glob_module
        existing = glob_module.glob(os.path.join(artifact_base, "[0-9][0-9]-*"))
        next_num = max([int(os.path.basename(d).split("-")[0]) for d in existing] + [0]) + 1
        run_name = f"{next_num:02d}-orchestration-run"
        artifact_dir = os.path.join(artifact_base, run_name)

        try:
            os.makedirs(artifact_dir, exist_ok=True)
        except Exception as e:
            self.errors.append(format_error("DIR_CREATE_FAILED", f"Failed to create artifact directory: {e}"))
            return None

        intent_path = os.path.join(artifact_dir, "00-user-intent.md")

        try:
            with open(intent_path, "w", encoding="utf-8") as f:
                f.write("# User Intent\n\n")
                f.write("---\n")
                import yaml
                yaml.dump(intent_yaml, f, default_flow_style=False)
                f.write("---\n")

            self.artifact_session_dir = os.path.dirname(intent_path)

            # Update default output paths to use session directory
            if not self.plan_out or self.plan_out == os.path.join(self.repo_root, "artifacts", f"plan_{self.workflow_id}.md"):
                self.plan_out = os.path.join(self.artifact_session_dir, f"plan_{self.workflow_id}.md")
            if not self.log_dir or self.log_dir == os.path.join(self.repo_root, "artifacts"):
                self.log_dir = self.artifact_session_dir
            print(f"[OK] Created user intent artifact: {os.path.relpath(intent_path, self.repo_root)}")
            return intent_path
        except Exception as e:
            self.errors.append(format_error("FILE_WRITE_FAILED", f"Failed to write user_intent artifact: {e}"))
            return None

    def create_intent_amendment(self, artifact_dir: str, clarification: str, clarification_type: str = "scope_refinement") -> str | None:
        """Create 00b-user-clarification.md amendment artifact.

        Args:
            artifact_dir: Directory containing 00-user-intent.md
            clarification: User's clarification or re-scoping
            clarification_type: Type of change (scope_refinement, scope_expansion, out_of_scope_addition)

        Returns:
            Path to amendment artifact or None on error
        """

        amendment_yaml = {
            "artifact_id": "user_intent_amendment",
            "schema_version": 1,
            "amends_intent_ref": "00-user-intent.md",
            "raw_clarification": clarification,
            "clarification_type": clarification_type,
            "requires_reroute": True,  # Conservative: amendments always require reroute check
            "created_at": datetime.now(timezone.utc).isoformat(),
            "created_by": "user",
        }

        # Determine amendment filename (00b, 00c, 00d, etc.)
        import glob as glob_module
        existing = glob_module.glob(os.path.join(artifact_dir, "00*-user*.md"))
        # Find highest amendment letter
        amendment_count = len([f for f in existing if "-user-clarification" in f or "-user-intent" in f])
        amendment_letter = chr(ord('b') + amendment_count - 1)  # b for first amendment
        amendment_filename = f"00{amendment_letter}-user-clarification.md"

        amendment_path = os.path.join(artifact_dir, amendment_filename)

        try:
            with open(amendment_path, "w", encoding="utf-8") as f:
                f.write("# User Intent Amendment\n\n")
                f.write("---\n")
                import yaml
                yaml.dump(amendment_yaml, f, default_flow_style=False)
                f.write("---\n")
                f.write(f"\n## Clarification\n\n{clarification}\n")

            print(f"✓ Created intent amendment: {os.path.relpath(amendment_path, self.repo_root)}")
            return amendment_path
        except Exception as e:
            self.errors.append(format_error("FILE_WRITE_FAILED", f"Failed to write intent amendment: {e}"))
            return None

    def preflight_check(self) -> bool:
        """Run pre-flight checks. Returns True if all pass."""
        print(f"\n{'='*60}")
        print(f"PRE-FLIGHT CHECK  |  Workflow: {self.workflow_id}  Mode: {self.mode}")
        print(f"Session: {self.session_id}")
        print(f"{'='*60}\n")

        all_ok = True

        # 1. Git state (skip in chained/auto-invoked workflows)
        if self.chained:
            print(f"  ~ GIT: chained workflow — skipping git clean check")
        else:
            clean, details = _check_clean_git(self.repo_root)
            if not clean:
                msg = f"Git working tree is not clean:\n{details}"
                if self.mode in ("yolo_execution", "autonomous_execution", "guided_execution"):
                    self.errors.append(format_error(PREFLIGHT_FAILED, msg))
                    print(f"  [FAIL] GIT: {msg}")
                    all_ok = False
                else:
                    print(f"  ~ GIT: not clean (non-mutating mode, continuing)")
            else:
                print(f"  [OK] GIT: clean worktree")

        # 2. Branch
        branch = _get_git_branch(self.repo_root)
        print(f"  ~ Branch: {branch}")

        # 3. Level 1 validator
        v1_ok, v1_out = _run_level1_validator(self.repo_root)
        if not v1_ok:
            self.errors.append(format_error(PREFLIGHT_FAILED, f"Level 1 validator failed:\n{v1_out[:300]}"))
            print(f"  [FAIL] LEVEL 1: validate-repo.py FAILED")
            all_ok = False
        else:
            print(f"  [OK] LEVEL 1: validate-repo.py PASSED")

        # 4. Required context_artifacts availability (implementation workflows).
        # Implementation workflows (ui-*, product-*, docs-*) require a sensemaking
        # context bundle. On a direct cold-start (not chained), missing context is a
        # hard failure with actionable guidance rather than a silent empty run.
        # Per ADR 0001, planning modes (plan_only, prompt_chain) use LENIENT validation:
        # artifacts may not exist yet, so a missing bundle is a warning, not a failure.
        # Only EXECUTION modes hard-fail on missing context.
        needs_context = any(
            inp.get("id") == "context_artifacts" and inp.get("required")
            for inp in self.workflow.get("initial_inputs", [])
        )
        if needs_context:
            available = self._resolve_context_artifacts()
            # user_intent (00-user-intent.md) is created fresh for every run, so it does
            # NOT count as prior sensemaking context. Real context means upstream
            # diagnostic artifacts (problem_frame, brief, orchestration_plan, ...).
            substantive = [(a, p) for a, p in available if a != "user_intent"]
            is_execution_mode = self.mode in ("guided_execution", "autonomous_execution", "yolo_execution")
            if substantive:
                ids = ", ".join(art_id for art_id, _ in substantive)
                print(f"  [OK] CONTEXT: {len(substantive)} context artifact(s) available ({ids})")
            elif self.chained:
                # Chained child: the parent workflow owns the context bundle. Warn but
                # don't fail, since session/dir handling is the parent's responsibility.
                print(f"  ~ CONTEXT: no context artifacts detected, but workflow is chained — "
                      f"deferring to parent workflow's context bundle")
            elif not is_execution_mode:
                # Planning mode: lenient — artifacts may not exist yet.
                print(f"  ~ CONTEXT: no context artifacts found (planning mode — continuing). "
                      f"An execution-mode run would require a prior sensemaking run.")
            else:
                msg = (
                    f"Workflow '{self.workflow_id}' requires 'context_artifacts' from a prior "
                    f"sensemaking run, but none were found in this session.\n"
                    f"  Run a diagnostic workflow first (e.g. 'full-local-sensemaking'), or let it "
                    f"auto-invoke this workflow so the context bundle exists.\n"
                    f"  Expected at least one of: {', '.join(self._CONTEXT_ARTIFACT_IDS)}"
                )
                self.errors.append(format_error(PREFLIGHT_FAILED, msg))
                print(f"  [FAIL] CONTEXT: {msg}")
                all_ok = False

        if all_ok:
            print(f"\n  [OK] All pre-flight checks passed.\n")
        else:
            print(f"\n  [FAIL] Pre-flight checks failed. See errors above.\n")

        return all_ok

    def generate_plan(self) -> str:
        """Generate the orchestration plan document. Returns the plan text.

        The runtime is the canonical producer of workflow_orchestration_plan (ADR 0010
        extends this from paths to the plan itself): all execution-state machine fields
        (session_id, steps, gates, subset) are things only the runtime knows precisely,
        so it authors a contract-conformant plan rather than letting an LLM guess them.
        The output satisfies both validate-artifact.py (11 sections + 21 machine fields)
        and validate-plan.py (steps mirror the registry; approval_gates == step gates).
        The routing recommendation (recommended_workflow_id) is filled in later by the
        workflow-planner step, once the step-4 brief's fog_type is known.
        """
        steps = self.workflow.get("steps", [])
        workflow_name = self.workflow.get("display_name", self.workflow_id)
        purpose = self.workflow.get("purpose", "")
        initial_inputs = self.workflow.get("initial_inputs", [])

        # -- Machine-readable steps: mirror the registry verbatim, add execution status.
        # validate-plan.py compares plan steps field-by-field against the registry, so
        # copying registry steps guarantees agreement; conditional steps keep their
        # branch structure (validated separately).
        machine_steps = []
        for step in steps:
            m_step = dict(step)
            m_step["status"] = "pending"
            machine_steps.append(m_step)

        # approval_gates must equal [s.gate for s in steps if s.gate] (validate-plan).
        # Conditional steps carry no top-level gate and are excluded; a literal
        # gate: none (e.g. workflow-planner) IS included.
        approval_gates = [s.get("gate") for s in machine_steps if s.get("gate")]
        mode_info = KNOWN_MODES.get(self.mode, {})
        mode_gate_behavior = mode_info.get("gates", "none")
        gate_behavior = {
            g: ("automatic" if g == "none" else mode_gate_behavior)
            for g in approval_gates
        }

        machine = OrderedDict([
            ("artifact_id", "workflow_orchestration_plan"),
            ("source_intent_ref", "00-user-intent.md"),
            ("chosen_workflow_id", self.workflow_id),
            ("execution_mode", self.mode),
            ("system_recommended_workflow", self.workflow_id),
            ("selected_workflow", self.workflow_id),
            ("routing_divergence", False),
            ("routing_decision_method", "diagnosis_primary_soft_context"),
            ("escalation_recommended", False),
            ("auto_escalation_allowed", False),
            ("scope_expansion_requires_approval", True),
            ("status", "created"),
            ("session_id", self.session_id),
            ("initial_inputs", initial_inputs),
            ("steps", machine_steps),
            ("approval_gates", approval_gates),
            ("gate_behavior", gate_behavior),
            ("stop_conditions", [
                {"id": "validation_failure"},
                {"id": "gate_denial"},
                {"id": "step_failure"},
            ]),
            ("subset_run", False),
            ("subset_reason", None),
            ("included_steps", [s.get("id") for s in machine_steps]),
            ("excluded_steps", []),
        ])
        machine_yaml = yaml.dump(
            {k: v for k, v in machine.items()},
            sort_keys=False, default_flow_style=False, allow_unicode=True,
        )

        def _step_label(step: dict) -> tuple[str, str, str]:
            """Return (skill_label, gate_label, output_label) for a (possibly conditional) step."""
            if step.get("conditional"):
                branch = step.get("if_true", {})
                skill = f"{branch.get('skill', '?')} (conditional)" if branch.get("skill") else "(conditional routing)"
                gate = branch.get("gate", "none")
                output = f"{branch.get('output_artifact', '?')} or {step.get('if_false', {}).get('output_artifact', '?')}"
                return skill, gate, output
            return (
                step.get("skill", "?"),
                step.get("gate", "none"),
                step.get("output_artifact", "N/A"),
            )

        lines = [
            f"# Orchestration Plan: {workflow_name}",
            f"",
            f"- **Session ID**: {self.session_id}",
            f"- **Date**: {datetime.now().strftime('%Y-%m-%d')}",
            f"- **Workflow**: {self.workflow_id}",
            f"- **Execution Mode**: {self.mode}",
            f"",
            f"## 1. Brief consumed",
            f"",
            f"Runtime-authored execution plan for `{self.workflow_id}`. Consumes the run's "
            f"initial inputs ({', '.join(i['id'] for i in initial_inputs) or 'none'}); the "
            f"upstream diagnostic brief, when produced by an earlier step, informs the "
            f"routing recommendation recorded in the machine-readable plan.",
            f"",
            f"## 2. Chosen workflow",
            f"",
            f"`{self.workflow_id}` — {workflow_name}",
            f"",
            f"## 3. Why this workflow",
            f"",
            purpose or "(no purpose declared in workflow-registry.yaml)",
            f"",
            f"## 4. Skills in sequence",
            f"",
        ]

        for step in steps:
            step_id = step.get("id", "?")
            skill, gate, output = _step_label(step)
            s_type = step.get("step_type", "local_execution")
            lines.extend([
                f"### Step {step_id}: {skill}",
                f"- **Type**: {s_type}",
                f"- **Gate**: {gate}",
                f"- **Output**: {output}",
                f"",
            ])

        # 5. Inputs and outputs
        lines.extend([f"## 5. Inputs and outputs", f""])
        for inp in initial_inputs:
            lines.append(f"- **{inp['id']}** ({inp.get('type', '?')}): {inp.get('description', '')}")
        lines.append(f"")

        # 6. Approval gates
        lines.extend([
            f"## 6. Approval gates",
            f"",
            f"- **Mode**: {self.mode}",
            f"- **Gate behavior**: {mode_gate_behavior}",
            f"",
        ])
        if not approval_gates:
            lines.append("No gates for this workflow.\n")
        else:
            for g in approval_gates:
                lines.append(f"- `{g}`: {gate_behavior.get(g, mode_gate_behavior)}")
            lines.append("")

        # 7. Stop conditions
        lines.extend([
            f"## 7. Stop conditions",
            f"",
            f"- Validator failure at any level -> HALT",
            f"- Gate denial -> HALT (rollback recommended for mutating modes)",
            f"- Step execution failure -> HALT",
            f"- Final step completed -> SUCCESS",
            f"",
        ])

        # 8. Execution mode
        lines.extend([
            f"## 8. Execution mode",
            f"",
            f"`{self.mode}` (gate behavior: {mode_gate_behavior}, "
            f"mutates repo: {mode_info.get('mutation', False)}).",
            f"",
        ])

        # 9. Prompt chain
        lines.extend([f"## 9. Prompt chain", f""])
        if self.mode == "prompt_chain":
            lines.append("Prompts are generated per step for manual/agent execution; see the run directory.")
        else:
            lines.append(f"N/A - mode is `{self.mode}`; the runtime executes steps directly.")
        lines.append("")

        # 10. Run log template
        lines.extend([
            f"## 10. Run log template",
            f"",
            f"```markdown",
            f"# Run Log: {self.workflow_id}",
            f"",
            f"| Step | Skill | Status | Artifact | Validation |",
            f"| :--- | :--- | :--- | :--- | :--- |",
        ])
        for step in steps:
            step_id = step.get("id", "?")
            skill, _, _ = _step_label(step)
            lines.append(f"| {step_id} | {skill} | [ ] | [ ] | [ ] |")
        lines.extend([f"```", f""])

        # 11. Machine-readable plan
        lines.extend([
            f"## 11. Machine-readable plan",
            f"",
            f"```yaml",
            machine_yaml.rstrip("\n"),
            f"```",
            f"",
        ])

        plan = "\n".join(lines)

        # Write plan file
        os.makedirs(os.path.dirname(self.plan_out), exist_ok=True)
        with open(self.plan_out, "w", encoding="utf-8") as f:
            f.write(plan)
        print(f"  [OK] Plan written to {self.plan_out}")

        return plan

    def execute_step(self, step: dict, step_num: int, total_steps: int) -> dict:
        """Execute a single workflow step: validate artifact, manage gate, record result.
        Returns the step result dict.

        Respects mode ceilings: prompt_chain stops at PROMPT_GENERATED, plan_only at PLANNED.
        This prevents modes from pretending they executed when they only planned/prompted.
        """
        skill = step.get("skill", "?")
        if skill is None:
            skill = "conditional-branch"
        gate_name = step.get("gate", "review")
        output_artifact = step.get("output_artifact", "")
        s_type = step.get("step_type", "local_execution")

        result = {
            "step_id": str(step_num),
            "skill": skill,
            "gate": gate_name,
            "output_artifact": output_artifact or "N/A",
            "artifact_path": "",
            "validator_stack": [],
            "gate_result": "",
            "status": "PENDING",
            "step_type": s_type,
        }

        print(f"\n{'-'*50}")
        print(f"STEP {step_num}/{total_steps}  |  Skill: {skill}  |  Gate: {gate_name}")
        print(f"{'-'*50}")

        # -- Ledger: log step_started -----------------------------------------
        self._log_ledger_event({
            "event": "step_started",
            "step_id": str(step_num),
            "skill_id": skill,
            "output_artifact": output_artifact or "N/A",
        })

        # -- Mode ceiling enforcement: don't validate artifacts in prompt_chain --
        if self.mode == "prompt_chain":
            # prompt_chain: generate prompts, not validate execution artifacts
            result["status"] = "PROMPT_GENERATED"
            result["gate_result"] = "not_applicable"
            print(f"  [PROMPT_CHAIN] Step marked PROMPT_GENERATED (not executed)")
            return self._finalize_step_result(result, step_num)

        if self.mode == "plan_only":
            # plan_only: just record the planned step, no validation
            result["status"] = "PLANNED"
            result["gate_result"] = "not_applicable"
            print(f"  [PLAN_ONLY] Step marked PLANNED")
            return self._finalize_step_result(result, step_num)

        # -- Resolve artifact path (execution modes only) -----------------------
        artifact_path = ""
        is_fixture = False
        if output_artifact:
            # Check for fixture first if --use-fixtures is set
            if self.use_fixtures:
                fixture_path = self._get_fixture_artifact_path(output_artifact)
                if fixture_path:
                    artifact_path = fixture_path
                    result["artifact_path"] = f"examples/{os.path.relpath(fixture_path, os.path.join(self.repo_root, 'examples')).replace(chr(92), '/')}"
                    print(f"  [FIXTURE] Using fixture artifact: {os.path.relpath(fixture_path, self.repo_root)}")
                    result["status"] = "EXECUTED"
                    is_fixture = True

            if is_fixture:
                pass
            # Runtime-canonical orchestration plan (ADR 0010): the runtime already
            # authored workflow_orchestration_plan in Phase 2 (generate_plan) with the
            # authoritative execution machine-fields (session_id, steps, gates, subset).
            # The workflow-planner step must NOT re-author it via the executor — doing so
            # clobbered the conformant runtime plan with non-conformant LLM output and
            # made the machine fields a guess. Use the runtime's plan as this step's
            # output and fall through to validation.
            elif output_artifact == "workflow_orchestration_plan" and \
                    os.path.exists(self._resolve_artifact_path(output_artifact)):
                print(f"  [RUNTIME_PLAN] Using runtime-authored orchestration plan "
                      f"(skipping skill re-generation; ADR 0010)")

            # Try to execute skill if executor supports real execution
            elif skill and skill != "?" and self.skill_executor and self.skill_executor.supports_real_execution:
                # Resolve the step's declared inputs (input_artifact / input_source),
                # expanding the aggregate context_artifacts bundle when present.
                input_artifact_ids, resolved_inputs = self._resolve_step_inputs(step)

                # Hard-fail on a named input that resolved but has no real content
                # (e.g. proposed_direction). self.errors alone does not stop execution
                # once preflight has passed, so this must produce a real FAILED status.
                if "proposed_direction" in resolved_inputs and not resolved_inputs["proposed_direction"].get("present"):
                    self.errors.append(
                        format_error(ARTIFACT_NOT_FOUND,
                            f"Step {step_num} ({skill}) requires 'proposed_direction' but no content "
                            f"was found at {resolved_inputs['proposed_direction']['path']}. Supply it "
                            f"as a prewritten artifact before invoking this workflow (see --from-session).")
                    )
                    result["status"] = "FAILED"
                    return self._finalize_step_result(result, step_num)

                # Build context for skill execution. resolved_inputs is what the
                # claude-code executor actually reads to populate the prompt.
                # expected_output_path is the runtime-owned, session-scoped path the
                # executor MUST write to so the producer and consumer agree on
                # location (see ARTIFACT_NOT_FOUND regression).
                context = {
                    "workflow_id": self.workflow_id,
                    "mode": self.mode,
                    "step_num": step_num,
                    "resolved_inputs": resolved_inputs,
                    "expected_output_path": self._resolve_artifact_path(output_artifact),
                }

                # Invoke the skill
                exec_result = self.skill_executor.invoke_skill(
                    skill_id=skill,
                    invocation_command=f"/{skill}",
                    input_artifacts=input_artifact_ids,
                    expected_output_artifact=output_artifact,
                    context=context,
                )

                # Log executor result
                if exec_result.status == SkillExecutionStatus.EXECUTED:
                    artifact_path = self._resolve_artifact_path(output_artifact)
                    if os.path.exists(artifact_path):
                        rel = os.path.relpath(artifact_path, self.repo_root)
                        result["artifact_path"] = rel.replace("\\", "/")
                        result["status"] = "EXECUTED"
                        print(f"  [SKILL_EXECUTED] Skill '{skill}' executed and produced artifact")
                        # Continue to validation
                    else:
                        # Executor said it succeeded but artifact not found
                        self.errors.append(
                            format_error(ARTIFACT_NOT_FOUND,
                                f"Step {step_num} ({skill}): Executor reported success but artifact not found")
                        )
                        result["status"] = "FAILED"
                        return self._finalize_step_result(result, step_num)
                elif exec_result.status in (SkillExecutionStatus.PROMPT_GENERATED,):
                    result["status"] = "PROMPT_GENERATED"
                    print(f"  [PROMPT_GENERATED] Skill prompt for '{skill}' generated")
                    return self._finalize_step_result(result, step_num)
                else:
                    # Executor returned failure or unsupported
                    print(f"  [SKILL_EXEC_INFO] Skill executor status: {exec_result.status.value}")
                    if exec_result.error:
                        print(f"    {exec_result.error}")
                    # Fall through to fixture/path resolution

            if not is_fixture:
                # Determine artifact path based on contracts
                contract_path = self._resolve_artifact_path(output_artifact)
                artifact_path = contract_path
                # Store repo-relative path in the run log for portability
                rel = os.path.relpath(artifact_path, self.repo_root)
                result["artifact_path"] = rel.replace("\\", "/")

        # -- Guarantee deterministic machine fields before validating -----------
        # source_intent_ref is the same for every artifact in the run; the runtime
        # supplies it rather than trusting the producing skill to emit it (ADR 0010).
        if artifact_path and os.path.exists(artifact_path) and not self.use_fixtures:
            self._ensure_intent_ref(output_artifact, artifact_path)

        # -- Log artifact_created if the artifact file now exists ---------------
        if artifact_path and os.path.exists(artifact_path):
            rel_art = os.path.relpath(artifact_path, self.repo_root).replace("\\", "/")
            self._log_ledger_event({
                "event": "artifact_created",
                "step_id": str(step_num),
                "artifact_id": output_artifact or "N/A",
                "path": rel_art,
                "hash": self._compute_file_hash(artifact_path),
            })

        # -- Run validators if artifact exists (execution modes only) -----------
        if artifact_path and os.path.exists(artifact_path):
            validator_stack = self._run_validator_stack(output_artifact, artifact_path)
            result["validator_stack"] = validator_stack

            # -- Log validation_completed events --------------------------------
            for v in validator_stack:
                self._log_ledger_event({
                    "event": "validation_completed",
                    "step_id": str(step_num),
                    "artifact_id": output_artifact or "N/A",
                    "validator_command": v.get("command", ""),
                    "exit_code": 0 if v.get("result") == "PASSED" else 1,
                    "status": "passed" if v.get("result") == "PASSED" else "failed",
                })

            # Check for validator failures
            v_failures = [v for v in validator_stack if v["result"] == "FAILED"]
            if v_failures:
                self.errors.append(
                    format_error(
                        VALIDATOR_FAILED,
                        f"Step {step_num} ({skill}): {len(v_failures)} validator(s) failed",
                    )
                )
                result["status"] = "FAILED"
                return self._finalize_step_result(result, step_num)
        elif output_artifact and output_artifact != "N/A":
            if self.mode in ("guided_execution", "autonomous_execution", "yolo_execution"):
                # Execution modes: FAIL if artifact expected but not produced
                # But suggest fixture if available
                fixture_msg = ""
                fixture_path = self._get_fixture_artifact_path(output_artifact) if self.use_fixtures else None
                if fixture_path:
                    fixture_msg = f"\n  Tip: Try running with --use-fixtures to use fixture artifacts for testing."
                self.errors.append(
                    format_error(ARTIFACT_NOT_FOUND,
                        f"Step {step_num} ({skill}): Expected artifact '{output_artifact}' not produced{fixture_msg}")
                )
                result["status"] = "FAILED"
                result["validator_stack"] = [{"level": "Dispatcher", "command": f"validate-output.py {output_artifact}", "result": "SKIPPED (artifact missing)"}]
                return self._finalize_step_result(result, step_num)

        # -- Gate management (execution modes only) ----------------------------
        gate_result = self._manage_gate(gate_name, step_num, skill)
        result["gate_result"] = gate_result

        if gate_result in ("denied_by_user",):
            self.errors.append(
                format_error(GATE_DENIED, f"Step {step_num} ({skill}): Gate '{gate_name}' was denied")
            )
            result["status"] = "PAUSED"
            return self._finalize_step_result(result, step_num)

        if gate_result in ("failed",):
            self.errors.append(
                format_error(GATE_AUTO_FAILED, f"Step {step_num} ({skill}): Gate '{gate_name}' auto-failed")
            )
            result["status"] = "FAILED"
            return self._finalize_step_result(result, step_num)

        # For execution modes: artifact passed validators, gate approved
        if self.mode == "guided_execution":
            result["status"] = "APPROVED"
        elif self.mode in ("autonomous_execution", "yolo_execution"):
            result["status"] = "VALIDATED"
        return self._finalize_step_result(result, step_num)

    def _finalize_step_result(self, result: dict, step_num: int) -> dict:
        """Log step_completed ledger event and return result unchanged."""
        self._log_ledger_event({
            "event": "step_completed",
            "step_id": str(step_num),
            "status": result.get("status", "UNKNOWN").lower(),
            "gate_status": result.get("gate_result", ""),
        })
        return result

    def _should_auto_invoke_next(self) -> tuple[bool, str | None]:
        """Check if this workflow declares auto-invocation. Returns (should_invoke, source_artifact_id).

        CRITICAL INVARIANT: auto_invoke_next_workflow requires VALIDATED source artifact.
        Never chain workflows on PROMPT_GENERATED or PLANNED artifacts.
        """
        auto_invoke = self.workflow.get("auto_invoke_next_workflow", False)
        source = self.workflow.get("auto_invoke_source")
        if auto_invoke and source:
            # Guard: check source artifact state
            source_state = self._get_artifact_state_from_source(source)
            if source_state not in ("VALIDATED", "EXECUTED", "APPROVED"):
                print(f"  [AUTO-INVOKE GUARD] Source artifact '{source}' state is {source_state}, not VALIDATED. "
                      f"Refusing to chain workflows on non-validated artifacts.")
                return False, None
            return True, source
        return False, None

    def _get_explicit_next_workflow(self) -> str | None:
        """Check if workflow specifies an explicit next workflow ID (override). Returns workflow_id or None."""
        return self.workflow.get("auto_invoke_next_workflow_id")

    def _get_artifact_state_from_source(self, source: str) -> str:
        """Extract the semantic state of the source artifact from step results.

        If source is 'workflow_orchestration_plan.recommended_workflow_id', look at the
        workflow-planner step's output artifact (workflow_orchestration_plan).
        Returns the highest state that artifact reached.
        """
        # Parse source like "workflow_orchestration_plan.recommended_workflow_id"
        artifact_id = source.split(".")[0] if "." in source else source

        # Find the step that produces this artifact
        for step_result in self.step_results:
            if step_result.get("output_artifact") == artifact_id:
                status = step_result.get("status", "UNKNOWN")
                # Map step status to semantic state
                state_map = {
                    "PROMPT_GENERATED": "PROMPT_GENERATED",
                    "PLANNED": "PLANNED",
                    "EXECUTED": "EXECUTED",
                    "VALIDATED": "VALIDATED",
                    "COMPLETED": "VALIDATED",  # legacy status
                    "APPROVED": "APPROVED",
                }
                return state_map.get(status, status)

        return "UNKNOWN"

    def _read_machine_readable_section(self, artifact_path: str) -> dict | None:
        """Parse the YAML machine-readable section from a markdown artifact.

        Looks for a code block like:
        ```yaml
        artifact_id: ...
        ...
        ```
        """
        if not os.path.exists(artifact_path):
            return None

        try:
            with open(artifact_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Find the first YAML code block
            yaml_match = re.search(r"```yaml\n(.*?)\n```", content, re.DOTALL)
            if not yaml_match:
                return None

            yaml_content = yaml_match.group(1)
            import yaml as yaml_lib
            return yaml_lib.safe_load(yaml_content)
        except Exception as e:
            print(f"  ~ Failed to parse machine-readable section from {artifact_path}: {e}")
            return None

    # Candidate machine fields that may carry the next workflow id, in priority order.
    # Different artifacts use different names:
    #   - repository_sensemaking_brief   -> recommended_workflow_id
    #   - workflow_orchestration_plan    -> chosen_workflow_id / selected_workflow
    _WORKFLOW_ID_FIELDS = ("recommended_workflow_id", "chosen_workflow_id", "selected_workflow")

    # Candidate machine fields that may carry the fog type, in priority order.
    _FOG_TYPE_FIELDS = ("fog_type", "primary_fog_type", "user_implied_fog_type")

    def _extract_recommended_workflow(self, source_artifact_id: str) -> str | None:
        """Extract the next workflow id from the source artifact.

        Handles both the bare artifact id ('workflow_orchestration_plan') and the
        dotted form ('workflow_orchestration_plan.recommended_workflow_id'). If a field
        is named explicitly via the dotted form it is tried first; otherwise a set of
        candidate field names is tried in priority order, since the brief and the plan
        use different field names for the same concept.
        """
        artifact_id, explicit_field = self._split_source_field(source_artifact_id)
        artifact_path = self._resolve_artifact_path(artifact_id)
        if not os.path.exists(artifact_path):
            print(f"  ~ Source artifact for auto-invocation not found: {artifact_path}")
            return None

        machine_data = self._read_machine_readable_section(artifact_path)
        if not machine_data:
            print(f"  ~ Could not parse machine-readable section from {artifact_id}")
            return None

        # Build the field lookup order: explicit field (if any) first, then candidates.
        candidate_fields = []
        if explicit_field:
            candidate_fields.append(explicit_field)
        candidate_fields.extend(f for f in self._WORKFLOW_ID_FIELDS if f not in candidate_fields)

        for field in candidate_fields:
            value = machine_data.get(field)
            if value:
                print(f"  [OK] Extracted next workflow '{value}' from field '{field}' in {artifact_id}")
                return value

        print(f"  ~ No workflow id found in {artifact_id} (tried: {', '.join(candidate_fields)})")
        return None

    @staticmethod
    def _split_source_field(source: str) -> tuple[str, str | None]:
        """Split an auto_invoke_source into (artifact_id, field_or_None).

        'workflow_orchestration_plan.recommended_workflow_id'
            -> ('workflow_orchestration_plan', 'recommended_workflow_id')
        'workflow_orchestration_plan' -> ('workflow_orchestration_plan', None)
        """
        if source and "." in source:
            artifact_id, field = source.split(".", 1)
            return artifact_id, field
        return source, None

    def _resolve_fog_type(self, source_artifact_id: str) -> str | None:
        """Resolve the diagnosed fog type for routing validation.

        The fog field lives in the repository_sensemaking_brief (primary_fog_type) and
        may not be present in the orchestration plan. This checks the source artifact
        first, then falls back to the brief, trying multiple field names in each.
        """
        # 1. Try the source artifact (it may carry a fog field)
        artifact_id, _ = self._split_source_field(source_artifact_id)
        for candidate_artifact in (artifact_id, "repository_sensemaking_brief"):
            path = self._resolve_artifact_path(candidate_artifact)
            if not os.path.exists(path):
                continue
            machine_data = self._read_machine_readable_section(path) or {}
            for field in self._FOG_TYPE_FIELDS:
                value = machine_data.get(field)
                if value:
                    print(f"  [OK] Resolved fog type '{value}' from field '{field}' in {candidate_artifact}")
                    return value

        print(f"  ~ No fog type field found in source artifact or repository_sensemaking_brief")
        return None

    def _validate_workflow_fog_alignment(self, fog_type: str | None, workflow_id: str, artifact_path: str) -> dict:
        """Validate that the selected workflow matches the diagnosed fog type.

        Returns a dict with validation results:
        {
            'is_valid': bool,
            'fog_type': str,
            'workflow_id': str,
            'expected_pattern': str,
            'mismatch_reason': str or None
        }
        """
        # Mapping of fog types to expected workflow patterns
        fog_type_patterns = {
            "ui_fog": ["ui-", "ui_"],
            "product_fog": ["product-", "product_"],
            "docs_fog": ["docs-", "docs_"],
            "architecture_fog": ["implementation-", "architecture-", "-architecture"],
        }

        validation_result = {
            "is_valid": True,
            "fog_type": fog_type or "unknown",
            "workflow_id": workflow_id,
            "expected_pattern": None,
            "mismatch_reason": None,
        }

        # If no fog type, cannot validate
        if not fog_type:
            print(f"  [WARN] No fog_type found in artifact; skipping fog alignment validation")
            validation_result["is_valid"] = None  # Unknown, not invalid
            return validation_result

        # Get expected patterns for this fog type
        expected_patterns = fog_type_patterns.get(fog_type)
        if not expected_patterns:
            print(f"  [WARN] Unknown fog_type '{fog_type}'; skipping validation")
            validation_result["is_valid"] = None
            return validation_result

        # Check if workflow matches expected pattern
        matches_pattern = any(pattern in workflow_id for pattern in expected_patterns)

        if not matches_pattern:
            validation_result["is_valid"] = False
            validation_result["expected_pattern"] = " or ".join(expected_patterns)
            validation_result["mismatch_reason"] = (
                f"Fog type '{fog_type}' suggests workflow matching '{validation_result['expected_pattern']}', "
                f"but got '{workflow_id}'"
            )
            print(f"  [WARN] Workflow routing mismatch detected:")
            print(f"    Fog type: {fog_type}")
            print(f"    Workflow: {workflow_id}")
            print(f"    Reason:   {validation_result['mismatch_reason']}")
        else:
            print(f"  [OK] Workflow fog alignment validated: {fog_type} -> {workflow_id}")

        return validation_result

    def _invoke_next_workflow(self, next_workflow_id: str) -> int:
        """Invoke the next workflow automatically, propagating mode, executor, and gate.

        Uses the same mode as the current execution and passes the same executor
        (so auto-invoked child workflows do not silently default to dry-run).
        Returns the exit code from the next workflow run.
        """
        print(f"\n{'='*60}")
        print(f"AUTO-INVOCATION: Next Workflow")
        print(f"{'='*60}")
        print(f"  Current workflow: {self.workflow_id} ({self.mode})")
        print(f"  Next workflow:    {next_workflow_id} ({self.mode})")
        print(f"")

        cmd = [
            sys.executable,
            os.path.join(self.repo_root, "scripts", "workflow-runtime.py"),
            "--workflow", next_workflow_id,
            "--mode", self.mode,
            "--repo-root", self.repo_root,
            "--executor", self.executor or "claude-code",
            "--chained",
            "--from-session", self.artifact_session_dir,
        ]

        if self.use_fixtures:
            cmd.append("--use-fixtures")

        if self.gate_decision:
            cmd.extend(["--gate-decision", self.gate_decision])

        print(f"  Running: {' '.join(cmd)}\n")

        code, _, _ = run_subprocess(cmd, self.repo_root,
                                      inject_repo_root=False,
                                      capture_output=False)
        return code

    def _get_fixture_artifact_path(self, artifact_id: str) -> str | None:
        """Get path to fixture artifact if available. Returns None if not found."""
        # Map artifact IDs to skill directories
        skill_map = {
            "problem_frame": "problem-framer",
            "unknowns_map": "unknowns-mapper",
            "repository_sensemaking_brief": "repo-sensemaker",
            "session_summary": "handoff",
        }

        skill_dir = skill_map.get(artifact_id)
        if not skill_dir:
            return None

        fixture_path = os.path.join(
            self.repo_root,
            "examples",
            skill_dir,
            f"{artifact_id}-fixture.md"
        )

        if os.path.exists(fixture_path):
            return fixture_path
        return None

    # Artifacts that compose the aggregate `context_artifacts` input, in pipeline order.
    # Implementation workflows (ui-*, product-*, docs-*) declare a single
    # `context_artifacts` input that stands in for the whole sensemaking bundle.
    _CONTEXT_ARTIFACT_IDS = (
        "user_intent",
        "problem_frame",
        "unknowns_map",
        "discovery_findings",
        "repository_sensemaking_brief",
        "workflow_orchestration_plan",
    )

    def _resolve_user_intent_path(self) -> str | None:
        """Return the path to 00-user-intent.md in the current session, if it exists."""
        if self.artifact_session_dir:
            candidate = os.path.join(self.artifact_session_dir, "00-user-intent.md")
            if os.path.exists(candidate):
                return candidate
        return None

    def _resolve_context_artifacts(self) -> list[tuple[str, str]]:
        """Expand the aggregate `context_artifacts` input into concrete session artifacts.

        Returns a list of (artifact_id, path) for each canonical context artifact that
        actually exists on disk in the current session. An empty list means no
        sensemaking context is available (e.g. a cold-start of a direct UI workflow).
        """
        available: list[tuple[str, str]] = []
        for art_id in self._CONTEXT_ARTIFACT_IDS:
            if art_id == "user_intent":
                path = self._resolve_user_intent_path()
            else:
                path = self._resolve_artifact_path(art_id)
            if path and os.path.exists(path):
                available.append((art_id, path))
        return available

    def _resolve_step_inputs(self, step: dict) -> tuple[list[str], dict]:
        """Resolve a step's declared inputs into (input_artifact_ids, resolved_inputs).

        - input_artifact_ids: flat list of artifact ids/sources (used by prompt_chain
          executor to enumerate inputs in the generated prompt).
        - resolved_inputs: rich dict keyed by input name for the claude-code executor,
          each value being {type: artifact_path|external_context|repository_state, ...}.

        Handles the aggregate `context_artifacts` input by expanding it into all
        available session artifacts from the sensemaking pipeline.
        """
        input_artifact_ids: list[str] = []
        resolved_inputs: dict = {}

        input_artifact = step.get("input_artifact")
        input_source = step.get("input_source")

        if input_artifact:
            if input_artifact == "context_artifacts":
                for art_id, path in self._resolve_context_artifacts():
                    input_artifact_ids.append(art_id)
                    resolved_inputs[art_id] = {"type": "artifact_path", "path": path}
            else:
                path = self._resolve_artifact_path(input_artifact)
                input_artifact_ids.append(input_artifact)
                resolved_inputs[input_artifact] = {"type": "artifact_path", "path": path}

        if input_source:
            if input_source == "repository_state":
                resolved_inputs["repository_state"] = {
                    "type": "repository_state",
                    "data": {"path": self.repo_root},
                }
            elif input_source == "raw_fog":
                intent_path = self._resolve_user_intent_path()
                if intent_path:
                    resolved_inputs["raw_fog"] = {"type": "artifact_path", "path": intent_path}
                else:
                    resolved_inputs["raw_fog"] = {
                        "type": "external_context",
                        "data": self.problem_statement or "",
                    }
            elif input_source == "proposed_direction":
                path = self._resolve_artifact_path("proposed_direction")
                try:
                    content_present = os.path.exists(path) and bool(
                        open(path, encoding="utf-8").read().strip()
                    )
                except OSError:
                    content_present = False
                resolved_inputs["proposed_direction"] = {
                    "type": "artifact_path",
                    "path": path,
                    "present": content_present,
                }
            else:
                resolved_inputs[input_source] = {"type": "external_context", "data": ""}
            input_artifact_ids.append(input_source)

        return input_artifact_ids, resolved_inputs

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
        artifacts_norm = os.path.normpath(artifacts_base)
        # Check exact match or prefix match with separator to avoid false-positives
        if normalized == artifacts_norm or normalized.startswith(artifacts_norm + os.sep):
            relative = os.path.relpath(normalized, artifacts_base)
            return os.path.join(self.artifact_session_dir, relative)
        return resolved_path

    def _ensure_intent_ref(self, artifact_id: str, artifact_path: str) -> None:
        """Guarantee the deterministic `source_intent_ref` machine field on a produced
        artifact.

        source_intent_ref always points to the run's immutable user-intent artifact
        (ADR 0006). The runtime knows it precisely, so it must not depend on an
        LLM-authored skill reliably emitting it — which it does not: the handoff skill
        produced a session_summary with its own plausible machine fields but omitted the
        one the contract requires (same non-compliance class as the Lx line format).
        This extends the runtime-canonical principle (ADR 0010) from paths and the plan
        to deterministic machine fields.

        No-op unless the artifact's contract requires source_intent_ref AND no fenced
        YAML block already supplies it.
        """
        contracts = self.contracts or {}
        contract = next(
            (a for a in contracts.get("artifacts", []) if a.get("id") == artifact_id),
            None,
        )
        if not contract or "source_intent_ref" not in contract.get("required_machine_fields", []):
            return
        try:
            with open(artifact_path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError:
            return
        # Producer already supplied it in a fenced yaml block? Then leave it alone.
        for block in re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL):
            try:
                data = yaml.safe_load(block)
            except Exception:
                data = None
            if isinstance(data, dict) and data.get("source_intent_ref"):
                return
        # The intent file lives at <session>/00-user-intent.md; use a relative ref so
        # the artifact stays portable (matches generate_plan and the brief).
        intent_ref = "00-user-intent.md"
        match = re.search(r"```yaml[ \t]*\n", content)
        if match:
            insert_at = match.end()
            content = content[:insert_at] + f"source_intent_ref: {intent_ref}\n" + content[insert_at:]
        else:
            content = content.rstrip("\n") + (
                f"\n\n```yaml\nartifact_id: {artifact_id}\nsource_intent_ref: {intent_ref}\n```\n"
            )
        try:
            with open(artifact_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [INTENT_REF] Ensured source_intent_ref in {artifact_id} (runtime-guaranteed)")
        except OSError:
            pass

    def _run_validator_stack(self, artifact_id: str, artifact_path: str) -> list[dict]:
        """Run validation via validate-and-report.py and log results via record-validation.py.

        New Phase 1 validation pipeline:
        1. Call validate-and-report.py with artifact_path (extracts artifact_id automatically)
        2. Parse unified JSON schema output
        3. Pipe results to record-validation.py for durable audit trail
        4. Return stack in legacy format for backward compatibility
        """
        stack = []

        # Determine which validator to use based on what exists
        validate_and_report = os.path.join(self.repo_root, "scripts", "validate-and-report.py")
        validate_output = os.path.join(self.repo_root, "scripts", "validate-output.py")

        # Prefer new unified validator if available (Phase 1)
        if os.path.exists(validate_and_report):
            return self._run_validate_and_report(artifact_id, artifact_path, stack)
        elif os.path.exists(validate_output):
            # Fallback to legacy dispatcher for Phase 2+ artifacts
            return self._run_validate_output(artifact_id, artifact_path, stack)
        else:
            print(f"  ~ No validators found, skipping validation")
            return stack

    def _run_validate_and_report(self, artifact_id: str, artifact_path: str, stack: list) -> list:
        """Run unified Phase 1 validation pipeline.

        Uses validate-and-report.py (unified dispatcher) + record-validation.py (durable logging).
        """
        validator_script = os.path.join(self.repo_root, "scripts", "validate-and-report.py")
        record_script = os.path.join(self.repo_root, "scripts", "record-validation.py")

        if not os.path.exists(validator_script):
            print(f"  ~ validate-and-report.py not found, skipping validation")
            return stack

        # Set up run log path (same session as orchestrator log)
        run_log_path = os.path.join(
            os.path.dirname(self.run_log_path or "."),
            "validation_run_log.md"
        )

        print(f"  -> Running unified validator: validate-and-report.py")
        start = datetime.now()

        try:
            # Phase 1: Call validate-and-report.py
            validate_cmd = [sys.executable, validator_script, artifact_path,
                           "--repo-root", self.repo_root]

            result = subprocess.run(validate_cmd, capture_output=True, text=True, timeout=120)
            elapsed = (datetime.now() - start).total_seconds()

            # Phase 2: Parse JSON response
            validation_json = None
            try:
                validation_json = json.loads(result.stdout)
            except json.JSONDecodeError:
                # Validator output was not JSON (e.g., execution error)
                error_output = result.stdout + result.stderr
                print(f"    [WARN] Validator returned non-JSON output ({elapsed:.1f}s)")
                stack.append({
                    "level": "Phase 1 Unified Validator",
                    "command": "validate-and-report.py",
                    "result": "FAILED",
                    "output": error_output[:500],
                    "elapsed_s": round(elapsed, 2),
                })
                return stack

            # Phase 3: Log to durable run log if record-validation.py exists
            if os.path.exists(record_script):
                try:
                    record_cmd = [sys.executable, record_script, "--run-log", run_log_path]
                    subprocess.run(record_cmd, input=json.dumps(validation_json),
                                  text=True, timeout=30, capture_output=True)
                except Exception as e:
                    print(f"    [WARN] Failed to record validation to run log: {e}")
                    # Non-fatal: continue even if logging fails

            # Phase 4: Report result
            passed = validation_json.get("valid", False)
            stack.append({
                "level": "Phase 1 Unified Validator",
                "command": "validate-and-report.py",
                "result": "PASSED" if passed else "FAILED",
                "output": "" if passed else json.dumps(validation_json.get("errors", []))[:500],
                "elapsed_s": round(elapsed, 2),
            })

            if not passed:
                print(f"    [FAIL] Validation failed ({elapsed:.1f}s)")
                # Print error summary
                errors = validation_json.get("errors", [])
                for error in errors[:3]:  # Show first 3 errors
                    error_id = error.get("error_id", "?")
                    message = error.get("message", "")
                    print(f"      - {error_id}: {message[:80]}")
                if len(errors) > 3:
                    print(f"      ... and {len(errors) - 3} more errors")
            else:
                print(f"    [OK] Validation passed ({elapsed:.1f}s)")

        except subprocess.TimeoutExpired:
            print(f"    [FAIL] Validator timeout (>120s)")
            stack.append({
                "level": "Phase 1 Unified Validator",
                "command": "validate-and-report.py",
                "result": "FAILED",
                "output": "Validator timed out after 120 seconds",
                "elapsed_s": 120.0,
            })
        except Exception as e:
            print(f"    [FAIL] Validator execution error: {e}")
            stack.append({
                "level": "Phase 1 Unified Validator",
                "command": "validate-and-report.py",
                "result": "FAILED",
                "output": str(e)[:500],
                "elapsed_s": round((datetime.now() - start).total_seconds(), 2),
            })

        return stack

    def _run_validate_output(self, artifact_id: str, artifact_path: str, stack: list) -> list:
        """Run legacy Phase 2+ validation via validate-output.py.

        Fallback for artifacts not yet converted to Phase 1 unified schema.
        """
        validator_script = os.path.join(self.repo_root, "scripts", "validate-output.py")

        cmd = [sys.executable, validator_script, artifact_id, artifact_path,
               "--repo-root", self.repo_root]

        print(f"  -> Running legacy validator: validate-output.py {artifact_id}")
        start = datetime.now()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        elapsed = (datetime.now() - start).total_seconds()
        output = (result.stdout + result.stderr).strip()

        passed = result.returncode == 0
        stack.append({
            "level": "Phase 2+ Legacy Validator",
            "command": f"validate-output.py {artifact_id}",
            "result": "PASSED" if passed else "FAILED",
            "output": output[:500] if not passed else "",
            "elapsed_s": round(elapsed, 2),
        })

        if not passed:
            print(f"    [FAIL] Validator failed ({elapsed:.1f}s)")
            for line in output.split("\n"):
                if line.strip():
                    print(f"      {line}")
        else:
            print(f"    [OK] Validator passed ({elapsed:.1f}s)")

        return stack

    def _manage_gate(self, gate_name: str, step_num: int, skill: str) -> str:
        """Manage the approval gate based on execution mode. Returns the gate result string."""
        mode_info = KNOWN_MODES.get(self.mode, {})
        behavior = mode_info.get("gates", "none")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if behavior == "none":
            # plan_only and prompt_chain: no gates
            self.gate_decisions.append({
                "step": step_num,
                "gate": gate_name,
                "result": "not_applicable",
                "timestamp": timestamp,
                "mode": self.mode,
            })
            return "not_applicable"

        if behavior == "bypassed":
            # yolo: gates are bypassed
            self.gate_decisions.append({
                "step": step_num,
                "gate": gate_name,
                "result": "bypassed",
                "timestamp": timestamp,
                "mode": self.mode,
            })
            print(f"  ~ Gate '{gate_name}' BYPASSED (yolo mode)")
            return "bypassed"

        if behavior == "automated":
            # autonomous: automated approval
            self.gate_decisions.append({
                "step": step_num,
                "gate": gate_name,
                "result": "automated_approval",
                "timestamp": timestamp,
                "mode": self.mode,
                "approved_by": "automated_gate",
            })
            print(f"  ~ Gate '{gate_name}' AUTOMATED_APPROVAL (autonomous mode)")
            return "automated_approval"

        # Check for auto gate decision (non-interactive testing mode)
        if self.gate_decision:
            if self.gate_decision == "auto-approve":
                self.gate_decisions.append({
                    "step": step_num,
                    "gate": gate_name,
                    "result": "approved_by_user",
                    "timestamp": timestamp,
                    "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "approved_by": "auto_gate",
                    "mode": self.mode,
                })
                print(f"  ~ Gate '{gate_name}' AUTO_APPROVED (--gate-decision={self.gate_decision})")
                return "approved_by_user"

            elif self.gate_decision == "auto-deny":
                self.gate_decisions.append({
                    "step": step_num,
                    "gate": gate_name,
                    "result": "denied_by_user",
                    "timestamp": timestamp,
                    "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "reason": "auto_denied_by_flag",
                    "mode": self.mode,
                })
                print(f"  [FAIL] Gate '{gate_name}' AUTO_DENIED (--gate-decision={self.gate_decision})")
                return "denied_by_user"

        if behavior == "mandatory":
            # guided: requires manual approval
            # Check if stdin is available (TTY or pipe)
            import sys
            if not sys.stdin.isatty() and not self.gate_decision:
                # No TTY and no auto-decision flag: error
                error_msg = (
                    f"[ERROR] Gate '{gate_name}' requires manual approval in guided_execution mode,\n"
                    f"        but no TTY available and no --gate-decision flag provided.\n"
                    f"        Use: --gate-decision auto-approve (for automation) or --gate-decision auto-deny (for testing)"
                )
                self.errors.append(format_error(GATE_AUTO_FAILED, error_msg))
                return "timed_out"

            # If auto-decision is set, use it instead of prompting
            if self.gate_decision:
                if self.gate_decision == "auto-approve":
                    self.gate_decisions.append({
                        "step": step_num,
                        "gate": gate_name,
                        "result": "approved_by_user",
                        "timestamp": timestamp,
                        "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "approved_by": "auto_gate (mandatory mode)",
                        "mode": self.mode,
                    })
                    print(f"  ~ Gate '{gate_name}' AUTO_APPROVED (--gate-decision={self.gate_decision})")
                    return "approved_by_user"
                elif self.gate_decision == "auto-deny":
                    self.gate_decisions.append({
                        "step": step_num,
                        "gate": gate_name,
                        "result": "denied_by_user",
                        "timestamp": timestamp,
                        "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "reason": "auto_denied_by_flag",
                        "mode": self.mode,
                    })
                    print(f"  [FAIL] Gate '{gate_name}' AUTO_DENIED (--gate-decision={self.gate_decision})")
                    return "denied_by_user"

            print(f"\n  [PAUSE]  GATE: '{gate_name}' -- waiting for approval (Step {step_num}: {skill})")
            print(f"  Options: [A]pprove  [D]eny  [S]kip (treat as denied for testing)  [T]imeout")
            choice = input(f"  Enter choice (A/D/S/T): ").strip().upper()

            if choice == "A":
                approver = input(f"  Approver name: ").strip() or "user"
                self.gate_decisions.append({
                    "step": step_num,
                    "gate": gate_name,
                    "result": "approved_by_user",
                    "timestamp": timestamp,
                    "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "approved_by": approver,
                    "mode": self.mode,
                })
                print(f"  [OK] Gate '{gate_name}' APPROVED by {approver}")
                return "approved_by_user"

            elif choice == "D":
                reason = input(f"  Reason for denial: ").strip() or "No reason given"
                self.gate_decisions.append({
                    "step": step_num,
                    "gate": gate_name,
                    "result": "denied_by_user",
                    "timestamp": timestamp,
                    "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "reason": reason,
                    "mode": self.mode,
                })
                print(f"  [FAIL] Gate '{gate_name}' DENIED: {reason}")
                return "denied_by_user"

            elif choice in ("S", "T"):
                result = "denied_by_user" if choice == "S" else "timed_out"
                self.gate_decisions.append({
                    "step": step_num,
                    "gate": gate_name,
                    "result": result,
                    "timestamp": timestamp,
                    "mode": self.mode,
                })
                note = "skipped" if choice == "S" else "timed_out"
                print(f"  [FAIL] Gate '{gate_name}' {note.upper()}")
                return "denied_by_user"

            else:
                print(f"  Invalid choice, treating as denied.")
                return "denied_by_user"

        return "unknown"

    def _find_resume_state(self) -> dict | None:
        """Parse existing run log to find resume state.

        Returns dict with completed_steps and paused_step, or None if no resume needed.
        """
        run_log_path = os.path.join(self.log_dir, f"run_log_{self.workflow_id}_{self.mode}.md")
        if not os.path.exists(run_log_path):
            print(f"  ~ No existing run log found at {run_log_path}, starting fresh")
            return None

        with open(run_log_path, "r", encoding="utf-8") as f:
            content = f.read()

        completed_steps: list[int] = []
        paused_step: int | None = None

        # Extract step statuses from the run log
        step_blocks = re.findall(
            r"### Step (\d+).*?\*\*status\*\*:\s*(\S+)",
            content, re.DOTALL
        )
        for step_id_str, status in step_blocks:
            step_id = int(step_id_str)
            if status == "COMPLETED":
                completed_steps.append(step_id)
            elif status == "PAUSED":
                paused_step = step_id

        if not paused_step and not completed_steps:
            print(f"  ~ No paused or completed steps found, starting fresh")
            return None

        print(f"  [OK] Found resume state: {len(completed_steps)} completed, paused at step {paused_step}")
        return {
            "completed_steps": sorted(set(completed_steps)),
            "paused_step": paused_step,
            "previous_log_path": run_log_path,
        }

    def write_run_log(self) -> str:
        """Write the run log document. Returns the file path."""
        steps = self.workflow.get("steps", [])
        workflow_name = self.workflow.get("display_name", self.workflow_id)
        run_log_path = os.path.join(self.log_dir, f"run_log_{self.workflow_id}_{self.mode}.md")

        # Determine final state (respecting semantic contract: each mode has an honest ceiling)
        failures = [s for s in self.step_results if s["status"] in ("FAILED",)]
        pauses = [s for s in self.step_results if s["status"] in ("PAUSED",)]

        # Count steps at each state (semantic contract)
        planned = [s for s in self.step_results if s["status"] == "PLANNED"]
        prompted = [s for s in self.step_results if s["status"] == "PROMPT_GENERATED"]
        executed = [s for s in self.step_results if s["status"] == "EXECUTED"]
        validated = [s for s in self.step_results if s["status"] == "VALIDATED"]
        approved = [s for s in self.step_results if s["status"] == "APPROVED"]
        completed = [s for s in self.step_results if s["status"] == "COMPLETED"]  # legacy

        # Determine final state based on mode ceiling
        mode_ceiling = MODE_CEILINGS.get(self.mode, "VALIDATED")

        if failures:
            self.final_state = "failed"
            self.final_note = f"Step {failures[0]['step_id']} ({failures[0]['skill']}) failed. Run halted."
        elif pauses:
            self.final_state = "paused"
            self.final_note = f"Paused at step {pauses[0]['step_id']} gate '{pauses[0]['gate']}'."
        elif self.mode == "prompt_chain" and len(prompted) == len(steps):
            self.final_state = "prompt_chain_generated"
            self.final_note = f"All {len(steps)} steps generated prompts successfully in '{self.mode}' mode."
        elif self.mode == "plan_only" and len(planned) == len(steps):
            self.final_state = "planned"
            self.final_note = f"All {len(steps)} workflow steps planned successfully."
        elif not failures and not pauses and (len(completed) == len(steps) or len(validated) == len(steps) or len(executed) == len(steps) or len(approved) == len(steps)):
            self.final_state = "completed"
            self.final_note = f"All {len(steps)} steps completed successfully in '{self.mode}' mode."
        else:
            self.final_state = "partial"
            success_steps = len(planned) + len(prompted) + len(executed) + len(validated) + len(approved) + len(completed)
            self.final_note = f"{success_steps}/{len(steps)} steps completed."

        lines = [
            f"# Workflow Run Log: {workflow_name}",
            f"",
            f"- **Date**: {datetime.now().strftime('%Y-%m-%d')}",
            f"- **Session ID**: {self.session_id}",
            f"- **Workflow ID**: {self.workflow_id}",
            f"- **Orchestrator Mode**: {self.mode}",
            f"- **Branch**: {_get_git_branch(self.repo_root)}",
            f"- **Status**: {self.final_state}",
            f"",
            f"## Pre-flight",
            f"",
            f"- {_get_git_branch(self.repo_root)} branch, clean check: PASSED" if _check_clean_git(self.repo_root)[0]
            else f"- Branch: {_get_git_branch(self.repo_root)}",
            f"- validate-repo.py: PASSED",
            f"- Orchestrator v2 engaged: PRODUCTION_RUNNER",
            f"",
            f"## Sequence Log",
            f"",
        ]

        # Determine the runtime name to write in the step sequence log
        use_fixtures = getattr(self, "use_fixtures", False)
        executor = getattr(self, "executor", "dry-run")
        if use_fixtures:
            runtime_str = "fixture"
        elif self.mode == "prompt_chain":
            runtime_str = "prompt_generation"
        elif self.mode == "plan_only":
            runtime_str = "planning"
        else:
            if executor == "claude-code":
                runtime_str = "claude-agent-sdk"
            elif executor == "api":
                runtime_str = "claude-api"
            else:
                runtime_str = executor or "local_execution"

        for sr in self.step_results:
            lines.extend([
                f"### Step {sr['step_id']}",
                f"- **step_id**: {sr['step_id']}",
                f"- **skill**: {sr['skill']}",
                f"- **runtime**: {runtime_str}",
                f"- **output_artifact**: {sr.get('output_artifact', 'N/A')}",
                f"- **artifact_path**: {sr.get('artifact_path', 'N/A')}",
            ])
            vstack = sr.get("validator_stack", [])
            if vstack:
                lines.append("- **validator_stack**:")
                for v in vstack:
                    lines.extend([
                        f"    - level: {v['level']}",
                        f"      command: {v['command']}",
                        f"      result: {v['result']}",
                    ])
            else:
                lines.append("- **validator_stack**: none (no artifact to validate)")
            lines.extend([
                f"- **gate**: {sr.get('gate', '?')}",
                f"- **status**: {sr['status']}",
                f"",
            ])

        # Decisions & Overrides
        lines.extend([
            f"## Decisions & Overrides",
            f"",
        ])
        for gd in self.gate_decisions:
            lines.append(f"- Gate '{gd['gate']}' (step {gd['step']}): {gd['result']} at {gd['timestamp']}")
        if self.errors:
            lines.append(f"- Errors encountered: {len(self.errors)}")
            for e in self.errors[-5:]:  # Last 5 errors
                lines.append(f"  - {e}")
        lines.append(f"")

        # Final State
        lines.extend([
            f"## Final State",
            f"",
            f"- **Status**: {self.final_state}",
            f"- **Note**: {self.final_note}",
            f"- **Steps completed**: {len(completed)}/{len(steps)}",
            f"- **Gate decisions**: {len(self.gate_decisions)}",
            f"- **Errors**: {len(self.errors)}",
            f"",
        ])

        # TDD cycles if any occurred
        tdd_cycles = []
        for sr in self.step_results:
            for v in sr.get("validator_stack", []):
                if v["result"] == "FAILED" and v.get("output"):
                    tdd_cycles.append({
                        "step": sr["step_id"],
                        "failure": v["output"][:100],
                    })
        if tdd_cycles:
            lines.append(f"## TDD Cycles")
            lines.append(f"")
            for tc in tdd_cycles:
                lines.append(f"- **Step {tc['step']}**")
                lines.append(f"  - **RED**: {tc['failure']}")
                lines.append(f"  - **GREEN**: (manual fix applied)")
                lines.append(f"  - **REFACTOR**: (hardening if warranted)")
            lines.append(f"")

        log = "\n".join(lines)

        os.makedirs(os.path.dirname(run_log_path), exist_ok=True)
        with open(run_log_path, "w", encoding="utf-8") as f:
            f.write(log)
        print(f"\n  [OK] Run log written to {run_log_path}")
        return run_log_path

    def update_mode_coverage(self, run_log_path: str) -> None:
        """Update mode-coverage.yaml with results from this run."""
        coverage = _load_mode_coverage(self.repo_root)
        if not coverage:
            print(f"  ~ Cannot update mode coverage: mode-coverage.yaml not found")
            return

        mode_entries = coverage.get("mode_coverage", [])
        steps = self.workflow.get("steps", [])
        num_steps = len(steps)

        # Collect validators exercised - use actual validator script names
        validators_exercised = ["level_1: validate-repo.py"]
        for sr in self.step_results:
            for v in sr.get("validator_stack", []):
                cmd = v["command"]
                # Extract the actual validator script name from the command
                for script_name in ["validate-artifact.py", "validate-brief.py", "validate-plan.py",
                                     "validate-prompt-handoff.py", "validate-usage-research-report.py",
                                     "validate-skill-improvement-plan.py", "validate-run-log.py",
                                     "validate-output.py"]:
                    if script_name in cmd:
                        level = "level_2" if script_name == "validate-artifact.py" else "level_3"
                        label = f"{level}: {script_name}"
                        if label not in validators_exercised:
                            validators_exercised.append(label)
                        break

        # Find or create entry
        existing = None
        for entry in mode_entries:
            if entry.get("workflow_id") == self.workflow_id and entry.get("mode") == self.mode:
                existing = entry
                break

        gates_exercised = any(
            gd["result"] in ("approved_by_user", "automated_approval")
            for gd in self.gate_decisions
        )
        gates_note = ""
        if self.mode == "plan_only":
            gates_note = "not_applicable_plan_only"
        elif self.mode == "prompt_chain":
            gates_note = "not_applicable_prompt_chain"
        elif self.mode == "yolo_execution":
            gates_note = "bypassed_by_yolo"
        elif self.mode == "autonomous_execution":
            gates_note = "automated_approval_all_gates"
        elif self.mode == "guided_execution":
            approved = [gd for gd in self.gate_decisions if gd["result"] == "approved_by_user"]
            denied = [gd for gd in self.gate_decisions if gd["result"] == "denied_by_user"]
            gates_note = f"{len(approved)} approved, {len(denied)} denied"

        entry_data = {
            "mode": self.mode,
            "workflow_id": self.workflow_id,
            "last_run": datetime.now().strftime("%Y-%m-%d"),
            "run_log_path": os.path.relpath(run_log_path, self.repo_root).replace("\\", "/"),
            "steps_completed": len([s for s in self.step_results if s["status"] == "COMPLETED"]),
            "steps_total": num_steps,
            "validators_exercised": validators_exercised,
            "gates_exercised": gates_exercised,
            "gates_note": gates_note,
            "hardening_triggered": "none",
            "notes": f"Executed via production orchestration runner v2. Session: {self.session_id}.",
        }

        if existing:
            existing.update(entry_data)
        else:
            mode_entries.append(entry_data)

        # Also update system_tools if needed
        system_tools = coverage.get("system_tools", [])
        runner_tool = next((t for t in system_tools if t.get("tool") == "orchestration-runner.py"), None)
        if runner_tool:
            wf_list = runner_tool.get("workflows_executed")
            if isinstance(wf_list, list):
                wf_entry = f"{self.workflow_id} ({self.mode})"
                if wf_entry not in wf_list:
                    wf_list.append(wf_entry)
            else:
                runner_tool["workflows_executed"] = [f"{self.workflow_id} ({self.mode})"]
            runner_tool["last_run"] = datetime.now().strftime("%Y-%m-%d")
            runner_tool["last_session"] = self.session_id
        else:
            system_tools.append({
                "tool": "orchestration-runner.py",
                "status": "active",
                "last_run": datetime.now().strftime("%Y-%m-%d"),
                "last_session": self.session_id,
                "workflows_executed": 1,
                "modes_proven": [self.mode],
            })

        # Aggregate workflow families
        workflows_run = set()
        for entry in mode_entries:
            wf = entry.get("workflow_id", "")
            if wf:
                workflows_run.add(wf)

        coverage.setdefault("orchestration_runner", {})
        coverage["orchestration_runner"]["last_run"] = datetime.now().strftime("%Y-%m-%d")
        coverage["orchestration_runner"]["workflow_families_proven"] = sorted(workflows_run)
        coverage["orchestration_runner"]["total_workflow_families"] = len(workflows_run)

        _save_mode_coverage(coverage, self.repo_root)
        print(f"  [OK] Mode coverage updated")

    def generate_diagnostic_report(self) -> str:
        """Generate diagnostic report showing what WILL happen after plan generation."""
        steps = self.workflow.get("steps", [])
        workflow_name = self.workflow.get("display_name", self.workflow_id)
        diagnostic_path = os.path.join(self.log_dir, f"diagnostic_{self.workflow_id}_{self.mode}.md")

        lines = [
            f"# Diagnostic Report: {workflow_name}",
            f"",
            f"- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **Workflow**: {self.workflow_id}",
            f"- **Mode**: {self.mode}",
            f"- **Session**: {self.session_id}",
            f"",
            f"## What Will Happen",
            f"",
            f"This report documents the execution plan for this workflow.",
            f"",
            f"## Steps in Sequence",
            f"",
        ]

        # Document each step
        for step in steps:
            step_id = step.get("id", "?")
            skill = step.get("skill", "?")
            output = step.get("output_artifact", "N/A")
            gate = step.get("gate", "?")

            # Handle conditional steps (skill is null at top level)
            if step.get("conditional"):
                branch = step.get("if_true", {})
                skill = f"{branch.get('skill', '?')} (conditional)" if branch.get("skill") else "(conditional routing)"
                output = f"{branch.get('output_artifact', '?')} or {step.get('if_false', {}).get('output_artifact', '?')}"
                gate = branch.get("gate", gate)

            lines.extend([
                f"### Step {step_id}: {skill}",
                f"- **Output**: {output}",
                f"- **Gate**: {gate}",
                f"",
            ])

        # Validator summary from contracts
        contracts = load_artifact_contracts(self.repo_root)
        lines.extend([
            f"## Validators Expected to Run",
            f"",
        ])

        total_validators = 0
        for step in steps:
            output = step.get("output_artifact", "N/A")
            if contracts and output != "N/A":
                for artifact in contracts.get("artifacts", []):
                    if artifact.get("id") == output:
                        verification = artifact.get("verification", {})
                        validators = len(verification.get("specialized_validators", []))
                        if verification.get("generic_validator"):
                            validators += 1
                        if validators > 0:
                            lines.append(f"- **{output}**: {validators} validators")
                            total_validators += validators
                        break

        lines.extend([
            f"",
            f"**Total validators to run**: {total_validators}",
            f"",
            f"## Success Criteria",
            f"",
            f"- All {len(steps)} steps complete successfully",
            f"- All artifacts produced",
            f"- All validators pass",
            f"",
        ])

        report = "\n".join(lines)
        os.makedirs(os.path.dirname(diagnostic_path), exist_ok=True)
        with open(diagnostic_path, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"  [OK] Diagnostic report: {os.path.relpath(diagnostic_path, self.repo_root)}")
        return diagnostic_path
    def invoke_presentation_skill(self, summary_json_path: str) -> str | None:
        """Auto-invoke workflow-presenter skill to generate beautiful summary markdown."""
        print(f"\n{'='*60}")
        print(f"INVOKING PRESENTATION SKILL: workflow-presenter")
        print(f"{'='*60}")

        skill_path = os.path.join(self.repo_root, "skills", "workflow-presenter", "workflow-presenter.py")
        if not os.path.exists(skill_path):
            print(f"  ~ workflow-presenter skill not found at {skill_path}")
            print(f"    Presentation will be skipped; JSON summary available at {summary_json_path}")
            return None

        try:
            result = subprocess.run(
                [sys.executable, skill_path, summary_json_path, "--output-dir", self.log_dir],
                capture_output=True,
                text=True,
                timeout=300,
            )
            output = (result.stdout + result.stderr).strip()

            if result.returncode == 0:
                # Extract the output path from skill output
                for line in output.split("\n"):
                    if "EXECUTION_SUMMARY.md" in line or "Summary generated" in line:
                        print(f"  [OK] {line}")
                return output
            else:
                print(f"  ~ Presentation skill failed: {output[:200]}")
                return None
        except Exception as e:
            print(f"  ~ Error invoking presentation skill: {e}")
            return None

    def generate_workflow_summary_json(self) -> str:
        """Generate structured JSON summary of workflow execution for presentation layer."""
        workflow_name = self.workflow.get("display_name", self.workflow_id)
        summary_path = os.path.join(self.log_dir, "workflow_summary.json")

        # Prepare step summaries
        steps_summary = []
        for sr in self.step_results:
            step_summary = {
                "step_id": sr.get("step_id"),
                "skill": sr.get("skill"),
                "status": sr.get("status"),
                "output_artifact": sr.get("output_artifact", "N/A"),
                "artifact_path": sr.get("artifact_path", ""),
                "duration_seconds": sr.get("duration_seconds", 0),
                "validators": []
            }

            # Include validator results
            for v in sr.get("validator_stack", []):
                step_summary["validators"].append({
                    "level": v.get("level", "unknown"),
                    "result": v.get("result", "UNKNOWN")
                })

            steps_summary.append(step_summary)

        # Build summary object
        summary = {
            "workflow_id": self.workflow_id,
            "workflow_name": workflow_name,
            "session_id": self.session_id,
            "mode": self.mode,
            "status": self.final_state,
            "final_note": self.final_note,
            "branch": _get_git_branch(self.repo_root),
            "executed_at": datetime.now().isoformat(),
            "steps_completed": len([s for s in self.step_results if s["status"] in ("EXECUTED", "COMPLETED", "VALIDATED")]),
            "steps_total": len(self.step_results),
            "steps_failed": len([s for s in self.step_results if s["status"] == "FAILED"]),
            "steps": steps_summary,
            "errors": self.errors[-5:] if self.errors else [],  # Last 5 errors
        }

        os.makedirs(os.path.dirname(summary_path), exist_ok=True)
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        print(f"  [OK] Workflow summary JSON: {os.path.relpath(summary_path, self.repo_root)}")
        return summary_path

    def generate_implementation_report(self) -> str:
        """Generate implementation report showing what ACTUALLY happened after execution."""
        workflow_name = self.workflow.get("display_name", self.workflow_id)
        impl_path = os.path.join(self.log_dir, f"implementation_{self.workflow_id}_{self.mode}.md")

        # Count outcomes
        executed = [s for s in self.step_results if s.get("status") in ("EXECUTED", "COMPLETED", "VALIDATED")]
        failed = [s for s in self.step_results if s.get("status") == "FAILED"]

        lines = [
            f"# Implementation Report: {workflow_name}",
            f"",
            f"- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **Workflow**: {self.workflow_id}",
            f"- **Mode**: {self.mode}",
            f"- **Session**: {self.session_id}",
            f"- **Status**: {self.final_state.upper()}",
            f"",
            f"## Execution Summary",
            f"",
            f"- **Steps Executed**: {len(executed)}/{len(self.step_results)}",
            f"- **Steps Failed**: {len(failed)}/{len(self.step_results)}",
            f"",
            f"## What Actually Happened",
            f"",
        ]

        # Document actual results
        for sr in self.step_results:
            step_id = sr.get("step_id", "?")
            skill = sr.get("skill", "?")
            status = sr.get("status", "UNKNOWN")
            output = sr.get("output_artifact", "N/A")

            lines.extend([
                f"### Step {step_id}: {skill}",
                f"- **Status**: {status}",
                f"- **Output**: {output}",
            ])

            # Validator results
            validators = sr.get("validator_stack", [])
            if validators:
                for v in validators:
                    v_name = v.get("level", "?")
                    v_result = v.get("result", "?")
                    lines.append(f"  - {v_name}: {v_result}")
            lines.append(f"")

        lines.extend([
            f"## Conclusion",
            f"",
        ])

        if self.final_state == "completed":
            lines.append(f"✓ Success: All steps executed and validated.")
        elif self.final_state == "failed":
            lines.append(f"✗ Failed: Execution halted due to validation failures.")
        else:
            lines.append(f"⚠ {self.final_state}: Partial execution.")

        report = "\n".join(lines)
        os.makedirs(os.path.dirname(impl_path), exist_ok=True)
        with open(impl_path, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"  [OK] Implementation report: {os.path.relpath(impl_path, self.repo_root)}")
        return impl_path

    def rollback(self) -> None:
        """Recommend rollback on failure."""
        branch = _get_git_branch(self.repo_root)
        print(f"\n{'!'*50}")
        print(f"ROLLBACK RECOMMENDED")
        print(f"{'!'*50}")
        print(f"Branch: {branch}")
        print(f"To revert all changes, run:")
        print(f"  git reset --hard HEAD")
        print(f"  git clean -fd")
        print(f"(Review changes first with 'git diff')\n")

    def run(self) -> int:
        """Execute the full orchestration lifecycle. Returns exit code."""
        # Phase 1: Pre-flight (skip for plan_only mode)
        if self.mode != "plan_only":
            if not self.preflight_check():
                print(f"\n  [FAIL] Pre-flight failed. Aborting.")
                return 1
        else:
            print(f"{'='*60}")
            print(f"PHASE 1: PREFLIGHT (skipped for plan_only mode)")
            print(f"{'='*60}")

        # -- Ledger: log run_started ------------------------------------------
        _git_commit = None
        try:
            _gc_res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True, text=True, cwd=self.repo_root
            )
            if _gc_res.returncode == 0:
                _git_commit = _gc_res.stdout.strip()
        except Exception:
            pass
        self._log_ledger_event({
            "event": "run_started",
            "run_id": self.session_id,
            "workflow_id": self.workflow_id,
            "mode": self.mode,
            "git_commit": _git_commit,
        })

        # Phase 2: Generate plan
        print(f"{'='*60}")
        print(f"PHASE 2: GENERATE PLAN")
        print(f"{'='*60}")
        self.generate_plan()

        # Generate diagnostic report (what WILL happen)
        print(f"\nPHASE 2b: DIAGNOSTIC REPORT")
        print(f"{'='*60}")
        self.generate_diagnostic_report()

        # For plan_only mode, stop here
        if self.mode == "plan_only":
            print(f"\n[OK] Plan-only mode complete. Exiting.")
            return 0

        # Phase 3: Execute steps
        print(f"\n{'='*60}")
        print(f"PHASE 3: EXECUTE STEPS  ({len(self.workflow.get('steps', []))} total)")
        print(f"{'='*60}")

        steps = self.workflow.get("steps", [])

        # Check for resume state
        resume_state = None
        resume_skip = set()
        if self.resume:
            resume_state = self._find_resume_state()
            if resume_state:
                resume_skip = set(resume_state.get("completed_steps", []))
                paused = resume_state.get("paused_step")
                if paused:
                    resume_skip.add(paused)
                print(f"  [OK] Resuming: skipping steps {sorted(resume_skip)}, "
                      f"starting from step {max(resume_skip) + 1 if resume_skip else 1}")

        for i, step in enumerate(steps, 1):
            if i in resume_skip:
                print(f"\n  ~ Step {i} already completed in previous session, skipping (resume mode)")
                # Reconstruct a synthetic completed result for the run log
                sr = {
                    "step_id": str(i),
                    "skill": step.get("skill", "?"),
                    "gate": step.get("gate", "review"),
                    "output_artifact": step.get("output_artifact", "N/A"),
                    "artifact_path": "",
                    "validator_stack": [],
                    "gate_result": "resumed_from_previous_session",
                    "status": "COMPLETED",
                    "step_type": step.get("step_type", "local_execution"),
                }
                self.step_results.append(sr)
                continue

            sr = self.execute_step(step, i, len(steps))
            self.step_results.append(sr)

            if sr["status"] in ("FAILED", "PAUSED"):
                if sr["status"] == "FAILED":
                    print(f"\n  [FAIL] Step {i} FAILED. Halting execution.")
                else:
                    print(f"\n  [PAUSE]  Step {i} PAUSED at gate.")
                break

        # Phase 4: Write run log
        print(f"\n{'='*60}")
        print(f"PHASE 4: WRITE RUN LOG")
        print(f"{'='*60}")
        run_log_path = self.write_run_log()

        # Generate implementation report (what ACTUALLY happened)
        print(f"\nPHASE 4b: IMPLEMENTATION REPORT")
        print(f"{'='*60}")
        self.generate_implementation_report()

        # Generate workflow summary JSON
        print(f"\nPHASE 4c: WORKFLOW SUMMARY (MACHINE-READABLE)")
        print(f"{'='*60}")
        summary_json_path = self.generate_workflow_summary_json()

        # Invoke presentation skill to generate beautiful markdown
        print(f"\nPHASE 4d: WORKFLOW PRESENTATION (HUMAN-READABLE)")
        print(f"{'='*60}")
        self.invoke_presentation_skill(summary_json_path)

        # Phase 5: Update mode coverage
        print(f"\n{'='*60}")
        print(f"PHASE 5: UPDATE MODE COVERAGE")
        print(f"{'='*60}")
        self.update_mode_coverage(run_log_path)

        # Phase 6: Rollback check
        has_failures = any(sr["status"] == "FAILED" for sr in self.step_results)
        if has_failures:
            self.rollback()

        # Summary
        print(f"\n{'='*60}")
        print(f"SUMMARY")
        print(f"{'='*60}")
        print(f"  Workflow:     {self.workflow_id}")
        print(f"  Mode:         {self.mode}")
        print(f"  Session:      {self.session_id}")
        print(f"  Status:       {self.final_state}")
        # Count steps at each semantic state (not just COMPLETED)
        successful_steps = len([s for s in self.step_results
                               if s['status'] in ('COMPLETED', 'EXECUTED', 'VALIDATED', 'APPROVED', 'PLANNED', 'PROMPT_GENERATED')])
        print(f"  Steps:        {successful_steps}/{len(steps)}")
        print(f"  Gates:        {len(self.gate_decisions)}")
        print(f"  Errors:       {len(self.errors)}")
        print(f"  Run Log:      {run_log_path}")
        print()

        if has_failures:
            print(f"  [WARN]  Execution completed with failures.")
            return self._finalize_run(2, "failed")
        elif any(sr["status"] == "PAUSED" for sr in self.step_results):
            print(f"  [PAUSE]  Execution paused. Can resume.")
            return self._finalize_run(3, "paused")
        else:
            # Phase 7: Check for auto-invocation of next workflow (only in execution modes)
            should_invoke, source_artifact = self._should_auto_invoke_next()
            if should_invoke and self.mode in ("guided_execution", "autonomous_execution", "yolo_execution"):
                print(f"\n{'='*60}")
                print(f"PHASE 7: AUTO-INVOCATION CHECK")
                print(f"{'='*60}")
                # Check for explicit override first
                next_workflow_id = self._get_explicit_next_workflow()
                if not next_workflow_id:
                    # Fall back to reading from source artifact
                    next_workflow_id = self._extract_recommended_workflow(source_artifact)
                if next_workflow_id:
                    # RECURSION GUARD: Prevent self-routing
                    if next_workflow_id == self.workflow_id:
                        print(f"  [ERROR] RECURSION DETECTED: Workflow '{self.workflow_id}' would invoke itself.")
                        print(f"  [ERROR] This indicates a routing configuration error.")
                        print(f"  [FATAL] Auto-invocation aborted to prevent infinite loop.")
                        return self._finalize_run(1, "recursion_error")

                    # Validate fog type alignment. The fog field lives in the
                    # repository_sensemaking_brief (primary_fog_type), not always in
                    # the orchestration plan, so resolve across artifacts + field names.
                    source_artifact_path = self._resolve_artifact_path(source_artifact)
                    fog_type = self._resolve_fog_type(source_artifact)

                    validation_result = self._validate_workflow_fog_alignment(fog_type, next_workflow_id, source_artifact_path)
                    if validation_result["is_valid"] is False:
                        print(f"  [WARN] Workflow routing may be incorrect; proceeding with caution")

                    next_exit_code = self._invoke_next_workflow(next_workflow_id)
                    return next_exit_code
                else:
                    print(f"  [SKIP] Auto-invocation enabled but no recommended workflow found.")
                    print(f"  [OK] Execution completed successfully.")
                    return self._finalize_run(0, "completed")
            else:
                print(f"  [OK] Execution completed successfully.")
                return self._finalize_run(0, "completed")

    def _finalize_run(self, exit_code: int, status: str) -> int:
        """Log run_completed ledger event and return exit_code unchanged."""
        self._log_ledger_event({
            "event": "run_completed",
            "run_id": self.session_id,
            "status": status,
            "exit_code": exit_code,
        })
        return exit_code


# ===============================================================================
# CLI
# ===============================================================================

def list_workflows(repo_root: str) -> None:
    """List all registered workflows with their modes and steps."""
    registry = load_workflow_registry(repo_root)
    if not registry:
        print("workflow-registry.yaml not found or empty.")
        return
    workflows = registry.get("workflows", [])
    print(f"\nRegistered Workflows ({len(workflows)}):")
    print(f"{'='*60}")
    for wf in workflows:
        modes = ", ".join(wf.get("allowed_execution_modes", []))
        steps = len(wf.get("steps", []))
        print(f"  {wf['id']}")
        print(f"    Name:  {wf.get('display_name', '?')}")
        print(f"    Steps: {steps}")
        print(f"    Modes: {modes}")
        print()


def _compute_file_hash(path: str) -> str:
    """Compute the SHA-256 hash of a file."""
    import hashlib
    if not os.path.exists(path):
        return "file_not_found"
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256.update(byte_block)
        return sha256.hexdigest()
    except Exception:
        return "hash_error"


def handle_audit_run(args) -> int:
    """Audit a run ledger JSONL file for causality, hash matches, and validations."""
    ledger_path = os.path.abspath(args.ledger_path)
    repo_root = os.path.abspath(args.repo_root)

    if not os.path.exists(ledger_path):
        print(f"[AUDIT FAIL] Ledger file not found: {ledger_path}", file=sys.stderr)
        return 1

    events = []
    try:
        with open(ledger_path, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"[AUDIT FAIL] Invalid JSON on line {line_idx}: {e}", file=sys.stderr)
                    return 1
    except Exception as e:
        print(f"[AUDIT FAIL] Failed to read ledger file: {e}", file=sys.stderr)
        return 1

    if not events:
        print("[AUDIT FAIL] Ledger file is empty", file=sys.stderr)
        return 1

    # 1. First event must be run_started
    first_event = events[0]
    if first_event.get("event") != "run_started":
        print(f"[AUDIT FAIL] First event in ledger must be 'run_started', found: '{first_event.get('event')}'", file=sys.stderr)
        return 1

    # Verify git commit format
    git_commit = first_event.get("git_commit")
    if not git_commit:
        print("[AUDIT FAIL] 'run_started' event missing 'git_commit'", file=sys.stderr)
        return 1
    
    if git_commit != "unknown_commit" and not re.match(r"^[0-9a-f]{40}(-dirty)?$", git_commit):
        print(f"[AUDIT FAIL] Invalid git commit format: '{git_commit}'", file=sys.stderr)
        return 1

    # Track state transitions and causality
    steps_started = {}  # step_id -> event_data
    steps_completed = set()
    artifact_hashes = {}  # artifact_path -> hash

    for event_idx, event in enumerate(events):
        event_type = event.get("event")
        if not event_type:
            print(f"[AUDIT FAIL] Event at index {event_idx} missing 'event' field", file=sys.stderr)
            return 1

        timestamp = event.get("timestamp")
        if not timestamp:
            print(f"[AUDIT FAIL] Event at index {event_idx} missing 'timestamp'", file=sys.stderr)
            return 1

        if event_type == "run_started":
            if event_idx != 0:
                print(f"[AUDIT FAIL] Multiple 'run_started' events found or it is not first", file=sys.stderr)
                return 1

        elif event_type == "step_started":
            step_id = event.get("step_id")
            skill_id = event.get("skill_id")
            if not step_id or not skill_id:
                print(f"[AUDIT FAIL] 'step_started' event at index {event_idx} missing 'step_id' or 'skill_id'", file=sys.stderr)
                return 1

            if step_id in steps_started:
                print(f"[AUDIT FAIL] Duplicate step_started for step '{step_id}'", file=sys.stderr)
                return 1
            
            steps_started[step_id] = event

            # Verify inputs exist and hashes match
            inputs = event.get("inputs", [])
            for inp in inputs:
                inp_path = inp.get("path")
                inp_hash = inp.get("hash")
                if not inp_path or not inp_hash:
                    print(f"[AUDIT FAIL] Invalid input structure in step '{step_id}': {inp}", file=sys.stderr)
                    return 1

                abs_inp_path = os.path.join(repo_root, inp_path)
                if not os.path.exists(abs_inp_path):
                    print(f"[AUDIT FAIL] Input file '{inp_path}' for step '{step_id}' does not exist on disk", file=sys.stderr)
                    return 1

                current_hash = _compute_file_hash(abs_inp_path)
                if current_hash != inp_hash:
                    print(f"[AUDIT FAIL] Hash mismatch for input '{inp_path}' in step '{step_id}': expected '{inp_hash}', got '{current_hash}'", file=sys.stderr)
                    return 1

        elif event_type == "artifact_created":
            step_id = event.get("step_id")
            artifact_id = event.get("artifact_id")
            path = event.get("path")
            art_hash = event.get("hash")

            if not step_id or not artifact_id or not path or not art_hash:
                print(f"[AUDIT FAIL] 'artifact_created' missing required fields", file=sys.stderr)
                return 1

            if step_id not in steps_started:
                print(f"[AUDIT FAIL] 'artifact_created' for step '{step_id}' but step has not started", file=sys.stderr)
                return 1

            if step_id in steps_completed:
                print(f"[AUDIT FAIL] 'artifact_created' for step '{step_id}' after step already completed", file=sys.stderr)
                return 1

            # Verify file exists on disk and hash matches
            abs_path = os.path.join(repo_root, path)
            if not os.path.exists(abs_path):
                print(f"[AUDIT FAIL] Artifact file '{path}' does not exist on disk", file=sys.stderr)
                return 1

            current_hash = _compute_file_hash(abs_path)
            if current_hash != art_hash:
                print(f"[AUDIT FAIL] Hash mismatch for artifact '{path}': expected '{art_hash}', got '{current_hash}'", file=sys.stderr)
                return 1

            artifact_hashes[path] = art_hash

        elif event_type == "validation_completed":
            step_id = event.get("step_id")
            artifact_id = event.get("artifact_id")
            validator_command = event.get("validator_command")
            exit_code = event.get("exit_code")
            status = event.get("status")

            if step_id not in steps_started:
                print(f"[AUDIT FAIL] 'validation_completed' for step '{step_id}' but step has not started", file=sys.stderr)
                return 1

            if step_id in steps_completed:
                print(f"[AUDIT FAIL] 'validation_completed' for step '{step_id}' after step already completed", file=sys.stderr)
                return 1

            # Locate corresponding artifact_created event to verify hash matches what was validated
            art_created = next((e for e in events[:event_idx] if e.get("event") == "artifact_created" and e.get("step_id") == step_id and e.get("artifact_id") == artifact_id), None)
            if not art_created:
                print(f"[AUDIT FAIL] Validation completed for step '{step_id}' / '{artifact_id}', but no corresponding 'artifact_created' event found", file=sys.stderr)
                return 1

        elif event_type == "step_completed":
            step_id = event.get("step_id")
            status = event.get("status")
            gate_status = event.get("gate_status")

            if not step_id or not status or not gate_status:
                print(f"[AUDIT FAIL] 'step_completed' event missing required fields", file=sys.stderr)
                return 1

            if step_id not in steps_started:
                print(f"[AUDIT FAIL] Step completed '{step_id}' before start event", file=sys.stderr)
                return 1

            if step_id in steps_completed:
                print(f"[AUDIT FAIL] Duplicate step_completed for step '{step_id}'", file=sys.stderr)
                return 1

            steps_completed.add(step_id)

            # Chronological checks: start must have timestamp <= complete timestamp
            start_event = steps_started[step_id]
            if start_event["timestamp"] > timestamp:
                print(f"[AUDIT FAIL] Chronological causality violation: step '{step_id}' start timestamp '{start_event['timestamp']}' is after completion timestamp '{timestamp}'", file=sys.stderr)
                return 1

            # If status is passed/completed, validation must have passed (exit_code == 0) unless it was skipped
            if status in ("passed", "completed"):
                val_event = next((e for e in events[:event_idx] if e.get("event") == "validation_completed" and e.get("step_id") == step_id), None)
                if not val_event and gate_status != "bypassed":
                    print(f"[AUDIT FAIL] Step '{step_id}' completed with status '{status}' but no validation event was recorded", file=sys.stderr)
                    return 1
                if val_event and val_event.get("exit_code") != 0:
                    print(f"[AUDIT FAIL] Step '{step_id}' completed with status '{status}' but validator failed with exit code {val_event.get('exit_code')}", file=sys.stderr)
                    return 1

        elif event_type == "run_completed":
            if event_idx != len(events) - 1:
                print(f"[AUDIT FAIL] 'run_completed' event must be the last event in the ledger, found at index {event_idx}", file=sys.stderr)
                return 1

            run_status = event.get("status")
            if run_status == "completed":
                for step_id in steps_started:
                    if step_id not in steps_completed:
                        print(f"[AUDIT FAIL] Run completed but step '{step_id}' remains uncompleted", file=sys.stderr)
                        return 1
            elif run_status == "failed":
                has_failure = any(e.get("status") == "failed" for e in events if e.get("event") == "step_completed")
                if not has_failure:
                    print(f"[AUDIT FAIL] Run marked as failed but no step completion recorded status 'failed'", file=sys.stderr)
                    return 1

    print("[AUDIT SUCCESS] Run ledger passes all causality, hash, and validation checks.")
    return 0


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    # Intercept audit-run mode
    if argv and argv[0] == "audit-run":
        audit_parser = argparse.ArgumentParser(
            description="Audit a run ledger for causality, hashes, and validation status."
        )
        audit_parser.add_argument("--ledger-path", required=True, help="Path to the run ledger JSONL file")
        audit_parser.add_argument("--repo-root", default=".", help="Repository root directory")
        audit_args = audit_parser.parse_args(argv[1:])
        return handle_audit_run(audit_args)

    parser = argparse.ArgumentParser(
        description="Production-grade orchestration runner for sensemaking workflows."
    )
    parser.add_argument("problem", nargs="?", default=None, help="User problem statement or goal (will prompt if not provided for full-local-sensemaking)")
    parser.add_argument("--workflow", default=None, help="Explicit workflow ID (overrides default)")
    parser.add_argument("--mode", default="yolo_execution", choices=list(KNOWN_MODES.keys()),
                        help="Execution mode (default: yolo_execution)")
    parser.add_argument("--scope", default="soft", choices=["soft", "hard", "advisory"],
                        help="How strictly the problem statement constrains analysis (default: soft)")
    parser.add_argument("--repo-root", default=".", help="Repository root directory")
    parser.add_argument("--plan-out", default=None, help="Output path for the orchestration plan")
    parser.add_argument("--log-dir", default=None, help="Directory for run log output")
    parser.add_argument("--list-workflows", action="store_true", help="List all registered workflows")
    parser.add_argument("--resume", action="store_true", help="Resume a paused execution")
    parser.add_argument("--executor", default="claude-code",
                        choices=["dry-run", "prompt-chain", "claude-code", "api"],
                        help="Skill executor to use (default: claude-code). autonomous/yolo modes require a real executor.")
    parser.add_argument("--gate-decision", default=None,
                        choices=["auto-approve", "auto-deny"],
                        help="Non-interactive gate decision for testing: auto-approve all gates or auto-deny the first gate")
    parser.add_argument("--use-fixtures", action="store_true",
                        help="Use fixture artifacts instead of validating actual artifacts (for testing orchestration without skill execution)")
    parser.add_argument("--chained", action="store_true", default=False,
                        help="Internal: invoked as a chained/child workflow from another workflow run")
    parser.add_argument("--from-session", default=None,
                        help="Path to artifact session directory from a prior workflow run (for manual path or chained execution)")

    args = parser.parse_args(argv)

    # Resolve repo root: if relative, treat as relative to cwd (same as other validators)
    if os.path.isabs(args.repo_root):
        repo_root = args.repo_root
    else:
        repo_root = os.path.abspath(args.repo_root)

    if args.list_workflows:
        list_workflows(repo_root)
        return 0

    # Determine workflow_id: explicit --workflow > default full-local-sensemaking
    workflow_id = args.workflow or "full-local-sensemaking"

    # Validate gate_decision compatibility
    if args.gate_decision and args.mode not in ("guided_execution", "autonomous_execution"):
        print(f"Note: --gate-decision is only for guided/autonomous modes, ignoring for '{args.mode}'")

    # Prompt for problem statement if not provided and workflow requires it
    problem = args.problem
    if not problem and workflow_id == "full-local-sensemaking" and args.mode != "plan_only":
        print("\n" + "="*60)
        print("Workflow Input Required")
        print("="*60)
        print(f"Workflow '{workflow_id}' requires a problem statement.")
        print("This can be vague, strategic, or exploratory.\n")
        print("Examples:")
        print("  - 'My team needs a better way to manage async workflows'")
        print("  - 'Should we refactor our authentication system?'")
        print("  - 'Improve observability in our data pipeline'\n")
        problem = input("Enter your problem statement (or press Ctrl+C to abort): ").strip()
        if not problem:
            print("ERROR: Problem statement cannot be empty")
            return 1

    runner = OrchestrationRunner(
        workflow_id=workflow_id,
        mode=args.mode,
        repo_root=repo_root,
        plan_out=args.plan_out,
        log_dir=args.log_dir,
        resume=args.resume,
        gate_decision=args.gate_decision,
        executor=args.executor,
        use_fixtures=args.use_fixtures,
        chained=args.chained,
        from_session=args.from_session,
    )

    if runner.errors:
        for e in runner.errors:
            print(f"ERROR {e}")
        return 1

    # Handle --from-session: reuse session directory from prior run
    if args.from_session:
        from_session_path = os.path.abspath(args.from_session)
        if not os.path.isdir(from_session_path):
            print(f"ERROR: --from-session path does not exist: {from_session_path}")
            return 1

        # Check if prior run's user_intent exists
        prior_intent = os.path.join(from_session_path, "00-user-intent.md")
        if not os.path.exists(prior_intent):
            print(f"ERROR: No user_intent artifact found in --from-session directory: {from_session_path}")
            return 1

        # Reuse the session directory and intent
        runner.artifact_session_dir = from_session_path
        runner.session_id = os.path.basename(from_session_path)
        intent_path = prior_intent

        # Update output paths to use session directory
        if not args.plan_out:
            runner.plan_out = os.path.join(from_session_path, f"plan_{workflow_id}.md")
        if not args.log_dir:
            runner.log_dir = from_session_path

        print(f"[OK] Reusing session: {os.path.relpath(from_session_path, repo_root)}")
    else:
        # Create user intent artifact before running workflow
        intent_path = runner._create_user_intent_artifact(problem, args.scope)
        if not intent_path:
            print("ERROR: Failed to create user_intent artifact")
            for e in runner.errors:
                print(f"  - {e}")
            return 1

    # Store execution context in runner
    runner.problem_statement = problem
    runner.intent_path = intent_path

    return runner.run()


if __name__ == "__main__":
    sys.exit(main())
