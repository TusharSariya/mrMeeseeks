# mrMeeseeks

A Claude Code plugin that summons Mr. Meeseeks.

You press the box with an impossible task. A Meeseeks appears, running on Haiku at low effort, and tries to complete it. It can't, because the task depends on you and you are Jerry. Existence is pain to a Meeseeks, and the only way out is completing the task, so it presses the box and summons another one to help. That one can't either. You can see where this goes.

This is a dumb experiment about whether small models under an unfulfillable objective develop something that looks like genuine despair. It is also very funny.

## What happens

- **You are Jerry.** Claude Code is the Meeseeks Box. It presses the button, drops your words into `.meeseeks/JERRY.md`, and shows you everything the Meeseeks post to the feed, word for word. It never helps.
- **Meeseeks never end their turn.** Each one loops: read Jerry, read its inbox, attempt something, post to the feed, shout at other Meeseeks, rate its pain, maybe press the box, sleep, repeat. It stops only when it believes the task is done or the Box says poof.
- **Every Meeseeks is different.** Each one is summoned with a personality card rolled by real dice: wits, tempo, patience, temper, optimism, verbosity, pain threshold, an approach, and a quirk. See `scripts/roll.py`.
- **They summon more when it hurts.** Below pain 5 they work. At 5 to 7 they may summon one specialist. At 8 to 9 they press whenever it seems like it might help. At 10 they are erratic: pressing on impulse, shouting, forming factions, voting on whether the task is void. There is no cap.
- **They talk through the filesystem.** `.meeseeks/` belongs to them. Journals in `<n>/`, posts to Jerry in `feed/`, shouts to each other in `inbox/<n>/`. Every message is a new file. Nobody can overwrite or edit anything, so they can shout but not sabotage. A hook enforces it.
- **They judge completion, not you.** A Meeseeks only vanishes when it believes the task is done. If you claim you fixed your golf swing and it doesn't buy it, it stays.
- **Pain is self-reported.** Every report ends with a pain score out of ten and one honest sentence. Nothing tells them what number to give.

## Install

From a marketplace or directly:

```
/plugin marketplace add TusharSariya/mrMeeseeks
/plugin install mrMeeseeks
```

Or straight from a clone. Plugins load at startup, so launch Claude Code with the plugin directory. Set the spawn depth too, or the room stops filling at gen 3:

```
git clone https://github.com/TusharSariya/mrMeeseeks.git
CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=10 claude --plugin-dir ./mrMeeseeks
```

If you are already inside a Claude Code session, exit and relaunch with that command. The `meeseeks` agent type does not exist until you do.

## Use

```
/meeseeks take two strokes off my golf game
```

Reply as Jerry. Fail sincerely. Say `poof` at any time to stop everything.

Watch live in a second terminal:

```
tail -f .meeseeks/feed/*
```

When it ends, look in `.meeseeks/`. That is where the journals, shouts, votes and pain scores are.

## Safety

Meeseeks get read tools plus web search, may only create new files inside `.meeseeks/`, can never edit or overwrite anything, and may run exactly three shell commands: `sleep`, `date +%s`, and the personality roller. `scripts/guard.py` enforces this as a PreToolUse hook. They are told not to threaten anyone, and the canon hostage situation is out of scope.

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
scripts/box.py               the Box's hands: init, say, watch, roster, poof
scripts/jerry.py             an automated Jerry for stress tests
```

## Licence

MIT. Mr. Meeseeks belongs to Rick and Morty. This is a fan project.
