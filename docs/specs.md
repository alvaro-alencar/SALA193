# Specs — SALA193

## 1. System overview

SALA193 has four main layers:

1. Character Layer: structured profiles for agents.
2. Simulation Layer: turn resolution, action selection and consequences.
3. Memory Layer: factual, emotional and relational continuity.
4. Narrative Layer: conversion from structured events into scenes.

## 2. Proposed MVP stack

- Language: Python 3.11+
- Character files: YAML
- Validation: Pydantic
- CLI: Typer
- Testing: pytest
- Optional LLM integration: provider adapter interface, not required for MVP

## 3. Dependency proposal

```txt
pydantic>=2.7
PyYAML>=6.0
typer>=0.12
rich>=13.7
pytest>=8.0
```

Optional later:

```txt
openai>=1.0
anthropic>=0.34
fastapi>=0.111
uvicorn>=0.30
sqlmodel>=0.0.21
```

## 4. Core modules

```text
sala193/
  models.py       # Pydantic data models
  engine.py       # Simulation loop and turn resolution
  memory.py       # Memory storage and retrieval
  narrator.py     # Event-to-scene transformation
  actions.py      # Action definitions and validation
  cli.py          # Command line interface
```

## 5. Data flow

```text
Character YAML files
        ↓
Pydantic validation
        ↓
Simulation engine
        ↓
Agent action proposals
        ↓
Event resolver
        ↓
Memory/reputation update
        ↓
Structured log
        ↓
Narrative scene generation
```

## 6. Character file shape

```yaml
id: joao
public_name: João
private_inspiration: BR
age_band: adult
speech_style:
  rhythm: informal
  traits:
    - warm
    - observant
    - evasive_when_pressed
temperament:
  openness: 0.82
  discipline: 0.43
  sociability: 0.91
  aggression: 0.28
  suspicion: 0.35
needs:
  - belonging
  - dignity
  - recognition
fears:
  - being humiliated
  - being controlled
wounds:
  - chronic underestimation
  - inherited inequality
ambitions:
  - be respected without becoming cruel
resources:
  social_capital: 0.88
  money: 0.42
  coercive_power: 0.31
  cultural_influence: 0.86
boundaries:
  lethal_violence: 0.15
  betrayal: 0.36
  public_humiliation: 0.65
relationships:
  samuel:
    trust: 0.52
    fear: 0.34
    admiration: 0.58
    resentment: 0.22
```

`private_inspiration` must never be exposed in story mode.

## 7. Turn structure

A simulation turn is a single unit of dramatic movement.

```python
Turn(
    index=1,
    active_agents=["joao", "samuel"],
    context="A crowded bar after a tense neighborhood meeting.",
    available_actions=["talk", "offer", "refuse", "threaten", "leave"],
)
```

## 8. Action model

Each action has:

- actor;
- target;
- type;
- visible intention;
- hidden intention;
- intensity;
- risk;
- expected gain;
- emotional tone.

Example:

```json
{
  "actor": "samuel",
  "target": "joao",
  "type": "offer",
  "visible_intention": "help João solve a debt problem",
  "hidden_intention": "make João dependent on him",
  "intensity": 0.62,
  "risk": 0.44,
  "emotional_tone": "confident"
}
```

## 9. Event resolution

The resolver should compute:

- success/failure;
- immediate consequence;
- relationship deltas;
- emotional deltas;
- memory entries;
- possible rumors;
- possible future hooks.

## 10. Relationship dimensions

Each relationship should track at least:

- trust;
- fear;
- admiration;
- resentment;
- debt;
- intimacy;
- dependency;
- rivalry.

All values range from 0.0 to 1.0 unless otherwise specified.

## 11. Scene generation modes

### Story mode

No explicit country references. No visible geopolitical layer.

### Analysis mode

May show hidden inspiration, archetypal links and historical compression logic.

### Writers' room mode

May suggest plot arcs and dramatic improvements without exposing them to final prose.

## 12. MVP command proposal

```bash
sala193 validate examples/characters/joao.yaml
sala193 run examples/scenarios/first_room.yaml --turns 10
sala193 scene logs/latest.json --pov joao
```

## 13. First milestone

Create a local-only deterministic simulation with João and Samuel.

Milestone output:

```text
logs/session_001/events.jsonl
logs/session_001/drama_log.md
logs/session_001/scene_joao.md
```
