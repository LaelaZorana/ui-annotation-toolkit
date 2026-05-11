"""Summary stats and validation."""
from __future__ import annotations

from collections import Counter

from jsonschema import Draft7Validator

from .schema import ANNOTATION_SCHEMA


def summarize(records: list[dict]) -> dict:
    """Compute roll-up stats across a batch of annotation records."""
    if not records:
        return {"total_tasks": 0}

    elem_types: Counter = Counter()
    severities: Counter = Counter()
    categories: Counter = Counter()
    issues_per_screenshot: list[int] = []
    elements_with_no_issues = 0

    for rec in records:
        n_issues = 0
        for el in rec.get("elements", []):
            elem_types[el.get("type", "other")] += 1
            if not el.get("issues"):
                elements_with_no_issues += 1
            for iss in el.get("issues", []) or []:
                severities[iss.get("severity", "LOW")] += 1
                categories[iss.get("category", "other")] += 1
                n_issues += 1
        issues_per_screenshot.append(n_issues)

    return {
        "total_tasks": len(records),
        "total_elements": sum(elem_types.values()),
        "total_issues": sum(severities.values()),
        "elements_with_no_issues": elements_with_no_issues,
        "by_element_type": dict(elem_types.most_common()),
        "by_severity": dict(severities.most_common()),
        "by_category": dict(categories.most_common()),
        "mean_issues_per_screenshot":
            round(sum(issues_per_screenshot) / len(issues_per_screenshot), 2)
            if issues_per_screenshot else 0,
    }


def validate(records: list[dict]) -> list[dict]:
    """Return a list of validation errors. Empty list means all records valid."""
    validator = Draft7Validator(ANNOTATION_SCHEMA)
    errors = []
    for i, rec in enumerate(records):
        for err in validator.iter_errors(rec):
            errors.append({
                "task_index": i,
                "task_id": rec.get("task_id", "?"),
                "path": ".".join(str(p) for p in err.path) or "<root>",
                "message": err.message,
            })
    return errors
