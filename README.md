# Pharma Content QA

AI Content Compliance Test Framework — a QA testing framework for validating AI-generated pharmaceutical marketing content against regulatory compliance standards.

## Why this exists

Testing non-deterministic AI systems in regulated industries is difficult because correctness is not a single fixed output. When AI-generated marketing content varies from run to run, traditional assertion-based tests such as asserting exactly one string is insufficient and can miss critical compliance failures with real-world consequences.

## Architecture

The framework uses a two-layer approach. First, Playwright E2E tests exercise the UI and capture generated content end to end. Second, an LLM-as-judge evaluates the captured content against a compliance rubric that checks claim accuracy, required disclosures, prohibited language, tone, and factual grounding. Both layers share the same evaluation engine through pytest fixtures.

## Test categories

Planned test categories include E2E compliance checks, consistency and non-determinism tests, adversarial prompt injection defenses, and evaluation calibration tests.

## Tech stack

Python, FastAPI, Playwright, pytest, Anthropic API, and httpx.

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and add your Anthropic API key.
5. Install Playwright browsers with `playwright install`.
6. Start the app with `uvicorn app.main:app --reload`.
7. Run tests with `pytest`.

## Project structure

```text
pharma-content-qa/
├── app/                # FastAPI app and UI routes
├── utils/              # Compliance judge and markdown report generator
├── fixtures/           # Golden dataset JSON files added by the user
├── reports/            # Generated markdown and HTML reports
├── tests/              # Pytest fixtures and future UI/API tests
├── .env.example        # Template environment file
├── .gitignore          # Standard Python ignore rules
├── pytest.ini          # Pytest configuration and markers
├── requirements.txt    # Python dependencies
└── README.md           # Project overview
```
