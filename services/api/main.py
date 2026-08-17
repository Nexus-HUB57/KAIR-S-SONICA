from __future__ import annotations

import asyncio
import threading
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from kairos_core.audio.pipeline import AudioPipeline
from kairos_core.config import Settings
from kairos_core.persona import DEFAULT_PERSONA
from kairos_core.schemas import (
    GenerateResponse,
    PersonaResponse,
    Progress,
    TaskSnapshot,
    TrackPlan,
    TrackRequest,
)


class TaskStore:
    def __init__(self) -> None:
        self._items: dict[str, TaskSnapshot] = {}
        self._lock = threading.Lock()

    def create(self, task_id: str) -> TaskSnapshot:
        snapshot = TaskSnapshot(task_id=task_id, status="PENDING", progress=Progress(step="queued", percent=0, message="Tarefa enfileirada"))
        with self._lock:
            self._items[task_id] = snapshot
        return snapshot

    def get(self, task_id: str) -> TaskSnapshot | None:
        with self._lock:
            return self._items.get(task_id)

    def update(self, task_id: str, **changes: Any) -> TaskSnapshot:
        with self._lock:
            current = self._items[task_id]
            updated = current.model_copy(update={**changes, "updated_at": datetime.now(timezone.utc)})
            self._items[task_id] = updated
            return updated


settings = Settings.from_env()
store = TaskStore()
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
