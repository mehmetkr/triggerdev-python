"""Trigger.dev sync client."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from triggerdev._base_client import BaseClient
from triggerdev.resources.runs import Runs
from triggerdev.resources.schedules import Schedules
from triggerdev.resources.tasks import Tasks

if TYPE_CHECKING:
    import httpx


class Client(BaseClient):
    """Sync client for the Trigger.dev management API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int | None = None,
        http_client: httpx.Client | None = None,
        default_headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
            default_headers=default_headers,
        )

    @cached_property
    def tasks(self) -> Tasks:
        return Tasks(self)

    @cached_property
    def runs(self) -> Runs:
        return Runs(self)

    @cached_property
    def schedules(self) -> Schedules:
        return Schedules(self)

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()
