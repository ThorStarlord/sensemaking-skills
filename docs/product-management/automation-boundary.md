# Product Management automation and authority boundary

## Automation levels

| Level | Name | Meaning |
|---|---|---|
| A1 | capability invocation | A compatible harness can expose and invoke a canonical PM capability. |
| A2 | artifact production | The capability returns its declared PM artifact. |
| A3 | mechanical validation | Deterministic validation checks representation/contract invariants. |
| A4 | Campaign integration | Validated exact bytes can be admitted, referenced, traced, and handed off. |
| A5 | bounded continuation | An explicitly authorized PM workflow envelope may continue while responsibility, evidence, and authority remain sufficient. |
| A6 | evidence acquisition | Authorized tools/connectors retrieve real repository/customer/market/analytics/experiment evidence. |
| A7 | external execution | The system changes an external state: customer contact, publication, pricing, launch, campaign, experiment, or other mutation. |

The Customer Discovery pilot targets A1-A5. A6 is incremental. A7 always remains an explicit external-action boundary.

## Workflow-envelope authority

A user instruction such as "run Customer Discovery end-to-end" may authorize the bounded responsibility sequence declared by the workflow. It does **not** authorize:

- unrelated adjacent analysis;
- changes to a target repository merely because analysis recommends them;
- customer outreach;
- experiment launch;
- price changes;
- publishing a release or GTM campaign;
- any capability outside the authorized scope.

## Mandatory stop/defer conditions

The active agent must stop, defer, or return for owner input when any of the following becomes consequential:

1. required evidence is absent and cannot be acquired within current authority;
2. owner intent is decision-blocking;
3. artifact validation fails;
4. Campaign integrity cannot be established;
5. scope expansion is required;
6. external action is required;
7. authority is insufficient;
8. material evidence conflicts with the assumption needed to continue;
9. the next responsibility cannot be warranted;
10. harness/adapter failure prevents trustworthy execution or invocation evidence.

## Anti-automation rules

Do not implement deterministic machinery that declares:

- the best persona;
- the most important opportunity;
- the correct product strategy;
- whether a hypothesis is likely to succeed;
- that PMF exists;
- that a launch should occur.

Mechanical machinery may verify that the representation needed to make those judgments is structurally present and traceable.
