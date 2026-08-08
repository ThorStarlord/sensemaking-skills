# Task P1 — Owner Synthesis (compact human-facing answer)

experiment_type: product_interaction
record: owner-synthesis-v1
produced_by: repo-sensemaker (canonical in-repo copy @ b580389, standalone invocation)
shown_to_owner: 2026-08-07
source_investigation: repo-sensemaker-investigation-v1.md
validation: validation-result-v1.json (valid=false, 3 blocking EVIDENCE_QUOTE_NOT_FOUND on multiline excerpts; not repaired per P1 protocol)

---

## Recommended next work

Fix the **execution/distribution surface** first: ship the canonical SKILL.md
trees in the wheel, make `setup-skills` resolve its source from the installed
package, and add a drift check so installed copies cannot silently diverge from
the repo.

Why: this is a precondition for everything else. Users following the documented
install path (`pip install` + `setup-skills`) either cannot get the skills at
all (the wheel contains no SKILL.md) or run a stale copy — the one on this
machine is 4 months old and still teaches the `create-artifact.py` path
recomputation that ADR 0010/issue #40 explicitly forbids. Any product or
interaction improvement you make to repo-sensemaker is invisible to anyone
invoking an installed copy until this is fixed.

## Strongest evidence

1. The built wheel (`dist/sensemaking_skills-0.2.1-py3-none-any.whl`, 25
   entries) contains **no SKILL.md files**; `pyproject.toml:49` globs
   `skills/**/*` only under the package (Python modules), not the repo-root
   `skills/` trees where the actual skills live.
2. `src/sensemaking_skills/setup_skills.py:29-30` resolves its source as
   `Path(__file__).parent.parent.parent / "skills"` — a source-checkout-only
   layout; from an installed wheel the path does not exist, so the documented
   flow fails with "Skills directory not found ... incomplete installation".
3. `setup_skills.py:100-101` refuses to overwrite without `--force`; the
   installed copy at `~/.agents/skills/repo-sensemaker/SKILL.md` (119 lines)
   matches commit `178d5f0` (2026-05-22) and still says "Call
   `scripts/create-artifact.py` to resolve the output path" — while the
   canonical `SKILL.md:114` forbids exactly that call.
4. E1 (DEMOTE) and E2 (USE_AS_TRIAGE_SIGNAL) — both merged to `main` —
   independently concluded label accuracy is not the primary quality gate;
   decision-usefulness is. That supports your product/interaction direction,
   but the execution surface must be trustworthy before interaction
   improvements can reach anyone.

## Alternatives

- **A. Directly pursue the owner-facing interaction improvement** (compact
  synthesis, alternatives, uncertainty in the skill itself). Real and aligned
  with your priority, but it cannot be delivered through the current
  execution surface — users would never receive it.
- **B. Fix the docs maturity drift** (README says "production-ready" while
  CONTEXT.md records 60% progress and no value-production run). Real but low
  consequence; a cleanup, not a decision blocker.
- **C. Resolve the closed hardening-branch disposition** (452-line SKILL.md,
  GAP-5..GAP-9, deterministic exploration protocol). Consequential as a
  governance decision, but it does not block the distribution fix.
- **D. Do nothing / defer**: the framework has no external value-production
  users yet (CONTEXT.md:322). Defensible only if you intend to keep this
  internal; the distribution defect is already biting you (this very P1 run
  had to work around the stale installed copy).

## Uncertainty

- Whether the failure modes are hit by a **fresh** `pip install` in a clean
  venv (the probe was read-only; the wheel inspection and path resolution are
  deterministic, so confidence is high, but a clean-env reproduction is the
  definitive proof).
- Whether fixing distribution is a prerequisite you want *before* the
  interaction work, or whether you consider the interaction work valuable
  enough to do in-repo first and ship both together.
- Whether the closed hardening-branch content (which contains the standalone
  vs runtime invocation fix this run hit) should be salvaged as part of the
  fix or left closed.

## Decision-changing evidence

- If a clean-venv `pip install dist/*.whl && setup-skills` actually installs
  current SKILL.md files, the distribution boundary is not broken and the
  recommendation shifts to direct interaction work.
- If you decide the installed surface is irrelevant (e.g. all real users
  always clone the repo), the recommendation shifts to interaction work with
  distribution as a later hardening item.
- If the interaction work is time-boxed as a probe (like P1 itself) rather
  than a build, that changes sequencing: a second small real interaction
  could run before any implementation, including distribution.
