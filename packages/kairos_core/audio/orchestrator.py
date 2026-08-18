from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kairos_core.audio.pipeline import AudioPipeline
from kairos_core.audio.processing import AudioAnalysis, AudioProcessor
from kairos_core.audio.transcription import TranscriptResult, build_transcriber
from kairos_core.config import Settings
from kairos_core.schemas import MultimediaRequest, TrackRequest

ProgressCallback = Callable[[str, int, str], None]


@dataclass(frozen=True, slots=True)
class MultimediaResult:
    task_id: str
    artifact_path: Path | None
    transcript_path: Path | None
    metadata_path: Path
    metadata: dict[str, Any]


class MultimediaOrchestrator:
    """Coordena os canais multimídia do Káiros em uma tarefa observável.

    O fluxo aceita uma referência de áudio opcional, produz análise técnica,
    transcrição por backend configurável, gera um artefato musical quando
    solicitado e grava sidecars JSON para consumo por clientes e auditoria.
    """

    def __init__(
        self,
        settings: Settings,
        audio_pipeline: AudioPipeline | None = None,
        audio_processor: AudioProcessor | None = None,
    ) -> None:
        self.settings = settings
        self.audio_pipeline = audio_pipeline or AudioPipeline(settings)
        self.audio_processor = audio_processor or AudioProcessor(ffmpeg_bin=settings.ffmpeg_bin)

    def run(
        self,
        request: MultimediaRequest,
        task_id: str,
        progress: ProgressCallback | None = None,
    ) -> MultimediaResult:
        self.settings.ensure_directories()

        def emit(step: str, percent: int, message: str) -> None:
            if progress:
                progress(step, percent, message)

        emit("ingesting", 5, "Validando referência multimídia e diretórios permitidos")
        input_path = self._resolve_input(request.audio_path)
        analysis: AudioAnalysis | None = None
        transcript: TranscriptResult | None = None

        if input_path and request.analyze_audio:
            emit("analyzing_audio", 20, "Extraindo duração, canais, loudness aproximado e tempo")
            analysis = self.audio_processor.analyze(input_path)

        transcript_path: Path | None = None
        if input_path and request.transcribe:
            emit("transcribing", 35, "Transcrevendo referência pelo backend configurado")
            backend = request.transcription_backend or self.settings.transcription_backend
            model = request.transcription_model or self.settings.transcription_model
            transcriber = build_transcriber(
                backend=backend,
                model=model,
                device=self.settings.transcription_device,
                compute_type=self.settings.transcription_compute_type,
            )
            transcript = transcriber.transcribe(input_path, language=request.transcription_language)
            transcript_path = self.settings.output_dir / f"{task_id}.transcript.json"
            transcript_path.write_text(
                json.dumps(transcript.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        artifact_path: Path | None = None
        plan: dict[str, Any] | None = None
        if request.generate_audio:
            emit("orchestrating_generation", 50, "Construindo TrackRequest a partir do prompt e da referência")
            prompt = (request.prompt or "").strip()
            if not prompt and transcript:
                prompt = transcript.text[:2_000]
            if not prompt:
                prompt = "Criar uma peça instrumental coerente com a referência multimídia"
            lyrics = request.lyrics or (transcript.text if transcript else None)
            track_request = TrackRequest(
                prompt=prompt,
                route_id=request.route_id,
                artist_id=request.artist_id,
                genre=request.genre,
                bpm=request.bpm,
                key=request.key,
                scale=request.scale,
                lyrics=lyrics,
                duration_seconds=request.duration_seconds,
                swing=request.swing,
                humanize_ms=request.humanize_ms,
                sample_rate=request.sample_rate,
                output_format=request.output_format,
                stems=request.stems,
                seed=request.seed,
            )
            result = self.audio_pipeline.run(track_request, task_id, progress=progress)
            artifact_path = result.artifact_path
            plan = result.plan.model_dump()

        metadata = {
            "task_id": task_id,
            "orchestrator_id": "kairos.aai_apo",
            "orchestrator_role": "creative_minister_maestro_dj_ai",
            "artist_id": request.artist_id,
            "route_id": request.route_id,
            "input_path": str(input_path) if input_path else None,
            "analysis": analysis.to_dict() if analysis else None,
            "transcription": transcript.to_dict() if transcript else None,
            "plan": plan,
            "artifact_path": str(artifact_path) if artifact_path else None,
            "status": "SUCCEEDED",
        }
        metadata_path = self.settings.output_dir / f"{task_id}.metadata.json"
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        emit("completed", 100, "Orquestração multimídia concluída")
        return MultimediaResult(
            task_id=task_id,
            artifact_path=artifact_path,
            transcript_path=transcript_path,
            metadata_path=metadata_path,
            metadata=metadata,
        )

    def _resolve_input(self, raw_path: str | None) -> Path | None:
        if not raw_path:
            return None
        requested = Path(raw_path)
        if requested.is_absolute() or requested.exists():
            candidate = requested
        else:
            candidate = self.settings.upload_dir / requested
        candidate = candidate.resolve()
        allowed_roots = (self.settings.upload_dir.resolve(), self.settings.output_dir.resolve())
        if not any(self._is_within(candidate, root) for root in allowed_roots):
            raise ValueError("audio_path deve apontar para data/uploads ou data/output")
        if not candidate.is_file():
            raise FileNotFoundError(f"Referência multimídia não encontrada: {candidate}")
        return candidate

    @staticmethod
    def _is_within(path: Path, root: Path) -> bool:
        try:
            path.relative_to(root)
        except ValueError:
            return False
        return True
