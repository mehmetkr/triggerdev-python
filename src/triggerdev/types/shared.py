"""Shared types across Trigger.dev resources."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

RunTag = Annotated[str, Field(max_length=128)]
"""A single run tag, up to 128 characters."""

RunTags = RunTag | Annotated[list[RunTag], Field(max_length=10)]
"""One or more tags for a run, up to 10. Uniqueness is server-enforced."""

TTL = str | float
"""How long a run may wait in the queue before expiring."""

Delay = str
"""How long to wait before executing a task."""

Machine = Literal[
    "micro",
    "small-1x",
    "small-2x",
    "medium-1x",
    "medium-2x",
    "large-1x",
    "large-2x",
]
"""Compute size for a run."""

TriggerFunction = Literal[
    "trigger",
    "triggerAndWait",
    "batchTrigger",
    "batchTriggerAndWait",
]
"""How the run was triggered."""


class _ApiModel(BaseModel):
    """Base for all Trigger.dev API models."""

    model_config = ConfigDict(populate_by_name=True)


class QueueOptions(_ApiModel):
    """Queue settings for a triggered task."""

    name: str | None = Field(
        default=None,
        description="You can define a shared queue and then pass the name in to your task.",
    )
    concurrency_limit: int | None = Field(
        default=None,
        ge=0,
        le=1000,
        alias="concurrencyLimit",
        description="Maximum number of concurrent run executions.",
    )


class SerializedError(_ApiModel):
    """An error captured during a run attempt."""

    message: str = Field(..., examples=["Something went wrong"])
    name: str | None = Field(default=None, examples=["Error"])
    stack_trace: str | None = Field(
        default=None,
        alias="stackTrace",
        examples=["Error: Something went wrong"],
    )


class ErrorResponse(_ApiModel):
    """A simple error response."""

    error: str = Field(..., examples=["Something went wrong"])


class ErrorDetail(_ApiModel):
    """One item in a structured error response."""

    code: str = Field(..., description="The error code", examples=["custom"])
    message: str = Field(
        ...,
        description="The error message",
        examples=["Invalid status values: FOOBAR"],
    )
    path: list[str] | None = Field(
        default=None,
        description="The relevant path in the request",
        examples=[["filter[status]"]],
    )


class ErrorWithDetailsResponse(_ApiModel):
    """An error response with structured details."""

    error: str = Field(..., examples=["Query Error"])
    details: list[ErrorDetail] | None = None


__all__ = [
    "TTL",
    "Delay",
    "ErrorDetail",
    "ErrorResponse",
    "ErrorWithDetailsResponse",
    "Machine",
    "QueueOptions",
    "RunTag",
    "RunTags",
    "SerializedError",
    "TriggerFunction",
    "_ApiModel",
]
