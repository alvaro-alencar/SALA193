# Simulation Loop — SALA193

## 1. Goal

The simulation loop must generate dramatic continuity, not merely agent chatter.

Each turn should move at least one of these dimensions:

- relationship;
- resource;
- reputation;
- secret;
- threat;
- emotional state;
- future obligation.

If a turn changes nothing, it should be compressed or discarded.

## 2. Loop stages

### Stage 1 — Select scene frame

A frame defines:

- location;
- time;
- participants;
- pressure;
- recent context;
- dramatic question.

Example:

```yaml
location: Bar do Antônio
time: Thursday night
participants: [joao, samuel]
pressure: João owes money and Samuel knows it.
dramatic_question: Will João accept help from someone he does not fully trust?
```

### Stage 2 — Load agent states

For each participant:

- current emotion;
- relevant memories;
- relationship values;
- private goals;
- public posture;
- stress level.

### Stage 3 — Propose actions

Each active agent proposes one or more possible actions.

Action examples:

- talk;
- offer;
- request;
- refuse;
- threaten;
- apologize;
- expose_secret;
- hide_information;
- leave;
- escalate;
- protect;
- humiliate;
- reconcile.

### Stage 4 — Resolve action

The resolver determines:

- whether the action succeeds;
- what is seen by others;
- what is hidden;
- who gains leverage;
- who loses face;
- who remembers what.

### Stage 5 — Update state

Update:

- relationships;
- emotional states;
- resources;
- reputations;
- memories;
- unresolved hooks.

### Stage 6 — Produce logs

Generate:

- structured event;
- drama log;
- possible scene seed.

## 3. Event schema

```json
{
  "id": "e_0001",
  "turn": 1,
  "scene_id": "s_001",
  "actor": "samuel",
  "target": "joao",
  "action_type": "offer",
  "visible_action": "Samuel offers to pay João's debt.",
  "hidden_intention": "Increase João's dependency.",
  "outcome": "João accepts publicly but feels humiliated.",
  "relationship_delta": {
    "joao->samuel": {
      "debt": 0.18,
      "trust": 0.04,
      "resentment": 0.07
    },
    "samuel->joao": {
      "protectiveness": 0.08,
      "dependency": 0.12
    }
  },
  "memory_tags": ["debt", "favor", "public_pressure"],
  "future_hooks": ["João may resist Samuel's next request."]
}
```

## 4. Relationship update principles

A single action can create contradictory effects.

Samuel helping João may increase:

- gratitude;
- debt;
- resentment;
- dependency;
- admiration;
- fear.

Contradiction is not a bug. It is character.

## 5. Dramatic pressure

Every scene needs pressure.

Good pressure:

- someone owes someone;
- someone knows a secret;
- someone needs help but hates needing it;
- someone is about to be humiliated;
- someone must choose a side;
- someone offers protection that may become control;
- someone tries to apologize but cannot admit the real crime.

Weak pressure:

- characters discuss abstract philosophy;
- characters explain their motivations;
- characters summarize history;
- characters describe the setting without conflict.

## 6. Turn selection

The engine should prefer turns where:

- high resentment meets high dependency;
- low trust meets high need;
- high pride meets public exposure;
- high fear meets ambiguous threat;
- old memory is triggered by new action.

## 7. Emergence policy

Do not hardcode historical events.

Instead, hardcode psychological tendencies and environmental pressures.

Wrong:

- force Samuel to attack Ivan in turn 10.

Right:

- give Samuel high threat sensitivity, high coercive power and a rumor that Ivan is hiding weapons.

If conflict emerges, it emerges.

## 8. Scene seed output

After each meaningful event, the engine can produce a seed for prose generation:

```yaml
pov: joao
scene_type: bar_confrontation
central_emotion: humiliation
dramatic_question: Will João accept help from Samuel?
must_include:
  - Samuel pays before João can refuse
  - Antônio notices João's face
  - João jokes to hide shame
must_avoid:
  - country references
  - political exposition
  - explaining the metaphor
```

## 9. Stop conditions

A simulation session can end when:

- max turns reached;
- a major rupture occurs;
- a death/disappearance occurs;
- a pact is formed;
- a secret is revealed;
- emotional tension resolves temporarily.
