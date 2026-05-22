#!/usr/bin/env python3
"""CLI utility to create an artifact conforming to its contract.

Locates the template for the artifact or generates a skeleton structure
based on contract requirements, and guarantees that the machine-readable YAML block
is initialized with correct fields (including artifact_id and source_intent_ref).
"""

import os
import sys
import argparse
import re
import yaml


def load_artifact_contracts(repo_root: str) -> dict | None:
    path = os.path.join(repo_root, "skills", "workflow-planner", "references", "artifact-contracts.yaml")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading artifact contracts: {e}", file=sys.stderr)
        return None


def get_skill_name(contract: dict) -> str:
    produced_by = contract.get("produced_by", "unknown")
    if isinstance(produced_by, list):
        return produced_by[0] if produced_by else "unknown"
    return str(produced_by)


def generate_skeleton(contract: dict) -> str:
    artifact_id = contract.get("id", "artifact")
    title = artifact_id.replace("_", " ").title()
    lines = [f"# {title}\n"]

    required_sections = contract.get("required_sections", [])
    for section in required_sections:
        sec_title = section.replace("_", " ").title()
        lines.extend([
            f"## {sec_title}",
            "",
            "(Fill in details here)",
            ""
        ])

    return "\n".join(lines)


def inject_yaml_block(content: str, artifact_id: str, intent_ref: str, required_fields: list) -> str:
    # Look for existing YAML blocks (fenced or non-fenced YAML blocks)
    yaml_match = re.search(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
    
    metadata = {}
    if yaml_match:
        try:
            parsed = yaml.safe_load(yaml_match.group(1))
            if isinstance(parsed, dict):
                metadata = parsed
        except Exception:
            pass

    # Ensure required fields have values
    metadata["artifact_id"] = artifact_id
    metadata["source_intent_ref"] = intent_ref
    
    for field in required_fields:
        if field not in metadata:
            # Set a placeholder value
            if field == "created_at":
                import datetime
                metadata[field] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif field == "status":
                metadata[field] = "draft"
            else:
                metadata[field] = "placeholder_value"

    yaml_block = yaml.dump(metadata, default_flow_style=False).strip()
    formatted_block = f"\n\n```yaml\n{yaml_block}\n```\n"

    if yaml_match:
        # Replace the existing block
        content = content[:yaml_match.start()] + f"```yaml\n{yaml_block}\n```" + content[yaml_match.end():]
    else:
        # Append to the end
        content = content.rstrip() + formatted_block

    return content


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a compliant artifact skeleton or template.")
    parser.add_argument("--artifact-id", required=True, help="ID of the artifact to create")
    parser.add_argument("--path", help="Output path where the file should be written (optional if run-id and step-id provided)")
    parser.add_argument("--intent-ref", help="Path or filename reference for source_intent_ref (optional)")
    parser.add_argument("--run-id", help="Run ID of the active session (optional)")
    parser.add_argument("--step-id", help="Step ID of the active step (optional)")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")

    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    contracts = load_artifact_contracts(repo_root)
    if not contracts:
        print(f"[ERROR] Could not load artifact-contracts.yaml under {repo_root}", file=sys.stderr)
        return 1

    contract = next((a for a in contracts.get("artifacts", []) if a.get("id") == args.artifact_id), None)
    if not contract:
        print(f"[ERROR] Contract not found for artifact ID: {args.artifact_id}", file=sys.stderr)
        return 1

    # Resolve output path
    out_path = args.path
    if not out_path:
        if not args.run_id or not args.step_id:
            print("[ERROR] Either --path or both --run-id and --step-id must be provided.", file=sys.stderr)
            return 1
        # Resolve standardized path: artifacts/<run_id>/<step_id>-<artifact_id>.md
        # Keep path slash format consistent
        out_path = os.path.join(repo_root, "artifacts", args.run_id, f"{args.step_id}-{args.artifact_id}.md")
    
    out_path = os.path.abspath(out_path)

    # Resolve intent-ref
    intent_ref = args.intent_ref
    if not intent_ref:
        if args.run_id:
            candidate = os.path.join(repo_root, "artifacts", args.run_id, "00-user-intent.md")
            if os.path.exists(candidate):
                intent_ref = os.path.relpath(candidate, repo_root).replace("\\", "/")
        if not intent_ref:
            import glob
            candidates = glob.glob(os.path.join(repo_root, "artifacts", "**", "00-user-intent.md"), recursive=True)
            if candidates:
                intent_ref = os.path.relpath(candidates[0], repo_root).replace("\\", "/")
            else:
                intent_ref = "artifacts/00-user-intent.md"

    produced_by = get_skill_name(contract)
    
    # Try loading from skill references folder
    template_paths = [
        os.path.join(repo_root, "skills", produced_by, "references", f"{args.artifact_id}-template.md"),
        os.path.join(repo_root, "skills", produced_by, "references", f"{args.artifact_id.replace('_', '-')}-template.md"),
        os.path.join(repo_root, "skills", produced_by, "references", "repo-analysis-template.md") if args.artifact_id == "repository_sensemaking_brief" else ""
    ]

    content = ""
    loaded_template = False
    for t_path in template_paths:
        if t_path and os.path.exists(t_path):
            try:
                with open(t_path, "r", encoding="utf-8") as f:
                    content = f.read()
                loaded_template = True
                print(f"  [OK] Loaded template from: {os.path.relpath(t_path, repo_root)}")
                break
            except Exception as e:
                print(f"  [WARN] Failed to read template at {t_path}: {e}", file=sys.stderr)

    if not loaded_template:
        print(f"  ~ No template found for '{args.artifact_id}', generating contract skeleton")
        content = generate_skeleton(contract)

    # Inject required machine fields into the YAML block
    required_fields = contract.get("required_machine_fields", [])
    content = inject_yaml_block(content, args.artifact_id, intent_ref, required_fields)

    # Write to target path
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        # Print path relative to repo root using forward slashes for output verification
        rel_out = os.path.relpath(out_path, repo_root).replace("\\", "/")
        print(f"[OK] Compliant artifact created at: {rel_out}")
        return 0
    except Exception as e:
        print(f"[ERROR] Failed to write artifact to {out_path}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
