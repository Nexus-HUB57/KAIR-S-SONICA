from fastapi.testclient import TestClient
from kairos_core.schemas import Progress

from services.api.main import app, store


def test_task_websocket_streams_snapshot() -> None:
    task_id = "websocket-test-task"
    store.create(task_id)
    store.update(
        task_id,
        status="SUCCEEDED",
        progress=Progress(step="completed", percent=100, message="Artefato pronto"),
    )

    with TestClient(app) as client, client.websocket_connect(f"/ws/tasks/{task_id}") as websocket:
        snapshot = websocket.receive_json()

    assert snapshot["task_id"] == task_id
    assert snapshot["status"] == "SUCCEEDED"
    assert snapshot["progress"]["percent"] == 100
