"""Real Claude provider for exploratory campaign attempts (Phase 6, #122).

The provider is FRAMEWORK-GOVERNED (pinned by ``framework_sha``) and its
SDK call is STRUCTURALLY gated: ``__call__`` requires a genuine, consumed,
attempt-bound ``ProviderPermit`` issued by the Phase 4 durable boundary
AFTER the durable INVOKED transition. Every gate runs BEFORE the
``claude_agent_sdk`` module is imported or any client is constructed:

1. the permit must be genuine (closure sentinel + on-disk registry record
   + ledger state INVOKED + consumed marker) and bound to the exact
   attempt, campaign, and configuration;
2. the provider's own bound configuration (constructed from the validated
   campaign configuration) must match the invocation context's model,
   target repository, target SHA, framework SHA, and artifact type;

Only then is the SDK imported and ``query`` reached. A direct call without
a permit, with a forged permit, or with a config mismatch fails before the
SDK exists. The class is not subclassable, so a subclass cannot override
``__call__`` to bypass the gates.

Execution confinement:

* ``cwd`` is the verified TARGET checkout (never the framework checkout);
* the tool envelope is Read/Glob/Grep ONLY -- no Write, no Bash, no
  filesystem mutation;
* settings sources are explicitly empty -- no project or user ambient
  settings, hooks, plugins, or MCP servers can alter the run;
* the provider performs NO artifact persistence and creates NO output
  paths; it returns raw response bytes plus post-hoc usage observations,
  and the Phase 4 recorder remains the sole durable persistence authority.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sensemaking_skills.campaign_accounting import (
    ProviderResponse,
    require_usable_provider_permit,
)

#: The minimal, authorized SDK tool envelope. No Write: the recorder owns
#: all persistence. No Bash/BashTool: no arbitrary execution.
ALLOWED_SDK_TOOLS = ("Read", "Glob", "Grep")

#: Settings sources are explicitly empty: ambient user/project settings,
#: hooks, plugins, and MCP servers are all excluded from the run.
ALLOWED_SETTING_SOURCES = ()


class ProviderConfigMismatch(Exception):
    """The provider's bound configuration disagrees with the invocation."""


class ProviderPermitDenied(Exception):
    """The provider call was refused before any SDK import or client."""


class ProviderInvocationError(Exception):
    """The SDK call itself failed; no partial output may be used."""


class ClaudeProvider:
    """Invoke the approved model under the pinned skill and return the raw
    response bytes. Not subclassable; requires a consumed provider permit."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        raise TypeError(
            "ClaudeProvider may not be subclassed; a subclass could "
            "override the permit-gated provider path"
        )

    def __init__(
        self,
        *,
        model: str,
        target_repository: str,
        target_sha: str,
        framework_sha: str,
        artifact_type: str,
        target_checkout: Path,
        timeout_seconds: int = 1800,
    ) -> None:
        self._model = model
        self._target_repository = target_repository
        self._target_sha = target_sha
        self._framework_sha = framework_sha
        self._artifact_type = artifact_type
        self._target_checkout = Path(target_checkout)
        self._timeout_seconds = timeout_seconds

    # -- bound configuration (constructed from the validated document) -----
    @property
    def model(self) -> str:
        return self._model

    @property
    def target_repository(self) -> str:
        return self._target_repository

    @property
    def target_sha(self) -> str:
        return self._target_sha

    @property
    def framework_sha(self) -> str:
        return self._framework_sha

    @property
    def artifact_type(self) -> str:
        return self._artifact_type

    @property
    def target_checkout(self) -> Path:
        return self._target_checkout

    # -- the permit-gated call ---------------------------------------------
    def __call__(
        self,
        *,
        permit: Any,
        context: Any,
        prompt: str,
    ) -> ProviderResponse:
        """Run the approved model under the pinned skill.

        Refused (before any SDK import or client construction) unless a
        genuine, consumed, attempt-bound permit is supplied and the bound
        configuration matches the invocation context.
        """
        # 1. Structural permit gate: the one-shot provider permit issued by
        #    the durable boundary after INVOKED. Fails before the SDK
        #    module is even imported.
        campaign_root = Path(getattr(context, "campaign_root", "") or ".")
        try:
            require_usable_provider_permit(
                permit,
                campaign_root=campaign_root,
                attempt_id=str(getattr(context, "attempt_id", "")),
                campaign_id=str(getattr(context, "campaign_id", "")),
                configuration_id=str(getattr(context, "configuration_id", "")),
            )
        except Exception as exc:  # any permit failure is a denial
            raise ProviderPermitDenied(
                f"provider entry refused before SDK import: {exc}"
            ) from exc

        # 2. Configuration binding: the ACTUAL adapter must be the validated
        #    configuration, not merely a production-looking class.
        mismatches = []
        if self._model != getattr(context, "model", None):
            mismatches.append(
                f"model {self._model!r} != context {getattr(context, 'model', None)!r}"
            )
        if self._target_repository != getattr(context, "target_repository", None):
            mismatches.append("target_repository differs from the invocation context")
        if self._target_sha != getattr(context, "target_sha", None):
            mismatches.append("target_sha differs from the invocation context")
        if self._framework_sha != getattr(context, "framework_sha", None):
            mismatches.append("framework_sha differs from the invocation context")
        if self._artifact_type != getattr(context, "artifact_type", None):
            mismatches.append("artifact_type differs from the invocation context")
        if mismatches:
            raise ProviderConfigMismatch(
                "provider configuration is not the validated configuration: "
                + "; ".join(mismatches)
            )

        # 3. The SDK is imported ONLY here, after every gate passed.
        try:
            from claude_agent_sdk import ClaudeAgentOptions, query  # type: ignore
        except Exception as exc:  # an unavailable SDK fails closed
            raise ProviderInvocationError(
                f"claude_agent_sdk is unavailable: {exc}"
            ) from exc

        try:
            import asyncio

            result_text: list[str] = []
            tokens_observed: int | None = None
            cost_observed: dict | None = None

            async def _run() -> None:
                nonlocal tokens_observed, cost_observed
                async for message in query(
                    prompt=prompt,
                    options=ClaudeAgentOptions(
                        cwd=str(self._target_checkout),
                        model=self._model,
                        allowed_tools=list(ALLOWED_SDK_TOOLS),
                        setting_sources=list(ALLOWED_SETTING_SOURCES),
                        mcp_servers={},
                        skills=[],
                    ),
                ):
                    text = getattr(message, "text", None)
                    if text:
                        result_text.append(text)
                    total_cost = getattr(message, "total_cost_usd", None)
                    if total_cost is not None:
                        cost_observed = {
                            "amount": float(total_cost),
                            "currency": "USD",
                        }
                    usage = getattr(message, "usage", None)
                    if usage is not None:
                        tokens_observed = int(
                            getattr(usage, "input_tokens", 0) or 0
                        ) + int(getattr(usage, "output_tokens", 0) or 0)

            asyncio.run(asyncio.wait_for(_run(), timeout=self._timeout_seconds))
        except Exception as exc:  # fail closed, never partial
            raise ProviderInvocationError(
                f"provider invocation failed: {type(exc).__name__}: {exc}"
            ) from exc

        raw = "\n".join(result_text)
        if not raw.strip():
            raise ProviderInvocationError(
                "provider invocation returned no output; refusing to "
                "return empty raw output"
            )
        return ProviderResponse(
            raw_output=raw.encode("utf-8"),
            tokens_observed=tokens_observed,
            cost_observed=cost_observed,
        )
