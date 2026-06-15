from pathlib import Path

from sala193.models import Character, Scenario


def test_load_joao_character() -> None:
    character = Character.from_yaml(Path("examples/characters/joao.yaml"))

    assert character.id == "joao"
    assert character.public_name == "João"
    assert character.private_inspiration == "BR"
    assert "samuel" in character.relationships


def test_load_first_room_scenario() -> None:
    scenario = Scenario.from_yaml(Path("examples/scenarios/first_room.yaml"))

    assert scenario.id == "first_room"
    assert scenario.pov == "joao"
    assert scenario.frames
    assert "joao" in scenario.frames[0].participants
