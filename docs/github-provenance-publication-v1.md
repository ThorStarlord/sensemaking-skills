# GitHub Campaign Provenance Publication v1

**Status:** post-RC2 development contract  
**Default:** preview only  
**Mutation authority:** explicit caller transition only

## Purpose

Sensemaking already renders deterministic local Campaign provenance. This
surface lets an operator explicitly publish that exact projection as a GitHub
Issue/PR comment without turning publication into a default side effect.

```text
generate provenance != publish provenance
publish provenance != authorize work
mechanical provenance != semantic correctness
```

## Preview

Preview is the default and performs no network mutation:

```bash
sensemaking-skills campaign provenance-publish \
  --workspace /path/to/CMP-1 \
  --repository OWNER/REPO \
  --issue-number 123 \
  --json
```

The projection contains:

- exact destination repository and issue/PR number;
- deterministic provenance body;
- a deterministic body SHA-256;
- a marker binding Campaign ID and body digest;
- `published: false`;
- `authorization_explicit: false`.

## Explicit publication

Publication requires `--publish` and a token available from an explicitly
named environment variable:

```bash
sensemaking-skills campaign provenance-publish \
  --workspace /path/to/CMP-1 \
  --repository OWNER/REPO \
  --issue-number 123 \
  --publish \
  --token-env GITHUB_TOKEN \
  --json
```

The token value is never rendered into output.

The publisher first reads up to 100 existing comments and searches for the exact
provenance marker. If present, it returns the existing comment rather than
posting a duplicate. Otherwise it posts one issue comment through the GitHub
Issue Comments API, which also supports pull requests.

## Authority boundary

The command requires the destination and publication transition from the
caller. It does not:

- select a repository;
- select an issue/PR;
- infer permission from Campaign authority metadata;
- merge or modify code;
- publish execution handoffs automatically;
- promote provenance into semantic truth.

```text
--publish supplied = explicit mutation request
!= evidence that the published reasoning is semantically correct
```

Network access remains optional. Normal Sensemaking operation remains
local-first.
