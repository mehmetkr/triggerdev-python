"""Shared test fixtures."""

from __future__ import annotations

import httpx
import pytest
import respx

from triggerdev import Client


@pytest.fixture()
def base_url() -> str:
    return "https://api.trigger.dev"


@pytest.fixture()
def api_key() -> str:
    return "tr_dev_sk_test_1234"


@pytest.fixture()
def respx_mock() -> respx.MockRouter:
    with respx.mock(assert_all_called=False) as router:
        yield router


@pytest.fixture()
def client(api_key: str, base_url: str) -> Client:
    return Client(api_key=api_key, base_url=base_url)


@pytest.fixture()
def mock_response() -> httpx.Response:
    return httpx.Response(200, json={"id": "run_1234"})
