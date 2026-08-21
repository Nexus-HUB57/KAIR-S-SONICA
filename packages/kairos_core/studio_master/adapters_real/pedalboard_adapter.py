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
    adapter_id="pedalboard",
    package="pedalboard",
    import_module="pedalboard",
    code_license="GPL-3.0-only",
    code_license_url="https://github.com/spotify/pedalboard/blob/main/LICENSE",
    source_url="https://github.com/spotify/pedalboard",
    model_artifact_policy="not_applicable",
    requires_gpu=False,
    requires_external_asset=False,
    fallback="numpy_dsp_preview",
    risk_level="copyleft_and_plugin_review",
)


class PedalboardAdapter:
    adapter_id = SPEC.adapter_id

    def __init__(self, settings: Any) -> None:
        self.context = AdapterContext(settings, SPEC)

    def capability(self):
        return self.context.capability()

    def run(
        self,
        samples: list[float] | list[list[float]],
        sample_rate: int,
        *,
        chain: list[dict[str, Any]] | None = None,
        output_path: str | None = None,
        fallback: bool = True,
    ) -> AdapterResult:
        try:
            self.context.require_ready()
            if sample_rate < 1:
                raise AdapterUnavailable("sample_rate inválido")
            audio = np.asarray(samples, dtype=np.float32)
            if audio.ndim == 1:
                audio = audio.reshape(1, -1)
            if audio.ndim != 2 or audio.shape[0] not in {1, 2} or audio.shape[1] == 0:
                raise AdapterUnavailable("Pedalboard exige array mono/estéreo")
            if not np.isfinite(audio).all():
                raise AdapterUnavailable("Pedalboard exige samples finitos")
            import pedalboard  # type: ignore[import-not-found]

            plugins = self._build_plugins(pedalboard, chain or [])
            board = pedalboard.Pedalboard(plugins)
            rendered = np.asarray(board(audio, sample_rate), dtype=np.float32)
            metadata: dict[str, Any] = {"sample_rate": sample_rate, "plugins": len(plugins)}
            if output_path:
                final_path = self.context.new_output(output_path)
                from pedalboard.io import AudioFile  # type: ignore[import-not-found]

                with AudioFile(str(final_path), "w", sample_rate, rendered.shape[0]) as handle:
                    handle.write(rendered)
                metadata["output_path"] = str(final_path)
            return AdapterResult(
                adapter_id=self.adapter_id,
                method="pedalboard.Pedalboard/v1",
                status="SUCCEEDED",
                output=rendered.tolist() if not output_path else None,
                metadata=metadata,
            )
        except (AdapterUnavailable, ImportError, OSError, RuntimeError, TypeError, ValueError) as exc:
            if not fallback:
                raise
            return AdapterResult(
                adapter_id=self.adapter_id,
                method="numpy-dsp-preview/fallback-v1",
                status="FALLBACK",
                output=np.asarray(samples, dtype=np.float32).tolist(),
                warnings=[f"Pedalboard indisponível: {exc}"],
                metadata={"fallback": self.context.spec.fallback},
                fallback_used=True,
            )

    @staticmethod
    def _build_plugins(pedalboard: Any, chain: list[dict[str, Any]]) -> list[Any]:
        plugins: list[Any] = []
        for step in chain[:16]:
            algorithm = str(step.get("algorithm", "")).lower()
            parameters = step.get("parameters", {})
            if not isinstance(parameters, dict):
                raise AdapterUnavailable("parâmetros de cadeia inválidos")
            if algorithm in {"gain", "makeup_gain"}:
                plugins.append(pedalboard.Gain(gain_db=float(parameters.get("gain_db", 0.0))))
            elif algorithm in {"compressor", "multiband_comp"}:
                plugins.append(
                    pedalboard.Compressor(
                        threshold_db=float(parameters.get("threshold_db", -18.0)),
                        ratio=float(parameters.get("ratio", 2.0)),
                    )
                )
            elif algorithm == "limiter":
                plugins.append(pedalboard.Limiter())
            elif algorithm == "reverb":
                plugins.append(pedalboard.Reverb(room_size=float(parameters.get("room_size", 0.25))))
            elif algorithm == "delay":
                plugins.append(
                    pedalboard.Delay(
                        delay_seconds=float(parameters.get("delay_seconds", 0.18)),
                        mix=float(parameters.get("mix", 0.12)),
                    )
                )
            elif algorithm in {"highpass", "highpass_filter"}:
                plugins.append(
                    pedalboard.HighpassFilter(cutoff_frequency_hz=float(parameters.get("cutoff_hz", 80.0)))
                )
            elif algorithm in {"lowpass", "lowpass_filter"}:
                plugins.append(
                    pedalboard.LowpassFilter(cutoff_frequency_hz=float(parameters.get("cutoff_hz", 16_000.0)))
                )
            elif algorithm == "chorus":
                plugins.append(pedalboard.Chorus())
            elif algorithm == "distortion":
                plugins.append(pedalboard.Distortion())
            elif algorithm in {"convolution", "convolution_reverb"}:
                raise AdapterUnavailable("convolution exige IR aprovado e adapter explícito")
            else:
                raise AdapterUnavailable(f"efeito Pedalboard não permitido nesta cadeia: {algorithm}")
        return plugins
