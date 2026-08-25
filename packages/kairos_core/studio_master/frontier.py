from __future__ import annotations

import importlib.util
import shutil
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from kairos_core.config import Settings

FrontierProfile = Literal[
    "audio_reactive_video",
    "music_video",
    "live_capture",
    "release_preflight",
]
ComputeTarget = Literal["auto", "cpu", "webgpu", "cuda"]
AudioBackend = Literal["web_audio", "webcodecs", "ffmpeg"]
VideoBackend = Literal["browser_webcodecs", "ltx2_optional", "skyreels_optional"]
AspectRatio = Literal["9:16", "16:9", "1:1"]


class FrontierPlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile: FrontierProfile = "audio_reactive_video"
    duration_seconds: float = Field(default=15.0, gt=0, le=300)
    aspect_ratio: AspectRatio = "9:16"
    fps: int = Field(default=24, ge=1, le=120)
    compute: ComputeTarget = "auto"
    audio_backend: AudioBackend = "web_audio"
    video_backend: VideoBackend = "browser_webcodecs"
    approved_asset_id: str | None = Field(default=None, min_length=1, max_length=160)


class FrontierComponent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    component_id: str = Field(min_length=1, max_length=120)
    surface: Literal["browser", "server", "optional_adapter", "control_plane"]
    status: Literal["READY", "OPTIONAL", "FALLBACK_ONLY", "NOT_CONFIGURED"]
    capability: str = Field(min_length=1, max_length=500)
    requirement: str = Field(min_length=1, max_length=500)
    fallback: str = Field(min_length=1, max_length=240)
    provenance: str = Field(min_length=1, max_length=500)


class FrontierPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    status: Literal["READY_FOR_APPROVAL"] = "READY_FOR_APPROVAL"
    method: str = Field(default="capability-first-av-orchestration/v1", max_length=120)
    harness: Literal["PHD"] = "PHD"
    profile: FrontierProfile
    target: dict[str, Any]
    selected_stack: list[str] = Field(min_length=1, max_length=16)
    stages: list[dict[str, Any]] = Field(min_length=4, max_length=12)
    gates: dict[str, Any]
    handoff: dict[str, Any]
    fallbacks: list[str] = Field(min_length=1, max_length=12)
    warnings: list[str] = Field(default_factory=list, max_length=24)


class AudiovisualFrontier:
    """Catálogo plan-first de uma arquitetura audiovisual de última geração.

    O módulo descreve capacidades e produz planos auditáveis. Ele não baixa
    modelos, não inicia renderizações e não promove nenhum ativo sem aprovação.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def capabilities(self) -> dict[str, Any]:
        ffmpeg_ready = shutil.which(self.settings.ffmpeg_bin) is not None
        ffprobe_ready = shutil.which(self.settings.ffprobe_bin) is not None
        demucs_ready = importlib.util.find_spec("demucs") is not None
        ltx2_configured = bool(
            self.settings.ltx2_enabled
            and self.settings.ltx2_repo
            and self.settings.ltx2_model_id
            and self.settings.ltx2_license_accepted
        )
        components = [
            FrontierComponent(
                component_id="web-audio-audio-worklet",
                surface="browser",
                status="READY",
                capability="Captura, monitoramento e controle interativo de áudio no navegador",
                requirement="Permissão do navegador e dispositivo de entrada",
                fallback="MediaRecorder + AudioContext local",
                provenance="Web Audio API / implementação local do StudioMaster",
            ),
            FrontierComponent(
                component_id="webcodecs-av1-opus",
                surface="browser",
                status="OPTIONAL",
                capability="Codificação/decodificação de frames e áudio codificado com controle de baixa camada",
                requirement="Navegador compatível e codec disponível",
                fallback="Canvas + Web Audio + exportação backend",
                provenance="MDN WebCodecs API; integração ainda não executa por padrão",
            ),
            FrontierComponent(
                component_id="webgpu-compute",
                surface="browser",
                status="OPTIONAL",
                capability="Computação paralela e visualização reativa em GPU no browser",
                requirement="HTTPS, navegador compatível e GPU exposta",
                fallback="CPU/NumPy e WebGL/Canvas",
                provenance="MDN WebGPU API; disponibilidade limitada em alguns browsers",
            ),
            FrontierComponent(
                component_id="ffmpeg-ffprobe-delivery",
                surface="server",
                status="READY" if ffmpeg_ready and ffprobe_ready else "FALLBACK_ONLY",
                capability="Probe, transcodificação e entrega controlada de áudio/vídeo",
                requirement="Binários ffmpeg e ffprobe instalados",
                fallback="Entregar WAV e metadados sem transcodificação",
                provenance="Configuração do KAIR-S-SONICA",
            ),
            FrontierComponent(
                component_id="demucs-stem-separation",
                surface="optional_adapter",
                status="OPTIONAL" if demucs_ready else "FALLBACK_ONLY",
                capability="Separação opcional de vocal, drums, bass e accompaniment",
                requirement="Adapter, checkpoint, licença e manifesto de proveniência",
                fallback="approved_stem_handoff sem separação automática",
                provenance="Demucs Hybrid Transformer; projeto upstream arquivado e não mantido ativamente",
            ),
            FrontierComponent(
                component_id="ltx2-audio-video",
                surface="optional_adapter",
                status="READY" if ltx2_configured else "NOT_CONFIGURED",
                capability="Proposta de geração audiovisual sincronizada com áudio",
                requirement="Repo, modelo, GPU, licença aceita e manifesto auditável",
                fallback="browser_webcodecs ou SkyReels já governado pelo pipeline",
                provenance="Lightricks LTX-2; integração não habilita download implícito",
            ),
            FrontierComponent(
                component_id="taskstore-websocket-gates",
                surface="control_plane",
                status="READY",
                capability="Estados observáveis, handoff explícito e acompanhamento em tempo real",
                requirement="TaskStore SQLite e gateway FastAPI",
                fallback="Snapshot HTTP de tarefa",
                provenance="Arquitetura KAIR-S-SONICA",
            ),
        ]
        return {
            "schema_version": 1,
            "name": "kairos-studio-master-frontier",
            "harness": "PHD",
            "harness_meaning": "Preflight · Handoff · Determinism",
            "mode": "plan-first",
            "enabled": True,
            "components": [component.model_dump(mode="json") for component in components],
            "governance": {
                "human_approval_required": True,
                "auto_publish": False,
                "implicit_model_download": False,
                "voice_and_identity_consent_required": True,
                "source_repository": "Nexus-HUB57/KAIR-S-SONICA",
            },
        }

    def plan(self, request: FrontierPlanRequest) -> FrontierPlan:
        capabilities = {item["component_id"]: item for item in self.capabilities()["components"]}
        selected_stack = [
            "intake-and-rights-check",
            "groove-dna-deterministic-v1",
            "taskstore-websocket-gates",
        ]
        warnings = [
            "Este plano é READY_FOR_APPROVAL; não inicia renderização, treino, publicação ou download.",
            "A aprovação humana de KTD continua sendo o gate artístico final.",
        ]
        fallbacks = ["CPU/NumPy", "Canvas/Web Audio", "FFmpeg sem modelo neural", "handoff manual de stem aprovado"]

        if request.audio_backend == "webcodecs":
            selected_stack.append("webcodecs-av1-opus")
            warnings.append("WebCodecs depende de suporte do navegador e codec; o fallback mantém Web Audio/MediaRecorder.")
        elif request.audio_backend == "ffmpeg":
            selected_stack.append("ffmpeg-ffprobe-delivery")
        else:
            selected_stack.append("web-audio-audio-worklet")

        if request.compute == "webgpu":
            selected_stack.append("webgpu-compute")
            warnings.append("WebGPU exige HTTPS e disponibilidade do navegador; localhost HTTP deve usar fallback CPU.")
        elif request.compute == "cuda":
            selected_stack.append("skyreels-optional")
            warnings.append("CUDA só pode ser usado após readiness do host, checkpoint, licença e preflight.")
        else:
            selected_stack.append("cpu-deterministic-preview")

        if request.video_backend == "ltx2_optional":
            selected_stack.append("ltx2-audio-video")
            if capabilities["ltx2-audio-video"]["status"] != "READY":
                warnings.append("LTX-2 foi solicitado como adapter, mas não está configurado com repo/modelo/licença; plano fica em fallback.")
        elif request.video_backend == "skyreels_optional":
            selected_stack.append("skyreels-optional")
            warnings.append("SkyReels continua opcional e requer o preflight do host GPU existente.")
        else:
            selected_stack.append("webcodecs-av1-opus")

        if request.approved_asset_id:
            handoff_payload = {
                "asset_id": request.approved_asset_id,
                "target": "POST /v1/studio/handoff",
                "approval_required": True,
                "submits_task": False,
            }
        else:
            handoff_payload = {
                "target": "POST /v1/studio/handoff",
                "approval_required": True,
                "submits_task": False,
                "asset_id": None,
            }
            warnings.append("Nenhum asset aprovado foi anexado; o handoff permanece um template revisável.")

        stages = [
            {"id": "preflight", "name": "Preflight", "owner": "QA", "output": "capability_matrix"},
            {"id": "intent_lock", "name": "Intent lock", "owner": "Káiros + KTD", "output": "rights_and_style_lock"},
            {"id": "audio_reactive_plan", "name": "Audio-reactive plan", "owner": "Sound Designer", "output": "groove_dna_and_sync_map"},
            {"id": "visual_execution_slot", "name": "Visual execution slot", "owner": "DoP + VFX", "output": "approved_render_request"},
            {"id": "handoff", "name": "Explicit handoff", "owner": "Producer", "output": "MultimediaRequest_patch"},
            {"id": "qa_approval", "name": "QA and approval", "owner": "QA + KTD", "output": "READY_TO_DELIVER_or_REJECTED"},
            {"id": "atomic_delivery", "name": "Atomic delivery", "owner": "Delivery", "output": "manifest_and_checksum"},
        ]
        gates = {
            "preflight": True,
            "human_approval": True,
            "rights_and_consent": True,
            "model_license_and_provenance": request.video_backend != "browser_webcodecs",
            "no_auto_publish": True,
            "deterministic_fallback_required": True,
        }
        return FrontierPlan(
            profile=request.profile,
            target={
                "duration_seconds": request.duration_seconds,
                "aspect_ratio": request.aspect_ratio,
                "fps": request.fps,
                "compute": request.compute,
                "audio_backend": request.audio_backend,
                "video_backend": request.video_backend,
            },
            selected_stack=list(dict.fromkeys(selected_stack)),
            stages=stages,
            gates=gates,
            handoff=handoff_payload,
            fallbacks=fallbacks,
            warnings=warnings,
        )
