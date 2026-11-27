"""Tests for the Runs resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx
import pytest
import respx

from triggerdev._exceptions import NotFoundError
from triggerdev.types.runs import (
    ListRunsResult,
    RetrieveRunResponse,
)

if TYPE_CHECKING:
    from triggerdev import Client

RETRIEVE_RUN_RESPONSE: dict[str, Any] = {
    "id": "run_1234",
    "status": "COMPLETED",
    "taskIdentifier": "my-task",
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:01:00Z",
    "isTest": False,
    "attempts": [
        {
            "id": "attempt_1",
            "status": "COMPLETED",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:01:00Z",
        }
    ],
}


class TestRunsList:
    @respx.mock
    def test_list_basic(self, client: Client) -> None:
        route = respx.get("https://api.trigger.dev/api/v1/runs").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "run_1",
                            "status": "COMPLETED",
                            "taskIdentifier": "t1",
                            "env": {"id": "env_1", "name": "dev"},
                            "isTest": False,
                            "createdAt": "2024-01-01T00:00:00Z",
                            "updatedAt": "2024-01-01T00:01:00Z",
                        }
                    ],
                    "pagination": {"next": "run_2"},
                },
            )
        )
        result = client.runs.list()
        assert isinstance(result, ListRunsResult)
        assert result.data is not None
        assert len(result.data) == 1
        assert result.data[0].id == "run_1"
        assert route.called

    @respx.mock
    def test_list_with_status_filter(self, client: Client) -> None:
        route = respx.get("https://api.trigger.dev/api/v1/runs").mock(
            return_value=httpx.Response(200, json={"data": []})
        )
        client.runs.list(status=["QUEUED", "EXECUTING"])
        request = route.calls[0].request
        url = str(request.url)
        assert "filter%5Bstatus%5D=QUEUED%2CEXECUTING" in url or "filter[status]=QUEUED,EXECUTING" in url

    @respx.mock
    def test_list_with_pagination(self, client: Client) -> None:
        route = respx.get("https://api.trigger.dev/api/v1/runs").mock(
            return_value=httpx.Response(200, json={"data": []})
        )
        client.runs.list(page_size=10, cursor_after="run_100")
        request = route.calls[0].request
        url = str(request.url)
        assert "page%5Bsize%5D=10" in url or "page[size]=10" in url
        assert "page%5Bafter%5D=run_100" in url or "page[after]=run_100" in url

    @respx.mock
    def test_list_with_created_at_period(self, client: Client) -> None:
        route = respx.get("https://api.trigger.dev/api/v1/runs").mock(
            return_value=httpx.Response(200, json={"data": []})
        )
        client.runs.list(created_at_period="30d")
        request = route.calls[0].request
        url = str(request.url)
        assert "filter%5BcreatedAt%5D%5Bperiod%5D=30d" in url or "filter[createdAt][period]=30d" in url


class TestRunsRetrieve:
    @respx.mock
    def test_retrieve(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v3/runs/run_1234").mock(
            return_value=httpx.Response(200, json=RETRIEVE_RUN_RESPONSE)
        )
        result = client.runs.retrieve("run_1234")
        assert isinstance(result, RetrieveRunResponse)
        assert result.id == "run_1234"
        assert result.status == "COMPLETED"

    @respx.mock
    def test_retrieve_not_found(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v3/runs/run_bad").mock(
            return_value=httpx.Response(404, json={"error": "Run not found"})
        )
        with pytest.raises(NotFoundError):
            client.runs.retrieve("run_bad")


class TestRunsResult:
    @respx.mock
    def test_result_success(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v1/runs/run_1234/result").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ok": True,
                    "id": "run_1234",
                    "output": '{"result": 42}',
                    "outputType": "application/json",
                    "taskIdentifier": "my-task",
                    "usage": {"durationMs": 150},
                },
            )
        )
        result = client.runs.result("run_1234")
        assert result.ok is True
        assert result.id == "run_1234"
        assert result.output == '{"result": 42}'

    @respx.mock
    def test_result_failure(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v1/runs/run_bad/result").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ok": False,
                    "id": "run_bad",
                    "error": {"message": "Task failed"},
                },
            )
        )
        result = client.runs.result("run_bad")
        assert result.ok is False
        assert result.error is not None


class TestRunsReplay:
    @respx.mock
    def test_replay_no_overrides(self, client: Client) -> None:
        route = respx.post("https://api.trigger.dev/api/v1/runs/run_1234/replay").mock(
            return_value=httpx.Response(200, json={"id": "run_5678"})
        )
        result = client.runs.replay("run_1234")
        assert result.id == "run_5678"
        assert route.called

    @respx.mock
    def test_replay_with_overrides(self, client: Client) -> None:
        import json

        route = respx.post("https://api.trigger.dev/api/v1/runs/run_1234/replay").mock(
            return_value=httpx.Response(200, json={"id": "run_9999"})
        )
        result = client.runs.replay(
            "run_1234",
            payload={"new": "data"},
            tags=["replayed"],
            delay="10m",
        )
        assert result.id == "run_9999"
        body = json.loads(route.calls[0].request.read())
        assert body["payload"] == {"new": "data"}
        assert body["tags"] == ["replayed"]
        assert body["delay"] == "10m"


class TestRunsCancel:
    @respx.mock
    def test_cancel(self, client: Client) -> None:
        respx.post("https://api.trigger.dev/api/v2/runs/run_1234/cancel").mock(
            return_value=httpx.Response(200, json={"id": "run_1234"})
        )
        result = client.runs.cancel("run_1234")
        assert result.id == "run_1234"


class TestRunsReschedule:
    @respx.mock
    def test_reschedule_with_delay_string(self, client: Client) -> None:
        respx.post("https://api.trigger.dev/api/v1/runs/run_1234/reschedule").mock(
            return_value=httpx.Response(200, json=RETRIEVE_RUN_RESPONSE)
        )
        result = client.runs.reschedule("run_1234", delay="1h30m")
        assert isinstance(result, RetrieveRunResponse)

    @respx.mock
    def test_reschedule_with_datetime(self, client: Client) -> None:
        import json
        from datetime import datetime, timezone

        route = respx.post("https://api.trigger.dev/api/v1/runs/run_1234/reschedule").mock(
            return_value=httpx.Response(200, json=RETRIEVE_RUN_RESPONSE)
        )
        dt = datetime(2026, 12, 1, 15, 30, 0, tzinfo=timezone.utc)
        result = client.runs.reschedule("run_1234", delay=dt)
        assert isinstance(result, RetrieveRunResponse)
        body = json.loads(route.calls[0].request.read())
        assert body["delay"] == "2026-12-01T15:30:00+00:00"


class TestRunsUpdateMetadata:
    @respx.mock
    def test_update_metadata(self, client: Client) -> None:
        import json

        route = respx.put("https://api.trigger.dev/api/v1/runs/run_1234/metadata").mock(
            return_value=httpx.Response(200, json={"metadata": {"key": "value"}})
        )
        result = client.runs.update_metadata("run_1234", metadata={"key": "value"})
        assert result.metadata == {"key": "value"}
        body = json.loads(route.calls[0].request.read())
        assert body["metadata"] == {"key": "value"}


class TestRunsAddTags:
    @respx.mock
    def test_add_tags(self, client: Client) -> None:
        import json

        route = respx.post("https://api.trigger.dev/api/v1/runs/run_1234/tags").mock(
            return_value=httpx.Response(200, json={"message": "Successfully set 2 new tags."})
        )
        result = client.runs.add_tags("run_1234", tags=["tag-1", "tag-2"])
        assert "Successfully" in result.message
        body = json.loads(route.calls[0].request.read())
        assert body["tags"] == ["tag-1", "tag-2"]

    @respx.mock
    def test_add_single_tag_as_string(self, client: Client) -> None:
        respx.post("https://api.trigger.dev/api/v1/runs/run_1234/tags").mock(
            return_value=httpx.Response(200, json={"message": "Successfully set 1 new tags."})
        )
        result = client.runs.add_tags("run_1234", tags="single-tag")
        assert result.message is not None


class TestRunsEvents:
    @respx.mock
    def test_events(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v1/runs/run_1234/events").mock(
            return_value=httpx.Response(
                200,
                json={
                    "events": [
                        {
                            "spanId": "span_1",
                            "message": "Task started",
                            "startTime": "1700000000000000000",
                            "duration": 100000,
                            "isError": False,
                            "isPartial": False,
                            "isCancelled": False,
                            "level": "INFO",
                        }
                    ]
                },
            )
        )
        result = client.runs.events("run_1234")
        assert isinstance(result, dict)
        assert "events" in result


class TestRunsTrace:
    @respx.mock
    def test_trace_tree(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v1/runs/run_1234/trace").mock(
            return_value=httpx.Response(
                200,
                json={
                    "trace": {
                        "traceId": "abc123",
                        "rootSpan": {
                            "id": "span_root",
                            "runId": "run_1234",
                            "data": {"message": "root"},
                        },
                    }
                },
            )
        )
        result = client.runs.trace("run_1234")
        assert isinstance(result, dict)
        assert "trace" in result

    @respx.mock
    def test_trace_paged(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v1/runs/run_1234/trace").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [{"id": "span_1", "message": "hello"}],
                    "pagination": {"next": "cursor_abc"},
                },
            )
        )
        result = client.runs.trace_paged("run_1234", page_size=1000)
        assert isinstance(result, dict)
        assert "data" in result
