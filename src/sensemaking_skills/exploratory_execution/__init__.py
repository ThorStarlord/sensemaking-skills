"""Framework-governed campaign execution (Phase 6 correction, #122).

This package replaces the Phase 6 readiness "external infrastructure" with
execution machinery that lives INSIDE the pinned framework. Every module
here is an execution-relevant input under ADR 0023 §5/§10 and is therefore
bound by ``framework_sha`` -- part of the validated configuration and the
policy allowlist -- BEFORE execution, not merely digest-recorded after it.

Public API:

* ``ProductionSignedCommitVerifier`` -- full signed-commit approval
  binding: trusted repository, governed protected ancestry, registered
  signer fingerprint mapped to ``claimed_approver_identity``, exact
  approval-bytes equality, and signed-document field agreement.
* ``TargetCheckout.prepare`` -- materialize (or verify) the approved
  target repository at the exact SHA, clean and submodule-free.
* ``ClaudeProvider`` -- the permit-gated real provider: no SDK import or
  client without a genuine, consumed, attempt-bound provider permit; no
  Write tool; no ambient settings; no artifact persistence.
* ``CampaignBriefValidator`` -- delegates to the pinned canonical
  ``validate-brief.py`` with structural/substantive classification.
* ``build_exploratory_prompt`` -- the single pinned prompt construction.
* ``framework_tree_unchanged`` / ``execution_module_digests`` -- full-tree
  drift proof and byte-exact execution records.

The provider permit itself is issued by the Phase 4 durable boundary
(``campaign_accounting.permit``) after the durable INVOKED transition.
"""

from .artifact_validator import CampaignBriefValidator
from .claude_provider import (
    ALLOWED_SDK_TOOLS,
    ALLOWED_SETTING_SOURCES,
    ClaudeProvider,
    ProviderConfigMismatch,
    ProviderInvocationError,
    ProviderPermitDenied,
)
from .execution_identity import (
    GOVERNED_APPROVAL_PATH,
    GOVERNED_GITHUB_REPOSITORY,
    GOVERNED_PROTECTED_BRANCH,
    GOVERNED_REQUIRED_APPROVER_PERMISSION,
    TRUSTED_FRAMEWORK_REMOTE,
    checkout_sha,
    execution_module_digests,
    framework_tree_unchanged,
    module_digest,
)
from .conversation_approval import (
    APPROVAL_FILENAME as CONVERSATION_APPROVAL_FILENAME,
    APPROVAL_MECHANISM as CONVERSATION_APPROVAL_MECHANISM,
    APPROVAL_REFERENCE_KIND_GITHUB_ISSUE_COMMENT,
    APPROVAL_TEXT,
    ConversationApprovalVerifier,
    extract_frontmatter,
)
from .github_approval import (
    APPROVAL_MARKER,
    APPROVAL_MECHANISM,
    ApprovalCaptureError,
    GitHubApprovalError,
    GitHubIssueCommentApprovalVerifier,
    capture_approval_snapshot,
    parse_approval_comment,
)
from .production_verifier import ProductionSignedCommitVerifier
from .prompt_builder import build_exploratory_prompt
from .target_checkout import TargetCheckout, TargetCheckoutError

__all__ = [
    "ALLOWED_SDK_TOOLS",
    "ALLOWED_SETTING_SOURCES",
    "APPROVAL_MARKER",
    "APPROVAL_MECHANISM",
    "APPROVAL_REFERENCE_KIND_GITHUB_ISSUE_COMMENT",
    "APPROVAL_TEXT",
    "ApprovalCaptureError",
    "CONVERSATION_APPROVAL_FILENAME",
    "CONVERSATION_APPROVAL_MECHANISM",
    "ConversationApprovalVerifier",
    "GOVERNED_APPROVAL_PATH",
    "GOVERNED_GITHUB_REPOSITORY",
    "GOVERNED_PROTECTED_BRANCH",
    "GOVERNED_REQUIRED_APPROVER_PERMISSION",
    "TRUSTED_FRAMEWORK_REMOTE",
    "CampaignBriefValidator",
    "ClaudeProvider",
    "GitHubApprovalError",
    "GitHubIssueCommentApprovalVerifier",
    "ProductionSignedCommitVerifier",
    "TargetCheckout",
    "TargetCheckoutError",
    "build_exploratory_prompt",
    "capture_approval_snapshot",
    "checkout_sha",
    "execution_module_digests",
    "extract_frontmatter",
    "framework_tree_unchanged",
    "module_digest",
    "parse_approval_comment",
    "ProviderConfigMismatch",
    "ProviderInvocationError",
    "ProviderPermitDenied",
]
