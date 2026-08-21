from __future__ import annotations

from typing import ClassVar

from kairos_core.studio_master.v2_contracts import ViralClipPlanRequest


class ViralClipPlanner:
    """Cria um plano de exportação social; não publica nem gera vídeo automaticamente."""

    _resolutions: ClassVar[dict[str, tuple[int, int]]] = {
        "9:16": (1080, 1920),
        "1:1": (1080, 1080),
        "16:9": (1920, 1080),
    }

    def plan(self, request: ViralClipPlanRequest) -> dict[str, object]:
        width, height = self._resolutions[request.aspect_ratio]
        return {
            "schema_version": 1,
            "status": "READY_FOR_APPROVAL",
            "method": "waveform-social-clip-plan/v1",
            "platform": request.platform,
            "duration_seconds": request.duration_seconds,
            "canvas": {"width": width, "height": height, "fps": 24},
            "audio": {
                "asset_id": request.audio_asset_id,
                "required": True,
                "source_policy": "operator-uploaded-or-generated-approved-asset",
            },
            "visualizer": {
                "mode": "rms-waveform",
                "window_ms": 20,
                "palette": {"background": "#0A0A0A", "accent": "#FF4B4B", "text": "#FFFFFF"},
            },
            "text": {"title": request.title, "watermark": request.watermark, "caption_adapter": "optional"},
            "render": {
                "adapter": "moviepy-or-browser-canvas",
                "output": "mp4",
                "automatic_publish": False,
                "approval_required": True,
            },
            "warnings": [
                "Plano não baixa áudio, fontes ou referências externas.",
                "Publicação em rede social requer revisão e ação explícita do operador.",
            ],
        }
