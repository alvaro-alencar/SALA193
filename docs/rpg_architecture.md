# RPG Architecture — SALA193

SALA193 now follows a tabletop RPG architecture.

## Roles

### Character

A fictional person with sheet, memory, wounds, relationships and current emotional state.

The character does not know any hidden historical layer.

### Agent Adapter

The player behind the character.

Current adapters:

```text
RuleBasedAgentAdapter
PassiveAgentAdapter
LLMAgentAdapter
```

Future adapters may include:

```text
LocalLLMAgentAdapter
OpenAIAgentAdapter
HybridAgentAdapter
HumanAgentAdapter
```

The engine should not care which one is used.

### Game Master

The arbiter of consequence.

The agent says:

> I try to help João in public.

The Game Master decides:

> The help succeeds, but creates debt, shame and future resistance.

### Dramatic Roll

A deterministic RPG-like check used to resolve uncertainty.

It considers:

- actor temperament;
- actor resources;
- relationship values;
- action intensity;
- action risk;
- scene pressure;
- a stable pseudo-roll.

The goal is not physical realism. The goal is dramatic plausibility.

## Flow

```text
Scene frame
  ↓
Agent adapter proposes action
  ↓
Game Master resolves action
  ↓
Rules produce dramatic roll
  ↓
Relationships and memories update
  ↓
Narrator converts logs into prose
```

## Why this matters

This separation lets SALA193 become a real simulation table.

Without this separation, every character is just a function.

With it, each character can eventually have its own intelligence provider, memory strategy, prompt style, secrets, lies and long-term goals.

## LLM adapter contract

`LLMAgentAdapter` receives:

- public character sheet;
- recent memories;
- scene frame;
- legal available actions;
- story mode constraints.

It must return a structured `ProposedAction`, not prose.

The adapter validates:

- actor identity;
- target legality;
- action legality;
- Pydantic schema validity.

The prose belongs to the narrator. The decision belongs to the agent. The consequence belongs to the Game Master.

## Next architecture step

Add provider implementations around the `LLMClient` protocol:

- local model client;
- OpenAI client;
- Anthropic client;
- scripted test client;
- mixed human/AI client.
