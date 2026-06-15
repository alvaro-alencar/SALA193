from pathlib import Path

from sala193.engine import SimulationEngine
from sala193.models import Character, Scenario
from sala193.narrator import Narrator


def test_engine_generates_events() -> None:
    characters = [
        Character.from_yaml(Path("examples/characters/joao.yaml")),
        Character.from_yaml(Path("examples/characters/samuel.yaml")),
    ]
    scenario = Scenario.from_yaml(Path("examples/scenarios/first_room.yaml"))

    engine = SimulationEngine(characters=characters, scenario=scenario)
    log = engine.run(turns=2)

    assert len(log.events) == 4
    assert log.events[0].scene_id == "bar_debt_001"
    assert log.events[0].actor in {"joao", "samuel"}


def test_narrator_generates_story_mode_scene() -> None:
    characters = [
        Character.from_yaml(Path("examples/characters/joao.yaml")),
        Character.from_yaml(Path("examples/characters/samuel.yaml")),
    ]
    scenario = Scenario.from_yaml(Path("examples/scenarios/first_room.yaml"))
    engine = SimulationEngine(characters=characters, scenario=scenario)
    log = engine.run(turns=1)

    scene = Narrator(engine.characters).scene(log, pov="joao")

    assert "Meu nome é João" in scene
    assert "país" not in scene.lower()
    assert "geopolítica" not in scene.lower()
