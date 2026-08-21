from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kairos_core.artistic_island.contracts import AlgorithmSpec, InstrumentProfile

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only in minimal production images
    yaml = None


DEFAULT_ATLAS_PATH = Path(__file__).resolve().parents[3] / "config" / "instrument_atlas.yaml"

ALGORITHM_REGISTRY: tuple[AlgorithmSpec, ...] = (
    AlgorithmSpec(
        "dynamic_eq",
        "Dynamic EQ",
        "Equalização por bandas com threshold adaptativo.",
        {"bands": "lista de bandas freq/gain/Q", "threshold_db": "limiar opcional"},
        "numpy-compatible",
        "scipy/pedalboard",
    ),
    AlgorithmSpec(
        "multiband_comp",
        "Multiband Compressor",
        "Compressão independente por faixas com crossover revisável.",
        {"crossovers_hz": "lista crescente", "ratio": "1..20", "attack_ms": "ms", "release_ms": "ms"},
        "numpy-compatible",
        "scipy/pedalboard",
    ),
    AlgorithmSpec(
        "transient_shaper",
        "Transient Shaper",
        "Controle de ataque e sustain por envelope.",
        {"attack_gain_db": "-24..24", "sustain_gain_db": "-24..24"},
        "contract-only",
        "optional DSP adapter",
    ),
    AlgorithmSpec(
        "harmonic_exciter",
        "Harmonic Exciter",
        "Saturação tonal limitada por mix e cutoff.",
        {"drive_db": "0..18", "mix": "0..1", "harmonics": "odd/even"},
        "contract-only",
        "optional DSP adapter",
    ),
    AlgorithmSpec(
        "spectral_balancer",
        "Spectral Balancer",
        "Sugestão de equilíbrio espectral sem aplicar áudio automaticamente.",
        {"masking_depth_db": "0..12", "reference_id": "id opcional"},
        "contract-only",
        "optional RAG/DSP adapter",
    ),
    AlgorithmSpec(
        "deesser",
        "De-Esser",
        "Redução de sibilância em voz e elementos brilhantes.",
        {"freq_hz": "5000..10000", "threshold_db": "limiar"},
        "contract-only",
        "optional DSP adapter",
    ),
    AlgorithmSpec(
        "pitch_corrector",
        "Pitch Corrector",
        "Correção de afinação como etapa opcional e revisável.",
        {"strength": "0..1", "speed": "0..1"},
        "contract-only",
        "crepe/pyin adapter",
    ),
    AlgorithmSpec(
        "formant_shifter",
        "Formant Shifter",
        "Variação de formantes para backing vocals e doubling.",
        {"shift_semitones": "-12..12", "preserve_q": "boolean"},
        "contract-only",
        "optional DSP adapter",
    ),
    AlgorithmSpec(
        "convolution_reverb",
        "Convolution Reverb",
        "Profundidade baseada em resposta impulsiva registrada.",
        {"ir_id": "id do IR", "dry_wet": "0..1", "predelay_ms": "ms"},
        "contract-only",
        "optional DSP adapter",
    ),
    AlgorithmSpec(
        "stereo_widener",
        "Stereo Widener",
        "Largura estéreo com proteção de compatibilidade mono.",
        {"width": "0..2", "mid_gain_db": "dB", "side_gain_db": "dB"},
        "contract-only",
        "optional DSP adapter",
    ),
    AlgorithmSpec(
        "delay_stack",
        "Delay Stack",
        "Repetições temporizadas para textura, adlibs e transições.",
        {"time_ms": "ms", "feedback": "0..0.95", "mix": "0..1"},
        "contract-only",
        "optional DSP adapter",
    ),
    AlgorithmSpec(
        "hrtf_panner",
        "HRTF Panner",
        "Posicionamento espacial opcional para contextos orquestrais.",
        {"azimuth": "-180..180", "elevation": "-90..90", "distance_m": "metros"},
        "contract-only",
        "optional spatial adapter",
    ),
)


@dataclass(frozen=True, slots=True)
class InstrumentAtlas:
    profiles: dict[str, InstrumentProfile]
    source_path: Path | None
    source_status: str

    @classmethod
    def load(cls, path: Path | None = None) -> InstrumentAtlas:
        atlas_path = path or DEFAULT_ATLAS_PATH
        if yaml is None or not atlas_path.is_file():
            return cls(_fallback_profiles(), None, "embedded-fallback")
        payload = yaml.safe_load(atlas_path.read_text(encoding="utf-8")) or {}
        raw_instruments = payload.get("instruments", {})
        profiles: dict[str, InstrumentProfile] = {}
        for family, entries in raw_instruments.items():
            for name, raw in (entries or {}).items():
                profile = _profile_from_yaml(name, family, raw or {})
                profiles[profile.name] = profile
        if not profiles:
            return cls(_fallback_profiles(), atlas_path, "yaml-empty-fallback")
        return cls(profiles, atlas_path, "yaml")

    def get(self, name: str) -> InstrumentProfile | None:
        return self.profiles.get(name.strip().lower())

    def names(self) -> list[str]:
        return sorted(self.profiles)

    def families(self) -> list[str]:
        return sorted({profile.family for profile in self.profiles.values()})

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": str(self.source_path) if self.source_path else self.source_status,
            "source_status": self.source_status,
            "instrument_count": len(self.profiles),
            "families": self.families(),
            "instruments": [profile.to_dict() for profile in self.profiles.values()],
        }


def algorithm_specs() -> list[dict[str, Any]]:
    return [item.to_dict() for item in ALGORITHM_REGISTRY]


def _profile_from_yaml(name: str, family: str, raw: dict[str, Any]) -> InstrumentProfile:
    normalized_name = str(name).lower()
    return InstrumentProfile(
        name=normalized_name,
        family=str(raw.get("family", family)),
        roles=tuple(str(item) for item in raw.get("roles", [])),
        tags=tuple(str(item) for item in raw.get("tags", [])),
        eq_presets=tuple(dict(item) for item in raw.get("eq_presets", [])),
        compression=dict(raw.get("compression", {})),
        space=dict(raw.get("space", {})),
        vocal=dict(raw.get("vocal", {})),
    )


def _fallback_profiles() -> dict[str, InstrumentProfile]:
    return {
        "kick": InstrumentProfile(
            "kick",
            "rhythm_section",
            ("low-end", "transient"),
            ("kick", "punch"),
            ({"type": "peak", "freq_hz": 60, "gain_db": 2.0, "q": 0.9},),
            {"threshold_db": -18, "ratio": 4.0, "attack_ms": 8, "release_ms": 90},
            {"reverb_send": 0.04, "stereo_width": 0.7, "depth_m": 1.5},
        ),
        "lead_vocal": InstrumentProfile(
            "lead_vocal",
            "vocals",
            ("lead", "presence"),
            ("vocal", "lead"),
            ({"type": "peak", "freq_hz": 2800, "gain_db": 1.5, "q": 1.0},),
            {"threshold_db": -20, "ratio": 4.0, "attack_ms": 5, "release_ms": 80},
            {"reverb_send": 0.15, "stereo_width": 0.8, "depth_m": 3.0},
            {"deesser_freq_hz": 7200, "pitch_strength": 0.65, "stack": False},
        ),
        "synth_pad": InstrumentProfile(
            "synth_pad",
            "melodic",
            ("harmony", "atmosphere", "width"),
            ("pad", "synth", "texture"),
            ({"type": "highpass", "freq_hz": 120, "gain_db": 0, "q": 0.7},),
            {"threshold_db": -24, "ratio": 2.0, "attack_ms": 30, "release_ms": 220},
            {"reverb_send": 0.34, "stereo_width": 1.35, "depth_m": 7.0},
        ),
    }
