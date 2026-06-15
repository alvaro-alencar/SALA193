from pathlib import Path

from sala193.llm_agent import LLMAgentAdapter, build_agent_prompt
from sala193.models import Character, Scenario


class FakeClient:
    def complete_json(self, prompt: str) -> dict:
        return {
            "actor": "joao",
            "target": "samuel",
            "action_type": "talk",
            "visible_intention": "João tries to keep the conversation from hardening.",
            "hidden_intention": "avoid owing more than he can pay back",
            "intensity": 0.41,
            "risk": 0.22,
            "emotional_tone": "warm but careful",
        }


def test_llm_agent_adapter_accepts_structured_action() -> None:
    joao = Character.from_yaml(Path("examples/characters/joao.yaml"))
    samuel = Character.from_yaml(Path("examples/characters/samuel.yaml"))
    scenario = Scenario.from_yaml(Path("examples/scenarios/first_room.yaml"))

    action = LLMAgentAdapter(FakeClient()).propose(
        actor=joao,
        frame=scenario.frames[0],
        turn_index=1,
        characters={"joao": joao, "samuel": samuel},
    )

    assert action.actor == "joao"
    assert action.target == "samuel"
    assert action.action_type.value == "talk"


def test_llm_prompt_hides_private_inspiration() -> None:
    joao = Character.from_yaml(Path("examples/characters/joao.yaml"))
    samuel = Character.from_yaml(Path("examples/characters/samuel.yaml"))
    scenario = Scenario.from_yaml(Path("examples/scenarios/first_room.yaml"))

    prompt = build_agent_prompt(
        actor=joao,
        frame=scenario.frames[0],
        turn_index=1,
        characters={"joao": joao, "samuel": samuel},
    )

    assert "private_inspiration" not in prompt
    assert "BR" not in prompt
    assert "US" not in prompt
