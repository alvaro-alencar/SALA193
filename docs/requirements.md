# Requirements — SALA193

## 1. Product vision

SALA193 is a simulation-first narrative system where 193 AI agents interact in a shared fictional environment. Each agent is a fully fictional character whose hidden archetypal structure is inspired by a country, but the simulation must remain readable as ordinary human drama.

The system must help generate scenes, arcs, conflicts and long-form narrative material from agent interaction logs.

## 2. Core experience

The user should be able to:

1. define characters with YAML or JSON files;
2. define a shared scenario;
3. run simulation turns;
4. inspect raw events;
5. inspect relationship changes;
6. generate narrative scenes from selected events;
7. preserve continuity across sessions.

## 3. Narrative constraints

The system must not expose country identities inside generated scenes unless explicitly configured for analysis mode.

The system must avoid direct geopolitical terminology in story mode, including terms such as country, nation, UN, treaty, sanctions, GDP, army, border, colony, empire or invasion, unless those terms naturally belong to the ordinary fictional world.

The system should translate macro-historical structures into small-scale human situations.

Examples:

| Historical pattern | Fictional translation |
| --- | --- |
| annexation | coercive relationship, takeover of home/business/identity |
| genocide or complete destruction | murder, disappearance, erasure of a person or family |
| war causing mass death | beating, feud, arson, gang fight, neighborhood trauma |
| alliance | friendship, pact, debt, marriage, shared secret |
| sanctions | exclusion, boycott, blocked access, reputational isolation |
| economic dependence | debt, employment dependency, addiction to patronage |
| migration | people arriving, moving in, seeking shelter or opportunity |
| revolution | family rupture, workplace takeover, public humiliation, rebellion |

## 4. Agent requirements

Each agent must have:

- public name;
- private inspiration key;
- age band;
- temperament;
- needs;
- fears;
- wounds;
- ambitions;
- resources;
- moral boundaries;
- speech style;
- relationship map;
- memory log;
- current emotional state;
- behavioral rules.

Agents must be capable of:

- initiating dialogue;
- responding to dialogue;
- making offers;
- refusing offers;
- forming alliances;
- breaking alliances;
- escalating conflict;
- de-escalating conflict;
- hiding intentions;
- remembering betrayal;
- apologizing;
- lying when their profile allows it.

## 5. Simulation requirements

The engine must support turn-based simulation.

Each turn should include:

1. world state summary;
2. agent private state;
3. available actions;
4. agent decision;
5. event resolution;
6. relationship updates;
7. memory updates;
8. narrative log generation.

The first version may run locally with deterministic Python logic and mocked agent decisions. Later versions may plug into LLM providers.

## 6. Memory requirements

The system must distinguish:

- factual memory: what happened;
- emotional memory: how the agent felt;
- relational memory: how this changed trust, fear, admiration or resentment;
- rumor memory: unverified information;
- secret memory: known only to one or more agents.

## 7. Output requirements

The system should produce three output layers:

1. `events`: structured simulation events;
2. `drama_log`: human-readable summary of what happened;
3. `scene`: prose narrative written from a selected point of view.

## 8. Initial MVP scope

The MVP should include:

- 2 sample characters: João and Samuel;
- 1 simple location;
- 1 simulation loop;
- 5 basic actions;
- simple relationship scoring;
- memory append-only log;
- scene generator stub.

## 9. Non-goals for MVP

The MVP will not include:

- all 193 characters;
- web UI;
- persistent database;
- multi-provider LLM orchestration;
- real-time visualization;
- complex economic modeling;
- combat simulation.

## 10. Success criteria

The MVP succeeds if it can produce a coherent sequence of interactions where João and Samuel feel like consistent characters and where conflict or alliance emerges from their traits without hardcoding a specific historical event.
