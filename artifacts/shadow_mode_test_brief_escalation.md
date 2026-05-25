# Repository Sensemaking Brief: Escalation Test

**Repository**: escalation-test-repo  
**Analysis Date**: 2026-05-25  
**Analyzer**: Shadow Mode Test Suite  

---

## 1. Repository Overview

A complex monorepo with mixed architecture patterns that require expert analysis.

---

## 2. Architecture Analysis

Omitted for brevity in this test artifact.

---

## 3. Fog Type Classification

### Primary Fog Type: product_fog
**Confidence**: 45%
**Reasoning**: Some product signals but mixed with other fog types

### Escalation Assessment
- **Escalation Recommended**: true
- **Reasoning**: Mixed fog signals (product, docs, architecture) require full-fog-workflow
- **Recommended Workflow**: full-fog-workflow

---

## 13. Machine-readable brief

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
repository_name: escalation-test-repo
primary_fog_type: product_fog
confidence_level: 45
evidence:
  - "Mixed architectural patterns detected"
  - "Product signals conflict with architectural signals"
  - "Expert analysis recommended"
escalation_recommended: true
recommended_workflow_id: full-fog-workflow
immutable: true
```
