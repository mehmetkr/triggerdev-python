"""Schedules resource client."""

from __future__ import annotations

from typing import Any

from triggerdev._base_client import SyncAPIResource
from triggerdev.types.schedules import (
    GetTimezonesResult,
    ListSchedulesResult,
    ScheduleObject,
)


class Schedules(SyncAPIResource):
    """Methods for managing schedules."""

    def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ListSchedulesResult:
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["perPage"] = per_page
        return self._request(
            "GET",
            "/api/v1/schedules",
            cast_to=ListSchedulesResult,
            params=params or None,
        )

    def create(
        self,
        *,
        task: str,
        cron: str,
        deduplication_key: str,
        external_id: str | None = None,
        timezone: str | None = None,
    ) -> ScheduleObject:
        body: dict[str, Any] = {
            "task": task,
            "cron": cron,
            "deduplicationKey": deduplication_key,
        }
        if external_id is not None:
            body["externalId"] = external_id
        if timezone is not None:
            body["timezone"] = timezone
        return self._request(
            "POST",
            "/api/v1/schedules",
            cast_to=ScheduleObject,
            body=body,
        )

    def retrieve(self, schedule_id: str) -> ScheduleObject:
        return self._request(
            "GET",
            f"/api/v1/schedules/{schedule_id}",
            cast_to=ScheduleObject,
        )

    def update(
        self,
        schedule_id: str,
        *,
        task: str,
        cron: str,
        external_id: str | None = None,
        timezone: str | None = None,
    ) -> ScheduleObject:
        body: dict[str, Any] = {
            "task": task,
            "cron": cron,
        }
        if external_id is not None:
            body["externalId"] = external_id
        if timezone is not None:
            body["timezone"] = timezone
        return self._request(
            "PUT",
            f"/api/v1/schedules/{schedule_id}",
            cast_to=ScheduleObject,
            body=body,
        )

    def delete(self, schedule_id: str) -> None:
        self._request(
            "DELETE",
            f"/api/v1/schedules/{schedule_id}",
            cast_to=None,
        )

    def activate(self, schedule_id: str) -> ScheduleObject:
        return self._request(
            "POST",
            f"/api/v1/schedules/{schedule_id}/activate",
            cast_to=ScheduleObject,
        )

    def deactivate(self, schedule_id: str) -> ScheduleObject:
        return self._request(
            "POST",
            f"/api/v1/schedules/{schedule_id}/deactivate",
            cast_to=ScheduleObject,
        )

    def timezones(
        self,
        *,
        exclude_utc: bool = False,
    ) -> GetTimezonesResult:
        params: dict[str, Any] = {}
        if exclude_utc:
            params["excludeUtc"] = "true"
        return self._request(
            "GET",
            "/api/v1/timezones",
            cast_to=GetTimezonesResult,
            params=params or None,
        )
