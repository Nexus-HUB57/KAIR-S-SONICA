from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field

try:
    from pydantic import field_validator
except ImportError:  # Pydantic v1 compatibility for lightweight environments.
    from pydantic import validator as field_validator


class TrackRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2_000)
    genre: str = Field(default="Trap Soul", min_length=1, max_length=120)
    bpm: int = Field(default=140, ge=40, le=240)
    key: str = Field(default="C#", min_length=1, max_length=8)
    scale: str = Field(default="minor", min_length=1, max_length=24)
    lyrics: str | None = Field(default=None, max_length=20_000)
    duration_seconds: float = Field(default=8.0, ge=1.0, le=120.0)
    swing: float = Field(default=0.60, ge=0.50, le=0.67)
    humanize_ms: float = Field(default=6.0, ge=0.0, le=30.0)
    sample_rate: int = Field(default=44_100, ge=8_000, le=96_000)
    output_format: Literal["wav", "mp3"] = "wav"
    stems: bool = False
    seed: int | None = Field(default=None, ge=0, le=2**31 - 1)

    @field_validator("scale")
    @classmethod
    def normalize_scale(cls, value: str) -> str:
        value = value.strip().lower()
        aliases = {"m": "minor", "min": "minor", "maj": "major"}
        return aliases.get(value, value)


class GrooveSettings(BaseModel):
    swing: float = Field(ge=0.50, le=0.67)
    humanize_ms: float = Field(ge=0.0, le=30.0)
    subdivision: int = Field(default=2, ge=1, le=4)


class SectionPlan(BaseModel):
    name: str
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    energy: float = Field(ge=0, le=1)


class TrackPlan(BaseModel):
    request_id: str
    prompt: str
    genre: str
    bpm: int
    key: str
    scale: str
    duration_seconds: float
    lyrics: str | None = None
    groove: GrooveSettings
    sections: list[SectionPlan]


class Progress(BaseModel):
    step: str
    percent: int = Field(ge=0, le=100)
    message: str | None = None


class TaskSnapshot(BaseModel):
    task_id: str
    status: Literal["PENDING", "RUNNING", "SUCCEEDED", "FAILED"]
    progress: Progress
    artifact_url: str | None = None
    error: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GenerateResponse(BaseModel):
    task_id: str
    status: Literal["PENDING", "RUNNING", "SUCCEEDED", "FAILED"]
