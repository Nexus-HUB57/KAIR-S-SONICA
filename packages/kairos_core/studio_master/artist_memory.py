from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    context: str
    adjustments: dict[str, Any]
    project_id: str | None = None


class LocalArtistMemory:
    """Memória textual opt-in; não armazena áudio nem afirma ser um vector DB."""

    def __init__(self, path: str | Path, *, enabled: bool = False) -> None:
        self.path = Path(path)
        self.enabled = enabled

    def capabilities(self) -> dict[str, object]:
        return {
            "name": "artist-memory",
            "backend": "local-jsonl-keyword",
            "enabled": self.enabled,
            "vector_database": False,
            "stores_audio": False,
            "embedding_adapter": "optional-chroma-or-provider",
        }

    def store_feedback(
        self,
        context: str,
        adjustments: dict[str, Any],
        *,
        project_id: str | None = None,
    ) -> dict[str, object]:
        if not self.enabled:
            return {"stored": False, "reason": "artist-memory gate disabled"}
        if not context.strip():
            raise ValueError("context não pode ser vazio")
        record = {
            "context": context.strip()[:500],
            "adjustments": adjustments,
            "project_id": project_id,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        return {"stored": True, "path": str(self.path), "metadata_only": True}

    def recall_similar(self, context: str, *, limit: int = 1) -> dict[str, Any]:
        if not self.enabled or not self.path.exists() or limit < 1:
            return {}
        query = self._tokens(context)
        if not query:
            return {}
        scored: list[tuple[int, int, dict[str, Any]]] = []
        for index, line in enumerate(self.path.read_text(encoding="utf-8").splitlines()):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            overlap = len(query & self._tokens(str(record.get("context", ""))))
            if overlap:
                scored.append((overlap, -index, record))
        if not scored:
            return {}
        scored.sort(reverse=True, key=lambda item: (item[0], item[1]))
        return dict(scored[0][2].get("adjustments") or {})

    @staticmethod
    def _tokens(value: str) -> set[str]:
        return {token for token in re.findall(r"[\wÀ-ÿ]+", value.lower()) if len(token) > 2}
