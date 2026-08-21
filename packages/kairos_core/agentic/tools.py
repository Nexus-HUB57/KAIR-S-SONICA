from __future__ import annotations

from dataclasses import asdict
from typing import Any

from kairos_core.agentic.contracts import AgenticRunRequest, Handoff
from kairos_core.complementary import provider_chain_from_names
from kairos_core.complementary.planner import build_complementary_plan
from kairos_core.config import Settings
from kairos_core.schemas import MultimediaRequest, VideoRequest
from kairos_core.studio_master import (
    ArrangementArchitect,
    ArrangementRequest,
    CanonIndex,
    KairosSignaturePlanner,
    RepertoireCatalog,
    ResponsivePlanRequest,
    SignatureModeRequest,
    StudioMasterPlanner,
)


class AgenticToolbox:
    """Tools locais e determinísticos; execução externa só ocorre em endpoints explícitos."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        canon = CanonIndex.load(settings.canon_index_path)
        repertoire = RepertoireCatalog.load(settings.instrumentation_repertoire_path)
        self.studio_master = StudioMasterPlanner(canon, repertoire)
        self.arrangement_architect = ArrangementArchitect()
        self.signature_planner = KairosSignaturePlanner()

    def scene_plan(self, request: AgenticRunRequest) -> dict[str, Any]:
        plan = build_complementary_plan(
            prompt=request.prompt,
            duration_seconds=request.duration_seconds,
            aspect_ratio=request.aspect_ratio,
            resolution=request.resolution,
            fps=request.fps,
            scene_seconds=request.scene_seconds,
            audio_mode=request.audio_mode,
            media_mode=request.media_mode,
            seed=request.seed,
        )
        return plan.to_dict()

    def video_handoffs(self, scene_plan: dict[str, Any]) -> list[Handoff]:
        handoffs: list[Handoff] = []
        for index, scene in enumerate(scene_plan["scenes"], start=1):
            template = VideoRequest.model_validate(scene["video_request_template"])
            handoffs.append(
                Handoff(
                    from_agent="scriptwriter",
                    to_agent="vfx",
                    kind="video_request",
                    payload={"scene_index": index, "request": template.model_dump(mode="json")},
                    requires_approval=True,
                )
            )
        return handoffs

    def audio_handoff(self, request: AgenticRunRequest) -> Handoff:
        studio_plan = self.studio_master_plan(request)
        patch = studio_plan.get("handoff", {}).get("request_patch", {})
        audio_request = MultimediaRequest(
            prompt=request.prompt,
            duration_seconds=request.duration_seconds,
            generate_audio=True,
            transcribe=False,
            analyze_audio=False,
            output_format="wav",
            seed=request.seed,
            bpm=int(patch.get("bpm", 140)),
            swing=float(patch.get("swing", 0.60)),
            humanize_ms=float(patch.get("humanize_ms", 6.0)),
            genre=str(patch.get("genre", "Trap Soul")),
        )
        return Handoff(
            from_agent="sound_designer",
            to_agent="audio_pipeline",
            kind="multimedia_request",
            payload={
                "request": audio_request.model_dump(mode="json"),
                "studio_master_plan": studio_plan,
            },
            requires_approval=True,
        )

    def studio_master_plan(self, request: AgenticRunRequest) -> dict[str, Any]:
        if not self.settings.studio_master_enabled:
            return {
                "status": "DISABLED",
                "handoff": {"request_patch": {"bpm": 140, "swing": 0.60, "humanize_ms": 6.0}},
                "warnings": ["StudioMaster desabilitado; usando defaults do pipeline."],
            }
        style = _style_from_prompt(request.prompt)
        responsive = self.studio_master.responsive_plan(
            ResponsivePlanRequest(style=style, bpm=140, swing_ratio=0.60, grid_follow=True)
        ).model_dump(mode="json")
        responsive["arrangement"] = self.arrangement_architect.build(
            ArrangementRequest(style=style, mood=_mood_from_prompt(request.prompt), bpm=140, total_bars=32)
        ).model_dump(mode="json")
        responsive["signature_plan"] = self.signature_planner.plan(
            SignatureModeRequest(target="mix_bus")
        ).model_dump(mode="json")
        responsive["studio_master_2"] = {
            "execution_mode": "plan-first",
            "automatic_render": False,
            "automatic_publish": False,
        }
        return responsive

    def media_references(self, query: str, *, kind: str = "image") -> list[dict[str, Any]]:
        chain = provider_chain_from_names(self.settings.media_provider_order)
        if kind == "video":
            assets = chain.search_videos(query, per_page=5, orientation="portrait")
        else:
            assets = chain.search_images(query, per_page=5)
        return [asdict(asset) for asset in assets]

    def social_variants(self, aspect_ratio: str) -> list[dict[str, Any]]:
        formats = [
            {"channel": "instagram-reels", "aspect_ratio": "9:16", "duration_limit_seconds": 90},
            {"channel": "youtube-shorts", "aspect_ratio": "9:16", "duration_limit_seconds": 60},
            {"channel": "tiktok", "aspect_ratio": "9:16", "duration_limit_seconds": 180},
        ]
        if aspect_ratio == "16:9":
            formats.append({"channel": "youtube-landscape", "aspect_ratio": "16:9", "duration_limit_seconds": 600})
        return formats


def _mood_from_prompt(prompt: str) -> str:
    lowered = prompt.lower()
    if any(token in lowered for token in ("cinematic", "cinemático", "cinematográfico")):
        return "cinematic"
    if any(token in lowered for token in ("nostalgia", "reflexivo", "melancólico")):
        return "reflective"
    if any(token in lowered for token in ("foco", "preciso", "minimal")):
        return "focused"
    return "energetic"


def _style_from_prompt(prompt: str) -> str:
    lowered = prompt.lower()
    if any(token in lowered for token in ("funk", "mandelão", "mandelao", "grave pesado")):
        return "brazilian_funk_heavy"
    if any(token in lowered for token in ("nostalgia", "suingue", "swing", "arrocha")):
        return "brazilian_funk_swing"
    return "boom_bap"
