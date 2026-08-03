"""Installed-wheel smoke test.

Builds the package as an actual wheel, installs it into a throwaway venv
alongside its declared runtime dependencies, and exercises the FULL public
API -- including an actual valid policy + operative approval + configuration
bundle validation -- from a working directory that has neither ``docs/``
nor ``scripts/`` available. This proves the package does not silently
depend on ``Path(__file__).parents[...] / "docs"`` / ``"scripts"`` / a
sibling repository-root layout at runtime (it must load its JSON schemas
via ``importlib.resources`` and its path-containment helpers via a normal
package import, not a repository-relative filesystem walk), AND that a
genuinely successful validation actually works end-to-end through the
installed distribution, not merely that imports resolve.

This test is slow (builds a wheel and a venv) and touches the network only
to resolve already-pinned dependency versions from the configured index
(no external network calls are made by the package itself). It runs as a
dedicated CI job (see .github/workflows/validation.yml's
"Phase 2 installed-wheel smoke test" job) rather than being folded into the
main campaign-validation suite, precisely so a packaging regression here is
visually distinct from an ordinary test failure.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
import venv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# The bundle-construction / YAML-rendering logic below is DELIBERATELY
# reimplemented inline (not imported from this repo's tests/campaign_validation
# fixture helpers) -- the whole point of this test is to exercise the
# INSTALLED PACKAGE from a location with no access to this repository's test
# helpers at all, only to the public API the wheel actually ships.
_SMOKE_SCRIPT = r'''
import os
import sys

assert not os.path.isdir("docs"), "docs/ must not be visible to this smoke test"
assert not os.path.isdir("scripts"), "scripts/ must not be visible to this smoke test"

import sensemaking_skills.campaign_validation as cv
from sensemaking_skills import path_containment as pc

# --- Schemas load as packaged resources -------------------------------------
from sensemaking_skills.campaign_validation import schema_validation
assert schema_validation.policy_schema_errors({}) != []

# --- Path-containment helpers load and work ---------------------------------
canon = pc.canonicalize_path("a/b/c")
assert canon.parts == ("a", "b", "c")


def _quote(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _scalar(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    return _quote(str(v))


def dump(value, indent=0):
    pad = "  " * indent
    if isinstance(value, dict):
        if not value:
            return pad + "{}\n"
        lines = []
        for k, v in value.items():
            if isinstance(v, dict) and v:
                lines.append(pad + k + ":")
                lines.append(dump(v, indent + 1).rstrip("\n"))
            elif isinstance(v, list) and v:
                lines.append(pad + k + ":")
                lines.append(dump(v, indent).rstrip("\n"))
            elif isinstance(v, dict):
                lines.append(pad + k + ": {}")
            elif isinstance(v, list):
                lines.append(pad + k + ": []")
            else:
                lines.append(pad + k + ": " + _scalar(v))
        return "\n".join(lines) + "\n"
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, dict):
                sub = dump(item, indent + 1).split("\n")
                lines.append(pad + "- " + sub[0].strip())
                lines.extend(x for x in sub[1:] if x.strip())
            else:
                lines.append(pad + "- " + _scalar(item))
        return "\n".join(lines) + "\n"
    return pad + _scalar(value) + "\n"


FRAMEWORK_SHA = "a" * 40
TARGET_SHA = "b" * 40
TARGET_REPO = "https://example.invalid/example-owner/example-target.git"
MODEL = "example-model-identifier"
ARTIFACT_TYPE = "repository_sensemaking_brief"
APPROVER = "example-authorized-owner"

config_doc = {
    "configuration_schema_version": "1",
    "configuration_id": "0" * 64,
    "campaign_id": "EXP-0001-example",
    "framework_sha": FRAMEWORK_SHA,
    "target_repository": TARGET_REPO,
    "target_sha": TARGET_SHA,
    "model_identifier": MODEL,
    "prompt_or_skill_revision": "example-skill@v1",
    "validator_revision": "example-validator@v1",
    "artifact_type": ARTIFACT_TYPE,
    "execution_parameters": {"max_tokens_hint": 4096, "tool_allowlist": ["read_repository"]},
}
config_doc["configuration_id"] = cv.compute_configuration_id(config_doc)

policy_doc = {
    "policy_schema_version": "1",
    "campaign_id": "EXP-0001-example",
    "policy_digest": "0" * 64,
    "classification": "EXPLORATORY_NOT_CANONICAL_EVIDENCE",
    "allowed_framework_shas": [FRAMEWORK_SHA],
    "allowed_targets": [{"repository": TARGET_REPO, "sha": TARGET_SHA}],
    "allowed_models": [MODEL],
    "allowed_artifact_types": [ARTIFACT_TYPE],
    "allowed_configuration_ids": [config_doc["configuration_id"]],
    "max_attempt_slots": 5,
    "max_provider_invocations": 5,
    "max_attempts_per_configuration": 2,
    "concurrency_ceiling": 1,
    "token_ceiling": None,
    "cost_ceiling": None,
    "validity_window": {
        "not_before": "2026-01-01T00:00:00+00:00",
        "not_after": "2027-01-08T00:00:00+00:00",
    },
    "target_mutation_prohibited": True,
    "fallback_prohibited": True,
    "repair_prohibited": True,
    "automatic_merge_prohibited": True,
    "preservation_requirements": "Every reservation and attempt result is preserved.",
    "logging_requirements": "Every provider invocation is logged.",
    "prepared_by": "campaign-operator-agent",
    "prepared_at": "2026-01-01T00:00:00+00:00",
}
policy_doc["policy_digest"] = cv.compute_policy_digest(policy_doc)

approval_doc = {
    "approval_schema_version": "1",
    "campaign_id": policy_doc["campaign_id"],
    "policy_digest": policy_doc["policy_digest"],
    "claimed_approver_identity": APPROVER,
    "approval_provenance": {"mechanism": "signed_commit", "reference": "c" * 40},
    "approval_statement": "I approve this exploratory campaign policy.",
    "approved_at": "2026-01-02T00:00:00+00:00",
}

policy_bytes = dump(policy_doc).encode("utf-8")
approval_bytes = dump(approval_doc).encode("utf-8")
config_bytes = dump(config_doc).encode("utf-8")

ctx = cv.ValidationContext(
    current_time="2026-06-01T00:00:00+00:00",
    allowed_approver_identities=frozenset({APPROVER}),
)

# --- The actual valid-bundle validation, through the installed public API --
result = cv.validate_campaign_bundle(policy_bytes, approval_bytes, config_bytes, ctx)
assert result.valid, (result.failure_code, result.detail)
assert isinstance(result.value, cv.ValidatedCampaignBundle), type(result.value)
assert isinstance(result.value.policy, cv.CampaignPolicy)
assert isinstance(result.value.approval, cv.CampaignApproval)
assert isinstance(result.value.configuration, cv.ConfigurationIdentity)

# The bundle is immutable even from the installed wheel.
try:
    result.value.policy.raw["campaign_id"] = "tampered"
    raise AssertionError("expected TypeError mutating an immutable raw mapping")
except TypeError:
    pass

# --- No provider module was imported or invoked -----------------------------
_FORBIDDEN_PROVIDER_MODULE_SUBSTRINGS = (
    "anthropic", "openai", "skill_executor", "gate_a_authorization", "provider_client",
)
for modname in list(sys.modules):
    for bad in _FORBIDDEN_PROVIDER_MODULE_SUBSTRINGS:
        assert bad not in modname, f"provider-facing module imported: {modname}"

print("WHEEL_SMOKE_OK")
'''


def test_installed_wheel_validates_a_full_bundle_outside_repository_checkout(tmp_path):
    wheel_dir = tmp_path / "wheel"
    venv_dir = tmp_path / "venv"
    work_dir = tmp_path / "work"
    work_dir.mkdir()

    build = subprocess.run(
        [sys.executable, "-m", "pip", "wheel", str(REPO_ROOT), "--no-deps",
         "--wheel-dir", str(wheel_dir)],
        capture_output=True, text=True, timeout=300,
    )
    assert build.returncode == 0, build.stdout + build.stderr

    wheels = list(wheel_dir.glob("*.whl"))
    assert len(wheels) == 1, f"expected exactly one wheel, got {wheels}"

    venv.create(venv_dir, with_pip=True)
    venv_python = venv_dir / ("Scripts/python.exe" if sys.platform.startswith("win")
                               else "bin/python")

    install = subprocess.run(
        [str(venv_python), "-m", "pip", "install", str(wheels[0]),
         "PyYAML>=6.0,<7.0", "jsonschema>=4.18,<5.0", "rfc8785>=0.1.4,<0.2"],
        capture_output=True, text=True, timeout=300,
    )
    assert install.returncode == 0, install.stdout + install.stderr

    run = subprocess.run(
        [str(venv_python), "-c", _SMOKE_SCRIPT],
        capture_output=True, text=True, timeout=60, cwd=str(work_dir),
    )
    assert run.returncode == 0, run.stdout + run.stderr
    assert "WHEEL_SMOKE_OK" in run.stdout
