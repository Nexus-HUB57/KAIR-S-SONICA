from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import threading
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from kairos_core.config import Settings
from kairos_core.schemas import VideoRequest

VideoProgressCallback = Callable[[str, int, str], None]

_SEMAPHORE_LOCK = threading.Lock()
_SEMAPHORES: dict[tuple[str, str], threading.BoundedSemaphore] = {}


class VideoBackendError(RuntimeError):
    """Erro explícito de configuração ou execução do backend de vídeo."""


@dataclass(frozen=True, slots=True)
class VideoResult:
    task_id: str
    artifact_path: Path
    metadata_path: Path
    metadata: dict[str, object]


class SkyReelsVideoAdapter:
    """Ponte não destrutiva entre o KAIR e os entry points do SkyReels-V2.

    O código do SkyReels permanece em seu clone/licença próprios. Este adaptador
    chama os CLIs oficiais apenas quando o operador habilita o backend e fornece
    um checkpoint local, ou habilita explicitamente o download do modelo.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def run(
        self,
        request: VideoRequest,
        task_id: str,
        progress: VideoProgressCallback | None = None,
    ) -> VideoResult:
        self._ensure_enabled()
        self.settings.ensure_directories()
        repo = self._repo_path()
        self._preflight_entrypoint(repo, request.engine)
        model_id = self._model_id(request)
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
        try:
            command = self.build_command(request, task_id, staging_dir, repo=repo, model_id=model_id)
        except Exception:
            self._cleanup_staging(staging_dir)
            raise

        slot = self._concurrency_slot(repo, model_id)
        self._emit(progress, "video_queued", 15, "Aguardando slot de inferência GPU")
        with slot:
            self._emit(progress, "video_generating", 20, "Executando o backend SkyReels-V2 em staging isolado")
            try:
                completed = subprocess.run(
                    command,
                    cwd=repo,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=self.settings.skyreels_timeout_seconds,
                )
            except subprocess.TimeoutExpired as exc:
                self._cleanup_staging(staging_dir)
                raise VideoBackendError(
                    f"SkyReels excedeu o timeout de {self.settings.skyreels_timeout_seconds}s"
                ) from exc
            except OSError as exc:
                self._cleanup_staging(staging_dir)
                raise VideoBackendError(f"Não foi possível iniciar o SkyReels: {exc}") from exc

        if completed.returncode != 0:
            self._cleanup_staging(staging_dir)
            detail = (completed.stderr or completed.stdout or "sem saída do backend")[-4_000:]
            raise VideoBackendError(
                f"SkyReels terminou com código {completed.returncode}: {detail}"
            )

        self._emit(progress, "video_collecting", 85, "Validando e promovendo o MP4 produzido")
        candidates = sorted(
            staging_dir.rglob("*.mp4"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        if not candidates:
            self._cleanup_staging(staging_dir)
            detail = (completed.stderr or completed.stdout or "nenhum MP4 encontrado")[-4_000:]
            raise VideoBackendError(f"SkyReels não produziu MP4: {detail}")

        candidate = candidates[0]
        try:
            media = self._validate_mp4(candidate)
            self._promote_without_overwrite(candidate, artifact_path)

            metadata: dict[str, object] = {
                "task_id": task_id,
                "status": "SUCCEEDED",
                "backend": "skyreels-v2",
                "engine": request.engine,
                "mode": request.mode,
                "model_id": model_id,
                "resolution": request.resolution,
                "num_frames": self._num_frames(request),
                "fps": request.fps,
                "seed": request.seed,
                "artifact_path": str(artifact_path),
                "staging_id": safe_task_id,
                "command": list(command),
                "stdout_tail": (completed.stdout or "")[-2_000:],
                "stderr_tail": (completed.stderr or "")[-2_000:],
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
        finally:
            if not self.settings.skyreels_keep_staging:
                self._cleanup_staging(staging_dir)

    def build_command(
        self,
        request: VideoRequest,
        task_id: str,
        staging_dir: Path,
        *,
        repo: Path | None = None,
        model_id: str | None = None,
    ) -> list[str]:
        """Monta o comando oficial sem iniciar inferência; útil para testes e dry-runs."""
        repo = repo or self._repo_path()
        model_id = model_id or self._model_id(request)
        self._validate_request(request, model_id)
        script_name = "generate_video_df.py" if request.engine == "diffusion_forcing" else "generate_video.py"
        command = [
            self.settings.skyreels_python,
            str(repo / script_name),
            "--outdir",
            str(staging_dir),
            "--model_id",
            model_id,
            "--resolution",
            request.resolution,
            "--num_frames",
            str(self._num_frames(request)),
            "--prompt",
            request.prompt,
            "--guidance_scale",
            str(request.guidance_scale),
            "--shift",
            str(request.shift),
            "--inference_steps",
            str(request.inference_steps),
            "--fps",
            str(request.fps),
        ]
        if request.seed is not None:
            command.extend(["--seed", str(request.seed)])
        if request.offload:
            command.append("--offload")
        if request.prompt_enhancer:
            command.append("--prompt_enhancer")
        if request.teacache:
            command.extend(["--teacache", "--teacache_thresh", str(request.teacache_thresh)])
        if request.use_ret_steps:
            command.append("--use_ret_steps")
        if request.use_usp:
            command.append("--use_usp")

        if request.engine == "diffusion_forcing":
            command.extend(
                [
                    "--ar_step",
                    str(request.ar_step),
                    "--causal_block_size",
                    str(request.causal_block_size),
                    "--base_num_frames",
                    str(self._base_num_frames(request)),
                    "--addnoise_condition",
                    str(request.addnoise_condition),
                ]
            )
            overlap = self._overlap_history(request)
            if overlap is not None:
                command.extend(["--overlap_history", str(overlap)])
            if request.video_path:
                command.extend(["--video_path", str(self._resolve_media(request.video_path))])
            if request.image_path:
                command.extend(["--image", str(self._resolve_media(request.image_path))])
            if request.end_image_path:
                command.extend(["--end_image", str(self._resolve_media(request.end_image_path))])
        elif request.image_path:
            command.extend(["--image", str(self._resolve_media(request.image_path))])

        return command

    def _concurrency_slot(self, repo: Path, model_id: str) -> threading.BoundedSemaphore:
        key = (str(repo), model_id)
        with _SEMAPHORE_LOCK:
            semaphore = _SEMAPHORES.get(key)
            if semaphore is None:
                semaphore = threading.BoundedSemaphore(max(1, self.settings.skyreels_max_concurrency))
                _SEMAPHORES[key] = semaphore
            return semaphore

    def _ensure_enabled(self) -> None:
        if not self.settings.enable_skyreels:
            raise VideoBackendError(
                "SkyReels está desabilitado; defina KAIROS_ENABLE_SKYREELS=true conscientemente"
            )

    def _preflight_entrypoint(self, repo: Path, engine: str) -> None:
        script_name = "generate_video_df.py" if engine == "diffusion_forcing" else "generate_video.py"
        script = repo / script_name
        if not script.is_file():
            raise VideoBackendError(f"Entry point do SkyReels não encontrado: {script}")
        python = Path(self.settings.skyreels_python).expanduser()
        if not python.is_file() and shutil.which(self.settings.skyreels_python) is None:
            raise VideoBackendError(
                f"Interpretador do SkyReels não encontrado: {self.settings.skyreels_python}"
            )

    def _repo_path(self) -> Path:
        repo = self.settings.skyreels_repo
        if repo is None:
            raise VideoBackendError("KAIROS_SKYREELS_REPO não foi configurado")
        repo = repo.expanduser().resolve()
        if not repo.is_dir():
            raise FileNotFoundError(f"Clone do SkyReels não encontrado: {repo}")
        return repo

    def _model_id(self, request: VideoRequest) -> str:
        model_id = request.model_id or self.settings.skyreels_model_id
        if not model_id:
            raise VideoBackendError(
                "Informe model_id ou KAIROS_SKYREELS_MODEL_ID; pesos não são embutidos no KAIR"
            )
        model_path = Path(model_id).expanduser()
        if model_path.exists():
            return str(model_path.resolve())
        if not self.settings.skyreels_allow_model_download:
            raise VideoBackendError(
                "O modelo não existe localmente e downloads estão bloqueados; "
                "configure um caminho local ou KAIROS_SKYREELS_ALLOW_MODEL_DOWNLOAD=true"
            )
        return model_id

    def _validate_request(self, request: VideoRequest, model_id: str) -> None:
        del model_id  # Reservado para validações de compatibilidade futuras.
        fields = {
            "t2v": (request.image_path, request.end_image_path, request.video_path),
            "i2v": (request.image_path, request.end_image_path, request.video_path),
            "start_end": (request.image_path, None, request.video_path),
            "extend": (None, request.end_image_path, request.video_path),
        }
        if request.mode == "t2v" and any(fields["t2v"]):
            raise ValueError("modo t2v não aceita image_path, end_image_path ou video_path")
        if request.mode == "i2v" and not request.image_path:
            raise ValueError("modo i2v exige image_path")
        if request.mode == "i2v" and request.end_image_path:
            raise ValueError("modo i2v não aceita end_image_path; use start_end")
        if request.mode == "start_end":
            if not request.image_path or not request.end_image_path:
                raise ValueError("modo start_end exige image_path e end_image_path")
            if request.video_path:
                raise ValueError("modo start_end não aceita video_path")
        if request.mode == "extend" and not request.video_path:
            raise ValueError("modo extend exige video_path")
        if request.mode == "extend" and request.image_path:
            raise ValueError("modo extend não aceita image_path")
        if request.mode == "extend" and request.end_image_path:
            raise ValueError("modo extend não aceita end_image_path")
        if request.engine == "standard" and request.mode in {"extend", "start_end"}:
            raise ValueError("engine standard suporta somente t2v e i2v")
        if request.prompt_enhancer and request.mode != "t2v":
            raise ValueError("prompt_enhancer só é aplicado ao modo t2v pelo CLI do SkyReels")
        if request.use_usp and request.seed is None:
            raise ValueError("use_usp exige seed explícita para inferência distribuída")
        if request.ar_step > 0 and request.causal_block_size == 1:
            raise ValueError("ar_step > 0 exige causal_block_size maior que 1")
        if request.overlap_history is not None and request.overlap_history >= self._base_num_frames(request):
            raise ValueError("overlap_history deve ser menor que base_num_frames")
        for raw_path in (request.image_path, request.end_image_path, request.video_path):
            if raw_path:
                self._resolve_media(raw_path)

    def _resolve_media(self, raw_path: str) -> Path:
        roots = (self.settings.upload_dir.resolve(), self.settings.output_dir.resolve())
        requested = Path(raw_path).expanduser()
        candidates = [requested] if requested.is_absolute() else [root / requested for root in roots]
        for candidate in candidates:
            candidate = candidate.resolve()
            if any(self._is_within(candidate, root) for root in roots) and candidate.is_file():
                return candidate
        raise ValueError("caminho de mídia deve apontar para data/uploads ou data/output")

    def _num_frames(self, request: VideoRequest) -> int:
        return request.num_frames or (97 if request.resolution == "540P" else 121)

    def _base_num_frames(self, request: VideoRequest) -> int:
        return request.base_num_frames or (97 if request.resolution == "540P" else 121)

    def _overlap_history(self, request: VideoRequest) -> int | None:
        if request.overlap_history is not None:
            return request.overlap_history
        if request.mode == "extend" or self._num_frames(request) > self._base_num_frames(request):
            return 17
        return None

    @staticmethod
    def _safe_task_id(task_id: str) -> str:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "-", task_id).strip(".-")
        if not safe:
            raise ValueError("task_id inválido")
        return safe[:120]

    @staticmethod
    def _is_within(path: Path, root: Path) -> bool:
        try:
            path.relative_to(root)
        except ValueError:
            return False
        return True

    def _validate_mp4(self, path: Path) -> dict[str, object]:
        if not path.is_file() or path.stat().st_size == 0:
            raise VideoBackendError(f"MP4 inválido ou vazio: {path}")
        try:
            completed = subprocess.run(
                [
                    self.settings.ffprobe_bin,
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration:stream=codec_type",
                    "-of",
                    "json",
                    str(path),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise VideoBackendError(f"Não foi possível validar o MP4 com ffprobe: {exc}") from exc
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout or "sem saída do ffprobe")[-2_000:]
            raise VideoBackendError(f"ffprobe rejeitou o MP4: {detail}")
        try:
            probe = json.loads(completed.stdout or "{}")
            streams = [
                stream for stream in probe.get("streams", []) if stream.get("codec_type") == "video"
            ]
            duration = float(probe.get("format", {}).get("duration", 0))
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise VideoBackendError("Saída inválida do ffprobe para o MP4") from exc
        if not streams or duration <= 0:
            raise VideoBackendError("MP4 sem stream de vídeo ou duração positiva")
        return {"duration_seconds": round(duration, 3), "video_streams": len(streams)}

    @staticmethod
    def _cleanup_staging(path: Path) -> None:
        if path.exists():
            shutil.rmtree(path)
        parent = path.parent
        if parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()

    @staticmethod
    def _promote_without_overwrite(source: Path, destination: Path) -> None:
        temporary = destination.with_name(f".{destination.name}.tmp")
        if temporary.exists():
            raise FileExistsError(f"staging temporário já existe e não será reutilizado: {temporary}")
        shutil.copy2(source, temporary)
        try:
            os.link(temporary, destination)
        except FileExistsError as exc:
            raise FileExistsError(
                f"Saída já existe e não será sobrescrita: {destination}"
            ) from exc
        finally:
            temporary.unlink(missing_ok=True)

    @staticmethod
    def _write_json_once(path: Path, payload: dict[str, object]) -> None:
        if path.exists():
            raise FileExistsError(f"sidecar já existe e não será sobrescrito: {path}")
        temporary = path.with_name(f".{path.name}.tmp")
        if temporary.exists():
            raise FileExistsError(f"sidecar temporário já existe e não será reutilizado: {temporary}")
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            os.link(temporary, path)
        except FileExistsError as exc:
            raise FileExistsError(f"sidecar já existe e não será sobrescrito: {path}") from exc
        finally:
            temporary.unlink(missing_ok=True)

    @staticmethod
    def _emit(
        progress: VideoProgressCallback | None,
        step: str,
        percent: int,
        message: str,
    ) -> None:
        if progress:
            progress(step, percent, message)
