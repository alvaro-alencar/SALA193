# Quickstart — SALA193

## 1. Install locally

```bash
git clone https://github.com/alvaro-alencar/SALA193.git
cd SALA193
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell
pip install -e .[dev]
```

## 2. Validate a character

```bash
sala193 validate examples/characters/joao.yaml
```

Expected result:

```text
João validado com sucesso.
```

## 3. Inspect the hidden table setup

```bash
sala193 inspect examples/scenarios/first_room.yaml
```

This command is for writers' room use. It may show private inspiration keys and should not be treated as story output.

## 4. Run the first simulation

```bash
sala193 run examples/scenarios/first_room.yaml --turns 4 --adapter rules
```

This creates:

```text
logs/latest/events.jsonl
logs/latest/drama_log.md
logs/latest/scene_joao.md
```

## 5. Try a quiet/passive table

```bash
sala193 run examples/scenarios/first_room.yaml --turns 2 --adapter passive --output-dir logs/passive
```

This is useful for testing scene and memory plumbing without active conflict.

## 6. Read the generated scene

```bash
cat logs/latest/scene_joao.md
```

## 7. Run tests

```bash
pytest
```

## 8. Current architecture

SALA193 now separates four roles:

- character sheet: who the person is;
- agent adapter: who plays the character;
- game master: who resolves consequences;
- narrator: who converts logs into prose.

The current engine is deterministic and simple. It does not yet use external LLMs.

## 9. Next step

Add an `LLMAgentAdapter` that returns structured `ProposedAction` objects from a model call.

The agent decides. The Game Master resolves. The narrator writes.
