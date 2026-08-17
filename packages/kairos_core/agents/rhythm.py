from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from kairos_core.schemas import GrooveSettings


@dataclass(frozen=True, slots=True)
class RhythmEvent:
    """Evento abstrato; o áudio pode ser renderizado por qualquer gerador."""

    name: str
    beat: float
    velocity: float


class RhythmAgent:
    """Cria uma grade simples com swing e humanização determinísticos."""

    def schedule(self, bpm: int, duration_seconds: float, settings: GrooveSettings, seed: int | None = None) -> list[RhythmEvent]:
        beat_duration = 60.0 / bpm
        step_duration = beat_duration / settings.subdivision
        steps = int(np.ceil(duration_seconds / step_duration))
        rng = np.random.default_rng(seed)
        events: list[RhythmEvent] = []
        for step in range(steps):
            if step % settings.subdivision == 1 and settings.subdivision == 2:
                offset = (settings.swing - 0.5) * beat_duration
            else:
                offset = 0.0
            jitter = float(rng.uniform(-settings.humanize_ms, settings.humanize_ms) / 1000.0)
            beat = max(0.0, step * step_duration + offset + jitter)
            name = "kick" if step % 4 == 0 else "snare" if step % 4 == 2 else "hat"
            velocity = 0.90 if name == "kick" else 0.72 if name == "snare" else 0.42
            events.append(RhythmEvent(name=name, beat=beat, velocity=velocity))
        return [event for event in events if event.beat < duration_seconds]
