"""Validator for Sensemaking session and semantic query receipts.

A receipt is a small, typed YAML record a session leaves behind so a later
session (or an owner reading asynchronously) can reconstruct where it stopped,
what it was authorized to do, and which questions remain open. It is not an
essay, not reviewed knowledge, and never an authority grant.

Artifact ids (see skills/workflow-planner/references/artifact-contracts.yaml):
  sensemaking_session_receipt  -> skills/using-sensemaking/references/session-receipt-v1.md
  semantic_query_receipt       -> skills/repository-semantic-steward/references/query-receipt.md

Error codes (substrings matched by tests/fixtures/validate-receipt/):
  RECEIPT_NOT_FOUND
  RECEIPT_PARSE_ERROR
  RECEIPT_ARTIFACT_ID
  RECEIPT_SCHEMA_VERSION
  RECEIPT_MISSING_FIELD
  RECEIPT_TYPE
  RECEIPT_ENUM
  RECEIPT_FORMAT
  RECEIPT_TEXT_TOO_LONG
  RECEIPT_DUPLICATE_ID
  RECEIPT_UNKNOWN_REF
  RECEIPT_STATE_CONFLICT
  RECEIPT_NON_DURABLE_REF
  RECEIPT_REF_MISSING
  RECEIPT_AUTHORITY_CLAIM
  RECEIPT_AUTHORITY_OVERLAP
  RECEIPT_OWNER_QUESTION_OPTIONS
  RECEIPT_STOP_WITHOUT_QUESTION
  RECEIPT_FILENAME
  RECEIPT_MISS_NOT_RECORDED
  RECEIPT_MISS_QUERY_OUTCOME
  RECEIPT_MODE_EVIDENCE
Warnings (non-blocking):
  RECEIPT_NOT_FINAL
  RECEIPT_NOT_DURABLE
  RECEIPT_LARGE

Exit codes: 0 = valid (warnings allowed), 1 = invalid.
Output is ASCII-only (repository convention: no non-ASCII on stdout).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

SESSION_RECEIPT_ID = "sensemaking_session_receipt"
QUERY_RECEIPT_ID = "semantic_query_receipt"
RECEIPT_ARTIFACT_IDS = (SESSION_RECEIPT_ID, QUERY_RECEIPT_ID)
FILE_SUFFIX = {SESSION_RECEIPT_ID: ".session.yaml", QUERY_RECEIPT_ID: ".query.yaml"}
RECEIPT_DIR = ".sensemaking/receipts"

SESSION_REF_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]{0,63}$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
QUALIFIED_QUESTION_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]{0,63}#Q-\d+$")

MAX_TEXT = 300
MAX_LABEL = 120
MAX_LINES = 250

STATES = ("in_progress", "final")
PERSISTENCE = ("pending", "committed", "working_tree_only", "host_uploaded")
LOAD_MODES = ("harness_discovered", "manual_explicit_load", "unknown")
GOAL_SOURCES = ("owner_message", "issue", "handoff", "prior_receipt", "campaign", "other")
AUTHORITY = (
    "read", "local_write", "run_local_commands", "commit", "push", "open_pr",
    "merge", "release", "deploy", "tracker_write", "knowledge_edit",
    "external_publication",
)
RESPONSIBILITY_STATUS = ("in_progress", "completed", "partial", "skipped", "blocked", "not_started")
VALIDATION_RESULTS = ("PASS", "FAIL", "NOT_RUN")
EPISTEMIC_STATUS = (
    "OBSERVED", "DERIVED", "INFERRED", "HYPOTHESIZED", "RATIFIED",
    "CONTRADICTED", "SUPERSEDED", "UNRESOLVED",
)
FINDING_DISPOSITIONS = ("open", "resolved", "handed_off", "no_action")
UNCERTAINTY_SOURCES = ("repository_evidence", "empirical", "owner_intent", "external_environment")
STOP_DISPOSITIONS = (
    "IN_PROGRESS", "GOAL_SATISFIED", "NO_FURTHER_WARRANT", "OWNER_DECISION_REQUIRED",
    "AUTHORITY_BOUNDARY", "EXTERNAL_BLOCKER", "SAFETY_STOP", "SCOPE_EXHAUSTED",
    "INTERRUPTED",
)

STEWARD_MODES = ("RECALL", "AUDIT", "RECONCILE", "BOOTSTRAP")
QUERY_OPERATIONS = (
    "orient", "build", "search", "explain", "why", "impact", "workspace-impact",
    "changes", "contradictions", "history", "audit", "proposal-check",
)
QUERY_OUTCOMES = ("HIT", "PARTIAL", "MISS", "NOT_ASSESSED", "NOT_APPLICABLE")
SOURCE_CHECK_RESULTS = ("SUPPORTED", "CONTRADICTED", "STALE", "NOT_CHECKED")
MISS_KINDS = ("NOT_ASSESSED", "NO_MATCH_IN_SCOPE")
MISS_FOLLOW_UPS = ("ADD_PROPOSED", "ADDED", "NO_MODEL_CHANGE", "DEFERRED")
RECONCILE_DISPOSITIONS = ("CONFIRM", "REVISE", "SUPERSEDE", "ADD", "CONTEST", "NO_MODEL_CHANGE")
PROPOSAL_CHECK_RESULTS = ("SEMANTIC_KNOWLEDGE_PROPOSAL_VALID", "INVALID", "NOT_RUN")

FRONTMATTER_RE = re.compile(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n", re.DOTALL)


class Checker:
    """Collects errors and warnings with stable codes."""

    def __init__(self) -> None:
        self.findings: list[dict[str, str]] = []

    def error(self, code: str, field: str, message: str) -> None:
        self.findings.append({"code": code, "severity": "error", "field": field, "message": message})

    def warn(self, code: str, field: str, message: str) -> None:
        self.findings.append({"code": code, "severity": "warning", "field": field, "message": message})

    @property
    def valid(self) -> bool:
        return not any(f["severity"] == "error" for f in self.findings)

    # -- primitive checks -------------------------------------------------

    def require(self, data: dict, key: str, field: str) -> bool:
        if key not in data:
            self.error("RECEIPT_MISSING_FIELD", field, f"missing required field: {field}")
            return False
        return True

    def mapping(self, data: dict, key: str, field: str) -> dict | None:
        if not self.require(data, key, field):
            return None
        value = data[key]
        if not isinstance(value, dict):
            self.error("RECEIPT_TYPE", field, f"{field} must be a mapping")
            return None
        return value

    def items(self, data: dict, key: str, field: str) -> list:
        if not self.require(data, key, field):
            return []
        value = data[key]
        if not isinstance(value, list):
            self.error("RECEIPT_TYPE", field, f"{field} must be a list")
            return []
        return value

    def text(self, value: Any, field: str, limit: int = MAX_TEXT, nullable: bool = False) -> None:
        if value is None and nullable:
            return
        if not isinstance(value, str) or not value.strip():
            self.error("RECEIPT_TYPE", field, f"{field} must be a non-empty string")
            return
        if len(value) > limit:
            self.error(
                "RECEIPT_TEXT_TOO_LONG", field,
                f"{field} is {len(value)} characters; limit is {limit}. A receipt records "
                "facts and pointers, not prose: move narrative into the referenced artifact.",
            )

    def enum(self, value: Any, allowed: tuple[str, ...], field: str) -> None:
        if value not in allowed:
            self.error("RECEIPT_ENUM", field, f"{field} has value {value!r}; allowed: {', '.join(allowed)}")

    def boolean(self, value: Any, field: str) -> None:
        if not isinstance(value, bool):
            self.error("RECEIPT_TYPE", field, f"{field} must be true or false")

    def pattern(self, value: Any, regex: re.Pattern[str], field: str, label: str, nullable: bool = False) -> None:
        if value is None and nullable:
            return
        if not isinstance(value, str) or not regex.match(value):
            self.error("RECEIPT_FORMAT", field, f"{field} must be {label}; got {value!r}")

    def string_list(self, value: Any, field: str, limit: int = MAX_LABEL, non_empty: bool = False) -> list[str]:
        if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
            self.error("RECEIPT_TYPE", field, f"{field} must be a list of non-empty strings")
            return []
        if non_empty and not value:
            self.error("RECEIPT_MISSING_FIELD", field, f"{field} must not be empty")
        for index, item in enumerate(value):
            if len(item) > limit:
                self.error("RECEIPT_TEXT_TOO_LONG", f"{field}[{index}]",
                           f"{field}[{index}] exceeds {limit} characters")
        return value

    def durable_ref(self, value: Any, field: str, target_repo: Path | None, nullable: bool = True) -> None:
        """A reference must be repository-relative so it survives the session."""
        if value is None and nullable:
            return
        if not isinstance(value, str) or not value.strip():
            self.error("RECEIPT_TYPE", field, f"{field} must be a repository-relative path")
            return
        posix = value.replace("\\", "/")
        if (
            posix.startswith("/")
            or posix.startswith("~")
            or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", posix)
            or ".." in posix.split("/")
        ):
            self.error(
                "RECEIPT_NON_DURABLE_REF", field,
                f"{field} is {value!r}: absolute, home, scheme-prefixed or '..' paths do not "
                "survive the session. Persist the artifact inside the repository and reference "
                "it by plain repository-relative path.",
            )
            return
        if target_repo is not None and not (target_repo / posix).exists():
            self.error("RECEIPT_REF_MISSING", field, f"{field} {value!r} does not exist under {target_repo}")

    def unique_ids(self, entries: list, prefix: str, field: str) -> set[str]:
        seen: set[str] = set()
        regex = re.compile(rf"^{re.escape(prefix)}-\d+$")
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                self.error("RECEIPT_TYPE", f"{field}[{index}]", f"{field}[{index}] must be a mapping")
                continue
            entry_id = entry.get("id")
            if not isinstance(entry_id, str) or not regex.match(entry_id):
                self.error("RECEIPT_FORMAT", f"{field}[{index}].id", f"id must look like {prefix}-1; got {entry_id!r}")
                continue
            if entry_id in seen:
                self.error("RECEIPT_DUPLICATE_ID", f"{field}[{index}].id", f"duplicate id {entry_id}")
            seen.add(entry_id)
        return seen


# -- shared envelope -------------------------------------------------------

def _check_envelope(c: Checker, data: dict, artifact_id: str, path: Path | None) -> None:
    if data.get("schema_version") != 1:
        c.error("RECEIPT_SCHEMA_VERSION", "schema_version", "schema_version must be 1")
    if c.require(data, "session_ref", "session_ref"):
        c.pattern(data["session_ref"], SESSION_REF_RE, "session_ref", "YYYY-MM-DD-<lowercase-slug>")
    if c.require(data, "state", "state"):
        c.enum(data["state"], STATES, "state")
    for key in ("created_at", "updated_at"):
        if c.require(data, key, key):
            c.pattern(data[key], TIMESTAMP_RE, key, "an ISO-8601 UTC timestamp like 2026-10-23T06:00:00Z")
    if c.require(data, "target_repository", "target_repository"):
        c.pattern(data["target_repository"], REPOSITORY_RE, "target_repository", "owner/repository")
    if c.require(data, "persistence", "persistence"):
        c.enum(data["persistence"], PERSISTENCE, "persistence")
    if c.require(data, "immutable", "immutable"):
        c.boolean(data["immutable"], "immutable")

    state = data.get("state")
    persistence = data.get("persistence")
    immutable = data.get("immutable")
    if state == "final":
        if immutable is not True:
            c.error("RECEIPT_STATE_CONFLICT", "immutable", "a final receipt must set immutable: true")
        if persistence == "pending":
            c.error("RECEIPT_STATE_CONFLICT", "persistence",
                    "a final receipt must record how it was persisted, not 'pending'")
        if persistence == "working_tree_only":
            c.warn("RECEIPT_NOT_DURABLE", "persistence",
                   "receipt was not committed or uploaded; it is lost when this checkout is discarded")
    elif state == "in_progress":
        if immutable is True:
            c.error("RECEIPT_STATE_CONFLICT", "immutable", "an in_progress receipt cannot be immutable")
        c.warn("RECEIPT_NOT_FINAL", "state",
               "session has not finalized this receipt; if no session is running, it was interrupted")

    if path is not None and path.suffix in (".yaml", ".yml"):
        session_ref = data.get("session_ref")
        expected = f"{session_ref}{FILE_SUFFIX[artifact_id]}"
        if isinstance(session_ref, str) and path.name != expected:
            c.error("RECEIPT_FILENAME", "session_ref", f"file must be named {expected}; got {path.name}")


# -- sensemaking_session_receipt -------------------------------------------

def _check_session(c: Checker, data: dict, target_repo: Path | None) -> None:
    state = data.get("state")

    identity = c.mapping(data, "source_identity", "source_identity")
    if identity is not None:
        if c.require(identity, "start_ref", "source_identity.start_ref"):
            c.pattern(identity["start_ref"], SHA_RE, "source_identity.start_ref", "a 40-character commit SHA")
        if c.require(identity, "end_ref", "source_identity.end_ref"):
            c.pattern(identity["end_ref"], SHA_RE, "source_identity.end_ref", "a 40-character commit SHA", nullable=True)
        if c.require(identity, "worktree_clean_at_end", "source_identity.worktree_clean_at_end"):
            value = identity["worktree_clean_at_end"]
            if value is not None:
                c.boolean(value, "source_identity.worktree_clean_at_end")
        if state == "final" and identity.get("end_ref") is None:
            c.error("RECEIPT_STATE_CONFLICT", "source_identity.end_ref", "a final receipt must record end_ref")

    skill = c.mapping(data, "skill_identity", "skill_identity")
    if skill is not None:
        if c.require(skill, "load_mode", "skill_identity.load_mode"):
            c.enum(skill["load_mode"], LOAD_MODES, "skill_identity.load_mode")
        if c.require(skill, "sensemaking_source_ref", "skill_identity.sensemaking_source_ref"):
            c.text(skill["sensemaking_source_ref"], "skill_identity.sensemaking_source_ref", MAX_LABEL, nullable=True)

    goal = c.mapping(data, "goal", "goal")
    if goal is not None:
        if c.require(goal, "statement", "goal.statement"):
            c.text(goal["statement"], "goal.statement")
        if c.require(goal, "source", "goal.source"):
            c.enum(goal["source"], GOAL_SOURCES, "goal.source")
        if c.require(goal, "source_ref", "goal.source_ref"):
            c.text(goal["source_ref"], "goal.source_ref", 200, nullable=True)

    delegation = c.mapping(data, "delegation", "delegation")
    if delegation is not None:
        granted = c.string_list(delegation.get("granted"), "delegation.granted", non_empty=True) \
            if c.require(delegation, "granted", "delegation.granted") else []
        withheld = c.string_list(delegation.get("withheld"), "delegation.withheld") \
            if c.require(delegation, "withheld", "delegation.withheld") else []
        for index, item in enumerate(granted):
            c.enum(item, AUTHORITY, f"delegation.granted[{index}]")
        for index, item in enumerate(withheld):
            c.enum(item, AUTHORITY, f"delegation.withheld[{index}]")
        overlap = sorted(set(granted) & set(withheld))
        if overlap:
            c.error("RECEIPT_AUTHORITY_OVERLAP", "delegation",
                    f"authority both granted and withheld: {', '.join(overlap)}")

    continuity = c.mapping(data, "continuity", "continuity")
    if continuity is not None:
        if c.require(continuity, "resumes", "continuity.resumes"):
            c.pattern(continuity["resumes"], SESSION_REF_RE, "continuity.resumes", "a session_ref", nullable=True)
        if c.require(continuity, "campaign_ref", "continuity.campaign_ref"):
            c.durable_ref(continuity["campaign_ref"], "continuity.campaign_ref", target_repo)
        if c.require(continuity, "resolves_questions", "continuity.resolves_questions"):
            refs = c.string_list(continuity["resolves_questions"], "continuity.resolves_questions")
            for index, ref in enumerate(refs):
                c.pattern(ref, QUALIFIED_QUESTION_RE, f"continuity.resolves_questions[{index}]",
                          "<session_ref>#Q-<n>")

    responsibilities = c.items(data, "responsibilities", "responsibilities")
    c.unique_ids(responsibilities, "R", "responsibilities")
    for index, entry in enumerate(responsibilities):
        if not isinstance(entry, dict):
            continue
        field = f"responsibilities[{index}]"
        if c.require(entry, "responsibility", f"{field}.responsibility"):
            c.text(entry["responsibility"], f"{field}.responsibility", MAX_LABEL)
        if c.require(entry, "capability", f"{field}.capability"):
            c.text(entry["capability"], f"{field}.capability", MAX_LABEL, nullable=True)
        if c.require(entry, "status", f"{field}.status"):
            c.enum(entry["status"], RESPONSIBILITY_STATUS, f"{field}.status")
            if state == "final" and entry["status"] == "in_progress":
                c.error("RECEIPT_STATE_CONFLICT", f"{field}.status",
                        "a final receipt cannot contain an in_progress responsibility")
        if c.require(entry, "reason", f"{field}.reason"):
            c.text(entry["reason"], f"{field}.reason")
        if c.require(entry, "artifact_refs", f"{field}.artifact_refs"):
            refs = c.string_list(entry["artifact_refs"], f"{field}.artifact_refs", 200)
            for ref_index, ref in enumerate(refs):
                c.durable_ref(ref, f"{field}.artifact_refs[{ref_index}]", target_repo, nullable=False)
        if c.require(entry, "validation", f"{field}.validation"):
            checks = entry["validation"]
            if not isinstance(checks, list):
                c.error("RECEIPT_TYPE", f"{field}.validation", "validation must be a list")
            else:
                for check_index, check in enumerate(checks):
                    check_field = f"{field}.validation[{check_index}]"
                    if not isinstance(check, dict):
                        c.error("RECEIPT_TYPE", check_field, f"{check_field} must be a mapping")
                        continue
                    if c.require(check, "command", f"{check_field}.command"):
                        c.text(check["command"], f"{check_field}.command", 200)
                    if c.require(check, "result", f"{check_field}.result"):
                        c.enum(check["result"], VALIDATION_RESULTS, f"{check_field}.result")

    findings = c.items(data, "findings", "findings")
    c.unique_ids(findings, "F", "findings")
    for index, entry in enumerate(findings):
        if not isinstance(entry, dict):
            continue
        field = f"findings[{index}]"
        if c.require(entry, "statement", f"{field}.statement"):
            c.text(entry["statement"], f"{field}.statement")
        if c.require(entry, "epistemic_status", f"{field}.epistemic_status"):
            c.enum(entry["epistemic_status"], EPISTEMIC_STATUS, f"{field}.epistemic_status")
        if c.require(entry, "evidence_refs", f"{field}.evidence_refs"):
            c.string_list(entry["evidence_refs"], f"{field}.evidence_refs", 200, non_empty=True)
        if c.require(entry, "disposition", f"{field}.disposition"):
            c.enum(entry["disposition"], FINDING_DISPOSITIONS, f"{field}.disposition")

    questions = c.items(data, "open_questions", "open_questions")
    question_ids = c.unique_ids(questions, "Q", "open_questions")
    blocking_owner_questions = 0
    for index, entry in enumerate(questions):
        if not isinstance(entry, dict):
            continue
        field = f"open_questions[{index}]"
        if c.require(entry, "question", f"{field}.question"):
            c.text(entry["question"], f"{field}.question")
        if c.require(entry, "source", f"{field}.source"):
            c.enum(entry["source"], UNCERTAINTY_SOURCES, f"{field}.source")
        if c.require(entry, "blocking", f"{field}.blocking"):
            c.boolean(entry["blocking"], f"{field}.blocking")
        if c.require(entry, "durable_ref", f"{field}.durable_ref"):
            c.durable_ref(entry["durable_ref"], f"{field}.durable_ref", target_repo)
        options = entry.get("options", [])
        if not isinstance(options, list):
            c.error("RECEIPT_TYPE", f"{field}.options", "options must be a list")
            options = []
        for option_index, option in enumerate(options):
            option_field = f"{field}.options[{option_index}]"
            if not isinstance(option, dict):
                c.error("RECEIPT_TYPE", option_field, f"{option_field} must be a mapping")
                continue
            if c.require(option, "option", f"{option_field}.option"):
                c.text(option["option"], f"{option_field}.option", MAX_LABEL)
            if c.require(option, "consequence", f"{option_field}.consequence"):
                c.text(option["consequence"], f"{option_field}.consequence")
        if entry.get("source") == "owner_intent":
            if len(options) < 2:
                c.error(
                    "RECEIPT_OWNER_QUESTION_OPTIONS", f"{field}.options",
                    "an owner_intent question needs at least two options, each stating its "
                    "consequence, so the owner can answer without reconstructing the session",
                )
            if entry.get("blocking") is True:
                blocking_owner_questions += 1

    stop = c.mapping(data, "stop", "stop")
    if stop is not None:
        disposition = stop.get("disposition")
        if c.require(stop, "disposition", "stop.disposition"):
            c.enum(disposition, STOP_DISPOSITIONS, "stop.disposition")
        if c.require(stop, "reason", "stop.reason"):
            c.text(stop["reason"], "stop.reason")
        if state == "final" and disposition == "IN_PROGRESS":
            c.error("RECEIPT_STATE_CONFLICT", "stop.disposition", "a final receipt needs a terminal stop disposition")
        if state == "in_progress" and disposition not in (None, "IN_PROGRESS"):
            c.error("RECEIPT_STATE_CONFLICT", "stop.disposition",
                    "an in_progress receipt must keep stop.disposition: IN_PROGRESS")
        if disposition == "OWNER_DECISION_REQUIRED" and blocking_owner_questions == 0:
            c.error(
                "RECEIPT_STOP_WITHOUT_QUESTION", "stop.disposition",
                "OWNER_DECISION_REQUIRED needs at least one blocking owner_intent question in "
                "open_questions; otherwise the decision is lost with the session",
            )

    upcoming = c.mapping(data, "next", "next")
    if upcoming is not None:
        if c.require(upcoming, "warranted_responsibility", "next.warranted_responsibility"):
            c.text(upcoming["warranted_responsibility"], "next.warranted_responsibility", nullable=True)
        if c.require(upcoming, "blocked_on", "next.blocked_on"):
            blockers = c.string_list(upcoming["blocked_on"], "next.blocked_on")
            for index, blocker in enumerate(blockers):
                field = f"next.blocked_on[{index}]"
                if blocker.startswith("authority:"):
                    c.enum(blocker.split(":", 1)[1], AUTHORITY, field)
                elif blocker not in question_ids:
                    c.error("RECEIPT_UNKNOWN_REF", field,
                            f"{blocker!r} is neither an open_questions id nor authority:<grant>")

    if c.require(data, "claim_ceiling", "claim_ceiling"):
        c.text(data["claim_ceiling"], "claim_ceiling")
    if data.get("action_authorized_by_receipt") is not False:
        c.error("RECEIPT_AUTHORITY_CLAIM", "action_authorized_by_receipt",
                "action_authorized_by_receipt must be false: a receipt records authority, it never grants it")


# -- semantic_query_receipt ------------------------------------------------

def _check_query(c: Checker, data: dict, target_repo: Path | None) -> None:
    modes = c.string_list(data.get("modes"), "modes", non_empty=True) if c.require(data, "modes", "modes") else []
    for index, mode in enumerate(modes):
        c.enum(mode, STEWARD_MODES, f"modes[{index}]")
    if len(set(modes)) != len(modes):
        c.error("RECEIPT_DUPLICATE_ID", "modes", "modes must not repeat")
    if c.require(data, "decision", "decision"):
        c.text(data["decision"], "decision")

    cli = c.mapping(data, "cli_identity", "cli_identity")
    if cli is not None:
        if c.require(cli, "sensemaking_source_ref", "cli_identity.sensemaking_source_ref"):
            c.text(cli["sensemaking_source_ref"], "cli_identity.sensemaking_source_ref", MAX_LABEL, nullable=True)
        if c.require(cli, "invocation_prefix", "cli_identity.invocation_prefix"):
            c.text(cli["invocation_prefix"], "cli_identity.invocation_prefix", 200)
        if c.require(cli, "version_output", "cli_identity.version_output"):
            c.text(cli["version_output"], "cli_identity.version_output", MAX_LABEL, nullable=True)

    index_info = c.mapping(data, "index", "index")
    if index_info is not None:
        if c.require(index_info, "indexed_ref", "index.indexed_ref"):
            c.pattern(index_info["indexed_ref"], SHA_RE, "index.indexed_ref", "a 40-character commit SHA", nullable=True)
        if c.require(index_info, "current_head", "index.current_head"):
            c.pattern(index_info["current_head"], SHA_RE, "index.current_head", "a 40-character commit SHA")
        for key in ("worktree_clean", "uncommitted_changes_not_indexed"):
            if c.require(index_info, key, f"index.{key}"):
                c.boolean(index_info[key], f"index.{key}")

    queries = c.items(data, "queries", "queries")
    query_ids = c.unique_ids(queries, "QY", "queries")
    outcomes: dict[str, str] = {}
    needs_miss: list[str] = []
    operations: list[str] = []
    for index, entry in enumerate(queries):
        if not isinstance(entry, dict):
            continue
        field = f"queries[{index}]"
        if c.require(entry, "operation", f"{field}.operation"):
            c.enum(entry["operation"], QUERY_OPERATIONS, f"{field}.operation")
            operations.append(entry["operation"])
        if c.require(entry, "terms", f"{field}.terms"):
            terms = c.string_list(entry["terms"], f"{field}.terms", 80)
            if len(terms) > 8:
                c.error("RECEIPT_FORMAT", f"{field}.terms", "at most 8 literal terms (the CLI's own limit)")
        if c.require(entry, "subject", f"{field}.subject"):
            c.text(entry["subject"], f"{field}.subject", MAX_LABEL, nullable=True)
        if c.require(entry, "expect_kinds", f"{field}.expect_kinds"):
            c.string_list(entry["expect_kinds"], f"{field}.expect_kinds")
        if c.require(entry, "target_ref", f"{field}.target_ref"):
            c.pattern(entry["target_ref"], SHA_RE, f"{field}.target_ref", "a 40-character commit SHA", nullable=True)
        result = c.mapping(entry, "result", f"{field}.result")
        if result is not None:
            if c.require(result, "hit_count", f"{field}.result.hit_count"):
                hits = result["hit_count"]
                if not isinstance(hits, int) or isinstance(hits, bool) or hits < 0:
                    c.error("RECEIPT_TYPE", f"{field}.result.hit_count", "hit_count must be a non-negative integer")
            for key in ("claim_ids", "not_assessed_kinds"):
                if c.require(result, key, f"{field}.result.{key}"):
                    c.string_list(result[key], f"{field}.result.{key}")
            if c.require(result, "truncated", f"{field}.result.truncated"):
                c.boolean(result["truncated"], f"{field}.result.truncated")
        if c.require(entry, "outcome", f"{field}.outcome"):
            c.enum(entry["outcome"], QUERY_OUTCOMES, f"{field}.outcome")
        if c.require(entry, "decision_relevant", f"{field}.decision_relevant"):
            c.boolean(entry["decision_relevant"], f"{field}.decision_relevant")
        entry_id = entry.get("id")
        if isinstance(entry_id, str):
            outcomes[entry_id] = entry.get("outcome")
            if entry.get("decision_relevant") is True and entry.get("outcome") in ("MISS", "NOT_ASSESSED"):
                needs_miss.append(entry_id)

    if "RECALL" in modes and not queries:
        c.error("RECEIPT_MODE_EVIDENCE", "queries", "RECALL mode requires at least one recorded query")
    if "AUDIT" in modes and "audit" not in operations:
        c.error("RECEIPT_MODE_EVIDENCE", "queries", "AUDIT mode requires a recorded audit operation")

    checks = c.items(data, "source_checks", "source_checks")
    for index, entry in enumerate(checks):
        field = f"source_checks[{index}]"
        if not isinstance(entry, dict):
            c.error("RECEIPT_TYPE", field, f"{field} must be a mapping")
            continue
        if c.require(entry, "claim_id", f"{field}.claim_id"):
            c.text(entry["claim_id"], f"{field}.claim_id", MAX_LABEL)
        if c.require(entry, "sources", f"{field}.sources"):
            c.string_list(entry["sources"], f"{field}.sources", 200, non_empty=True)
        if c.require(entry, "result", f"{field}.result"):
            c.enum(entry["result"], SOURCE_CHECK_RESULTS, f"{field}.result")

    misses = c.items(data, "misses", "misses")
    c.unique_ids(misses, "M", "misses")
    recorded_for: set[str] = set()
    for index, entry in enumerate(misses):
        if not isinstance(entry, dict):
            continue
        field = f"misses[{index}]"
        query_ref = entry.get("query_ref")
        if c.require(entry, "query_ref", f"{field}.query_ref"):
            if query_ref not in query_ids:
                c.error("RECEIPT_UNKNOWN_REF", f"{field}.query_ref", f"query_ref {query_ref!r} is not a recorded query id")
            elif outcomes.get(query_ref) in ("HIT", "NOT_APPLICABLE"):
                c.error("RECEIPT_MISS_QUERY_OUTCOME", f"{field}.query_ref",
                        f"{query_ref} has outcome {outcomes.get(query_ref)}; a miss must reference a MISS, NOT_ASSESSED or PARTIAL query")
            else:
                recorded_for.add(query_ref)
        if c.require(entry, "needed_for", f"{field}.needed_for"):
            c.text(entry["needed_for"], f"{field}.needed_for")
        if c.require(entry, "kind", f"{field}.kind"):
            c.enum(entry["kind"], MISS_KINDS, f"{field}.kind")
        if c.require(entry, "resolved_by", f"{field}.resolved_by"):
            c.text(entry["resolved_by"], f"{field}.resolved_by", nullable=True)
        follow_up = entry.get("follow_up")
        if c.require(entry, "follow_up", f"{field}.follow_up"):
            c.enum(follow_up, MISS_FOLLOW_UPS, f"{field}.follow_up")
        if c.require(entry, "proposal_ref", f"{field}.proposal_ref"):
            c.durable_ref(entry["proposal_ref"], f"{field}.proposal_ref", target_repo)
            if follow_up in ("ADD_PROPOSED", "ADDED") and entry["proposal_ref"] is None:
                c.error("RECEIPT_MISSING_FIELD", f"{field}.proposal_ref",
                        f"follow_up {follow_up} requires proposal_ref to the drafted or added knowledge file")

    for query_id in needs_miss:
        if query_id not in recorded_for:
            c.error(
                "RECEIPT_MISS_NOT_RECORDED", "misses",
                f"{query_id} is decision-relevant with outcome {outcomes[query_id]} but no misses "
                "entry records what was needed and how it was resolved; negative knowledge must "
                "survive the session",
            )

    reconcile = c.items(data, "reconcile", "reconcile")
    for index, entry in enumerate(reconcile):
        field = f"reconcile[{index}]"
        if not isinstance(entry, dict):
            c.error("RECEIPT_TYPE", field, f"{field} must be a mapping")
            continue
        disposition = entry.get("disposition")
        if c.require(entry, "disposition", f"{field}.disposition"):
            c.enum(disposition, RECONCILE_DISPOSITIONS, f"{field}.disposition")
        if c.require(entry, "claim_id", f"{field}.claim_id"):
            c.text(entry["claim_id"], f"{field}.claim_id", MAX_LABEL, nullable=disposition == "NO_MODEL_CHANGE")
        if c.require(entry, "applied", f"{field}.applied"):
            c.boolean(entry["applied"], f"{field}.applied")
        if c.require(entry, "proposal_ref", f"{field}.proposal_ref"):
            c.durable_ref(entry["proposal_ref"], f"{field}.proposal_ref", target_repo)
        if c.require(entry, "proposal_check", f"{field}.proposal_check"):
            c.enum(entry["proposal_check"], PROPOSAL_CHECK_RESULTS, f"{field}.proposal_check")
    if "RECONCILE" in modes and not reconcile:
        c.error("RECEIPT_MODE_EVIDENCE", "reconcile",
                "RECONCILE mode requires at least one disposition (NO_MODEL_CHANGE is a valid one)")

    for key in ("action_authorized", "semantic_truth_established"):
        if data.get(key) is not False:
            c.error("RECEIPT_AUTHORITY_CLAIM", key, f"{key} must be false: a query receipt records retrieval, not truth or permission")


# -- entry points ----------------------------------------------------------

def load_receipt(path: Path) -> tuple[dict | None, str | None]:
    """Load a receipt file; tolerate the fixture harness's frontmatter convention."""
    if not path.is_file():
        return None, f"receipt file not found: {path}"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"unreadable: {exc}"
    body = FRONTMATTER_RE.sub("", text, count=1)
    try:
        data = yaml.safe_load(body)
    except yaml.YAMLError as exc:
        return None, f"invalid YAML: {exc}"
    if not isinstance(data, dict):
        return None, "receipt is not a YAML mapping"
    return data, None


def validate_receipt(path: Path, target_repo: Path | None = None) -> tuple[str | None, Checker]:
    c = Checker()
    data, problem = load_receipt(path)
    if data is None:
        code = "RECEIPT_NOT_FOUND" if problem and problem.startswith("receipt file not found") else "RECEIPT_PARSE_ERROR"
        c.error(code, "receipt", problem or "unreadable receipt")
        return None, c
    artifact_id = data.get("artifact_id")
    if artifact_id not in RECEIPT_ARTIFACT_IDS:
        c.error("RECEIPT_ARTIFACT_ID", "artifact_id",
                f"artifact_id must be one of {', '.join(RECEIPT_ARTIFACT_IDS)}; got {artifact_id!r}")
        return None, c
    _check_envelope(c, data, artifact_id, path)
    if artifact_id == SESSION_RECEIPT_ID:
        _check_session(c, data, target_repo)
    else:
        _check_query(c, data, target_repo)
    try:
        line_count = len(path.read_text(encoding="utf-8").splitlines())
    except OSError:
        line_count = 0
    if line_count > MAX_LINES:
        c.warn("RECEIPT_LARGE", "receipt",
               f"receipt has {line_count} lines (soft limit {MAX_LINES}); keep receipts to pointers and facts")
    return artifact_id, c


def _ascii(text: str) -> str:
    return text.encode("ascii", "replace").decode("ascii")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate a Sensemaking session or semantic query receipt")
    parser.add_argument("artifact_path", help="Path to the receipt YAML (or a frontmatter-prefixed fixture)")
    parser.add_argument("--repo-root", default=".", help="Framework root (harness/router contract; unused)")
    parser.add_argument("--target-repo", default=None,
                        help="Repository the receipt describes; when given, referenced paths must exist there")
    parser.add_argument("--json", action="store_true", help="Emit the router's JSON result envelope")
    args = parser.parse_args(argv)

    path = Path(args.artifact_path)
    target = Path(args.target_repo).resolve() if args.target_repo else None
    artifact_id, checker = validate_receipt(path, target)

    if args.json:
        payload = {
            "valid": checker.valid,
            "artifact_id": artifact_id or "unknown",
            "artifact_path": str(path.resolve()),
            "validator": "validate-receipt.py",
            "errors": [
                {
                    "error_id": f"{artifact_id or 'unknown'}.{f['field']}.{f['code'].lower()}",
                    "error_type": f["code"],
                    "field": f["field"],
                    "severity": f["severity"],
                    "message": f["message"],
                    "reference": "skills/using-sensemaking/references/session-receipt-v1.md",
                }
                for f in checker.findings
            ],
        }
        print(_ascii(json.dumps(payload, indent=2)))
    else:
        for finding in checker.findings:
            label = "WARN " if finding["severity"] == "warning" else ""
            print(_ascii(f"{label}[{finding['code']}] {finding['field']}: {finding['message']}"))
        print("RECEIPT_VALID" if checker.valid else "RECEIPT_INVALID")
    return 0 if checker.valid else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
