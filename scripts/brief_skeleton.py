"""
Runtime-owned skeleton for repository_sensemaking_brief (issue #55 / ADR-pending).

Problem this closes: PR #54 proved that asking a free-form model to also
produce deterministic artifact grammar (exact headings, a single YAML fence,
`artifact_id`, schema/version fields, timestamps, field ordering) is not
reliable -- the model omitted the YAML block entirely and validation failed
before semantic fields could even be checked.

Architecture (per skills/workflow-planner/references/artifact-contracts.yaml's
`repository_sensemaking_brief` contract and CLAUDE.md's "artifacts are the
API" principle):

    runtime creates canonical artifact skeleton
        -> model fills designated semantic regions
        -> runtime reconciles model output back into the canonical skeleton
        -> runtime writes the final artifact
        -> validate-brief.py validates it (unchanged, still authoritative)

Three responsibilities stay separate:
  - Runtime guarantees SHAPE: headings, the single YAML fence, field
    ordering, and runtime-owned field values can never be lost or
    overwritten by model output, however the model responds (no YAML at
    all, custom headings, an attempt to replace the whole file, an attempt
    to overwrite artifact_id, ...).
  - Validator guarantees CONTRACT: validate-brief.py is untouched by this
    module and remains the sole authority on whether semantic content is
    acceptable.
  - Model supplies JUDGMENT: fog classification, workflow choice, escalation
    flag, evidence, and prose. If the model emits an invalid value (e.g. a
    skill id like "docs-aligner" instead of a workflow id), that invalid
    value is preserved verbatim in the reconciled artifact -- never silently
    replaced with a valid-looking default. The validator must be the one to
    reject it.

This module owns skeleton generation and reconciliation. It does not invoke
the model and does not talk to the SDK; scripts/skill_executor.py wires it
into the actual invocation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

ARTIFACT_ID = "repository_sensemaking_brief"
SCHEMA_VERSION = 1

# --- Field classification (Phase 1 ownership table) -------------------------
#
# | Field/section              | Owner                  |
# |-----------------------------|------------------------|
# | artifact_id                 | runtime                |
# | schema_version              | runtime                |
# | created_at                  | runtime                |
# | created_by                  | runtime                |
# | immutable                   | runtime                |
# | required_inputs             | runtime                |
# | source_intent_ref            | runtime (from context) |
# | primary_fog_type            | model, constrained     |
# | user_implied_fog_type       | model, constrained     |
# | diagnosis_conflict          | model, constrained     |
# | escalation_recommended      | model, constrained     |
# | recommended_workflow_id     | model, registry-checked (never silently fixed) |
# | recommended_execution_mode  | model, constrained     |
# | evidence                    | model, constrained     |
# | weakest_boundary            | model, constrained     |
# | repository goal (sec 1)     | model, prose           |
# | strong signals (sec 3)      | model, prose           |
# | missing pieces (sec 4)      | model, prose           |
# | improvement opps (sec 5)    | model, prose           |
# | weakest boundary prose (6)  | model, prose           |
# | evidence prose (7)          | model, prose           |
# | evidence excerpts (8)       | model, constrained yaml|
# | why it matters (9)          | model, prose           |
# | candidate next steps (10)   | model, prose           |
# | recommended next step (11)  | model, prose           |
# | ready-to-copy prompt (14)   | model, prose           |
#
# Runtime-owned YAML keys: never taken from the model, always the runtime's
# own values, in this fixed order.
RUNTIME_OWNED_YAML_FIELDS = (
    "artifact_id",
    "schema_version",
    "source_intent_ref",
    "created_at",
    "immutable",
)

# Model-authored but constrained YAML keys: the model supplies the value:
# the runtime preserves it verbatim (valid or not) so the validator, not the
# runtime, is the thing that rejects bad values.
MODEL_YAML_FIELDS = (
    "user_implied_fog_type",
    "primary_fog_type",
    "diagnosis_conflict",
    "escalation_recommended",
    "evidence",
    "recommended_workflow_id",
    "recommended_execution_mode",
    "weakest_boundary",
    "required_inputs",
)

# Prose sections the model fills, each bounded by a stable, greppable marker
# pair. Order matches the human-facing section numbering in
# skills/repo-sensemaker/references/repo-analysis-template.md.
MODEL_SECTIONS: tuple[tuple[str, str], ...] = (
    ("repository_goal", "## 1. Repository goal"),
    ("current_shape", "## 2. Current shape"),
    ("strong_signals", "## 3. Strong signals"),
    ("missing_pieces", "## 4. Missing pieces"),
    ("improvement_opportunities", "## 5. Improvement opportunities"),
    ("weakest_boundary_prose", "## 6. Weakest boundary"),
    ("evidence_prose", "## 7. Evidence"),
    ("why_boundary_matters", "## 9. Why this boundary matters"),
    ("candidate_next_steps", "## 10. Candidate next steps"),
    ("recommended_next_step", "## 11. Recommended next step"),
    ("ready_to_copy_prompt", "## 14. Ready-to-copy prompt"),
)


def _marker(section_id: str, which: str) -> str:
    return f"<!-- MODEL_SECTION:{section_id}:{which} -->"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class SkeletonContext:
    """Runtime-owned values a skeleton is built from. Never model-supplied."""
    source_intent_ref: str = "artifacts/01-orchestration-run/00-user-intent.md"
    created_at: str = field(default_factory=_now_iso)
    created_by: str = "workflow-runtime"


def build_skeleton(ctx: SkeletonContext | None = None) -> str:
    """Build the canonical repository_sensemaking_brief skeleton.

    Every required heading and the single authoritative YAML fence are
    present up front, with runtime-owned fields already filled in and
    model-authored fields present as empty placeholders the model must
    replace. The model can never "forget" the envelope because the runtime
    wrote it before the model ever ran.
    """
    ctx = ctx or SkeletonContext()

    lines: list[str] = []
    lines.append("# Repository Sensemaking Brief")
    lines.append("")
    lines.append(f"<!-- artifact_id: {ARTIFACT_ID} | schema_version: {SCHEMA_VERSION} -->")
    lines.append(f"<!-- runtime-generated skeleton created_at: {ctx.created_at} -->")
    lines.append("")

    for section_id, heading in MODEL_SECTIONS:
        lines.append(heading)
        lines.append("")
        lines.append(_marker(section_id, "BEGIN"))
        lines.append("")
        lines.append(_marker(section_id, "END"))
        lines.append("")
        if section_id == "weakest_boundary_prose":
            # Section 6.5: fog classification is a constrained YAML field,
            # not free prose, but keep the heading for human readability.
            lines.append("## 6.5. Problem classification (fog type)")
            lines.append("")
            lines.append(
                "Fog type is recorded in the machine-readable handoff block "
                "(Section 13), not here."
            )
            lines.append("")
        if section_id == "evidence_prose":
            lines.append("## 8. Evidence excerpts")
            lines.append("")
            lines.append(_marker("evidence_excerpts", "BEGIN"))
            lines.append("")
            lines.append("```yaml")
            lines.append("evidence_excerpts: []")
            lines.append("```")
            lines.append("")
            lines.append(_marker("evidence_excerpts", "END"))
            lines.append("")

    lines.append("## 12. Recommended workflow")
    lines.append("")
    lines.append(
        "See `recommended_workflow_id` in Section 13. Must match an id in "
        "workflow-registry.yaml. Do not invent workflow ids."
    )
    lines.append("")

    lines.append("## 13. Machine-readable handoff")
    lines.append("")
    lines.append("```yaml")
    lines.append(f"artifact_id: {ARTIFACT_ID}")
    lines.append(f"schema_version: {SCHEMA_VERSION}")
    lines.append(f"source_intent_ref: {ctx.source_intent_ref}")
    lines.append("user_implied_fog_type:  # model fills: product_fog | ui_fog | docs_fog | architecture_fog | unknown")
    lines.append("primary_fog_type:  # model fills: product_fog | ui_fog | docs_fog | architecture_fog | mixed | unknown")
    lines.append("diagnosis_conflict:  # model fills: true | false")
    lines.append("escalation_recommended:  # model fills: true | false")
    lines.append("evidence: []  # model fills: list of \"path/to/file (lines Lx-Ly): citation\"")
    lines.append("recommended_workflow_id:  # model fills: MUST match an id in workflow-registry.yaml")
    lines.append("recommended_execution_mode:  # model fills: plan_only | guided_execution")
    lines.append("weakest_boundary:  # model fills: short slug")
    lines.append("required_inputs:")
    lines.append("  - user_intent")
    lines.append("  - repository_state")
    lines.append(f"created_at: \"{ctx.created_at}\"")
    lines.append("immutable: true")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


# --- Reconciliation ----------------------------------------------------------

_YAML_BLOCK_RE = re.compile(r"```yaml\s*(.*?)\s*```", re.DOTALL)


def _extract_last_yaml_mapping(text: str) -> dict[str, Any]:
    """Best-effort: find the last parseable YAML mapping in arbitrary text.

    Used only to *harvest field values* from whatever the model produced,
    however malformed the surrounding document is. This never decides
    validity -- validate-brief.py does that on the final reconciled file.
    """
    import yaml

    best: dict[str, Any] = {}
    for match in _YAML_BLOCK_RE.finditer(text):
        try:
            data = yaml.safe_load(match.group(1))
        except Exception:
            continue
        if isinstance(data, dict):
            best.update(data)
    return best


def _extract_model_sections(text: str) -> dict[str, str]:
    """Pull whatever prose the model placed between each MODEL_SECTION marker.

    If the model didn't preserve markers at all (e.g. replaced the whole
    file), this returns an empty dict for every section and the skeleton's
    empty placeholders survive -- an empty required section is a validator
    concern, not something the runtime papers over.
    """
    found: dict[str, str] = {}
    for section_id, _heading in MODEL_SECTIONS:
        begin = re.escape(_marker(section_id, "BEGIN"))
        end = re.escape(_marker(section_id, "END"))
        pattern = re.compile(f"{begin}(.*?){end}", re.DOTALL)
        m = pattern.search(text)
        if m:
            content = m.group(1).strip("\n")
            if content.strip():
                found[section_id] = content

    # evidence_excerpts is its own marker pair, holding a yaml fence rather
    # than prose; keep it distinct from the free-prose sections above.
    begin = re.escape(_marker("evidence_excerpts", "BEGIN"))
    end = re.escape(_marker("evidence_excerpts", "END"))
    pattern = re.compile(f"{begin}(.*?){end}", re.DOTALL)
    m = pattern.search(text)
    if m:
        block = m.group(1).strip("\n")
        if block.strip() and "evidence_excerpts: []" not in block:
            found["evidence_excerpts"] = block

    return found


def reconcile(model_output_text: str, ctx: SkeletonContext | None = None) -> str:
    """Merge whatever the model produced back into a fresh canonical skeleton.

    This is the enforcement point: regardless of what `model_output_text`
    contains -- no YAML fence at all, custom headings, an attempted full
    file replacement, an attempted overwrite of artifact_id/created_at/
    immutable -- the returned artifact always has the runtime-owned
    envelope intact. Model-authored fields are copied verbatim (including
    invalid values like a skill id used as a workflow id); the runtime
    never invents a valid-looking substitute for an invalid model value.
    """
    ctx = ctx or SkeletonContext()
    skeleton = build_skeleton(ctx)

    harvested_yaml = _extract_last_yaml_mapping(model_output_text)
    harvested_sections = _extract_model_sections(model_output_text)

    out = skeleton

    # Merge constrained YAML fields (verbatim, no validity rewriting).
    for key in MODEL_YAML_FIELDS:
        if key not in harvested_yaml:
            continue
        value = harvested_yaml[key]
        if key == "evidence":
            if isinstance(value, list) and value:
                block = "evidence:\n" + "\n".join(f'  - "{v}"' for v in value)
            else:
                continue
            out = re.sub(r"evidence: \[\].*", block, out)
        elif key == "required_inputs":
            # Runtime already ships a safe default (user_intent,
            # repository_state); only override if the model gave a
            # non-empty list, preserved verbatim.
            if isinstance(value, list) and value:
                block = "required_inputs:\n" + "\n".join(f"  - {v}" for v in value)
                out = re.sub(
                    r"required_inputs:\n(?:  - .*\n)*", block + "\n", out
                )
        else:
            placeholder_re = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
            out = placeholder_re.sub(f"{key}: {value}", out, count=1)

    # Merge prose sections.
    for section_id, _heading in MODEL_SECTIONS:
        if section_id not in harvested_sections:
            continue
        content = harvested_sections[section_id]
        begin = _marker(section_id, "BEGIN")
        end = _marker(section_id, "END")
        out = out.replace(f"{begin}\n\n{end}", f"{begin}\n\n{content}\n\n{end}")

    if "evidence_excerpts" in harvested_sections:
        content = harvested_sections["evidence_excerpts"]
        begin = _marker("evidence_excerpts", "BEGIN")
        end = _marker("evidence_excerpts", "END")
        replacement = f"{begin}\n\n```yaml\n{content}\n```\n\n{end}"
        out = re.sub(
            re.escape(begin) + r".*?" + re.escape(end),
            lambda _m: replacement,
            out,
            count=1,
            flags=re.DOTALL,
        )

    return out


def skeleton_integrity_ok(text: str) -> bool:
    """True iff every runtime-owned marker/field is present and unaltered enough
    for validate-brief.py to at least find the YAML fence and required headings.
    Used by tests, not by the reconciliation path itself (reconcile() always
    rebuilds from a fresh skeleton, so this should always be True on its output).
    """
    if text.count("```yaml") < 1:
        return False
    if f"artifact_id: {ARTIFACT_ID}" not in text:
        return False
    if "## 13. Machine-readable handoff" not in text:
        return False
    for section_id, heading in MODEL_SECTIONS:
        if heading not in text:
            return False
    return True
