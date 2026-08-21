from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from kairos_core.studio_master.contracts import PerformanceCommand, PerformanceState


class PerformanceController:
    """Estado efêmero de performance; não grava áudio nem muta o cânone automaticamente."""

    def __init__(self) -> None:
        self._states: dict[str, PerformanceState] = {}
        self._lock = threading.Lock()

    def get(self, session_id: str, *, bpm: float = 140, swing_ratio: float = 0.60) -> PerformanceState:
        with self._lock:
            return self._states.setdefault(
                session_id,
                self._new_state(session_id, bpm=bpm, swing_ratio=swing_ratio),
            ).model_copy(deep=True)

    def apply(self, session_id: str, command: PerformanceCommand) -> PerformanceState:
        with self._lock:
            current = self._states.setdefault(session_id, self._new_state(session_id))
            updates: dict[str, Any] = {
                "last_action": command.action,
                "status": "ACTIVE",
                "proposal": None,
                "warnings": [],
            }
            if command.action == "SET_SWING":
                ratio = _coerce_swing(command.value)
                updates.update({"swing_ratio": ratio, "swing_ms": _swing_ms(current.bpm, ratio)})
            elif command.action == "SET_GRID_FOLLOW":
                updates["grid_follow"] = _coerce_bool(command.value)
            elif command.action == "SET_BPM":
                bpm = _coerce_bpm(command.bpm if command.bpm is not None else command.value)
                updates.update({"bpm": bpm, "swing_ms": _swing_ms(bpm, current.swing_ratio)})
            elif command.action == "BOOST_PUNCHLINE":
                enabled = True if command.value is None else _coerce_bool(command.value)
                updates.update(
                    {
                        "punchline_boost_db": 3.0 if enabled else 0.0,
                        "reverb_reduction_db": 3.0 if enabled else 0.0,
                    }
                )
            elif command.action == "PUSH_TO_LIBRARY":
                proposal_id = f"manual-{uuid4().hex}"
                updates.update(
                    {
                        "status": "PENDING_APPROVAL",
                        "proposal": {
                            "proposal_id": proposal_id,
                            "reference_id": command.reference_id,
                            "created_at": datetime.now(timezone.utc).isoformat(),
                            "kind": "manual-groove-override",
                            "metadata_only": True,
                            "approval_required": True,
                            "snapshot": {
                                "bpm": current.bpm,
                                "swing_ratio": current.swing_ratio,
                                "swing_ms": current.swing_ms,
                                "grid_follow": current.grid_follow,
                            },
                        },
                        "warnings": [
                            "Proposta criada; nenhuma gravação, MIDI ou amostra foi persistida.",
                            "Aprovação editorial e verificação de licença são obrigatórias antes de publicar no cânone.",
                        ],
                    }
                )
            elif command.action == "RESET":
                updates = {
                    "bpm": 140.0,
                    "swing_ratio": 0.60,
                    "swing_ms": _swing_ms(140.0, 0.60),
                    "grid_follow": True,
                    "punchline_boost_db": 0.0,
                    "reverb_reduction_db": 0.0,
                    "last_action": "RESET",
                    "status": "ACTIVE",
                    "proposal": None,
                    "warnings": [],
                }
            updated = current.model_copy(update=updates)
            self._states[session_id] = updated
            return updated.model_copy(deep=True)

    @staticmethod
    def _new_state(session_id: str, *, bpm: float = 140, swing_ratio: float = 0.60) -> PerformanceState:
        return PerformanceState(
            session_id=session_id,
            bpm=bpm,
            swing_ratio=swing_ratio,
            swing_ms=_swing_ms(bpm, swing_ratio),
            grid_follow=True,
            punchline_boost_db=0.0,
            reverb_reduction_db=0.0,
            last_action="INIT",
        )


def _swing_ms(bpm: float, swing_ratio: float) -> float:
    return round((swing_ratio - 0.5) * (60_000 / bpm), 6)


def _coerce_swing(value: float | bool | str | None) -> float:
    if isinstance(value, bool) or value is None:
        raise ValueError("SET_SWING exige um valor entre 0.50 e 0.67 ou 50% e 67%")
    try:
        numeric = float(str(value).strip().replace("%", ""))
    except ValueError as exc:
        raise ValueError("SET_SWING recebeu valor inválido") from exc
    if numeric > 1:
        numeric /= 100
    if not 0.50 <= numeric <= 0.67:
        raise ValueError("SET_SWING deve permanecer entre 0.50 e 0.67")
    return round(numeric, 6)


def _coerce_bool(value: float | bool | str | None) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.strip().lower() in {"1", "true", "yes", "on"}:
        return True
    if isinstance(value, str) and value.strip().lower() in {"0", "false", "no", "off"}:
        return False
    if isinstance(value, (int, float)) and value in {0, 1}:
        return bool(value)
    raise ValueError("O comando exige um booleano")


def _coerce_bpm(value: float | bool | str | None) -> float:
    if isinstance(value, bool) or value is None:
        raise ValueError("SET_BPM exige bpm entre 40 e 240")
    try:
        bpm = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("SET_BPM recebeu bpm inválido") from exc
    if not 40 <= bpm <= 240:
        raise ValueError("SET_BPM deve permanecer entre 40 e 240")
    return round(bpm, 4)
