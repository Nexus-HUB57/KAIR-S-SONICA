from __future__ import annotations

import json
import mimetypes
import os
import time
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from kairos_core.config import Settings


class ExternalAgentError(RuntimeError):
    """Erro normalizado para integrações externas do agregador."""


class ExternalAgentClient:
    def __init__(self, base_url: str, *, timeout_seconds: int) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
        body: bytes | None = None,
        content_type: str | None = None,
        timeout_seconds: int | None = None,
    ) -> tuple[int, bytes, dict[str, str]]:
        target = f"{self.base_url}/{path.lstrip('/')}"
        request_headers = {"Accept": "application/json", **(headers or {})}
        if content_type:
            request_headers["Content-Type"] = content_type
        if body is None and payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            request_headers.setdefault("Content-Type", "application/json")
        request = Request(target, data=body, headers=request_headers, method=method)
        try:
            with urlopen(request, timeout=timeout_seconds or self.timeout_seconds) as response:
                return response.status, response.read(), dict(response.headers.items())
        except HTTPError as exc:
            exc.close()
            raise ExternalAgentError(f"{method} {path} retornou HTTP {exc.code}") from exc
        except (OSError, URLError, TimeoutError) as exc:
            raise ExternalAgentError(f"Falha de comunicação com {target}: {exc}") from exc

    @staticmethod
    def _json(body: bytes) -> Any:
        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ExternalAgentError("Resposta externa não é JSON válido") from exc


class SkyReelsSpaceClient(ExternalAgentClient):
    """Cliente para o Space Gradio documentado em `agents.md`."""

    def __init__(self, settings: Settings) -> None:
        super().__init__(
            settings.skyreels_space_base_url,
            timeout_seconds=settings.skyreels_space_timeout_seconds,
        )
        self.settings = settings
        self.endpoint = settings.skyreels_space_endpoint

    def info(self) -> dict[str, Any]:
        _, body, _ = self._request("GET", "/gradio_api/info")
        payload = self._json(body)
        return payload if isinstance(payload, dict) else {"raw": payload}

    def config(self) -> dict[str, Any]:
        _, body, _ = self._request("GET", "/config")
        payload = self._json(body)
        return payload if isinstance(payload, dict) else {"raw": payload}

    def upload(self, path: str | Path) -> dict[str, Any]:
        file_path = Path(path).expanduser().resolve()
        if not file_path.is_file():
            raise ExternalAgentError(f"Arquivo de referência não encontrado: {file_path}")
        boundary = f"----kair-{uuid.uuid4().hex}"
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        data = file_path.read_bytes()
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="files"; filename="{file_path.name}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode() + data + f"\r\n--{boundary}--\r\n".encode()
        _, response_body, _ = self._request(
            "POST",
            "/gradio_api/upload",
            body=body,
            content_type=f"multipart/form-data; boundary={boundary}",
        )
        payload = self._json(response_body)
        return self._normalize_file_data(payload)

    @staticmethod
    def _normalize_file_data(payload: Any) -> dict[str, Any]:
        if isinstance(payload, list) and payload:
            payload = payload[0]
        if isinstance(payload, str):
            return {"path": payload, "meta": {"_type": "gradio.FileData"}}
        if isinstance(payload, dict) and "files" in payload and isinstance(payload["files"], list):
            return SkyReelsSpaceClient._normalize_file_data(payload["files"])
        if isinstance(payload, dict) and "path" in payload:
            normalized = dict(payload)
            normalized.setdefault("meta", {"_type": "gradio.FileData"})
            return normalized
        raise ExternalAgentError("Upload do Space não retornou um FileData reconhecível")

    def generate(
        self,
        *,
        prompt: str,
        model_id: str = "Skywork/SkyReels-V2-DF-1.3B-540P",
        resolution: str = "540P",
        num_frames: int = 97,
        ar_step: int = 0,
        causal_attention: bool = False,
        causal_block_size: int = 1,
        base_num_frames: int = 97,
        overlap_history: int | None = None,
        addnoise_condition: int = 0,
        guidance_scale: float = 6.0,
        shift: float = 8.0,
        inference_steps: int = 30,
        use_usp: bool = False,
        offload: bool = True,
        fps: int = 24,
        seed: int | None = None,
        prompt_enhancer: bool = False,
        use_teacache: bool = True,
        teacache_thresh: float = 0.2,
        use_ret_steps: bool = True,
        input_image: str | Path | None = None,
        video_length_target: str = "4",
        poll_seconds: float = 3.0,
    ) -> dict[str, Any]:
        inputs: list[Any] = [
            prompt,
            None,
            video_length_target,
            model_id,
            resolution,
            num_frames,
            ar_step,
            causal_attention,
            causal_block_size,
            base_num_frames,
            overlap_history,
            addnoise_condition,
            guidance_scale,
            shift,
            inference_steps,
            use_usp,
            offload,
            fps,
            seed,
            prompt_enhancer,
            use_teacache,
            teacache_thresh,
            use_ret_steps,
        ]
        if input_image is not None:
            inputs[1] = self.upload(input_image)
        response = self._submit(inputs)
        event_id = response.get("event_id") or response.get("id")
        if not event_id:
            raise ExternalAgentError("Space não retornou event_id para a geração")
        return self.poll(str(event_id), poll_seconds=poll_seconds)

    def _submit(self, inputs: list[Any]) -> dict[str, Any]:
        payload = {"data": inputs}
        errors: list[str] = []
        for path in (
            f"/gradio_api/call/v2/{self.endpoint}",
            f"/gradio_api/call/{self.endpoint}",
        ):
            try:
                _, body, _ = self._request("POST", path, payload=payload)
                response = self._json(body)
                if isinstance(response, dict):
                    return response
                return {"data": response}
            except ExternalAgentError as exc:
                errors.append(str(exc))
        raise ExternalAgentError("Não foi possível iniciar o endpoint do Space: " + " | ".join(errors))

    def poll(self, event_id: str, *, poll_seconds: float = 3.0) -> dict[str, Any]:
        deadline = time.monotonic() + self.timeout_seconds
        path = f"/gradio_api/call/{self.endpoint}/{event_id}"
        while time.monotonic() < deadline:
            _, body, headers = self._request("GET", path, timeout_seconds=min(30, self.timeout_seconds))
            parsed = self._parse_event_stream(body, headers)
            status = str(parsed.get("status", "")).lower()
            if status in {"complete", "completed", "success", "succeeded"}:
                return parsed
            if status in {"error", "failed", "failure"}:
                raise ExternalAgentError(f"SkyReels Space reportou falha: {parsed}")
            time.sleep(max(0.1, poll_seconds))
        raise ExternalAgentError(f"SkyReels Space excedeu timeout de {self.timeout_seconds}s")

    @staticmethod
    def _parse_event_stream(body: bytes, headers: Mapping[str, str]) -> dict[str, Any]:
        text = body.decode("utf-8", errors="replace")
        content_type = next(
            (value for key, value in headers.items() if key.lower() == "content-type"),
            "",
        ).lower()
        if "text/event-stream" not in content_type:
            payload = json.loads(text)
            return payload if isinstance(payload, dict) else {"data": payload}
        last: dict[str, Any] = {"status": "running"}
        for line in text.splitlines():
            if not line.startswith("data:"):
                continue
            raw = line.partition(":")[2].strip()
            if raw in {"", "[DONE]"}:
                continue
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if not isinstance(parsed, dict):
                continue
            last = {**last, **parsed}
            message = parsed.get("msg")
            if message == "process_completed" and parsed.get("success", True):
                last["status"] = "completed"
                output = parsed.get("output")
                if isinstance(output, dict) and "data" in output:
                    last["data"] = output["data"]
            elif message in {"process_error", "close_stream"} or parsed.get("success") is False:
                last["status"] = "failed"
        return last


class LlamaGenClient(ExternalAgentClient):
    """Cliente REST mínimo para o Comic API do LlamaGen."""

    def __init__(self, settings: Settings) -> None:
        super().__init__(settings.llamagen_base_url, timeout_seconds=settings.llamagen_timeout_seconds)
        self.settings = settings

    def _auth_headers(self) -> dict[str, str]:
        token = os.getenv(self.settings.llamagen_api_key_env)
        if not token:
            raise ExternalAgentError(
                f"Variável {self.settings.llamagen_api_key_env} não está disponível; "
                "a chave não é armazenada no repositório"
            )
        return {"Authorization": f"Bearer {token}"}

    def health(self) -> dict[str, Any]:
        path = "/v1/comics/generations/nonexistent"
        try:
            status, body, _ = self._request("GET", path, headers=self._auth_headers())
        except ExternalAgentError as exc:
            message = str(exc)
            if "HTTP 401" in message or "HTTP 403" in message:
                return {"status": "unauthorized", "reachable": True, "detail": message}
            if "HTTP 404" in message:
                return {"status": "reachable", "reachable": True, "detail": message}
            return {"status": "unreachable", "reachable": False, "detail": message}
        return {"status": "reachable", "reachable": True, "http_status": status, "body": self._json(body)}

    def upload_reference(self, path: str | Path) -> dict[str, Any]:
        file_path = Path(path).expanduser().resolve()
        if not file_path.is_file():
            raise ExternalAgentError(f"Arquivo de referência não encontrado: {file_path}")
        boundary = f"----kair-{uuid.uuid4().hex}"
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode() + file_path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
        _, response_body, _ = self._request(
            "POST",
            "/v1/comics/upload",
            headers=self._auth_headers(),
            body=body,
            content_type=f"multipart/form-data; boundary={boundary}",
        )
        payload = self._json(response_body)
        return payload if isinstance(payload, dict) else {"raw": payload}

    def create_generation(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        _, body, _ = self._request(
            "POST",
            "/v1/comics/generations",
            headers=self._auth_headers(),
            payload=dict(payload),
        )
        response = self._json(body)
        return response if isinstance(response, dict) else {"raw": response}

    def get_status(self, generation_id: str, *, page: int | None = None, panel: int | None = None) -> dict[str, Any]:
        query = ""
        if page is not None:
            params = {"page": page}
            if panel is not None:
                params["panel"] = panel
            query = "?" + urlencode(params)
        _, body, _ = self._request(
            "GET",
            f"/v1/comics/generations/{generation_id}{query}",
            headers=self._auth_headers(),
        )
        response = self._json(body)
        return response if isinstance(response, dict) else {"raw": response}

    def update_generation(self, generation_id: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        _, body, _ = self._request(
            "PATCH",
            f"/v1/comics/generations/{generation_id}",
            headers=self._auth_headers(),
            payload=dict(payload),
        )
        response = self._json(body)
        return response if isinstance(response, dict) else {"raw": response}
