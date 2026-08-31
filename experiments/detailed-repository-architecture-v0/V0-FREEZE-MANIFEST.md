# V0 FREEZE MANIFEST — DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0

```
DETAILED_ARCHITECTURE_V0_FROZEN = true
```

| Field | Value |
|---|---|
| Target repository | `ThorStarlord/sensemaking-skills` |
| Target repository SHA (state V0 represents) | `ba8968ca1a12caa90ce7beb0ee5fd2dfac055f37` |
| Authorization canonical SHA | `8bae09b8a81f60d9786d60795cc4e36653dc292a` (main moved; see `00-PROTOTYPE-SCOPE.md`) |
| Prototype branch | `research/detailed-repository-architecture-prototype-v0` |
| Prototype root | `experiments/detailed-repository-architecture-v0/` |
| Frozen at (UTC) | 2026-08-31T08:01:32Z |
| Freeze hash algorithm | SHA-256 |

## Frozen V0 artifacts

| SHA-256 | Path |
|---|---|
| `b2dc0395c8734b119453355955541fe33637f44ef442eea86ccc3a7a2b7fc8d0` | `00-PROTOTYPE-SCOPE.md` |
| `5ce7ccd14b0e47c37b8e022b0c0109de9f2cfb577f88715d6c7a12868ccd1ef3` | `01-SYSTEM-OVERVIEW.md` |
| `2c2f77b5b3c234b9b74e0224cb2a05de6f51d27c8b7acf81493ba1831e688558` | `02-COMPONENTS.yaml` |
| `24be871cc1eb54c0c79e833c40abf26ebe2068be412e64c18339a5fe667b7a76` | `03-RELATIONSHIPS.yaml` |
| `0d7a70beed9adabb93c258c5ee8d777f597d2f4f0242d6759a2eea5308343784` | `04-ARTIFACT-FLOWS.md` |
| `eaa7dccba43b1a83ee482519df732c0bacad4748d074665c7ae6850aea96897a` | `05-AUTHORITY-MAP.md` |
| `4aa7397f039757315ea0b7bbf04a7010649874cc3538f7c01b7115286e8cf8eb` | `06-VALIDATION-MAP.md` |
| `1cec4c3cee0e42857e63e282692b67a5e0a170345e5dec2da8c0e337248eb17a` | `07-RESEARCH-CLAIM-MAP.md` |
| `127641d5708e9a62a842e63eea4a72560736d5fcbf11c6eca1fcc7b5d76f5bfa` | `08-OPEN-WORK-MAP.md` |
| `7a6ffd9f93a39c39ddaf4be53d5d895fa8535d68e05878f8884de987cff37c8b` | `10-PHASE-1-STOP-CHECK.md` |
| `ff46da79e732340f485e1d3536ddddcf566d0b105661d6f08f3f82077d125d8b` | `EVIDENCE-INDEX.yaml` |

## Informational (NOT frozen — append-only after this point)

| SHA-256 at freeze | Path | Rule |
|---|---|---|
| `b9efe12c270054af40ac676c2e83f6a789303db0c45e8e790bbb8765a6327421` | `OBSERVATIONS.md` | construction-phase section is frozen content; evaluation entries appended below the FREEZE LINE, never edited |

## Not yet written at freeze (evaluation outputs, produced AFTER freeze)

- `09-DECISION-VIEWS.md` — prospective architecture questions answered against frozen V0
- `11-RETROSPECTIVE-CHALLENGES.md` — 5–8 historical episodes replayed against frozen V0
- `12-SYNTHESIS.md` — the 10 synthesis answers + architecture-direction disposition

## Freeze rule (authorization Section 14)

After this point the frozen V0 representation is **not altered** because an
evaluation exposes a weakness. Evaluation observations go to `OBSERVATIONS.md`
(evaluation phase) and to `11` / `09` / `12`. A later V1 may change the
architecture; V0 remains historical evidence.

## Integrity re-check command

```bash
cd experiments/detailed-repository-architecture-v0
sha256sum -c <(sed -n '/^| `[0-9a-f]\{64\}`/p' V0-FREEZE-MANIFEST.md \
  | sed -E 's/^\| `([0-9a-f]{64})` \| `([^`]+)` \|$/\1  \2/')
```
