import argparse
import json
from pathlib import Path

STORE = Path("tasks.json")

def load():
    if not STORE.exists():
        return []
    return json.loads(STORE.read_text())

def add(title: str):
    tasks = load()
    tasks.append({"id": len(tasks) + 1, "title": title, "done": False})
    STORE.write_text(json.dumps(tasks))

def main():
    p = argparse.ArgumentParser(prog="tasks")
    sub = p.add_subparsers(dest="cmd")
    add_p = sub.add_parser("add"); add_p.add_argument("title")
    sub.add_parser("list")
    done_p = sub.add_parser("done"); done_p.add_argument("id", type=int)
    args = p.parse_args()
    if args.cmd == "add":
        add(args.title)
    elif args.cmd == "list":
        for t in load():
            print(t)
    elif args.cmd == "done":
        print("not implemented")

if __name__ == "__main__":
    main()
