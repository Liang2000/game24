"""本地 JSON 成绩记录存储（高光时刻数据）。"""
import json
import os
from pathlib import Path


def default_path() -> Path:
    """返回成绩记录的默认存储位置。"""
    base = os.environ.get("APPDATA")
    if base:
        return Path(base) / "game24" / "records.json"
    return Path.home() / ".game24" / "records.json"


def load_records(path):
    """读取记录，按时间戳升序返回；文件不存在或损坏时返回空列表。"""
    p = Path(path)
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    records = [r for r in data if isinstance(r, dict)]
    records.sort(key=lambda r: r.get("timestamp", ""))
    return records


def append_record(path, record):
    """追加一条记录，自动创建目录与文件。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    records = load_records(p)
    records.append(record)
    records.sort(key=lambda r: r.get("timestamp", ""))
    p.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
