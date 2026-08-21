from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import sqlite3
import threading
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from kairos_core.agentic import AgenticOrchestrator, AgenticRunRequest
from kairos_core.agentic.memory import ProjectMemory
from kairos_core.agents import AgentAggregator, ExternalAgentError
from kairos_core.artistic_island import MixPlan, MixPlanRequest, SkillGenerator
from kairos_core.audio.orchestrator import MultimediaOrchestrator
from kairos_core.audio.pipeline import AudioPipeline
from kairos_core.complementary import (
    MediaCache,
    MediaProviderError,
    build_complementary_plan,
    complementary_capabilities,
    provider_chain_from_names,
)
from kairos_core.config import Settings
from kairos_core.observability import configure_logging
from kairos_core.persona import DEFAULT_PERSONA
from kairos_core.schemas import (
    ComplementaryMediaSearchRequest,
    ComplementaryPlanRequest,
    GenerateResponse,
    MultimediaRequest,
    PersonaResponse,
    Progress,
    TaskSnapshot,
    TrackPlan,
    TrackRequest,
    VideoRequest,
)
from kairos_core.video.orchestrator import VideoOrchestrator


class TaskStore:
    """Armazena snapshots em SQLite para sobreviver a reinícios do processo."""

    def __init__(self, db_path) -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS tasks (task_id TEXT PRIMARY KEY, snapshot TEXT NOT NULL)"
            )
            connection.execute(
                "CREATE TABLE IF NOT EXISTS task_jobs ("
                "task_id TEXT PRIMARY KEY, kind TEXT NOT NULL, payload TEXT NOT NULL, "
                "claimed_at TEXT, FOREIGN KEY(task_id) REFERENCES tasks(task_id))"
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._db_path, timeout=30)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _encode(snapshot: TaskSnapshot) -> str:
        return json.dumps(snapshot.model_dump(mode="json"), ensure_ascii=False)

    @staticmethod
    def _decode(payload: str) -> TaskSnapshot:
        return TaskSnapshot.model_validate(json.loads(payload))

    def create(
        self,
        task_id: str,
        *,
        job_kind: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> TaskSnapshot:
        snapshot = TaskSnapshot(
            task_id=task_id,
            status="PENDING",
            progress=Progress(step="queued", percent=0, message="Tarefa enfileirada"),
        )
        with self._lock, self._connect() as connection:
            connection.execute(
                "INSERT INTO tasks(task_id, snapshot) VALUES (?, ?) "
                "ON CONFLICT(task_id) DO UPDATE SET snapshot = excluded.snapshot",
                (task_id, self._encode(snapshot)),
            )
            if job_kind and payload is not None:
                connection.execute(
                    "INSERT INTO task_jobs(task_id, kind, payload, claimed_at) VALUES (?, ?, ?, NULL) "
                    "ON CONFLICT(task_id) DO UPDATE SET kind = excluded.kind, payload = excluded.payload, claimed_at = NULL",
                    (task_id, job_kind, json.dumps(payload, ensure_ascii=False)),
                )
        return snapshot

    def get(self, task_id: str) -> TaskSnapshot | None:
        with self._lock, self._connect() as connection:
            row = connection.execute(
                "SELECT snapshot FROM tasks WHERE task_id = ?", (task_id,)
            ).fetchone()
        return None if row is None else self._decode(row["snapshot"])

    def update(self, task_id: str, **changes: Any) -> TaskSnapshot:
        with self._lock, self._connect() as connection:
            row = connection.execute(
                "SELECT snapshot FROM tasks WHERE task_id = ?", (task_id,)
            ).fetchone()
            if row is None:
                raise KeyError(task_id)
            current = self._decode(row["snapshot"])
            updated = current.model_copy(
                update={**changes, "updated_at": datetime.now(timezone.utc)}
            )
            connection.execute(
                "UPDATE tasks SET snapshot = ? WHERE task_id = ?",
                (self._encode(updated), task_id),
            )
            if updated.status in {"SUCCEEDED", "FAILED"}:
                connection.execute("DELETE FROM task_jobs WHERE task_id = ?", (task_id,))
        return updated

    def reset_orphaned_jobs(self) -> None:
        """Devolve jobs não terminais ao estado enfileirado após restart do processo."""
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                "SELECT j.task_id, j.payload, t.snapshot FROM task_jobs j "
                "JOIN tasks t ON t.task_id = j.task_id"
            ).fetchall()
            for row in rows:
                snapshot = self._decode(row["snapshot"])
                if snapshot.status not in {"PENDING", "RUNNING"}:
                    continue
                reset = snapshot.model_copy(
                    update={
                        "status": "PENDING",
                        "progress": Progress(
                            step="queued",
                            percent=0,
                            message="Tarefa recuperada após reinício do worker",
                        ),
                        "error": None,
                        "updated_at": datetime.now(timezone.utc),
                    }
                )
                connection.execute(
                    "UPDATE tasks SET snapshot = ? WHERE task_id = ?",
                    (self._encode(reset), row["task_id"]),
                )
                connection.execute(
                    "UPDATE task_jobs SET claimed_at = NULL WHERE task_id = ?",
                    (row["task_id"],),
                )

    def claim_recoverable_jobs(self, worker_id: str) -> list[tuple[str, str, dict[str, Any]]]:
        """Reivindica jobs enfileirados de forma atômica para recuperação após restart."""
        recovered: list[tuple[str, str, dict[str, Any]]] = []
        now = datetime.now(timezone.utc).isoformat()
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                "SELECT task_id, kind, payload FROM task_jobs WHERE claimed_at IS NULL"
            ).fetchall()
            for row in rows:
                updated = connection.execute(
                    "UPDATE task_jobs SET claimed_at = ? WHERE task_id = ? AND claimed_at IS NULL",
                    (f"{now}:{worker_id}", row["task_id"]),
                )
                if updated.rowcount != 1:
                    continue
                recovered.append((row["task_id"], row["kind"], json.loads(row["payload"])))
        return recovered

settings = Settings.from_env()
configure_logging(settings.log_level)
store = TaskStore(settings.task_db_path)
agent_aggregator = AgentAggregator(settings)
agentic_orchestrator = AgenticOrchestrator(
    settings,
    memory=ProjectMemory(settings.agentic_memory_dir),
)
artistic_island = SkillGenerator(atlas_path=settings.instrument_atlas_path)


def _native_checkpoint_ready() -> bool:
    model = settings.skyreels_native_model_id
    if not model:
        return False
    path = Path(model).expanduser()
    if settings.skyreels_allow_model_download and not path.exists():
        return True
    required = ("model_index.json", "vae/config.json", "transformer/config.json")
    return path.is_dir() and all((path / relative).is_file() for relative in required)


def _native_runtime_ready() -> bool:
    if not importlib.util.find_spec("torch") or not importlib.util.find_spec("diffusers"):
        return False
    if not settings.skyreels_device.startswith("cuda"):
        return True
    try:
        torch = __import__("torch")
        return bool(torch.cuda.is_available())
    except (ImportError, AttributeError, RuntimeError):
        return False


app = FastAPI(title="KAIR-S-SONICA API", version="0.1.0", description="Gateway do Agente Káiros")
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


def _run_task(task_id: str, request: TrackRequest) -> None:
    store.update(task_id, status="RUNNING", progress=Progress(step="starting", percent=1, message="Pipeline iniciado"))
    try:
        pipeline = AudioPipeline(settings)

        def report(step: str, percent: int, message: str) -> None:
            store.update(task_id, progress=Progress(step=step, percent=percent, message=message))

        pipeline.run(request, task_id, progress=report)
        store.update(task_id, status="SUCCEEDED", progress=Progress(step="completed", percent=100, message="Artefato pronto"), artifact_url=f"/v1/audio/{task_id}")
    except Exception as exc:  # noqa: BLE001  # Convert worker failures into task snapshots.
        store.update(task_id, status="FAILED", progress=Progress(step="failed", percent=100, message="Pipeline interrompido"), error=str(exc))


def _run_multimedia_task(task_id: str, request: MultimediaRequest) -> None:
    store.update(task_id, status="RUNNING", progress=Progress(step="starting", percent=1, message="Orquestração multimídia iniciada"))
    try:
        orchestrator = MultimediaOrchestrator(settings)

        def report(step: str, percent: int, message: str) -> None:
            store.update(task_id, progress=Progress(step=step, percent=percent, message=message))

        result = orchestrator.run(request, task_id, progress=report)
        artifact_url = f"/v1/audio/{task_id}" if result.artifact_path else None
        transcript_url = f"/v1/transcript/{task_id}" if result.transcript_path else None
        metadata_url = f"/v1/metadata/{task_id}"
        public_result = {
            "artifact_url": artifact_url,
            "transcript_url": transcript_url,
            "metadata_url": metadata_url,
            "analysis": result.metadata.get("analysis"),
            "transcription": result.metadata.get("transcription"),
            "plan": result.metadata.get("plan"),
        }
        store.update(
            task_id,
            status="SUCCEEDED",
            progress=Progress(step="completed", percent=100, message="Orquestração multimídia concluída"),
            artifact_url=artifact_url,
            result=public_result,
        )
    except Exception as exc:  # noqa: BLE001  # Convert worker failures into task snapshots.
        store.update(task_id, status="FAILED", progress=Progress(step="failed", percent=100, message="Orquestração interrompida"), error=str(exc))


def _run_video_task(task_id: str, request: VideoRequest) -> None:
    store.update(task_id, status="RUNNING", progress=Progress(step="starting", percent=1, message="Geração de vídeo iniciada"))
    try:
        orchestrator = VideoOrchestrator(settings)

        def report(step: str, percent: int, message: str) -> None:
            store.update(task_id, progress=Progress(step=step, percent=percent, message=message))

        result = orchestrator.run(request, task_id, progress=report)
        video_url = f"/v1/video/{task_id}"
        metadata_url = f"/v1/metadata/{task_id}"
        public_result = {
            "video_url": video_url,
            "metadata_url": metadata_url,
            "video": result.metadata,
        }
        store.update(
            task_id,
            status="SUCCEEDED",
            progress=Progress(step="completed", percent=100, message="Vídeo pronto"),
            artifact_url=video_url,
            result=public_result,
        )
    except Exception as exc:  # noqa: BLE001  # Convert worker failures into task snapshots.
        store.update(task_id, status="FAILED", progress=Progress(step="failed", percent=100, message="Geração de vídeo interrompida"), error=str(exc))


def _launch_recovered_jobs() -> None:
    store.reset_orphaned_jobs()
    worker_id = f"api-{os.getpid()}"
    for task_id, kind, payload in store.claim_recoverable_jobs(worker_id):
        try:
            if kind == "audio":
                target = _run_task
                request = TrackRequest.model_validate(payload)
            elif kind == "multimedia":
                target = _run_multimedia_task
                request = MultimediaRequest.model_validate(payload)
            elif kind == "video":
                target = _run_video_task
                request = VideoRequest.model_validate(payload)
            else:
                raise ValueError(f"tipo de job desconhecido: {kind}")
        except Exception as exc:  # noqa: BLE001
            store.update(
                task_id,
                status="FAILED",
                progress=Progress(step="failed", percent=100, message="Payload recuperado inválido"),
                error=str(exc),
            )
            continue
        thread = threading.Thread(target=target, args=(task_id, request), daemon=True)
        thread.start()


if settings.worker_mode == "inline":
    _launch_recovered_jobs()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "kairos-sonica-api", "version": "0.1.0"}


@app.get("/ready")
def readiness() -> dict[str, Any]:
    checks: dict[str, str] = {"task_store": "ok"}
    if settings.enable_skyreels:
        repo = settings.skyreels_repo.expanduser().resolve() if settings.skyreels_repo else None
        engine = "diffusion_forcing"
        if settings.skyreels_native_api:
            native_model_ok = _native_checkpoint_ready()
            checks["skyreels_native_runtime"] = "ok" if _native_runtime_ready() else "missing"
            checks["skyreels_native_model"] = "ok" if native_model_ok else "missing"
        else:
            model = settings.skyreels_model_id
            script_ok = bool(repo and (repo / "generate_video_df.py").is_file())
            model_ok = bool(model and (Path(model).expanduser().exists() or settings.skyreels_allow_model_download))
            checks["skyreels_repo"] = "ok" if repo and repo.is_dir() else "missing"
            checks["skyreels_entrypoint"] = "ok" if script_ok else "missing"
            checks["skyreels_model"] = "ok" if model_ok else "missing"
        if not all(value == "ok" for value in checks.values()):
            raise HTTPException(status_code=503, detail={"status": "not_ready", "checks": checks, "engine": engine})
    else:
        checks["skyreels"] = "disabled"
    return {"status": "ok", "checks": checks}


@app.get("/v1/agentic/capabilities")
def agentic_capabilities() -> dict[str, Any]:
    return agentic_orchestrator.capabilities()


@app.post("/v1/agentic/run")
def agentic_run(request: AgenticRunRequest) -> dict[str, Any]:
    if not settings.agentic_core_enabled:
        raise HTTPException(status_code=503, detail="Núcleo agentico desabilitado")
    if request.submit_handoffs and not request.approve_handoffs:
        raise HTTPException(
            status_code=409,
            detail="Submissão agentica exige approve_handoffs=true",
        )
    try:
        result = agentic_orchestrator.run(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    payload = result.to_dict()
    submissions: list[dict[str, str]] = []
    if request.submit_handoffs:
        submissions = _submit_agentic_handoffs(result.handoffs)
        payload["status"] = "SUBMITTED"
    payload["submissions"] = submissions
    return payload


@app.get("/v1/artistic-island/capabilities")
def artistic_island_capabilities() -> dict[str, Any]:
    if not settings.artistic_island_enabled:
        return {
            "schema_version": 1,
            "name": "kairos-artistic-production-island",
            "enabled": False,
            "replaces_existing_core": False,
        }
    return artistic_island.capabilities()


@app.get("/v1/artistic-island/instruments")
def artistic_island_instruments() -> dict[str, Any]:
    if not settings.artistic_island_enabled:
        raise HTTPException(status_code=503, detail="Ilha Artística desabilitada")
    return {"schema_version": 1, "instruments": artistic_island.instruments()}


@app.post("/v1/artistic-island/mix-plan", response_model=MixPlan)
def artistic_island_mix_plan(request: MixPlanRequest) -> MixPlan:
    if not settings.artistic_island_enabled:
        raise HTTPException(status_code=503, detail="Ilha Artística desabilitada")
    try:
        return artistic_island.generate_chain(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/v1/agents/capabilities")
def agent_capabilities() -> dict[str, Any]:
    return agent_aggregator.catalog()


@app.get("/v1/agents/{agent_name}/probe")
def probe_agent(agent_name: str) -> dict[str, Any]:
    try:
        return agent_aggregator.probe(agent_name)
    except ExternalAgentError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def _submit_agentic_handoffs(handoffs: list[Any]) -> list[dict[str, str]]:
    submissions: list[dict[str, str]] = []
    for handoff in handoffs:
        if handoff.kind == "video_request":
            task_id = uuid4().hex
            video_request = VideoRequest.model_validate(handoff.payload["request"])
            store.create(task_id, job_kind="video", payload=video_request.model_dump(mode="json"))
            if settings.worker_mode == "inline":
                thread = threading.Thread(target=_run_video_task, args=(task_id, video_request), daemon=True)
                thread.start()
            submissions.append({"task_id": task_id, "kind": "video", "agent": handoff.to_agent})
        elif handoff.kind == "multimedia_request":
            task_id = uuid4().hex
            multimedia_request = MultimediaRequest.model_validate(handoff.payload["request"])
            store.create(task_id, job_kind="multimedia", payload=multimedia_request.model_dump(mode="json"))
            if settings.worker_mode == "inline":
                thread = threading.Thread(
                    target=_run_multimedia_task,
                    args=(task_id, multimedia_request),
                    daemon=True,
                )
                thread.start()
            submissions.append({"task_id": task_id, "kind": "multimedia", "agent": handoff.to_agent})
    return submissions


@app.get("/v1/complementary/capabilities")
def complementary_capability_catalog() -> dict[str, Any]:
    return complementary_capabilities(
        enabled=settings.complementary_core_enabled,
        media_provider_order=settings.media_provider_order,
        media_cache_dir=str(settings.media_cache_dir),
        media_cache_max_bytes=settings.media_cache_max_bytes,
    )


@app.post("/v1/complementary/plan")
def complementary_plan(request: ComplementaryPlanRequest) -> dict[str, Any]:
    """Planeja cenas e handoffs sem substituir ou iniciar os pipelines existentes."""
    if not settings.complementary_core_enabled:
        raise HTTPException(status_code=503, detail="Núcleo complementar desabilitado")
    return build_complementary_plan(**request.model_dump()).to_dict()


@app.post("/v1/complementary/media/search")
def complementary_media_search(request: ComplementaryMediaSearchRequest) -> dict[str, Any]:
    """Busca mídia somente por ação explícita; o planner nunca chama este endpoint."""
    if not settings.complementary_core_enabled:
        raise HTTPException(status_code=503, detail="Núcleo complementar desabilitado")
    chain = provider_chain_from_names(settings.media_provider_order)
    if request.kind == "video":
        assets = chain.search_videos(
            request.query,
            per_page=request.per_page,
            orientation=request.orientation,
        )
    else:
        assets = chain.search_images(request.query, per_page=request.per_page)
    downloaded: list[dict[str, str]] = []
    if request.download:
        cache = MediaCache(settings.media_cache_dir, max_bytes=settings.media_cache_max_bytes)
        for asset in assets:
            try:
                path = cache.get_or_download(asset.url)
            except MediaProviderError as exc:
                raise HTTPException(status_code=502, detail="Falha ao baixar ativo de mídia") from exc
            downloaded.append({"url_hash": cache.cache_key(asset.url), "path": str(path)})
    return {
        "query": request.query,
        "kind": request.kind,
        "provider_order": list(settings.media_provider_order),
        "assets": [asdict(asset) for asset in assets],
        "downloaded": downloaded,
    }


@app.get("/v1/persona", response_model=PersonaResponse)
def get_persona() -> PersonaResponse:
    return PersonaResponse.model_validate(DEFAULT_PERSONA.to_dict())


@app.post("/v1/plan", response_model=TrackPlan)
def create_plan(request: TrackRequest) -> TrackPlan:
    return AudioPipeline(settings).maestro.build_plan(request)


@app.post("/v1/generate", response_model=GenerateResponse, status_code=202)
def generate(request: TrackRequest) -> GenerateResponse:
    task_id = uuid4().hex
    store.create(task_id, job_kind="audio", payload=request.model_dump(mode="json"))
    if settings.worker_mode == "inline":
        thread = threading.Thread(target=_run_task, args=(task_id, request), daemon=True)
        thread.start()
    return GenerateResponse(task_id=task_id, status="PENDING")


@app.post("/v1/orchestrate", response_model=GenerateResponse, status_code=202)
def orchestrate(request: MultimediaRequest) -> GenerateResponse:
    """Executa a central multimídia sem bloquear o request HTTP."""
    task_id = uuid4().hex
    store.create(task_id, job_kind="multimedia", payload=request.model_dump(mode="json"))
    if settings.worker_mode == "inline":
        thread = threading.Thread(target=_run_multimedia_task, args=(task_id, request), daemon=True)
        thread.start()
    return GenerateResponse(task_id=task_id, status="PENDING")


@app.get("/v1/video/capabilities")
def video_capabilities() -> dict[str, Any]:
    native_configured = settings.enable_skyreels and settings.skyreels_native_api
    native_model_ready = _native_checkpoint_ready()
    native_runtime_ready = _native_runtime_ready()
    native_ready = native_configured and native_model_ready and native_runtime_ready
    return {
        "backends": {
            "cli": {"enabled": settings.enable_skyreels, "engine": ["standard", "diffusion_forcing"]},
            "native": {
                "enabled": native_configured,
                "ready": native_ready,
                "engine": ["standard", "diffusion_forcing"],
                "runtime": native_runtime_ready,
                "checkpoint": native_model_ready,
            },
        },
        "modes": ["t2v", "i2v", "extend", "start_end"],
        "default_backend": "native" if native_ready else "cli",
    }


@app.post("/v1/video/generate", response_model=GenerateResponse, status_code=202)
def generate_video(request: VideoRequest) -> GenerateResponse:
    """Enfileira T2V/I2V/DF sem bloquear o request HTTP."""
    task_id = uuid4().hex
    store.create(task_id, job_kind="video", payload=request.model_dump(mode="json"))
    if settings.worker_mode == "inline":
        thread = threading.Thread(target=_run_video_task, args=(task_id, request), daemon=True)
        thread.start()
    return GenerateResponse(task_id=task_id, status="PENDING")


@app.get("/v1/tasks/{task_id}", response_model=TaskSnapshot)
def task_status(task_id: str) -> TaskSnapshot:
    snapshot = store.get(task_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return snapshot


@app.get("/v1/audio/{task_id}")
def get_audio(task_id: str) -> FileResponse:
    snapshot = store.get(task_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    if snapshot.status != "SUCCEEDED":
        raise HTTPException(status_code=409, detail="O artefato ainda não está pronto")
    candidates = [settings.output_dir / f"{task_id}.mp3", settings.output_dir / f"{task_id}.wav"]
    artifact = next((path for path in candidates if path.is_file()), None)
    if artifact is None:
        raise HTTPException(status_code=404, detail="Artefato não encontrado")
    media_type = "audio/mpeg" if artifact.suffix == ".mp3" else "audio/wav"
    return FileResponse(artifact, media_type=media_type, filename=artifact.name)


@app.get("/v1/video/{task_id}")
def get_video(task_id: str) -> FileResponse:
    snapshot = store.get(task_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    if snapshot.status != "SUCCEEDED":
        raise HTTPException(status_code=409, detail="O vídeo ainda não está pronto")
    artifact = settings.output_dir / f"{task_id}.mp4"
    if not artifact.is_file():
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    return FileResponse(artifact, media_type="video/mp4", filename=artifact.name)


@app.get("/v1/transcript/{task_id}")
def get_transcript(task_id: str) -> FileResponse:
    snapshot = store.get(task_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    transcript = settings.output_dir / f"{task_id}.transcript.json"
    if not transcript.is_file():
        raise HTTPException(status_code=404, detail="Transcrição não encontrada")
    return FileResponse(transcript, media_type="application/json", filename=transcript.name)


@app.get("/v1/metadata/{task_id}")
def get_metadata(task_id: str) -> FileResponse:
    snapshot = store.get(task_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    metadata = settings.output_dir / f"{task_id}.metadata.json"
    if not metadata.is_file():
        raise HTTPException(status_code=404, detail="Metadados não encontrados")
    return FileResponse(metadata, media_type="application/json", filename=metadata.name)


@app.websocket("/ws/tasks/{task_id}")
async def task_events(websocket: WebSocket, task_id: str) -> None:
    await websocket.accept()
    if store.get(task_id) is None:
        await websocket.close(code=1008, reason="Tarefa não encontrada")
        return
    try:
        while True:
            snapshot = store.get(task_id)
            if snapshot is None:
                break
            await websocket.send_json(snapshot.model_dump(mode="json"))
            if snapshot.status in {"SUCCEEDED", "FAILED"}:
                break
            await asyncio.sleep(0.25)
    except WebSocketDisconnect:
        return
