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
    adapter_id="fluidsynth",
    package="pyfluidsynth",
    import_module="fluidsynth",
    code_license="LGPL-2.1-or-later",
    code_license_url="https://github.com/FluidSynth/fluidsynth/blob/master/LICENSE",
    source_url="https://github.com/fluidsynth/fluidsynth",
    model_artifact_policy="soundfont_license_required",
    requires_gpu=False,
    requires_external_asset=True,
    fallback="declarative_instrument_plan",
    risk_level="soundfont_provenance_review",
)


class FluidSynthAdapter:
    adapter_id = SPEC.adapter_id

    def __init__(self, settings: Any) -> None:
        self.context = AdapterContext(settings, SPEC)

    def capability(self):
        return self.context.capability()

    def run(
        self,
        notes: list[dict[str, Any]],
        sample_rate: int,
        *,
        soundfont_path: str,
        bank: int = 0,
        program: int = 0,
        fallback: bool = True,
    ) -> AdapterResult:
        try:
            self.context.require_ready()
            soundfont = self.context.approved_asset(soundfont_path)
            if sample_rate < 8_000 or sample_rate > 192_000:
                raise AdapterUnavailable("sample_rate fora do intervalo suportado")
            if not notes or len(notes) > 128:
                raise AdapterUnavailable("a lista de notas deve conter de 1 a 128 itens")
            normalized = [self._normalize_note(note) for note in notes]
            import fluidsynth  # type: ignore[import-not-found]

            synth = fluidsynth.Synth(samplerate=sample_rate)
            try:
                soundfont_id = synth.sfload(str(soundfont))
                synth.program_select(0, soundfont_id, bank, program)
                rendered: list[float] = []
                for note in normalized:
                    synth.noteon(0, note["pitch"], note["velocity"])
                    frame_count = int(note["duration_seconds"] * sample_rate)
                    audio = np.asarray(synth.get_samples(frame_count), dtype=np.float32)
                    if audio.size:
                        rendered.extend((audio / 32768.0).tolist())
                    synth.noteoff(0, note["pitch"])
                return AdapterResult(
                    adapter_id=self.adapter_id,
                    method="fluidsynth.Synth/v1",
                    status="SUCCEEDED",
                    output=rendered,
                    metadata={
                        "sample_rate": sample_rate,
                        "soundfont": soundfont.name,
                        "bank": bank,
                        "program": program,
                        "notes": len(normalized),
                    },
                )
            finally:
                delete = getattr(synth, "delete", None)
                if callable(delete):
                    delete()
        except (AdapterUnavailable, ImportError, OSError, RuntimeError, TypeError, ValueError) as exc:
            if not fallback:
                raise
            return AdapterResult(
                adapter_id=self.adapter_id,
                method="declarative-instrument-plan/fallback-v1",
                status="FALLBACK",
                output=normalized if "normalized" in locals() else [],
                warnings=[f"FluidSynth indisponível: {exc}"],
                metadata={"fallback": self.context.spec.fallback},
                fallback_used=True,
            )

    @staticmethod
    def _normalize_note(note: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(note, dict):
            raise AdapterUnavailable("nota inválida")
        pitch = int(note.get("pitch", 60))
        velocity = int(note.get("velocity", 90))
        duration = float(note.get("duration_seconds", 0.25))
        if not 0 <= pitch <= 127 or not 1 <= velocity <= 127 or not 0.01 <= duration <= 30:
            raise AdapterUnavailable("nota fora dos limites MIDI")
        return {"pitch": pitch, "velocity": velocity, "duration_seconds": duration}
