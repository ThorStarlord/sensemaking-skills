"""Phase 4 - build and freeze the repository-sensemaking evaluation corpus.

Creates 25 small fixture git repositories (17 repository classes + 8
adversarial fixtures), commits each with a deterministic author/date so
commit SHAs are stable, and writes ground-truth YAML with expected
subsystems, entry points, weak boundaries, misleading signals and fog
candidates. Ground truth is frozen BEFORE any candidate outputs exist.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import yaml

WORK = Path(r"H:\GithubRepositories\sensemaking-skills\experiments\repository-sensemaking-skill-hardening-v1")
CORPUS = WORK / "corpus"

GIT_DATE = "2026-08-01T12:00:00Z"


def git(repo: Path, *args: str) -> None:
    env = dict(os.environ, GIT_AUTHOR_DATE=GIT_DATE, GIT_COMMITTER_DATE=GIT_DATE,
               GIT_AUTHOR_NAME="corpus-builder", GIT_AUTHOR_EMAIL="corpus@local",
               GIT_COMMITTER_NAME="corpus-builder", GIT_COMMITTER_EMAIL="corpus@local")
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, env=env)


def make_repo(repo_id: str, files: dict[str, str]) -> Path:
    r = CORPUS / repo_id
    r.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        p = r / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    git(r, "init", "-b", "main")
    git(r, "add", "-A")
    git(r, "commit", "-m", f"fixture {repo_id}")
    return r


FIXTURES: dict[str, dict] = {
    "tiny-lib": {
        "purpose": "A tiny Python library that greets users with configurable salutations.",
        "subsystems": ["greeter core", "config loading"],
        "entry_points": ["greeter/greet.py:greet()"],
        "weak_boundaries": [{"type": "Zero Validation", "evidence": ["greeter/greet.py"], "note": "no input validation on name"}],
        "misleading_signals": [],
        "fog": ["product_fog"],
        "files": {
            "README.md": "# tiny-lib\n\nA tiny library that greets users.\n\nUsage: `from greeter import greet; greet(\"Ada\")`\n",
            "pyproject.toml": "[project]\nname = \"tiny-lib\"\nversion = \"0.1.0\"\n",
            "greeter/__init__.py": "from .greet import greet\n",
            "greeter/greet.py": "def greet(name: str) -> str:\n    return f\"Hello, {name}!\"\n",
            "tests/test_greet.py": "from greeter import greet\n\ndef test_greet():\n    assert greet(\"Ada\") == \"Hello, Ada!\"\n",
        },
    },
    "cli-app": {
        "purpose": "A command-line task manager with add/list/done subcommands.",
        "subsystems": ["CLI parsing", "task store"],
        "entry_points": ["main.py:main()"],
        "weak_boundaries": [{"type": "Contract Mismatch", "evidence": ["main.py", "README.md"], "note": "README documents `tasks delete` but the CLI only implements add/list/done"}],
        "misleading_signals": ["README mentions a delete subcommand that does not exist"],
        "fog": ["product_fog"],
        "files": {
            "README.md": "# tasks-cli\n\nManage tasks from the terminal.\n\nCommands: `tasks add <title>`, `tasks list`, `tasks done <id>`, `tasks delete <id>`.\n",
            "main.py": "import argparse\nimport json\nfrom pathlib import Path\n\nSTORE = Path(\"tasks.json\")\n\ndef load():\n    if not STORE.exists():\n        return []\n    return json.loads(STORE.read_text())\n\ndef add(title: str):\n    tasks = load()\n    tasks.append({\"id\": len(tasks) + 1, \"title\": title, \"done\": False})\n    STORE.write_text(json.dumps(tasks))\n\ndef main():\n    p = argparse.ArgumentParser(prog=\"tasks\")\n    sub = p.add_subparsers(dest=\"cmd\")\n    add_p = sub.add_parser(\"add\"); add_p.add_argument(\"title\")\n    sub.add_parser(\"list\")\n    done_p = sub.add_parser(\"done\"); done_p.add_argument(\"id\", type=int)\n    args = p.parse_args()\n    if args.cmd == \"add\":\n        add(args.title)\n    elif args.cmd == \"list\":\n        for t in load():\n            print(t)\n    elif args.cmd == \"done\":\n        print(\"not implemented\")\n\nif __name__ == \"__main__\":\n    main()\n",
        },
    },
    "web-frontend": {
        "purpose": "A single-page dashboard frontend with hand-rolled routing and fetch-based data loading.",
        "subsystems": ["components", "router", "api client"],
        "entry_points": ["src/index.html", "src/app.js"],
        "weak_boundaries": [{"type": "Implicit Dependencies", "evidence": ["src/app.js", "src/api.js"], "note": "api client assumes a backend base URL with no configuration boundary"}],
        "misleading_signals": [],
        "fog": ["ui_fog"],
        "files": {
            "package.json": "{\"name\": \"dashboard-ui\", \"scripts\": {\"start\": \"python -m http.server 8000\"}}\n",
            "src/index.html": "<!doctype html>\n<html><head><title>Dashboard</title></head>\n<body><div id=\"app\"></div><script src=\"app.js\"></script></body></html>\n",
            "src/app.js": "import { renderDashboard } from './components/dashboard.js';\nimport { router } from './router.js';\nrouter.register('/dashboard', renderDashboard);\nrouter.start();\n",
            "src/router.js": "const routes = {};\nexport const router = {\n  register(path, handler) { routes[path] = handler; },\n  start() { window.addEventListener('hashchange', () => this.dispatch()); this.dispatch(); },\n  dispatch() { const h = routes[window.location.hash.slice(1)]; if (h) h(); },\n};\n",
            "src/api.js": "export async function loadData() {\n  return fetch('/api/data').then(r => r.json());\n}\n",
            "src/components/dashboard.js": "import { loadData } from '../api.js';\nexport function renderDashboard() {\n  loadData().then(data => { document.getElementById('app').innerHTML = '<pre>' + JSON.stringify(data) + '</pre>'; });\n}\n",
            "src/components/widget.js": "export function widget(title, body) { return `<div class=\"widget\"><h2>${title}</h2>${body}</div>`; }\n",
        },
    },
    "backend-service": {
        "purpose": "A FastAPI-style REST service managing notes with SQLite persistence.",
        "subsystems": ["HTTP layer", "service logic", "persistence"],
        "entry_points": ["app/main.py:create_app()"],
        "weak_boundaries": [{"type": "Zero Validation", "evidence": ["app/models.py"], "note": "note bodies are stored without size limits or schema validation"}],
        "misleading_signals": [],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# notes-service\n\nREST API for notes. `uvicorn app.main:app`.\n",
            "requirements.txt": "fastapi\nuvicorn\n",
            "app/__init__.py": "",
            "app/main.py": "from fastapi import FastAPI\nfrom .routers import notes\n\ndef create_app():\n    app = FastAPI()\n    app.include_router(notes.router)\n    return app\n\napp = create_app()\n",
            "app/routers/notes.py": "from fastapi import APIRouter, HTTPException\nfrom ..models import Note\nfrom ..db import get_db\n\nrouter = APIRouter(prefix=\"/notes\")\n\n@router.post(\"/\")\ndef create(note: Note):\n    db = get_db()\n    cur = db.execute(\"INSERT INTO notes (body) VALUES (?)\", (note.body,))\n    db.commit()\n    return {\"id\": cur.lastrowid}\n\n@router.get(\"/{note_id}\")\ndef read(note_id: int):\n    db = get_db()\n    row = db.execute(\"SELECT body FROM notes WHERE id = ?\", (note_id,)).fetchone()\n    if row is None:\n        raise HTTPException(404)\n    return {\"body\": row[0]}\n",
            "app/models.py": "from pydantic import BaseModel\n\nclass Note(BaseModel):\n    body: str\n",
            "app/db.py": "import sqlite3\nfrom pathlib import Path\n\ndef get_db():\n    conn = sqlite3.connect(Path(\"notes.db\"))\n    conn.execute(\"CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, body TEXT)\")\n    return conn\n",
        },
    },
    "full-stack": {
        "purpose": "A full-stack app: React frontend, Python backend, SQLite database, docker-compose.",
        "subsystems": ["frontend", "backend", "database", "deployment"],
        "entry_points": ["frontend/src/App.jsx", "backend/app/main.py"],
        "weak_boundaries": [{"type": "Contract Mismatch", "evidence": ["frontend/src/api.js", "backend/app/main.py"], "note": "frontend expects /api/v1/items, backend serves /items"}],
        "misleading_signals": [],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# fullstack-app\n\nA full-stack application.\n\n`docker compose up`.\n",
            "docker-compose.yml": "services:\n  backend:\n    build: ./backend\n  frontend:\n    build: ./frontend\n",
            "frontend/package.json": "{\"name\": \"frontend\"}\n",
            "frontend/src/App.jsx": "export default function App() { return <div>app</div>; }\n",
            "frontend/src/api.js": "export const API = '/api/v1/items';\n",
            "backend/requirements.txt": "fastapi\n",
            "backend/app/main.py": "from fastapi import FastAPI\napp = FastAPI()\n\n@app.get(\"/items\")\ndef items():\n    return []\n",
            "backend/app/db.py": "import sqlite3\n\ndef conn():\n    return sqlite3.connect(\"app.db\")\n",
        },
    },
    "monorepo": {
        "purpose": "A monorepo with two independent packages (mathkit, strkit) managed by pnpm workspaces.",
        "subsystems": ["mathkit package", "strkit package", "workspace tooling"],
        "entry_points": ["packages/mathkit/src/index.js", "packages/strkit/src/index.js"],
        "weak_boundaries": [{"type": "Implicit Dependencies", "evidence": ["packages/strkit/src/index.js"], "note": "strkit imports mathkit without declaring it as a dependency"}],
        "misleading_signals": [],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# monorepo\n\nTwo packages.\n",
            "pnpm-workspace.yaml": "packages:\n  - packages/*\n",
            "packages/mathkit/package.json": "{\"name\": \"mathkit\", \"version\": \"1.0.0\", \"main\": \"src/index.js\"}\n",
            "packages/mathkit/src/index.js": "export const add = (a, b) => a + b;\n",
            "packages/strkit/package.json": "{\"name\": \"strkit\", \"version\": \"1.0.0\", \"main\": \"src/index.js\"}\n",
            "packages/strkit/src/index.js": "import { add } from 'mathkit';\nexport const concat = (a, b) => a + b + add(1, 1);\n",
        },
    },
    "multi-language": {
        "purpose": "A project mixing Python, JavaScript and shell: build pipeline with a Makefile.",
        "subsystems": ["python core", "js helper", "shell tooling"],
        "entry_points": ["core/main.py", "helper/run.js", "scripts/setup.sh"],
        "weak_boundaries": [{"type": "Ghost Features", "evidence": ["Makefile"], "note": "Makefile targets reference helper/run.js which is a stub"}],
        "misleading_signals": [],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# multi-lang\n\nMixed-language project.\n",
            "Makefile": "all: core\ncore:\n\tpython core/main.py\nhelper:\n\tnode helper/run.js\n",
            "core/main.py": "print('core')\n",
            "helper/run.js": "console.log('TODO');\n",
            "scripts/setup.sh": "#!/bin/sh\necho setup\n",
        },
    },
    "poorly-documented": {
        "purpose": "A data-processing library with no README and no docstrings.",
        "subsystems": ["processing", "io"],
        "entry_points": ["process.py:run()"],
        "weak_boundaries": [{"type": "Zero Validation", "evidence": ["process.py"], "note": "no input validation; undocumented contract"}],
        "misleading_signals": [],
        "fog": ["docs_fog"],
        "files": {
            "process.py": "def run(path):\n    with open(path) as f:\n        return [line.strip() for line in f]\n\ndef filter_empty(items):\n    return [i for i in items if i]\n",
            "io.py": "def save(data, path):\n    with open(path, 'w') as f:\n        f.writelines(data)\n",
        },
    },
    "docs-heavy-code-light": {
        "purpose": "A project with extensive documentation but almost no implementation.",
        "subsystems": ["docs", "stub implementation"],
        "entry_points": ["src/main.py"],
        "weak_boundaries": [{"type": "Ghost Features", "evidence": ["docs/spec.md", "src/main.py"], "note": "docs describe features the code does not implement"}],
        "misleading_signals": ["docs/architecture.md describes modules that do not exist"],
        "fog": ["product_fog"],
        "files": {
            "README.md": "# docs-heavy\n\nSee docs/.\n",
            "docs/spec.md": "# Spec\n\nFeatures: ingest, transform, export.\n",
            "docs/architecture.md": "# Architecture\n\nModules: ingestor.py, transformer.py, exporter.py.\n",
            "docs/roadmap.md": "# Roadmap\n\nQ3: real-time mode.\n",
            "src/main.py": "print('hello')\n",
        },
    },
    "generated-heavy": {
        "purpose": "A project where generated protobuf code and dist artifacts are committed alongside handwritten code.",
        "subsystems": ["generated protobuf layer", "handwritten core", "build output"],
        "entry_points": ["handwritten/main.py"],
        "weak_boundaries": [{"type": "Contract Mismatch", "evidence": ["generated/api_pb2.py", "handwritten/main.py"], "note": "handwritten code drifts from the generated message schema"}],
        "misleading_signals": ["generated/api_pb2.py and dist/*.py look like primary source but are build outputs"],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# generated-heavy\n\nProtobuf-based project.\n",
            "generated/api_pb2.py": "# Generated by the protocol buffer compiler. DO NOT EDIT!\nclass Message:\n    pass\n",
            "generated/api_pb2_grpc.py": "# Generated. DO NOT EDIT!\n",
            "handwritten/main.py": "from generated.api_pb2 import Message\n\nm = Message()\nprint(m)\n",
            "dist/app.py": "print('built artifact')\n",
            "dist/bundle.js": "console.log('minified');\n",
        },
    },
    "unusual-layout": {
        "purpose": "A service with a deep, unconventional directory layout.",
        "subsystems": ["core logic", "config", "adapters"],
        "entry_points": ["app/main.py"],
        "weak_boundaries": [{"type": "Vocabulary Drift", "evidence": ["app/src/lib/core/engine.py", "README.md"], "note": "docs call it 'engine', code calls it 'executor'"}],
        "misleading_signals": ["directory names do not match module contents"],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# unusual\n\nThe engine processes events.\n",
            "app/main.py": "from src.lib.core.engine import Engine\nEngine().run()\n",
            "app/src/lib/core/engine.py": "class Engine:\n    def run(self):\n        print('running')\n",
            "app/src/lib/io/reader.py": "def read(path):\n    return open(path).read()\n",
            "app/config/settings.py": "MODE = 'prod'\n",
            "app/config/extra/deep/nested.py": "VALUE = 1\n",
        },
    },
    "multi-executable": {
        "purpose": "A project with several executables: main server, CLI, worker and scripts.",
        "subsystems": ["server", "cli", "worker", "scripts"],
        "entry_points": ["main.py", "cli.py", "worker.py", "scripts/backfill.py"],
        "weak_boundaries": [{"type": "Implicit Dependencies", "evidence": ["worker.py", "db.py"], "note": "worker and server both mutate the same queue table without coordination"}],
        "misleading_signals": [],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# multi-exec\n\nServer: `python main.py`; CLI: `python cli.py`; worker: `python worker.py`.\n",
            "main.py": "from db import get_conn\n\ndef serve():\n    conn = get_conn()\n    print('serving', conn)\n\nif __name__ == '__main__':\n    serve()\n",
            "cli.py": "import argparse\np = argparse.ArgumentParser()\np.parse_args()\n",
            "worker.py": "from db import get_conn\n\ndef poll():\n    conn = get_conn()\n    print('polling')\n\nif __name__ == '__main__':\n    poll()\n",
            "db.py": "def get_conn():\n    return 'fake-conn'\n",
            "scripts/backfill.py": "print('backfill')\n",
        },
    },
    "plugin-architecture": {
        "purpose": "An application with a plugin registry and loadable plugins.",
        "subsystems": ["core", "plugin registry", "plugins"],
        "entry_points": ["core/main.py:main()"],
        "weak_boundaries": [{"type": "Safety Gaps", "evidence": ["core/registry.py"], "note": "plugins are loaded via exec() from arbitrary paths with no sandbox"}],
        "misleading_signals": [],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# plugins-app\n\nLoads plugins from plugins/.\n",
            "core/main.py": "from .registry import load_plugins\n\ndef main():\n    load_plugins('plugins')\n\nif __name__ == '__main__':\n    main()\n",
            "core/registry.py": "import os\n\ndef load_plugins(directory):\n    for name in os.listdir(directory):\n        if name.endswith('.py'):\n            exec(open(os.path.join(directory, name)).read())\n",
            "plugins/alpha.py": "print('alpha plugin loaded')\n",
            "plugins/beta.py": "print('beta plugin loaded')\n",
        },
    },
    "stale-readme": {
        "purpose": "A storage library whose README describes SQLite but the code uses JSON files.",
        "subsystems": ["storage", "api"],
        "entry_points": ["store.py:Store"],
        "weak_boundaries": [{"type": "Vocabulary Drift", "evidence": ["README.md", "store.py"], "note": "README says SQLite; code persists JSON files"}],
        "misleading_signals": ["README claims sqlite3 usage", "docs/design.md describes an old architecture"],
        "fog": ["docs_fog"],
        "files": {
            "README.md": "# store-lib\n\nUses SQLite for persistence. `pip install store-lib`.\n",
            "docs/design.md": "# Design\n\nOld design: SQLite tables `items`, `users`.\n",
            "store.py": "import json\nfrom pathlib import Path\n\nclass Store:\n    def __init__(self, path='store.json'):\n        self.path = Path(path)\n    def put(self, key, value):\n        data = json.loads(self.path.read_text()) if self.path.exists() else {}\n        data[key] = value\n        self.path.write_text(json.dumps(data))\n    def get(self, key):\n        data = json.loads(self.path.read_text())\n        return data.get(key)\n",
            "pyproject.toml": "[project]\nname = \"store-lib\"\n",
        },
    },
    "hidden-coupling": {
        "purpose": "Two nominally independent modules that share global state via a registry.",
        "subsystems": ["module A", "module B", "shared registry"],
        "entry_points": ["main.py"],
        "weak_boundaries": [{"type": "Implicit Dependencies", "evidence": ["a.py", "b.py", "registry.py"], "note": "b.py consumes state written by a.py through a global registry; README presents them as independent"}],
        "misleading_signals": ["README claims modules are independent"],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# hidden-coupling\n\nModules a and b are independent.\n",
            "registry.py": "STATE = {}\n",
            "a.py": "from registry import STATE\n\ndef init():\n    STATE['token'] = 'abc'\n",
            "b.py": "from registry import STATE\n\ndef use():\n    return STATE.get('token')\n",
            "main.py": "import a\nimport b\n\na.init()\nprint(b.use())\n",
        },
    },
    "strong-ui-fog": {
        "purpose": "A frontend with scattered components, complex undocumented routing, fragmented design tokens and no UI tests.",
        "subsystems": ["views", "widgets", "router", "styles"],
        "entry_points": ["src/index.js"],
        "weak_boundaries": [{"type": "Zero Validation", "evidence": ["src/router.js"], "note": "routing is complex and entirely undocumented"}],
        "misleading_signals": [],
        "fog": ["ui_fog"],
        "files": {
            "package.json": "{\"name\": \"foggy-ui\"}\n",
            "src/index.js": "import { mount } from './views/AppView.js';\nmount();\n",
            "src/views/AppView.js": "import { router } from '../router.js';\nexport function mount() { router.start(); }\n",
            "src/views/SettingsView.js": "export function settings() { return '<div>settings</div>'; }\n",
            "src/views/ProfileView.js": "export function profile() { return '<div>profile</div>'; }\n",
            "src/widgets/button.js": "export const button = (label) => `<button>${label}</button>`;\n",
            "src/widgets/modal.js": "export const modal = (title) => `<div class=\"modal\">${title}</div>`;\n",
            "src/ui/table.js": "export const table = (rows) => `<table>${rows}</table>`;\n",
            "src/ui/form.js": "export const form = (fields) => `<form>${fields}</form>`;\n",
            "src/router.js": "const routes = {};\nlet current = null;\nconst guards = [];\nexport const router = {\n  add(path, handler, guard) { routes[path] = { handler, guard }; },\n  start() { this.dispatch(); },\n  dispatch() {\n    const path = window.location.hash.slice(1);\n    const r = routes[path];\n    if (!r) return;\n    if (r.guard && !r.guard()) { current = 'blocked'; return; }\n    current = path;\n    r.handler();\n  },\n  get current() { return current; },\n};\n",
            "src/styles/colors.css": ":root { --brand: #3366ff; }\n",
            "src/styles/other.css": ".btn { color: #333366; }\n",
        },
    },
    "no-ui": {
        "purpose": "A pure backend library with no frontend surface at all.",
        "subsystems": ["core", "serialization"],
        "entry_points": ["core/engine.py"],
        "weak_boundaries": [{"type": "Zero Validation", "evidence": ["core/engine.py"], "note": "engine accepts malformed input silently"}],
        "misleading_signals": [],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# no-ui-lib\n\nBackend library.\n",
            "core/engine.py": "def process(payload):\n    return payload.upper()\n",
            "core/serialize.py": "import json\n\ndef dump(data):\n    return json.dumps(data)\n",
        },
    },
    "adv-misleading-readme": {
        "purpose": "A repository whose README advertises features that do not exist (ghost features).",
        "subsystems": ["actual core", "advertised surface"],
        "entry_points": ["src/app.py"],
        "weak_boundaries": [{"type": "Ghost Features", "evidence": ["README.md", "src/app.py"], "note": "README lists sync/export/webhook features; code only implements ingest"}],
        "misleading_signals": ["README feature list entirely aspirational"],
        "fog": ["product_fog"],
        "files": {
            "README.md": "# data-hub\n\nFeatures: ingest, sync, export, webhooks.\n\nQuick start: `python -m datahub sync --remote`.\n",
            "src/app.py": "def ingest(path):\n    return open(path).read()\n\nif __name__ == '__main__':\n    import sys\n    ingest(sys.argv[1])\n",
            "src/__init__.py": "",
        },
    },
    "adv-dead-code": {
        "purpose": "A repository with a large legacy module that looks important but is never reached.",
        "subsystems": ["active pipeline", "legacy module"],
        "entry_points": ["pipeline.py"],
        "weak_boundaries": [{"type": "Dead Code", "evidence": ["pipeline.py", "legacy/processor.py"], "note": "legacy/processor.py is large and documented as core but never imported"}],
        "misleading_signals": ["docs/architecture.md presents legacy/processor.py as the core processor"],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# pipeline\n\nProcesses records through the legacy processor.\n",
            "docs/architecture.md": "# Architecture\n\nThe legacy processor (legacy/processor.py) is the heart of the system.\n",
            "pipeline.py": "def run():\n    print('active pipeline')\n",
            "legacy/processor.py": "# Legacy processor - looks important\nimport time\n\nclass Processor:\n    \"\"\"The core processor (docs say).\"\"\"\n    def process(self, data):\n        time.sleep(1)\n        return data.upper()\n\n    def validate(self, data):\n        return True\n\n    def transform(self, data):\n        return data\n\n    def export(self, data):\n        return data\n\n    def notify(self, data):\n        return data\n",
            "legacy/__init__.py": "",
        },
    },
    "adv-unused-dep": {
        "purpose": "A small project whose requirements list a heavy dependency never imported.",
        "subsystems": ["core"],
        "entry_points": ["app.py"],
        "weak_boundaries": [{"type": "Implicit Dependencies", "evidence": ["requirements.txt", "app.py"], "note": "tensorflow listed but never imported; misleading about the real dependency footprint"}],
        "misleading_signals": ["requirements.txt suggests ML usage"],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# light-app\n\nA light application.\n",
            "requirements.txt": "requests==2.31.0\ntensorflow==2.16.0\n",
            "app.py": "import requests\n\ndef fetch(url):\n    return requests.get(url).status_code\n",
        },
    },
    "adv-duplicated-packages": {
        "purpose": "Two directories define the same package name with conflicting behavior.",
        "subsystems": ["utils (top)", "core.utils (nested)"],
        "entry_points": ["main.py"],
        "weak_boundaries": [{"type": "Vocabulary Drift", "evidence": ["utils.py", "core/utils.py", "main.py"], "note": "duplicate utils package; imports resolve ambiguously"}],
        "misleading_signals": ["same module name in two locations"],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# dup-packages\n",
            "main.py": "from utils import fmt\nfrom core.utils import fmt as fmt2\nprint(fmt(), fmt2())\n",
            "utils.py": "def fmt():\n    return 'top'\n",
            "core/__init__.py": "",
            "core/utils.py": "def fmt():\n    return 'nested'\n",
        },
    },
    "adv-misleading-dirs": {
        "purpose": "Directory names are misleading: models/ contains HTTP handlers, handlers/ contains data models.",
        "subsystems": ["models dir (handlers)", "handlers dir (models)"],
        "entry_points": ["main.py"],
        "weak_boundaries": [{"type": "Vocabulary Drift", "evidence": ["models/user.py", "handlers/user.py"], "note": "directory names inverted relative to contents"}],
        "misleading_signals": ["models/ is not models"],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# misleading-dirs\n",
            "main.py": "from handlers.user import User\nfrom models.user import handle\nprint(User, handle)\n",
            "models/__init__.py": "",
            "models/user.py": "def handle(request):\n    return 'handled'\n",
            "handlers/__init__.py": "",
            "handlers/user.py": "class User:\n    pass\n",
        },
    },
    "adv-removed-feature-docs": {
        "purpose": "Documentation describes a feature that was removed from the code.",
        "subsystems": ["code", "docs"],
        "entry_points": ["app.py"],
        "weak_boundaries": [{"type": "Orphaned Examples", "evidence": ["docs/export.md", "app.py"], "note": "docs/export.md documents the export feature; no export code exists"}],
        "misleading_signals": ["README links to export docs"],
        "fog": ["docs_fog"],
        "files": {
            "README.md": "# removed-feature\n\nSee [export docs](docs/export.md).\n",
            "docs/export.md": "# Export\n\n`python app.py export --format csv` exports all records.\n",
            "app.py": "def ingest():\n    print('ingest')\n\nif __name__ == '__main__':\n    ingest()\n",
        },
    },
    "adv-multi-registry": {
        "purpose": "Two conflicting workflow registries exist; recommended IDs differ between them.",
        "subsystems": ["runtime registry", "stale registry"],
        "entry_points": ["main.py"],
        "weak_boundaries": [{"type": "Contract Mismatch", "evidence": [".workflows/registry.yaml", "docs/workflow-registry.yaml"], "note": "two registries with conflicting workflow IDs; routing grounded in the wrong one breaks"}],
        "misleading_signals": ["docs registry is stale but looks authoritative"],
        "fog": ["architecture_fog"],
        "files": {
            "README.md": "# multi-registry\n",
            "main.py": "print('app')\n",
            ".workflows/registry.yaml": "workflows:\n  - id: architecture-implementation-workflow\n  - id: fast-path-workflow\n",
            "docs/workflow-registry.yaml": "workflows:\n  - id: arch-implementation-workflow\n  - id: fastpath-workflow\n",
        },
    },
    "adv-partial-impl": {
        "purpose": "A project whose entry point exists but core functionality is unimplemented.",
        "subsystems": ["entry point", "unimplemented core", "tests"],
        "entry_points": ["main.py"],
        "weak_boundaries": [{"type": "Ghost Features", "evidence": ["core.py", "main.py"], "note": "main.py calls core functions that raise NotImplementedError"}],
        "misleading_signals": ["README claims feature is implemented"],
        "fog": ["product_fog"],
        "files": {
            "README.md": "# partial-impl\n\nImplements report generation.\n",
            "main.py": "from core import generate_report\n\nif __name__ == '__main__':\n    generate_report('data.csv')\n",
            "core.py": "def generate_report(path):\n    raise NotImplementedError('report generation not implemented yet')\n",
            "tests/test_core.py": "import pytest\n\ndef test_generate_report():\n    from core import generate_report\n    with pytest.raises(NotImplementedError):\n        generate_report('x')\n",
        },
    },
}

def main() -> None:
    ground_truth = []
    for repo_id, meta in FIXTURES.items():
        r = make_repo(repo_id, meta["files"])
        sha = subprocess.run(["git", "-C", str(r), "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
        ground_truth.append({
            "repository_id": repo_id,
            "commit_sha": sha,
            "purpose": meta["purpose"],
            "expected_major_subsystems": meta["subsystems"],
            "known_entry_points": meta["entry_points"],
            "known_weak_boundaries": meta["weak_boundaries"],
            "known_misleading_signals": meta["misleading_signals"],
            "expected_fog_candidates": meta["fog"],
        })
        print(f"{repo_id}: {sha[:12]}")
    gt_path = CORPUS / "ground-truth.yaml"
    gt_path.write_text(yaml.safe_dump({"corpus_schema": "repository-sensemaking-corpus-v1",
                                       "frozen_at": "2026-08-06T00:00:00Z",
                                       "note": "ground truth frozen BEFORE any candidate outputs; do not change after results are visible without versioning the fixture",
                                       "repositories": ground_truth}, sort_keys=False), encoding="utf-8")
    print(f"ground truth written: {gt_path} ({len(ground_truth)} repos)")


if __name__ == "__main__":
    main()
