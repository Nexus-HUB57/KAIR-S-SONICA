from kairos_core.schemas import Progress

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


def test_task_store_returns_none_for_unknown_task(tmp_path) -> None:
    store = TaskStore(tmp_path / "tasks.sqlite3")

    assert store.get("missing") is None
