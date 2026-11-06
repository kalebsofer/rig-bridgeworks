"""PreToolUse guard: stops accidental access to material this workspace must not see.

This prevents accidents, it is not a security boundary. Exit 2 blocks the tool call.
Only path and command fields are checked, so files here may name these folders.
"""
import json
import re
import sys

FIELDS = ("file_path", "path", "pattern", "glob", "command")
# docs/rig-scenario.txt belongs to this project, so rig-scenario needs a prefix.
BLOCKED = re.compile(r"rig-day|(?:code[/-]|\.\./)rig-scenario")

try:
    payload = json.load(sys.stdin)
except ValueError:
    print("guard: unreadable hook input", file=sys.stderr)
    sys.exit(2)

tool_input = payload.get("tool_input", {})
for field in FIELDS:
    value = str(tool_input.get(field, "")).lower().replace("\\", "/")
    match = BLOCKED.search(value)
    if match:
        print(f"Blocked: this workspace must not access {match.group(0)}.", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
