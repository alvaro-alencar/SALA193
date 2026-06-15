from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator


Score = float


class Mode(str, Enum):
    STORY = "story"
    ANALYSIS = "analysis"
    WRITERS_ROOM = "writers_room"


class AgeBand(str, Enum):
    CHILD = "child"
    TEEN = "teen"
    ADULT = "adult"
    ELDER = "elder"
    ANCIENT = "ancient"


class ActionType(str, Enum):
    TALK = "talk"
    OFFER = "offer"
    REQUEST = "request"
    REFUSE = "refuse"
    THREATEN = "threaten"
    APOLOGIZE = "apologize"
    EXPOSE_SECRET = "expose_secret"
    HIDE_INFORMATION = "hide_information"
    LEAVE = "leave"
    ESCALATE = "escalate"
    PROTECT = "protect"
    HUMILIATE = "humiliate"
    RECONCILE = "reconcile"


class SpeechStyle(BaseModel):
    rhythm: str = "natural"
    traits: list[str] = Field(default_factory=list)
    favorite_phrases: list[str] = Field(default_factory=list)
    avoids: list[str] = Field(default_factory=list)


class Temperament(BaseModel):
    openness: Score = Field(default=0.5, ge=0, le=1)
    discipline: Score = Field(default=0.5, ge=0, le=1)
    sociability: Score = Field(default=0.5, ge=0, le=1)
    aggression: Score = Field(default=0.5, ge=0, le=1)
    suspicion: Score = Field(default=0.5, ge=0, le=1)
    ambition: Score = Field(default=0.5, ge=0, le=1)
    patience: Score = Field(default=0.5, ge=0, le=1)
    shame_sensitivity: Score = Field(default=0.5, ge=0, le=1)
    risk_tolerance: Score = Field(default=0.5, ge=0, le=1)
    loyalty: Score = Field(default=0.5, ge=0, le=1)
    pride: Score = Field(default=0.5, ge=0, le=1)
    mercy: Score = Field(default=0.5, ge=0, le=1)


class Resources(BaseModel):
    money: Score = Field(default=0.5, ge=0, le=1)
    social_capital: Score = Field(default=0.5, ge=0, le=1)
    coercive_power: Score = Field(default=0.5, ge=0, le=1)
    institutional_access: Score = Field(default=0.5, ge=0, le=1)
    cultural_influence: Score = Field(default=0.5, ge=0, le=1)
    technical_skill: Score = Field(default=0.5, ge=0, le=1)
    family_network: Score = Field(default=0.5, ge=0, le=1)
    information: Score = Field(default=0.5, ge=0, le=1)
    mobility: Score = Field(default=0.5, ge=0, le=1)
    resilience: Score = Field(default=0.5, ge=0, le=1)


class MoralBoundaries(BaseModel):
    lie: Score = Field(default=0.3, ge=0, le=1)
    betray: Score = Field(default=0.2, ge=0, le=1)
    abandon: Score = Field(default=0.2, ge=0, le=1)
    humiliate: Score = Field(default=0.2, ge=0, le=1)
    exploit: Score = Field(default=0.2, ge=0, le=1)
    threaten: Score = Field(default=0.2, ge=0, le=1)
    injure: Score = Field(default=0.1, ge=0, le=1)
    kill: Score = Field(default=0.05, ge=0, le=1)


class Relationship(BaseModel):
    trust: Score = Field(default=0.5, ge=0, le=1)
    fear: Score = Field(default=0.0, ge=0, le=1)
    admiration: Score = Field(default=0.0, ge=0, le=1)
    resentment: Score = Field(default=0.0, ge=0, le=1)
    debt: Score = Field(default=0.0, ge=0, le=1)
    intimacy: Score = Field(default=0.0, ge=0, le=1)
    dependency: Score = Field(default=0.0, ge=0, le=1)
    rivalry: Score = Field(default=0.0, ge=0, le=1)
    attraction: Score = Field(default=0.0, ge=0, le=1)
    guilt: Score = Field(default=0.0, ge=0, le=1)
    protectiveness: Score = Field(default=0.0, ge=0, le=1)

    def apply_delta(self, delta: dict[str, float]) -> "Relationship":
        data = self.model_dump()
        for key, value in delta.items():
            if key in data:
                data[key] = min(1.0, max(0.0, data[key] + value))
        return Relationship(**data)


class EmotionalState(BaseModel):
    dominant: str = "neutral"
    stress: Score = Field(default=0.2, ge=0, le=1)
    shame: Score = Field(default=0.0, ge=0, le=1)
    anger: Score = Field(default=0.0, ge=0, le=1)
    fear: Score = Field(default=0.0, ge=0, le=1)
    hope: Score = Field(default=0.5, ge=0, le=1)


class MemoryEntry(BaseModel):
    event_id: str
    summary: str
    participants: list[str]
    emotional_impact: dict[str, Score] = Field(default_factory=dict)
    interpretation: str = ""
    confidence: Score = Field(default=1.0, ge=0, le=1)
    secrecy: Literal["public", "private", "secret", "rumor"] = "public"
    tags: list[str] = Field(default_factory=list)


class Character(BaseModel):
    id: str
    public_name: str
    private_inspiration: str | None = None
    age_band: AgeBand = AgeBand.ADULT
    social_position: str = "ordinary person"
    ordinary_life_anchor: str = "neighborhood regular"
    speech_style: SpeechStyle = Field(default_factory=SpeechStyle)
    temperament: Temperament = Field(default_factory=Temperament)
    needs: list[str] = Field(default_factory=list)
    fears: list[str] = Field(default_factory=list)
    wounds: list[str] = Field(default_factory=list)
    ambitions: list[str] = Field(default_factory=list)
    addictions: list[str] = Field(default_factory=list)
    recurring_mistakes: list[str] = Field(default_factory=list)
    forbidden_desires: list[str] = Field(default_factory=list)
    resources: Resources = Field(default_factory=Resources)
    boundaries: MoralBoundaries = Field(default_factory=MoralBoundaries)
    relationships: dict[str, Relationship] = Field(default_factory=dict)
    emotional_state: EmotionalState = Field(default_factory=EmotionalState)
    memories: list[MemoryEntry] = Field(default_factory=list)
    behavioral_rules: list[str] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("character id cannot be empty")
        return value.strip().lower().replace(" ", "_")

    def public_dict(self, mode: Mode = Mode.STORY) -> dict[str, Any]:
        data = self.model_dump()
        if mode == Mode.STORY:
            data.pop("private_inspiration", None)
        return data

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Character":
        with Path(path).open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return cls(**data)


class SceneFrame(BaseModel):
    id: str
    location: str
    time: str
    participants: list[str]
    pressure: str
    dramatic_question: str
    context: str = ""
    available_actions: list[ActionType] = Field(default_factory=lambda: [
        ActionType.TALK,
        ActionType.OFFER,
        ActionType.REQUEST,
        ActionType.REFUSE,
        ActionType.LEAVE,
    ])


class Scenario(BaseModel):
    id: str
    title: str
    pov: str = "joao"
    frames: list[SceneFrame]

    @model_validator(mode="after")
    def validate_frames(self) -> "Scenario":
        if not self.frames:
            raise ValueError("scenario must contain at least one frame")
        return self

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Scenario":
        with Path(path).open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return cls(**data)


class ProposedAction(BaseModel):
    actor: str
    target: str | None = None
    action_type: ActionType
    visible_intention: str
    hidden_intention: str = ""
    intensity: Score = Field(default=0.5, ge=0, le=1)
    risk: Score = Field(default=0.3, ge=0, le=1)
    emotional_tone: str = "neutral"


class RelationshipDelta(BaseModel):
    source: str
    target: str
    delta: dict[str, float]


class SimulationEvent(BaseModel):
    id: str
    turn: int
    scene_id: str
    actor: str
    target: str | None = None
    action_type: ActionType
    visible_action: str
    hidden_intention: str = ""
    outcome: str
    relationship_deltas: list[RelationshipDelta] = Field(default_factory=list)
    memory_tags: list[str] = Field(default_factory=list)
    future_hooks: list[str] = Field(default_factory=list)


class SimulationLog(BaseModel):
    scenario_id: str
    events: list[SimulationEvent] = Field(default_factory=list)

    def as_jsonl(self) -> str:
        return "\n".join(event.model_dump_json() for event in self.events)
