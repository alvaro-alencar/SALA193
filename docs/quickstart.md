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

## 3. Run the first simulation

```bash
sala193 run examples/scenarios/first_room.yaml --turns 4
```

This creates:

```text
logs/latest/events.jsonl
logs/latest/drama_log.md
logs/latest/scene_joao.md
```

## 4. Read the generated scene

```bash
cat logs/latest/scene_joao.md
```

## 5. Run tests

```bash
pytest
```

## 6. Current limitations

The current engine is deterministic and simple. It does not yet use external LLMs.

The purpose of this version is to prove the skeleton:

- character sheets load;
- relationships update;
- events are generated;
- memories are appended;
- scenes are produced without exposing the hidden geopolitical layer.

## 7. Next step

Add an `AgentAdapter` interface so actions can be proposed by:

1. deterministic rules;
2. local LLMs;
3. remote LLM APIs;
4. hybrid writer's-room mode.
