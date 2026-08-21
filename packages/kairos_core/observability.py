from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, TextIO

_RESERVED_FIELDS = {"args", "asctime", "created", "exc_info", "exc_text", "filename", "funcName", "levelname", "levelno", "lineno", "module", "msecs", "message", "msg", "name", "pathname", "process", "processName", "relativeCreated", "stack_info", "thread", "threadName"}


class JsonFormatter(logging.Formatter):
    """Formatter estruturado sem incluir segredos ou cabeçalhos de autenticação."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key.startswith("_") or key in _RESERVED_FIELDS:
                continue
            if key.lower() in {"authorization", "api_key", "token", "secret", "password"}:
                continue
            try:
                json.dumps(value)
            except (TypeError, ValueError):
                value = repr(value)
            payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def configure_logging(level: str = "INFO", *, stream: TextIO | None = None) -> None:
    """Configura um handler JSON no root logger sem duplicar handlers existentes."""
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    for handler in root.handlers:
        if getattr(handler, "_kairos_json", False):
            handler.setLevel(root.level)
            return
    handler = logging.StreamHandler(stream or sys.stderr)
    handler.setLevel(root.level)
    handler.setFormatter(JsonFormatter())
    handler._kairos_json = True  # type: ignore[attr-defined]
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def log_event(logger: logging.Logger, level: int, event: str, **fields: Any) -> None:
    safe_fields = {
        key: value
        for key, value in fields.items()
        if key.lower() not in {"authorization", "api_key", "token", "secret", "password"}
    }
    logger.log(level, event, extra={"event": event, **safe_fields})
