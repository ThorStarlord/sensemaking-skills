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
        self.assertIn("BLOCKED while execution_framework_sha is unset", self.text)

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
# them, and the Gate A verification that enforces it before invocation.
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
            self.assertIn(f"blocked while", self.text)
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
        self.assertIn(
            "Digest verification occurs BEFORE model invocation.", self.text
        )

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

    def test_all_twentythree_hard_stops_declared(self):
        self.assertEqual(len(self.stops), 23)
        self.assertEqual(len(set(self.stops)), 23)
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
            "no authorization record exists. No owner approval exists.", collapsed
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


if __name__ == "__main__":
    unittest.main()
