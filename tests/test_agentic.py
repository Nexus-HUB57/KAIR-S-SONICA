from __future__ import annotations

from kairos_core.agentic import AGENT_ROLES, AgenticOrchestrator, AgenticRunRequest, ProjectMemory
from kairos_core.config import Settings


def test_agentic_orchestrator_runs_all_twelve_roles_without_external_tools(tmp_path) -> None:
    settings = Settings(agentic_memory_dir=tmp_path / "memory", agentic_external_tools_enabled=False)
    result = AgenticOrchestrator(settings).run(
        AgenticRunRequest(
            prompt="clipe de rap em chuva neon",
            project_id="test-project",
            duration_seconds=10,
            scene_seconds=5,
            seed=42,
            include_media_references=True,
        )
    )

    assert len(AGENT_ROLES) == 12
    assert len(result.roles) == 12
    assert result.status == "READY_FOR_APPROVAL"
    assert len(result.handoffs) == 3
    assert result.artifacts["retrieval"]["retrieval_mode"] == "disabled-by-external-tools-gate"
    assert result.artifacts["quality"]["passed"] is True
    assert result.artifacts["scene_plan"]["scenes"]
    assert {handoff.kind for handoff in result.handoffs} == {"video_request", "multimedia_request"}


def test_project_memory_recent_and_search_are_persistent(tmp_path) -> None:
    memory = ProjectMemory(tmp_path, "campaign/001")
    memory.append(run_id="run-1", role="ceo", kind="strategy", content={"briefing": "montanha e rock"})

    reopened = ProjectMemory(tmp_path, "campaign/001")

    assert reopened.recent(1)[0]["run_id"] == "run-1"
    assert reopened.search("rock")[0]["role"] == "ceo"
    assert "campaign_001.jsonl" in str(reopened.path)


def test_agentic_capabilities_expose_twelve_roles(tmp_path) -> None:
    settings = Settings(agentic_memory_dir=tmp_path)
    capabilities = AgenticOrchestrator(settings).capabilities()

    assert capabilities["enabled"] is True
    assert len(capabilities["roles"]) == 12
    assert capabilities["external_tools_default"] is False
    assert capabilities["roles"][-1]["key"] == "qa"
