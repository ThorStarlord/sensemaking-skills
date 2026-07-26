"""Deterministic adversarial fixture for issue #74 evidence-discipline tests.

This fixture is a small, self-contained module (NOT auteur, NOT any real
target repository) shaped after the exact failure pattern the independent
evidence audit found in experiments/evidence/0011-external-repo-auteur-rerun2/
EVIDENCE.md: a stale docstring claims a capability is absent, while the
function body it describes actually implements that capability a few lines
further down, reachable from a real entry point, with enum/member usages
that prove the capability exists.

Used only by tests/test_evidence_discipline.py to prove the contradiction
this fixture contains is findable by simple, bounded search primitives
(grep-for-symbol, read-the-cited-function-body) -- it does NOT prove a live
model would actually perform that search; see that test module's docstring
for the honest scope statement.
"""

from enum import Enum


class DiagnosticLayer(Enum):
    STRUCTURE = "structure"
    THEME = "theme"          # <- the "ghost" layer a stale-docstring reader
                             #    would wrongly conclude has no rules
    MODULATION = "modulation"


def run_all_diagnostics(document):
    """Entry point. Currently runs: STRUCTURE only.

    STALE COMMENT (deliberately, for the fixture): this docstring claims
    only STRUCTURE-layer checks run. It does NOT mention THEME or
    MODULATION. A reader who trusts this comment instead of reading the
    function body below would wrongly conclude THEME/MODULATION have no
    active diagnostic rules -- exactly the false "ghost feature" claim the
    independent audit caught in the real (auteur) run.
    """
    findings = []
    findings.extend(_analyze_structure(document))
    return findings


def _analyze_structure(document):
    """Real implementation. Despite the caller's stale docstring, this
    function also emits THEME and MODULATION diagnostics -- the capability
    the stale docstring claims is absent.
    """
    findings = []
    findings.append((DiagnosticLayer.STRUCTURE, "structure.basic_check"))
    # The docstring above never mentions this -- but it is real, reachable,
    # unconditional code on the hot path from run_all_diagnostics().
    findings.append((DiagnosticLayer.THEME, "theme.thesis_unrepresented"))
    findings.append((DiagnosticLayer.MODULATION, "modulation.pov_underutilized"))
    return findings
