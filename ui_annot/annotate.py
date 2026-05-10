"""Interactive annotation prompts."""
from .schema import REGIONS, ELEMENT_TYPES


def _menu(prompt, options):
    print(prompt)
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        raw = input("Choice: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]


def _yes(p):
    return input(f"{p} (y/n): ").strip().lower() in {"y", "yes"}


def annotate_task(task, rater):
    elements = []
    i = 1
    while _yes(f"Add element #{i}?"):
        region = _menu("Region:", REGIONS)
        etype = _menu("Type:", ELEMENT_TYPES)
        label = input("Label (Enter to skip): ").strip() or None
        elements.append({"id": f"el_{i}", "region": region, "type": etype, "label": label, "issues": []})
        i += 1
    return {"task_id": task.get("task_id"), "screenshot": task.get("screenshot"),
            "rater": rater, "elements": elements}
