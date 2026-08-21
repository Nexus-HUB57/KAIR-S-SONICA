from __future__ import annotations

import numpy as np

from kairos_core.studio_master.v2_contracts import (
    ExpressiveNote,
    HumanExpressionRequest,
    HumanExpressionResult,
)


class HumanExpressionEngine:
    """Aplica microdinâmica reproduzível sem randomismo global ou mutação in-place."""

    def apply(self, request: HumanExpressionRequest) -> HumanExpressionResult:
        rng = np.random.default_rng(request.seed)
        beat_ms = 60_000.0 / request.bpm
        expressive_notes: list[ExpressiveNote] = []
        maximum_shift_ms = 0.0
        for note in request.notes:
            bar = int(note.time_beats // 4)
            energy = float(np.clip(request.energy_map.get(bar, 0.5), 0.0, 1.0))
            step = round(note.time_beats * 4)
            is_offbeat = step % 2 == 1
            accent = 0.10 if note.time_beats % 4 < 0.1 else 0.0
            rhythmic_bias = 0.06 if is_offbeat else 0.0
            jitter_ms = float(rng.uniform(-request.humanize_ms, request.humanize_ms))
            swing_ms = (request.swing_ratio - 0.5) * 30.0 if is_offbeat else 0.0
            shift_ms = swing_ms + jitter_ms
            shift_beats = shift_ms / beat_ms
            target_velocity = note.velocity + round((energy - 0.5) * 24 + accent * 20 + rhythmic_bias * 20)
            velocity_jitter = int(rng.integers(-3, 4))
            velocity = int(np.clip(target_velocity + velocity_jitter, 1, 127))
            maximum_shift_ms = max(maximum_shift_ms, abs(shift_ms))
            expressive_notes.append(
                note.model_copy(
                    update={
                        "time_beats": round(max(0.0, note.time_beats + shift_beats), 9),
                        "velocity": velocity,
                    }
                )
            )
        return HumanExpressionResult(
            notes=expressive_notes,
            applied_swing_ratio=request.swing_ratio,
            max_timing_shift_ms=round(maximum_shift_ms, 6),
            warnings=[
                "Expressividade usa seed explícito e permanece revisável.",
                "Nenhum arquivo MIDI ou áudio é escrito por este módulo.",
            ],
        )
