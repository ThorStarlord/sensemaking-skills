# Frequently Asked Questions

## Installation & Setup

### Q: How do I install sensemaking-skills?
A: Two options:
```bash
# Option 1: From PyPI (recommended)
pip install sensemaking-skills

# Option 2: From source
git clone https://github.com/ThorStarlord/sensemaking-skills.git
cd sensemaking-skills
pip install -e .
```

### Q: What are the system requirements?
A: Python 3.11 or higher. That's it! Only dependency is click (installed automatically).

### Q: Does it work on Windows/Mac/Linux?
A: Yes! It works on all operating systems that support Python 3.11+.

## Usage

### Q: How do I diagnose my repository?
A: Three-step process:
1. Prepare: `sensemaking-skills analyze --repo /path/to/repo`
2. Diagnose: Open repo in Claude Code, read skills, ask agent to analyze
3. Validate: `sensemaking-skills validate --artifact artifacts/brief.md`

### Q: What are the 4 fog types?
A: Four types of repository confusion:
- **Product Fog**: Unclear feature boundaries, API design issues
- **UI Fog**: UI component organization, styling inconsistency
- **Docs Fog**: Missing documentation, outdated examples
- **Architecture Fog**: Service coupling, layer violations

### Q: How long does diagnosis take?
A: Typically < 10 minutes for most repositories. Agent-driven, so it depends on your repository size and complexity.

### Q: Can I use this without Claude Code?
A: The CLI utilities (`analyze`, `validate`) work standalone. But the diagnosis itself requires Claude Code or another agent that can read skills and execute workflows.

### Q: Do I need to share my code?
A: No! Everything runs locally. Your repository never leaves your machine.

## Troubleshooting

### Q: "sensemaking-skills command not found"
A: Try: `python -m sensemaking_skills.cli --version`
Or reinstall: `pip install --upgrade sensemaking-skills`

### Q: Validate command fails with error
A: Check the error message for what's missing. Common issues:
- Brief not in expected location
- Brief missing required sections
- Artifact path incorrect

Review PHASE-3-TESTING-RESULTS.md for validation details.

### Q: Agent won't read the skills
A: Make sure:
- Repository is open in Claude Code
- Path to skills is correct
- SKILL.md file exists at that location

## Features

### Q: Can I export the brief in JSON?
A: Currently outputs Markdown. JSON export planned for 0.3.0.

### Q: Can I compare two diagnoses?
A: Not yet, but tracking feature for 0.3.0.

### Q: Can I run diagnostics on multiple repos at once?
A: Not yet. Planned for 0.3.0.

## Contributing

### Q: How can I help?
A: See CONTRIBUTING.md! We welcome:
- Bug reports
- Feature requests
- Documentation improvements
- Code contributions

### Q: Is there a code of conduct?
A: Yes! See CODE_OF_CONDUCT.md. Be respectful and inclusive.

### Q: Can I propose a new fog type?
A: Yes! Open an issue. We're considering custom fog types for 0.3.0.

## Project

### Q: What's the roadmap?
A: 
- 0.2.1: Current release (PyPI available)
- 0.3.0: User-requested features (JSON export, caching, etc.)
- 1.0.0: Stable API, comprehensive docs

### Q: Is this production-ready?
A: Yes! Phase 3 testing proved it works (11/11 tests PASS).

### Q: How is this licensed?
A: MIT License. See LICENSE file.

### Q: Who maintains this?
A: Core team with community contributions.

## Still Have Questions?

- Check the README.md
- Open a GitHub discussion
- Report a bug with details
- Read GETTING_STARTED.md for workflow examples
