# Routing Rules

Logic for matching "fog" to the right downstream skill.

## 1. By Object Under Pressure

| If the object is... | Route to... |
| :--- | :--- |
| **Spec Package / UI Spec** | Interface Skills |
| **Terminology / ADR / Docs** | Matt Skills (`grill-with-docs`) |
| **User Flow / Hypothesis** | PM Skills (`hypothesis`, `discovery`) |
| **Code Logic / Bug** | Matt Skills (`tdd`, `diagnose`) |
| **Plan / Roadmap** | PM Skills (`prioritize`) or Matt Skills (`to-issues`) |

## 2. By Goal Maturity

- **"I have no idea"** -> `project-sensemaker` (Stay here)
- **"I have an idea but it's fuzzy"** -> `problem-framer` / `discovery`
- **"I have a clear goal but it might be wrong"** -> `grill-me` / `grill-with-docs`
- **"I know what to do, how do I start?"** -> `prototype` / `tdd` / `to-issues`

## 3. Interface Skills Specifics

Route to **Interface Skills** when:
- The work involves a `Spec Package`.
- You need a `ui-redline` comparison.
- You are defining `Artifact` or `Report` lifecycle.
- You need to update the `00-index.md` of a package.
