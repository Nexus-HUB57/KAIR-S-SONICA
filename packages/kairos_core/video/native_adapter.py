from __future__ import annotations

import importlib
import threading
from pathlib import Path
from typing import Any

from kairos_core.schemas import VideoRequest
from kairos_core.video.adapter import (
    SkyReelsVideoAdapter,
    VideoBackendError,
    VideoProgressCallback,
    VideoResult,
)

_NATIVE_PIPELINES: dict[tuple[str, str, str, str, float, bool], Any] = {}
_NATIVE_PIPELINES_LOCK = threading.Lock()


class SkyReelsNativeAdapter(SkyReelsVideoAdapter):
    """Executa SkyReels-V2 através das pipelines nativas do Diffusers.

    O import do stack pesado é lazy: o runtime base continua utilizável sem
    CUDA, torch ou diffusers. O checkpoint é carregado uma vez por processo e
    combinação de modelo/modo/device/dtype, enquanto o semáforo herdado limita
    chamadas concorrentes no mesmo modelo.
    """

    def run(
        self,
        request: VideoRequest,
        task_id: str,
        progress: VideoProgressCallback | None = None,
    ) -> VideoResult:
        self._ensure_enabled()
        if not self.settings.skyreels_native_api:
            raise VideoBackendError(
                "API nativa desabilitada; defina KAIROS_SKYREELS_NATIVE_API=true conscientemente"
            )
        self.settings.ensure_directories()
        model_id = self._native_model_id(request)
        self._validate_request(request, model_id)

        safe_task_id = self._safe_task_id(task_id)
        output_dir = self.settings.output_dir.expanduser().resolve()
        artifact_path = output_dir / f"{safe_task_id}.mp4"
        metadata_path = output_dir / f"{safe_task_id}.metadata.json"
        if artifact_path.exists() or metadata_path.exists():
            raise FileExistsError(
                f"Saída já existe para task_id={task_id}; nenhuma saída foi sobrescrita"
            )
        staging_dir = output_dir / ".skyreels" / safe_task_id
        staging_dir.mkdir(parents=True, exist_ok=False)

        slot = self._concurrency_slot(Path(model_id), model_id)
        try:
            self._emit(progress, "video_queued", 15, "Aguardando slot de inferência GPU nativa")
            with slot:
                self._emit(progress, "video_loading", 18, "Carregando pipeline nativa do Diffusers")
                pipeline, pipeline_name = self._get_pipeline(request, model_id)
                self._emit(progress, "video_generating", 20, "Executando SkyReels-V2 pela API nativa")
                self._generate_mp4(pipeline, request, staging_dir / "generated.mp4")

            self._emit(progress, "video_collecting", 85, "Validando e promovendo o MP4 produzido")
            media = self._validate_mp4(staging_dir / "generated.mp4")
            self._promote_without_overwrite(staging_dir / "generated.mp4", artifact_path)
            metadata: dict[str, object] = {
                "task_id": task_id,
                "status": "SUCCEEDED",
                "backend": "skyreels-v2",
                "backend_api": "diffusers-native",
                "pipeline": pipeline_name,
                "engine": request.engine,
                "mode": request.mode,
                "model_id": model_id,
                "device": self.settings.skyreels_device,
                "dtype": self.settings.skyreels_dtype,
                "resolution": request.resolution,
                "num_frames": self._num_frames(request),
                "fps": request.fps,
                "seed": request.seed,
                "artifact_path": str(artifact_path),
                "staging_id": safe_task_id,
                "duration_seconds": media["duration_seconds"],
                "video_streams": media["video_streams"],
            }
            self._write_json_once(metadata_path, metadata)
            self._emit(progress, "video_completed", 100, "Artefato de vídeo pronto e auditado")
            return VideoResult(
                task_id=task_id,
                artifact_path=artifact_path,
                metadata_path=metadata_path,
                metadata=metadata,
            )
        except Exception:
            self._cleanup_staging(staging_dir)
            raise
        finally:
            if not self.settings.skyreels_keep_staging:
                self._cleanup_staging(staging_dir)

    def _native_model_id(self, request: VideoRequest) -> str:
        model_id = request.model_id or self.settings.skyreels_native_model_id
        if not model_id:
            raise VideoBackendError(
                "Informe model_id ou KAIROS_SKYREELS_NATIVE_MODEL_ID para a API nativa"
            )
        local_path = Path(model_id).expanduser()
        if local_path.exists():
            local_path = local_path.resolve()
            if not local_path.is_dir():
                raise VideoBackendError(f"Checkpoint nativo não é um diretório: {local_path}")
            if not (local_path / "model_index.json").is_file():
                raise VideoBackendError(
                    "Checkpoint nativo local não possui model_index.json; "
                    "use o formato *-Diffusers oficial"
                )
            return str(local_path)
        if not self.settings.skyreels_allow_model_download:
            raise VideoBackendError(
                "Checkpoint nativo não existe localmente e downloads estão bloqueados"
            )
        return model_id

    def _get_pipeline(self, request: VideoRequest, model_id: str) -> tuple[Any, str]:
        pipeline_class, pipeline_name = self._pipeline_class(request)
        key = (
            model_id,
            pipeline_name,
            self.settings.skyreels_device,
            self.settings.skyreels_dtype,
            self._effective_shift(request),
            request.offload,
        )
        with _NATIVE_PIPELINES_LOCK:
            pipeline = _NATIVE_PIPELINES.get(key)
            if pipeline is None:
                pipeline = self._load_pipeline(pipeline_class, model_id, request)
                _NATIVE_PIPELINES[key] = pipeline
        return pipeline, pipeline_name

    def _pipeline_class(self, request: VideoRequest) -> tuple[str, str]:
        if request.prompt_enhancer or request.teacache or request.use_ret_steps or request.use_usp:
            raise VideoBackendError(
                "prompt_enhancer, teacache, use_ret_steps e use_usp exigem o backend CLI; "
                "a API nativa usa os parâmetros Diffusers documentados"
            )
        if request.engine == "diffusion_forcing":
            if request.mode == "t2v":
                return "SkyReelsV2DiffusionForcingPipeline", "df_t2v"
            if request.mode in {"i2v", "start_end"}:
                return "SkyReelsV2DiffusionForcingImageToVideoPipeline", "df_i2v"
            return "SkyReelsV2DiffusionForcingVideoToVideoPipeline", "df_v2v"
        if request.mode == "t2v":
            return "SkyReelsV2Pipeline", "standard_t2v"
        return "SkyReelsV2ImageToVideoPipeline", "standard_i2v"

    def _load_pipeline(self, pipeline_class_name: str, model_id: str, request: VideoRequest) -> Any:
        try:
            torch = importlib.import_module("torch")
            diffusers = importlib.import_module("diffusers")
        except ImportError as exc:
            raise VideoBackendError(
                "API nativa requer torch e diffusers instalados no runtime GPU"
            ) from exc
        if not torch.cuda.is_available() and self.settings.skyreels_device.startswith("cuda"):
            raise VideoBackendError("API nativa configurada para CUDA, mas torch.cuda não está disponível")

        pipeline_class = getattr(diffusers, pipeline_class_name, None)
        if pipeline_class is None:
            raise VideoBackendError(
                f"Classe {pipeline_class_name} não existe na versão instalada do Diffusers"
            )
        dtype = self._torch_dtype(torch)
        vae_class = getattr(diffusers, "AutoencoderKLWan", None) or getattr(diffusers, "AutoModel", None)
        if vae_class is None:
            raise VideoBackendError("Diffusers não expõe AutoencoderKLWan/AutoModel para o VAE SkyReels")
        load_kwargs: dict[str, Any] = {}
        if self.settings.skyreels_cache_dir:
            self.settings.skyreels_cache_dir.mkdir(parents=True, exist_ok=True)
            load_kwargs["cache_dir"] = str(self.settings.skyreels_cache_dir)
        if not self.settings.skyreels_allow_model_download:
            load_kwargs["local_files_only"] = True
        try:
            vae = vae_class.from_pretrained(
                model_id,
                subfolder="vae",
                torch_dtype=torch.float32,
                **load_kwargs,
            )
            pipeline = pipeline_class.from_pretrained(
                model_id,
                vae=vae,
                torch_dtype=dtype,
                **load_kwargs,
            )
            scheduler_class = getattr(diffusers, "UniPCMultistepScheduler", None)
            if scheduler_class is not None and hasattr(pipeline, "scheduler"):
                flow_shift = self._effective_shift(request)
                pipeline.scheduler = scheduler_class.from_config(
                    pipeline.scheduler.config,
                    flow_shift=flow_shift,
                )
            if self.settings.skyreels_device.startswith("cuda") and self.settings.skyreels_device:
                if hasattr(pipeline, "enable_model_cpu_offload") and self.settings.skyreels_device == "cuda" and request.offload:
                    pipeline.enable_model_cpu_offload()
                else:
                    pipeline.to(self.settings.skyreels_device)
            else:
                pipeline.to(self.settings.skyreels_device)
        except Exception as exc:  # Surface model/runtime failure as a backend error.
            raise VideoBackendError(f"Falha ao carregar pipeline nativa {pipeline_class_name}: {exc}") from exc
        return pipeline

    @staticmethod
    def _effective_shift(request: VideoRequest) -> float:
        if request.mode in {"i2v", "start_end", "extend"} and request.shift == 8.0:
            return 5.0
        return request.shift

    def _torch_dtype(self, torch: Any) -> Any:
        allowed = {"float16": torch.float16, "bfloat16": torch.bfloat16, "float32": torch.float32}
        try:
            return allowed[self.settings.skyreels_dtype]
        except KeyError as exc:
            raise VideoBackendError(
                "KAIROS_SKYREELS_DTYPE deve ser float16, bfloat16 ou float32"
            ) from exc

    def _generate_mp4(self, pipeline: Any, request: VideoRequest, output_path: Path) -> None:
        try:
            diffusers_utils = importlib.import_module("diffusers.utils")
            export_to_video = diffusers_utils.export_to_video
        except (ImportError, AttributeError) as exc:
            raise VideoBackendError("Diffusers não expõe export_to_video") from exc
        kwargs: dict[str, Any] = {
            "prompt": request.prompt,
            "height": 544 if request.resolution == "540P" else 720,
            "width": 960 if request.resolution == "540P" else 1280,
            "num_frames": self._num_frames(request),
            "num_inference_steps": request.inference_steps,
            "guidance_scale": request.guidance_scale,
            "fps": request.fps,
        }
        if request.seed is not None:
            torch = importlib.import_module("torch")
            kwargs["generator"] = torch.Generator(device=self.settings.skyreels_device).manual_seed(request.seed)
        if request.engine == "diffusion_forcing":
            kwargs.update(
                {
                    "base_num_frames": self._base_num_frames(request),
                    "ar_step": request.ar_step,
                    "causal_block_size": request.causal_block_size if request.ar_step > 0 else None,
                    "overlap_history": self._overlap_history(request),
                    "addnoise_condition": request.addnoise_condition,
                }
            )
        if request.mode in {"i2v", "start_end"}:
            kwargs["image"] = self._load_image(self._resolve_media(request.image_path))
        elif request.mode == "extend":
            kwargs["video"] = self._load_video(self._resolve_media(request.video_path))
        if request.mode == "start_end":
            kwargs["last_image"] = self._load_image(self._resolve_media(request.end_image_path))
        try:
            kwargs = {key: value for key, value in kwargs.items() if value is not None}
            result = pipeline(**kwargs)
            frames = result.frames[0] if isinstance(result.frames, list) and result.frames else result.frames
            output_path.parent.mkdir(parents=True, exist_ok=True)
            export_to_video(frames, str(output_path), fps=request.fps)
        except Exception as exc:  # Convert model errors into task failures.
            raise VideoBackendError(f"Falha na inferência nativa SkyReels: {exc}") from exc

    @staticmethod
    def _load_image(raw_path: str | Path | None) -> Any:
        if not raw_path:
            raise VideoBackendError("API nativa recebeu uma referência de imagem ausente")
        try:
            from PIL import Image

            return Image.open(raw_path).convert("RGB")
        except Exception as exc:
            raise VideoBackendError(f"Não foi possível carregar a imagem de referência: {exc}") from exc

    @staticmethod
    def _load_video(raw_path: str | Path | None) -> Any:
        if not raw_path:
            raise VideoBackendError("API nativa recebeu uma referência de vídeo ausente")
        try:
            utils = importlib.import_module("diffusers.utils")
            return utils.load_video(raw_path)
        except Exception as exc:
            raise VideoBackendError(f"Não foi possível carregar o vídeo de referência: {exc}") from exc
