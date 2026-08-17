from __future__ import annotations

from kairos_core.agents.rhythm import RhythmAgent, RhythmEvent
from kairos_core.schemas import GrooveSettings


def build_groove_grid(bpm: int, duration_seconds: float, settings: GrooveSettings, seed: int | None = None) -> list[RhythmEvent]:
    """Retorna eventos temporais; nenhum áudio é deslocado destrutivamente nesta etapa."""
    return RhythmAgent().schedule(bpm, duration_seconds, settings, seed=seed)
