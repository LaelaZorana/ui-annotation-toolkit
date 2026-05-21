# ui-annotation-toolkit

A small CLI for **annotating software screenshots** — the kind of task that shows up in AI training pipelines that need labelled UI data (dashboards, admin panels, CRMs, web apps) or in old-fashioned UX/QA review work where you walk through a screen and flag what's wrong with it.

I built this because I was doing a bunch of UI review tasks where I'd open a screenshot in Preview, write a Google Doc with "the *Save* button on the orders dashboard isn't aligned with the *Cancel* button, also the field label says 'Phone' but the placeholder is for an email…" and then realise three days later that my notes weren't structured enough to compare across screenshots. So I made the structure explicit.

## What it does

Given a folder of screenshots and a JSONL of annotation tasks, the CLI walks you through each screenshot in order and lets you record:

- **UI elements** you see, by rough region (`top-left`, `top-right`, `middle`, `bottom-left`, `bottom-right`, etc.) and type (`button`, `input`, `dropdown`, `nav`, `header`, `table`, `modal`, `error`, `other`)
- **Issues** with each element, tagged by severity (`CRITICAL` / `HIGH` / `MEDIUM` / `LOW`) and category (`layout`, `label_mismatch`, `accessibility`, `state_inconsistency`, `data_problem`, `other`)
- **Observations vs inferences** — every issue has an `evidence` field forcing you to say *what you see* before saying *what you think it means*. This is the difference between a useful annotation and an opinion.

Output is JSONL — one record per screenshot, with all annotations attached. A `summary` command rolls up counts by element type, severity, and category.

## Quick start

```bash
pip install -r requirements.txt
python -m ui_annot annotate examples/sample_tasks.jsonl --rater laela --out my_annotations.jsonl

# Summary over your annotations
python -m ui_annot summary my_annotations.jsonl

# Validate an annotations file against the JSON schema
python -m ui_annot validate my_annotations.jsonl
```

## Example annotation record

```json
{
  "task_id": "scr_orders_001",
  "screenshot": "examples/screenshots/orders_dashboard.png",
  "rater": "laela",
  "elements": [
    {"id": "el_1", "region": "top-right", "type": "button", "label": "Save",
     "issues": [
       {"severity": "MEDIUM", "category": "layout",
        "evidence": "Save button sits 6-8 px lower than the Cancel button to its left.",
        "inference": "Vertical misalignment will read as inconsistent design quality."}
     ]},
    {"id": "el_2", "region": "middle", "type": "input", "label": "Phone",
     "issues": [
       {"severity": "HIGH", "category": "label_mismatch",
        "evidence": "Label reads 'Phone' but placeholder text reads 'name@example.com'.",
        "inference": "Field is likely an email input mislabelled, or a phone input with the wrong placeholder."}
     ]}
  ]
}
```

## Why the evidence/inference split

Three years of compliance training reviews taught me that the most expensive QC mistakes are when a reviewer writes down their conclusion ("the button is broken") without writing down what they observed ("the button does not respond to clicks in the screenshot, though the cursor changes to a pointer on hover"). Forcing the two fields apart catches my own confirmation bias.

## Project layout

```
ui_annot/
  __main__.py        CLI
  annotate.py        the interactive prompt UX
  schema.py          JSON schema for annotation records
  stats.py           summary / validation
tests/
examples/
  sample_tasks.jsonl    3 toy tasks for testing
```

## License

MIT.
