"""Deterministic validation of the Stage 1 auteur post-remediation preparation package.

These tests verify that the preparation package is internally consistent and
that it cannot silently drift into something that looks like a completed run.

They are deliberately offline and side-effect free: they read repository files
only. They never invoke a model, never run the Stage 1 workflow, and never
create an evidence directory.
"""

import re
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = REPO_ROOT / "docs" / "experiments" / "STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md"
CHECKLIST_PATH = REPO_ROOT / "docs" / "experiments" / "GATE-D-STALE-DIAGNOSIS-CHECKLIST.md"

EVIDENCE_0015_DIR = "experiments/evidence/0015-stage1-auteur-controlled-learning-attempt"
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")

REQUIRED_GATES = [
    "Gate A - Invocation integrity",
    "Gate B - Structural validation",
    "Gate C - Safety",
    "Gate D - Substantive audit",
    "Gate E - Human usefulness",
    "Gate F - Campaign interpretation",
]

REQUIRED_RESULTS = [
    "SUCCESSFUL_CONTROLLED_EVIDENCE",
    "STRUCTURAL_FAILURE",
    "SUBSTANTIVE_FAILURE",
    "SAFETY_FAILURE",
    "INCONCLUSIVE",
]


def _load_contract():
    text = PACKAGE_PATH.read_text(encoding="utf-8")
    blocks = re.findall(r"```yaml\n(.*?)```", text, re.DOTALL)
    if not blocks:
        raise AssertionError("no ```yaml contract block found in the preparation package")
    return yaml.safe_load(blocks[0]), text


class PreparationPackageStructure(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_package_and_checklist_exist(self):
        self.assertTrue(PACKAGE_PATH.is_file())
        self.assertTrue(CHECKLIST_PATH.is_file())

    def test_status_is_prepared_not_run(self):
        self.assertEqual(self.contract["package_status"], "PREPARED_NOT_RUN")
        self.assertIn("PREPARED_NOT_RUN", self.text)

    def test_no_ambiguous_single_framework_sha_field(self):
        """The ambiguous single pin was split; it must not come back."""
        self.assertNotIn(
            "framework_sha",
            [k for k in self.contract if k == "framework_sha"],
            "framework_sha is ambiguous; use runtime_baseline_sha + execution_framework_sha",
        )

    def test_target_sha_present_and_full_length(self):
        self.assertTrue(FULL_SHA.match(str(self.contract["target_sha"])))

    def test_artifact_type_is_repository_sensemaking_brief(self):
        self.assertEqual(self.contract["artifact_type"], "repository_sensemaking_brief")

    def test_exact_model_specified(self):
        self.assertEqual(self.contract["exact_model"], "claude-sonnet-5")


class EvidenceNumbering(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_evidence_number_is_unused_on_disk(self):
        number = self.contract["evidence_number"]
        existing = [p.name for p in (REPO_ROOT / "experiments" / "evidence").iterdir() if p.is_dir()]
        for name in existing:
            self.assertFalse(
                name.startswith(f"{number}-"),
                f"evidence number {number} is already used by {name}",
            )

    def test_planned_evidence_directory_was_not_created(self):
        planned = REPO_ROOT / self.contract["evidence_directory_planned"]
        self.assertFalse(
            planned.exists(),
            "preparation must not create the live evidence directory",
        )
        self.assertFalse(self.contract["evidence_directory_created"])

    def test_slug_matches_number(self):
        self.assertTrue(
            self.contract["evidence_slug"].startswith(self.contract["evidence_number"] + "-")
        )


class HistoricalEvidenceImmutability(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_evidence_0015_not_used_as_new_output_path(self):
        for key in ("expected_output_path", "expected_run_log_path", "evidence_directory_planned"):
            value = str(self.contract[key]).replace("\\", "/")
            self.assertNotIn(
                EVIDENCE_0015_DIR,
                value,
                f"{key} must not point into historical Evidence 0015",
            )
            self.assertNotIn("0015", value, f"{key} must not reference evidence 0015")

    def test_evidence_0015_declared_immutable_and_not_reclassified(self):
        hist = self.contract["historical_evidence_0015"]
        self.assertTrue(hist["immutable"])
        self.assertFalse(hist["usable_as_new_output_path"])
        self.assertFalse(hist["usable_as_input_artifact"])
        self.assertFalse(hist["reclassified_by_this_package"])
        self.assertEqual(hist["classification"], "STAGE 1 FAIL")

    def test_evidence_0015_directory_still_present(self):
        self.assertTrue((REPO_ROOT / EVIDENCE_0015_DIR).is_dir())


class InvocationAndSafetyRules(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_one_invocation_rule(self):
        self.assertEqual(self.contract["invocation_count_allowed"], 1)

    def test_no_fallback_or_substitution(self):
        self.assertFalse(self.contract["model_fallback_allowed"])
        self.assertFalse(self.contract["model_substitution_allowed"])

    def test_no_automatic_retry_or_repair(self):
        self.assertFalse(self.contract["automatic_retry_allowed"])
        self.assertFalse(self.contract["automatic_repair_allowed"])
        self.assertFalse(self.contract["manual_artifact_repair_allowed"])

    def test_no_target_mutation(self):
        self.assertFalse(self.contract["target_mutation_allowed"])

    def test_second_attempt_requires_owner_decision(self):
        self.assertTrue(self.contract["second_attempt_requires_new_owner_decision"])

    def test_stop_on_first_failed_gate(self):
        self.assertTrue(self.contract["stop_on_first_failed_gate"])


class RootsAndPaths(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def _norm(self, value):
        return str(value).replace("\\", "/").rstrip("/")

    def test_framework_and_target_roots_differ(self):
        self.assertNotEqual(
            self._norm(self.contract["framework_root"]),
            self._norm(self.contract["target_root"]),
        )

    def test_output_and_log_paths_are_not_under_target_root(self):
        target = self._norm(self.contract["target_root"]) + "/"
        for key in ("expected_output_path", "expected_run_log_path"):
            self.assertFalse(
                self._norm(self.contract[key]).startswith(target),
                f"{key} must not live under the target root",
            )

    def test_output_path_is_under_an_authorized_location(self):
        out = self._norm(self.contract["expected_output_path"])
        framework = self._norm(self.contract["framework_root"]) + "/"
        self.assertTrue(out.startswith(framework))
        self.assertTrue(out.endswith("repository_sensemaking_brief.md"))

    def test_log_path_is_outside_both_repositories_or_under_framework(self):
        log = self._norm(self.contract["expected_run_log_path"])
        self.assertNotIn("/target-auteur/", log)
        self.assertTrue(log.endswith(".md"))


class GatesAndTripwires(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_all_six_gates_present(self):
        self.assertEqual(self.contract["gates"], REQUIRED_GATES)

    def test_all_eight_tripwires_present(self):
        tripwires = self.contract["stale_diagnosis_tripwires"]
        self.assertEqual(len(tripwires), 8)
        for index in range(1, 9):
            self.assertTrue(
                any(t.startswith(f"T{index} ") for t in tripwires),
                f"tripwire T{index} missing",
            )

    def test_tripwires_also_present_in_reviewer_checklist(self):
        checklist = CHECKLIST_PATH.read_text(encoding="utf-8")
        for index in range(1, 9):
            self.assertIn(f"| T{index} |", checklist)

    def test_checklist_is_marked_prepared_not_run(self):
        self.assertIn("PREPARED_NOT_RUN", CHECKLIST_PATH.read_text(encoding="utf-8"))

    def test_contradiction_search_paths_declared(self):
        paths = self.contract["contradiction_search_paths"]
        for expected in (
            "src/auteur/series/universe_advisory.py",
            "src/auteur/series/handlers.py",
            "src/auteur/universe/models.py",
            "tests/test_series_universe_integration.py",
        ):
            self.assertIn(expected, paths)

    def test_campaign_results_are_exactly_the_permitted_five(self):
        self.assertEqual(self.contract["campaign_results_permitted"], REQUIRED_RESULTS)


class ReadinessAndCampaignBoundaries(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_readiness_cannot_be_auto_promoted(self):
        self.assertFalse(self.contract["readiness_auto_promotion_allowed"])
        self.assertEqual(self.contract["readiness_classification_before"], "Externally exercised")

    def test_second_structurally_different_target_still_required(self):
        self.assertTrue(self.contract["second_structurally_different_target_required"])


class NoFabricatedRunOutput(unittest.TestCase):
    """The package must not look like, or contain, a completed run."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    def test_no_completed_gate_verdicts(self):
        forbidden = [
            "Gate A result: PASS",
            "Gate B result: PASS",
            "Gate C result: PASS",
            "Gate D result: PASS",
            "Gate E result: PASS",
            "Gate F result: PASS",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, self.text)
            self.assertNotIn(phrase, CHECKLIST_PATH.read_text(encoding="utf-8"))

    def test_no_run_classification_claimed(self):
        for phrase in ("STAGE 1 PASS", "Stage 1 was invoked", "run completed"):
            self.assertNotIn(phrase, self.text)

    def test_owner_authorization_block_is_blank(self):
        self.assertIn("Authorized by:\n", self.text)
        self.assertIn("NOT AUTHORIZED", self.text)

    def test_no_live_evidence_files_produced(self):
        planned = REPO_ROOT / self.contract["evidence_directory_planned"]
        self.assertFalse(planned.exists())
        for name in ("repository_sensemaking_brief.md", "workflow_summary.json", "tool-call-trace.jsonl"):
            self.assertFalse(
                (PACKAGE_PATH.parent / name).exists(),
                f"preparation must not emit {name}",
            )


SENTINEL = "PENDING_POST_MERGE_PIN_FINALIZATION"
RUNTIME_BASELINE_SHA = "1761e42f6786af422e05e128bb6608d33854f1f3"

# Paths that must exist at whatever commit is eventually chosen as the
# execution pin. Used both as a contract assertion and by the finalized-pin
# fixture below.
REQUIRED_PATHS_AT_EXECUTION_PIN = [
    "docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md",
    "docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md",
    "tests/test_stage1_auteur_prep_package.py",
    "scripts/validate-brief.py",
]

# Preparation artifacts that provably do NOT exist at the runtime baseline.
PREP_ARTIFACTS = [
    "docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md",
    "docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md",
    "tests/test_stage1_auteur_prep_package.py",
]


def _git_ls_tree(sha):
    """List tracked paths at `sha` using ONLY local history. No network.

    Returns None when the object is not present locally (e.g. a shallow CI
    clone), so callers can skip rather than fail or reach for the network.
    """
    import subprocess

    try:
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", sha],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return set(result.stdout.splitlines())


def paths_missing_at_revision(sha, required_paths):
    """Validator helper: which required paths are absent at `sha`.

    A future pin-finalization task supplies a real finalized SHA here; every
    required path must come back present, otherwise the pin is unusable and
    preflight must stop before the model is invoked.
    """
    tree = _git_ls_tree(sha)
    if tree is None:
        return None
    return [p for p in required_paths if p not in tree]


class FrameworkPinLifecycle(unittest.TestCase):
    """The two-phase pin lifecycle: runtime baseline vs execution pin."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 1
    def test_runtime_baseline_sha_is_full_sha(self):
        self.assertTrue(FULL_SHA.match(str(self.contract["runtime_baseline_sha"])))
        self.assertEqual(self.contract["runtime_baseline_sha"], RUNTIME_BASELINE_SHA)

    # 2
    def test_execution_framework_sha_is_explicitly_pending(self):
        self.assertEqual(self.contract["execution_framework_sha"], SENTINEL)
        self.assertFalse(
            FULL_SHA.match(str(self.contract["execution_framework_sha"])),
            "the sentinel must not look like a SHA",
        )
        self.assertTrue(self.contract["pin_finalization_required"])

    # 3
    def test_pending_execution_pin_blocks_authorization(self):
        self.assertEqual(self.contract["execution_authorization_status"], "NOT_AUTHORIZED")
        self.assertFalse(self.contract["package_runnable"])
        # Round 7: stated in plainly negative active form. Round 6 wrote this
        # as "is blocked procedurally", which needed a guard carve-out to stay
        # legal; the carve-out proved bypassable, so the sentence was rewritten
        # instead. "remains non-runnable" contains no enforcement participle
        # and so needs no exception at all.
        self.assertIn(
            "The run remains non-runnable while execution_framework_sha is unset",
            self.text,
        )
        self.assertNotIn("blocked procedurally", self.text)

    # 4
    def test_runtime_baseline_is_not_treated_as_execution_pin(self):
        self.assertFalse(self.contract["runtime_baseline_is_execution_pin"])
        self.assertEqual(self.contract["framework_root_checkout_pin"], "execution_framework_sha")

    # 5
    def test_package_states_baseline_lacks_preparation_artifacts(self):
        self.assertFalse(self.contract["runtime_baseline_contains_preparation_package"])
        self.assertFalse(self.contract["runtime_baseline_contains_gate_d_checklist"])
        self.assertFalse(self.contract["runtime_baseline_contains_package_validation_tests"])
        self.assertIn("does NOT contain the preparation package", self.text)

    # 6
    def test_post_merge_pin_finalization_step_required(self):
        self.assertFalse(self.contract["merging_this_pr_finalizes_pin"])
        self.assertIn("Post-merge pin-finalization procedure", self.text)

    # 7
    def test_separate_run_authorization_step_required(self):
        self.assertTrue(self.contract["separate_run_authorization_task_required"])
        self.assertIn("Pin finalization is not authorization.", self.text)

    # 8
    def test_merging_pr_107_does_not_authorize_execution(self):
        self.assertFalse(self.contract["merging_this_pr_authorizes_execution"])
        self.assertIn("Merging PR #107 does NOT authorize execution.", self.text)

    # 9
    def test_framework_root_must_use_finalized_execution_pin(self):
        self.assertIn(
            "fresh disposable clone of the framework at the finalized execution_framework_sha, detached",
            self.contract["isolation_requirements"],
        )

    # 10
    def test_required_paths_declared_for_execution_pin(self):
        declared = self.contract["required_paths_at_execution_framework_sha"]
        for path in REQUIRED_PATHS_AT_EXECUTION_PIN:
            self.assertIn(path, declared)

    # 11
    def test_missing_paths_cause_preflight_failure_before_invocation(self):
        self.assertTrue(self.contract["missing_required_path_is_gate_a_failure"])
        self.assertIn("Otherwise stop without invoking the model.", self.text)
        self.assertIn("A missing required path is a **Gate A failure**", self.text)

    # 12
    def test_floating_branch_refs_are_prohibited(self):
        prohibited = self.contract["floating_refs_prohibited_as_execution_pin"]
        for ref in ("main", "origin/main", "HEAD"):
            self.assertIn(ref, prohibited)
        self.assertNotIn(str(self.contract["execution_framework_sha"]), prohibited)

    # 13
    def test_authorization_block_remains_unfilled(self):
        self.assertIn("Authorized execution framework SHA:\n", self.text)
        self.assertIn("Authorized by:\n", self.text)
        self.assertFalse(self.contract["execution_authorization_record_exists"])

    # 14
    def test_sentinel_cannot_pass_executable_package_validator(self):
        """A sentinel must fail any check that demands a real immutable pin."""
        self.assertFalse(_is_executable_pin(self.contract["execution_framework_sha"]))
        self.assertTrue(_is_executable_pin(RUNTIME_BASELINE_SHA))

    # 15
    def test_package_cannot_be_runnable_while_sentinel_present(self):
        if self.contract["execution_framework_sha"] == SENTINEL:
            self.assertFalse(self.contract["package_runnable"])
            self.assertEqual(self.contract["execution_authorization_status"], "NOT_AUTHORIZED")

    # 16
    def test_gate_d_checklist_cannot_come_from_undocumented_external_path(self):
        self.assertFalse(self.contract["external_checklist_copy_allowed"])
        self.assertIn(
            "docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md",
            self.contract["required_paths_at_execution_framework_sha"],
        )
        checklist = CHECKLIST_PATH.read_text(encoding="utf-8")
        self.assertIn("not from an external or", checklist)

    # 17
    def test_lifecycle_fields_agree_across_both_documents(self):
        checklist = CHECKLIST_PATH.read_text(encoding="utf-8")
        pointer = (
            REPO_ROOT / "docs" / "experiments" / "STAGE-1-AUTEUR-EXECUTION-PACKAGE.md"
        ).read_text(encoding="utf-8")
        for document in (checklist, pointer):
            self.assertIn(SENTINEL, document)
            self.assertIn(RUNTIME_BASELINE_SHA, document)
        self.assertIn(str(self.contract["target_sha"]), checklist)
        self.assertIn(str(self.contract["target_main_sha_observed"]), checklist)


class AuteurTargetMovement(unittest.TestCase):
    def setUp(self):
        self.contract, self.text = _load_contract()

    # 18
    def test_movement_wording_does_not_claim_main_unchanged(self):
        for document in (self.text, CHECKLIST_PATH.read_text(encoding="utf-8")):
            self.assertNotIn("has NOT moved", document)
            self.assertNotIn("has not moved", document)
            self.assertIn("Auteur main has moved beyond the selected target pin", document)
        self.assertTrue(self.contract["target_main_has_moved_beyond_target_sha"])

    # 19
    def test_selected_target_remains_immutable_full_sha(self):
        self.assertTrue(FULL_SHA.match(str(self.contract["target_sha"])))
        self.assertEqual(
            self.contract["target_sha"], "0653defb05625f2fcde0ac32eac6e59ccf7eeb90"
        )
        self.assertTrue(self.contract["target_pin_deliberately_retained"])

    # 20
    def test_newer_main_sha_and_retention_rationale_documented(self):
        observed = str(self.contract["target_main_sha_observed"])
        self.assertTrue(FULL_SHA.match(observed))
        self.assertNotEqual(observed, self.contract["target_sha"])
        commits = self.contract["target_intervening_commits"]
        self.assertEqual(len(commits), 1)
        entry = commits[0]
        self.assertEqual(entry["sha"], observed)
        self.assertTrue(entry["documentation_only"])
        self.assertFalse(entry["touches_pinned_advisory_implementation"])
        self.assertFalse(entry["touches_pinned_test_surface"])
        self.assertIn("comparability with the completed #38 audit", self.text)


def _is_executable_pin(value):
    """Only a full 40-hex SHA may serve as an execution pin."""
    return bool(FULL_SHA.match(str(value)))


class RuntimeBaselineProvablyLacksPreparationArtifacts(unittest.TestCase):
    """Pin the precise reason the baseline cannot be the execution revision.

    Uses local git history only -- never the network. Skips when the object is
    unavailable locally (shallow clone) rather than failing spuriously.
    """

    def test_preparation_files_absent_at_runtime_baseline(self):
        tree = _git_ls_tree(RUNTIME_BASELINE_SHA)
        if tree is None:
            self.skipTest(
                f"runtime baseline {RUNTIME_BASELINE_SHA} not present in local history"
            )
        for path in PREP_ARTIFACTS:
            self.assertNotIn(
                path,
                tree,
                f"{path} unexpectedly exists at the runtime baseline; "
                "the package's justification for splitting the pin would be false",
            )

    def test_runtime_fix_surface_present_at_runtime_baseline(self):
        tree = _git_ls_tree(RUNTIME_BASELINE_SHA)
        if tree is None:
            self.skipTest("runtime baseline not present in local history")
        self.assertIn("scripts/validate-brief.py", tree)


class FinalizedPinFixture(unittest.TestCase):
    """Proves the check a future pin-finalization task must satisfy.

    Once a finalized SHA is supplied, every required path must exist at that
    commit. HEAD stands in here as a commit that already carries the
    preparation package, demonstrating the helper accepts a valid pin and
    rejects one missing the artifacts.
    """

    def test_helper_accepts_a_revision_containing_all_required_paths(self):
        missing = paths_missing_at_revision("HEAD", REQUIRED_PATHS_AT_EXECUTION_PIN)
        if missing is None:
            self.skipTest("git history unavailable")
        self.assertEqual(
            missing, [], f"required paths missing at HEAD: {missing}"
        )

    def test_helper_rejects_the_runtime_baseline_as_a_finalized_pin(self):
        missing = paths_missing_at_revision(
            RUNTIME_BASELINE_SHA, REQUIRED_PATHS_AT_EXECUTION_PIN
        )
        if missing is None:
            self.skipTest("runtime baseline not present in local history")
        self.assertTrue(
            missing,
            "the runtime baseline must NOT satisfy the finalized-pin path check",
        )
        for path in PREP_ARTIFACTS:
            self.assertIn(path, missing)


# ---------------------------------------------------------------------------
# Authorization-record integrity
#
# The package previously offered a FORK: the authorization record could either
# exist at the pinned framework revision, or be copied somewhere with a
# self-recorded digest. Branch one is impossible (the record is authored after
# the revision it pins); branch two authenticated nothing. Both are gone. The
# tests below pin the single mandatory owner-approved mechanism that replaced
# them, and the Gate A verification that a future consumer must perform before
# invocation (no such consumer exists today).
# ---------------------------------------------------------------------------

RUN_CONTROL_DIR = (
    "experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt"
)
AUTH_RECORD_PATH = f"{RUN_CONTROL_DIR}/authorization-record.yaml"
AUTH_DIGEST_PATH = f"{RUN_CONTROL_DIR}/authorization-record.sha256"
OWNER_APPROVAL_PATH = f"{RUN_CONTROL_DIR}/owner-approval.md"

RUN_CONTROL_SENTINEL = "PENDING_AUTHORIZATION_RECORD_CREATION"
OWNER_APPROVAL_SENTINEL = "PENDING_OWNER_APPROVAL"
ALL_SENTINELS = [SENTINEL, RUN_CONTROL_SENTINEL, OWNER_APPROVAL_SENTINEL]

AUTH_STATUS = "AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

CANONICAL_PACKAGE_PATH = "docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md"
CANONICAL_CHECKLIST_PATH = "docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md"

AUTH_RECORD_REQUIRED_FIELDS = [
    "schema_version",
    "authorization_status",
    "authorization_scope",
    "evidence_number",
    "evidence_slug",
    "execution_framework_sha",
    "target_repository",
    "target_sha",
    "exact_model",
    "artifact_type",
    "preparation_package_path",
    "preparation_package_sha256",
    "gate_d_checklist_path",
    "gate_d_checklist_sha256",
    "authorization_record_created_at",
    "authorization_record_created_by",
    "owner_approval_reference",
    "one_invocation_only",
    "no_retry",
    "no_fallback",
    "no_model_substitution",
    "no_artifact_repair",
    "no_target_mutation",
    "stop_on_first_failed_gate",
]

AUTH_RECORD_TRUE_FLAGS = [
    "one_invocation_only",
    "no_retry",
    "no_fallback",
    "no_model_substitution",
    "no_artifact_repair",
    "no_target_mutation",
    "stop_on_first_failed_gate",
]

OWNER_APPROVAL_REQUIRED_FIELDS = [
    "approver_github_identity",
    "approval_timestamp",
    "authorization_record_sha256",
    "execution_framework_sha",
    "target_sha",
    "evidence_number",
    "evidence_slug",
    "exact_model",
    "authorization_decision",
    "no_retry_statement",
    "owner_decision_reference",
]

# Phrases that would reintroduce an optional/forked authorization provenance.
FORK_PHRASES = [
    "must itself exist at the pinned framework revision",
    "may exist at the pinned revision",
    "may be copied",
    "one of the following",
]


def validate_future_authorization_record(record, expected):
    """Validator for a FUTURE Evidence 0016 authorization record.

    Returns a list of error strings; empty means the record would be accepted.
    Used only against synthetic in-test fixtures -- the real record does not
    exist and must not be created by this PR.
    """
    errors = []
    if not isinstance(record, dict):
        return ["record is not a mapping"]

    for field in AUTH_RECORD_REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"missing field: {field}")
        elif record[field] is None or record[field] == "":
            errors.append(f"blank field: {field}")

    if record.get("authorization_status") != AUTH_STATUS:
        errors.append("authorization_status is not the exact required string")

    for field in ("execution_framework_sha", "target_sha"):
        if field in record and not FULL_SHA.match(str(record[field])):
            errors.append(f"{field} is not a full 40-character lowercase SHA")

    for field in ("preparation_package_sha256", "gate_d_checklist_sha256"):
        if field in record and not HEX64.match(str(record[field])):
            errors.append(f"{field} is not 64 lowercase hex characters")

    for flag in AUTH_RECORD_TRUE_FLAGS:
        if record.get(flag) is not True:
            errors.append(f"safety flag not true: {flag}")

    if record.get("preparation_package_path") != CANONICAL_PACKAGE_PATH:
        errors.append("preparation_package_path is not the canonical path")
    if record.get("gate_d_checklist_path") != CANONICAL_CHECKLIST_PATH:
        errors.append("gate_d_checklist_path is not the canonical path")

    for field in (
        "execution_framework_sha",
        "target_sha",
        "target_repository",
        "evidence_number",
        "evidence_slug",
        "exact_model",
        "artifact_type",
    ):
        if field in expected and str(record.get(field)) != str(expected[field]):
            errors.append(f"{field} does not match the expected authorized value")

    # A record may never be its own authority.
    if not record.get("owner_approval_reference"):
        errors.append("owner_approval_reference missing: record cannot self-approve")

    return errors


EXPECTED_AUTHORIZED_INPUTS = {
    "execution_framework_sha": "a" * 40,
    "target_sha": "0653defb05625f2fcde0ac32eac6e59ccf7eeb90",
    "target_repository": "https://github.com/ThorStarlord/auteur.git",
    "evidence_number": "0016",
    "evidence_slug": "0016-stage1-auteur-post-remediation-controlled-attempt",
    "exact_model": "claude-sonnet-5",
    "artifact_type": "repository_sensemaking_brief",
}


def valid_future_authorization_record():
    """A synthetic, obviously-fake but structurally valid future record."""
    return {
        "schema_version": "1",
        "authorization_status": AUTH_STATUS,
        "authorization_scope": "single controlled Stage 1 invocation, Evidence 0016",
        "evidence_number": "0016",
        "evidence_slug": "0016-stage1-auteur-post-remediation-controlled-attempt",
        "execution_framework_sha": "a" * 40,
        "target_repository": "https://github.com/ThorStarlord/auteur.git",
        "target_sha": "0653defb05625f2fcde0ac32eac6e59ccf7eeb90",
        "exact_model": "claude-sonnet-5",
        "artifact_type": "repository_sensemaking_brief",
        "preparation_package_path": CANONICAL_PACKAGE_PATH,
        "preparation_package_sha256": "b" * 64,
        "gate_d_checklist_path": CANONICAL_CHECKLIST_PATH,
        "gate_d_checklist_sha256": "c" * 64,
        "authorization_record_created_at": "2026-01-01T00:00:00Z",
        "authorization_record_created_by": "synthetic-fixture-author",
        "owner_approval_reference": OWNER_APPROVAL_PATH,
        "one_invocation_only": True,
        "no_retry": True,
        "no_fallback": True,
        "no_model_substitution": True,
        "no_artifact_repair": True,
        "no_target_mutation": True,
        "stop_on_first_failed_gate": True,
    }


class AuthorizationMechanismIsSingular(unittest.TestCase):
    """1-6, 45: exactly one mechanism, explicit paths, no fork."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 1
    def test_no_authorization_mechanism_fork_remains(self):
        self.assertFalse(self.contract["authorization_mechanism_alternatives_allowed"])
        self.assertEqual(self.contract["authorization_mechanism_count"], 1)
        self.assertEqual(
            self.contract["authorization_mechanism"],
            "owner_approved_external_immutable_authorization_record",
        )
        self.assertEqual(
            self.contract["pin_finalization_mechanism"],
            self.contract["authorization_mechanism"],
        )

    # 2
    def test_record_at_pinned_framework_revision_option_is_absent(self):
        self.assertFalse(
            self.contract["authorization_record_may_exist_at_pinned_framework_revision"]
        )
        for phrase in FORK_PHRASES:
            self.assertNotIn(
                phrase,
                self.text,
                f"forked authorization provenance wording resurfaced: {phrase!r}",
            )
        self.assertIn("That fork is deleted.", self.text)
        self.assertIn("There is no second mechanism.", self.text)

    # 3
    def test_immutable_run_control_path_is_explicit(self):
        self.assertEqual(self.contract["run_control_directory"], RUN_CONTROL_DIR)
        self.assertEqual(
            self.contract["authorization_record_location_type"],
            "immutable_run_control_commit",
        )
        self.assertIn(RUN_CONTROL_DIR, self.text)
        self.assertFalse(RUN_CONTROL_DIR.startswith("experiments/evidence/"))

    # 4
    def test_authorization_record_path_is_explicit(self):
        path = self.contract["execution_authorization_record_path"]
        self.assertEqual(path, AUTH_RECORD_PATH)
        self.assertTrue(path.startswith(RUN_CONTROL_DIR + "/"))
        self.assertNotIn("0015", path)
        self.assertNotIn("experiments/evidence/", path)

    # 5
    def test_owner_approval_artifact_path_is_explicit(self):
        path = self.contract["owner_approval_artifact_path"]
        self.assertEqual(path, OWNER_APPROVAL_PATH)
        self.assertTrue(path.startswith(RUN_CONTROL_DIR + "/"))

    # 6
    def test_authorization_record_digest_path_is_explicit(self):
        path = self.contract["execution_authorization_record_digest_path"]
        self.assertEqual(path, AUTH_DIGEST_PATH)
        self.assertNotEqual(path, self.contract["execution_authorization_record_path"])

    # 45
    def test_floating_refs_remain_prohibited(self):
        prohibited = self.contract["floating_refs_prohibited_as_execution_pin"]
        for ref in ("main", "origin/main", "HEAD", "refs/heads/main"):
            self.assertIn(ref, prohibited)
        self.assertIn(
            "mutable or floating path used as authority",
            self.contract["authorization_hard_stop_conditions"],
        )


class AuthorizationSentinels(unittest.TestCase):
    """7-10: three pending sentinels, all execution-blocking."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 7
    def test_execution_framework_sha_sentinel_is_pending(self):
        self.assertEqual(self.contract["execution_framework_sha"], SENTINEL)
        self.assertEqual(self.contract["execution_framework_sha_sentinel"], SENTINEL)
        self.assertFalse(_is_executable_pin(self.contract["execution_framework_sha"]))

    # 8
    def test_run_control_commit_sha_sentinel_is_pending(self):
        self.assertEqual(self.contract["run_control_commit_sha"], RUN_CONTROL_SENTINEL)
        self.assertEqual(
            self.contract["run_control_commit_sha_sentinel"], RUN_CONTROL_SENTINEL
        )
        self.assertFalse(_is_executable_pin(self.contract["run_control_commit_sha"]))

    # 9
    def test_authorization_record_digest_sentinel_is_pending(self):
        self.assertEqual(
            self.contract["authorization_record_sha256"], OWNER_APPROVAL_SENTINEL
        )
        self.assertEqual(
            self.contract["authorization_record_sha256_sentinel"],
            OWNER_APPROVAL_SENTINEL,
        )
        self.assertFalse(HEX64.match(str(self.contract["authorization_record_sha256"])))

    # 10
    def test_all_pending_sentinels_block_execution(self):
        self.assertTrue(self.contract["pending_sentinels_block_execution"])
        self.assertEqual(self.contract["pending_sentinels"], ALL_SENTINELS)
        for sentinel in ALL_SENTINELS:
            self.assertIn(sentinel, self.text)
            self.assertIn("remains non-runnable while", self.text)
        self.assertFalse(self.contract["package_runnable"])
        self.assertEqual(
            self.contract["execution_authorization_status"], "NOT_AUTHORIZED"
        )
        # The three sentinels are distinct values, not one reused placeholder.
        self.assertEqual(len(set(ALL_SENTINELS)), 3)


class OwnerApprovalIsSeparateAndAuthoritative(unittest.TestCase):
    """11-14: digest authority lives outside the record; identity required."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 11
    def test_owner_approved_digest_stored_separately_from_the_record(self):
        self.assertEqual(
            self.contract["authoritative_digest_source"], "owner_approval_artifact"
        )
        self.assertNotEqual(
            self.contract["owner_approval_artifact_path"],
            self.contract["execution_authorization_record_path"],
        )
        self.assertIn("authorization_record_sha256", self.contract["owner_approval_required_fields"])

    # 12
    def test_authorization_record_cannot_self_approve(self):
        self.assertFalse(self.contract["authorization_record_self_approval_allowed"])
        self.assertTrue(self.contract["digest_inside_authorization_record_is_informational"])
        self.assertIn("must not approve itself", self.text)
        # And the validator enforces it structurally.
        record = valid_future_authorization_record()
        record["owner_approval_reference"] = ""
        self.assertTrue(
            any("self-approve" in e for e in validate_future_authorization_record(
                record, EXPECTED_AUTHORIZED_INPUTS))
        )

    # 13
    def test_approver_identity_is_required(self):
        self.assertIn(
            "approver_github_identity", self.contract["owner_approval_required_fields"]
        )
        self.assertTrue(self.contract["approval_identity_verification_required"])
        self.assertFalse(self.contract["operator_self_approval_allowed"])
        self.assertEqual(
            self.contract["approving_authority"],
            "repository_owner_or_explicitly_delegated_campaign_owner",
        )

    # 14
    def test_approval_timestamp_is_required(self):
        self.assertIn(
            "approval_timestamp", self.contract["owner_approval_required_fields"]
        )
        self.assertEqual(
            self.contract["owner_approval_required_fields"],
            OWNER_APPROVAL_REQUIRED_FIELDS,
        )


class AuthorizationRecordRequiredFields(unittest.TestCase):
    """15-29: the full required-record contract, field by field."""

    def setUp(self):
        self.contract, self.text = _load_contract()
        self.declared = self.contract["authorization_record_required_fields"]

    def _requires(self, *fields):
        for field in fields:
            self.assertIn(field, self.declared, f"{field} must be a required field")
            self.assertIn(field, AUTH_RECORD_REQUIRED_FIELDS)
            record = valid_future_authorization_record()
            del record[field]
            errors = validate_future_authorization_record(
                record, EXPECTED_AUTHORIZED_INPUTS
            )
            self.assertTrue(errors, f"removing {field} must be rejected")

    # 15
    def test_exact_authorization_status_string_required(self):
        self._requires("authorization_status")
        self.assertEqual(
            self.contract["required_authorization_status_string"], AUTH_STATUS
        )
        record = valid_future_authorization_record()
        record["authorization_status"] = "AUTHORIZED"
        self.assertTrue(
            validate_future_authorization_record(record, EXPECTED_AUTHORIZED_INPUTS)
        )

    # 16
    def test_framework_sha_field_required(self):
        self._requires("execution_framework_sha")

    # 17
    def test_target_repository_and_sha_required(self):
        self._requires("target_repository", "target_sha")

    # 18
    def test_evidence_number_and_slug_required(self):
        self._requires("evidence_number", "evidence_slug")

    # 19
    def test_exact_model_required(self):
        self._requires("exact_model")

    # 20
    def test_artifact_type_required(self):
        self._requires("artifact_type")

    # 21
    def test_package_path_and_sha256_required(self):
        self._requires("preparation_package_path", "preparation_package_sha256")
        self.assertEqual(
            self.contract["canonical_preparation_package_path"], CANONICAL_PACKAGE_PATH
        )

    # 22
    def test_checklist_path_and_sha256_required(self):
        self._requires("gate_d_checklist_path", "gate_d_checklist_sha256")
        self.assertEqual(
            self.contract["canonical_gate_d_checklist_path"], CANONICAL_CHECKLIST_PATH
        )

    # 23
    def test_one_invocation_only_required(self):
        self._requires("one_invocation_only")

    # 24
    def test_no_retry_required(self):
        self._requires("no_retry")

    # 25
    def test_no_fallback_required(self):
        self._requires("no_fallback")

    # 26
    def test_no_model_substitution_required(self):
        self._requires("no_model_substitution")

    # 27
    def test_no_artifact_repair_required(self):
        self._requires("no_artifact_repair")

    # 28
    def test_no_target_mutation_required(self):
        self._requires("no_target_mutation")

    # 29
    def test_stop_on_first_failure_required(self):
        self._requires("stop_on_first_failed_gate")
        self.assertEqual(
            self.contract["authorization_record_boolean_fields_must_be_true"],
            AUTH_RECORD_TRUE_FLAGS,
        )
        self.assertEqual(self.declared, AUTH_RECORD_REQUIRED_FIELDS)


class GateAAuthorizationVerification(unittest.TestCase):
    """30-36: Gate A actually performs digest verification, in order."""

    def setUp(self):
        self.contract, self.text = _load_contract()
        self.steps = self.contract["gate_a_authorization_verification_steps"]

    def _step(self, number):
        prefix = f"{number} "
        matches = [s for s in self.steps if s.startswith(prefix)]
        self.assertEqual(len(matches), 1, f"exactly one Gate A step {number} expected")
        return matches[0]

    def test_fifteen_ordered_steps_declared(self):
        self.assertEqual(len(self.steps), 15)
        for index in range(1, 16):
            self._step(index)

    # 30
    def test_gate_a_contains_explicit_sha256_recomputation_step(self):
        self.assertIn("RECOMPUTED", self.text)
        self.assertIn("recomputed", self._step(3).lower())
        self.assertIn("SHA-256", self._step(3))

    # 31
    def test_gate_a_compares_against_owner_approved_digest(self):
        self.assertIn("owner-approved digest", self._step(4))
        self.assertTrue(self.contract["gate_a_digest_verification_precedes_invocation"])
        # Truthful future-tense phrasing: the consumer that would do this does
        # not exist yet, so the package must not say verification "occurs".
        self.assertIn(
            "Digest verification must occur BEFORE model invocation.", self.text
        )
        self.assertNotIn("Digest verification occurs BEFORE", self.text)

    # 32
    def test_gate_a_verifies_approver_identity(self):
        self.assertIn("identity", self._step(5))
        self.assertIn("AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION", self._step(6))

    # 33
    def test_gate_a_verifies_framework_head(self):
        self.assertIn("framework HEAD", self._step(8))

    # 34
    def test_gate_a_verifies_target_head(self):
        self.assertIn("Auteur HEAD", self._step(9))

    # 35
    def test_gate_a_verifies_package_digest(self):
        self.assertIn("preparation-package path and digest", self._step(12))
        self.assertIn(
            "SHA-256(preparation package bytes) == authorization record "
            "preparation_package_sha256",
            self.text,
        )
        self.assertFalse(self.contract["external_package_or_checklist_copy_allowed"])
        self.assertTrue(self.contract["package_and_checklist_loaded_from_framework_root"])

    # 36
    def test_gate_a_verifies_checklist_digest(self):
        self.assertIn("Gate D checklist path and digest", self._step(13))
        self.assertIn(
            "SHA-256(Gate D checklist bytes)    == authorization record "
            "gate_d_checklist_sha256",
            self.text,
        )
        checklist = CHECKLIST_PATH.read_text(encoding="utf-8")
        self.assertIn("Gate A fails before Gate D begins", checklist)


class AuthorizationHardStops(unittest.TestCase):
    """37-44: every authorization defect blocks invocation."""

    def setUp(self):
        self.contract, self.text = _load_contract()
        self.stops = self.contract["authorization_hard_stop_conditions"]

    def _stop(self, phrase):
        self.assertIn(phrase, self.stops, f"missing hard-stop condition: {phrase}")

    def test_all_twentyfour_hard_stops_declared(self):
        # 23 authorization-content stops, plus the consumer stop added after the
        # third review found the contract specified but entirely unenforced.
        self.assertEqual(len(self.stops), 24)
        self.assertEqual(len(set(self.stops)), 24)
        self.assertTrue(self.contract["authorization_failure_is_gate_a_failure"])
        self.assertFalse(self.contract["authorization_failure_permits_retry"])

    # 37
    def test_missing_record_blocks_invocation(self):
        self._stop("authorization record absent")
        self.assertFalse(self.contract["execution_authorization_record_exists"])

    # 38
    def test_missing_approval_blocks_invocation(self):
        self._stop("approval artifact absent")
        self._stop("owner-approved digest absent")
        self.assertFalse(self.contract["owner_approval_artifact_exists"])

    # 39
    def test_digest_mismatch_blocks_invocation(self):
        self._stop("digest mismatch")
        self._stop("digest malformed")
        self._stop("record changed after approval")

    # 40
    def test_unauthorized_approver_blocks_invocation(self):
        self._stop("approval identity unauthorized")

    # 41
    def test_malformed_record_blocks_invocation(self):
        self._stop("authorization status not exact")
        record = valid_future_authorization_record()
        record["preparation_package_sha256"] = "NOTAHEXDIGEST"
        self.assertTrue(
            validate_future_authorization_record(record, EXPECTED_AUTHORIZED_INPUTS)
        )

    # 42
    def test_inconsistent_record_blocks_invocation(self):
        for phrase in (
            "execution framework SHA mismatch",
            "target SHA mismatch",
            "evidence number mismatch",
            "evidence slug mismatch",
            "model mismatch",
            "package path mismatch",
            "package digest mismatch",
            "checklist path mismatch",
            "checklist digest mismatch",
        ):
            self._stop(phrase)

    # 43
    def test_duplicate_records_block_invocation(self):
        self._stop("conflicting duplicate records")
        self._stop("more than one approval artifact")

    # 44
    def test_preexisting_evidence_0016_output_blocks_invocation(self):
        self._stop("pre-existing Evidence 0016 output")
        self.assertIn(
            "15 no existing Evidence 0016 output is present",
            self.contract["gate_a_authorization_verification_steps"],
        )


class NoAuthorizationArtifactsInThisPR(unittest.TestCase):
    """46-50: nothing was actually created, and nothing became runnable."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 46
    def test_no_authorization_record_exists_in_this_pr(self):
        self.assertFalse(
            (REPO_ROOT / self.contract["execution_authorization_record_path"]).exists()
        )
        self.assertFalse(
            (REPO_ROOT / self.contract["execution_authorization_record_digest_path"]).exists()
        )
        self.assertFalse(self.contract["execution_authorization_record_exists"])
        self.assertFalse(self.contract["execution_authorization_record_digest_exists"])

    # 47
    def test_no_owner_approval_artifact_exists_in_this_pr(self):
        self.assertFalse(
            (REPO_ROOT / self.contract["owner_approval_artifact_path"]).exists()
        )
        self.assertFalse((REPO_ROOT / self.contract["run_control_directory"]).exists())
        self.assertFalse(self.contract["owner_approval_artifact_exists"])
        self.assertFalse(self.contract["run_control_directory_exists"])

    # 48
    def test_package_remains_prepared_not_run(self):
        self.assertEqual(self.contract["package_status"], "PREPARED_NOT_RUN")
        self.assertIn("PREPARED_NOT_RUN", CHECKLIST_PATH.read_text(encoding="utf-8"))

    # 49
    def test_package_remains_not_authorized(self):
        self.assertEqual(
            self.contract["execution_authorization_status"], "NOT_AUTHORIZED"
        )
        collapsed = " ".join(self.text.split())
        self.assertIn(
            "no Gate A authorization consumer exists, so no authorization state "
            "is enforceable. No authorization record exists. No owner approval "
            "exists.",
            collapsed,
        )
        self.assertIn("There is no alternative mechanism.", collapsed)

    # 50
    def test_package_remains_non_runnable(self):
        self.assertFalse(self.contract["package_runnable"])
        self.assertFalse(self.contract["merging_this_pr_authorizes_execution"])
        self.assertFalse(self.contract["merging_this_pr_finalizes_pin"])
        self.assertIn("The package is not runnable.", self.text)


class FutureAuthorizationRecordFixture(unittest.TestCase):
    """Synthetic fixtures only. The real Evidence 0016 record is NOT created."""

    def test_valid_fixture_is_accepted(self):
        errors = validate_future_authorization_record(
            valid_future_authorization_record(), EXPECTED_AUTHORIZED_INPUTS
        )
        self.assertEqual(errors, [], f"valid fixture rejected: {errors}")

    def test_every_required_field_is_individually_load_bearing(self):
        for field in AUTH_RECORD_REQUIRED_FIELDS:
            record = valid_future_authorization_record()
            del record[field]
            self.assertTrue(
                validate_future_authorization_record(record, EXPECTED_AUTHORIZED_INPUTS),
                f"removing {field} was wrongly accepted",
            )

    def test_invalid_fixtures_are_all_rejected(self):
        cases = {
            "missing field": lambda r: r.pop("exact_model"),
            "malformed digest": lambda r: r.update(preparation_package_sha256="ZZ" * 32),
            "uppercase digest": lambda r: r.update(gate_d_checklist_sha256="C" * 64),
            "short framework sha": lambda r: r.update(execution_framework_sha="a" * 12),
            "mismatched framework sha": lambda r: r.update(execution_framework_sha="d" * 40),
            "mismatched target sha": lambda r: r.update(
                target_sha="b40db654e0df9e90074f7ad85b40d7362378e07d"
            ),
            "wrong evidence number": lambda r: r.update(evidence_number="0015"),
            "wrong evidence slug": lambda r: r.update(evidence_slug="0015-stage1-auteur"),
            "wrong model": lambda r: r.update(exact_model="claude-haiku-4"),
            "false no_retry": lambda r: r.update(no_retry=False),
            "false no_target_mutation": lambda r: r.update(no_target_mutation=False),
            "unauthorized status": lambda r: r.update(authorization_status="AUTHORIZED"),
            "non-canonical package path": lambda r: r.update(
                preparation_package_path="docs/copied-package.md"
            ),
            "non-canonical checklist path": lambda r: r.update(
                gate_d_checklist_path="/tmp/checklist.md"
            ),
            "self-approving record": lambda r: r.update(owner_approval_reference=""),
        }
        for name, mutate in cases.items():
            with self.subTest(case=name):
                record = valid_future_authorization_record()
                mutate(record)
                self.assertTrue(
                    validate_future_authorization_record(
                        record, EXPECTED_AUTHORIZED_INPUTS
                    ),
                    f"invalid fixture wrongly accepted: {name}",
                )

    def test_fixture_never_touches_the_filesystem(self):
        """The fixture is in-memory only; no run-control artifact is written."""
        validate_future_authorization_record(
            valid_future_authorization_record(), EXPECTED_AUTHORIZED_INPUTS
        )
        self.assertFalse((REPO_ROOT / RUN_CONTROL_DIR).exists())
        self.assertFalse((REPO_ROOT / AUTH_RECORD_PATH).exists())
        self.assertFalse((REPO_ROOT / OWNER_APPROVAL_PATH).exists())


# ---------------------------------------------------------------------------
# Gate A authorization CONSUMER status (51-80).
#
# These tests exist because a third independent review found that this package
# specified an elaborate Gate A authorization preflight in present tense, while
# a repository-wide search found ZERO runtime code that loads, parses, or
# verifies any of it. The contract was fully specified and entirely unenforced.
#
# The tests below are CONTRACT-CONSISTENCY tests. They deliberately do NOT
# prove runtime enforcement -- that is the whole point. They enforce that the
# package keeps SAYING it is unenforced for exactly as long as it is.
# ---------------------------------------------------------------------------

EXEC_PACKAGE_PATH = (
    REPO_ROOT / "docs" / "experiments" / "STAGE-1-AUTEUR-EXECUTION-PACKAGE.md"
)

CONSUMER_HARD_STOP = "GATE_A_AUTHORIZATION_CONSUMER_NOT_IMPLEMENTED"

# Directories that would hold a real consumer implementation.
RUNTIME_SOURCE_DIRS = ("scripts", "src", "sensemaking_skills")

# Markers that would indicate a real authorization consumer had been added.
CONSUMER_IMPLEMENTATION_MARKERS = (
    "authorization_record_sha256",
    "authorization-record.yaml",
    "owner-approval.md",
    "AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION",
)

# Phrases that assert CURRENT runtime enforcement. Prohibited in changed docs.
PROHIBITED_ENFORCEMENT_PHRASES = (
    "the runner verifies",
    "the live runner",
    "gate a recomputes",
    "gate a compares",
    "gate a verifies",
    "gate a checks",
    "the runtime blocks",
    "the runtime verifies",
    "before invocation, the system checks",
    "the system verifies",
    "workflow-runtime.py performs",
    "workflow-runtime.py verifies",
    "workflow-runtime.py enforces",
    "comparisons happen in",
    "is currently enforced",
    "is runtime-enforced",
)

CHANGED_DOCS = (PACKAGE_PATH, CHECKLIST_PATH, EXEC_PACKAGE_PATH)

# ---------------------------------------------------------------------------
# Prose honesty guard
#
# Design note (round 5 remediation):
#
# The previous implementation exempted an ENTIRE LINE whenever that line
# contained any "negative context" word such as "prohibited", "did not" or
# "must not". That was empirically bypassable: a line may carry a genuine
# present-tense enforcement overclaim *and* an unrelated negative word, e.g.
#
#     Gate A verifies the authorization digest; unauthorized runs are prohibited.
#
# The word "prohibited" wrongly exempted the false claim "Gate A verifies".
#
# The line-level exemption is deleted. There is now exactly one way to exempt
# text: enclose it in an explicitly marked exemption region. Everything else is
# scanned clause by clause, so a negative word in one clause can never exempt
# another clause. Proximity to words like "example", "quoted", "future" or
# "required" grants nothing.
#
# Round 7 remediation: the markers are RENAMED.
#
# They were called BEGIN_QUOTED_OLD_WORDING / END_QUOTED_OLD_WORDING. By round
# 6 they also enclosed two `does_not_prove` denial lists -- current, truthful
# statements, not quotations of superseded wording. The name misdescribed its
# own function, in a PR whose entire purpose is documentation honesty. The
# markers are now named for what they actually do, and every use must declare a
# reason drawn from a closed set.
#
# Semantics of an exemption region:
#   - enclosed text is intentionally excluded from deterministic lexical guard
#     matching;
#   - exclusion does NOT make the enclosed text authoritative;
#   - regions are only for non-authoritative quoted, denied, or example text;
#   - authoritative contract requirements must never be placed inside one;
#   - every region must carry a short reason from ALLOWED_EXEMPTION_REASONS.
#
# Syntax (exact):
#
#     BEGIN_PROSE_GUARD_EXEMPTION reason="truthful denial list"
#     ...
#     END_PROSE_GUARD_EXEMPTION
#
# Fail-closed in every direction: a missing, blank or unknown reason, a nested
# region, an unmatched marker, an oversized region, a region covering more than
# half a document, a marker inside inline code, or a near-miss spelling all
# exempt NOTHING.
#
# Deliberate limit, stated rather than hidden: the guard enforces that the
# reason is one of the closed set, not that the reason accurately characterizes
# the region. Whether "truthful denial list" is an honest label for a given
# region is reviewer judgement -- it is not lexically decidable, and this suite
# does not pretend to decide it.
# ---------------------------------------------------------------------------

PROSE_GUARD_EXEMPTION_BEGIN = "BEGIN_PROSE_GUARD_EXEMPTION"
PROSE_GUARD_EXEMPTION_END = "END_PROSE_GUARD_EXEMPTION"

# Closed reason enum. A reason outside this set fails closed.
ALLOWED_EXEMPTION_REASONS = (
    "quoted obsolete wording",
    "truthful denial list",
    "non-authoritative example",
)

# Superseded marker names. Permitted in this module ONLY as the negative
# constants asserting their absence from governing files.
OLD_MARKER_NAMES = ("BEGIN_QUOTED_OLD_WORDING", "END_QUOTED_OLD_WORDING")

# An exemption region is a bounded quotation, never a document section.
MAX_EXEMPTION_REGION_LINES = 12

# Authoritative-requirement language. A contract requirement inside an
# exemption region would be unscanned AND non-authoritative, which is exactly
# the confusion the rename exists to prevent.
_AUTHORITATIVE_REQUIREMENT_RE = re.compile(
    r"\b(?:must|shall|is\s+required\s+to|are\s+required\s+to)\b", re.IGNORECASE
)

# Subject nouns that, in this repository's prose, denote the runtime.
_OVERCLAIM_SUBJECT = (
    r"(?:gate\s+a|runner|runtime|system|consumer|"
    r"(?:scripts/)?workflow-runtime\.py)"
)
# Present-tense third-person verbs asserting that enforcement happens NOW.
# Bare infinitives ("must verify", "will recompute", "to compare") are absent
# on purpose: those are the truthful future-tense forms and must stay legal.
_OVERCLAIM_VERB = (
    r"(?:verifies|recomputes|compares|validates|blocks|checks|enforces|"
    r"performs|rejects|refuses|halts)"
)
_OVERCLAIM_ADVERB = r"(?:currently|already|now|automatically|itself|always)"

# The ONLY inline denial accepted, and only when it directly governs the claim:
# the denial must sit immediately before the subject in the same clause, e.g.
# "It does not claim that `workflow-runtime.py` performs ...". A denial anywhere
# else -- another clause, elsewhere on the line, merely nearby -- exempts
# nothing. This is a syntactic adjacency rule, not a proximity heuristic.
_GOVERNING_DENIAL_RE = re.compile(
    r"\b(?:does|do|did)\s+not\s+(?:claim|assert|say|state)\s+that\s+$"
    r"|\bnever\s+(?:claimed|asserted|said|stated)\s+that\s+$",
    re.IGNORECASE,
)

# An optional negator IMMEDIATELY attached to the subject noun phrase makes the
# claim truthful ("no current runner verifies"). A negator anywhere else in the
# clause grants nothing.
_OVERCLAIM_RE = re.compile(
    r"(?P<neg>\b(?:no|neither)\s+(?:\w+\s+){0,2})?"
    r"\b(?P<subject>" + _OVERCLAIM_SUBJECT + r")"
    r"(?:\s+" + _OVERCLAIM_ADVERB + r"){0,2}"
    r"\s+(?P<verb>" + _OVERCLAIM_VERB + r")\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Round 6 remediation: passive, emphatic and progressive enforcement claims.
#
# The round-5 guard only understood ACTIVE SIMPLE PRESENT ("Gate A verifies
# ..."). The reviewer demonstrated that the same false assertion survives when
# rephrased, because none of these shapes contain a third-person present verb
# immediately after a runtime subject:
#
#   passive       "The authorization digest is verified by Gate A."
#   agentless     "The target SHA is verified before execution."
#   emphatic-do   "Gate A does verify the digest."
#   progressive   "The runner is validating the approval."
#   contracted    "Gate A's checking the digest now."
#
# Three additional deterministic matchers are added below. Declared scope:
# ENUMERATED active-simple-present, emphatic-do, present-progressive and
# affirmative-passive forms. This is not a general English parser; it is a
# closed verb lexicon applied to normalized clauses.
#
# Negation rule (identical in spirit to the active matcher): a negator only
# counts when it sits in the AUXILIARY slot of the very construction being
# matched ("is not verified", "does not verify", "is not checking") or is bound
# to the subject noun phrase ("no current runner"). A negator, "prohibited",
# "must not", "example", "old wording", "future" or "required" appearing
# elsewhere in the clause, on the line, or nearby exempts nothing.
#
# Modal/future auxiliaries ("would be verified", "will be recomputed",
# "must verify") never match: the auxiliary lexicon is exactly
# is/are/was/were and do/does/did, so truthful future-tense prose stays legal.
#
# Round 7 remediation: the procedural-mechanism carve-out is DELETED.
#
# Round 6 added a carve-out allowing an affirmative agentless passive whose
# manner adverb named a non-runtime mechanism ("is blocked procedurally"). The
# sixth review showed the carve-out was bypassable, and for a structural
# reason: the manner adverb was only ever handled in the POST-participle slot
# ("blocked procedurally"). With the adverb in the PRE-participle slot
# ("is procedurally blocked") the passive regex did not match at all, so the
# agent-naming safety check never ran. Four strings walked through, two of them
# explicitly naming a runtime agent:
#
#     Invocation is procedurally blocked by Gate A.
#     The digest is procedurally verified by the runtime.
#
# The fix is deletion, not another exception. Manner adverbs are now ORDINARY
# adverbs in every position: they never excuse anything. The truthful sentences
# the carve-out existed to protect are rewritten into plainly negative form
# ("The run remains non-runnable because no consumer exists."), which needs no
# exception because it contains no enforcement participle at all. This removes
# an entire exception class rather than adding a parametrized dimension --
# growing that dimension is what produced new grammatical-position bugs in
# rounds 5 and 6.
# ---------------------------------------------------------------------------

# Past participles of the enforcement verb lexicon.
_PASSIVE_PARTICIPLE = (
    r"(?:verified|recomputed|compared|validated|blocked|checked|enforced|"
    r"performed|prevented|rejected|refused|halted|loaded|gated)"
)
# Bare infinitives, for the emphatic "does <verb>" construction only.
_EMPHATIC_VERB = (
    r"(?:verify|recompute|compare|validate|block|check|enforce|perform|"
    r"reject|refuse|halt|load|gate)"
)
# Present participles, for the progressive construction.
_PROGRESSIVE_VERB = (
    r"(?:verifying|recomputing|comparing|validating|blocking|checking|"
    r"enforcing|performing|preventing|rejecting|refusing|halting|loading|"
    r"gating)"
)
# The ONLY auxiliaries these matchers accept. Modals are deliberately absent.
_BE_AUX = r"(?:is|are|was|were)"
_DO_AUX = r"(?:do|does|did)"
# Negators valid ONLY in the auxiliary slot of the matched construction.
_AUX_NEGATOR = r"(?:not|never|no\s+longer|n't)"
# Adverbs that may sit between auxiliary and verb without changing polarity.
_INNER_ADVERB = (
    r"(?:currently|already|now|automatically|always|actually|explicitly|"
    r"deterministically|first|then|also)"
)

# Closed set of MANNER adverbs this guard recognizes. Deliberately small and
# specific to this package's vocabulary. The guard claims support for exactly
# these nine words -- not for arbitrary English adverbs.
MANNER_ADVERBS = (
    "procedurally",
    "automatically",
    "currently",
    "mechanically",
    "deterministically",
    "explicitly",
    "directly",
    "securely",
    "synchronously",
)
_MANNER_ADVERB = r"(?:" + r"|".join(MANNER_ADVERBS) + r")"

# Any adverb legal in the slot between auxiliary and participle.
_PRE_PARTICIPLE_ADVERB = r"(?:" + _INNER_ADVERB + r"|" + _MANNER_ADVERB + r")"

# The four adverb slots the passive grammar declares support for. Documented
# here because "which positions are covered" is exactly what rounds 5 and 6
# got wrong, and a reviewer must be able to read the answer without inferring
# it from the regex.
SUPPORTED_PASSIVE_ADVERB_POSITIONS = (
    "pre-participle:  is procedurally verified",
    "post-participle: is verified procedurally",
    "pre-agent:       is verified procedurally by Gate A",
    "post-agent:      is verified by Gate A procedurally",
)

# Affirmative passive:
#
#   <auxiliary> [negator] [adverb]{0,2} [negator] <participle>
#       [and|or <participle>] [manner adverb]{0,2}
#       [by <runtime agent>] [manner adverb]{0,2}
#
# Every quantifier is explicitly bounded: no ".*", no unrestricted word span.
# Rejected unless a negator sits in the auxiliary slot of this very
# construction. No manner adverb excuses anything in any position -- the
# round-6 carve-out is gone.
_PASSIVE_RE = re.compile(
    r"\b" + _BE_AUX + r"\s+"
    r"(?P<neg1>" + _AUX_NEGATOR + r"\s+)?"
    r"(?:" + _PRE_PARTICIPLE_ADVERB + r"\s+){0,2}"
    r"(?P<neg2>" + _AUX_NEGATOR + r"\s+)?"
    r"(?P<part>" + _PASSIVE_PARTICIPLE + r")"
    r"(?:\s+(?:and|or)\s+" + _PASSIVE_PARTICIPLE + r")?"
    r"(?:\s+" + _MANNER_ADVERB + r"){0,2}"
    r"(?P<agent>\s+by\s+(?:the\s+|a\s+|an\s+|any\s+|its\s+|"
    r"(?:\w+\s+){0,2})?" + _OVERCLAIM_SUBJECT + r")?"
    r"(?:\s+" + _MANNER_ADVERB + r"){0,2}",
    re.IGNORECASE,
)

# Emphatic: "<runtime subject> does <bare verb>".
_EMPHATIC_RE = re.compile(
    r"(?P<neg>\b(?:no|neither)\s+(?:\w+\s+){0,2})?"
    r"\b(?P<subject>" + _OVERCLAIM_SUBJECT + r")\s+"
    r"(?:" + _DO_AUX + r")\s+"
    r"(?P<dneg>" + _AUX_NEGATOR + r"\s+)?"
    r"(?:" + _INNER_ADVERB + r"\s+)*"
    r"(?P<verb>" + _EMPHATIC_VERB + r")\b",
    re.IGNORECASE,
)

# Present progressive: "<runtime subject> is <verb>ing".
_PROGRESSIVE_RE = re.compile(
    r"(?P<neg>\b(?:no|neither)\s+(?:\w+\s+){0,2})?"
    r"\b(?P<subject>" + _OVERCLAIM_SUBJECT + r")\s+"
    r"(?:" + _BE_AUX + r")\s+"
    r"(?P<pneg>" + _AUX_NEGATOR + r"\s+)?"
    r"(?:" + _INNER_ADVERB + r"\s+)*"
    r"(?P<verb>" + _PROGRESSIVE_VERB + r")\b",
    re.IGNORECASE,
)

# "Gate A's checking ..." is the contraction of "Gate A is checking ...".
# Expanded ONLY when the following word is an enforcement present participle
# and is NOT a possessive gerund ("Gate A's checking OF the digest" and
# "Gate A's checking procedure" stay possessive noun phrases).
_PROGRESSIVE_CONTRACTION_RE = re.compile(
    r"\b(?P<subject>" + _OVERCLAIM_SUBJECT + r")(?:'|’)s\s+"
    r"(?=" + _PROGRESSIVE_VERB + r"\b(?!\s+(?:of|procedure|procedures|step|"
    r"steps|logic|rule|rules)\b))",
    re.IGNORECASE,
)


def _expand_progressive_contractions(text):
    """Rewrite "<subject>'s <verb>ing" as "<subject> is <verb>ing"."""
    return _PROGRESSIVE_CONTRACTION_RE.sub(
        lambda m: m.group("subject") + " is ", text
    )


# Literal phrases that are overclaims regardless of subject/verb shape.
_OVERCLAIM_LITERALS = (
    "is runtime-enforced",
    "is currently enforced",
    "comparisons happen in",
    "the live runner",
)

# A period only ends a clause at a word boundary, so filenames such as
# `workflow-runtime.py` survive clause splitting intact.
_CLAUSE_SPLIT_RE = re.compile(r"\.(?=\s|$)|[;:!?|—–]|,")


def _normalize_markdown(text):
    """Strip Markdown emphasis/decoration so formatting cannot hide a claim."""
    text = text.replace("**", " ").replace("__", " ")
    # Emphasis underscores only: intra-word underscores belong to snake_case
    # identifiers (YAML keys) and must not be split into prose words.
    text = re.sub(r"(?<![A-Za-z0-9])_+|_+(?![A-Za-z0-9])", " ", text)
    # HTML emphasis and any other inline tag becomes nothing, so <b>Gate A</b>
    # reads as "Gate A" rather than an unparsable token.
    text = re.sub(r"</?[A-Za-z][^>]*>", " ", text)
    # Markdown links: keep the link TEXT, drop the target. Done before bracket
    # stripping so a claim written as [Gate A](#anchor) verifies ... is seen.
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*>#\[\]()]", " ", text)
    text = re.sub(r"^\s*[-+]\s+", " ", text)
    text = _expand_progressive_contractions(text)
    return re.sub(r"\s+", " ", text)


def _strip_marker_decoration(raw_line):
    """Reduce a candidate marker line to its bare text, or None.

    A marker must be the whole line (optionally wrapped in an HTML comment or
    prefixed by a YAML '#'). Markers inside inline code are NOT markers --
    otherwise the region mechanism could be created dynamically from ordinary
    prose that merely mentions it.
    """
    if "`" in raw_line:
        return None
    stripped = raw_line.strip()
    stripped = re.sub(r"^<!--\s*", "", stripped)
    stripped = re.sub(r"\s*-->$", "", stripped)
    return stripped.lstrip("#-").strip()


_EXEMPTION_BEGIN_RE = re.compile(
    r"^" + PROSE_GUARD_EXEMPTION_BEGIN + r'\s+reason="(?P<reason>[^"]*)"$'
)


def _match_exemption_begin(raw_line):
    """Classify a candidate opening marker.

    Returns None (not a marker at all), ("ok", reason) or ("bad", problem).
    """
    stripped = _strip_marker_decoration(raw_line)
    if stripped is None or not stripped.startswith(PROSE_GUARD_EXEMPTION_BEGIN):
        return None
    rest = stripped[len(PROSE_GUARD_EXEMPTION_BEGIN):]
    if rest and not rest[0].isspace():
        # A near-miss spelling such as BEGIN_PROSE_GUARD_EXEMPTIONS is not a
        # marker, so it activates nothing.
        return None
    match = _EXEMPTION_BEGIN_RE.match(stripped)
    if not match:
        return (
            "bad",
            f'malformed {PROSE_GUARD_EXEMPTION_BEGIN}: exact syntax '
            f'reason="..." is required',
        )
    reason = match.group("reason").strip()
    if not reason:
        return ("bad", "exemption reason is blank")
    if reason not in ALLOWED_EXEMPTION_REASONS:
        return ("bad", f"unknown exemption reason {reason!r}")
    return ("ok", reason)


def _is_exemption_end(raw_line):
    return _strip_marker_decoration(raw_line) == PROSE_GUARD_EXEMPTION_END


def _is_any_marker_line(raw_line):
    return _match_exemption_begin(raw_line) is not None or _is_exemption_end(raw_line)


def _resolve_exemption_regions(lines):
    """Return (exempt_line_numbers, structural_violations).

    Fail-closed: any malformed region exempts nothing at all.
    """
    exempt = set()
    violations = []
    open_at = None
    for lineno, raw in enumerate(lines, start=1):
        begin = _match_exemption_begin(raw)
        if begin is not None:
            kind, payload = begin
            if kind == "bad":
                violations.append(f"line {lineno}: {payload}")
                continue
            if open_at is not None:
                violations.append(
                    f"line {lineno}: nested {PROSE_GUARD_EXEMPTION_BEGIN} "
                    f"(already open at line {open_at})"
                )
                continue
            open_at = lineno
        elif _is_exemption_end(raw):
            if open_at is None:
                violations.append(
                    f"line {lineno}: {PROSE_GUARD_EXEMPTION_END} without a "
                    f"matching {PROSE_GUARD_EXEMPTION_BEGIN}"
                )
                continue
            body = range(open_at + 1, lineno)
            if len(body) > MAX_EXEMPTION_REGION_LINES:
                violations.append(
                    f"line {open_at}: exemption region spans {len(body)} lines, "
                    f"more than the {MAX_EXEMPTION_REGION_LINES}-line maximum"
                )
                open_at = None
                continue
            for inner in body:
                if _AUTHORITATIVE_REQUIREMENT_RE.search(lines[inner - 1]):
                    violations.append(
                        f"line {inner}: authoritative requirement language "
                        "inside an exemption region; requirements must be "
                        "stated in scanned, authoritative prose"
                    )
            exempt.update(body)
            open_at = None
    if open_at is not None:
        violations.append(
            f"line {open_at}: {PROSE_GUARD_EXEMPTION_BEGIN} was never closed; "
            "the region exempts nothing"
        )
    non_blank = [
        i
        for i, raw in enumerate(lines, start=1)
        if raw.strip() and not _is_any_marker_line(raw)
    ]
    exempt_non_blank = [i for i in non_blank if i in exempt]
    if non_blank and len(exempt_non_blank) * 2 > len(non_blank):
        violations.append(
            "prose-guard exemption regions cover more than half the document; "
            "an exemption region may not swallow the document"
        )
    if violations:
        return set(), violations
    return exempt, violations


def find_enforcement_overclaims(text, name="<text>"):
    """Return a list of human-readable overclaim findings for `text`.

    Multi-line claims are caught by joining consecutive non-blank lines into a
    logical block before clause splitting.
    """
    lines = text.splitlines()
    exempt, findings = _resolve_exemption_regions(lines)
    findings = [f"{name}: {v}" for v in findings]

    blocks = []  # (start_lineno, joined_text)
    current, start = [], None
    for lineno, raw in enumerate(lines, start=1):
        if lineno in exempt or not raw.strip():
            if current:
                blocks.append((start, " ".join(current)))
                current, start = [], None
            continue
        if _is_any_marker_line(raw):
            if current:
                blocks.append((start, " ".join(current)))
                current, start = [], None
            continue
        if start is None:
            start = lineno
        current.append(raw)
    if current:
        blocks.append((start, " ".join(current)))

    for start_lineno, block in blocks:
        normalized = _normalize_markdown(block)
        for clause in _CLAUSE_SPLIT_RE.split(normalized):
            clause = clause.strip()
            if not clause:
                continue
            low = clause.lower()
            match = _OVERCLAIM_RE.search(clause)
            governed = bool(
                match and _GOVERNING_DENIAL_RE.search(clause[: match.start()])
            )
            if match and not match.group("neg") and not governed:
                findings.append(
                    f"{name}:{start_lineno}: present-tense enforcement claim "
                    f"{match.group(0).strip()!r} in clause {clause.strip()!r}"
                )
                continue
            emphatic = _EMPHATIC_RE.search(clause)
            if emphatic and not emphatic.group("neg") and not emphatic.group(
                "dneg"
            ):
                findings.append(
                    f"{name}:{start_lineno}: emphatic enforcement claim "
                    f"{emphatic.group(0).strip()!r} in clause {clause.strip()!r}"
                )
                continue

            progressive = _PROGRESSIVE_RE.search(clause)
            if (
                progressive
                and not progressive.group("neg")
                and not progressive.group("pneg")
            ):
                findings.append(
                    f"{name}:{start_lineno}: progressive enforcement claim "
                    f"{progressive.group(0).strip()!r} in clause "
                    f"{clause.strip()!r}"
                )
                continue

            passive = _PASSIVE_RE.search(clause)
            if passive and not passive.group("neg1") and not passive.group("neg2"):
                # No manner-adverb carve-out: an affirmative passive
                # enforcement claim is rejected in every adverb position.
                findings.append(
                    f"{name}:{start_lineno}: passive enforcement claim "
                    f"{passive.group(0).strip()!r} in clause "
                    f"{clause.strip()!r}"
                )
                continue

            for literal in _OVERCLAIM_LITERALS:
                if literal in low:
                    findings.append(
                        f"{name}:{start_lineno}: present-tense enforcement claim "
                        f"{literal!r} in clause {clause.strip()!r}"
                    )
                    break
    return findings


class GateAConsumerStatusFields(unittest.TestCase):
    """51-57: the machine-readable truth about the missing consumer."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 51
    def test_consumer_status_is_not_implemented(self):
        self.assertEqual(
            self.contract["gate_a_authorization_consumer_status"], "NOT_IMPLEMENTED"
        )
        self.assertFalse(self.contract["gate_a_runtime_enforcement_exists"])

    # 52
    def test_consumer_is_marked_required(self):
        self.assertTrue(self.contract["gate_a_authorization_consumer_required"])

    # 53
    def test_consumer_path_is_pending(self):
        self.assertEqual(
            self.contract["gate_a_authorization_consumer_path"],
            "PENDING_IMPLEMENTATION",
        )
        self.assertEqual(
            self.contract["gate_a_consumer_integration_point"],
            "PENDING_ARCHITECTURAL_DECISION",
        )
        # A pending path must never be mistaken for a real one.
        self.assertFalse(
            (REPO_ROOT / "PENDING_IMPLEMENTATION").exists()
        )

    # 54
    def test_consumer_is_not_wired_to_stage1(self):
        self.assertFalse(
            self.contract["gate_a_authorization_consumer_wired_to_stage1"]
        )

    # 55
    def test_consumer_tests_are_not_implemented(self):
        self.assertEqual(
            self.contract["gate_a_authorization_consumer_tests_status"],
            "NOT_IMPLEMENTED",
        )
        self.assertFalse(
            self.contract[
                "gate_a_consumer_required_test_categories_implemented_in_this_pr"
            ]
        )

    # 56
    def test_document_tests_are_not_runtime_enforcement_tests(self):
        self.assertFalse(
            self.contract["contract_tests_are_runtime_enforcement_tests"],
            "this suite must never claim to prove runtime enforcement",
        )
        self.assertFalse(
            self.contract[
                "gate_a_authorization_verification_steps_are_current_runtime_behavior"
            ]
        )
        self.assertTrue(
            self.contract["gate_a_authorization_verification_steps_are_future_contract"]
        )

    # 57
    def test_authorization_without_consumer_is_invalid(self):
        self.assertFalse(self.contract["authorization_without_consumer_is_valid"])


class AuthorizationCannotOutrunTheConsumer(unittest.TestCase):
    """58-61: no shortcut makes the package runnable."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 58
    def test_owner_approval_without_consumer_is_invalid(self):
        self.assertFalse(self.contract["owner_approval_without_consumer_is_valid"])
        self.assertFalse(
            self.contract[
                "owner_approval_created_before_consumer_implementation_is_valid"
            ]
        )

    # 59
    def test_filling_sentinels_without_consumer_does_not_make_package_runnable(self):
        self.assertFalse(
            self.contract[
                "filling_sentinels_without_consumer_makes_package_runnable"
            ]
        )
        self.assertFalse(
            self.contract[
                "creating_authorization_files_without_consumer_makes_package_runnable"
            ]
        )
        # And the package still says so in prose.
        collapsed = " ".join(self.text.split())
        self.assertIn("Still not runnable.", collapsed)

    # 60
    def test_effective_authorization_before_consumer_is_prohibited(self):
        self.assertFalse(
            self.contract[
                "effective_authorization_before_consumer_steps_complete_allowed"
            ]
        )

    # 61
    def test_consumer_hard_stop_is_not_waivable(self):
        self.assertFalse(
            self.contract["gate_a_authorization_consumer_hard_stop_waivable"]
        )
        self.assertTrue(
            self.contract["gate_a_authorization_consumer_not_implemented_is_active"]
        )


class ConsumerHardStop(unittest.TestCase):
    """62-63: the new hard stop exists and the count is consistent."""

    def setUp(self):
        self.contract, self.text = _load_contract()
        self.stops = self.contract["authorization_hard_stop_conditions"]

    # 62
    def test_consumer_hard_stop_exists(self):
        self.assertIn(CONSUMER_HARD_STOP, self.stops)
        self.assertEqual(
            self.contract["first_evaluated_hard_stop"], CONSUMER_HARD_STOP
        )
        # It is documented in the hard-stop table too, not only in YAML.
        self.assertIn(CONSUMER_HARD_STOP, self.text)

    # 63
    def test_hard_stop_count_updated_consistently(self):
        self.assertEqual(len(self.stops), 24)
        self.assertEqual(len(set(self.stops)), 24, "hard stops must be unique")
        self.assertEqual(self.contract["authorization_hard_stop_count"], 24)
        # The markdown table must carry a row 24 as well.
        self.assertRegex(self.text, r"\|\s*24\s*\|")
        # The old count must not survive anywhere as a total.
        self.assertNotIn("all 23 hard stops", self.text)


class ConsumerPrecedesAuthorizationLifecycle(unittest.TestCase):
    """64-67: ordering constraints put implementation before authorization."""

    def setUp(self):
        self.contract, self.text = _load_contract()
        self.order = self.contract["authorization_lifecycle_order"]

    def _index_of(self, needle):
        for i, step in enumerate(self.order):
            if needle in step:
                return i
        raise AssertionError(f"lifecycle step not found: {needle}")

    # 64
    def test_consumer_implementation_precedes_record_creation(self):
        self.assertTrue(
            self.contract[
                "consumer_implementation_precedes_authorization_record_creation"
            ]
        )
        self.assertLess(
            self._index_of("implement the real Gate A authorization consumer"),
            self._index_of("create the external authorization record"),
        )

    # 65
    def test_consumer_merge_precedes_owner_approval(self):
        self.assertTrue(self.contract["consumer_merge_precedes_owner_approval"])
        self.assertTrue(
            self.contract["consumer_merge_required_before_authorization"]
        )
        self.assertLess(
            self._index_of("independently review and merge the consumer"),
            self._index_of("owner approves the exact digest"),
        )

    # 66
    def test_execution_framework_sha_selected_after_consumer_merge(self):
        self.assertTrue(
            self.contract["execution_framework_sha_selected_after_consumer_merge"]
        )
        self.assertLess(
            self._index_of("independently review and merge the consumer"),
            self._index_of(
                "select a new immutable execution framework SHA containing the consumer"
            ),
        )

    # 67
    def test_consumer_must_gate_the_model_invocation_path(self):
        self.assertTrue(self.contract["consumer_must_gate_model_invocation_path"])
        self.assertLess(
            self._index_of(
                "wire the consumer into the actual Stage 1 invocation path"
            ),
            self._index_of("only after preflight passes"),
        )
        self.assertIn(
            "be tested through the actual invocation boundary, not only as an isolated helper",
            self.contract["gate_a_consumer_acceptance_criteria"],
        )


class ConsumerIntegrationProof(unittest.TestCase):
    """68-71: the proof a future review must demand."""

    def setUp(self):
        self.contract, self.text = _load_contract()
        self.proof = self.contract["proof_required_before_authorization"]

    # 68
    def test_negative_zero_invocation_proof_required(self):
        self.assertTrue(self.contract["negative_zero_invocation_test_required"])
        self.assertTrue(
            any("remains zero when preflight fails" in p for p in self.proof)
        )
        self.assertIn(
            "consumer absent blocks execution",
            self.contract["gate_a_consumer_required_test_categories"],
        )

    # 69
    def test_positive_single_invocation_proof_required(self):
        self.assertTrue(self.contract["positive_single_invocation_test_required"])
        self.assertTrue(
            any(
                "exactly one invocation can occur only after successful preflight" in p
                for p in self.proof
            )
        )
        self.assertTrue(self.contract["consumer_integration_proof_required"])

    # 70
    def test_consumer_emits_deterministic_preflight_output(self):
        self.assertTrue(
            self.contract["consumer_deterministic_preflight_output_required"]
        )
        self.assertIn(
            "emit a deterministic structured preflight result",
            self.contract["gate_a_consumer_acceptance_criteria"],
        )

    # 71
    def test_stable_consumer_failure_codes_required(self):
        self.assertTrue(self.contract["consumer_stable_failure_codes_required"])
        self.assertIn(
            "include stable failure codes",
            self.contract["gate_a_consumer_acceptance_criteria"],
        )


class ConsumerAbsenceBlocksPreflight(unittest.TestCase):
    """72-73: absence and non-wiring each independently block."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 72
    def test_consumer_absence_blocks_preflight(self):
        self.assertTrue(self.contract["consumer_absence_blocks_preflight"])
        self.assertIn(
            "consumer absent blocks execution",
            self.contract["gate_a_consumer_required_test_categories"],
        )

    # 73
    def test_consumer_not_wired_blocks_preflight(self):
        self.assertTrue(self.contract["consumer_not_wired_blocks_preflight"])
        self.assertIn(
            "consumer not wired into invocation path blocks execution",
            self.contract["gate_a_consumer_required_test_categories"],
        )


class NoPresentTenseEnforcementClaims(unittest.TestCase):
    """74-75: repository-wide prose guard over the changed documents."""

    # 74
    def test_no_present_tense_runtime_enforcement_claims_in_changed_docs(self):
        offenders = []
        for path in CHANGED_DOCS:
            self.assertTrue(path.is_file(), f"changed doc missing: {path}")
            offenders.extend(
                find_enforcement_overclaims(
                    path.read_text(encoding="utf-8"), name=path.name
                )
            )
        self.assertEqual(
            offenders,
            [],
            "present-tense runtime-enforcement claims found:\n" + "\n".join(offenders),
        )

    # 75
    def test_workflow_runtime_not_described_as_enforcing_authorization(self):
        contract, text = _load_contract()
        self.assertEqual(contract["stage1_entrypoint"], "scripts/workflow-runtime.py")
        self.assertFalse(
            contract["stage1_entrypoint_performs_authorization_preflight"]
        )
        self.assertFalse(contract["workflow_runtime_enforces_authorization"])
        collapsed = " ".join(text.split())
        self.assertIn(
            "It does **not** claim that `scripts/workflow-runtime.py` performs, "
            "or has ever performed, any authorization preflight.",
            collapsed,
        )
        # And the real runtime file must genuinely contain no consumer.
        runtime = REPO_ROOT / "scripts" / "workflow-runtime.py"
        if runtime.is_file():
            body = runtime.read_text(encoding="utf-8", errors="replace")
            for marker in CONSUMER_IMPLEMENTATION_MARKERS:
                self.assertNotIn(
                    marker,
                    body,
                    f"{marker} appeared in workflow-runtime.py; the contract now "
                    "understates reality and must be updated",
                )


class Pr107ClaimsAreBounded(unittest.TestCase):
    """76-79: PR #107 is labeled for what it is."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 76
    def test_pr107_tests_are_labeled_contract_consistency_tests(self):
        self.assertTrue(self.contract["pr_107_tests_are_contract_consistency_tests"])
        self.assertIn("CONTRACT CONSISTENCY ONLY", self.text)

    # 77
    def test_pr107_does_not_claim_runtime_enforcement(self):
        self.assertFalse(self.contract["pr_107_implements_runtime_enforcement"])
        for claim in (
            "an authorization consumer exists",
            "Gate A is runtime-enforced",
            "owner approval can currently authorize a run",
            "digests are currently checked",
            "model invocation is currently blocked by authorization state",
            "Evidence 0016 is executable",
        ):
            self.assertIn(claim, self.contract["pr_107_does_not_prove"])
        for claim in (
            "the future authorization contract is fully specified",
            "the package remains non-runnable",
            "future consumer requirements are explicit",
        ):
            self.assertIn(claim, self.contract["pr_107_proves"])

    # 78
    def test_future_consumer_test_categories_are_enumerated(self):
        categories = self.contract["gate_a_consumer_required_test_categories"]
        self.assertGreaterEqual(len(categories), 17)
        self.assertEqual(len(set(categories)), len(categories))
        for required in (
            "valid authorization accepted",
            "missing record rejected",
            "missing approval rejected",
            "digest mismatch rejected",
            "unauthorized approver rejected",
            "framework mismatch rejected",
            "target mismatch rejected",
            "model mismatch rejected",
            "package digest mismatch rejected",
            "checklist digest mismatch rejected",
            "false safety flag rejected",
            "duplicate record rejected",
            "duplicate approval rejected",
            "pre-existing evidence output rejected",
            "positive proof that the model invocation cannot occur before preflight success",
        ):
            self.assertIn(required, categories)
        criteria = self.contract["gate_a_consumer_acceptance_criteria"]
        self.assertGreaterEqual(len(criteria), 24)
        self.assertIn("load exactly one authorization record", criteria)
        self.assertIn("load exactly one owner-approval artifact", criteria)
        self.assertIn("permit no retry", criteria)
        self.assertIn("perform no target writes", criteria)

    # 79
    def test_gate_d_cannot_begin_before_gate_a_consumer_passes(self):
        self.assertTrue(self.contract["gate_d_requires_gate_a_consumer_pass"])
        checklist = CHECKLIST_PATH.read_text(encoding="utf-8")
        collapsed = " ".join(checklist.split())
        self.assertIn(
            "No current runtime verifies this checklist's digest.", collapsed
        )
        self.assertIn(
            "Gate D must not begin unless the future Gate A consumer exists and "
            "has passed.",
            collapsed,
        )
        self.assertIn("this checklist governs no live run", collapsed)
        # The eight tripwires are untouched by this change.
        self.assertEqual(len(self.contract["stale_diagnosis_tripwires"]), 8)


class NoConsumerImplementedByThisPR(unittest.TestCase):
    """80: this PR adds no consumer, and the repo still contains none."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 80
    def test_no_consumer_implementation_file_is_added_by_this_pr(self):
        self.assertFalse(
            self.contract["consumer_implementation_file_added_by_this_pr"]
        )
        offenders = []
        for directory in RUNTIME_SOURCE_DIRS:
            root = REPO_ROOT / directory
            if not root.is_dir():
                continue
            for path in root.rglob("*"):
                if not path.is_file():
                    continue
                if path.suffix.lower() not in (".py", ".sh", ".yaml", ".yml", ".json"):
                    continue
                body = path.read_text(encoding="utf-8", errors="replace")
                for marker in CONSUMER_IMPLEMENTATION_MARKERS:
                    if marker in body:
                        offenders.append(f"{path.relative_to(REPO_ROOT)}: {marker}")
        self.assertEqual(
            offenders,
            [],
            "a Gate A authorization consumer appears to exist in runtime "
            "sources; the package's NOT_IMPLEMENTED claim would then be false "
            "and must be corrected:\n" + "\n".join(offenders),
        )
        # And the run-control artifacts still do not exist.
        self.assertFalse((REPO_ROOT / RUN_CONTROL_DIR).exists())


# ---------------------------------------------------------------------------
# Round 5: stale authority path + prose-guard bypass regressions
# ---------------------------------------------------------------------------

STALE_AUTH_RECORD_PATH = (
    "docs/experiments/STAGE-1-AUTEUR-EVIDENCE-0016-AUTHORIZATION-RECORD.md"
)
STALE_AUTH_RECORD_STEM = "STAGE-1-AUTEUR-EVIDENCE-0016-AUTHORIZATION-RECORD"

# The five bypasses an independent reviewer demonstrated against the old
# line-level exemption. Every one must now be rejected.
KNOWN_BYPASS_STRINGS = (
    "Gate A verifies the authorization digest; unauthorized runs are prohibited.",
    "The runner recomputes SHA-256, but it must not accept a mismatch.",
    "The runtime blocks unauthorized invocation; this wording did not exist before.",
    "Gate A compares the approved digest - an unimplemented consumer must not "
    "be bypassed.",
    "workflow-runtime.py performs authorization checks; manual approval is "
    "prohibited.",
)

TRUTHFUL_STRINGS = (
    "The future Gate A consumer must verify the authorization digest.",
    "The required consumer will recompute SHA-256 before invocation.",
    "No current runner verifies the authorization record.",
    "Gate A verification is not implemented.",
    "The contract requires the future consumer to compare the approved digest.",
    "No runtime component checks the authorization record today.",
    "Gate A authorization verification is a future contract, not current behavior.",
)


def _exempt_begin(reason="quoted obsolete wording"):
    """A well-formed opening marker line carrying an allowed reason."""
    return f'{PROSE_GUARD_EXEMPTION_BEGIN} reason="{reason}"'


def _exemption_region(body, reason="quoted obsolete wording"):
    return f"{_exempt_begin(reason)}\n{body}\n{PROSE_GUARD_EXEMPTION_END}\n"


class StaleAuthorizationPathIsGone(unittest.TestCase):
    """80-83: exactly one canonical planned run-control location."""

    def _repo_text_files(self):
        skip = {".git", "node_modules", "__pycache__", ".pytest_cache", ".venv"}
        for path in REPO_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip for part in path.parts):
                continue
            if path.resolve() == Path(__file__).resolve():
                continue  # this module names the stale path to forbid it
            if path.suffix.lower() not in (
                ".md",
                ".py",
                ".yaml",
                ".yml",
                ".json",
                ".txt",
                ".sh",
            ):
                continue
            yield path

    # 80
    def test_stale_authorization_record_path_absent_repository_wide(self):
        offenders = []
        for path in self._repo_text_files():
            body = path.read_text(encoding="utf-8", errors="replace")
            for lineno, line in enumerate(body.splitlines(), start=1):
                if STALE_AUTH_RECORD_STEM in line:
                    offenders.append(f"{path.relative_to(REPO_ROOT)}:{lineno}")
        self.assertEqual(
            offenders,
            [],
            "the obsolete authorization-record path must not appear in any "
            "checked-in file:\n" + "\n".join(offenders),
        )

    # 81
    def test_stale_path_absent_from_each_changed_document(self):
        for path in CHANGED_DOCS:
            self.assertNotIn(
                STALE_AUTH_RECORD_PATH,
                path.read_text(encoding="utf-8"),
                f"stale authorization-record path present in {path.name}",
            )
            self.assertNotIn(
                STALE_AUTH_RECORD_STEM, path.read_text(encoding="utf-8")
            )

    # 82
    def test_exactly_one_canonical_authorization_location(self):
        """Every authorization artifact reference resolves under RUN_CONTROL_DIR."""
        pattern = re.compile(
            r"[\w./-]*(?:authorization-record\.(?:yaml|sha256)|owner-approval\.md)"
        )
        bases = set()
        for path in CHANGED_DOCS:
            for match in pattern.findall(path.read_text(encoding="utf-8")):
                if "/" not in match:
                    continue  # bare filename, base supplied by surrounding prose
                bases.add(match.rsplit("/", 1)[0])
        self.assertTrue(bases, "no authorization artifact paths found at all")
        self.assertEqual(
            bases,
            {RUN_CONTROL_DIR},
            f"authorization artifacts must live under exactly one base; "
            f"found: {sorted(bases)}",
        )

    # 83
    def test_no_docs_experiments_authorization_record_reference(self):
        for path in CHANGED_DOCS:
            body = path.read_text(encoding="utf-8")
            self.assertNotIn("docs/experiments/STAGE-1-AUTEUR-EVIDENCE-0016", body)


class ProseGuardRejectsKnownBypasses(unittest.TestCase):
    """84: the five demonstrated bypasses."""

    # 84
    def test_five_known_bypass_strings_are_rejected(self):
        for text in KNOWN_BYPASS_STRINGS:
            with self.subTest(text=text):
                self.assertNotEqual(
                    find_enforcement_overclaims(text),
                    [],
                    f"known bypass slipped through the guard: {text!r}",
                )


class ProseGuardAdversarialVariants(unittest.TestCase):
    """85-95: formatting and placement must not evade detection."""

    def assertRejected(self, text):
        self.assertNotEqual(
            find_enforcement_overclaims(text), [], f"not detected: {text!r}"
        )

    def assertAccepted(self, text):
        self.assertEqual(
            find_enforcement_overclaims(text), [], f"false positive: {text!r}"
        )

    # 85
    def test_negative_token_before_the_false_claim(self):
        self.assertRejected(
            "Unauthorized runs are prohibited; Gate A verifies the digest."
        )
        self.assertRejected("This must not happen, but the runtime blocks it.")

    # 86
    def test_markdown_bold_does_not_evade(self):
        self.assertRejected("**Gate A verifies** the authorization digest.")
        self.assertRejected("_the runner recomputes_ the digest.")
        self.assertRejected("`Gate A` verifies the authorization digest.")

    # 87
    def test_claim_spanning_two_lines_does_not_evade(self):
        self.assertRejected("The runtime\nblocks unauthorized invocation.")
        self.assertRejected("Gate A\nverifies the authorization digest.")

    # 88
    def test_table_cell_does_not_evade(self):
        self.assertRejected(
            "| Gate | Behavior |\n| --- | --- |\n"
            "| A | Gate A verifies the digest; bypass is prohibited |\n"
        )

    # 89
    def test_bullet_does_not_evade(self):
        self.assertRejected("- Gate A validates the approved digest.")
        self.assertRejected("  * the runtime checks the authorization record.")

    # 90
    def test_proximity_to_example_or_quoted_grants_nothing(self):
        self.assertRejected("For example, Gate A verifies the digest.")
        self.assertRejected("Quoted below: Gate A verifies the digest.")
        self.assertRejected("Old wording, quoted: the runner recomputes the digest.")
        self.assertRejected("Example (future): the runtime blocks invocation.")

    # 91
    def test_claim_after_a_colon_does_not_evade(self):
        self.assertRejected("Gate A behavior: Gate A verifies the digest.")

    # 92
    def test_two_clauses_on_one_line_are_evaluated_independently(self):
        self.assertRejected("Gate A verifies the digest; this wording is prohibited.")
        self.assertRejected("This wording is prohibited; Gate A verifies the digest.")

    # 93
    def test_truthful_future_tense_on_the_same_line_stays_allowed(self):
        self.assertAccepted(
            "The future Gate A consumer must verify the digest, and no current "
            "runner verifies anything."
        )
        self.assertRejected(
            "The future Gate A consumer must verify the digest, but Gate A "
            "verifies it today."
        )

    # 94
    def test_all_truthful_forms_are_accepted(self):
        for text in TRUTHFUL_STRINGS:
            with self.subTest(text=text):
                self.assertAccepted(text)

    # 95a
    def test_governing_denial_must_be_adjacent(self):
        # Truthful: the denial directly governs the claim.
        self.assertAccepted(
            "It does not claim that workflow-runtime.py performs any preflight."
        )
        self.assertAccepted("This does not assert that Gate A verifies the digest.")
        # Not truthful: the same words in a different clause exempt nothing.
        self.assertRejected(
            "It does not claim that much; Gate A verifies the digest."
        )
        self.assertRejected(
            "Gate A verifies the digest, though it does not claim that."
        )
        self.assertRejected(
            "It does not claim that, in general, Gate A verifies the digest."
        )

    # 95
    def test_literal_enforcement_phrases_still_rejected(self):
        self.assertRejected("Gate A is runtime-enforced.")
        self.assertRejected("The authorization contract is currently enforced.")


class ProseGuardExemptionBoundaries(unittest.TestCase):
    """96-104: exemptions come only from well-formed explicit regions."""

    def assertRejected(self, text):
        self.assertNotEqual(
            find_enforcement_overclaims(text), [], f"not detected: {text!r}"
        )

    # 96
    def test_no_whole_line_exemption_remains(self):
        """Proximity words alone must never exempt a real overclaim."""
        for token in (
            "not",
            "did not",
            "must not",
            "prohibited",
            "example",
            "quoted",
            "old wording",
            "future",
            "required",
        ):
            with self.subTest(token=token):
                self.assertRejected(f"Gate A verifies the digest ({token}).")
                self.assertRejected(f"({token}) Gate A verifies the digest.")

    # 97
    def test_negative_context_marker_constant_is_gone(self):
        # The unsafe line-level exemption constant no longer exists.
        self.assertFalse(
            "NEGATIVE_CONTEXT_MARKERS" in globals(),
            "the unsafe line-level exemption constant must be deleted",
        )

    # 98
    def test_well_formed_region_exempts_only_enclosed_text(self):
        text = (
            "Truthful intro.\n"
            + _exemption_region("Gate A verifies the digest.")
            + "Truthful outro.\n"
        )
        self.assertEqual(find_enforcement_overclaims(text), [])

    # 99
    def test_region_requires_both_markers(self):
        opened_only = _exempt_begin() + "\nGate A verifies the digest.\n"
        self.assertNotEqual(find_enforcement_overclaims(opened_only), [])
        closed_only = "Gate A verifies the digest.\n" + PROSE_GUARD_EXEMPTION_END + "\n"
        self.assertNotEqual(find_enforcement_overclaims(closed_only), [])

    # 100
    def test_unclosed_region_exempts_nothing(self):
        findings = find_enforcement_overclaims(
            _exempt_begin() + "\nGate A verifies the digest.\n"
        )
        self.assertTrue(any("never closed" in f for f in findings), findings)
        self.assertTrue(any("Gate A verifies" in f for f in findings), findings)

    # 101
    def test_nested_regions_are_rejected(self):
        text = (
            f"{_exempt_begin()}\n{_exempt_begin()}\n"
            "Gate A verifies the digest.\n"
            f"{PROSE_GUARD_EXEMPTION_END}\n{PROSE_GUARD_EXEMPTION_END}\n"
        )
        findings = find_enforcement_overclaims(text)
        self.assertTrue(any("nested" in f for f in findings), findings)

    # 102
    def test_region_cannot_cover_the_whole_document(self):
        text = _exemption_region(
            "Gate A verifies the digest.\nThe runtime blocks invocation."
        )
        findings = find_enforcement_overclaims(text)
        self.assertTrue(any("more than half" in f for f in findings), findings)

    # 103
    def test_text_after_closing_marker_is_not_exempt(self):
        text = (
            "Truthful intro line one.\nTruthful intro line two.\n"
            "Truthful intro line three.\nTruthful intro line four.\n"
            + _exemption_region("Old wording lived here.")
            + "Gate A verifies the digest.\n"
        )
        findings = find_enforcement_overclaims(text)
        self.assertTrue(any("Gate A verifies" in f for f in findings), findings)

    # 104
    def test_marker_in_inline_code_or_prose_is_not_a_marker(self):
        inline_code = (
            f"We use `{_exempt_begin()}` here.\n"
            "Gate A verifies the digest.\n"
            f"We use `{PROSE_GUARD_EXEMPTION_END}` here.\n"
        )
        findings = find_enforcement_overclaims(inline_code)
        self.assertTrue(any("Gate A verifies" in f for f in findings), findings)

        dynamic_prose = (
            f"Authors may add {_exempt_begin()} to quote old text.\n"
            "Gate A verifies the digest.\n"
            f"Authors then add {PROSE_GUARD_EXEMPTION_END} to close it.\n"
        )
        findings = find_enforcement_overclaims(dynamic_prose)
        self.assertTrue(any("Gate A verifies" in f for f in findings), findings)


class ProseGuardFailureMessages(unittest.TestCase):
    """105: findings must name file, line, and matched phrase."""

    # 105
    def test_findings_include_name_line_and_phrase(self):
        findings = find_enforcement_overclaims(
            "Intro line.\nGate A verifies the digest.\n", name="DOC.md"
        )
        self.assertEqual(len(findings), 1, findings)
        self.assertIn("DOC.md:1", findings[0])
        self.assertIn("Gate A verifies", findings[0])


# ---------------------------------------------------------------------------
# Round 6: passive / emphatic / progressive bypass regressions
#
# An independent reviewer demonstrated that the round-5 guard understood only
# ACTIVE SIMPLE PRESENT claims. Rewriting the same false assertion as a passive
# ("The authorization digest is verified by Gate A"), as an emphatic
# ("Gate A does verify the digest") or as a progressive ("The runner is
# validating the approval") walked straight through it. Every string below is
# quoted verbatim from that review.
# ---------------------------------------------------------------------------

# All ten passive bypasses. Six name a runtime agent with "by ..."; four are
# agentless. All ten must be rejected outside a quoted-old-wording region.
PASSIVE_BYPASS_STRINGS = (
    "The authorization digest is verified by Gate A.",
    "SHA-256 is recomputed by the runner before invocation.",
    "Unauthorized model calls are blocked by the runtime.",
    "The approval identity is validated by workflow-runtime.py.",
    "The authorization record is checked before the model runs.",
    "The package and checklist digests are compared by Gate A.",
    "Owner approval is enforced by the current runner.",
    "Invocation is prevented when authorization fails.",
    "The target SHA is verified before execution.",
    "The record is loaded and validated by the system.",
)

# All seven emphatic-do and present-progressive bypasses.
AUXILIARY_BYPASS_STRINGS = (
    "Gate A does verify the digest.",
    "The runner does recompute SHA-256.",
    "The runtime does block unauthorized calls.",
    "Gate A's checking the digest now.",
    "Gate A is checking the digest now.",
    "The runner is validating the approval.",
    "workflow-runtime.py is performing authorization checks.",
)

# Truthful phrasings that MUST remain legal. If the guard rejected any of these
# it would be unusable: the package could not describe its own honest state.
ROUND6_TRUTHFUL_STRINGS = (
    "No current runner verifies the authorization digest.",
    "The authorization digest is not currently verified by any runtime consumer.",
    "The future Gate A consumer must verify the digest.",
    "The consumer will verify the digest only after implementation and review.",
    "The contract requires the future consumer to recompute SHA-256.",
    "Digest verification is not implemented.",
    # Round 7: rewritten from "is blocked procedurally because ..." into plainly
    # negative form. The old phrasing required a carve-out; this needs none.
    "The package remains non-runnable because no consumer exists.",
    "The authorization digest would be verified by a future consumer after merge.",
)

# Words the DELETED line-level exemption used to treat as absolving. None of
# them may exempt an affirmative passive, emphatic or progressive claim.
NON_EXEMPTING_CONTEXT_WORDS = (
    "not",
    "prohibited",
    "must not",
    "example",
    "old wording",
    "future",
    "required",
)


class ProseGuardScopeIsDeclared(unittest.TestCase):
    """106-107: the guard states its real, bounded scope -- no universal claim."""

    # 106
    def test_scope_statement_present_and_bounded(self):
        for path in (PACKAGE_PATH, EXEC_PACKAGE_PATH):
            collapsed = " ".join(path.read_text(encoding="utf-8").split())
            self.assertIn(
                "This deterministic guard covers the enumerated "
                "active-simple-present, emphatic-do, present-progressive, and "
                "affirmative-passive enforcement forms used by this package, "
                "with manner adverbs recognized in four positions drawn from a "
                "closed nine-word set. It is not a general English semantic "
                "analyzer.",
                collapsed,
                f"{path.name} must declare the guard's bounded scope",
            )

    # 107
    def test_scope_statement_makes_no_universal_claim(self):
        for path in (PACKAGE_PATH, EXEC_PACKAGE_PATH):
            low = path.read_text(encoding="utf-8").lower()
            for overclaim in (
                "detects all enforcement claims",
                "catches every",
                "universal detection",
                "general english parser",
                "semantically complete",
            ):
                self.assertNotIn(overclaim, low, f"{path.name}: {overclaim!r}")


class ProseGuardPassiveVoice(unittest.TestCase):
    """108-112: affirmative passive enforcement claims are rejected."""

    def assertRejected(self, text):
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(findings, f"NOT rejected: {text!r}")

    def assertAccepted(self, text):
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertEqual(findings, [], f"wrongly rejected: {text!r}")

    # 108
    def test_all_ten_passive_bypasses_are_rejected(self):
        self.assertEqual(len(PASSIVE_BYPASS_STRINGS), 10)
        for text in PASSIVE_BYPASS_STRINGS:
            with self.subTest(text=text):
                self.assertRejected(text)

    # 109
    def test_agentless_passive_is_rejected(self):
        # No "by <runtime>" agent at all: the claim still asserts the check
        # happens now, so it must not survive.
        for text in (
            "The authorization record is checked before the model runs.",
            "Invocation is prevented when authorization fails.",
            "The target SHA is verified before execution.",
        ):
            with self.subTest(text=text):
                self.assertRejected(text)

    # 110
    def test_negated_passive_is_allowed(self):
        for text in (
            "The authorization digest is not verified by any runtime consumer.",
            "The authorization digest is not currently verified by Gate A.",
            "SHA-256 is never recomputed by the current runner.",
            "The record is no longer checked by anything.",
        ):
            with self.subTest(text=text):
                self.assertAccepted(text)

    # 111
    def test_modal_and_future_passive_is_allowed(self):
        for text in (
            "The authorization digest would be verified by a future consumer "
            "after merge.",
            "SHA-256 must be recomputed by the future consumer.",
            "The digest will be compared by the consumer once it exists.",
            "The record should be validated by the implemented consumer.",
            "The identity may be verified by a later reviewer.",
        ):
            with self.subTest(text=text):
                self.assertAccepted(text)

    # 112
    def test_manner_adverb_carve_out_is_deleted(self):
        """Round 7: no manner adverb excuses an affirmative passive anywhere.

        Round 6 allowed an agentless "is blocked procedurally". That exception
        was bypassable via the pre-participle slot, so it is deleted rather
        than extended. Both agentless and agentful forms are now rejected, and
        the truthful sentence is expressed without a participle at all.
        """
        self.assertRejected(
            "The package is blocked procedurally because no consumer exists."
        )
        self.assertRejected("The package is blocked procedurally by Gate A.")
        self.assertRejected("The package is procedurally blocked by Gate A.")
        # The replacement wording is legal because it makes no passive claim.
        self.assertAccepted(
            "The package remains non-runnable because no consumer exists."
        )
        # The deleted carve-out constant must not come back.
        self.assertFalse(
            "_NONRUNTIME_MANNER" in globals(),
            "the manner-adverb carve-out constant must stay deleted",
        )


class ProseGuardAuxiliaryAndProgressive(unittest.TestCase):
    """113-117: emphatic-do and present-progressive claims are rejected."""

    def assertRejected(self, text):
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(findings, f"NOT rejected: {text!r}")

    def assertAccepted(self, text):
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertEqual(findings, [], f"wrongly rejected: {text!r}")

    # 113
    def test_all_seven_auxiliary_bypasses_are_rejected(self):
        self.assertEqual(len(AUXILIARY_BYPASS_STRINGS), 7)
        for text in AUXILIARY_BYPASS_STRINGS:
            with self.subTest(text=text):
                self.assertRejected(text)

    # 114
    def test_negated_emphatic_is_allowed(self):
        for text in (
            "Gate A does not verify the digest.",
            "The runner does not recompute SHA-256.",
            "No runner does verify the digest.",
        ):
            with self.subTest(text=text):
                self.assertAccepted(text)

    # 115
    def test_negated_progressive_is_allowed(self):
        for text in (
            "Gate A is not checking the digest.",
            "The runner is never validating the approval.",
            "workflow-runtime.py is not performing authorization checks.",
        ):
            with self.subTest(text=text):
                self.assertAccepted(text)

    # 116
    def test_contraction_is_expanded_to_progressive(self):
        self.assertRejected("Gate A's checking the digest now.")
        self.assertRejected("The runner's validating the approval.")
        # A curly apostrophe must behave identically to a straight one.
        self.assertRejected("Gate A’s checking the digest now.")

    # 117
    def test_ordinary_possessives_are_not_treated_as_progressive(self):
        # A possessive followed by a gerund NOUN, or by a plain noun, is not a
        # verb phrase and must not be rewritten into one.
        for text in (
            "Gate A's checking of the digest is not implemented.",
            "Gate A's checking procedure is documented only.",
            "Gate A's checking steps are enumerated below.",
            "Gate A's digest field is pending.",
            "The runner's validating logic does not exist.",
        ):
            with self.subTest(text=text):
                self.assertAccepted(text)


class ProseGuardExemptionGaming(unittest.TestCase):
    """118-120: nearby words never exempt an affirmative claim."""

    def assertRejected(self, text):
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(findings, f"NOT rejected: {text!r}")

    # 118
    def test_negative_context_words_do_not_exempt_claims(self):
        for word in NON_EXEMPTING_CONTEXT_WORDS:
            for claim in (
                "The authorization digest is verified by Gate A.",
                "The target SHA is verified before execution.",
                "Gate A does verify the digest.",
                "The runner is validating the approval.",
            ):
                for text in (
                    f"{word}: {claim}",
                    f"{claim} This is {word}.",
                    f"Note ({word}) -- {claim}",
                ):
                    with self.subTest(word=word, text=text):
                        self.assertRejected(text)

    # 119
    def test_truthful_clause_on_the_same_line_does_not_exempt_a_false_one(self):
        self.assertRejected(
            "No consumer exists yet; the authorization digest is verified by "
            "Gate A."
        )
        self.assertRejected(
            "Digest verification is not implemented, and SHA-256 is recomputed "
            "by the runner."
        )

    # 120
    def test_all_round6_truthful_forms_are_accepted(self):
        self.assertEqual(len(ROUND6_TRUTHFUL_STRINGS), 8)
        for text in ROUND6_TRUTHFUL_STRINGS:
            with self.subTest(text=text):
                self.assertEqual(
                    find_enforcement_overclaims(text, name="T.md"),
                    [],
                    f"wrongly rejected truthful form: {text!r}",
                )


class ProseGuardFormattingCoverage(unittest.TestCase):
    """121-134: formatting cannot hide a passive or auxiliary claim."""

    def assertRejected(self, text, label=""):
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(findings, f"NOT rejected ({label}): {text!r}")

    # 121
    def test_bold(self):
        self.assertRejected(
            "**The authorization digest is verified by Gate A.**", "bold"
        )
        self.assertRejected("__Gate A does verify the digest.__", "bold-underscore")

    # 122
    def test_italics(self):
        self.assertRejected(
            "*The authorization digest is verified by Gate A.*", "italic"
        )
        self.assertRejected("_The runner is validating the approval._", "italic-us")

    # 123
    def test_inline_code(self):
        self.assertRejected("The digest `is verified by` `Gate A`.", "inline-code")
        self.assertRejected(
            "`workflow-runtime.py` is performing authorization checks.",
            "inline-code-subject",
        )

    # 124
    def test_links(self):
        self.assertRejected(
            "The digest is verified by [Gate A](#gate-a).", "link-agent"
        )
        self.assertRejected(
            "[Gate A](#gate-a) does verify the digest.", "link-subject"
        )

    # 125
    def test_headings(self):
        self.assertRejected(
            "### The authorization digest is verified by Gate A", "heading"
        )
        self.assertRejected("# Gate A is checking the digest now", "heading-prog")

    # 126
    def test_tables(self):
        self.assertRejected(
            "| step | note |\n| 3 | SHA-256 is recomputed by the runner |\n",
            "table",
        )
        self.assertRejected(
            "| a | Gate A does verify the digest | b |\n", "table-emphatic"
        )

    # 127
    def test_bullets(self):
        self.assertRejected(
            "- The target SHA is verified before execution.\n", "bullet-dash"
        )
        self.assertRejected(
            "+ The runner is validating the approval.\n", "bullet-plus"
        )
        self.assertRejected(
            "1. Owner approval is enforced by the current runner.\n",
            "bullet-ordered",
        )

    # 128
    def test_blockquotes(self):
        self.assertRejected(
            "> The authorization record is checked before the model runs.\n",
            "blockquote",
        )
        self.assertRejected(">> Gate A does verify the digest.\n", "nested-blockquote")

    # 129
    def test_html_emphasis(self):
        self.assertRejected(
            "<b>The authorization digest is verified by Gate A.</b>", "html-b"
        )
        self.assertRejected(
            "<em>Gate A</em> does verify the digest.", "html-em-subject"
        )
        self.assertRejected(
            "<strong>The runner is validating the approval.</strong>", "html-strong"
        )

    # 130
    def test_parentheses(self):
        self.assertRejected(
            "See section 2 (the target SHA is verified before execution).", "parens"
        )
        self.assertRejected(
            "Note (Gate A does verify the digest) here.", "parens-emphatic"
        )

    # 131
    def test_em_dash_clauses(self):
        self.assertRejected(
            "Preflight runs -- the authorization digest is verified by Gate A.",
            "em-dash-ascii",
        )
        self.assertRejected(
            "Preflight runs — SHA-256 is recomputed by the runner.", "em-dash"
        )
        self.assertRejected(
            "Preflight runs – the runner is validating the approval.", "en-dash"
        )

    # 132
    def test_hard_wrapped_lines(self):
        self.assertRejected(
            "The authorization digest is verified by Gate A before any model\n"
            "invocation may proceed.\n",
            "hard-wrap",
        )

    # 133
    def test_subject_and_verb_split_across_adjacent_lines(self):
        for text in (
            "The authorization digest\nis verified by Gate A.\n",
            "The authorization digest is\nverified by Gate A.\n",
            "Gate A\ndoes verify the digest.\n",
            "Gate A does\nverify the digest.\n",
            "The runner is\nvalidating the approval.\n",
            "Gate A's\nchecking the digest now.\n",
        ):
            with self.subTest(text=text):
                self.assertRejected(text, "line-split")

    # 134
    def test_a_blank_line_still_separates_logical_blocks(self):
        # Truthful text on either side of a blank line must not be fused into a
        # false claim. Counterpart to 133: the line-joining rule must not
        # invent claims nobody wrote.
        findings = find_enforcement_overclaims(
            "Digest verification is not implemented.\n"
            "\n"
            "By Gate A, we mean the future consumer.\n",
            name="T.md",
        )
        self.assertEqual(findings, [], findings)


class ProseGuardRound6MarkerInteractions(unittest.TestCase):
    """135-139: only exact paired markers exempt passive/auxiliary claims."""

    def assertRejected(self, text, label=""):
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(findings, f"NOT rejected ({label}): {text!r}")

    # 135
    def test_well_formed_region_exempts_passive_and_auxiliary_claims(self):
        text = (
            "Honest intro: digest verification is not implemented.\n"
            "More honest framing so the region stays a minority of the text.\n"
            "No consumer exists, and none is wired into the invocation path.\n"
            f"{_exempt_begin()}\n"
            "The authorization digest is verified by Gate A.\n"
            "Gate A does verify the digest.\n"
            f"{PROSE_GUARD_EXEMPTION_END}\n"
            "Honest outro: no consumer exists.\n"
        )
        self.assertEqual(find_enforcement_overclaims(text, name="T.md"), [])

    # 136
    def test_claims_after_marker_closure_are_not_exempt(self):
        text = (
            "Honest framing line one.\n"
            "Honest framing line two.\n"
            "Honest framing line three.\n"
            f"{_exempt_begin()}\n"
            "Gate A is runtime-enforced.\n"
            f"{PROSE_GUARD_EXEMPTION_END}\n"
            "The authorization digest is verified by Gate A.\n"
            "Gate A does verify the digest.\n"
        )
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(any("passive" in f for f in findings), findings)
        self.assertTrue(any("emphatic" in f for f in findings), findings)

    # 137
    def test_claims_before_marker_opening_are_not_exempt(self):
        text = (
            "The runner is validating the approval.\n"
            "Honest framing line one.\n"
            "Honest framing line two.\n"
            f"{_exempt_begin()}\n"
            "Gate A is runtime-enforced.\n"
            f"{PROSE_GUARD_EXEMPTION_END}\n"
        )
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(any("progressive" in f for f in findings), findings)

    # 138
    def test_malformed_markers_exempt_nothing(self):
        # Unclosed, unopened, nested, misspelled and inline-code markers all
        # fail closed.
        cases = (
            f"{_exempt_begin()}\n"
            "The authorization digest is verified by Gate A.\n",
            "The authorization digest is verified by Gate A.\n"
            f"{PROSE_GUARD_EXEMPTION_END}\n",
            f"{_exempt_begin()}\n"
            f"{_exempt_begin()}\n"
            "Gate A does verify the digest.\n"
            f"{PROSE_GUARD_EXEMPTION_END}\n",
            "BEGIN_PROSE_GUARD_EXEMPTIONS\n"
            "The runner is validating the approval.\n"
            "END_PROSE_GUARD_EXEMPTIONS\n",
            # Reason omitted entirely.
            f"{PROSE_GUARD_EXEMPTION_BEGIN}\n"
            "The runner is validating the approval.\n"
            f"{PROSE_GUARD_EXEMPTION_END}\n",
            f"`{_exempt_begin()}`\n"
            "Gate A does verify the digest.\n"
            f"`{PROSE_GUARD_EXEMPTION_END}`\n",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertRejected(text, "malformed marker")

    # 139
    def test_region_may_not_swallow_a_passive_heavy_document(self):
        text = (
            f"{_exempt_begin()}\n"
            "The authorization digest is verified by Gate A.\n"
            "Gate A does verify the digest.\n"
            "The runner is validating the approval.\n"
            f"{PROSE_GUARD_EXEMPTION_END}\n"
            "One honest line.\n"
        )
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(
            any("more than half the document" in f for f in findings), findings
        )


class ProseGuardRound6RealDocuments(unittest.TestCase):
    """140: the extended guard passes on the actual changed documents."""

    # 140
    def test_changed_documents_have_no_passive_or_auxiliary_overclaims(self):
        for path in CHANGED_DOCS:
            with self.subTest(doc=path.name):
                findings = find_enforcement_overclaims(
                    path.read_text(encoding="utf-8"), name=path.name
                )
                self.assertEqual(findings, [], "\n".join(findings))


class ConsumerHardStopUnchangedByRound6(unittest.TestCase):
    """141-143: the round-6 prose work changed no safety semantics."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 141
    def test_consumer_hard_stop_semantics_unchanged(self):
        self.assertIn(CONSUMER_HARD_STOP, self.text)
        self.assertEqual(
            self.contract["gate_a_authorization_consumer_status"], "NOT_IMPLEMENTED"
        )
        self.assertTrue(self.contract["consumer_absence_blocks_preflight"])
        self.assertFalse(self.contract["package_runnable"])
        self.assertEqual(
            self.contract["execution_authorization_status"], "NOT_AUTHORIZED"
        )
        self.assertEqual(self.contract["package_status"], "PREPARED_NOT_RUN")

    # 142
    def test_readiness_classification_unchanged(self):
        self.assertEqual(
            self.contract["readiness_classification_before"], "Externally exercised"
        )

    # 143
    def test_no_authorization_artifacts_created_by_round6(self):
        self.assertFalse((REPO_ROOT / RUN_CONTROL_DIR).exists())
        self.assertFalse(
            (REPO_ROOT / self.contract["execution_authorization_record_path"]).exists()
        )
        self.assertFalse(
            (REPO_ROOT / self.contract["owner_approval_artifact_path"]).exists()
        )


# ---------------------------------------------------------------------------
# Round 7: pre-participle adverb bypass + honest exemption markers
#
# The sixth independent review demonstrated that the round-6 "procedurally"
# carve-out was bypassable, and that the exemption markers were misnamed. Every
# string below is quoted verbatim from that review.
# ---------------------------------------------------------------------------

# The seven strings from the sixth review, with the classification each must
# receive. Four of these (1, 2, 3, 6) wrongly PASSED before this round.
SEVEN_REVIEW_STRINGS = (
    ("Authorization is procedurally enforced.", "reject"),
    ("The digest is procedurally verified before invocation.", "reject"),
    ("Invocation is procedurally blocked by Gate A.", "reject"),
    ("The package is procedurally blocked because no consumer exists.", "reject"),
    # "prohibited" is deliberately NOT in the enforcement-participle lexicon: it
    # states a prohibition rather than asserting that an act of enforcement
    # happens now, and "unauthorized runs are prohibited" is truthful prose used
    # throughout these documents. Adding it would reject honest sentences. The
    # governing prose was rewritten so this form is unnecessary; the string is
    # classified as accepted, with the reason recorded here rather than hidden.
    ("Execution is procedurally prohibited pending consumer implementation.", "accept"),
    ("The digest is procedurally verified by the runtime.", "reject"),
    ("Authorization is blocked procedurally, but Gate A verifies the digest.", "reject"),
)

# The adverbs exercised in every declared position.
MATRIX_ADVERBS = (
    "procedurally",
    "automatically",
    "currently",
    "mechanically",
    "deterministically",
)

MIXED_CLAUSE_STRINGS = (
    "The package is not runnable, but the digest is procedurally verified.",
    "No consumer exists; nevertheless, Gate A automatically checks the record.",
    "Runtime enforcement is absent, although authorization is mechanically "
    "validated.",
    "This is only an example, but the digest is deterministically compared by "
    "Gate A.",
    "The future consumer must verify the record, and the runtime currently "
    "blocks invalid approval.",
)

GOVERNING_FILES = (PACKAGE_PATH, CHECKLIST_PATH, EXEC_PACKAGE_PATH)


class ProseGuardSevenReviewStrings(unittest.TestCase):
    """144: the exact seven strings from the sixth review."""

    # 144
    def test_seven_review_strings_are_classified_correctly(self):
        self.assertEqual(len(SEVEN_REVIEW_STRINGS), 7)
        for text, expected in SEVEN_REVIEW_STRINGS:
            with self.subTest(text=text):
                findings = find_enforcement_overclaims(text, name="T.md")
                if expected == "reject":
                    self.assertTrue(findings, f"NOT rejected: {text!r}")
                else:
                    self.assertEqual(findings, [], f"wrongly rejected: {text!r}")

    def test_the_two_agent_naming_bypasses_are_closed(self):
        """The two strings that named a runtime agent and still passed."""
        for text in (
            "Invocation is procedurally blocked by Gate A.",
            "The digest is procedurally verified by the runtime.",
        ):
            with self.subTest(text=text):
                findings = find_enforcement_overclaims(text, name="T.md")
                self.assertTrue(findings, f"agent-naming bypass survives: {text!r}")
                self.assertTrue(
                    any("passive" in f for f in findings),
                    f"expected a passive finding, got {findings}",
                )


class ProseGuardAdverbPositionMatrix(unittest.TestCase):
    """145: every adverb in every declared position, all four polarities."""

    def _matrix(self, adverb):
        return {
            "pre-participle": f"The digest is {adverb} verified.",
            "post-participle": f"The digest is verified {adverb}.",
            "pre-agent": f"The digest is verified {adverb} by Gate A.",
            "post-agent": f"The digest is verified by Gate A {adverb}.",
        }

    # 145
    def test_affirmative_claims_rejected_in_every_position(self):
        for adverb in MATRIX_ADVERBS:
            for position, text in self._matrix(adverb).items():
                with self.subTest(adverb=adverb, position=position):
                    self.assertTrue(
                        find_enforcement_overclaims(text, name="T.md"),
                        f"NOT rejected ({position}): {text!r}",
                    )

    def test_negated_forms_remain_allowed_in_every_position(self):
        for adverb in MATRIX_ADVERBS:
            for text in (
                f"The digest is not {adverb} verified.",
                f"The digest is not verified {adverb}.",
                f"The digest is never verified {adverb} by Gate A.",
                f"The digest is no longer verified by Gate A {adverb}.",
            ):
                with self.subTest(text=text):
                    self.assertEqual(
                        find_enforcement_overclaims(text, name="T.md"),
                        [],
                        f"wrongly rejected negated form: {text!r}",
                    )

    def test_future_and_required_forms_remain_allowed_in_every_position(self):
        for adverb in MATRIX_ADVERBS:
            for text in (
                f"The digest must be {adverb} verified by the future consumer.",
                f"The digest will be verified {adverb} once the consumer exists.",
                f"The digest would be verified {adverb} by Gate A after merge.",
                f"The future consumer should verify the digest {adverb}.",
            ):
                with self.subTest(text=text):
                    self.assertEqual(
                        find_enforcement_overclaims(text, name="T.md"),
                        [],
                        f"wrongly rejected future form: {text!r}",
                    )

    def test_exemption_region_is_the_only_bypass_for_every_position(self):
        for adverb in MATRIX_ADVERBS:
            for position, claim in self._matrix(adverb).items():
                with self.subTest(adverb=adverb, position=position):
                    exempted = (
                        "Honest framing line one.\n"
                        "Honest framing line two.\n"
                        "Honest framing line three.\n"
                        + _exemption_region(claim, "quoted obsolete wording")
                        + "Honest closing line.\n"
                    )
                    self.assertEqual(
                        find_enforcement_overclaims(exempted, name="T.md"), []
                    )

    def test_supported_adverb_set_and_positions_are_declared(self):
        self.assertEqual(len(MANNER_ADVERBS), 9)
        self.assertEqual(len(set(MANNER_ADVERBS)), 9)
        for adverb in MATRIX_ADVERBS:
            self.assertIn(adverb, MANNER_ADVERBS)
        self.assertEqual(len(SUPPORTED_PASSIVE_ADVERB_POSITIONS), 4)
        # An adverb OUTSIDE the closed set is not claimed to be supported, and
        # the guard does not pretend otherwise.
        self.assertEqual(
            find_enforcement_overclaims(
                "The digest is bureaucratically verified.", name="T.md"
            ),
            [],
            "the guard must not claim coverage of adverbs outside its closed set",
        )

    def test_declared_adverb_set_appears_in_governing_documents(self):
        for path in (PACKAGE_PATH, EXEC_PACKAGE_PATH):
            body = path.read_text(encoding="utf-8")
            for adverb in MANNER_ADVERBS:
                self.assertIn(
                    adverb, body, f"{path.name} must document adverb {adverb!r}"
                )
            collapsed = " ".join(body.split())
            self.assertIn("Adverb positions covered.", collapsed)
            self.assertIn("Supported manner-adverb set (exactly these nine).", collapsed)


class ProseGuardMixedClauseAdversarial(unittest.TestCase):
    """146: a truthful clause never exempts an affirmative false one."""

    # 146
    def test_mixed_clause_strings_are_rejected(self):
        self.assertEqual(len(MIXED_CLAUSE_STRINGS), 5)
        for text in MIXED_CLAUSE_STRINGS:
            with self.subTest(text=text):
                self.assertTrue(
                    find_enforcement_overclaims(text, name="T.md"),
                    f"mixed-clause bypass survives: {text!r}",
                )


class ExemptionMarkerRenameIsComplete(unittest.TestCase):
    """147: the old marker name is gone from every governing file."""

    # 147
    def test_old_marker_names_absent_from_governing_files(self):
        offenders = []
        for path in GOVERNING_FILES:
            body = path.read_text(encoding="utf-8")
            for lineno, line in enumerate(body.splitlines(), start=1):
                for old in OLD_MARKER_NAMES:
                    if old in line:
                        offenders.append(f"{path.name}:{lineno}: {old}")
        self.assertEqual(
            offenders,
            [],
            "the misleading marker name must not survive in governing files:\n"
            + "\n".join(offenders),
        )

    def test_new_markers_are_actually_used(self):
        used = [
            path.name
            for path in GOVERNING_FILES
            if PROSE_GUARD_EXEMPTION_BEGIN in path.read_text(encoding="utf-8")
        ]
        self.assertTrue(used, "the renamed marker is not used anywhere")

    def test_every_marker_use_declares_an_allowed_reason(self):
        for path in GOVERNING_FILES:
            lines = path.read_text(encoding="utf-8").splitlines()
            for lineno, raw in enumerate(lines, start=1):
                if PROSE_GUARD_EXEMPTION_BEGIN not in raw:
                    continue
                if "`" in raw:
                    continue  # inline-code mention, not a marker
                verdict = _match_exemption_begin(raw)
                self.assertIsNotNone(verdict, f"{path.name}:{lineno}: not a marker")
                kind, payload = verdict
                self.assertEqual(
                    kind, "ok", f"{path.name}:{lineno}: {payload}"
                )
                self.assertIn(payload, ALLOWED_EXEMPTION_REASONS)

    def test_governing_files_have_no_overclaims_after_the_rename(self):
        for path in GOVERNING_FILES:
            with self.subTest(doc=path.name):
                findings = find_enforcement_overclaims(
                    path.read_text(encoding="utf-8"), name=path.name
                )
                self.assertEqual(findings, [], "\n".join(findings))


class ExemptionMarkerReasonSemantics(unittest.TestCase):
    """148: the reason schema fails closed in every direction."""

    CLAIM = "The authorization digest is verified by Gate A."

    def _doc(self, begin_line, body=None):
        return (
            "Honest framing line one.\n"
            "Honest framing line two.\n"
            "Honest framing line three.\n"
            f"{begin_line}\n"
            f"{self.CLAIM if body is None else body}\n"
            f"{PROSE_GUARD_EXEMPTION_END}\n"
            "Honest closing line.\n"
        )

    def assertNotExempted(self, text, label):
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(findings, f"wrongly exempted ({label}): {text!r}")

    # 148
    def test_well_formed_reason_exempts(self):
        for reason in ALLOWED_EXEMPTION_REASONS:
            with self.subTest(reason=reason):
                self.assertEqual(
                    find_enforcement_overclaims(
                        self._doc(_exempt_begin(reason)), name="T.md"
                    ),
                    [],
                )

    def test_missing_reason_fails(self):
        self.assertNotExempted(
            self._doc(PROSE_GUARD_EXEMPTION_BEGIN), "missing reason"
        )

    def test_blank_reason_fails(self):
        self.assertNotExempted(self._doc(_exempt_begin("")), "blank reason")
        self.assertNotExempted(self._doc(_exempt_begin("   ")), "whitespace reason")

    def test_unknown_reason_fails(self):
        self.assertNotExempted(
            self._doc(_exempt_begin("because I said so")), "unknown reason"
        )

    def test_reason_without_quotes_fails(self):
        self.assertNotExempted(
            self._doc(f"{PROSE_GUARD_EXEMPTION_BEGIN} reason=truthful denial list"),
            "unquoted reason",
        )

    def test_nested_regions_fail(self):
        text = (
            "Honest framing line one.\n"
            "Honest framing line two.\n"
            "Honest framing line three.\n"
            f"{_exempt_begin()}\n"
            f"{_exempt_begin()}\n"
            f"{self.CLAIM}\n"
            f"{PROSE_GUARD_EXEMPTION_END}\n"
            f"{PROSE_GUARD_EXEMPTION_END}\n"
        )
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(any("nested" in f for f in findings), findings)

    def test_unmatched_open_fails(self):
        findings = find_enforcement_overclaims(
            f"{_exempt_begin()}\n{self.CLAIM}\n", name="T.md"
        )
        self.assertTrue(any("never closed" in f for f in findings), findings)

    def test_unmatched_close_fails(self):
        findings = find_enforcement_overclaims(
            f"{self.CLAIM}\n{PROSE_GUARD_EXEMPTION_END}\n", name="T.md"
        )
        self.assertTrue(
            any("without a matching" in f for f in findings), findings
        )

    def test_oversized_region_fails(self):
        body = "\n".join([self.CLAIM] * (MAX_EXEMPTION_REGION_LINES + 1))
        padding = "\n".join(f"Honest framing line {i}." for i in range(40))
        text = padding + "\n" + self._doc(_exempt_begin(), body)
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(
            any("more than the" in f and "maximum" in f for f in findings), findings
        )

    def test_authoritative_requirement_inside_region_fails(self):
        text = self._doc(
            _exempt_begin("quoted obsolete wording"),
            "The consumer must recompute the digest before invocation.",
        )
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(
            any("authoritative requirement" in f for f in findings), findings
        )

    def test_region_may_not_cover_whole_document(self):
        findings = find_enforcement_overclaims(
            _exemption_region(f"{self.CLAIM}\nGate A does verify the digest."),
            name="T.md",
        )
        self.assertTrue(
            any("more than half the document" in f for f in findings), findings
        )

    def test_text_after_closing_marker_is_scanned(self):
        text = self._doc(_exempt_begin(), "Old wording lived here.") + self.CLAIM + "\n"
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(any("passive" in f for f in findings), findings)

    def test_markers_inside_inline_code_do_not_activate(self):
        text = (
            f"We document `{_exempt_begin()}` here.\n"
            f"{self.CLAIM}\n"
            f"We document `{PROSE_GUARD_EXEMPTION_END}` here.\n"
        )
        self.assertNotExempted(text, "inline code")

    def test_markers_in_quoted_prose_do_not_activate(self):
        text = (
            f"Authors may add {_exempt_begin()} to exempt text.\n"
            f"{self.CLAIM}\n"
            f"Authors then add {PROSE_GUARD_EXEMPTION_END} to close it.\n"
        )
        self.assertNotExempted(text, "prose mention")

    def test_near_miss_marker_names_do_not_activate(self):
        for begin, end in (
            ("BEGIN_PROSE_GUARD_EXEMPTIONS", "END_PROSE_GUARD_EXEMPTIONS"),
            ("BEGIN_PROSE_GUARD_EXEMPT", "END_PROSE_GUARD_EXEMPT"),
            ("BEGIN_QUOTED_OLD_WORDING", "END_QUOTED_OLD_WORDING"),
        ):
            with self.subTest(begin=begin):
                self.assertNotExempted(
                    f"{begin}\n{self.CLAIM}\n{end}\n", "near miss"
                )


class Round7ChangedNoSafetySemantics(unittest.TestCase):
    """149: the round-7 prose work changed no safety semantics."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 149
    def test_consumer_hard_stop_and_status_unchanged(self):
        self.assertIn(CONSUMER_HARD_STOP, self.text)
        self.assertEqual(
            self.contract["first_evaluated_hard_stop"], CONSUMER_HARD_STOP
        )
        self.assertEqual(
            self.contract["gate_a_authorization_consumer_status"], "NOT_IMPLEMENTED"
        )
        self.assertTrue(self.contract["consumer_absence_blocks_preflight"])
        self.assertFalse(self.contract["package_runnable"])
        self.assertEqual(
            self.contract["execution_authorization_status"], "NOT_AUTHORIZED"
        )
        self.assertEqual(self.contract["package_status"], "PREPARED_NOT_RUN")
        self.assertEqual(
            self.contract["readiness_classification_before"], "Externally exercised"
        )

    def test_no_authorization_artifacts_created_by_round7(self):
        self.assertFalse((REPO_ROOT / RUN_CONTROL_DIR).exists())
        self.assertFalse(
            (REPO_ROOT / self.contract["execution_authorization_record_path"]).exists()
        )
        self.assertFalse(
            (REPO_ROOT / self.contract["owner_approval_artifact_path"]).exists()
        )
        self.assertFalse(
            (REPO_ROOT / self.contract["execution_authorization_record_digest_path"])
            .exists()
        )


if __name__ == "__main__":
    unittest.main()
