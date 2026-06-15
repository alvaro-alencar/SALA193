from __future__ import annotations

from sala193.models import ActionType, Character, ProposedAction, SceneFrame


def choose_target(actor: Character, frame: SceneFrame) -> str | None:
    for participant in frame.participants:
        if participant != actor.id:
            return participant
    return None


def propose_action(actor: Character, frame: SceneFrame, turn_index: int) -> ProposedAction:
    """Return a deterministic first-pass action proposal.

    This is intentionally simple. The MVP needs visible behavior before LLM-driven
    agency. Later, this function becomes an adapter boundary.
    """

    target = choose_target(actor, frame)
    temperament = actor.temperament
    resources = actor.resources
    emotion = actor.emotional_state

    if target is None:
        return ProposedAction(
            actor=actor.id,
            action_type=ActionType.LEAVE,
            visible_intention=f"{actor.public_name} steps away from the room.",
            emotional_tone=emotion.dominant,
        )

    relationship = actor.relationships.get(target)
    resentment = relationship.resentment if relationship else 0.0
    debt = relationship.debt if relationship else 0.0
    trust = relationship.trust if relationship else 0.5

    if emotion.stress > 0.74 and temperament.aggression > 0.55:
        return ProposedAction(
            actor=actor.id,
            target=target,
            action_type=ActionType.THREATEN,
            visible_intention=f"{actor.public_name} warns {target} not to push him further.",
            hidden_intention="regain control of the room through fear",
            intensity=min(1.0, emotion.stress + temperament.aggression / 3),
            risk=0.72,
            emotional_tone="cornered",
        )

    if resentment > 0.55 and trust < 0.45:
        return ProposedAction(
            actor=actor.id,
            target=target,
            action_type=ActionType.REFUSE,
            visible_intention=f"{actor.public_name} refuses help before the offer is even finished.",
            hidden_intention="avoid looking dependent",
            intensity=0.64,
            risk=0.41,
            emotional_tone="defensive",
        )

    if resources.money > 0.68 and resources.social_capital > 0.55 and temperament.ambition > 0.55:
        return ProposedAction(
            actor=actor.id,
            target=target,
            action_type=ActionType.OFFER,
            visible_intention=f"{actor.public_name} offers to solve the immediate problem in front of everyone.",
            hidden_intention="turn help into leverage",
            intensity=0.66,
            risk=0.48,
            emotional_tone="confident",
        )

    if debt > 0.45 and temperament.pride > 0.5:
        return ProposedAction(
            actor=actor.id,
            target=target,
            action_type=ActionType.LEAVE,
            visible_intention=f"{actor.public_name} makes a joke and tries to leave before the conversation gets serious.",
            hidden_intention="escape humiliation",
            intensity=0.43,
            risk=0.27,
            emotional_tone="evasive",
        )

    if temperament.sociability > 0.65:
        return ProposedAction(
            actor=actor.id,
            target=target,
            action_type=ActionType.TALK,
            visible_intention=f"{actor.public_name} tries to keep the conversation light while watching everyone's face.",
            hidden_intention="measure the room before choosing a side",
            intensity=0.37,
            risk=0.2,
            emotional_tone="warm but alert",
        )

    return ProposedAction(
        actor=actor.id,
        target=target,
        action_type=ActionType.TALK,
        visible_intention=f"{actor.public_name} answers carefully and reveals almost nothing.",
        hidden_intention="preserve room to maneuver",
        intensity=0.33,
        risk=0.18,
        emotional_tone="guarded",
    )
