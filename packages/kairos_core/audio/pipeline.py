from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from kairos_core.agents.maestro import MaestroAgent
from kairos_core.agents.mix_master import MixMasterAgent
from kairos_core.audio.generation import AudioGenerator, ProceduralDemoGenerator
from kairos_core.audio.transcode import transcode_to_mp3, write_wav
from kairos_core.config import Settings
from kairos_core.schemas import TrackPlan, TrackRequest

ProgressCallback = Callable[[str, int, str], None]


@dataclass(frozen=True, slots=True)
class PipelineResult:
    plan: TrackPlan
    wav_path: Path
    artifact_path: Path


class AudioPipeline:
    def __init__(self, settings: Settings, generator: AudioGenerator | None = None) -> None:
        self.settings = settings
        self.generator = generator or ProceduralDemoGenerator()
        self.maestro = MaestroAgent()
        self.master = MixMasterAgent()

    def run(self, request: TrackRequest, request_id: str, progress: ProgressCallback | None = None) -> PipelineResult:
        self.settings.ensure_directories()

        def emit(step: str, percent: int, message: str) -> None:
            if progress:
                progress(step, percent, message)

        emit("planning", 10, "Plano musical estruturado pelo Maestro")
        plan = self.maestro.build_plan(request, request_id=request_id)
        emit("generating", 45, "Renderizando áudio pelo adaptador configurado")
        audio = self.generator.generate(plan, sample_rate=request.sample_rate, seed=request.seed)
        emit("mastering", 70, "Aplicando saturação, RMS e limitador de pico")
        mastered = self.master.process(audio)

        wav_path = self.settings.output_dir / f"{request_id}.wav"
        write_wav(wav_path, mastered, request.sample_rate)
        artifact_path = wav_path
        if request.output_format == "mp3":
            emit("transcoding", 88, "Transcodificando WAV para MP3 CBR 320 kbps")
            artifact_path = transcode_to_mp3(wav_path, self.settings.output_dir / f"{request_id}.mp3", self.settings.ffmpeg_bin)
        emit("completed", 100, "Artefato pronto")
        return PipelineResult(plan=plan, wav_path=wav_path, artifact_path=artifact_path)
