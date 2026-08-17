from __future__ import annotations

import re
from uuid import uuid4

from kairos_core.schemas import GrooveSettings, SectionPlan, TrackPlan, TrackRequest

_KEY_PATTERN = re.compile(r"(?<![A-Za-z])([A-Ga-g](?:#|b)?)[\s-]+(major|minor|maj|min|m)\b", re.IGNORECASE)
_BPM_PATTERN = re.compile(r"\b([4-9]\d|1\d\d|2[0-3]\d)\s*(?:bpm|batidas)\b", re.IGNORECASE)


class MaestroAgent:
    """Converte intenção textual em um plano musical estável e auditável."""

    def build_plan(self, request: TrackRequest, request_id: str | None = None) -> TrackPlan:
        request_id = request_id or uuid4().hex
        text = f"{request.prompt} {request.genre} {request.key} {request.scale}"
        bpm_match = _BPM_PATTERN.search(text)
        bpm = int(bpm_match.group(1)) if bpm_match else request.bpm
        key_match = _KEY_PATTERN.search(text)
        key = key_match.group(1) if key_match else request.key
        scale = key_match.group(2).lower() if key_match else request.scale
        scale = {"m": "minor", "min": "minor", "maj": "major"}.get(scale, scale)

        return TrackPlan(
            request_id=request_id,
            prompt=request.prompt.strip(),
            genre=request.genre.strip(),
            bpm=bpm,
            key=key,
            scale=scale,
            duration_seconds=request.duration_seconds,
            lyrics=request.lyrics,
            groove=GrooveSettings(swing=request.swing, humanize_ms=request.humanize_ms),
            sections=self._sections(request.duration_seconds),
        )

    @staticmethod
    def _sections(duration: float) -> list[SectionPlan]:
        if duration <= 8:
            names = [("intro", 0.0, 0.2), ("verse", 0.2, 0.7), ("hook", 0.7, 1.0)]
        else:
            names = [("intro", 0.0, 0.12), ("verse", 0.12, 0.42), ("hook", 0.42, 0.68), ("bridge", 0.68, 0.82), ("outro", 0.82, 1.0)]
        sections: list[SectionPlan] = []
        for name, start, end in names:
            sections.append(SectionPlan(name=name, start_seconds=round(duration * start, 3), end_seconds=round(duration * end, 3), energy=min(1.0, 0.35 + end)))
        return sections
