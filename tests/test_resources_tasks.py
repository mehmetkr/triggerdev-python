"""Tests for the Tasks resource."""

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import respx

from triggerdev.types.tasks import (
    BatchTriggerTaskResponse,
    TriggerTaskResponse,
)

if TYPE_CHECKING:
    from triggerdev import Client


class TestTasksTrigger:
    @respx.mock
    def test_trigger_basic(self, client: Client) -> None:
        route = respx.post("https://api.trigger.dev/api/v1/tasks/my-task/trigger").mock(
            return_value=httpx.Response(200, json={"id": "run_1234"})
        )
        result = client.tasks.trigger("my-task", payload={"message": "hello"})
        assert isinstance(result, TriggerTaskResponse)
        assert result.id == "run_1234"
        assert route.called
        body = route.calls[0].request.read()
        import json

        parsed = json.loads(body)
        assert parsed["payload"] == {"message": "hello"}

    @respx.mock
    def test_trigger_with_options(self, client: Client) -> None:
        route = respx.post("https://api.trigger.dev/api/v1/tasks/my-task/trigger").mock(
            return_value=httpx.Response(200, json={"id": "run_5678"})
        )
        result = client.tasks.trigger(
            "my-task",
            payload={"data": 1},
            context={"user": "u1"},
        )
        assert result.id == "run_5678"
        import json

        body = json.loads(route.calls[0].request.read())
        assert body["payload"] == {"data": 1}
        assert body["context"] == {"user": "u1"}

    @respx.mock
    def test_trigger_empty_payload(self, client: Client) -> None:
        respx.post("https://api.trigger.dev/api/v1/tasks/my-task/trigger").mock(
            return_value=httpx.Response(200, json={"id": "run_0"})
        )
        result = client.tasks.trigger("my-task")
        assert result.id == "run_0"


class TestTasksBatchTrigger:
    @respx.mock
    def test_batch_trigger_by_task_id(self, client: Client) -> None:
        route = respx.post("https://api.trigger.dev/api/v1/tasks/my-task/batch").mock(
            return_value=httpx.Response(
                200,
                json={"batchId": "batch_1", "runs": ["run_1", "run_2"]},
            )
        )
        result = client.tasks.batch_trigger(
            "my-task",
            items=[{"payload": {"n": 1}}, {"payload": {"n": 2}}],
        )
        assert isinstance(result, BatchTriggerTaskResponse)
        assert result.batch_id == "batch_1"
        assert result.runs == ["run_1", "run_2"]
        assert route.called

    @respx.mock
    def test_batch_trigger_multi_task(self, client: Client) -> None:
        route = respx.post("https://api.trigger.dev/api/v1/tasks/batch").mock(
            return_value=httpx.Response(
                200,
                json={"batchId": "batch_2", "runs": ["run_3"]},
            )
        )
        result = client.tasks.batch_trigger_multi(
            items=[{"task": "task-a", "payload": {"n": 1}}],
        )
        assert result.batch_id == "batch_2"
        assert route.called
