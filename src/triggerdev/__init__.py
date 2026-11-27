"""The first fully typed Python SDK for the Trigger.dev management API."""

from triggerdev._client import Client
from triggerdev._exceptions import (
    APIConnectionError,
    APIError,
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
from triggerdev._version import __version__

__all__ = [
    "APIConnectionError",
    "APIError",
    "APIStatusError",
    "APITimeoutError",
    "AuthenticationError",
    "BadRequestError",
    "Client",
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
    "__version__",
]
