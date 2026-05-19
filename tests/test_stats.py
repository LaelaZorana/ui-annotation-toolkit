from ui_annot import stats


def _el(t, issues=None):
    return {"id": "x", "region": "middle", "type": t, "issues": issues or []}


def _iss(sev, cat):
    return {"severity": sev, "category": cat,
            "evidence": "observed something", "inference": None}


def test_summary_empty():
    assert stats.summarize([]) == {"total_tasks": 0}


def test_summary_basic():
    recs = [
        {"task_id": "1", "screenshot": "x", "rater": "l", "elements": [
            _el("button", [_iss("HIGH", "layout"), _iss("LOW", "spacing")]),
            _el("input", [_iss("MEDIUM", "label_mismatch")]),
            _el("nav", []),
        ]},
        {"task_id": "2", "screenshot": "y", "rater": "l", "elements": [
            _el("button", [_iss("CRITICAL", "broken_link")]),
        ]},
    ]
    s = stats.summarize(recs)
    assert s["total_tasks"] == 2
    assert s["total_elements"] == 4
    assert s["total_issues"] == 4
    assert s["elements_with_no_issues"] == 1
    assert s["by_element_type"]["button"] == 2
    assert s["by_severity"]["HIGH"] == 1
    assert s["by_severity"]["CRITICAL"] == 1
    assert s["by_category"]["layout"] == 1
