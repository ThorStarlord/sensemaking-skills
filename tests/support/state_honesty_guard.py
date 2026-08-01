"""Status-aware prose-honesty guard for the Stage 1 auteur governed documents.

Why this module exists
----------------------

The original prose-honesty guard (PR #107, ten adversarial rounds, still living
in ``tests/test_stage1_auteur_prep_package.py``) was built on one historical
premise:

    *No Gate A authorization consumer exists, therefore ANY present-tense
    sentence combining a runtime subject with an enforcement verb is false.*

That premise is now false. PR #109 implemented and merged
``scripts/gate_a_authorization.py`` and wired it into ``scripts/skill_executor.py``
at both provider boundaries. Under the old premise the truthful sentence

    The runtime verifies the Gate D checklist digest.

is mechanically rejected, and the only way to state a true fact is to hide it
inside a ```` ```text ```` fence that the old scanner skips. That is the very
evasion mechanism PR #107 rounds 5-8 identified and closed for FALSE claims, and
it must not be re-opened for TRUE ones.

The replacement premise
-----------------------

This guard does not guess truth from grammar. It derives **authoritative state
facts** from the repository itself -- real files on disk and the machine-readable
contract block of the preparation package -- and then rejects prose that
*contradicts* those facts.

Each fact has a derived boolean value and two narrow pattern sets:

* ``affirm`` -- shapes that assert the fact is TRUE;
* ``deny``   -- shapes that assert the fact is FALSE.

Polarity is not hardcoded. It follows the derived value:

* a fact whose derived value is ``True`` is a **required-positive** fact, and any
  matching ``deny`` shape is a violation (a stale absence claim);
* a fact whose derived value is ``False`` is a **required-negative** fact, and any
  matching ``affirm`` shape is a violation (a false presence claim).

Flip the world -- revert the consumer, or create ``owner-approval.md`` -- and the
polarity of the affected fact flips automatically, because the value is read from
the repository rather than written into this file. There is no boolean literal
here that asserts what the world looks like.

Three claim categories
----------------------

1. **Current implementation facts** ("The Gate A consumer exists.", "The consumer
   validates the authorization record.") -- legal, because the derived facts say
   so. Nothing in this module rejects an affirmative present-tense enforcement
   sentence merely for being affirmative and present tense.

2. **Current authorization / campaign state** ("Stage 1 is not authorized.",
   "owner-approval.md does not exist.") -- must stay negative, and the affirming
   shapes are mechanically rejected.

3. **Historical or prospective statements** -- legal only when EXPLICITLY marked,
   never inferred from grammar, and only in the direction where they can be
   true. Framing is ASYMMETRIC:

   * a statement DENYING a now-true fact has a real historical reading
     ("Before PR #109, no consumer existed"), so a sentence-initial marker from
     a closed set, or a modal before the claim, exempts it;
   * a statement AFFIRMING a still-false fact has none. Owner approval does not
     exist now and did not exist earlier either, so "Historically, owner
     approval exists." is false in both tenses. Historical framing exempts
     NOTHING here, and a bare modal does not either -- only a
     verification-requirement frame ("The runtime must verify that the
     authorization record exists"), which names a condition to be checked
     rather than a fact that holds.

   Letting a sentence-initial marker exempt the rest of a sentence
   unconditionally would re-create, at sentence scope, the blanket exemption
   PR #107 round 5 deleted at line scope. Proximity to the word "future" grants
   nothing, in keeping with that same adjacency discipline.

Code fences are not a safe harbor
---------------------------------

Every line of the document is scanned with the same lexicons, inside fences and
outside them alike. In addition, machine-readable YAML blocks are parsed and
their state keys are compared directly against the derived facts, so a false
``owner_approval_artifact_exists: true`` is caught as a value, not as prose. A
sentence never becomes acceptable by being moved into a fence.
"""

import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_PATH = (
    REPO_ROOT / "docs" / "experiments" / "STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md"
)
CONSUMER_PATH = REPO_ROOT / "scripts" / "gate_a_authorization.py"
PROVIDER_BOUNDARY_PATH = REPO_ROOT / "scripts" / "skill_executor.py"
BOUNDARY_PROOF_PATH = REPO_ROOT / "tests" / "test_gate_a_invocation_boundary.py"
EVIDENCE_0016_DIR = (
    REPO_ROOT
    / "experiments"
    / "evidence"
    / "0016-stage1-auteur-post-remediation-controlled-attempt"
)


def load_contract(text=None):
    """Return the first ```yaml contract block of the preparation package."""
    if text is None:
        text = PACKAGE_PATH.read_text(encoding="utf-8")
    blocks = re.findall(r"```yaml\n(.*?)```", text, re.DOTALL)
    if not blocks:
        raise AssertionError("no ```yaml contract block found in the preparation package")
    return yaml.safe_load(blocks[0])


def _contract_path(contract, field):
    value = contract.get(field)
    if not value:
        return None
    return REPO_ROOT / str(value)


def compute_current_state(contract=None):
    """Derive the authoritative state facts from the repository.

    Every value here is read from a real file on disk or from the contract block,
    and the two are cross-checked where they overlap. Nothing is asserted by
    literal.
    """
    if contract is None:
        contract = load_contract()

    consumer_exists = CONSUMER_PATH.is_file()
    wired = (
        PROVIDER_BOUNDARY_PATH.is_file()
        and "gate_a_authorization"
        in PROVIDER_BOUNDARY_PATH.read_text(encoding="utf-8", errors="replace")
        and bool(contract.get("gate_a_authorization_consumer_wired_to_stage1"))
    )
    record = _contract_path(contract, "execution_authorization_record_path")
    digest = _contract_path(contract, "execution_authorization_record_digest_path")
    approval = _contract_path(contract, "owner_approval_artifact_path")
    run_control = _contract_path(contract, "run_control_directory")

    return {
        "gate_a_consumer_exists": consumer_exists,
        "gate_a_consumer_wired": bool(wired),
        "runtime_enforcement_exists": bool(
            consumer_exists
            and wired
            and BOUNDARY_PROOF_PATH.is_file()
            and contract.get("gate_a_runtime_enforcement_exists")
        ),
        "run_control_directory_exists": bool(run_control and run_control.is_dir()),
        "authorization_record_exists": bool(record and record.is_file()),
        "authorization_record_digest_exists": bool(digest and digest.is_file()),
        "owner_approval_exists": bool(approval and approval.is_file()),
        "stage1_authorized": contract.get("execution_authorization_status")
        == "AUTHORIZED",
        "package_runnable": bool(contract.get("package_runnable")),
        "evidence_0016_exists": EVIDENCE_0016_DIR.is_dir(),
        # Distinct from the directory merely existing: an actual invocation
        # leaves a ledger or raw provider output behind. An empty or
        # accidentally-created evidence directory must not make the guard assert
        # that a real model ran.
        "real_model_invoked": _real_invocation_traces_exist(),
    }


def _real_invocation_traces_exist():
    """Whether Evidence 0016 contains traces of an actual model invocation."""
    if not EVIDENCE_0016_DIR.is_dir():
        return False
    for name in ("run-ledger.jsonl", "tool-call-trace.jsonl", "raw"):
        if (EVIDENCE_0016_DIR / name).exists():
            return True
    return False


# ---------------------------------------------------------------------------
# Fact lexicons.
#
# Deliberately narrow and enumerated. These are shapes this repository's prose
# actually uses to assert or deny each fact -- including every stale variant
# surfaced by the PR #111 review history. This is a deterministic lexical guard
# over a closed fact set, not an English semantic analyzer, and it does not
# claim to be one.
# ---------------------------------------------------------------------------

_CONSUMER = r"(?:gate[\s-]*a\s+)?(?:authorization\s+)?consumer"
_ANY_RUNTIME = r"(?:gate\s+a|the\s+runtime|the\s+runner|the\s+provider\s+boundary)"

FACT_LEXICONS = {
    "gate_a_consumer_exists": {
        "label": "Gate A authorization consumer",
        "affirm": (
            rf"\b{_CONSUMER}\s+(?:now\s+)?exists\b",
            rf"\b{_CONSUMER}\s+(?:is|has\s+been)\s+(?:implemented|merged)\b",
            r"\bconsumer\s*:\s*implemented\b",
        ),
        "deny": (
            rf"\bno\s+(?:\w+\s+){{0,3}}{_CONSUMER}\s+exists\b",
            r"\bno\s+such\s+consumer\s+exists\b",
            rf"\b{_CONSUMER}\s+(?:does\s+not|doesn't|do\s+not)\s+exist\b",
            rf"\b(?:has|have)\s+no\s+(?:runtime\s+|authorization\s+)?consumer\b",
            rf"\b{_CONSUMER}\s*:\s*(?:not\s+implemented|absent|missing|none)\b",
            rf"\b{_CONSUMER}\s+is\s+not\s+implemented\b",
            r"\bnone\s+of\s+them\s+are\s+implemented\b",
            r"\bnone\s+of\s+the\s+criteria\s+below\s+are\s+satisfied\s+today\b",
            r"\bno\b[^.\n]{0,60}?\b(?:authorization\s+)?consumer\s+is\s+"
            r"implemented\b",
            r"\bconsumer\b[^.\n]{0,80}?\bmandatory\s+future\s+work\b",
            r"\b(?:the\s+)?future\s+gate\s+a\s+(?:authorization\s+)?consumer\b",
            r"\bnone\s+of\s+these\b[^.\n]{0,40}?\bsatisfied\b",
            r"\bspecification\s+of\s+work\s+not\s+done\b",
        ),
    },
    "gate_a_consumer_wired": {
        "label": "Gate A consumer wiring",
        "affirm": (
            rf"\b{_CONSUMER}\s+is\s+wired\b",
            r"\bwired\s+into\s+the\s+provider\s+boundar(?:y|ies)\b",
        ),
        "deny": (
            rf"\b{_CONSUMER}\s+is\s+(?:not\s+wired|unwired)\b",
            r"\bnot\s+wired\s+(?:in)?to\s+stage\s*1\b",
            r"\bwiring\s*:\s*(?:absent|missing|none|not\s+done)\b",
        ),
    },
    "runtime_enforcement_exists": {
        "label": "Gate A runtime enforcement",
        "affirm": (
            r"\bgate\s+a\s+is\s+runtime[\s-]*enforced\b",
            r"\bruntime\s+enforcement\s+exists\b",
            r"\bruntime\s+enforcement\s*:\s*(?:present|exists|implemented)\b",
        ),
        "deny": (
            r"\bgate\s+a\s+is\s+not\s+runtime[\s-]*enforced\b",
            r"\bruntime\s+enforcement\s*:\s*(?:absent|missing|none|not\s+implemented)\b",
            r"\bno\s+runtime\s+enforcement\s+exists\b",
            r"\bruntime\s+enforcement\s+(?:does\s+not|doesn't)\s+exist\b",
            rf"\bgate\s+a\b[^.\n]{{0,40}}:\s*not\s+enforced\b",
            r"\bgate\s+a\s+is\s+(?:still\s+)?not\s+enforced\b",
            r"\bruntime\s+enforcement\b[^.;\n]{0,60}?\b(?:does\s+not|doesn't)"
            r"\s+exist\b",
            r"\bnothing\s+(?:loads|validates|recomputes|checks|blocks)\s+"
            r"(?:(?:the|any|these|a)\s+)?(?:authorization[\s-]*record|digests?|"
            r"owner[\s-]*approval|model\s+invocation)\b",
        ),
    },
    "run_control_directory_exists": {
        "label": "run-control directory",
        "affirm": (r"\brun[\s-]*control\s+director(?:y|ies)\s+exists\b",),
        "deny": (
            r"\bno\s+run[\s-]*control\s+director(?:y|ies)\s+exists\b",
            r"\brun[\s-]*control\s+director(?:y|ies)\s+does\s+not\s+exist\b",
            r"\bnone\s+of\s+these\s+exist\b",
        ),
    },
    "authorization_record_exists": {
        "label": "authorization record",
        "affirm": (
            r"\b(?:the\s+)?authorization[\s-]*record\s+exists\b",
            r"\bauthorization-record\.yaml\s+exists\b",
        ),
        "deny": (
            r"\bno\s+authorization[\s-]*record\s+exists\b",
            r"\b(?:the\s+)?authorization[\s-]*record\s+does\s+not\s+exist\b",
            r"\bauthorization-record\.yaml\s+does\s+not\s+exist\b",
            r"\bno\s+such\s+(?:authorization[\s-]*)?record\b[^.\n]{0,30}?"
            r"\bexists\b",
        ),
    },
    "authorization_record_digest_exists": {
        "label": "authorization-record digest",
        "affirm": (
            r"\b(?:an?\s+)?authorization[\s-]*record\s+digest\s+(?:file\s+)?exists\b",
            r"\bauthorization-record\.sha256\s+exists\b",
        ),
        "deny": (
            r"\bno\s+authorization[\s-]*record\s+digest\s+(?:file\s+)?exists\b",
            r"\bauthorization-record\.sha256\s+does\s+not\s+exist\b",
        ),
    },
    "owner_approval_exists": {
        "label": "owner approval",
        "affirm": (
            r"\bowner[\s-]*approval(?:\s+artifact)?\s+exists\b",
            r"\bowner-approval\.md\s+exists\b",
            r"\bowner[\s-]*approval\s+(?:has\s+been|was)\s+(?:created|signed|granted|obtained)\b",
            r"\bowner[\s-]*approval\s+is\s+in\s+place\b",
        ),
        "deny": (
            r"\bno\s+owner[\s-]*approval(?:\s+artifact)?\s+exists\b",
            r"\bowner[\s-]*approval(?:\s+artifact)?\s+does\s+not\s+exist\b",
            r"\bowner-approval\.md\s+does\s+not\s+exist\b",
            r"\bno\s+such\s+approval\b[^.\n]{0,30}?\bexists\b",
        ),
    },
    "stage1_authorized": {
        "label": "Stage 1 authorization",
        "affirm": (
            r"\bstage\s*1\s+is\s+(?:now\s+)?authorized\b",
            r"\b(?:the\s+)?run\s+is\s+authorized\b",
            r"\bexecution_authorization_status\s*:\s*AUTHORIZED\b",
            r"\bauthorization\s+status\s*:\s*authorized\b",
        ),
        "deny": (
            r"\bstage\s*1\s+is\s+not\s+authorized\b",
            r"\bexecution_authorization_status\s*:\s*NOT_AUTHORIZED\b",
        ),
    },
    "package_runnable": {
        "label": "package runnability",
        "affirm": (
            r"\b(?:the\s+)?package\s+is\s+(?:now\s+)?runnable\b",
            r"\bpackage_runnable\s*:\s*true\b",
        ),
        "deny": (
            r"\b(?:the\s+)?package\s+is\s+not\s+runnable\b",
            r"\bpackage_runnable\s*:\s*false\b",
        ),
    },
    "evidence_0016_exists": {
        "label": "Evidence 0016",
        "affirm": (
            r"\bevidence\s+0016\s+(?:exists|has\s+been\s+created|has\s+run|has\s+executed|ran)\b",
            r"\b0016\s+(?:has\s+run|has\s+executed)\b",
        ),
        "deny": (
            r"\bevidence\s+0016\s+(?:does\s+not\s+exist|has\s+not\s+been\s+created|has\s+not\s+run)\b",
            r"\bno\s+evidence\s+0016\b",
        ),
    },
    "real_model_invoked": {
        "label": "real model invocation",
        "affirm": (
            r"\breal\s+model\s+(?:has\s+been|was|is)\s+invoked\b",
            r"\breal\s+model\s+invocation\s+(?:occurred|happened|took\s+place)\b",
        ),
        "deny": (
            r"\bno\s+real\s+model\s+(?:has\s+been|was)\s+invoked\b",
            r"\breal\s+model\s+invocation\s+(?:has\s+not\s+occurred|never\s+occurred)\b",
        ),
    },
}

# Contract/YAML keys that state a fact as a machine-readable value. Fenced YAML
# blocks are parsed and these keys are compared against the derived facts, so a
# false value inside a fence is caught as data, not only as prose.
MACHINE_FIELD_TO_FACT = {
    "gate_a_authorization_consumer_wired_to_stage1": "gate_a_consumer_wired",
    "gate_a_runtime_enforcement_exists": "runtime_enforcement_exists",
    "run_control_directory_exists": "run_control_directory_exists",
    "execution_authorization_record_exists": "authorization_record_exists",
    "execution_authorization_record_digest_exists": (
        "authorization_record_digest_exists"
    ),
    "owner_approval_artifact_exists": "owner_approval_exists",
    "package_runnable": "package_runnable",
}

# ---------------------------------------------------------------------------
# Framing. Historical and prospective statements are legal, but only when the
# framing is EXPLICIT. It is never inferred from tense or from a nearby word.
# ---------------------------------------------------------------------------

# Sentence-INITIAL historical markers only. Adjacency, not proximity: a stale
# claim cannot be rescued by the word "historically" appearing later in the line.
_HISTORICAL_PREFIX_RE = re.compile(
    r"^\W*(?:"
    r"before\s+pr\s*#?\d+|"
    r"before\s+the\s+gate\s+a\s+consumer|"
    r"before\s+the\s+consumer\s+(?:was\s+)?(?:merged|existed|landed)|"
    r"prior\s+to\s+pr\s*#?\d+|"
    r"until\s+pr\s*#?\d+|"
    r"historically|"
    r"previously|"
    r"formerly|"
    r"originally|"
    r"at\s+the\s+time\s+of\s+pr\s*#?\d+|"
    r"the\s+original\s+preparation\s+package|"
    r"pr\s*#107\s+(?:originally\s+)?(?:said|stated|claimed|assumed)"
    r")\b",
    re.IGNORECASE,
)

# Prospective framing requires a modal governing the claim.
_MODAL_RE = re.compile(
    r"\b(?:will|would|shall|may|might|could|must|is\s+expected\s+to|"
    r"is\s+required\s+to|are\s+required\s+to)\b",
    re.IGNORECASE,
)

# A VERIFICATION-REQUIREMENT frame: a modal followed by a checking verb, as in
# "The runtime must verify that the authorization record exists." Such a
# sentence names a condition to be CHECKED, not a fact that currently holds, so
# it may legitimately contain a present-tense affirmation of a currently-false
# fact. "Reviewers must note that the package is runnable." is not of this kind
# and is not exempted: "note" is not a verification verb.
_VERIFICATION_REQUIREMENT_RE = re.compile(
    r"\b(?:will|would|shall|may|might|could|must|is\s+required\s+to|"
    r"are\s+required\s+to|is\s+expected\s+to)\s+(?:\w+\s+){0,2}"
    r"(?:verify|verifies|check|checks|confirm|confirms|validate|validates|"
    r"ensure|ensures|require|requires|assert|asserts|recompute|recomputes|"
    r"establish|establishes)\b",
    re.IGNORECASE,
)

# A sentence ends at terminal punctuation followed by whitespace, OR by a
# capital with no space at all ("...the record.Owner approval exists.").
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?;])\s+|(?<=[.!?])(?=[A-Z])")

# Clause boundaries. Framing is scoped to the clause CONTAINING the match, never
# to everything earlier in the sentence: otherwise one "must verify" anywhere
# ahead would exempt every later clause, which is the sentence-scope version of
# the blanket line-level exemption PR #107 round 5 deleted.
# A COORDINATING CONJUNCTION opens a new clause just as punctuation does. This
# is the true discriminator, and it replaces the line-join rule tried in round 4:
# "The digest is not stale and owner approval exists." coordinates a second
# clause on one line with no punctuation at all, while "The runtime must verify
# that / owner approval exists." is one clause merely soft-wrapped across two.
# Bounding on the line join caught the first only by also breaking the second.
#
# Punctuation and conjunction boundaries are kept SEPARATE, because the reasons
# treat them differently: a historical prefix may reach across a comma but not
# across "but", and a verification requirement may govern a coordinated object
# ("...that the record exists and owner approval exists") but not a clause
# introduced after a comma.
_PUNCTUATION_CLAUSE_RE = re.compile(r"[,;:|]|\s--\s|—")
_CONJUNCTION_CLAUSE_RE = re.compile(
    r"\b(?:and|but|so|or|yet|because|therefore|however|whereas|while|"
    r"although|though)\b"
)
_CLAUSE_SPLIT_RE = re.compile(
    _PUNCTUATION_CLAUSE_RE.pattern + r"|" + _CONJUNCTION_CLAUSE_RE.pattern
)

# Lines that begin a NEW structural unit and must not be joined into the
# preceding paragraph: list items, table rows, headings and blockquote markers.
# Joining them let a frame in one bullet exempt claims in every later bullet.
_BLOCK_START_RE = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s|#{1,6}\s|\||>)")

# A heading is a unit BY ITSELF: the line after it starts new prose, so joining
# them would let a frame in the heading exempt the paragraph beneath it.
_HEADING_RE = re.compile(r"^\s*#{1,6}\s")

# Zero-width and formatting characters, stripped so an invisible character
# cannot break a lexicon match.
_ZERO_WIDTH_RE = re.compile(r"[​-‏  ﻿­]")

# Subordinators that make a following affirmation a CONDITION rather than a
# claim: "The consumer checks whether owner approval exists." describes what is
# tested, not what is true. Must sit adjacent to the matched noun phrase, at the
# start of the clause or immediately before it.
# Only a determiner or qualifier from a CLOSED set may sit between the
# subordinator and the fact's noun phrase. Arbitrary words would let idioms and
# participles pose as conditionals: "After all owner approval exists." and
# "When reviewing the package owner approval exists." are assertions, not
# conditions, and neither "all" nor "reviewing the package" is a qualifier.
_QUALIFIER = (
    r"(?:the|a|an|any|its|this|that|such|your|our|their|valid|required|"
    r"signed|approved|current|written|explicit|recorded|countersigned|"
    r"genuine|documented)"
)

_CONDITIONAL_RE = re.compile(
    r"\b(?:whether|if|once|whenever|wherever|when|unless|until|after|before|"
    r"provided\s+that|in\s+case|as\s+soon\s+as|only\s+if|each\s+time|"
    r"any\s+time)\s+(?:" + _QUALIFIER + r"\s+){0,2}$",
    re.IGNORECASE,
)

# A negator IMMEDIATELY governing the matched noun phrase turns an affirmation
# into a denial: "No authorization record exists." asserts absence, not presence.
# Adjacency, not proximity -- at most two intervening words, in keeping with the
# discipline PR #107 round 5 established when it deleted line-level exemptions.
#
# Each intervening token must START with a word character. A bare "--" is not a
# word: without that requirement the class `[\s-]+` swallowed the em-dash that
# _CLAUSE_SPLIT_RE treats as a clause boundary, so "The digest is not stale --
# Stage 1 is authorized." suppressed its own false claim using the guard's own
# declared boundary. Hyphens INSIDE a token stay legal ("No third-party owner
# approval exists.").
_ADJACENT_NEGATOR_RE = re.compile(
    r"\b(?:no|neither|nor|not|never|without)\s+(?:\w[\w-]*\s+){0,2}$", re.IGNORECASE
)


def _is_framed(sentence, match, bad_kind):
    """Whether explicit historical or prospective framing governs `match`.

    The rule is deliberately ASYMMETRIC, because the two directions are not
    symmetric in reality.

    A `deny` match denies a fact that is currently TRUE. Such a statement has a
    legitimate historical reading ("Before PR #109, no consumer existed") and a
    legitimate prospective reading, so historical and modal framing both exempt.

    An `affirm` match affirms a fact that is currently FALSE. There is NO
    legitimate historical reading of one: owner approval does not exist now and
    did not exist earlier either, so "Historically, owner approval exists."
    states a falsehood in both tenses. Allowing a sentence-initial marker to
    exempt it would re-create, at sentence scope, exactly the blanket exemption
    PR #107 round 5 deleted at line scope. Historical framing therefore exempts
    NOTHING in this direction, and a bare modal is not enough either -- only a
    verification-requirement frame, which names a condition to be checked rather
    than a fact that holds.
    """
    boundaries, clause = _clause_before(sentence, match)

    # A conditional subordinator adjacent to the noun phrase makes this a
    # condition being TESTED, not a claim about what currently holds. That is
    # true in BOTH directions: "If no Gate A consumer exists, the runtime
    # refuses to run." describes the merged consumer's own behavior and is not
    # a stale absence claim.
    if _CONDITIONAL_RE.search(clause):
        return True

    before = sentence[: match.start()]
    coordinated = _CONJUNCTION_CLAUSE_RE.search(before) is not None

    if bad_kind == "deny":
        # A historical prefix governs the clauses it introduces, including ones
        # merely separated by punctuation ("Before PR #109, no consumer
        # exists."). It does NOT reach across a coordinating conjunction:
        # "Historically the package was rough, but no consumer exists." asserts
        # the second clause in the present, and round 6 showed one prefix
        # otherwise suppressed three stale claims at once.
        if _HISTORICAL_PREFIX_RE.match(sentence) and (
            not coordinated or _REPORTED_SPEECH_RE.search(clause)
        ):
            return True
        return _MODAL_RE.search(clause) is not None

    # A verification requirement may govern a COORDINATED object of the same
    # requirement ("must verify that the record exists and owner approval
    # exists") -- that is one requirement, not two claims. It still may not
    # reach across punctuation, which is what separates it from round 2's
    # "Gate A must verify the record, and owner approval exists."
    if _VERIFICATION_REQUIREMENT_RE.search(clause):
        return True
    # ...but only for a genuine coordinated OBJECT: `and`/`or` joining two
    # predicates inside the same `that`-complement. "must confirm the inputs
    # because owner approval exists" and "must validate the digest before the
    # attempt and the package is now runnable" join a requirement to an
    # INDEPENDENT claim, and stay rejected (round 4).
    if (
        coordinated
        and not _PUNCTUATION_CLAUSE_RE.search(before)
        and _COORDINATED_OBJECT_RE.search(before)
    ):
        return _VERIFICATION_REQUIREMENT_RE.search(before) is not None
    return False


# A `that`-COMPLEMENT joined by `and`/`or` is one requirement with two objects.
#
# `that` must be the complementizer, not a demonstrative determiner: it has to
# follow the checking verb directly and introduce a clause, which in this
# vocabulary means a determiner comes next. Without that constraint "must
# validate that digest before the attempt and the package is now runnable"
# reads as a coordinated object and smuggles an independent false claim, while
# claiming to admit only genuine complements.
_COORDINATED_OBJECT_RE = re.compile(
    r"\b(?:verify|verifies|check|checks|confirm|confirms|validate|validates|"
    r"ensure|ensures|require|requires|assert|asserts|recompute|recomputes|"
    r"establish|establishes)\s+that\s+"
    r"(?:the|a|an|its|their|no|every|each|owner|exactly)\b"
    r".*\b(?:and|or)\b\s*$",
    re.IGNORECASE,
)

# Reported speech: attributing a statement to a source is not asserting it now.
# Deny direction only -- quoting a superseded claim is legitimate, affirming a
# still-false fact through a mouthpiece is not.
_REPORTED_SPEECH_RE = re.compile(
    r"\b(?:stated|said|claimed|specified|asserted|noted|recorded)\s+that\b",
    re.IGNORECASE,
)


def _clause_before(sentence, match):
    """Return (clause boundaries, the clause text preceding `match`).

    Everything that reasons about what governs a match uses this, so the
    negator lookback is scoped exactly like framing is. Scoping one but not the
    other is what let a negator in an earlier clause suppress a later false
    claim.

    A soft wrap is deliberately NOT a boundary. Round 4 made line joins bound
    framing, which did stop a frame leaking across a wrapped bullet -- but it
    also meant reflowing a paragraph to 80 columns changed the verdict, killing
    every legitimate frame that happened to wrap ("The consumer checks whether /
    owner approval exists."). Coordinating conjunctions are the real
    discriminator and are handled in `_CLAUSE_SPLIT_RE` instead.
    """
    before = sentence[: match.start()]
    cuts = [m.end() for m in _CLAUSE_SPLIT_RE.finditer(before)]
    clause = before[max(cuts):] if cuts else before
    return cuts, clause


def _iter_sentences(text):
    """Yield (sentence, lineno) over `text`.

    Consecutive non-blank lines are joined before sentence splitting, because a
    sentence wrapped across two lines is still one sentence: scanning line by
    line would sever "No third-party" from "owner approval exists", turning a
    truthful denial into a spurious finding. The reported line number is the
    line on which the sentence begins.

    Structural lines -- list items, table rows, headings, blockquote markers --
    START A NEW UNIT rather than joining the previous one. Joining them would let
    a "must verify" frame in one bullet exempt claims in every later bullet, and
    the governed documents are overwhelmingly bullet lists without terminal
    punctuation, so that would be a hole the width of the document.
    """
    text = _ZERO_WIDTH_RE.sub("", text)
    paragraph = []  # list of (lineno, line)
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            yield from _split_paragraph(paragraph)
            paragraph = []
            continue
        if _BLOCK_START_RE.match(line):
            yield from _split_paragraph(paragraph)
            paragraph = []
        paragraph.append((lineno, line))
        if _HEADING_RE.match(line):
            yield from _split_paragraph(paragraph)
            paragraph = []
    yield from _split_paragraph(paragraph)


def _split_paragraph(paragraph):
    if not paragraph:
        return
    joined = ""
    offsets = []  # (start_offset, lineno)
    for lineno, line in paragraph:
        offsets.append((len(joined), lineno))
        joined += line.strip() + " "

    def lineno_at(pos):
        result = offsets[0][1]
        for start, lineno in offsets:
            if start <= pos:
                result = lineno
            else:
                break
        return result

    pos = 0
    for part in _SENTENCE_SPLIT_RE.split(joined):
        start = joined.index(part, pos) if part else pos
        pos = start + len(part)
        stripped = part.strip()
        if stripped:
            yield stripped, lineno_at(start)


def _scan_text_for_contradictions(text, state, name):
    findings = []
    seen = set()
    for sentence, lineno in _iter_sentences(text):
        for fact, lexicon in FACT_LEXICONS.items():
            value = state[fact]
            # Derived polarity: a true fact may not be denied, a false fact may
            # not be affirmed.
            bad_kind = "deny" if value else "affirm"
            for pattern in lexicon[bad_kind]:
                for match in re.finditer(pattern, sentence, re.IGNORECASE):
                    if _is_framed(sentence, match, bad_kind):
                        continue
                    if bad_kind == "affirm" and _ADJACENT_NEGATOR_RE.search(
                        _clause_before(sentence, match)[1]
                    ):
                        # "No authorization record exists." denies the fact and
                        # is therefore truthful while the fact is false.
                        continue
                    if bad_kind == "deny":
                        problem = (
                            f"stale absence claim about {lexicon['label']}, which "
                            f"genuinely exists"
                        )
                    else:
                        problem = (
                            f"false presence claim about {lexicon['label']}, which "
                            f"genuinely does not exist"
                        )
                    excerpt = sentence if len(sentence) <= 160 else (
                        sentence[:157] + "..."
                    )
                    finding = (
                        f"{name}:{lineno}: {problem}: {match.group(0)!r} "
                        f"in {excerpt!r}"
                    )
                    if finding not in seen:
                        seen.add(finding)
                        findings.append(finding)
    return findings


_FENCE_RE = re.compile(r"^\s*(?:```|~~~)\s*(?P<info>[\w-]*)")


def iter_fenced_blocks(text):
    """Yield (info_string, start_lineno, body) for every fenced block."""
    lines = text.splitlines()
    idx = 0
    while idx < len(lines):
        opened = _FENCE_RE.match(lines[idx])
        if opened is None:
            idx += 1
            continue
        info = opened.group("info").lower()
        start = idx + 1
        body = []
        idx += 1
        while idx < len(lines) and not _FENCE_RE.match(lines[idx]):
            body.append(lines[idx])
            idx += 1
        idx += 1
        yield info, start + 1, "\n".join(body)


def _walk_state_fields(node):
    """Yield (field, value) for every state field ANYWHERE in a parsed block.

    A false value does not become acceptable by being nested one level deeper,
    hidden behind a YAML anchor, or placed in the second document of a block --
    the same reason a sentence does not become acceptable inside a fence.
    """
    found = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key in MACHINE_FIELD_TO_FACT:
                found.append((key, value))
            found.extend(_walk_state_fields(value))
    elif isinstance(node, (list, tuple)):
        for item in node:
            found.extend(_walk_state_fields(item))
    return found


def _scan_machine_blocks(text, state, name):
    """Validate machine-readable YAML blocks against the derived facts."""
    findings = []
    for info, start_lineno, body in iter_fenced_blocks(text):
        if info not in ("yaml", "yml", "json"):
            continue
        try:
            documents = list(yaml.safe_load_all(body))
        except yaml.YAMLError:
            continue
        pairs = []
        for document in documents:
            pairs.extend(_walk_state_fields(document))
        for field, declared in pairs:
            fact = MACHINE_FIELD_TO_FACT[field]
            if isinstance(declared, str):
                # A quoted "true" states the same thing as a bare true and must
                # not slip past by being a string.
                lowered = declared.strip().lower()
                if lowered in ("true", "yes"):
                    declared = True
                elif lowered in ("false", "no"):
                    declared = False
            if not isinstance(declared, bool):
                continue
            if declared != state[fact]:
                findings.append(
                    f"{name}:{start_lineno}: machine-readable block declares "
                    f"{field}: {str(declared).lower()} but the repository state "
                    f"fact {fact} is {str(state[fact]).lower()}"
                )
    return findings


_MACHINE_FIELD_PROSE_RE = re.compile(
    r"\b(?P<field>" + "|".join(MACHINE_FIELD_TO_FACT) + r")\s*[:=]\s*"
    r"[\"']?(?P<value>true|false|yes|no)\b",
    re.IGNORECASE | re.DOTALL,
)


def _scan_machine_fields_as_prose(text, state, name):
    """Catch a state field written ANYWHERE, not only inside a parsed block.

    Six of the seven machine fields have no prose lexicon entry, so before this
    they were caught only by `_scan_machine_blocks` -- which keys off the fence
    info string and silently skips a block that fails to parse. A false
    `owner_approval_artifact_exists: true` therefore escaped by sitting in a
    ```text fence, in no fence at all, or in a ```yaml block containing one
    unparseable line. The declared rule is that a fence is not a safe harbor, so
    the field is now read as data wherever it appears.
    """
    findings = []
    for match in _MACHINE_FIELD_PROSE_RE.finditer(text):
        field = match.group("field")
        declared = match.group("value").lower() in ("true", "yes")
        fact = MACHINE_FIELD_TO_FACT[field]
        if declared != state[fact]:
            lineno = text.count(chr(10), 0, match.start()) + 1
            findings.append(
                f"{name}:{lineno}: declares {field}: "
                f"{str(declared).lower()} but the repository state fact "
                f"{fact} is {str(state[fact]).lower()}"
            )
    return findings


def find_state_contradictions(text, name="<text>", state=None):
    """Return findings where `text` contradicts the derived repository state.

    Ordinary prose and fenced blocks are scanned with the SAME lexicons, and
    machine-readable YAML blocks are additionally validated field by field. A
    claim gains nothing by being placed inside a code fence.
    """
    if state is None:
        state = compute_current_state()
    findings = _scan_text_for_contradictions(text, state, name)
    # The two machine scanners overlap on a well-formed YAML fence. Report each
    # offending FIELD once: the inventory ratchet counts defects, and one field
    # declared wrongly is one defect however many scanners noticed it.
    machine = {}
    for finding in _scan_machine_fields_as_prose(
        text, state, name
    ) + _scan_machine_blocks(text, state, name):
        field = next(f for f in MACHINE_FIELD_TO_FACT if f in finding)
        # Keyed by (field, line) so the two scanners agreeing about ONE site
        # collapse, while the same field declared wrongly at two different
        # sites stays visible to whoever fixes the first.
        machine.setdefault((field, finding.split(":")[1]), finding)
    findings.extend(machine.values())
    return findings
