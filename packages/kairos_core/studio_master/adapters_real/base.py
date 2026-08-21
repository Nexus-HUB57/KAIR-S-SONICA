from __future__ import annotations

import json
from dataclasses import dataclass, field
from importlib.metadata import PackageNotFoundError, version
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Protocol


class AdapterUnavailable(RuntimeError):
    """Dependência, licença, asset ou configuração necessários não estão prontos."""


@dataclass(frozen=True, slots=True)
class LicensePolicy:
    adapter_id: str
    code_license: str
    code_license_url: str
    source_url: str
    model_artifact_policy: str
    risk_level: str
    accepted: bool = False


@dataclass(frozen=True, slots=True)
class AdapterCapability:
    adapter_id: str
    package: str
    import_module: str
    available: bool
    enabled: bool
    license: LicensePolicy
    requires_gpu: bool
    requires_external_asset: bool
    fallback: str
    package_version: str | None = None
    reason: str | None = None


@dataclass(slots=True)
class AdapterResult:
    adapter_id: str
    method: str
    status: str
    output: Any = None
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    fallback_used: bool = False


@dataclass(frozen=True, slots=True)
class AdapterSpec:
    adapter_id: str
    package: str
    import_module: str
    code_license: str
    code_license_url: str
    source_url: str
    model_artifact_policy: str
    requires_gpu: bool
    requires_external_asset: bool
    fallback: str
    risk_level: str


class AdapterContext:
    """Contexto comum: manifest, settings e policy de execução sem import pesado."""

    def __init__(self, settings: Any, spec: AdapterSpec) -> None:
        self.settings = settings
        self.spec = spec

    def dependency_available(self) -> bool:
        return find_spec(self.spec.import_module) is not None

    def package_version(self) -> str | None:
        try:
            return version(self.spec.package)
        except PackageNotFoundError:
            return None

    def license_accepted(self) -> bool:
        accepted = {item.strip() for item in self.settings.studio_master_accepted_adapter_licenses}
        return self.spec.code_license in accepted

    def model_manifest_ready(self) -> bool:
        if self.spec.model_artifact_policy == "not_applicable":
            return True
        path = Path(self.settings.studio_master_adapter_model_manifest_path)
        if not path.is_file():
            return False
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return False
        entry = payload.get("adapters", {}).get(self.spec.adapter_id, {}) if isinstance(payload, dict) else {}
        return bool(
            isinstance(entry, dict)
            and entry.get("approved") is True
            and entry.get("license")
            and entry.get("checksum")
            and entry.get("artifact_ref")
        )

    def explicitly_enabled(self) -> bool:
        enabled_ids = set(self.settings.studio_master_enabled_adapter_ids)
        return (
            self.settings.studio_master_real_adapters_enabled
            and self.spec.adapter_id in enabled_ids
            and self.license_accepted()
            and self.model_manifest_ready()
        )

    def capability(self) -> AdapterCapability:
        dependency_available = self.dependency_available()
        license_policy = LicensePolicy(
            adapter_id=self.spec.adapter_id,
            code_license=self.spec.code_license,
            code_license_url=self.spec.code_license_url,
            source_url=self.spec.source_url,
            model_artifact_policy=self.spec.model_artifact_policy,
            risk_level=self.spec.risk_level,
            accepted=self.license_accepted(),
        )
        reasons: list[str] = []
        if not dependency_available:
            reasons.append(f"dependência ausente: {self.spec.import_module}")
        if not self.license_accepted():
            reasons.append("licença não foi aceita no ambiente")
        if not self.settings.studio_master_real_adapters_enabled:
            reasons.append("gate global desligado")
        elif self.spec.adapter_id not in set(self.settings.studio_master_enabled_adapter_ids):
            reasons.append("adapter não está na allowlist")
        if self.spec.model_artifact_policy != "not_applicable" and not self.model_manifest_ready():
            reasons.append("manifesto de modelo/asset sem aprovação, licença, checksum e artifact_ref")
        return AdapterCapability(
            adapter_id=self.spec.adapter_id,
            package=self.spec.package,
            import_module=self.spec.import_module,
            available=dependency_available,
            enabled=self.explicitly_enabled() and dependency_available,
            license=license_policy,
            requires_gpu=self.spec.requires_gpu,
            requires_external_asset=self.spec.requires_external_asset,
            fallback=self.spec.fallback,
            package_version=self.package_version(),
            reason="; ".join(reasons) if reasons else None,
        )

    def require_ready(self) -> None:
        capability = self.capability()
        if not capability.enabled:
            raise AdapterUnavailable(capability.reason or "adapter não está pronto")

    def approved_asset(self, raw_path: str | Path) -> Path:
        candidate = Path(raw_path).expanduser().resolve()
        root = Path(self.settings.studio_master_adapter_assets_dir).expanduser().resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise AdapterUnavailable("asset fora do diretório aprovado") from exc
        if not candidate.is_file():
            raise AdapterUnavailable("asset aprovado não existe")
        return candidate

    def new_output(self, raw_path: str | Path) -> Path:
        candidate = Path(raw_path).expanduser().resolve()
        root = Path(self.settings.studio_master_adapter_output_dir).expanduser().resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise AdapterUnavailable("saída fora do diretório de adapters") from exc
        if candidate.exists():
            raise AdapterUnavailable("saída existente não será sobrescrita")
        candidate.parent.mkdir(parents=True, exist_ok=True)
        return candidate


class RealAdapter(Protocol):
    adapter_id: str

    def capability(self) -> AdapterCapability:
        ...

    def run(self, *args: Any, **kwargs: Any) -> AdapterResult:
        ...
