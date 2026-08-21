from kairos_core.schemas import Progress, TrackRequest

from services.api.main import TaskStore


def test_task_store_persists_snapshots(tmp_path) -> None:
    database = tmp_path / "tasks.sqlite3"
    first_store = TaskStore(database)
    created = first_store.create("task-1")
    first_store.update(
        "task-1",
        status="SUCCEEDED",
        progress=Progress(step="completed", percent=100, message="Pronto"),
        result={"format": "wav"},
    )

    second_store = TaskStore(database)
    restored = second_store.get("task-1")

    assert created.status == "PENDING"
    assert restored is not None
    assert restored.status == "SUCCEEDED"
    assert restored.progress.percent == 100
    assert restored.result == {"format": "wav"}


def test_task_store_recovers_orphaned_job_after_restart(tmp_path) -> None:
    store = TaskStore(tmp_path / "tasks.sqlite3")
    request = TrackRequest(prompt="recovery")
    store.create("recover-me", job_kind="audio", payload=request.model_dump(mode="json"))
    store.update(
        "recover-me",
        status="RUNNING",
        progress=Progress(step="generating", percent=50, message="Em execução"),
    )

    store.reset_orphaned_jobs()
    recovered = store.claim_recoverable_jobs("test-worker")

    assert recovered == [("recover-me", "audio", request.model_dump(mode="json"))]
    snapshot = store.get("recover-me")
    assert snapshot is not None
    assert snapshot.status == "PENDING"
    assert snapshot.progress.step == "queued"
    assert store.claim_recoverable_jobs("second-worker") == []


def test_task_store_returns_none_for_unknown_task(tmp_path) -> None:
    store = TaskStore(tmp_path / "tasks.sqlite3")

    assert store.get("missing") is None
