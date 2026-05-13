# Contributing to Sensemaking Skills

Thank you for your interest in contributing! To maintain the quality and focus of this repository, please follow these guidelines:

## Core Rule
Sensemaking skills sit **before** specialized tools. They are designed for uncertainty, not implementation.

## Guidelines
1. **New Skills**: Every new skill must have a `SKILL.md` with YAML frontmatter.
2. **Registry Entries**: Every new routing entry in `skill-registry.yaml` must include:
   - `use_when`
   - `do_not_use_when`
   - `expected_input`
   - `expected_output`
   - `example_prompt`
3. **V1 Validation**: All new skills or major workflows must include at least one fixture in the `examples/` directory that passes `scripts/validate-repo.py`.
4. **Template Compliance**: Examples must follow the exact template for their skill (e.g., 13 sections for `repo-sensemaker`, 10 sections for `workflow-orchestrator`).
5. **Evidence Requirement**: Diagnostic examples must cite specific file paths and line ranges.
6. **Negative Fixtures**: Changes to orchestration logic must include a negative fixture proving safe refusal or downgrade behavior.
7. **Boundary Rule**: Skills must not perform downstream building (PRDs, code, issues) unless explicitly requested.
8. **V1 Validation**: Do not add downstream execution skills until the core `repo-sensemaker` V1 is fully validated.

## Submission Process
1. Fork the repo.
2. Create a feature branch.
3. Submit a Pull Request with a clear description of the "Fog" you are helping to clear.
