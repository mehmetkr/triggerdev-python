"""Tests for the Client class and BaseClient."""

from __future__ import annotations

import os
from unittest.mock import patch

import httpx
import pytest
import respx

from triggerdev import Client
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


class TestClientConstructor:
    def test_api_key_from_param(self) -> None:
        client = Client(api_key="tr_dev_sk_test")
        assert client.api_key == "tr_dev_sk_test"

    def test_api_key_from_env(self) -> None:
        with patch.dict(os.environ, {"TRIGGER_SECRET_KEY": "tr_dev_sk_env"}):
            client = Client()
            assert client.api_key == "tr_dev_sk_env"

    def test_api_key_missing_raises(self) -> None:
        with patch.dict(os.environ, {}, clear=True), pytest.raises(TriggerDevError, match="API key"):
            Client()

    def test_param_overrides_env(self) -> None:
        with patch.dict(os.environ, {"TRIGGER_SECRET_KEY": "tr_dev_sk_env"}):
            client = Client(api_key="tr_dev_sk_param")
            assert client.api_key == "tr_dev_sk_param"

    def test_default_base_url(self) -> None:
        client = Client(api_key="tr_dev_sk_test")
        assert client.base_url == "https://api.trigger.dev"

    def test_custom_base_url(self) -> None:
        client = Client(api_key="tr_dev_sk_test", base_url="https://custom.example.com")
        assert client.base_url == "https://custom.example.com"

    def test_base_url_strips_trailing_slash(self) -> None:
        client = Client(api_key="tr_dev_sk_test", base_url="https://custom.example.com/")
        assert client.base_url == "https://custom.example.com"

    def test_default_timeout(self) -> None:
        client = Client(api_key="tr_dev_sk_test")
        assert client.timeout == httpx.Timeout(60.0)

    def test_custom_timeout_float(self) -> None:
        client = Client(api_key="tr_dev_sk_test", timeout=30.0)
        assert client.timeout == httpx.Timeout(30.0)

    def test_custom_timeout_object(self) -> None:
        t = httpx.Timeout(10.0, connect=5.0)
        client = Client(api_key="tr_dev_sk_test", timeout=t)
        assert client.timeout == t

    def test_resource_namespaces_exist(self) -> None:
        client = Client(api_key="tr_dev_sk_test")
        assert hasattr(client, "tasks")
        assert hasattr(client, "runs")
        assert hasattr(client, "schedules")


class TestClientContextManager:
    def test_context_manager(self) -> None:
        with Client(api_key="tr_dev_sk_test") as client:
            assert not client.is_closed
        assert client.is_closed

    def test_close(self) -> None:
        client = Client(api_key="tr_dev_sk_test")
        assert not client.is_closed
        client.close()
        assert client.is_closed

    def test_custom_http_client_not_closed(self) -> None:
        http_client = httpx.Client()
        client = Client(api_key="tr_dev_sk_test", http_client=http_client)
        client.close()
        assert not http_client.is_closed
        http_client.close()


class TestClientAuth:
    @respx.mock
    def test_auth_header_sent(self, client: Client) -> None:
        route = respx.get("https://api.trigger.dev/api/v1/timezones").mock(
            return_value=httpx.Response(200, json={"timezones": []})
        )
        client.schedules.timezones()
        assert route.called
        request = route.calls[0].request
        assert request.headers["authorization"] == "Bearer tr_dev_sk_test_1234"


class TestErrorMapping:
    @pytest.mark.parametrize(
        ("status", "exc_cls"),
        [
            (400, BadRequestError),
            (401, AuthenticationError),
            (403, PermissionDeniedError),
            (404, NotFoundError),
            (409, ConflictError),
            (413, ContentTooLargeError),
            (422, UnprocessableEntityError),
            (429, RateLimitError),
            (500, InternalServerError),
            (501, HTTPNotImplementedError),
            (503, ServiceUnavailableError),
        ],
    )
    @respx.mock
    def test_status_code_to_exception(self, client: Client, status: int, exc_cls: type) -> None:
        respx.get("https://api.trigger.dev/api/v3/runs/run_1234").mock(
            return_value=httpx.Response(status, json={"error": "test error"})
        )
        with pytest.raises(exc_cls):
            client.runs.retrieve("run_1234")

    @respx.mock
    def test_unknown_4xx_raises_api_status_error(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v3/runs/run_1234").mock(
            return_value=httpx.Response(418, json={"error": "I'm a teapot"})
        )
        with pytest.raises(APIStatusError) as exc_info:
            client.runs.retrieve("run_1234")
        assert exc_info.value.status_code == 418

    @respx.mock
    def test_error_body_parsed(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v3/runs/run_1234").mock(
            return_value=httpx.Response(404, json={"error": "Run not found"})
        )
        with pytest.raises(NotFoundError) as exc_info:
            client.runs.retrieve("run_1234")
        assert exc_info.value.body == {"error": "Run not found"}
        assert "Run not found" in str(exc_info.value)

    @respx.mock
    def test_non_json_error_body(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v3/runs/run_1234").mock(
            return_value=httpx.Response(
                502,
                content=b"<html>Bad Gateway</html>",
                headers={"content-type": "text/html"},
            )
        )
        with pytest.raises(APIStatusError) as exc_info:
            client.runs.retrieve("run_1234")
        assert exc_info.value.status_code == 502
        assert exc_info.value.body is None

    @respx.mock
    def test_connection_error(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v3/runs/run_1234").mock(
            side_effect=httpx.ConnectError("Connection refused")
        )
        with pytest.raises(APIConnectionError):
            client.runs.retrieve("run_1234")

    @respx.mock
    def test_timeout_error(self, client: Client) -> None:
        respx.get("https://api.trigger.dev/api/v3/runs/run_1234").mock(side_effect=httpx.ReadTimeout("Read timed out"))
        with pytest.raises(APITimeoutError):
            client.runs.retrieve("run_1234")


class TestPublicReExports:
    def test_client_importable_from_package(self) -> None:
        import triggerdev

        assert hasattr(triggerdev, "Client")
