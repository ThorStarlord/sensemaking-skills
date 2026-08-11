---
validator_case: negative
expected_error_contains: PROBE_REPORT_RELATIONSHIPS_SHAPE
---
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
  test_file_count: 2
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
relationships: "this is not a mapping"
