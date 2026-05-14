# Unknowns Map (Scenario: False-Routing Product vs Repo)

## 1. Knowns
- The user has "lots of ideas" for AI products.
- The user intends to use this repository for product velocity.
- The user is currently confused about the repository's internal structure (workflows, artifacts, handoffs).

## 2. Unknowns
- **Primary Unknown**: Which specific workflow in `workflow-registry.yaml` is the correct starting point for the user's specific (yet unstated) ideas?
- **Capability Gap**: Does the user have the prerequisites (e.g., specific API keys or environment setup) for the workflows they might select?

## 3. Assumptions
- We assume that the user's "ideas" are actually buildable within the current framework of skills.
- We assume the user is looking for a structured pipeline rather than just a chatbot.

## 4. Risks
- **False Routing (Critical)**: Routing to a domain-specific skill (like `to-prd`) based on the "product" keyword before the "how to use this repo" problem is solved.
- **Cognitive Abandonment**: The user gives up because the "meta-skill" of using the repo is too high-friction.

## 5. Research Paths
- **Path 1: Workflow Audit**: Review `workflow-registry.yaml` to identify the "Cold Start" or "Entry Point" workflows (e.g., `guided-repo-sensemaking`).
- **Path 2: Intent Disambiguation**: Prompt the user to provide a single concrete example of an "idea" to perform a dry-run routing.

## 6. Stopping Rule
Stop when we have identified a specific workflow in `workflow-registry.yaml` that explicitly accepts "Raw Fog" as an input and produces a "Problem Frame" as an output, and verified its technical prerequisites.
