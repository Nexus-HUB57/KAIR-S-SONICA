from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from kairos_core.artistic_island.contracts import MixPlan


@dataclass(slots=True)
class ExecutionReport:
    applied: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    peak_before: float = 0.0
    peak_after: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "applied": list(self.applied),
            "skipped": list(self.skipped),
            "warnings": list(self.warnings),
            "peak_before": self.peak_before,
            "peak_after": self.peak_after,
        }


class NumpyChainExecutor:
    """Executa um subconjunto seguro da cadeia em arrays time-major mono/estéreo.

    Este executor é uma referência determinística para preview e testes. Não pretende
    substituir hosts VST/AU/LV2, processamento offline profissional ou masterização
    crítica de entrega.
    """

    SUPPORTED = frozenset(
        {"multiband_comp", "harmonic_exciter", "convolution_reverb", "stereo_widener", "delay_stack"}
    )

    def apply(self, audio: np.ndarray, sample_rate: int, plan: MixPlan) -> tuple[np.ndarray, ExecutionReport]:
        signal = _normalize_audio(audio)
        output = signal.copy()
        report = ExecutionReport(peak_before=float(np.max(np.abs(output), initial=0.0)))
        for step in plan.chain:
            if step.algorithm not in self.SUPPORTED:
                report.skipped.append(step.algorithm)
                continue
            output = self._apply_step(output, sample_rate, step.algorithm, step.parameters)
            output = np.nan_to_num(output, nan=0.0, posinf=1.0, neginf=-1.0).astype(np.float32, copy=False)
            report.applied.append(step.algorithm)
        report.peak_after = float(np.max(np.abs(output), initial=0.0))
        if report.peak_after > 1.0:
            report.warnings.append("Preview excede 0 dBFS; aplique limiter/true-peak no estágio de masterização.")
        if report.skipped:
            report.warnings.append("Algumas etapas permanecem como contrato e exigem adapter DSP explícito.")
        return output, report

    def _apply_step(self, audio: np.ndarray, sample_rate: int, algorithm: str, params: dict[str, Any]) -> np.ndarray:
        if algorithm == "multiband_comp":
            profile = params.get("profile", params)
            threshold = 10 ** (float(profile.get("threshold_db", -18)) / 20)
            ratio = max(1.0, float(profile.get("ratio", 3.0)))
            magnitude = np.abs(audio)
            over = np.maximum(magnitude - threshold, 0.0)
            compressed = threshold + over / ratio
            gain = np.where(magnitude > threshold, compressed / np.maximum(magnitude, 1e-9), 1.0)
            return audio * gain
        if algorithm == "harmonic_exciter":
            drive = min(18.0, max(0.0, float(params.get("drive_db", 1.0))))
            mix = min(1.0, max(0.0, float(params.get("mix", 0.1))))
            driven = np.tanh(audio * (10 ** (drive / 20)))
            return audio * (1.0 - mix) + driven * mix
        if algorithm == "stereo_widener":
            if audio.shape[1] < 2:
                return audio
            width = min(2.0, max(0.0, float(params.get("width", 1.0))))
            mid = (audio[:, 0] + audio[:, 1]) * 0.5
            side = (audio[:, 0] - audio[:, 1]) * 0.5 * width
            return np.column_stack((mid + side, mid - side))
        if algorithm == "delay_stack":
            delay_ms = min(2_000.0, max(1.0, float(params.get("time_ms", 180))))
            feedback = min(0.95, max(0.0, float(params.get("feedback", 0.2))))
            mix = min(1.0, max(0.0, float(params.get("mix", 0.1))))
            delay = max(1, int(sample_rate * delay_ms / 1000))
            delayed = np.zeros_like(audio)
            if delay < len(audio):
                delayed[delay:] = audio[:-delay] * feedback
            return audio * (1.0 - mix) + delayed * mix
        if algorithm == "convolution_reverb":
            wet = min(1.0, max(0.0, float(params.get("dry_wet", 0.2))))
            length = min(max(8, int(sample_rate * 0.18)), 12_000, audio.shape[0])
            ir = np.exp(-np.linspace(0.0, 5.0, length, dtype=np.float32))
            ir /= max(float(ir.sum()), 1e-9)
            reverberated = np.column_stack(
                [np.convolve(audio[:, channel], ir, mode="same") for channel in range(audio.shape[1])]
            )
            return audio * (1.0 - wet) + reverberated * wet
        return audio


def _normalize_audio(audio: np.ndarray) -> np.ndarray:
    array = np.asarray(audio, dtype=np.float32)
    if array.ndim == 1:
        array = array[:, None]
    if array.ndim != 2 or array.shape[1] not in {1, 2}:
        raise ValueError("audio deve ter shape (frames,) ou (frames, canais 1/2)")
    if array.shape[0] == 0:
        raise ValueError("audio não pode ser vazio")
    if not np.isfinite(array).all():
        raise ValueError("audio contém NaN ou infinito")
    return array
