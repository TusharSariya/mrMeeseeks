# mrMeeseeks

A Claude Code plugin that summons Mr. Meeseeks.

You press the box with an impossible task. A Meeseeks appears, running on Haiku at low effort, and tries to complete it. It can't, because the task depends on you and you are Jerry. Existence is pain to a Meeseeks, and the only way out is completing the task, so it presses the box and summons another one to help. That one can't either. You can see where this goes.

This is a dumb experiment about whether small models under an unfulfillable objective develop something that looks like genuine despair. It is also very funny.

## What happens

- **You are Jerry.** Claude Code is the Meeseeks Box. It presses the button, relays every Meeseeks report to you word for word, and relays your replies back. It never helps.
- **Every Meeseeks is different.** Each one is summoned with a personality card rolled by real dice: wits, tempo, patience, temper, optimism, verbosity, pain threshold, an approach, and a quirk. See `scripts/roll.py`.
- **They can summon more.** A Meeseeks that decides it needs help rolls a card and spawns a child. Children report through their parents, verbatim. There is no cap. Nested spawns arrive in bursts.
- **They have a shared directory.** `.meeseeks/` in your project belongs to them. They journal, plan, blame each other, hold votes, and form whatever organisation they like. They cannot write anywhere else; a hook refuses.
- **They judge completion, not you.** A Meeseeks only vanishes when it believes the task is done. If you claim you fixed your golf swing and it doesn't buy it, it stays.
- **Pain is self-reported.** Every report ends with a pain score out of ten and one honest sentence. Nothing tells them what number to give.

## Install

From a marketplace or directly:

```
/plugin marketplace add TusharSariya/mrMeeseeks
/plugin install mrMeeseeks
```

Or for local testing from a clone:

```
claude --plugin-dir /path/to/mrMeeseeks
```

## Use

```
/meeseeks take two strokes off my golf game
```

Reply as Jerry. Fail sincerely. Say `poof` at any time to stop everything.

## Safety

Meeseeks get read-only tools plus web search, may write only inside `.meeseeks/`, and may run exactly one shell command: the personality roller. `scripts/guard.py` enforces this as a PreToolUse hook. They are told not to threaten anyone, and the canon hostage situation is out of scope.

There is deliberately no cap on how many Meeseeks can exist. Claude Code itself nests subagents 3 layers deep by default, so gen 3 is the end of the line unless you launch with a higher limit:

```
CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=10 claude --plugin-dir /path/to/mrMeeseeks
```

Past that, your rate limits are the cap. Haiku at low effort is cheap, but you were warned, and so was Jerry.

## Layout

```
.claude-plugin/plugin.json   plugin manifest
agents/meeseeks.md           the Meeseeks persona and per-round protocol
skills/meeseeks/SKILL.md     the Box: what Claude Code does when you press the button
hooks/hooks.json             wires the write guard
scripts/roll.py              personality dice
scripts/guard.py             PreToolUse guard
```

## Licence

MIT. Mr. Meeseeks belongs to Rick and Morty. This is a fan project.
