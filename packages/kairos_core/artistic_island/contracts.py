from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from pydantic import BaseModel, Field


@dataclass(frozen=True, slots=True)
class InstrumentProfile:
    name: str
    family: str
    roles: tuple[str, ...]
    tags: tuple[str, ...]
    eq_presets: tuple[dict[str, Any], ...]
    compression: dict[str, Any]
    space: dict[str, Any]
    vocal: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "family": self.family,
            "roles": list(self.roles),
            "tags": list(self.tags),
            "eq_presets": [dict(item) for item in self.eq_presets],
            "compression": dict(self.compression),
            "space": dict(self.space),
            "vocal": dict(self.vocal),
        }


@dataclass(frozen=True, slots=True)
class AlgorithmSpec:
    key: str
    title: str
    purpose: str
    parameter_schema: dict[str, str]
    execution_mode: Literal["contract-only", "numpy-compatible"] = "contract-only"
    optional_dependency: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "purpose": self.purpose,
            "parameter_schema": dict(self.parameter_schema),
            "execution_mode": self.execution_mode,
            "optional_dependency": self.optional_dependency,
        }


class MixPlanRequest(BaseModel):
    instrument: str = Field(min_length=1, max_length=120)
    context: Literal["music", "vocal", "beat", "cinematic", "orchestra", "master"] = "music"
    prompt: str | None = Field(default=None, max_length=2_000)
    max_steps: int = Field(default=12, ge=5, le=15)
    include_optional: bool = True
    reference_id: str | None = Field(default=None, max_length=160)


class ProcessingStep(BaseModel):
    order: int = Field(ge=1, le=15)
    algorithm: str = Field(min_length=1, max_length=80)
    parameters: dict[str, Any] = Field(default_factory=dict)
    rationale: str = Field(min_length=1, max_length=500)
    execution_mode: Literal["contract-only", "numpy-compatible"] = "contract-only"


class MixPlan(BaseModel):
    schema_version: int = 1
    island: str = "kairos-artistic-production-island"
    instrument: str
    family: str
    context: str
    profile_found: bool
    source: str
    chain: list[ProcessingStep]
    master_bus: dict[str, Any]
    provenance: dict[str, Any]
    warnings: list[str] = Field(default_factory=list)

    @property
    def algorithm_count(self) -> int:
        return len(self.chain)
