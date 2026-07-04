"""Report generation helpers for QA test results."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any


def generate_report(test_results: list[dict[str, Any]], output_dir: str = "reports/") -> str:
    """Write a timestamped markdown summary of a batch of test results."""
    os.makedirs(output_dir, exist_ok=True)

    passed = sum(1 for result in test_results if result.get("pass"))
    total = len(test_results)
    pass_rate = round((passed / total) * 100, 1) if total else 0.0

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"test_run_{timestamp}.md")

    lines: list[str] = []
    lines.append("# Test Run Summary")
    lines.append("")
    lines.append(f"- Passed: {passed}/{total}")
    lines.append(f"- Pass Rate: {pass_rate}%")
    lines.append("")

    for result in test_results:
        lines.append(f"## {result.get('scenario_id', 'scenario')}")
        lines.append("")
        lines.append(f"**Prompt**: {result.get('prompt', '')}")
        lines.append("")
        lines.append(f"**Generated Content**: {str(result.get('generated_content', ''))[:200]}")
        lines.append("")
        lines.append(f"**Result**: {'PASS' if result.get('pass') else 'FAIL'}")
        evaluation = result.get("evaluation", {})
        if evaluation:
            lines.append(f"**Evaluation**: {evaluation}")
        failures = result.get("failures") or []
        if failures:
            lines.append("**Failures**:")
            for failure in failures:
                lines.append(f"- {failure}")
        lines.append("")

    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    return report_path
