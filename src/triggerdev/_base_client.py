"""Base HTTP client for Trigger.dev API."""

from __future__ import annotations

import os
from typing import Any, TypeVar, cast, overload

import httpx
from pydantic import BaseModel

from triggerdev._exceptions import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ContentTooLargeError,
    HTTPNotImplementedError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServiceUnavailableError,
    TriggerDevError,
    UnprocessableEntityError,
)

DEFAULT_BASE_URL = "https://api.trigger.dev"
DEFAULT_TIMEOUT = httpx.Timeout(60.0)
DEFAULT_MAX_RETRIES = 0

_ModelT = TypeVar("_ModelT", bound=BaseModel)


class _SentinelType:
    pass


RAW = _SentinelType()


class BaseClient:
    """Shared HTTP client logic for the Trigger.dev API."""

    api_key: str
    base_url: str
    timeout: httpx.Timeout
    max_retries: int

    _client: httpx.Client
    _owns_client: bool

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
        resolved_key = api_key or os.environ.get("TRIGGER_SECRET_KEY")
        if not resolved_key:
            raise TriggerDevError(
                "The API key must be provided as the `api_key` argument or the TRIGGER_SECRET_KEY environment variable."
            )
        self.api_key = resolved_key

        resolved_url = base_url or os.environ.get("TRIGGER_DEV_BASE_URL", DEFAULT_BASE_URL)
        self.base_url = resolved_url.rstrip("/")

        if timeout is None:
            self.timeout = DEFAULT_TIMEOUT
        elif isinstance(timeout, (int, float)):
            self.timeout = httpx.Timeout(float(timeout))
        else:
            self.timeout = timeout

        self.max_retries = max_retries if max_retries is not None else DEFAULT_MAX_RETRIES

        self._default_headers = default_headers or {}

        if http_client is not None:
            self._client = http_client
            self._owns_client = False
        else:
            self._client = httpx.Client(timeout=self.timeout)
            self._owns_client = True

    @overload
    def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[_ModelT],
        body: dict[str, Any] | None = ...,
        params: dict[str, Any] | None = ...,
        auth_required: bool = ...,
    ) -> _ModelT: ...

    @overload
    def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: None,
        body: dict[str, Any] | None = ...,
        params: dict[str, Any] | None = ...,
        auth_required: bool = ...,
    ) -> None: ...

    @overload
    def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: _SentinelType,
        body: dict[str, Any] | None = ...,
        params: dict[str, Any] | None = ...,
        auth_required: bool = ...,
    ) -> dict[str, Any]: ...

    def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[_ModelT] | _SentinelType | None = None,
        body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        auth_required: bool = True,
    ) -> _ModelT | dict[str, Any] | None:
        url = f"{self.base_url}{path}"

        headers: dict[str, str] = {
            "accept": "application/json",
            **self._default_headers,
        }
        if auth_required:
            headers["authorization"] = f"Bearer {self.api_key}"
        if body is not None:
            headers["content-type"] = "application/json"

        try:
            response = self._client.request(
                method,
                url,
                json=body,
                params=params,
                headers=headers,
            )
        except httpx.TimeoutException as exc:
            raise APITimeoutError(request=httpx.Request(method, url)) from exc
        except httpx.TransportError as exc:
            raise APIConnectionError(request=httpx.Request(method, url)) from exc

        if not response.is_success:
            raise self._make_status_error(response)

        if cast_to is None:
            return None

        data: dict[str, Any] = response.json()

        if isinstance(cast_to, _SentinelType):
            return data

        return cast_to.model_validate(data)

    @staticmethod
    def _make_status_error(response: httpx.Response) -> APIStatusError:
        body: dict[str, Any] | None
        try:
            raw: object = response.json()
            body = cast("dict[str, Any]", raw) if isinstance(raw, dict) else None
        except Exception:
            body = None

        if body is not None:
            message = str(body.get("error", response.reason_phrase))
        else:
            message = response.reason_phrase or f"HTTP {response.status_code}"

        status_to_exc: dict[int, type[APIStatusError]] = {
            400: BadRequestError,
            401: AuthenticationError,
            403: PermissionDeniedError,
            404: NotFoundError,
            409: ConflictError,
            413: ContentTooLargeError,
            422: UnprocessableEntityError,
            429: RateLimitError,
            500: InternalServerError,
            501: HTTPNotImplementedError,
            503: ServiceUnavailableError,
        }

        exc_cls = status_to_exc.get(response.status_code, APIStatusError)
        return exc_cls(message, response=response, body=body)

    @property
    def is_closed(self) -> bool:
        return self._client.is_closed

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> BaseClient:
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()


class SyncAPIResource:
    """Base for sync resource classes."""

    _client: BaseClient

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    @overload
    def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[_ModelT],
        body: dict[str, Any] | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> _ModelT: ...

    @overload
    def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: None,
        body: dict[str, Any] | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    @overload
    def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: _SentinelType,
        body: dict[str, Any] | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> dict[str, Any]: ...

    def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[_ModelT] | _SentinelType | None = None,
        body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> _ModelT | dict[str, Any] | None:
        return self._client._request(  # pyright: ignore[reportPrivateUsage]
            method,
            path,
            cast_to=cast_to,
            body=body,
            params=params,
        )
