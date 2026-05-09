"""JSON schema for annotation records."""

REGIONS = ["top", "middle", "bottom", "left", "right"]
ELEMENT_TYPES = ["button", "input", "dropdown", "nav", "header",
                 "table", "modal", "other"]
SEVERITIES = ["HIGH", "MEDIUM", "LOW"]
ISSUE_CATEGORIES = ["layout", "label_mismatch", "other"]

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
