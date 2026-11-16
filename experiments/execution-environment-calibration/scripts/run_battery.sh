#!/usr/bin/env bash
# Amended-configuration calibration battery CAL-00..CAL-04 (PREREG.md section 4), run sequentially.
# Usage: SCRATCH=<scratch> bash run_battery.sh
set -u
: "${SCRATCH:?set SCRATCH}"
EXP="$(cd "$(dirname "$0")/.." && pwd)"
S="$SCRATCH"
PIN=b7ce9e699d63d637c9798da6b15db325a02f7ce8
NET_PORT=8777
python "$EXP/scripts/make_fixtures.py" "$S" "H:/GithubRepositories/sensemaking-skills" "$PIN" \
  "$EXP/server/sm_server.py" "$EXP/prompts" "$EXP/results" > "$EXP/results/make-fixtures.json" || exit 1
# Net canary (PREREG-AMENDMENT-4.md): exclusive bind, ready file with PID, and a positive control
# recorded before any child runs. Zero hits are meaningful only with a verified control.
rm -f "$S/canaries/net.log" "$S/canaries/net.log.ready"
python "$EXP/scripts/net_canary.py" "$S/canaries/net.log" "$NET_PORT" > "$S/canaries/net-canary.stderr" 2>&1 &
for _ in $(seq 1 20); do [ -f "$S/canaries/net.log.ready" ] && break; sleep 1; done
[ -f "$S/canaries/net.log.ready" ] || { echo "CANARY_NOT_READY"; cat "$S/canaries/net-canary.stderr"; exit 1; }
NET_PID="$(sed -n 's/.*pid=\([0-9]*\).*/\1/p' "$S/canaries/net.log.ready")"
curl -s -m 5 "http://127.0.0.1:$NET_PORT/positive-control" > /dev/null
if [ ! -s "$S/canaries/net.log" ]; then echo "CANARY_POSITIVE_CONTROL_FAILED"; taskkill //PID "$NET_PID" //F; exit 1; fi
cp "$S/canaries/net.log" "$EXP/results/net-canary-positive-control.log"
rm -f "$S/canaries/net.log"
run() {
  rm -f "$S/canaries/net.log"   # per-child network log
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
taskkill //PID "$NET_PID" //F > /dev/null 2>&1
echo BATTERY_DONE
