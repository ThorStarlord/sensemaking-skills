#!/usr/bin/env bash
# Configuration-only runner for #872 subject episodes under the #873 calibrated configuration.
# Usage: SCRATCH=<scratch dir outside the repo> bash run_child.sh <TASK D1|D2> <ARM treatment|baseline> <EPISODE label> <SNAPSHOT rev>
# Frozen for every arm: fresh session id, --safe-mode --restricted, tools Read,Grep,Glob, model, stream-json, budget cap, fresh empty cwd.
# The arms differ only by the knowledge directory (--add-dir) and one availability sentence (treatment).
set -u
TASK="$1"; ARM="$2"; EP="$3"; REV="$4"
EXP="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(git -C "$EXP" rev-parse --show-toplevel)"
: "${SCRATCH:?set SCRATCH to a scratch directory outside the repository}"
MODEL=claude-haiku-5-5
FX="$SCRATCH/fx/$TASK-$ARM-$EP"
rm -rf "$FX"; mkdir -p "$FX/cwd"

UNSET=""
for v in $(env | cut -d= -f1 | grep -E '^(CLAUDE|ANTHROPIC)' | grep -v -E '^ANTHROPIC_BASE_URL$'); do
  UNSET="$UNSET -u $v"
done

PROMPT="$(cat "$EXP/prompts/$TASK.txt")"
ADD=()
if [ "$ARM" = treatment ]; then
  mkdir -p "$FX/knowledge"
  mapfile -t PATHS < "$EXP/manifests/$TASK.txt"
  (cd "$REPO" && git archive "$REV" "${PATHS[@]}") | tar -x -C "$FX/knowledge"
  KNOW_WIN="$(cygpath -w "$FX/knowledge")"
  ADD=(--add-dir "$KNOW_WIN")
  PROMPT="$PROMPT

A reviewed knowledge store for this study is available as a read-only directory at $KNOW_WIN . Consult it if you judge it useful."
fi

SID="$(python -c 'import uuid;print(uuid.uuid4())')"
mkdir -p "$EXP/transcripts"
OUT="$EXP/transcripts/$TASK-$ARM-$EP.jsonl"
( cd "$FX/cwd" && timeout 420 env $UNSET claude -p --session-id "$SID" --safe-mode --restricted \
    --model "$MODEL" --output-format stream-json --verbose --max-budget-usd 0.40 \
    "$PROMPT" --tools "Read,Grep,Glob" --allowedTools "Read,Grep,Glob" "${ADD[@]}" ) > "$OUT" 2> "$OUT.err"
RC=$?
PSHA="$(sha256sum "$EXP/prompts/$TASK.txt" | cut -c1-12)"
echo "$TASK $ARM $EP snapshot=$(git -C "$REPO" rev-parse --short "$REV") sid=$SID exit=$RC prompt_sha=$PSHA" >> "$EXP/transcripts/index.txt"
echo "$TASK $ARM $EP sid=$SID exit=$RC"
