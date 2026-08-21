from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace

import numpy as np

from kairos_core.agents.rhythm import RhythmEvent
from kairos_core.studio_master.canon import CanonIndex
from kairos_core.studio_master.contracts import GrooveDna, OnsetPoint


class DeterministicGrooveExtractor:
    """Extrator leve de referência; não substitui um modelo neural treinado."""

    def __init__(self, canon: CanonIndex) -> None:
        self.canon = canon

    def extract(
        self,
        samples: Iterable[float],
        *,
        sample_rate: int,
        bpm: float,
        canon_id: str | None = None,
    ) -> GrooveDna:
        audio = np.asarray(list(samples), dtype=np.float32)
        if audio.ndim != 1:
            raise ValueError("A análise de groove exige uma forma de onda mono")
        if audio.size == 0 or not np.isfinite(audio).all():
            raise ValueError("A forma de onda precisa conter amostras finitas")
        if audio.size > 250_000:
            raise ValueError("A forma de onda excede o limite de análise")

        duration = audio.size / sample_rate
        envelope = np.abs(audio)
        window = max(1, int(sample_rate * 0.012))
        if envelope.size >= window:
            envelope = np.convolve(envelope, np.ones(window) / window, mode="same")
        threshold = max(float(np.percentile(envelope, 78)) * 0.45, 0.015)
        min_distance = max(1, int(sample_rate * 0.045))
        candidates = np.flatnonzero(
            (envelope >= threshold)
            & (envelope >= np.r_[envelope[:1], envelope[:-1]])
            & (envelope >= np.r_[envelope[1:], envelope[-1:]])
        )
        peak_indices: list[int] = []
        for index in candidates:
            if not peak_indices or index - peak_indices[-1] >= min_distance:
                peak_indices.append(int(index))
            elif envelope[index] > envelope[peak_indices[-1]]:
                peak_indices[-1] = int(index)

        onsets = [index / sample_rate for index in peak_indices]
        quarter = 60.0 / bpm
        grid = quarter / 4.0
        offsets = [_signed_grid_offset(time, grid) for time in onsets]
        offset_ms = np.asarray(offsets, dtype=np.float64) * 1000
        mean_offset = float(np.mean(offset_ms)) if offset_ms.size else 0.0
        std_offset = float(np.std(offset_ms)) if offset_ms.size else 0.0
        positive_offbeat = [offset for time, offset in zip(onsets, offsets) if _is_offbeat(time, grid)]
        swing_delta = float(np.median(positive_offbeat)) if positive_offbeat else 0.0
        swing_ratio = float(np.clip(0.5 + swing_delta / quarter, 0.5, 0.67))
        density = len(onsets) / max(duration, 1e-6)
        confidence = float(np.clip((len(onsets) / max(duration * 2, 1)) * (1 - min(std_offset / 80, 1)), 0, 1))
        selected = self.canon.nearest(bpm=bpm, swing_ratio=swing_ratio, canon_id=canon_id)
        probabilities = self.canon.culture_probabilities(bpm=bpm, swing_ratio=swing_ratio)
        warning = "Análise determinística por energia; nenhum modelo neural foi executado."
        return GrooveDna(
            method="deterministic-onset-energy/v1",
            sample_rate=sample_rate,
            duration_seconds=round(duration, 6),
            bpm=round(bpm, 4),
            swing_ratio=round(swing_ratio, 6),
            mean_offset_ms=round(mean_offset, 6),
            offset_std_ms=round(std_offset, 6),
            onset_density=round(density, 6),
            rhythmic_confidence=round(confidence, 6),
            culture=[{"label": item["label"], "probability": item["probability"]} for item in probabilities],
            canon_match=selected.id,
            onsets=[
                OnsetPoint(
                    time_seconds=round(time, 6),
                    strength=round(float(envelope[index] / max(float(envelope.max()), 1e-6)), 6),
                )
                for index, time in zip(peak_indices[:512], onsets[:512])
            ],
            warnings=[warning],
        )


def apply_flow_to_events(
    events: Iterable[RhythmEvent],
    groove: GrooveDna,
    *,
    bpm: float,
    grid_follow: bool = True,
) -> list[RhythmEvent]:
    """Aplica o microtiming ao contrato de eventos sem editar o áudio destrutivamente."""
    if not grid_follow:
        return list(events)
    quarter = 60.0 / bpm
    grid = quarter / 4.0
    swing_delta = (groove.swing_ratio - 0.5) * quarter
    global_offset = float(np.clip(groove.mean_offset_ms / 1000.0, -0.5 * grid, 0.5 * grid))
    adjusted: list[RhythmEvent] = []
    for event in events:
        step = max(0, round(event.beat / grid))
        offbeat = step % 2 == 1
        delta = swing_delta if offbeat else 0.0
        beat = max(0.0, event.beat + delta + global_offset)
        adjusted.append(replace(event, beat=round(beat, 9)))
    return adjusted


def _signed_grid_offset(time_seconds: float, grid: float) -> float:
    position = time_seconds / grid
    nearest = round(position) * grid
    return time_seconds - nearest


def _is_offbeat(time_seconds: float, grid: float) -> bool:
    return round(time_seconds / grid) % 2 == 1
