from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True, slots=True)
class CanonEntry:
    id: str
    name: str
    region: str
    bpm_min: float
    bpm_max: float
    swing_ratio: float
    pattern: str
    cultural_context: str
    source: str
    rights_note: str

    @property
    def bpm_midpoint(self) -> float:
        return (self.bpm_min + self.bpm_max) / 2

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "region": self.region,
            "bpm_range": [self.bpm_min, self.bpm_max],
            "swing_ratio": self.swing_ratio,
            "pattern": self.pattern,
            "cultural_context": self.cultural_context,
            "source": self.source,
            "rights_note": self.rights_note,
        }


class CanonIndex:
    """Índice de padrões rítmicos; metadados apenas, sem samples ou modelos."""

    def __init__(self, entries: list[CanonEntry], *, source_path: Path | None = None) -> None:
        if not entries:
            raise ValueError("O índice canônico precisa de ao menos uma entrada")
        identifiers = [entry.id for entry in entries]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("O índice canônico contém IDs duplicados")
        self._entries = tuple(entries)
        self.source_path = source_path

    @classmethod
    def load(cls, path: Path | str | None = None) -> CanonIndex:
        source_path = Path(path) if path else None
        if source_path and source_path.is_file():
            try:
                raw = yaml.safe_load(source_path.read_text(encoding="utf-8")) or {}
                entries = [cls._entry_from_mapping(item) for item in raw.get("canon", [])]
                if entries:
                    return cls(entries, source_path=source_path)
            except (OSError, TypeError, ValueError, yaml.YAMLError):
                pass
        return cls(cls._fallback_entries(), source_path=source_path)

    def entries(self) -> list[dict[str, Any]]:
        return [entry.to_dict() for entry in self._entries]

    def get(self, canon_id: str) -> CanonEntry | None:
        normalized = canon_id.strip().lower()
        return next((entry for entry in self._entries if entry.id.lower() == normalized), None)

    def nearest(self, *, bpm: float, swing_ratio: float, canon_id: str | None = None) -> CanonEntry:
        if canon_id:
            selected = self.get(canon_id)
            if selected is None:
                raise ValueError(f"Padrão canônico desconhecido: {canon_id}")
            return selected
        return min(
            self._entries,
            key=lambda entry: abs(entry.bpm_midpoint - bpm) / 80
            + abs(entry.swing_ratio - swing_ratio) * 3,
        )

    def culture_probabilities(self, *, bpm: float, swing_ratio: float) -> list[dict[str, Any]]:
        scores: dict[str, float] = {}
        for entry in self._entries:
            score = 1 / (0.08 + abs(entry.bpm_midpoint - bpm) / 80 + abs(entry.swing_ratio - swing_ratio) * 3)
            scores[entry.region] = scores.get(entry.region, 0.0) + score
        total = sum(scores.values()) or 1.0
        aliases = {
            "US": "US",
            "LATIN": "LATIN",
            "EUROPE": "EUROPE",
            "BRAZIL": "BRAZILIAN_FUNK",
        }
        return [
            {"label": aliases.get(region, "UNKNOWN"), "probability": round(score / total, 6)}
            for region, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)
        ]

    @staticmethod
    def _entry_from_mapping(item: Any) -> CanonEntry:
        if not isinstance(item, dict):
            raise TypeError("Entrada canônica inválida")
        bpm_range = item.get("bpm_range", [item.get("bpm", 140), item.get("bpm", 140)])
        if not isinstance(bpm_range, list | tuple) or len(bpm_range) != 2:
            raise ValueError("bpm_range deve conter dois valores")
        return CanonEntry(
            id=str(item["id"]),
            name=str(item["name"]),
            region=str(item.get("region", "UNKNOWN")),
            bpm_min=float(bpm_range[0]),
            bpm_max=float(bpm_range[1]),
            swing_ratio=float(item.get("swing_ratio", 0.5)),
            pattern=str(item.get("pattern", "metadado não especificado")),
            cultural_context=str(item.get("cultural_context", "contexto não especificado")),
            source=str(item.get("source", "operator-curated")),
            rights_note=str(item.get("rights_note", "Usar somente material licenciado ou próprio.")),
        )

    @staticmethod
    def _fallback_entries() -> list[CanonEntry]:
        return [
            CanonEntry(
                "fallback_boom_bap",
                "Boom Bap de referência",
                "US",
                78,
                100,
                0.64,
                "kick sincopado, caixa no 2 e 4, hats em colcheias com swing",
                "descrição abstrata de produção; não é reprodução de gravação",
                "built-in-fallback",
                "Nenhum áudio ou obra protegida incluído.",
            ),
            CanonEntry(
                "fallback_brazilian_funk",
                "Funk brasileiro percussivo",
                "BRAZIL",
                125,
                155,
                0.53,
                "pulsação grave, cortes secos e síncopa percussiva",
                "descrição abstrata de produção; revisão cultural recomendada",
                "built-in-fallback",
                "Nenhum áudio ou obra protegida incluído.",
            ),
        ]
