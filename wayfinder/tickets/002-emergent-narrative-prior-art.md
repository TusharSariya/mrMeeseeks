# Prior art: game-master agents and emergent narrative in multi-agent sims

Label: wayfinder:research
Status: closed
Assignee:
Blocked by: 

## Question

What patterns exist for an adjudicating World agent in multi-agent simulations: Generative Agents (Smallville), AI game masters, tabletop-style adjudication with dice, event-driven versus tick-based worlds, and how they keep outcomes consistent and unbiased. What failure modes are documented: the GM taking sides, agents talking past the world, runaway verbosity. Surface three concrete adjudication protocols the World ticket can choose between.

## Resolution

- Every coherent system splits the Action (actor writes an attempt) from the Outcome (a single World writer decides), keeps facts in a small structured state the World reads before narrating, and lets a table or die, not the model, pick success once difficulty is set.
- Documented failures match our run: the GM is seduced by persuasive phrasing (17% false pass under pseudo-logic), actors narrate their own results, ungrounded narration drifts ("killed the Mind Flayer"), and lockstep ticks starve parallelism while free-running swarms flood the log.
- Three protocols to choose between in ticket 003: A ordered inbox with dice (simple, serial), B sharded Worlds by place (parallel, more cost), C two-pass judge without dice (auditable, most exposed to seduction).

Findings: `research/002-emergent-narrative-prior-art.md`.
