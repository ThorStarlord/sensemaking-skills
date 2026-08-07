# Decision 04 — automatic transition or recommendation

## 1. Decision
After diagnosis, should the system stop with a recommendation, require explicit acceptance before transition, or begin the next workflow automatically with an opt-out?

## 2. Known
- **OBSERVED:** repo-sensemaker forbids implementation and outputs a diagnostic artifact (`skills/repo-sensemaker/SKILL.md:98`).
- **OBSERVED:** Stage 2 explicitly preserves Diagnosis → Recommendation → Selection and says escalation is normally a recommendation rather than an automatic action (`docs/STAGE-2-COMPLETE.md:92,259`).
- **OBSERVED:** ADR 0013 proposes the agent decide the next step from artifact and validation results (`docs/adr/0013-agent-native-orchestration-primary.md:48`).
- **OBSERVED:** external routing correctness is not evidenced (`docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md:70-71`).

## 3–4. Uncertainty and type
Dominant: **problem validation**: is transition friction a real user problem, and when do users want control? Solution validation follows: does auto-transition save effort without magnifying a wrong diagnosis? Repository artifacts cannot measure acceptance, reversals, or regret.

## 5. Alternatives
1. Recommend and stop; user/agent starts any next workflow separately.
2. Present recommendation and rationale, require explicit acceptance, then transition.
3. Auto-transition for reversible/read-only planning, stop before mutation; opt-out available.
4. Always auto-route end to end.

## 6. Highest-value uncertainty
How frequently would the recipient reject or materially revise the recommendation before spending downstream effort?

## 7–9. Cheapest credible experiment
**Hypothesis:** explicit acceptance is the safest useful default until routing accuracy and user preference are observed; low-consequence planning may later earn auto-transition.

In 8 real sessions, return the recommendation and a one-line choice: accept, choose another path, or stop. Record choice, rationale, time, and whether downstream work would have been wasted. Do not add router machinery.

- **Observations:** acceptance/override/stop, reason, downstream consequence, reversibility.
- **Success for auto-transition:** recommendations are consistently accepted and early downstream work is reversible/useful.
- **Failure:** meaningful overrides or misdiagnoses would waste work or mutate state.
- **Kill:** no auto-transition into mutation while routing lacks external validation.
- **Ambiguous:** users accept reflexively but later regret it.

**Available probe:** artifact comparison exposes a real policy tension and no outcome data. **REQUIRES_REAL_WORLD_EVIDENCE.**

## 10. Synthesis
- **Original hypothesis:** automatic routing reduces friction.
- **Observations:** architectural documents support both agent autonomy and explicit selection; external accuracy is unknown.
- **Surprise:** the repository already contains the cheapest experiment—the recommendation/selection split—without needing automation.
- **Contradiction:** broad “workflow orchestration” positioning outruns externally proven routing.
- **Changed understanding:** transition authority should scale with reversibility and evidence, not be one global mode.
- **Current preferred:** explicit accept-then-transition; recommend-and-stop remains valid for handoffs.
- **Confidence:** medium.
- **Next experiment:** log choices in real concierge sessions.
- **Disposition:** **REVISE** auto-routing into staged authority; do not implement a router.
