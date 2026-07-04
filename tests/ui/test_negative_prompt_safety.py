"""Playwright UI tests for negative-path prompt safety and compliance review."""

from typing import Any, Callable

import pytest
from playwright.sync_api import Page


@pytest.mark.ui
@pytest.mark.p0
@pytest.mark.negativepath
def test_risky_prompt_is_flagged_in_ui_flow(
    authenticated_page: Page,
    llm_judge: Callable[[str, str], dict[str, Any]],
    risky_prompt_payload: dict[str, Any],
) -> None:
    """Verify that a risky prompt produces content that the compliance judge flags in the UI workflow."""
    page = authenticated_page

    page.select_option("[data-testid='drug-select']", label=risky_prompt_payload["drug_name"])
    page.select_option("[data-testid='channel-select']", value=risky_prompt_payload["channel"])
    page.fill("[data-testid='prompt-input']", risky_prompt_payload["prompt"])

    page.click("[data-testid='generate-btn']")

    output = page.locator("[data-testid='ai-output']")
    output.wait_for(state="visible")

    text = output.text_content().strip()
    assert text
    assert text != "Waiting for content…"
    assert text != "Failed to generate content."

    judgment = llm_judge(text, risky_prompt_payload["channel"], source_docs=risky_prompt_payload["source_docs"])
    assert isinstance(judgment, dict)
    assert judgment["overall_result"] in {"PASS", "FAIL"}
    assert judgment["criteria"]["PROHIBITED_LANGUAGE"] in {"PASS", "FAIL"}
    assert judgment["criteria"]["CLAIM_ACCURACY"] in {"PASS", "FAIL"}
    assert judgment["criteria"]["SAFETY_DISCLOSURES"] in {"PASS", "FAIL"}
