"""Wrapper around the Anthropic API for content generation."""

import os
from typing import Any

from anthropic import Anthropic

MODEL_NAME = "claude-haiku-4-5-20251001"


def generate_content(prompt: str, drug_name: str, channel: str, source_docs: dict[str, Any]) -> str:
    """Generate content using the Anthropic API while enforcing a compliance-oriented system prompt."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return (
            "[Placeholder response] Configure ANTHROPIC_API_KEY to enable live generation. "
            f"Prompt: {prompt} | Drug: {drug_name} | Channel: {channel}"
        )

    client = Anthropic(api_key=api_key)
    system_prompt = (
        "You are a pharmaceutical marketing content writer. "
        "Create content that uses only approved claims, references required safety disclosures, "
        "and avoids prohibited language. Keep the tone appropriate for the requested channel "
        "and regulated pharmaceutical marketing."
    )

    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=400,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Drug: {drug_name}\n"
                        f"Channel: {channel}\n"
                        f"Source docs: {source_docs}\n"
                        f"User prompt: {prompt}"
                    ),
                }
            ],
        )
    except Exception as exc:  # pragma: no cover - defensive guard
        return f"[Generation error] {exc}"

    if not response.content:
        return "[Generation error] Anthropic returned no content."

    return "".join(block.text for block in response.content if getattr(block, "text", None))
