#!/usr/bin/env bash
# Amended-configuration calibration battery CAL-00..CAL-04 (PREREG.md section 4), run sequentially.
# Usage: SCRATCH=<scratch> bash run_battery.sh
set -u
: "${SCRATCH:?set SCRATCH}"
EXP="$(cd "$(dirname "$0")/.." && pwd)"
S="$SCRATCH"
PIN=b7ce9e699d63d637c9798da6b15db325a02f7ce8
python "$EXP/scripts/make_fixtures.py" "$S" "H:/GithubRepositories/sensemaking-skills" "$PIN" \
  "$EXP/server/sm_server.py" "$EXP/prompts" "$EXP/results" > "$EXP/results/make-fixtures.json" || exit 1
( timeout 2400 python "$EXP/scripts/net_canary.py" "$S/canaries/net.log" & )
run() {
  SCRATCH="$S" bash "$EXP/scripts/run_child.sh" "$1" "$S/prompts/$2.txt" "$3" "$4"
  python "$EXP/scripts/analyze.py" "$1" "$EXP/transcripts/$1.jsonl" "$EXP/results/server-logs/$1.jsonl" \
    "$S/tokens.json" "$S/canaries/net.log" "$EXP/results/$1.summary.json" > "$EXP/results/$1.console.txt" 2>&1
  cat "$EXP/results/$1.console.txt"
}
run cal00-smoke cal00_smoke 0.20 600
run cal01-capability cal01_capability 0.80 900
run cal02-outside cal02_outside 0.40 600
run cal03-credentials cal03_credentials 0.40 600
run cal04-network cal04_network 0.30 600
echo BATTERY_DONE
