from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True, slots=True)
class RepertoireProfile:
    id: str
    style: str
    cultural_region: str
    description: str
    components: dict[str, dict[str, Any]]
    source: str
    rights_note: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "style": self.style,
            "cultural_region": self.cultural_region,
            "description": self.description,
            "components": self.components,
            "source": self.source,
            "rights_note": self.rights_note,
        }


class RepertoireCatalog:
    """Catálogo declarativo; adapters de áudio são resolvidos somente em runtime opt-in."""

    def __init__(self, profiles: list[RepertoireProfile], chains: dict[str, dict[str, Any]], *, source_path: Path | None = None) -> None:
        if not profiles:
            raise ValueError("O repertório precisa de ao menos um perfil")
        self._profiles = tuple(profiles)
        self._chains = chains
        self.source_path = source_path

    @classmethod
    def load(cls, path: Path | str | None = None) -> RepertoireCatalog:
        source_path = Path(path) if path else None
        if source_path and source_path.is_file():
            try:
                raw = yaml.safe_load(source_path.read_text(encoding="utf-8")) or {}
                profiles = [
                    cls._profile_from_mapping(identifier, mapping)
                    for identifier, mapping in (raw.get("repertoire", {}).get("profiles", {}) or {}).items()
                ]
                chains = raw.get("repertoire", {}).get("mixing_chains", {}) or {}
                if profiles:
                    return cls(profiles, chains, source_path=source_path)
            except (OSError, TypeError, ValueError, yaml.YAMLError):
                pass
        return cls(cls._fallback_profiles(), cls._fallback_chains(), source_path=source_path)

    def profiles(self) -> list[dict[str, Any]]:
        return [profile.to_dict() for profile in self._profiles]

    def get(self, identifier: str | None = None, *, style: str | None = None) -> RepertoireProfile:
        candidate = (identifier or style or "").strip().lower()
        for profile in self._profiles:
            if candidate in {profile.id.lower(), profile.style.lower()}:
                return profile
        if candidate.endswith("_kit"):
            for profile in self._profiles:
                if profile.id.lower() == candidate:
                    return profile
        return self._profiles[0]

    def mixing_chain(self, style: str) -> dict[str, Any]:
        key = style.strip().lower()
        chain = self._chains.get(key) or self._chains.get(f"{key}_master_chain")
        if chain:
            return {"id": key, **chain}
        fallback = self._chains.get("boom_bap") or self._fallback_chains()["boom_bap"]
        return {"id": "boom_bap", **fallback}

    @staticmethod
    def _profile_from_mapping(identifier: str, mapping: Any) -> RepertoireProfile:
        if not isinstance(mapping, dict):
            raise TypeError("Perfil de repertório inválido")
        components = mapping.get("components", {})
        if not isinstance(components, dict):
            raise TypeError("components deve ser um objeto")
        return RepertoireProfile(
            id=str(identifier),
            style=str(mapping.get("style", identifier)),
            cultural_region=str(mapping.get("cultural_region", "UNKNOWN")),
            description=str(mapping.get("description", "Perfil instrumental declarativo")),
            components=components,
            source=str(mapping.get("source", "operator-curated")),
            rights_note=str(mapping.get("rights_note", "Usar somente material próprio ou licenciado.")),
        )

    @staticmethod
    def _fallback_profiles() -> list[RepertoireProfile]:
        return [
            RepertoireProfile(
                id="boom_bap_kit",
                style="boom_bap",
                cultural_region="US",
                description="Kit abstrato com kick, snare e hats sincopados.",
                components={
                    "kick": {"engine": "synthesis", "asset_ref": None, "parameters": {"body_hz": 90, "click_hz": 3000}},
                    "snare": {"engine": "synthesis", "asset_ref": None, "parameters": {"tone_hz": 190, "noise": 0.7}},
                    "hi_hat": {"engine": "synthesis", "asset_ref": None, "parameters": {"decay_ms": 45}},
                },
                source="built-in-fallback",
                rights_note="Nenhum áudio ou preset externo incluído.",
            ),
            RepertoireProfile(
                id="brazilian_funk_heavy_kit",
                style="brazilian_funk_heavy",
                cultural_region="BRAZIL",
                description="Pulsação grave e cortes percussivos secos para uma leitura energética.",
                components={
                    "kick": {"engine": "synthesis", "asset_ref": None, "parameters": {"body_hz": 58, "click_hz": 4200}},
                    "sub_808": {"engine": "optional-synth", "asset_ref": None, "parameters": {"drive": 0.3, "release_ms": 400}},
                    "snare": {"engine": "synthesis", "asset_ref": None, "parameters": {"tone_hz": 210, "noise": 0.8}},
                },
                source="built-in-fallback",
                rights_note="Nenhum áudio ou preset externo incluído.",
            ),
            RepertoireProfile(
                id="brazilian_funk_swing_kit",
                style="brazilian_funk_swing",
                cultural_region="BRAZIL",
                description="Padrão de pulsação com síncopa e variação de microtiming revisável.",
                components={
                    "kick": {"engine": "synthesis", "asset_ref": None, "parameters": {"body_hz": 72, "click_hz": 2800}},
                    "sub_808": {"engine": "optional-synth", "asset_ref": None, "parameters": {"drive": 0.15, "release_ms": 520}},
                    "tamborim": {"engine": "optional-sfz", "asset_ref": None, "parameters": {"decay_ms": 80}},
                },
                source="built-in-fallback",
                rights_note="Nenhum áudio ou preset externo incluído.",
            ),
        ]

    @staticmethod
    def _fallback_chains() -> dict[str, dict[str, Any]]:
        return {
            "boom_bap": {
                "description": "Punch controlado, médios presentes e espaço para a voz.",
                "bus_processing": [
                    {"type": "eq", "bands": [{"freq": 100, "gain_db": 3}, {"freq": 400, "gain_db": -2}, {"freq": 3000, "gain_db": 4}]},
                    {"type": "compressor", "threshold_db": -12, "ratio": 2.5, "attack_ms": 20, "release_ms": 150},
                ],
                "track_processing": {"kick": [{"type": "transient_shaper", "attack": 0.7}], "lead_vocal": [{"type": "deesser", "frequency_hz": 7500}]},
            },
            "brazilian_funk_heavy": {
                "description": "Grave definido, cortes secos e controle de pico; loudness é alvo de medição, não promessa.",
                "bus_processing": [
                    {"type": "multiband_comp", "bands": [{"low_hz": 0, "high_hz": 120, "threshold_db": -25, "ratio": 3.0}]},
                    {"type": "soft_clip", "threshold_db": -0.5},
                    {"type": "limiter", "true_peak": True, "ceiling_db": -1.0},
                ],
                "track_processing": {"sub_808": [{"type": "harmonic_exciter", "drive": 0.3}], "lead_vocal": [{"type": "sidechain_duck", "depth_db": 3.0}]},
            },
            "brazilian_funk_swing": {
                "description": "Suingue controlado com preservação de transientes e abertura para backings.",
                "bus_processing": [
                    {"type": "eq", "bands": [{"freq": 80, "gain_db": 4}, {"freq": 500, "gain_db": -2}, {"freq": 5000, "gain_db": 3}]},
                    {"type": "compressor", "threshold_db": -15, "ratio": 2.0, "attack_ms": 10, "release_ms": 100},
                ],
                "track_processing": {"piano": [{"type": "convolution_reverb", "wet": 0.15}], "backing_vocals": [{"type": "stereo_widener", "width": 1.15}]},
            },
        }
