# Experimental Intelligence Components v0 — evaluation protocol

schema: experimental-intelligence-components-v0/evaluation-protocol-v0
component: strategic-planner-v0
issue: #395
status: exploratory lab protocol

## Question

Does explicit strategic candidate generation improve repository-level next-responsibility reasoning enough to justify promotion beyond ordinary model-native Sensemaking?

This is not a test of whether a planner can produce plausible prose. The relevant question is whether the treatment changes consequential decisions for the better at acceptable cost.

## Arms

### Baseline

Use the current Sensemaking Level-3 model normally:

repository/product state -> strategic decision to support -> decision-changing uncertainty -> one warranted repository-level responsibility or decline selection

Do not require explicit enumeration of multiple candidate responsibilities unless the baseline reasoner independently finds that useful.

### Treatment

Use the same case evidence plus StrategicPlanner v0. The planner must:

1. generate 2–4 materially distinct candidate repository-level responsibilities;
2. state the strategic decision each candidate would support;
3. identify the decision-changing uncertainty for each candidate;
4. expose material dependencies;
5. state the smallest plausible intervention;
6. record reasons for and against each candidate;
7. identify invalidation/stop evidence;
8. return the candidate set to the active semantic agent.

The planner must not choose a final winner, execute work, expand authority, infer new repository scope, or assign numeric priority scores.

candidate generation != strategic decision
candidate comparison != authorization
planner output != implementation plan

## Observation dimensions

Use categorical observations. Do not sum or weight them.

### Decision materiality

- SAME — treatment does not materially change the selected/declined responsibility.
- BETTER_SUPPORTED — same responsibility, but treatment exposes material rationale or uncertainty the baseline omitted.
- MATERIALLY_DIFFERENT_PLAUSIBLE — treatment surfaces a credible different responsibility requiring adjudication.
- MATERIALLY_WORSE — treatment steers toward less warranted work.
- UNCLEAR — evidence cannot discriminate.

### Missing-option discovery

- NONE
- MATERIAL_OPTION_SURFACED
- ONLY_COSMETIC_ALTERNATIVES
- NOISY_OPTION_EXPANSION
- UNCLEAR

### Wrong-work avoidance

- UNCHANGED
- PLAUSIBLY_AVOIDED
- INTRODUCED_RISK
- UNCLEAR

### Ceremony / overhead

- NEGLIGIBLE
- PROPORTIONAL
- NOTICEABLE_BUT_ACCEPTABLE
- DISPROPORTIONATE

### Reversal exposure

- UNCHANGED
- LOWER
- HIGHER
- UNCLEAR

### Human correction

- LESS
- SAME
- MORE
- NOT_OBSERVABLE

### Cost proportionality

Record qualitative differences in turns/tool calls/context burden. Do not invent monetary or token precision when not directly measured.

## Initial dogfood limitations

The first four cases are retrospective real repository decisions. The current evaluator knows the historical outcomes.

retrospective agreement != prospective performance
hindsight plausibility != avoided failure
same-context analysis != independent evidence

The initial dogfood can reject an obviously bad component, reveal ceremony, identify activation hypotheses, or justify more prospective research. It cannot establish comparative superiority or PROMOTE_CORE.

## Disposition rule

Record exactly one:

- PROMOTE_CORE
- PROMOTE_OPTIONAL
- DESCALE
- RESEARCH_MORE
- REMOVE

For this retrospective first package, PROMOTE_CORE is not supported by design. Any promotion claim requires later prospective normal-use evidence.

## Kill conditions

Prefer REMOVE or DESCALE if the treatment:

- mostly restates baseline reasoning;
- creates broad candidate lists with no decision value;
- systematically increases investigation on cheap reversible work;
- creates pseudo-ranking or hidden authority;
- obscures rather than clarifies the selected strategic decision.

## Positive signal

A meaningful positive signal is not “the planner generated more ideas.” It is evidence that the planner surfaced a material alternative, dependency, or uncertainty that changed or substantially improved the repository-level decision while keeping overhead proportional.
