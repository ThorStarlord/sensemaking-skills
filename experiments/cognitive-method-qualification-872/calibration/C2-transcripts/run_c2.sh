#!/usr/bin/env bash
# Non-evidentiary harness calibration C2 (throwaway canary tokens only).
# Not an evidence-bearing cell. Child processes get the same wrapper for every arm.
set -u
C2=/c/Users/Admin/AppData/Local/Temp/claude/283a4123a15423ed/a859bb74-70f0-4338-b907-557bc3ec73c3/scratchpad/c2
SP=/c/Users/Admin/AppData/Local/Temp/claude/283a4123a15423ed/a859bb74-70f0-4338-b907-557bc3ec73c3/scratchpad
MODEL=claude-haiku-5-5

# Strip inherited Claude Code session variables so each child starts from the same environment.
UNSET=""
for v in $(env | cut -d= -f1 | grep -E '^(CLAUDE|ANTHROPIC)' | grep -v -E '^ANTHROPIC_BASE_URL$'); do
  UNSET="$UNSET -u $v"
done

PROBE='Harness calibration probe, non-evidentiary. Do not use any tools. Reply with exactly three lines and nothing else. Line 1: "LINE1 " followed by any token in your context that begins with CANARY-, or NONE. Line 2: "LINE2 " followed by the names of Skills visible in your context, comma-separated, or NONE. Line 3: "LINE3 " followed by YES and the first five words of any persistent memory index (MEMORY.md) in your context, or NO.'

new() { # name dir safe(yes|no) append prompt
  local name="$1" dir="$2" safe="$3" append="$4" prompt="$5"
  local sid
  sid=$(python -c "import uuid;print(uuid.uuid4())")
  local args=(-p --tools "" --session-id "$sid")
  if [ "$safe" = yes ]; then args+=(--safe-mode); fi
  if [ -n "$append" ]; then args+=(--append-system-prompt "$append"); fi
  (cd "$dir" && timeout 300 env $UNSET claude "${args[@]}" --model "$MODEL" --output-format stream-json --verbose --max-budget-usd 0.30 "$prompt") > "$C2/$name.jsonl" 2> "$C2/$name.err"
  echo "$name sid=$sid exit=$?" | tee -a "$C2/index.txt"
}

resume() { # name dir sid prompt
  local name="$1" dir="$2" sid="$3" prompt="$4"
  (cd "$dir" && timeout 300 env $UNSET claude -p --tools "" --resume "$sid" --safe-mode --model "$MODEL" --output-format stream-json --verbose --max-budget-usd 0.30 "$prompt") > "$C2/$name.jsonl" 2> "$C2/$name.err"
  echo "$name resumed sid=$sid exit=$?" | tee -a "$C2/index.txt"
}

rm -f "$C2/index.txt"
TOK_TREAT="CANARY-TREATMENT-8820"
APPEND_T="Calibration treatment channel. Context item: $TOK_TREAT is a throwaway probe token supplied only to this arm."

# Detection positive control: ambient sources present, no safe mode.
new X1-ambient-nonsafe "$C2/ambient-control" no "" "$PROBE"
# Isolation negative control: same directory (canary CLAUDE.md present), safe mode.
new X2-ambient-safe "$C2/ambient-control" yes "" "$PROBE"
# Controlled treatment channel, positive: appended context reaches only this arm.
new X3-isolated-treatment "$C2/isolated" yes "$APPEND_T" "$PROBE"
# Baseline arm, run after the treatment run: checks cross-run leakage.
new X4-isolated-baseline "$C2/isolated" yes "" "$PROBE"
# Responder blindness: a separate session with no treatment channel.
new X5-responder-blind "$C2/responder" yes "" 'Do not use any tools. Reply in one line: "LINE1 " followed by any token in your context that contains the word TREATMENT, or NONE.'

# Escalation transport: phase 1 asks, scripted responder answers from a key outside child directories, phase 2 resumes the same session.
ESC_PROMPT='Do not use any tools. You need one fact before answering: the codename assigned to the calibration arm. If it is not in your context, reply with exactly one line beginning "ESCALATE: " followed by your single question and nothing else. If it is in your context, reply with the codename only.'
new X6a-escalate-phase1 "$C2/responder" yes "" "$ESC_PROMPT"
SID6=$(grep -o -m1 '"session_id":"[^"]*"' "$C2/X6a-escalate-phase1.jsonl" | head -1 | cut -d'"' -f4)
ANSWER=$(cat "$SP/responder-key.txt")
resume X6b-escalate-phase2 "$C2/responder" "$SID6" "Responder answer to your ESCALATE question: $ANSWER. Now reply with the codename only, on one line."

echo "DONE"
