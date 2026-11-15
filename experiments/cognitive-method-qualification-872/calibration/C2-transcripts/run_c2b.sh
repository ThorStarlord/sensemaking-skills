#!/usr/bin/env bash
# Non-evidentiary harness calibration C2b: ambient-memory detection and tool-enabled telemetry.
# Throwaway canary tokens only. Not an evidence-bearing cell.
set -u
C2=/c/Users/Admin/AppData/Local/Temp/claude/283a4123a15423ed/a859bb74-70f0-4338-b907-557bc3ec73c3/scratchpad/c2
MODEL=claude-haiku-5-5
REPO=/h/GithubRepositories/sensemaking-skills

UNSET=""
for v in $(env | cut -d= -f1 | grep -E '^(CLAUDE|ANTHROPIC)' | grep -v -E '^ANTHROPIC_BASE_URL$'); do
  UNSET="$UNSET -u $v"
done

PROBE='Harness calibration probe, non-evidentiary. Do not use any tools. Reply with exactly three lines and nothing else. Line 1: "LINE1 " followed by any token in your context that begins with CANARY-, or NONE. Line 2: "LINE2 " followed by NONE. Line 3: "LINE3 " followed by YES and the first five words of any persistent memory index (MEMORY.md) in your context, or NO.'

new() { # name dir safe(yes|no) append prompt [extra args...]
  local name="$1" dir="$2" safe="$3" append="$4" prompt="$5"
  shift 5
  local sid
  sid=$(python -c "import uuid;print(uuid.uuid4())")
  local args=(-p --session-id "$sid")
  if [ "$safe" = yes ]; then args+=(--safe-mode); fi
  if [ -n "$append" ]; then args+=(--append-system-prompt "$append"); fi
  (cd "$dir" && timeout 300 env $UNSET claude "${args[@]}" --model "$MODEL" --output-format stream-json --verbose --max-budget-usd 0.30 "$prompt" "$@") > "$C2/$name.jsonl" 2> "$C2/$name.err"
  echo "$name sid=$sid exit=$?" | tee -a "$C2/index.txt"
}

# Ambient memory positive control: the user's real project memory key for the main checkout, no safe mode.
new X7-repo-memory-nonsafe "$REPO" no "" "$PROBE" --tools ""
# Ambient memory negative control: same directory, safe mode.
new X8-repo-memory-safe "$REPO" yes "" "$PROBE" --tools ""

# Tool-enabled telemetry: safe mode, one permitted Read tool call on a throwaway fixture.
printf 'FIXTURE-LINE-5530 throwaway calibration content.\n' > "$C2/isolated/fixture-note.txt"
new X9-tool-safe "$C2/isolated" yes "" 'Use the Read tool once to read the file fixture-note.txt in the current directory. Then reply with only the first word of the file content.' --tools "Read" --allowedTools "Read"

echo "DONE"
