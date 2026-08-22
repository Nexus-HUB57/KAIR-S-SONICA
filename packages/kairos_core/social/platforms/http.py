from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from kairos_core.social.platforms.base import PlatformError


def request_json(
    method: str,
    url: str,
    *,
    token: str,
    body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    request_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        **(headers or {}),
    }
    request = urllib.request.Request(
        url,
        method=method,
        headers=request_headers,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return payload if isinstance(payload, dict) else {"data": payload}
    except urllib.error.HTTPError as exc:
        retryable = exc.code == 429 or exc.code >= 500
        raise PlatformError(
            f"provedor retornou HTTP {exc.code}",
            code=f"http_{exc.code}",
            retryable=retryable,
        ) from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise PlatformError(
            f"falha de transporte: {type(exc).__name__}",
            code="transport_error",
            retryable=True,
        ) from exc


def build_url(base: str, path: str, params: dict[str, Any] | None = None) -> str:
    url = f"{base.rstrip('/')}/{path.lstrip('/')}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    return url
