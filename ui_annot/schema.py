"""JSON schema for annotation records."""

REGIONS = ["top-left", "top-center", "top-right",
           "middle-left", "middle", "middle-right",
           "bottom-left", "bottom-center", "bottom-right"]
ELEMENT_TYPES = ["button", "input", "dropdown", "nav", "header", "footer",
                 "table", "card", "modal", "error", "image", "icon", "link", "text", "other"]
SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
ISSUE_CATEGORIES = ["layout", "label_mismatch", "accessibility",
                    "state_inconsistency", "spacing", "color_contrast",
                    "broken_link", "missing_element", "other"]

ANNOTATION_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["task_id", "screenshot", "rater", "elements"],
    "properties": {
        "task_id": {"type": "string"},
        "screenshot": {"type": "string"},
        "rater": {"type": "string"},
        "elements": {"type": "array"},
    },
}
