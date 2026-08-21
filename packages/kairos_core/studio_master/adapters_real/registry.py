from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, ClassVar

import yaml

from kairos_core.studio_master.adapters_real.base import AdapterUnavailable
from kairos_core.studio_master.adapters_real.crepe_adapter import CrepeAdapter
from kairos_core.studio_master.adapters_real.demucs_adapter import DemucsAdapter
from kairos_core.studio_master.adapters_real.fluidsynth_adapter import FluidSynthAdapter
from kairos_core.studio_master.adapters_real.mosnet_adapter import MosnetAdapter
from kairos_core.studio_master.adapters_real.moviepy_adapter import MoviePyAdapter
from kairos_core.studio_master.adapters_real.pedalboard_adapter import PedalboardAdapter


class RealAdapterRegistry:
    """Registro lazy dos adapters reais, com licença e fallback visíveis."""

    _adapter_types: ClassVar[dict[str, type[Any]]] = {
        "crepe": CrepeAdapter,
        "pedalboard": PedalboardAdapter,
        "fluidsynth": FluidSynthAdapter,
        "demucs": DemucsAdapter,
        "mosnet": MosnetAdapter,
        "moviepy": MoviePyAdapter,
    }

    def __init__(self, settings: Any) -> None:
        self.settings = settings
        self._adapters = {adapter_id: adapter_type(settings) for adapter_id, adapter_type in self._adapter_types.items()}
        self._manifest, self._manifest_error = self._load_manifest(settings.studio_master_adapter_licenses_path)

    def capabilities(self) -> list[dict[str, Any]]:
        payload: list[dict[str, Any]] = []
        for adapter_id, adapter in self._adapters.items():
            capability = asdict(adapter.capability())
            manifest_entry = self._manifest.get("adapters", {}).get(adapter_id, {})
            if self._manifest_error:
                capability["enabled"] = False
                capability["reason"] = f"manifesto de licença inválido: {self._manifest_error}"
            elif not self._manifest_entry_matches(adapter_id, manifest_entry, capability["license"]):
                capability["enabled"] = False
                capability["reason"] = "entrada do manifesto não corresponde ao adapter"
            capability["license_status"] = "accepted" if capability["license"]["accepted"] else "pending"
            capability["operational_status"] = "READY" if capability["enabled"] else "FALLBACK_ONLY"
            payload.append(capability)
        return payload

    def preflight(self, adapter_id: str) -> dict[str, Any]:
        adapter = self._adapters.get(adapter_id)
        if adapter is None:
            raise AdapterUnavailable(f"adapter desconhecido: {adapter_id}")
        capability = next(item for item in self.capabilities() if item["adapter_id"] == adapter_id)
        return {
            "adapter_id": adapter_id,
            "status": capability["operational_status"],
            "capability": capability,
            "run_requires": {
                "real_execution": "gate + allowlist + license acceptance + artifact manifest",
                "fallback": capability["fallback"],
            },
        }

    def get(self, adapter_id: str) -> Any:
        adapter = self._adapters.get(adapter_id)
        if adapter is None:
            raise AdapterUnavailable(f"adapter desconhecido: {adapter_id}")
        return adapter

    @staticmethod
    def _load_manifest(path: str | Path) -> tuple[dict[str, Any], str | None]:
        manifest_path = Path(path)
        if not manifest_path.is_file():
            return {}, f"arquivo não encontrado: {manifest_path}"
        try:
            payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            return {}, str(exc)
        if not isinstance(payload, dict) or not isinstance(payload.get("adapters"), dict):
            return {}, "manifesto deve conter adapters como objeto"
        return payload, None

    @staticmethod
    def _manifest_entry_matches(adapter_id: str, entry: Any, license_payload: dict[str, Any]) -> bool:
        return bool(
            isinstance(entry, dict)
            and entry.get("package")
            and entry.get("source_url")
            and entry.get("code_license") == license_payload["code_license"]
            and entry.get("code_license_url") == license_payload["code_license_url"]
            and adapter_id == license_payload["adapter_id"]
        )
