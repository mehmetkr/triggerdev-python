"""Schedule management types."""

from __future__ import annotations

from typing import Literal

from pydantic import AwareDatetime, Field

from triggerdev.types.shared import _ApiModel


class ScheduleGenerator(_ApiModel):
    """Cron generator for a schedule."""

    type: Literal["CRON"] | None = None
    expression: str | None = Field(
        default=None,
        description="The cron expression used to generate the schedule.",
        examples=["0 0 * * *"],
    )
    description: str | None = Field(
        default=None,
        description="The description of the generator in plain English.",
        examples=["Every day at midnight"],
    )


class AppliedSchedulePolicy(_ApiModel):
    """Plan-enforced limits on a schedule."""

    minimum_window_seconds: float | None = Field(
        default=None,
        alias="minimumWindowSeconds",
        description="The minimum window, in seconds, applied on top of the configured window.",
        examples=[3600],
    )
    reason: Literal["free_schedule"] | None = Field(
        default=None,
        description="Why the minimum window is applied.",
    )


class ScheduleEnvironment(_ApiModel):
    """An environment linked to a schedule."""

    id: str | None = None
    type: str | None = None
    user_name: str | None = Field(default=None, alias="userName")


class ScheduleObject(_ApiModel):
    """A complete schedule with its configuration."""

    id: str | None = Field(
        default=None,
        description="The unique ID of the schedule, prefixed with ``sched_``.",
        examples=["sched_1234"],
    )
    task: str | None = Field(
        default=None,
        description="The id of the scheduled task that will be triggered by this schedule.",
        examples=["my-scheduled-task"],
    )
    type: str | None = Field(
        default=None,
        description=(
            "The type of schedule: ``DECLARATIVE`` (set via ``cron`` property in code) "
            "or ``IMPERATIVE`` (created via dashboard or ``schedules.create()``)."
        ),
        examples=["IMPERATIVE"],
    )
    active: bool | None = Field(
        default=None,
        description="Whether the schedule is active or not.",
        examples=[True],
    )
    deduplication_key: str | None = Field(
        default=None,
        alias="deduplicationKey",
        description="The deduplication key used to prevent creating duplicate schedules.",
        examples=["dedup_key_1234"],
    )
    external_id: str | None = Field(
        default=None,
        alias="externalId",
        description="The external ID of the schedule.",
        examples=["user_1234"],
    )
    generator: ScheduleGenerator | None = None
    timezone: str | None = Field(
        default=None,
        description="IANA timezone. Defaults to UTC.",
        examples=["America/New_York"],
    )
    next_run: AwareDatetime | None = Field(
        default=None,
        alias="nextRun",
        description="The next time the schedule will run.",
        examples=["2024-04-01T00:00:00Z"],
    )
    applied_schedule_policy: AppliedSchedulePolicy | None = Field(
        default=None,
        alias="appliedSchedulePolicy",
        description="Present only when a plan policy applies a minimum window to this schedule.",
    )
    environments: list[ScheduleEnvironment] | None = None


class SchedulesPagination(_ApiModel):
    """Page cursors for schedule listings."""

    current_page: int | None = Field(default=None, alias="currentPage")
    total_pages: int | None = Field(default=None, alias="totalPages")
    count: int | None = None


class ListSchedulesResult(_ApiModel):
    """A page of schedules."""

    data: list[ScheduleObject] | None = None
    pagination: SchedulesPagination | None = None


class CreateScheduleOptions(_ApiModel):
    """Options for creating a schedule."""

    task: str
    cron: str
    deduplication_key: str = Field(..., alias="deduplicationKey")
    external_id: str | None = Field(default=None, alias="externalId")
    timezone: str | None = Field(
        default=None,
        description="IANA timezone. Defaults to UTC.",
        examples=["America/New_York"],
    )


class UpdateScheduleOptions(_ApiModel):
    """Options for updating a schedule."""

    task: str
    cron: str
    external_id: str | None = Field(default=None, alias="externalId")
    timezone: str | None = Field(
        default=None,
        description="IANA timezone. Defaults to UTC.",
        examples=["America/New_York"],
    )


class GetTimezonesResult(_ApiModel):
    """Available timezones for scheduling."""

    timezones: list[str] | None = None


__all__ = [
    "AppliedSchedulePolicy",
    "CreateScheduleOptions",
    "GetTimezonesResult",
    "ListSchedulesResult",
    "ScheduleEnvironment",
    "ScheduleGenerator",
    "ScheduleObject",
    "SchedulesPagination",
    "UpdateScheduleOptions",
]
