#!/usr/bin/env bash
# Blind evaluation: one fresh evaluator session per relabelled response. The evaluator sees the rubric and one response only.
# Usage: bash evaluate_blind.sh <TASK D1|D2> <BLIND DIR> <TAG>
set -u
TASK="$1"; BDIR="$2"; TAG="$3"
EXP="$(cd "$(dirname "$0")/.." && pwd)"
RUBRIC="$EXP/rubrics/$TASK-rubric.md"
mkdir -p "$EXP/transcripts"
for R in "$BDIR"/R*.txt; do
  L="$(basename "$R" .txt)"
  P="$BDIR/$L.prompt.txt"
  { cat "$RUBRIC"; printf '\n\nRESPONSE TO SCORE:\n<<<\n'; cat "$R"; printf '\n>>>\n'; } > "$P"
  SID="$(bash "$EXP/runner/run_eval.sh" "$P" "$EXP/transcripts/eval-$TAG-$TASK-$L.jsonl")"
  echo "eval $TAG $TASK $L sid=$SID" >> "$EXP/transcripts/index.txt"
  echo "eval $TAG $TASK $L sid=$SID"
done
