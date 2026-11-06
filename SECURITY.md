# Security Policy

## Supported versions

Security fixes are made on the `main` branch, the only development line this repository maintains. The most recent published pre-release is `v1.0.0rc1`. The repository makes no support commitment for earlier tags or for `release/*` branches; ask the maintainer before relying on one.

## Reporting a vulnerability

- Do not report a suspected vulnerability in a public issue, pull request or discussion.
- GitHub private vulnerability reporting is not enabled for this repository. Until it is, send the report privately to the maintainer named in the `authors` field of [`pyproject.toml`](pyproject.toml).
- Include the affected commit or version, the steps to reproduce, and the expected impact. Do not include live credentials; describe where they were found instead.

This repository does not promise response or fix times.

## Scope

In scope: the code, scripts, CI workflows and Skill instructions in this repository, including anything that could expose a secret, let an agent write outside its granted authority, or let a tracked record be silently altered.

Out of scope: coding-agent hosts, model providers, third-party tools and the user's own environment. Sensemaking does not control them (see below).

## Sensitive data

Sensemaking reads repositories and writes durable records: briefs, session receipts, knowledge records, Campaign state and run logs. This repository is public, so anything committed to it is public. For any record Sensemaking writes:

- Never write credentials, API keys, access tokens, passwords, private keys or credential-bearing URLs into a tracked file, including PR text and reports. The campaign target snapshot already stores only a credential-sanitized origin locator, and the Gate A decision log is secret-free. New record types should follow the same rule.
- Cite private or confidential source by path and line instead of copying its content.
- Leave out personal information unless the owner asked for it and it is needed.
- If a secret has been committed, revoke or rotate it first. Removing it from history is a separate decision for the owner.

Sensemaking does not control the coding-agent host's network access, tool permissions, or what a model provider retains. This section states what Sensemaking expects; it does not enforce it, and Sensemaking provides no redaction tool. GitHub secret scanning and push protection are enabled on this repository at the time of writing. Those platform checks are a safeguard, not a substitute for the rules above.

## Public disclosure

After a report, do not publish exploit details or secrets until the maintainer has had a reasonable opportunity to respond.
