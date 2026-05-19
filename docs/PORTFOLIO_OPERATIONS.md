# Portfolio Operations Guide

## Introduction

The Portfolio Orchestrator enables organizations to manage multiple projects flowing through the sensemaking system simultaneously. Instead of working on one project at a time, teams can batch-process portfolios of related or independent projects.

## Quick Start

### Scenario 1: Rapid Startup Validation (5 ideas, plan_only mode)

You have 5 startup ideas and want to quickly validate which workflows they'd follow:

```bash
# Create a portfolio directory
mkdir portfolio-validation
cp idea-1.md idea-2.md idea-3.md idea-4.md idea-5.md portfolio-validation/

# Run portfolio validation
python scripts/portfolio-orchestrator.py \
  --projects-dir portfolio-validation \
  --mode plan_only \
  --parallel 5

# Review artifacts/portfolio_report.md
```

**Output**: Which workflows each idea maps to, without executing anything.  
**Time**: ~1-2 seconds.

### Scenario 2: Full Execution with Parallelism (3 SaaS projects)

You have 3 SaaS product ideas ready for full pipeline execution:

```bash
mkdir saas-portfolio
cp project-{a,b,c}.md saas-portfolio/

python scripts/portfolio-orchestrator.py \
  --projects-dir saas-portfolio \
  --mode autonomous_execution \
  --parallel 3 \
  --report-out saas_results.md
```

**Output**: All 3 projects routed and workflows executed in parallel.  
**Time**: Depends on workflow complexity (typically 5-15 minutes).

### Scenario 3: Batch Handoff to Teams

You want to generate a portfolio plan for review by downstream teams:

```bash
mkdir team-handoff
cp projects/*.md team-handoff/

python scripts/portfolio-orchestrator.py \
  --projects-dir team-handoff \
  --mode plan_only \
  --json \
  --report-out team_briefing.json
```

**Output**: JSON report that teams can parse and use for planning.

## Common Workflows

### Portfolio Intake & Triage

**Goal**: Quickly classify incoming project ideas without executing

```bash
# 1. Create intake directory
mkdir intake/$(date +%Y-%m-%d)

# 2. Move all incoming project files
mv /inbox/*.md intake/$(date +%Y-%m-%d)/

# 3. Run portfolio classification
python scripts/portfolio-orchestrator.py \
  --projects-dir intake/$(date +%Y-%m-%d) \
  --mode plan_only \
  --parallel 10

# 4. Review artifacts/portfolio_report.md
less artifacts/portfolio_report.md

# 5. Archive report with intake
cp artifacts/portfolio_report.md intake/$(date +%Y-%m-%d)/triage_results.md
```

**Time to triage**: ~5 seconds for 10 projects

### Parallel Full Pipeline Execution

**Goal**: Execute 3 projects through their complete workflows simultaneously

```bash
mkdir execution/wave-1
cp wave-1-projects/*.md execution/wave-1/

python scripts/portfolio-orchestrator.py \
  --projects-dir execution/wave-1 \
  --mode guided_execution \
  --parallel 3 \
  --report-out execution/wave-1/results.md

# Each project generates artifacts in artifacts/ directory
# Final portfolio report available immediately after all complete
```

**Notes**:
- With `guided_execution`, gates at each step require user review
- Review happens in sequence (safest)
- Or use `autonomous_execution` to skip gates entirely

### Periodic Portfolio Health Check

**Goal**: Monitor a portfolio of ongoing projects monthly

```bash
#!/bin/bash
# monthly-portfolio-check.sh

DATE=$(date +%Y-%m-%d)
REPORT_DIR="reports/$DATE"
mkdir -p "$REPORT_DIR"

python scripts/portfolio-orchestrator.py \
  --projects-dir ongoing-projects \
  --mode plan_only \
  --json \
  --report-out "$REPORT_DIR/portfolio_$(date +%s).json"

# Analyze trends
echo "Portfolio Status Report for $DATE" > "$REPORT_DIR/summary.txt"
echo "Total Projects: $(jq '.total_projects' $REPORT_DIR/*.json | tail -1)" >> "$REPORT_DIR/summary.txt"
echo "Average Routing Time: $(jq '.total_time' $REPORT_DIR/*.json | awk '{sum+=$1} END {print sum/NR}')" >> "$REPORT_DIR/summary.txt"

# Archive
tar czf "reports/archive/${DATE}_portfolio.tar.gz" "$REPORT_DIR"
```

### Confidence-Based Filtering

**Goal**: Only execute high-confidence projects, plan uncertain ones

```bash
# All projects as JSON
python scripts/portfolio-orchestrator.py \
  --projects-dir projects \
  --mode plan_only \
  --json \
  --report-out full_analysis.json

# Extract high-confidence projects
jq '.results[] | select(.confidence >= 80)' full_analysis.json | jq -r '.project_name' > high_confidence.txt

# Create high-confidence directory
mkdir high-conf-projects
while read proj; do
  cp "projects/$proj.md" high-conf-projects/
done < high_confidence.txt

# Execute high-confidence projects
python scripts/portfolio-orchestrator.py \
  --projects-dir high-conf-projects \
  --mode autonomous_execution \
  --parallel 5
```

## Mode Selection Guide

### When to Use plan_only
- **Intake & triage**: Classify projects without commitment
- **Validation**: Verify routing is correct
- **Team review**: Present plans for stakeholder sign-off before execution
- **Learning**: Explore how workflows map to different project types

**Command**: `--mode plan_only`

### When to Use guided_execution
- **Default for new projects**: Each step reviewed by human
- **High-risk domains**: Where decisions need verification
- **Process training**: Team learning about workflows
- **Complex interdependencies**: Between project steps

**Command**: `--mode guided_execution`  
**Note**: Requires user review at each step

### When to Use autonomous_execution
- **Mature processes**: Well-understood project types
- **High-confidence projects**: Confidence score ≥ 80%
- **Batch processing**: Running many projects at scale
- **Time-sensitive**: Need quick turnaround

**Command**: `--mode autonomous_execution`  
**Note**: Gates are automated, no human review required

### When to Use yolo_execution
- **Experimental**: Testing new workflows
- **Rapid prototyping**: Speed over safety
- **Non-critical projects**: Low-risk, exploratory work
- **Demo/PoC**: Proof of concept

**Command**: `--mode yolo_execution`  
**Note**: Minimal safeguards, gates bypassed

## Parallelism Configuration

### Rule of Thumb for Worker Count

| Scenario | Recommended | Reasoning |
|:---|:---:|:---|
| Personal/laptop | 2-3 | Limit CPU usage |
| Single server | 5-10 | Balanced execution |
| CI/CD pipeline | 10-20 | Maximize throughput |
| Batch job on cluster | 50+ | Full resource utilization |

### Memory & CPU Considerations

Each parallel worker needs:
- **Memory**: ~50-100MB (Python process overhead)
- **CPU**: ~1 core (router CPU time is minimal)
- **I/O**: Project file read + output write

**Formula**: `max_workers = (total_available_memory / 100) * 0.8`

### Finding Optimal Parallelism

```bash
# Test with increasing worker counts
for workers in 1 2 3 5 10; do
  time python scripts/portfolio-orchestrator.py \
    --projects-dir test-projects \
    --parallel $workers \
    --mode plan_only
done

# Note the time for each - sweet spot is where time plateaus
```

## Troubleshooting

### "Portfolio report is empty"

**Problem**: Results list shows 0 projects processed.

**Solution**:
1. Verify project files exist: `ls projects/*.md`
2. Check file format: `head projects/project-*.md`
3. Run in verbose mode with stderr output

### "Routing confidence is too low"

**Problem**: Projects keep getting classified as "research" (confidence < 70%)

**Solution**:
1. Add clearer terminology to project descriptions
2. Explicitly mention project type: "SaaS", "mobile app", "tool", etc.
3. Check against classification guide in `scripts/router.py`
4. File issue if you think classification is wrong

### "Execution timeout / execution never completes"

**Problem**: Workflow execution hangs or times out.

**Solution**:
1. Check individual project: `python scripts/workflow-runtime.py <workflow> --mode plan_only`
2. Verify git working tree is clean
3. Check disk space for artifact generation
4. Increase timeout if needed: edit `scripts/portfolio-orchestrator.py` line ~180

### "Port already in use" (if running web services)

**Problem**: Workflows bind to ports and multiple projects conflict.

**Solution**:
1. Run in `plan_only` mode (no execution)
2. Use lower parallelism to space out startup times
3. Configure projects to use different ports in their descriptions

## Performance Monitoring

### Basic Metrics

```bash
# Extract timing from JSON report
python -c "
import json
with open('artifacts/portfolio_report.md') as f:
    data = json.load(f)
    times = [r['execution_time'] for r in data['results']]
    print(f'Total: {data[\"total_time\"]}s')
    print(f'Min: {min(times):.1f}s')
    print(f'Max: {max(times):.1f}s')
    print(f'Avg: {sum(times)/len(times):.1f}s')
"
```

### Scaling Efficiency

```bash
# Measure parallelism benefit
parallel_time=$(time ... --parallel 5 2>&1 | grep real)
sequential_time=$(time ... --parallel 1 2>&1 | grep real)
efficiency=$((sequential_time / parallel_time))
echo "Parallel speedup: ${efficiency}x"
```

**Ideal**: Near-linear speedup up to CPU core count  
**Expected**: 80-90% efficiency with 5-10 workers

## Integration Examples

### GitHub Actions CI/CD

```yaml
name: Portfolio Routing

on:
  push:
    paths:
      - 'projects/**'

jobs:
  route:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - name: Run portfolio orchestrator
        run: |
          python scripts/portfolio-orchestrator.py \
            --projects-dir projects \
            --mode plan_only \
            --json \
            --report-out portfolio_result.json
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: portfolio-report
          path: portfolio_result.json
```

### Airflow DAG

```python
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG('portfolio-orchestration') as dag:
    orchestrate = BashOperator(
        task_id='orchestrate_portfolio',
        bash_command='''
            python /repo/scripts/portfolio-orchestrator.py \
              --projects-dir /inbox/projects \
              --mode autonomous_execution \
              --parallel 5 \
              --report-out /output/portfolio_results.md
        '''
    )
```

## Best Practices

1. **Start with plan_only**: Always run in plan_only mode first to verify routing
2. **Archive reports**: Keep portfolio reports for audit trail
3. **Version projects**: Include date in project filenames (project-2026-05-16-saas.md)
4. **Monitor confidence**: Track confidence scores over time
5. **Batch by type**: Group similar project types together
6. **Schedule off-peak**: Run large portfolios during low-traffic times
7. **Test incrementally**: Run 2-3 projects before running 50+
8. **Document assumptions**: Record why each project uses its selected workflow

## FAQ

**Q: Can I run the same project multiple times?**  
A: Yes, but the orchestrator will process it like a new project. Use versioning: `project-v1.md`, `project-v2.md`

**Q: What if a project fails mid-workflow?**  
A: Portfolio continues processing other projects. Failed project is marked in report.

**Q: Can I pause/resume portfolio?**  
A: Not currently. Run `plan_only` to review before full execution.

**Q: How do I update an already-processed project?**  
A: Modify the .md file and re-run the portfolio. The system will re-classify and re-route.

**Q: Can I specify project execution order?**  
A: Not in current version. Projects are processed in parallel, order is arbitrary.

## Support

For issues or questions:
1. Check this guide
2. Review project classification in `scripts/router.py`
3. Test single project: `python scripts/router.py project.md`
4. File issue with: project description + expected workflow
