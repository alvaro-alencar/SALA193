from __future__ import annotations

from itertools import count

from sala193.agents import AgentAdapter, RuleBasedAgentAdapter
from sala193.gamemaster import GameMaster
from sala193.memory import append_memories, apply_relationship_deltas
from sala193.models import Character, Scenario, SimulationEvent, SimulationLog


class SimulationEngine:
    """Runs a SALA193 table.

    This class is intentionally small: agents choose actions, the Game Master
    resolves consequences, and memory records what the characters will carry.
    """

    def __init__(
        self,
        characters: list[Character],
        scenario: Scenario,
        agent_adapter: AgentAdapter | None = None,
        game_master: GameMaster | None = None,
    ):
        self.characters = {character.id: character for character in characters}
        self.scenario = scenario
        self.agent_adapter = agent_adapter or RuleBasedAgentAdapter()
        self.game_master = game_master or GameMaster()
        self._event_counter = count(1)

    def run(self, turns: int = 5) -> SimulationLog:
        log = SimulationLog(scenario_id=self.scenario.id)
        for turn_index in range(1, turns + 1):
            events = self.run_turn(turn_index)
            log.events.extend(events)
        return log

    def run_turn(self, turn_index: int) -> list[SimulationEvent]:
        frame = self.scenario.frames[(turn_index - 1) % len(self.scenario.frames)]
        active_characters = [
            self.characters[character_id]
            for character_id in frame.participants
            if character_id in self.characters
        ]

        events: list[SimulationEvent] = []
        for character in active_characters:
            action = self.agent_adapter.propose(
                actor=character,
                frame=frame,
                turn_index=turn_index,
                characters=self.characters,
            )
            event = self.game_master.resolve(
                action=action,
                frame=frame,
                turn_index=turn_index,
                event_id=self._next_event_id(),
                characters=self.characters,
            )
            self.apply_event(event)
            events.append(event)
        return events

    def apply_event(self, event: SimulationEvent) -> None:
        apply_relationship_deltas(self.characters, event)
        append_memories(self.characters, event)
        self._update_emotions(event)

    def _next_event_id(self) -> str:
        return f"e_{next(self._event_counter):04d}"

    def _update_emotions(self, event: SimulationEvent) -> None:
        actor = self.characters.get(event.actor)
        target = self.characters.get(event.target) if event.target else None
        success = bool(event.resolution.get("success", True))

        if actor and event.action_type.value == "offer":
            actor.emotional_state.dominant = "confident" if success else "insistent"
            actor.emotional_state.hope = min(1.0, actor.emotional_state.hope + 0.03)

        if target and event.action_type.value == "offer":
            target.emotional_state.dominant = "grateful and ashamed" if success else "polite and suspicious"
            target.emotional_state.shame = min(1.0, target.emotional_state.shame + 0.17)
            target.emotional_state.stress = min(1.0, target.emotional_state.stress + 0.08)

        if target and event.action_type.value in {"threaten", "humiliate"}:
            target.emotional_state.dominant = "cornered"
            target.emotional_state.fear = min(1.0, target.emotional_state.fear + 0.2)
            target.emotional_state.anger = min(1.0, target.emotional_state.anger + 0.14)

        if actor and event.action_type.value == "leave":
            actor.emotional_state.dominant = "evasive"
            actor.emotional_state.stress = max(0.0, actor.emotional_state.stress - 0.03)
