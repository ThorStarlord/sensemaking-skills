# Proposed Task: Fix Cross-Drive Windows Paths in workflow-runtime.py

## Summary
Two locations in `scripts/workflow-runtime.py` where `os.path.relpath()` can fail when paths are on different Windows drives (e.g., C: vs H:) need fallback handling with focused testing.

## Affected Locations

### Location 1: diagnostic_path output (line ~2155)
**Current behavior**: `os.path.relpath(diagnostic_path, self.repo_root)` raises ValueError if paths are on different drives.

**Current line**:
```python
print(f"  [OK] Diagnostic report: {os.path.relpath(diagnostic_path, self.repo_root)}")
```

**Expected behavior (same drive)**: Returns relative path like `plan_123/diagnostic.md`

**Expected behavior (cross-drive)**: Falls back to absolute path like `C:\temp\session\diagnostic.md`

### Location 2: session reuse message (line ~2889)
**Current behavior**: `os.path.relpath(from_session_path, repo_root)` raises ValueError if paths are on different drives.

**Current line**:
```python
print(f"[OK] Reusing session: {os.path.relpath(from_session_path, repo_root)}")
```

**Expected behavior (same drive)**: Returns relative path like `..\..\temp\session` or absolute if parent traversal needed

**Expected behavior (cross-drive)**: Falls back to absolute path like `C:\temp\session`

## Proposed Solution
Wrap both calls in try-except ValueError with absolute-path fallback:

```python
try:
    rel_path = os.path.relpath(path, base)
except ValueError:
    # Cross-drive: Windows can't create relative paths across drives
    rel_path = os.path.abspath(path)
print(f"Message: {rel_path}")
```

## Required Tests

### Test 1: Same Drive Relative Path (Windows)
- Verify `os.path.relpath()` succeeds without exception
- Verify output is a valid relative path (contains `..` or relative segments)
- Verify message is printed correctly

### Test 2: Cross-Drive Absolute Fallback (Windows)
- Create paths on different drives (C:, H:, etc.)
- Verify ValueError is caught
- Verify fallback uses `os.path.abspath()` 
- Verify output is absolute path starting with drive letter
- Verify message is printed correctly

### Test 3: Downstream Acceptance (All Platforms)
- Verify run.log contains both messages
- Verify absolute paths in run.log are correctly formatted
- Verify subsequent steps parse and use the paths without error
- Verify Linux/macOS behavior is unchanged (no try-except hit, normal relative paths)

## Acceptance Criteria
- [ ] Both locations have try-except ValueError with absolute fallback
- [ ] Same-drive test passes on Windows
- [ ] Cross-drive test passes on Windows
- [ ] Run log contains correct paths in both cases
- [ ] Linux/macOS unaffected (tests pass normally)
- [ ] No other relpath calls in workflow-runtime.py need updating

## Dependencies
This fix should be applied after:
- Preflight validation defect is resolved
- Architectural-review acceptance test passes

This ensures the acceptance test can run on systems with temp directories on different drives than the repo.
