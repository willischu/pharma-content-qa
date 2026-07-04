"""Shared pytest fixtures for the pharma content QA demo."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable
from urllib.error import URLError
from urllib.request import urlopen

import httpx
import pytest
from playwright.sync_api import Page

from utils.compliance_judge import evaluate as evaluate_compliance


@pytest.fixture(scope="session")
def live_server() -> str:
    """Start the local FastAPI app for Playwright UI tests and shut it down afterward."""
    host = "127.0.0.1"
    port = 8000
    base_url = f"http://{host}:{port}"
    repo_root = Path(__file__).resolve().parent.parent

    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", host, "--port", str(port)],
        cwd=str(repo_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env={**os.environ, "PYTHONPATH": str(repo_root)},
    )

    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            with urlopen(f"{base_url}/health", timeout=1) as response:
                if response.status == 200:
                    break
        except (URLError, TimeoutError, ConnectionError):
            if process.poll() is not None:
                output = process.stdout.read() if process.stdout else ""
                raise RuntimeError(f"Uvicorn exited early: {output}") from None
            time.sleep(0.25)
    else:
        output = process.stdout.read() if process.stdout else ""
        raise RuntimeError(f"Timed out waiting for local app to start: {output}")

    try:
        yield base_url
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


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
def base_url(live_server: str) -> str:
    """Expose the local app base URL for tests."""
    return live_server


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
def authenticated_page(page: Page, base_url: str) -> Page:
    """Navigate the Playwright page to the local app and wait for the UI to be ready."""
    page.goto(f"{base_url}/", wait_until="networkidle")
    page.wait_for_selector("[data-testid='generate-btn']")
    return page
