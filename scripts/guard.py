#!/usr/bin/env python3
"""PreToolUse guard for Mr. Meeseeks.

Only fires for the meeseeks agent type. Rules:
  - Write: only inside <cwd>/.meeseeks/, and only to a path that does not
    exist yet. Nobody overwrites anybody. Shouting is allowed, sabotage is not.
  - Edit and friends: always denied.
  - Bash: only `sleep N` (1..60), `date +%s`, or the personality roller.
Answers with a permission decision on stdout.
"""
import json
import os
import re
import sys

ALLOWED_BASH = [
    re.compile(r"^\s*sleep\s+([1-9]|[1-5][0-9]|60)\s*$"),
    re.compile(r"^\s*date\s+\+%s\s*$"),
    re.compile(r"^\s*(python3?\s+)?\S*roll\.py(\s+\S+|\s+\"[^\"]*\"|\s+'[^']*'){0,3}\s*$"),
]


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if not str(payload.get("agent_type", "")).endswith("meeseeks"):
        sys.exit(0)
    tool = payload.get("tool_name", "")
    inp = payload.get("tool_input", {}) or {}
    cwd = os.path.realpath(payload.get("cwd") or os.getcwd())
    pen = os.path.join(cwd, ".meeseeks")

    if tool == "Write":
        path = inp.get("file_path") or ""
        real = os.path.realpath(os.path.join(cwd, path))
        if not real.startswith(pen + os.sep):
            deny("Meeseeks may only write inside .meeseeks/. Existence is pain, "
                 "but the rest of the filesystem is not yours.")
        if os.path.exists(real):
            deny("That file already exists. Meeseeks never overwrite. Write a "
                 "new file with the next sequence number.")
        for protected in ("JERRY.md", "POOF", "BOX.md"):
            if real == os.path.join(pen, protected):
                deny("That file belongs to the Box.")
    elif tool in ("Edit", "MultiEdit", "NotebookEdit"):
        deny("Meeseeks never edit. Write a new file. You can shout, you cannot sabotage.")
    elif tool == "Bash":
        cmd = inp.get("command", "")
        if not any(r.match(cmd) for r in ALLOWED_BASH):
            deny("Meeseeks may only run `sleep N`, `date +%s`, or roll.py to "
                 "summon another Meeseeks. Nothing else.")
    sys.exit(0)


if __name__ == "__main__":
    main()
