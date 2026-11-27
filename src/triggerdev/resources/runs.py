"""Runs resource client."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from triggerdev._base_client import RAW, SyncAPIResource
from triggerdev.types.runs import (
    AddTagsResponse,
    CancelRunResponse,
    ListRunsResult,
    ListRunStatus,
    ReplayRunResponse,
    RetrieveRunResponse,
    RunResultResponse,
    UpdateMetadataResponse,
)

if TYPE_CHECKING:
    from triggerdev.types.shared import TTL, Machine, RunTags


def _build_runs_filter_params(
    *,
    status: list[ListRunStatus] | None = None,
    task_identifier: list[str] | None = None,
    version: list[str] | None = None,
    bulk_action: str | None = None,
    schedule: str | None = None,
    is_test: bool | None = None,
    tag: list[str] | None = None,
    error: str | None = None,
    created_at_from: str | datetime | None = None,
    created_at_to: str | datetime | None = None,
    created_at_period: str | None = None,
    page_size: int | None = None,
    cursor_after: str | None = None,
    cursor_before: str | None = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    if status is not None:
        params["filter[status]"] = ",".join(status)
    if task_identifier is not None:
        params["filter[taskIdentifier]"] = ",".join(task_identifier)
    if version is not None:
        params["filter[version]"] = ",".join(version)
    if bulk_action is not None:
        params["filter[bulkAction]"] = bulk_action
    if schedule is not None:
        params["filter[schedule]"] = schedule
    if is_test is not None:
        params["filter[isTest]"] = str(is_test).lower()
    if tag is not None:
        params["filter[tag]"] = ",".join(tag)
    if error is not None:
        params["filter[error]"] = error
    if created_at_from is not None:
        val = created_at_from.isoformat() if isinstance(created_at_from, datetime) else created_at_from
        params["filter[createdAt][from]"] = val
    if created_at_to is not None:
        val = created_at_to.isoformat() if isinstance(created_at_to, datetime) else created_at_to
        params["filter[createdAt][to]"] = val
    if created_at_period is not None:
        params["filter[createdAt][period]"] = created_at_period
    if page_size is not None:
        params["page[size]"] = page_size
    if cursor_after is not None:
        params["page[after]"] = cursor_after
    if cursor_before is not None:
        params["page[before]"] = cursor_before

    return params


_List = list


class Runs(SyncAPIResource):
    """Methods for managing runs."""

    def list(
        self,
        *,
        status: _List[ListRunStatus] | None = None,
        task_identifier: _List[str] | None = None,
        version: _List[str] | None = None,
        bulk_action: str | None = None,
        schedule: str | None = None,
        is_test: bool | None = None,
        tag: _List[str] | None = None,
        error: str | None = None,
        created_at_from: str | datetime | None = None,
        created_at_to: str | datetime | None = None,
        created_at_period: str | None = None,
        page_size: int | None = None,
        cursor_after: str | None = None,
        cursor_before: str | None = None,
    ) -> ListRunsResult:
        params = _build_runs_filter_params(
            status=status,
            task_identifier=task_identifier,
            version=version,
            bulk_action=bulk_action,
            schedule=schedule,
            is_test=is_test,
            tag=tag,
            error=error,
            created_at_from=created_at_from,
            created_at_to=created_at_to,
            created_at_period=created_at_period,
            page_size=page_size,
            cursor_after=cursor_after,
            cursor_before=cursor_before,
        )
        return self._request(
            "GET",
            "/api/v1/runs",
            cast_to=ListRunsResult,
            params=params or None,
        )

    def retrieve(self, run_id: str) -> RetrieveRunResponse:
        return self._request(
            "GET",
            f"/api/v3/runs/{run_id}",
            cast_to=RetrieveRunResponse,
        )

    def result(self, run_id: str) -> RunResultResponse:
        return self._request(
            "GET",
            f"/api/v1/runs/{run_id}/result",
            cast_to=RunResultResponse,
        )

    def events(self, run_id: str) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/api/v1/runs/{run_id}/events",
            cast_to=RAW,
        )

    def trace(self, run_id: str) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/api/v1/runs/{run_id}/trace",
            cast_to=RAW,
        )

    def trace_paged(
        self,
        run_id: str,
        *,
        page_size: int | None = None,
        page_after: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size
        if page_after is not None:
            params["page[after]"] = page_after
        return self._request(
            "GET",
            f"/api/v1/runs/{run_id}/trace",
            cast_to=RAW,
            params=params or None,
        )

    def replay(
        self,
        run_id: str,
        *,
        payload: object | None = None,
        payload_type: str | None = None,
        metadata: dict[str, object] | None = None,
        tags: RunTags | None = None,
        queue: str | None = None,
        concurrency_key: str | None = None,
        machine: Machine | None = None,
        version: str | None = None,
        region: str | None = None,
        delay: str | None = None,
        ttl: TTL | None = None,
        idempotency_key: str | None = None,
        idempotency_key_ttl: str | None = None,
        max_attempts: int | None = None,
        max_duration: float | None = None,
        priority: float | None = None,
    ) -> ReplayRunResponse:
        body: dict[str, Any] = {}
        if payload is not None:
            body["payload"] = payload
        if payload_type is not None:
            body["payloadType"] = payload_type
        if metadata is not None:
            body["metadata"] = metadata
        if tags is not None:
            body["tags"] = tags
        if queue is not None:
            body["queue"] = queue
        if concurrency_key is not None:
            body["concurrencyKey"] = concurrency_key
        if machine is not None:
            body["machine"] = machine
        if version is not None:
            body["version"] = version
        if region is not None:
            body["region"] = region
        if delay is not None:
            body["delay"] = delay
        if ttl is not None:
            body["ttl"] = ttl
        if idempotency_key is not None:
            body["idempotencyKey"] = idempotency_key
        if idempotency_key_ttl is not None:
            body["idempotencyKeyTTL"] = idempotency_key_ttl
        if max_attempts is not None:
            body["maxAttempts"] = max_attempts
        if max_duration is not None:
            body["maxDuration"] = max_duration
        if priority is not None:
            body["priority"] = priority
        return self._request(
            "POST",
            f"/api/v1/runs/{run_id}/replay",
            cast_to=ReplayRunResponse,
            body=body or None,
        )

    def cancel(self, run_id: str) -> CancelRunResponse:
        return self._request(
            "POST",
            f"/api/v2/runs/{run_id}/cancel",
            cast_to=CancelRunResponse,
        )

    def reschedule(
        self,
        run_id: str,
        *,
        delay: str | datetime,
    ) -> RetrieveRunResponse:
        delay_val: str = delay.isoformat() if isinstance(delay, datetime) else delay
        return self._request(
            "POST",
            f"/api/v1/runs/{run_id}/reschedule",
            cast_to=RetrieveRunResponse,
            body={"delay": delay_val},
        )

    def update_metadata(
        self,
        run_id: str,
        *,
        metadata: dict[str, Any],
    ) -> UpdateMetadataResponse:
        return self._request(
            "PUT",
            f"/api/v1/runs/{run_id}/metadata",
            cast_to=UpdateMetadataResponse,
            body={"metadata": metadata},
        )

    def add_tags(
        self,
        run_id: str,
        *,
        tags: _List[str] | str,
    ) -> AddTagsResponse:
        tag_list = [tags] if isinstance(tags, str) else tags
        return self._request(
            "POST",
            f"/api/v1/runs/{run_id}/tags",
            cast_to=AddTagsResponse,
            body={"tags": tag_list},
        )
