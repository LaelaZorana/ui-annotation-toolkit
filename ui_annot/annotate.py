"""Interactive annotation prompts."""
from __future__ import annotations

from .schema import REGIONS, ELEMENT_TYPES, SEVERITIES, ISSUE_CATEGORIES


def _menu(prompt: str, options: list[str]) -> str:
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"  {i:2d}. {opt}")
    while True:
        raw = input("Choice (number): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("  Invalid choice.")


def _yes(prompt: str) -> bool:
    return input(f"{prompt} (y/n): ").strip().lower() in {"y", "yes"}


def annotate_task(task: dict, rater: str) -> dict:
    """Walk through a task interactively, collecting structured annotations."""
    print("\n" + "=" * 70)
    print(f"Task: {task.get('task_id', '?')}")
    print(f"Screenshot: {task.get('screenshot', '?')}")
    if task.get("notes"):
        print(f"Notes: {task['notes']}")
    print("-" * 70)
    print("Open the screenshot in Preview/your image viewer alongside this terminal.")

    elements: list[dict] = []
    el_idx = 1
    while True:
        if not _yes(f"\nAdd UI element #{el_idx}?"):
            break
        region = _menu("Region:", REGIONS)
        etype = _menu("Element type:", ELEMENT_TYPES)
        label = input("Label/text on the element (Enter for none): ").strip() or None

        issues: list[dict] = []
        iss_idx = 1
        while _yes(f"  Add issue #{iss_idx} for this element?"):
            severity = _menu("  Severity:", SEVERITIES)
            category = _menu("  Category:", ISSUE_CATEGORIES)
            evidence = input("  Evidence (what you observe, not what you think): ").strip()
            while len(evidence) < 5:
                evidence = input("  Too short — give a real observation: ").strip()
            inference = input("  Inference (optional — what this might mean): ").strip() or None
            issues.append({
                "severity": severity,
                "category": category,
                "evidence": evidence,
                "inference": inference,
            })
            iss_idx += 1

        elements.append({
            "id": f"el_{el_idx}",
            "region": region,
            "type": etype,
            "label": label,
            "issues": issues,
        })
        el_idx += 1

    return {
        "task_id": task.get("task_id"),
        "screenshot": task.get("screenshot"),
        "rater": rater,
        "elements": elements,
    }
