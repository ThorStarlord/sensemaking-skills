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
3. **Examples**: Every new example must follow the 12-section **Sensemaking Brief** template and include an **Expected Behavior Checklist**.
4. **Boundary Rule**: Skills must not perform downstream building (PRDs, code, issues) unless explicitly requested.
5. **V1 Validation**: Do not add downstream execution skills until the core `repo-sensemaker` V1 is fully validated.

## Submission Process
1. Fork the repo.
2. Create a feature branch.
3. Submit a Pull Request with a clear description of the "Fog" you are helping to clear.
