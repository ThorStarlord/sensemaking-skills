# Extending Sensemaking Skills

Customize sensemaking-skills by adding custom skills, defining new workflows, and overriding canonical vocabulary.

---

## Adding Custom Skills

### Step 1: Create a Custom Skill Class

Create a Python file in your project's `.sensemaking/skills/` directory:

```python
# .sensemaking/skills/security_auditor.py

from sensemaking_skills.skills.base import BaseSkill
from pathlib import Path
from typing import Dict, Any


class SecurityAuditorSkill(BaseSkill):
    """Security auditor skill for vulnerability assessment."""

    skill_id = "security-auditor"
    version = "1.0.0"
    description = "Audits codebase for security vulnerabilities and patterns"

    def __init__(self, repo_root: str, artifacts_dir: str):
        super().__init__(repo_root, artifacts_dir)
        self.repo_path = Path(repo_root)

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze repository for security issues.

        Args:
            context: Dict containing:
              - problem_statement: User's problem description
              - repo_structure: Repository file tree
              - fog_type: Detected fog type

        Returns:
            Dict with keys:
              - security_brief: Security audit findings
              - vulnerabilities: List of identified issues
              - recommendations: List of remediation steps
        """
        problem = context.get("problem_statement", "")
        repo_structure = context.get("repo_structure", "")

        # Analyze codebase for security patterns
        vulnerabilities = self._find_vulnerabilities(repo_structure)
        recommendations = self._generate_recommendations(vulnerabilities)

        brief = f"""# Security Audit Brief

## Vulnerabilities Found
{vulnerabilities}

## Recommendations
{recommendations}

## Priority
High: {len([v for v in vulnerabilities if 'critical' in v.lower()])} critical issues
"""

        return {
            "artifact_type": "security_brief",
            "artifact_version": "1.0.0",
            "security_brief": brief,
            "vulnerabilities": vulnerabilities,
            "recommendations": recommendations,
            "status": "complete",
        }

    def _find_vulnerabilities(self, repo_structure: str) -> str:
        """Find potential security vulnerabilities."""
        # Implementation: scan for hardcoded secrets, exposed API keys, etc.
        findings = []

        if "password" in repo_structure.lower():
            findings.append("- Potential hardcoded passwords detected")
        if "api_key" in repo_structure.lower():
            findings.append("- Potential exposed API keys detected")

        return "\n".join(findings) if findings else "- No critical vulnerabilities detected"

    def _generate_recommendations(self, vulnerabilities: str) -> str:
        """Generate remediation recommendations."""
        recommendations = [
            "1. Implement environment variable management for secrets",
            "2. Add pre-commit hooks to block committed secrets",
            "3. Use dependency scanning tools (safety, bandit)",
            "4. Implement SAST (Static Application Security Testing)",
        ]
        return "\n".join(recommendations)

    @property
    def required_inputs(self) -> list:
        """Return required context fields."""
        return ["problem_statement", "repo_structure"]

    @property
    def output_schema(self) -> Dict[str, str]:
        """Define output structure."""
        return {
            "artifact_type": "security_brief",
            "artifact_version": "1.0.0",
            "security_brief": "str",
            "vulnerabilities": "list",
            "recommendations": "list",
            "status": "str",
        }
```

### Step 2: Register the Skill

Add your skill to the skill registry in your custom `sensemaking-config.yaml`:

```yaml
# sensemaking-config.yaml

repo_root: /path/to/repo
artifacts_dir: .sensemaking/artifacts

# Load custom skills
skills:
  enabled:
    - repo-sensemaker        # Built-in
    - workflow-planner       # Built-in
    - security-auditor       # Custom (from .sensemaking/skills/)
  
  custom_paths:
    - .sensemaking/skills    # Directory containing custom skill modules
```

---

## Define Custom Workflow in sensemaking-config.yaml

### Workflow Definition

Create a custom workflow that chains your skills:

```yaml
# sensemaking-config.yaml

workflows:
  custom-workflow:
    id: custom-workflow
    name: "Custom Security + Implementation Workflow"
    description: "Audits security then generates implementation plan"
    
    # Skill sequence - skills execute in order
    skill_sequence:
      - security-auditor
      - repo-sensemaker
      - workflow-planner
    
    # Gates: pause for user approval at specific steps
    approval_gates:
      - after_step: security-auditor
        message: "Review security findings before proceeding"
      - after_step: repo-sensemaker
        message: "Approve repository brief"
    
    # Automatic routing based on detected fog type
    auto_invoke_next_workflow: true
    
    # Which workflow to invoke after this one completes (by fog_type)
    chained_workflows:
      product_fog: product-implementation-workflow
      ui_fog: ui-implementation-workflow
      docs_fog: docs-implementation-workflow
      architecture_fog: implementation-workflow
```

### Run Custom Workflow

```bash
sensemaking-skills analyze --repo /path/to/repo \
  --workflow custom-workflow \
  --mode guided_execution
```

---

## Composing Workflows

### Combining Built-in and Custom Skills

Mix built-in and custom skills in any sequence:

```yaml
workflows:
  full-security-implementation:
    skill_sequence:
      # Diagnostic phase
      - repo-sensemaker          # Built-in: analyze repository
      - security-auditor         # Custom: find vulnerabilities
      
      # Planning phase
      - workflow-planner         # Built-in: recommend workflow
      
      # Implementation phase (auto-chained)
      - to-prd                   # Built-in (external skill pack)
      - to-issues                # Built-in (external skill pack)
      - security-remediation     # Custom: generate security fixes
```

### Conditional Routing

Route to different workflows based on detected fog type:

```yaml
workflows:
  intelligent-analyzer:
    skill_sequence:
      - repo-sensemaker
      - workflow-planner
    
    # Route to implementation based on fog type
    chained_workflows:
      product_fog: product-implementation-workflow
      security_fog: custom-workflow  # Your custom workflow
      ui_fog: ui-implementation-workflow
```

---

## Overriding Canonical Vocabulary

### Adding Custom Fog Types

Extend the fog type classification system:

```yaml
# sensemaking-config.yaml

vocabulary:
  fog_types:
    # Built-in types
    - product_fog
    - ui_fog
    - docs_fog
    - architecture_fog
    
    # Custom types
    - security_fog        # New type for security-focused analysis
    - performance_fog     # New type for performance issues
    - infrastructure_fog  # New type for DevOps/infrastructure
```

### Adding Custom Fields to Artifacts

Extend artifact structure with custom fields:

```yaml
vocabulary:
  artifact_fields:
    repository_sensemaking_brief:
      # Built-in fields
      - fog_type
      - weakest_boundary
      - recommended_workflows
      
      # Custom fields
      - security_score          # New: vulnerability severity rating
      - performance_metrics     # New: code quality scores
      - infrastructure_notes    # New: deployment constraints
```

### Custom Validation Rules

Define validation rules for custom fields:

```yaml
vocabulary:
  validation_rules:
    security_score:
      type: integer
      min: 0
      max: 100
      required: true
      description: "Security assessment score"
    
    performance_metrics:
      type: object
      required: false
      fields:
        - coverage_percent
        - avg_query_time_ms
        - cache_hit_rate
```

---

## Full Example: Custom Security Workflow

### Files to Create

Create this directory structure:

```
your-repo/
├── .sensemaking/
│   ├── skills/
│   │   └── security_auditor.py      # Custom skill
│   └── artifacts/                    # Output location
└── sensemaking-config.yaml          # Configuration
```

### 1. Custom Skill (`security_auditor.py`)

```python
from sensemaking_skills.skills.base import BaseSkill
from pathlib import Path
from typing import Dict, Any
import re


class SecurityAuditorSkill(BaseSkill):
    """Security auditor skill for vulnerability assessment."""

    skill_id = "security-auditor"
    version = "1.0.0"
    description = "Audits codebase for security vulnerabilities"

    def __init__(self, repo_root: str, artifacts_dir: str):
        super().__init__(repo_root, artifacts_dir)
        self.repo_path = Path(repo_root)

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze repository for security issues."""
        repo_structure = context.get("repo_structure", "")
        
        issues = self._scan_for_issues(repo_structure)
        brief = self._generate_brief(issues)

        return {
            "artifact_type": "security_brief",
            "artifact_version": "1.0.0",
            "security_brief": brief,
            "issues": issues,
            "severity": self._assess_severity(issues),
            "status": "complete",
        }

    def _scan_for_issues(self, repo_structure: str) -> list:
        """Scan for common security issues."""
        issues = []
        
        patterns = {
            "hardcoded_secrets": r"(?i)(password|secret|api[_-]?key|token)[\s:=]+['\"]?[a-z0-9]{8,}",
            "sql_injection": r"(?i)(execute|query).*\$\{",
            "path_traversal": r"(?i)open.*\.\./",
        }
        
        for issue_type, pattern in patterns.items():
            if re.search(pattern, repo_structure):
                issues.append({"type": issue_type, "severity": "high"})
        
        return issues

    def _generate_brief(self, issues: list) -> str:
        """Generate security audit brief."""
        if not issues:
            return "# Security Audit\n\nNo critical vulnerabilities detected."
        
        brief = "# Security Audit\n\n## Issues Found\n"
        for issue in issues:
            brief += f"- {issue['type']} (Severity: {issue['severity']})\n"
        
        return brief

    def _assess_severity(self, issues: list) -> str:
        """Assess overall security severity."""
        if not issues:
            return "low"
        high_count = len([i for i in issues if i.get("severity") == "high"])
        return "critical" if high_count >= 3 else "high" if high_count > 0 else "medium"

    @property
    def required_inputs(self) -> list:
        return ["repo_structure"]

    @property
    def output_schema(self) -> Dict[str, str]:
        return {
            "artifact_type": "security_brief",
            "security_brief": "str",
            "issues": "list",
            "severity": "str",
        }
```

### 2. Configuration (`sensemaking-config.yaml`)

```yaml
repo_root: .
artifacts_dir: .sensemaking/artifacts

execution_mode: guided_execution

# Enable custom skills
skills:
  enabled:
    - repo-sensemaker
    - security-auditor
    - workflow-planner
  
  custom_paths:
    - .sensemaking/skills

# Define custom workflow
workflows:
  security-first-workflow:
    id: security-first-workflow
    name: "Security-First Analysis and Implementation"
    description: "Audits security first, then implements solutions"
    
    skill_sequence:
      - security-auditor
      - repo-sensemaker
      - workflow-planner
    
    approval_gates:
      - after_step: security-auditor
        message: "Review security findings"
    
    auto_invoke_next_workflow: true
    
    chained_workflows:
      product_fog: product-implementation-workflow
      architecture_fog: implementation-workflow

# Custom vocabulary
vocabulary:
  fog_types:
    - product_fog
    - ui_fog
    - docs_fog
    - architecture_fog
    - security_fog
```

### 3. Run the Custom Workflow

```bash
# Initialize
sensemaking-skills init --repo .

# Run custom workflow
sensemaking-skills analyze --repo . \
  --workflow security-first-workflow \
  --mode guided_execution
```

---

## Best Practices

### 1. Artifact Contracts

Document your skill's input and output format in `output_schema`:

```python
@property
def output_schema(self) -> Dict[str, str]:
    """Define what your skill produces."""
    return {
        "artifact_type": "security_brief",  # Must match usage
        "security_brief": "str",            # Field type
        "issues": "list",
        "severity": "str",
    }
```

### 2. Error Handling

Handle missing inputs gracefully:

```python
def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute with proper error handling."""
    try:
        repo_structure = context.get("repo_structure")
        if not repo_structure:
            raise ValueError("repo_structure required but not provided")
        
        result = self._analyze(repo_structure)
        return result
    
    except Exception as e:
        return {
            "artifact_type": "error",
            "error": str(e),
            "status": "failed",
        }
```

### 3. Logging

Use standard Python logging for debugging:

```python
import logging

logger = logging.getLogger(__name__)

class MySkill(BaseSkill):
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Starting analysis of {context.get('repo_root')}")
        try:
            result = self._do_work(context)
            logger.info("Analysis complete")
            return result
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise
```

### 4. Testing Custom Skills

Write tests for your skills:

```python
# tests/test_security_auditor.py

import pytest
from pathlib import Path
from .security_auditor import SecurityAuditorSkill


def test_security_auditor_finds_hardcoded_secrets():
    """Test that security auditor detects hardcoded secrets."""
    skill = SecurityAuditorSkill(repo_root=".", artifacts_dir=".sensemaking/artifacts")
    
    context = {
        "repo_structure": "password = 'secret123'"
    }
    
    result = skill.execute(context)
    
    assert result["status"] == "complete"
    assert len(result["issues"]) > 0
    assert any(i["type"] == "hardcoded_secrets" for i in result["issues"])
```

---

## Next Steps

- **Integration**: See [INSTALLATION.md](INSTALLATION.md) to integrate custom skills
- **API Usage**: See [API.md](API.md) to use custom skills in Python code
- **Examples**: See [docs/examples/](docs/examples/) for more patterns
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md) to share your skills

---

## Support

- **Skill Development**: Read [docs/skill-development.md](docs/skill-development.md)
- **Artifact Contracts**: See [docs/artifact-contracts.md](docs/artifact-contracts.md)
- **Issues**: Report problems at https://github.com/dimmi-andreus/sensemaking-skills/issues
