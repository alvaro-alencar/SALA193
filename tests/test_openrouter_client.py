import json

import pytest

from sala193.llm_agent import LLMAgentAdapter, build_agent_prompt
from sala193.engine import SimulationEngine
from sala193.models import Character, MemoryEntry, Scenario, SimulationLog
from sala193.narrator import Narrator
from sala193.openrouter_client import OpenRouterClient, OpenRouterError


class MockHTTPResponse:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        content = {
            "actor": "joao", "target": "samuel", "action_type": "talk",
            "visible_intention": "João tenta resolver a tensão.",
            "hidden_intention": "Evitar uma dívida maior.",
            "intensity": 0.4, "risk": 0.2, "emotional_tone": "cauteloso",
            "dialogue": "Você fala fácil, Samuel. Quero ver na hora do aperto.",
        }
        return json.dumps(
            {"choices": [{"message": {"content": json.dumps(content)}}]}
        ).encode("utf-8")


def test_openrouter_json_schema_request(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["request"] = request
        captured["timeout"] = timeout
        return MockHTTPResponse()

    monkeypatch.setattr("sala193.openrouter_client.urlopen", fake_urlopen)
    client = OpenRouterClient(model="openai/gpt-4o-mini", api_key="not-a-real-key")
    result = client.complete_json("Escolha a ação de João em JSON.")
    body = json.loads(captured["request"].data.decode("utf-8"))
    assert body["response_format"]["type"] == "json_schema"
    assert body["provider"]["require_parameters"] is True
    assert body["model"] == "openai/gpt-4o-mini"
    assert captured["request"].get_header("Authorization") == "Bearer not-a-real-key"
    assert result["dialogue"].startswith("Você fala")


def test_openrouter_requires_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(OpenRouterError, match="OPENROUTER_API_KEY"):
        OpenRouterClient(model="some/model")


def test_other_character_private_state_is_not_in_prompt():
    joao = Character(id="joao", public_name="João")
    samuel = Character(
        id="samuel", public_name="Samuel",
        private_inspiration="US",
        wounds=["SEGREDO_INACESSIVEL"],
        memories=[MemoryEntry(
            event_id="s_1", summary="CONFIDENCIA_SECRETA",
            participants=["samuel"], secrecy="secret"
        )],
    )
    scenario = Scenario.from_yaml("examples/scenarios/first_room.yaml")
    prompt = build_agent_prompt(
        actor=joao, frame=scenario.frames[0], turn_index=1,
        characters={"joao": joao, "samuel": samuel},
    )
    assert "SEGREDO_INACESSIVEL" not in prompt
    assert "CONFIDENCIA_SECRETA" not in prompt
    assert "private_inspiration" not in prompt


def test_dialogue_survives_agent_gm_and_narrator():
    class FakeClient:
        def complete_json(self, prompt):
            return {
                "actor": "joao", "target": "samuel", "action_type": "talk",
                "visible_intention": "João procura conversar.",
                "hidden_intention": "Manter amizade",
                "intensity": 0.3, "risk": 0.2, "emotional_tone": "curioso",
                "dialogue": "E você vai pagar essa conta mesmo?",
            }

    scenario = Scenario.from_yaml("examples/scenarios/first_room.yaml")
    joao = Character(id="joao", public_name="João")
    samuel = Character(id="samuel", public_name="Samuel")
    engine = SimulationEngine(
        [joao, samuel], scenario, agent_adapter=LLMAgentAdapter(FakeClient())
    )
    action = engine.agent_adapter.propose(
        joao, scenario.frames[0], 1, engine.characters
    )
    event = engine.game_master.resolve(
        action, scenario.frames[0], 1, "e_0001", engine.characters
    )
    assert event.spoken_text == "E você vai pagar essa conta mesmo?"
    prose = Narrator(engine.characters).scene(
        SimulationLog(scenario_id="teste", events=[event])
    )
    assert "E você vai pagar essa conta mesmo?" in prose


def test_llm_rejects_action_outside_scene():
    class InvalidClient:
        def complete_json(self, prompt):
            return {
                "actor": "joao", "target": "samuel", "action_type": "kill",
                "visible_intention": "Violação", "hidden_intention": "",
                "intensity": 0.5, "risk": 0.5, "emotional_tone": "raiva",
                "dialogue": "Não.",
            }
    scenario = Scenario.from_yaml("examples/scenarios/first_room.yaml")
    joao = Character(id="joao", public_name="João")
    with pytest.raises(ValueError):
        LLMAgentAdapter(InvalidClient()).propose(
            joao, scenario.frames[0], 1, {"joao": joao}
        )
