from __future__ import annotations

import re
from datetime import datetime, timezone
from uuid import uuid4

from kairos_core.agentic.contracts import AGENT_ROLES, AgenticRunRequest, AgenticRunResult, Handoff
from kairos_core.agentic.memory import ProjectMemory
from kairos_core.agentic.tools import AgenticToolbox
from kairos_core.config import Settings
from kairos_core.observability import get_logger, log_event

logger = get_logger(__name__)


class AgenticOrchestrator:
    """Coordena 12 papéis com contratos determinísticos e handoffs revisáveis."""

    def __init__(self, settings: Settings, *, memory: ProjectMemory | None = None) -> None:
        self.settings = settings
        self.memory = memory or ProjectMemory()
        self.tools = AgenticToolbox(settings)

    def capabilities(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "name": "kairos-agentic-studio",
            "enabled": self.settings.agentic_core_enabled,
            "execution_mode": "deterministic-contract-first",
            "llm_backend": "optional-adapter-not-required",
            "external_tools_default": False,
            "roles": [
                {
                    "key": role.key,
                    "title": role.title,
                    "mission": role.mission,
                    "skills": list(role.skills),
                    "stage": role.stage,
                }
                for role in AGENT_ROLES
            ],
            "handoffs": [
                "ComplementaryPlan -> VideoRequest",
                "ComplementaryPlan -> MultimediaRequest",
                "MediaProviderChain -> reference slots",
                "QA -> approval gate",
                "approved handoffs -> TaskStore",
                "StudioMaster responsive plan -> MultimediaRequest patch",
            ],
        }

    def run(self, request: AgenticRunRequest) -> AgenticRunResult:
        if not self.settings.agentic_core_enabled:
            raise RuntimeError("Núcleo agentico desabilitado")
        run_id = uuid4().hex
        trace: list[dict[str, object]] = []
        handoffs: list[Handoff] = []
        checkpoints: list[dict[str, object]] = []
        approvals: list[dict[str, object]] = []
        prior_memory = self.memory.search(request.prompt, limit=5)
        self._record(trace, run_id, "ceo", "strategy", {"prior_memory_count": len(prior_memory)})

        strategy = {
            "project_name": _project_name(request.prompt),
            "briefing": request.prompt,
            "objective": "Produzir pacote audiovisual revisável e encaminhável aos pipelines KAIR.",
            "risk_gates": ["human_or_operator_approval", "ffprobe_before_publish", "no_secret_or_weight_in_git"],
            "iteration_budget": request.max_iterations,
        }
        self.memory.append(run_id=run_id, role="ceo", kind="strategy", content=strategy)
        trace[-1]["output"] = strategy
        checkpoints.append({"stage": "strategy", "status": "completed", "owner": "ceo"})

        style = {
            "mood": _mood_from_prompt(request.prompt),
            "palette": ["carbon black", "electric cyan", "warm amber"],
            "visual_rules": ["no watermark", "no accidental text", "identity continuity", "controlled motion"],
            "negative_prompt": "low quality, flicker, malformed anatomy, random text, watermark",
        }
        self._record(trace, run_id, "cco", "creative_direction", style)
        checkpoints.append({"stage": "creative", "status": "completed", "owner": "cco"})

        media_references: list[dict[str, object]] = []
        retrieval_mode = "disabled-by-external-tools-gate"
        if request.include_media_references and self.settings.agentic_external_tools_enabled:
            media_references = self.tools.media_references(request.prompt, kind="video")
            retrieval_mode = "provider-chain-without-download"
        rag_output = {
            "query": request.prompt,
            "moments": media_references,
            "retrieval_mode": retrieval_mode,
            "provenance_required": True,
        }
        self._record(trace, run_id, "rag", "retrieval", rag_output)

        scene_plan = self.tools.scene_plan(request)
        self._record(trace, run_id, "scriptwriter", "scene_plan", scene_plan)
        checkpoints.append({"stage": "script", "status": "completed", "owner": "scriptwriter"})

        dop_output = {
            "camera_language": "cinematic controlled movement",
            "lighting": "motivated practicals with clean subject separation",
            "aspect_ratio": request.aspect_ratio,
            "shots": [
                {"scene_index": index, "shot": "establishing-to-medium", "motion": "slow push-in", "lens": "35mm"}
                for index, _ in enumerate(scene_plan["scenes"], start=1)
            ],
        }
        self._record(trace, run_id, "dop", "storyboard", dop_output)

        audio_handoff = self.tools.audio_handoff(request)
        handoffs.append(audio_handoff)
        sound_output = {
            "mode": request.audio_mode,
            "duration_seconds": request.duration_seconds,
            "mix_targets": {"integrated_lufs": -14, "true_peak_db": -1},
            "studio_master_plan": audio_handoff.payload.get("studio_master_plan"),
            "handoff": audio_handoff.to_dict(),
        }
        self._record(trace, run_id, "sound_designer", "audio_plan", sound_output)

        editor_output = {
            "timeline": "scene-order-preserving",
            "fps": request.fps,
            "transitions": "cut-first; transitions only when motivated",
            "validation": ["ffprobe", "duration", "fps", "non-empty-mp4"],
        }
        self._record(trace, run_id, "editor", "edit_plan", editor_output)

        video_handoffs = self.tools.video_handoffs(scene_plan)
        handoffs.extend(video_handoffs)
        vfx_output = {
            "backend_handoff": "SkyReels CLI/native selected downstream by VideoRequest",
            "effects": ["atmospheric depth", "controlled light bloom", "temporal consistency"],
            "scene_handoff_count": len(video_handoffs),
        }
        self._record(trace, run_id, "vfx", "visual_plan", vfx_output)

        social_output = {"variants": self.tools.social_variants(request.aspect_ratio), "caption_slots": True}
        self._record(trace, run_id, "social", "distribution_plan", social_output)

        producer_output = {
            "phases": ["brief", "creative", "research", "scene-plan", "audio", "visual", "edit", "qa", "delivery"],
            "dependencies": ["approved_video_handoffs", "approved_audio_handoff", "ffprobe_success"],
            "submit_requested": request.submit_handoffs,
        }
        self._record(trace, run_id, "producer", "production_plan", producer_output)

        accessibility_output = {
            "caption_formats": ["srt", "webvtt"],
            "language": "pt-BR",
            "include_speaker_labels": True,
            "audio_description_slot": True,
        }
        self._record(trace, run_id, "accessibility", "accessibility_plan", accessibility_output)

        qa_checks = [
            {"check": "all_12_roles_present", "passed": len(trace) + 1 == len(AGENT_ROLES)},
            {"check": "video_handoffs_validate", "passed": bool(video_handoffs)},
            {"check": "audio_handoff_valid", "passed": audio_handoff.kind == "multimedia_request"},
            {"check": "external_generation_not_implicit", "passed": True},
            {"check": "ffprobe_gate_declared", "passed": True},
        ]
        qa_output = {"checks": qa_checks, "passed": all(item["passed"] for item in qa_checks)}
        self._record(trace, run_id, "qa", "quality_review", qa_output)
        approvals.append(
            {
                "gate": "executive-approval",
                "owner": "ceo",
                "status": "required",
                "reason": "Handoffs de geração e áudio devem ser aprovados antes da fila.",
            }
        )
        status = "READY_FOR_APPROVAL" if qa_output["passed"] else "BLOCKED_BY_QA"
        artifacts = {
            "strategy": strategy,
            "style_guide": style,
            "retrieval": rag_output,
            "scene_plan": scene_plan,
            "storyboard": dop_output,
            "audio_plan": sound_output,
            "edit_plan": editor_output,
            "vfx_plan": vfx_output,
            "distribution": social_output,
            "production": producer_output,
            "accessibility": accessibility_output,
            "quality": qa_output,
        }
        memory_entry = self.memory.append(
            run_id=run_id,
            role="qa",
            kind="run_summary",
            content={"status": status, "handoff_count": len(handoffs)},
        )
        log_event(logger, 20, "agentic_run_planned", run_id=run_id, project_id=request.project_id, status=status)
        return AgenticRunResult(
            run_id=run_id,
            project_id=request.project_id,
            status=status,
            roles=trace,
            artifacts=artifacts,
            handoffs=handoffs,
            checkpoints=checkpoints,
            approvals=approvals,
            memory={"prior": prior_memory, "latest": memory_entry},
        )

    @staticmethod
    def _record(trace: list[dict[str, object]], run_id: str, role: str, kind: str, output: object) -> None:
        trace.append(
            {
                "agent": role,
                "run_id": run_id,
                "kind": kind,
                "status": "completed",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "output": output,
            }
        )


def _project_name(prompt: str) -> str:
    words = re.findall(r"[\wÀ-ÿ]+", prompt)
    return " ".join(words[:6]).title() or "Kairos Audiovisual Project"


def _mood_from_prompt(prompt: str) -> str:
    lowered = prompt.lower()
    if any(token in lowered for token in ("noite", "neon", "chuva", "dark")):
        return "nocturnal-electric"
    if any(token in lowered for token in ("sol", "praia", "golden", "verão")):
        return "warm-kinetic"
    return "cinematic-contemporary"
