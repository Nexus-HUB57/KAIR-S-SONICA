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
    ltx2_enabled: bool = False
    ltx2_repo: Path | None = None
    ltx2_model_id: str | None = None
    ltx2_license_accepted: bool = False
    agent_aggregator_enabled: bool = False
    skyreels_space_enabled: bool = False
    skyreels_space_base_url: str = "https://fffiloni-skyreels-v2.hf.space"
    skyreels_space_endpoint: str = "generate_diffusion_forced_video"
    skyreels_space_timeout_seconds: int = 1_800
    llamagen_enabled: bool = False
    llamagen_base_url: str = "https://api.llamagen.ai"
    llamagen_api_key_env: str = "LLAMAGEN_API_KEY"
    llamagen_timeout_seconds: int = 60
    complementary_core_enabled: bool = True
    log_level: str = "INFO"
    media_cache_dir: Path = Path("data/media-cache")
    media_cache_max_bytes: int = 100 * 1024 * 1024
    media_provider_order: tuple[str, ...] = ("pexels", "unsplash")
    agentic_core_enabled: bool = True
    agentic_memory_dir: Path = Path("data/agentic-memory")
    agentic_external_tools_enabled: bool = False
    social_orchestrator_enabled: bool = True
    social_llm_enabled: bool = False
    social_schedule_db_path: Path = Path("data/social/schedules.sqlite3")
    artistic_island_enabled: bool = True
    instrument_atlas_path: Path = Path("config/instrument_atlas.yaml")
    studio_master_enabled: bool = True
    canon_index_path: Path = Path("config/canon_index.yaml")
    instrumentation_repertoire_path: Path = Path("config/instrumentation_repertoire.yaml")
    studio_master_max_input_samples: int = 250_000
    studio_master_memory_enabled: bool = False
    studio_master_memory_path: Path = Path("data/studio-master/artist-memory.jsonl")
    studio_master_auto_retrain_enabled: bool = False
    studio_master_retrain_manifest_path: Path = Path("data/studio-master/retrain-manifest.json")
    studio_master_analytics_path: Path = Path("data/production_history.json")
    studio_master_real_adapters_enabled: bool = False
    studio_master_adapter_licenses_path: Path = Path("config/studio_master_adapter_licenses.yaml")
    studio_master_adapter_model_manifest_path: Path = Path("data/studio-master/model-manifest.json")
    studio_master_adapter_assets_dir: Path = Path("data/approved-assets")
    studio_master_adapter_output_dir: Path = Path("data/studio-master/adapter-output")
    studio_master_adapter_allow_model_download: bool = False
    studio_master_accepted_adapter_licenses: tuple[str, ...] = ()
    studio_master_enabled_adapter_ids: tuple[str, ...] = ()
    studio_upload_token: str | None = None
    studio_upload_max_bytes: int = 100 * 1024 * 1024
    studio_upload_max_duration_seconds: float = 900.0
    studio_upload_allowed_extensions: tuple[str, ...] = (
        ".wav",
        ".mp3",
        ".m4a",
        ".flac",
        ".ogg",
        ".webm",
    )
    studio_master_preflight_dir: Path = Path("data/studio-master/preflight")
    studio_master_auto_review_enabled: bool = True
    cloud_video_fallback_enabled: bool = False
    cloud_video_fallback_provider: str = "NOT_CONFIGURED"
    cloud_video_fallback_base_url: str | None = None
    cloud_video_fallback_submit_path: str = "/v1/video/generations"
    cloud_video_fallback_api_key_env: str = "KAIROS_CLOUD_VIDEO_FALLBACK_API_KEY"
    cloud_video_fallback_timeout_seconds: int = 1_800
    cloud_video_fallback_allowed_providers: tuple[str, ...] = ()
    cloud_video_fallback_license_acknowledged: bool = False
    cloud_video_fallback_retention_acknowledged: bool = False
    cloud_video_fallback_spending_limit_cents: int = 0
    cloud_video_fallback_max_upload_bytes: int = 100 * 1024 * 1024

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
            ltx2_enabled=os.getenv("KAIROS_LTX2_ENABLED", "false").lower()
            in {"1", "true", "yes", "on"},
            ltx2_repo=cls._optional_path(os.getenv("KAIROS_LTX2_REPO")),
            ltx2_model_id=os.getenv("KAIROS_LTX2_MODEL_ID") or None,
            ltx2_license_accepted=os.getenv("KAIROS_LTX2_LICENSE_ACCEPTED", "false").lower()
            in {"1", "true", "yes", "on"},
            agent_aggregator_enabled=os.getenv("KAIROS_AGENT_AGGREGATOR_ENABLED", "false").lower()
            in {"1", "true", "yes", "on"},
            skyreels_space_enabled=os.getenv("KAIROS_SKYREELS_SPACE_ENABLED", "false").lower()
            in {"1", "true", "yes", "on"},
            skyreels_space_base_url=os.getenv(
                "KAIROS_SKYREELS_SPACE_BASE_URL",
                "https://fffiloni-skyreels-v2.hf.space",
            ).rstrip("/"),
            skyreels_space_endpoint=os.getenv(
                "KAIROS_SKYREELS_SPACE_ENDPOINT",
                "generate_diffusion_forced_video",
            ),
            skyreels_space_timeout_seconds=int(
                os.getenv("KAIROS_SKYREELS_SPACE_TIMEOUT_SECONDS", "1800")
            ),
            llamagen_enabled=os.getenv("KAIROS_LLAMAGEN_ENABLED", "false").lower()
            in {"1", "true", "yes", "on"},
            llamagen_base_url=os.getenv(
                "KAIROS_LLAMAGEN_BASE_URL", "https://api.llamagen.ai"
            ).rstrip("/"),
            llamagen_api_key_env=os.getenv("KAIROS_LLAMAGEN_API_KEY_ENV", "LLAMAGEN_API_KEY"),
            llamagen_timeout_seconds=int(os.getenv("KAIROS_LLAMAGEN_TIMEOUT_SECONDS", "60")),
            complementary_core_enabled=os.getenv(
                "KAIROS_COMPLEMENTARY_CORE_ENABLED", "true"
            ).lower()
            in {"1", "true", "yes", "on"},
            log_level=os.getenv("KAIROS_LOG_LEVEL", "INFO").upper(),
            media_cache_dir=Path(os.getenv("KAIROS_MEDIA_CACHE_DIR", "data/media-cache")),
            media_cache_max_bytes=int(
                os.getenv("KAIROS_MEDIA_CACHE_MAX_BYTES", str(100 * 1024 * 1024))
            ),
            media_provider_order=cls._csv(
                os.getenv("KAIROS_MEDIA_PROVIDER_ORDER", "pexels,unsplash")
            ),
            agentic_core_enabled=os.getenv("KAIROS_AGENTIC_CORE_ENABLED", "true").lower()
            in {"1", "true", "yes", "on"},
            agentic_memory_dir=Path(os.getenv("KAIROS_AGENTIC_MEMORY_DIR", "data/agentic-memory")),
            agentic_external_tools_enabled=os.getenv(
                "KAIROS_AGENTIC_EXTERNAL_TOOLS_ENABLED", "false"
            ).lower()
            in {"1", "true", "yes", "on"},
            social_orchestrator_enabled=os.getenv(
                "KAIROS_SOCIAL_ORCHESTRATOR_ENABLED", "true"
            ).lower()
            in {"1", "true", "yes", "on"},
            social_llm_enabled=os.getenv("KAIROS_SOCIAL_LLM_ENABLED", "false").lower()
            in {"1", "true", "yes", "on"},
            social_schedule_db_path=Path(
                os.getenv("KAIROS_SOCIAL_SCHEDULE_DB_PATH", "data/social/schedules.sqlite3")
            ),
            artistic_island_enabled=os.getenv("KAIROS_ARTISTIC_ISLAND_ENABLED", "true").lower()
            in {"1", "true", "yes", "on"},
            instrument_atlas_path=Path(
                os.getenv("KAIROS_INSTRUMENT_ATLAS_PATH", "config/instrument_atlas.yaml")
            ),
            studio_master_enabled=os.getenv("KAIROS_STUDIO_MASTER_ENABLED", "true").lower()
            in {"1", "true", "yes", "on"},
            canon_index_path=Path(os.getenv("KAIROS_CANON_INDEX_PATH", "config/canon_index.yaml")),
            instrumentation_repertoire_path=Path(
                os.getenv(
                    "KAIROS_INSTRUMENTATION_REPERTOIRE_PATH",
                    "config/instrumentation_repertoire.yaml",
                )
            ),
            studio_master_max_input_samples=int(
                os.getenv("KAIROS_STUDIO_MASTER_MAX_INPUT_SAMPLES", "250000")
            ),
            studio_master_memory_enabled=os.getenv(
                "KAIROS_STUDIO_MASTER_MEMORY_ENABLED", "false"
            ).lower()
            in {"1", "true", "yes", "on"},
            studio_master_memory_path=Path(
                os.getenv(
                    "KAIROS_STUDIO_MASTER_MEMORY_PATH", "data/studio-master/artist-memory.jsonl"
                )
            ),
            studio_master_auto_retrain_enabled=os.getenv(
                "KAIROS_STUDIO_MASTER_AUTO_RETRAIN_ENABLED", "false"
            ).lower()
            in {"1", "true", "yes", "on"},
            studio_master_retrain_manifest_path=Path(
                os.getenv(
                    "KAIROS_STUDIO_MASTER_RETRAIN_MANIFEST_PATH",
                    "data/studio-master/retrain-manifest.json",
                )
            ),
            studio_master_analytics_path=Path(
                os.getenv("KAIROS_STUDIO_MASTER_ANALYTICS_PATH", "data/production_history.json")
            ),
            studio_master_real_adapters_enabled=os.getenv(
                "KAIROS_STUDIO_MASTER_REAL_ADAPTERS_ENABLED", "false"
            ).lower()
            in {"1", "true", "yes", "on"},
            studio_master_adapter_licenses_path=Path(
                os.getenv(
                    "KAIROS_STUDIO_MASTER_ADAPTER_LICENSES_PATH",
                    "config/studio_master_adapter_licenses.yaml",
                )
            ),
            studio_master_adapter_model_manifest_path=Path(
                os.getenv(
                    "KAIROS_STUDIO_MASTER_ADAPTER_MODEL_MANIFEST_PATH",
                    "data/studio-master/model-manifest.json",
                )
            ),
            studio_master_adapter_assets_dir=Path(
                os.getenv("KAIROS_STUDIO_MASTER_ADAPTER_ASSETS_DIR", "data/approved-assets")
            ),
            studio_master_adapter_output_dir=Path(
                os.getenv(
                    "KAIROS_STUDIO_MASTER_ADAPTER_OUTPUT_DIR",
                    "data/studio-master/adapter-output",
                )
            ),
            studio_master_adapter_allow_model_download=os.getenv(
                "KAIROS_STUDIO_MASTER_ADAPTER_ALLOW_MODEL_DOWNLOAD", "false"
            ).lower()
            in {"1", "true", "yes", "on"},
            studio_master_accepted_adapter_licenses=cls._csv(
                os.getenv("KAIROS_STUDIO_MASTER_ACCEPTED_ADAPTER_LICENSES", "")
            ),
            studio_master_enabled_adapter_ids=cls._csv(
                os.getenv("KAIROS_STUDIO_MASTER_ENABLED_ADAPTER_IDS", "")
            ),
            studio_upload_token=os.getenv("KAIROS_STUDIO_UPLOAD_TOKEN") or None,
            studio_upload_max_bytes=int(
                os.getenv("KAIROS_STUDIO_UPLOAD_MAX_BYTES", str(100 * 1024 * 1024))
            ),
            studio_upload_max_duration_seconds=float(
                os.getenv("KAIROS_STUDIO_UPLOAD_MAX_DURATION_SECONDS", "900")
            ),
            studio_upload_allowed_extensions=cls._csv(
                os.getenv(
                    "KAIROS_STUDIO_UPLOAD_ALLOWED_EXTENSIONS", ".wav,.mp3,.m4a,.flac,.ogg,.webm"
                )
            ),
            studio_master_preflight_dir=Path(
                os.getenv("KAIROS_STUDIO_MASTER_PREFLIGHT_DIR", "data/studio-master/preflight")
            ),
            studio_master_auto_review_enabled=os.getenv(
                "KAIROS_STUDIO_MASTER_AUTO_REVIEW_ENABLED", "true"
            ).lower()
            in {"1", "true", "yes", "on"},
            cloud_video_fallback_enabled=os.getenv(
                "KAIROS_CLOUD_VIDEO_FALLBACK_ENABLED", "false"
            ).lower()
            in {"1", "true", "yes", "on"},
            cloud_video_fallback_provider=os.getenv(
                "KAIROS_CLOUD_VIDEO_FALLBACK_PROVIDER", "NOT_CONFIGURED"
            ),
            cloud_video_fallback_base_url=(
                os.getenv("KAIROS_CLOUD_VIDEO_FALLBACK_BASE_URL") or None
            ),
            cloud_video_fallback_submit_path=os.getenv(
                "KAIROS_CLOUD_VIDEO_FALLBACK_SUBMIT_PATH", "/v1/video/generations"
            ),
            cloud_video_fallback_api_key_env=os.getenv(
                "KAIROS_CLOUD_VIDEO_FALLBACK_API_KEY_ENV",
                "KAIROS_CLOUD_VIDEO_FALLBACK_API_KEY",
            ),
            cloud_video_fallback_timeout_seconds=int(
                os.getenv("KAIROS_CLOUD_VIDEO_FALLBACK_TIMEOUT_SECONDS", "1800")
            ),
            cloud_video_fallback_allowed_providers=cls._csv(
                os.getenv("KAIROS_CLOUD_VIDEO_FALLBACK_ALLOWED_PROVIDERS", "")
            ),
            cloud_video_fallback_license_acknowledged=os.getenv(
                "KAIROS_CLOUD_VIDEO_FALLBACK_LICENSE_ACKNOWLEDGED", "false"
            ).lower()
            in {"1", "true", "yes", "on"},
            cloud_video_fallback_retention_acknowledged=os.getenv(
                "KAIROS_CLOUD_VIDEO_FALLBACK_RETENTION_ACKNOWLEDGED", "false"
            ).lower()
            in {"1", "true", "yes", "on"},
            cloud_video_fallback_spending_limit_cents=int(
                os.getenv("KAIROS_CLOUD_VIDEO_FALLBACK_SPENDING_LIMIT_CENTS", "0")
            ),
            cloud_video_fallback_max_upload_bytes=int(
                os.getenv(
                    "KAIROS_CLOUD_VIDEO_FALLBACK_MAX_UPLOAD_BYTES",
                    str(100 * 1024 * 1024),
                )
            ),
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
