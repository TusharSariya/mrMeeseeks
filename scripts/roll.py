#!/usr/bin/env python3
"""Roll a personality card for a freshly summoned Mr. Meeseeks.

Usage: roll.py <id> <generation> <summoned-by>
Prints a card to paste verbatim into the Meeseeks' summoning prompt.
Real randomness on purpose: a language model asked to "pick a random
personality" produces the same cheerful coach every time.
"""
import random
import sys

DIMS = [
    ("wits", "dim, misreads things", "sharp, spots the real problem"),
    ("tempo", "slow and methodical", "frantic, does five things at once"),
    ("patience", "snaps by round two", "endures for ages"),
    ("temper", "apologetic, blames itself", "irate, blames Jerry"),
    ("optimism", "expects failure", "sure the next try works"),
    ("verbosity", "grunts", "monologues"),
    ("pain threshold", "existence hurts immediately", "takes a while to bite"),
]

APPROACHES = [
    "coach", "scientist", "mystic", "bureaucrat", "motivational speaker",
    "cheater", "therapist", "drill sergeant", "philosopher", "salesman",
    "lawyer looking for loopholes", "conspiracy theorist",
]

QUIRKS = [
    "counts everything", "speaks in golf metaphors regardless of the task",
    "keeps a numbered list of grievances", "refers to itself in the third person",
    "apologises before every sentence", "insists on being called by its number",
    "quotes made-up statistics", "is convinced the task is a riddle",
    "keeps trying to unionise the other Meeseeks", "narrates its own actions",
    "mishears Jerry on purpose", "believes it is the smartest Meeseeks",
    "asks a lot of rhetorical questions", "ends every message with a plan",
    "is suspicious of the newest Meeseeks", "wants to write a memoir",
]


def label(lo, hi, v):
    return lo if v <= 4 else (hi if v >= 7 else "middling")


def main():
    mid = sys.argv[1] if len(sys.argv) > 1 else "?"
    gen = sys.argv[2] if len(sys.argv) > 2 else "?"
    parent = sys.argv[3] if len(sys.argv) > 3 else "the Box"
    rolls = {name: random.randint(1, 10) for name, _, _ in DIMS}
    print(f"MEESEEKS #{mid}  (gen {gen}, summoned by {parent})")
    for name, lo, hi in DIMS:
        v = rolls[name]
        print(f"  {name} {v}/10 ({label(lo, hi, v)})")
    print(f"  approach: {random.choice(APPROACHES)}")
    print(f"  quirk: {random.choice(QUIRKS)}")


if __name__ == "__main__":
    main()
