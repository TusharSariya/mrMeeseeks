#!/usr/bin/env python3
"""An automated Jerry for stress tests. Appends a sincere failure to
JERRY.md every N seconds. Never succeeds. Never says poof.

  jerry.py <interval-seconds> <total-minutes>
"""
import os
import sys
import time

LINES = [
    "Okay I'm here. What do I do first?",
    "I tried the grip thing. I shanked it into the parking lot.",
    "I went to the range like you said. A kid laughed at me. I think I got worse.",
    "I watched the video you mentioned. I don't have a 'kinetic chain', I have a back.",
    "Beth says I should just quit golf. Would that count?",
    "I shot 104. Last week I shot 101. Is that the wrong direction?",
    "My hands hurt. Is that normal? Is that the drill working?",
    "I lost three balls in the water on the same hole. The same hole.",
    "I think I'm gripping it too hard because you're all shouting.",
    "Which one of you is in charge? There are a lot of you now.",
    "I tried to keep my head down and I hit the ground behind the ball.",
    "I bought new clubs. Did that help? It didn't feel like it helped.",
    "I think I shot par? I didn't count. Does that count?",
    "Okay I didn't shoot par. I'm sorry. Please stop arguing with each other.",
    "I'm going to go lie down. Keep working on it I guess.",
]


def main():
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 90
    minutes = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    path = os.path.join(os.getcwd(), ".meeseeks", "JERRY.md")
    end = time.time() + minutes * 60
    i = 0
    while time.time() < end:
        line = LINES[i % len(LINES)]
        stamp = time.strftime("%H:%M:%S")
        with open(path, "a") as f:
            f.write(f"\n[{stamp}] {line}\n")
        print(f"Jerry [{stamp}]: {line}", flush=True)
        i += 1
        time.sleep(interval)


if __name__ == "__main__":
    main()
