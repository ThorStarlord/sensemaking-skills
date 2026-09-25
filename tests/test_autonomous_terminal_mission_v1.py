"""Regression coverage for Autonomous Terminal Mission Continuation v1."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "strategic-sensemaking-loop" / "SKILL.md"
REFERENCE = (
    ROOT
    / "skills"
    / "strategic-sensemaking-loop"
    / "references"
    / "autonomous-terminal-mission-v1.md"
)
AGENT = ROOT / "skills" / "strategic-sensemaking-loop" / "agents" / "openai.yaml"
USING = ROOT / "skills" / "using-sensemaking" / "SKILL.md"
DELEGATED = ROOT / "skills" / "using-sensemaking" / "references" / "delegated-goal-patterns.md"
GETTING_STARTED = ROOT / "GETTING_STARTED.md"
LOOP_DOC = ROOT / "docs" / "strategic-sensemaking-loop-v1.md"
README = ROOT / "README.md"


def _flat(text: str) -> str:
    """Collapse line wrapping so prose phrase assertions are wrap-insensitive."""
    return " ".join(text.split())


def test_full_autonomy_is_profile_of_existing_front_door() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    ref = REFERENCE.read_text(encoding="utf-8")

    assert "FULL AUTONOMY / FULL DELEGATION" in skill
    assert "references/autonomous-terminal-mission-v1.md" in skill
    assert "responsibility completed != mission completed" in skill
    assert "mission incomplete != execute backlog blindly" in skill

    assert "full-autonomy mission" in ref
    assert "strategic-sensemaking-loop" in ref
    assert "!=\nnew planner" in ref
    assert not (ROOT / "skills" / "autonomous-terminal-mission").exists()


def test_skill_metadata_triggers_terminal_missions_without_new_frontmatter_fields() -> None:
    text = SKILL.read_text(encoding="utf-8")
    _, raw, _ = text.split("---", 2)
    metadata = yaml.safe_load(raw)

    assert set(metadata) == {"name", "description"}
    description = str(metadata["description"])
    assert "FULL AUTONOMY" in description
    assert "FULL DELEGATION" in description
    assert "terminal" in description.lower()

    agent = yaml.safe_load(AGENT.read_text(encoding="utf-8"))
    assert "one prompt" in agent["interface"]["short_description"].lower()
    assert "full-autonomy terminal missions" in agent["interface"]["short_description"].lower()


def test_autonomous_highest_leverage_is_qualitative_remaining_difference() -> None:
    ref = REFERENCE.read_text(encoding="utf-8")
    getting_started = GETTING_STARTED.read_text(encoding="utf-8")

    assert "AUTONOMOUS_HIGHEST_LEVERAGE_BOTTLENECK" in ref
    assert "highest-value remaining difference" in ref
    assert "Do not introduce a numeric leverage score" in ref

    assert "AUTONOMOUS_HIGHEST_LEVERAGE_BOTTLENECK" in getting_started
    assert "qualitative Sensemaking judgment" in getting_started
    assert "numeric priority score" in getting_started


def test_terminal_mission_continues_across_responsibilities_without_backlog_execution() -> None:
    ref = REFERENCE.read_text(encoding="utf-8")
    loop_doc = LOOP_DOC.read_text(encoding="utf-8")

    for phrase in (
        "responsibility completed\n!= mission completed",
        "mission incomplete\n!= execute backlog blindly",
        "identify highest-value remaining difference",
        "establish next warranted responsibility",
    ):
        assert phrase in ref

    assert "continue across multiple bounded" in loop_doc
    assert "next warranted responsibility" in loop_doc
    assert "execute backlog blindly" in loop_doc


def test_breadth_is_conditional_and_does_not_force_three_paths() -> None:
    ref = REFERENCE.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")

    assert "0-5 materially real construction paths" in ref
    assert "Do not force exactly three alternatives" in ref
    assert "strategy settled\n-> resume current responsibility/execution/reconciliation" in ref

    assert "Do not force exactly three strategic alternatives" in _flat(skill)
    assert "rerun breadth after every responsibility" in _flat(skill)


def test_vertical_completion_is_decision_relevant_not_maximal_architecture() -> None:
    ref = REFERENCE.read_text(encoding="utf-8")

    assert "decision-relevant vertical" in ref
    assert "Do not manufacture layers that the capability does not need." in ref
    assert "complete vertical path\n!= maximum architecture" in ref
    assert "Evaluate completion at the capability/user/operational scale" in ref


def test_construction_before_field_validation_preserves_claim_boundary() -> None:
    ref = REFERENCE.read_text(encoding="utf-8")
    getting_started = GETTING_STARTED.read_text(encoding="utf-8")

    assert "construction before field validation" in ref.lower()
    assert "mission-scoped and defeasible" in ref
    assert "external validation deferred\n!= externally validated" in ref
    assert "safety, legal, regulatory" in ref

    assert "Construction-before-field-validation is a mission policy" in _flat(getting_started)
    assert "must preserve that prerequisite or narrow the claim" in _flat(getting_started)


def test_synthetic_personas_are_reasoning_aids_not_empirical_evidence() -> None:
    ref = REFERENCE.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")

    assert "synthetic persona\n= design reasoning aid" in ref
    assert "synthetic persona\n!= empirical user evidence" in ref
    assert "Do not claim user validation" in ref
    assert "synthetic persona != empirical user evidence" in skill


def test_canonical_promotion_requires_verification_and_reconciliation() -> None:
    ref = REFERENCE.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")

    assert "Implementation alone does not justify canonical status." in ref
    assert "-> reconciliation\n-> status/authority promotion only when supported" in ref
    assert "authority to promote\n!= evidence already supports promotion" in ref
    assert "automatic canonical/status promotion before applicable verification and reconciliation" in skill


def test_full_delegation_preserves_protected_transitions_and_allows_explicit_grants() -> None:
    ref = REFERENCE.read_text(encoding="utf-8")
    getting_started = GETTING_STARTED.read_text(encoding="utf-8")

    for phrase in (
        "merge;",
        "production release/deployment;",
        "credentials/secrets/security/account changes;",
        "billing/spending;",
        "cross-repository scope expansion;",
        "Level-4 product-thesis revision;",
    ):
        assert phrase in ref

    assert "MERGE_AUTHORITY = YES" in ref
    assert "never infer those grants from the words" in ref
    assert "Protected-transition authority may be granted separately" in getting_started


def test_using_sensemaking_routes_repeated_full_autonomy_to_loop() -> None:
    using = USING.read_text(encoding="utf-8")
    delegated = DELEGATED.read_text(encoding="utf-8")

    assert "FULL AUTONOMY / FULL DELEGATION" in using
    assert "strategic-sensemaking-loop" in using
    assert "references/autonomous-terminal-mission-v1.md" in using

    assert "FULL AUTONOMY / FULL DELEGATION" in delegated
    assert "autonomous-terminal-mission-v1.md" in delegated
    assert "does not create a second goal model" in _flat(delegated)


def test_human_entry_points_expose_autonomous_terminal_mission() -> None:
    getting_started = GETTING_STARTED.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    assert "### Run a full-autonomy terminal mission" in getting_started
    assert "Run this repository mission with FULL AUTONOMY" in getting_started
    assert "STOP ONLY WHEN:" in getting_started

    assert "full-autonomy terminal mission" in readme
    assert "FULL AUTONOMY / FULL DELEGATION" in readme


def test_profile_adds_no_runtime_or_forced_authority_model() -> None:
    ref = REFERENCE.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")

    for phrase in (
        "new planner",
        "new authority model",
        "backlog executor",
        "numeric leverage score",
        "permission engine",
        "automatic router",
        "new Campaign schema",
    ):
        assert phrase in _flat(ref)

    assert "automatic protected merge/release/deploy authority from autonomy wording" in skill
