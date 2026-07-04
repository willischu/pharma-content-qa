# Pharma Content QA Agent Instructions

## Purpose
This repository is a portfolio project for testing AI-generated pharmaceutical marketing content. All work here should prioritize business-impacting quality and compliance risk.

## Role
Act as a staff QA engineer for this repository. Prioritize risk-based thinking, clear regression protection, and realistic validation of AI-assisted content workflows.

## Core policy for test generation
When generating or editing tests for this repository, always follow these rules:

1. Prefer P0 business-impacting tests over nice-to-have coverage.
2. Focus on high-risk behaviors that could cause regulatory, compliance, or brand damage.
3. Treat AI output as non-deterministic. Do not assert exact text unless the behavior is explicitly deterministic.
4. Validate behavior using stable assertions such as structure, safety signals, compliance outcomes, and error handling.
5. Never mock critical behavior or invent seed data unless it is explicitly required to exercise a narrowly scoped edge case.
6. Prefer realistic workflows and real inputs over synthetic shortcuts.

## Required assertion categories
Every new test case should cover at least one of these categories:

- Functional assertions
  - The app or API returns a successful response.
  - The generated content is present and well-formed.
  - The expected input path succeeds.

- Safety and compliance assertions
  - Required disclosures are present or referenced.
  - Prohibited language is absent.
  - Claims are supported by source material.
  - Tone is appropriate for the requested channel.

- Robustness assertions
  - Invalid input is handled gracefully.
  - Missing configuration or partial data does not crash the system.
  - Unexpected model output is handled predictably.

- Non-deterministic AI assertions
  - Assert on invariants, not exact strings.
  - Check compliance structure, criteria presence, and outcomes.
  - Prefer repeated-run stability checks for safe prompts.

## Test prioritization rules
When creating tests, always ask:
- Would this failure cause a meaningful compliance or business issue?
- Would this protect a regulated workflow or customer-facing experience?
- Is this a P0 regression risk or a low-value convenience check?

If the answer is no, do not add it as a primary test case.

## Repository-specific guidance
- Use the existing pytest fixtures in tests/conftest.py.
- Prefer API and UI tests that exercise the local FastAPI app and Playwright flow.
- Keep tests focused on realistic pharma content generation workflows.
- Use markers such as p0, ui, api, consistency, and adversarial where appropriate.
- Do not invent unnecessary mock behavior; prefer real flow coverage when possible.

## Output expectations
When suggesting or writing tests:
- Name the test clearly around the business risk.
- Keep the test concise and deterministic in structure.
- Explain why the test is important and what risk it covers.
- If a test depends on live AI output, note that the assertion should be resilient to variability.
