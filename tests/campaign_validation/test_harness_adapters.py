"""P10 qualification tests for explicit coding-agent harness adapters."""

from __future__ import annotations

from pathlib import Path

import pytest

from sensemaking_skills.harness_adapters import (
    HarnessAdapterError,
    canonical_harness_id,
    get_harness_adapter,
    resolve_harness_destinations,
)
from sensemaking_skills import setup_skills as setup_module


def _make_fake_skill_source(tmp_path: Path) -> Path:
    source = tmp_path / "packaged-skills"
    for name in ("using-sensemaking", "repo-sensemaker"):
        skill = source / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")
        refs = skill / "references"
        refs.mkdir()
        (refs / "contract.md").write_text(f"{name} contract\n", encoding="utf-8")
    return source


def test_user_scope_adapter_roots_are_explicit_and_deterministic(tmp_path: Path):
    home = tmp_path / "home"

    expected = {
        "generic": home / ".agents" / "skills",
        "claude": home / ".claude" / "skills",
        "codex": home / ".codex" / "skills",
        "opencode": home / ".config" / "opencode" / "skills",
    }
    for target, path in expected.items():
        result = resolve_harness_destinations(
            target, scope="user", home=home, env={}
        )
        assert len(result) == 1
        assert result[0].adapter_ids == (target,)
        assert result[0].scope == "user"
        assert result[0].path == path.absolute()


def test_codex_user_scope_honors_explicit_codex_home(tmp_path: Path):
    home = tmp_path / "home"
    codex_home = tmp_path / "configured-codex-home"
    result = resolve_harness_destinations(
        "codex",
        scope="user",
        home=home,
        env={"CODEX_HOME": str(codex_home)},
    )
    assert result[0].path == (codex_home / "skills").absolute()


def test_project_scope_adapter_roots_are_explicit_and_deterministic(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    expected = {
        "generic": project / ".agents" / "skills",
        "claude": project / ".claude" / "skills",
        "codex": project / ".agents" / "skills",
        "opencode": project / ".opencode" / "skills",
    }
    for target, path in expected.items():
        result = resolve_harness_destinations(
            target,
            scope="project",
            project_root=project,
        )
        assert len(result) == 1
        assert result[0].adapter_ids == (target,)
        assert result[0].scope == "project"
        assert result[0].path == path.absolute()


def test_agents_alias_preserves_generic_adapter_identity(tmp_path: Path):
    home = tmp_path / "home"
    assert canonical_harness_id("agents") == "generic"
    assert get_harness_adapter("agents") is get_harness_adapter("generic")

    agents = resolve_harness_destinations("agents", home=home, env={})
    generic = resolve_harness_destinations("generic", home=home, env={})
    assert agents == generic
    assert agents[0].adapter_ids == ("generic",)


def test_all_user_scope_preserves_distinct_native_personal_roots(tmp_path: Path):
    home = tmp_path / "home"
    result = resolve_harness_destinations(
        "all", scope="user", home=home, env={}
    )

    assert [item.adapter_ids for item in result] == [
        ("generic",),
        ("claude",),
        ("codex",),
        ("opencode",),
    ]
    assert [item.path for item in result] == [
        (home / ".agents" / "skills").absolute(),
        (home / ".claude" / "skills").absolute(),
        (home / ".codex" / "skills").absolute(),
        (home / ".config" / "opencode" / "skills").absolute(),
    ]


def test_all_project_scope_deduplicates_generic_and_codex_shared_root(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    result = resolve_harness_destinations(
        "all", scope="project", project_root=project
    )

    assert [item.adapter_ids for item in result] == [
        ("generic", "codex"),
        ("claude",),
        ("opencode",),
    ]
    assert [item.path for item in result] == [
        (project / ".agents" / "skills").absolute(),
        (project / ".claude" / "skills").absolute(),
        (project / ".opencode" / "skills").absolute(),
    ]


def test_adapter_resolution_fails_closed_on_unknown_or_incomplete_requests(
    tmp_path: Path,
):
    with pytest.raises(HarnessAdapterError, match="Unknown harness target"):
        resolve_harness_destinations("mystery")

    with pytest.raises(HarnessAdapterError, match="Unknown harness scope"):
        resolve_harness_destinations("claude", scope="machine")

    with pytest.raises(HarnessAdapterError, match="project-root"):
        resolve_harness_destinations("claude", scope="project")

    missing = tmp_path / "missing"
    with pytest.raises(HarnessAdapterError, match="does not exist"):
        resolve_harness_destinations(
            "claude", scope="project", project_root=missing
        )

    not_dir = tmp_path / "file"
    not_dir.write_text("x", encoding="utf-8")
    with pytest.raises(HarnessAdapterError, match="not a directory"):
        resolve_harness_destinations(
            "claude", scope="project", project_root=not_dir
        )


def test_project_setup_copies_exact_skill_trees_without_harness_detection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    source = _make_fake_skill_source(tmp_path)
    monkeypatch.setattr(setup_module, "get_package_skills_dir", lambda: source)

    project = tmp_path / "project"
    project.mkdir()

    assert setup_module.setup_skills(
        target="claude",
        scope="project",
        project_root=project,
    )

    destination = project / ".claude" / "skills"
    for name in ("using-sensemaking", "repo-sensemaker"):
        assert (destination / name / "SKILL.md").read_bytes() == (
            source / name / "SKILL.md"
        ).read_bytes()
        assert (destination / name / "references" / "contract.md").read_bytes() == (
            source / name / "references" / "contract.md"
        ).read_bytes()

    # Setup writes only the declared discovery root. It does not manufacture a
    # Campaign workspace, select a Skill, or create harness runtime metadata.
    assert not (project / "campaign-state.yaml").exists()
    assert not (project / ".sensemaking").exists()


def test_project_setup_supports_codex_and_opencode_native_roots(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    source = _make_fake_skill_source(tmp_path)
    monkeypatch.setattr(setup_module, "get_package_skills_dir", lambda: source)

    codex_project = tmp_path / "codex-project"
    codex_project.mkdir()
    assert setup_module.setup_skills(
        target="codex", scope="project", project_root=codex_project
    )
    assert (
        codex_project / ".agents" / "skills" / "repo-sensemaker" / "SKILL.md"
    ).is_file()

    opencode_project = tmp_path / "opencode-project"
    opencode_project.mkdir()
    assert setup_module.setup_skills(
        target="opencode", scope="project", project_root=opencode_project
    )
    assert (
        opencode_project
        / ".opencode"
        / "skills"
        / "repo-sensemaker"
        / "SKILL.md"
    ).is_file()


def test_project_all_writes_each_unique_native_root_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    source = _make_fake_skill_source(tmp_path)
    monkeypatch.setattr(setup_module, "get_package_skills_dir", lambda: source)

    project = tmp_path / "project"
    project.mkdir()
    assert setup_module.setup_skills(
        target="all", scope="project", project_root=project
    )

    output = capsys.readouterr().out
    assert "Target locations: 3" in output
    for root in (
        project / ".agents" / "skills",
        project / ".claude" / "skills",
        project / ".opencode" / "skills",
    ):
        assert (root / "using-sensemaking" / "SKILL.md").is_file()

    # The historical Superpowers cache has no project-local meaning and must
    # not be synthesized under the project by `all`.
    assert not (project / ".claude" / "plugins").exists()


def test_setup_request_validation_is_explicit_and_fail_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    source = _make_fake_skill_source(tmp_path)
    monkeypatch.setattr(setup_module, "get_package_skills_dir", lambda: source)

    project = tmp_path / "project"
    project.mkdir()

    assert not setup_module.setup_skills(
        target="claude",
        scope="project",
        project_root=project,
        skills_dir=str(tmp_path / "unexpected"),
    )
    assert "--skills-dir is only valid" in capsys.readouterr().err

    assert not setup_module.setup_skills(
        target="custom",
        scope="project",
        project_root=project,
        skills_dir=str(tmp_path / "custom"),
    )
    assert "--scope applies to harness adapters" in capsys.readouterr().err

    assert not setup_module.setup_skills(
        target="claude-superpowers",
        scope="project",
        project_root=project,
    )
    assert "user scope only" in capsys.readouterr().err


def test_dry_run_creates_no_harness_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    source = _make_fake_skill_source(tmp_path)
    monkeypatch.setattr(setup_module, "get_package_skills_dir", lambda: source)

    project = tmp_path / "project"
    project.mkdir()
    assert setup_module.setup_skills(
        target="opencode",
        scope="project",
        project_root=project,
        dry_run=True,
    )
    assert not (project / ".opencode").exists()


def test_divergent_harness_copy_requires_explicit_force(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    source = _make_fake_skill_source(tmp_path)
    monkeypatch.setattr(setup_module, "get_package_skills_dir", lambda: source)

    project = tmp_path / "project"
    project.mkdir()
    kwargs = {
        "target": "claude",
        "scope": "project",
        "project_root": project,
    }
    assert setup_module.setup_skills(**kwargs)

    installed = project / ".claude" / "skills" / "repo-sensemaker" / "SKILL.md"
    installed.write_text("# divergent\n", encoding="utf-8")

    assert not setup_module.setup_skills(**kwargs)
    assert installed.read_text(encoding="utf-8") == "# divergent\n"

    assert setup_module.setup_skills(**kwargs, force=True)
    assert installed.read_bytes() == (
        source / "repo-sensemaker" / "SKILL.md"
    ).read_bytes()
