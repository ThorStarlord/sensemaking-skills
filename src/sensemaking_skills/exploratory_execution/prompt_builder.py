"""Pinned prompt construction for EXP-0001 attempts (Phase 6 correction).

Prompt construction is an execution-relevant input, so it lives in the
pinned framework (bound by ``framework_sha``) as ONE implementation --
never duplicated inside an adapter. The prompt embeds:

* the exact frozen repo-sensemaker skill bytes from the pinned framework
  checkout (``prompt_or_skill_revision`` == ``framework_sha``);
* the exact approved target identity (repository + commit);
* the exact runtime-owned expected artifact path for THIS attempt;
* the requirement to RETURN the complete brief in the final response --
  the provider has no Write tool, so the model cannot persist anything;
  the Phase 4 recorder owns all persistence.

The prompt is deterministic: identical inputs produce identical bytes.
"""

from __future__ import annotations


def build_exploratory_prompt(
    *,
    skill_text: str,
    target_repository: str,
    target_sha: str,
    expected_output_path: str,
    artifact_type: str,
    campaign_id: str = "EXP-0001-stage1-auteur-autonomy-pilot",
) -> str:
    """Build the exact prompt for one exploratory attempt.

    ``expected_output_path`` is the attempt's runtime-owned produced
    artifact path (the path the recorder will preserve the artifact
    under); it is the ONLY output path named anywhere in the run.
    """
    return (
        "You are executing the 'repo-sensemaker' skill as one attempt of "
        f"the {campaign_id} exploratory campaign.\n\n"
        "## Frozen skill definition\n"
        f"{skill_text}\n\n"
        "## Target repository\n"
        f"{target_repository}\n"
        "## Target commit (must be the exact repository state you analyze)\n"
        f"{target_sha}\n\n"
        "## Output contract\n"
        f"- Artifact type: {artifact_type}\n"
        "- Produce the COMPLETE repository_sensemaking_brief document: the "
        "prose sections AND the Section 13 machine-readable handoff YAML "
        "block.\n"
        "- RETURN the complete brief document in your final response. You "
        "have no Write tool; do not attempt to write files.\n"
        "- The runtime records this response as the raw output and "
        "preserves the validated artifact at the exact runtime-owned "
        f"path:\n{expected_output_path}\n"
        "- Every claim about the target must be grounded in files you "
        "actually read from the target repository checkout (Read, Glob, "
        "Grep). Do not rely on memory or external context.\n"
    )
