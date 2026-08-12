schema_version: 1
probe_tool: sensemaking-skills probe-repo v1
generated_at: "2026-08-09T12:00:00Z"
repo_root: .
git_state:
  is_git_repo: true
  branch: main
  head_sha: abc1234
  head_message: initial
  tracked_file_count: 10
  untracked_file_count: 5
  ignored_present_entry_count: 2
  dirty_file_count: 1
verification_gap:
  declared_checks: [scripts/check.py]
  enforced_checks: [scripts/check.py]
  declared_in_ci: [scripts/check.py]
  vg: 0.0
  notes: ""
context_entropy:
  tracked_volume: 10
  untracked_volume: 5
  ignored_present_volume: 2
  ce: 0.7
  notes: "untracked+ignored (7) / tracked (10)"
test_collection:
  test_file_count: 3
  pytest_config_present: true
  markers_declared: ""
fixtures_coverage:
  total_validators: 2
  covered_validators: 2
  missing_fixtures: []
  coverage: 1.0
churn:
  commits_scanned: 50
  changed_files_last_n: 40
  top_changed_files: [identity.py, validate-identity.py]
relationships:
  doc_surface:
    total: 12
    live: 4
    by_class: {candidate: 0, example: 2, fixture: 1, generated: 1, historical: 4, live: 4, vendor: 0}
  version:
    declarations: 1
    subpackage_declarations: 0
    claims: 3
    distinct_values: ["0.2.1", "0.2.2"]
    findings:
      - concept: product_version
        finding_type: conflicting_values
        observations:
          - source: pyproject.toml
            location: pyproject.toml:7
            value: "0.2.2"
            evidence: version = "0.2.2"
            source_kind: declaration
            claim_class: declared
          - source: README.md
            location: README.md:9
            value: "0.2.1"
            evidence: "Current release: 0.2.1"
            source_kind: documentation
            claim_class: current
            source_class: live
        confidence: high
        requires_semantic_review: true
        notes: "Values disagree mechanically across sources."
  adr:
    files: 1
    catalog:
      - id: "0001"
        file: docs/adr/0001-example.md
        title: "ADR 0001: Example"
        status: proposed
        raw_status: "Proposed"
    references: 1
    findings: []
