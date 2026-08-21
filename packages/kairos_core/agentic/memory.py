from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

_TOKEN_RE = re.compile(r"[\wÀ-ÿ]{3,}", re.UNICODE)


class ProjectMemory:
    """Memória local de projeto; deliberadamente simples e substituível por um backend vetorial."""

    def __init__(self, root: str | Path = "data/agentic-memory", namespace: str = "default") -> None:
        safe_namespace = re.sub(r"[^a-zA-Z0-9_.-]", "_", namespace).strip(".") or "default"
        self.path = Path(root) / f"{safe_namespace}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def append(self, *, run_id: str, role: str, kind: str, content: Any) -> dict[str, Any]:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "run_id": run_id,
            "role": role,
            "kind": kind,
            "content": content,
        }
        with self._lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry

    def recent(self, limit: int = 10) -> list[dict[str, Any]]:
        if not self.path.is_file():
            return []
        with self._lock, self.path.open(encoding="utf-8") as handle:
            entries = [json.loads(line) for line in handle if line.strip()]
        return entries[-max(1, limit) :]

    def search(self, query: str, *, limit: int = 5) -> list[dict[str, Any]]:
        query_tokens = set(_TOKEN_RE.findall(query.lower()))
        if not query_tokens or not self.path.is_file():
            return []
        scored: list[tuple[int, dict[str, Any]]] = []
        with self._lock, self.path.open(encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                entry = json.loads(line)
                haystack = json.dumps(entry.get("content", ""), ensure_ascii=False).lower()
                score = sum(token in haystack for token in query_tokens)
                if score:
                    scored.append((score, entry))
        scored.sort(key=lambda item: (item[0], item[1].get("timestamp", "")), reverse=True)
        return [entry for _, entry in scored[: max(1, limit)]]
