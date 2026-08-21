from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kairos_core.studio_master.v2_contracts import AutoRetrainStatus


class AutoRetrainGuard:
    """Gate seguro para evolução de modelos; valida metadados, não treina sozinho."""

    def __init__(self, manifest_path: str | Path, *, enabled: bool = False, min_approved_samples: int = 20) -> None:
        self.manifest_path = Path(manifest_path)
        self.enabled = enabled
        self.min_approved_samples = min_approved_samples

    def status(self) -> AutoRetrainStatus:
        required = ["operator_approval", "license_provenance", "validation_split"]
        if not self.enabled:
            return AutoRetrainStatus(
                enabled=False,
                ready=False,
                status="DISABLED",
                required_approvals=required,
                warnings=["Auto-retraining permanece desligado por padrão."],
            )
        if not self.manifest_path.is_file():
            return AutoRetrainStatus(
                enabled=True,
                ready=False,
                status="WAITING_MANIFEST",
                dataset_manifest=str(self.manifest_path),
                required_approvals=required,
                warnings=["Crie um manifesto com samples aprovados e proveniência antes de treinar."],
            )
        try:
            manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return AutoRetrainStatus(
                enabled=True,
                ready=False,
                status="BLOCKED",
                dataset_manifest=str(self.manifest_path),
                required_approvals=required,
                warnings=[f"Manifesto inválido: {exc}"],
            )
        if not isinstance(manifest, dict):
            return AutoRetrainStatus(
                enabled=True,
                ready=False,
                status="BLOCKED",
                dataset_manifest=str(self.manifest_path),
                required_approvals=required,
                warnings=["Manifesto deve ser um objeto JSON."],
            )
        missing = [field for field in required if not manifest.get(field)]
        approved_samples = int(manifest.get("approved_samples", 0) or 0)
        if missing or approved_samples < self.min_approved_samples:
            warnings = [
                f"São necessários pelo menos {self.min_approved_samples} samples aprovados; recebido {approved_samples}."
            ]
            if missing:
                warnings.append(f"Campos obrigatórios ausentes: {', '.join(missing)}.")
            return AutoRetrainStatus(
                enabled=True,
                ready=False,
                status="WAITING_MANIFEST",
                dataset_manifest=str(self.manifest_path),
                required_approvals=required,
                warnings=warnings,
            )
        return AutoRetrainStatus(
            enabled=True,
            ready=True,
            status="READY_FOR_APPROVAL",
            dataset_manifest=str(self.manifest_path),
            required_approvals=required,
            warnings=[
                "Manifesto elegível para revisão; nenhum treino ou promoção foi executado.",
                "Promoção deve usar checkpoint novo e troca atômica validada por teste/ffprobe quando aplicável.",
            ],
        )

    def execution_plan(self) -> dict[str, Any]:
        current = self.status()
        return {
            "status": current.model_dump(),
            "action": "manual-approval-required",
            "train_command": "python scripts/train_groove_extractor.py --manifest <approved-manifest>",
            "promotion_policy": "write-new-checkpoint-then-atomic-rename-after-validation",
            "automatic_execution": False,
        }
