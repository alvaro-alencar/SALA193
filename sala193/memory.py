from __future__ import annotations

from sala193.models import Character, MemoryEntry, Relationship, RelationshipDelta, SimulationEvent


def ensure_relationship(character: Character, other_id: str) -> Relationship:
    if other_id not in character.relationships:
        character.relationships[other_id] = Relationship()
    return character.relationships[other_id]


def apply_relationship_deltas(characters: dict[str, Character], event: SimulationEvent) -> None:
    for relationship_delta in event.relationship_deltas:
        source = characters.get(relationship_delta.source)
        if source is None:
            continue
        current = ensure_relationship(source, relationship_delta.target)
        source.relationships[relationship_delta.target] = current.apply_delta(relationship_delta.delta)


def append_memories(characters: dict[str, Character], event: SimulationEvent) -> None:
    participants = [event.actor]
    if event.target and event.target not in participants:
        participants.append(event.target)

    for participant_id in participants:
        character = characters.get(participant_id)
        if character is None:
            continue
        character.memories.append(
            MemoryEntry(
                event_id=event.id,
                summary=event.outcome,
                participants=participants,
                emotional_impact=_emotional_impact_for(character.id, event),
                interpretation=_interpretation_for(character.id, event),
                confidence=0.84,
                secrecy="public",
                tags=event.memory_tags,
            )
        )


def _emotional_impact_for(character_id: str, event: SimulationEvent) -> dict[str, float]:
    impact: dict[str, float] = {}

    if event.action_type.value in {"offer", "protect"}:
        impact["gratitude"] = 0.24
        impact["suspicion"] = 0.16

    if event.action_type.value in {"humiliate", "threaten"}:
        impact["anger"] = 0.35
        impact["fear"] = 0.23

    if event.target == character_id and "debt" in event.memory_tags:
        impact["humiliation"] = 0.32

    return impact


def _interpretation_for(character_id: str, event: SimulationEvent) -> str:
    if event.target == character_id and event.action_type.value == "offer":
        return "He helped me, but he made sure the room saw it."
    if event.actor == character_id and event.hidden_intention:
        return "I did not say the real reason out loud."
    return "I will remember how the room felt when this happened."
