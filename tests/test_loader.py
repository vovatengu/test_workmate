from __future__ import annotations

import csv
from pathlib import Path

import pytest

from src.loader import FileLoadError, load_csv_files


def test_load_csv_files_success(csv_file_content: str) -> None:
    data = load_csv_files([csv_file_content])
    assert len(data) == 1
    assert data[0]["title"] == "Test Vid"
    assert isinstance(data[0]["ctr"], float)
    assert isinstance(data[0]["retention_rate"], float)


def test_load_csv_files_not_found() -> None:
    with pytest.raises(FileLoadError, match="Файл не найден"):
        load_csv_files(["non_existent_file.csv"])


@pytest.mark.parametrize(
    ("ctr", "retention", "expected_count"),
    [
        ("18.5", "30.0", 1),
        ("not-a-number", "30.0", 0),
        ("18.5", "bad", 0),
        ("", "", 0),
    ],
    ids=["valid", "bad-ctr", "bad-retention", "empty"],
)
def test_load_csv_skips_invalid_rows(
    tmp_path: Path,
    ctr: str,
    retention: str,
    expected_count: int,
) -> None:
    file_path = tmp_path / "data.csv"
    fieldnames = ["title", "ctr", "retention_rate", "views", "likes", "avg_watch_time"]
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "title": "X",
                "ctr": ctr,
                "retention_rate": retention,
                "views": "1",
                "likes": "1",
                "avg_watch_time": "1.0",
            }
        )

    result = load_csv_files([str(file_path)])
    assert len(result) == expected_count


def test_load_csv_files_merges_multiple(tmp_path: Path, csv_file_content: str) -> None:
    second = tmp_path / "second.csv"
    fieldnames = ["title", "ctr", "retention_rate", "views", "likes", "avg_watch_time"]
    with open(second, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "title": "Other",
                "ctr": "5.0",
                "retention_rate": "70.0",
                "views": "10",
                "likes": "1",
                "avg_watch_time": "2.0",
            }
        )

    data = load_csv_files([csv_file_content, str(second)])
    assert len(data) == 2
    assert {row["title"] for row in data} == {"Test Vid", "Other"}
