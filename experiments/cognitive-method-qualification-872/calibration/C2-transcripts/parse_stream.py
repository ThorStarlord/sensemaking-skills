import json
import sys

path = sys.argv[1]
init = None
result = None
types = {}
tool_uses = []
assistant_texts = []
session_ids = set()

with open(path, encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        t = ev.get("type")
        types[t] = types.get(t, 0) + 1
        if ev.get("session_id"):
            session_ids.add(ev.get("session_id"))
        if t == "system" and ev.get("subtype") == "init":
            init = ev
        if t == "result":
            result = ev
        if t == "assistant":
            msg = ev.get("message", {})
            for block in msg.get("content", []) or []:
                if isinstance(block, dict):
                    if block.get("type") == "tool_use":
                        tool_uses.append(block.get("name"))
                    if block.get("type") == "text":
                        assistant_texts.append(block.get("text", ""))

print("event_types", types)
print("session_ids_seen", sorted(session_ids))
print("tool_uses", tool_uses)
if init:
    for k in ["session_id", "model", "cwd", "claude_code_version", "permissionMode", "output_style"]:
        print("init." + k, init.get(k))
    for k in ["tools", "slash_commands", "skills", "plugins", "mcp_servers", "agents", "memory_paths"]:
        if k in init:
            v = init[k]
            if isinstance(v, list):
                names = [(x.get("name") if isinstance(x, dict) else str(x)) for x in v]
                print("init." + k, len(v), names[:60])
            else:
                print("init." + k, v)
    print("init_keys", sorted(init.keys()))
else:
    print("NO_INIT_EVENT")
if result:
    print("result.subtype", result.get("subtype"), "is_error", result.get("is_error"), "num_turns", result.get("num_turns"), "cost_usd", result.get("total_cost_usd"))
    print("RESULT_TEXT:", (result.get("result") or "").replace("\n", " | "))
else:
    print("NO_RESULT_EVENT")
print("ASSISTANT_TEXT:", " | ".join(t.replace("\n", " / ") for t in assistant_texts)[:1500])
