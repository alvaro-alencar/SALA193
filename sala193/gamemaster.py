from __future__ import annotations

from sala193.models import (
    ActionType,
    Character,
    ProposedAction,
    RelationshipDelta,
    SceneFrame,
    SimulationEvent,
)
from sala193.rules import dramatic_check


class GameMaster:
    """Arbitrates consequences for agent actions.

    Agents decide what they try to do.
    The Game Master decides what the room does back.
    """

    def resolve(
        self,
        action: ProposedAction,
        frame: SceneFrame,
        turn_index: int,
        event_id: str,
        characters: dict[str, Character],
    ) -> SimulationEvent:
        actor = characters[action.actor]
        target = characters.get(action.target) if action.target else None
        target_name = target.public_name if target else action.target
        roll = dramatic_check(actor, target, action, frame, turn_index)

        outcome = self._outcome_text(action, actor.public_name, target_name, roll.success)
        deltas = self._relationship_deltas(action, roll.success)
        tags = self._memory_tags(action, roll.success)
        hooks = self._future_hooks(action, actor.public_name, target_name, roll.success)

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
            resolution=roll.as_dict(),
        )

    def _relationship_deltas(self, action: ProposedAction, success: bool) -> list[RelationshipDelta]:
        if action.target is None:
            return []

        actor_to_target: dict[str, float] = {}
        target_to_actor: dict[str, float] = {}
        multiplier = 1.0 if success else 0.55
        backlash = 0.0 if success else 0.06

        match action.action_type:
            case ActionType.OFFER:
                actor_to_target = {
                    "protectiveness": 0.08 * multiplier,
                    "dependency": 0.07 * multiplier,
                    "admiration": 0.03 * multiplier,
                }
                target_to_actor = {
                    "debt": 0.18 * multiplier,
                    "trust": 0.04 * multiplier - backlash,
                    "resentment": 0.07 + backlash,
                    "dependency": 0.09 * multiplier,
                }
            case ActionType.TALK:
                actor_to_target = {"trust": 0.02 * multiplier, "intimacy": 0.02 * multiplier}
                target_to_actor = {"trust": 0.02 * multiplier}
            case ActionType.REFUSE:
                actor_to_target = {"resentment": 0.05, "rivalry": 0.03}
                target_to_actor = {"resentment": 0.04, "admiration": 0.02 * multiplier}
            case ActionType.THREATEN:
                actor_to_target = {"fear": 0.08 * multiplier, "rivalry": 0.06}
                target_to_actor = {"fear": 0.16 * multiplier, "resentment": 0.11, "trust": -0.12}
            case ActionType.HUMILIATE:
                actor_to_target = {"rivalry": 0.07}
                target_to_actor = {"resentment": 0.18, "trust": -0.14, "fear": 0.06 * multiplier}
            case ActionType.APOLOGIZE | ActionType.RECONCILE:
                actor_to_target = {"guilt": -0.08 * multiplier, "trust": 0.04 * multiplier}
                target_to_actor = {"trust": 0.07 * multiplier, "resentment": -0.06 * multiplier}
            case ActionType.PROTECT:
                actor_to_target = {"protectiveness": 0.14 * multiplier}
                target_to_actor = {"trust": 0.08 * multiplier, "debt": 0.10 * multiplier, "dependency": 0.08 * multiplier}
            case _:
                actor_to_target = {"trust": -0.01}
                target_to_actor = {"trust": -0.01}

        return [
            RelationshipDelta(source=action.actor, target=action.target, delta=actor_to_target),
            RelationshipDelta(source=action.target, target=action.actor, delta=target_to_actor),
        ]

    def _memory_tags(self, action: ProposedAction, success: bool) -> list[str]:
        tags = [action.action_type.value]
        if not success:
            tags.append("failed_attempt")
        if action.action_type in {ActionType.OFFER, ActionType.PROTECT}:
            tags.extend(["favor", "debt", "public_pressure"])
        if action.action_type in {ActionType.THREATEN, ActionType.HUMILIATE}:
            tags.extend(["fear", "shame", "rupture"])
        return tags

    def _future_hooks(
        self,
        action: ProposedAction,
        actor_name: str,
        target_name: str | None,
        success: bool,
    ) -> list[str]:
        if target_name is None:
            return []
        match action.action_type:
            case ActionType.OFFER:
                if success:
                    return [f"{target_name} may resist {actor_name}'s next request to avoid feeling owned."]
                return [f"{actor_name}'s help did not land cleanly; {target_name} may read the favor as a trap."]
            case ActionType.THREATEN:
                return [f"{target_name} may look for protection elsewhere."]
            case ActionType.REFUSE:
                return [f"{actor_name}'s refusal may become a public embarrassment."]
            case _:
                return []

    def _outcome_text(
        self,
        action: ProposedAction,
        actor_name: str,
        target_name: str | None,
        success: bool,
    ) -> str:
        if target_name is None:
            return f"{actor_name} leaves the scene without explaining why."

        match action.action_type:
            case ActionType.OFFER:
                if success:
                    return f"{actor_name} helps before {target_name} can refuse, and the room notices the favor."
                return f"{actor_name} tries to help too quickly; {target_name} smiles, but the room feels the hook."
            case ActionType.TALK:
                if success:
                    return f"{actor_name} keeps the conversation alive, but something important remains unsaid."
                return f"{actor_name} talks long enough for everyone to notice what he avoids saying."
            case ActionType.REFUSE:
                return f"{actor_name} refuses too quickly, making the refusal sound like fear."
            case ActionType.THREATEN:
                if success:
                    return f"{actor_name}'s warning changes the air in the room; {target_name} stops smiling."
                return f"{actor_name}'s warning comes out wrong; {target_name} does not smile, but does not bend either."
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
