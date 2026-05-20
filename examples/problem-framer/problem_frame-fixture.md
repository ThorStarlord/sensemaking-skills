# Problem Frame: Workflow Orchestration & Skill Execution

## Problem Under Pressure
How should skills be invoked to produce artifacts during workflow orchestration?

## Object Under Pressure
The `skill_executor` module and its integration with `workflow-runtime.py` execute_step() function.

## The Problem
The sensemaking-skills repository has a working orchestration system (workflow-runtime.py) that can plan and validate workflow execution, but it cannot currently execute skills to generate the intermediate artifacts that each step depends on. This blocks end-to-end workflow testing and real-world usage.

### What's working:
- ✅ Workflow registry and artifact contracts are well-defined
- ✅ Orchestration plan generation works
- ✅ Validator infrastructure is robust (zero-tolerance in yolo mode)
- ✅ Run logging and audit trails are complete
- ✅ Error messages are clear and actionable

### What's broken:
- ❌ Skills cannot be invoked during workflow execution
- ❌ Artifacts are not generated for downstream steps
- ❌ Workflow halts after Step 1 due to missing artifacts
- ❌ Integration testing is impossible without skill execution

## Strategic Question
What is the simplest path to enable:
1. **Short-term**: Test orchestration logic with fixture artifacts (no skill execution)
2. **Medium-term**: Execute skills to produce real artifacts (Claude API or subprocess)
3. **Long-term**: Multi-user skill execution with caching and versioning

## Forces at Play
- **Time pressure**: Need working end-to-end flow for validation testing
- **Unknown unknowns**: Skill execution architecture not yet designed
- **Testing gap**: Can't validate orchestration without progressing through steps
- **User experience**: Error messages need to be clear about what's missing

## Machine-readable metadata

```yaml
problem_type: "architecture_fog"
object_under_pressure: "skill_executor"
strategic_question_id: "skill_execution_mechanism"
severity: "critical"
impact: "workflow_execution_blocked"
```
