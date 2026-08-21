from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

CultureLabel = Literal["US", "LATIN", "EUROPE", "BRAZILIAN_FUNK", "UNKNOWN"]
PerformanceAction = Literal[
    "SET_SWING",
    "SET_GRID_FOLLOW",
    "BOOST_PUNCHLINE",
    "PUSH_TO_LIBRARY",
    "SET_BPM",
    "RESET",
]


class OnsetPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    time_seconds: float = Field(ge=0, le=600)
    strength: float = Field(ge=0, le=1)
    kind: Literal["accent", "unknown"] = "accent"


class CultureProbability(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: CultureLabel
    probability: float = Field(ge=0, le=1)


class GrooveDna(BaseModel):
    """Resumo auditável de uma análise de groove/flow, sem alegar classificação neural."""

    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    method: str = Field(min_length=1, max_length=120)
    sample_rate: int = Field(ge=8_000, le=96_000)
    duration_seconds: float = Field(ge=0, le=600)
    bpm: float = Field(ge=40, le=240)
    swing_ratio: float = Field(ge=0.50, le=0.67)
    mean_offset_ms: float = Field(ge=-1_000, le=1_000)
    offset_std_ms: float = Field(ge=0, le=1_000)
    onset_density: float = Field(ge=0, le=500)
    rhythmic_confidence: float = Field(ge=0, le=1)
    culture: list[CultureProbability]
    canon_match: str | None = Field(default=None, max_length=120)
    onsets: list[OnsetPoint] = Field(default_factory=list, max_length=512)
    warnings: list[str] = Field(default_factory=list, max_length=20)


class GrooveAnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    samples: list[float] = Field(min_length=1, max_length=250_000)
    sample_rate: int = Field(default=44_100, ge=8_000, le=96_000)
    bpm: float = Field(default=140, ge=40, le=240)
    canon_id: str | None = Field(default=None, min_length=1, max_length=120)


class ResponsivePlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    style: str = Field(default="boom_bap", min_length=1, max_length=120)
    canon_id: str | None = Field(default=None, min_length=1, max_length=120)
    repertoire_id: str | None = Field(default=None, min_length=1, max_length=160)
    bpm: float = Field(default=140, ge=40, le=240)
    swing_ratio: float = Field(default=0.60, ge=0.50, le=0.67)
    humanize_ms: float = Field(default=6, ge=0, le=30)
    grid_follow: bool = True
    vocal_focus: bool = True
    punchline_enabled: bool = True
    flow: GrooveDna | None = None


class ResponsiveMixPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    status: Literal["READY_FOR_APPROVAL"] = "READY_FOR_APPROVAL"
    style: str
    canon: dict[str, Any]
    repertoire: dict[str, Any]
    timing: dict[str, Any]
    vocal_focus: dict[str, Any]
    handoff: dict[str, Any]
    warnings: list[str] = Field(default_factory=list)


class PerformanceCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: PerformanceAction
    value: float | bool | str | None = None
    bpm: float | None = Field(default=None, ge=40, le=240)
    reference_id: str | None = Field(default=None, max_length=160)


class PerformanceState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    session_id: str
    bpm: float = Field(ge=40, le=240)
    swing_ratio: float = Field(ge=0.50, le=0.67)
    swing_ms: float = Field(ge=-500, le=500)
    grid_follow: bool
    punchline_boost_db: float = Field(ge=0, le=12)
    reverb_reduction_db: float = Field(ge=0, le=24)
    last_action: str
    status: Literal["ACTIVE", "PENDING_APPROVAL"] = "ACTIVE"
    proposal: dict[str, Any] | None = None
    warnings: list[str] = Field(default_factory=list)
