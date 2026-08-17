from __future__ import annotations

import numpy as np


def apply_saturation(audio: np.ndarray, drive: float = 1.15) -> np.ndarray:
    """Saturação soft-clip simples, previsível e adequada ao modo demo."""
    return np.tanh(np.asarray(audio, dtype=np.float32) * drive)


def rms_dbfs(audio: np.ndarray) -> float:
    rms = float(np.sqrt(np.mean(np.square(np.asarray(audio, dtype=np.float64))) + 1e-12))
    return 20.0 * float(np.log10(max(rms, 1e-12)))


def peak_dbfs(audio: np.ndarray) -> float:
    peak = float(np.max(np.abs(np.asarray(audio, dtype=np.float64))) + 1e-12)
    return 20.0 * float(np.log10(peak))


def normalize_rms(audio: np.ndarray, target_dbfs: float = -14.0) -> np.ndarray:
    current = rms_dbfs(audio)
    gain = 10 ** ((target_dbfs - current) / 20.0)
    return np.asarray(audio, dtype=np.float32) * np.float32(gain)


def limit_peak(audio: np.ndarray, target_peak_dbfs: float = -1.0) -> np.ndarray:
    target = 10 ** (target_peak_dbfs / 20.0)
    peak = float(np.max(np.abs(audio)) + 1e-12)
    if peak <= target:
        return np.asarray(audio, dtype=np.float32)
    return np.asarray(audio, dtype=np.float32) * np.float32(target / peak)


def master_audio(audio: np.ndarray, target_peak_dbfs: float = -1.0, target_rms_dbfs: float = -14.0) -> np.ndarray:
    mastered = apply_saturation(audio, drive=1.05)
    mastered = normalize_rms(mastered, target_dbfs=target_rms_dbfs)
    mastered = limit_peak(mastered, target_peak_dbfs=target_peak_dbfs)
    return np.clip(mastered, -1.0, 1.0).astype(np.float32)
