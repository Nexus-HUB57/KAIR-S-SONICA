from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

try:
    from pydantic import field_validator
except ImportError:  # Pydantic v1 compatibility for lightweight environments.
    from pydantic import validator as field_validator


class TrackRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2_000)
    route_id: str = Field(default="default", min_length=1, max_length=120)
    artist_id: str = Field(default="kairos.khairus_the_dragon", min_length=1, max_length=120)
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
    result: dict[str, Any] | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GenerateResponse(BaseModel):
    task_id: str
    status: Literal["PENDING", "RUNNING", "SUCCEEDED", "FAILED"]


class PersonaResponse(BaseModel):
    id: str
    name: str
    version: str
    language: str
    mission: str
    identity: str
    roles: list[str]
    capabilities: list[str]
    operating_principles: list[str]
    pipeline: list[str]
    output_contract: list[str]
    guardrails: list[str]
    system_prompt: str


class VideoRequest(BaseModel):
    """Parâmetros portáveis para o backend opcional SkyReels-V2."""

    prompt: str = Field(min_length=1, max_length=4_000)
    mode: Literal["t2v", "i2v", "extend", "start_end"] = "t2v"
    engine: Literal["diffusion_forcing", "standard"] = "diffusion_forcing"
    backend: Literal["cli", "native"] = "cli"
    model_id: str | None = Field(default=None, min_length=1, max_length=500)
    resolution: Literal["540P", "720P"] = "540P"
    num_frames: int | None = Field(default=None, ge=1, le=1_457)
    base_num_frames: int | None = Field(default=None, ge=1, le=1_457)
    overlap_history: int | None = Field(default=None, ge=1, le=300)
    addnoise_condition: int = Field(default=20, ge=0, le=60)
    ar_step: int = Field(default=0, ge=0, le=100)
    causal_block_size: int = Field(default=1, ge=1, le=32)
    inference_steps: int = Field(default=30, ge=1, le=200)
    fps: int = Field(default=24, ge=1, le=120)
    guidance_scale: float = Field(default=6.0, ge=0, le=30)
    shift: float = Field(default=8.0, ge=0, le=30)
    image_path: str | None = Field(default=None, max_length=500)
    end_image_path: str | None = Field(default=None, max_length=500)
    video_path: str | None = Field(default=None, max_length=500)
    seed: int | None = Field(default=None, ge=0, le=2**32 - 2)
    offload: bool = True
    prompt_enhancer: bool = False
    teacache: bool = False
    teacache_thresh: float = Field(default=0.2, gt=0, le=1)
    use_ret_steps: bool = False
    use_usp: bool = False


class MultimediaRequest(BaseModel):
    prompt: str | None = Field(default=None, max_length=2_000)
    route_id: str = Field(default="default", min_length=1, max_length=120)
    artist_id: str = Field(default="kairos.khairus_the_dragon", min_length=1, max_length=120)
    audio_path: str | None = Field(default=None, max_length=500)
    transcribe: bool = True
    transcription_backend: Literal["sidecar", "faster-whisper"] | None = None
    transcription_model: str | None = Field(default=None, min_length=1, max_length=80)
    transcription_language: str | None = Field(default=None, max_length=16)
    analyze_audio: bool = True
    generate_audio: bool = True
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
    def normalize_multimedia_scale(cls, value: str) -> str:
        value = value.strip().lower()
        aliases = {"m": "minor", "min": "minor", "maj": "major"}
        return aliases.get(value, value)


class MultimediaResult(BaseModel):
    task_id: str
    status: Literal["PENDING", "RUNNING", "SUCCEEDED", "FAILED"]
    artifact_url: str | None = None
    transcript_url: str | None = None
    metadata_url: str | None = None
    result: dict[str, Any] | None = None
