from __future__ import annotations

from math import log2

from kairos_core.studio_master.v2_contracts import (
    HumPitchFrame,
    HumToMidiRequest,
    HumToMidiResult,
    SketchNote,
)


class HumToMidiSketcher:
    """Converte frames de pitch/confiança em uma partitura abstrata revisável."""

    def convert(self, request: HumToMidiRequest) -> HumToMidiResult:
        valid = [
            frame
            for frame in sorted(request.frames, key=lambda item: item.time_seconds)
            if frame.confidence >= request.min_confidence
            and frame.frequency_hz >= request.min_frequency_hz
        ]
        if not valid:
            return HumToMidiResult(
                warnings=[
                    "Nenhum frame ultrapassou os limites de confiança e frequência.",
                    "Um adapter de pitch tracking pode fornecer frames para nova tentativa.",
                ]
            )

        notes: list[SketchNote] = []
        current_note: int | None = None
        current_start = 0.0
        current_end = 0.0
        confidences: list[float] = []
        previous_time: float | None = None

        def close_note() -> None:
            if current_note is None or current_end <= current_start:
                return
            notes.append(
                SketchNote(
                    midi_note=current_note,
                    start_seconds=round(current_start, 6),
                    end_seconds=round(current_end, 6),
                    confidence=round(sum(confidences) / len(confidences), 6),
                )
            )

        for frame in valid:
            note = self._frequency_to_midi(frame)
            gap = previous_time is not None and frame.time_seconds - previous_time > request.max_gap_seconds
            if current_note is None:
                current_note = note
                current_start = frame.time_seconds
                confidences = [frame.confidence]
            elif note != current_note or gap:
                close_note()
                current_note = note
                current_start = frame.time_seconds
                confidences = [frame.confidence]
            else:
                confidences.append(frame.confidence)
            current_end = frame.time_seconds
            previous_time = frame.time_seconds
        close_note()
        return HumToMidiResult(
            notes=notes,
            warnings=[
                "As notas são uma sugestão de sketch e exigem revisão antes do arranjo.",
                "Exportação MIDI binária permanece delegada a adapter opcional.",
            ],
        )

    @staticmethod
    def _frequency_to_midi(frame: HumPitchFrame) -> int:
        return max(0, min(127, round(69 + 12 * log2(frame.frequency_hz / 440.0))))
