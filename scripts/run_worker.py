#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import signal
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
for import_root in (ROOT, ROOT / "packages"):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from kairos_core.config import Settings
from kairos_core.schemas import MultimediaRequest, Progress, TrackRequest, VideoRequest

from services.api.main import (
    TaskStore,
    _run_multimedia_task,
    _run_task,
    _run_video_task,
)

RUNNERS: dict[str, tuple[type[Any], Callable[[str, Any], None]]] = {

    "audio": (TrackRequest, _run_task),
    "multimedia": (MultimediaRequest, _run_multimedia_task),
    "video": (VideoRequest, _run_video_task),
}


class Worker:
    def __init__(self, store: TaskStore, poll_seconds: float) -> None:
        self.store = store
        self.poll_seconds = max(0.1, poll_seconds)
        self.running = True
        self.worker_id = f"worker-{os.getpid()}"

    def stop(self, *_: object) -> None:
        self.running = False

    def dispatch(self, task_id: str, kind: str, payload: dict[str, Any]) -> None:
        runner_spec = RUNNERS.get(kind)
        if runner_spec is None:
            self.store.update(
                task_id,
                status="FAILED",
                progress=Progress(step="failed", percent=100, message="Tipo de job desconhecido"),
                error=f"tipo de job desconhecido: {kind}",
            )
            return
        request_type, runner = runner_spec
        try:
            request = request_type.model_validate(payload)
        except Exception as exc:  # noqa: BLE001
            self.store.update(
                task_id,
                status="FAILED",
                progress=Progress(step="failed", percent=100, message="Payload inválido"),
                error=str(exc),
            )
            return
        runner(task_id, request)

    def run(self, once: bool = False) -> None:
        self.store.reset_orphaned_jobs()
        while self.running:
            jobs = self.store.claim_recoverable_jobs(self.worker_id)
            for task_id, kind, payload in jobs:
                self.dispatch(task_id, kind, payload)
            if once:
                return
            if not jobs:
                time.sleep(self.poll_seconds)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Worker persistente do KAIR-S-SONICA")
    parser.add_argument("--poll-seconds", type=float, default=2.0)
    parser.add_argument("--once", action="store_true", help="Processa o lote atual e encerra")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = Settings.from_env()
    worker = Worker(TaskStore(settings.task_db_path), args.poll_seconds)
    signal.signal(signal.SIGTERM, worker.stop)
    signal.signal(signal.SIGINT, worker.stop)
    worker.run(once=args.once)


if __name__ == "__main__":
    main()
