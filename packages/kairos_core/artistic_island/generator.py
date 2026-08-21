from __future__ import annotations

from pathlib import Path
from typing import Any

from kairos_core.artistic_island.atlas import ALGORITHM_REGISTRY, InstrumentAtlas
from kairos_core.artistic_island.contracts import MixPlan, MixPlanRequest, ProcessingStep


class SkillGenerator:
    """Gera planos de cadeia revisáveis; não processa áudio nem carrega plugins."""

    def __init__(self, atlas: InstrumentAtlas | None = None, atlas_path: Path | None = None) -> None:
        self.atlas = atlas or InstrumentAtlas.load(atlas_path)
        self._algorithms = {item.key: item for item in ALGORITHM_REGISTRY}

    def capabilities(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "name": "kairos-artistic-production-island",
            "enabled": True,
            "execution_mode": "plan-first",
            "replaces_existing_core": False,
            "atlas": self.atlas.to_dict(),
            "algorithms": [item.to_dict() for item in ALGORITHM_REGISTRY],
            "external_plugins_default": False,
            "audio_execution": "delegated-to-explicit-adapter",
        }

    def instruments(self) -> list[dict[str, Any]]:
        return [self.atlas.profiles[name].to_dict() for name in self.atlas.names()]

    def generate_chain(self, request: MixPlanRequest) -> MixPlan:
        profile = self.atlas.get(request.instrument)
        if profile is None:
            known = ", ".join(self.atlas.names()[:12])
            raise ValueError(f"Instrumento não encontrado no Atlas: {request.instrument}. Exemplos: {known}")

        chain: list[ProcessingStep] = []
        if profile.family == "vocals" or "vocal" in profile.tags:
            vocal = profile.vocal
            self._append(
                chain,
                "pitch_corrector",
                {"strength": vocal.get("pitch_strength", 0.5), "speed": 0.7},
                "Estabilizar afinação antes de comprimir a voz.",
            )
            self._append(
                chain,
                "deesser",
                {"freq_hz": vocal.get("deesser_freq_hz", 7000), "threshold_db": -24},
                "Controlar sibilância sem retirar articulação.",
            )

        self._append(
            chain,
            "dynamic_eq",
            {"bands": list(profile.eq_presets), "threshold_db": -26},
            "Aplicar o contorno tonal inicial do perfil do Atlas.",
        )
        self._append(
            chain,
            "multiband_comp",
            {"profile": dict(profile.compression), "crossovers_hz": [120, 800, 4000]},
            "Controlar dinâmica preservando o papel musical do instrumento.",
        )

        if request.include_optional:
            self._append(
                chain,
                "harmonic_exciter",
                {"drive_db": 1.5 if profile.family in {"vocals", "melodic"} else 0.8, "mix": 0.12, "harmonics": "odd"},
                "Adicionar presença harmônica em dose conservadora e revisável.",
            )
            self._append(
                chain,
                "spectral_balancer",
                {"masking_depth_db": 2.0, "reference_id": request.reference_id},
                "Sinalizar mascaramento potencial sem aplicar correção automática.",
            )

        if profile.vocal.get("stack") and request.include_optional:
            voices = int(profile.vocal.get("voices", 2))
            self._append(
                chain,
                "formant_shifter",
                {"shift_semitones": 0.02, "preserve_q": True, "voices": voices},
                "Preparar doubling sutil para ampliar backings sem substituir a voz principal.",
            )
            self._append(
                chain,
                "stereo_widener",
                {"width": min(1.6, 1.0 + voices * 0.08), "mid_gain_db": -0.5, "side_gain_db": 0.8},
                "Abrir a camada vocal mantendo centro e compatibilidade mono.",
            )

        if request.context == "orchestra":
            self._append(
                chain,
                "hrtf_panner",
                {"azimuth": -18 if profile.name.endswith("section") else 12, "elevation": 0, "distance_m": profile.space.get("depth_m", 6)},
                "Posicionar a fonte em profundidade orquestral de forma explícita.",
            )

        if request.context in {"vocal", "cinematic"} or "texture" in profile.roles:
            self._append(
                chain,
                "delay_stack",
                {"time_ms": 180, "feedback": 0.22, "mix": 0.1},
                "Criar cauda temporal controlada para espaço e transição.",
            )

        self._append(
            chain,
            "convolution_reverb",
            {"ir_id": "operator-selected-reference-room", "dry_wet": profile.space.get("reverb_send", 0.2), "predelay_ms": 20},
            "Inserir profundidade somente após o equilíbrio e a dinâmica.",
        )
        self._append(
            chain,
            "stereo_widener",
            {"width": profile.space.get("stereo_width", 1.0), "mid_gain_db": 0, "side_gain_db": 0},
            "Conferir largura final preservando o centro do mix.",
        )

        chain = chain[: request.max_steps]
        warnings: list[str] = []
        if len(chain) < 5:
            warnings.append("A cadeia resultante ficou abaixo de cinco etapas após os limites solicitados.")
        if request.reference_id is None and "spectral_balancer" in {step.algorithm for step in chain}:
            warnings.append("Spectral Balancer está em modo sugestão; nenhum áudio de referência foi anexado.")
        warnings.append("Execução DSP, VST/AU/LV2 e processamento de stems exigem adapter explícito e não ocorrem neste endpoint.")

        return MixPlan(
            instrument=profile.name,
            family=profile.family,
            context=request.context,
            profile_found=True,
            source=self.atlas.source_status,
            chain=chain,
            master_bus={
                "integrated_lufs_target": -14,
                "true_peak_db_target": -1,
                "sample_rate": 48000,
                "bit_depth": 24,
                "dither": "final-stage-only",
            },
            provenance={
                "atlas_instrument": profile.name,
                "reference_id": request.reference_id,
                "prompt": request.prompt,
                "external_plugin_execution": False,
            },
            warnings=warnings,
        )

    def _append(self, chain: list[ProcessingStep], algorithm: str, parameters: dict[str, Any], rationale: str) -> None:
        if algorithm not in self._algorithms:
            raise ValueError(f"Algoritmo não registrado: {algorithm}")
        spec = self._algorithms[algorithm]
        chain.append(
            ProcessingStep(
                order=len(chain) + 1,
                algorithm=algorithm,
                parameters=parameters,
                rationale=rationale,
                execution_mode=spec.execution_mode,
            )
        )
