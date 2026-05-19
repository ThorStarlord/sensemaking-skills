# Deployment Guide: Sensemaking Skills in Production

## Deployment Architecture

The system is designed for three deployment scenarios:

### Scenario 1: Local Development
Single machine with manual workflow execution.

### Scenario 2: CI/CD Pipeline (Recommended)
Integrated with GitHub Actions, GitLab CI, or Jenkins for automated workflow execution.

### Scenario 3: Multi-Tenant Service
Deployed as a service with portfolio orchestration for multiple projects.

## Prerequisites

- Python 3.9+
- Git
- 2GB disk space minimum
- 1GB RAM minimum

## Installation Steps

1. **Clone repository**
   ```bash
   git clone https://github.com/your-org/sensemaking-skills.git
   cd sensemaking-skills
   ```

2. **Install dependencies**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python scripts/workflow-runtime.py --list-workflows
   ```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Sensemaking Workflow
on: [workflow_dispatch, schedule: {cron: '0 2 * * 0'}]

jobs:
  orchestrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python scripts/portfolio-orchestrator.py --mode autonomous_execution
```

## Monitoring and Logging

Logs are automatically created in:
- `artifacts/NN-project-name/` — Run folder with numbered pipeline artifacts
- `artifacts/run_log_<workflow>_<timestamp>.md` — Historical execution log (pre-organization)
- `artifacts/execution_plan_<workflow>.json` — Historical execution plan (pre-organization)

Monitor these files for:
- Execution success/failure
- Validator results
- Gate decisions
- Error codes

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for common issues and solutions.

## Support

For deployment questions, consult:
- `docs/CUSTOMER_ONBOARDING.md` — Getting started
- `docs/TROUBLESHOOTING.md` — Common issues
- `docs/validator-ecosystem/ARCHITECTURE.md` — System design
