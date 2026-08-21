from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ArrangementStyle = Literal[
    "boom_bap",
    "brazilian_funk_heavy",
    "brazilian_funk_swing",
    "vocal_focus",
]
Mood = Literal["energetic", "focused", "reflective", "cinematic"]


class ArrangementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    style: ArrangementStyle = "boom_bap"
    mood: Mood = "energetic"
    bpm: float = Field(default=140, ge=40, le=240)
    total_bars: int = Field(default=32, ge=4, le=256)
    key: str = Field(default="C#", min_length=1, max_length=12)


class ArrangementSection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=80)
    bars: int = Field(ge=1, le=64)
    energy: float = Field(ge=0, le=1)
    instruments: list[str] = Field(min_length=1, max_length=24)
    automation: dict[str, float] = Field(default_factory=dict, max_length=12)


class ArrangementPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    status: Literal["READY_FOR_APPROVAL"] = "READY_FOR_APPROVAL"
    method: str = Field(default="rule-based-arrangement/v1", max_length=120)
    style: ArrangementStyle
    mood: Mood
    bpm: float = Field(ge=40, le=240)
    total_bars: int = Field(ge=4, le=256)
    key: str = Field(min_length=1, max_length=12)
    sections: list[ArrangementSection] = Field(min_length=1, max_length=32)
    warnings: list[str] = Field(default_factory=list, max_length=20)

    @model_validator(mode="after")
    def validate_bar_budget(self) -> ArrangementPlan:
        if sum(section.bars for section in self.sections) != self.total_bars:
            raise ValueError("A soma das seções deve ser igual a total_bars")
        return self


class ExpressiveNote(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pitch: int = Field(ge=0, le=127)
    time_beats: float = Field(ge=0, le=100_000)
    duration_beats: float = Field(gt=0, le=64)
    velocity: int = Field(default=80, ge=1, le=127)
    channel: int = Field(default=0, ge=0, le=15)


class HumanExpressionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    notes: list[ExpressiveNote] = Field(min_length=1, max_length=20_000)
    energy_map: dict[int, float] = Field(default_factory=dict, max_length=256)
    bpm: float = Field(default=140, ge=40, le=240)
    swing_ratio: float = Field(default=0.60, ge=0.50, le=0.67)
    humanize_ms: float = Field(default=2.0, ge=0, le=10)
    seed: int = Field(default=0, ge=0, le=2_147_483_647)


class HumanExpressionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    method: str = Field(default="deterministic-expression/v1", max_length=120)
    notes: list[ExpressiveNote] = Field(min_length=1, max_length=20_000)
    applied_swing_ratio: float = Field(ge=0.50, le=0.67)
    max_timing_shift_ms: float = Field(ge=0, le=10)
    warnings: list[str] = Field(default_factory=list, max_length=20)


class HumPitchFrame(BaseModel):
    model_config = ConfigDict(extra="forbid")

    time_seconds: float = Field(ge=0, le=600)
    frequency_hz: float = Field(ge=0, le=20_000)
    confidence: float = Field(ge=0, le=1)


class HumToMidiRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    frames: list[HumPitchFrame] = Field(min_length=1, max_length=20_000)
    min_confidence: float = Field(default=0.70, ge=0, le=1)
    min_frequency_hz: float = Field(default=80, ge=20, le=2_000)
    max_gap_seconds: float = Field(default=0.18, ge=0.01, le=2)


class SketchNote(BaseModel):
    model_config = ConfigDict(extra="forbid")

    midi_note: int = Field(ge=0, le=127)
    start_seconds: float = Field(ge=0, le=600)
    end_seconds: float = Field(gt=0, le=600)
    confidence: float = Field(ge=0, le=1)


class HumToMidiResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    status: Literal["READY_FOR_APPROVAL"] = "READY_FOR_APPROVAL"
    method: str = Field(default="pitch-contour-to-midi/v1", max_length=120)
    notes: list[SketchNote] = Field(default_factory=list, max_length=2_000)
    midi_export: Literal["not-generated", "adapter-required"] = "not-generated"
    warnings: list[str] = Field(default_factory=list, max_length=20)


class SignatureModeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intensity: float = Field(default=0.65, ge=0, le=1)
    vocal_presence: float = Field(default=0.70, ge=0, le=1)
    low_end_focus: float = Field(default=0.65, ge=0, le=1)
    spatial_depth: float = Field(default=0.35, ge=0, le=1)
    target: Literal["audio_input", "mix_bus", "vocal_bus"] = "audio_input"


class SignatureModePlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    status: Literal["READY_FOR_APPROVAL"] = "READY_FOR_APPROVAL"
    mode: Literal["kairos_signature"] = "kairos_signature"
    target: str
    chain: list[dict[str, Any]] = Field(min_length=3, max_length=12)
    guardrails: dict[str, Any]
    provenance: dict[str, Any]
    warnings: list[str] = Field(default_factory=list, max_length=20)


class ViralClipPlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(default="DJ Káiros | StudioMaster", min_length=1, max_length=120)
    duration_seconds: int = Field(default=15, ge=5, le=60)
    aspect_ratio: Literal["9:16", "1:1", "16:9"] = "9:16"
    platform: Literal["tiktok", "reels", "shorts", "generic"] = "generic"
    watermark: str = Field(default="@DJKairos | AI Studio", max_length=80)
    audio_asset_id: str | None = Field(default=None, max_length=160)


class AutoRetrainStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool
    ready: bool
    status: Literal["DISABLED", "WAITING_MANIFEST", "READY_FOR_APPROVAL", "BLOCKED"]
    dataset_manifest: str | None = None
    required_approvals: list[str] = Field(default_factory=list, max_length=12)
    warnings: list[str] = Field(default_factory=list, max_length=20)


class DuckingPreviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mix_bus: list[float] = Field(min_length=1, max_length=100_000)
    reference_track: list[float] = Field(min_length=1, max_length=100_000)
    strength: float = Field(default=0.5, ge=0, le=1)
    window_size: int = Field(default=1_024, ge=8, le=16_384)


class SignalHealthRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    samples: list[float] = Field(min_length=1, max_length=250_000)
    target_score: float = Field(default=4.0, ge=0, le=5)


class MemoryFeedbackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    context: str = Field(min_length=1, max_length=500)
    adjustments: dict[str, Any] = Field(max_length=64)
    project_id: str | None = Field(default=None, max_length=160)


class ProductionRecordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str = Field(min_length=1, max_length=160)
    genre: str = Field(default="unknown", min_length=1, max_length=120)
    bpm: float | None = Field(default=None, ge=40, le=240)
    mos_score: float | None = Field(default=None, ge=0, le=5)
    master_asset_id: str | None = Field(default=None, max_length=160)
    approved: bool = False


class ProductionAnalytics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    source: Literal["empty", "production_history"]
    total_productions: int = Field(ge=0)
    average_mos: float | None = Field(default=None, ge=0, le=5)
    genres: dict[str, int] = Field(default_factory=dict, max_length=100)
    latest: list[dict[str, Any]] = Field(default_factory=list, max_length=20)
    feedback_proposals: int = Field(default=0, ge=0)
    auto_retrain: dict[str, Any]
