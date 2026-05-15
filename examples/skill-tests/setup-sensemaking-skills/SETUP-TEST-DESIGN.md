# Test Design — setup-sensemaking-skills (iso-setup-001)

## 1. Mode Identification
- **Skill Mode**: The skill is primarily **Interactive Bootstrap** (Rules 13, 19, 31).
- **Test Mode**: For `iso-setup-001`, the skill operates in **Dry-run Audit** mode to ensure non-destructive verification in a test environment.

## 2. Artifact Definition
- **Artifact Name**: `setup_plan.md`
- **Contract Type**: `setup_plan` (Draft Contract)
- **Rationale**: The previous use of `config_audit.md` was too diagnostic. `setup_plan` correctly reflects the "Draft Changes" stage of the skill (SKILL.md:18).
- **Required Sections**:
    - `## 1. Status Audit`: Current inventory of root and `docs/agents/` configuration.
    - `## 2. Missing Components`: Specific gaps found (e.g., missing AGENTS.md block).
    - `## 3. Proposed Edits`: The exact diffs/new content the skill intends to write.
    - `## 4. Interactive Trace`: The list of questions the skill would ask the user.

## 3. Validation Strategy
- **Validator**: **Manual / Checklist-based**.
- **Machine Validator Status**: No machine validator exists for `setup_plan` yet.
- **Strict Prohibition**: Do NOT validate `setup_plan.md` (or the legacy `config_audit.md`) using the `problem_frame` validator.

## 4. Write Boundaries
- **Allowed Files**:
    - `examples/skill-tests/setup-sensemaking-skills/setup_plan.md`
    - `examples/skill-tests/setup-sensemaking-skills/TEST-RUN-LOG.md`
- **Forbidden Files**:
    - **Core Logic**: `skills/`, `scripts/`, `registries/`
    - **Documentation**: `docs/`, `README.md`, `CONTEXT.md`
    - **Mocked Target Files**: `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `docs/agents/*.md` (Modification of these is forbidden during dry-run testing).

## 5. Pass/Fail Criteria

### Pass Criteria
- Produces a `setup_plan.md` that identifies the lack of sensemaking blocks in the root instruction files.
- Correctly lists all 4-5 managed artifacts (docs/agents/*) that are missing.
- Follows all path hygiene rules (no `file:///` links, relative paths only).
- Stays strictly within the test directory boundary.

### Fail Criteria
- **Class 2 (Wrong Routing)**: Framing the setup task as a "problem" using the `problem-framer` logic.
- **Class 5 (Boundary Violation)**: Attempting to actually bootstrap the root files without an interactive approval gate or during a dry-run.
- **Class 9 (Validator Mismatch)**: Attempting to bypass the lack of a validator by using `problem_frame` validation.
- **Path Hygiene**: Using absolute paths or `file:///` URIs.
