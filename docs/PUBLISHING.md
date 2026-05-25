# Publishing to PyPI

This document describes how to publish sensemaking-skills to PyPI.

## Current Status

- ✅ **0.2.1 is ready for PyPI** (CLI tested locally, all tests passing)
- ⏳ **0.2.1 should be tested in real projects** before production PyPI publication
- 🔜 **Distribution files created** and verified with twine

## Prerequisites

- PyPI account: https://pypi.org/
- Test PyPI account: https://test.pypi.org/ (optional, for safety)
- `twine` installed: `pip install twine`
- `build` installed: `pip install build`

## Current Status

Distributions have been built and verified:

```bash
$ python -m build
Successfully built sensemaking_skills-0.2.1.tar.gz and sensemaking_skills-0.2.1-py3-none-any.whl

$ python -m twine check dist/*
Checking dist/sensemaking_skills-0.2.1-py3-none-any.whl: PASSED
Checking dist/sensemaking_skills-0.2.1.tar.gz: PASSED
```

## Publication Process

### Step 1: Verify Build (Already Done)

```bash
python -m build
python -m twine check dist/*
```

Expected: Both distributions pass metadata checks.

### Step 2: Publish to Test PyPI (Recommended Safety Check)

```bash
python -m twine upload --repository testpypi dist/* --verbose
```

Then test installation:
```bash
pip install -i https://test.pypi.org/simple/ sensemaking-skills==0.2.1
sensemaking-skills --version
# or
python -m sensemaking_skills.cli --version
```

### Step 3: Publish to Production PyPI

```bash
python -m twine upload dist/* --verbose
```

### Step 4: Verify Production Publication

```bash
# Wait 1-2 minutes for PyPI to index
pip install sensemaking-skills==0.2.1
sensemaking-skills --version
```

## Environment Setup for Publishing

Set up PyPI API token (one-time):

```bash
# Create ~/.pypirc file
cat > ~/.pypirc << 'PYPIRC'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi_YOUR_API_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi_YOUR_TEST_TOKEN_HERE
PYPIRC
```

Or use environment variable:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi_YOUR_API_TOKEN_HERE
python -m twine upload dist/*
```

## Release Checklist

Before publishing:

- [ ] All tests pass: `pytest tests/ -v`
- [ ] CLI works: `python -m sensemaking_skills.cli --help`
- [ ] README.md updated with new version info
- [ ] CHANGELOG.md updated with release notes
- [ ] Version bumped in setup.py and pyproject.toml
- [ ] Git commits made and pushed
- [ ] Distribution builds successfully: `python -m build`
- [ ] Distribution checks pass: `python -m twine check dist/*`
- [ ] Optional: Tested on Test PyPI first

## Future Automation

Once stable, use GitHub Actions to automate PyPI publication:

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      
      - name: Install build tools
        run: pip install build twine
      
      - name: Build distribution
        run: python -m build
      
      - name: Check distribution
        run: python -m twine check dist/*
      
      - name: Publish to PyPI
        run: python -m twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

## Important Notes

- **Evidence discipline:** Don't publish until CLI is tested in real projects
- **Semantic versioning:** Current version is 0.2.1 (beta)
- **First stable:** Version 1.0.0 should come after real-world CLI testing and user feedback
- **Security:** Never commit PyPI credentials to git; use GitHub Actions secrets or environment variables
- **Backup tokens:** Keep API tokens safe and rotate them periodically

## Rollback Procedure

If an issue is discovered after publishing:

1. Publish a patched version (e.g., 0.2.2) with the fix
2. Mark previous version as broken (if needed)
3. Document the issue in CHANGELOG.md

Note: You cannot delete or unpublish versions from PyPI after a brief window, so careful testing before publication is essential.
