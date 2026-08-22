from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from kairos_core.social.contracts import SocialRunRequest
from kairos_core.social.scheduler import SocialScheduleStore


def test_schedule_store_claims_and_dispatches_due_request(tmp_path: Path) -> None:
    store = SocialScheduleStore(tmp_path / "social.sqlite3")
    request = SocialRunRequest(
        objective="prepare a scheduled KTD launch package",
        campaign_id="scheduled-1",
        schedule_at=datetime.now(timezone.utc) - timedelta(minutes=1),
        include_llm=False,
        execute_actions=False,
    )
    created = store.create(request, schedule_id="schedule-1")
    assert created["status"] == "SCHEDULED"

    due = store.claim_due(now=datetime.now(timezone.utc))
    assert len(due) == 1
    assert due[0].campaign_id == "scheduled-1"
    assert store.claim_due(now=datetime.now(timezone.utc)) == []


def test_schedule_store_persists_and_lists_requests(tmp_path: Path) -> None:
    store = SocialScheduleStore(tmp_path / "social.sqlite3")
    request = SocialRunRequest(
        objective="collect analytics for KTD",
        campaign_id="analytics-1",
        schedule_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    store.create(request, schedule_id="schedule-2")

    listed = store.list(status="SCHEDULED")
    assert len(listed) == 1
    assert listed[0]["schedule_id"] == "schedule-2"
    assert listed[0]["request"]["campaign_id"] == "analytics-1"
