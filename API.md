# API Reference

Use sensemaking-skills programmatically in Python to integrate artifact generation and analysis into your applications.

---

## Installation

First, install the package:

```bash
pip install sensemaking-skills
```

Then import the core classes:

```python
from sensemaking_skills.config import ConfigManager
from sensemaking_skills.runner import SkillsOrchestrator
from sensemaking_skills.skills.base import BaseSkill
```

---

## Basic Usage

### 1. Load Configuration

```python
from sensemaking_skills.config import ConfigManager
from pathlib import Path

# Load configuration from a repository
config_manager = ConfigManager(repo_root="/path/to/repo")
config = config_manager.load()

# Now config contains:
# - config.repo_root: Repository path
# - config.artifacts_dir: Where to save artifacts
# - config.execution_mode: guided_execution, autonomous_execution, etc.
# - config.skills: List of enabled skills
# - config.workflows: Registered workflows
```

### 2. Create Orchestrator

```python
from sensemaking_skills.runner import SkillsOrchestrator

orchestrator = SkillsOrchestrator(config=config)
```

### 3. Run a Workflow

```python
# Run the fast-path-workflow
result = orchestrator.run_workflow(
    workflow_id="fast-path-workflow",
    execution_mode="guided_execution",
    problem_statement="Our codebase has unclear architecture",
)

# Result contains:
# - result.success: bool - whether workflow succeeded
# - result.artifacts: dict - all generated artifacts
# - result.logs: list - execution logs
# - result.fog_type: str - detected fog type (product_fog, ui_fog, etc.)
```

Pass `execution_mode` explicitly when calling `SkillsOrchestrator.run_workflow`. Omitting it is deprecated. During the compatibility window, an omitted mode still behaves as `yolo_execution` and emits a `FutureWarning`; that fallback is not a stable product default and may be removed or changed only through a later versioned release decision.

---

## API Classes

### ConfigManager

Loads and manages sensemaking configuration.

```python
from sensemaking_skills.config import ConfigManager

class ConfigManager:
    """Manages sensemaking configuration."""
    
    def __init__(self, repo_root: str):
        """
        Initialize config manager.
        
        Args:
            repo_root: Path to repository
        """
        pass
    
    def load(self) -> SkillsConfig:
        """
        Load configuration from sensemaking-config.yaml.
        
        Returns:
            SkillsConfig object with repo_root, artifacts_dir, skills, workflows
        
        Raises:
            FileNotFoundError: If sensemaking-config.yaml not found
        """
        pass
    
    def save(self, config: SkillsConfig) -> None:
        """
        Save configuration to sensemaking-config.yaml.
        
        Args:
            config: SkillsConfig object to save
        """
        pass
```

**Example**:
```python
from sensemaking_skills.config import ConfigManager

config_manager = ConfigManager(repo_root=".")
config = config_manager.load()

print(f"Repo root: {config.repo_root}")
print(f"Artifacts dir: {config.artifacts_dir}")
print(f"Enabled skills: {config.skills.enabled}")
```

### SkillsConfig

Data class representing configuration.

```python
from sensemaking_skills.config import SkillsConfig
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SkillsConfig:
    """Configuration for sensemaking skills."""
    
    repo_root: str
    artifacts_dir: str
    execution_mode: str  # guided_execution, autonomous_execution, plan_only
    skills: Dict[str, List[str]]  # { enabled: [...], disabled: [...] }
    workflows: Dict[str, Dict[str, Any]]  # workflow registry
    vocabulary: Dict[str, Any]  # custom vocabulary overrides
```

**Example**:
```python
from sensemaking_skills.config import SkillsConfig

config = SkillsConfig(
    repo_root="/path/to/repo",
    artifacts_dir="/path/to/repo/.sensemaking/artifacts",
    execution_mode="autonomous_execution",
    skills={"enabled": ["repo-sensemaker", "workflow-planner"]},
    workflows={},
    vocabulary={},
)
```

### SkillsOrchestrator

Main orchestrator for running workflows.

```python
from sensemaking_skills.runner import SkillsOrchestrator
from sensemaking_skills.config import SkillsConfig
from typing import Dict, Any

class SkillsOrchestrator:
    """Orchestrates skill execution and workflow chaining."""
    
    def __init__(self, config: SkillsConfig):
        """
        Initialize orchestrator.
        
        Args:
            config: SkillsConfig object from ConfigManager.load()
        """
        pass
    
    def run_workflow(
        self,
        workflow_id: str,
        execution_mode: str = ...,  # omission is accepted temporarily but deprecated
        problem_statement: str = "",
        context_artifacts: Dict[str, str] = None,
    ) -> Dict[str, Any]:
        """
        Run a workflow.
        
        Args:
            workflow_id: ID of workflow to run (e.g., "fast-path-workflow")
            execution_mode: Explicit execution mode. Callers should pass one of
                plan_only, guided_execution, autonomous_execution, or yolo_execution.
                Omitting this argument is deprecated; the current compatibility
                fallback is yolo_execution and emits FutureWarning.
            problem_statement: User's problem description (optional)
            context_artifacts: Prior artifacts for chained workflows (optional)
        
        Returns:
            Dict with keys:
              - success: bool
              - artifacts: dict of generated artifacts
              - logs: list of execution logs
              - fog_type: detected problem type
              - recommendations: suggested next steps
        """
        pass
    
    def list_workflows(self) -> Dict[str, Dict[str, Any]]:
        """
        List all available workflows.
        
        Returns:
            Dict mapping workflow_id -> workflow metadata
        """
        pass
    
    def validate_workflow(self, workflow_id: str) -> bool:
        """
        Validate workflow configuration.
        
        Args:
            workflow_id: ID to validate
        
        Returns:
            True if valid, False otherwise
        """
        pass
```

**Example**:
```python
from sensemaking_skills.runner import SkillsOrchestrator
from sensemaking_skills.config import ConfigManager

config_manager = ConfigManager(repo_root=".")
config = config_manager.load()

orchestrator = SkillsOrchestrator(config=config)

result = orchestrator.run_workflow(
    workflow_id="fast-path-workflow",
    execution_mode="autonomous_execution",
    problem_statement="Need to refactor data layer",
)

print(f"Success: {result['success']}")
print(f"Fog type: {result['fog_type']}")
print(f"Artifacts: {list(result['artifacts'].keys())}")
```

### BaseSkill

Base class for creating custom skills.

```python
from sensemaking_skills.skills.base import BaseSkill
from typing import Dict, Any
from abc import abstractmethod

class BaseSkill:
    """Base class for sensemaking skills."""
    
    skill_id: str  # Unique identifier
    version: str  # Semantic version
    description: str  # Human-readable description
    
    def __init__(self, repo_root: str, artifacts_dir: str):
        """
        Initialize skill.
        
        Args:
            repo_root: Repository root directory
            artifacts_dir: Directory for output artifacts
        """
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the skill.
        
        Args:
            context: Input context with problem statement, repo structure, etc.
        
        Returns:
            Dict with artifact_type and generated artifact content
        """
        pass
    
    @property
    @abstractmethod
    def required_inputs(self) -> list:
        """Return list of required context keys."""
        pass
    
    @property
    @abstractmethod
    def output_schema(self) -> Dict[str, str]:
        """Define output structure (field_name -> type)."""
        pass
```

**Example**: See [EXTENDING.md](EXTENDING.md#step-1-create-a-custom-skill-class) for full custom skill example.

---

## Full Example: Custom Analysis Script

This example shows how to use the API to create a custom analysis script:

```python
#!/usr/bin/env python
"""Custom analysis script using sensemaking-skills API."""

from sensemaking_skills.config import ConfigManager
from sensemaking_skills.runner import SkillsOrchestrator
from pathlib import Path
import json
import sys


def analyze_repository(repo_path: str, output_file: str = None) -> dict:
    """
    Analyze a repository and return results.
    
    Args:
        repo_path: Path to repository to analyze
        output_file: Optional file to save results as JSON
    
    Returns:
        Dict with analysis results
    """
    try:
        # 1. Load configuration
        print(f"Loading configuration from {repo_path}...")
        config_manager = ConfigManager(repo_root=repo_path)
        config = config_manager.load()
        print("✓ Configuration loaded")
        
        # 2. Create orchestrator
        print("Initializing orchestrator...")
        orchestrator = SkillsOrchestrator(config=config)
        print("✓ Orchestrator ready")
        
        # 3. Run diagnostic workflow
        print("\nRunning diagnostic workflow...")
        result = orchestrator.run_workflow(
            workflow_id="fast-path-workflow",
            execution_mode="autonomous_execution",
            problem_statement="Perform full repository analysis",
        )
        
        # 4. Check success
        if not result["success"]:
            print(f"✗ Workflow failed: {result.get('error', 'Unknown error')}")
            return {"success": False, "error": result.get("error")}
        
        print("✓ Workflow complete")
        
        # 5. Extract results
        artifacts = result.get("artifacts", {})
        fog_type = result.get("fog_type")
        recommendations = result.get("recommendations", [])
        
        print(f"\nAnalysis Results:")
        print(f"  Fog Type: {fog_type}")
        print(f"  Artifacts Generated: {len(artifacts)}")
        print(f"  Recommendations: {len(recommendations)}")
        
        # 6. Prepare output
        output = {
            "success": True,
            "repo_path": repo_path,
            "fog_type": fog_type,
            "artifact_count": len(artifacts),
            "artifact_types": list(artifacts.keys()),
            "recommendations": recommendations,
            "artifacts_dir": config.artifacts_dir,
        }
        
        # 7. Save results if requested
        if output_file:
            with open(output_file, "w") as f:
                json.dump(output, f, indent=2)
            print(f"\n✓ Results saved to {output_file}")
        
        return output
    
    except FileNotFoundError as e:
        print(f"✗ Configuration not found: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"✗ Error during analysis: {e}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    repo = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = analyze_repository(repo, output_file)
    
    exit_code = 0 if result["success"] else 1
    sys.exit(exit_code)
```

**Run the script**:
```bash
python analysis_script.py /path/to/repo results.json
```

---

## Integration with CI/CD

### GitHub Actions Example

Integrate sensemaking-skills into your CI/CD pipeline:

```yaml
# .github/workflows/analyze.yml

name: Repository Analysis

on:
  pull_request:
  push:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install sensemaking-skills
        run: pip install sensemaking-skills
      
      - name: Initialize configuration
        run: sensemaking-skills init --repo .
      
      - name: Run analysis
        run: |
          sensemaking-skills analyze \
            --repo . \
            --workflow fast-path-workflow \
            --mode autonomous_execution
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: sensemaking-artifacts
          path: .sensemaking/artifacts/
        if: always()
```

### Python Script in CI/CD

```python
# scripts/ci_analysis.py

#!/usr/bin/env python
"""Run sensemaking analysis in CI/CD pipeline."""

from sensemaking_skills.config import ConfigManager
from sensemaking_skills.runner import SkillsOrchestrator
import sys


def main():
    """Run analysis and report results."""
    try:
        # Load and run
        config = ConfigManager(repo_root=".").load()
        orchestrator = SkillsOrchestrator(config=config)
        
        result = orchestrator.run_workflow(
            workflow_id="fast-path-workflow",
            execution_mode="autonomous_execution",
        )
        
        # Report
        if result["success"]:
            print(f"✓ Analysis complete (Fog type: {result['fog_type']})")
            return 0
        else:
            print(f"✗ Analysis failed: {result.get('error')}")
            return 1
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
```

---

## Error Handling

Always handle errors gracefully:

```python
from sensemaking_skills.config import ConfigManager
from sensemaking_skills.runner import SkillsOrchestrator


def safe_analyze(repo_path: str) -> dict:
    """Safely analyze repository with error handling."""
    try:
        # 1. Load config
        config_manager = ConfigManager(repo_root=repo_path)
        config = config_manager.load()
    
    except FileNotFoundError:
        return {
            "success": False,
            "error": "Configuration not found. Run 'sensemaking-skills init' first.",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to load configuration: {e}",
        }
    
    try:
        # 2. Run workflow
        orchestrator = SkillsOrchestrator(config=config)
        result = orchestrator.run_workflow(
            workflow_id="fast-path-workflow",
            execution_mode="autonomous_execution",
        )
        return result
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Workflow execution failed: {e}",
        }
```

---

## Logging

Enable logging to see detailed execution information:

```python
import logging
from sensemaking_skills.config import ConfigManager
from sensemaking_skills.runner import SkillsOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Now run your code - you'll see detailed logs
config = ConfigManager(repo_root=".").load()
orchestrator = SkillsOrchestrator(config=config)
result = orchestrator.run_workflow(
    workflow_id="fast-path-workflow",
    execution_mode="guided_execution",
)
```

---

## Type Hints

The API uses Python type hints for better IDE support and type checking:

```python
from typing import Dict, Any, Optional
from pathlib import Path
from sensemaking_skills.config import ConfigManager, SkillsConfig
from sensemaking_skills.runner import SkillsOrchestrator


def analyze(repo: Path, mode: str = "guided_execution") -> Dict[str, Any]:
    """Analyze repository and return results."""
    config_manager: ConfigManager = ConfigManager(str(repo))
    config: SkillsConfig = config_manager.load()
    
    orchestrator: SkillsOrchestrator = SkillsOrchestrator(config=config)
    result: Dict[str, Any] = orchestrator.run_workflow(
        workflow_id="fast-path-workflow",
        execution_mode=mode,
    )
    
    return result
```

---

## Next Steps

- **Installation**: See [INSTALLATION.md](INSTALLATION.md) for setup instructions
- **Extension**: See [EXTENDING.md](EXTENDING.md) to create custom skills
- **Examples**: See [docs/examples/](docs/examples/) for more code samples
- **CLI Usage**: See [GETTING_STARTED.md](GETTING_STARTED.md) for command-line interface

---

## Support

- **Documentation**: See [README.md](README.md) for full feature overview
- **Issues**: Report bugs at https://github.com/dimmi-andreus/sensemaking-skills/issues
- **Discussions**: Ask questions at https://github.com/dimmi-andreus/sensemaking-skills/discussions

---

## License

MIT License - See [LICENSE](LICENSE) for details.