#!python
"""Workflow runner — coding agent mode only.

Hardcodes the claude-code executor and removes all CLI options for API,
prompt-chain, and dry-run modes. This is the runner to use when you (the
coding agent) want to execute a sensemaking workflow by delegating skill
calls to the claude-code SDK.

Usage:
    python scripts/workflow-runner-agent.py "I want to improve X" --mode guided
    python scripts/workflow-runner-agent.py --mode yolo
    python scripts/workflow-runner-agent.py --list-workflows

Options:
    problem         User problem statement or goal (will prompt if omitted)
    --workflow      Workflow ID (default: full-local-sensemaking)
    --mode          Execution mode (default: guided_execution)
                    Choices: plan_only, prompt_chain, guided_execution,
                             autonomous_execution, yolo_execution
    --gate-decision auto-approve|auto-deny  (for non-interactive runs)
    --scope         soft|hard|advisory (how strictly to constrain analysis)
    --use-fixtures  Use pre-built fixture artifacts (for testing)
    --list-workflows  List all registered workflows and exit
"""

import os
import sys
import argparse

from _orchestrator import (
    OrchestrationRunner,
    KNOWN_MODES,
    list_workflows,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Workflow runner for coding agent mode (claude-code executor only)."
    )
    parser.add_argument("problem", nargs="?", default=None,
                        help="User problem statement or goal (will prompt if not provided)")
    parser.add_argument("--workflow", default=None,
                        help="Explicit workflow ID (default: full-local-sensemaking)")
    parser.add_argument("--mode", default="guided_execution", choices=list(KNOWN_MODES.keys()),
                        help="Execution mode (default: guided_execution)")
    parser.add_argument("--scope", default="soft", choices=["soft", "hard", "advisory"],
                        help="How strictly the problem constrains analysis (default: soft)")
    parser.add_argument("--repo-root", default=".",
                        help="Repository root directory (default: .)")
    parser.add_argument("--gate-decision", default=None,
                        choices=["auto-approve", "auto-deny"],
                        help="Non-interactive gate decision for automated runs")
    parser.add_argument("--use-fixtures", action="store_true",
                        help="Use pre-built fixture artifacts (for testing orchestration)")
    parser.add_argument("--plan-out", default=None,
                        help="Output path for the orchestration plan (optional)")
    parser.add_argument("--log-dir", default=None,
                        help="Directory for run log output (optional)")
    parser.add_argument("--resume", action="store_true",
                        help="Resume a paused execution")
    parser.add_argument("--chained", action="store_true", default=False,
                        help="Internal: invoked as chained workflow from another run")
    parser.add_argument("--list-workflows", action="store_true",
                        help="List all registered workflows and exit")

    args = parser.parse_args(argv)

    if os.path.isabs(args.repo_root):
        repo_root = args.repo_root
    else:
        repo_root = os.path.abspath(args.repo_root)

    if args.list_workflows:
        list_workflows(repo_root)
        return 0

    workflow_id = args.workflow or "full-local-sensemaking"

    if args.gate_decision and args.mode not in ("guided_execution", "autonomous_execution"):
        print(f"Note: --gate-decision is only for guided/autonomous modes, ignoring for '{args.mode}'")

    # Prompt for problem statement if not provided
    problem = args.problem
    if not problem and workflow_id == "full-local-sensemaking" and args.mode != "plan_only":
        print()
        print("=" * 60)
        print("Workflow Input Required")
        print("=" * 60)
        print(f"Workflow '{workflow_id}' requires a problem statement.")
        print("This can be vague, strategic, or exploratory.")
        print()
        print("Examples:")
        print("  - 'My team needs a better way to manage async workflows'")
        print("  - 'Should we refactor our authentication system?'")
        print("  - 'Improve observability in our data pipeline'")
        print()
        problem = input("Enter your problem statement (or press Ctrl+C to abort): ").strip()
        if not problem:
            print("ERROR: Problem statement cannot be empty")
            return 1

    # Hardcode executor to claude-code — this is the coding agent runner
    runner = OrchestrationRunner(
        workflow_id=workflow_id,
        mode=args.mode,
        repo_root=repo_root,
        plan_out=args.plan_out,
        log_dir=args.log_dir,
        resume=args.resume,
        gate_decision=args.gate_decision,
        executor="claude-code",
        use_fixtures=args.use_fixtures,
        chained=args.chained,
    )

    if runner.errors:
        for e in runner.errors:
            print(f"ERROR {e}")
        return 1

    intent_path = runner._create_user_intent_artifact(problem, args.scope)
    if not intent_path:
        print("ERROR: Failed to create user_intent artifact")
        for e in runner.errors:
            print(f"  - {e}")
        return 1

    runner.problem_statement = problem
    runner.intent_path = intent_path

    return runner.run()


if __name__ == "__main__":
    sys.exit(main())
