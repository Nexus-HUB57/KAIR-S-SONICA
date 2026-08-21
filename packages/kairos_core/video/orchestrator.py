from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kairos_core.config import Settings
from kairos_core.schemas import VideoRequest
from kairos_core.video.adapter import SkyReelsVideoAdapter, VideoResult

ProgressCallback = Callable[[str, int, str], None]


@dataclass(frozen=True, slots=True)
class VideoOrchestrationResult:
    task_id: str
    artifact_path: Path
    metadata_path: Path
    metadata: dict[str, Any]


class VideoOrchestrator:
    """Executa a cadeia de geração de vídeo com um backend explicitamente habilitado."""

    def __init__(self, settings: Settings, adapter: SkyReelsVideoAdapter | None = None) -> None:
        self.settings = settings
        self.adapter = adapter or SkyReelsVideoAdapter(settings)

    def run(
        self,
        request: VideoRequest,
        task_id: str,
        progress: ProgressCallback | None = None,
    ) -> VideoOrchestrationResult:
        self._emit(progress, "ingesting_video", 5, "Validando parâmetros e referências visuais")
        self._emit(progress, "planning_video", 12, "Selecionando o modo de geração e o sampler")
        result: VideoResult = self.adapter.run(request, task_id, progress=progress)
        return VideoOrchestrationResult(
            task_id=result.task_id,
            artifact_path=result.artifact_path,
            metadata_path=result.metadata_path,
            metadata=result.metadata,
        )

    @staticmethod
    def _emit(
        progress: ProgressCallback | None,
        step: str,
        percent: int,
        message: str,
    ) -> None:
        if progress:
            progress(step, percent, message)
