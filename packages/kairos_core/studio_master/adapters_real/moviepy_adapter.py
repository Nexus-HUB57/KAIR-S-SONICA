from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any, ClassVar

from kairos_core.studio_master.adapters_real.base import (
    AdapterContext,
    AdapterResult,
    AdapterSpec,
    AdapterUnavailable,
)

SPEC = AdapterSpec(
    adapter_id="moviepy",
    package="moviepy",
    import_module="moviepy",
    code_license="MIT",
    code_license_url="https://github.com/zulko/moviepy",
    source_url="https://github.com/zulko/moviepy",
    model_artifact_policy="not_applicable",
    requires_gpu=False,
    requires_external_asset=True,
    fallback="browser_canvas_clip_plan",
    risk_level="ffmpeg_and_asset_review",
)


class MoviePyAdapter:
    adapter_id = SPEC.adapter_id
    _sizes: ClassVar[dict[str, tuple[int, int]]] = {"9:16": (1080, 1920), "1:1": (1080, 1080), "16:9": (1920, 1080)}

    def __init__(self, settings: Any) -> None:
        self.context = AdapterContext(settings, SPEC)

    def capability(self):
        return self.context.capability()

    def run(
        self,
        audio_path: str,
        output_path: str,
        *,
        aspect_ratio: str = "9:16",
        duration_seconds: float = 15.0,
        fps: int = 24,
        background: tuple[int, int, int] = (10, 10, 10),
        fallback: bool = True,
    ) -> AdapterResult:
        temporary: Path | None = None
        try:
            self.context.require_ready()
            audio = self.context.approved_asset(audio_path)
            final_path = self.context.new_output(output_path)
            if aspect_ratio not in self._sizes or not 1 <= fps <= 60:
                raise AdapterUnavailable("aspect_ratio ou fps inválido")
            if not 1 <= duration_seconds <= 60:
                raise AdapterUnavailable("duration_seconds deve estar entre 1 e 60")
            from moviepy import AudioFileClip, ColorClip  # type: ignore[import-not-found]

            audio_clip = AudioFileClip(str(audio))
            try:
                duration = min(float(duration_seconds), float(audio_clip.duration or duration_seconds))
                video = ColorClip(size=self._sizes[aspect_ratio], color=background).with_duration(duration)
                with_audio = getattr(video, "with_audio", None)
                clip = with_audio(audio_clip) if callable(with_audio) else video.set_audio(audio_clip)
                temporary = final_path.with_name(f".{final_path.name}.partial")
                clip.write_videofile(
                    str(temporary),
                    fps=fps,
                    codec="libx264",
                    audio_codec="aac",
                    logger=None,
                )
                self._validate_mp4(temporary)
                os.replace(temporary, final_path)
                return AdapterResult(
                    adapter_id=self.adapter_id,
                    method="moviepy-colorclip-audio/v1",
                    status="SUCCEEDED",
                    output=str(final_path),
                    warnings=["O clip base usa fundo sólido; composição visual avançada requer uma etapa explícita."],
                    metadata={
                        "aspect_ratio": aspect_ratio,
                        "duration_seconds": duration,
                        "fps": fps,
                        "validated_with": "ffprobe",
                    },
                )
            finally:
                close = getattr(audio_clip, "close", None)
                if callable(close):
                    close()
                close_clip = locals().get("clip")
                if close_clip is not None:
                    close = getattr(close_clip, "close", None)
                    if callable(close):
                        close()
        except (AdapterUnavailable, ImportError, OSError, RuntimeError, subprocess.SubprocessError, TypeError, ValueError) as exc:
            if temporary and temporary.exists():
                temporary.unlink()
            if not fallback:
                raise
            return AdapterResult(
                adapter_id=self.adapter_id,
                method="browser-canvas-clip-plan/fallback-v1",
                status="FALLBACK",
                output={"audio_path": audio_path, "output_path": output_path},
                warnings=[f"MoviePy indisponível: {exc}"],
                metadata={"fallback": self.context.spec.fallback},
                fallback_used=True,
            )

    def _validate_mp4(self, path: Path) -> None:
        command = [
            self.context.settings.ffprobe_bin,
            "-v",
            "error",
            "-show_entries",
            "format=format_name:stream=codec_type",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]
        result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=30)
        if "mp4" not in result.stdout.lower() and "mov" not in result.stdout.lower():
            raise AdapterUnavailable("ffprobe não confirmou container MP4/MOV")
