# Pharma Content QA

I built this project as a practical QA framework for testing AI-generated pharmaceutical marketing content. It shows how I set up a simple end-to-end workflow for validating content safety, compliance, and business risk.

## Why I built it

I did not have prior experience testing LLM prompts, so I built this project as a hands-on way to learn the difference between traditional deterministic testing and the probabilistic nature of AI output. In a typical software test, I can rely on a fixed expectation. With AI-generated content, the output can vary, so I had to shift my mindset toward testing for safety, structure, and business rules rather than one exact response. This project helped me learn that approach by building a framework around compliance checks, PASS/FAIL outcomes, and realistic review criteria.

## How I set up the framework

I structured the project in a simple flow:

1. I provide a prompt, a drug, and a channel in the app.
2. The app generates marketing content.
3. I use a compliance judge to review that content against a small set of business rules.
4. I validate the result with clear PASS/FAIL checks.

This gives me a clean way to show how I approach AI testing in a real-world, high-risk setting.

## What I am validating

The tests in this repository are designed around the following business requirements:

- Claim accuracy: any benefit or efficacy claim must be supported by approved source material.
- Safety disclosures: required warnings or prescribing information must be present or referenced.
- Prohibited language: terms such as guaranteed or miracle should not appear.
- Channel fit: the tone should be appropriate for the selected channel.
- Factual grounding: the content should stay within the approved information provided.

If any of these checks fail, I treat the content as a meaningful compliance risk.

## What the compliance judge does

I use the compliance judge in [utils/compliance_judge.py](utils/compliance_judge.py) to review the generated content and return a structured assessment. It looks at the content, the selected channel, and the source information provided to the system.

It returns:

- a result for each key area: claim accuracy, safety disclosures, prohibited language, tone, and factual grounding
- an overall PASS or FAIL result
- a short explanation of the decision

That gives me a reliable way to validate safety and compliance without depending on one exact wording.

## Source documents

The source_docs input provides the approved background information for the generation and review process. It can include items such as:

- approved claims
- required disclosures
- prohibited language

These inputs help me keep the content within approved boundaries and give the judge something concrete to review.

## How I write the tests

I focus the tests on business outcomes rather than exact wording. A strong test in this project checks that:

- the request succeeds
- content is generated
- the judge returns the expected structure
- the relevant criteria are marked PASS or FAIL
- the overall result is appropriate for the scenario

In short, I am using these tests to protect the business and the audience, not to match one specific sentence.

## Tech stack

Python, FastAPI, Playwright, pytest, Anthropic API, and httpx.

## How to run the test and generate a report

From the project root, I run the UI test with:

```bash
./.venv/bin/python -m pytest -q tests/ui/test_generate_flow.py
```

Pytest now handles the reporting workflow automatically:

- it generates the HTML report at [reports/test_report.html](reports/test_report.html)
- it writes a markdown summary at [reports/test_summary.md](reports/test_summary.md)
- it shows the pass/fail result in the terminal

If I want to overwrite the summary and report on a later run, I can set:

```bash
RUN_REPORT=1 ./.venv/bin/python -m pytest -q tests/ui/test_generate_flow.py
```

## How to view the report and summary

- Open [reports/test_report.html](reports/test_report.html) in a browser to view the full HTML report.
- Open [reports/test_summary.md](reports/test_summary.md) to review a simple written summary of the latest run.

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
