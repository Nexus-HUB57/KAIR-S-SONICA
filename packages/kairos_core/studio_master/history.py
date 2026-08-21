from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ProductionHistoryStore:
    """Histórico JSON local para métricas; apenas registros explicitamente aprovados."""

    def __init__(self, path: str | Path, *, max_records: int = 10_000) -> None:
        self.path = Path(path)
        self.max_records = max_records

    def append(self, record: dict[str, Any], *, approved: bool) -> dict[str, object]:
        if not approved:
            raise PermissionError("registro requer aprovação explícita")
        existing = self._read()
        payload = {
            **record,
            "timestamp": record.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        }
        existing.append(payload)
        existing = existing[-self.max_records :]
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=f".{self.path.name}.", suffix=".tmp", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(existing, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
            os.replace(temporary, self.path)
        except Exception:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise
        return {"stored": True, "records": len(existing), "path": str(self.path)}

    def _read(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"histórico inválido: {exc}") from exc
        if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
            raise ValueError("histórico deve ser uma lista de objetos")
        return payload
