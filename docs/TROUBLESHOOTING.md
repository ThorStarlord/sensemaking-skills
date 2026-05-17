# Troubleshooting Guide

## Common Issues and Solutions

### Error: WORKFLOW_NOT_FOUND

**Problem**: Workflow doesn't exist or typo in workflow ID.

**Solution**:
1. List available workflows: `python scripts/orchestration-runner.py --list-workflows`
2. Check spelling of workflow ID
3. Verify workflow-registry.yaml exists in `skills/workflow-orchestrator/references/`

### Error: MODE_NOT_ALLOWED

**Problem**: Requested mode not supported for this workflow.

**Solution**:
1. Check workflow definition in workflow-registry.yaml
2. Verify execution mode in allowed_execution_modes list
3. Try a supported mode (plan_only always supported)

### Error: ARTIFACT_NOT_FOUND

**Problem**: Workflow step output artifact wasn't created.

**Solution**:
1. Check execution log: `artifacts/run_log_<workflow>_<mode>.md`
2. Verify all previous steps passed validation
3. Check artifact contracts in `artifact-contracts.yaml`

### Error: VALIDATOR_FAILED

**Problem**: Output artifact failed validation.

**Solution**:
1. Review validator output in run log
2. Check validator expectations in artifact contracts
3. Verify artifact format matches contract specification

### Error: EXECUTION_TIMEOUT

**Problem**: Workflow execution exceeded timeout limit.

**Solution**:
1. Increase timeout: `--timeout 7200` (default 3600)
2. Run in plan_only mode first to check complexity
3. Check system resources (disk, memory)

## Debugging

### Enable Verbose Logging

```bash
python scripts/orchestration-runner.py <workflow> --verbose
```

### Check Execution Log

After each run, review:
```bash
cat artifacts/run_log_<workflow>_<timestamp>.md
```

### Inspect Artifacts

```bash
ls -la artifacts/
cat artifacts/<artifact_name>
```

## Performance Tuning

### Slow Execution

- Check system load: `top` or `Task Manager`
- Try plan_only mode to isolate bottleneck
- Review validator output for performance issues

### High Memory Usage

- Run one workflow at a time (not portfolio-orchestrator)
- Check for large input artifacts
- Monitor with `ps aux | grep python`

## Production Support

For production issues:
1. Capture full error output
2. Save artifacts and logs
3. Check system resources
4. Review `docs/DEPLOYMENT_GUIDE.md`
5. Contact your system administrator

## Error Code Reference

| Code | Meaning | Action |
|------|---------|--------|
| WORKFLOW_NOT_FOUND | Workflow doesn't exist | Verify workflow ID |
| MODE_NOT_ALLOWED | Mode not supported | Check allowed modes |
| ARTIFACT_NOT_FOUND | Output missing | Check step success |
| VALIDATOR_FAILED | Validation failed | Review validator output |
| GATE_DENIED | User denied gate | Re-run with approval |
| EXECUTION_TIMEOUT | Exceeded time limit | Increase timeout |

---

**For additional help**: See `docs/CUSTOMER_ONBOARDING.md` or contact your administrator.
