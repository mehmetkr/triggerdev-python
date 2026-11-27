"""Tests for the Schedules resource."""

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest
import respx

from triggerdev._exceptions import NotFoundError
from triggerdev.types.schedules import (
    GetTimezonesResult,
    ListSchedulesResult,
    ScheduleObject,
)

if TYPE_CHECKING:
    from triggerdev import Client

SCHEDULE_JSON = {
    "id": "sched_1234",
    "task": "my-task",
    "type": "IMPERATIVE",
    "active": True,
    "deduplicationKey": "dedup_1",
    "generator": {"type": "CRON", "expression": "0 0 * * *"},
    "timezone": "UTC",
}


class TestSchedulesList:
    @respx.mock
    def test_list_basic(self, client: Client) -> None:
        route = respx.get("https://api.trigger.dev/api/v1/schedules").mock(
            return_value=httpx.Response(
                200,
                json={"data": [SCHEDULE_JSON], "pagination": {"currentPage": 1, "totalPages": 1, "count": 1}},
            )
        )
        result = client.schedules.list()
        assert isinstance(result, ListSchedulesResult)
        assert result.data is not None
        assert len(result.data) == 1
        assert result.data[0].id == "sched_1234"
        assert route.called

    @respx.mock
    def test_list_with_pagination(self, client: Client) -> None:
        route = respx.get("https://api.trigger.dev/api/v1/schedules").mock(
            return_value=httpx.Response(200, json={"data": []})
        )
        client.schedules.list(page=2, per_page=10)
        url = str(route.calls[0].request.url)
        assert "page=2" in url
        assert "perPage=10" in url


class TestSchedulesCreate:
    @respx.mock
    def test_create(self, client: Client) -> None:
        import json

        route = respx.post("https://api.trigger.dev/api/v1/schedules").mock(
            return_value=httpx.Response(200, json=SCHEDULE_JSON)
        )
        result = client.schedules.create(
            task="my-task",
            cron="0 0 * * *",
            deduplication_key="dedup_1",
            timezone="UTC",
        )
        assert isinstance(result, ScheduleObject)
        assert result.id == "sched_1234"
        body = json.loads(route.calls[0].request.read())
        assert body["task"] == "my-task"
        assert body["cron"] == "0 0 * * *"
        assert body["deduplicationKey"] == "dedup_1"


class TestSchedulesRetrieve:
    @respx.mock
    def test_retrieve(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v1/schedules/sched_1234").mock(
            return_value=httpx.Response(200, json=SCHEDULE_JSON)
        )
        result = client.schedules.retrieve("sched_1234")
        assert isinstance(result, ScheduleObject)
        assert result.id == "sched_1234"

    @respx.mock
    def test_retrieve_not_found(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v1/schedules/sched_bad").mock(
            return_value=httpx.Response(404, json={"error": "Resource not found"})
        )
        with pytest.raises(NotFoundError):
            client.schedules.retrieve("sched_bad")


class TestSchedulesUpdate:
    @respx.mock
    def test_update(self, client: Client) -> None:
        import json

        route = respx.put("https://api.trigger.dev/api/v1/schedules/sched_1234").mock(
            return_value=httpx.Response(200, json=SCHEDULE_JSON)
        )
        result = client.schedules.update(
            "sched_1234",
            task="my-task",
            cron="0 12 * * *",
        )
        assert isinstance(result, ScheduleObject)
        body = json.loads(route.calls[0].request.read())
        assert body["cron"] == "0 12 * * *"


class TestSchedulesDelete:
    @respx.mock
    def test_delete(self, client: Client) -> None:
        route = respx.delete("https://api.trigger.dev/api/v1/schedules/sched_1234").mock(
            return_value=httpx.Response(200)
        )
        result = client.schedules.delete("sched_1234")
        assert result is None
        assert route.called


class TestSchedulesActivateDeactivate:
    @respx.mock
    def test_activate(self, client: Client) -> None:
        respx.post("https://api.trigger.dev/api/v1/schedules/sched_1234/activate").mock(
            return_value=httpx.Response(200, json={**SCHEDULE_JSON, "active": True})
        )
        result = client.schedules.activate("sched_1234")
        assert isinstance(result, ScheduleObject)
        assert result.active is True

    @respx.mock
    def test_deactivate(self, client: Client) -> None:
        respx.post("https://api.trigger.dev/api/v1/schedules/sched_1234/deactivate").mock(
            return_value=httpx.Response(200, json={**SCHEDULE_JSON, "active": False})
        )
        result = client.schedules.deactivate("sched_1234")
        assert isinstance(result, ScheduleObject)
        assert result.active is False


class TestSchedulesTimezones:
    @respx.mock
    def test_timezones(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v1/timezones").mock(
            return_value=httpx.Response(200, json={"timezones": ["UTC", "America/New_York"]})
        )
        result = client.schedules.timezones()
        assert isinstance(result, GetTimezonesResult)
        assert result.timezones is not None
        assert "UTC" in result.timezones

    @respx.mock
    def test_timezones_exclude_utc(self, client: Client) -> None:
        route = respx.get("https://api.trigger.dev/api/v1/timezones").mock(
            return_value=httpx.Response(200, json={"timezones": ["America/New_York"]})
        )
        client.schedules.timezones(exclude_utc=True)
        url = str(route.calls[0].request.url)
        assert "excludeUtc=true" in url
