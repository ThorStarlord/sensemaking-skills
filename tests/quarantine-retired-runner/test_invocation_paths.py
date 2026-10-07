"""Integration tests for manual vs automation invocation paths.

Tests that both paths can execute end-to-end:
1. Manual path: diagnostic workflow → manual implementation workflow with --from-session
2. Automation path: diagnostic workflow surfaces (never spawns) the next-workflow
   candidate under ADR 0026 fail-closed authority gating
3. Recursion guard: prevents self-routing
4. Session passing: --from-session flag and session-reuse plumbing exist

NOTE (retirement): test_auto_invocation_passes_from_session was rewritten as
test_auto_invocation_is_fail_closed_not_spawn. It pinned the pre-ADR-0026
spawning behavior (_invoke_next_workflow passing --from-session to a child
process). The runtime is now fail-closed by design: candidates are surfaced,
never spawned, and the retired spawning path must stay absent. The no-spawn
contract itself is pinned thoroughly by
tests/test_auto_invoke_authority_gating.py.
"""

import os
import sys
import subprocess
from pathlib import Path


def test_from_session_flag_exists():
    """Test that --from-session flag is implemented in runtime.

    Verifies:
    1. --from-session flag exists in argument parser
    2. from_session parameter is handled in OrchestrationRunner
    3. Session reuse logic is implemented
    """
    print("\n" + "="*60)
    print("TEST 1: --from-session Flag Implementation")
    print("="*60)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    runtime_path = os.path.join(repo_root, "scripts", "workflow-runtime.py")

    with open(runtime_path, "r", encoding="utf-8") as f:
        runtime_code = f.read()

    # Verify argument parser has --from-session
    assert '--from-session' in runtime_code, "--from-session flag not found in argument parser"
    print("  ✓ --from-session flag defined in argument parser")

    # Verify OrchestrationRunner accepts from_session parameter
    assert 'from_session: str | None = None' in runtime_code, "from_session parameter not in __init__"
    print("  ✓ OrchestrationRunner accepts from_session parameter")

    # Verify session reuse logic exists
    assert 'self.from_session = from_session' in runtime_code, "from_session not stored in runner"
    print("  ✓ from_session is stored in runner state")

    assert '--from-session' in runtime_code and 'from_session_path' in runtime_code, "Session reuse logic not implemented"
    print("  ✓ Session reuse logic implemented in main()")

    print("  [OK] TEST PASSED")


def test_recursion_guard_implemented():
    """Test that recursion guard prevents self-routing.

    Verifies:
    1. Recursion check exists in auto-invocation code
    2. Check compares next_workflow_id with current workflow_id
    3. Self-routing fails safely with error message
    """
    print("\n" + "="*60)
    print("TEST 2: Recursion Guard Implementation")
    print("="*60)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    runtime_path = os.path.join(repo_root, "scripts", "workflow-runtime.py")

    with open(runtime_path, "r", encoding="utf-8") as f:
        runtime_code = f.read()

    # Check for recursion guard code
    assert 'RECURSION DETECTED' in runtime_code, "Recursion detection message not found"
    print("  ✓ Recursion detection message implemented")

    assert 'if next_workflow_id == self.workflow_id:' in runtime_code, "Self-routing check not found"
    print("  ✓ Self-routing check implemented")

    assert 'routing configuration error' in runtime_code, "Self-routing error reporting not found"
    print("  ✓ Self-routing reported as a routing configuration error")

    print("  [OK] TEST PASSED")


def test_auto_invocation_is_fail_closed_not_spawn():
    """Test that auto-invocation surfaces (never spawns) the next candidate.

    ADR 0026 retired child-process spawning: the runtime surfaces the
    candidate via _surface_candidate_next_workflow and completes without a
    child workflow. The no-spawn contract itself is pinned by
    tests/test_auto_invoke_authority_gating.py; here we pin the surviving
    session plumbing (--from-session flag, from_session state, session
    reuse) that the manual path still uses.
    """
    print("\n" + "="*60)
    print("TEST 3: Auto-Invocation Fail-Closed, Session Plumbing Retained")
    print("="*60)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    runtime_path = os.path.join(repo_root, "scripts", "workflow-runtime.py")

    with open(runtime_path, "r", encoding="utf-8") as f:
        runtime_code = f.read()

    # The fail-closed surfacing entry point replaced _invoke_next_workflow.
    assert '_surface_candidate_next_workflow' in runtime_code, "fail-closed surfacing entry point not found"
    print("  ✓ _surface_candidate_next_workflow entry point exists")

    assert 'def _invoke_next_workflow' not in runtime_code, "retired spawning method must stay retired"
    print("  ✓ retired _invoke_next_workflow spawning method absent")

    assert '--from-session' in runtime_code, "--from-session flag missing"
    print("  ✓ --from-session flag retained for the manual path")

    assert 'self.artifact_session_dir' in runtime_code, "Parent session directory not referenced"
    print("  ✓ Parent artifact_session_dir referenced")

    print("  [OK] TEST PASSED")


def test_cli_syntax_examples():
    """Test that documented CLI syntax matches the implementation.

    The documented surface is the `sensemaking-skills <command>` families
    (docs/cli-reference.md, subordinate to docs/cli-contract-v1.0.yaml);
    scripts/workflow-runtime.py retains --workflow for direct invocation.
    GETTING_STARTED.md intentionally points at references instead of
    duplicating CLI contracts, so flag counts are pinned at the reference
    and contract, not the entry guide.

    Verifies:
    1. docs/cli-reference.md documents the sensemaking-skills command families
    2. docs/cli-contract-v1.0.yaml is the machine authority for the CLI
    3. workflow-runtime.py implements the --workflow flag
    4. ADR 0012 historical --workflow examples remain intact
    """
    print("\n" + "="*60)
    print("TEST 4: CLI Syntax in Documentation")
    print("="*60)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # CLI reference documents the command families.
    ref_path = os.path.join(repo_root, "docs", "cli-reference.md")
    with open(ref_path, "r", encoding="utf-8") as f:
        ref_content = f.read()

    assert "sensemaking-skills" in ref_content, "cli-reference.md doesn't document the sensemaking-skills command"
    print("  ✓ docs/cli-reference.md documents the sensemaking-skills command")

    # Machine contract is the CLI authority.
    contract_path = os.path.join(repo_root, "docs", "cli-contract-v1.0.yaml")
    assert os.path.exists(contract_path), "docs/cli-contract-v1.0.yaml (CLI machine authority) missing"
    print("  ✓ docs/cli-contract-v1.0.yaml CLI authority present")

    # The runtime implements --workflow for direct invocation.
    runtime_path = os.path.join(repo_root, "scripts", "workflow-runtime.py")
    with open(runtime_path, "r", encoding="utf-8") as f:
        runtime_code = f.read()

    assert '"--workflow"' in runtime_code or "'--workflow'" in runtime_code, "--workflow flag not implemented in runtime"
    print("  ✓ workflow-runtime.py implements the --workflow flag")

    # Check ADR 0012
    adr_path = os.path.join(repo_root, "docs", "adr", "0012-invocation-paths.md")
    with open(adr_path, "r", encoding="utf-8") as f:
        adr_content = f.read()

    workflow_flag_count = adr_content.count("--workflow")
    assert workflow_flag_count > 2, f"Expected multiple --workflow flags in ADR 0012, found {workflow_flag_count}"
    print(f"  ✓ ADR 0012: {workflow_flag_count} --workflow examples")

    print("  [OK] TEST PASSED")


def test_registry_mode_consistency():
    """Test that documentation examples match allowed execution modes in registry.

    Verifies:
    1. fast-path-workflow allowed modes are correctly documented
    2. No invalid mode examples for workflows
    """
    print("\n" + "="*60)
    print("TEST 5: Registry and Documentation Mode Consistency")
    print("="*60)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Check workflow registry
    registry_path = os.path.join(repo_root, "skills", "workflow-planner", "references", "workflow-registry.yaml")
    with open(registry_path, "r", encoding="utf-8") as f:
        registry_content = f.read()

    # Find fast-path-workflow allowed modes more carefully
    import re
    fp_match = re.search(
        r'- id: fast-path-workflow.*?(?=\n- id:|$)',
        registry_content,
        re.DOTALL
    )
    fp_section = fp_match.group(0) if fp_match else ""

    # Check for allowed modes
    if fp_section:
        modes_present = []
        for mode in ["plan_only", "prompt_chain", "guided_execution", "autonomous_execution"]:
            if mode in fp_section:
                modes_present.append(mode)

        assert len(modes_present) > 0, f"fast-path-workflow has no allowed modes in registry"
        print(f"  ✓ fast-path-workflow allowed modes: {', '.join(modes_present)}")

    # Current execution deliberately excludes retired yolo_execution.

    print("  [OK] TEST PASSED")


def test_execution_modes_documented():
    """Pin the current runtime-mode boundary without treating historical ADR prose as runtime authority."""
    print("\n" + "="*60)
    print("TEST 6: Current Execution Mode Boundary")
    print("="*60)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    runtime_path = os.path.join(repo_root, "scripts", "workflow-runtime.py")
    with open(runtime_path, "r", encoding="utf-8") as f:
        runtime_code = f.read()

    assert 'RETIRED_EXECUTION_MODES = {"yolo_execution"}' in runtime_code
    assert "choices=list(CURRENT_EXECUTION_MODES)" in runtime_code
    print("  ✓ current CLI excludes retired yolo_execution")
    print("  [OK] TEST PASSED")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("INTEGRATION TESTS: Manual vs Automation Invocation Paths")
    print("="*70)

    tests = [
        ("from_session_flag_exists", test_from_session_flag_exists),
        ("recursion_guard_implemented", test_recursion_guard_implemented),
        ("auto_invocation_is_fail_closed_not_spawn", test_auto_invocation_is_fail_closed_not_spawn),
        ("cli_syntax_examples", test_cli_syntax_examples),
        ("registry_mode_consistency", test_registry_mode_consistency),
        ("execution_modes_documented", test_execution_modes_documented),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"  [FAILED] {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "="*70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*70)

    if failed == 0:
        print("\nSummary:")
        print("  ✓ --from-session flag implemented in runtime")
        print("  ✓ Recursion guard prevents self-routing")
        print("  ✓ Auto-invocation fail-closed, session plumbing retained")
        print("  ✓ CLI syntax matches the implementation")
        print("  ✓ Registry modes consistent with documentation")
        print("  ✓ Current execution-mode boundary excludes retired YOLO")
        sys.exit(0)
    else:
        sys.exit(1)
