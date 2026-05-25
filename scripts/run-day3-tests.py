#!/usr/bin/env python3
"""Execute Day 3 testing (33 repositories)."""

import sys
import json
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from shadow_mode_runner import ShadowModeRunner, load_sample_repos

os.chdir("H:\\GithubRepositories\\sensemaking-skills")

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
