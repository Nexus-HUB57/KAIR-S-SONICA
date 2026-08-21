from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from kairos_core.studio_master.v2_contracts import (
    ArrangementPlan,
    ArrangementRequest,
    ArrangementSection,
)


@dataclass(frozen=True, slots=True)
class _SectionTemplate:
    id: str
    bars: int
    energy: float
    instruments: tuple[str, ...]


class ArrangementArchitect:
    """Gera uma macroestrutura revisável sem depender de LLM ou dados protegidos."""

    _templates: ClassVar[dict[str, tuple[_SectionTemplate, ...]]] = {
        "boom_bap": (
            _SectionTemplate("intro", 4, 0.30, ("piano", "hat", "pad")),
            _SectionTemplate("verse_1", 8, 0.62, ("kick", "snare", "bass", "piano")),
            _SectionTemplate("hook_1", 8, 0.88, ("kick", "snare", "bass", "piano", "pad")),
            _SectionTemplate("verse_2", 8, 0.70, ("kick", "snare", "bass", "piano")),
            _SectionTemplate("outro", 4, 0.22, ("piano", "pad")),
        ),
        "brazilian_funk_heavy": (
            _SectionTemplate("intro", 4, 0.30, ("piano", "hat", "pad")),
            _SectionTemplate("verse", 8, 0.64, ("kick", "snare", "bass", "piano")),
            _SectionTemplate("lift", 4, 0.78, ("kick", "hat", "bass", "rolls")),
            _SectionTemplate("drop", 8, 1.00, ("kick", "snare", "bass", "rolls", "pad_heavy")),
            _SectionTemplate("bridge", 4, 0.42, ("bass", "pad", "hat")),
            _SectionTemplate("outro", 4, 0.20, ("piano", "pad")),
        ),
        "brazilian_funk_swing": (
            _SectionTemplate("intro", 4, 0.32, ("piano", "hat", "pad")),
            _SectionTemplate("verse", 8, 0.60, ("kick", "snare", "bass", "piano")),
            _SectionTemplate("hook", 8, 0.90, ("kick", "snare", "bass", "piano", "pad")),
            _SectionTemplate("verse_2", 8, 0.68, ("kick", "snare", "bass", "piano")),
            _SectionTemplate("outro", 4, 0.24, ("piano", "pad")),
        ),
        "vocal_focus": (
            _SectionTemplate("intro", 4, 0.25, ("pad", "piano")),
            _SectionTemplate("verse", 8, 0.55, ("kick", "bass", "piano")),
            _SectionTemplate("chorus", 8, 0.84, ("kick", "snare", "bass", "pad")),
            _SectionTemplate("bridge", 8, 0.48, ("bass", "pad", "strings")),
            _SectionTemplate("outro", 4, 0.18, ("piano", "pad")),
        ),
    }

    def build(self, request: ArrangementRequest) -> ArrangementPlan:
        templates = self._templates[request.style]
        bars = self._fit_bars(templates, request.total_bars)
        sections = [
            ArrangementSection(
                id=template.id,
                bars=section_bars,
                energy=round(template.energy, 3),
                instruments=list(template.instruments),
                automation={
                    "filter_cutoff_hz": round(800 + 19_200 * template.energy, 2),
                    "reverb_wet": round(0.10 + 0.35 * template.energy, 3),
                    "drive": round(0.04 + 0.18 * template.energy, 3),
                },
            )
            for template, section_bars in zip(templates, bars, strict=True)
        ]
        return ArrangementPlan(
            style=request.style,
            mood=request.mood,
            bpm=request.bpm,
            total_bars=request.total_bars,
            key=request.key,
            sections=sections,
            warnings=[
                "Arranjo é proposta macro e não substitui revisão musical.",
                "Instrumentos com engine opcional exigem asset próprio/licenciado.",
            ],
        )

    @staticmethod
    def _fit_bars(templates: tuple[_SectionTemplate, ...], total_bars: int) -> list[int]:
        if total_bars < len(templates):
            return [1 if index < total_bars else 0 for index in range(len(templates))]
        bars = [template.bars for template in templates]
        while sum(bars) < total_bars:
            peak = max(range(len(templates)), key=lambda index: (templates[index].energy, -index))
            bars[peak] += 1
        while sum(bars) > total_bars:
            candidate = max(
                (index for index, value in enumerate(bars) if value > 1),
                key=lambda index: (bars[index], -templates[index].energy, -index),
            )
            bars[candidate] -= 1
        return bars
