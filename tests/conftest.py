from __future__ import annotations

import csv
from pathlib import Path

import pytest


@pytest.fixture
def sample_data() -> list[dict[str, object]]:
    return [
        {"title": "Video A", "ctr": 18.2, "retention_rate": 35.0, "views": 100},
        {"title": "Video B", "ctr": 10.0, "retention_rate": 30.0, "views": 200},
        {"title": "Video C", "ctr": 20.0, "retention_rate": 50.0, "views": 300},
        {"title": "Video D", "ctr": 25.0, "retention_rate": 20.0, "views": 400},
    ]


@pytest.fixture
def csv_file_content(tmp_path: Path) -> str:
    file_path = tmp_path / "test.csv"
    rows = [
        {
            "title": "Test Vid",
            "ctr": "18.5",
            "retention_rate": "30.0",
            "views": "100",
            "likes": "10",
            "avg_watch_time": "5.0",
        }
    ]
    fieldnames = ["title", "ctr", "retention_rate", "views", "likes", "avg_watch_time"]
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return str(file_path)
