"""JSON schema for annotation records."""
from __future__ import annotations

REGIONS = [
    "top-left", "top-center", "top-right",
    "middle-left", "middle", "middle-right",
    "bottom-left", "bottom-center", "bottom-right",
    "full-width",
]
ELEMENT_TYPES = [
    "button", "input", "dropdown", "checkbox", "radio",
    "nav", "header", "footer", "table", "card", "modal",
    "error", "tooltip", "image", "icon", "link", "text", "other",
]
SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
ISSUE_CATEGORIES = [
    "layout", "label_mismatch", "accessibility",
    "state_inconsistency", "data_problem", "spacing",
    "color_contrast", "broken_link", "missing_element",
    "duplicate_element", "other",
]

ANNOTATION_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "UI Annotation Record",
    "type": "object",
    "required": ["task_id", "screenshot", "rater", "elements"],
    "properties": {
        "task_id": {"type": "string"},
        "screenshot": {"type": "string"},
        "rater": {"type": "string"},
        "elements": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "region", "type"],
                "properties": {
                    "id": {"type": "string"},
                    "region": {"type": "string", "enum": REGIONS},
                    "type": {"type": "string", "enum": ELEMENT_TYPES},
                    "label": {"type": ["string", "null"]},
                    "issues": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["severity", "category", "evidence"],
                            "properties": {
                                "severity": {"type": "string", "enum": SEVERITIES},
                                "category": {"type": "string", "enum": ISSUE_CATEGORIES},
                                "evidence": {"type": "string", "minLength": 5},
                                "inference": {"type": ["string", "null"]},
                            },
                        },
                    },
                },
            },
        },
    },
}
