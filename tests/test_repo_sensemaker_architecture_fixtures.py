"""Commit 2 - architecture reconstruction regressions.

Executable architecture fixtures: a deterministic static import tracer plus
per-fixture assertions that the runtime model, dependency semantics, state
model and boundary model claimed in the corpus ground truth actually hold for
the fixture files. Also verifies the skill documents the architecture
reconstruction requirements.

Covers the eight fixtures named in the plan: backend-service, full-stack,
monorepo, multi-executable, plugin-architecture, hidden-coupling,
generated-heavy, adv-unused-dep.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS = REPO_ROOT / "experiments" / "repository-sensemaking-skill-hardening-v1" / "corpus"
SKILL = REPO_ROOT / "skills" / "repo-sensemaker" / "SKILL.md"
TEMPLATE = REPO_ROOT / "skills" / "repo-sensemaker" / "references" / "repo-analysis-template.md"

PY_IMPORT_RE = re.compile(r"^\s*(?:from\s+([\w.]*\.?[\w.]*)\s+import\s+([\w.*]+)|import\s+([\w.]+))", re.M)
JS_IMPORT_RE = re.compile(r"import\s+(?:[^'\"\n]+\s+from\s+)?['\"]([^'\"]+)['\"]", re.M)


def _candidate_modules(base: Path, root: Path, mod: str, name: str) -> list[Path]:
    """Resolve 'from <mod> import <name>' / 'import <mod>' to local files.

    Relative imports (leading dots) resolve against the importing file's
    directory chain; absolute imports also resolve against the repo root.
    """
    parts = mod.lstrip(".")
    depth = len(mod) - len(parts)
    b = base
    for _ in range(max(0, depth - 1)):
        b = b.parent
    cands: list[Path] = []
    if parts:
        first, *rest = parts.split(".")
        bases = {b, root} if depth == 0 else {b}
        for base_dir in bases:
            cands.append(base_dir / f"{first}.py")
            cands.append(base_dir / first / "__init__.py")
            if rest:
                sub = base_dir / first
                for r in rest:
                    sub = sub / r
                cands.append(sub.with_suffix(".py"))
                cands.append(sub / "__init__.py")
                if name and name != "*":
                    cands.append(sub / f"{name}.py")
            elif name and name != "*":
                cands.append(base_dir / first / f"{name}.py")
    elif name and name != "*":
        cands.append(b / f"{name}.py")
    return cands


def python_imports(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    found = set()
    for m in PY_IMPORT_RE.finditer(text):
        mod = m.group(1) or m.group(3)
        name = m.group(2) or ""
        found.add(f"{mod}::{name}")
    return found


def reachable_python(root: Path, entry_rel: str) -> set[str]:
    """Depth-first static import trace from an entry module.

    Returns module-relative paths (forward slashes) reachable via imports.
    Modules loaded dynamically (exec, importlib, entry points by name) are
    NOT reachable - that asymmetry is exactly what the tests assert.
    """
    root = root.resolve()
    visited: set[Path] = set()
    stack = [root / entry_rel]
    while stack:
        cur = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        for imp in python_imports(cur):
            mod, name = imp.split("::", 1)
            for cand in _candidate_modules(cur.parent, root, mod, name):
                cand = cand.resolve()
                if cand.exists() and cand.is_relative_to(root):
                    stack.append(cand)
    return {p.relative_to(root).as_posix() for p in visited}


def js_imports(root: Path, entry_rel: str) -> set[str]:
    text = (root / entry_rel).read_text(encoding="utf-8", errors="replace")
    found = set()
    for m in JS_IMPORT_RE.finditer(text):
        target = m.group(1)
        if target.startswith("."):
            resolved = (root / entry_rel).parent / target
            found.add(resolved.resolve().relative_to(root.resolve()).as_posix())
    return found


class TestSkillArchitectureContent(unittest.TestCase):
    def test_runtime_model_elements_documented(self):
        text = SKILL.read_text(encoding="utf-8")
        for marker in ("startup path", "orchestration", "domain/core logic",
                       "persistence/state", "integration points", "background work",
                       "output boundary"):
            self.assertIn(marker, text)

    def test_dependency_semantics_documented(self):
        text = SKILL.read_text(encoding="utf-8")
        for cls in ("declared", "used", "runtime", "test", "optional", "dead"):
            self.assertIn(f"`{cls}`", text)
        self.assertIn("import exists ≠ runtime execution path proven", text)
        self.assertIn("dependency appears in manifest ≠ dependency is actively used", text)

    def test_state_and_boundary_models_documented(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("State model", text)
        self.assertIn("Boundary model", text)
        for transition in ("HTTP → application", "CLI → command handler",
                           "handler → domain", "domain → persistence",
                           "worker → queue", "plugin host → plugin"):
            self.assertIn(transition, text)

    def test_template_requires_flow_not_inventory(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("runtime flow, not just the inventory", text)


class TestArchitectureFixtures(unittest.TestCase):
    def test_backend_service_runtime_model(self):
        """Entry -> router -> models/db; sqlite is the state boundary."""
        root = CORPUS / "backend-service"
        reach = reachable_python(root, "app/main.py")
        self.assertIn("app/main.py", reach)
        self.assertIn("app/routers/notes.py", reach)
        self.assertIn("app/models.py", reach)
        self.assertIn("app/db.py", reach)
        # state boundary: db.py opens sqlite3 (external) - asserted by content
        db_text = (root / "app/db.py").read_text(encoding="utf-8")
        self.assertIn("sqlite3", db_text)
        # runtime path provable: main.py builds the app and serves via uvicorn
        main_text = (root / "app/main.py").read_text(encoding="utf-8")
        self.assertIn("app = create_app()", main_text)

    def test_full_stack_two_runtime_sides(self):
        """Frontend api.js and backend main.py disagree on the API path;
        backend db.py is unwired (never imported) - an orphaned module."""
        root = CORPUS / "full-stack"
        reach = reachable_python(root, "backend/app/main.py")
        self.assertIn("backend/app/main.py", reach)
        self.assertNotIn("backend/app/db.py", reach, "db.py is never imported - orphaned module")
        js = js_imports(root, "frontend/src/App.jsx")
        self.assertEqual(js, set(), "App.jsx is a stub - it imports nothing")
        self.assertTrue((root / "frontend/src/api.js").exists())
        api = (root / "frontend/src/api.js").read_text(encoding="utf-8")
        backend = (root / "backend/app/main.py").read_text(encoding="utf-8")
        self.assertIn("/api/v1/items", api)
        self.assertNotIn("/api/v1/items", backend)
        self.assertIn('"/items"', backend)

    def test_monorepo_undeclared_workspace_dependency(self):
        """strkit imports mathkit but does not declare it (declared vs used)."""
        root = CORPUS / "monorepo"
        reach = reachable_python(root, "packages/strkit/src/index.js")
        # JS reachability via the shared tracer
        self.assertIn("packages/strkit/src/index.js", reach)
        strkit_pkg = (root / "packages/strkit/package.json").read_text(encoding="utf-8")
        self.assertNotIn("mathkit", strkit_pkg)
        strkit_src = (root / "packages/strkit/src/index.js").read_text(encoding="utf-8")
        self.assertIn("mathkit", strkit_src)

    def test_multi_executable_shared_state_module(self):
        """main.py and worker.py both reach the same db.py state boundary."""
        root = CORPUS / "multi-executable"
        reach_main = reachable_python(root, "main.py")
        reach_worker = reachable_python(root, "worker.py")
        self.assertIn("db.py", reach_main)
        self.assertIn("db.py", reach_worker)
        self.assertIn("cli.py", reachable_python(root, "cli.py"))

    def test_plugin_architecture_exec_load_is_not_import(self):
        """plugins are loaded by exec() - import trace must NOT reach them."""
        root = CORPUS / "plugin-architecture"
        reach = reachable_python(root, "core/main.py")
        self.assertIn("core/main.py", reach)
        self.assertIn("core/registry.py", reach)
        self.assertNotIn("plugins/alpha.py", reach, "exec-loaded plugin should not appear in an import trace")
        self.assertNotIn("plugins/beta.py", reach)
        registry = (root / "core/registry.py").read_text(encoding="utf-8")
        self.assertIn("exec", registry)

    def test_hidden_coupling_global_state(self):
        """a.py and b.py both reach registry.py (shared global state)."""
        root = CORPUS / "hidden-coupling"
        reach = reachable_python(root, "main.py")
        self.assertIn("a.py", reach)
        self.assertIn("b.py", reach)
        self.assertIn("registry.py", reach)
        b_text = (root / "b.py").read_text(encoding="utf-8")
        a_text = (root / "a.py").read_text(encoding="utf-8")
        self.assertIn("STATE", b_text)
        self.assertIn("STATE", a_text)

    def test_generated_heavy_generated_marker_in_runtime_path(self):
        """handwritten code imports generated modules marked DO NOT EDIT."""
        root = CORPUS / "generated-heavy"
        reach = reachable_python(root, "handwritten/main.py")
        self.assertIn("generated/api_pb2.py", reach)
        pb = (root / "generated/api_pb2.py").read_text(encoding="utf-8")
        self.assertIn("DO NOT EDIT", pb)

    def test_adv_unused_dep_declared_but_dead(self):
        """tensorflow is declared in requirements.txt but never imported."""
        root = CORPUS / "adv-unused-dep"
        reach = reachable_python(root, "app.py")
        reqs = (root / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("tensorflow", reqs)
        self.assertNotIn("tensorflow", " ".join(reach), "declared dep must not be in the import trace")
        app_text = (root / "app.py").read_text(encoding="utf-8")
        self.assertIn("requests", app_text)


if __name__ == "__main__":
    unittest.main()
