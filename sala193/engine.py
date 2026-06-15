from __future__ import annotations

from itertools import count

from sala193.actions import propose_action
from sala193.memory import append_memories, apply_relationship_deltas
from sala193.models import (
    ActionType,
    Character,
    ProposedAction,
    RelationshipDelta,
    Scenario,
    SceneFrame,
    SimulationEvent,
    SimulationLog,
)


class SimulationEngine:
    def __init__(self, characters: list[Character], scenario: Scenario):
        self.characters = {character.id: character for character in characters}
        self.scenario = scenario
        self._event_counter = count(1)

    def run(self, turns: int = 5) -> SimulationLog:
        log = SimulationLog(scenario_id=self.scenario.id)
        for turn_index in range(1, turns + 1):
            frame = self.scenario.frames[(turn_index - 1) % len(self.scenario.frames)]
            active_characters = [
                self.characters[character_id]
                for character_id in frame.participants
                if character_id in self.characters
            ]

            for character in active_characters:
                action = propose_action(character, frame, turn_index)
                event = self.resolve_action(action, frame, turn_index)
                apply_relationship_deltas(self.characters, event)
                append_memories(self.characters, event)
                self._update_emotions(event)
                log.events.append(event)
        return log

    def resolve_action(self, action: ProposedAction, frame: SceneFrame, turn_index: int) -> SimulationEvent:
        event_id = f"e_{next(self._event_counter):04d}"
        actor = self.characters[action.actor]
        target_name = self.characters[action.target].public_name if action.target in self.characters else action.target

        outcome = self._outcome_text(action, actor.public_name, target_name)
        deltas = self._relationship_deltas(action)
        tags = self._memory_tags(action)
        hooks = self._future_hooks(action, actor.public_name, target_name)

        return SimulationEvent(
            id=event_id,
            turn=turn_index,
            scene_id=frame.id,
            actor=action.actor,
            target=action.target,
            action_type=action.action_type,
            visible_action=action.visible_intention,
            hidden_intention=action.hidden_intention,
            outcome=outcome,
            relationship_deltas=deltas,
            memory_tags=tags,
            future_hooks=hooks,
        )

    def _relationship_deltas(self, action: ProposedAction) -> list[RelationshipDelta]:
        if action.target is None:
            return []

        actor_to_target: dict[str, float] = {}
        target_to_actor: dict[str, float] = {}

        match action.action_type:
            case ActionType.OFFER:
                actor_to_target = {"protectiveness": 0.08, "dependency": 0.07, "admiration": 0.03}
                target_to_actor = {"debt": 0.18, "trust": 0.04, "resentment": 0.07, "dependency": 0.09}
            case ActionType.TALK:
                actor_to_target = {"trust": 0.02, "intimacy": 0.02}
                target_to_actor = {"trust": 0.02}
            case ActionType.REFUSE:
                actor_to_target = {"resentment": 0.05, "rivalry": 0.03}
                target_to_actor = {"resentment": 0.04, "admiration": 0.02}
            case ActionType.THREATEN:
                actor_to_target = {"fear": 0.08, "rivalry": 0.06}
                target_to_actor = {"fear": 0.16, "resentment": 0.11, "trust": -0.12}
            case ActionType.HUMILIATE:
                actor_to_target = {"rivalry": 0.07}
                target_to_actor = {"resentment": 0.18, "trust": -0.14, "fear": 0.06}
            case ActionType.APOLOGIZE | ActionType.RECONCILE:
                actor_to_target = {"guilt": -0.08, "trust": 0.04}
                target_to_actor = {"trust": 0.07, "resentment": -0.06}
            case ActionType.PROTECT:
                actor_to_target = {"protectiveness": 0.14}
                target_to_actor = {"trust": 0.08, "debt": 0.1, "dependency": 0.08}
            case _:
                actor_to_target = {"trust": -0.01}
                target_to_actor = {"trust": -0.01}

        return [
            RelationshipDelta(source=action.actor, target=action.target, delta=actor_to_target),
            RelationshipDelta(source=action.target, target=action.actor, delta=target_to_actor),
        ]

    def _memory_tags(self, action: ProposedAction) -> list[str]:
        tags = [action.action_type.value]
        if action.action_type in {ActionType.OFFER, ActionType.PROTECT}:
            tags.extend(["favor", "debt", "public_pressure"])
        if action.action_type in {ActionType.THREATEN, ActionType.HUMILIATE}:
            tags.extend(["fear", "shame", "rupture"])
        return tags

    def _future_hooks(self, action: ProposedAction, actor_name: str, target_name: str | None) -> list[str]:
        if target_name is None:
            return []
        match action.action_type:
            case ActionType.OFFER:
                return [f"{target_name} may resist {actor_name}'s next request to avoid feeling owned."]
            case ActionType.THREATEN:
                return [f"{target_name} may look for protection elsewhere."]
            case ActionType.REFUSE:
                return [f"{actor_name}'s refusal may become a public embarrassment."]
            case _:
                return []

    def _outcome_text(self, action: ProposedAction, actor_name: str, target_name: str | None) -> str:
        if target_name is None:
            return f"{actor_name} leaves the scene without explaining why."

        match action.action_type:
            case ActionType.OFFER:
                return f"{actor_name} helps before {target_name} can refuse, and the room notices the favor."
            case ActionType.TALK:
                return f"{actor_name} keeps the conversation alive, but something important remains unsaid."
            case ActionType.REFUSE:
                return f"{actor_name} refuses too quickly, making the refusal sound like fear."
            case ActionType.THREATEN:
                return f"{actor_name}'s warning changes the air in the room; {target_name} stops smiling."
            case ActionType.LEAVE:
                return f"{actor_name} escapes the conversation with a joke that convinces nobody."
            case ActionType.HUMILIATE:
                return f"{actor_name} wins the room for a second and loses something harder to name."
            case ActionType.APOLOGIZE:
                return f"{actor_name} apologizes for the small thing and avoids the real one."
            case ActionType.PROTECT:
                return f"{actor_name} protects {target_name}, but protection arrives with a handle attached."
            case _:
                return f"{actor_name} acts, and {target_name} understands less than he pretends."

    def _update_emotions(self, event: SimulationEvent) -> None:
        actor = self.characters.get(event.actor)
        target = self.characters.get(event.target) if event.target else None

        if actor and event.action_type == ActionType.OFFER:
            actor.emotional_state.dominant = "confident"
            actor.emotional_state.hope = min(1.0, actor.emotional_state.hope + 0.03)

        if target and event.action_type == ActionType.OFFER:
            target.emotional_state.dominant = "grateful and ashamed"
            target.emotional_state.shame = min(1.0, target.emotional_state.shame + 0.17)
            target.emotional_state.stress = min(1.0, target.emotional_state.stress + 0.08)

        if target and event.action_type in {ActionType.THREATEN, ActionType.HUMILIATE}:
            target.emotional_state.dominant = "cornered"
            target.emotional_state.fear = min(1.0, target.emotional_state.fear + 0.2)
            target.emotional_state.anger = min(1.0, target.emotional_state.anger + 0.14)
