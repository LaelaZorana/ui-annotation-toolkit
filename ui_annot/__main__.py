"""CLI: annotate / summary / validate"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import annotate as annotate_mod
from . import stats as stats_mod


def _read_jsonl(path: Path) -> list[dict]:
    out: list[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"{path} line {i}: invalid JSON: {e}") from e
    return out


def _append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def cmd_annotate(args) -> int:
    out = args.out
    already = set()
    if out.exists():
        already = {r["task_id"] for r in _read_jsonl(out)}
        print(f"Resuming — {len(already)} tasks already annotated.")

    n = 0
    try:
        for task in _read_jsonl(args.tasks):
            if task.get("task_id") in already:
                continue
            rec = annotate_mod.annotate_task(task, args.rater)
            _append_jsonl(out, rec)
            n += 1
    except KeyboardInterrupt:
        print(f"\nStopped. Annotated {n} task(s) this session.")
        return 0

    print(f"\nDone. Annotated {n} task(s) → {out}")
    return 0


def cmd_summary(args) -> int:
    recs = _read_jsonl(args.annotations)
    s = stats_mod.summarize(recs)
    print(json.dumps(s, indent=2))
    return 0


def cmd_validate(args) -> int:
    recs = _read_jsonl(args.annotations)
    errors = stats_mod.validate(recs)
    if not errors:
        print(f"OK — {len(recs)} record(s), no validation errors.")
        return 0
    print(f"FAIL — {len(errors)} error(s):")
    for e in errors:
        print(f"  [{e['task_id']}] {e['path']}: {e['message']}")
    return 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="ui_annot")
    sub = p.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("annotate", help="Interactively annotate screenshots")
    pa.add_argument("tasks", type=Path)
    pa.add_argument("--rater", required=True)
    pa.add_argument("--out", required=True, type=Path)

    ps = sub.add_parser("summary", help="Roll-up stats over annotations")
    ps.add_argument("annotations", type=Path)

    pv = sub.add_parser("validate", help="Validate annotations against schema")
    pv.add_argument("annotations", type=Path)

    args = p.parse_args(argv)
    if args.cmd == "annotate":
        return cmd_annotate(args)
    if args.cmd == "summary":
        return cmd_summary(args)
    if args.cmd == "validate":
        return cmd_validate(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
