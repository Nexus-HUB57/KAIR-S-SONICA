from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LyricSegment:
    text: str
    section: str
    syllable_count: int


class VocalAgent:
    """Organiza letra sem sintetizar identidade vocal ou imitar pessoa real."""

    def align(self, lyrics: str | None, sections: list[str]) -> list[LyricSegment]:
        if not lyrics:
            return []
        lines = [line.strip() for line in lyrics.splitlines() if line.strip()]
        if not lines:
            lines = [lyrics.strip()]
        result: list[LyricSegment] = []
        for index, line in enumerate(lines):
            section = sections[index % len(sections)] if sections else "verse"
            syllables = max(1, len([word for word in line.split() if word]))
            result.append(LyricSegment(text=line, section=section, syllable_count=syllables))
        return result
