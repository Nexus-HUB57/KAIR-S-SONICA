from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from pydantic import BaseModel, Field


@dataclass(frozen=True, slots=True)
class AgentRole:
    key: str
    title: str
    mission: str
    skills: tuple[str, ...]
    stage: str


AGENT_ROLES: tuple[AgentRole, ...] = (
    AgentRole("ceo", "CEO / Diretor Geral", "Definir estratégia, riscos e critérios de aprovação.", ("strategy", "risk", "approval"), "strategy"),
    AgentRole("cco", "Diretor de Criação", "Fixar identidade visual, mood e guia de estilo.", ("art-direction", "moodboard", "palette"), "creative"),
    AgentRole("scriptwriter", "Roteirista-Chefe", "Converter briefing em narrativa e cenas executáveis.", ("screenwriting", "scene-structure", "visual-prompts"), "script"),
    AgentRole("dop", "Diretor de Fotografia", "Definir enquadramentos, luz e movimento de câmera.", ("cinematography", "storyboard", "lighting"), "visual"),
    AgentRole("sound_designer", "Designer de Som / Trilha", "Planejar narração, trilha, efeitos e mixagem.", ("audio-design", "tts-slot", "music-slot"), "audio"),
    AgentRole("editor", "Editor-Chefe", "Montar o rough cut e sincronizar vídeo, áudio e legendas.", ("editing", "timeline", "ffmpeg-handoff"), "edit"),
    AgentRole("vfx", "Especialista em VFX / Animação", "Planejar efeitos, motion graphics e animações.", ("vfx", "animation", "compositing"), "visual"),
    AgentRole("social", "Diretor de Mídias Sociais", "Adaptar o pacote para canais e formatos de publicação.", ("reels", "shorts", "metadata"), "distribution"),
    AgentRole("producer", "Produtor Executivo", "Gerenciar cronograma, recursos, dependências e handoffs.", ("schedule", "resource-gates", "delivery"), "production"),
    AgentRole("rag", "Pesquisador / Arquivista RAG", "Recuperar referências e momentos sem gerar conteúdo automaticamente.", ("hybrid-search", "media-retrieval", "provenance"), "research"),
    AgentRole("accessibility", "Legendas e Acessibilidade", "Planejar legendas, tradução, descrição e SEO acessível.", ("captions", "srt", "accessibility"), "accessibility"),
    AgentRole("qa", "QA / Crítico", "Verificar requisitos técnicos/artísticos e solicitar iteração.", ("quality", "ffprobe-gates", "review"), "quality"),
)


class AgenticRunRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4_000)
    project_id: str = Field(default="default", min_length=1, max_length=120)
    duration_seconds: float = Field(default=15.0, gt=0, le=600.0)
    aspect_ratio: Literal["9:16", "16:9", "1:1"] = "9:16"
    resolution: Literal["540P", "720P"] = "720P"
    fps: int = Field(default=24, ge=1, le=120)
    scene_seconds: float = Field(default=5.0, gt=0, le=60.0)
    audio_mode: str = Field(default="external-slot", min_length=1, max_length=80)
    media_mode: str = Field(default="generated-or-stock-slot", min_length=1, max_length=120)
    seed: int | None = Field(default=None, ge=0, le=2**32 - 2)
    include_media_references: bool = False
    submit_handoffs: bool = False
    approve_handoffs: bool = False
    max_iterations: int = Field(default=1, ge=1, le=3)


@dataclass(frozen=True, slots=True)
class Handoff:
    from_agent: str
    to_agent: str
    kind: str
    payload: dict[str, Any]
    requires_approval: bool = False
    schema_version: int = 1

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AgenticRunResult:
    run_id: str
    project_id: str
    status: str
    roles: list[dict[str, Any]]
    artifacts: dict[str, Any]
    handoffs: list[Handoff] = field(default_factory=list)
    checkpoints: list[dict[str, Any]] = field(default_factory=list)
    approvals: list[dict[str, Any]] = field(default_factory=list)
    memory: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "project_id": self.project_id,
            "status": self.status,
            "roles": self.roles,
            "artifacts": self.artifacts,
            "handoffs": [handoff.to_dict() for handoff in self.handoffs],
            "checkpoints": self.checkpoints,
            "approvals": self.approvals,
            "memory": self.memory,
        }
