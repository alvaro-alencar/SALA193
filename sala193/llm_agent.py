from __future__ import annotations

import json
from typing import Protocol

from pydantic import ValidationError

from sala193.models import Character, Mode, ProposedAction, SceneFrame


class LLMClient(Protocol):
    """Provider-independent structured model client."""

    def complete_json(self, prompt: str) -> dict:
        ...


class LLMAgentAdapter:
    """The player's AI: chooses an action, not its consequences."""

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
        prompt = build_agent_prompt(
            actor=actor, frame=frame, turn_index=turn_index, characters=characters,
        )
        try:
            action = ProposedAction.model_validate(self.client.complete_json(prompt))
        except ValidationError as exc:
            raise ValueError(f"LLM returned an invalid action: {exc}") from exc

        if action.actor != actor.id:
            raise ValueError("LLM tried to act as a different character")

        allowed_targets = set(frame.participants) - {actor.id}
        if action.target is not None and action.target not in allowed_targets:
            raise ValueError("LLM chose a target outside this scene")

        if action.action_type not in frame.available_actions:
            raise ValueError("LLM chose an action not available in this scene")

        return action


def build_agent_prompt(
    actor: Character,
    frame: SceneFrame,
    turn_index: int,
    characters: dict[str, Character],
) -> str:
    """Give one actor its own inner life, never another actor's private state."""
    actor_sheet = actor.public_dict(mode=Mode.STORY)
    actor_sheet["memories"] = [
        memory.model_dump(mode="json") for memory in actor.memories[-8:]
    ]
    actor_sheet["relationships"] = {
        other_id: relation.model_dump(mode="json")
        for other_id, relation in actor.relationships.items()
        if other_id in frame.participants and other_id != actor.id
    }

    others = [
        {
            "id": other.id,
            "public_name": other.public_name,
            "social_position": other.social_position,
            "ordinary_life_anchor": other.ordinary_life_anchor,
        }
        for other in characters.values()
        if other.id in frame.participants and other.id != actor.id
    ]

    payload = {
        "task": (
            "Você é o JOGADOR deste personagem num RPG de convivência. "
            "Decida uma única ação e uma fala breve, sem determinar o resultado. "
            "Responda apenas em JSON, com os campos especificados."
        ),
        "rules": [
            "Todos os textos e falas devem estar em português brasileiro.",
            "Nunca mencione países, nações, geopolítica ou inspirações históricas.",
            "Não revele sua intenção oculta em dialogue.",
            "Não declare o resultado da ação: somente a intenção e a fala.",
            "Você conhece suas próprias memórias, mas não as memórias ou intenções dos demais.",
            "A ação precisa estar entre as disponíveis nesta cena.",
            "As falas devem soar naturais, específicas, sem discursos explicativos.",
        ],
        "fields": {
            "actor": actor.id,
            "target": "outro participante ou null",
            "action_type": [action.value for action in frame.available_actions],
            "visible_intention": "ação pretendida, descritiva, sem resultado",
            "hidden_intention": "motivação íntima não dita, ou string vazia",
            "intensity": "número de 0 a 1",
            "risk": "número de 0 a 1",
            "emotional_tone": "emoção predominante",
            "dialogue": "frase curta que o personagem efetivamente diz, ou string vazia",
        },
        "turn_index": turn_index,
        "scene": frame.model_dump(mode="json"),
        "you": actor_sheet,
        "others_visible": others,
    }

    return json.dumps(payload, ensure_ascii=False, indent=2)
