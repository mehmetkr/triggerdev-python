"""Trigger.dev SDK exceptions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import httpx


class TriggerDevError(Exception):
    """Base for all Trigger.dev SDK errors."""

    message: str

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class APIError(TriggerDevError):
    """An error from the Trigger.dev API."""

    request: httpx.Request
    body: object | None

    def __init__(
        self,
        message: str,
        *,
        request: httpx.Request,
        body: object | None,
    ) -> None:
        super().__init__(message)
        self.request = request
        self.body = body


class APIStatusError(APIError):
    """An HTTP error response from the API."""

    response: httpx.Response
    status_code: int

    def __init__(
        self,
        message: str,
        *,
        response: httpx.Response,
        body: object | None,
    ) -> None:
        super().__init__(
            message,
            request=response.request,
            body=body,
        )
        self.response = response
        self.status_code = response.status_code

    def __str__(self) -> str:
        return f"{self.status_code} {self.message}"


class BadRequestError(APIStatusError):
    """The request was malformed or contained invalid parameters."""


class AuthenticationError(APIStatusError):
    """The API key is missing or invalid."""


class PermissionDeniedError(APIStatusError):
    """The API key lacks permission for this action."""


class NotFoundError(APIStatusError):
    """The requested resource does not exist."""


class ConflictError(APIStatusError):
    """The request conflicts with the current resource state."""


class ContentTooLargeError(APIStatusError):
    """The request payload exceeds the size limit."""


class UnprocessableEntityError(APIStatusError):
    """The request was well-formed but contained semantic errors."""


class RateLimitError(APIStatusError):
    """Too many requests or concurrent operations."""

    @property
    def retry_after(self) -> float | None:
        """Seconds to wait before retrying, or None if not specified."""
        header = self.response.headers.get("retry-after")
        if header is None:
            return None
        try:
            return float(header)
        except ValueError:
            return None


class InternalServerError(APIStatusError):
    """The API encountered an internal error."""


class HTTPNotImplementedError(InternalServerError):
    """The requested functionality is not yet available."""


class ServiceUnavailableError(InternalServerError):
    """The API is temporarily unavailable."""


class APIConnectionError(APIError):
    """Failed to connect to the API."""

    def __init__(self, *, request: httpx.Request) -> None:
        super().__init__(
            "Connection error.",
            request=request,
            body=None,
        )


class APITimeoutError(APIConnectionError):
    """The request timed out."""

    def __init__(self, *, request: httpx.Request) -> None:
        super().__init__(request=request)
        self.message = "Request timed out."


__all__ = [
    "APIConnectionError",
    "APIError",
    "APIStatusError",
    "APITimeoutError",
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "ContentTooLargeError",
    "HTTPNotImplementedError",
    "InternalServerError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServiceUnavailableError",
    "TriggerDevError",
    "UnprocessableEntityError",
]
