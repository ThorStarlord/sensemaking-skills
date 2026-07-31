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
        # A real model invocation would leave an evidence directory behind. The
        # campaign invariant is that none has ever occurred.
        "real_model_invoked": EVIDENCE_0016_DIR.is_dir(),
    }


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
        ),
    },
    "run_control_directory_exists": {
        "label": "run-control directory",
        "affirm": (r"\brun[\s-]*control\s+director(?:y|ies)\s+exists\b",),
        "deny": (
            r"\bno\s+run[\s-]*control\s+director(?:y|ies)\s+exists\b",
            r"\brun[\s-]*control\s+director(?:y|ies)\s+does\s+not\s+exist\b",
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

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?;])\s+")

# A negator IMMEDIATELY governing the matched noun phrase turns an affirmation
# into a denial: "No authorization record exists." asserts absence, not presence.
# Adjacency, not proximity -- at most two intervening words, in keeping with the
# discipline PR #107 round 5 established when it deleted line-level exemptions.
_ADJACENT_NEGATOR_RE = re.compile(
    r"\b(?:no|neither|nor|not|never|without)\s+(?:\w+[\s-]+){0,3}$", re.IGNORECASE
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
    if bad_kind == "deny":
        if _HISTORICAL_PREFIX_RE.match(sentence):
            return True
        return _MODAL_RE.search(sentence[: match.start()]) is not None
    return _VERIFICATION_REQUIREMENT_RE.search(sentence[: match.start()]) is not None


def _iter_sentences(text):
    """Yield (sentence, lineno) over `text`.

    Consecutive non-blank lines are joined before sentence splitting, because a
    sentence wrapped across two lines is still one sentence: scanning line by
    line would sever "No third-party" from "owner approval exists", turning a
    truthful denial into a spurious finding. The reported line number is the
    line on which the sentence begins.
    """
    paragraph = []  # list of (lineno, line)
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.strip():
            paragraph.append((lineno, line))
            continue
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
                        sentence[: match.start()]
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


def _scan_machine_blocks(text, state, name):
    """Validate machine-readable YAML blocks against the derived facts."""
    findings = []
    for info, start_lineno, body in iter_fenced_blocks(text):
        if info not in ("yaml", "yml", "json"):
            continue
        try:
            data = yaml.safe_load(body)
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        for field, fact in MACHINE_FIELD_TO_FACT.items():
            if field not in data:
                continue
            declared = data[field]
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


def find_state_contradictions(text, name="<text>", state=None):
    """Return findings where `text` contradicts the derived repository state.

    Ordinary prose and fenced blocks are scanned with the SAME lexicons, and
    machine-readable YAML blocks are additionally validated field by field. A
    claim gains nothing by being placed inside a code fence.
    """
    if state is None:
        state = compute_current_state()
    findings = _scan_text_for_contradictions(text, state, name)
    findings.extend(_scan_machine_blocks(text, state, name))
    return findings
