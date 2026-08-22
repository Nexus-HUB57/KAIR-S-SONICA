from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Callable
from uuid import uuid4

from kairos_core.social.contracts import SocialRunRequest, SocialRunResult


class SocialScheduleStore:
    """Agenda persistente mínima para jobs sociais; o host deve executar o dispatcher periodicamente."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        with self._connect() as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS social_schedules ("
                "schedule_id TEXT PRIMARY KEY, run_at TEXT NOT NULL, request_json TEXT NOT NULL, "
                "status TEXT NOT NULL, created_at TEXT NOT NULL, claimed_at TEXT"
                ")"
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path, timeout=30)
        connection.row_factory = sqlite3.Row
        return connection

    def create(self, request: SocialRunRequest, *, schedule_id: str | None = None) -> dict[str, Any]:
        if request.schedule_at is None:
            raise ValueError("schedule_at é obrigatório para criar uma agenda")
        schedule_id = schedule_id or uuid4().hex
        created_at = datetime.now(timezone.utc).isoformat()
        with self._lock, self._connect() as connection:
            connection.execute(
                "INSERT INTO social_schedules(schedule_id, run_at, request_json, status, created_at, claimed_at) "
                "VALUES (?, ?, ?, 'SCHEDULED', ?, NULL)",
                (
                    schedule_id,
                    request.schedule_at.astimezone(timezone.utc).isoformat(),
                    json.dumps(request.model_dump(mode="json"), ensure_ascii=False),
                    created_at,
                ),
            )
        return self.get(schedule_id)  # type: ignore[return-value]

    def get(self, schedule_id: str) -> dict[str, Any] | None:
        with self._lock, self._connect() as connection:
            row = connection.execute(
                "SELECT schedule_id, run_at, request_json, status, created_at, claimed_at "
                "FROM social_schedules WHERE schedule_id = ?",
                (schedule_id,),
            ).fetchone()
        if row is None:
            return None
        payload = dict(row)
        payload["request"] = json.loads(payload.pop("request_json"))
        return payload

    def list(self, *, status: str | None = None) -> list[dict[str, Any]]:
        query = "SELECT schedule_id FROM social_schedules"
        params: tuple[Any, ...] = ()
        if status:
            query += " WHERE status = ?"
            params = (status,)
        query += " ORDER BY run_at ASC"
        with self._lock, self._connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [self.get(str(row["schedule_id"])) for row in rows if self.get(str(row["schedule_id"]))]

    def claim_due(self, *, now: datetime | None = None, limit: int = 10) -> list[SocialRunRequest]:
        current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
        claimed_at = datetime.now(timezone.utc).isoformat()
        requests: list[SocialRunRequest] = []
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                "SELECT schedule_id, request_json FROM social_schedules "
                "WHERE status = 'SCHEDULED' AND run_at <= ? AND claimed_at IS NULL "
                "ORDER BY run_at ASC LIMIT ?",
                (current, limit),
            ).fetchall()
            for row in rows:
                changed = connection.execute(
                    "UPDATE social_schedules SET status = 'CLAIMED', claimed_at = ? "
                    "WHERE schedule_id = ? AND status = 'SCHEDULED' AND claimed_at IS NULL",
                    (claimed_at, row["schedule_id"]),
                )
                if changed.rowcount != 1:
                    continue
                requests.append(SocialRunRequest.model_validate(json.loads(row["request_json"])))
        return requests

    def mark(self, schedule_id: str, *, status: str) -> None:
        with self._lock, self._connect() as connection:
            connection.execute(
                "UPDATE social_schedules SET status = ? WHERE schedule_id = ?",
                (status, schedule_id),
            )

    def dispatch_due(
        self,
        runner: Callable[[SocialRunRequest], SocialRunResult],
        *,
        now: datetime | None = None,
        limit: int = 10,
    ) -> list[SocialRunResult]:
        results: list[SocialRunResult] = []
        for request in self.claim_due(now=now, limit=limit):
            try:
                result = runner(request)
                results.append(result)
            except Exception:
                # O job já foi reivindicado; o host pode implementar retry/backoff externo.
                continue
        return results
