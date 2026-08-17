from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    """Configuração pequena e explícita para desenvolvimento local e containers."""

    environment: str = "development"
    output_dir: Path = Path("data/output")
    upload_dir: Path = Path("data/uploads")
    sample_rate: int = 44_100
    ffmpeg_bin: str = "ffmpeg"
    transcription_backend: str = "sidecar"
    transcription_model: str = "small"
    transcription_device: str = "cpu"
    transcription_compute_type: str = "int8"
    enable_external_models: bool = False

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            environment=os.getenv("KAIROS_ENV", "development"),
            output_dir=Path(os.getenv("KAIROS_OUTPUT_DIR", "data/output")),
            upload_dir=Path(os.getenv("KAIROS_UPLOAD_DIR", "data/uploads")),
            sample_rate=int(os.getenv("KAIROS_DEFAULT_SAMPLE_RATE", "44100")),
            ffmpeg_bin=os.getenv("KAIROS_FFMPEG_BIN", "ffmpeg"),
            transcription_backend=os.getenv("KAIROS_TRANSCRIPTION_BACKEND", "sidecar"),
            transcription_model=os.getenv("KAIROS_TRANSCRIPTION_MODEL", "small"),
            transcription_device=os.getenv("KAIROS_TRANSCRIPTION_DEVICE", "cpu"),
            transcription_compute_type=os.getenv("KAIROS_TRANSCRIPTION_COMPUTE_TYPE", "int8"),
            enable_external_models=os.getenv("KAIROS_ENABLE_EXTERNAL_MODELS", "false").lower()
            in {"1", "true", "yes", "on"},
        )

    def ensure_directories(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
