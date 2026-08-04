"""Real claude-sonnet-5 provider adapter (Issue #122).

The Phase 4 durable boundary calls ``provider() -> bytes`` and preserves
the return value as the attempt's RAW provider output. This adapter is the
real provider integration: it builds the repo-sensemaker prompt from the
FROZEN framework checkout (the pinned ``framework_sha`` tree, which also
pins ``prompt_or_skill_revision``), invokes the pinned model through the
Claude Agent SDK, and returns the model's raw output bytes.

The adapter is INFRASTRUCTURE OUTSIDE THE CAMPAIGN CONFIGURATION. Its
content digest (``versions.adapter_versions``) is recorded in the
execution record; it never changes the campaign policy, configuration, or
framework bytes.

The adapter is never invoked by tests: every test injects a spy provider.
It is constructed only by an operator who intends a real provider call,
and it raises ``ProviderAdapterError`` on any failure instead of returning
partial or fabricated output.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class ProviderAdapterError(Exception):
    """The provider adapter failed; no partial output may be used."""


class ClaudeProviderAdapter:
    """Invoke ``claude-sonnet-5`` under the repo-sensemaker skill and return
    the raw model output bytes."""

    def __init__(
        self,
        *,
        framework_checkout: Path,
        target_repository: str,
        target_sha: str,
        model: str = "claude-sonnet-5",
        session_dir: Optional[Path] = None,
        timeout_seconds: int = 1800,
    ) -> None:
        self._framework_checkout = Path(framework_checkout)
        self._target_repository = target_repository
        self._target_sha = target_sha
        self._model = model
        self._session_dir = Path(session_dir) if session_dir else None
        self._timeout_seconds = timeout_seconds

    # -- config binding -----------------------------------------------------
    @property
    def model(self) -> str:
        return self._model

    @property
    def skill_path(self) -> Path:
        """The repo-sensemaker skill from the FROZEN framework checkout."""
        skill = self._framework_checkout / "skills" / "repo-sensemaker" / "SKILL.md"
        if not skill.is_file():
            raise ProviderAdapterError(
                f"frozen framework checkout has no repo-sensemaker skill at "
                f"{skill} (is the checkout at the pinned framework_sha?)"
            )
        return skill

    # -- the real call ------------------------------------------------------
    def __call__(self) -> bytes:
        """Run the skill against the pinned target and return raw bytes.

        NEVER invoked by tests; this is the real provider boundary. The
        prompt is built from the frozen framework checkout's skill file
        (pinned prompt_or_skill_revision), and the model is the pinned
        configuration model.
        """
        skill_text = self.skill_path.read_text(encoding="utf-8")
        output_dir = self._session_dir or Path(
            "experiments/campaigns/EXP-0001-stage1-auteur-autonomy-pilot"
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = (
            output_dir
            / f"raw-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.md"
        )

        prompt = (
            "You are executing the 'repo-sensemaker' skill as part of the "
            "EXP-0001 exploratory campaign.\n\n"
            f"## Frozen skill definition\n{skill_text}\n\n"
            f"## Target repository\n{self._target_repository}\n"
            f"## Target commit\n{self._target_sha}\n\n"
            "Produce the repository_sensemaking_brief artifact and write it "
            f"to:\n{output_path}\n"
        )

        try:
            # Lazy import: the SDK is an execution-time dependency, never a
            # test or import-time dependency (mirrors skill_executor.py).
            from claude_agent_sdk import ClaudeAgentOptions, query  # type: ignore

            result_text: list[str] = []
            import asyncio

            async def _run() -> None:
                async for message in query(
                    prompt=prompt,
                    options=ClaudeAgentOptions(
                        cwd=str(self._framework_checkout),
                        setting_sources=["project", "user"],
                        skills=["repo-sensemaker"],
                        allowed_tools=["Read", "Write", "Glob", "Grep"],
                        model=self._model,
                    ),
                ):
                    text = getattr(message, "text", None)
                    if text:
                        result_text.append(text)

            asyncio.run(asyncio.wait_for(_run(), timeout=self._timeout_seconds))
        except Exception as exc:  # noqa: BLE001 - fail closed, never partial
            raise ProviderAdapterError(
                f"provider invocation failed: {type(exc).__name__}: {exc}"
            ) from exc

        raw = "\n".join(result_text)
        if not raw.strip():
            raise ProviderAdapterError(
                "provider invocation returned no output; refusing to "
                "return empty raw output"
            )
        return raw.encode("utf-8")
