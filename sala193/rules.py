from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from sala193.models import Character, ProposedAction, SceneFrame


@dataclass(frozen=True)
class DramaticRoll:
    """Deterministic RPG-like roll used by the Game Master.

    The goal is not realism. The goal is repeatable dramatic arbitration.
    Given the same scene, actor and action, the roll stays stable enough for tests
    and debuggable simulations.
    """

    seed: str
    roll: float
    pressure: float
    advantage: float
    score: float
    success: bool

    def as_dict(self) -> dict[str, float | str | bool]:
        return {
            "seed": self.seed,
            "roll": round(self.roll, 4),
            "pressure": round(self.pressure, 4),
            "advantage": round(self.advantage, 4),
            "score": round(self.score, 4),
            "success": self.success,
        }


def clamp(value: float, floor: float = 0.0, ceiling: float = 1.0) -> float:
    return min(ceiling, max(floor, value))


def stable_roll(seed: str) -> float:
    digest = sha256(seed.encode("utf-8")).hexdigest()
    integer = int(digest[:12], 16)
    return (integer % 10_000) / 10_000


def dramatic_check(
    actor: Character,
    target: Character | None,
    action: ProposedAction,
    frame: SceneFrame,
    turn_index: int,
) -> DramaticRoll:
    """Resolve a human-scale action with psychological pressure.

    This works like a tiny RPG system:
    - the actor brings temperament and resources;
    - the relationship brings trust, fear, debt or resentment;
    - the scene brings pressure;
    - the deterministic roll brings uncertainty without test flakiness.
    """

    relationship = actor.relationships.get(target.id) if target else None

    social_force = (
        actor.resources.social_capital * 0.22
        + actor.resources.money * 0.16
        + actor.resources.coercive_power * 0.12
        + actor.temperament.ambition * 0.14
        + actor.temperament.discipline * 0.10
        + actor.temperament.sociability * 0.10
    )

    relational_force = 0.0
    if relationship:
        relational_force += relationship.trust * 0.10
        relational_force += relationship.fear * 0.08
        relational_force += relationship.debt * 0.12
        relational_force -= relationship.resentment * 0.10
        relational_force -= relationship.rivalry * 0.08

    pressure = clamp(0.25 + action.risk * 0.35 + actor.emotional_state.stress * 0.25)
    advantage = clamp(social_force + relational_force)
    seed = f"{frame.id}:{turn_index}:{actor.id}:{target.id if target else 'none'}:{action.action_type.value}:{action.visible_intention}"
    roll = stable_roll(seed)
    score = clamp(advantage + action.intensity * 0.25 + roll * 0.20 - pressure * 0.20)
    success = score >= 0.48

    return DramaticRoll(
        seed=seed,
        roll=roll,
        pressure=pressure,
        advantage=advantage,
        score=score,
        success=success,
    )
