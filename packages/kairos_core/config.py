from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    """Configuração pequena e explícita para desenvolvimento local e containers."""

    environment: str = "development"
    worker_mode: str = "inline"
    output_dir: Path = Path("data/output")
    upload_dir: Path = Path("data/uploads")
    task_db_path: Path = Path("data/kairos_tasks.sqlite3")
    sample_rate: int = 44_100
    ffmpeg_bin: str = "ffmpeg"
    ffprobe_bin: str = "ffprobe"
    cors_origins: tuple[str, ...] = ("http://localhost:8080", "http://127.0.0.1:8080")
    transcription_backend: str = "sidecar"
    transcription_model: str = "small"
    transcription_device: str = "cpu"
    transcription_compute_type: str = "int8"
    enable_external_models: bool = False
    enable_skyreels: bool = False
    skyreels_repo: Path | None = None
    skyreels_model_id: str | None = None
    skyreels_native_model_id: str | None = None
    skyreels_native_api: bool = False
    skyreels_device: str = "cuda"
    skyreels_dtype: str = "bfloat16"
    skyreels_cache_dir: Path | None = None
    skyreels_python: str = "python3"
    skyreels_allow_model_download: bool = False
    skyreels_keep_staging: bool = False
    skyreels_max_concurrency: int = 1
    skyreels_timeout_seconds: int = 3_600

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            environment=os.getenv("KAIROS_ENV", "development"),
            worker_mode=os.getenv("KAIROS_WORKER_MODE", "inline"),
            output_dir=Path(os.getenv("KAIROS_OUTPUT_DIR", "data/output")),
            upload_dir=Path(os.getenv("KAIROS_UPLOAD_DIR", "data/uploads")),
            task_db_path=Path(os.getenv("KAIROS_TASK_DB_PATH", "data/kairos_tasks.sqlite3")),
            sample_rate=int(os.getenv("KAIROS_DEFAULT_SAMPLE_RATE", "44100")),
            ffmpeg_bin=os.getenv("KAIROS_FFMPEG_BIN", "ffmpeg"),
            ffprobe_bin=os.getenv("KAIROS_FFPROBE_BIN", "ffprobe"),
            cors_origins=cls._csv(
                os.getenv(
                    "KAIROS_CORS_ORIGINS",
                    "http://localhost:8080,http://127.0.0.1:8080",
                )
            ),
            transcription_backend=os.getenv("KAIROS_TRANSCRIPTION_BACKEND", "sidecar"),
            transcription_model=os.getenv("KAIROS_TRANSCRIPTION_MODEL", "small"),
            transcription_device=os.getenv("KAIROS_TRANSCRIPTION_DEVICE", "cpu"),
            transcription_compute_type=os.getenv("KAIROS_TRANSCRIPTION_COMPUTE_TYPE", "int8"),
            enable_external_models=os.getenv("KAIROS_ENABLE_EXTERNAL_MODELS", "false").lower()
            in {"1", "true", "yes", "on"},
            enable_skyreels=os.getenv("KAIROS_ENABLE_SKYREELS", "false").lower()
            in {"1", "true", "yes", "on"},
            skyreels_repo=cls._optional_path(os.getenv("KAIROS_SKYREELS_REPO")),
            skyreels_model_id=os.getenv("KAIROS_SKYREELS_MODEL_ID") or None,
            skyreels_native_model_id=os.getenv("KAIROS_SKYREELS_NATIVE_MODEL_ID") or None,
            skyreels_native_api=os.getenv("KAIROS_SKYREELS_NATIVE_API", "false").lower()
            in {"1", "true", "yes", "on"},
            skyreels_device=os.getenv("KAIROS_SKYREELS_DEVICE", "cuda"),
            skyreels_dtype=os.getenv("KAIROS_SKYREELS_DTYPE", "bfloat16"),
            skyreels_cache_dir=cls._optional_path(os.getenv("KAIROS_SKYREELS_CACHE_DIR")),
            skyreels_python=os.getenv("KAIROS_SKYREELS_PYTHON", "python3"),
            skyreels_allow_model_download=os.getenv(
                "KAIROS_SKYREELS_ALLOW_MODEL_DOWNLOAD", "false"
            ).lower()
            in {"1", "true", "yes", "on"},
            skyreels_keep_staging=os.getenv("KAIROS_SKYREELS_KEEP_STAGING", "false").lower()
            in {"1", "true", "yes", "on"},
            skyreels_max_concurrency=int(os.getenv("KAIROS_SKYREELS_MAX_CONCURRENCY", "1")),
            skyreels_timeout_seconds=int(os.getenv("KAIROS_SKYREELS_TIMEOUT_SECONDS", "3600")),
        )

    @staticmethod
    def _optional_path(raw_path: str | None) -> Path | None:
        return Path(raw_path).expanduser() if raw_path else None

    @staticmethod
    def _csv(raw_value: str) -> tuple[str, ...]:
        return tuple(value.strip() for value in raw_value.split(",") if value.strip())

    def ensure_directories(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
