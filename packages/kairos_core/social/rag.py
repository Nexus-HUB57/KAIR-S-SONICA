from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

_TOKEN_RE = re.compile(r"[\wÀ-ÿ]{3,}", re.UNICODE)


@dataclass(frozen=True, slots=True)
class RagDocument:
    source_id: str
    text: str
    locator: str
    title: str | None = None
    version: str | None = None
    provenance: str = "repo"
    metadata: dict[str, Any] | None = None

    def searchable(self) -> str:
        return " ".join(
            value
            for value in (
                self.source_id,
                self.text,
                self.locator,
                self.title or "",
                json.dumps(self.metadata or {}, ensure_ascii=False),
            )
            if value
        ).lower()


class SocialRagIndex:
    """Índice local determinístico; embeddings são uma extensão opcional, não uma dependência."""

    def __init__(self, documents: Iterable[RagDocument] | None = None) -> None:
        self._documents: list[RagDocument] = list(documents or [])

    @property
    def documents(self) -> tuple[RagDocument, ...]:
        return tuple(self._documents)

    def add(self, document: RagDocument) -> None:
        self._documents.append(document)

    def add_path(self, path: str | Path, *, source_id: str | None = None, provenance: str = "repo") -> None:
        file_path = Path(path)
        if not file_path.is_file():
            return
        text = file_path.read_text(encoding="utf-8", errors="replace")
        self.add(
            RagDocument(
                source_id=source_id or file_path.stem,
                text=text,
                locator=str(file_path),
                title=file_path.name,
                version=None,
                provenance=provenance,
            )
        )

    def add_jsonl(self, path: str | Path, *, provenance: str = "repo") -> None:
        file_path = Path(path)
        if not file_path.is_file():
            return
        for line in file_path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            self.add(
                RagDocument(
                    source_id=str(payload.get("source_id") or payload.get("run_id") or file_path.stem),
                    text=json.dumps(payload.get("content", payload), ensure_ascii=False),
                    locator=str(file_path),
                    title=str(payload.get("kind") or file_path.name),
                    version=str(payload.get("timestamp") or "") or None,
                    provenance=provenance,
                    metadata={"role": payload.get("role"), "kind": payload.get("kind")},
                )
            )

    def search(self, query: str, *, limit: int = 8, provenance: str | None = None) -> list[dict[str, Any]]:
        query_tokens = set(_TOKEN_RE.findall(query.lower()))
        if not query_tokens:
            return []
        scored: list[tuple[float, RagDocument]] = []
        for document in self._documents:
            if provenance and document.provenance != provenance:
                continue
            haystack = document.searchable()
            hits = sum(token in haystack for token in query_tokens)
            if not hits:
                continue
            coverage = hits / len(query_tokens)
            score = hits + coverage
            scored.append((score, document))
        scored.sort(key=lambda item: (item[0], item[1].source_id), reverse=True)
        retrieved_at = datetime.now(timezone.utc).isoformat()
        return [
            {
                "source_id": document.source_id,
                "locator": document.locator,
                "title": document.title,
                "version": document.version,
                "provenance": document.provenance,
                "score": round(score, 4),
                "retrieved_at": retrieved_at,
                "text_excerpt": document.text[:1_200],
                "metadata": document.metadata or {},
            }
            for score, document in scored[: max(1, limit)]
        ]

    @classmethod
    def from_repo(cls, repo_root: str | Path) -> "SocialRagIndex":
        root = Path(repo_root)
        index = cls()
        known_files = (
            root / "docs/ktd-visual-bible.md",
            root / "docs/ktd-physical-spec.md",
            root / "docs/singles/single-11-i-wont-waste-this-life-campaign-model-a-b-v1.md",
            root / "docs/singles/single-11-i-wont-waste-this-life-tiktok-instagram-launch-adaptation-v1.md",
            root / "docs/singles/single-11-i-wont-waste-this-life-youtube-community-shorts-playbook-v1.md",
            root / "docs/social/ktd-social-orchestrator-architecture-v1.md",
        )
        for path in known_files:
            index.add_path(path)
        memory_root = root / "data/agentic-memory"
        if memory_root.is_dir():
            for path in sorted(memory_root.glob("*.jsonl")):
                index.add_jsonl(path)
        return index
