# Metamorfose Classes System - Run Analysis

**Date**: 2026-05-17  
**Project**: Metamorfose Edutech Classes Management Subsystem  
**Artifacts**: 04 files  

## Summary

Sensemaking pipeline analysis of classes system design clarity. Identified hidden knowledge (undocumented storage strategy) and design gaps (student-class relationships). Executed grill-with-docs to resolve storage question. Discovered documentation drift: code uses Supabase but UI labels contradicted this.

## Files

1. **problem-frame.md** — Problem statement: under-specified data model and relationships
2. **unknowns-map.md** — 8 unknowns mapped; research_needed = true (different from Finance: design-incomplete vs. implementation-driven)
3. **sensemaking-brief.md** — Diagnostic identifying undocumented storage strategy as weakest boundary
4. **grilled-findings.md** — Validation via grill-with-docs: Storage IS Supabase, but documentation was scattered and UI contradicted reality

## Key Findings

- unknowns_count: 8 (triggers research)
- clarity_assessment: high (contrasts with Finance's "medium")
- Problem type: Design-incomplete (hidden knowledge), not implementation-driven (like Finance)
- Weakest boundary: Classes ↔ Students relationships + undocumented storage decision
- Workflow effectiveness: grill-with-docs successfully clarified the storage strategy

## Root Cause

Documentation drift—migration decision was documented in ADRs but not visible in code comments or UI labels. Facade naming (`alpha-store`) made actual storage implementation appear unclear.

## Resolutions Applied

- Added inline comments explaining Supabase-backed storage in `classes/page.tsx` and `classes/[classId]/page.tsx`
- Removed stale "Storage alpha: `.data/saas/alpha-db.json`" UI labels
- Created reference to ADR-2026-02-21-persistence-before-new-ui.md for context

## Next Steps

- Consider renaming `alpha-store.ts` to `saas-store.ts` to reduce confusion
- Audit other systems for similar documentation drift patterns
- Validate whether "hidden knowledge" is as common as "missing knowledge" across systems

## Related Runs

- 2026-05-17-01-metamorfose-finance (comparable analysis on more complex system)
