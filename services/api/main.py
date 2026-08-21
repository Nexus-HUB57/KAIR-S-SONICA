from __future__ import annotations

import asyncio
import json
import sqlite3
import threading
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from kairos_core.audio.orchestrator import MultimediaOrchestrator
from kairos_core.audio.pipeline import AudioPipeline
from kairos_core.config import Settings
from kairos_core.persona import DEFAULT_PERSONA
from kairos_core.schemas import (
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

    def create(self, task_id: str) -> TaskSnapshot:
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
        return updated

settings = Settings.from_env()
store = TaskStore(settings.task_db_path)
app = FastAPI(title="KAIR-S-SONICA API", version="0.1.0", description="Gateway do Agente Káiros")


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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "kairos-sonica-api", "version": "0.1.0"}


@app.get("/v1/persona", response_model=PersonaResponse)
def get_persona() -> PersonaResponse:
    return PersonaResponse.model_validate(DEFAULT_PERSONA.to_dict())


@app.post("/v1/plan", response_model=TrackPlan)
def create_plan(request: TrackRequest) -> TrackPlan:
    return AudioPipeline(settings).maestro.build_plan(request)


@app.post("/v1/generate", response_model=GenerateResponse, status_code=202)
def generate(request: TrackRequest) -> GenerateResponse:
    task_id = uuid4().hex
    store.create(task_id)
    thread = threading.Thread(target=_run_task, args=(task_id, request), daemon=True)
    thread.start()
    return GenerateResponse(task_id=task_id, status="PENDING")


@app.post("/v1/orchestrate", response_model=GenerateResponse, status_code=202)
def orchestrate(request: MultimediaRequest) -> GenerateResponse:
    """Executa a central multimídia sem bloquear o request HTTP."""
    task_id = uuid4().hex
    store.create(task_id)
    thread = threading.Thread(target=_run_multimedia_task, args=(task_id, request), daemon=True)
    thread.start()
    return GenerateResponse(task_id=task_id, status="PENDING")


@app.post("/v1/video/generate", response_model=GenerateResponse, status_code=202)
def generate_video(request: VideoRequest) -> GenerateResponse:
    """Enfileira T2V/I2V/DF sem bloquear o request HTTP."""
    task_id = uuid4().hex
    store.create(task_id)
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
