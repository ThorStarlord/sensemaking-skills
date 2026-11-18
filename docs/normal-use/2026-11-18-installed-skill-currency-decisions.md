# Installed Skill currency and related decisions (2026-11-18)

**Status:** operator record of one host's installed Sensemaking Skills, plus three decisions made under the owner's delegation on 2026-11-18. It changes no product behavior, authority, schema or qualification record.

**Source boundary:** `origin/main` at `573c8c90`. Checks were byte-level Git blob and tree-digest comparisons, and one dry run and one real run of the packaged installer. No unit or synthetic evidence tests were run, under the construction policy in CLAUDE.md.

## 1. What the host was loading

The user-level copy at `~/.claude/skills/using-sensemaking` was written on 2026-11-16 15:27Z by `setup-skills` from a source checkout (package `1.0.0rc5.dev0`). Its tree digest (`f4c2327e…`) matches the install record, so the copy had not changed since installation.

It is not a committed version. Its digest matches none of the 226 commits that touch `skills/using-sensemaking` on any ref. It was therefore installed from an uncommitted source tree. The install record stores a tree digest and a source kind, but no source commit, so the revision cannot be recovered from the record. Agents on this host were loading that copy until this update.

## 2. Remedy applied

1. **Backup.** The whole `~/.claude/skills` folder (7,801 files) was copied to `H:\GithubRepositories\smk-909-scratch\backup-claude-skills-20261118` before any write.
2. **Recorded copies.** `setup-skills --target claude --scope user --profile entrypoint --update` replaced 18 copies. The installer reported each as unchanged since its record, so the update was safe.
3. **Unrecorded divergent copy.** `strategic-repository-analysis` had no install record and differed from the packaged tree. It had a flat layout, a nested duplicate folder, and 13 of its reference files missing. The installer refused to overwrite it, as designed. After inspecting the target, I replaced it with `--force`. Its SKILL.md name and description match the source. The backup retains the original.
4. **Verification.** A dry run of the same profile now reports all 19 entrypoint Skills as `Current (already matches packaged version)`. The installed `using-sensemaking/SKILL.md` blob is `685268b5…`, identical to `origin/main`.

**Not touched:** `~/.agents/skills/using-sensemaking`. It has no install record from this installer, and its content differs from the packaged tree. Whether any harness loads it is unknown, so it needs an owner decision.

## 3. Calibration limit (decision: no edit)

The admitted `sm-readonly-A` record (`experiments/execution-environment-calibration/CALIBRATION-RESULT.md`) says the CLI's git calls at `knowledge_sources.py` lines 42, 75 and 78 lack `-c` neutralization. That statement is accurate for its pinned revision `b7ce9e69`, which has no `core.fsmonitor=false` on those calls. The guard was added later by commit `5af0a288` on 2026-11-16 at 03:59 -0300. The record is pinned, so it is not edited. Current `origin/main` carries the guard. Hook and filter coverage for those calls is unchanged from the record.

## 4. Span-level staleness (decision: defer)

Knowledge citations name whole files, so one edit flags every record that cites that file. A 2026-10-21 incident recorded 19 records flagged by one edit to a shared pack. Per-record classification already exists from PR #561. Per-line or span-level flags would need line-span citations, which is a schema change across every claim in the store.

No consequential decision is recorded as misled by a whole-file flag. Under the bounded-increment rule, the schema change is not warranted now. Revisit when a consequential decision is misled by a staleness flag, or when the owner authorizes a schema change.

## 5. Gap found, not implemented

The install record does not store a source commit. Adding one, when `setup-skills` runs from a Git checkout, would make the currency question answerable from the record. It is a small follow-up and is not part of this record.

## Claim ceiling

This record shows the state of one host's copies after one update. It does not show which Skill text any harness loaded during a session, and it does not show improved agent judgment.
