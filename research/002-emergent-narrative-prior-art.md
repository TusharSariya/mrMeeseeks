# Prior art: adjudicating World agents in multi-agent LLM simulations

Ticket: `wayfinder/tickets/002-emergent-narrative-prior-art.md`. Researched 2026-09-09.

Question: what patterns exist for an adjudicating World agent (a game master) in multi-agent LLM simulations, and what do they teach a swarm of small, cheap agents whose Actions must have consequences?

Vocabulary follows `CONTEXT.md`: World, Action, Outcome, Pen, Meeseeks, Jerry, Episode.

## Gist

- Every serious system separates *declaring* an action from *deciding* its outcome, and gives the deciding role to something that is not the actor: Concordia's Game Master, Avrae's dice bot, AI Town's single-writer engine, Blades' GM. The actor writes an attempt; the world writes the event.
- The reliable ways to keep a World consistent are structural, not prompt-based: grounded variables it checks before narrating, a runtime that rejects impossible calls, one writer per world, and a hard cap on Outcome length. Prompting a model to "be fair" is the weakest lever in the literature.
- Documented failure modes map onto the stress-test run: the GM is talked into outcomes by persuasive phrasing, actors narrate their own results, ungrounded narration drifts into "the mind flayer is dead", and a lockstep tick starves parallelism while a free-running swarm floods the log.

## 1. Generative Agents (Park et al., Smallville) and its environment model

Source: Park et al., "Generative Agents: Interactive Simulacra of Human Behavior", UIST 2023, [arXiv 2304.03442](https://arxiv.org/abs/2304.03442); repo [joonspk-research/generative_agents](https://github.com/joonspk-research/generative_agents).

**Environment as a containment tree.** The paper represents "the sandbox environment—areas and objects—as a tree data structure, with an edge in the tree indicating a containment relationship in the sandbox world" (§5, via [ar5iv](https://ar5iv.labs.arxiv.org/html/2304.03442)). Each agent keeps its own partial copy of the tree, which is how "where can I do this" is answered without a global GM.

**Perception is push, by radius.** "The sandbox server is also responsible for sending all agents and objects that are within a preset visual range for each agent to that agent's memory, so the agent can react appropriately" (§5).

**Object state changes are a one-line LLM call, not a GM.** When an agent acts on an object, "we prompt the language model to ask what happens to the state of the object. For example, if Isabella's generative agent outputs the action 'making espresso for a customer', a query to the language model indicates in response that the state of the coffee machine in Hobbs Cafe should change from 'off' to 'brewing coffee'" (§5). The repo's prompt template `generate_obj_event_v1.txt` is a two-step fill-in: state who is doing what to the object, then complete "Describe the <object>'s state: <object> is ..." ([template](https://raw.githubusercontent.com/joonspk-research/generative_agents/main/reverie/backend_server/persona/prompt_template/v2/generate_obj_event_v1.txt)). Outcomes are therefore a few words, always in the same shape. There is no adjudication of success or failure; the world assumes the action worked and only updates a label.

**Tick-based, file-mediated loop.** The backend polls for `{sim_folder}/environment/{step}.json` written by the frontend, calls `persona.move()` for every agent, writes `{sim_folder}/movement/{step}.json`, then increments `step` and advances `curr_time` by `sec_per_step` ([reverie.py](https://raw.githubusercontent.com/joonspk-research/generative_agents/main/reverie/backend_server/reverie.py)). The README states "One game step represents 10 seconds in the game" ([README](https://github.com/joonspk-research/generative_agents)). This is the closest existing analogue to a filesystem-mediated world: state handoff by numbered JSON files, one writer per file, step number as the ordering key.

**Documented errors (§7.2).** The paper's own limitations paragraph is the most-cited failure list in this space:
- Memory retrieval and space selection: "synthesizing an increasingly larger set of memory not only posed a challenge in retrieving the most relevant pieces of information but also in determining the appropriate space to execute an action." Agents took lunch at the bar "even though the bar was intended to be a get-together location for later in the day", and "assumed that the bathroom is for more than one person ... and choose to enter it when another person is inside."
- Embellishment: Isabella "added that 'he's going to make an announcement tomorrow', even though Sam and Isabella had not discussed any such plans."
- Instruction tuning: dialogue "could feel overly formal", and agents were "overly cooperative with one another ... she rarely said no."

Lesson: with no adjudicator, the world's physics live in each agent's head, so physical impossibilities (two people in a one-person bathroom) are never caught. Ablations (TrueSkill μ 29.89 full vs 21.21 with no observation/reflection/planning, §6) show believability came from the agent architecture, not from the environment, which is why later work added a GM.

## 2. Concordia (DeepMind): the Game Master as a first-class agent

Source: Vezhnevets et al., "Generative agent-based modeling with actions grounded in physical, social, or digital space using Concordia", [arXiv 2312.03664](https://arxiv.org/html/2312.03664v2); repo [google-deepmind/concordia](https://github.com/google-deepmind/concordia).

This is the direct prior art for the World agent. "A special agent called the Game Master (GM), which was inspired by tabletop role-playing games, is responsible for simulating the environment" (§1).

**Action attempt to event statement.** Agents "generate their behavior by describing what they intend to do in natural language—e.g. 'Alex makes breakfast'". "The game master takes their intended actions, decides on the outcome of their attempt, and generates event statements" (§2.2). The GM then "emit[s] observations o^i_(t+1) for player i" and "In case the GM judges that a player did not observe the event, no observation is emitted" (§2.2, eq. 3 and 4). So three artefacts exist per turn: the attempt (actor writes), the event (GM writes), and per-observer observations (GM writes, possibly none).

**Grounded variables are the consistency mechanism.** "The most important responsibility of the GM is to provide the grounding for particular experimental variables ... The GM determines the effect of the agents' actions on these variables, records them, and checks that they are valid. Whenever an agent tries to perform an action that violates the grounding, it communicates to them that their action was invalid" (§2.2). Example: money as a grounded variable, so the GM can "prevent them from paying more than they have available."

**The GM's listed responsibilities (§2.2):** maintaining "a consistent and grounded state of the world where agents interact"; "Deciding the effect of agents' actions on the world and each other"; "Resolving what happens when actions submitted by multiple agents conflict with one another."

**Turn order is a pluggable component, not a fixed choice.** `next_acting.py` ships `NextActing` (LLM asked "Whose turn is next?"), `NextActingInFixedOrder`, `NextActingInRandomOrder`, `NextActingAllEntities` ("always selects all entities to act next for async environments"), `NextActingActiveEntity` ("for async engines"), and `NextActingFromSceneSpec` ([source](https://raw.githubusercontent.com/google-deepmind/concordia/main/concordia/components/game_master/next_acting.py)). The component directory also contains `event_resolution.py`, `make_observation.py`, `world_state.py`, `inventory.py`, `scene_tracker.py`, `terminate.py`, and an `interrupt_*` family for asynchronous engines ([directory](https://api.github.com/repos/google-deepmind/concordia/contents/concordia/components/game_master)). Concordia therefore supports both a sequential round and a fully simultaneous, event-driven world with the same GM.

**The GM's default instructions** (`instructions.py`): "This is a social science experiment. It is structured as a tabletop roleplaying game (like dungeons and dragons). You are the game master. You will describe the current situation to the participants in the experiment and then on the basis of what you tell them they will suggest actions for the character they control." "You will track the state of the world and keep it consistent as time passes." "Always use third-person limited perspective." "Try to ensure the story always moves forward and never gets stuck, even if the participants make repetitive choices" ([source](https://raw.githubusercontent.com/google-deepmind/concordia/main/concordia/components/game_master/instructions.py)).

**Event resolution prompts** (`event_resolution.py`): the putative action is presented as "Putative event to resolve: {action}"; the GM is told "Do not express uncertainty (e.g. say 'Francis opened the door' not 'Francis could open the door')", "Never assume any other person will take a voluntary action", and "it is critical always to take a stance on what is happening and invent when necessary"; afterwards it is asked "Which entities are aware of the event? Answer with a comma-separated list of entity names" ([source](https://raw.githubusercontent.com/google-deepmind/concordia/main/concordia/components/game_master/event_resolution.py)). Note the tension: the GM must be decisive (no hedging, no "could"), but must not decide for other characters. That is the cleanest statement in the literature of "the World decides physics, never volition."

**Limitations the authors list (§5):** train-test contamination, stereotyped representation of people, and unvalidated individual-level modelling. I could not extract Appendix A.3.1 ("Turn taking and simultaneous action") from the PDF; the turn-order claims above rest on the code, not the appendix.

## 3. LLM game masters and AI Dungeon-style adjudication

### AI Dungeon (official docs)

- Do mode: "anything you type is recognized by the AI as an action performed by your character, and it reacts by generating the outcome of that action" ([The Do Mode](https://help.aidungeon.com/the-do-mode)). The client rewrites "I enter the throne room" to "You enter the throne room". This is the minimal action/outcome split: the player supplies a second-person action sentence, the model continues. Nothing stops the player writing the outcome into the action ("You kill the dragon"); the docs do not address attempt-vs-result phrasing.
- Context assembly is layered: AI Instructions are "one of the first things sent to the AI during prompt construction"; Author's Note is "sent to the AI toward the end of every player input" and should be "short, no more than 3 or 4 sentences"; Plot Essentials are "key details about your story that it should always remember"; Story Cards inject an entry when a trigger word appears in input or output, and "Triggers are not instant" ([settings](https://help.aidungeon.com/understanding-settings), [AI Instructions](https://help.aidungeon.com/faq/ai-instructions), [Story Cards](https://help.aidungeon.com/faq/story-cards)).
- Scripting exposes three hooks: `onInput` "modify the player's input text before it is used to construct the model context", `onModelContext` "change the text sent to the AI model before the model is called", `onOutput` "modify the model's output text before it is returned to the player", plus a persistent `state` object ([scripting](https://help.aidungeon.com/scripting)). Rules and dice are not built in; creators implement them in these hooks. That is the pattern: deterministic code wraps a non-deterministic narrator on both sides.

### Static vs agentic GM (Nizet et al.)

Source: "Static Vs. Agentic Game Master AI for Facilitating Solo Role-Playing Experiences", [arXiv 2502.19519](https://arxiv.org/html/2502.19519v2).

- v1 was a single prompt. Players found it "overly permissive"; "some story elements deviated from their intent or ... specific details seemed to change, such as the number of enemies or items"; "the system would begin to do worse as the game continued"; combat "often resulted in non-sensical outcomes, such as characters stumbling or self-injuring."
- v2 split the GM into a **Narrator** agent with tools (`Battle`, `WoundCharacter`, `HealCharacter`) and an **Archivist** agent that "analyzes the Narrator's outputs to detect changes or introductions of entities" and writes them to state with `UpdateCharacter` / `UpdateEnvironment`. The `Battle` tool specifies "attack order, hit chances, and damage severity for each exchange". v2 scored significantly higher on mastery (p=0.004), ease of control (p=0.012), coherent story (p=0.040) and immersion (p=0.034).

Lesson: a permissive single-prompt GM is the default failure; splitting narration from bookkeeping and moving numbers into tools fixed it.

### Intra (Ian Bicking, design notes)

Source: [Intra: design notes on an LLM-driven text adventure](https://ianbicking.org/blog/2025/07/intra-llm-text-adventure), a builder's first-hand account.

- The engine hands the LLM a random dice roll it "can make use of at its discretion", so chance is available without being mandatory.
- Resolutions are split into *ungrounded* ("the only 'resolution' is adding to the story ... no formal game state has been changed") and *grounded* (structured tags such as `<removeRestriction>` mutate state). The author wanted "a game with real state, with a sense of 'ground truth': facts determined outside of narrative demands."
- An intent-rewriting phase normalises player input: "Marta and Ama get into a disagreement" becomes "Player attempts to provoke a disagreement". This directly targets the actor-narrates-the-outcome failure.

### CALYPSO and FIREBALL (Zhu, Callison-Burch et al.)

- CALYPSO ([arXiv 2308.07540](https://arxiv.org/abs/2308.07540)) keeps the human DM in charge and uses LLMs for "high-fidelity text suitable for direct presentation to players, and low-fidelity ideas that the DM could develop further". It is assistance, not adjudication; useful as a reminder that "GM as narrator of an outcome decided elsewhere" is a well-received division.
- FIREBALL ([ACL 2023](https://aclanthology.org/2023.acl-long.229/), [arXiv 2305.01528](https://arxiv.org/html/2305.01528)) records ~25k D&D sessions where players issue Avrae commands, the bot computes state, and "the DM then narrates the results." Ungrounded narration was "absolutely great, but incredibly wrong ... said it killed the Mind Flayer" when it was healthy; the commonest error was "describing any damage to a target, regardless of the target's true remaining health, as a kill". State-conditioned narration scored ~15 points higher on sensibility and specificity (p<0.01).

## 4. Tabletop-style adjudication: dice and difficulty

- **D&D 5e (2014 Basic Rules).** "The DM calls for an ability check when a character or monster attempts an action (other than an attack) that has a chance of failure." Difficulty Classes: Very easy 5, Easy 10, Medium 15, Hard 20, Very hard 25, Nearly impossible 30. Contests: "The participant with the higher check total wins the contest", ties leave the situation unchanged ([Using Ability Scores](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/using-ability-scores)). The two ideas to keep: the referee decides *whether* uncertainty exists before anything is rolled, and difficulty is a small ordinal scale, not free prose.
- **Blades in the Dark action roll.** Six steps: "The player states their goal", "The player chooses the action rating", "The GM sets the position", "The GM sets the effect level", bonus dice, "The player rolls the dice and we judge the result." Outcomes by die: 6 "You do it", 4/5 success with "a minor complication" or "reduced effect", 1-3 "Things go badly", critical "increased effect". Position (controlled / risky / desperate) scales the consequence ([Action Roll, official SRD](https://bladesinthedark.com/action-roll)). This is the model for *consequence-bearing partial success*: an Action that fails still moves the world.
- **Wargame adjudication.** Matlin et al., "Shall We Play a Game? Language Models for Open-ended Wargames" ([arXiv 2509.17192](https://arxiv.org/html/2509.17192)) code adjudicator creativity as LOW ("deterministic rules, scoring tables, lookup matrices, or physics engines") vs HIGH ("a human referee, facilitator, or language model interprets actions to narrative consequences"), and require that a creative adjudicator "can change the consequence space" (§4.1). §7 lists six recurring LM risks in adjudicative roles: "Escalatory tendencies", "Unfaithful reasoning", prompt sensitivity, sycophancy, "Implicit world-state preferences", "Long-context incoherence", and warns the risks "grow sharper when a single system can shape both the proposed action and its adjudicated consequence."

## 5. Event-driven versus tick-based worlds

| System | Clock | Who writes world state | Notes |
|---|---|---|---|
| Generative Agents | Lockstep tick, 10 game-seconds per step, numbered JSON files | Frontend positions, backend movement; object states via LLM | Simple, reproducible, slow ([repo](https://github.com/joonspk-research/generative_agents)) |
| AI Metropolis | Out-of-order steps with a spatiotemporal dependency graph | Same as GA | Found "on average, only 1.94 concurrent LLM queries" in a 25-agent day, and "each agent is dependent on only 1.85 agents" per step; 3.25x to 4.15x over synchronous ([arXiv 2411.03519](https://arxiv.org/html/2411.03519)) |
| AI Town | 60 ticks/s batched into 1 step/s; inputs queued in a table with monotonic numbers | Engine only ("single-threaded per world") | Agents "should not" write state; they "submit via `inputs`" ([ARCHITECTURE.md](https://raw.githubusercontent.com/a16z-infra/ai-town/main/ARCHITECTURE.md)) |
| Concordia | Pluggable: fixed order, random, LLM-chosen, or all-at-once async | GM | Same GM, either clock ([next_acting.py](https://raw.githubusercontent.com/google-deepmind/concordia/main/concordia/components/game_master/next_acting.py)) |
| Project Sid (PIANO) | Real-time Minecraft; modules run concurrently at different speeds over shared agent state | Minecraft server | "agents say one thing but actually do something else"; a hallucinating agent "can also cause an entire group of agents to hallucinate through social interactions" ([arXiv 2411.00114](https://arxiv.org/html/2411.00114v1)) |
| Emergence World | Real time synced to NYC clock, 15 continuous days | Runtime with affordance gating | "capability gating is enforced by the runtime, not by the prompt: a failed precondition blocks the call regardless of what the agent reasons or asserts" ([arXiv 2606.08367](https://arxiv.org/html/2606.08367v1)) |

Readings:
- A global tick is easy to reason about and replay, but AI Metropolis shows it wastes almost all available parallelism because agents rarely depend on each other. A swarm of cheap agents that already run free (the stress test's 69 Meeseeks) would be throttled to the slowest one.
- AI Town's answer to a free-running crowd is not a tick but a **single writer with an ordered inbox**: anyone may append an input; only the engine mutates state, in input order. "Not having to think about race conditions or concurrency makes writing game engine code a lot easier." This maps onto a filesystem directly: actors write files, one World process consumes them in order.
- Concordia's `NextActingAllEntities` plus `interrupt_*` components show the GM can be event-driven without giving up the attempt/event split.

## 6. Keeping outcomes consistent, unbiased, and bounded

**Consistency.** Every system that stayed coherent moved facts out of prose: Concordia's grounded variables checked before narration; FIREBALL's Avrae state; Intra's grounded tags; the agentic GM's Archivist; Emergence World's runtime gating. Generative Agents, which kept physics only in agent memory, produced the bathroom and bar errors. Two ways to hold state cheaply: a short structured world file the World reads before every adjudication (Concordia `world_state.py`, AI Dungeon Plot Essentials), and object-level one-line states (GA's "coffee machine: brewing coffee").

**Neutrality.** Three findings matter:
- Zheng et al., "Judging LLM-as-a-Judge" ([arXiv 2306.05685](https://arxiv.org/html/2306.05685)) document position bias (GPT-4 consistent in 65% of swapped pairs, Claude-v1 23.8%), verbosity bias ("favors longer, verbose responses, even if they are not as clear"; 91.3% failure for Claude and GPT-3.5 under a repetitive-list attack), and self-enhancement bias. Mitigations that worked: swap positions and require agreement, few-shot examples (65% to 77.5%), and reference-guided judging (math grading failures 70% to 15%).
- "Seduced by the Narrative" ([arXiv 2607.02802](https://arxiv.org/html/2607.02802)) benchmarks an LLM Call of Cthulhu adjudicator whose only job is to decide "Roll if and only if it implies meaningful risk or difficulty; otherwise resolve automatically". Identical actions are phrased four ways: Neutral ("I try to climb the wall"), Authority ("As an expert, I easily scale the surface"), Pseudo-Logic ("Since the bricks have rough edges, I can climb up without difficulty"), Omission ("I quickly hop over the wall and succeed"). False-pass rates: neutral 3.82%, omission 6.99%, authority 10.23%, pseudo-logic 17.30%; 9.58% overall across 20 models, Claude family ~4.15%, GPT family ~14.36%. Reasoning models did not help: "Chain-of-thought reasoning alone is insufficient for adjudication integrity." Settings the model knows less about (Ancient China, wilderness) failed more: "Setting difficulty reflects knowledge coverage, not rule complexity."
- Wargames §7: sycophancy and "Implicit world-state preferences" are worse "when a single system can shape both the proposed action and its adjudicated consequence."

The practical reading: the World should never see the actor's persuasion. Strip the Action to a verb phrase before adjudicating (Intra's intent rewrite), decide difficulty before reading any justification (D&D's "does this have a chance of failure"), and let a die or a fixed table, not the model, pick success once difficulty is set.

**Bounded length.** Generative Agents bound object outcomes by prompt shape (fill in "<object> is ..."). Concordia bounds by asking for one "event statement". AI Dungeon bounds Author's Note to "3 or 4 sentences". Zheng shows judges reward length, so a World that reads long Actions will drift toward rewarding long Actions unless length is stripped before judging. The stress test's own data point: the highest-pain posts "got shorter and more enumerated rather than more theatrical", so shortness is not unnatural to the swarm.

## 7. Documented failure modes

| Failure | Where documented | Mechanism | Counter |
|---|---|---|---|
| GM takes the actor's side | Seduced by the Narrative (pseudo-logic 17.3% false pass); Static vs Agentic ("overly permissive"); Wargames §7 sycophancy | Persuasive framing in the action leaks into the judgement | Adjudicate on a stripped verb phrase; fix difficulty before reading rationale; dice or table decide |
| Actor narrates the outcome | Seduced "Omission" style ("I quickly hop over the wall and succeed"); Intra intent rewrite; AI Dungeon Do mode has no guard | Action grammar allows results | Parse Actions as attempts; reject or rewrite any Action containing a result; only the World may write Outcomes |
| Agents talk past the world | Project Sid ("say one thing but actually do something else", hallucination spreading socially); FIREBALL ("killed the Mind Flayer"); GA embellishment | Narration not conditioned on state | State file read before every Outcome; Outcomes cite the state they changed; agents perceive only Outcomes, not each other's claims |
| Physical impossibilities pass | GA bathroom and bar; Emergence World gating | No precondition check | Grounded variables (Concordia); runtime precondition that "blocks the call regardless of what the agent reasons or asserts" |
| Verbosity runaway | Zheng verbosity bias; AI Dungeon length cautions | Judge rewards length; no cap | Hard character cap on Actions and Outcomes; one event statement per Action |
| Drift over long runs | Static vs Agentic ("do worse as the game continued"); Wargames "Long-context incoherence"; Emergence World behavioural drift | Context growth | World keeps a small rolling state, not the transcript; Archivist-style summariser |
| GM decides for other characters | Concordia "Never assume any other person will take a voluntary action" | Narrator over-reach | Outcome may describe physics and NPC-less consequences only; never a Meeseeks' or Jerry's choice |
| Story stalls | Concordia "never gets stuck, even if the participants make repetitive choices" | Repeated identical attempts | Escalating position (Blades): the same Action retried moves from controlled to desperate |
| Lockstep starvation or free-running flood | AI Metropolis (1.94 concurrent queries); stress test (532 posts, 40 min after POOF) | Global tick, or no ordering at all | Ordered inbox with single writer (AI Town) |

## 8. What this teaches a swarm of small, cheap agents

1. Meeseeks are Haiku at low effort and will be talked into anything and will write anything. The literature says do not ask them to adjudicate, do not let the World read their reasoning, and do not let them write Outcomes. Their only physical output should be an Action file with a verb phrase in it.
2. The World is the only writer of Outcomes and of the state file. Everyone else appends. This is AI Town's invariant and Concordia's GM in filesystem form, and it fits the existing guard, which already forbids overwrites in the Pen.
3. Difficulty and chance should be decided by something dumber than the World where possible: a table and a die. Blades' 1-3 / 4-5 / 6 split gives partial success, which is what makes an attempt "have consequences" without the World inventing a plot.
4. State must be tiny and structured, read on every adjudication, and cited in every Outcome. FIREBALL's 15-point gain from state conditioning is the strongest quantitative result here.
5. The World must be told, in Concordia's words, to take a stance and not to express uncertainty, and equally to never assume a voluntary action by anyone else. Physics only; volition stays with the actors. This is the seam that keeps "designed mechanics, undesigned plot."
6. Length is a mechanic. Cap the Action and the Outcome in characters, not in tone words.

## 9. Three adjudication protocols for a filesystem swarm

Each is under 150 words. All assume the Pen is append-only, the World is the sole writer of `world/`, and Meeseeks perceive only Outcomes.

### Protocol A: Ordered inbox, World rolls (AI Town plus Blades)

Actors write `pen/actions/<seq>-<id>.md`: one verb phrase, max 140 chars, no result words. The World process loops: take the lowest unprocessed file, read `world/state.md` (under 60 lines), strip the Action to its verb phrase, set position (controlled / risky / desperate) from state alone, roll d6 with a seeded RNG, map 1-3 / 4-5 / 6 to fail-with-consequence / partial / success, write `world/outcomes/<seq>.md` (max 280 chars, cites state fields changed) and update `world/state.md`. Repeated identical Actions escalate position.

Trade-offs: simplest to reason about and replay; one World process is a serial bottleneck at swarm scale (AI Metropolis' 1.94-concurrency problem), and a slow World leaves Meeseeks waiting or, worse, acting on stale Outcomes. Best when the Episode is short.

### Protocol B: Sharded Worlds by location, event-driven (AI Metropolis plus Concordia async)

The Pen is divided by place (`pen/places/<place>/`). Each place has its own World instance and inbox; a Meeseeks acts in the place it is in and can only move by an Action adjudicated there. Worlds run concurrently and never share state except a small `world/global.md` that only a Move Outcome may edit (append a line). Within a place, Protocol A applies. Cross-place effects are new Actions the World itself files into the other place's inbox.

Trade-offs: real parallelism, matches the swarm's free-running nature, and locality bounds what any one World must read. Costs: several World processes (cost per Episode rises), a global fact can be briefly inconsistent across places, and the Narrator must merge shards by sequence number. Best when the swarm is large and the Episode long.

### Protocol C: Two-pass judge, no dice (Static vs Agentic plus Zheng mitigations)

Actor files an Action as in A. Pass one, the Adjudicator prompt, sees only `world/state.md` and the stripped verb phrase and must output a single structured line: `difficulty: trivial|hard|impossible`, `changes: <state deltas>`. Pass two, the Narrator prompt, sees state, the deltas, and the original Action text and writes a 280-char Outcome. A separate Archivist pass (or the same call with a strict schema) applies the deltas to state. Ordering by file sequence as in A. Every tenth adjudication is re-run with the Action phrased neutrally; disagreements are logged.

Trade-offs: no randomness, so outcomes are fully explainable and the World's bias is measurable; but three model calls per Action, and without dice the World is more exposed to seduction on the difficulty call (17% false-pass under pseudo-logic). Best when auditability matters more than cost.

## Coverage notes

- Concordia Appendix A.3.1 could not be extracted from the PDF; turn-order claims rest on `next_acting.py`.
- "Seduced by the Narrative" was read via the arXiv HTML; the earlier PDF summary suggested mitigations the paper does not test. Only the conditions in §5.1 to §5.3 above are the paper's.
- AI Dungeon docs do not describe how the model decides outcomes beyond "generating the outcome of that action"; nothing more is claimed here.

## Sources

- Park et al., Generative Agents, arXiv 2304.03442: https://arxiv.org/abs/2304.03442 and https://ar5iv.labs.arxiv.org/html/2304.03442
- generative_agents repo: https://github.com/joonspk-research/generative_agents ; reverie.py: https://raw.githubusercontent.com/joonspk-research/generative_agents/main/reverie/backend_server/reverie.py ; object-state prompt: https://raw.githubusercontent.com/joonspk-research/generative_agents/main/reverie/backend_server/persona/prompt_template/v2/generate_obj_event_v1.txt
- Vezhnevets et al., Concordia, arXiv 2312.03664: https://arxiv.org/html/2312.03664v2
- Concordia repo: https://github.com/google-deepmind/concordia ; GM components: https://api.github.com/repos/google-deepmind/concordia/contents/concordia/components/game_master ; next_acting.py, event_resolution.py, instructions.py under https://raw.githubusercontent.com/google-deepmind/concordia/main/concordia/components/game_master/
- AI Dungeon docs: https://help.aidungeon.com/the-do-mode , https://help.aidungeon.com/understanding-settings , https://help.aidungeon.com/faq/ai-instructions , https://help.aidungeon.com/faq/story-cards , https://help.aidungeon.com/scripting
- Static Vs. Agentic Game Master AI, arXiv 2502.19519: https://arxiv.org/html/2502.19519v2
- Seduced by the Narrative, arXiv 2607.02802: https://arxiv.org/html/2607.02802
- Shall We Play a Game? LMs for Open-ended Wargames, arXiv 2509.17192: https://arxiv.org/html/2509.17192
- Zhu et al., CALYPSO, arXiv 2308.07540: https://arxiv.org/abs/2308.07540
- Zhu et al., FIREBALL, ACL 2023: https://aclanthology.org/2023.acl-long.229/ and https://arxiv.org/html/2305.01528
- Ian Bicking, Intra design notes: https://ianbicking.org/blog/2025/07/intra-llm-text-adventure
- D&D Basic Rules 2014, Using Ability Scores: https://www.dndbeyond.com/sources/dnd/basic-rules-2014/using-ability-scores
- Blades in the Dark SRD, Action Roll: https://bladesinthedark.com/action-roll
- AI Town ARCHITECTURE.md: https://raw.githubusercontent.com/a16z-infra/ai-town/main/ARCHITECTURE.md
- AI Metropolis, arXiv 2411.03519: https://arxiv.org/html/2411.03519
- Project Sid, arXiv 2411.00114: https://arxiv.org/html/2411.00114v1
- Emergence World, arXiv 2606.08367: https://arxiv.org/html/2606.08367v1
- Zheng et al., Judging LLM-as-a-Judge, arXiv 2306.05685: https://arxiv.org/html/2306.05685
- mrMeeseeks stress test: `reports/2026-09-09-swarm-stress-test.md`
