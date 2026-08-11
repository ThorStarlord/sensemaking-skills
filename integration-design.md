# Integration design: cross-artifact relationship probes in the Probe Engine

- **Date**: 2026-08-12
- **Branch**: `feat/probe-engine-relationship-integration` (worktree
  `.claude/worktrees/probe-engine-integration`), based on `main` @ `90780f5`.
  The spike branch (`feat/spike-semantic-drift`) is evidence/reference only.

## Existing responsibility boundaries (inspected)

| Component | Responsibility |
|---|---|
| `scripts/repo_probes.py` | Pure probe functions (git/fs reads only; no network, no writes; YAML-safe dicts). `probe_all()` assembles the flat report dict (10 keys). |
| `scripts/probe-repo.py` | Thin CLI: `--repo-root/--output/--no-write/--churn-commits`, writes `probe-report.yaml`, prints 6-line ASCII summary, exit 0/2. |
| `scripts/validate-probe-report.py` | Schema contract: `REQUIRED_KEYS` (missing => fail), vg/ce range checks. Unknown top-level keys are ALLOWED (additive). Exit 1 on invalid. |
| `tests/fixtures/validate-probe-report/{valid,invalid}` | Valid exemplar + negative fixtures; consumed generically by `scripts/test-validators.py`. |
| `skills/repo-sensemaker/SKILL.md` "Probe Engine" | Mandatory pre-synthesis step: run probe, read report, surface numbers, cite `probe-report.yaml:<field>` in Section 8. |
| Prompt injection | `repo_probes.append_probe_section()` embeds the whole report into executor prompts. |

## Proposed integration point

A new canonical module `scripts/probe_relationships.py` (pure functions,
same conventions as `repo_probes.py`: no network, no writes, plain
YAML-safe dicts) exporting one entry point:

    relationships(repo_root) -> dict
        ├── doc_surface: {total, live, by_class}
        ├── version:     {declarations, claims, distinct_values, findings[]}
        └── adr:         {files, catalog[], references, findings[]}

`repo_probes.probe_all()` gains one additive top-level key:
`"relationships": relationships(repo_root)`. Everything else in the
engine (CLI flags, exit codes, summary, prompt injection, REQUIRED_KEYS)
is unchanged; the summary gains one line.

The report section shape mirrors the spike's evidence-candidate contract
(concept / finding_type / observations with source+location+value+
evidence / confidence / requires_semantic_review / notes), so
repo-sensemaker consumes relationship findings exactly like other probe
evidence: measured candidates requiring semantic review, never diagnoses.

## Alternatives considered

1. **Extend `repo_probes.py` directly** — rejected: it is a single
   ~400-line module of git/fs metric probes; relationship probes are a
   distinct family with their own classifier (~250 lines). A sibling
   module preserves the existing boundary (one probe family per module).
2. **Separate CLI `probe-relationships.py`** — rejected: that is not
   integration into the engine; repo-sensemaker runs ONE probe command
   and reads ONE `probe-report.yaml`. Findings must land in the report.
3. **Import the spike script** — rejected: canonical code must not depend
   on a file living on another (evidence-only) branch. Logic is distilled
   and rewritten, not copied.
4. **Graph/node/edge abstraction** — rejected: findings are plain lists
   with provenance; no consumer needs graph traversal (see the spike's
   experiment-1 verdict).

## Why this is the smallest coherent shape

It changes exactly one contract surface (an additive report key), one new
module, one validator extension (optional shape check + fixtures), and a
few consumption lines in SKILL.md. Every existing contract — CLI, exit
codes, required keys, summary format, prompt injection, validator
compatibilty with older reports (unknown keys allowed) — is preserved.
The probe never emits diagnoses: `requires_semantic_review` and
`confidence` flags carry the "candidate, not conclusion" semantics.

## Semantics carried over from the spike (conceptually, not literally)

- **Doc-surface discovery**: bounded os.walk (prunes hidden + generic
  dirs); ordered path-signal classifier (historical / vendor / fixture /
  example / generated / candidate / live); only live docs are claim
  sources; non-live classes counted (`doc_surface.by_class`).
- **Version**: declared versions (pyproject.toml / setup.py /
  package.json + top-level `src/<project-name>/__init__.py` `__version__`
  with sub-package role classification); live-doc + test-layer claims with
  current/historical/unknown classification; semver family filter;
  conflicting-values finding only when the decision set has >1 value.
- **ADR**: catalog (2-4 digit ids, `**Status**:` / `**Status:**` /
  `## Status` block forms, duplicates kept per-entry); references across
  live docs + `skills/**` + `docs/adr/*.md` + workflows + config
  (path-deduped, per-line dedupe, self-ref skip, per-reference status
  window); missing_reference / status_claim_mismatch (per-entry) /
  missing_status_line / unrecognized_status findings.
- **NOT carried over**: network-capability detector (NOT READY per
  experiment 2/3), capability-claim drift, the CLI summary's
  probe-specific wording, and all repo-specific scan lists.

## Contract change note

`probe-report.yaml` gains the `relationships` key. The validator treats
it as optional-but-validated-when-present (older reports and reports from
repos with no relationship findings still validate; the engine always
emits the section, possibly with empty findings). No new ADR is filed:
this is an additive contract extension within the existing schema's
tolerance (unknown keys allowed), not a new governance decision.
