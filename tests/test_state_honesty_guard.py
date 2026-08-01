"""Adversarial tests for the status-aware prose-honesty guard.

Scope of this module
--------------------

This is the self-test battery for ``tests/support/state_honesty_guard.py``, the
replacement for the obsolete premise of the PR #107 prose-honesty guard. It is
deliberately built from SYNTHETIC fixture strings, not from edits to the governed
documents. The follow-up rewrite of the governed documents (this PR) drove their
outstanding contradictions to zero and pinned the ratchet at the bottom of this
module accordingly.

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
    "run_control_directory_exists": True,
    "authorization_record_exists": True,
    "authorization_record_digest_exists": True,
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
        """The draft artifacts exist; only the operative approval is absent."""
        contract = guard.load_contract()
        for field in (
            "execution_authorization_record_path",
            "execution_authorization_record_digest_path",
            "run_control_directory",
        ):
            self.assertTrue(guard._contract_path(contract, field).exists(), field)
        self.assertFalse(
            guard._contract_path(contract, "owner_approval_artifact_path").exists(),
            "owner-approval.md must not exist: a draft record is not authority",
        )

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
        "The run-control directory exists.",
        "The authorization record exists.",
        "The authorization-record digest file exists.",
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
        "No Stage 1 run is authorized by this revision.",
    )

    def test_truthful_negative_statements_are_accepted(self):
        for text in self.TRUTHFUL_NEGATIVES:
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    STALE_DENIALS = (
        "No authorization record exists.",
        "No authorization-record digest file exists.",
        "No run-control directory exists.",
    )

    def test_stale_denials_of_merged_artifacts_are_rejected(self):
        """The draft record and digest now exist; denying them is stale."""
        for text in self.STALE_DENIALS:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

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


class FramingIsAsymmetric(GuardBase):
    """Independent-review regressions (PR #112 round 1).

    A fresh reviewer demonstrated that sentence-initial historical framing
    exempted the WHOLE sentence regardless of direction, so a false present-tense
    authorization claim slipped through behind a marker. That re-created, at
    sentence scope, the blanket exemption PR #107 round 5 deleted at line scope.

    Framing is now asymmetric: it may excuse denying a now-true fact, never
    affirming a still-false one.
    """

    HISTORICAL_BYPASS_ATTEMPTS = (
        "Historically, owner approval exists.",
        "Previously, the package is runnable.",
        "Originally, Stage 1 is now authorized.",
        "Formerly, a real model was invoked.",
        "Before PR #109, owner approval exists.",
        "The original preparation package says the package is runnable.",
    )

    def test_historical_framing_cannot_excuse_a_false_present_claim(self):
        for text in self.HISTORICAL_BYPASS_ATTEMPTS:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    MODAL_BYPASS_ATTEMPTS = (
        "Reviewers must note that the package is runnable.",
        "This may surprise you: stage 1 is now authorized.",
        "Readers will observe that owner approval exists.",
    )

    def test_a_bare_modal_cannot_excuse_a_false_present_claim(self):
        for text in self.MODAL_BYPASS_ATTEMPTS:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    VERIFICATION_REQUIREMENTS = (
        "The runtime must verify that the authorization record exists.",
        "Gate A must confirm that owner approval exists.",
        "The consumer will check that the run-control directory exists.",
        "Gate A is required to validate that authorization-record.sha256 exists.",
    )

    def test_verification_requirement_frames_remain_legal(self):
        """A condition to be CHECKED is not a claim that it currently holds."""
        for text in self.VERIFICATION_REQUIREMENTS:
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    def test_historical_framing_still_excuses_denials(self):
        """The legitimate direction is untouched."""
        self.assertAccepted("Before PR #109, no consumer exists in the tree.\n")
        self.assertAccepted("Historically, Gate A is not runtime-enforced.\n")


class FramingIsClauseScoped(GuardBase):
    """Independent-review regressions (PR #112 round 2).

    Round 1 narrowed WHICH frames excuse an affirmation but left the SCOPE bug
    underneath: the frame was searched across everything earlier in the joined
    paragraph, so one "must verify" suppressed every later clause -- and since
    the governed documents are overwhelmingly bullet lists without terminal
    punctuation, "earlier" spanned whole sections.

    Framing is now scoped to the clause containing the match, and structural
    lines (list items, table rows, headings, blockquotes) start their own unit.
    """

    SCOPE_EVASIONS = (
        "Gate A must verify the record, and owner approval exists.",
        "The runtime must verify the following: owner approval exists.",
        "- The runtime must verify the record\n- Owner approval exists",
        "| The runtime must confirm approval | owner approval exists |",
        "## The runtime must validate preconditions\nOwner approval exists.",
        "Reviewers must ensure the digest matches, the checklist is current, "
        "the run log is pinned, and owner approval exists.",
        "> The runtime must confirm the record, so owner approval exists.",
        "The runtime must verify the record.Owner approval exists.",
        "Owner​ approval exists.",
        "Historically, the digest is pinned, and owner approval exists.",
    )

    def test_a_frame_in_one_clause_does_not_exempt_another(self):
        for text in self.SCOPE_EVASIONS:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    def test_a_realistic_checklist_is_fully_scanned(self):
        """One framed bullet must not suppress the bullets beneath it."""
        checklist = (
            "Preconditions the operator must confirm before Stage 1\n\n"
            "- The runtime must verify the Gate D checklist digest\n"
            "- Owner approval exists\n"
            "- The package is runnable\n"
            "- Stage 1 is authorized\n"
            "- A real model was invoked\n"
        )
        self.assertEqual(len(self.scan(checklist)), 4)


class ConditionalsAreNotAssertions(GuardBase):
    """Independent-review regressions (PR #112 round 2): false positives.

    A condition being TESTED is not a claim that it currently holds. Without
    this, the guard rejected a true description of the merged consumer's own
    behavior -- the exact class of sentence this PR exists to unblock.
    """

    CONDITIONALS = (
        "The consumer checks whether owner approval exists.",
        "Once owner approval exists, the runtime authorizes Stage 1.",
        "If owner approval exists, Gate A permits the run.",
        "When owner approval exists, the operator may proceed.",
        "Gate A blocks execution unless owner approval exists.",
        "Stage 1 stays blocked until owner approval exists.",
        "After owner approval exists, the digest is recomputed.",
        "Gate A verifies whether the authorization record exists.",
    )

    def test_conditional_clauses_are_accepted(self):
        for text in self.CONDITIONALS:
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    def test_a_conditional_word_elsewhere_does_not_exempt(self):
        """Adjacency still governs: the subordinator must precede the claim."""
        self.assertRejected(
            "Owner approval exists, if you were wondering about it.\n"
        )


class NegatorLookbackIsClauseScoped(GuardBase):
    """Independent-review regressions (PR #112 round 3).

    Round 2 scoped FRAMING to the clause but left the negator lookback
    searching the whole prefix, and its character class swallowed the em-dash
    that `_CLAUSE_SPLIT_RE` treats as a boundary. A negator in an earlier clause
    therefore suppressed a later false claim, using the guard's own declared
    boundary to do it. A whole synthetic document of false claims scored zero.
    """

    CROSS_CLAUSE_NEGATOR_EVASIONS = (
        "Gate A is not yet closed -- owner approval exists.",
        "The digest is not stale -- Stage 1 is authorized.",
        "The plan is not final -- Evidence 0016 exists.",
        "Approval was never blocked - owner approval exists.",
        "The record is not yet complete but owner approval exists.",
    )

    def test_a_negator_in_another_clause_does_not_suppress(self):
        for text in self.CROSS_CLAUSE_NEGATOR_EVASIONS:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    def test_a_document_of_dash_separated_false_claims_is_caught(self):
        doc = (
            "- Gate A is not yet closed -- owner approval exists.\n"
            "- The digest is not stale -- Stage 1 is authorized.\n"
            "| Approval | not blocked - owner approval exists |\n"
        )
        self.assertEqual(len(self.scan(doc)), 3)

    def test_adjacent_negators_still_govern(self):
        """The legitimate direction is untouched, hyphenated words included."""
        for text in (
            "No owner approval exists.",
            "No third-party owner approval exists.",
            "No owner-approval artifact exists.",
            "No Stage 1 run is authorized by this revision.",
        ):
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    SUBORDINATOR_ABUSE = (
        "After all owner approval exists.",
        "When reviewing the package owner approval exists.",
    )

    def test_idioms_and_participles_cannot_pose_as_conditionals(self):
        for text in self.SUBORDINATOR_ABUSE:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    DENY_CONDITIONALS = (
        "If no Gate A consumer exists, the runtime refuses to run.",
        "The runtime raises an error when no Gate A consumer exists.",
    )

    def test_conditionals_are_handled_in_the_deny_direction_too(self):
        """These describe the merged consumer's behavior; neither is stale."""
        for text in self.DENY_CONDITIONALS:
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    def test_a_qualifier_may_sit_between_subordinator_and_noun_phrase(self):
        self.assertAccepted("If the required owner approval exists, Gate A proceeds.\n")


class Round4Regressions(GuardBase):
    """Independent-review regressions (PR #112 round 4)."""

    NESTED_MACHINE_BLOCKS = (
        "```yaml\ncontract:\n  owner_approval_artifact_exists: true\n```",
        "```yaml\n---\nfoo: 1\n---\nowner_approval_artifact_exists: true\n```",
        "```yaml\ndefaults: &d\n  owner_approval_artifact_exists: true\n"
        "prod:\n  <<: *d\n```",
        "```yaml\ncontract: {owner_approval_artifact_exists: true}\n```",
        "```yaml\n- owner_approval_artifact_exists: true\n```",
        '```json\n{"c": {"owner_approval_artifact_exists": true}}\n```',
    )

    def test_a_false_value_cannot_hide_by_nesting_or_anchoring(self):
        """Depth, anchors and multi-doc blocks are not a safe harbor either."""
        for text in self.NESTED_MACHINE_BLOCKS:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    WRAPPED_BULLET_EVASIONS = (
        "- The runtime must verify the Gate D checklist digest before Stage 1 runs\n"
        "  and no Gate A consumer exists today",
        "- The reviewer must confirm the run-control inputs\n"
        "  because owner approval exists",
        "The operator must validate the digest before the attempt\n"
        "  and the package is now runnable",
    )

    def test_a_frame_does_not_govern_a_wrapped_continuation_line(self):
        for text in self.WRAPPED_BULLET_EVASIONS:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    def test_a_negator_still_binds_across_a_wrap(self):
        """Line breaks bound framing, not the negator. Both must hold."""
        self.assertAccepted("No third-party\nowner approval exists yet either.\n")

    LEGITIMATE_QUALIFIERS = (
        "If this owner approval exists, proceed.",
        "If that owner approval exists, proceed.",
        "If such owner approval exists, proceed.",
        "If your owner approval exists, proceed.",
        "If countersigned owner approval exists, Stage 1 proceeds.",
        "Once written owner approval exists, Stage 1 proceeds.",
        "When explicit owner approval exists, the run may begin.",
        "Unless recorded owner approval exists, the runtime refuses.",
        "If genuine owner approval exists, proceed.",
    )

    def test_demonstratives_and_adjectives_do_not_break_conditionals(self):
        """The closed qualifier set must not reject ordinary conditionals."""
        for text in self.LEGITIMATE_QUALIFIERS:
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    def test_whenever_states_a_trigger_exactly_as_when_does(self):
        for text in (
            "TRIGGERED whenever no Gate A consumer exists.",
            "TRIGGERED when no Gate A consumer exists.",
            "The runtime refuses wherever no consumer exists.",
        ):
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    def test_the_idioms_that_motivated_the_closed_set_stay_rejected(self):
        self.assertRejected("After all owner approval exists.\n")
        self.assertRejected("When reviewing the package owner approval exists.\n")


class Round5Regressions(GuardBase):
    """Independent-review regressions (PR #112 round 5).

    Round 4 made a wrapped LINE JOIN bound framing. That stopped a frame leaking
    across a wrapped bullet, but it also meant reflowing a paragraph to 80
    columns changed the verdict -- killing every legitimate frame that happened
    to wrap. Coordinating conjunctions turned out to be the real discriminator
    for both, so the line-join rule was replaced rather than patched.
    """

    COORDINATED_CLAUSE_EVASIONS = (
        "The digest is not stale and owner approval exists.",
        "The record is not present so owner approval exists.",
        "There is no digest and owner approval exists.",
        "It is not stale therefore the package is runnable.",
        "This is without doubt and owner approval exists.",
        "- The runtime must verify the Gate D checklist digest before Stage 1 runs\n"
        "  and no Gate A consumer exists today",
        "- The reviewer must confirm the run-control inputs\n"
        "  because owner approval exists",
    )

    def test_a_conjunction_opens_a_new_clause(self):
        """A negator or frame cannot reach across `and`/`so`/`because`."""
        for text in self.COORDINATED_CLAUSE_EVASIONS:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    SOFT_WRAPPED_FRAMES = (
        "The runtime must verify that\nowner approval exists.",
        "The consumer must confirm\nowner approval exists.",
        "The consumer checks whether\nowner approval exists.",
        "- The consumer checks whether\n  owner approval exists",
        "Before PR #109,\nno such consumer exists.",
        # Round 5 also listed "Historically, the repository had gaps, and no
        # Gate A consumer exists." here. Round 6 showed that is wrong: the
        # coordinated clause asserts the absence in the PRESENT, and one prefix
        # was suppressing up to three stale claims. It is a rejection case now,
        # in HistoricalFramingDoesNotCrossAConjunction below.
        "Historically the repository had gaps,\nleaving no Gate A consumer.",
    )

    def test_reflowing_a_paragraph_does_not_change_the_verdict(self):
        """Cosmetic wrapping must never flip a legitimate sentence."""
        for text in self.SOFT_WRAPPED_FRAMES:
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    def test_one_line_and_wrapped_forms_agree(self):
        for one_line in (
            "The consumer checks whether owner approval exists.",
            "The runtime must verify that owner approval exists.",
        ):
            wrapped = one_line.replace(" owner approval", "\nowner approval")
            with self.subTest(text=one_line):
                self.assertEqual(self.scan(one_line + "\n"), [])
                self.assertEqual(self.scan(wrapped + "\n"), [])

    MACHINE_FIELDS_OUTSIDE_A_PARSED_BLOCK = (
        "owner_approval_artifact_exists: true",
        "```text\nowner_approval_artifact_exists: true\n```",
        "```console\nowner_approval_artifact_exists: true\n```",
        "```\ngate_a_runtime_enforcement_exists: false\n```",
        "```yaml\nowner_approval_artifact_exists: true\nbad: [\n```",
        'owner_approval_artifact_exists = "true"',
    )

    def test_a_state_field_is_read_as_data_wherever_it_appears(self):
        """Six of the seven fields have no prose lexicon entry; without this
        they were caught only inside a well-formed yaml fence, so an unparseable
        line or the wrong info string was a safe harbor."""
        for text in self.MACHINE_FIELDS_OUTSIDE_A_PARSED_BLOCK:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    def test_truthful_machine_field_values_stay_clean(self):
        for text in (
            "owner_approval_artifact_exists: false",
            "gate_a_runtime_enforcement_exists: true",
            "```text\npackage_runnable: false\n```",
        ):
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")


class HistoricalFramingDoesNotCrossAConjunction(GuardBase):
    """Independent-review regressions (PR #112 round 6).

    Round 5 let a historical prefix govern its whole sentence in the deny
    direction, reasoning there was no evasion risk. Round 6 disproved that: a
    stale present-tense clause coordinated after the frame escaped entirely, and
    one prefix could suppress three stale claims at once. A historical prefix
    now reaches across punctuation but not across a coordinating conjunction.
    """

    COORDINATED_STALE_CLAUSES = (
        "Previously the consumer was unwired, and Gate A is still not enforced.",
        "Historically the package was rough, but no Gate A authorization "
        "consumer exists.",
        "Previously things differed, and today no such consumer exists.",
        "Previously, no consumer exists, and Gate A is not runtime-enforced, "
        "so runtime enforcement does not exist.",
    )

    def test_a_prefix_does_not_launder_a_coordinated_present_claim(self):
        for text in self.COORDINATED_STALE_CLAUSES:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    def test_a_prefix_still_reaches_across_punctuation(self):
        for text in (
            "Before PR #109, no consumer exists in the tree.",
            "Historically, no consumer exists.",
            "Previously, the consumer is not implemented.",
        ):
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")

    def test_a_verification_requirement_governs_a_coordinated_object(self):
        """One requirement with two objects is one requirement, not two claims."""
        self.assertAccepted(
            "The runtime must verify that the authorization record exists "
            "and owner approval exists.\n"
        )

    def test_but_not_across_punctuation(self):
        """Round 2's evasion stays closed: a comma still ends the requirement."""
        self.assertRejected(
            "Gate A must verify the record, and owner approval exists.\n"
        )

    def test_a_field_value_on_the_following_line_is_still_read(self):
        self.assertRejected(
            "```text\nowner_approval_artifact_exists:\n  true\n```\n"
        )

    def test_one_wrong_field_is_reported_once(self):
        """Two scanners overlap on a YAML fence; the ratchet counts defects."""
        findings = self.scan("```yaml\nowner_approval_artifact_exists: true\n```\n")
        self.assertEqual(len(findings), 1, findings)

    def test_the_same_field_wrong_at_two_sites_is_reported_twice(self):
        """Dedupe must not hide the second site from whoever fixes the first."""
        findings = self.scan(
            "```yaml\nowner_approval_artifact_exists: true\n```\n\n"
            "Some prose.\n\n"
            "```yaml\nowner_approval_artifact_exists: true\n```\n"
        )
        self.assertEqual(len(findings), 2, findings)

    DEMONSTRATIVE_THAT_EVASIONS = (
        "The runtime must validate that digest before the attempt and "
        "the package is now runnable.",
        "Gate A must verify that record and owner approval exists.",
        "Gate A must check that box on the form or stage 1 is now authorized.",
    )

    def test_a_demonstrative_that_is_not_a_complement(self):
        """`that digest` is a determiner, not a complementizer. Round 7."""
        for text in self.DEMONSTRATIVE_THAT_EVASIONS:
            with self.subTest(text=text):
                self.assertRejected(text + "\n")

    def test_sentences_the_follow_up_rewrite_needs_all_pass(self):
        for text in (
            "The runtime must verify that the authorization record exists.",
            "Gate A must confirm that the owner approval artifact exists.",
            "The runtime must verify that the authorization record exists "
            "and owner approval exists.",
            "Stage 1 is not authorized because no owner approval exists.",
            "The package is not runnable and stage 1 is not authorized.",
            "Gate A is runtime-enforced, and owner approval does not exist.",
        ):
            with self.subTest(text=text):
                self.assertAccepted(text + "\n")


class MachineBlockEvasionRegressions(GuardBase):
    """Independent-review regressions (PR #112 round 1): container gaps."""

    def test_a_quoted_boolean_does_not_slip_past(self):
        findings = self.scan('```yaml\nowner_approval_artifact_exists: "true"\n```\n')
        self.assertTrue(findings)

    def test_a_json_block_is_validated_too(self):
        findings = self.scan('```json\n{"package_runnable": true}\n```\n')
        self.assertTrue(findings)

    def test_quoted_truthful_values_still_pass(self):
        self.assertAccepted('```yaml\nowner_approval_artifact_exists: "false"\n```\n')


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
            "run_control_directory_exists: true\n"
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
                "run_control_directory_exists": "No run-control directory exists.",
                "authorization_record_exists": "No authorization record exists.",
                "authorization_record_digest_exists": (
                    "No authorization-record digest file exists."
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
# The follow-up rewrite (this PR) drove every outstanding contradiction in the
# three governed documents to zero, together with recomputing their digests and
# the authorization record that pins them.
#
# The ratchet remains, pinned at zero: it records the EXACT number of
# outstanding contradictions per document. New stale claims cannot be added
# (the count would rise) and the guard cannot be quietly weakened (the count
# would fall), so any regression in either direction fails loudly.
# ---------------------------------------------------------------------------

DOCS_DIR = REPO_ROOT / "docs" / "experiments"

# How these numbers moved, stated plainly rather than presented as stable.
#
# 19/1/2 initially. Round-2 review tightened framing to clause scope and stopped
# joining structural lines, which surfaced three stale claims that had been
# masked -> 21/1/3. Round-4 review then showed two of those 21 were GUARD
# MISFIRES, not stale claims: the preparation package states trigger conditions
# with "TRIGGERED whenever ...", and `whenever` was missing from the conditional
# subordinator set while `when` was present. Adding it removed both -> 19/1/3.
#
# The follow-up rewrite of the documents (this PR) drove all three to 0/0/0.
# The ratchet is expected to move in both directions as the guard is corrected.
# What it must never do is drift silently, which exact equality prevents.
KNOWN_OUTSTANDING_CONTRADICTIONS = {
    "STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md": 0,
    "GATE-D-STALE-DIAGNOSIS-CHECKLIST.md": 0,
    "STAGE-1-AUTEUR-EXECUTION-PACKAGE.md": 0,
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
