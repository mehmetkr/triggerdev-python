"""Task trigger and batch trigger types."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from triggerdev.types.shared import (
    TTL,
    Delay,
    Machine,
    QueueOptions,
    RunTags,
    _ApiModel,
)


class TriggerTaskOptions(_ApiModel):
    """Execution options when triggering a task."""

    queue: QueueOptions | None = None
    concurrency_key: str | None = Field(
        default=None,
        alias="concurrencyKey",
        description="Scope the concurrency limit to a specific key.",
    )
    idempotency_key: str | None = Field(
        default=None,
        alias="idempotencyKey",
        description=(
            "An optional property that specifies the idempotency key used to prevent "
            "creating duplicate runs. If you provide an existing idempotency key, we "
            "will return the existing run ID."
        ),
    )
    ttl: TTL | None = None
    delay: Delay | None = None
    tags: RunTags | None = Field(
        default=None,
        description="Tags to attach to the run. Up to 10 tags, each less than 128 characters.",
    )
    machine: Machine | None = Field(
        default=None,
        description="The machine preset to use for this run.",
        examples=["small-2x"],
    )


class TriggerTaskRequestBody(_ApiModel):
    """Payload and options for triggering a task."""

    payload: Any | None = Field(
        default=None,
        description="The payload can include any valid JSON.",
    )
    context: Any | None = Field(
        default=None,
        description="The context can include any valid JSON.",
    )
    options: TriggerTaskOptions | None = None


class TriggerTaskResponse(_ApiModel):
    """The run ID returned after triggering a task."""

    id: str | None = Field(
        default=None,
        description="The ID of the run that was triggered.",
        examples=["run_1234"],
    )


class BatchTriggerTaskRequestBodyItem(TriggerTaskRequestBody):
    """One task in a multi-task batch trigger."""

    task: str = Field(
        ...,
        description="The task identifier to trigger. This is the ``id`` set in your ``task()`` functions.",
    )


class BatchTriggerV2RequestBody(_ApiModel):
    """A batch of tasks to trigger together."""

    items: list[BatchTriggerTaskRequestBodyItem] = Field(
        ...,
        description="An array of payloads to trigger the tasks with.",
    )


class BatchTriggerTaskResponse(_ApiModel):
    """The batch ID and run IDs returned after a batch trigger."""

    batch_id: str = Field(
        ...,
        alias="batchId",
        description="The ID of the batch that was triggered.",
        examples=["batch_1234"],
    )
    runs: list[str] = Field(
        ...,
        description="An array of run IDs that were triggered.",
    )


__all__ = [
    "BatchTriggerTaskRequestBodyItem",
    "BatchTriggerTaskResponse",
    "BatchTriggerV2RequestBody",
    "TriggerTaskOptions",
    "TriggerTaskRequestBody",
    "TriggerTaskResponse",
]
