from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np

from kairos_core.audio.groove import build_groove_grid
from kairos_core.schemas import TrackPlan


class AudioGenerator(Protocol):
    def generate(self, plan: TrackPlan, sample_rate: int, seed: int | None = None) -> np.ndarray:
        ...


class ExternalModelNotConfigured(RuntimeError):
    """Sinaliza que um adaptador neural foi solicitado sem dependências/modelo."""


@dataclass(slots=True)
class ProceduralDemoGenerator:
    """Gerador leve para smoke tests e desenvolvimento sem GPU."""

    def generate(self, plan: TrackPlan, sample_rate: int, seed: int | None = None) -> np.ndarray:
        total = max(1, round(plan.duration_seconds * sample_rate))
        audio = np.zeros((total, 2), dtype=np.float32)
        rng = np.random.default_rng(seed)
        t = np.arange(total, dtype=np.float32) / sample_rate
        key_index = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}.get(plan.key, 0)
        root_hz = 55.0 * (2.0 ** ((key_index - 9) / 12.0))

        pad = 0.08 * np.sin(2 * np.pi * root_hz * t) + 0.04 * np.sin(2 * np.pi * root_hz * 1.5 * t)
        audio[:, 0] += pad
        audio[:, 1] += pad * 0.97

        events = build_groove_grid(plan.bpm, plan.duration_seconds, plan.groove, seed=seed)
        for event in events:
            start = int(event.beat * sample_rate)
            if start >= total:
                continue
            length = min(total - start, int(0.35 * sample_rate))
            local_t = np.arange(length, dtype=np.float32) / sample_rate
            if event.name == "kick":
                sweep = root_hz * 0.5 + root_hz * 0.25 * np.exp(-local_t * 28)
                wave = 0.65 * np.sin(2 * np.pi * sweep * local_t) * np.exp(-local_t * 12)
            elif event.name == "snare":
                wave = 0.25 * rng.normal(0.0, 1.0, length).astype(np.float32) * np.exp(-local_t * 22)
            else:
                wave = 0.07 * rng.normal(0.0, 1.0, length).astype(np.float32) * np.exp(-local_t * 55)
            end = start + length
            audio[start:end, 0] += wave * event.velocity
            audio[start:end, 1] += wave * event.velocity * (0.92 if event.name == "snare" else 1.0)

        bass = 0.12 * np.sin(2 * np.pi * root_hz * 0.5 * t)
        audio[:, 0] += bass
        audio[:, 1] += bass * 0.98
        return np.clip(audio, -1.0, 1.0).astype(np.float32)


@dataclass(slots=True)
class MusicGenAdapter:
    """Ponto de extensão para MusicGen; não baixa pesos automaticamente."""

    def generate(self, plan: TrackPlan, sample_rate: int, seed: int | None = None) -> np.ndarray:
        raise ExternalModelNotConfigured("MusicGenAdapter requer dependências e checkpoint configurados pelo operador")


@dataclass(slots=True)
class BarkAdapter:
    """Ponto de extensão para síntese vocal/sonora compatível com Bark."""

    def generate(self, plan: TrackPlan, sample_rate: int, seed: int | None = None) -> np.ndarray:
        raise ExternalModelNotConfigured("BarkAdapter requer dependências e checkpoint configurados pelo operador")
