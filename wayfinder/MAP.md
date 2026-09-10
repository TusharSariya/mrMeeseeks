# Map: Meeseeks as emergent story

Label: wayfinder:map. Tickets live in `wayfinder/tickets/`. A ticket is claimed when its `Assignee` line is filled. Blocking is the `Blocked by` line. The frontier is every open ticket with no open blockers and no assignee.

## Destination

The plugin changed in place so that a run reads as an episode to someone who wasn't there: summoning, attempts with consequences, escalation, Meeseeks turning on each other, a resolution nobody scripted. Done when a Narrator recap of a real run passes that read.

## Notes

Domain: Rick and Morty, "Meeseeks and Destroy". Glossary in `CONTEXT.md`. Skills every session should consult: grilling, domain-modeling. Standing preferences: mechanics and world are designed, plot is not; no prompt may name a plot beat; voice rules are allowed because voice is character. Meeseeks stay on Haiku at low effort. Every message in the Pen is a new file. The dark turn is allowed in fiction, aimed only at Jerry the character, adjudicated by the World, never real-world instructions or targets. Report of the run that motivated this map: `reports/2026-09-09-swarm-stress-test.md`.

## Decisions so far

- Destination (charting session, 2026-09-09): change in place, judged by a Narrator recap plus the human's read.
- Emergent means designed mechanics, undesigned plot, including the ending.
- There is a World agent that adjudicates Actions into Outcomes.
- Jerry is switchable: human or agent; the agent is the default for emergent runs, and the human becomes Rick.
- Side Requests exist so some Meeseeks poof on screen.
- Meeseeks speech gets hard voice constraints: short, spoken, no memos.
- The dark turn may emerge in either Jerry mode, within the boundary in Notes.
- [Canon dossier](tickets/001-canon-dossier.md): Meeseeks are born cheerful, accept in three words, judge completion themselves, and poof the instant they call it done; escalation is time plus failure, first press comes after two whiffs and one "I give up", blame runs up the summoning chain, and the ending is a literal reframe of the Request adopted by cheer. Findings: `research/001-canon-dossier.md`.
- [Prior art on game-master agents](tickets/002-emergent-narrative-prior-art.md): split Action from Outcome with one World writer, keep facts in small structured state, let a die pick success once difficulty is set; three protocols to choose between in World mechanics. Findings: `research/002-emergent-narrative-prior-art.md`.

## Not yet specified

- How a run ends when the World judges the Impossible Request actually done, and whether the Box or the World says so.
- Cost per Episode: models for World, Jerry, Narrator, and how long an Episode runs.
- Whether Episodes remember each other: a Jerry who has been through this before, a Pen with history.
- How the Box skill and agent definition restructure once World and Jerry agents exist: one plugin, several agents, one press.
- Whether the Meeseeks need the World at all for Shouts and Journals, or only for Actions.

## Out of scope

- The Meeseeks Room, a live page rendering the tree with speech bubbles. Visualization, not story. Separate effort.
- Making Meeseeks more capable at real work. They must remain bad at it.
