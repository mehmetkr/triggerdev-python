"""Tests for the Trigger.dev exception hierarchy."""

from __future__ import annotations

import httpx
import pytest

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


def _make_request() -> httpx.Request:
    return httpx.Request("GET", "https://api.trigger.dev/api/v1/runs")


def _make_response(status_code: int, headers: dict[str, str] | None = None) -> httpx.Response:
    return httpx.Response(
        status_code,
        request=_make_request(),
        headers=headers or {},
    )


class TestHierarchy:
    def test_root_is_exception(self) -> None:
        assert issubclass(TriggerDevError, Exception)

    def test_api_error_is_triggerdev_error(self) -> None:
        assert issubclass(APIError, TriggerDevError)

    def test_status_error_is_api_error(self) -> None:
        assert issubclass(APIStatusError, APIError)

    def test_connection_error_is_api_error(self) -> None:
        assert issubclass(APIConnectionError, APIError)

    def test_timeout_error_is_connection_error(self) -> None:
        assert issubclass(APITimeoutError, APIConnectionError)

    def test_5xx_subclasses(self) -> None:
        assert issubclass(HTTPNotImplementedError, InternalServerError)
        assert issubclass(ServiceUnavailableError, InternalServerError)

    @pytest.mark.parametrize(
        ("cls", "expected"),
        [
            (BadRequestError, 400),
            (AuthenticationError, 401),
            (PermissionDeniedError, 403),
            (NotFoundError, 404),
            (ConflictError, 409),
            (ContentTooLargeError, 413),
            (UnprocessableEntityError, 422),
            (RateLimitError, 429),
            (InternalServerError, 500),
            (HTTPNotImplementedError, 501),
            (ServiceUnavailableError, 503),
        ],
    )
    def test_status_code_pinning(self, cls: type[APIStatusError], expected: int) -> None:
        resp = _make_response(expected)
        err = cls("test", response=resp, body=None)
        assert err.status_code == expected


class TestAttributes:
    def test_triggerdev_error_message(self) -> None:
        err = TriggerDevError("boom")
        assert err.message == "boom"
        assert str(err) == "boom"

    def test_api_error_attributes(self) -> None:
        req = _make_request()
        err = APIError("boom", request=req, body={"error": "boom"})
        assert err.message == "boom"
        assert err.request is req
        assert err.body == {"error": "boom"}

    def test_status_error_attributes(self) -> None:
        resp = _make_response(404)
        err = NotFoundError("not found", response=resp, body={"error": "not found"})
        assert err.response is resp
        assert err.status_code == 404
        assert err.request is resp.request
        assert err.body == {"error": "not found"}

    def test_status_error_str(self) -> None:
        resp = _make_response(401)
        err = AuthenticationError("Unauthorized", response=resp, body=None)
        assert str(err) == "401 Unauthorized"

    def test_connection_error_attributes(self) -> None:
        req = _make_request()
        err = APIConnectionError(request=req)
        assert err.request is req
        assert err.body is None
        assert err.message == "Connection error."

    def test_timeout_error_attributes(self) -> None:
        req = _make_request()
        err = APITimeoutError(request=req)
        assert err.request is req
        assert err.message == "Request timed out."


class TestRetryAfter:
    def test_retry_after_present(self) -> None:
        resp = _make_response(429, headers={"retry-after": "30"})
        err = RateLimitError("rate limited", response=resp, body=None)
        assert err.retry_after == 30.0

    def test_retry_after_float(self) -> None:
        resp = _make_response(429, headers={"retry-after": "1.5"})
        err = RateLimitError("rate limited", response=resp, body=None)
        assert err.retry_after == 1.5

    def test_retry_after_absent(self) -> None:
        resp = _make_response(429)
        err = RateLimitError("rate limited", response=resp, body=None)
        assert err.retry_after is None

    def test_retry_after_non_numeric(self) -> None:
        resp = _make_response(429, headers={"retry-after": "Wed, 21 Oct 2015 07:28:00 GMT"})
        err = RateLimitError("rate limited", response=resp, body=None)
        assert err.retry_after is None


class TestPublicReExports:
    def test_all_exceptions_importable_from_package(self) -> None:
        import triggerdev

        for name in [
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
        ]:
            assert hasattr(triggerdev, name), f"{name} not exported from triggerdev"


class TestCatchPatterns:
    def test_catch_all_with_root(self) -> None:
        resp = _make_response(500)
        err = InternalServerError("fail", response=resp, body=None)
        with pytest.raises(TriggerDevError):
            raise err

    def test_catch_status_errors(self) -> None:
        resp = _make_response(404)
        err = NotFoundError("missing", response=resp, body=None)
        with pytest.raises(APIStatusError):
            raise err

    def test_catch_connection_errors(self) -> None:
        req = _make_request()
        err = APITimeoutError(request=req)
        with pytest.raises(APIConnectionError):
            raise err

    def test_catch_5xx_with_internal_server_error(self) -> None:
        resp = _make_response(503)
        err = ServiceUnavailableError("unavailable", response=resp, body=None)
        with pytest.raises(InternalServerError):
            raise err
