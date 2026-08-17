from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    """Configuração pequena e explícita para desenvolvimento local e containers."""

    environment: str = "development"
    output_dir: Path = Path("data/output")
    sample_rate: int = 44_100
    ffmpeg_bin: str = "ffmpeg"
    enable_external_models: bool = False

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            environment=os.getenv("KAIROS_ENV", "development"),
            output_dir=Path(os.getenv("KAIROS_OUTPUT_DIR", "data/output")),
            sample_rate=int(os.getenv("KAIROS_DEFAULT_SAMPLE_RATE", "44100")),
            ffmpeg_bin=os.getenv("KAIROS_FFMPEG_BIN", "ffmpeg"),
            enable_external_models=os.getenv("KAIROS_ENABLE_EXTERNAL_MODELS", "false").lower()
            in {"1", "true", "yes", "on"},
        )

    def ensure_directories(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
