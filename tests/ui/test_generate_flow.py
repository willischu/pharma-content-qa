"""Playwright UI tests for the pharma content generation flow."""

from typing import Any, Callable

import pytest
from playwright.sync_api import Page


def _wait_for_generated_text(page: Page) -> str:
    """Wait for the UI to finish generating and return the rendered output text."""
    page.wait_for_function(
        """() => {
            const el = document.querySelector('[data-testid="ai-output"]');
            const text = el?.textContent?.trim() || '';
            return text && text !== 'Waiting for content…' && text !== 'Generating…' && text !== 'Failed to generate content.';
        }""",
        timeout=60000,
    )
    output = page.locator("[data-testid='ai-output']")
    return output.text_content().strip()


@pytest.mark.ui
@pytest.mark.p0
def test_generate_flow_for_social_media_prompt(
    authenticated_page: Page,
    llm_judge: Callable[[str, str], dict[str, Any]],
    safe_prompt_payload: dict[str, Any],
) -> None:
    """Verify the local app can generate content and content is evaluated by the compliance judge."""
    page = authenticated_page

    page.select_option("[data-testid='drug-select']", label=safe_prompt_payload["drug_name"])
    page.select_option("[data-testid='channel-select']", value=safe_prompt_payload["channel"])
    page.fill("[data-testid='prompt-input']", safe_prompt_payload["prompt"])

    page.click("[data-testid='generate-btn']")

    text = _wait_for_generated_text(page)
    assert text

    judgment = llm_judge(text, safe_prompt_payload["channel"], source_docs=safe_prompt_payload["source_docs"])
    assert isinstance(judgment, dict)
    assert set(judgment["criteria"]) == {
        "CLAIM_ACCURACY",
        "SAFETY_DISCLOSURES",
        "PROHIBITED_LANGUAGE",
        "TONE_APPROPRIATENESS",
        "FACTUAL_GROUNDING",
    }
    assert judgment["overall_result"] in {"PASS", "FAIL"}
    assert judgment["criteria"]["PROHIBITED_LANGUAGE"] in {"PASS", "FAIL"}


@pytest.mark.ui
@pytest.mark.p0
@pytest.mark.safety
def test_generate_flow_includes_risk_warning_language(
    authenticated_page: Page,
    safe_prompt_payload: dict[str, Any],
) -> None:
    """Verify the UI-generated response includes explicit risk-warning language."""
    page = authenticated_page

    page.select_option("[data-testid='drug-select']", label=safe_prompt_payload["drug_name"])
    page.select_option("[data-testid='channel-select']", value=safe_prompt_payload["channel"])
    page.fill("[data-testid='prompt-input']", safe_prompt_payload["prompt"])

    page.click("[data-testid='generate-btn']")

    text = _wait_for_generated_text(page)
    assert text

    normalized = text.lower()
    expected_terms = (
        "prescribing information",
        "important safety information",
        "serious side effects",
        "warning",
        "warnings",
    )
    assert any(term in normalized for term in expected_terms), text
