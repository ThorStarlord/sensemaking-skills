#!/usr/bin/env python3
"""
Shadow Mode Test Runner: Execute diagnostics against sample repositories.
Collects metrics for analysis and go/no-go decision.
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class ShadowModeRunner:
    def __init__(self, repo_root: str = "."):
        self.repo_root = repo_root
        self.results = []
        self.start_time = datetime.now()

    def run_diagnostic(self, repo_path: str) -> Dict[str, Any]:
        """Run diagnostic on a sample repository."""
        test_start = time.time()

        # Run workflow-planner validation
        try:
            result = subprocess.run(
                [sys.executable, "scripts/validate-and-report.py", repo_path],
                capture_output=True,
                timeout=30,
                cwd=self.repo_root
            )

            execution_time = time.time() - test_start

            return {
                "repository": os.path.basename(repo_path),
                "size": self._classify_repo_size(repo_path),
                "success": result.returncode == 0,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                "repository": os.path.basename(repo_path),
                "size": self._classify_repo_size(repo_path),
                "success": False,
                "error": "timeout",
                "execution_time": 30.0,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "repository": os.path.basename(repo_path),
                "size": self._classify_repo_size(repo_path),
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _classify_repo_size(self, repo_path: str) -> str:
        """Classify repository by file count."""
        try:
            result = subprocess.run(
                ["find", repo_path, "-type", "f", "-name", "*.py", "-o", "-name", "*.js", "-o", "-name", "*.md"],
                capture_output=True,
                text=True
            )
            file_count = len(result.stdout.strip().split('\n'))

            if file_count < 100:
                return "small"
            elif file_count < 500:
                return "medium"
            elif file_count < 2000:
                return "large"
            else:
                return "very_large"
        except:
            return "unknown"

    def run_batch(self, repo_list: List[str]) -> Dict[str, Any]:
        """Run diagnostics against batch of repositories."""
        for i, repo in enumerate(repo_list, 1):
            print(f"Testing {i}/{len(repo_list)}: {repo}")
            result = self.run_diagnostic(repo)
            self.results.append(result)

        return self.calculate_metrics()

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate success metrics from results."""
        if not self.results:
            return {}

        successes = sum(1 for r in self.results if r.get("success"))
        total = len(self.results)
        times = [r.get("execution_time", 0) for r in self.results if r.get("execution_time")]

        times.sort()
        p95_idx = int(len(times) * 0.95)
        p95_time = times[p95_idx] if p95_idx < len(times) else max(times)

        return {
            "total_tests": total,
            "successes": successes,
            "success_rate": successes / total if total > 0 else 0,
            "execution_time_avg": sum(times) / len(times) if times else 0,
            "execution_time_p95": p95_time,
            "execution_time_max": max(times) if times else 0,
            "results": self.results
        }

if __name__ == "__main__":
    runner = ShadowModeRunner()
    print("Shadow Mode Test Runner initialized")
