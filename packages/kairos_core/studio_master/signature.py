from __future__ import annotations

from kairos_core.studio_master.v2_contracts import SignatureModePlan, SignatureModeRequest


class KairosSignaturePlanner:
    """Propõe uma assinatura de mix em termos de parâmetros, não de imitação de fonte."""

    def plan(self, request: SignatureModeRequest) -> SignatureModePlan:
        intensity = request.intensity
        low_end = request.low_end_focus
        presence = request.vocal_presence
        depth = request.spatial_depth
        chain = [
            {
                "algorithm": "dynamic_eq",
                "parameters": {
                    "low_shelf_db": round(1.5 + 4.0 * low_end * intensity, 3),
                    "presence_db": round(1.0 + 3.5 * presence * intensity, 3),
                    "air_db": round(0.5 + 2.0 * presence * intensity, 3),
                },
                "rationale": "Grave controlado e inteligibilidade vocal, sem copiar uma curva externa.",
                "execution_mode": "adapter-required",
            },
            {
                "algorithm": "multiband_comp",
                "parameters": {
                    "low_ratio": round(1.4 + 1.8 * intensity, 3),
                    "mid_ratio": round(1.3 + 1.4 * presence, 3),
                    "attack_ms": round(8 - 4 * intensity, 3),
                },
                "rationale": "Densidade musical com headroom preservado.",
                "execution_mode": "numpy-preview-or-adapter",
            },
            {
                "algorithm": "harmonic_exciter",
                "parameters": {"drive": round(0.02 + 0.10 * intensity, 3), "mix": round(0.10 + 0.20 * presence, 3)},
                "rationale": "Textura harmônica moderada e reproduzível.",
                "execution_mode": "numpy-preview-or-adapter",
            },
            {
                "algorithm": "stereo_widener",
                "parameters": {"width": round(1.0 + 0.25 * depth, 3), "low_mono_hz": 120},
                "rationale": "Espaço controlado com baixa frequência centrada.",
                "execution_mode": "numpy-preview-or-adapter",
            },
            {
                "algorithm": "convolution_reverb",
                "parameters": {"wet": round(0.03 + 0.10 * depth, 3), "pre_delay_ms": round(18 + 30 * depth, 3)},
                "rationale": "Profundidade curta para não afastar a voz.",
                "execution_mode": "numpy-preview-or-adapter",
            },
            {
                "algorithm": "limiter",
                "parameters": {"ceiling_db": -1.0, "release_ms": 80},
                "rationale": "Teto de distribuição conservador e verificável.",
                "execution_mode": "adapter-required",
            },
        ]
        return SignatureModePlan(
            target=request.target,
            chain=chain,
            guardrails={
                "max_true_peak_db": -1.0,
                "reference_matching": False,
                "source_imitation": False,
                "automatic_file_write": False,
                "approval_required": True,
            },
            provenance={
                "method": "kairos-signature-parametric/v1",
                "source": "operator-configured production attributes",
                "requires_operator_review": True,
            },
            warnings=[
                "A assinatura é uma proposta paramétrica e não uma cópia de artista ou gravação.",
                "O processamento de arquivo exige adapter DSP explícito e aprovação.",
            ],
        )
