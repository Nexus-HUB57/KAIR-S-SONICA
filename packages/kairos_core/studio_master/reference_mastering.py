from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class ReferenceMasteringUnavailable(RuntimeError):
    """Indica que o backend de masterização referencial não foi habilitado."""


@dataclass(frozen=True, slots=True)
class ReferenceMasteringPlan:
    method: str
    target_reference: str
    fft_size: int
    approval_required: bool
    warnings: tuple[str, ...]


class ReferenceMasteringAdapter:
    """Seam explícito para Matchering; nunca seleciona referências por conta própria."""

    @staticmethod
    def capabilities() -> dict[str, object]:
        return {
            "name": "reference-mastering",
            "preview": "contract-only",
            "backend": "matchering",
            "automatic_reference_discovery": False,
            "requires_operator_reference": True,
        }

    def plan(self, reference_path: str | Path, *, fft_size: int = 4_096) -> ReferenceMasteringPlan:
        path = Path(reference_path)
        if not path.name or path.is_absolute() and not path.exists():
            raise ValueError("A referência deve ser um caminho existente aprovado pelo operador")
        if fft_size not in {1_024, 2_048, 4_096, 8_192}:
            raise ValueError("fft_size deve ser 1024, 2048, 4096 ou 8192")
        return ReferenceMasteringPlan(
            method="matchering-contract/v1",
            target_reference=str(path),
            fft_size=fft_size,
            approval_required=True,
            warnings=(
                "O adapter não baixa nem procura referências automaticamente.",
                "A referência deve ser própria, licenciada ou de domínio público.",
                "Nenhum arquivo é escrito durante o planejamento.",
            ),
        )

    @staticmethod
    def render(*_args: object, **_kwargs: object) -> None:
        raise ReferenceMasteringUnavailable(
            "Renderização Matchering requer dependência opcional, referência aprovada e gate explícito"
        )
