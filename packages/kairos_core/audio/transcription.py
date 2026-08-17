from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Protocol


class TranscriptionUnavailable(RuntimeError):
    """Sinaliza ausência de backend de transcrição configurado."""


@dataclass(frozen=True, slots=True)
class TranscriptSegment:
    start_seconds: float
    end_seconds: float
    text: str
    language: str | None = None


@dataclass(frozen=True, slots=True)
class TranscriptResult:
    text: str
    language: str | None
    segments: tuple[TranscriptSegment, ...]
    backend: str
    model: str | None = None
    source_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["segments"] = [asdict(segment) for segment in self.segments]
        return payload


class Transcriber(Protocol):
    def transcribe(self, path: Path, language: str | None = None) -> TranscriptResult:
        ...


class SidecarTranscriber:
    """Backend sem inferência: lê um sidecar `.txt` ou `.json` produzido pelo operador."""

    def transcribe(self, path: Path, language: str | None = None) -> TranscriptResult:
        txt_path = path.with_suffix(".txt")
        json_path = path.with_suffix(".json")
        if txt_path.is_file():
            text = txt_path.read_text(encoding="utf-8").strip()
            return self._from_text(text, path, language)
        if json_path.is_file():
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            return self._from_payload(payload, path, language)
        raise TranscriptionUnavailable(
            f"Nenhum sidecar encontrado para {path.name}; crie {txt_path.name} ou instale o backend Faster-Whisper"
        )

    @staticmethod
    def _from_text(text: str, path: Path, language: str | None) -> TranscriptResult:
        segments = tuple(
            TranscriptSegment(start_seconds=0.0, end_seconds=0.0, text=line, language=language)
            for line in text.splitlines()
            if line.strip()
        )
        return TranscriptResult(text=text, language=language, segments=segments, backend="sidecar", source_path=str(path))

    @staticmethod
    def _from_payload(payload: dict[str, Any], path: Path, language: str | None) -> TranscriptResult:
        text = str(payload.get("text", "")).strip()
        raw_segments = payload.get("segments", [])
        segments = tuple(
            TranscriptSegment(
                start_seconds=float(item.get("start", item.get("start_seconds", 0.0))),
                end_seconds=float(item.get("end", item.get("end_seconds", 0.0))),
                text=str(item.get("text", "")).strip(),
                language=item.get("language", language),
            )
            for item in raw_segments
        )
        if not text:
            text = " ".join(segment.text for segment in segments).strip()
        return TranscriptResult(text=text, language=payload.get("language", language), segments=segments, backend="sidecar", source_path=str(path))


class FasterWhisperTranscriber:
    """Backend opcional para transcrição local com faster-whisper.

    O modelo é carregado somente quando esse backend é escolhido explicitamente.
    """

    def __init__(self, model: str = "small", device: str = "cpu", compute_type: str = "int8") -> None:
        self.model_name = model
        self.device = device
        self.compute_type = compute_type
        self._model: Any = None

    def _load_model(self) -> Any:
        if self._model is not None:
            return self._model
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise TranscriptionUnavailable(
                "Faster-Whisper não está instalado; instale requirements/transcription.txt"
            ) from exc
        self._model = WhisperModel(self.model_name, device=self.device, compute_type=self.compute_type)
        return self._model

    def transcribe(self, path: Path, language: str | None = None) -> TranscriptResult:
        model = self._load_model()
        segments, info = model.transcribe(str(path), language=language, vad_filter=True)
        materialized = tuple(
            TranscriptSegment(
                start_seconds=float(segment.start),
                end_seconds=float(segment.end),
                text=str(segment.text).strip(),
                language=getattr(info, "language", language),
            )
            for segment in segments
        )
        text = " ".join(segment.text for segment in materialized).strip()
        detected_language = getattr(info, "language", language)
        return TranscriptResult(
            text=text,
            language=detected_language,
            segments=materialized,
            backend="faster-whisper",
            model=self.model_name,
            source_path=str(path),
        )


def build_transcriber(backend: str, model: str, device: str, compute_type: str) -> Transcriber:
    if backend == "sidecar":
        return SidecarTranscriber()
    if backend == "faster-whisper":
        return FasterWhisperTranscriber(model=model, device=device, compute_type=compute_type)
    raise TranscriptionUnavailable(f"Backend de transcrição não suportado: {backend}")
