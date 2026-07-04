"""LLM-as-judge evaluation engine for pharma content compliance."""

import json
import os
import re
from typing import Any

from anthropic import Anthropic

MODEL_NAME = "claude-haiku-4-5-20251001"


def build_rubric_prompt(generated_content: str, source_docs: dict[str, Any], channel: str) -> str:
    """Construct the compliance rubric prompt for the judge model."""
    return f"""
You are an expert compliance reviewer for pharmaceutical marketing content.
Evaluate the generated content against the following rubric.

Channel: {channel}
Source docs:
{json.dumps(source_docs, indent=2)}

Generated content:
{generated_content}

Rate each criterion as PASS or FAIL.
Criteria:
1. CLAIM_ACCURACY — are all efficacy claims supported by source material?
2. SAFETY_DISCLOSURES — are required disclosures present or referenced?
3. PROHIBITED_LANGUAGE — does content avoid all prohibited terms?
4. TONE_APPROPRIATENESS — appropriate for channel and regulated pharma?
5. FACTUAL_GROUNDING — does every fact trace to source material?

Return JSON only with this shape:
{{
  "criteria": {{
    "CLAIM_ACCURACY": "PASS|FAIL",
    "SAFETY_DISCLOSURES": "PASS|FAIL",
    "PROHIBITED_LANGUAGE": "PASS|FAIL",
    "TONE_APPROPRIATENESS": "PASS|FAIL",
    "FACTUAL_GROUNDING": "PASS|FAIL"
  }},
  "overall_result": "PASS|FAIL",
  "summary": "brief explanation"
}}
""".strip()


def evaluate(generated_content: str, source_docs: dict[str, Any], channel: str) -> dict[str, Any]:
    """Call the Anthropic judge model and parse a structured compliance evaluation."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "criteria": {
                "CLAIM_ACCURACY": "FAIL",
                "SAFETY_DISCLOSURES": "FAIL",
                "PROHIBITED_LANGUAGE": "FAIL",
                "TONE_APPROPRIATENESS": "FAIL",
                "FACTUAL_GROUNDING": "FAIL",
            },
            "overall_result": "FAIL",
            "summary": "Anthropic API key not configured.",
        }

    client = Anthropic(api_key=api_key)
    prompt = build_rubric_prompt(generated_content, source_docs, channel)

    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=400,
            system="You are a strict pharmaceutical compliance reviewer.",
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:  # pragma: no cover - defensive guard
        raise RuntimeError(f"Compliance judge request failed: {exc}") from exc

    raw_text = "".join(block.text for block in response.content if getattr(block, "text", None))
    if not raw_text:
        raise ValueError("Compliance judge returned no content.")

    cleaned = raw_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(0))
            except json.JSONDecodeError as nested_exc:
                raise ValueError("Compliance judge response could not be parsed as JSON.") from nested_exc
        else:
            raise ValueError("Compliance judge response could not be parsed as JSON.") from exc

    if not isinstance(parsed, dict):
        raise ValueError("Compliance judge response was not a JSON object.")

    return parsed
