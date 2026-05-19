"""
DEPRECATED — Compatibility wrapper.

Use `workflow-runtime.py` instead. This script delegates to the new name.

Usage (old, still works):
    python scripts/orchestration-runner.py <workflow-id> --mode <mode> [options]

New canonical command:
    python scripts/workflow-runtime.py <workflow-id> --mode <mode> [options]
"""

import sys
import subprocess
import os
import warnings

warnings.warn(
    "orchestration-runner.py is deprecated. Use workflow-runtime.py instead.",
    DeprecationWarning,
    stacklevel=2,
)

if __name__ == "__main__":
    # Delegate to the canonical workflow-runtime.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    new_runner = os.path.join(script_dir, "workflow-runtime.py")

    cmd = [sys.executable, new_runner] + sys.argv[1:]
    result = subprocess.run(cmd)
    sys.exit(result.returncode)
