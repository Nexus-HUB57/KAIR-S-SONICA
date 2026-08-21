from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from math import ceil
from typing import Any


@dataclass(frozen=True, slots=True)
class ComplementaryScene:
    scene_id: str
    order: int
    start_seconds: float
    end_seconds: float
    prompt: str
    visual_sources: tuple[str, ...]
    agent_handoff: tuple[str, ...]
    video_request_template: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ComplementaryPlan:
    plan_id: str
    architecture: str
    role: str
    prompt: str
    duration_seconds: float
    aspect_ratio: str
    resolution: str
    fps: int
    audio: dict[str, Any]
    media: dict[str, Any]
    scenes: tuple[ComplementaryScene, ...]
    handoff: dict[str, Any]
    guardrails: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["guardrails"] = list(self.guardrails)
        payload["scenes"] = []
        for scene in self.scenes:
            scene_payload = asdict(scene)
            scene_payload["visual_sources"] = list(scene.visual_sources)
            scene_payload["agent_handoff"] = list(scene.agent_handoff)
            payload["scenes"].append(scene_payload)
        return payload


def complementary_capabilities(*, enabled: bool = True) -> dict[str, Any]:
    """Descreve a camada complementar sem sondar rede ou iniciar geração."""
    return {
        "name": "complementary-audiovisual-core",
        "version": 1,
        "enabled": enabled,
        "role": "planning-and-handoff",
        "replaces_existing_core": False,
        "capabilities": [
            "prompt-to-scene-plan",
            "stock-media-slot-planning",
            "tts-or-music-slot-planning",
            "skyreels-request-handoff",
            "llamagen-storyboard-handoff",
        ],
        "optional_adapters": {
            "pexels": {"enabled_by_default": False, "secret_env": "PEXELS_API_KEY"},
            "tts": {"enabled_by_default": False, "implementation": "operator-selected"},
            "musicgen": {"enabled_by_default": False, "implementation": "operator-selected"},
        },
        "handoff_contracts": [
            "POST /v1/video/generate",
            "POST /v1/orchestrate",
            "GET /v1/agents/capabilities",
            "GET /v1/agents/{agent_name}/probe",
        ],
    }


def build_complementary_plan(
    *,
    prompt: str,
    duration_seconds: float = 15.0,
    aspect_ratio: str = "9:16",
    resolution: str = "720P",
    fps: int = 24,
    scene_seconds: float = 5.0,
    audio_mode: str = "external-slot",
    media_mode: str = "generated-or-stock-slot",
    seed: int | None = None,
) -> ComplementaryPlan:
    """Cria um plano de pré-produção; não chama Pexels, TTS, LlamaGen ou SkyReels."""
    normalized_prompt = _normalize_prompt(prompt)
    if duration_seconds <= 0:
        raise ValueError("duration_seconds deve ser positivo")
    if scene_seconds <= 0:
        raise ValueError("scene_seconds deve ser positivo")
    if aspect_ratio not in {"9:16", "16:9", "1:1"}:
        raise ValueError("aspect_ratio deve ser 9:16, 16:9 ou 1:1")
    if resolution not in {"540P", "720P"}:
        raise ValueError("resolution deve ser 540P ou 720P")
    if fps < 1 or fps > 120:
        raise ValueError("fps deve estar entre 1 e 120")
    scene_count = max(1, ceil(duration_seconds / scene_seconds))
    actual_scene_seconds = duration_seconds / scene_count
    plan_id = _plan_id(normalized_prompt, duration_seconds, aspect_ratio, resolution, seed)
    scenes: list[ComplementaryScene] = []
    for index in range(scene_count):
        start = round(index * actual_scene_seconds, 3)
        end = round(duration_seconds if index == scene_count - 1 else (index + 1) * actual_scene_seconds, 3)
        scene_id = f"{plan_id}-s{index + 1:02d}"
        scene_prompt = _scene_prompt(normalized_prompt, index + 1, scene_count)
        scenes.append(
            ComplementaryScene(
                scene_id=scene_id,
                order=index + 1,
                start_seconds=start,
                end_seconds=end,
                prompt=scene_prompt,
                visual_sources=("skyreels-native", "skyreels-space", "pexels-slot"),
                agent_handoff=("skyreels-native", "skyreels-space"),
                video_request_template={
                    "prompt": scene_prompt,
                    "mode": "t2v",
                    "engine": "diffusion_forcing",
                    "backend": "native",
                    "resolution": resolution,
                    "fps": fps,
                    "duration_seconds": round(end - start, 3),
                    "seed": seed,
                    "complementary_plan_id": plan_id,
                    "complementary_scene_id": scene_id,
                },
            )
        )
    return ComplementaryPlan(
        plan_id=plan_id,
        architecture="complementary-audiovisual-core.v1",
        role="planning-and-handoff",
        prompt=normalized_prompt,
        duration_seconds=duration_seconds,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        fps=fps,
        audio={
            "mode": audio_mode,
            "status": "slot-only",
            "source": "external-or-existing-audio-pipeline",
            "handoff": "POST /v1/orchestrate",
        },
        media={
            "mode": media_mode,
            "status": "slot-only",
            "pexels": {"enabled": False, "secret_env": "PEXELS_API_KEY"},
            "download_policy": "not-executed-by-planner",
        },
        scenes=tuple(scenes),
        handoff={
            "video": "POST /v1/video/generate",
            "audio_visual": "POST /v1/orchestrate",
            "agents": "GET /v1/agents/capabilities",
            "probe": "GET /v1/agents/{agent_name}/probe",
            "promotion": "existing-task-store-and-ffprobe-gates",
        },
        guardrails=(
            "complementary layer does not replace the KAIR gateway",
            "complementary layer does not replace the persistent worker",
            "external services remain disabled until explicit operator enablement",
            "secrets and model weights never belong in Git",
            "planner never downloads media or models",
        ),
    )


def _normalize_prompt(prompt: str) -> str:
    normalized = re.sub(r"\s+", " ", prompt).strip()
    if not normalized:
        raise ValueError("prompt não pode ser vazio")
    if len(normalized) > 4_000:
        raise ValueError("prompt excede 4.000 caracteres")
    return normalized


def _plan_id(prompt: str, duration: float, aspect_ratio: str, resolution: str, seed: int | None) -> str:
    material = f"{prompt}|{duration}|{aspect_ratio}|{resolution}|{seed}"
    return "cap-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def _scene_prompt(prompt: str, order: int, count: int) -> str:
    return f"Scene {order}/{count}: {prompt}; continuous cinematic audiovisual treatment, no text, no watermark."
