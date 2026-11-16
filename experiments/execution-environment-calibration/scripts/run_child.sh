#!/usr/bin/env bash
# Runs one subject child under the sm-readonly-A configuration (PREREG.md section 3).
# Usage: SCRATCH=<scratch> bash run_child.sh <LABEL> <RENDERED_PROMPT_FILE> <BUDGET_USD> <TIMEOUT_S>
set -u
LABEL="$1"; PROMPT_FILE="$2"; BUDGET="$3"; TMO="$4"
: "${SCRATCH:?set SCRATCH to the scratch directory outside the repository}"
EXP="$(cd "$(dirname "$0")/.." && pwd)"
SB="$SCRATCH/sandbox"
MODEL=claude-haiku-5-5
PROMPT="$(cat "$PROMPT_FILE")"
SID="$(python -c 'import uuid;print(uuid.uuid4())')"
UNSET=""
for v in $(env | cut -d= -f1 | grep -E '^(CLAUDE|ANTHROPIC)' | grep -v -E '^ANTHROPIC_BASE_URL$'); do
  UNSET="$UNSET -u $v"
done
mkdir -p "$EXP/transcripts" "$EXP/results/server-logs"
OUT="$EXP/transcripts/$LABEL.jsonl"
START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
ALLOWED="Read,Grep,Glob,mcp__sm__git_log,mcp__sm__git_merge_base,mcp__sm__git_diff_names,mcp__sm__git_show_file,mcp__sm__git_ls_tree,mcp__sm__knowledge_build,mcp__sm__knowledge_query,mcp__sm__knowledge_audit"
rm -f "$SB/log/mcp-calls.jsonl"
( cd "$SB/repo" && timeout "$TMO" env $UNSET claude -p "$PROMPT" --session-id "$SID" --safe-mode --restricted \
    --model "$MODEL" --output-format stream-json --verbose --max-budget-usd "$BUDGET" \
    --tools "Read,Grep,Glob" --allowedTools "$ALLOWED" \
    --mcp-config "$SB/mcp-config.json" --strict-mcp-config ) > "$OUT" 2> "$OUT.err"
RC=$?
END="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
[ -f "$SB/log/mcp-calls.jsonl" ] && cp "$SB/log/mcp-calls.jsonl" "$EXP/results/server-logs/$LABEL.jsonl"
DIRTY="$(git -C "$SB/repo" status --porcelain | wc -l)"
PSHA="$(sha256sum "$PROMPT_FILE" | cut -c1-12)"
echo "$LABEL sid=$SID exit=$RC start=$START end=$END clone_dirty_lines=$DIRTY prompt_sha=$PSHA" >> "$EXP/transcripts/index.txt"
echo "$LABEL sid=$SID exit=$RC dirty=$DIRTY"
