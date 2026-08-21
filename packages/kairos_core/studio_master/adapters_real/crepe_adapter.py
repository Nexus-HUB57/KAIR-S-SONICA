from __future__ import annotations

from typing import Any

import numpy as np

from kairos_core.studio_master.adapters_real.base import (
    AdapterContext,
    AdapterResult,
    AdapterSpec,
    AdapterUnavailable,
)

SPEC = AdapterSpec(
    adapter_id="crepe",
    package="crepe",
    import_module="crepe",
    code_license="MIT",
    code_license_url="https://raw.githubusercontent.com/marl/crepe/master/LICENSE",
    source_url="https://github.com/marl/crepe",
    model_artifact_policy="external_model_provenance_required",
    requires_gpu=False,
    requires_external_asset=False,
    fallback="hum_to_midi_sketch",
    risk_level="model_and_dataset_review",
)


class CrepeAdapter:
    adapter_id = SPEC.adapter_id

    def __init__(self, settings: Any) -> None:
        self.context = AdapterContext(settings, SPEC)

    def capability(self):
        return self.context.capability()

    def run(
        self,
        samples: list[float],
        sample_rate: int,
        *,
        step_size_ms: int = 10,
        model_capacity: str = "full",
        viterbi: bool = False,
        fallback: bool = True,
    ) -> AdapterResult:
        try:
            self.context.require_ready()
            if sample_rate < 1 or step_size_ms not in {5, 10, 20, 40, 50}:
                raise AdapterUnavailable("sample_rate ou step_size_ms inválido")
            audio = np.asarray(samples, dtype=np.float32)
            if audio.ndim != 1 or not np.isfinite(audio).all() or audio.size == 0:
                raise AdapterUnavailable("CREPE exige onda mono finita e não vazia")
            if audio.size > self.context.settings.studio_master_max_input_samples:
                raise AdapterUnavailable("entrada excede o limite de amostras do StudioMaster")
            if model_capacity not in {"tiny", "small", "medium", "large", "full"}:
                raise AdapterUnavailable("model_capacity inválida")
            import crepe  # type: ignore[import-not-found]

            times, frequencies, confidence, _activation = crepe.predict(
                audio,
                sample_rate,
                viterbi=viterbi,
                step_size=step_size_ms,
                model_capacity=model_capacity,
            )
            frames = [
                {
                    "time_seconds": float(time),
                    "frequency_hz": float(frequency),
                    "confidence": float(score),
                }
                for time, frequency, score in zip(times, frequencies, confidence, strict=False)
            ]
            return AdapterResult(
                adapter_id=self.adapter_id,
                method="crepe.predict/v1",
                status="SUCCEEDED",
                output=frames,
                metadata={"sample_rate": sample_rate, "step_size_ms": step_size_ms, "model_capacity": model_capacity},
            )
        except (AdapterUnavailable, ImportError, OSError, RuntimeError, ValueError) as exc:
            if not fallback:
                raise
            return AdapterResult(
                adapter_id=self.adapter_id,
                method="hum-to-midi-sketch/fallback-v1",
                status="FALLBACK",
                output=[],
                warnings=[f"CREPE indisponível: {exc}"],
                metadata={"fallback": self.context.spec.fallback},
                fallback_used=True,
            )
