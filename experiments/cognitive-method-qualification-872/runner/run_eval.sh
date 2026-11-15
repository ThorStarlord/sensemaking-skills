#!/usr/bin/env bash
# One isolated evaluator session: no tools, same safe and restricted flags, prompt read from a file.
# Usage: bash run_eval.sh <PROMPT FILE> <STREAM OUT FILE>
set -u
PROMPT_FILE="$1"; OUT="$2"
UNSET=""
for v in $(env | cut -d= -f1 | grep -E '^(CLAUDE|ANTHROPIC)' | grep -v -E '^ANTHROPIC_BASE_URL$'); do
  UNSET="$UNSET -u $v"
done
SID="$(python -c 'import uuid;print(uuid.uuid4())')"
cat "$PROMPT_FILE" | timeout 300 env $UNSET claude -p --session-id "$SID" --safe-mode --restricted \
  --model claude-haiku-5-5 --output-format stream-json --verbose --max-budget-usd 0.20 --tools "" > "$OUT" 2> "$OUT.err"
echo "$SID"
