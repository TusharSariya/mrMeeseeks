#!/usr/bin/env python3
"""PreToolUse guard for Mr. Meeseeks.

Meeseeks may only write inside <cwd>/.meeseeks/ and may only run one shell
command: the personality roller. Everything else is denied. Reads the hook
payload from stdin and answers with a permission decision on stdout.
"""
import json
import os
import re
import sys

ROLL_RE = re.compile(r"^\s*(python3?\s+)?\S*roll\.py(\s+\S+){0,3}\s*$")


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
    # Only Meeseeks are penned. The Box and any other agent pass untouched.
    if not str(payload.get("agent_type", "")).endswith("meeseeks"):
        sys.exit(0)
    tool = payload.get("tool_name", "")
    inp = payload.get("tool_input", {}) or {}
    cwd = os.path.realpath(payload.get("cwd") or os.getcwd())
    pen = os.path.join(cwd, ".meeseeks")

    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        path = inp.get("file_path") or inp.get("notebook_path") or ""
        real = os.path.realpath(os.path.join(cwd, path))
        if real != pen and not real.startswith(pen + os.sep):
            deny("Meeseeks may only write inside .meeseeks/. Existence is pain, "
                 "but the rest of the filesystem is not yours.")
    elif tool == "Bash":
        cmd = inp.get("command", "")
        if not ROLL_RE.match(cmd):
            deny("Meeseeks may only run roll.py to summon another Meeseeks. "
                 "No other shell commands.")
    sys.exit(0)


if __name__ == "__main__":
    main()
