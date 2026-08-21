from __future__ import annotations

from typing import Any

from kairos_core.studio_master.canon import CanonIndex
from kairos_core.studio_master.contracts import ResponsiveMixPlan, ResponsivePlanRequest
from kairos_core.studio_master.repertoire import RepertoireCatalog


class StudioMasterPlanner:
    """Converte intenção musical em plano executável apenas após aprovação."""

    def __init__(self, canon: CanonIndex, repertoire: RepertoireCatalog) -> None:
        self.canon = canon
        self.repertoire = repertoire

    def capabilities(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "name": "kairos-studiomaster",
            "enabled": True,
            "execution_mode": "plan-first",
            "deterministic_analyzer": "onset-energy/v1",
            "optional_adapters": [
                "neural-groove-extractor",
                "librosa",
                "aubio",
                "pedalboard",
                "pyrubberband",
                "fluidsynth",
                "demucs",
                "crepe",
                "matchering",
                "chromadb",
                "mosnet",
                "moviepy",
            ],
            "phase7_pillars": [
                "auto-retraining-gate",
                "kairos-signature-plan",
                "viral-clip-plan",
                "production-analytics",
            ],
            "external_generation_default": False,
            "canon_metadata_only": True,
            "commands": ["SET_SWING", "SET_GRID_FOLLOW", "BOOST_PUNCHLINE", "PUSH_TO_LIBRARY"],
        }

    def canon_entries(self) -> list[dict[str, Any]]:
        return self.canon.entries()

    def repertoire_profiles(self) -> list[dict[str, Any]]:
        return self.repertoire.profiles()

    def responsive_plan(self, request: ResponsivePlanRequest) -> ResponsiveMixPlan:
        effective_bpm = request.flow.bpm if request.flow else request.bpm
        effective_swing = request.flow.swing_ratio if request.flow else request.swing_ratio
        canon_entry = self.canon.nearest(
            bpm=effective_bpm,
            swing_ratio=effective_swing,
            canon_id=request.canon_id or (request.flow.canon_match if request.flow else None),
        )
        profile = self.repertoire.get(request.repertoire_id, style=request.style)
        chain = self.repertoire.mixing_chain(profile.style)
        quarter_ms = 60_000 / effective_bpm
        swing_ms = round((effective_swing - 0.5) * quarter_ms, 4)
        humanize_ms = round(
            max(request.humanize_ms, min(request.flow.offset_std_ms, 30.0)) if request.flow else request.humanize_ms,
            4,
        )
        vocal_chain = (chain.get("track_processing") or {}).get("lead_vocal", [])
        warnings = [
            "Plano não renderiza áudio e não inicia uma tarefa automaticamente.",
            "Use apenas samples, gravações e presets com procedência e licença verificáveis.",
        ]
        if request.flow and request.flow.method != "neural-groove-extractor":
            warnings.append("O flow recebido foi produzido por um método não neural; revise a confiança antes do bounce.")
        if request.grid_follow and not request.flow:
            warnings.append("Grid follow está ativo, mas nenhum mapa de flow foi fornecido; o plano usa o swing declarado.")
        return ResponsiveMixPlan(
            style=profile.style,
            canon={**canon_entry.to_dict(), "match_type": "explicit" if request.canon_id else "nearest"},
            repertoire={**profile.to_dict(), "mixing_chain": chain},
            timing={
                "bpm": round(effective_bpm, 4),
                "swing_ratio": round(effective_swing, 6),
                "swing_ms": swing_ms,
                "humanize_ms": humanize_ms,
                "grid_follow": request.grid_follow,
                "offbeat_policy": "follow_flow_then_apply_swing" if request.grid_follow else "preserve_source_timing",
            },
            vocal_focus={
                "enabled": request.vocal_focus,
                "sidechain": "multiband-keyed-by-lead-vocal" if request.vocal_focus else "disabled",
                "lead_vocal_chain": vocal_chain,
                "punchline": {
                    "enabled": request.punchline_enabled,
                    "gain_db": 3.0 if request.punchline_enabled else 0.0,
                    "reverb_reduction_db": 3.0 if request.punchline_enabled else 0.0,
                    "trigger": "explicit-performance-command",
                },
            },
            handoff={
                "target": "POST /v1/orchestrate",
                "approval_required": True,
                "request_patch": {
                    "bpm": round(effective_bpm),
                    "swing": round(effective_swing, 6),
                    "humanize_ms": humanize_ms,
                    "genre": profile.style,
                    "stems": True,
                },
            },
            warnings=warnings,
        )
