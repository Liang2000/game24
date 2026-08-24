from game24.storage import append_record, load_records


def _rec(timestamp, level=1, score=8, passed=True, duration=60.0):
    return {
        "timestamp": timestamp,
        "level": level,
        "score": score,
        "passed": passed,
        "duration": duration,
    }


def test_append_then_load_roundtrip(tmp_path):
    p = tmp_path / "records.json"
    rec = _rec("2026-08-24T10:00:00")
    append_record(p, rec)
    assert load_records(p) == [rec]


def test_missing_file_returns_empty(tmp_path):
    assert load_records(tmp_path / "nope.json") == []


def test_auto_creates_file_and_dir(tmp_path):
    p = tmp_path / "sub" / "dir" / "records.json"
    append_record(p, _rec("2026-08-24T10:00:00"))
    assert p.exists()


def test_sorted_by_timestamp(tmp_path):
    p = tmp_path / "records.json"
    append_record(p, _rec("2026-08-24T12:00:00", level=2, score=9))
    append_record(p, _rec("2026-08-24T09:00:00", level=1, score=8))
    records = load_records(p)
    assert [r["timestamp"] for r in records] == [
        "2026-08-24T09:00:00",
        "2026-08-24T12:00:00",
    ]


def test_corrupted_file_returns_empty(tmp_path):
    p = tmp_path / "records.json"
    p.write_text("{not valid json", encoding="utf-8")
    assert load_records(p) == []
