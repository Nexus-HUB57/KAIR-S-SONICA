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
    adapter_id="mosnet",
    package="mosnet",
    import_module="mosnet",
    code_license="MIT",
    code_license_url="https://github.com/lochenchou/MOSNet",
    source_url="https://github.com/lochenchou/MOSNet",
    model_artifact_policy="checkpoint_and_vcc2018_data_review_required",
    requires_gpu=False,
    requires_external_asset=False,
    fallback="technical_signal_health",
    risk_level="estimated_score_not_human_mos",
)


class MosnetAdapter:
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
        model_path: str,
        fallback: bool = True,
    ) -> AdapterResult:
        try:
            self.context.require_ready()
            model = self.context.approved_asset(model_path)
            audio = np.asarray(samples, dtype=np.float32)
            if audio.ndim != 1 or audio.size == 0 or not np.isfinite(audio).all():
                raise AdapterUnavailable("MOSNet exige onda mono finita e não vazia")
            if audio.size > self.context.settings.studio_master_max_input_samples:
                raise AdapterUnavailable("entrada excede o limite de amostras")
            if sample_rate < 1:
                raise AdapterUnavailable("sample_rate inválido")
            import tensorflow as tf  # type: ignore[import-not-found]

            loaded = tf.keras.models.load_model(str(model), compile=False)
            prediction = np.asarray(loaded.predict(audio[None, :], verbose=0), dtype=np.float32)
            if prediction.size == 0 or not np.isfinite(prediction).all():
                raise AdapterUnavailable("MOSNet retornou previsão inválida")
            estimated_mos = float(np.clip(prediction.mean(), 1.0, 5.0))
            return AdapterResult(
                adapter_id=self.adapter_id,
                method="tensorflow-mosnet-checkpoint/v1",
                status="SUCCEEDED",
                output={"estimated_mos": estimated_mos},
                warnings=["MOSNet é uma estimativa de modelo; não substitui avaliação humana."],
                metadata={"sample_rate": sample_rate, "model_path": model.name, "estimated": True},
            )
        except (AdapterUnavailable, ImportError, OSError, RuntimeError, TypeError, ValueError) as exc:
            if not fallback:
                raise
            return AdapterResult(
                adapter_id=self.adapter_id,
                method="technical-signal-health/fallback-v1",
                status="FALLBACK",
                output=None,
                warnings=[f"MOSNet indisponível: {exc}"],
                metadata={"fallback": self.context.spec.fallback, "estimated": False},
                fallback_used=True,
            )
