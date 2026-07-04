"""Shared pytest fixtures for the pharma content QA demo."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import httpx
import pytest
from playwright.sync_api import Page

from utils.compliance_judge import evaluate as evaluate_compliance


@pytest.fixture(scope="function")
def llm_judge() -> Callable[[str, str], dict[str, Any]]:
    """Return a thin wrapper around the compliance evaluation engine."""

    def _judge(generated_content: str, channel: str, source_docs: dict[str, Any] | None = None) -> dict[str, Any]:
        return evaluate_compliance(
            generated_content=generated_content,
            source_docs=source_docs or {},
            channel=channel,
        )

    return _judge


@pytest.fixture(scope="session")
def ai_client() -> httpx.Client:
    """Create an HTTPX client targeted at the local FastAPI app."""
    return httpx.Client(base_url="http://localhost:8000", timeout=10.0)


@pytest.fixture(scope="session")
def base_url() -> str:
    """Expose the local app base URL for tests."""
    return "http://localhost:8000"


@pytest.fixture(scope="session")
def golden_dataset() -> list[dict[str, Any]]:
    """Load all JSON fixtures from the fixtures directory, if present."""
    fixtures_dir = Path(__file__).resolve().parent.parent / "fixtures"
    if not fixtures_dir.exists():
        return []

    scenarios: list[dict[str, Any]] = []
    for fixture_path in sorted(fixtures_dir.glob("*.json")):
        with fixture_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, dict):
            scenarios.append(payload)
        elif isinstance(payload, list):
            scenarios.extend([item for item in payload if isinstance(item, dict)])

    return scenarios


@pytest.fixture(scope="function")
def authenticated_page(page: Page) -> Page:
    """Navigate the Playwright page to the local app and wait for the UI to be ready."""
    page.goto("http://localhost:8000/", wait_until="networkidle")
    page.wait_for_selector("[data-testid='generate-btn']")
    return page
