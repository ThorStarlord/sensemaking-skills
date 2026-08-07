# Decision 05 — product-sensemaking layer

## 1. Decision
Should Sensemaking Skills add a distinct product-sensemaking capability above engineering diagnosis, keep discovery as a manual prompt/playbook, or do nothing and use existing tools?

## 2. Known
- **OBSERVED:** the repository vocabulary recognizes product fog, while repo-sensemaker diagnoses codebase signals and recommends workflows.
- **OBSERVED:** current credible evidence is narrower than the broad diagnosis-and-orchestration positioning: external usefulness, routing, and provider coverage remain unvalidated (`docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md:70,280-311`).
- **OBSERVED:** this experiment's five cases repeatedly encounter questions that repository artifacts cannot answer: actionability, user preference, consent comprehension, and comparative executor value.
- **DERIVED:** engineering sensemaking alone can identify evidence gaps, but cannot manufacture demand or behavior evidence.

## 3–4. Uncertainty and type
Dominant: **problem validation**. Do maintainers repeatedly make costly build decisions without identifying decision-changing uncertainty? Does a lightweight loop change those decisions? Skill packaging and construction are downstream.

## 5. Alternatives
1. Do nothing: use existing prompts, repo-sensemaker, and human judgment.
2. Keep a manual discovery worksheet/concierge practice outside canonical skills.
3. Prototype a narrow evidence-synthesis or experiment-design skill after repeated use.
4. Build a broad `product-sensemaker` lifecycle/router now.

## 6. Highest-value uncertainty
Across real decisions, does the process change what is done next enough to outweigh its burden—and is that benefit attributable to repeatable mechanics rather than a good facilitator?

## 7–9. Cheapest credible experiment
**Hypothesis:** a short manual sequence—decision, known/unknown, alternatives, decision-changing uncertainty, cheapest credible probe, predeclared evidence, synthesis—prevents premature implementation, but a broad skill is premature.

This task is the concierge probe across five decisions. Compare the initial binary framing with final disposition and identify steps that changed understanding.

- **Observations:** reframed decisions, discarded implementation, external-evidence flags, repeated steps, ceremony.
- **Success:** several cases change next action or prevent unjustified build work for traceable reasons.
- **Failure:** conclusions are identical and steps only expand prose.
- **Kill:** do not build a broad skill unless the method repeats in real owner decisions and produces externally validated value.
- **Ambiguous:** analysis changes language but no actual owner action is observed.

**Probe result:** all five cases changed from binary architecture choices to bounded experiments or proportional policies; four explicitly require real-world evidence. This is evidence of reasoning utility, not product demand or outcome value.

## 10. Synthesis
- **Original hypothesis:** a product-sensemaker may be useful.
- **Evidence:** all case analyses plus repository readiness gaps.
- **Observations:** highest-value uncertainty and evidence boundaries repeatedly prevented implementation; full lifecycle labels added little.
- **Surprise:** experiment design and evidence synthesis repeated more than “problem discovery.”
- **Contradiction:** repeated reasoning utility does not establish need for a named product layer.
- **Changed understanding:** retain a manual decision-probe, not a new system layer.
- **Current preferred:** keep manual; no broad skill.
- **Confidence:** high on “do not build yet,” low on eventual demand.
- **Unresolved:** owner/user behavior and facilitation burden in real sessions.
- **Next experiment:** apply a one-page manual worksheet prospectively to 5 real owner decisions and compare action before/after.
- **Disposition:** **DISCARD for now** the broad skill; **CONTINUE** manual testing.
