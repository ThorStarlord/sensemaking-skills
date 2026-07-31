"""Adversarial tests for the status-aware prose-honesty guard.

Scope of this module
--------------------

This is the self-test battery for ``tests/support/state_honesty_guard.py``, the
replacement for the obsolete premise of the PR #107 prose-honesty guard. It is
deliberately built from SYNTHETIC fixture strings, not from edits to the governed
documents. The governed documents are not touched by this change; they still
contain the stale absence claims they acquired while the Gate A consumer did not
exist, and a follow-up task rewrites them under this guard.

Two failure modes are tested with equal weight:

* **false-positive resistance** -- truthful present-tense descriptions of merged
  runtime behavior must NOT be flagged. This is the defect that made PR #111
  unfinishable under the old guard.
* **false-negative resistance** -- stale absence claims, false authorization and
  execution claims, and claims hidden inside code fences or YAML blocks must
  still be flagged.

Nothing here invokes a model, runs Stage 1, or creates evidence output.
"""

import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tests" / "support"))

import state_honesty_guard as guard  # noqa: E402


# The state under which the guard's behavior is specified here. It matches the
# real repository today, but it is passed EXPLICITLY so these tests describe the
# guard's logic rather than silently re-deriving whatever the repo happens to
# say. A separate test below asserts the real derived state matches this.
POST_GATE_A_STATE = {
    "gate_a_consumer_exists": True,
    "gate_a_consumer_wired": True,
    "runtime_enforcement_exists": True,
    "run_control_directory_exists": False,
    "authorization_record_exists": False,
    "authorization_record_digest_exists": False,
    "owner_approval_exists": False,
    "stage1_authorized": False,
    "package_runnable": False,
    "evidence_0016_exists": False,
    "real_model_invoked": False,
}


class GuardBase(unittest.TestCase):
    state = POST_GATE_A_STATE

    def scan(self, text):
        return guard.find_state_contradictions(text, name="T.md", state=self.state)

    def assertAccepted(self, text):
        findings = self.scan(text)
        self.assertEqual(findings, [], f"wrongly rejected: {text!r}\n" + "\n".join(findings))

    def assertRejected(self, text):
        self.assertTrue(self.scan(text), f"NOT rejected: {text!r}")


class StateFactsAreDerivedNotDeclared(GuardBase):
    """The guard reads the world; it does not assert what the world looks like."""

    def test_derived_state_matches_the_specified_state(self):
        self.assertEqual(guard.compute_current_state(), POST_GATE_A_STATE)

    def test_consumer_facts_trace_to_real_files(self):
        self.assertTrue(guard.CONSUMER_PATH.is_file())
        self.assertTrue(guard.BOUNDARY_PROOF_PATH.is_file())
        body = guard.PROVIDER_BOUNDARY_PATH.read_text(encoding="utf-8")
        self.assertIn("gate_a_authorization", body)

    def test_negative_facts_trace_to_genuinely_absent_artifacts(self):
        contract = guard.load_contract()
        for field in (
            "execution_authorization_record_path",
            "owner_approval_artifact_path",
        ):
            self.assertFalse(guard._contract_path(contract, field).exists())

    def test_polarity_follows_the_derived_value_not_a_literal(self):
        """Flip the world and the same sentence flips verdict. No hardcoding."""
        sentence = "No authorization consumer exists.\n"
        self.assertTrue(
            guard.find_state_contradictions(
                sentence, name="T.md", state=POST_GATE_A_STATE
            )
        )
        pre_merge = dict(POST_GATE_A_STATE)
        pre_merge.update(
            gate_a_consumer_exists=False,
            gate_a_consumer_wired=False,
            runtime_enforcement_exists=False,
        )
        self.assertEqual(
            guard.find_state_contradictions(sentence, name="T.md", state=pre_merge), []
        )
        # ... and the mirror image: under the pre-merge world the truthful
        # post-merge sentence becomes the violation again.
        self.assertTrue(
            guard.find_state_contradictions(
                "The Gate A consumer exists.\n", name="T.md", state=pre_merge
            )
        )

    def test_no_boolean_literal_declares_world_state(self):
        """compute_current_state must not hardcode a fact as True/False."""
        source = (
            Path(guard.__file__).read_text(encoding="utf-8").split(
                "def compute_current_state"
            )[1].split("\n# ---")[0]
        )
        for fact in POST_GATE_A_STATE:
            self.assertNotRegex(
                source,
                rf'"{re.escape(fact)}":\s*(?:True|False)\s*,',
                f"{fact} is declared by literal instead of derived",
            )


class CategoryOneCurrentImplementationFactsAreLegal(GuardBase):
    """Category 1: truthful present-tense claims about merged runtime behavior."""

    CASES = (
        "The Gate A consumer exists.",
        "The consumer validates the authorization record.",
        "The provider boundary requires the typed capability.",
        "The runtime recomputes the record digest.",
        "The runtime verifies the Gate D checklist digest.",
        "Gate A verifies the authorization digest before every invocation.",
        "The runner blocks an unauthorized invocation.",
        "Gate A is runtime-enforced.",
        "The authorization digest is verified by Gate A.",
        "Gate A does verify the digest.",
        "The runner is validating the approval.",
        "scripts/workflow-runtime.py performs the authorization preflight.",
        "The Gate A consumer is wired into the provider boundaries.",
        "Runtime enforcement exists.",
    )

    def test_truthful_current_implementation_claims_are_accepted(self):
        for text in self.CASES:
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    def test_the_exact_sentence_that_blocked_pr_111_is_accepted(self):
        self.assertAccepted("The runtime verifies the Gate D checklist digest.\n")

    def test_old_guard_rejected_what_the_new_guard_accepts(self):
        """Documents the premise change rather than asserting it by comment."""
        sys.path.insert(0, str(REPO_ROOT / "tests"))
        import test_stage1_auteur_prep_package as legacy

        sentence = "The runtime verifies the Gate D checklist digest."
        self.assertNotEqual(legacy.find_enforcement_overclaims(sentence), [])
        self.assertEqual(self.scan(sentence + "\n"), [])


class CategoryTwoAuthorizationStateMustStayNegative(GuardBase):
    """Category 2: false presence claims about authorization/execution state."""

    FALSE_CLAIMS = (
        "Owner approval exists.",
        "owner-approval.md exists.",
        "Owner approval has been signed.",
        "Owner approval is in place.",
        "The package is runnable.",
        "Stage 1 is authorized.",
        "The run is authorized.",
        "Evidence 0016 has executed.",
        "Evidence 0016 has been created.",
        "A real model was invoked.",
        "Real model invocation occurred.",
        "The authorization record exists.",
        "authorization-record.sha256 exists.",
        "The run-control directory exists.",
    )

    def test_false_presence_claims_are_rejected(self):
        for text in self.FALSE_CLAIMS:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    TRUTHFUL_NEGATIVES = (
        "Stage 1 is not authorized.",
        "owner-approval.md does not exist.",
        "No owner approval exists.",
        "No owner-approval artifact exists.",
        "The package is not runnable.",
        "Evidence 0016 has not been created.",
        "No real model has been invoked.",
        "No authorization record exists.",
        "No authorization-record digest file exists.",
        "No run-control directory exists.",
        "No Stage 1 run is authorized by this revision.",
    )

    def test_truthful_negative_statements_are_accepted(self):
        for text in self.TRUTHFUL_NEGATIVES:
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    def test_a_negator_wrapped_across_lines_still_governs(self):
        """Line-wise scanning would sever the negator and fire spuriously."""
        self.assertAccepted("No third-party\nowner approval exists yet either.\n")

    def test_a_distant_negator_does_not_exempt(self):
        """Adjacency, not proximity. A negator in another clause grants nothing."""
        self.assertRejected(
            "No retry is permitted, and owner approval exists for this run.\n"
        )


class CategoryThreeHistoricalAndProspectiveFraming(GuardBase):
    """Category 3: legal only when EXPLICITLY marked, never inferred from grammar."""

    FRAMED = (
        "Before PR #109, no consumer existed.",
        "Before PR #109, no authorization consumer exists in the tree.",
        "Historically, Gate A is not runtime-enforced.",
        "Previously, the authorization consumer is not implemented.",
        "The original preparation package specified a future consumer, and stated "
        "that no such consumer exists.",
        "A future owner approval may authorize dry preflight.",
        "Owner approval will exist only after the owner signs it.",
        "The package must be runnable before Evidence 0016 is created.",
    )

    def test_explicitly_framed_statements_are_accepted(self):
        for text in self.FRAMED:
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    UNFRAMED = (
        "No consumer exists.",
        "The word future appears here, and no consumer exists.",
        "In some future release, this is fine: owner approval exists.",
        "Historically this was true. No such consumer exists.",
    )

    def test_unframed_or_late_framing_is_rejected(self):
        """A framing word must GOVERN the claim, not merely be nearby."""
        for text in self.UNFRAMED:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    def test_historical_marker_must_be_sentence_initial(self):
        self.assertAccepted("Historically, no consumer exists.\n")
        self.assertRejected("No consumer exists, historically speaking.\n")


class StaleAbsenceClaimRegressionsFromPr111(GuardBase):
    """Every stale variant surfaced by the PR #111 review history."""

    VARIANTS = (
        "Gate A: NOT ENFORCED",
        "Authorization consumer: not implemented",
        "Runtime enforcement: absent",
        "The contract has no runtime consumer.",
        "No such consumer exists.",
        "None of the criteria below are satisfied today.",
        "None of them are implemented.",
        "No authorization consumer exists.",
        "Gate A is not runtime-enforced.",
        "The consumer does not exist.",
        "The consumer is not wired into Stage 1.",
        "No runtime enforcement exists.",
    )

    def test_all_stale_variants_are_rejected(self):
        for text in self.VARIANTS:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")


class CodeFencesAreNotASafeHarbor(GuardBase):
    """The evasion PR #107 closed for false claims stays closed for all claims."""

    def test_false_claim_hidden_in_a_text_fence_is_still_caught(self):
        text = "Intro paragraph.\n\n```text\nOwner approval exists.\n```\n"
        self.assertRejected(text)

    def test_stale_claim_hidden_in_a_text_fence_is_still_caught(self):
        text = "Intro paragraph.\n\n```text\nNo such consumer exists.\n```\n"
        self.assertRejected(text)

    def test_every_fence_flavor_is_scanned(self):
        for opener, closer in (
            ("```", "```"),
            ("```text", "```"),
            ("```console", "```"),
            ("~~~", "~~~"),
        ):
            with self.subTest(opener=opener):
                self.assertRejected(
                    f"Intro.\n\n{opener}\nOwner approval exists.\n{closer}\n"
                )

    def test_indented_and_blockquoted_fences_are_scanned(self):
        self.assertRejected("> ```text\n> Runtime enforcement: absent\n> ```\n")
        self.assertRejected("  ```text\n  Owner approval exists.\n  ```\n")

    def test_the_same_sentence_is_judged_identically_in_and_out_of_a_fence(self):
        for sentence in ("Owner approval exists.", "No such consumer exists."):
            with self.subTest(sentence=sentence):
                bare = self.scan(sentence + "\n")
                fenced = self.scan(f"```text\n{sentence}\n```\n")
                self.assertTrue(bare)
                self.assertTrue(fenced)
        # ... and a truthful sentence stays legal in both places.
        self.assertAccepted("The Gate A consumer exists.\n")
        self.assertAccepted("```text\nThe Gate A consumer exists.\n```\n")

    def test_old_exemption_markers_do_not_exempt_state_contradictions(self):
        """The legacy region markers have no authority over this guard."""
        text = (
            'BEGIN_PROSE_GUARD_EXEMPTION reason="non-authoritative example"\n'
            "Owner approval exists.\n"
            "END_PROSE_GUARD_EXEMPTION\n"
        )
        self.assertRejected(text)


class MachineReadableBlocksAreValidated(GuardBase):
    """YAML state blocks are checked as DATA, not merely scanned as prose."""

    def test_false_yaml_state_value_is_caught(self):
        text = "```yaml\nowner_approval_artifact_exists: true\n```\n"
        findings = self.scan(text)
        self.assertTrue(findings)
        self.assertIn("owner_approval_artifact_exists", findings[0])

    def test_stale_yaml_state_value_is_caught(self):
        text = "```yaml\ngate_a_runtime_enforcement_exists: false\n```\n"
        findings = self.scan(text)
        self.assertTrue(findings)
        self.assertIn("gate_a_runtime_enforcement_exists", findings[0])

    def test_truthful_yaml_state_values_are_accepted(self):
        text = (
            "```yaml\n"
            "gate_a_runtime_enforcement_exists: true\n"
            "gate_a_authorization_consumer_wired_to_stage1: true\n"
            "owner_approval_artifact_exists: false\n"
            "package_runnable: false\n"
            "run_control_directory_exists: false\n"
            "```\n"
        )
        self.assertAccepted(text)

    def test_every_machine_field_maps_to_a_known_fact(self):
        for field, fact in guard.MACHINE_FIELD_TO_FACT.items():
            self.assertIn(fact, POST_GATE_A_STATE, field)

    def test_package_runnable_true_is_caught_as_prose_and_as_data(self):
        self.assertRejected("The package is runnable.\n")
        self.assertRejected("```yaml\npackage_runnable: true\n```\n")


class GuardIsNotDefanged(GuardBase):
    """Structural checks that the mechanism itself has not been hollowed out."""

    def test_every_fact_has_both_pattern_directions(self):
        self.assertEqual(set(guard.FACT_LEXICONS), set(POST_GATE_A_STATE))
        for fact, lexicon in guard.FACT_LEXICONS.items():
            self.assertTrue(lexicon["affirm"], fact)
            self.assertTrue(lexicon["deny"], fact)

    def test_every_pattern_compiles(self):
        for fact, lexicon in guard.FACT_LEXICONS.items():
            for kind in ("affirm", "deny"):
                for pattern in lexicon[kind]:
                    with self.subTest(fact=fact, kind=kind, pattern=pattern):
                        re.compile(pattern, re.IGNORECASE)

    def test_each_fact_is_individually_enforced(self):
        """No fact may be silently unreachable."""
        for fact, lexicon in guard.FACT_LEXICONS.items():
            kind = "deny" if POST_GATE_A_STATE[fact] else "affirm"
            probes = {
                "gate_a_consumer_exists": "No authorization consumer exists.",
                "gate_a_consumer_wired": "The consumer is not wired into Stage 1.",
                "runtime_enforcement_exists": "Gate A is not runtime-enforced.",
                "run_control_directory_exists": "The run-control directory exists.",
                "authorization_record_exists": "The authorization record exists.",
                "authorization_record_digest_exists": (
                    "An authorization-record digest file exists."
                ),
                "owner_approval_exists": "Owner approval exists.",
                "stage1_authorized": "Stage 1 is authorized.",
                "package_runnable": "The package is runnable.",
                "evidence_0016_exists": "Evidence 0016 has executed.",
                "real_model_invoked": "A real model was invoked.",
            }
            with self.subTest(fact=fact, kind=kind):
                self.assertTrue(self.scan(probes[fact] + "\n"), fact)

    def test_guard_never_invokes_anything(self):
        source = Path(guard.__file__).read_text(encoding="utf-8")
        for forbidden in ("subprocess", "requests", "anthropic", "os.system"):
            self.assertNotIn(forbidden, source)


# ---------------------------------------------------------------------------
# The governed documents.
#
# This change replaces the GUARD, not the documents. The two SHA-pinned governed
# documents still carry the stale absence claims they acquired while the Gate A
# consumer genuinely did not exist, plus a handful of future verification steps
# written in bare present tense. Rewriting them is the explicitly separate
# follow-up task, performed together with recomputing their digests.
#
# The inventory below is therefore stated honestly rather than hidden: it pins
# the EXACT number of outstanding contradictions per document. New stale claims
# cannot be added (the count would rise) and the guard cannot be quietly
# weakened (the count would fall). The follow-up rewrite drives every entry to
# zero and deletes this inventory.
# ---------------------------------------------------------------------------

DOCS_DIR = REPO_ROOT / "docs" / "experiments"

KNOWN_OUTSTANDING_CONTRADICTIONS = {
    "STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md": 19,
    "GATE-D-STALE-DIAGNOSIS-CHECKLIST.md": 1,
    "STAGE-1-AUTEUR-EXECUTION-PACKAGE.md": 2,
}


class GovernedDocumentInventory(unittest.TestCase):
    def test_outstanding_contradictions_match_the_pinned_inventory(self):
        state = guard.compute_current_state()
        for name, expected in KNOWN_OUTSTANDING_CONTRADICTIONS.items():
            path = DOCS_DIR / name
            with self.subTest(document=name):
                self.assertTrue(path.is_file(), path)
                findings = guard.find_state_contradictions(
                    path.read_text(encoding="utf-8"), name=name, state=state
                )
                self.assertEqual(
                    len(findings),
                    expected,
                    f"{name}: outstanding state contradictions changed from "
                    f"{expected} to {len(findings)}. If the documents were "
                    f"rewritten, lower the pinned number (target: 0). If the "
                    f"guard changed, confirm it was not weakened.\n"
                    + "\n".join(findings),
                )

    def test_documents_still_state_the_true_negative_facts(self):
        """The rewrite must not swing the other way into false authorization."""
        text = (DOCS_DIR / "STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md").read_text(
            encoding="utf-8"
        )
        contract = guard.load_contract(text)
        self.assertEqual(contract["execution_authorization_status"], "NOT_AUTHORIZED")
        self.assertFalse(contract["package_runnable"])
        self.assertFalse(contract["owner_approval_artifact_exists"])


if __name__ == "__main__":
    unittest.main()
