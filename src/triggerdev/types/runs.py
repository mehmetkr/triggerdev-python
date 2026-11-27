"""Run lifecycle and retrieval types."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import AwareDatetime, Field

from triggerdev.types.shared import TTL, SerializedError, TriggerFunction, _ApiModel

RunStatus = Literal[
    "PENDING_VERSION",
    "DELAYED",
    "QUEUED",
    "EXECUTING",
    "REATTEMPTING",
    "FROZEN",
    "COMPLETED",
    "CANCELED",
    "FAILED",
    "CRASHED",
    "INTERRUPTED",
    "SYSTEM_FAILURE",
]
"""Possible states of a run."""

ListRunStatus = Literal[
    "PENDING_VERSION",
    "QUEUED",
    "EXECUTING",
    "REATTEMPTING",
    "FROZEN",
    "COMPLETED",
    "CANCELED",
    "FAILED",
    "CRASHED",
    "INTERRUPTED",
    "SYSTEM_FAILURE",
]
"""Run states returned in listings."""

AttemptStatus = Literal[
    "PENDING",
    "EXECUTING",
    "PAUSED",
    "COMPLETED",
    "FAILED",
    "CANCELED",
]
"""Possible states of an attempt."""


class RunEnvironment(_ApiModel):
    """The environment a run belongs to."""

    id: str = Field(
        ...,
        description="The unique ID of the environment.",
        examples=["cl1234"],
    )
    name: str = Field(
        ...,
        description="The name of the environment.",
        examples=["dev"],
    )
    user: str | None = Field(
        default=None,
        description="If this is a dev environment, the username of the user.",
        examples=["Anna"],
    )


class ListRunItem(_ApiModel):
    """A run summary in a list."""

    id: str = Field(
        ...,
        description="The unique ID of the run, prefixed with ``run_``.",
        examples=["run_1234"],
    )
    status: ListRunStatus = Field(..., description="The status of the run.")
    task_identifier: str = Field(
        ...,
        alias="taskIdentifier",
        description="The identifier of the task that was run.",
        examples=["my-task"],
    )
    version: str | None = Field(
        default=None,
        description="The version of the worker that executed the run.",
        examples=["20240523.1"],
    )
    env: RunEnvironment = Field(..., description="The environment of the run.")
    idempotency_key: str | None = Field(
        default=None,
        alias="idempotencyKey",
        description="The idempotency key used to prevent creating duplicate runs, if provided.",
        examples=["idempotency_key_1234"],
    )
    is_test: bool = Field(
        ...,
        alias="isTest",
        description="Whether the run is a test run or not.",
        examples=[False],
    )
    created_at: AwareDatetime = Field(..., alias="createdAt")
    updated_at: AwareDatetime = Field(..., alias="updatedAt")
    started_at: AwareDatetime | None = Field(
        default=None,
        alias="startedAt",
        description="The time the run started.",
    )
    finished_at: AwareDatetime | None = Field(
        default=None,
        alias="finishedAt",
        description="The time the run finished.",
    )
    delayed_until: AwareDatetime | None = Field(
        default=None,
        alias="delayedUntil",
        description="If triggered with a delay, the time the run will be enqueued.",
    )
    ttl: TTL | None = None
    expired_at: AwareDatetime | None = Field(
        default=None,
        alias="expiredAt",
        description="If the run had a TTL and that time has passed, when the run expired.",
    )
    tags: list[str] | None = Field(
        default=None,
        description="Tags attached to the run.",
        examples=[["user_5df987al13", "org_c6b7dycmxw"]],
    )
    cost_in_cents: float | None = Field(
        default=None,
        alias="costInCents",
        description="The compute cost of the run (so far) in cents.",
        examples=[0.00292],
    )
    base_cost_in_cents: float | None = Field(
        default=None,
        alias="baseCostInCents",
        description="The invocation cost of the run in cents.",
        examples=[0.0025],
    )
    duration_ms: float | None = Field(
        default=None,
        alias="durationMs",
        description="The duration of compute (so far) in milliseconds, excluding waits.",
        examples=[491],
    )


class CommonRunObject(_ApiModel):
    """Core fields shared by all detailed run views."""

    id: str = Field(
        ...,
        description="The unique ID of the run, prefixed with ``run_``.",
        examples=["run_1234"],
    )
    status: RunStatus = Field(..., description="The status of the run.")
    task_identifier: str = Field(
        ...,
        alias="taskIdentifier",
        description="The identifier of the task that was run.",
        examples=["my-task"],
    )
    version: str | None = Field(
        default=None,
        description="The version of the worker that executed the run.",
        examples=["20240523.1"],
    )
    idempotency_key: str | None = Field(
        default=None,
        alias="idempotencyKey",
        description="The idempotency key used to prevent creating duplicate runs.",
        examples=["idempotency_key_1234"],
    )
    created_at: AwareDatetime = Field(..., alias="createdAt")
    updated_at: AwareDatetime = Field(..., alias="updatedAt")
    is_test: bool | None = Field(
        default=None,
        alias="isTest",
        description="Whether the run is a test run.",
        examples=[False],
    )
    started_at: AwareDatetime | None = Field(
        default=None,
        alias="startedAt",
        description="The time the run started.",
    )
    finished_at: AwareDatetime | None = Field(
        default=None,
        alias="finishedAt",
        description="The time the run finished.",
    )
    delayed_until: AwareDatetime | None = Field(
        default=None,
        alias="delayedUntil",
        description="If triggered with a delay, the time the run will be enqueued.",
    )
    ttl: TTL | None = None
    expired_at: AwareDatetime | None = Field(
        default=None,
        alias="expiredAt",
        description="If the run had a TTL and that time has passed, when the run expired.",
    )
    tags: list[str] | None = Field(
        default=None,
        description="Tags attached to the run.",
        examples=[["user_5df987al13", "org_c6b7dycmxw"]],
    )
    metadata: dict[str, Any] | None = Field(
        default=None,
        description="The metadata of the run.",
        examples=[{"foo": "bar"}],
    )
    cost_in_cents: float | None = Field(
        default=None,
        alias="costInCents",
        description="The compute cost of the run (so far) in cents.",
        examples=[0.00292],
    )
    base_cost_in_cents: float | None = Field(
        default=None,
        alias="baseCostInCents",
        description="The invocation cost of the run in cents.",
        examples=[0.0025],
    )
    duration_ms: float | None = Field(
        default=None,
        alias="durationMs",
        description="The duration of compute (so far) in milliseconds, excluding waits.",
        examples=[491],
    )
    depth: int | None = Field(
        default=None,
        description="The depth of the run in the task run hierarchy. The root run has a depth of 0.",
        examples=[0],
    )
    batch_id: str | None = Field(
        default=None,
        alias="batchId",
        description="The ID of the batch that this run belongs to.",
        examples=["batch_1234"],
    )
    trigger_function: TriggerFunction | None = Field(
        default=None,
        alias="triggerFunction",
        description="The name of the function that triggered the run.",
    )


class RelatedRuns(_ApiModel):
    """Parent, root, and child runs in the hierarchy."""

    root: CommonRunObject | None = Field(
        default=None,
        description="The root run of the run hierarchy. Omitted if this run is the root.",
    )
    parent: CommonRunObject | None = Field(
        default=None,
        description="The parent run. Omitted if this run is the root.",
    )
    children: list[CommonRunObject] | None = Field(
        default=None,
        description="The immediate children of the run. Omitted if the run has no children.",
    )


class RunSchedule(_ApiModel):
    """The schedule that triggered a run."""

    id: str = Field(
        ...,
        description="The unique ID of the schedule, prefixed with ``sched_``.",
        examples=["sched_1234"],
    )
    external_id: str | None = Field(
        default=None,
        alias="externalId",
        description="The external ID of the schedule.",
        examples=["user_1234"],
    )
    deduplication_key: str | None = Field(
        default=None,
        alias="deduplicationKey",
        description="The deduplication key used to prevent creating duplicate schedules.",
        examples=["dedup_key_1234"],
    )
    generator: RunScheduleGenerator


class RunScheduleGenerator(_ApiModel):
    """Cron generator for a run's schedule."""

    type: Literal["CRON"] | None = None
    expression: str | None = Field(
        default=None,
        description="The cron expression.",
        examples=["0 0 * * *"],
    )
    description: str | None = Field(
        default=None,
        description="The description of the generator in plain English.",
        examples=["Every day at midnight"],
    )


class Attempt(_ApiModel):
    """One execution attempt of a run."""

    id: str = Field(
        ...,
        description="The unique ID of the attempt, prefixed with ``attempt_``.",
        examples=["attempt_1234"],
    )
    status: AttemptStatus
    error: SerializedError | None = None
    created_at: AwareDatetime = Field(..., alias="createdAt")
    updated_at: AwareDatetime = Field(..., alias="updatedAt")
    started_at: AwareDatetime | None = Field(default=None, alias="startedAt")
    completed_at: AwareDatetime | None = Field(default=None, alias="completedAt")


class RetrieveRunResponse(CommonRunObject):
    """Complete run detail with payload, output, and attempts."""

    payload: dict[str, Any] | None = Field(
        default=None,
        description="The payload sent to the task. Omitted with Public API keys.",
        examples=[{"foo": "bar"}],
    )
    payload_presigned_url: str | None = Field(
        default=None,
        alias="payloadPresignedUrl",
        description="Presigned URL to download the payload when it is too large. Expires in 5 minutes.",
    )
    output: dict[str, Any] | None = Field(
        default=None,
        description="The output of the run. Omitted with Public API keys.",
        examples=[{"foo": "bar"}],
    )
    output_presigned_url: str | None = Field(
        default=None,
        alias="outputPresignedUrl",
        description="Presigned URL to download the output when it is too large. Expires in 5 minutes.",
    )
    related_runs: RelatedRuns | None = Field(default=None, alias="relatedRuns")
    schedule: RunSchedule | None = Field(
        default=None,
        description="The schedule that triggered the run. Omitted if not schedule-triggered.",
    )
    attempts: list[Attempt]


class RunsPagination(_ApiModel):
    """Page cursors for run listings."""

    next: str | None = Field(
        default=None,
        description="The run ID to start the next page after.",
        examples=["run_1234"],
    )
    previous: str | None = Field(
        default=None,
        description="The run ID to start the previous page before.",
        examples=["run_5678"],
    )


class RunsAppliedCreatedAtFilter(_ApiModel):
    """Time window applied to a run listing."""

    period: str | None = Field(
        default=None,
        description="The period, when the list used one.",
        examples=["7d"],
    )
    from_: AwareDatetime | None = Field(
        default=None,
        alias="from",
        description="Start of the window.",
    )
    to: AwareDatetime | None = Field(
        default=None,
        description="End of the window.",
    )
    is_default: bool | None = Field(
        default=None,
        alias="isDefault",
        description="True when the default 7-day period applied.",
    )


class RunsAppliedFilters(_ApiModel):
    """Filters applied to a run listing, including defaults."""

    created_at: RunsAppliedCreatedAtFilter | None = Field(
        default=None,
        alias="createdAt",
        description="The creation-time window the list used.",
    )


class ListRunsResult(_ApiModel):
    """A page of runs with applied filters."""

    data: list[ListRunItem] | None = None
    pagination: RunsPagination | None = None
    applied_filters: RunsAppliedFilters | None = Field(
        default=None,
        alias="appliedFilters",
        description="The filters the list was run with, including defaults.",
    )


class RescheduleRunRequestBody(_ApiModel):
    """New delay or timestamp for rescheduling a run."""

    delay: str | AwareDatetime | None = None


class RunResultUsage(_ApiModel):
    """Execution usage stats for a completed run."""

    duration_ms: float | None = Field(
        default=None,
        alias="durationMs",
        description="Duration of the run in milliseconds.",
    )


class RunResultResponse(_ApiModel):
    """The execution result of a completed run."""

    ok: bool
    id: str
    output: str | None = Field(
        default=None,
        description="Serialized output string (present when ok is true).",
    )
    output_type: str | None = Field(
        default=None,
        alias="outputType",
        description="Content type of the serialized output.",
    )
    error: dict[str, Any] | None = Field(
        default=None,
        description="Error details (present when ok is false).",
    )
    usage: RunResultUsage | None = None
    task_identifier: str | None = Field(
        default=None,
        alias="taskIdentifier",
    )


class ReplayRunResponse(_ApiModel):
    """The new run ID returned after replaying a run."""

    id: str


class CancelRunResponse(_ApiModel):
    """The run ID returned after canceling a run."""

    id: str


class UpdateMetadataResponse(_ApiModel):
    """The updated metadata of a run."""

    metadata: dict[str, Any]


class AddTagsResponse(_ApiModel):
    """Confirmation message after adding tags."""

    message: str


RunSchedule.model_rebuild()


__all__ = [
    "AddTagsResponse",
    "Attempt",
    "AttemptStatus",
    "CancelRunResponse",
    "CommonRunObject",
    "ListRunItem",
    "ListRunStatus",
    "ListRunsResult",
    "RelatedRuns",
    "ReplayRunResponse",
    "RescheduleRunRequestBody",
    "RetrieveRunResponse",
    "RunEnvironment",
    "RunResultResponse",
    "RunResultUsage",
    "RunSchedule",
    "RunScheduleGenerator",
    "RunStatus",
    "RunsAppliedCreatedAtFilter",
    "RunsAppliedFilters",
    "RunsPagination",
    "UpdateMetadataResponse",
]
