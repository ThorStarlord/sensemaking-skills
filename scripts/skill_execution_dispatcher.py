"""
Skill Execution Dispatcher: Manages skill execution subprocess.

Orchestration-runner delegates skill invocation to this dispatcher when
running in autonomous_execution or yolo_execution modes.

Usage (internal):
    dispatcher = SkillExecutionDispatcher(plan_path, repo_root, executor=executor)
    success, output = dispatcher.run_with_timeout(timeout=3600)
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Tuple

from _validator_utils import format_error, resolve_repo_root

DISPATCHER_TIMEOUT = "DISPATCHER_TIMEOUT"
DISPATCHER_FAILED = "DISPATCHER_FAILED"
SKILL_EXECUTION_FAILED = "SKILL_EXECUTION_FAILED"


class SkillExecutionDispatcher:
    """Manages skill execution subprocess with timeout and error handling."""

    def __init__(self, plan_path: str, repo_root: str, executor: str = "dry-run"):
        self.plan_path = os.path.abspath(plan_path)
        self.repo_root = os.path.abspath(repo_root)
        self.executor = executor
        self.agent_script = os.path.join(self.repo_root, "scripts", "skill-execution-agent.py")
        self.process = None
        self.output = ""
        self.error_output = ""

    def run_with_timeout(self, timeout_seconds: int = 3600) -> Tuple[bool, str, dict]:
        """
        Run skill execution agent with timeout.

        Returns (success: bool, combined_output: str, parsed_results: dict)
        """
        if not os.path.exists(self.plan_path):
            return False, format_error(DISPATCHER_FAILED, f"Plan file not found: {self.plan_path}"), {}

        if not os.path.exists(self.agent_script):
            return False, format_error(DISPATCHER_FAILED, f"Agent script not found: {self.agent_script}"), {}

        cmd = [
            sys.executable,
            self.agent_script,
            self.plan_path,
            "--repo-root", self.repo_root,
            "--executor", self.executor,
            "--timeout", str(timeout_seconds),
        ]

        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.repo_root
            )

            try:
                self.output, self.error_output = self.process.communicate(timeout=timeout_seconds)
                returncode = self.process.returncode
            except subprocess.TimeoutExpired:
                self.process.kill()
                return False, format_error(DISPATCHER_TIMEOUT, f"Skill execution exceeded {timeout_seconds}s timeout"), {}

            combined = f"{self.output}\n{self.error_output}"

            # Try to parse JSON results from output
            parsed_results = {}
            try:
                # Look for JSON in the output (skill-execution-agent outputs JSON at the end)
                lines = self.output.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('{'):
                        json_str = '\n'.join(lines[i:])
                        parsed_results = json.loads(json_str)
                        break
            except (json.JSONDecodeError, ValueError):
                pass  # No valid JSON found, continue with empty results

            if returncode != 0:
                return False, format_error(SKILL_EXECUTION_FAILED, combined), parsed_results

            return True, self.output, parsed_results

        except Exception as e:
            return False, format_error(DISPATCHER_FAILED, f"Subprocess error: {str(e)}"), {}


def dispatch_skill_execution(plan_path: str, repo_root: str, executor: str = "dry-run", timeout: int = 3600) -> Tuple[bool, str, dict]:
    """
    Convenience function for dispatching skill execution from workflow-runtime.

    Returns (success: bool, output: str, parsed_results: dict)
    """
    dispatcher = SkillExecutionDispatcher(plan_path, repo_root, executor=executor)
    return dispatcher.run_with_timeout(timeout_seconds=timeout)
