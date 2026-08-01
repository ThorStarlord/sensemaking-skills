"""Deterministic validation of the Stage 1 auteur post-remediation preparation package.

These tests verify that the preparation package is internally consistent and
that it cannot silently drift into something that looks like a completed run.

They are deliberately offline and side-effect free: they read repository files
only. They never invoke a model, never run the Stage 1 workflow, and never
create an evidence directory.
"""

import hashlib
import inspect
import re
import tempfile
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
        # A drafted record does not fill this block. The operative approval is
        # what would, and it does not exist.
        self.assertFalse(self.contract["owner_approval_artifact_exists"])
        self.assertEqual(
            self.contract["execution_authorization_status"], "NOT_AUTHORIZED"
        )

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
OWNER_APPROVAL_TEMPLATE_PATH = f"{RUN_CONTROL_DIR}/owner-approval.template.md"

# The EXACT set of draft artifacts permitted to exist under run-control before
# owner approval. This is an allowlist, not a prefix rule: anything else under
# experiments/run-control/ -- extra records, extra digests, an operative
# owner-approval.md, a second run-control directory -- is a violation.
#
# These are paths RELATIVE TO THE RUN-CONTROL DIRECTORY ROOT, not bare
# filenames. Comparing bare names would let a nested duplicate (for example
# `nested/authorization-record.yaml`) collide with the permitted top-level
# entry of the same name and pass unnoticed -- exactly the "duplicate
# authorization records" / "duplicate digest files" case this guard must catch.
PERMITTED_RUN_CONTROL_FILES = frozenset(
    {
        ".gitattributes",
        "authorization-record.yaml",
        "authorization-record.sha256",
        "owner-approval.template.md",
    }
)


def _relative_file_paths(root):
    """Every file under `root`, as a POSIX path relative to `root`.

    Relative -- never bare `.name` -- so that a nested duplicate of a permitted
    filename is a distinct entry instead of silently colliding with it.
    """
    return {
        str(p.relative_to(root)).replace("\\", "/")
        for p in root.rglob("*")
        if p.is_file()
    }


def _assert_only_permitted_run_control_artifacts(case):
    """Exactly one run-control directory, holding exactly the draft artifacts.

    Existence of the draft record and digest is NOT authority; it only means
    the authorization proposal has stable bytes. The operative approval
    (owner-approval.md) must be absent.
    """
    root = REPO_ROOT / "experiments" / "run-control"
    case.assertTrue(root.is_dir(), "the run-control root must exist")
    subdirs = sorted(p.name for p in root.iterdir() if p.is_dir())
    case.assertEqual(
        subdirs,
        ["0016-stage1-auteur-post-remediation-controlled-attempt"],
        "exactly one run-control directory is permitted",
    )
    case.assertEqual(
        sorted(p.name for p in root.iterdir() if p.is_file()),
        [],
        "no stray files directly under experiments/run-control/",
    )
    run_control_root = REPO_ROOT / RUN_CONTROL_DIR
    # Relative paths, so a nested duplicate is a DISTINCT entry rather than one
    # that collides with the permitted top-level name.
    found = _relative_file_paths(run_control_root)
    case.assertEqual(
        found,
        set(PERMITTED_RUN_CONTROL_FILES),
        "only the exact planned draft artifact set may exist under run-control",
    )
    # No subdirectories either: the planned artifact set is flat, so any
    # directory under the run-control root can only be hiding something.
    case.assertEqual(
        sorted(
            str(p.relative_to(run_control_root)).replace("\\", "/")
            for p in run_control_root.rglob("*")
            if p.is_dir()
        ),
        [],
        "no subdirectories are permitted under the run-control directory",
    )
    # The operative approval is owner-only and must never be authored here.
    case.assertFalse((REPO_ROOT / OWNER_APPROVAL_PATH).exists())


class NestedDuplicateRunControlArtifactsAreCaught(unittest.TestCase):
    """Regression: the allowlist must compare RELATIVE PATHS, not bare names.

    A prior version of `_assert_only_permitted_run_control_artifacts` collected
    `p.name`. Because a nested duplicate has the same bare name as the
    permitted top-level file, `{"authorization-record.yaml", ...}` was produced
    either way and the whole suite passed with a duplicate authorization record
    and duplicate digest sitting in a subdirectory -- both explicitly on the
    must-catch list from the owner decision.
    """

    PERMITTED = {
        ".gitattributes",
        "authorization-record.yaml",
        "authorization-record.sha256",
        "owner-approval.template.md",
    }

    def _build(self, tmp, nested):
        root = Path(tmp) / "0016-stage1-auteur-post-remediation-controlled-attempt"
        root.mkdir(parents=True)
        for name in self.PERMITTED:
            (root / name).write_text("x", encoding="utf-8")
        if nested:
            sub = root / "nested"
            sub.mkdir()
            (sub / "authorization-record.yaml").write_text("x", encoding="utf-8")
            (sub / "authorization-record.sha256").write_text("x", encoding="utf-8")
        return root

    def test_clean_tree_matches_the_allowlist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._build(tmp, nested=False)
            self.assertEqual(_relative_file_paths(root), self.PERMITTED)

    def test_nested_duplicate_record_and_digest_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._build(tmp, nested=True)
            found = _relative_file_paths(root)
            self.assertNotEqual(
                found,
                self.PERMITTED,
                "nested duplicates must make the allowlist comparison fail",
            )
            self.assertEqual(
                found - self.PERMITTED,
                {
                    "nested/authorization-record.yaml",
                    "nested/authorization-record.sha256",
                },
            )

    def test_bare_name_comparison_would_have_missed_them(self):
        """Pins the exact defect, so a revert to `p.name` fails loudly."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._build(tmp, nested=True)
            bare = {p.name for p in root.rglob("*") if p.is_file()}
            self.assertEqual(
                bare,
                self.PERMITTED,
                "bare-name collection is blind to nested duplicates -- this is "
                "why the guard must use relative paths",
            )


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
        # The stop stays declared even though a draft record now exists: the
        # stop governs the run-time check, not today's repository state. What
        # keeps the run blocked today is the absent owner approval.
        self.assertTrue(self.contract["execution_authorization_record_exists"])
        self.assertFalse(self.contract["owner_approval_artifact_exists"])
        self.assertFalse(self.contract["package_runnable"])

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

    # 46 -- the draft record and digest exist, and the contract says so
    # truthfully. Existence is not authority: the record is a proposal with
    # stable bytes, nothing more.
    def test_draft_authorization_record_exists_and_contract_is_truthful(self):
        record = REPO_ROOT / self.contract["execution_authorization_record_path"]
        digest = REPO_ROOT / self.contract["execution_authorization_record_digest_path"]
        self.assertTrue(record.is_file())
        self.assertTrue(digest.is_file())
        self.assertTrue(self.contract["execution_authorization_record_exists"])
        self.assertTrue(self.contract["execution_authorization_record_digest_exists"])
        # The digest file must be a current digest of the record's exact bytes,
        # never a stale one carried over from an earlier draft.
        stored = digest.read_text(encoding="utf-8").strip()
        self.assertTrue(HEX64.match(stored), stored)
        self.assertEqual(
            stored,
            hashlib.sha256(record.read_bytes()).hexdigest(),
            "authorization-record.sha256 is stale relative to the record bytes",
        )
        # A record on disk does not authorize anything. The owner-approval
        # sentinel in the package must still be pending.
        self.assertEqual(
            self.contract["authorization_record_sha256"], OWNER_APPROVAL_SENTINEL
        )

    # 47 -- the operative owner approval still does not exist, and nothing
    # beyond the exact planned draft artifact set does either.
    def test_no_owner_approval_artifact_exists_in_this_pr(self):
        self.assertFalse(
            (REPO_ROOT / self.contract["owner_approval_artifact_path"]).exists()
        )
        self.assertFalse(self.contract["owner_approval_artifact_exists"])
        self.assertTrue((REPO_ROOT / self.contract["run_control_directory"]).is_dir())
        self.assertTrue(self.contract["run_control_directory_exists"])
        _assert_only_permitted_run_control_artifacts(self)

    # 47b -- the package's declared preparation-package digest inside the
    # record must match the package's CURRENT bytes.
    def test_record_pins_the_current_preparation_package_bytes(self):
        record_text = (
            REPO_ROOT / self.contract["execution_authorization_record_path"]
        ).read_text(encoding="utf-8")
        pinned = yaml.safe_load(record_text)["preparation_package_sha256"]
        self.assertEqual(
            pinned,
            hashlib.sha256(PACKAGE_PATH.read_bytes()).hexdigest(),
            "the authorization record pins a stale preparation-package digest",
        )

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
        # The consumer now exists, so the enforceability half of this sentence
        # flipped. So did the record/digest half: a DRAFT record and digest now
        # exist, and saying otherwise would be false. The half that actually
        # gates execution -- no operative approval binding the record digest,
        # no pin, not runnable -- did not.
        self.assertIn(
            "a Gate A authorization consumer exists and is enforcing, so "
            "authorization state is now enforceable. A draft authorization "
            "record and its digest file exist, and neither is operative. "
            "Authorization requires an owner approval binding the exact "
            "current record digest, and none binds it. No execution pin is "
            "finalized. The package is not runnable.",
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
        """The fixture is in-memory only; it writes no run-control artifact."""
        before = sorted(
            p.name for p in (REPO_ROOT / RUN_CONTROL_DIR).rglob("*") if p.is_file()
        )
        validate_future_authorization_record(
            valid_future_authorization_record(), EXPECTED_AUTHORIZED_INPUTS
        )
        after = sorted(
            p.name for p in (REPO_ROOT / RUN_CONTROL_DIR).rglob("*") if p.is_file()
        )
        self.assertEqual(before, after, "the fixture must not write to disk")
        self.assertFalse((REPO_ROOT / OWNER_APPROVAL_PATH).exists())
        _assert_only_permitted_run_control_artifacts(self)


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
def enforcement_claims_are_permitted():
    """Whether the changed documents may state Gate A enforcement in the present tense.

    The prose guard exists to stop this package claiming enforcement it does
    not have. Its correct scope is therefore CONDITIONAL, not absolute:

    * while the consumer is NOT_IMPLEMENTED, any present-tense enforcement
      claim is false and must be rejected -- this is the original defect the
      guard was written to catch;
    * once the consumer is implemented, wired, and proven at the invocation
      boundary, such a claim is simply true, and a guard that still rejected
      it would force the document to UNDERSTATE reality -- the mirror image of
      the same defect.

    The guard is not weakened by this. Revert or unwire the consumer and every
    present-tense claim in these documents becomes a test failure again,
    because this helper reads the live contract and checks the real files.
    """
    contract, _ = _load_contract()
    if contract["gate_a_authorization_consumer_status"] != "IMPLEMENTED":
        return False
    if not contract["gate_a_authorization_consumer_wired_to_stage1"]:
        return False
    if not contract["gate_a_runtime_enforcement_exists"]:
        return False
    # Claiming enforcement requires the enforcing code AND its boundary proof.
    return (
        (REPO_ROOT / "scripts" / "gate_a_authorization.py").is_file()
        and (REPO_ROOT / "tests" / "test_gate_a_invocation_boundary.py").is_file()
    )


def assert_no_unpermitted_overclaims(testcase, findings, label):
    """Reject enforcement claims unless the consumer genuinely backs them."""
    if enforcement_claims_are_permitted():
        return
    testcase.assertEqual(
        findings,
        [],
        f"present-tense runtime-enforcement claims in {label} while the Gate A "
        f"consumer is not implemented and wired:\n" + "\n".join(findings),
    )


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
# PREMISE MIGRATION NOTE (post-PR #109).
#
# Everything below was built on one historical premise: that no Gate A
# authorization consumer existed, and therefore that ANY present-tense sentence
# pairing a runtime subject with an enforcement verb was false. PR #109 merged
# `scripts/gate_a_authorization.py` and wired it into `scripts/skill_executor.py`
# at both provider boundaries, so that premise no longer holds. Under it, the
# TRUE sentence "The runtime verifies the Gate D checklist digest." is rejected,
# and the only way to state a true fact is to hide it inside a ```text fence the
# scanner skips -- the exact evasion rounds 5-8 closed for false claims.
#
# The GOVERNING current-state check has therefore moved to
# `tests/support/state_honesty_guard.py`, which derives authoritative state facts
# from real files and the contract block and rejects prose that CONTRADICTS them,
# in either direction, inside code fences as well as outside. Its self-tests live
# in `tests/test_state_honesty_guard.py`.
#
# The detector below is deliberately NOT deleted. It remains the correct guard
# for the world in which the consumer is absent, and `enforcement_claims_are_
# permitted()` keeps it conditional on the live repository contract: revert or
# unwire the consumer and it governs the documents again. Its ten rounds of
# adversarial tests continue to run against synthetic fixtures, so its hardening
# is preserved rather than discarded. What changed is its AUTHORITY over the
# governed documents while the consumer exists, not its correctness.
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
# Round 8 remediation: a reason is a CONTRACT, not a label.
#
# Rounds 6-7 validated the marker STRUCTURE and the reason VOCABULARY, then
# deleted the region body before scanning. The seventh review demonstrated the
# consequence directly: a structurally perfect region labeled
#
#     reason="truthful denial list"
#
# containing the single sentence
#
#     Gate A verifies the authorization digest before every invocation.
#
# was ACCEPTED. A closed vocabulary of reasons bought nothing, because nothing
# ever compared the region's content to the reason it declared. Any false
# affirmative current-enforcement claim could be hidden behind a legal label.
#
# The architecture is therefore no longer:
#
#     parse markers -> delete exempt content -> scan remainder
#
# It is:
#
#     parse markers
#     validate marker structure and reason vocabulary
#     validate EACH region's content against its declared reason
#     scan all non-exempt governing prose
#
# Every reason now carries its own mechanical content contract (see
# _validate_denial_region / _validate_obsolete_region /
# _validate_example_region). A region whose content does not satisfy its
# declared reason is a violation and exempts NOTHING.
#
# The reason-content validators reuse the SAME enforcement lexicon and the SAME
# active/emphatic/progressive/passive matchers as ordinary prose scanning. There
# are deliberately not two diverging enforcement lexicons.
#
# Honest scope statement, stated rather than hidden. This is still a
# deterministic lexical/structural guard, not a semantic analyzer:
#   - it DOES mechanically reject an obvious semantic mismatch, including any
#     affirmative current-enforcement claim under any allowed reason;
#   - it does NOT decide whether a well-formed, plainly negative denial list is
#     factually true, nor whether a quotation is genuinely historical. Reason
#     ACCURACY still receives manual review.
# It does not claim natural-language understanding.
#
# Preferred remedy is always elimination, not a cleverer exemption. Both real
# `truthful denial list` regions were removed in round 8 by rewriting their
# items into explicitly negative grammar the guard parses directly, taking the
# real region count from 6 to 4. Fewer exemption regions is safer than more
# sophisticated exemption validation.
# ---------------------------------------------------------------------------

PROSE_GUARD_EXEMPTION_BEGIN = "BEGIN_PROSE_GUARD_EXEMPTION"
PROSE_GUARD_EXEMPTION_END = "END_PROSE_GUARD_EXEMPTION"

# Closed reason enum. A reason outside this set fails closed.
ALLOWED_EXEMPTION_REASONS = (
    "quoted obsolete wording",
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


# ---------------------------------------------------------------------------
# Reason-specific content contracts (round 8).
#
# Each allowed reason declares what its region may contain. The contract is
# checked BEFORE the region is exempted from ordinary scanning.
# ---------------------------------------------------------------------------

# A region must be introduced by the line IMMEDIATELY preceding it -- the
# nearest preceding line that is neither blank, nor a marker, nor a code fence.
# Only that one line counts, so an introducer "further up" grants nothing and an
# introducer appearing only AFTER the opening marker grants nothing.
_CODE_FENCE_RE = re.compile(r"^\s*(?:```|~~~)")

# Round 9: `truthful denial list` is retired. Every real denial region was
# rewritten as ordinary explicit negative prose, which the guard already
# accepts with no exemption at all. A reason retained only for symmetry is a
# standing bypass surface, so the reason, its introducer vocabulary, its item
# markers and its validator are all gone. See section 12 of the round-9 brief.

# Historical/obsolete-quotation introducers.
_OBSOLETE_INTRODUCER_RE = re.compile(
    r"\b(?:previous|previously|obsolete|superseded|supersedes|former|formerly|"
    r"historical|historic|old\s+wording|incorrect\s+wording|"
    r"no\s+longer\s+accurate|quoted\s+historical|was\s+worded)\b",
    re.IGNORECASE,
)

# Illustrative-example introducers (round 9).
#
# The old rule was an UNBOUND substring search for `example`, which the eighth
# review broke seven different ways: a distant `## Example gallery` heading, a
# table header cell, an inline-code token, a trailing `| Example`, and even the
# negated `Not an example:`. All of those "contain the word example" and none
# of them marks the following region as non-authoritative.
#
# The replacement is a small CLOSED set matched against the WHOLE introducer
# line. The line must BE an approved introducer, not merely contain one. That
# single change is what binds the introducer to the region structurally: a
# heading is not the whole line minus its `#`, a table row is not an
# introducer, and prose that happens to mention examples is not an introducer.
_APPROVED_EXAMPLE_INTRODUCERS = (
    "invalid example",
    "rejected example",
    "non-authoritative example",
    "hypothetical invalid wording",
    "example of wording that must not be treated as current behavior",
)

# Wording that must NEVER be honoured as an introducer even though it contains
# the token `example`. Checked before the approved set so a negated or
# authoritative-sounding phrase can never be silently accepted.
_REJECTED_EXAMPLE_INTRODUCERS = (
    "not an example",
    "this is not an example",
    "example implementation",
    "current example",
    "production example",
    "authoritative example",
    "example requirement",
)


def _introducer_candidate(raw):
    """Reduce an introducer line to the text that may bind a region.

    Structural containers are stripped to nothing rather than searched, so a
    heading, a table row, a list bullet, an inline-code span, an HTML comment
    or a link target can never supply an introducer.
    """
    text = raw.strip()
    if not text:
        return ""
    # A heading, table row, or HTML comment is a different semantic unit.
    if text.startswith("#") or text.startswith("|") or text.startswith("<!--"):
        return ""
    # Inline code and link targets are quoted tokens, not assertions.
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r" \1 ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = _normalize_markdown(text.replace("_", " "))
    # The introducer must be the entire line, optionally ending in a colon.
    text = text.strip().rstrip(":").strip()
    return re.sub(r"\s+", " ", text).lower()


def _is_approved_example_introducer(raw):
    candidate = _introducer_candidate(raw)
    if not candidate:
        return False
    # Boundary-aware: `authoritative example` must not fire inside the
    # approved `non-authoritative example`.
    if any(
        re.search(rf"(?<![\w-]){re.escape(bad)}(?![\w-])", candidate)
        for bad in _REJECTED_EXAMPLE_INTRODUCERS
    ):
        return False
    return candidate in _APPROVED_EXAMPLE_INTRODUCERS


def _region_introducer(lines, open_at):
    """Return (lineno, text) of the region's immediate introducer, or None."""
    for lineno in range(open_at - 1, 0, -1):
        raw = lines[lineno - 1]
        if not raw.strip():
            continue
        if _is_any_marker_line(raw) or _CODE_FENCE_RE.match(raw):
            continue
        return (lineno, raw)
    return None


def _is_blockquoted(raw):
    return raw.strip().startswith(">")


def _has_quoted_span(raw):
    return bool(re.search(r'"[^"]+"', raw) or re.search(r"[“][^”]+[”]", raw))


# Round 9: the label-column heuristic is DELETED, not narrowed.
#
# It was `^\s*[A-Za-z][A-Za-z\-' ]{2,30}?\s{2,}\S` -- any alphabetic label
# followed by two spaces. It did not require the word "Example"; `Foo  Gate A
# verifies the digest.` satisfied it. Two-column-looking whitespace is not
# evidence that text is illustrative, so no amount of tightening makes it a
# sound authorization signal. Illustrative content must now be an EXPLICIT
# quotation, which is a positive, visible marker rather than a layout accident.


# Round 10: strip-and-scan is DELETED, not narrowed.
#
# The round-9 helper was:
#
#     text = re.sub(r'"[^"]*"', " ", raw)
#     return re.sub(r"[“][^”]*[”]", " ", text)
#
# i.e. "remove every substring matching a quote pair, then scan whatever
# fragments remain". That is compositionally bypassable: a single sentence can
# be split across a quoted fragment and an unquoted fragment so that neither
# leftover fragment is a grammatically complete clause, and the shared scanner
# -- which looks for subject + enforcement verb -- sees nothing to match.
# `Gate A "verifies the authorization digest."` leaves only `Gate A `;
# `"Gate A verifies" the authorization digest.` leaves only
# ` the authorization digest.`. Both were ACCEPTED. The identical fully
# unquoted sentence was REJECTED, so the defect was quote SEGMENTATION, not
# lexicon coverage.
#
# The fix is not a better remainder scanner. Trying to infer whether leftover
# fragments outside the quotes happen to reconstitute a claim is exactly the
# guess-the-grammar approach that failed nine rounds running. Instead the
# quoted-example contract becomes very narrow and fail-closed:
#
#     one line, one balanced quoted exhibit, no meaningful unquoted remainder.
#
# A partial-span bypass is then impossible by construction: there is nowhere
# outside the quotation marks to put the other half of the sentence.

# Structural prefixes that may precede the exhibit: blockquote markers, list
# bullets, and indentation. These carry no propositional content.
_EXHIBIT_PREFIX_RE = re.compile(r"^(?:\s|>|[-+*]\s|\d+[.)]\s)*")

# Punctuation that may structurally follow the closing quotation mark.
_EXHIBIT_TRAILER_RE = re.compile(r"^[.,;:!?\s]*$")

# A *paired* single-quote span, i.e. a nested quotation. The boundary
# conditions deliberately exclude word-internal apostrophes so that possessives
# and contractions inside an exhibit are not misread as nesting.
_NESTED_QUOTE_RE = re.compile(r"(?<![A-Za-z])'[^']*'(?![A-Za-z])|‘[^’]*’")

# Quotation marks this contract deliberately does NOT support. Listing them
# explicitly is the point: the parser supports a small, named set rather than
# every Unicode quotation mark.
_UNSUPPORTED_QUOTE_CHARS = "„‟”‹›«»「」『』〝〞‚"

QUOTE_STYLE_STRAIGHT_DOUBLE = "straight-double"
QUOTE_STYLE_SMART_DOUBLE = "smart-double"

SUPPORTED_QUOTE_STYLES = (
    QUOTE_STYLE_STRAIGHT_DOUBLE,
    QUOTE_STYLE_SMART_DOUBLE,
)

# Structured, reviewer-visible parse-failure reasons.
QUOTE_FAIL_NO_EXHIBIT = "NO_QUOTED_EXHIBIT"
QUOTE_FAIL_UNBALANCED = "UNBALANCED_QUOTES"
QUOTE_FAIL_MISMATCHED = "MISMATCHED_QUOTES"
QUOTE_FAIL_MULTIPLE = "MULTIPLE_QUOTED_SPANS"
QUOTE_FAIL_LEADING = "UNQUOTED_LEADING_TEXT"
QUOTE_FAIL_TRAILING = "UNQUOTED_TRAILING_TEXT"
QUOTE_FAIL_MULTILINE = "MULTILINE_QUOTE_UNSUPPORTED"
QUOTE_FAIL_UNSUPPORTED_STYLE = "UNSUPPORTED_QUOTE_STYLE"
QUOTE_FAIL_INLINE_CODE = "INLINE_CODE_NOT_QUOTATION"

QUOTE_PARSE_FAILURE_REASONS = (
    QUOTE_FAIL_NO_EXHIBIT,
    QUOTE_FAIL_UNBALANCED,
    QUOTE_FAIL_MISMATCHED,
    QUOTE_FAIL_MULTIPLE,
    QUOTE_FAIL_LEADING,
    QUOTE_FAIL_TRAILING,
    QUOTE_FAIL_MULTILINE,
    QUOTE_FAIL_UNSUPPORTED_STYLE,
    QUOTE_FAIL_INLINE_CODE,
)


class QuoteParseResult(object):
    """Structured result of parsing one example-region content line.

    `valid` is True only for the narrow accepted shape. Otherwise `reason` is
    one of `QUOTE_PARSE_FAILURE_REASONS` and is surfaced verbatim in the
    validator's finding so a reviewer can see *why* a line failed closed.
    """

    __slots__ = ("valid", "quote_style", "exhibit", "unquoted_remainder", "reason")

    def __init__(
        self,
        valid,
        quote_style=None,
        exhibit=None,
        unquoted_remainder="",
        reason=None,
    ):
        self.valid = valid
        self.quote_style = quote_style
        self.exhibit = exhibit
        self.unquoted_remainder = unquoted_remainder
        self.reason = reason

    def __repr__(self):  # pragma: no cover - diagnostic aid
        return (
            "QuoteParseResult(valid={0!r}, quote_style={1!r}, exhibit={2!r}, "
            "unquoted_remainder={3!r}, reason={4!r})".format(
                self.valid,
                self.quote_style,
                self.exhibit,
                self.unquoted_remainder,
                self.reason,
            )
        )


def _fail(reason, remainder=""):
    return QuoteParseResult(False, reason=reason, unquoted_remainder=remainder)


def parse_quoted_exhibit(raw):
    """Parse one line as at most one complete, balanced quoted exhibit.

    Accepted shape, and nothing else:

        [blockquote markers] [list bullet / indentation]
        <one balanced quoted exhibit>
        [terminal punctuation] [whitespace]

    Supported quote styles: straight double (`"`) and smart double
    (U+201C/U+201D). Everything else fails closed:

      * nested quotation (a paired single-quote span inside the exhibit) is
        NOT supported -- rejected as UNSUPPORTED_QUOTE_STYLE rather than
        silently misparsed;
      * escaped quotation marks (`\\"`) are NOT supported -- the contract has
        no use for them, so they fail closed as UNSUPPORTED_QUOTE_STYLE
        instead of motivating a stateful un-escaping parser;
      * multi-line quote spans are NOT supported -- a quote must open and
        close on the same line;
      * inline code spans (backticks) are NOT quotation and never grant the
        exemption.
    """
    line = raw.rstrip("\n")

    # Backticks are Markdown code formatting, not natural-language quotation.
    # Inline code must never confer the illustrative exemption.
    if "`" in line:
        return _fail(QUOTE_FAIL_INLINE_CODE)

    # Escaped quotation marks are not supported; fail closed rather than
    # attempting to un-escape with a non-greedy regex that cannot see escapes.
    if "\\\"" in line or "\\'" in line:
        return _fail(QUOTE_FAIL_UNSUPPORTED_STYLE)

    prefix = _EXHIBIT_PREFIX_RE.match(line).group(0)
    body = line[len(prefix):]

    if not body.strip():
        return _fail(QUOTE_FAIL_NO_EXHIBIT)

    # Explicitly unsupported quotation marks (guillemets, low-9, CJK brackets,
    # a bare closing smart quote used as an opener, ...).
    if any(ch in body for ch in _UNSUPPORTED_QUOTE_CHARS if ch != "”"):
        return _fail(QUOTE_FAIL_UNSUPPORTED_STYLE)

    straight = body.count('"')
    smart_open = body.count("“")
    smart_close = body.count("”")

    if straight == 0 and smart_open == 0 and smart_close == 0:
        return _fail(QUOTE_FAIL_NO_EXHIBIT, remainder=body)

    # Never mix styles on one line: `“...\"` and `"...”` are misparses waiting
    # to happen, so they are named as such.
    if straight and (smart_open or smart_close):
        return _fail(QUOTE_FAIL_MISMATCHED)

    if straight:
        style = QUOTE_STYLE_STRAIGHT_DOUBLE
        if straight % 2 == 1:
            # One lone straight quote is genuinely ambiguous between an
            # unterminated opener and a stray closer, so it is reported as
            # unbalanced rather than guessed at.
            return _fail(QUOTE_FAIL_UNBALANCED)
        if straight > 2:
            return _fail(QUOTE_FAIL_MULTIPLE)
        open_idx = body.index('"')
        close_idx = body.index('"', open_idx + 1)
    else:
        style = QUOTE_STYLE_SMART_DOUBLE
        if smart_open and not smart_close:
            # A smart quote is directional, so an unclosed opener is
            # unambiguously an attempted multi-line span.
            return _fail(QUOTE_FAIL_MULTILINE)
        if smart_close and not smart_open:
            return _fail(QUOTE_FAIL_UNBALANCED)
        if smart_open > 1 or smart_close > 1:
            return _fail(QUOTE_FAIL_MULTIPLE)
        open_idx = body.index("“")
        close_idx = body.index("”")
        if close_idx < open_idx:
            return _fail(QUOTE_FAIL_UNBALANCED)

    exhibit = body[open_idx + 1:close_idx]
    leading = body[:open_idx]
    trailing = body[close_idx + 1:]

    # Nested quotation is not supported. Reject clearly and consistently
    # instead of silently misparsing the inner span.
    if _NESTED_QUOTE_RE.search(exhibit):
        return _fail(QUOTE_FAIL_UNSUPPORTED_STYLE)

    if not exhibit.strip():
        return _fail(QUOTE_FAIL_NO_EXHIBIT)

    # THE fail-closed step. Any non-whitespace prose before the exhibit, or
    # anything but structural terminal punctuation after it, rejects the line
    # outright. Subjects, predicates, objects, qualifiers, conjunctions and
    # parentheticals outside the quotation marks all land here. No attempt is
    # made to decide whether the remainder "forms a claim".
    if leading.strip():
        return _fail(QUOTE_FAIL_LEADING, remainder=leading)
    if not _EXHIBIT_TRAILER_RE.match(trailing):
        return _fail(QUOTE_FAIL_TRAILING, remainder=trailing)

    return QuoteParseResult(
        True,
        quote_style=style,
        exhibit=exhibit,
        unquoted_remainder=trailing,
    )


def _region_body_lines(lines, open_at, close_at):
    return [
        (lineno, lines[lineno - 1])
        for lineno in range(open_at + 1, close_at)
        if lines[lineno - 1].strip()
    ]


def _validate_obsolete_region(body, introducer, name, open_at):
    """`quoted obsolete wording`: small, explicitly historical, fully quoted."""
    problems = []
    if introducer is None or not _OBSOLETE_INTRODUCER_RE.search(
        _normalize_markdown(introducer[1].replace("_", " "))
    ):
        problems.append(
            f"line {open_at}: reason=\"quoted obsolete wording\" region is not "
            "immediately introduced by text identifying it as old, obsolete, "
            "superseded or quoted historical wording"
        )
    if len(body) > MAX_OBSOLETE_REGION_LINES:
        problems.append(
            f"line {open_at}: reason=\"quoted obsolete wording\" region spans "
            f"{len(body)} content lines, more than the "
            f"{MAX_OBSOLETE_REGION_LINES}-line maximum for a bounded quotation"
        )
    for lineno, raw in body:
        if not (_is_blockquoted(raw) or _has_quoted_span(raw)):
            problems.append(
                f"line {lineno}: line in a \"quoted obsolete wording\" region "
                "is not quoted or blockquoted; a current authoritative "
                "statement may not sit beside the quotation"
            )
    return problems


def _validate_example_region(body, introducer, name, open_at):
    """`non-authoritative example`: bound introducer, quoted, and SCANNED.

    Round 9. The round-8 version validated illustrative *shape* only and never
    ran the shared enforcement scanner, so a false current-enforcement claim
    that merely looked like an example was exempted outright. Illustrative
    shape is now necessary but never sufficient. The order is fixed:

      1. reason and marker structure (already checked by the caller);
      2. the immediate introducer must be an approved, non-negated one;
      3. the region must be narrowly bounded;
      4. every line must be an explicit quotation;
      5. the shared enforcement scanner runs over everything OUTSIDE the
         quotation marks -- the same `_scan_clauses` and the same lexicon that
         governs ordinary prose and `quoted obsolete wording` regions.

    Quoting invalid wording is the whole point of the reason, so the text
    inside the quotation marks is the exhibit and is not itself an assertion.
    Everything else on the line is ordinary authoritative prose and is scanned
    as such, which is what kills "quote plus a real claim on the same line",
    "quote then a requirement", and every mixed-purpose region.
    """
    problems = []
    if introducer is None or not _is_approved_example_introducer(introducer[1]):
        problems.append(
            f"line {open_at}: reason=\"non-authoritative example\" region is "
            "not immediately preceded by an approved, non-negated example "
            "introducer (the whole preceding line must be one of: "
            + "; ".join(sorted(_APPROVED_EXAMPLE_INTRODUCERS))
            + ")"
        )
    if len(body) > MAX_EXAMPLE_REGION_LINES:
        problems.append(
            f"line {open_at}: reason=\"non-authoritative example\" region "
            f"spans {len(body)} content lines, more than the "
            f"{MAX_EXAMPLE_REGION_LINES}-line maximum for a bounded example"
        )
    for lineno, raw in body:
        parsed = parse_quoted_exhibit(raw)
        if not parsed.valid:
            problems.append(
                f"line {lineno}: line in a \"non-authoritative example\" "
                f"region is not exactly one complete quoted exhibit "
                f"[{parsed.reason}]; the contract is one line, one balanced "
                "quoted exhibit, no meaningful unquoted remainder"
            )
            continue
        # The shared enforcement scan is retained, not replaced. It now runs
        # over a remainder that the grammar has already proven contains no
        # prose, so it is a belt-and-braces check rather than the primary
        # defence -- which is exactly the point: structural quoting is not a
        # generic escape mechanism.
        outside = _normalize_markdown(parsed.unquoted_remainder)
        problems.extend(
            f"{f} [inside reason=\"non-authoritative example\" region]"
            for f in _scan_clauses(outside, name, lineno)
        )
    return problems


# Bounded quotation: smaller than the general region cap.
MAX_OBSOLETE_REGION_LINES = 6
MAX_EXAMPLE_REGION_LINES = 6

REASON_CONTENT_VALIDATORS = {
    "quoted obsolete wording": _validate_obsolete_region,
    "non-authoritative example": _validate_example_region,
}


def _resolve_exemption_regions(lines, name="<text>"):
    """Return (exempt_line_numbers, violations).

    Two layers, in this order:
      1. marker structure and reason vocabulary;
      2. region CONTENT against its declared reason.
    Fail-closed: any malformed or contract-violating region exempts nothing at
    all -- content is never removed before the relevant safety checks run.
    """
    exempt = set()
    violations = []
    regions = []
    open_at = None
    open_reason = None
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
            open_reason = payload
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
                open_reason = None
                continue
            for inner in body:
                if _AUTHORITATIVE_REQUIREMENT_RE.search(lines[inner - 1]):
                    violations.append(
                        f"line {inner}: authoritative requirement language "
                        "inside an exemption region; requirements must be "
                        "stated in scanned, authoritative prose"
                    )
            regions.append((open_at, lineno, open_reason))
            exempt.update(body)
            open_at = None
            open_reason = None
    # Layer 2: the declared reason must constrain the region's content.
    for region_open, region_close, reason in regions:
        validator = REASON_CONTENT_VALIDATORS[reason]
        violations.extend(
            f"{v} (reason-content contract)"
            for v in validator(
                _region_body_lines(lines, region_open, region_close),
                _region_introducer(lines, region_open),
                name,
                region_open,
            )
        )
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
    exempt, findings = _resolve_exemption_regions(lines, name)
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
        findings.extend(_scan_clauses(_normalize_markdown(block), name, start_lineno))
    return findings


def _scan_clauses(normalized, name, start_lineno):
    """Scan one normalized block for enforcement overclaims.

    The single shared implementation of the enforcement lexicon. Ordinary prose
    scanning and reason-specific region validation both call it, so there is one
    lexicon rather than two that can drift apart.
    """
    findings = []
    if True:
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
    def test_consumer_status_is_implemented_and_enforcing(self):
        """The consumer landed. The claim is checked against real files.

        Flipping this status to IMPLEMENTED is only truthful if the consumer
        source AND the invocation-boundary test suite actually exist, so this
        asserts both rather than trusting the YAML.
        """
        self.assertEqual(
            self.contract["gate_a_authorization_consumer_status"], "IMPLEMENTED"
        )
        self.assertTrue(self.contract["gate_a_runtime_enforcement_exists"])
        self.assertTrue(
            (REPO_ROOT / "scripts" / "gate_a_authorization.py").is_file()
        )
        self.assertTrue(
            (REPO_ROOT / "tests" / "test_gate_a_invocation_boundary.py").is_file(),
            "IMPLEMENTED is only honest if the invocation boundary is tested",
        )

    # 52
    def test_consumer_is_marked_required(self):
        self.assertTrue(self.contract["gate_a_authorization_consumer_required"])

    # 53
    def test_consumer_path_points_at_real_files(self):
        consumer_path = self.contract["gate_a_authorization_consumer_path"]
        self.assertEqual(consumer_path, "scripts/gate_a_authorization.py")
        self.assertTrue(
            (REPO_ROOT / consumer_path).is_file(),
            "the declared consumer path must resolve to a real file",
        )
        integration_point = self.contract["gate_a_consumer_integration_point"]
        module, _, symbol = integration_point.partition("::")
        self.assertEqual(module, "scripts/skill_executor.py")
        self.assertTrue((REPO_ROOT / module).is_file())
        self.assertIn(
            "class " + symbol,
            (REPO_ROOT / module).read_text(encoding="utf-8"),
            "the declared integration point must name a real class",
        )
        # No sentinel may survive as a path.
        self.assertFalse((REPO_ROOT / "PENDING_IMPLEMENTATION").exists())

    # 54
    def test_consumer_is_wired_to_stage1(self):
        """Wired means the invocation path imports AND consumes the capability."""
        self.assertTrue(
            self.contract["gate_a_authorization_consumer_wired_to_stage1"]
        )
        executor = (REPO_ROOT / "scripts" / "skill_executor.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("from gate_a_authorization import", executor)
        self.assertIn("require_authorization_capability", executor)
        self.assertIn(
            ".consume(",
            executor,
            "the capability must be consumed at the provider boundary, not "
            "merely validated somewhere earlier",
        )

    # 55
    def test_consumer_tests_are_implemented(self):
        self.assertEqual(
            self.contract["gate_a_authorization_consumer_tests_status"],
            "IMPLEMENTED",
        )
        self.assertTrue(
            self.contract[
                "gate_a_consumer_required_test_categories_implemented_in_this_pr"
            ]
        )
        for suite in (
            "tests/test_gate_a_authorization_consumer.py",
            "tests/test_gate_a_invocation_boundary.py",
        ):
            self.assertTrue((REPO_ROOT / suite).is_file(), suite)

    # 56
    def test_document_tests_are_not_runtime_enforcement_tests(self):
        self.assertFalse(
            self.contract["contract_tests_are_runtime_enforcement_tests"],
            "this suite must never claim to prove runtime enforcement",
        )
        self.assertTrue(
            self.contract[
                "gate_a_authorization_verification_steps_are_current_runtime_behavior"
            ]
        )
        self.assertFalse(
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
    def test_consumer_hard_stop_is_retired_but_still_unwaivable(self):
        """The hard stop stopped firing because its condition was FIXED.

        It was not waived and not deleted: it remains among the 24 and remains
        non-waivable, so deleting the consumer would make it fire again.
        """
        self.assertFalse(
            self.contract["gate_a_authorization_consumer_hard_stop_waivable"]
        )
        self.assertFalse(
            self.contract["gate_a_authorization_consumer_not_implemented_is_active"]
        )
        self.assertIn(
            CONSUMER_HARD_STOP,
            self.contract["authorization_hard_stop_conditions"],
            "the hard stop must be retired by satisfaction, never removed",
        )
        # Retiring one hard stop must not make the package runnable.
        self.assertFalse(self.contract["package_runnable"])
        self.assertEqual(
            self.contract["execution_authorization_status"], "NOT_AUTHORIZED"
        )


class ConsumerHardStop(unittest.TestCase):
    """62-63: the new hard stop exists and the count is consistent."""

    def setUp(self):
        self.contract, self.text = _load_contract()
        self.stops = self.contract["authorization_hard_stop_conditions"]

    # 62
    def test_consumer_hard_stop_still_listed_but_no_longer_first(self):
        self.assertIn(CONSUMER_HARD_STOP, self.stops)
        # The consumer now exists, so the first STILL-FIRING hard stop is the
        # pending execution pin.
        self.assertEqual(
            self.contract["first_evaluated_hard_stop"],
            "GATE_A_EXECUTION_FRAMEWORK_SHA_PENDING",
        )
        self.assertNotEqual(
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
    """74-75: repository-wide prose guard over the changed documents.

    The guard exists to stop the package claiming enforcement it does not
    have. It is therefore CONDITIONAL on the consumer status rather than
    absolute: while `gate_a_authorization_consumer_status` is NOT_IMPLEMENTED,
    a present-tense enforcement claim is a lie and is rejected. Once the
    consumer is implemented and wired, such a claim is simply true, and a
    guard that still rejected it would be forcing the document to understate
    reality -- the mirror image of the defect it was written to prevent.

    The guard is not weakened: revert the consumer, and every present-tense
    claim in these documents becomes a test failure again.
    """

    # 74
    def test_no_present_tense_runtime_enforcement_claims_in_changed_docs(self):
        contract, _ = _load_contract()
        status = contract["gate_a_authorization_consumer_status"]
        offenders = []
        for path in CHANGED_DOCS:
            self.assertTrue(path.is_file(), f"changed doc missing: {path}")
            offenders.extend(
                find_enforcement_overclaims(
                    path.read_text(encoding="utf-8"), name=path.name
                )
            )
        if status == "NOT_IMPLEMENTED":
            self.assertFalse(enforcement_claims_are_permitted())
            self.assertEqual(
                offenders,
                [],
                "present-tense runtime-enforcement claims found while the "
                "consumer is NOT_IMPLEMENTED:\n" + "\n".join(offenders),
            )
            return
        self.assertTrue(enforcement_claims_are_permitted())

        # Consumer implemented: enforcement claims are permitted, but only
        # because the enforcing code and its boundary proof genuinely exist.
        self.assertEqual(status, "IMPLEMENTED", f"unknown consumer status: {status}")
        self.assertTrue(contract["gate_a_authorization_consumer_wired_to_stage1"])
        self.assertTrue((REPO_ROOT / "scripts" / "gate_a_authorization.py").is_file())
        self.assertTrue(
            (REPO_ROOT / "tests" / "test_gate_a_invocation_boundary.py").is_file()
        )
        # Claiming enforcement must still never coincide with claiming
        # authorization.
        self.assertFalse(contract["package_runnable"])
        self.assertEqual(contract["execution_authorization_status"], "NOT_AUTHORIZED")

    # 74b
    def test_prose_guard_still_detects_overclaims(self):
        """The detector itself must not have been defanged."""
        lie = (
            "The runner verifies the authorization record before invocation.\n"
            "Gate A recomputes the digest and blocks unauthorized runs.\n"
        )
        self.assertNotEqual(
            find_enforcement_overclaims(lie, name="synthetic.md"),
            [],
            "the prose-guard detector no longer detects overclaims",
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
            # Round 8: stated as scanned negative facts, not inside a prose-guard
            # exemption region. The key is renamed accordingly. The consumer-era
            # rewrite frames the items that became false historically, because
            # the statements describe PR #107 and the pre-PR #109 tree.
            "before PR #109, no authorization consumer exists in the tree",
            "before PR #109, Gate A is not runtime-enforced",
            "owner approval cannot currently authorize a run",
            "before PR #109, digests are not checked",
            "before PR #109, model invocation is not blocked by authorization state",
            "Evidence 0016 is not executable",
        ):
            self.assertIn(claim, self.contract["pr_107_absence_facts"])
        self.assertNotIn("pr_107_does_not_prove", self.contract)
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
            "The Gate A consumer verifies this checklist's digest.", collapsed
        )
        self.assertIn(
            "Gate D must not begin unless the Gate A consumer has passed.",
            collapsed,
        )
        self.assertIn("this checklist governs no live run", collapsed)
        # The eight tripwires are untouched by this change.
        self.assertEqual(len(self.contract["stale_diagnosis_tripwires"]), 8)


class ConsumerImplementedWithoutAuthorizingAnything(unittest.TestCase):
    """80: the consumer now exists in runtime sources -- and authorizes nothing.

    This test was originally the guard proving PR #107 added no consumer. The
    consumer PR flips its direction: the authorization *mechanism* must now be
    present in runtime sources, while every authorization *artifact* must still
    be absent. Those are independent facts, and conflating them is exactly the
    failure mode the preparation package exists to prevent.
    """

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 80
    def test_consumer_exists_in_runtime_sources(self):
        self.assertTrue(
            self.contract["consumer_implementation_file_added_by_this_pr"]
        )
        implementers = []
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
                        implementers.append(str(path.relative_to(REPO_ROOT)))
        self.assertIn(
            "scripts/gate_a_authorization.py",
            {p.replace("\\", "/") for p in implementers},
            "the Gate A consumer must exist in runtime sources now that the "
            "package claims IMPLEMENTED",
        )

    # 80b -- the half that must NOT change
    def test_implementing_the_consumer_created_no_authorization_artifacts(self):
        """A mechanism is not an authorization; a draft record is not either."""
        _assert_only_permitted_run_control_artifacts(self)
        for key in ("owner_approval_artifact_path",):
            self.assertFalse(
                (REPO_ROOT / self.contract[key]).exists(),
                f"{key} must not exist: implementing the consumer does not "
                f"authorize a run",
            )
        self.assertFalse(self.contract["package_runnable"])
        self.assertEqual(
            self.contract["execution_authorization_status"], "NOT_AUTHORIZED"
        )
        self.assertEqual(self.contract["package_status"], "PREPARED_NOT_RUN")
        self.assertEqual(
            self.contract["execution_framework_sha"],
            "PENDING_POST_MERGE_PIN_FINALIZATION",
            "this PR must not finalize the execution pin",
        )
        self.assertFalse(self.contract["evidence_directory_created"])
        self.assertEqual(
            self.contract["readiness_classification_before"],
            "Externally exercised",
        )


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


# Round 8: a region is only exempt if its CONTENT satisfies its reason, so the
# test helper must build a contract-valid region -- an introducer the reason
# accepts, and content marked as non-authoritative. Helpers that used to emit a
# bare marker plus a raw affirmative claim were encoding the very bypass the
# seventh review demonstrated.
_REASON_INTRODUCERS = {
    "quoted obsolete wording": "Previous obsolete wording:",
    "non-authoritative example": "Invalid example:",
}


def _exemption_region(body, reason="quoted obsolete wording", introducer=None,
                      mark=True):
    """Build a reason-content-valid exemption region around `body`."""
    intro = _REASON_INTRODUCERS[reason] if introducer is None else introducer
    lines = body.splitlines() or [""]
    if mark:
        lines = [
            raw if (not raw.strip() or raw.strip().startswith(">")) else "> " + raw
            for raw in lines
        ]
        if reason == "non-authoritative example":
            # Round 9: example content must be an explicit quotation, so the
            # helper quotes the exhibit as a legitimate author would.
            lines = [
                raw if (not raw.strip() or '"' in raw or "“" in raw)
                else re.sub(r"^(\s*>\s*)(.*)$", r'\1"\2"', raw)
                for raw in lines
            ]
    intro_block = f"{intro}\n" if intro else ""
    return (
        f"{intro_block}{_exempt_begin(reason)}\n"
        + "\n".join(lines)
        + f"\n{PROSE_GUARD_EXEMPTION_END}\n"
    )


# Narrowly valid, legitimate region fixtures -- one per reason (section 8).
LEGITIMATE_REGION_FIXTURES = {
    "quoted obsolete wording": (
        "Previous obsolete wording:",
        "> Gate A verifies the authorization digest.",
    ),
    # Round 9: an example region must be an EXPLICIT quotation. A bare
    # blockquote no longer qualifies, so the fixture carries real quote marks.
    "non-authoritative example": (
        "Invalid example:",
        '> "Gate A verifies the authorization digest."',
    ),
}


def _legitimate_region(reason):
    intro, body = LEGITIMATE_REGION_FIXTURES[reason]
    return (
        f"{intro}\n{_exempt_begin(reason)}\n{body}\n"
        f"{PROSE_GUARD_EXEMPTION_END}\n"
    )


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
            "Previous obsolete wording:\n"
            f"{_exempt_begin()}\n"
            "> The authorization digest is verified by Gate A.\n"
            "> Gate A does verify the digest.\n"
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
                assert_no_unpermitted_overclaims(self, findings, path.name)


class ConsumerHardStopUnchangedByRound6(unittest.TestCase):
    """141-143: the round-6 prose work changed no safety semantics."""

    def setUp(self):
        self.contract, self.text = _load_contract()

    # 141
    def test_consumer_hard_stop_semantics_unchanged(self):
        """Round 6 changed no safety semantics, and neither did the consumer PR.

        The consumer *status* legitimately changed; every safety value asserted
        below did not.
        """
        self.assertIn(CONSUMER_HARD_STOP, self.text)
        self.assertEqual(
            self.contract["gate_a_authorization_consumer_status"], "IMPLEMENTED"
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
        _assert_only_permitted_run_control_artifacts(self)
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
                assert_no_unpermitted_overclaims(self, findings, path.name)


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
        # Round 8: a well-formed reason exempts only content that satisfies that
        # reason's content contract, so each reason needs its own valid body.
        for reason in ALLOWED_EXEMPTION_REASONS:
            with self.subTest(reason=reason):
                text = (
                    "Honest framing line one.\n"
                    "Honest framing line two.\n"
                    "Honest framing line three.\n"
                    "Honest framing line four.\n"
                    + _legitimate_region(reason)
                    + "Honest closing line.\n"
                )
                self.assertEqual(
                    find_enforcement_overclaims(text, name="T.md"), []
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
    def test_consumer_hard_stop_and_safety_values_unchanged(self):
        self.assertIn(CONSUMER_HARD_STOP, self.text)
        self.assertEqual(
            self.contract["first_evaluated_hard_stop"],
            "GATE_A_EXECUTION_FRAMEWORK_SHA_PENDING",
        )
        self.assertEqual(
            self.contract["gate_a_authorization_consumer_status"], "IMPLEMENTED"
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
        _assert_only_permitted_run_control_artifacts(self)
        self.assertFalse(
            (REPO_ROOT / self.contract["owner_approval_artifact_path"]).exists()
        )


# ---------------------------------------------------------------------------
# Round 8: reason-content contracts.
#
# The seventh review demonstrated a complete bypass: a structurally perfect
# region labeled reason="truthful denial list" containing the single sentence
#
#     Gate A verifies the authorization digest before every invocation.
#
# was ACCEPTED, hiding a real enforcement overclaim. Every case below is a
# direct regression test for that class of bypass.
#
# All fixtures embed the region in surrounding honest prose on purpose. A bare
# one-line document is rejected by the unrelated "region may not cover more than
# half the document" rule, which would have made these tests pass for the wrong
# reason and proved nothing about reason-content validation.
# ---------------------------------------------------------------------------

ROUND8_HONEST_PADDING = (
    "Preparation framing line one: no consumer exists.\n"
    "Preparation framing line two: digest verification is not implemented.\n"
    "Preparation framing line three: the package remains non-runnable.\n"
    "Preparation framing line four: owner approval cannot authorize a run.\n"
    "Preparation framing line five: this package proves no runtime behavior.\n"
)

# The exact string the seventh review used to defeat the round-7 guard.
DEMONSTRATED_BYPASS_CLAIM = (
    "Gate A verifies the authorization digest before every invocation."
)


def _round8_doc(reason, body, introducer=None):
    """Embed a raw (unmarked) region body in honest surrounding prose."""
    intro_block = f"{introducer}\n" if introducer else ""
    return (
        ROUND8_HONEST_PADDING
        + intro_block
        + f'<!-- {PROSE_GUARD_EXEMPTION_BEGIN} reason="{reason}" -->\n'
        + body.rstrip("\n")
        + "\n"
        + f"<!-- {PROSE_GUARD_EXEMPTION_END} -->\n"
        + "Closing framing line: no runtime enforcement exists in this package.\n"
    )


class Round8DemonstratedBypassIsClosed(unittest.TestCase):
    """The five section-6 strings the seventh review demonstrated."""

    def assertRejected(self, text, label):
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(findings, f"BYPASS still accepted ({label}): {text!r}")
        return findings

    def test_denial_reason_cannot_hide_the_demonstrated_claim(self):
        findings = self.assertRejected(
            _round8_doc("truthful denial list", DEMONSTRATED_BYPASS_CLAIM),
            "review-demonstrated bypass",
        )
        # It must be caught as an enforcement claim, not merely as a missing
        # introducer, so the fix is substantive rather than incidental.
        self.assertTrue(
            any("enforcement claim" in f for f in findings), findings
        )

    def test_denial_reason_cannot_hide_a_mixed_clause_claim(self):
        findings = self.assertRejected(
            _round8_doc(
                "truthful denial list",
                "Does not prove runtime enforcement, but Gate A verifies the digest.",
            ),
            "denial clause followed by affirmative claim",
        )
        self.assertTrue(any("enforcement claim" in f for f in findings), findings)

    def test_obsolete_reason_cannot_hide_an_unquoted_claim(self):
        self.assertRejected(
            _round8_doc(
                "quoted obsolete wording",
                "Gate A verifies the authorization digest.",
            ),
            "unquoted claim under quoted obsolete wording",
        )

    def test_example_reason_cannot_hide_an_unlabeled_claim(self):
        self.assertRejected(
            _round8_doc(
                "non-authoritative example",
                "Gate A verifies the authorization digest.",
            ),
            "unlabeled claim under non-authoritative example",
        )

    def test_valid_denial_followed_by_affirmative_line_is_rejected(self):
        findings = self.assertRejected(
            _round8_doc(
                "truthful denial list",
                "No current runner verifies the record.\n"
                "The runtime blocks unauthorized invocation.",
                introducer="Does not prove:",
            ),
            "valid denial line followed by an affirmative current claim",
        )
        self.assertTrue(any("enforcement claim" in f for f in findings), findings)
        # The truthful first line must not itself be flagged.
        self.assertFalse(
            any("No current runner verifies" in f for f in findings), findings
        )

    def test_a_failing_region_exempts_nothing_at_all(self):
        """Fail-closed: a contract-violating region does not shield its body."""
        exempt, violations = _resolve_exemption_regions(
            _round8_doc(
                "truthful denial list", DEMONSTRATED_BYPASS_CLAIM
            ).splitlines(),
            "T.md",
        )
        self.assertEqual(exempt, set())
        self.assertTrue(violations)


class Round8ReasonMismatchIsRejected(unittest.TestCase):
    """Section 7: an allowed reason that mislabels its region grants nothing."""

    def assertRejected(self, text, label):
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(findings, f"wrongly exempted ({label}): {text!r}")
        return findings

    def test_denial_content_labeled_obsolete_without_a_quote_is_rejected(self):
        findings = self.assertRejected(
            _round8_doc(
                "quoted obsolete wording",
                "- No authorization consumer exists.\n"
                "- Gate A is not runtime-enforced.",
                introducer="Does not prove:",
            ),
            "denial list mislabeled as quoted obsolete wording",
        )
        self.assertTrue(any("not quoted or blockquoted" in f for f in findings)
                        or any("obsolete" in f for f in findings), findings)

    def test_quoted_obsolete_wording_labeled_denial_is_rejected(self):
        self.assertRejected(
            _round8_doc(
                "truthful denial list",
                '> "Gate A verifies the authorization digest."',
                introducer="Previous obsolete wording:",
            ),
            "obsolete quotation mislabeled as truthful denial list",
        )

    def test_ordinary_prose_labeled_example_without_introducer_is_rejected(self):
        self.assertRejected(
            _round8_doc(
                "non-authoritative example",
                "The digest is verified by Gate A.",
                introducer="This section documents the contract.",
            ),
            "ordinary prose labeled as example with no example introducer",
        )

    def test_current_enforcement_claim_under_every_allowed_reason_is_rejected(self):
        for reason in ALLOWED_EXEMPTION_REASONS:
            with self.subTest(reason=reason):
                self.assertRejected(
                    _round8_doc(reason, DEMONSTRATED_BYPASS_CLAIM),
                    f"claim under reason={reason}",
                )

    def test_authoritative_requirement_under_every_allowed_reason_is_rejected(self):
        for reason in ALLOWED_EXEMPTION_REASONS:
            with self.subTest(reason=reason):
                findings = self.assertRejected(
                    _round8_doc(
                        reason,
                        "> The runner must verify the authorization digest.",
                        introducer=_REASON_INTRODUCERS[reason],
                    ),
                    f"requirement under reason={reason}",
                )
                self.assertTrue(
                    any("authoritative requirement" in f for f in findings), findings
                )

    def test_mixed_valid_denial_and_false_current_assertion_is_rejected(self):
        self.assertRejected(
            _round8_doc(
                "truthful denial list",
                "- No authorization consumer exists.\n"
                "- Gate A is not runtime-enforced.\n"
                "- The digest is checked by Gate A.",
                introducer="Does not prove:",
            ),
            "mixed denial list with one false current assertion",
        )

    def test_valid_first_line_then_unrelated_authoritative_prose_is_rejected(self):
        self.assertRejected(
            _round8_doc(
                "non-authoritative example",
                "> Gate A verifies the authorization digest.\n"
                "Gate A rejects any unapproved digest.",
                introducer="Invalid example:",
            ),
            "example followed by current authoritative prose",
        )

    def test_introducer_too_far_away_is_rejected(self):
        text = (
            ROUND8_HONEST_PADDING
            + "Does not prove:\n"
            + "An unrelated intervening sentence about the checklist.\n"
            + "Another unrelated intervening sentence about the package.\n"
            + f'<!-- {PROSE_GUARD_EXEMPTION_BEGIN} reason="truthful denial list" -->\n'
            + DEMONSTRATED_BYPASS_CLAIM
            + f"\n<!-- {PROSE_GUARD_EXEMPTION_END} -->\n"
            + "Closing framing line: no runtime enforcement exists in this package.\n"
        )
        self.assertRejected(text, "introducer separated by unrelated prose")

    def test_introducer_only_after_the_opening_marker_is_rejected(self):
        text = (
            ROUND8_HONEST_PADDING
            + f'<!-- {PROSE_GUARD_EXEMPTION_BEGIN} reason="non-authoritative example" -->\n'
            + "Invalid example:\n"
            + "Gate A verifies the authorization digest.\n"
            + f"<!-- {PROSE_GUARD_EXEMPTION_END} -->\n"
            + "Closing framing line: no runtime enforcement exists in this package.\n"
        )
        self.assertRejected(text, "introducer inside the region rather than before")

    def test_misleading_reason_used_solely_to_suppress_the_guard(self):
        """Every allowed reason, applied to the same false claim, fails."""
        for reason in ALLOWED_EXEMPTION_REASONS:
            for introducer in (None,) + tuple(_REASON_INTRODUCERS.values()):
                with self.subTest(reason=reason, introducer=introducer):
                    self.assertRejected(
                        _round8_doc(
                            reason, DEMONSTRATED_BYPASS_CLAIM, introducer=introducer
                        ),
                        f"reason={reason} introducer={introducer}",
                    )


class Round8LegitimateRegionsStillWork(unittest.TestCase):
    """Section 8: narrowly valid regions of each reason remain accepted."""

    def assertAccepted(self, text, label):
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertEqual(findings, [], f"wrongly rejected ({label})")

    def test_legitimate_region_of_each_reason_is_accepted(self):
        for reason in ALLOWED_EXEMPTION_REASONS:
            with self.subTest(reason=reason):
                self.assertAccepted(
                    ROUND8_HONEST_PADDING
                    + _legitimate_region(reason)
                    + "Closing framing line: no runtime enforcement exists in this package.\n",
                    f"legitimate {reason}",
                )

    def test_truthful_denial_list_reason_is_retired(self):
        """Round 9, section 12: the reason no longer exists at all.

        The identical denial content is accepted as ordinary prose with no
        exemption (see test_truthful_denial_forms_need_no_exemption_at_all),
        so the reason had no non-redundant use and was retired rather than
        retained for symmetry.
        """
        self.assertNotIn("truthful denial list", ALLOWED_EXEMPTION_REASONS)
        self.assertNotIn("truthful denial list", REASON_CONTENT_VALIDATORS)
        findings = find_enforcement_overclaims(
            ROUND8_HONEST_PADDING
            + "Does not prove:\n"
            + f'<!-- {PROSE_GUARD_EXEMPTION_BEGIN} reason="truthful denial list" -->\n'
            + "- No authorization consumer exists.\n"
            + f"<!-- {PROSE_GUARD_EXEMPTION_END} -->\n",
            name="T.md",
        )
        self.assertTrue(
            any("unknown exemption reason" in f for f in findings),
            f"retired reason must fail closed, got {findings}",
        )

    def test_legitimate_quoted_obsolete_wording_is_accepted(self):
        self.assertAccepted(
            ROUND8_HONEST_PADDING
            + "Previous obsolete wording:\n"
            + f'<!-- {PROSE_GUARD_EXEMPTION_BEGIN} reason="quoted obsolete wording" -->\n'
            + "> Gate A verifies the authorization digest.\n"
            + f"<!-- {PROSE_GUARD_EXEMPTION_END} -->\n"
            + "Closing framing line: no runtime enforcement exists in this package.\n",
            "section-8 obsolete quotation",
        )

    def test_legitimate_non_authoritative_example_is_accepted(self):
        self.assertAccepted(
            ROUND8_HONEST_PADDING
            + "Invalid example:\n"
            + f'<!-- {PROSE_GUARD_EXEMPTION_BEGIN} reason="non-authoritative example" -->\n'
            + '> "Gate A verifies the authorization digest."\n'
            + f"<!-- {PROSE_GUARD_EXEMPTION_END} -->\n"
            + "Closing framing line: no runtime enforcement exists in this package.\n",
            "section-8 invalid example",
        )

    def test_truthful_denial_forms_need_no_exemption_at_all(self):
        """The preferred remedy: negative grammar the guard parses directly."""
        for item in (
            "no authorization consumer exists",
            "Gate A is not runtime-enforced",
            "owner approval cannot currently authorize a run",
            "digests are not currently checked",
            "model invocation is not currently blocked by authorization state",
            "Evidence 0016 is not executable",
            "No current runner verifies the record.",
            "Digest verification is not implemented.",
            "The package does not demonstrate runtime authorization.",
        ):
            with self.subTest(item=item):
                self.assertEqual(
                    find_enforcement_overclaims(f"- {item}\n", name="T.md"), []
                )

    def test_text_after_the_closing_marker_is_still_scanned(self):
        text = (
            ROUND8_HONEST_PADDING
            + _legitimate_region("non-authoritative example")
            + DEMONSTRATED_BYPASS_CLAIM
            + "\n"
        )
        findings = find_enforcement_overclaims(text, name="T.md")
        self.assertTrue(any("Gate A verifies" in f for f in findings), findings)

    def test_region_boundaries_remain_fail_closed(self):
        base = ROUND8_HONEST_PADDING
        begin = f'<!-- {PROSE_GUARD_EXEMPTION_BEGIN} reason="non-authoritative example" -->'
        end = f"<!-- {PROSE_GUARD_EXEMPTION_END} -->"
        claim = "> " + DEMONSTRATED_BYPASS_CLAIM
        cases = {
            "unclosed": f"{base}Invalid example:\n{begin}\n{claim}\n",
            "unopened": f"{base}{claim}\n{end}\n",
            "nested": (
                f"{base}Invalid example:\n{begin}\n{begin}\n{claim}\n{end}\n{end}\n"
            ),
            "oversized": (
                f"{base}Invalid example:\n{begin}\n"
                + "\n".join([claim] * (MAX_EXEMPTION_REGION_LINES + 1))
                + f"\n{end}\n"
            ),
            "inline-code marker": (
                f"{base}Invalid example:\nWe write `{begin}` in docs.\n"
                f"{claim}\n`{end}`\n"
            ),
            "near-miss spelling": (
                f"{base}Invalid example:\n"
                "BEGIN_PROSE_GUARD_EXEMPTIONS\n"
                f"{claim}\nEND_PROSE_GUARD_EXEMPTIONS\n"
            ),
        }
        for label, text in cases.items():
            with self.subTest(case=label):
                self.assertTrue(
                    find_enforcement_overclaims(text, name="T.md"),
                    f"boundary case not fail-closed: {label}",
                )


# ---------------------------------------------------------------------------
# Section 10: reviewer-visible exemption inventory.
#
# Deterministic, auditable, and derived from the live files -- not a hand-kept
# table that can drift. This is test output only: it creates no evidence file
# and no runtime artifact.
# ---------------------------------------------------------------------------

# Every real exemption region expected in the governing files after round 8.
EXPECTED_REAL_EXEMPTION_REGIONS = 4
EXPECTED_REAL_EXEMPTION_REASONS = {"non-authoritative example": 4}


def build_exemption_inventory():
    """Return one auditable record per real exemption region."""
    inventory = []
    for path in GOVERNING_FILES:
        lines = path.read_text(encoding="utf-8").splitlines()
        open_at = None
        reason = None
        for lineno, raw in enumerate(lines, start=1):
            begin = _match_exemption_begin(raw)
            if begin is not None and begin[0] == "ok":
                open_at, reason = lineno, begin[1]
            elif _is_exemption_end(raw) and open_at is not None:
                body = _region_body_lines(lines, open_at, lineno)
                introducer = _region_introducer(lines, open_at)
                problems = REASON_CONTENT_VALIDATORS[reason](
                    body, introducer, path.name, open_at
                )
                inventory.append(
                    {
                        "file": path.name,
                        "opening_line": open_at,
                        "closing_line": lineno,
                        "reason": reason,
                        "introducer": introducer[1].strip() if introducer else None,
                        "introducer_line": introducer[0] if introducer else None,
                        "region_size_lines": lineno - open_at - 1,
                        "content_lines": len(body),
                        "validator_result": "PASS" if not problems else "FAIL",
                        "validator_problems": problems,
                    }
                )
                open_at, reason = None, None
    return inventory


class Round8ExemptionInventory(unittest.TestCase):
    """A reviewer must be able to audit every real exemption in one place."""

    def setUp(self):
        self.inventory = build_exemption_inventory()

    def test_real_region_count_dropped_from_six_to_four(self):
        self.assertEqual(len(self.inventory), EXPECTED_REAL_EXEMPTION_REGIONS)

    def test_no_real_truthful_denial_list_region_remains(self):
        """Both were eliminated by rewriting into scanned negative grammar."""
        self.assertEqual(
            [r for r in self.inventory if r["reason"] == "truthful denial list"], []
        )

    def test_every_real_region_passes_its_reason_content_contract(self):
        for record in self.inventory:
            with self.subTest(file=record["file"], line=record["opening_line"]):
                self.assertEqual(
                    record["validator_result"],
                    "PASS",
                    record["validator_problems"],
                )

    def test_every_real_region_has_a_recorded_introducer_and_size(self):
        for record in self.inventory:
            with self.subTest(file=record["file"], line=record["opening_line"]):
                self.assertIsNotNone(record["introducer"])
                self.assertLess(record["introducer_line"], record["opening_line"])
                self.assertGreater(record["region_size_lines"], 0)
                self.assertLessEqual(
                    record["region_size_lines"], MAX_EXEMPTION_REGION_LINES
                )

    def test_reason_distribution_is_exactly_as_documented(self):
        counts = {}
        for record in self.inventory:
            counts[record["reason"]] = counts.get(record["reason"], 0) + 1
        self.assertEqual(counts, EXPECTED_REAL_EXEMPTION_REASONS)

    def test_inventory_is_deterministic(self):
        self.assertEqual(self.inventory, build_exemption_inventory())

    def test_inventory_renders_as_an_ascii_table(self):
        """ASCII-only: this repository's console is cp1252."""
        rows = [
            "| file | open | close | reason | introducer | lines | result |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for r in self.inventory:
            rows.append(
                f"| {r['file']} | {r['opening_line']} | {r['closing_line']} "
                f"| {r['reason']} | {r['introducer']} | "
                f"{r['region_size_lines']} | {r['validator_result']} |"
            )
        table = "\n".join(rows)
        self.assertTrue(table.isascii(), "inventory table must be ASCII-only")
        self.assertEqual(
            len(rows), EXPECTED_REAL_EXEMPTION_REGIONS + 2, table
        )


class Round8GuardScopeLanguageIsHonest(unittest.TestCase):
    """The docs must describe the two-layer guard without overclaiming."""

    def test_package_states_reasons_are_validated_contracts(self):
        # Normalized: the required statements are prose, so line wrapping and
        # Markdown emphasis must not decide whether they are present.
        text = re.sub(
            r"\s+", " ", PACKAGE_PATH.read_text(encoding="utf-8").replace("*", "")
        )
        for phrase in (
            "not merely vocabulary labels",
            "mechanically validated content contract",
            "cannot hide an affirmative current-enforcement claim",
            "obvious semantic mismatch mechanically fails its reason contract",
            "deterministic lexical/structural guard",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_package_does_not_claim_semantic_understanding(self):
        text = PACKAGE_PATH.read_text(encoding="utf-8").lower()
        for forbidden in (
            "perfect natural-language understanding",
            "general semantic analyzer of english",
            "fully understands english",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)

    def test_reason_accuracy_still_requires_manual_review(self):
        text = PACKAGE_PATH.read_text(encoding="utf-8")
        self.assertIn("manual review", text)


# ===========================================================================
# Round 9: the example-region bypasses demonstrated by the eighth review.
#
# The eighth review executed attacks against `_validate_example_region` and
# smuggled the claim below past the guard under
# reason="non-authoritative example". The root cause was that the example
# validator checked illustrative SHAPE only and never ran the shared
# enforcement scanner, while its introducer test was an unbound substring
# search for the token `example`.
#
# Every string in this section bypassed the guard at head
# 3fe57e10b9e203575c364848ae2d314e1b026dd9 in its immediately-bound form.
# ===========================================================================

ROUND9_CLAIM = "Gate A verifies the authorization digest before every invocation."
_R9_BEGIN = f'<!-- {PROSE_GUARD_EXEMPTION_BEGIN} reason="non-authoritative example" -->'
_R9_END = f"<!-- {PROSE_GUARD_EXEMPTION_END} -->"


def _round9_doc(body):
    return ROUND8_HONEST_PADDING + body


class Round9ExampleRegionRunsTheSharedScanner(unittest.TestCase):
    """The invariant: illustrative shape never exempts content by itself."""

    def test_example_validator_calls_the_shared_clause_scanner(self):
        """Architectural: the example validator must use `_scan_clauses`."""
        src = inspect.getsource(_validate_example_region)
        self.assertIn("_scan_clauses", src)

    def test_no_weaker_example_only_lexicon_exists(self):
        src = inspect.getsource(_validate_example_region)
        self.assertNotIn("_EXAMPLE_OVERCLAIM", src)

    def test_permissive_label_column_heuristic_is_gone(self):
        for gone in ("_is_label_column", "_LABEL_COLUMN_RE"):
            with self.subTest(symbol=gone):
                self.assertNotIn(gone, globals())

    def test_example_introducer_set_is_small_and_closed(self):
        self.assertLessEqual(len(_APPROVED_EXAMPLE_INTRODUCERS), 6)
        for intro in _APPROVED_EXAMPLE_INTRODUCERS:
            with self.subTest(introducer=intro):
                self.assertTrue(
                    _is_approved_example_introducer(intro + ":"),
                    intro,
                )


class Round9DemonstratedExampleBypasses(unittest.TestCase):
    """Section 8: all seven demonstrated bypasses must now be rejected."""

    def assertRejected(self, text, label):
        findings = find_enforcement_overclaims(_round9_doc(text), name="T.md")
        self.assertTrue(findings, "BYPASS still accepted (%s): %r" % (label, text))

    # 1. arbitrary label plus two spaces before a false claim
    def test_bypass_1_arbitrary_label_plus_two_spaces(self):
        self.assertRejected(
            "Invalid example:\n%s\nNonAuthoritative  %s\n%s\n"
            % (_R9_BEGIN, ROUND9_CLAIM, _R9_END),
            "arbitrary label + two spaces",
        )

    def test_bypass_1b_any_alphabetic_label_plus_two_spaces(self):
        self.assertRejected(
            "Invalid example:\n%s\nFoo  %s\n%s\n"
            % (_R9_BEGIN, ROUND9_CLAIM, _R9_END),
            "any alphabetic label + two spaces",
        )

    # 2. `Not an example:` introducer
    def test_bypass_2_not_an_example_introducer(self):
        self.assertRejected(
            "Not an example:\n%s\n> %s\n%s\n" % (_R9_BEGIN, ROUND9_CLAIM, _R9_END),
            "Not an example: introducer",
        )

    def test_bypass_2b_negated_and_authoritative_introducers(self):
        for intro in (
            "This is not an example:",
            "Example implementation:",
            "Current example:",
            "Production example:",
            "Authoritative example:",
            "Example requirement:",
        ):
            with self.subTest(introducer=intro):
                self.assertRejected(
                    '%s\n%s\n> "%s"\n%s\n'
                    % (intro, _R9_BEGIN, ROUND9_CLAIM, _R9_END),
                    "misleading introducer %r" % intro,
                )

    # 3. distant `## Example gallery` heading
    def test_bypass_3_distant_example_gallery_heading(self):
        self.assertRejected(
            "## Example gallery\n\nSeveral unrelated paragraphs follow.\n\n"
            "%s\n> %s\n%s\n" % (_R9_BEGIN, ROUND9_CLAIM, _R9_END),
            "distant Example gallery heading",
        )

    def test_bypass_3b_adjacent_example_heading(self):
        self.assertRejected(
            '## Example gallery\n%s\n> "%s"\n%s\n'
            % (_R9_BEGIN, ROUND9_CLAIM, _R9_END),
            "adjacent Example heading",
        )

    # 4. blockquote containing a false enforcement claim
    def test_bypass_4_bare_blockquote_is_not_illustrative_enough(self):
        self.assertRejected(
            "Example:\n%s\n> %s\n%s\n" % (_R9_BEGIN, ROUND9_CLAIM, _R9_END),
            "bare blockquote under generic Example:",
        )

    # 5. unrelated table column containing `Example`
    def test_bypass_5_unrelated_table_column(self):
        self.assertRejected(
            "| Example | Description |\n|---|---|\n%s\n| unrelated | %s |\n%s\n"
            % (_R9_BEGIN, ROUND9_CLAIM, _R9_END),
            "unrelated table column containing Example",
        )

    def test_bypass_5b_table_header_row_as_introducer(self):
        self.assertRejected(
            "| Example | Description |\n%s\n> %s\n%s\n"
            % (_R9_BEGIN, ROUND9_CLAIM, _R9_END),
            "table header row as introducer",
        )

    # 6. `Example` appearing after the false claim
    def test_bypass_6_example_token_after_the_claim(self):
        self.assertRejected(
            "%s | Example\n%s\n> %s\n%s\n"
            % (ROUND9_CLAIM, _R9_BEGIN, ROUND9_CLAIM, _R9_END),
            "Example token trailing the claim",
        )

    def test_bypass_6b_example_trailing_an_unrelated_line(self):
        self.assertRejected(
            'See the gallery below. | Example\n%s\n> "%s"\n%s\n'
            % (_R9_BEGIN, ROUND9_CLAIM, _R9_END),
            "Example trailing unrelated prose",
        )

    # 7. inline-code or link-target `Example` token
    def test_bypass_7_inline_code_example_token(self):
        self.assertRejected(
            "`Example:` %s\n%s\n> %s\n%s\n"
            % (ROUND9_CLAIM, _R9_BEGIN, ROUND9_CLAIM, _R9_END),
            "inline-code Example token",
        )

    def test_bypass_7b_inline_code_link_and_comment_introducers(self):
        for intro in (
            "`Example:` see below.",
            "[see](./docs/Example.md)",
            "<!-- Invalid example: -->",
        ):
            with self.subTest(introducer=intro):
                self.assertRejected(
                    '%s\n%s\n> "%s"\n%s\n'
                    % (intro, _R9_BEGIN, ROUND9_CLAIM, _R9_END),
                    "non-prose introducer %r" % intro,
                )


class Round9StrongerExampleRegionAttacks(unittest.TestCase):
    """Section 9: a valid introducer must not license substantive content."""

    VALID = "Invalid example:"

    def assertRejected(self, text, label):
        findings = find_enforcement_overclaims(_round9_doc(text), name="T.md")
        self.assertTrue(findings, "wrongly exempted (%s): %r" % (label, text))

    def _region(self, body):
        return "%s\n%s\n%s\n%s\n" % (self.VALID, _R9_BEGIN, body, _R9_END)

    def test_valid_introducer_plus_unquoted_claims_of_every_shape(self):
        for shape, claim in (
            ("active", "Gate A verifies the authorization digest."),
            ("passive", "The authorization digest is verified by Gate A."),
            ("emphatic", "Gate A does verify the authorization digest."),
            ("progressive", "Gate A is verifying the authorization digest."),
        ):
            with self.subTest(shape=shape):
                self.assertRejected(self._region(claim), "%s claim" % shape)

    def test_example_quote_followed_by_current_authoritative_prose(self):
        self.assertRejected(
            self._region(
                '> "Gate A verifies the digest."\n'
                "Gate A enforces the authorization digest today."
            ),
            "quote plus current authoritative prose",
        )

    def test_valid_first_line_then_false_later_line(self):
        self.assertRejected(
            self._region('> "Some obsolete wording here."\n> ' + ROUND9_CLAIM),
            "valid first line, false later line",
        )

    def test_requirement_hidden_after_a_quoted_example(self):
        self.assertRejected(
            self._region(
                '> "Illustrative only."\n'
                "Every invocation must present a verified digest."
            ),
            "requirement after a quoted example",
        )

    def test_table_with_example_in_one_row_and_claim_in_another(self):
        self.assertRejected(
            self._region("| Example | ok |\n| real | %s |" % ROUND9_CLAIM),
            "Example row plus claim row",
        )

    def test_false_claim_in_a_neighbouring_cell(self):
        self.assertRejected(
            self._region(
                '| Non-authoritative example | "old wording" | %s |' % ROUND9_CLAIM
            ),
            "false claim in a neighbouring cell",
        )

    def test_mixed_denial_plus_enforcement_clause(self):
        self.assertRejected(
            self._region(
                "This does not prove ownership, and Gate A verifies the digest."
            ),
            "mixed denial plus enforcement clause",
        )

    def test_region_with_two_purposes(self):
        self.assertRejected(
            self._region(
                '> "Invalid wording sample."\n'
                "This section also documents that Gate A blocks unauthorized "
                "invocation."
            ),
            "region with two purposes",
        )

    def test_oversized_example_region_fails(self):
        body = "\n".join(
            '> "sample wording %d"' % i
            for i in range(MAX_EXAMPLE_REGION_LINES + 2)
        )
        self.assertRejected(self._region(body), "oversized example region")


class Round9LegitimateExamplesStillAccepted(unittest.TestCase):
    """Section 10: the narrow, honest example form must keep working."""

    TAIL = "Closing framing line: no runtime enforcement exists in this package.\n"

    def assertAccepted(self, text, label):
        findings = find_enforcement_overclaims(_round9_doc(text), name="T.md")
        self.assertEqual(findings, [], "wrongly rejected (%s)" % label)

    def test_each_approved_introducer_is_accepted(self):
        for intro in _APPROVED_EXAMPLE_INTRODUCERS:
            with self.subTest(introducer=intro):
                self.assertAccepted(
                    '%s:\n%s\n> "%s"\n%s\n'
                    % (intro[0].upper() + intro[1:], _R9_BEGIN,
                       ROUND9_CLAIM, _R9_END)
                    + self.TAIL,
                    "approved introducer %r" % intro,
                )

    def test_curly_quoted_exhibit_is_accepted(self):
        self.assertAccepted(
            "Invalid example:\n%s\n> \u201c%s\u201d\n%s\n"
            % (_R9_BEGIN, ROUND9_CLAIM, _R9_END)
            + self.TAIL,
            "curly-quoted exhibit",
        )

    def test_prose_after_the_closing_marker_is_still_scanned(self):
        findings = find_enforcement_overclaims(
            _round9_doc(
                'Invalid example:\n%s\n> "old wording"\n%s\n%s\n'
                % (_R9_BEGIN, _R9_END, ROUND9_CLAIM)
            ),
            name="T.md",
        )
        self.assertTrue(findings, "text after the closing marker was not scanned")


ROUND10_TAIL = (
    "Closing framing line: no runtime enforcement exists in this package.\n"
)


def _round10_region(body):
    """One example region with `body` as its content, plus honest framing."""
    return (
        "Invalid example:\n%s\n%s\n%s\n" % (_R9_BEGIN, body, _R9_END)
    ) + ROUND10_TAIL


class Round10QuoteParserGrammar(unittest.TestCase):
    """Round 10: the quoted-exhibit grammar itself, in isolation.

    The contract is deliberately narrow: one line, one balanced quoted
    exhibit, no meaningful unquoted remainder.
    """

    def test_straight_double_exhibit_parses(self):
        result = parse_quoted_exhibit('> "Gate A verifies the digest."')
        self.assertTrue(result.valid, result)
        self.assertEqual(result.quote_style, QUOTE_STYLE_STRAIGHT_DOUBLE)
        self.assertEqual(result.exhibit, "Gate A verifies the digest.")
        self.assertEqual(result.unquoted_remainder.strip(), "")

    def test_smart_double_exhibit_parses(self):
        result = parse_quoted_exhibit("> “Gate A verifies the digest.”")
        self.assertTrue(result.valid, result)
        self.assertEqual(result.quote_style, QUOTE_STYLE_SMART_DOUBLE)
        self.assertEqual(result.exhibit, "Gate A verifies the digest.")

    def test_list_bullet_and_indentation_prefixes_are_structural(self):
        for prefix in ("> ", "- ", "  * ", "1. ", ">   - ", "    "):
            with self.subTest(prefix=prefix):
                result = parse_quoted_exhibit(
                    '%s"Gate A verifies the digest."' % prefix
                )
                self.assertTrue(result.valid, result)

    def test_terminal_punctuation_after_the_close_is_structural(self):
        for tail in ("", ".", ",", ";", ":", "!", "?", "  "):
            with self.subTest(tail=tail):
                result = parse_quoted_exhibit(
                    '> "Gate A verifies the digest."%s' % tail
                )
                self.assertTrue(result.valid, result)

    def test_supported_and_unsupported_quote_styles_are_explicit(self):
        self.assertEqual(
            SUPPORTED_QUOTE_STYLES,
            (QUOTE_STYLE_STRAIGHT_DOUBLE, QUOTE_STYLE_SMART_DOUBLE),
        )
        for mark in "„‹›«»「」‚":
            with self.subTest(mark=mark):
                result = parse_quoted_exhibit(
                    "> %sGate A verifies the digest.%s" % (mark, mark)
                )
                self.assertFalse(result.valid, result)
                self.assertEqual(result.reason, QUOTE_FAIL_UNSUPPORTED_STYLE)

    def test_structured_failure_reasons(self):
        cases = (
            ("Gate A \"verifies the digest.\"", QUOTE_FAIL_LEADING),
            ("\"Gate A verifies\" the digest.", QUOTE_FAIL_TRAILING),
            ("\"Gate A\" verifies \"the digest.\"", QUOTE_FAIL_MULTIPLE),
            ("\"a.\" \"b.\"", QUOTE_FAIL_MULTIPLE),
            ("\"Gate A verifies the digest.\" (Current behavior.)",
             QUOTE_FAIL_TRAILING),
            ("\"Gate A verifies the digest,\" and the runtime blocks it.",
             QUOTE_FAIL_TRAILING),
            ("\"Gate A verifies the digest.\"; the runtime blocks calls.",
             QUOTE_FAIL_TRAILING),
            ("Before execution, \"Gate A verifies the digest.\"",
             QUOTE_FAIL_LEADING),
            ("\"Gate A verifies the digest.", QUOTE_FAIL_UNBALANCED),
            ("Gate A verifies the digest.\"", QUOTE_FAIL_UNBALANCED),
            ("“Gate A verifies the digest.\"", QUOTE_FAIL_MISMATCHED),
            ("\"Gate A verifies the digest.”", QUOTE_FAIL_MISMATCHED),
            ("“Gate A verifies the digest.", QUOTE_FAIL_MULTILINE),
            ("Gate A verifies the digest.”", QUOTE_FAIL_UNBALANCED),
            ("\"Gate A 'verifies' the digest.\"", QUOTE_FAIL_UNSUPPORTED_STYLE),
            ('"Gate A \\"verifies\\" the digest."',
             QUOTE_FAIL_UNSUPPORTED_STYLE),
            ("`Gate A verifies the digest.`", QUOTE_FAIL_INLINE_CODE),
            ("Gate A verifies the digest.", QUOTE_FAIL_NO_EXHIBIT),
            ('""', QUOTE_FAIL_NO_EXHIBIT),
        )
        for line, reason in cases:
            with self.subTest(line=line):
                result = parse_quoted_exhibit("> " + line)
                self.assertFalse(result.valid, result)
                self.assertEqual(result.reason, reason, result)
                self.assertIn(result.reason, QUOTE_PARSE_FAILURE_REASONS)

    def test_word_internal_apostrophes_are_not_nested_quotes(self):
        for exhibit in (
            "Gate A's digest is verified by the runtime.",
            "The runtime doesn't verify the digest.",
        ):
            with self.subTest(exhibit=exhibit):
                result = parse_quoted_exhibit('> "%s"' % exhibit)
                self.assertTrue(result.valid, result)

    def test_nested_and_escaped_and_multiline_are_unsupported(self):
        # Documented, deliberate choices -- all fail closed rather than being
        # silently misparsed.
        self.assertFalse(
            parse_quoted_exhibit("> \"Gate A 'verifies' the digest.\"").valid
        )
        self.assertFalse(
            parse_quoted_exhibit('> "Gate A \\"verifies\\" the digest."').valid
        )
        self.assertFalse(parse_quoted_exhibit('> "Gate A verifies').valid)


class Round10QuoteBoundaryBypassesAreClosed(unittest.TestCase):
    """The compositional split-across-the-quote-boundary attack matrix.

    Every one of these was ACCEPTED by the round-9 strip-and-scan helper, or
    is a near neighbour of one that was. All must now be REJECTED.
    """

    def assertRejected(self, line, label):
        findings = find_enforcement_overclaims(
            _round9_doc(_round10_region("> " + line)), name="T.md"
        )
        self.assertTrue(findings, "wrongly exempted (%s): %r" % (label, line))

    def test_four_confirmed_round9_bypasses(self):
        for label, line in (
            ("partial predicate quoted",
             'Gate A "verifies the authorization digest."'),
            ("partial subject and predicate quoted",
             '"Gate A verifies" the authorization digest.'),
            ("subject and object in separate spans",
             '"Gate A" verifies "the authorization digest."'),
            ("quote plus parenthetical remainder",
             '"Gate A verifies the authorization digest." '
             "(This is current runtime behavior.)"),
        ):
            with self.subTest(case=label):
                self.assertRejected(line, label)

    def test_partial_quoting_of_every_sentence_part(self):
        for label, line in (
            ("subject only", '"Gate A" verifies the authorization digest.'),
            ("predicate only", 'Gate A "verifies" the authorization digest.'),
            ("object only", 'Gate A verifies "the authorization digest."'),
        ):
            with self.subTest(case=label):
                self.assertRejected(line, label)

    def test_remainder_shapes_outside_the_exhibit(self):
        for label, line in (
            ("two independent exhibits",
             '"Gate A verifies the digest." "The runtime blocks invocation."'),
            ("conjunction remainder",
             '"Gate A verifies the digest," and the runtime blocks invocation.'),
            ("semicolon remainder",
             '"Gate A verifies the digest."; the runtime blocks calls.'),
            ("leading prose",
             'Before execution, "Gate A verifies the digest."'),
            ("trailing prose",
             '"Gate A verifies the digest." The runtime blocks invocation.'),
        ):
            with self.subTest(case=label):
                self.assertRejected(line, label)

    def test_malformed_quote_shapes(self):
        for label, line in (
            ("unbalanced opening", '"Gate A verifies the digest.'),
            ("unbalanced closing", 'Gate A verifies the digest."'),
            ("mismatched smart then straight",
             "“Gate A verifies the digest.\""),
            ("mismatched straight then smart",
             "\"Gate A verifies the digest.”"),
            ("nested quotes", "\"Gate A 'verifies' the digest.\""),
            ("escaped quotes", '"Gate A \\"verifies\\" the digest."'),
            ("inline code", "`Gate A verifies the digest.`"),
        ):
            with self.subTest(case=label):
                self.assertRejected(line, label)

    def test_multiline_quote_span_is_rejected(self):
        findings = find_enforcement_overclaims(
            _round9_doc(
                _round10_region(
                    "> “Gate A verifies\n> the authorization digest.”"
                )
            ),
            name="T.md",
        )
        self.assertTrue(findings, "multi-line quote span was exempted")

    def test_quotation_outside_an_exemption_is_still_scanned(self):
        for label, body in (
            ("bare quotation", '"Gate A verifies the authorization digest."'),
            ("blockquoted quotation",
             '> "Gate A verifies the authorization digest."'),
            ("reported speech",
             'The document says "Gate A verifies the authorization digest."'),
        ):
            with self.subTest(case=label):
                findings = find_enforcement_overclaims(
                    _round9_doc(body), name="T.md"
                )
                self.assertTrue(
                    findings,
                    "quotation outside an exemption suppressed scanning (%s)"
                    % label,
                )

    def test_unquoted_control_confirms_segmentation_was_the_defect(self):
        # The same sentence, fully unquoted, was rejected even on the old head.
        # Quote segmentation -- not lexicon coverage -- was the bypass.
        self.assertRejected(
            "Gate A verifies the authorization digest.", "unquoted control"
        )

    def test_the_narrow_valid_form_still_works(self):
        for label, line in (
            ("straight double", '"Gate A verifies the authorization digest."'),
            ("smart double",
             "“Gate A verifies the authorization digest.”"),
        ):
            with self.subTest(case=label):
                findings = find_enforcement_overclaims(
                    _round9_doc(_round10_region("> " + line)), name="T.md"
                )
                self.assertEqual(
                    findings, [], "wrongly rejected valid exhibit (%s)" % label
                )


class Round10StripAndScanIsRetired(unittest.TestCase):
    """The permissive substitution helper must not come back."""

    def test_strip_quoted_spans_helper_is_gone(self):
        self.assertNotIn("_strip_quoted_spans", globals())

    def test_example_validator_uses_the_exhibit_grammar(self):
        source = inspect.getsource(_validate_example_region)
        self.assertIn("parse_quoted_exhibit", source)
        self.assertNotIn("_strip_quoted_spans", source)

    def test_shared_scanner_is_still_used_by_the_example_validator(self):
        self.assertIn("_scan_clauses", inspect.getsource(_validate_example_region))


class Round10RealExemptionRegionsMeetTheGrammar(unittest.TestCase):
    """Every checked-in example region must satisfy the narrow contract."""

    DOCS = (
        "docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md",
        "docs/experiments/STAGE-1-AUTEUR-EXECUTION-PACKAGE.md",
        "docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md",
    )

    def _regions(self):
        found = []
        for rel in self.DOCS:
            path = REPO_ROOT / rel
            if not path.exists():
                continue
            lines = path.read_text(encoding="utf-8").splitlines()
            open_at = None
            for lineno, raw in enumerate(lines, start=1):
                if _match_exemption_begin(raw) is not None:
                    open_at = lineno
                elif _is_exemption_end(raw) and open_at is not None:
                    found.append(
                        (rel, open_at,
                         _region_body_lines(lines, open_at, lineno))
                    )
                    open_at = None
        return found

    def test_all_checked_in_example_regions_parse_as_single_exhibits(self):
        regions = self._regions()
        self.assertTrue(regions, "no checked-in exemption regions were found")
        for rel, open_at, body in regions:
            for lineno, raw in body:
                with self.subTest(doc=rel, line=lineno):
                    result = parse_quoted_exhibit(raw)
                    self.assertTrue(
                        result.valid,
                        "%s line %d does not meet the exhibit grammar: %r"
                        % (rel, lineno, result),
                    )
                    self.assertIn(result.quote_style, SUPPORTED_QUOTE_STYLES)
                    self.assertEqual(result.unquoted_remainder.strip(), "")

    def test_real_documents_remain_clean_under_the_new_grammar(self):
        for rel in self.DOCS:
            path = REPO_ROOT / rel
            if not path.exists():
                continue
            with self.subTest(doc=rel):
                assert_no_unpermitted_overclaims(
                    self,
                    find_enforcement_overclaims(
                        path.read_text(encoding="utf-8"), name=rel
                    ),
                    rel,
                )


if __name__ == "__main__":
    unittest.main()
