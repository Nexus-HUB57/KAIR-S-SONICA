from __future__ import annotations

from collections.abc import Callable
from typing import Any

from kairos_core.social.contracts import PeerHandoff


PeerCallable = Callable[[PeerHandoff, dict[str, Any]], dict[str, Any]]


class PeerCoordinator:
    """Registro local de peers; a integração externa é injetada e nunca implícita."""

    def __init__(self, peers: dict[str, PeerCallable] | None = None) -> None:
        self._peers = dict(peers or {})

    def register(self, role: str, callback: PeerCallable) -> None:
        self._peers[role] = callback

    def available(self) -> list[str]:
        return sorted(self._peers)

    def delegate(self, handoff: PeerHandoff, *, context: dict[str, Any]) -> PeerHandoff:
        callback = self._peers.get(handoff.peer_role)
        if callback is None:
            return handoff.model_copy(update={"status": "planned"})
        result = callback(handoff, context)
        confidence = result.get("confidence")
        return handoff.model_copy(
            update={
                "result": result,
                "confidence": float(confidence) if confidence is not None else None,
                "status": "completed",
            }
        )

    @staticmethod
    def reconcile(handoffs: list[PeerHandoff]) -> dict[str, Any]:
        completed = [item for item in handoffs if item.status == "completed" and item.result]
        completed.sort(key=lambda item: item.confidence or 0.0, reverse=True)
        return {
            "status": "completed" if completed else "pending",
            "selected_peer": completed[0].peer_role if completed else None,
            "completed_count": len(completed),
            "results": [item.result for item in completed],
        }
