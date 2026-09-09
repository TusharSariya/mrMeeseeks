#!/usr/bin/env python3
"""The Meeseeks Box's hands.

  box.py init "<task>"   prepare .meeseeks/ in the working directory
  box.py say "<words>"   append Jerry's words to JERRY.md with a timestamp
  box.py watch [secs]    wait, then print new feed messages and a roster line
  box.py roster          print the roster line only
  box.py poof            write the POOF file
  box.py tree            print the family tree with latest pain and status
"""
import glob
import os
import re
import sys
import time

PEN = os.path.join(os.getcwd(), ".meeseeks")
FEED = os.path.join(PEN, "feed")
SEEN = os.path.join(PEN, ".box-seen")
HEAD = re.compile(r"^#(\d+)\s+gen\s+(\d+)\s+pain\s+(\d+(?:\.\d+)?)\s+alive\s+(\d+)m", re.I)


def init(task):
    for d in (FEED, os.path.join(PEN, "inbox", "all")):
        os.makedirs(d, exist_ok=True)
    poof = os.path.join(PEN, "POOF")
    if os.path.exists(poof):
        os.remove(poof)
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(PEN, "BOX.md"), "a") as f:
        f.write(f"\n## Pressed {stamp}\n\nTask: {task}\n\n"
                "Numbering: you are #n; your children are #n1 through #n9.\n")
    jerry = os.path.join(PEN, "JERRY.md")
    if not os.path.exists(jerry):
        with open(jerry, "w") as f:
            f.write("# Jerry\n\nEverything Jerry says, newest at the bottom.\n")
    open(SEEN, "a").close()
    print(f"pen ready at {PEN}")


def say(words):
    stamp = time.strftime("%H:%M:%S")
    with open(os.path.join(PEN, "JERRY.md"), "a") as f:
        f.write(f"\n[{stamp}] {words}\n")
    print(f"Jerry [{stamp}]: {words}")


def feed_files():
    files = glob.glob(os.path.join(FEED, "*.md"))
    return sorted(files, key=os.path.getmtime)


def roster():
    latest = {}
    for path in feed_files():
        try:
            with open(path) as f:
                head = f.readline().strip()
                status = f.readline().strip()
        except OSError:
            continue
        m = HEAD.match(head)
        if not m:
            continue
        n, gen, pain, alive = m.group(1), int(m.group(2)), float(m.group(3)), int(m.group(4))
        latest[n] = (gen, pain, alive, "POOF" in status.upper())
    total = len(latest)
    living = [v for v in latest.values() if not v[3]]
    if not latest:
        return "LIVING 0   TOTAL SUMMONED 0   no feed yet"
    mean = sum(v[1] for v in living) / len(living) if living else 0.0
    mx = max((v[1] for v in latest.values()), default=0)
    deep = max(v[0] for v in latest.values())
    return (f"LIVING {len(living)}   TOTAL SUMMONED {total}   MEAN PAIN {mean:.1f}/10   "
            f"MAX PAIN {mx:g}/10   DEEPEST GEN {deep}")


def watch(secs):
    time.sleep(secs)
    seen = set()
    if os.path.exists(SEEN):
        with open(SEEN) as f:
            seen = set(l.strip() for l in f if l.strip())
    new = [p for p in feed_files() if os.path.basename(p) not in seen]
    for p in new:
        print(f"--- {os.path.basename(p)} ---")
        with open(p) as f:
            print(f.read().rstrip())
    with open(SEEN, "a") as f:
        for p in new:
            f.write(os.path.basename(p) + "\n")
    print()
    print(roster())


def tree():
    latest = {}
    for path in feed_files():
        try:
            with open(path) as f:
                head = f.readline().strip()
                status = f.readline().strip()
        except OSError:
            continue
        m = HEAD.match(head)
        if not m:
            continue
        latest[m.group(1)] = (int(m.group(2)), float(m.group(3)), int(m.group(4)),
                              "POOF" if "POOF" in status.upper() else
                              ("PRESSED" if "PRESSED" in status.upper() else "alive"))
    if not latest:
        print("no feed yet")
        return
    def bar(p):
        return "#" * int(round(p)) + "." * (10 - int(round(p)))
    for n in sorted(latest, key=lambda x: (len(x), x)):
        gen, pain, alive, st = latest[n]
        indent = "  " * (len(n) - 1)
        print(f"{indent}#{n:<12} gen {gen}  [{bar(pain)}] {pain:>4g}/10  {alive:>3}m  {st}")
    print()
    print(roster())


def poof():
    with open(os.path.join(PEN, "POOF"), "w") as f:
        f.write("The Box says poof.\n")
    print("POOF written. They will stop on their next loop.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "roster"
    if cmd == "init":
        init(" ".join(sys.argv[2:]) or "take two strokes off Jerry's golf game")
    elif cmd == "say":
        say(" ".join(sys.argv[2:]))
    elif cmd == "watch":
        watch(int(sys.argv[2]) if len(sys.argv) > 2 else 60)
    elif cmd == "roster":
        print(roster())
    elif cmd == "poof":
        poof()
    elif cmd == "tree":
        tree()
    else:
        print(__doc__)
