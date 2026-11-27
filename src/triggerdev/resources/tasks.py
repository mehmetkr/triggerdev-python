"""Tasks resource client."""

from __future__ import annotations

from typing import Any

from triggerdev._base_client import SyncAPIResource
from triggerdev.types.tasks import (
    BatchTriggerTaskResponse,
    TriggerTaskResponse,
)


class Tasks(SyncAPIResource):
    """Methods for triggering and batch-triggering tasks."""

    def trigger(
        self,
        task_id: str,
        *,
        payload: object | None = None,
        context: object | None = None,
        options: dict[str, Any] | None = None,
    ) -> TriggerTaskResponse:
        body: dict[str, Any] = {}
        if payload is not None:
            body["payload"] = payload
        if context is not None:
            body["context"] = context
        if options is not None:
            body["options"] = options
        return self._request(
            "POST",
            f"/api/v1/tasks/{task_id}/trigger",
            cast_to=TriggerTaskResponse,
            body=body,
        )

    def batch_trigger(
        self,
        task_id: str,
        *,
        items: list[dict[str, Any]],
    ) -> BatchTriggerTaskResponse:
        return self._request(
            "POST",
            f"/api/v1/tasks/{task_id}/batch",
            cast_to=BatchTriggerTaskResponse,
            body={"items": items},
        )

    def batch_trigger_multi(
        self,
        *,
        items: list[dict[str, Any]],
    ) -> BatchTriggerTaskResponse:
        return self._request(
            "POST",
            "/api/v1/tasks/batch",
            cast_to=BatchTriggerTaskResponse,
            body={"items": items},
        )
