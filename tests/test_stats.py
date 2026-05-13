from ui_annot import stats


def _el(t, issues=None):
    return {"id": "x", "region": "middle", "type": t, "issues": issues or []}


def _iss(sev, cat):
    return {"severity": sev, "category": cat, "evidence": "observed something"}


def test_summary_empty():
    assert stats.summarize([]) == {"total_tasks": 0}


def test_summary_basic():
    recs = [
        {"task_id": "1", "screenshot": "x", "rater": "l", "elements": [
            _el("button", [_iss("HIGH", "layout")]),
        ]},
    ]
    s = stats.summarize(recs)
    assert s["total_tasks"] == 1
    assert s["total_issues"] == 1
