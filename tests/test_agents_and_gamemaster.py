from pathlib import Path

from sala193.agents import RuleBasedAgentAdapter, get_agent_adapter
from sala193.engine import SimulationEngine
from sala193.models import Character, Scenario


def test_rule_based_agent_adapter_proposes_action() -> None:
    character = Character.from_yaml(Path("examples/characters/joao.yaml"))
    scenario = Scenario.from_yaml(Path("examples/scenarios/first_room.yaml"))
    frame = scenario.frames[0]

    action = RuleBasedAgentAdapter().propose(
        actor=character,
        frame=frame,
        turn_index=1,
        characters={character.id: character},
    )

    assert action.actor == "joao"
    assert action.action_type.value in {action.value for action in frame.available_actions} | {"threaten", "humiliate", "protect", "apologize", "reconcile"}


def test_game_master_adds_resolution_metadata() -> None:
    characters = [
        Character.from_yaml(Path("examples/characters/joao.yaml")),
        Character.from_yaml(Path("examples/characters/samuel.yaml")),
    ]
    scenario = Scenario.from_yaml(Path("examples/scenarios/first_room.yaml"))
    engine = SimulationEngine(characters=characters, scenario=scenario, agent_adapter=get_agent_adapter("rules"))

    log = engine.run(turns=1)

    assert log.events
    assert "success" in log.events[0].resolution
    assert "roll" in log.events[0].resolution
