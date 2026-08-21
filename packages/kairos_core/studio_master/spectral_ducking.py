from __future__ import annotations

from dataclasses import dataclass

import numpy as np


class OptionalAdapterUnavailable(RuntimeError):
    """Indica que o backend profissional de um adapter não está configurado."""


@dataclass(frozen=True, slots=True)
class DuckingPreview:
    audio: np.ndarray
    method: str
    strength: float
    warnings: tuple[str, ...]


class SpectralDucker:
    """Preview RMS determinístico; o ducking espectral profissional fica atrás de adapter."""

    @staticmethod
    def capabilities() -> dict[str, object]:
        return {
            "name": "spectral-ducking",
            "preview": "numpy-rms-envelope/v1",
            "professional_adapter": "pedalboard-or-scipy",
            "external_dependencies_optional": True,
        }

    def preview(
        self,
        mix_bus: np.ndarray,
        reference_track: np.ndarray,
        *,
        strength: float = 0.5,
        window_size: int = 1_024,
    ) -> DuckingPreview:
        mix = self._mono_or_stereo(mix_bus)
        reference = self._mono_or_stereo(reference_track)
        strength = float(np.clip(strength, 0.0, 1.0))
        if mix.shape[0] == 0 or reference.shape[0] == 0:
            raise ValueError("mix_bus e reference_track não podem estar vazios")
        reference = self._fit_length(reference, mix.shape[0])
        envelope = self._moving_rms(reference, max(8, window_size))
        normalized = envelope / max(float(np.percentile(envelope, 90)), 1e-6)
        gain = np.clip(1.0 - strength * 0.35 * normalized, 0.55, 1.0)
        if mix.ndim == 1:
            ducked = mix * gain
        else:
            ducked = mix * gain[:, None]
        return DuckingPreview(
            audio=np.asarray(ducked, dtype=np.float32),
            method="numpy-rms-envelope/v1",
            strength=round(strength, 6),
            warnings=(
                "Preview não é ducking espectral multibanda profissional.",
                "Use adapter Pedalboard/SciPy após validar licença e parâmetros.",
            ),
        )

    @staticmethod
    def require_professional_adapter() -> None:
        raise OptionalAdapterUnavailable(
            "Ducking espectral profissional requer adapter opcional Pedalboard/SciPy configurado"
        )

    @staticmethod
    def _mono_or_stereo(audio: np.ndarray) -> np.ndarray:
        array = np.asarray(audio, dtype=np.float32)
        if array.ndim not in (1, 2) or array.size == 0:
            raise ValueError("áudio deve ser array mono ou estéreo não vazio")
        if not np.isfinite(array).all():
            raise ValueError("áudio deve conter apenas valores finitos")
        return array

    @staticmethod
    def _fit_length(audio: np.ndarray, length: int) -> np.ndarray:
        if audio.shape[0] >= length:
            return audio[:length]
        padding = ((0, length - audio.shape[0]),) + ((0, 0),) * (audio.ndim - 1)
        return np.pad(audio, padding)

    @staticmethod
    def _moving_rms(audio: np.ndarray, window_size: int) -> np.ndarray:
        mono = audio if audio.ndim == 1 else audio.mean(axis=1)
        squared = mono.astype(np.float64) ** 2
        cumulative = np.concatenate(([0.0], np.cumsum(squared)))
        indices = np.arange(1, len(mono) + 1)
        starts = np.maximum(0, indices - window_size)
        sums = cumulative[indices] - cumulative[starts]
        widths = indices - starts
        return np.sqrt(sums / np.maximum(widths, 1)).astype(np.float32)
