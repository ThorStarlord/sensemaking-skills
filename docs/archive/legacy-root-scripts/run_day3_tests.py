#!/usr/bin/env python3
"""Execute Day 3 testing (33 repositories)."""

import sys
import json
import os
import importlib.util
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root / "scripts"))

# Import shadow-mode-runner module with hyphenated name
spec = importlib.util.spec_from_file_location(
    "shadow_mode_runner",
    repo_root / "scripts" / "shadow-mode-runner.py"
)
shadow_mode_runner_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shadow_mode_runner_module)

ShadowModeRunner = shadow_mode_runner_module.ShadowModeRunner
load_sample_repos = shadow_mode_runner_module.load_sample_repos

os.chdir(str(repo_root))

runner = ShadowModeRunner()
repos = load_sample_repos('data/sample-repos.txt')
day3_repos = repos[:33]  # First 33

print(f'Day 3: Testing {len(day3_repos)} repositories...')
metrics = runner.run_batch(day3_repos)

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

with open('logs/shadow-mode-day3.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print(f"Day 3: {metrics['successes']}/{metrics['total_tests']} PASS")
