from ui_annot import stats


VALID = {
    "task_id": "t1", "screenshot": "x.png", "rater": "laela",
    "elements": [
        {"id": "el_1", "region": "top-right", "type": "button", "label": "Save",
         "issues": [{"severity": "MEDIUM", "category": "layout",
                     "evidence": "Save sits 6-8 px below Cancel.",
                     "inference": "vertical misalignment"}]}
    ],
}


def test_valid_record_passes():
    assert stats.validate([VALID]) == []


def test_unknown_region_fails():
    bad = {**VALID,
           "elements": [{**VALID["elements"][0], "region": "outer-space"}]}
    errors = stats.validate([bad])
    assert any("region" in e["path"] for e in errors)


def test_unknown_severity_fails():
    bad_issue = {**VALID["elements"][0]["issues"][0], "severity": "URGENT"}
    bad_el = {**VALID["elements"][0], "issues": [bad_issue]}
    bad = {**VALID, "elements": [bad_el]}
    errors = stats.validate([bad])
    assert any("severity" in e["message"] or "severity" in e["path"]
               for e in errors)


def test_short_evidence_fails():
    bad_issue = {**VALID["elements"][0]["issues"][0], "evidence": "x"}
    bad_el = {**VALID["elements"][0], "issues": [bad_issue]}
    bad = {**VALID, "elements": [bad_el]}
    errors = stats.validate([bad])
    assert any("evidence" in e["path"] for e in errors)


def test_missing_rater_fails():
    bad = {k: v for k, v in VALID.items() if k != "rater"}
    errors = stats.validate([bad])
    assert any("rater" in e["message"] for e in errors)
