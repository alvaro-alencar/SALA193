from __future__ import annotations

from typing import Protocol

from sala193.actions import propose_action
from sala193.models import Character, ProposedAction, SceneFrame


class AgentAdapter(Protocol):
    """Boundary between character sheet and player intelligence.

    In tabletop language, this is the player sitting behind the character.
    For now, the default player is deterministic. Later, this interface can call
    a local model, an API model, or a hybrid agent without changing the engine.
    """

    name: str

    def propose(
        self,
        actor: Character,
        frame: SceneFrame,
        turn_index: int,
        characters: dict[str, Character],
    ) -> ProposedAction:
        ...


class RuleBasedAgentAdapter:
    name = "rules"

    def propose(
        self,
        actor: Character,
        frame: SceneFrame,
        turn_index: int,
        characters: dict[str, Character],
    ) -> ProposedAction:
        return propose_action(actor=actor, frame=frame, turn_index=turn_index)


class PassiveAgentAdapter:
    """Useful for tests and quiet background characters."""

    name = "passive"

    def propose(
        self,
        actor: Character,
        frame: SceneFrame,
        turn_index: int,
        characters: dict[str, Character],
    ) -> ProposedAction:
        from sala193.models import ActionType

        return ProposedAction(
            actor=actor.id,
            target=None,
            action_type=ActionType.LEAVE,
            visible_intention=f"{actor.public_name} stays at the edge of the scene and says almost nothing.",
            hidden_intention="avoid becoming responsible for the room",
            intensity=0.18,
            risk=0.08,
            emotional_tone="withheld",
        )


def get_agent_adapter(name: str) -> AgentAdapter:
    normalized = name.strip().lower()
    if normalized == "rules":
        return RuleBasedAgentAdapter()
    if normalized == "passive":
        return PassiveAgentAdapter()
    raise ValueError(f"unknown agent adapter: {name}")
