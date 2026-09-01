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
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import yaml

import evidence_quote_extractor as _qe

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
# | weakness_type                | model, constrained (issue #80) |
# | weakness_type_explanation    | model, constrained (required only if weakness_type == Other) |
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
    "weakness_type",
    "weakness_type_explanation",
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
            # Deliberately does NOT spell out the two-word marker phrase
            # validate-brief.py's NO_LOGIC_TRACE check scans for (see the
            # execution-instruction prompt in scripts/skill_executor.py's
            # build_semantic_authorities_block for the literal phrase and
            # full explanation) -- if this reminder said the phrase itself,
            # every skeleton would trivially satisfy that check even when
            # the model never wrote the required reasoning paragraph,
            # silently defeating the validator.
            lines.append(
                "<!-- REQUIRED: this section's prose must include a "
                "paragraph giving the diagnostic reasoning chain that "
                "connects the cited evidence to the weakest-boundary "
                "conclusion, starting with the exact two-word marker phrase "
                "specified in your execution instructions followed by a "
                "colon. validate-brief.py fails the whole artifact "
                "(error code NO_LOGIC_TRACE) if that reasoning paragraph is "
                "absent. -->"
            )
            lines.append("")
            lines.append("## 8. Evidence excerpts")
            lines.append("")
            lines.append(_marker("evidence_excerpts", "BEGIN"))
            lines.append("")
            lines.append(
                "<!-- REQUIRED: every item below must include file, lines, "
                "supports_claim (exact key names -- `citation` or similar "
                "does NOT satisfy this). Give the SMALLEST sufficient line "
                "range that contains the cited text -- do not invent paths. "
                "A `quote` key is also required by the schema, but its "
                "text does not matter: the runtime OVERWRITES it with the "
                "exact verbatim text read from file/lines before "
                "validation (issue #89) -- write a short placeholder like "
                "'see file/lines' rather than trying to retype the source "
                "text yourself. validate-brief.py raises "
                "EVIDENCE_EXCERPT_FIELD per missing/misnamed key, per "
                "excerpt. -->"
            )
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
    lines.append("primary_fog_type:  # model fills: product_fog | ui_fog | docs_fog | architecture_fog")
    lines.append("diagnosis_conflict:  # model fills: true | false")
    lines.append("escalation_recommended:  # model fills: true | false")
    lines.append("evidence: []  # model fills: list of \"path/to/file (lines Lx-Ly): citation\"")
    lines.append("recommended_workflow_id:  # model fills: MUST match an id in workflow-registry.yaml")
    lines.append("recommended_execution_mode:  # model fills: plan_only | guided_execution")
    lines.append("weakest_boundary:  # model fills: short slug")
    lines.append(
        "weakness_type:  # model fills: one of the registered types in "
        "skills/repo-sensemaker/references/weakness-types.md, or 'Other'"
    )
    lines.append(
        "weakness_type_explanation: null  # model fills with a non-empty string ONLY "
        "if weakness_type is 'Other'; otherwise leave null"
    )
    lines.append("required_inputs:")
    lines.append("  - user_intent")
    lines.append("  - repository_state")
    lines.append(f"created_at: \"{ctx.created_at}\"")
    lines.append("immutable: true")
    lines.append("```")
    lines.append("")

    lines.append("## 15. Extended analysis")
    lines.append("")
    lines.append(
        "<!-- OPTIONAL, non-blocking (ADR 0024, ACCEPTED). Leave this block "
        "absent entirely if you have nothing here; validate-brief.py never "
        "requires it. If present, it must be a single `extended_analysis:` "
        "YAML mapping with any of: domain (list, reuses canonical fog "
        "vocabulary), consequential_boundary ({description, rationale, "
        "is_demonstrated_weakness}), uncertainty ({source, question}), "
        "owner_intent_state ({known, status}). -->"
    )
    lines.append("")
    lines.append(_marker("extended_analysis", "BEGIN"))
    lines.append("")
    lines.append(_marker("extended_analysis", "END"))
    lines.append("")

    return "\n".join(lines)


# --- Reconciliation ----------------------------------------------------------

_YAML_BLOCK_RE = re.compile(r"```yaml\s*(.*?)\s*```", re.DOTALL)

# Sentinel written into `quote` when deterministic extraction cannot complete
# (issue #89). Deliberately cannot match any real source line, so
# validate-brief.py's EVIDENCE_QUOTE_NOT_FOUND check -- the real downstream
# consumer -- always rejects it. This is the "fail loudly, never keep an
# unverified model quote" behavior: the reconciled artifact is still written
# (so the run doesn't crash uncleanly), but it is structurally guaranteed to
# fail brief validation rather than silently pass with an unverified quote.
QUOTE_EXTRACTION_FAILED_SENTINEL = "[[QUOTE_EXTRACTION_FAILED: {reason}]]"


class _QuotedStr(str):
    """Marker subclass: dumped as a double-quoted YAML scalar so the exact
    extracted text (Unicode code points, leading indentation, trailing
    spaces, embedded newlines, Markdown bold/backtick characters) survives
    YAML round-tripping byte-for-byte -- double-quoted scalars are the one
    YAML string style that never depends on re-indentation rules the way
    block-literal ('|') scalars do, which matters because extracted quotes
    can have inconsistent internal indentation.
    """


class _EvidenceExcerptDumper(yaml.SafeDumper):
    pass


def _quoted_str_representer(dumper: yaml.SafeDumper, data: "_QuotedStr"):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style='"')


_EvidenceExcerptDumper.add_representer(_QuotedStr, _quoted_str_representer)


def _strip_yaml_fence(text: str) -> str:
    """If `text` is wrapped in a ```yaml ... ``` fence, return the inner
    content; otherwise return `text` unchanged. Extraction must tolerate
    the model either following instructions literally (leaving the fence
    marks in place between the markers) or replacing only the inner list.
    """
    m = _YAML_BLOCK_RE.search(text)
    if m and m.group(0).strip() == text.strip():
        return m.group(1)
    return text


def reconcile_evidence_excerpt_quotes(raw_block_text: str, target_root: str) -> tuple[str, list[str]]:
    """Deterministically overwrite every evidence_excerpts[].quote with text
    read from the source file at `target_root`/file, lines `lines` (issue
    #89). The model's own `quote` value, if any, is discarded and never
    trusted -- this function is the sole verbatim-copy boundary.

    Returns (bare_yaml_text, warnings). `bare_yaml_text` has no ```yaml
    fence wrapper (the caller adds one). `warnings` is a list of
    human-readable extraction failures, one per excerpt where extraction
    could not complete; each such excerpt's `quote` is replaced with
    QUOTE_EXTRACTION_FAILED_SENTINEL, which is guaranteed to fail
    validate-brief.py's EVIDENCE_QUOTE_NOT_FOUND check rather than silently
    keeping an unverified value.
    """
    inner = _strip_yaml_fence(raw_block_text).strip()
    try:
        data = yaml.safe_load(inner)
    except Exception as e:
        # Cannot parse at all -- leave the raw text untouched; validate-brief.py
        # already reports PARSING_ERROR / MISSING_EVIDENCE_EXCERPTS for this
        # case, which is the real downstream consumer for malformed YAML.
        return raw_block_text, [f"could not parse evidence_excerpts YAML: {e}"]

    if isinstance(data, dict):
        excerpts = data.get("evidence_excerpts")
        wrap_key = True
    elif isinstance(data, list):
        excerpts = data
        wrap_key = False
    else:
        return raw_block_text, ["evidence_excerpts block is not a list or a dict containing one"]

    if not isinstance(excerpts, list):
        return raw_block_text, ["evidence_excerpts value is not a list"]

    warnings: list[str] = []
    new_excerpts: list[dict] = []
    for i, exc in enumerate(excerpts):
        if not isinstance(exc, dict):
            new_excerpts.append(exc)
            continue
        item = dict(exc)
        file_path = item.get("file")
        lines_value = item.get("lines")
        if file_path and lines_value is not None:
            try:
                start, end = _qe.parse_lines_value(str(lines_value))
                extracted = _qe.extract_quote(str(file_path), start, end, target_root)
                item["quote"] = _QuotedStr(extracted.quote)
            except _qe.QuoteExtractionError as e:
                reason = str(e)
                warnings.append(f"excerpt[{i}] ({file_path!r} lines={lines_value!r}): {reason}")
                item["quote"] = _QuotedStr(QUOTE_EXTRACTION_FAILED_SENTINEL.format(reason=reason))
        # If file/lines are missing entirely, leave whatever quote (if any)
        # the model supplied -- validate-brief.py's EVIDENCE_EXCERPT_FIELD /
        # HALLUCINATED_FILE / INVALID_LINE_FORMAT checks already cover that
        # case; this function's job is quote fidelity, not field presence.
        new_excerpts.append(item)

    payload: Any = {"evidence_excerpts": new_excerpts} if wrap_key else new_excerpts
    dumped = yaml.dump(
        payload,
        Dumper=_EvidenceExcerptDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        # Without an explicit width, PyYAML wraps long double-quoted
        # scalars at ~80 columns using a literal line break rather than an
        # escaped "\n" -- and a literal line break inside a double-quoted
        # scalar folds back to a single space on the next parse (YAML line
        # folding), silently corrupting any extracted quote/evidence string
        # that contains a real newline or is simply long. A very large
        # width keeps every scalar on one physical line so embedded
        # newlines stay as explicit "\n" escapes and round-trip exactly.
        width=1_000_000,
    )
    return dumped.rstrip("\n"), warnings


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

    # extended_analysis (Section 15, ADR 0024): same shape as
    # evidence_excerpts -- its own marker pair holding a yaml fence, kept
    # out of MODEL_SECTIONS so build_skeleton() can place it after Section
    # 13 rather than inline with the free-prose sections. Unlike
    # evidence_excerpts, no quote-style deterministic overwrite is needed
    # here -- the raw harvested text is spliced back verbatim; validate-
    # brief.py is the sole authority on whether its content is acceptable.
    begin = re.escape(_marker("extended_analysis", "BEGIN"))
    end = re.escape(_marker("extended_analysis", "END"))
    pattern = re.compile(f"{begin}(.*?){end}", re.DOTALL)
    m = pattern.search(text)
    if m:
        block = m.group(1).strip("\n")
        if block.strip():
            found["extended_analysis"] = block

    return found


# Runtime-default required_inputs shipped by the skeleton when the model does
# not supply its own non-empty list.
_DEFAULT_REQUIRED_INPUTS = ["user_intent", "repository_state"]

# Model-authored scalar/bool machine fields, copied verbatim (invalid values
# are preserved unchanged for the validator to reject; runtime never repairs).
_MODEL_SCALAR_MACHINE_FIELDS = (
    "user_implied_fog_type",
    "primary_fog_type",
    "diagnosis_conflict",
    "escalation_recommended",
    "recommended_workflow_id",
    "recommended_execution_mode",
    "weakest_boundary",
    "weakness_type",
    "weakness_type_explanation",
    "outcome",  # optional explicit repository-action outcome (PHB §29)
)


def _project_evidence_strings(excerpts: list) -> list[str]:
    """Deterministically render Section-13 `evidence` strings from Section-8
    evidence_excerpts: ``<file> (lines <lines>): <supports_claim>``.

    Fail-closed: incomplete/missing excerpts are skipped; empty => [] (the
    validator still rejects). This is serialization of existing model-owned
    evidence, not inference.
    """
    projected = []
    for ex in excerpts:
        file = ex.get("file")
        lines = ex.get("lines")
        claim = ex.get("supports_claim")
        if not file or not claim:
            continue
        line_suffix = f" (lines {lines})" if lines else ""
        projected.append(f"{file}{line_suffix}: {claim}")
    return projected


def _render_machine_block(harvested: dict, excerpts: list, ctx) -> str:
    """Build the authoritative Section-13 machine YAML mapping ONCE and
    serialize it exactly once (one structured mapping -> one yaml.dump).

    Section 13 is an atomic deterministic serialization boundary: runtime-owned
    fields come from the envelope and are never overwritten; model-authored
    fields are copied verbatim (semantic judgment stays the model's; the
    validator is the acceptance authority); required_inputs is a runtime
    default with a non-empty model override; outcome is preserved; evidence is
    deterministically derived from Section-8 excerpts (fail-closed).

    Because the result is a single Python mapping (which by construction has
    unique keys), field-level regex splicing that could introduce duplicate
    YAML keys is gone -- a duplicate key is structurally impossible here.
    """
    machine = {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "source_intent_ref": ctx.source_intent_ref,
    }
    if isinstance(harvested, dict):
        for key in _MODEL_SCALAR_MACHINE_FIELDS:
            if key in harvested:
                machine[key] = harvested[key]
        # Ruling 2 (directive #23): the producer-authored task-relative
        # representation-sufficiency assessment is a machine block dict field,
        # carried verbatim to the warrant seam (model supplies the semantic
        # judgment; runtime maps it deterministically; fail-closed upstream).
        rs = harvested.get("representation_sufficiency")
        if isinstance(rs, dict):
            machine["representation_sufficiency"] = rs
        # required_inputs: runtime default, non-empty model list overrides.
        ri = harvested.get("required_inputs")
        if isinstance(ri, list) and ri:
            machine["required_inputs"] = ri
        else:
            machine["required_inputs"] = list(_DEFAULT_REQUIRED_INPUTS)
        evidence = _project_evidence_strings(excerpts)
        if not evidence:
            # No excerpt-derived evidence. Backward-compatible fallback: if the
            # model supplied its own non-empty Section-13 evidence list, preserve
            # it verbatim (legacy fixtures/direct model-authoring path). This is
            # NOT the authoritative projection path -- the minute Section-8
            # excerpts exist, the derived list wins. Empty => fail closed.
            me = harvested.get("evidence")
            if isinstance(me, list) and me:
                evidence = [_QuotedStr(v) if isinstance(v, str) else v for v in me]
    else:
        machine["required_inputs"] = list(_DEFAULT_REQUIRED_INPUTS)
        evidence = []
    # Evidence is derived (from excerpts) when available, else model-authored,
    # else empty (validator rejects).
    machine["evidence"] = [_QuotedStr(e) if isinstance(e, str) else e for e in evidence] if evidence else []

    machine["created_at"] = _ForceDoubleQuoted(ctx.created_at)
    machine["immutable"] = True

    return yaml.dump(
        machine,
        Dumper=_EvidenceExcerptDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1_000_000,
    ).rstrip("\n")


class _ForceDoubleQuoted(str):
    """Marker: emit this scalar with explicit double quotes (preserves the
    skeleton's canonical `created_at: "..."` presentation through the atomic
    serializer)."""


def _force_double_quoted_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style='"')


_EvidenceExcerptDumper.add_representer(_ForceDoubleQuoted, _force_double_quoted_representer)


def _replace_section13_block(artifact_text: str, machine_block: str) -> str:
    """Replace exactly one Section-13 authoritative YAML block with the atomic
    machine_block (everything between the ```yaml fence markers under the
    Section-13 heading). Returns the text unmodified if the canonical location
    is not found."""
    pattern = re.compile(
        r"(## 13\. Machine-readable handoff\s*\n\n```yaml\n).*?(\n```)",
        re.DOTALL,
    )
    out, n = pattern.subn(lambda _m: _m.group(1) + machine_block + _m.group(2),
                          artifact_text, count=1)
    return out


def reconcile(
    model_output_text: str,
    ctx: SkeletonContext | None = None,
    target_root: str | None = None,
    framework_root: str | None = None,
) -> str:
    """Merge whatever the model produced back into a fresh canonical skeleton.

    This is the enforcement point: regardless of what `model_output_text`
    contains -- no YAML fence at all, custom headings, an attempted full
    file replacement, an attempted overwrite of artifact_id/created_at/
    immutable -- the returned artifact always has the runtime-owned
    envelope intact. Model-authored fields are copied verbatim (including
    invalid values like a skill id used as a workflow id); the runtime
    never invents a valid-looking substitute for an invalid model value.

    Issue #89: the one exception to "copied verbatim" is
    `evidence_excerpts[].quote`. The model is no longer the verbatim-copy
    boundary for quote text -- it only supplies `file` + `lines` (+
    rationale/supports_claim). This function deterministically re-derives
    `quote` from the source file at `target_root` (the repository the brief
    is ABOUT) and overwrites whatever the model wrote there, discarding it
    unread. `target_root` falls back to `framework_root` when not supplied,
    mirroring scripts/validate-brief.py's `citation_root` fallback so
    internal (single-repo) runs behave identically to before. `quote`
    extraction never reads from or writes to anywhere outside
    `target_root`/`framework_root` -- see evidence_quote_extractor.py for
    the path-authority proof.
    """
    ctx = ctx or SkeletonContext()
    skeleton = build_skeleton(ctx)
    extraction_root = target_root or framework_root or "."

    harvested_yaml = _extract_last_yaml_mapping(model_output_text)
    harvested_sections = _extract_model_sections(model_output_text)

    out = skeleton

    # ATOMIC Section-13 machine block (PHB §56). Replace the per-field regex
    # splice with ONE deterministic serialization boundary: runtime-owned fields
    # + harvested model-authored fields + derived evidence + defaulted
    # required_inputs are assembled into a SINGLE mapping and serialized exactly
    # once via yaml.dump. A plain Python dict has unique keys by construction,
    # so field-level splicing that could create duplicate YAML keys (the fresh
    # editor-I/O RECONCILIATION_DEFECT) is structurally impossible.
    # Model-authored values are preserved verbatim (invalid values reach the
    # validator unchanged, never repaired). Evidence is derived from Section-8
    # excerpts at the end via _project_section13_evidence-equivalent logic and
    # is NOT independently model-authored. required_inputs keeps its runtime
    # default + non-empty model override. outcome (optional) is preserved.
    excerpts = _parse_evidence_excerpts(model_output_text)
    machine_block = _render_machine_block(harvested_yaml, excerpts, ctx)
    out = _replace_section13_block(out, machine_block)

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
        # Issue #89: deterministically overwrite quote text before splicing.
        # This never raises -- extraction failures are converted into a
        # guaranteed-to-fail sentinel per excerpt (see
        # reconcile_evidence_excerpt_quotes docstring) so a single bad
        # citation never crashes the whole run; validate-brief.py is still
        # the authority that rejects the resulting artifact.
        content, extraction_warnings = reconcile_evidence_excerpt_quotes(content, extraction_root)
        for warning in extraction_warnings:
            # ASCII-only (CLAUDE.md console-output rule); this repo runs on
            # Windows cp1252 and non-ASCII stdout crashes the process.
            print(f"WARNING [brief_skeleton.reconcile] quote extraction failed: {warning}")
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

    if "extended_analysis" in harvested_sections:
        content = harvested_sections["extended_analysis"]
        begin = _marker("extended_analysis", "BEGIN")
        end = _marker("extended_analysis", "END")
        out = out.replace(f"{begin}\n\n{end}", f"{begin}\n\n{content}\n\n{end}")

    # The Section-13 evidence projection is now folded into the ATOMIC machine
    # block built by _render_machine_block (PHB §56): Section 8 validated
    # evidence_excerpts are deterministically serialized into Section-13
    # evidence (fail-closed; empty => []). No post-hoc regex block splice runs
    # here, so the fresh editor-I/O duplicate-key defect cannot recur.
    return out


def _project_section13_evidence(artifact_text: str) -> str:
    """Deterministically render the Section-13 machine `evidence:` list from the
    validated Section-8 `evidence_excerpts`.

    Each excerpt supplies file + lines + supports_claim; the runtime formats
    ``<file> (lines <lines>): <supports_claim>``. This is a serialization of
    existing model-owned evidence -- it MUST NOT invent a file/line/claim, infer
    from prose, or fill when no excerpts exist. Empty excerpts => `evidence: []`,
    which the validator correctly rejects.

    Returns the artifact text with the Section-13 `evidence` field rewritten in
    place (final brief schema for that field is preserved: a list of strings).
    """
    excerpts = _parse_evidence_excerpts(artifact_text)

    projected = []
    for ex in excerpts:
        file = ex.get("file")
        lines = ex.get("lines")
        claim = ex.get("supports_claim")
        if not file or not claim:
            continue  # model supplied an incomplete excerpt; skip projection
        line_suffix = f" (lines {lines})" if lines else ""
        projected.append(f"{file}{line_suffix}: {claim}")

    # Build the machine `evidence:` value with the existing YAML-safe dumper so
    # every escaping rule is handled deterministically (mirrors reconcile's own
    # evidence serialization: _QuotedStr + _EvidenceExcerptDumper + width cap).
    if projected:
        block = yaml.dump(
            {"evidence": [_QuotedStr(str(v)) for v in projected]},
            Dumper=_EvidenceExcerptDumper,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
            width=1_000_000,
        ).rstrip("\n")
    else:
        block = "evidence: []"

    # Replace the FULL Section-13 evidence mapping: the `evidence:` line plus any
    # subsequent indented block (list items / continuation lines), terminating
    # before the next non-indented line (the next machine key). We KEEP the
    # newline that precedes the next key so the machine block stays well-formed.
    def _repl(m):
        # m.group(0) is the whole evidence block; we replace it, keeping the
        # newline that originally followed (so the next key starts on its own line).
        return m.group(1) + block + m.group(2)

    pattern = re.compile(
        r"(?m)^(\s*)evidence:.*(?:\n[ \t]+[^\n]*)*(?=(\n[ \t]*(?:user_implied_fog_type|primary_fog_type|diagnosis_conflict|escalation_recommended|recommended_workflow_id|recommended_execution_mode|weakest_boundary|weakness_type|required_inputs|created_at|immutable):))"
    )
    out, n = pattern.subn(_repl, artifact_text, count=1)
    if n == 0:
        # No machine `evidence:` block matched; leave the artifact unchanged.
        return artifact_text
    return out


def _parse_evidence_excerpts(artifact_text: str) -> list[dict]:
    """Extract the model-supplied evidence_excerpts (file/lines/supports_claim)
    from the Section 8 YAML block. Pure parse; returns [] if none/empty."""
    m = re.search(r"## 8\. Evidence excerpts(.*?)(?=## 9\.)", artifact_text, re.DOTALL | re.IGNORECASE)
    if not m:
        return []
    block = m.group(1)
    fence = re.search(r"```yaml\s*(.*?)\s*```", block, re.DOTALL)
    if not fence:
        return []
    try:
        data = yaml.safe_load(fence.group(1))
    except Exception:
        return []
    if not isinstance(data, dict) or not isinstance(data.get("evidence_excerpts"), list):
        return []
    result = []
    for item in data["evidence_excerpts"]:
        if not isinstance(item, dict):
            continue
        result.append({
            "file": item.get("file"),
            "lines": item.get("lines"),
            "supports_claim": item.get("supports_claim"),
        })
    return result


def skeleton_integrity_ok(text: str) -> bool:
    """True iff every runtime-owned marker/field is present and unaltered enough
    for validate-brief.py to at least find the YAML fence and required headings.

    NOTE: this is a purely structural (string-presence) check. It does NOT
    parse or validate any YAML content -- a document that has every marker
    and heading in place but a syntactically invalid Section 13 YAML block
    (e.g. Evidence 0014's unescaped-quote HANDOFF_YAML_PARSE_ERROR) still
    returns True here. Use `handoff_yaml_round_trips()` for the YAML-
    parseability guarantee; do not read "integrity_ok: true" as "the
    authoritative handoff parses."
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


def extract_handoff_yaml_block(text: str) -> str | None:
    """Return the raw text inside Section 13's ```yaml fence, or None if the
    section/fence cannot be located at all (a structural problem, not a YAML
    syntax problem -- see `skeleton_integrity_ok` for that check).
    """
    marker = "## 13. Machine-readable handoff"
    idx = text.find(marker)
    if idx == -1:
        return None
    m = _YAML_BLOCK_RE.search(text, idx)
    if not m:
        return None
    return m.group(1)


def handoff_yaml_round_trips(text: str) -> tuple[bool, str | None]:
    """The authoritative-handoff parseability guarantee (issue: Evidence
    0014's HANDOFF_YAML_PARSE_ERROR shipped with `integrity_ok: true`
    because integrity checking never actually parsed the YAML it claimed
    was intact).

    Returns (True, None) iff Section 13's YAML fence exists, is valid YAML
    per `yaml.safe_load`, and parses to a mapping. Returns (False, reason)
    otherwise. This is deliberately independent of validate-brief.py's own
    semantic checks (field values, evidence grounding, etc.) -- it only
    proves the block is syntactically well-formed YAML, which is the
    precondition validate-brief.py itself needs before it can even begin
    semantic validation.
    """
    block = extract_handoff_yaml_block(text)
    if block is None:
        return False, "Section 13 YAML fence not found"
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as e:
        return False, f"YAML_PARSE_ERROR: {e}"
    if not isinstance(data, dict):
        return False, "Section 13 YAML did not parse to a mapping"
    return True, None
