from __future__ import annotations

import json
import shutil
import subprocess
import wave
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


class AudioProcessingUnavailable(RuntimeError):
    """Sinaliza que a operação depende de uma biblioteca ou binário opcional."""


@dataclass(frozen=True, slots=True)
class AudioAnalysis:
    path: str
    format: str
    duration_seconds: float
    sample_rate: int
    channels: int
    frames: int
    rms_dbfs: float
    peak_dbfs: float
    tempo_bpm: float | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class AudioProcessor:
    """Fachada de processamento para referências multimídia e artefatos gerados.

    SoundFile é usado quando disponível, com fallback para WAV PCM via biblioteca
    padrão ou FFmpeg para formatos comprimidos. Librosa é opcional e acrescenta
    estimativa de tempo; FFprobe acrescenta metadados para formatos que não são WAV.
    """

    ffmpeg_bin: str = "ffmpeg"

    def load(self, path: Path, target_sample_rate: int | None = None, mono: bool = False) -> tuple[np.ndarray, int]:
        if not path.is_file():
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {path}")

        try:
            import soundfile as sf
        except ImportError:
            audio, sample_rate = self._load_with_fallback(path)
        else:
            try:
                audio, sample_rate = sf.read(str(path), always_2d=False, dtype="float32")
            except RuntimeError:
                audio, sample_rate = self._load_with_fallback(path)
            audio = np.asarray(audio, dtype=np.float32)

        if audio.ndim == 1:
            audio = audio[:, None]
        if mono:
            audio = np.mean(audio, axis=1, keepdims=True)
        if target_sample_rate and target_sample_rate != sample_rate:
            audio = self._resample(audio, sample_rate, target_sample_rate)
            sample_rate = target_sample_rate
        return np.clip(audio, -1.0, 1.0).astype(np.float32), sample_rate

    def analyze(self, path: Path) -> AudioAnalysis:
        audio, sample_rate = self.load(path, mono=False)
        mono = np.mean(audio, axis=1)
        rms = float(np.sqrt(np.mean(np.square(mono)) + 1e-12))
        peak = float(np.max(np.abs(audio)) + 1e-12)
        tempo = self._estimate_tempo(mono, sample_rate)
        return AudioAnalysis(
            path=str(path),
            format=path.suffix.lower().lstrip(".") or "unknown",
            duration_seconds=round(audio.shape[0] / sample_rate, 4),
            sample_rate=sample_rate,
            channels=audio.shape[1],
            frames=audio.shape[0],
            rms_dbfs=round(20.0 * float(np.log10(max(rms, 1e-12))), 3),
            peak_dbfs=round(20.0 * float(np.log10(max(peak, 1e-12))), 3),
            tempo_bpm=tempo,
        )

    def probe(self, path: Path, ffprobe_bin: str = "ffprobe") -> dict[str, object]:
        """Retorna metadados FFprobe quando o binário está instalado."""
        executable = shutil.which(ffprobe_bin)
        if not executable:
            raise AudioProcessingUnavailable("FFprobe não encontrado para inspeção multimídia")
        completed = subprocess.run(
            [executable, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)

    @staticmethod
    def _estimate_tempo(audio: np.ndarray, sample_rate: int) -> float | None:
        try:
            import librosa
        except ImportError:
            return None
        try:
            tempo, _ = librosa.beat.beat_track(y=audio, sr=sample_rate)
            value = float(np.asarray(tempo).reshape(-1)[0])
        except (RuntimeError, ValueError):
            return None
        return round(value, 2) if value > 0 else None

    @staticmethod
    def _resample(audio: np.ndarray, source_rate: int, target_rate: int) -> np.ndarray:
        try:
            import librosa
        except ImportError:
            source_positions = np.linspace(0.0, 1.0, num=audio.shape[0], endpoint=False)
            target_length = max(1, round(audio.shape[0] * target_rate / source_rate))
            target_positions = np.linspace(0.0, 1.0, num=target_length, endpoint=False)
            channels = [np.interp(target_positions, source_positions, audio[:, channel]) for channel in range(audio.shape[1])]
            return np.stack(channels, axis=1).astype(np.float32)
        channels = [librosa.resample(audio[:, channel], orig_sr=source_rate, target_sr=target_rate) for channel in range(audio.shape[1])]
        return np.stack(channels, axis=1).astype(np.float32)

    def _load_with_fallback(self, path: Path) -> tuple[np.ndarray, int]:
        if path.suffix.lower() == ".wav":
            return self._load_wav(path)
        executable = shutil.which(self.ffmpeg_bin)
        if not executable:
            raise AudioProcessingUnavailable(
                "FFmpeg não encontrado para decodificar formatos comprimidos; instale-o no sistema"
            )
        sample_rate = 44_100
        try:
            completed = subprocess.run(
                [executable, "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(sample_rate), "pipe:1"],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as exc:
            raise AudioProcessingUnavailable(f"FFmpeg não conseguiu decodificar {path.name}") from exc
        values = np.frombuffer(completed.stdout, dtype=np.float32)
        if values.size == 0:
            raise AudioProcessingUnavailable(f"FFmpeg não produziu amostras para {path.name}")
        return values.reshape(-1, 2), sample_rate

    @staticmethod
    def _load_wav(path: Path) -> tuple[np.ndarray, int]:
        if path.suffix.lower() != ".wav":
            raise AudioProcessingUnavailable("Fallback local suporta somente WAV; instale SoundFile/FFmpeg")
        with wave.open(str(path), "rb") as handle:
            channels = handle.getnchannels()
            sample_width = handle.getsampwidth()
            sample_rate = handle.getframerate()
            frames = handle.readframes(handle.getnframes())
        if sample_width == 1:
            values = np.frombuffer(frames, dtype=np.uint8).astype(np.float32)
            values = (values - 128.0) / 128.0
        elif sample_width == 2:
            values = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
        elif sample_width == 4:
            values = np.frombuffer(frames, dtype=np.int32).astype(np.float32) / 2147483648.0
        else:
            raise AudioProcessingUnavailable(f"Largura PCM WAV não suportada: {sample_width} bytes")
        return values.reshape(-1, channels), sample_rate
