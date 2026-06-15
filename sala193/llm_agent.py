from __future__ import annotations

import json
from typing import Protocol

from pydantic import ValidationError

from sala193.models import Character, Mode, ProposedAction, SceneFrame


class LLMClient(Protocol):
    """Minimal client contract for model providers.

    Any provider can implement this contract: OpenAI, Anthropic, local models,
    a test fake, or a future orchestration layer.
    """

    def complete_json(self, prompt: str) -> dict:
        ...


class LLMAgentAdapter:
    """Agent adapter that asks a model for a structured ProposedAction.

    This adapter does not generate prose. It generates decisions.
    The narrator remains responsible for prose.
    """

    name = "llm"

    def __init__(self, client: LLMClient):
        self.client = client

    def propose(
        self,
        actor: Character,
        frame: SceneFrame,
        turn_index: int,
        characters: dict[str, Character],
    ) -> ProposedAction:
        prompt = build_agent_prompt(actor=actor, frame=frame, turn_index=turn_index, characters=characters)
        raw = self.client.complete_json(prompt)
        try:
            action = ProposedAction(**raw)
        except ValidationError as exc:
            raise ValueError(f"LLM returned invalid ProposedAction: {exc}") from exc

        if action.actor != actor.id:
            raise ValueError(f"LLM tried to act as '{action.actor}', expected '{actor.id}'")

        allowed_targets = set(frame.participants) - {actor.id}
        if action.target is not None and action.target not in allowed_targets:
            raise ValueError(f"LLM chose invalid target: {action.target}")

        return action


def build_agent_prompt(
    actor: Character,
    frame: SceneFrame,
    turn_index: int,
    characters: dict[str, Character],
) -> str:
    visible_characters = {
        character_id: character.public_dict(mode=Mode.STORY)
        for character_id, character in characters.items()
        if character_id in frame.participants
    }

    payload = {
        "task": "Choose one action for the actor in this SALA193 tabletop scene. Return only JSON.",
        "rules": [
            "Do not write prose.",
            "Do not mention countries, nations, geopolitics, borders, empires or historical mappings.",
            "The character does not know any hidden inspiration layer.",
            "Choose a human-scale action that fits the character sheet and current scene pressure.",
            "Return a valid ProposedAction object.",
        ],
        "schema": {
            "actor": actor.id,
            "target": "one participant id or null",
            "action_type": [action.value for action in frame.available_actions],
            "visible_intention": "what others can see the actor trying to do",
            "hidden_intention": "what the actor privately wants, if any",
            "intensity": "float from 0.0 to 1.0",
            "risk": "float from 0.0 to 1.0",
            "emotional_tone": "short phrase",
        },
        "turn_index": turn_index,
        "actor_id": actor.id,
        "scene": frame.model_dump(mode="json"),
        "characters": visible_characters,
        "recent_memories": [memory.model_dump(mode="json") for memory in actor.memories[-8:]],
    }

    return json.dumps(payload, ensure_ascii=False, indent=2)
