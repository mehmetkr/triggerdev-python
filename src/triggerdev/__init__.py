"""The first fully typed async Python SDK for the Trigger.dev management API."""

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
]

__version__ = "0.0.0"
