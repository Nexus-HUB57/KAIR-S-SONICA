from __future__ import annotations

from dataclasses import dataclass, field

from kairos_core.agents.maestro import MaestroAgent
from kairos_core.agents.rhythm import RhythmAgent
from kairos_core.agents.vocal import VocalAgent
from kairos_core.schemas import TrackPlan, TrackRequest


@dataclass(slots=True)
class Orchestra:
    """Coordena agentes de planejamento, groove e organização lírica."""

    maestro: MaestroAgent = field(default_factory=MaestroAgent)
    rhythm: RhythmAgent = field(default_factory=RhythmAgent)
    vocal: VocalAgent = field(default_factory=VocalAgent)

    def plan(self, request: TrackRequest, request_id: str | None = None) -> TrackPlan:
        return self.maestro.build_plan(request, request_id=request_id)
