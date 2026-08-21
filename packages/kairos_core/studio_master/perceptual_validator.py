from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class PerceptualReport:
    score: float
    method: str
    peak_dbfs: float
    rms_dbfs: float
    dynamic_range_db: float
    passed: bool
    warnings: tuple[str, ...]


class PerceptualValidator:
    """Métrica técnica de smoke test; MOS neural exige um adapter externo explícito."""

    def capabilities(self) -> dict[str, object]:
        return {
            "name": "perceptual-validator",
            "method": "technical-signal-health/v1",
            "neural_backend": "optional-mosnet",
            "subjective_mos": False,
            "automatic_optimization": False,
        }

    def predict(self, audio: np.ndarray, *, target_score: float = 4.0) -> PerceptualReport:
        array = np.asarray(audio, dtype=np.float32)
        if array.ndim not in (1, 2) or array.size == 0:
            raise ValueError("áudio deve ser array mono ou estéreo não vazio")
        if not np.isfinite(array).all():
            raise ValueError("áudio deve conter apenas valores finitos")
        mono = array if array.ndim == 1 else array.mean(axis=1)
        peak = float(np.max(np.abs(mono)))
        rms = float(np.sqrt(np.mean(mono**2)))
        peak_dbfs = self._dbfs(peak)
        rms_dbfs = self._dbfs(rms)
        dynamic_range = max(0.0, peak_dbfs - rms_dbfs)
        clipping_penalty = min(2.0, max(0.0, peak - 0.98) * 10.0)
        silence_penalty = 2.0 if peak < 1e-6 else 0.0
        loudness_bonus = 0.35 if -24 <= rms_dbfs <= -8 else 0.0
        dynamics_bonus = 0.25 if 3 <= dynamic_range <= 18 else 0.0
        score = float(np.clip(3.8 + loudness_bonus + dynamics_bonus - clipping_penalty - silence_penalty, 0, 5))
        return PerceptualReport(
            score=round(score, 4),
            method="technical-signal-health/v1",
            peak_dbfs=round(peak_dbfs, 4),
            rms_dbfs=round(rms_dbfs, 4),
            dynamic_range_db=round(dynamic_range, 4),
            passed=score >= target_score,
            warnings=(
                "Score técnico não é MOS subjetivo e não substitui escuta humana.",
                "O backend MOSNet/TorchAudio continua opcional e não é carregado automaticamente.",
            ),
        )

    def optimization_plan(self, report: PerceptualReport, *, target_score: float = 4.0) -> dict[str, object]:
        if report.score >= target_score:
            return {"needed": False, "iterations": 0, "reason": "technical target reached"}
        return {
            "needed": True,
            "iterations": 1,
            "reason": "review headroom, loudness and dynamics",
            "approval_required": True,
            "automatic_file_write": False,
        }

    @staticmethod
    def _dbfs(value: float) -> float:
        return float(20.0 * np.log10(max(value, 1e-9)))
