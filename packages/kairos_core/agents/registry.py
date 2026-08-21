from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from kairos_core.agents.clients import LlamaGenClient, SkyReelsSpaceClient
from kairos_core.config import Settings


@dataclass(frozen=True, slots=True)
class AgentCapability:
    name: str
    kind: str
    source: str
    enabled: bool
    ready: bool
    skills: tuple[str, ...]
    algorithms: tuple[str, ...]
    operations: tuple[str, ...]
    notes: str


class AgentAggregator:
    """Catálogo seguro de agentes audiovisuais e de pré-visualização."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def catalog(self) -> dict[str, Any]:
        capabilities = [self._local_capability(), self._space_capability(), self._llamagen_capability()]
        return {
            "schema_version": 1,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "enabled": self.settings.agent_aggregator_enabled,
            "agents": [asdict(capability) for capability in capabilities],
        }

    def probe(self, name: str) -> dict[str, Any]:
        if not self.settings.agent_aggregator_enabled:
            raise RuntimeError(
                "Agregador desabilitado; defina KAIROS_AGENT_AGGREGATOR_ENABLED=true conscientemente"
            )
        if name == "skyreels-space":
            if not self.settings.skyreels_space_enabled:
                raise RuntimeError("SkyReels Space está desabilitado")
            client = SkyReelsSpaceClient(self.settings)
            return {"agent": name, "info": client.info(), "config": client.config()}
        if name == "llamagen":
            if not self.settings.llamagen_enabled:
                raise RuntimeError("LlamaGen está desabilitado")
            return {"agent": name, "health": LlamaGenClient(self.settings).health()}
        if name == "skyreels-native":
            return {"agent": name, "enabled": self.settings.enable_skyreels}
        raise ValueError(f"Agente desconhecido: {name}")

    def _local_capability(self) -> AgentCapability:
        return AgentCapability(
            name="skyreels-native",
            kind="local_gpu",
            source="KAIR-S-SONICA/SkyReels-V2 mounted checkpoint",
            enabled=self.settings.enable_skyreels,
            ready=self.settings.enable_skyreels and self.settings.skyreels_native_api,
            skills=("text-to-video", "image-to-video", "video-extension", "start-end-frame"),
            algorithms=("Diffusion Forcing", "rectified-flow scheduler", "temporal overlap history"),
            operations=("POST /v1/video/generate", "GET /v1/video/capabilities", "GET /v1/tasks/{task_id}"),
            notes="Execução local; readiness também depende de CUDA, runtime e checkpoint.",
        )

    def _space_capability(self) -> AgentCapability:
        return AgentCapability(
            name="skyreels-space",
            kind="remote_gradio_agent",
            source="https://huggingface.co/spaces/fffiloni/SkyReels-V2/agents.md",
            enabled=self.settings.agent_aggregator_enabled and self.settings.skyreels_space_enabled,
            ready=self.settings.agent_aggregator_enabled and self.settings.skyreels_space_enabled,
            skills=("remote-text-to-video", "optional-image-conditioning", "gradio-file-upload", "sse-polling"),
            algorithms=("SkyReels-V2 Diffusion Forcing", "Gradio queue", "server-side checkpoint"),
            operations=("GET /gradio_api/info", "GET /config", "POST /gradio_api/upload", "POST /gradio_api/call/v2/{endpoint}"),
            notes="Endpoint remoto descoberto por agents.md; o schema pode mudar e deve ser consultado antes de gerar.",
        )

    def _llamagen_capability(self) -> AgentCapability:
        key_available = bool(os.getenv(self.settings.llamagen_api_key_env))
        enabled = self.settings.agent_aggregator_enabled and self.settings.llamagen_enabled
        return AgentCapability(
            name="llamagen",
            kind="remote_rest_agent",
            source="https://llamagen.ai/comic-api/docs",
            enabled=enabled,
            ready=enabled and key_available,
            skills=("storyboard", "comic-panels", "character-references", "location-references", "panel-regeneration"),
            algorithms=("structured comic generation", "reference-conditioned identity consistency", "polling lifecycle"),
            operations=("POST /v1/comics/upload", "POST /v1/comics/generations", "GET /v1/comics/generations/{id}", "PATCH /v1/comics/generations/{id}"),
            notes="Bearer token lido apenas de ambiente; geração não é disparada pelo catálogo.",
        )
